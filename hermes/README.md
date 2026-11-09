# Hermes

Personal AI agent: `https://hermes.home.hexmelt.com` (dashboard port `9119`).

## Run

Requires the `homelab` network, `hermes_data`, and Hindsight for memory.
Settings come from `data/config.yaml`; credentials live in `/opt/data/.env`
inside the volume. From this directory:

```bash
docker compose up -d
```

## Storage

- `hermes_data` → `/opt/data`: sessions, credentials, skills, and agent state.
- `data/config.yaml` → `/opt/data/config.yaml`: Git-managed settings.
- `data/.env.example` → `/opt/data/.env.example`: read-only credentials template.
- `/Volumes/SSD1/homelab` → `/mounts/homelab`: writable repository access.

Back up the volume consistently and protect its credentials. Hindsight memory
requires a separate backup of its own volume.
