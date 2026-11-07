# Design-review skill template — generate the project's own review gate

`init` Phase 6 (see `init.md`). The generated skill is the project's **executable, diff-centric design reviewer** at `.agents/skills/design-review/SKILL.md` — invoked as `/design-review` before any UI change ships, the way `/code-review` gates a code change. `DESIGN.md` stays the single source of truth; the generated skill is its auditor, never a second constitution.

A static guidelines document fails here for two reasons this skill's own rules forbid: duplication (the same rules in two places drift) and passivity (a document nobody loads enforces nothing). The generated skill instead encodes the *audit process* with this project's rules extracted verbatim from its confirmed `DESIGN.md`. Big teams converge on the same shape — deterministic token linting + semantic invariant audit + visual regression gate — rather than manual inspection alone [S1][S2][S3][S4].

> **House process, not sourced fact.** Phase 6, the generated skill's tiers, severity names, and the staleness stamp are this skill's construction. The tool mechanics they invoke (Stylelint token enforcement, Playwright snapshots and axe, Agent Skills progressive disclosure) are sourced below. As-of: 2026-11-07.

## When this runs

- **At the end of `init`**, after the specimen is confirmed (`specimen.md`). Only then are the invariants settled enough to encode. Generating it earlier freezes guesses as gates.
- **On any `DESIGN.md` A/B/C patch or `document` regeneration** — regenerate the skill in the same session, never as a follow-up. A skill generated from stale invariants audits against a product that no longer exists.
- **On demand** via the global `design-review [target]` command (`SKILL.md`): generate if absent, refresh if the stamp mismatches, run if current.

## Inputs the generator reads

`PRODUCT.md` (surface inventory, density context) · `DESIGN.md` §1 (posture, signature move, 3–5 invariants) · §2 (token layers) · §5 + §12 (density classes per route) · §10 (component inventory + states) · §13 (a11y commitments) · §14 (anti-patterns) · §15 (verification gate) · `DESIGN-[framework].md` when present (import boundary, validation commands) · the token source located in Phase 4. Read the applied tokens, not just the spec — the skill audits what shipped.

## The generated skill, in full

Write exactly one file at the project root: `.agents/skills/design-review/SKILL.md`. No sibling markdown. Ancillary files only when the budget below forces disclosure.

### Invocation (decided, not optional)

Model-invoked: omit `disable-model-invocation`. Two reasons, from the invocation trade-off: (1) the agent must reach it autonomously on every UI diff — a gate that fires only when a human remembers its name is not a gate; (2) human typing still reaches it — model-invocation adds discovery without removing user reach. The cost is the description's permanent context load; that cost is the price of an unfailing gate. Shared reference the generated skill needs lives in this skill's playbooks, reached by pointers — never copied into the project's skill.

### Frontmatter

```yaml
---
name: design-review
description: Audits UI diffs against DESIGN.md tokens, density invariants, WCAG AA, and rendered pixels before shipping. Run before opening or merging any pull request or commit touching frontend files, when reviewing UI changes, or when invoked as /design-review.
generated-from: DESIGN.md as-of YYYY-MM-DD
stamp: sha256:<hash of DESIGN.md at generation>
---
```

The description is the skill's context pointer: front-loaded leading words (`Audits`, `UI diffs`, `before shipping`), one trigger per branch (pre-PR UI change · reviewing UI changes · explicit `/design-review`), zero identity the body already carries. The stamp is the staleness guard: if `DESIGN.md` changes after generation, the pre-flight check below reports the mismatch and the skill regenerates rather than auditing against dead rules.

### Body structure — steps first, reference co-located, < 250 lines

House budget, not a standard: keep the generated `SKILL.md` under ~250 lines so the ordered steps stay legible. Exceed it and the reference buries the steps — attention thins and the agent starts skipping. Disclose overflow to `references/` behind a pointer only when a branch genuinely needs it; inline what every run needs.

