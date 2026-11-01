# Init — capture product truth in PRODUCT.md, derive DESIGN.md + an optional adapter, apply tokens

`init` establishes the durable foundation of a logged-in B2B SaaS web product. Four deliverables:

1. **`PRODUCT.md`** — users, jobs, purpose, positioning, usage scene, constraints, brand. Web-specific:
   the **commercial model** (plans / seats / usage), **multi-tenancy** and **auth model**, because on
   web those three decide what the hardest screens look like.
2. **`DESIGN.md`** — a **framework-neutral** spec: token architecture, colour roles, type ramp,
   spacing *and* density scales, radius, elevation, motion, component inventory with states,
   light/dark strategy, density-mode strategy, a11y commitments, anti-patterns. No framework syntax.
3. **`DESIGN-[framework].md`** — **optional**, only when the host has a stack to bind to.
4. **Project source code** — generated tokens materialised into the project's real token source and
   validated by its own typecheck/lint/build.

These files are the single source of truth downstream. **Do not rush or cap the interview.** They are
written to the project root per invocation — never cached or shared across projects. A fifth artifact —
`design-system.html`, the **specimen** (Phase 5) — is disposable and derived from the applied tokens;
it gates scope but is never a source of truth.

> **House process, not sourced fact.** Phase order, the A/B/C options and the adapter phase are this
> skill's own process, adapted from `premium-mobile-design`'s `init`. Every CSS and WCAG fact below is
> cited inline and collected under `## Sources`. As-of: 2026-10-05.

## Communication protocol

Kickoff banner before the first question: `[1/5] Product Truth → PRODUCT.md (users, plans, auth)` ·
`[2/5] Design Specification → DESIGN.md` · `[3/5] Adapter (optional)` · `[4/5] Token Application →
live CSS, wired` · `[5/5] Specimen Review → design-system.html confirmed`. State that it is
deliberately thorough and takes multiple rounds. Phase headers:
`─── [1/5] PRODUCT TRUTH ───`, `[2/5] DESIGN SPECIFICATION ───`, `[3/5] IMPLEMENTATION ADAPTER ───`,
`[4/5] TOKEN APPLICATION & VALIDATION ───`, `[5/5] SPECIMEN REVIEW ───`, each with one sentence on
what it decides. Every question carries one sentence of rationale: *"A per-seat plan turns seat count
into a `Decide` surface, so cost and effective date must be legible before the click — a screen
archetype, not a badge."*

## 1. Load current state

Whenever `DESIGN.md` exists, ask before touching it:
> **A — Keep as-is.** Skip Phase 2, continue to the next missing phase.
> **B — Patch.** Re-derive only the named sections; leave the rest verbatim.
> **C — Re-interview.** Full Phase 2, replace the file. Use when product, plans or density model have
> materially changed.

**State matrix.** Neither exists → 1→2→3→4. Only `PRODUCT.md` → confirm, then 2→3→4. Only `DESIGN.md` →
ask A/B/C, run Phase 1 for `PRODUCT.md`, continue. Both, no adapter → ask A/B/C, generate if wanted.
All exist → ask what is stale; never overwrite a confirmed foundation without explicit intent.
Incumbent UI with established tokens → offer `document` instead, running Phase 1 alongside it.

## 2. Phase 1 — Product interview → `PRODUCT.md`

**Step 1: pre-interview repo exploration.** Don't make the user repeat settled facts. Read the
framework marker, the token source, existing docs, routes/entities, and the billing-entitlement code
paths. Framework + adapter target (house detection table): `next.config.*` / `app/`+`next` → Next.js
`DESIGN-nextjs.md` · `remix.config.*` / `@remix-run/*` → Remix · `astro.config.*` → Astro ·
`svelte.config.*` → Svelte · `nuxt.config.*` or `vue` → Vue/Nuxt · `angular.json` → Angular ·
`vite.config.*`+`solid-js` → Solid · `vite.config.*`+`react` → React · `@import "tailwindcss"` →
Tailwind v4 (note version) · `.css` entry only → plain CSS. Ambiguous, hybrid or greenfield without
markers → ask. Token sources to check: `tailwind.config.*`, `@theme` blocks, `tokens.css` / `:root`
custom properties, `tokens.json` (DTCG), `theme.ts`, a component-library `createTheme`, Storybook
globals.

**Step 2: interview rounds — skip anything the repo answered.**

1. **Users & context.** Who, on what hardware, for how long? A support agent on 1280×720 with two
   monitors and Slack behind the browser is a different product from a finance lead on a 32-inch 4K
   display. Secondary users — your customer's auditor, your own sales engineer?
