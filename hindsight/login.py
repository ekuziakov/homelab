"""Relay Docker's published callback port to Hindsight's loopback listener.

Host 127.0.0.1:1455 -> container :1456 -> container 127.0.0.1:1455.
OAuth state/PKCE and token exchange remain entirely in Hindsight's own CLI.
Never log callback URLs: they contain a one-time authorization code.
"""

import asyncio
from contextlib import suppress


async def forward_callback(reader, writer, callback_port=1455):
    upstream_writer = None
    try:
        upstream_reader, upstream_writer = await asyncio.open_connection(
            "127.0.0.1", callback_port,
        )

        async def copy(source, destination):
            while data := await source.read(65536):
                destination.write(data)
                await destination.drain()
            if destination.can_write_eof():
                destination.write_eof()

        await asyncio.gather(
            copy(reader, upstream_writer), copy(upstream_reader, writer),
        )
    except (ConnectionError, OSError):
        # The browser can probe the port before the CLI opens its listener.
        pass
    finally:
        for stream in (writer, upstream_writer):
            if stream is not None:
                stream.close()
                with suppress(ConnectionError, OSError):
                    await stream.wait_closed()


async def run_login(
    command=("hindsight-admin", "chatgpt", "login", "--no-browser"),
    *, relay_host="0.0.0.0", relay_port=1456, callback_port=1455,
):
    server = await asyncio.start_server(
        lambda reader, writer: forward_callback(reader, writer, callback_port),
        relay_host, relay_port,
    )
    async with server:
        process = await asyncio.create_subprocess_exec(*command)
        try:
            return await process.wait()
        finally:
            if process.returncode is None:
                process.terminate()
                try:
                    await asyncio.wait_for(process.wait(), timeout=5)
                except TimeoutError:
                    process.kill()
                    await process.wait()


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(run_login())
    except KeyboardInterrupt:
        exit_code = 130
    raise SystemExit(exit_code if exit_code >= 0 else 128 - exit_code)
