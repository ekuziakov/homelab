# Zigbee2MQTT on OrbStack

After quitting and reopening OrbStack, the Sonoff USB coordinator needs to be attached again. This script opens OrbStack, waits for Docker, attaches the coordinator if needed, and starts Mosquitto and Zigbee2MQTT. It runs once and exits—no background agent required.

## Startup script

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

Adjust the `cd` path to your Compose directory. OrbStack CLI, Docker Compose, existing images, and the external `homelab` Docker network must already be available. The script expects one Sonoff adapter with USB VID:PID `10c4:ea60`; its current device ID is discovered each time.

## Run from Terminal

Save the script as `start-orbstack.sh`, then run:

```bash
bash start-orbstack.sh
```

No `sudo` or executable permission is needed when invoking it with Bash.

## Run with Apple Shortcuts

1. Create a shortcut named **Start Homelab**.
2. Add the **Run Shell Script** action and select `/bin/bash` as the shell.
3. Paste the script above directly into the action. Do not enable administrator privileges.
4. Optionally add **Show Result** to display the shell action's output.
5. Add the shortcut to the Dock or menu bar, or assign a keyboard shortcut.

Launch OrbStack through this shortcut. Opening OrbStack normally does not run the script. Allow access to the external disk or script execution if macOS requests it.

The script does not recreate existing containers, build images, or pull images. It uses a simple two-second pause after Attach rather than checking device readiness; if startup fails because the device is not ready yet, run it again. It does not check application health or impose timeouts on individual commands.