2. **Job-to-be-done & positioning.** The primary job, and the mechanism a competitor cannot copy.
3. **Usage scene.** Session length, interruption pattern, notification load, ambient light,
   multi-monitor vs single window, whether the same route is used on a phone browser. *Why: an
   eight-hour session argues for a persistent shell and low chrome; a forty-second session argues for
   a Focused single-column entry and an immediate primary action.*
4. **Commercial model.** **Plans, seats, or usage — which is billed and which two are merely shown?**
   Trials? Proration? Downgrades that lose data? *Why: this decides how many `Decide` surfaces exist
   and whether the plan page is an overview or a checkout.*
5. **Multi-tenancy.** One workspace per user or many? Org → project → environment nesting? Who
   switches, how often? Data residency? *Why: the workspace switcher is shell chrome on every route
   and one of the most-used controls in the product.*
6. **Auth model.** Password / magic link / SSO (SAML, OIDC)? MFA? Session lifetime? Do admins and end
   users share routes? *Why: sign-in is Focused density and is often a marketing-owned template; a
   mismatch there reads as broken product.*
7. **Key workflows.** The 3–5 indispensable flows; bulk ops, imports/exports, scheduled jobs,
   real-time updates, third-party embeds.
8. **Constraints.** Browser floor, offline behaviour, data volume per screen, latency budget,
   compliance boundaries, accessibility targets.
9. **Voice & brand.** Copy tone; existing name, logo, palette, tokens — anything already committed
   that the design must not contradict.

**Step 3: write `PRODUCT.md`.** `# Product` + `<!-- premium-web-design:product-schema 1 -->` +
these sections: **Stack & Surfaces** (framework, rendering, routing, browser floor) · **Users**
(primary/secondary, hardware, sessions, jobs) · **Product Purpose** (what, why, success criteria) ·
**Positioning** · **Usage Scene** · **Commercial Model** (billing unit, trials, proration, downgrades,
hard limits) · **Multi-Tenancy** (model, nesting, switching frequency, residency) · **Auth & Access
Model** (credentials, SSO, MFA, session lifetime, roles) · **Capabilities and Constraints** ·
**Localization** (locales, RTL, expansion budget) · **Brand Commitments** · **Product Principles**
(3–5 that settle trade-offs) · **Accessibility & Inclusion** (WCAG target, keyboard model, density
control, screen-reader posture). Confirm before Phase 2.

## 3. Phase 2 — Design interview → `DESIGN.md`

**Reference selection.** Match the product against `design-systems/` categories (`devtools`,
`observability`, `data-bi`, `backend`, `crm`, `support`, `workspace`, `creative`, `identity`,
`fintech`, `commerce`, `cloud`). Present 2–3 posture-fit apps — *restrained instrument* (Linear,
Stripe, Grafana, Vercel) or *committed brand* (Figma, Retool) — one sentence each. Load at most 3
`design-systems/*/DESIGN.md` files. Then load in parallel: `craft-floor.md`, `tokens.md`.

**The web-specific interview items.** A mobile interview has none of these; ask all of them.

1. **Density class declaration — first, not last.** Every type and spacing rule inherits it.

   | Class | Surfaces | Base body | Row height | Measure |
   |---|---|---|---|---|
   | **Focused** | Auth, onboarding, checkout, single-form flows, settings detail | 16px | — | 60–70ch, centered |
   | **Standard** | Project home, card+list feeds, record detail | 14–15px | 40–44px | 65–80ch |
   | **Dense** | Data tables, admin consoles, observability, logs, trading, IDE-like | 12–13px | 28–32px | full-width |

   Boundaries are this skill's judgement (`craft-floor.md`), not a vendor or standards figure.
2. **Surface-class inventory.** Enumerate every route *class* and give each a density class and a mode
   (Operate / Read / Decide / Support). Minimum set: app shell, index/list, record detail, create/edit,
   settings & admin, members & invitations, roles & permissions, audit log, billing & plans, invoices,
   usage & limits, onboarding, empty/error/expired states. *Why: an unclassified route is where density
   drift enters.*
3. **Colour architecture.** Canvas + surface steps + hairlines; accent reserved for high-intent
   actions; status system with a non-colour glyph each; accent budget per class. Never colour alone —
   NN/g: "Do not rely only on color to communicate" (`visual-hierarchy.md`).
4. **Type ramp.** Role-based steps per class; the monospace rule for identifiers and figures; tabular
   figures mandated for anything comparable.
