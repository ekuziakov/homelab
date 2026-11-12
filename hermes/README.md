# Hermes

Personal AI agent: `https://hermes.home.hexmelt.com` (dashboard port `9119`).

## Run

Requires the `homelab` network, `hermes_data`, and Hindsight for memory.
Settings come from `data/config.yaml`; credentials come from the gitignored
`.env` file in this directory. Both files must exist before starting. From this directory:

```bash
docker compose up -d
```

## Storage
Prowlarr API access uses `http://prowlarr-prowlarr-1:9696` on the shared `homelab` network,
bypassing the outbound proxy. Set `PROWLARR_API_KEY` in `.env` using the key from
Prowlarr Settings → General. Never commit the key.

- `hermes_data` → `/opt/data`: sessions, skills, and agent state.
- `data/config.yaml` → `/opt/data/config.yaml`: Git-managed settings.
- `.env` → `/opt/data/.env`: writable credentials file (not tracked by Git).
- `data/.env.example` → `/opt/data/.env.example`: read-only credentials template.
- `/Volumes/SSD1/homelab` → `/mounts/homelab`: writable repository access.

Back up the volume and `.env` consistently and protect the credentials. Hindsight memory
requires a separate backup of its own volume.
