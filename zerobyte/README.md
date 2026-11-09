# Zerobyte

Backup UI: `http://localhost:4096` (local access only).

## Run

Configure `.env` using `.env.example`; keep `APP_SECRET` safe.
Requires `homelab`, `zerobyte_data`, and the Hindsight volume below.
Verify SSD1 is mounted and `/Volumes/SSD1/backups/zerobyte` exists.
From this directory:

```bash
docker compose up -d
```

Configure sources, repositories, jobs, and retention in the UI.

## Storage

- `zerobyte_data` → `/var/lib/zerobyte`: settings and application state.
- `/Volumes/SSD1/homelab` → `/sources/homelab`: read-only repository files.
- `hindsight_hindsight-data` → `/sources/hindsight`: read-only Hindsight data;
  override its volume name with `HINDSIGHT_VOLUME_NAME` in `.env` if needed.
- `/Volumes/SSD1/backups/zerobyte` → `/repositories`: backup repositories.

Other service volumes and external photos are not mounted. Arrange consistent
database dumps or downtime before backing up Hindsight. Back up Zerobyte state
separately and copy repositories to Backup01 only when backup/maintenance jobs
have finished.