5. **Spacing scale *and* density scale** — two axes, not one. See `tokens.md`.
6. **Light/dark posture.** **A** light-only (cheapest, legitimate for a day-office form product) ·
   **B** dark-only (justify it — an all-shift ops console in a dark room is the honest case) ·
   **C** dual parity *(recommended default)*: two complete semantic ramps, `prefers-color-scheme` plus
   a persisted manual toggle, **both modes getting their own surface ramp, border strength and shadow
   treatment**, `color-scheme` set so UA chrome follows, and `<meta name="color-scheme">` before the
   stylesheet to avoid a flash of the wrong scheme (MDN, `color-scheme`) · **D** org-tinted: dual
   parity plus a per-tenant accent confined to colour tokens, with geometry, type and layout frozen so
   a swap cannot move anything. Do **not** make `light-dark()` primary — MDN records it as **Baseline
   2024, newly available**.
7. **Component inventory + states.** For each real component (data table, filter bar, row action menu,
   drawer, command palette, stat tile, plan card, member row, audit entry): default / hover /
   focus-visible / active / selected / disabled / loading / error, plus keyboard behaviour and the
   exact microcopy for primary actions.
8. **Elevation strategy.** Choose **one**: shadow-based (light) or tonal-surface-step + 1px hairline
   (dark). Never mixed.
9. **Motion.** Durations per class; decelerate-in / accelerate-out asymmetry; `transform`/`opacity`
   only; a real `prefers-reduced-motion` variant — MDN names scaling and panning large objects as the
   triggers, so target those rather than disabling animation wholesale.
10. **Density mechanics.** Row height drives density, not font size. Carbon's productive/expressive
    type-set split is the vendor precedent: 14px productive base for product spaces, 16px expressive
    where condensation would distract.
11. **Accessibility commitments.** WCAG 2.2 AA target; SC 2.5.8 target size ≥24×24 CSS px or the
    spacing exception; focus indicator meeting 3:1 non-text contrast; all functionality
    keyboard-operable (SC 2.1.1); the reduced-motion variant; density control offered as an
    accessibility affordance — W3C's note on SC 2.5.8 endorses exactly this.
12. **Anti-patterns.** Copy the project's own bans from `craft-floor.md` **Refuse** into `DESIGN.md`,
    product-calibrated, each with its reason.
