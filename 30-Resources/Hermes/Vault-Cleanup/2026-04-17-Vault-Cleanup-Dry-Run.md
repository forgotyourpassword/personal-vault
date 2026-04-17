---
tags:
  - vault-cleanup
  - audit
  - dry-run
  - type/report
status: proposed
date: 2026-04-17
---

# Vault Cleanup Dry Run (Review Before Changes)

Scope: full vault audit for tagging, links, and structure optimization with no content edits applied.

## Baseline metrics

- Total notes: 155
- Notes with no tags: 60
- Broken wikilinks: 80
  - basename-missing: 53
  - path-missing: 22
  - folder-placeholder: 5
- High-confidence auto-fix link proposals: 19
- Redundant inline tags overlapping frontmatter: 0

## What this means

1) Tagging is the biggest cleanup opportunity right now.
2) Most actionable link breakage is concentrated in Home project links using a stale `/Active/` path segment.
3) A lot of basename-missing links are intentional-but-invalid references to folders, which should become proper index/MOC notes.

## Proposed tag policy (frontmatter is source of truth)

### Canonical domains (flat)

- home
- work
- family
- finance
- health
- fitness
- inventory
- crm
- project
- resource
- journal
- inbox

### Canonical qualifiers (namespaced)

- type/* (type/hub, type/index, type/template, type/log, type/report, type/reference)
- status/* (status/active, status/waiting, status/archived)
- activity/* (activity/hike, activity/ruck, activity/run, activity/lift)

### Migration recommendations

- Keep: type/*, status/*, activity/*
- Migrate: area/fitness -> fitness
- Migrate: area/family -> family
- Migrate: area/health -> health
- Normalize: workfromthewoods + work-outdoors -> work-from-the-woods

## Proposed change set (no edits yet)

### A) Tag fill-in (60 notes)

- 59 high-confidence path-based tag additions
- 1 low-confidence note requiring manual choice

High-confidence examples:
- `10-Areas/Finance/Finance Hub.md` -> `finance`, `type/hub`
- `10-Areas/Home/Decisions.md` -> `home`, `type/decision-log`
- `10-Areas/Home/Templates/Project Template.md` -> `home`, `type/template`
- `20-Projects/Projects Index.md` -> `project`, `type/index`

### B) Link repairs (19 high-confidence fixes)

Bulk pattern to apply:
- `20-Projects/Home/Active/Project - ...` -> `20-Projects/Home/Project - ...`

Primary impacted files:
- `10-Areas/Home/Dashboard.md`
- `10-Areas/Home/Areas/Area - Backyard.md`
- `10-Areas/Home/Areas/Area - Basement.md`
- `10-Areas/Home/Areas/Area - Flooring.md`
- `10-Areas/Home/Areas/Area - Kids Bathroom.md`
- `10-Areas/Home/Areas/Area - Living Room.md`
- `10-Areas/Home/Areas/Area - Master Bathroom.md`
- `10-Areas/Home/Areas/Area - Top Floor.md`
- `10-Areas/Home/Areas/Area - Whole House.md`

### C) MOC/index gap fixes (manual approval before creation)

`index.md` currently links to missing notes:
- `[[10-Areas]]`
- `[[30-Resources]]`

Recommendation:
- Create `10-Areas/Areas Index.md` and `30-Resources/Resources Index.md`, then repoint root links.
- Repoint `[[20-Projects/Home|Projects]]` to `[[20-Projects/Projects Index|Projects]]`.
- Repoint `[[Journal/Daily|Daily Journal]]` to a concrete note or daily index note.

## Artifacts generated for review

- `/home/mike/vault/30-Resources/Hermes/Vault-Cleanup/2026-04-17-untagged-proposals.csv`
- `/home/mike/vault/30-Resources/Hermes/Vault-Cleanup/2026-04-17-link-fix-proposals.csv`
- `/home/mike/vault/30-Resources/Hermes/Vault-Cleanup/2026-04-17-broken-links-full.csv`
- `/home/mike/vault/30-Resources/Hermes/Vault-Cleanup/2026-04-17-redundant-inline-tags.csv`

## Execution sequence once approved

1) Apply link fixes (safe, high confidence)
2) Apply tag additions for high-confidence untagged notes
3) Normalize tag variants
4) Build/repair top-level MOCs
5) Re-run audit and produce before/after metrics

## Phase 2 execution result (applied)

Applied on approval:
- Fixed high-confidence stale `/Active/` project links in 9 files.
- Added frontmatter tags to 59 high-confidence untagged files.
- Skipped `Reminders.md` as low-confidence tagging.

Before -> After:
- Untagged notes: 60 -> 1
- Broken links total: 80 -> 65
- Path-missing links: 22 -> 5

Current remaining issues (next pass):
- Folder-style links in `Fitness Hub` (workout subfolder links)
- Missing top-level MOCs referenced by root index (`10-Areas`, `30-Resources`)
- Inventory basename links to non-note category names (e.g., `Firearms`)

Quartz: http://192.168.1.223:8080/30-Resources/Hermes/Vault-Cleanup/2026-04-17-Vault-Cleanup-Dry-Run
