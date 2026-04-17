---
title: Wiki Schema
tags:
  - resource
created: 2026-04-07
updated: 2026-04-07
type: schema
---

# Wiki Schema

## Domain
Personal knowledge base — persistent, compounding knowledge across any domain:
AI/ML, productivity, health, finance, technology, science, culture, personal projects, and more.

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `transformer-architecture.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`

## Frontmatter
  ```yaml
  ---
  title: Page Title
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  type: entity | concept | comparison | query | summary
  tags: [from taxonomy below]
  sources: [raw/articles/source-name.md]
  ---
  ```

## Tag Taxonomy
Tags are added as they become useful. Initial set:

- People: person, creator, scientist, engineer
- Organizations: company, lab, open-source, institution
- Technology: ai, ml, software, hardware, tool, framework, language
- Concepts: methodology, technique, pattern, principle, trend
- Domains: health, finance, science, culture, productivity, personal
- Content types: comparison, timeline, controversy, prediction, tutorial, review

New tags must be added to this section before use. No freeform tags.

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines — break into sub-topics with cross-links
- **Archive a page** when its content is fully superseded — move to `_archive/`, remove from index

## Entity Pages
One page per notable entity (person, org, product). Include:
- Overview / what it is
- Key facts and dates
- Relationships to other entities ([[wikilinks]])
- Source references

## Concept Pages
One page per concept or topic. Include:
- Definition / explanation
- Current state of knowledge
- Open questions or debates
- Related concepts ([[wikilinks]])

## Comparison Pages
Side-by-side analyses. Include:
- What is being compared and why
- Dimensions of comparison (table format preferred)
- Verdict or synthesis
- Sources

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report
Quartz: http://192.168.1.223:8080/30-Resources/LLM-Wiki/SCHEMA
