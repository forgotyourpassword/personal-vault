# Hermes Backup to Office

Quartz: http://192.168.1.223:8080/30-Resources/Hermes/Hermes-Backup-to-Office

## Overview
Automated setup to transfer Hermes config backups from the Linux home server to the Windows "office" machine over SMB for offsite redundancy.

## Setup Details

| Item | Value |
|------|-------|
| Source | `~/hermes-backup-*.zip` (created by `hermes backup`) |
| Destination | `\\office\share\Backups\Hermes\` (D:\Backups\Hermes\) |
| Transport | SMB via pysmb |
| Script | `~/.hermes/scripts/backup_to_office.py` |
| Credentials | `~/.hermes/office-smb.gpg` (GPG encrypted) |
| Python env | `~/.hermes/venv/bin/python` |

## Office Machine
- Hostname: `office` / IP: `192.168.1.51`
- SMB share name: `share` (maps to D: drive root)
- SMB username: `share`

## Usage

### Run manually
```bash
# Upload latest backup automatically
~/.hermes/venv/bin/python ~/.hermes/scripts/backup_to_office.py

# Upload a specific file
~/.hermes/venv/bin/python ~/.hermes/scripts/backup_to_office.py --file ~/hermes-backup-2026-04-12-224643.zip
```

### Create a fresh backup first
```bash
hermes backup
~/.hermes/venv/bin/python ~/.hermes/scripts/backup_to_office.py
```

## Scheduled Job
- Cron job ID: `dc0f36d08ab0`
- Name: Hermes Nightly Backup to Office
- Schedule: daily at 3:00 AM
- Steps: `hermes backup` → `backup_to_office.py` → reports result to Telegram
- Each backup is timestamped so old files are never overwritten

## Notes
- The `share` user does NOT have access to `D$` (admin share) — must use the `share` share name
- Existing `Backups\Hermes` folder was already present on D: drive
- First upload: `hermes-backup-2026-04-12-224643.zip` (114.7 MB) — confirmed successful

## Related
- [[08 - Infrastructure & Scripts]]

Tags: #hermes #backup #infrastructure
