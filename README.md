# Homelab

Each service directory is an independent Compose project using the external
`homelab` network.

## Compose conventions

- Main file: `docker-compose.yaml`.
- Top-level order: `services`, `volumes`, `networks`.
- Two-space mapping indentation, block lists, and blank lines between sections.
- Service field order: image/build, profiles, restart/init, entrypoint/command,
  env_file/environment, ports/devices, volumes, depends_on, resources/shutdown,
  healthcheck. Omit unused fields.
- Environment variables use a mapping with quoted string values. Quote port and
  device mappings too.
- Mounts use long syntax: `type`, `source`, `target`, then access and mount options.
  Preserve existing defaults; formatting must not change mount behavior.
- Volume and network definitions put `name` before `external`. Keep existing
  resource names and the distinction between external and Compose-managed volumes.
- Dependencies use explicit conditions. Keep existing conditions unchanged.

Validate with `docker compose config --quiet` from the service directory.
For formatting-only changes, compare rendered configurations before and after,
including optional profiles and supported overrides. Expanded configurations can
contain secrets; do not commit or publish them.
