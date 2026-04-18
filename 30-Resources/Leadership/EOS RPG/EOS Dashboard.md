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

## Dataview: Cleared Boss Fights
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

Quartz: http://192.168.1.223:8080/30-Resources/Leadership/EOS-RPG/EOS-Dashboard