13. **Art direction.** Ground the product in one mood archetype (or a declared 80/20 blend), author
    the signature move — one of the five pointer/keyboard classes, with trigger, keyboard path, and
    reduced-motion fallback — declare both refusal tiers (the category's hidden workflow assumption;
    the category's visual cliché), and lock 3–5 brand invariants, each with its enforcing linter rule.
    Full protocol: `direction.md`. Written into `DESIGN.md` §1 — the specimen will render it, and
    `critique.md` will hold screens to it.

## 4. Phase 2 output — `DESIGN.md`

Write to the project root using the exact section list in
[`init-design-template.md`](init-design-template.md). Depth parity is mandatory: real hex, exact px,
contrast ratios **computed** per pairing, per-class ramps, every section populated, no `[placeholder]`
surviving. > **Strict neutrality:** *what the design is* — hex, px, ratios, curves. No selectors, no
component-library prop names, no framework syntax.

## 5. Phase 3 — optional adapter `DESIGN-[framework].md`

Skip entirely for a greenfield project with no stack, or when the user wants the spec to stay the only
artefact. When generated, it is short: where Layer 1–2 live in the host stack; why mode and density
live on `:root`/`[data-theme]` with `@theme inline` bridging (v4 `@theme` is top-level and cannot nest
in a selector or media query); which committed surface each spec component binds to; which stock
defaults must be overridden (a stock default inside a committed surface is a lapse —
`component-consistency.md`); wiring and validation commands. Every value traces to `DESIGN.md`.

## 6. Phase 4 — apply tokens to the project

1. **Locate the token source** via Step 1. Reuse an existing convention silently; stop and ask if two
   compete (monorepo, `styles/` vs `theme/`, library theme plus own CSS).
2. **Inventory every file** to be created or modified before writing.
3. **Merge, never blind-overwrite.** Diff existing files against generated tokens, merge additively,
   flag naming conflicts.
4. **Wire the modes:** `<meta name="color-scheme">` before CSS; `color-scheme` on `:root`;
   `[data-theme]` attributes; persistence of the manual theme choice.
5. **Validate** with the project's own typecheck/lint/build. Zero errors before exiting.

> **Canonical rule:** after Phase 4 the project's token files are canonical. Future token changes are
> made in code and documented back into `DESIGN.md` — never by regenerating markdown over live code.

## 7. Phase 5 — the system specimen (stop-and-ask)

Render the whole design language as one reviewable page: `<project>/design-system.html`, from
[`templates/system-specimen.html`](templates/system-specimen.html) and the **applied** token source
(Phase 4 made it canonical — the specimen validates what actually shipped, not just the spec). The
rules, the coverage mandate, and the stop-and-ask live in [`specimen.md`](specimen.md); the short
version:

- **Item-level coverage.** Every `DESIGN.md` §1–§14 item owns a section — density classes side by
  side, the component variant × state matrix, the keyboard/focus strip, both appearances, data
  furniture, the declared atmosphere with its static fallback, the signature move, the struck
  anti-patterns. An item that does not apply carries an explicit `n/a — reason`.
- **Token-faithful.** Every rendered value is a `var()` from the emitted token block; the greps run
  over the page itself.
- **Stop and ask.** Present the page and ask what should change before any screen is built. On an
  `init` project, no build command runs until the user confirms. Record
  `Specimen confirmed: YYYY-MM-DD` in `DESIGN.md` §15.

## 8. Completion gate

Both documents written and confirmed; adapter written or explicitly declined; every `DESIGN.md` section
populated — token architecture, spacing *and* density, component states, light/dark, density mode,
a11y, anti-patterns; every contrast pairing **computed, not asserted, and unrounded**; tokens
materialised, wired, 0 tooling errors; **specimen built, grep-clean, and confirmed by the user**;
files written to *this* project root. Then print the receipt:
`PRODUCT.md` · `DESIGN.md` · `DESIGN-[framework].md` · `[token directory]` · `design-system.html
(confirmed YYYY-MM-DD)` · `Tooling Status: 0 errors`
→ *NEXT: run `$premium-web-design screen <name>`*.

## Not found

- **A primary-source per-surface density detector.** The three classes are this skill's judgement; no
  vendor maps a route to a class. Settled by: observing production surfaces and naming the boundary
  case that broke each guess.
- **A standards basis for a density-mode token model.** W3C endorses *providing* a density control and
  publishes no token model. The `:root`/`@property` pattern in `tokens.md` is house mechanism.
- **Commercial-model, multi-tenancy and auth interview items** are house process adapted from the
  mobile skill; no external standard prescribes them.

## Sources

All accessed 2026-10-05. Parenthetical = what the citation carries in this file.

- **Design Tokens Format Module 2025.10** — W3C Design Tokens Community Group. (Groups arbitrary; tools SHOULD NOT infer type/purpose; `$type` determinable or invalid; names case-sensitive excluding `$`/`{`/`}`/`.`; circular refs MUST error.) https://www.designtokens.org/TR/2025.10/format/
- **Registering custom properties in CSS** — MDN, Mozilla. (`@property` needs `syntax` AND `inherits`; `initial-value` computationally independent, no `%`/`em`; registered interpolates, unregistered animates discretely; `inherits:false` narrows recalculation.) https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Properties_and_values_API/Registering_properties
- **`color-scheme`** — MDN, Mozilla. (Repaints UA chrome only; does not theme the document; `<meta name="color-scheme">` before CSS to avoid a flash; `light-dark()` Baseline 2024 newly available.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme
- **`prefers-color-scheme`** — MDN, Mozilla. https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme
- **`prefers-reduced-motion`** — MDN, Mozilla. (Baseline widely available; scaling and panning large objects named as vestibular triggers.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
- **`@layer`** — MDN, Mozilla. (Order beats specificity entirely; unlayered normal declarations outrank layered ones; `!important` reverses.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer
- **`@container`** — MDN, Mozilla. (Baseline widely available; content-box measurement; `cq*` falls back to small-viewport units with no eligible container; style queries compare computed values.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@container
- **Theme variables** — Tailwind CSS v4, Tailwind Labs. (`@theme` top-level only; `@theme inline` when a theme variable references another.) https://tailwindcss.com/docs/theme
- **Theming** — shadcn/ui. (One base `--radius` with derived `calc()` multipliers; one base `--spacing: 0.25rem` driving the scale.) https://ui.shadcn.com/docs/theming
- **WCAG 2.2** — W3C / W3C WAI. (SC 2.1.1; SC 2.5.8 target size — 24x24 CSS px or the spacing exception, zoom does not excuse it, density control endorsed; SC 1.4.11 3:1 non-text contrast; SC 1.4.8 measure ceiling.) https://www.w3.org/TR/WCAG22/ · https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html · https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html · https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html
- **Typography: type sets** — Carbon Design System, IBM. (Productive 14px base vs expressive 16px base.) https://carbondesignsystem.com/elements/typography/type-sets/
- **Visual Hierarchy in UX** — Nielsen Norman Group, Kelley Gordon, 2021-01-17. ("Do not rely only on color to communicate visual hierarchy.") https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
- Phase shape, A/B/C options, adapter phase, gate, `PRODUCT.md` schema — house process adapted from `premium-mobile-design` `references/init.md`.
