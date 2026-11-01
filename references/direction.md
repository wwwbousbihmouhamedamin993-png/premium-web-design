# Direction — mood archetype, signature move, category refusal, invariants

A technically compliant screen that looks like every other console is a failure of art direction.
This product's floors produce correct output; direction is what makes it recognizable when the logo is
removed — by its spatial geometry, typographic voice, and interaction mechanics.

**Relationship to `signature-moves.md`:** the postures there (*restrained instrument*, *committed
brand*, *configurable workbench*) decide **which production apps inform the execution** — what to
steal decisions from, and how many. This file decides **what this product itself asserts** — its
archetype, its authored move, its refusals, its invariants. Posture is citation; direction is
commitment. A product picks its posture in Phase 2 and authors its direction in the same interview.

**House process.** The archetype taxonomy and authoring recipe are this skill's process, adapted from
`premium-mobile-design` `references/direction.md` and re-aimed at pointer/keyboard product surfaces —
the haptics column is gone, and nothing here assumes a touch gesture.

**Done when:** `DESIGN.md` §1 records the mood archetype, the signature move (named, with its trigger,
its keyboard path, and its fallback), both refusal tiers, and 3–5 invariants — and the specimen
(`specimen.md`) renders all of it.

---

## 1. The mood archetypes

Do not invent atmosphere from scratch. Ground the product in one dominant archetype (or a declared
80/20 blend) and let it constrain tokens across the stack:

| Archetype | Core metaphor | Canvas & surfaces | Type voice | Radius & shape | Density posture | Pointer & keyboard kinetics |
|---|---|---|---|---|---|---|
| **Utilitarian** | Cockpit instrumentation (Linear, Grafana) | Matte neutral, hairlines, zero glow | Mono or condensed sans, strict tabular figures, Major Second (1.125) | Sharp, 4–6px | Leans Dense | Instant snap (80–140ms); keyboard-first; command palette as the front door |
| **Instrument** | Calibrated meter (Stripe dashboard) | Tinted white, level-based contrast, one restrained accent | Neutral sans, strict role ramp, tabular everywhere | 6–8px, one per element type | Standard → Dense | Hover reveals, 140–200ms decelerate; scrubbing on charts |
| **Clinical** | Diagnostic monitor (observability consoles) | Near-black or paper white; status illumination only, zero ambient glow | Neutral grotesque, oversized numerals | Uniform 8px | Standard | Critically damped 150–240ms; precision hover; no bounce anywhere |
| **Editorial** | Working document (Notion) | Paper tint or ink noir, hairline rules | Book sans/serif pairing, generous leading | Low, 4–8px | Standard, Focused on reading surfaces | Quiet crossfades 200–350ms; caret and selection are the primary feedback |
| **Workshop** | Creative bench (Figma, Retool) | Neutral chrome that recedes; content full-bleed | Compact UI sans | 4px chrome, canvas handles unrounded | Variable by surface | Direct manipulation; interruptible springs only where the user drags |
| **Vault** | Ledger and lock (billing, fintech consoles) | Light ledger canvas, dense tabular grids | Strict tabular figures; numerals are the display face | 4–8px | Dense | Deliberate: 250–300ms on `Decide` actions, no playfulness on irreversible paths |
| **Committed** | Branded instrument (Slack, PostHog) | Warm or saturated tint bounded by cost — density intact | Product voice in display moments, neutral in data | One shape personality, larger radii allowed | Standard | Underdamped springs on non-destructive feedback only |

The archetype names the temperature; it never overrides the density class a surface needs — a
Committed product still runs Dense tables at Dense rules.

---

## 2. The signature move

A signature move is not a logo, a mascot, or an accent color. It is an **authored interaction or
structural mechanic** that solves the product's primary job memorably — and on the web it must
survive three constraints mobile never faced: it works from the keyboard, it survives
`prefers-reduced-motion` with a declared static substitute, and it never blocks the data.

### The five mechanical classes (pointer/keyboard re-aim)

1. **Surface morph.** A container adapts between states with momentum instead of navigating — the
   command palette that grows from a trigger chip into a full modal; a filter bar that expands in
   place into a query builder. The spatial model persists; the route never changes.
2. **Continuous scrub & crossfilter.** Pointer position binds 1:1 to the data view — dragging one
   chart's range live-filters the others (Grafana, Linear insights). No modal round-trips for
   previewable state.
3. **State compression.** Dense multi-signal data compressed into one glanceable artifact that
   expands in place — a usage meter that opens into the quota breakdown, a status ring that opens
   into the incident list.
4. **Direct-manipulation canvas.** The surface is the object — drag to arrange (Retool, Notion
   blocks, Figma). Interruptible multi-axis physics, spatial persistence, keyboard equivalents for
   every drag.
5. **Provenance.** Every consequential action produces a tangible, inspectable record — the deploy
   log streaming as it runs, the invoice preview beside the change that caused it, the audit entry
   inline in the row. Trust made visible; the web's honest replacement for a physical metaphor.

### The six-step authoring recipe

1. **Pinpoint the climax friction loop** — the 30 seconds where the product delivers its value
   (query → insight, draft → shipped, incident → resolved).
2. **Select the material metaphor** from the archetype — cockpit, meter, ledger, bench.
3. **Map continuous 1:1 input.** Pointer/keyboard position binds directly to surface state; eliminate
   modal round-trips for anything previewable.
4. **Tune the physics honestly.** Springs only where the user drags; fixed durations from
   `radius-motion-tokens.md` for everything event-triggered. Animate from the current value, carry
   velocity, never lock input mid-transition.
