# Prowlarr

Indexer manager: `https://prowlarr.home.hexmelt.com` (port `9696` locally).
Internal address on `homelab`: `prowlarr:9696`.

## Run

Run these commands on the Mac hosting Docker/OrbStack, not inside Hermes.
Copy `.env.example` to `.env`; set `PUID` and `PGID` to the output of
`id -u` and `id -g` on the Mac. The example IDs are not auto-detected.

The external `homelab` network must exist (`docker network create homelab`
if it has not been created). Create the external config volume once, then
run from this directory:

```bash
docker volume create prowlarr_config
docker compose config --quiet
docker compose up -d
```

The Caddy route is included in `../caddy/Caddyfile`. Reload Caddy after deploying
and ensure local DNS resolves `prowlarr.home.hexmelt.com` to the Caddy host.
Do not expose the web interface to the public Internet.

Outbound HTTP/HTTPS proxy: `http://host.docker.internal:7897`, matching Lidarr.
Local Transmission, Prowlarr, Lidarr, and FlareSolverr addresses bypass the proxy
via `NO_PROXY`.
Recreate the container with `docker compose up -d` after changing proxy variables.

## FlareSolverr

Deploy `../flaresolverr` for browser challenges. Add an Indexer Proxy with host
`http://flaresolverr:8191` and tag `flaresolverr`; apply the same tag only to
indexers that need it. Test and save the proxy, then test an indexer and search.
See `../flaresolverr/README.md` for deployment and limitations.

## Storage

- `prowlarr_config` → `/config`: persistent application configuration and database.

Prowlarr does not need a media-directory mount.

Back up the config volume separately; copying this service directory does not
include volume data. Keep `.env` safe and out of Git.

## First setup

- Enable authentication and set a username/password on first access.
- Add your indexers in Prowlarr.
- In Settings → Apps, add Lidarr with Prowlarr server `http://prowlarr:9696`,
  Lidarr server `http://lidarr:8686`, and the Lidarr API key from Settings → General.
- Select the desired sync level; use Full Sync if Prowlarr should manage indexers.
- Download clients belong in Lidarr; adding Transmission to Prowlarr is only
  needed for downloads initiated directly in Prowlarr.

Image documentation: https://docs.linuxserver.io/images/docker-prowlarr/
