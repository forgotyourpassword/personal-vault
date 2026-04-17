---
tags:
  - resource
---

# Hermes Memory - Infrastructure & Scripts

## Office Machine (Windows)
- Hostname: `office` (192.168.1.51)
- SMB share: `\\office\share` — this is the D: drive root
- SMB username: `share`
- SMB password: encrypted at `~/.hermes/office-smb.gpg` (GPG key: Michaelmolloy89@gmail.com)
- Access via pysmb (installed in `~/.hermes/venv`)

## Hermes Backup to Office
- Script: `~/.hermes/scripts/backup_to_office.py`
- Uploads hermes-backup-*.zip from `~/` to `\\office\share\Backups\Hermes\`
- Picks latest backup automatically, or use `--file <path>` for specific file
- Reads SMB password from GPG: `~/.hermes/office-smb.gpg`
- Run with: `~/.hermes/venv/bin/python ~/.hermes/scripts/backup_to_office.py`
- Not yet scheduled (cron job pending)

## Scripts Directory
- Location: `~/.hermes/scripts/`
- `backup_to_office.py` — SMB upload to office (see above)
- `journal_kpi.py` — Journal KPI dashboard (sends to Telegram)
- `reminder_check.py` — Daily vault reminder check
- `journal_watcher.sh` — Journal file watcher

## Shared venv
- Location: `~/.hermes/venv`
- Packages: matplotlib, pillow, requests, pysmb
Quartz: http://192.168.1.223:8080/30-Resources/99-Hermes-Memory/08---Infrastructure-&-Scripts
