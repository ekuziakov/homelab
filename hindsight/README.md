# Hindsight

Memory API, web UI, and embedded PostgreSQL. Requires Docker/OrbStack and the
external `homelab` network. Run commands on the Mac.

## Setup

Keep the existing `.env`. On a fresh clone, copy `.env.example` to `.env`,
set `HINDSIGHT_API_KEY` using `openssl rand -hex 32`, and run `chmod 600 .env`.
The default `chatgpt` provider uses OAuth; it does not need an LLM API key.

```bash
cd /Volumes/SSD1/homelab/hindsight
docker compose run --rm --service-ports hindsight-login
```

Open the printed URL on the same Mac, authorize plan access, and wait for the
login container to exit. Port 1455 must be free; do not change the relay ports
independently. Repeat this command to renew authorization if needed.

```bash
docker compose up -d hindsight
docker compose exec hindsight hindsight-admin chatgpt status
```

- API: http://127.0.0.1:8888 (Bearer `HINDSIGHT_API_KEY`).
- UI: http://127.0.0.1:9999 (no separate UI login; keep it local).
- Data and OAuth: `hindsight_hindsight-data` at `/home/hindsight/.pg0`.
  The volume name changes with the Compose project name.

Back up the volume separately using a consistent PostgreSQL backup. Treat it
and `.env` as secrets. `docker compose down -v` deletes the database and OAuth.
Memory processing sends content to the configured LLM provider.

## Hermes

Use the Hindsight memory provider, not MCP: `local_external`, bank `hermes`,
URL `http://hindsight-hindsight-1:8888`. Keep this hostname in Hermes `NO_PROXY`
and set the same `HINDSIGHT_API_KEY` in `$HERMES_HOME/.env`.
If the project name changes, update the hostname and `NO_PROXY`.

For a new profile, run `hermes memory setup hindsight`. Restart Hermes if setup
requests it, then check `hermes memory status` in a new session.

## Checks

```bash
docker compose config --quiet
PYTHONDONTWRITEBYTECODE=1 python -W error -m unittest discover -s tests -v
```
