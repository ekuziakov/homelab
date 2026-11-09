# Caddy

HTTPS reverse proxy for `*.home.hexmelt.com` on ports `80` and `443`.
The included Dockerfile builds Caddy with Cloudflare DNS support.

## Run

Configure `.env` using `.env.example` and set `CF_API_TOKEN`.
The `homelab` network and external volumes below must already exist.
From this directory:

```bash
docker compose up -d
```

## Storage

- `Caddyfile` → `/etc/caddy/Caddyfile`: routes and TLS configuration.
- `caddy_data` → `/data`: certificates and TLS state.
- `caddy_config` → `/config`: Caddy runtime configuration.

Back up both volumes and keep `.env` safe; repository copies exclude volume data.
