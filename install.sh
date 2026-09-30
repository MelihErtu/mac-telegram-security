#!/bin/bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
LABEL="com.imactelegram.security"
WATCH="com.imactelegram.unlockwatcher"
UIDN="$(id -u)"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
WPLIST="$HOME/Library/LaunchAgents/$WATCH.plist"
command -v imagesnap >/dev/null || { echo 'imagesnap is not installed. Install it first: brew install imagesnap'; exit 1; }
[ -f "$DIR/config.json" ] || { cp "$DIR/config.example.json" "$DIR/config.json"; chmod 600 "$DIR/config.json"; echo 'config.json was created. Enter your bot token and Chat ID, then run install.sh again.'; exit 0; }
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><dict><key>Label</key><string>$LABEL</string><key>ProgramArguments</key><array><string>/usr/bin/python3</string><string>$DIR/imac_security.py</string></array><key>RunAtLoad</key><true/><key>StandardOutPath</key><string>/tmp/mac_telegram_security.log</string><key>StandardErrorPath</key><string>/tmp/mac_telegram_security_error.log</string></dict></plist>
EOF
cat > "$WPLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><dict><key>Label</key><string>$WATCH</string><key>ProgramArguments</key><array><string>/usr/bin/python3</string><string>$DIR/unlock_watcher.py</string></array><key>RunAtLoad</key><true/><key>KeepAlive</key><true/><key>StandardOutPath</key><string>/tmp/mac_unlock_watcher.log</string><key>StandardErrorPath</key><string>/tmp/mac_unlock_watcher_error.log</string></dict></plist>
EOF
launchctl bootout "gui/$UIDN/$LABEL" 2>/dev/null || true
launchctl bootout "gui/$UIDN/$WATCH" 2>/dev/null || true
launchctl bootstrap "gui/$UIDN" "$PLIST"
launchctl bootstrap "gui/$UIDN" "$WPLIST"
echo '✅ Installation complete.'
echo 'Allow Camera and Automation/Accessibility permissions if macOS requests them.'
