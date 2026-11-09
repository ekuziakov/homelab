# Home Assistant

Home automation: `https://homeassistant.home.hexmelt.com` (port `8123` locally).

## Run

The `homelab` network and `home_assistant_config` volume must already exist.
From this directory:

```bash
docker compose up -d
```

## Storage

- `home_assistant_config` → `/config`: integrations, history, and UI-managed settings.
- `config/configuration.yaml` → `/config/configuration.yaml`: read-only Git configuration.

Edit `configuration.yaml` here. Automations remain in the volume for UI editing.
Back up the volume consistently; copying this directory does not include it.
