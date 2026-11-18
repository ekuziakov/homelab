# Hermes

Personal AI agent: `https://hermes.home.hexmelt.com` (dashboard port `9119`).

## Run

Requires the `homelab` network, `hermes_data`, and Hindsight for memory.
Settings come from `data/config.yaml`; credentials come from the gitignored
`data/.env` file. Both files and the `shared/` directory must exist before starting.
From this directory:

```bash
docker compose up -d
```

## Storage
Prowlarr API access uses `http://prowlarr-prowlarr-1:9696` on the shared `homelab` network,
bypassing the outbound proxy. Set `PROWLARR_API_KEY` in `data/.env` using the key from
Prowlarr Settings → General. Never commit the key.

- `hermes_data` → `/opt/data`: sessions, skills, and agent state.
- `data/config.yaml` → `/opt/data/config.yaml`: Git-managed settings.
- `data/.env` → `/opt/data/.env`: writable credentials file (not tracked by Git).
- `data/.env.example` → `/opt/data/.env.example`: read-only credentials template.
- `/Volumes/SSD1/homelab` → `/mounts/homelab`: writable repository access.
- `shared/` → `/mounts/shared`: read/write file exchange with Hermes. On the host:
  `/Volumes/SSD1/homelab/hermes/shared`. Contents are excluded from Git.

After changing mounts, run `docker compose up -d --no-deps hermes` on the Docker host
to recreate the container. File exchange is also accessible through the repository
mount at `/mounts/homelab/hermes/shared`.

Back up the volume, `shared/`, and `data/.env` consistently and protect credentials.
Hindsight memory requires a separate backup of its own volume.
