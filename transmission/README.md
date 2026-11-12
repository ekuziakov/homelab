# Transmission

BitTorrent client: `https://transmission.home.hexmelt.com` (port `9091` locally).
Internal address on `homelab`: `transmission:9091`.

## Run

Run these commands on the Mac hosting Docker/OrbStack, not inside Hermes.
Copy `.env.example` to `.env`; set `PUID` and `PGID` to the output of
`id -u` and `id -g` on the Mac. The example IDs are not auto-detected.
Set the same `PUID` and `PGID` in Transmission and Lidarr.
Media paths are fixed in Compose. Create the directories first:

```bash
mkdir -p /Volumes/SSD1/downloads/incomplete /Volumes/SSD1/downloads/complete /Volumes/SSD1/music
```

Set a strong `TRANSMISSION_PASS`; Compose refuses to start with an empty password.

The external `homelab` network must exist (`docker network create homelab`
if it has not been created). Create the external config volume once, then
run from this directory:

```bash
docker volume create transmission_config
docker compose config --quiet
docker compose up -d
```

The Caddy route is included in `../caddy/Caddyfile`. Reload Caddy after deploying
and ensure local DNS resolves `transmission.home.hexmelt.com` to the Caddy host.
Do not expose the web interface to the public Internet.

## Storage

- `transmission_config` → `/config`: persistent application configuration and database.
- `/Volumes/SSD1/downloads` → `/downloads`: downloads on the external disk.

The bind source must already exist; `create_host_path: false` prevents silent
creation of an empty source when the disk/path is missing. Verify SSD1 is actually
mounted before starting. The path is resolved on the Docker host, not in Hermes.

Back up the config volume separately; copying this service directory does not
include volume data. Keep `.env` safe and out of Git.

## First setup

Before adding downloads, set the download directory in the web UI to
`/downloads/complete`. If using an incomplete directory, set it to
`/downloads/incomplete`. Lidarr downloads may use a `lidarr` subdirectory
under the completed-download directory.

In Lidarr, add a Transmission download client with host `transmission`, port
`9091`, SSL disabled (internal network), and the credentials from this `.env`.
Use category `lidarr` to separate music downloads. No remote path mapping is
needed because both containers see exactly the same `/downloads` paths.

Port `51413` is published for TCP and UDP peers. Router forwarding, if wanted,
is a separate configuration; these files do not set up a VPN.

Image documentation: https://docs.linuxserver.io/images/docker-transmission/