**Step 0 — Staleness check.** Recompute the hash of `DESIGN.md` and compare to the frontmatter stamp. Done ⇔ hashes match, or the skill was regenerated this session. Mismatch → regenerate, then continue. Never audit against a mismatched stamp.

**Step 1 — Diff gate (fast exit).** Run `git diff --name-only origin/main...HEAD` plus `git status --porcelain`. Done ⇔ every touched file is classified as UI or non-UI. Zero UI files (`.tsx .jsx .vue .svelte .html .css .scss .ts` touching a component or route) → output `No UI changes detected. Skipping design review.` and stop. This step exists so a backend-only diff pays nothing.

**Step 2 — Tier 1: deterministic mechanical.** Run over touched files only: raw hex / `rgb(` / `hsl(` outside the L1 token file, `border-radius` literals outside the token file, raw `<button>/<input>/<select>/<dialog>` shadow primitives outside `@/components/ui/*`, `outline: none` without a `:focus-visible` replacement in the same file, `clamp(`/`vw` in `font-size`, `transition` on `width/height/top/left`, `python <skill-base-dir>/scripts/unslop_grep.py <changed paths>`, `npx impeccable detect <changed paths>` reconciled per the density override table in `craft-floor.md` (see `detector-integration.md`). Done ⇔ every hit is either fixed or recorded as a named, dated exception — a hit is a lead, not a verdict; confirm before reporting. Contrast of every touched token pair is measured, unrounded, in both modes — 4.499:1 fails 4.5:1, per W3C, never rounded [S5].

**Step 3 — Tier 2: project invariant audit.** Read the confirmed `DESIGN.md` sections verbatim; audit each touched route/component against them: density class declared for this route and held (`craft-floor.md`); accent budget for this viewport; one primary filled CTA per view; status never colour alone; component reuse — canonical `@/components/ui/*` primitives, no re-authored controls; every fetching surface carries loading (skeleton matching final geometry) / empty (actionable) / error (recoverable) / offline; §14 anti-patterns as named bans for this product. Done ⇔ every touched component carries a pass or a file:line finding against a named `DESIGN.md` section. A finding that cites no section is not a finding.

**Step 4 — Tier 3: rendered verification.** Headless Chromium (Playwright MCP when present, otherwise CLI/library — see `render-loop.md`): default light 1440px, populated with long realistic data, dark mode, 320 CSS px reflow, keyboard-only tab-through with visible focus, real empty/error/loading routes. Axe-core (`@axe-core/playwright`, WCAG A/AA/2.2 AA): critical and serious violations are a failed pass, not notes [S6]. CLS probe: largest layout-shift burst ≤ 0.1, reserved space for async regions [S7]. Done ⇔ screenshots captured for every modified route in both modes plus narrow width, keyboard walk recorded, axe clean at critical/serious, CLS within target — or the pass is reported as not run and why. Unrun is an open item, not a pass.

**Step 5 — Report and verdict.** Emit the severity table (§ below), then exactly one verdict line. Done ⇔ every finding names element, value, and fix — "improve spacing" is never a finding — and the verdict matches the rules mechanically.

### Severity and verdict (binary)

| Severity | Meaning | Examples |
|---|---|---|
| 🔴 **Blocker** | Breaks a committed invariant or a WCAG AA clause | Raw hex in feature code, contrast under threshold, target under 24×24 CSS px (SC 2.5.8) [S5], keyboard trap, broken 320px reflow, invariant violation from §1 |
| 🟠 **Major** | System drift, user-visible but survivable | Wrong density class, missing state, competing primary CTA, shadow primitive instead of a canonical primitive |
| 🟡 **Minor** | Off-scale but local | Spacing off the 4px scale, copy that drifts from voice, icon weight mismatch |
| 🟢 **Polish** | Last 10% of craft | Motion-curve asymmetry, hover nuance |

**Verdict:** any 🔴 or 🟠 → `VERDICT: CHANGES REQUIRED` (exit 1). Otherwise → `VERDICT: APPROVED TO SHIP` (exit 0). The weights behind these bands are this skill's judgement — the thresholds they reference are sourced.

