# SparkyFitness

Fitness and nutrition tracking: `https://sparkyfitness.home.hexmelt.com`
(port `3004` locally).

## Run

Configure `.env` using `.env.example`. The `homelab` network and external
volumes below must already exist. From this directory:

```bash
docker compose up -d
```

## Storage

- `sparkyfitness_postgresql` → `/var/lib/postgresql`: PostgreSQL database.
- `sparkyfitness_backup` → `/app/SparkyFitnessServer/backup`: application backups.
- `sparkyfitness_uploads` → `/app/SparkyFitnessServer/uploads`: uploaded files.

Back up the database and uploads consistently, and retain the backup volume.
Keep `.env` and its encryption key safe; repository copies exclude volume data.
