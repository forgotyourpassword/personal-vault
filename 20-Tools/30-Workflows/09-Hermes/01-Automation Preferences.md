# Hermes Automation Preferences

## Recurring behaviors to keep

- **Daily journal via cron prompt** (job 05229e8dd3a3 @ 9:30 PM EST)
  - Delivered to Discord deliveries: 1495011785533689886
  - Note lives at `/home/mike/vault/Journal/Daily/YYYY-MM-DD.md`
  - **No auto-reply watcher** — `getUpdates` conflicts with Hermes gateway
  - Michael types replies directly to Hermes, one question at a time, when he wants to fill out the journal

- **Morning briefing** (cron job) delivers to Discord deliveries

- **Weekly journal review** (Sunday 8 AM)

- **Journal KPI dashboard** (11:30 PM) sends an image to Discord

## Interface rules

- **Stay at the default channel assignment** unless explicitly told to change it.
- **Do not repair Hermes with broad diagnostics without asking**. Give concise diagnoses first.
- **Confirm before deleting large chunks of memory.**
- **Use Hermes memory for short-term preferences and environment facts that are likely to change.**
- **Use the Obsidian vault for stable, long-term settings, conventions, and preferences** that don't need to auto-appear in every session.