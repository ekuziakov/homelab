# Zigbee2MQTT on OrbStack

Reattach the Sonoff USB coordinator after restarting OrbStack. Requires Docker
Compose, the external `homelab` network, and one adapter with VID:PID `10c4:ea60`.

Run this script on the Mac, or paste it into an Apple Shortcuts **Run Shell
Script** action using `/bin/bash` without administrator privileges:

```bash
#!/bin/bash
set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/Applications/OrbStack.app/Contents/MacOS/bin:$PATH"

open -a OrbStack
until docker --context orbstack info >/dev/null 2>&1; do
    (( SECONDS < 60 )) || { echo 'OrbStack: Docker did not start' >&2; exit 1; }
    sleep 1
done

device=$(orb usb list | awk '
    $2 == "10c4:ea60" { id=$1; state=$NF; count++ }
    END { if (count != 1) exit 1; print id, state }
') || { echo 'Expected exactly one Sonoff USB adapter (10c4:ea60)' >&2; exit 1; }
read -r id state <<< "$device"
if [ "$state" != attached ]; then
    orb usb attach "$id"
    sleep 2
fi

cd /Volumes/SSD1/homelab/zigbee2mqtt
docker compose up -d zigbee2mqtt
```

If saved as `start-orbstack.sh`, run `bash start-orbstack.sh`. Opening OrbStack
normally does not run it. The script waits two seconds after USB attachment;
retry if the device is not ready. It does not check application health.
