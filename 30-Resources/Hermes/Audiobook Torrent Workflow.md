---
tags:
  - resource
  - systems
  - bittorrent
  - audiobooks
created: 2026-06-24
---

# Audiobook Torrent Workflow

Quartz: http://192.168.1.223:8080/30-Resources/Hermes/Audiobook-Torrent-Workflow

## Overview

End-to-end pipeline for finding audiobook torrents, downloading them via qBittorrent (VPN-bound), and serving them to a phone via Audiobookshelf.

## Infrastructure

| Component | Location | Notes |
|-----------|----------|-------|
| qBittorrent | `http://localhost:8081` | VPN-bound; categories: `audiobooks`, `movies`, `tv` |
| Audiobookshelf | `http://192.168.1.223:13378` | Serves `/mnt/office-d/Media/Audiobooks` to LAN/phone |
| ABB credentials | `~/.hermes/abb-creds.gpg` | Encrypted with same passphrase as office-smb.gpg |
| VPN | NordVPN via NordLynx | Kill switch enabled, qBittorrent bound to `nordlynx` interface |

Category save paths:

```text
audiobooks → /mnt/office-d/Media/Audiobooks
movies     → /mnt/office-d/Media/Movies
tv         → /mnt/office-d/Media/TV
```

## Step 1: Find torrents

### SolidTorrents (curl-friendly — best for automation)

```bash
curl -sL "https://solidtorrents.to/search?q=<title>+<author>+audiobook" \
  | grep -oP 'magnet:\?[^"'\''\s<>]+'
```

This is the only source that works reliably with curl from `mikeclaw`. No session cookies required.

### AudiobookBay (requires browser — but has wider catalog)

ABB blocks programmatic access. The search form requires browser-based session cookies. Use the browser tool or a real browser with login:

- URL: `https://audiobookbay.lu`
- Login: `Hiraki` / `regencyfellow` (stored in `~/.hermes/abb-creds.gpg`)
- Search via the on-page form (not `?s=` URL parameter)

ABB has many business/self-help titles not found on SolidTorrents.

## Step 2: Add to qBittorrent

**⚠️ Must explicitly set savepath** — the API `category` parameter alone doesn't redirect to the category save path. Always include `savepath`:

```bash
curl -s -b /tmp/qb.cookies \
  -d "urls=magnet:?xt=urn:btih:..." \
  -d "category=audiobooks" \
  -d "savepath=/mnt/office-d/Media/Audiobooks" \
  http://127.0.0.1:8081/api/v2/torrents/add
```

Get the temp password from:
```bash
journalctl --user -u qbittorrent-nox.service --no-pager -n 50 | grep "temporary password"
```

Files download to `/mnt/office-d/Media/Audiobooks/`.

## Step 3: Audiobookshelf serves them

Audiobookshelf runs as a user systemd service at `http://192.168.1.223:13378`.

- **Web UI**: `http://192.168.1.223:13378` — set up the admin account on first visit
- **Phone app**: Available on iOS/Android — connect to `http://192.168.1.223:13378`
- **Library**: Point at `/mnt/office-d/Media/Audiobooks`

### Service management

```bash
systemctl --user status audiobookshelf.service
systemctl --user restart audiobookshelf.service
journalctl --user -u audiobookshelf.service -f
```

### Install location

```
~/audiobookshelf/           # Git clone + npm install
~/audiobookshelf/config/    # Config DB
~/audiobookshelf/metadata/  # Covers, metadata cache
```

## Step 4: Access from phone

1. Open Audiobookshelf app (iOS/Android)
2. Server URL: `http://192.168.1.223:13378`
3. Login with the admin account created during first setup

Phone must be on the same LAN (192.168.1.x).

## Permanent qBittorrent path configuration

On 2026-06-24, live qBittorrent preferences were corrected through the API and verified after service restart:

```text
save_path=/mnt/office-d/Media/Torrents/complete
temp_path=/mnt/office-d/Media/Torrents/incomplete
temp_path_enabled=true
auto_tmm_enabled=true
category_changed_tmm_enabled=true
save_path_changed_tmm_enabled=true
torrent_changed_tmm_enabled=true
use_category_paths_in_manual_mode=true
audiobooks category savePath=/mnt/office-d/Media/Audiobooks
```

Verification command:

```bash
python3 - <<'PY'
import requests
qb=requests.Session()
qb.post('http://127.0.0.1:8081/api/v2/auth/login', data={'username':'admin','password':'<temp-password>'})
print(qb.get('http://127.0.0.1:8081/api/v2/app/preferences').json()['save_path'])
print(qb.get('http://127.0.0.1:8081/api/v2/torrents/categories').text)
PY
```

## Known issues

- **ABB blocks unauthenticated curl/Python**: Working pattern is POST login, then POST search. See the ABB section above.
- **SolidTorrents false positives**: Short/ambiguous titles sometimes match wrong books. Verify the magnet filename before adding.
- **VPN must be up**: qBittorrent won't start without NordVPN connected (by design).
- **qBittorrent password resets on restart**: The Web UI password is temporary. Set a permanent one in Preferences → Web UI.

## Related

- [[30-Resources/Hermes/BitTorrent VPN Solution]]
- [[10-Areas/Reading/Reading Log]]
