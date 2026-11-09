# Zerobyte

Restic backup UI at http://localhost:4096. Requires the external `homelab`
network and an existing Hindsight volume. Run commands on the Mac.

## Setup

Keep the existing `.env`. On a fresh clone, copy `.env.example` to `.env`,
set `APP_SECRET` using `openssl rand -hex 32`, and run `chmod 600 .env`.
Set `HINDSIGHT_VOLUME_NAME` if the volume has a different name.

Verify SSD1 is mounted before creating the repository directory:

```bash
cd /Volumes/SSD1/homelab/zerobyte
diskutil info /Volumes/SSD1
# Continue only after confirming the correct disk.
mkdir -p /Volumes/SSD1/backups/zerobyte
docker volume inspect hindsight_hindsight-data
docker compose config --quiet
docker compose up -d
```

Create an admin account in the UI, then configure:

| Type | Container path |
| --- | --- |
| Directory source | `/sources/homelab` |
| Directory source | `/sources/hindsight` |
| Local repository | `/repositories/homelab` |

Create jobs and retention rules in the UI; Compose does not configure them.
Store repository credentials separately from SSD1.

## Backup safety

- Exclude `/sources/homelab/zerobyte/data`; back up Zerobyte state separately
  with a consistent copy. Its settings are otherwise not protected.
- Database dumps and container shutdown are not configured. Do not schedule raw
  backups of running PostgreSQL or SQLite databases without consistency handling.
  Keep Immich database and library backups consistent with each other.
- Sources are read-only. Restore to a separate writable directory or volume
  and test recovery. External photos are not mounted.
- The repository is on SSD1 at `/Volumes/SSD1/backups/zerobyte`. Run the existing
  SSD1-to-Backup01 rsync only after backup and maintenance jobs finish; verify
  both disks before using `--delete`.

Runtime, job execution, and restore verification must be performed on the Mac.
