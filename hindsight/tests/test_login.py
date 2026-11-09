"""Exercise the Docker OAuth callback relay using real local sockets."""

import asyncio
import importlib.util
from pathlib import Path
import unittest


LOGIN = Path(__file__).resolve().parents[1] / "login.py"


class LoginTests(unittest.IsolatedAsyncioTestCase):
    def load_login(self):
        self.assertTrue(LOGIN.is_file(), "Docker-only OAuth login helper is missing")
        spec = importlib.util.spec_from_file_location("hindsight_login", LOGIN)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    async def test_script_runs_hindsight_cli_and_returns_its_failure(self):
        import os
        import subprocess
        import sys
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            cli = Path(folder) / "hindsight-admin"
            cli.write_text(
                f"#!{sys.executable}\n"
                "import sys\n"
                "assert sys.argv[1:] == ['chatgpt', 'login', '--no-browser']\n"
                "raise SystemExit(7)\n"
            )
            cli.chmod(0o700)
            env = dict(os.environ, PATH=folder + os.pathsep + os.environ["PATH"])
            result = await asyncio.to_thread(
                subprocess.run, [sys.executable, str(LOGIN)],
                env=env, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 7, result.stderr)
            self.assertEqual(result.stdout, "")

    async def test_login_propagates_the_real_cli_exit_code(self):
        import sys
        login = self.load_login()
        self.assertTrue(hasattr(login, "run_login"), "CLI lifecycle is not implemented")
        result = await asyncio.wait_for(
            login.run_login(
                command=(sys.executable, "-c", "raise SystemExit(7)"),
                relay_host="127.0.0.1", relay_port=0,
            ),
            timeout=5,
        )
        self.assertEqual(result, 7)

    async def test_cancelled_login_terminates_its_child(self):
        import os
        import sys
        import tempfile
        login = self.load_login()
        with tempfile.TemporaryDirectory() as folder:
            pid_file = Path(folder) / "child.pid"
            command = (
                sys.executable, "-c",
                "import os,pathlib,time; "
                f"pathlib.Path({str(pid_file)!r}).write_text(str(os.getpid())); "
                "time.sleep(60)",
            )
            task = asyncio.create_task(login.run_login(
                command=command, relay_host="127.0.0.1", relay_port=0,
            ))
            try:
                async with asyncio.timeout(5):
                    while not pid_file.exists():
                        await asyncio.sleep(0.01)
                pid = int(pid_file.read_text())
            finally:
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await asyncio.wait_for(task, timeout=7)
            with self.assertRaises(ProcessLookupError):
                os.kill(pid, 0)

    async def test_missing_upstream_closes_connection_without_logging(self):
        import socket
        login = self.load_login()
        with socket.socket() as reserved:
            reserved.bind(("127.0.0.1", 0))
            unused_port = reserved.getsockname()[1]
        server = await asyncio.start_server(
            lambda reader, writer: login.forward_callback(reader, writer, unused_port),
            "127.0.0.1", 0,
        )
        async with server:
            reader, writer = await asyncio.open_connection(
                "127.0.0.1", server.sockets[0].getsockname()[1],
            )
            try:
                self.assertEqual(await asyncio.wait_for(reader.read(), timeout=3), b"")
            finally:
                writer.close()
                await writer.wait_closed()

    async def test_callback_request_and_response_are_forwarded_unchanged(self):
        login = self.load_login()
        received = asyncio.get_running_loop().create_future()
        request = b"GET /auth/callback?code=test-code&state=test-state HTTP/1.1\r\nHost: 127.0.0.1:1455\r\nConnection: close\r\n\r\n"
        response = b"HTTP/1.1 200 OK\r\nContent-Length: 9\r\nConnection: close\r\n\r\nsigned-in"

        async def callback(reader, writer):
            try:
                received.set_result(await reader.readuntil(b"\r\n\r\n"))
                writer.write(response)
                await writer.drain()
            finally:
                writer.close()
                await writer.wait_closed()

        upstream = await asyncio.start_server(callback, "127.0.0.1", 0)
        upstream_port = upstream.sockets[0].getsockname()[1]
        relay = await asyncio.start_server(
            lambda reader, writer: login.forward_callback(reader, writer, upstream_port),
            "127.0.0.1", 0,
        )
        async with upstream, relay:
            port = relay.sockets[0].getsockname()[1]
            reader, writer = await asyncio.open_connection("127.0.0.1", port)
            try:
                writer.write(request)
                await writer.drain()
                actual = await asyncio.wait_for(reader.read(), timeout=3)
                self.assertEqual(actual, response)
                self.assertEqual(await asyncio.wait_for(received, timeout=3), request)
            finally:
                writer.close()
                await writer.wait_closed()


if __name__ == "__main__":
    unittest.main()
