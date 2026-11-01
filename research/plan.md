# Research plan — `premium-web-design`

**Status:** planning only. No skill files written yet.

**Goal:** decide what a production-grade SaaS/web-product design skill must contain,
before writing any of it. Output = exhaustive *inventory* (what), not implementation (how).

## Explicitly out of scope this phase
- Writing SKILL.md, references, design-systems, scripts.
- Choosing final filenames / command names (proposed, but not committed).
- How the skill enforces rules (implementation detail).

## Sub-questions (parallel)

| ID | Question | Output file |
|---|---|---|
| R1 | Canonical anatomy of a production-grade web `DESIGN.md`; what belongs in platform-agnostic vs framework-variant files | `findings/01-design-md-anatomy.md` |
| R2 | Exhaustive taxonomy of B2B SaaS product surfaces (screen-by-screen) | `findings/02-saas-surface-taxonomy.md` |
| R3 | Catalog of real web/SaaS apps worth reverse-engineering, grouped by category, with what each uniquely teaches | `findings/03-app-catalog.md` |
| R4 | Web UX laws & enforceable specs: WCAG 2.2 AA, ARIA APG, Nielsen, Core Web Vitals, keyboard/focus, motion | `findings/04-ux-laws-standards.md` |
| R5 | Precise coverage delta vs Impeccable; adjacent skill landscape (what to borrow, what to skip) | `findings/05-impeccable-delta.md` |
| R6 | What a `design-systems/<app>/` folder must contain; evidence/screenshot practice; template to match | `findings/06-design-system-folder.md` |

## Effort level
Multi-part landscape, broad. 6 subagents, 10–15 searches each. One wave, then a targeted
second wave only for gaps.

## Working hypotheses to test, not assume
- H1: Premium-mobile-design's `init` derives `DESIGN.md` + `DESIGN-[framework].md` from the
  reference library — i.e. the web skill's `init` should do the same.
- H2: Impeccable's rules are marketing-biased; a density-classed floor must override several.
- H3: The largest uncovered surface is *data-dense product UI* (tables, consoles, settings IA),
  not visual polish.