### Writing rules the generated skill must obey

The generator writes the project's skill to the *Writing for Agents* standard. Every generated skill carries these properties; a generated skill missing one is regenerated, not patched:

- **Single source of truth.** Inlined rules name their `DESIGN.md` section. No rule is restated from this skill's playbooks — the generated skill points at `craft-floor.md`, `critique.md`, `render-loop.md`, `polish.md` and does not copy them. Copying is what makes fifty skills rot independently.
- **Positive target behaviour.** State what to do ("Use semantic tokens exclusively; import primitives from `@/components/ui/*`"), not what to avoid. A prohibition half-reads as an instruction to do the thing.
- **Completion criteria, checkable and exhaustive.** Each step above ends on a criterion an agent can mechanically verify. Vague bounds ("design looks premium") invite premature completion; the post-completion steps supply the pull, clarity supplies the resistance.
- **Leading words, reused, never re-explained.** `deterministic`, `verbatim`, `exhaustive`, `binary` — the generator uses the same tokens every time so the model anchors the same behaviour on later runs.
- **Pruning.** Delete every line that fails the no-op test — explanations of why contrast matters, CSS tutorials, filler. Keep commands, regexes, thresholds, the output template. Shorter survives; longer sediments.

### Wiring (the part that makes it fire)

- Append one line to the project's Design System Contract block (Phase 4, `init.md`): *Before proposing or submitting changes to UI files, run `/design-review` and resolve all Blockers and Majors.* This line is the context pointer that gives the skill its second trigger — the agent reaches it without a human typing its name.
- Recommend Tier 1 as a pre-commit hook (fast, under seconds) and Tiers 2–3 in CI on `pull_request` — the split big teams use so browsers never spin up for a backend diff. House recommendation, not a gate requirement.
- Record `Design-review skill generated: YYYY-MM-DD` in `DESIGN.md` §15 alongside the specimen confirmation.

### Completion gate for Phase 6

The generated skill exists at `.agents/skills/design-review/SKILL.md`, under the line budget, written to the rules above, with a stamp matching the confirmed `DESIGN.md` hash; the `AGENTS.md` contract line is in place; `DESIGN.md` §15 records the generation date. Then print the receipt and stop: `PRODUCT.md` · `DESIGN.md` · adapter or declined · token directory · `design-system.html` (confirmed) · `.agents/skills/design-review/SKILL.md` (generated) → *NEXT: run `/design-review` before shipping any UI change.*

### Output template for `.agents/skills/design-review/SKILL.md`

Every `[...]` below is replaced with the confirmed values from `DESIGN.md`. A generated skill contains zero unreplaced placeholders.

````markdown
---
name: design-review
description: Audits UI diffs against DESIGN.md tokens, density invariants, WCAG AA, and rendered pixels before shipping. Run before opening or merging any pull request or commit touching frontend files, when reviewing UI changes, or when invoked as /design-review.
generated-from: DESIGN.md as-of [YYYY-MM-DD]
stamp: sha256:[HASH_OF_DESIGN_MD]
---

# Design Review — [Product Name]

Diff-centric gate auditing frontend changes against confirmed `DESIGN.md` rules.

## Step 0 — Staleness check
Recompute `sha256(DESIGN.md)`.
Done ⇔ computed hash matches frontmatter `stamp`.
Mismatch → run `$premium-web-design design-review refresh` to regenerate this skill from current `DESIGN.md` invariants before continuing. Never audit against a mismatched stamp.

## Step 1 — Diff gate (fast exit)
1. Run `git diff --name-only origin/main...HEAD` (or target branch) and `git status --porcelain`.
2. Filter for UI files: `.tsx`, `.jsx`, `.vue`, `.svelte`, `.html`, `.css`, `.scss`, `.ts` touching components, styles, or routes.
Done ⇔ every touched file is classified.
Zero UI files → output `No UI changes detected. Skipping design review.` and exit 0.

