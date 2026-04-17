---
tags:
  - vault-cleanup
  - checklist
  - type/reference
frequency: monthly
owner: Michael
---

# Monthly Vault Hygiene Checklist

Purpose: keep the vault fast, link-safe, and easy to navigate in under 20 minutes.

## 1) Link health (5 min)
- [ ] Run broken-link audit and confirm total broken links = 0.
- [ ] If any breakage exists, fix path mismatches first, then missing-note links.

## 2) Tag hygiene (5 min)
- [ ] Confirm no untagged notes unless intentionally exempt.
- [ ] Keep frontmatter as source of truth.
- [ ] Normalize drifted tags to canonical set (family, fitness, health, work, home, finance, inventory, project, resource, journal).

## 3) Navigation hygiene (3 min)
- [ ] Check root `index.md` links resolve.
- [ ] Check `10-Areas/Areas Index.md` and `30-Resources/Resources Index.md` for dead links.
- [ ] Check `20-Projects/Projects Index.md` for stale references.

## 4) Inbox and reminders (3 min)
- [ ] Process `00-Inbox` items into Areas/Projects/Resources.
- [ ] Remove or complete past-due items in `Reminders.md`.

## 5) Commit hygiene (2-4 min)
- [ ] Commit cleanup changes with clear message.
- [ ] Push to `main`.

## Suggested monthly commit message
`chore: monthly vault hygiene (links, tags, navigation, reminders)`

Quartz: http://192.168.1.223:8080/30-Resources/Hermes/Vault-Cleanup/Monthly-Vault-Hygiene-Checklist