5. **Anchor with keyboard detents.** Every state of the move is reachable by keyboard, and the move
   has a named static form under reduced motion.
6. **Enforce exit symmetry.** Enter and exit paths mirror so the spatial model persists.

**Done when:** the move is named, documented with trigger, keyboard path, spring-or-duration choice,
and reduced-motion fallback — and it appears where the product's job is hardest, not on a marketing
screen inside the app (`atmosphere.md` governs that exception).

---

## 3. The category refusal protocol — two tiers

### Tier 1: structural refusal — the hidden workflow assumption

Category leaders monetize an unstated belief about how the work is done; the sharpest structural bet
is against that belief, because the leader cannot copy it without cannibalizing revenue. Write it
into `PRODUCT.md` and `DESIGN.md` §1.3:

> *"Category leaders monetize [the hidden workflow assumption]. We structurally refuse it by
> [the counter-bet], which incumbents cannot copy without breaking their revenue model."*

Product-shaped examples of the shape (not prescriptions):

- Analytics suites monetize dashboard-count and seat gates → the counter-bet makes *exploration*
  free-form and charges for collaboration or compute instead — so the UI is a query surface, not a
  report shelf.
- Project tools monetize per-seat access → the counter-bet prices the workspace flat — so guest and
  viewer surfaces are first-class, not locked.
- Ops tools assume dashboard-first consumption → the counter-bet makes conversation or triage the
  entry point — so the shell's first surface is a queue, not a chart wall.

### Tier 2: visual refusal — the category's cliché skin

| Category | Predictable cliché (the trap) | The intentional refusal |
|---|---|---|
| **AI / devtools** | Near-black canvas, purple/violet gradients, sparkle icons, empty chatbot box | Monochrome instrument precision; inline citation proof; command-first entry |
| **Analytics / BI** | Stat-card wall, pie charts, a rainbow per report | One dominant metric; ordinal single-hue ramps; sparklines in context |
| **Project / workspace** | Kanban clone, pastel label soup, emoji section headers | Density-honest tables; neutral labels; typographic hierarchy doing the grouping |
| **Fintech / billing** | Floating card stacks, green money accents, coin icons | Ledger tabular density; hairline rules; accent marks intent, never wealth |
| **Admin / settings** | Nested card walls, toggle-per-row, modal mazes | Settings as IA — sections, search, keyboard reach, inline edits |

`craft-floor.md`'s Refuse list enforces the mechanics of these bans; this table is where the product
**declares** which ones it is deliberately standing against, and what it borrows instead — often from
an unrelated category (the ledger discipline of accounting software; the restraint of aviation
instrumentation).

---

## 4. Brand invariants — 3–5, machine-enforced

Invariants are non-negotiable aesthetic axioms enforced across every surface, every state, and every
agent turn. Strong web examples:

1. **The corner rule** — one radius per element type, from the token scale; nested corners derived
   (`radius-motion-tokens.md`).
2. **The accent ceiling** — accent appears ≤ 2× per viewport [F/S], reserved for the primary action
   or active filter.
3. **The depth law** — elevation is surface steps and 1px hairlines, never shadows on dark.
4. **The numeric standard** — every comparable numeral renders `tabular-nums`, right-aligned.
5. **The keyboard guarantee** — every primary flow is keyboard-complete, and focus is never removed.

**Machine enforcement is the web's advantage — use it.** Invariants survive multi-agent code
generation only when a linter can fail the build:

- `stylelint-declaration-strict-value` on color, radius, and spacing declarations — raw hex, off-scale
  radii, and magic spacing fail CI (the same gate `tokens.md` expresses as greps).
- ESLint `no-restricted-syntax` for the interaction bans the product adopts (e.g. `alert(`,
  `confirm(`).
- The `DESIGN.md` §1.4 invariant list names the rule that enforces each invariant. An invariant with
  no enforcing check is an aspiration, not an invariant.

**Done when:** the 3–5 invariants are locked in `DESIGN.md` §1.4, each with its enforcing linter rule,
checked in `critique.md`, and demonstrated on the specimen page.

---

## 5. Workflow integration

- **`init` Phase 2** — the direction interview item asks: archetype (or 80/20 blend), signature move
  (one of the five classes, authored through the recipe), both refusal tiers, invariants. Written
  into `DESIGN.md` §1 before tokens are derived.
- **`specimen`** — the specimen page renders §1: the archetype's tokens, the signature move
  demonstrated live (with its static fallback), the refused cliché shown as a struck-through don't.
- **`screen` / `critique`** — the brief names the archetype's execution and the invariants at stake;
  critique scores the distinctiveness tell: *"Could this screen belong to a competitor with the logo
  covered? Naming a rival for this screen is a failure."*

## Sources

| Claim | Source | Label |
|---|---|---|
| Archetype taxonomy, two-tier refusal protocol, signature-move authoring, invariant discipline | House process adapted from `premium-mobile-design` `references/direction.md` (mobile retains the original, touch/haptic-oriented) | House |
| Posture system (which apps inform execution) | `signature-moves.md` — this skill | House |
| Density classes outrank archetype expression | `craft-floor.md` Density classes | House |
| `stylelint-declaration-strict-value` (restrict values to tokens/variables) | stylelint community plugin docs | Verified |
| ESLint `no-restricted-syntax` (ban syntax patterns) | ESLint user guide | Verified |
| Slop detector tell: "could this screen belong to a competitor with the logo covered?" | `critique.md` distinctiveness section — this skill | House |
