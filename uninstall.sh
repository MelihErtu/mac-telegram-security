#!/bin/bash
UIDN="$(id -u)"
for L in com.imactelegram.security com.imactelegram.unlockwatcher; do
  launchctl bootout "gui/$UIDN/$L" 2>/dev/null || true
  rm -f "$HOME/Library/LaunchAgents/$L.plist"
done
echo '✅ LaunchAgents removed. The project directory and config.json were not deleted.'
