# Actual Budget

Budget tracking: `https://actual.home.hexmelt.com` (port `5006` locally).

## Run

The `homelab` network and `actual_budget_data` volume must already exist.
From this directory:

```bash
docker compose up -d
```

## Storage

- `actual_budget_data` → `/data`: budgets and application state.

Back up the volume separately; copying this directory does not include it.
