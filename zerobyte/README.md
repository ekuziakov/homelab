# Zerobyte

Backup UI: `https://zerobyte.home.hexmelt.com` (HTTPS via Caddy).
Use this URL for login; the local HTTP port is not the authenticated access URL.

## Run

Configure `.env` using `.env.example`; keep `APP_SECRET` safe.
Requires the `homelab` network and all volumes declared in Compose.
Verify SSD1 and Backup01 are mounted on the Mac. From this directory:

```bash
docker compose up -d
```

## Storage

- `zerobyte_data` → `/var/lib/zerobyte`: writable application state.
- The 17 persistent volumes marked external in their service Compose files →
  `/sources/volumes/<volume-name>`: read-only sources, including Zerobyte's own
  state. Rebuildable caches such as Immich's model cache are excluded.
- Selected `/Volumes/SSD1` folders → `/sources/ssd/<folder>`: read-only sources:
  `books`, `courses`, `docs`, `homelab`, `music`, `photos`, `projects`, `videos`.
- `/Volumes/Backup01` → `/repositories`: writable backup destination.

Create Directory sources for `/sources/volumes` and `/sources/ssd` in the UI.
Use a repository subdirectory such as `/repositories/restic`; existing rsync
copies are not moved or deleted. Update old source and repository paths before
enabling jobs. Configure schedules and retention in the UI.

Allow crossing mount points: do not enable `--one-file-system` for these sources.
Read-only mounts do not make live databases consistent. Arrange database dumps
or downtime, including a separate consistent backup of Zerobyte's own state.
