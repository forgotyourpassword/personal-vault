---
tags:
  - eos
  - learning-game
  - dashboard
---

# EOS Dashboard

If Dataview is enabled, this becomes your campaign control panel.

## Quick Links
- [[EOS RPG Academy]]
- [[EOS Character Sheet]]
- [[EOS Campaign Map]]
- [[EOS Quest Log]]
- [[EOS Boss Fights]]
- [[EOS Harbor View Boss Fights]]
- [[10-Areas/Work/Harbor View Consulting/People/Harbor View Role Library]]
- [[EOS Loot Table & Badges]]
- [[EOS Tactical Question Bank - Part I]]
- [[EOS Progress Log]]

## Manual Snapshot
- **Current Rank:** 
- **Current XP:** 
- **Current Main Quest:** 
- **Current Boss Fight:** 

## Dataview: Session Log
```dataview
TABLE session_date as Date, xp_earned as XP, rank as Rank, focus as Focus, boss_fight as Boss
FROM "30-Resources/Leadership/EOS RPG/Sessions"
SORT session_date DESC
```

## Dataview: XP Total
```dataview
TABLE WITHOUT ID sum(xp_earned) as "Total XP"
FROM "30-Resources/Leadership/EOS RPG/Sessions"
```

---

## Hermes Automation Rules

**One question at a time. Strict judgment. No auto-launch deep debugging from alerts.**

- Report concise diagnoses first; ask before spending significant primary-model usage.
- Do not start background watchers, polling scripts, `getUpdates` bots, or reply-capture loops.
- Deliver daily journal notes to Discord deliveries channel; Michael replies directly to Hermes interactively.
- Save stable settings and preferences here; use Hermes short-term memory for vault-only facts that may drift.

[Axon not found — use **Quartz: http://192.168.1.223:8080/30-Resources/Leadership/EOS-RPG/EOS-Dashboard**]
```dataview
LIST boss_fight
FROM "30-Resources/Leadership/EOS RPG/Sessions"
WHERE boss_fight AND victory = true
SORT session_date DESC
```

## Dataview: Harbor View Applications
```dataview
TABLE session_date as Date, application_note as Application
FROM "30-Resources/Leadership/EOS RPG/Sessions"
WHERE contains(lower(string(focus)), "harbor view") OR application_note
SORT session_date DESC
```

## If Dataview Is Not Enabled
No problem. Use this note as a manual home base and ignore the code blocks. They won't bite.

---

## Hermes Automation Rules

**One question at a time. Strict judgment. No auto-launch deep debugging from alerts.**

- Report concise diagnoses first; ask before spending significant primary-model usage.
- Do not start background watchers, polling scripts, getUpdates bots, or reply-capture loops.
- Deliver daily journal notes to Discord deliveries channel; Michael replies directly to Hermes interactively.
- Save stable settings and preferences here; use Hermes short-term memory for vault-only facts that may drift.

Quartz: http://192.168.1.223:8080/30-Resources/Leadership/EOS-RPG/EOS-Dashboard
