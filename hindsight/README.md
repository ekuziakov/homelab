# Hindsight

Memory service with embedded PostgreSQL. Web UI: `https://hindsight.home.hexmelt.com`.
Local API: `http://127.0.0.1:8888`.

## Run

Configure `.env` using `.env.example`. The `homelab` network and
`hindsight_hindsight-data` volume must already exist. From this directory,
authorize ChatGPT on first use or when reauthorization is needed:

```bash
docker compose run --rm --service-ports hindsight-login
docker compose up -d hindsight
```

Open the printed login URL on the same Mac; port `1455` must be free.
For normal startup, run only the second command.

The API requires a Bearer `HINDSIGHT_API_KEY`. Hermes uses
`http://hindsight-hindsight-1:8888` with the same key; keep this hostname in
Hermes `NO_PROXY`. The UI has no separate login; access to Caddy must stay restricted.

## Storage

- `hindsight_hindsight-data` → `/home/hindsight/.pg0`: database and OAuth credentials.
- `login.py` → `/app/chatgpt-login.py`: read-only OAuth helper.

Use a consistent PostgreSQL backup and protect both the volume and `.env`.
Copying this directory does not include the database or OAuth credentials.
