# Vault Organization & Optimization Plan
**Date:** 2026-04-12
**Status:** Draft — awaiting approval before execution

---

## Goal

Reorganize and optimize the Obsidian vault at `/home/mike/vault` to eliminate structural inconsistencies, clean up stray folders, standardize note conventions, and make navigation, search, and Hermes automation more reliable.

---

## Current State Assessment

**What's working well:**
- PARA-like structure (00-Inbox / 10-Areas / 20-Projects / 30-Resources / 40-Archive) is solid and should be preserved
- Fitness area is the most mature: templates, workout logs, hub note, all consistently organized
- Personal CRM is well-structured with an index, individual notes, and subcategories
- Home management system is thorough (areas, projects, contractors, dashboards)
- Journal daily notes are consistent and tightly templated
- LLM-Wiki is self-contained with its own schema

**Problems identified:**

### 1. Duplicate / Parallel Structures (High Priority)
- `Home/` folder lives at root — should be inside `10-Areas/` (alongside Health, Family, Work, etc.)
- `Resources/` folder (LLM-Wiki only) lives at root alongside `30-Resources/` — these should merge
- `Templates/` folder at root is **empty** — can be deleted; real templates live in `Home/Templates/`
- `hermes-backups/` is inside the vault — backup zip files should not live here

### 2. Empty / Underused Sections
- `20-Projects/` is **completely empty** — active projects live inside `Home/Projects/Active/` instead; needs a proper home
- `40-Archive/` is empty — no archiving workflow established yet
- `00-Inbox/` has only one note (Traction.md) — good capture practice but needs a processing habit
- `10-Areas/Personal/` folder exists but has zero notes

### 3. Tag Inconsistency
- Most notes have NO tags at all (frontmatter or inline)
- Fitness notes use inline `#tags` at the top
- LLM-Wiki uses YAML frontmatter `tags:`
- No consistent tagging convention across the vault
- Orphaned notes: CRM people, inventory items, leadership notes have no tags

### 4. Missing Index / Hub Notes
- `10-Areas/Work/` has only one note (Work From The Woods) — no Work Hub or index
- `10-Areas/Family/` has calendar notes but no Family Hub
- `10-Areas/Finance/` folder exists but is completely empty
- Inventory has an index but no category grouping (all 40+ items in one flat folder)
- Leadership folder has 2 standalone notes, no hub

### 5. Scattered Hermes/Automation Files
- `30-Resources/99-Hermes Memory/` — good, stays
- `30-Resources/Hermes/` — Journal-KPI README and Hermes Backup note
- `Home/Hermes Memory.md` — stray Hermes memory note inside Home
- These should be consolidated into one `30-Resources/Hermes/` home

### 6. Quartz URLs
- Per convention, notes should include their Quartz static site URL
- Many notes (especially older ones) are missing this

---

## Proposed Changes

### Phase 1 — Structure Cleanup (Low Risk)
1. **Delete empty folders:** `Templates/` (root), `10-Areas/Personal/` (empty), `40-Archive/` (empty — recreate when first item archived)
2. **Move `Home/` → `10-Areas/Home/`** and update all internal wikilinks
3. **Move `Resources/LLM-Wiki/` → `30-Resources/LLM-Wiki/`** and update LLM-Wiki skill path reference
4. **Delete `Resources/`** (will be empty after LLM-Wiki move)
5. **Move `hermes-backups/`** out of the vault entirely (to `~/.hermes/` or similar)
6. **Consolidate Hermes files:** Move `Home/Hermes Memory.md` → `30-Resources/Hermes/`

### Phase 2 — Add Missing Hubs (Medium Effort)
7. **Create `10-Areas/Work/Work Hub.md`** — links to Kevin/Kurt CRM notes, active work projects, Harbor View context, leadership resources
8. **Create `10-Areas/Family/Family Hub.md`** — links to CRM family members, calendars, family events
9. **Create `10-Areas/Finance/Finance Hub.md`** — placeholder with structure for budget, accounts, expenses
10. **Populate `20-Projects/`** — either move `Home/Projects/Active/` items here or create a `20-Projects/README.md` clarifying the intent (home projects stay under Home, vault-level projects go here)

### Phase 3 — Tagging Convention (Medium Effort)
11. **Adopt a single standard:** YAML frontmatter for all notes going forward:
```yaml
---
tags: [area/health, fitness, workout]
---
```
12. **Backfill tags on key notes:** CRM people, inventory items, fitness, work, journal
13. **Tag taxonomy to establish:**
    - `area/health`, `area/work`, `area/family`, `area/home`, `area/finance`
    - `type/log`, `type/hub`, `type/index`, `type/template`, `type/reference`
    - `status/active`, `status/archived`, `status/someday`

### Phase 4 — Quartz URL Sweep (Low Effort, High Value)
14. Sweep all notes missing the Quartz URL and add it in the standard format:
    `Quartz: http://192.168.1.223:8080/[path]`

### Phase 5 — Inventory Categorization (Optional Enhancement)
15. Add category subfolders to `10-Areas/Inventory/`:
    - `Firearms/`, `Camping/`, `Fitness/`, `Electronics/`, `Bags/`
    - Move inventory items accordingly and update the Inventory Index

---

## Files That Will Change

| File / Folder | Change |
|---|---|
| `Home/` | Move → `10-Areas/Home/` |
| `Resources/LLM-Wiki/` | Move → `30-Resources/LLM-Wiki/` |
| `Resources/` | Delete (empty after move) |
| `Templates/` | Delete (empty) |
| `10-Areas/Personal/` | Delete (empty) |
| `hermes-backups/` | Move out of vault |
| `Home/Hermes Memory.md` | Move → `30-Resources/Hermes/` |
| All `Home/` wikilinks | Update to new path |
| LLM-Wiki skill | Update path reference |
| Hermes memory | Update vault path references if changed |
| Most notes | Add Quartz URLs, add/standardize tags |

---

## Risks & Tradeoffs

- **Wikilink breakage:** Moving `Home/` is the highest-risk change. Obsidian uses shortest-path resolution for links, but explicit paths like `Home/Projects/Active/...` (used in Home Dashboard) will break and need updating.
- **Hermes automation:** Scripts and skills reference specific paths. After `Resources/LLM-Wiki/` moves, the LLM-Wiki skill must be patched.
- **Git history:** All moves should be done with `git mv` to preserve file history.
- **Quartz rebuild:** After structural changes, Quartz may need a full rebuild pass.
- **Hermes memory references:** The memory note mentions `/home/mike/vault/Resources/LLM-Wiki/` — needs updating after move.

---

## Recommended Execution Order

1. Phase 1 first — structural cleanup is the foundation; do with `git mv` in one commit
2. Phase 4 next — Quartz URLs are quick, high value, no risk
3. Phase 3 — tagging (can be done incrementally, new notes first)
4. Phase 2 — hub notes (can be done anytime, additive only)
5. Phase 5 — optional, do if inventory gets unwieldy

---

## Open Questions

- Do you want `Home/` to move inside `10-Areas/` or stay at root for quick access?
- Should `20-Projects/` hold cross-life projects (work + personal + home) or just non-home projects?
- Do you want a Finance area built out now, or just a placeholder?
- Should the hermes-backups folder move to `~/.hermes/backups/` or somewhere else entirely?

---

*Plan saved to: `/home/mike/vault/.hermes/plans/2026-04-12_234500-vault-organization.md`*
*Quartz: http://192.168.1.223:8080 (plan files not published)*
