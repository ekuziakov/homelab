# FlareSolverr

Browser challenge helper for Prowlarr. Internal address: `http://flaresolverr:8191`
on the external `homelab` network. No host port or Caddy route is published.

## Run

Run on the Mac hosting Docker/OrbStack, from this directory:

```bash
docker network inspect homelab >/dev/null
docker volume create flaresolverr_config
docker compose config --quiet
docker compose up -d
docker compose ps
docker compose exec -T flaresolverr curl --fail --silent --show-error --noproxy '*' http://127.0.0.1:8191/
```

FlClash must be available at `http://host.docker.internal:7897`.
`PROXY_URL` sends browser requests through the same upstream proxy as Prowlarr.
Do not replace it with HTTP_PROXY: browser proxy configuration uses PROXY_URL.
Recreate Prowlarr from `../prowlarr` after its NO_PROXY change:

```bash
docker compose -f ../prowlarr/docker-compose.yaml --project-directory ../prowlarr up -d
```

## Prowlarr setup

Settings → Indexer Proxies → + → FlareSolverr:

- Name: `FlareSolverr`
- Host: `http://flaresolverr:8191` (no `/v1` suffix)
- Request Timeout: `60` seconds
- Tags: `flaresolverr`

Test, then Save. Add the same `flaresolverr` tag only to indexers that need it;
without matching tags the proxy is disabled. Prowlarr invokes it only when it
detects Cloudflare. Test a tagged indexer and run a search; inspect both services'
logs to verify an actual challenge request. A healthy API alone does not prove
that a tracker challenge can be solved. Do not initiate a download for this test.

FlareSolverr is not a general CAPTCHA solver. The upstream README warns that its
CAPTCHA solver adapters do not currently work. It also does not replace tracker
credentials or grant access to private trackers.

## Storage

- `flaresolverr_config` → `/config`: persistent configuration/log storage provided
  by the image; external volume, not included when backing up this directory.
- Browser temporary files use a RAM-backed `/tmp`, capped at 256 MiB.
- No media-directory mount and no .env file are required.

## References

- https://github.com/FlareSolverr/FlareSolverr
- https://wiki.servarr.com/prowlarr/settings#indexer-proxies
