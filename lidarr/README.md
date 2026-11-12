# Lidarr

Music library manager: `https://lidarr.home.hexmelt.com` (port `8686` locally).
Internal address on `homelab`: `lidarr:8686`.

## Run

Run these commands on the Mac hosting Docker/OrbStack, not inside Hermes.
Copy `.env.example` to `.env`; set `PUID` and `PGID` to the output of
`id -u` and `id -g` on the Mac. The example IDs are not auto-detected.
Set the same `PUID` and `PGID` in Transmission and Lidarr.
Media paths are fixed in Compose. Create the directories first:

```bash
mkdir -p /Volumes/SSD1/downloads/incomplete /Volumes/SSD1/downloads/complete /Volumes/SSD1/music
```

The external `homelab` network must exist (`docker network create homelab`
if it has not been created). Create the external config volume once, then
run from this directory:

```bash
docker volume create lidarr_config
docker compose config --quiet
docker compose up -d
```

The Caddy route is included in `../caddy/Caddyfile`. Reload Caddy after deploying
and ensure local DNS resolves `lidarr.home.hexmelt.com` to the Caddy host.
Do not expose the web interface to the public Internet.

Outbound HTTP/HTTPS proxy: `http://host.docker.internal:7897`, matching Hermes.
Local Transmission, Prowlarr, and Lidarr addresses bypass the proxy via `NO_PROXY`.
Recreate the container with `docker compose up -d` after changing proxy variables.
Proxy configuration alone does not prove an upstream HTTP 403 is resolved.

## Storage

- `lidarr_config` → `/config`: persistent application configuration and database.
- `/Volumes/SSD1/downloads` → `/downloads`: downloads on the external disk.
- `/Volumes/SSD1/music` → `/music`: music library on the external disk.

The bind source must already exist; `create_host_path: false` prevents silent
creation of an empty source when the disk/path is missing. Verify SSD1 is actually
mounted before starting. The path is resolved on the Docker host, not in Hermes.

Back up the config volume separately; copying this service directory does not
include volume data. Keep `.env` safe and out of Git.

## First setup

- Enable authentication and set a username/password on first access.
- Add `/music` as the root folder.
- Add Transmission at `transmission:9091`, using its configured credentials,
  SSL disabled on the internal network, and category `lidarr`.
- Keep all download paths under `/downloads`; no remote path mapping is needed.
- Enable Completed Download Handling.
- Downloads and music are separate Docker mounts: expect imports to copy files,
  not hardlink or atomically move them, even though both host folders are on SSD1.
  Keep torrent data in `/downloads` while seeding; imports into `/music` may
  therefore use additional disk space.
- Add Lidarr to Prowlarr using the Lidarr API key from Settings → General.

Image documentation: https://docs.linuxserver.io/images/docker-lidarr/
