# Floppy

Media tracker: `https://floppy.home.hexmelt.com` (port `8000` locally).
The MCP service is internal to `homelab` at `floppy-mcp:8000`.

## Run

Configure `.env` using `.env.example`. The `homelab` network and external
volumes below must already exist. From this directory:

```bash
docker compose up -d
```

Set `FLOPPY_TOKEN` from Settings → Integrations. Set `REGISTRATION=False`
after account setup.

## Storage

- `floppy_db` → `/floppy/db`: application database.
- `floppy_backups` → `/floppy/backups`: application backups.
- `floppy_redis` → `/data` in Redis: persistent Redis data.

Back up the volumes consistently and keep `.env` safe; copying this directory
does not include volume data.
