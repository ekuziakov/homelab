# iCloud Photos Downloader

One-shot, interactive iCloud photo/video download to SSD1. No web interface or
Caddy route. Run manually; this project intentionally has no restart policy or
watch loop.

> **Cloud deletion enabled:** the preserved `--keep-icloud-recent-days 30` option
> moves downloaded assets older than 30 days to iCloud Recently Deleted. This is
> not a copy-only backup. Remove that option and its value from Compose if cloud
> deletion is not intended. Live Photo video components are skipped, and files
> are stored directly in the destination (`--folder-structure none`).

## Run

Run on the Mac hosting Docker/OrbStack, not inside Hermes. Copy `.env.example`
to `.env` and check `ICLOUD_USERNAME`. Never put the Apple password or MFA code
in Compose or Git; enter them only at the interactive terminal prompts.

Verify SSD1 is mounted and the existing photo directory is writable. Create it
if needed, only after confirming the disk is mounted:

```bash
mkdir -p /Volumes/SSD1/photos/icloud
```

The external `homelab` network must exist (`docker network create homelab` if
needed). Create the external session volume once, then run from this directory:

```bash
docker volume create icloudpd_config
docker compose config --quiet
sh ./run.sh
```

`run.sh` works from any working directory. Equivalent from this directory:
`docker compose run --rm icloudpd`. Do not run concurrent downloads to the same
photo directory. First use requires Apple sign-in and may require MFA; session
expiry requires interactive authentication again.

## Storage

- `icloudpd_config` → `/config`: persistent iCloud cookies in `/config/cookies`.
- `/Volumes/SSD1/photos/icloud` → `/data`: existing downloaded originals.

The host bind path is fixed and must exist (`create_host_path: false`). It is
resolved on the Docker host, not inside Hermes. Existing photos are not moved.
Cookies persist across disposable containers; the previous configuration did not
persist them, so the first run with this configuration may require sign-in again.
Only cookies are explicitly persisted; do not assume the container's password
keyring survives removal. Protect and back up the session volume separately;
copying this service directory does not include it or the photos.

Immich already mounts `/Volumes/SSD1/photos` read-only as `/photos`; these files
are visible there at `/photos/icloud`. Scanning/indexing an external library is a
separate Immich setup step, not performed by this downloader.

Documentation: https://icloud-photos-downloader.github.io/icloud_photos_downloader/