## Step 2 — Tier 1: Deterministic mechanical audit
Run over touched UI files only:
1. **Token bypass:** zero raw hex (`#[0-9a-fA-F]{3,8}`), `rgb(`, `hsl(` outside token definitions.
2. **Radius literals:** zero hardcoded `border-radius` outside token definitions.
3. **Primitive imports:** all interactive elements imported from `@/components/ui/*`; zero raw `<button>`, `<input>`, `<select>`, `<dialog>` in feature code.
4. **Focus visible:** zero `outline: none` or `outline: 0` without a `:focus-visible` replacement in the same rule.
5. **Fluid font-size:** zero `clamp(` or `vw`/`vh` in `font-size`.
6. **Layout transitions:** zero `transition` on `width`, `height`, `top`, `left`, `margin`, `padding` (use `transform` / `opacity`).
7. **Slop sweep:** run `python <skill-base-dir>/scripts/unslop_grep.py [touched files]`. Zero ungrounded `0 0` box-shadows, zero gradient text, zero purple gradients, zero unverified buzzwords.
8. **Contrast:** measure contrast of every touched text/background token pair. Must meet ≥4.5:1 (body) or ≥3:1 (large text/borders), unrounded in both light and dark modes.
Done ⇔ every touched line is either clean or verified as a documented exception.

## Step 3 — Tier 2: Invariant audit against DESIGN.md
Verify against this project's confirmed invariants:
1. **Density class:** touched route matches assigned density class:
   - [Route / Surface pattern] → [Focused | Standard | Dense] (Row height: [X]px, Base font: [Y]px)
2. **Accent budget:** maximum [N] primary filled CTA per view. No competing filled buttons.
3. **Status independence:** every status indicator (success, warning, error, info) pairs colour with an icon, badge, or label. Never colour alone.
4. **Surface states:** every fetching surface implements loading (skeleton matching layout), empty (actionable with next step), and error (clear recovery action).
5. **Banned anti-patterns (§14):**
   - [Banned item 1 from DESIGN.md §14]
   - [Banned item 2 from DESIGN.md §14]
   - [Banned item 3 from DESIGN.md §14]
Done ⇔ every touched component checked against items 1–5 with file:line citation for any failure.

## Step 4 — Tier 3: Rendered verification
1. Start dev server or preview build.
2. Render modified routes in headless Chromium (Playwright / preview tools):
   - 1440px viewport, light mode, realistic content.
   - 1440px viewport, dark mode (verify authored dark ramp and contrast).
   - 320px viewport (verify reflow with zero horizontal scroll, SC 1.4.10).
   - Tab walk through all interactive elements (verify focus indicator visible on all elements, SC 2.4.7).
3. Run axe accessibility scan: zero critical or serious WCAG A/AA violations.
4. Verify CLS ≤ 0.1 on route load.
Done ⇔ screenshots captured or rendered pass completed with zero critical/serious issues.

## Step 5 — Verdict & Report
Format findings in table:
| Severity | File:Line | Issue | DESIGN.md Rule | Required Fix |
|---|---|---|---|---|

Severity weights:
- 🔴 **Blocker:** token bypass, contrast < threshold, target < 24x24px, keyboard trap, broken 320px reflow, invariant violation.
- 🟠 **Major:** wrong density class, missing loading/error/empty state, competing primary CTA, uncanonical shadow primitive.
- 🟡 **Minor:** off-scale spacing, copy drift, icon weight mismatch.
- 🟢 **Polish:** micro-motion curve, hover subtlety.

**Binary Verdict:**
- Any 🔴 Blocker or 🟠 Major → `VERDICT: CHANGES REQUIRED` (exit 1).
- Only 🟡 Minor or 🟢 Polish (or 0 findings) → `VERDICT: APPROVED TO SHIP` (exit 0).
````

## Not found

