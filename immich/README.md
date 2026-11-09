# Immich

Photo and video library: `https://immich.home.hexmelt.com` (port `2283` locally).

## Run

Configure `.env` using `.env.example`. The `homelab` network and external data
volumes listed below must already exist.

From this directory:

```bash
docker compose up -d
```

## Storage

- `immich_library_data` → `/data`: uploaded media and generated files.
- `immich_postgres_data` → `/var/lib/postgresql/data`: database.
- `/Volumes/SSD1/photos` → `/photos`: external originals, read-only.

Back up both data volumes and external originals. Copying this directory does
not back them up.
