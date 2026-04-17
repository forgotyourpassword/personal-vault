---
tags:
  - resource
---

# Hermes Memory

My persistent context about the user, environment, and conventions. Updated across sessions. I read this at the start of sessions or when context is needed.

---

## User Profile

- Telegram: `8021131601` (Michael Molloy)
- GitHub username: `forgotyourpassword`
- Machine hostname: `mikeclaw` (Ubuntu 24.04 x86_64)
- Home directory: `/home/mike/`
- Separate machine: `office` running LM Studio with local models, LM Link enabled
- Prefers local models when possible

## Environment

### LM Studio / Models
- Installed at `~/.lmstudio/bin/lms` on mikeclaw
- LM Link enabled, device `office` connected running `google/gemma-3-4b`
- Default model: `google/gemma-3-4b` via lmstudio provider at `http://localhost:1234/v1`
- `lms` daemon must be running for local models to work

### Obsidian Vault
- Location: `/home/mike/vault/`
- Organization: PARA (00-Inbox, 10-Areas, 20-Projects, 30-Resources, 40-Archive)
- Additional folders: Home, Journal, Templates
- Git: version controlled, remote `github-openclaw-vault:forgotyourpassword/personal-vault.git` on `main`
- SSH: authenticated via `github-openclaw-vault` host alias
- Git identity: `forgotyourpassword` / `michaelmolloy89@gmail.com`

### Communications
- Hermes Telegram integration configured (bot token stored in system memory)
- Telegram chat ID: `8021131601`

## Conventions
- Store memory here as markdown notes in the vault, not in the system memory blob (except critical auth tokens)
- Use `search_files` in the vault to find relevant context when needed
- Commit and push vault changes
Quartz: http://192.168.1.223:8080/30-Resources/Hermes/Hermes-Memory