- **A sourced size cap for a generated agent skill.** The ~250-line budget is this skill's judgement — the Agent Skills spec supports progressive disclosure [S8] but publishes no line cap. Settled by: running the skill, not by citation.
- **A sourced staleness stamp.** Hashing `DESIGN.md` into the generated skill's frontmatter is borrowed from compiler-generator practice, not from any Agent Skills document. Settled by: none; it is cheap and its absence is the known rot path.
- **A sourced weighting for 🔴/🟠/🟡/🟢.** No standard assigns severity weights to design findings; the thresholds inside each band are sourced, the bands are judgement. Settled by: task-success data from real reviews.
- **A normative pre-ship gate above WCAG AA.** WCAG 2.2 Level AA is the floor; the artefact requirements in Tier 3 are this skill's construction.

## Sources

All accessed 2026-11-07. Parenthetical = what the citation carries in this file.

- **[S1]** **Stylelint enforcement of semantic tokens** — GitHub Primer (`@primer/stylelint-config`, backed by `primer/primitives` via Style Dictionary; rejects hardcoded hex, raw spacing, unapproved radii in CI). https://github.com/primer/stylelint-config
- **[S2]** **Tokens as the enforced vocabulary** — Shopify Polaris (`@shopify/polaris-tokens`, `@shopify/stylelint-polaris`; mandates `--p-*` token properties, flags deprecated tokens). https://www.npmjs.com/package/@shopify/polaris-tokens
- **[S3]** **Token lint plugins in consumer repos** — Atlassian Design System (`@atlaskit/eslint-plugin-design-system`, `@atlaskit/stylelint-design-system`; enforces `@atlaskit/tokens`, catches deprecated tokens). https://atlassian.design/
- **[S4]** **Visual regression as a merge gate** — Playwright, Visual comparisons (`expect(page).toHaveScreenshot()`, pixelmatch, `-diff.png` artefacts, Docker-container baselines for stable rendering). https://playwright.dev/docs/test-snapshots · Chromatic, UI Review (Storybook snapshot capture; blocks merge status checks until changes receive sign-off). https://www.chromatic.com/docs/ui-review/
- **[S5]** **WCAG 2.2 thresholds** — W3C / W3C WAI (SC 1.4.3 contrast 4.5:1 body / 3:1 large text, unrounded; SC 1.4.11 3:1 non-text; SC 2.5.8 target size 24×24 CSS px; 44×44 is SC 2.5.5 Level AAA, not AA). https://www.w3.org/TR/WCAG22/ · https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html · https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- **[S6]** **Axe-core in CI** — Playwright, Accessibility testing (`AxeBuilder` with `wcag2a`/`wcag2aa`, `@axe-core/playwright` integration). https://playwright.dev/docs/accessibility-testing
- **[S7]** **CLS and Web Vitals gates** — Google / web.dev (CLS ≤ 0.1, LCP ≤ 2.5 s at the 75th percentile; reserve space for async regions; `layout-shift` PerformanceObserver). https://web.dev/articles/vitals · https://web.dev/articles/cls · Lighthouse CI. https://github.com/GoogleChrome/lighthouse-ci
- **[S8]** **Agent Skills progressive disclosure** — Agent Skills specification (skill = folder + `SKILL.md`; only `name` + `description` loaded at discovery, body on trigger, ancillary files on demand; placement at `.agents/skills/<name>/` or `.claude/skills/<name>/`). https://agentskills.io · Anthropic, Effective context engineering for AI agents. https://www.anthropic.com/news/effective-context-engineering-for-ai-agents
- **Writing discipline applied throughout** — Context pointers, the two loads, information hierarchy and progressive disclosure, completion criteria, leading words, negation, pruning and the no-op test: this skill's `writing-for-agents` reference (house framework). Context engineering, generally: Martin Fowler. https://martinfowler.com
- **Token schema validation in CI** — Terrazzo DTCG CLI (`tz check`: schema, unresolved aliases, circular references). https://terrazzo.dev
- Phase shape, A/B/C options, adapter phase, gate, `PRODUCT.md` schema — house process adapted from `premium-mobile-design` `references/init.md`.
