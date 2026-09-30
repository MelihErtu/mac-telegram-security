# Mac Telegram Security

Mac Telegram Security takes a webcam photo when you log in to macOS or unlock the screen, then sends it to your Telegram bot. The Telegram message includes two buttons: **Yes, It's Me** to approve the login and **No, Lock Mac** to immediately lock the Mac again.

> This project is intended for protecting your own Mac and Telegram account. Because it uses the camera, inform anyone who uses the device and comply with applicable privacy laws.

## Requirements

- macOS
- Python 3 (`/usr/bin/python3`)
- Homebrew
- `imagesnap`
- A Telegram bot and your Telegram Chat ID

## Installation

1. Download or clone this repository.
2. Install `imagesnap`:

```bash
brew install imagesnap
```

3. Make the installer executable and run it:

```bash
chmod +x install.sh uninstall.sh
./install.sh
```

The installer will create `config.json` and stop. Open that file and enter **your own** Telegram bot token and Chat ID:

```json
{
  "bot_token": "...",
  "chat_id": "..."
}
```

4. Run the installer again:

```bash
./install.sh
```

5. Allow the requested macOS permissions. Camera permission may be required for `imagesnap`. Remote locking through Telegram may also require Automation/Accessibility permission for `System Events`.

## How It Works

`imac_security.py` takes a photo, sends it to Telegram, and waits for a button response for about 120 seconds. `unlock_watcher.py` monitors the macOS lock state and starts the main program whenever the state changes from **locked → unlocked**. LaunchAgents start the main program at login and keep the unlock watcher running in the background.

## Uninstall

```bash
./uninstall.sh
```

This removes the LaunchAgents. It does **not** automatically delete `config.json` or the project directory.

## Security

- `config.json` is excluded from Git by `.gitignore`.
- Never publish your bot token in a README, issue, commit, screenshot, or log.
- If a token is accidentally exposed, revoke it with BotFather and generate a new one.
- The installer sets `config.json` permissions to `600`.
- Use only your own Telegram Chat ID.

## Troubleshooting

Logs are written to `/tmp/mac_telegram_security_error.log` and `/tmp/mac_unlock_watcher_error.log`.

If the camera does not work, check **System Settings → Privacy & Security → Camera** and make sure the required app/process has camera access.

## License

MIT License. See `LICENSE` for details.
