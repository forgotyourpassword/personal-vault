# Journal KPI Dashboard

Auto-generated habit progress dashboard sent to Telegram whenever a daily journal is saved.

## What it does

- Parses every `Journal/Daily/YYYY-MM-DD.md` file
- Reads the `[x]` checkboxes for **Exercise**, **Read**, and **Nourished well**
- Generates a dark-theme KPI image with:
  - Weekly donut gauges (Exercise / Reading / Nutrition %)
  - All-habits streak counter
  - 7-day habit calendar bars
  - 30-day rolling trend lines
  - Today's "one sentence on today" quote
- Sends the image + caption to Telegram via bot

## Trigger

A systemd user service (`journal-kpi-watcher.service`) watches the journal folder with `inotifywait`.
When a `YYYY-MM-DD.md` file is saved, it waits 30 seconds of quiet (debounce) then fires.

## Files

| File | Purpose |
|------|---------|
| `journal_kpi.py` | Parses journals, builds chart, sends to Telegram |
| `journal_watcher.sh` | inotifywait loop with debounce logic |
| `journal-kpi-watcher.service` | systemd user service definition |

Live copies of the scripts are at `~/.hermes/scripts/`.
The service file lives at `~/.config/systemd/user/journal-kpi-watcher.service`.

## Setup / Restore

```bash
# 1. Install dependencies
uv venv ~/.hermes/venv
uv pip install matplotlib pillow requests --python ~/.hermes/venv/bin/python

# 2. Install inotify-tools
sudo apt-get install -y inotify-tools

# 3. Copy scripts
cp journal_kpi.py ~/.hermes/scripts/
cp journal_watcher.sh ~/.hermes/scripts/
chmod +x ~/.hermes/scripts/journal_watcher.sh

# 4. Install and start the service
cp journal-kpi-watcher.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable journal-kpi-watcher.service
systemctl --user start journal-kpi-watcher.service
```

## Dependencies

- Python venv at `~/.hermes/venv` with: `matplotlib`, `pillow`, `requests`
- `inotify-tools` (apt package)
- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_HOME_CHANNEL` in `~/.hermes/.env`

## Logs

```bash
cat ~/.hermes/logs/journal_watcher.log
journalctl --user -u journal-kpi-watcher.service -f
```

## Manual run

```bash
source ~/.hermes/.env && \
  OBSIDIAN_VAULT_PATH=/home/mike/vault \
  ~/.hermes/venv/bin/python ~/.hermes/scripts/journal_kpi.py
```

*Tags: #hermes #automation #journal #habits #telegram*
