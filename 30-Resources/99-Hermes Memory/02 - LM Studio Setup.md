---
tags:
  - resource
---

# LM Studio Setup

## Installation
- Path: `~/.lmstudio/bin/lms` (on mikeclaw)
- CLI: `lms` commands

## Configuration
- Default model: `google/gemma-3-4b`
- Provider: `lmstudio` at `http://localhost:1234/v1`
- LM Link: enabled
- Device `office` connected running `google/gemma-3-4b`

## Office Machine — Network Access
- IP: 192.168.1.51, hostname: office
- SSH: not enabled (port 22 closed)
- SMB: port 445 open — use impacket for file transfers
- RDP: port 3389 open
- Windows username: Work
- Password: stored at ~/.hermes/office-smb.gpg (GPG encrypted, recipient 0F761A18ABB0F4D2)
- Always retrieve via: SMB_PASS=$(gpg --decrypt ~/.hermes/office-smb.gpg 2>/dev/null) — NEVER put in plaintext
- LM Studio username: forgotyourpassword (different from Windows login)
- SMB share "share" maps to D: drive — use this for file transfers (D$ admin share is access denied)
- Work account needs write permissions granted on target folder before uploads will succeed

## Gotchas
- `lms` daemon must be running for local models to work
Quartz: http://192.168.1.223:8080/30-Resources/99-Hermes-Memory/02---LM-Studio-Setup
