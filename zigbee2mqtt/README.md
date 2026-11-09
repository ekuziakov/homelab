# Zigbee2MQTT

Zigbee bridge and Mosquitto broker. Web UI: `http://localhost:8080`;
MQTT: port `1883`.

## Run

Requires `homelab`, both external volumes below, and the coordinator at
`/dev/ttyUSB0`. After restarting OrbStack, follow [USB attachment](USB.md).
From this directory:

```bash
docker compose up -d
```

## Storage

- `zigbee2mqtt_data` → `/app/data`: Zigbee network and device state.
- `mosquitto_data` → `/mosquitto/data`: MQTT persistence.
- `zigbee2mqtt/data/configuration.yaml` → `/app/data/configuration.yaml`: Git configuration.
- `mosquitto/config` → `/mosquitto/config`: broker configuration.

Back up both volumes consistently and retain the Git configuration; copying
this directory does not include volume data.
