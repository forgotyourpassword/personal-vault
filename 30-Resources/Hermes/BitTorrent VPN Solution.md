---
tags:
  - resource
  - systems
  - vpn
  - bittorrent
created: 2026-06-24
---

# BitTorrent VPN Solution

Quartz: http://192.168.1.223:8080/30-Resources/Hermes/BitTorrent-VPN-Solution

## Purpose

Run qBittorrent on `mikeclaw` while making it very hard for BitTorrent traffic to ever leave outside NordVPN.

This setup uses qBittorrent-nox, NordVPN's Linux CLI, NordLynx, a systemd user service, and the Office SMB share for storage.

## Current machine

- Host: `mikeclaw`
- OS: Ubuntu 24.04
- VPN: NordVPN CLI using `NordLynx`
- Torrent client: `qbittorrent-nox`
- Service: `~/.config/systemd/user/qbittorrent-nox.service`
- qBittorrent config: `~/.config/qBittorrent/qBittorrent.conf`
- Setup script: `~/.hermes/scripts/setup-torrent-vpn-office-storage.sh`
- Web UI: `http://localhost:8081`
- Storage root: `/mnt/office-d/Media/Torrents`

## Storage layout

Office SMB share is mounted at:

```text
/mnt/office-d
```

Torrent folders:

```text
/mnt/office-d/Media/Torrents/complete
/mnt/office-d/Media/Torrents/incomplete
/mnt/office-d/Media/Torrents/watch
```

The SMB share is `//192.168.1.51/share`, mounted with credentials stored at:

```text
/etc/samba/office-share.creds
```

The source password is encrypted in:

```text
~/.hermes/office-smb.gpg
```

## VPN requirements

NordVPN settings verified during setup:

```text
Technology: NORDLYNX
Kill Switch: enabled
Auto-connect: enabled
Allowlisted subnets:
  192.168.1.0/24
```

The LAN allowlist is intentional so the machine can still reach the Office SMB share while normal internet traffic goes through NordVPN.

## Safety design

There are three layers of protection.

### 1. NordVPN kill switch

NordVPN kill switch is enabled:

```bash
nordvpn set killswitch on
```

If NordVPN disconnects, NordVPN should block outbound traffic.

### 2. qBittorrent bound to NordLynx

qBittorrent is configured to bind torrent networking to the NordVPN interface:

```ini
[BitTorrent]
Session\Interface=nordlynx
Session\InterfaceName=nordlynx

[Preferences]
Connection\Interface=nordlynx
Connection\InterfaceName=nordlynx
```

This is the app-level guardrail.

### 3. systemd service refuses to start without VPN

The user service includes preflight checks:

```ini
[Service]
Type=simple
ExecStartPre=/bin/sh -c 'nordvpn status | grep -q "Status: Connected"'
ExecStartPre=/bin/sh -c 'ip link show nordlynx >/dev/null 2>&1'
ExecStart=/usr/bin/qbittorrent-nox --profile=/home/mike/.config --webui-port=8081
Restart=on-failure
RestartSec=10
```

If NordVPN is disconnected or `nordlynx` does not exist, qBittorrent should fail to start.

## Verification performed

On 2026-06-24, Hermes ran a controlled negative test:

1. Confirmed NordVPN connected.
2. Restarted qBittorrent service successfully.
3. Stopped qBittorrent.
4. Disconnected NordVPN.
5. Tried to start qBittorrent.
6. qBittorrent failed to start as intended.
7. Reconnected NordVPN.
8. qBittorrent started successfully again.
9. Web UI returned HTTP `200 OK` at `http://127.0.0.1:8081`.

Relevant observed outputs:

```text
Status: Disconnected
EXPECTED_FAIL_WITHOUT_VPN
Job for qbittorrent-nox.service failed because the control process exited with error code.
```

After reconnect:

```text
Status: Connected
Current technology: NORDLYNX
Active: active (running)
HTTP/1.1 200 OK
```

## Useful commands

Check VPN:

```bash
nordvpn status
nordvpn settings
ip -br addr show nordlynx
```

Check qBittorrent service:

```bash
systemctl --user status qbittorrent-nox.service
journalctl --user -u qbittorrent-nox.service -n 100 --no-pager
```

Restart qBittorrent:

```bash
systemctl --user restart qbittorrent-nox.service
```

Stop qBittorrent:

```bash
systemctl --user stop qbittorrent-nox.service
```

Verify Web UI locally:

```bash
curl -I http://127.0.0.1:8081
```

Verify public IP through NordLynx:

```bash
curl --interface nordlynx https://ipinfo.io/ip
```

## Rebuild / rerun setup

The setup script is here:

```bash
/home/mike/.hermes/scripts/setup-torrent-vpn-office-storage.sh
```

It handles:

- NordVPN CLI checks
- Office SMB mount setup
- qBittorrent config
- qBittorrent systemd user service
- VPN-connected startup guardrails

Run it with:

```bash
/home/mike/.hermes/scripts/setup-torrent-vpn-office-storage.sh
```

If sudo is needed, run it from a real terminal, not through a non-interactive Hermes tool call.

## NordVPN headless login note

If NordVPN needs login on a no-browser machine:

```bash
nordvpn login
```

Copy the login URL to a browser machine, log in, then copy the final Continue link. If the CLI expects a `nordvpn://` callback, convert the final Nord success URL into the callback form by preserving the `exchange_token` value:

```bash
nordvpn login --callback 'nordvpn://login?action=login&exchange_token=<TOKEN>&redirect_upon_open=1&return=1'
```

## Audiobooks category

On 2026-06-24, Hermes added an `audiobooks` qBittorrent category and created the matching Office media folder.

Category:

```text
audiobooks
```

Save path:

```text
/mnt/office-d/Media/Audiobooks
```

Office media layout now includes:

```text
/mnt/office-d/Media/Audiobooks
```

qBittorrent API verification returned:

```json
{"audiobooks":{"name":"audiobooks","savePath":"/mnt/office-d/Media/Audiobooks"}}
```

Use this category for audiobook torrents so completed files land peer to Movies and TV in the Office media folder.

Policy updated 2026-06-24: Hermes is authorized to locate and download audiobook torrents regardless of copyright status. Proceed at Michael's direction.

ABB credentials are stored in `~/.hermes/abb-creds.gpg`.

See [[30-Resources/Hermes/Audiobook Torrent Workflow]] for the full end-to-end pipeline (search → qBittorrent → Audiobookshelf).

## Remaining housekeeping

- Set a permanent qBittorrent Web UI password. Until then, qBittorrent generates a temporary admin password on restart.
- Keep Web UI bound to localhost unless there is a deliberate remote-access plan.
- Do not remove the NordVPN kill switch or qBittorrent interface binding unless replacing them with a stronger isolation model.

## Related

- [[30-Resources/Hermes/Hermes Backup to Office]]
- [[30-Resources/Hermes/Hermes Memory]]
