# Design System — Convex

<!-- premium-web-design:design-system 1 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: Convex marketing library spec (colour + type), Convex dashboard captures at docs.convex.dev (density + chrome), convex.dev live pages (posture + accents) -->
<!-- Surface classes: 10 routes classified; density classes [F/S/D] assigned -->

## 1. Design Posture & Atmosphere

Convex is a reactive backend-as-a-service — TypeScript functions, a real-time database, and a
dashboard that watches deployments breathe. Its visual register is the **warm engineering
notebook**: a cream-paper canvas (#f6eedb on marketing surfaces, #f4f0ed inside the console)
printed with near-black warm ink, hairline borders instead of shadows, and a single
retro "gas-station stripe" ribbon (yellow #f3b01c, orange-red #ed3431, plum #8d2a76) that carries
the brand personality without ever leaking into interactive UI. The metaphor is **a flight log
printed on cream stock** — calm, factual, always current, with the brand's slogan "ALL GAS NO
BREAKAGES" acting as the masthead of a service whose whole promise is that sync never breaks.

After eight hours in the console nothing shouts. The dashboard chrome is a warm near-white
(#fefcfb) separated from the page canvas by hairlines, type sits at whisper-weights in one
grotesque family, and colour is rationed: one indigo filled action (#3f5294), one green
deployment-identity pill (#cbf0b8 wash with #0a602a ink), and functional reds reserved for
failures in the log stream. Live data arrives continuously and the interface treats that as
routine — logs append, queries re-run, history accrues — so motion is nearly absent and
freshness is communicated by content changing in place, not by animation.

Against the backend-category default of cold white consoles with blue primaries, Convex is
distinguishable on three axes: the canvas is warm (cream and beige-grays, never #ffffff page
backgrounds), the accent set is retro-print rather than tech-blue (gas yellow, plum, ember
orange as brand moments; indigo #3f5294 as the single product action colour), and identifiers
are monospace everywhere — table names, document IDs, function names, log lines — reinforcing
that everything on screen is a real, copyable artifact.

**Key Characteristics**
- Cream paper canvas on marketing (#f6eedb) and warm beige-gray canvas in the console (#f4f0ed); pure white is a card surface, never a page background.
- Dark surfaces are warm ink (#2b1d1d hero, #1c1a19 console dark canvas) — never pure black.
- One filled action colour per context: indigo #3f5294 in the console; dark ink buttons on cream marketing; gas yellow #f3b01c only as the announcement chip fill.
- Separation is 1px hairlines and surface steps; the console uses no card shadows, marketing uses at most one soft shadow on floating overlays.
- Monospace is a load-bearing voice: table titles, document IDs, function signatures, timestamps, and command chips are all mono.
- Log stream is the densest surface: ~28px rows, failure rows washed #fad4ca with #a83226 text, mono timestamps with millisecond precision.
- Deployment identity is a green outlined pill ("Development (Cloud)") with light-green fill #cbf0b8 — environment is always visible in the top bar.
- The gas-stripe ribbon (yellow/orange/plum) is a brand illustration device, never a UI fill.
- Radii are squared: 4px chips, 8px buttons and inputs, 12px cards, 16px command palette; nothing rounder.
- Command surfaces are first-class: "Find anything" with the slash shortcut, deployment switcher with arrow/enter/escape hints printed in the footer.
- Numbers that compare (durations, counts, call quotas) render in tabular figures, right-aligned in tables.
- Live data is the default state; Pause, not Refresh, is the log stream's control.

## 2. Token Architecture   ← normative

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value*, referenced only by L2:
  `cream.100` #fefcfb · `cream.200` #f6eedb · `cream.300` #f4f0ed · `cream.250` #f6f4f0 ·
  `paper.100` #ffffff · `ink.900` #1c1917 · `ink.850` #2b1d1d · `ink.800` #1c1a19 ·
  `ink.700` #262321 · `ink.500` #57534e · `ink.400` #79716b · `ink.300` #8a8378 ·
  `ink.200` #d6d0c8 · `gas.yellow` #f3b01c · `gas.red` #ed3431 · `gas.plum` #8d2a76 ·
  `indigo.600` #3f5294 · `indigo.300` #93a7e8 · `green.700` #0a602a · `green.200` #cbf0b8 ·
  `green.400` #6fce8f · `red.600` #a83226 · `red.200` #fad4ca · `red.300` #ff9d93 ·
  `amber.600` #8a5606 · `amber.400` #e5a020 · `amber.700` #b97308.
  Banned: `--card-bg`, `--tooltip-color` and any other `[component]-[prop]` naming — one value,
  many roles.
- **L2 Semantic** — role names (`surface.canvas`, `surface.raised`, `text.primary`,
  `accent.action`, `status.error`, `border.strong`, `focus.ring`). The only layer a component
  may consume.
- **L3 Component** — only for deliberate deviation; points at L2 or L1, never a raw value,
  never a sibling component's token: `log.row.failure-wash` → `red.200`; `deployment.pill-fill`
  → `green.200`; `deployment.pill-ink` → `green.700`; `pricing.badge-ink` → `amber.700`;
  `palette.overlay-radius` → 16px.

**Rules.** Every token has a determinable type or it is invalid; names are case-sensitive, free
of `$`, `{`, `}`, `.`; circular references (`a → b → a`) are an error. Every semantic token has
a value in **every** shipped mode — the console ships light and dark, so each L2 role below
carries both; a role with no dark value resolves to its light value and fails contrast. The
marketing gas accents (`gas.yellow/red/plum`) are illustration primitives: they are consumed
only by the `brand.ribbon` and `brand.chip` L3 tokens and never remap for dark mode because
they never sit on dark UI chrome — only on the fixed hero artwork.
Animatable tokens (only `focus.ring-width` and `overlay-opacity` animate) must be registered
with both `syntax` and `inherits`; `initial-value` must be computationally independent, so `%`
or `em` lengths are illegal there.

**Layer order (low → high)** `[reset] → [primitives] → [semantic] → [components] → [utilities]`.
Layer order beats specificity entirely, and an un-layered normal declaration outranks every
layered one — a stray un-layered rule in a component file would silently beat this whole
system, so anything a consumer must override without `!important` sits in the top layer.

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` | #f4f0ed | #1c1a19 | Console page canvas (beige-gray); marketing paper is `cream.200` #f6eedb via `brand.page` |
| `surface.raised` | #fefcfb | #262321 | Sidebar, top bar, table cards, settings cards — warm near-white, never #ffffff page-wide |
| `surface.overlay` | #fefcfb | #2a2523 | Command palette, dropdowns, cookie card; sits on a 40% ink scrim |
| `surface.inset` | #f6f4f0 | #201d1b | Table wells, log panel interior, mono command chips on dark |
| `surface.hover` | #f5f3ef | #302c29 | Row and list-item hover fill |
| `surface.selected` | #efece6 | #35302c | Active sidebar item ("Data", "Logs"), selected table row tint |
| `border.subtle` | #e5e0d8 | #3a3532 | Hairline row separators, card edges on light chrome |
| `border.strong` | #8a8378 | #57514c | Emphasised boundaries; ≥3:1 on `surface.raised` |
| `border.focus` | #3f5294 | #93a7e8 | Focus indicator, 2px; ≥3:1 on every surface it crosses |
| `accent.action` | #3f5294 | #5a6cb0 | The one filled action: Pause, Start Tutorial, primary buttons |
| `accent.onAction` | #ffffff | #ffffff | Text/icons on `accent.action` |
| `accent.subtle` | #e9ebf5 | #333c5e | Accent wash: selected-with-accent, focus-tinted chips |
| `text.primary` | #1c1917 | #f4f0ed | Headings and body ink |
| `text.secondary` | #57534e | #c9c2ba | Descriptions, helper text, table secondary columns |
| `text.tertiary` | #79716b | #948d86 | Meta, relative timestamps, placeholder text (house floor 3:1) |
| `text.disabled` | #a9a29b | #6b645e | Disabled labels; paired with a "why" on hover/focus |
| `status.success` | #0a602a | #6fce8f | Success log status, deployment ready; ships a check glyph |
| `status.warning` | #8a5606 | #e5a020 | Usage-limit warnings, quota thresholds; ships a triangle glyph |
| `status.error` | #a83226 | #ff9d93 | Failures; wash `red.200` behind failing log rows; ships an x-circle glyph |
| `status.info` | #3f5294 | #93a7e8 | Links, neutral notices, actor names in history |
| `brand.ribbon` | #f3b01c / #ed3431 / #8d2a76 | same | Gas-stripe illustration token — hero artwork and OG art only, never UI fills |
| `brand.chip` | fill #f3b01c, ink #2b1d1d | same | The AI Gateway announcement chip; the only yellow fill in any UI |

Dark canvas is **not** pure black: the console dark mode runs `ink.800` #1c1a19 canvas with
`ink.700` #262321 raised steps; marketing dark bands run warmer still (`ink.850` #2b1d1d).
Depth in dark comes from surface steps and 1px strokes, never shadows.

**Contrast gate** — computed with the WCAG 2.2 relative-luminance formula; unrounded; 4.499:1
fails. Body ≥4.5:1; UI boundaries and focus indicators ≥3:1; large text is ≥24px or ≥18.5px bold.

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| `text.primary` L | #1c1917 | `surface.canvas` L | #f4f0ed | 15.434:1 | 4.5 | PASS |
| `text.primary` D | #f4f0ed | `surface.canvas` D | #1c1a19 | 15.302:1 | 4.5 | PASS |
| `text.secondary` L | #57534e | `surface.canvas` L | #f4f0ed | 6.733:1 | 4.5 | PASS |
| `text.secondary` D | #c9c2ba | `surface.canvas` D | #1c1a19 | 9.833:1 | 4.5 | PASS |
| `text.tertiary` L | #79716b | `surface.canvas` L | #f4f0ed | 4.224:1 | 3.0 (house floor) | PASS |
| `accent.onAction` | #ffffff | `accent.action` L | #3f5294 | 7.379:1 | 4.5 | PASS |
| `accent.action` L on canvas | #3f5294 | `surface.canvas` L | #f4f0ed | 6.512:1 | 3.0 | PASS |
| `border.strong` L | #8a8378 | `surface.raised` L | #fefcfb | 3.667:1 | 3.0 | PASS |
| `border.focus` L | #3f5294 | `surface.raised` L | #fefcfb | 7.214:1 | 3.0 | PASS |
| `status.error` L on wash | #a83226 | `red.200` wash | #fad4ca | 4.870:1 | 4.5 | PASS |
| `status.error` L on raised | #a83226 | `surface.raised` L | #fefcfb | 6.520:1 | 4.5 | PASS |
| `status.success` L on wash | #0a602a | `green.200` wash | #cbf0b8 | 6.139:1 | 4.5 | PASS |
| `status.success` L on raised | #0a602a | `surface.raised` L | #fefcfb | 7.550:1 | 4.5 | PASS |
| `status.warning` L | #8a5606 | `surface.raised` L | #fefcfb | 6.013:1 | 4.5 | PASS |
| `status.info` L | #3f5294 | `surface.raised` L | #fefcfb | 7.214:1 | 4.5 | PASS |
| `status.error` D | #ff9d93 | `surface.overlay` D | #2a2523 | 7.566:1 | 4.5 | PASS |
| `status.success` D | #6fce8f | `surface.overlay` D | #2a2523 | 7.857:1 | 4.5 | PASS |
| `status.warning` D | #e5a020 | `surface.overlay` D | #2a2523 | 6.762:1 | 4.5 | PASS |
| `status.info` D | #93a7e8 | `surface.overlay` D | #2a2523 | 6.439:1 | 4.5 | PASS |
| `brand.chip` ink | #2b1d1d | `brand.chip` fill | #f3b01c | 8.515:1 | 4.5 | PASS |

## 4. Typography

**Families.** UI: a single neo-grotesque — GT America is the canonical marketing face
(weights 400/500/700, self-hosted, preloaded, fallback stack of system sans); the console
renders the same-genre neutral grotesque, so GT America is the family to license and Inter or
General Sans are the approved substitutes. Numeric/code: the platform monospace stack
(JetBrains Mono or IBM Plex Mono as substitutes) for document IDs, table names, function
signatures, timestamps, log lines, and command chips. *Monospace is for identifiers and code,
never a costume* — the one sanctioned flourish is that a data table's own name (e.g. a table
title in the data view) is set in mono because it names a code artifact.

**One ramp table per class, not one blended table.**

- **[F] Focused, 16px base** — settings forms, team settings, pricing, marketing prose:

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Display | 56px | 700 | 1.00 | -0.05em | lining | Hero headline ("ALL GAS NO BREAKAGES") |
| Heading | 40px | 700 | 1.10 | -0.025em | lining | Page hero on marketing |
| Section title | 32px | 700 | 1.15 | -0.01em | lining | "Choose Your Plan", "Realtime, all the time" |
| Body | 16px | 400 | 1.50 | 0 | lining | Marketing prose, settings descriptions |
| Label | 14px | 500 | 1.40 | 0 | lining | Form labels, nav links |
| Meta | 12px | 500 | 1.40 | 0.025em | lining | Eyebrows ("TRUSTED BY", "POPULAR") |

- **[S] Standard, 14px base** — console pages: data view, functions, files, schedules, history:

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Page title | 24px | 700 | 1.20 | -0.01em | lining | "Logs", "Deployment History"; table names set in mono at 22px/700 |
| Section title | 18px | 600 | 1.30 | 0 | lining | Card headings in settings |
| Body | 14px | 400 | 1.50 | 0 | lining | Console prose, empty-state copy |
| Row primary | 14px | 500 | 1.40 | 0 | tabular | Table/document primary cell |
| Row secondary | 13px | 400 | 1.40 | 0 | tabular | Timestamps' relative label, slugs |
| Stat value | 20px | 600 | 1.20 | 0 | tabular | Usage numbers, document counts ("3 documents") |
| Stat label | 11px | 500 | 1.30 | 0.05em | lining | Uppercase stat captions |
| Meta | 12px | 400 | 1.40 | 0 | lining | Breadcrumbs, deployment names |

- **[D] Dense, 12–13px base, data surfaces only** — log stream, data grid cells:

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Grid header | 12px | 500 | 1.30 | 0 | lining | `_id`, `description`, `Timestamp`, `Status` |
| Grid cell numeric | 13px mono | 400 | 1.40 | 0 | tabular | Durations ("17ms"), quotas ("1,000,000 calls / month") |
| Grid cell text | 13px | 400 | 1.40 | 0 | lining | Document field values |
| Log line (mono) | 13px mono | 400 | 1.45 | 0 | tabular | Timestamp + ID + status + function + message |
| Inline help | 12px | 400 | 1.40 | 0 | lining | Keyboard hints ("Navigate", "Select", "Close") |

Prose inside a dense screen still steps up to 14px [S].

**Invariants.** `tabular-nums` on every comparable value — durations, counts, quotas, IDs,
timestamps (mono figures are inherently tabular). Right-align numerics, left-align text, never
centre a numeric column. Fixed stepped sizes; no fluid type scaling. Measure ≤80 characters
(SC 1.4.8); 65–80ch [F/S], unconstrained [D] (log lines truncate with an ellipsis and expand on
selection).

## 5. Spacing Scale & Density Scales   ← two axes, never one

**Spacing base: 4px grid; 8px comfortable [F/S], 4px [D].** `space.0` 0 · `1` 4px icon-to-label ·
`2` 8px control padding [D] · `3` 12px cell padding [S] · `4` 16px card padding [S] / page
gutter · `6` 24px card padding [F] + section gap · `8` 32px section gap [S] · `12` 48px region
separation · `16` 64px marketing band padding. *No 17px. No 23px. If a layout needs an
off-scale value, the layout is wrong.*

**Density mode — the rescaling axis.** (Console measurements taken from 2x dashboard captures:
top bar ≈56px, sidebar items ≈36px, log rows ≈28px, data-grid rows ≈36px.)

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | Marketing pages, team settings, pricing, onboarding |
| `standard` | 36–40px | 14px | 12px | 24px | Data view grid (36px), projects list, history, functions |
| `dense` | 28px | 12–13px | 8px | 16px | Log stream, function-run tables |

- Density comes from **row height, column pruning and leading** — never from type too small to
  read. A 13px mono timestamp in the log stream is correct; the same numeral in a Focused
  settings form is a defect.
- **Never switch mid-page.** The console keeps Standard across a route and Dense only where the
  job is streaming data; switching across routes with different jobs is legitimate and reads as
  a different room.
- **Chrome follows rows.** The top bar (~56px) and the log toolbar share one rhythm; a 40px
  toolbar over 28px log rows is a rhythm break, so the log filter bar is compact (32px controls).
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40%. House heuristic, validated
  against the captures: the log stream sits near the dense floor, settings near the focused
  ceiling.

## 6. Radius Scale

`none` 0 · `xs` 4px — badges, tags, keyboard-hint chips, log ID chips · `sm` 6px — inline code,
table header sort affordances · `md` 8px — buttons, inputs, selects, command chips, the
deployment pill · `lg` 12px — cards, panels, table containers, pricing cards · `xl` 16px —
command palette overlay and the deployment-switcher dialog only · `full` 9999px — avatars,
status dots, the "POPULAR" flag's host chip outline on marketing.

**One radius per component family**, never mixed ad-hoc: every console button is 8px, every
console card is 12px, and nested radii obey `radius_inner = radius_outer − padding` (a 12px card
with 4px inset gets 8px children).

## 7. Elevation

**One strategy: flat-first with hairlines; shadows exist only on floating overlays.** Light
console separation comes from surface steps (#f4f0ed → #fefcfb) plus 1px `border.subtle`
hairlines; dark separation comes from luminance steps (#1c1a19 → #262321 → #2a2523) plus 1px
strokes — a drop shadow is invisible on near-black, so dark uses zero shadows. Levels, low →
high: **0** canvas (no shadow) · **1** card/panel (hairline only; no shadow) · **2** sticky top
bar (hairline + canvas step) · **3** command palette / dropdown (soft ambient shadow
0 8px 24px at 12% ink + `border.subtle` + `radius.xl`) · **4** dialog (same shadow, stronger
40% scrim). Marketing may carry the level-3 shadow only on the cookie-consent card and
hover-lifted pricing cards; the hero artwork is perfectly flat.

## 8. Motion

`instant` 0ms · `fast` 120ms ease-out (exits [D], log row removal) · `base` 180ms
decelerate ([D] entrances, palette open) · `slow` 240–300ms decelerate ([F/S] entrances,
dialogs, pricing card lift).

- Entrances decelerate, exits accelerate; symmetric ease-in-out on both directions is a defect.
- Animate `transform` and `opacity` only — never `width`, `height`, `top`, `left`.
- **Live data arrives without transition**: log lines, query results and history entries appear
  at `instant` because the product's whole point is that sync is already done; animating
  subscription updates would perform freshness the backend already delivered. Freshness is shown
  by content changing in place and the log Pause/Resume state, not by motion.
- No bounce on irreversible moments: deleting a deployment, disabling a usage limit, or a plan
  change confirms with a plain state change, never a spring.
- **Reduced motion is a real variant**, not animation removal everywhere: the palette/dialog
  open becomes a ≤150ms crossfade, pricing lift flattens; the continuously-updating log stream
  is unaffected (it was never animated). Scaling and panning of large objects are what must be
  neutralised.

## 9. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell/sidebar | [S] | Console project shell; team-settings shell | default, collapsed ("Collapse"), active item | Tab order top-down; "Find anything" via / | "Health, Data, Schema, Functions, Files, Schedules, Logs" |
| Top bar | [S] | Console (team + deployment pill + search); marketing (wordmark + nav + pills) | sticky, scrolled | skip-to-content first | "Find anything" with slash hint |
| Deployment pill | [S] | Development/Production; Cloud/local | current (outlined green), switcher trigger | opens switcher on Enter | "Development (Cloud)" |
| Data table | [S/D] | Data grid; documents panel; projects list | loading, empty, row-selected, sorted | arrows navigate cells; Space selects | "3 documents", "Create Table" |
| Log stream | [D] | All functions / single function; all types | live, paused, failure rows washed, empty | Auto-follow; Pause toggles | "Pause", "Clear Logs", "Filter logs…" |
| Filter/search bar | [S] | Table search; log filter; project search | filled, cleared, no-results | slash focuses from anywhere | "Search tables…", "Filter logs…" |
| Command palette | [F] | Deployment switcher; "Find anything" | open, no-results, current marked | arrows, Enter, Esc printed in footer | "Search for a deployment in…" |
| Stat tile | [S] | Usage cards, health metrics | ok, warning, over-limit | — | "Warning threshold on Database storage" |
| Drawer/inspector | [S] | Document editor; function detail | open, dirty, saving, error | Esc closes | "Edit document" |
| Dialog | [F] | Confirmations; create table/project | open, confirming, blocked | focus-trapped; Esc | "Create Table" |
| Plan/seat control | [F] | Pricing cards; usage limits | current, popular, upgradeable, blocked | whole card CTA | "$25 per developer/month" |
| Member row | [F] | Team members list | pending, active, owner, removed | row menu | "Developers (1–6)" |
| Audit entry | [S] | Deployment history feed | actor-linked, expandable detail | Enter expands | "Nicolas Etlin deployed functions" |
| Date-range chip | [S] | History filter | open, applied | calendar focus | "Mar 03, 2026 – Mar 10, 2026" |
| Keyboard-hint chip | [D] | Palette footer, floating fn button | static | decorative-but-labelled | "esc Close" |

Every fetching surface also designs: **loading** — skeletons matching final row geometry (the
data grid shows grey row bars at final 36px height, never a centred spinner on a blank page);
**empty** — names what is missing plus the CTA that fixes it ("Create Table" beside an empty
tables list); **error** — the failure row pattern from the log stream (wash + glyph + message +
duration) reused for any failed action; **offline/stale** — because the product is
real-time-by-default, a dropped subscription shows a "reconnecting" chip in the top bar and the
log stream keeps rendered rows visible with a stale watermark rather than blanking.

Contracts this table encodes: one primary filled CTA per view [F/S] (the log toolbar may pair
the primary Pause with icon actions); every icon-only control carries a label or tooltip; a
disabled control states why — the disabled Save on untouched settings reads as inactive, and
focus/hover explains "unchanged"; a button never changes width between idle and loading —
"Save" reserves its label space.

## 10. Light / Dark Strategy

- **Posture: C dual-parity.** The console ships authored light and dark themes (verified: the
  deployment-switcher capture exists in both); marketing is light-only with dark hero bands
  rendered from the same primitives (`ink.850` hero, `cream.200` paper) so the brand reads
  identically in both.
- **Mechanism:** semantic roles remapped per mode per the §3 table; no role absent in either
  mode. `brand.ribbon`/`brand.chip` are the only single-mode tokens (illustration-only, never on
  chrome), stated here as the sanctioned exception.
- **`color-scheme`** is set on the root so UA chrome, form controls and scrollbars follow the
  active mode; it repaints UA-provided parts of the canvas only.
- A `color-scheme` meta tag sits in the document head before the stylesheet to prevent a flash
  of the wrong scheme.
- **Dark is authored, not inverted:** dark keeps the warm hue family (#1c1a19/#262321/#2a2523 —
  brown-grays, never blue-blacks), raises border strength (`#3a3532` subtle vs light's
  `#e5e0d8` — a hairline that reads as delicate on cream would vanish on ink), keeps the green
  deployment pill's identity (light-green wash swaps to dark-green outline), and swaps status
  hues to lighter steps (#ff9d93, #6fce8f, #e5a020, #93a7e8) that hold ≥6.4:1 on the overlay
  step. `light-dark()` is progressive enhancement only.
- Org-tinting is out of scope for Convex; if a white-label need arises, colour tokens may change
  while radii, type sizes and layout stay frozen so a theme swap cannot move anything.

## 11. Density-Mode Strategy

- **Default mode per surface class:** marketing and settings = `focused`; console project pages
  (data, functions, files, schedules, history) = `standard`; log stream and function-run tables
  = `dense`. The boundary is the job: reading forms vs operating on records vs streaming events.
- **Mechanism:** a density marker on the application root rescales row height, cell padding,
  gutter and body size together as a token axis — spacing primitives do not change with screen
  size, only with the density axis. It is never a media query.
- **Container queries for reflow:** size queries measure the *content box*, so the data grid
  reflows to its panel, not the viewport; with no eligible container, `cq*` units silently
  resolve to small-viewport units, so they are never used where that fallback would be wrong.
- **Style queries** (`@container style(...)` on the density marker) compare *computed* values,
  so the density marker is registered with `syntax` and `inherits`.
- **Offer the switch as an accessibility affordance**, not a preference: a console-wide
  "compact tables" toggle exists because users with visual field loss need a mechanism to
  control layout density; it flips `standard` ↔ `dense` on data surfaces only.

## 12. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA for contrast of body text in the log stream
  (7.55:1 achieved) and for `text.primary` everywhere (15.3:1).
- **Target size:** ≥24×24 CSS px hard minimum (SC 2.5.8); 44px is the design target for primary
  marketing controls, console row-anchored controls are full-row; zoom does not excuse it.
- **Keyboard:** every function operable (SC 2.1.1) — the deployment switcher documents the
  contract in its own footer (arrows navigate, Enter selects, Esc closes); focus indicator
  visible (SC 2.4.7) as 2px `border.focus`, never `outline: none` without a stronger
  `:focus-visible` replacement; the focused row is never entirely hidden behind the sticky
  top bar (SC 2.4.11).
- **Contrast:** text ≥4.5:1 (all computed pairs in §3 pass); UI boundaries ≥3:1
  (`border.strong` 3.667:1). **Colour independence:** every status pairs colour with a glyph and
  text — failure rows carry an x-circle icon, the word "failure", and the duration; success
  carries the word "success" plus "(cached)" when applicable; deltas in history carry an
  arrow glyph plus old → new values.
- **Motion:** the reduced-motion variant from §8 applies to palette/dialog transitions.
- **Text:** ≤80-character measure, 1.5 leading on prose, 200% resize without horizontal scroll
  (SC 1.4.8); the log stream truncates instead of wrapping and expands on selection.
- **Semantics:** real interactive elements throughout; headings match visual rank (page title →
  section title); live regions announce subscription updates politely; the streaming log region
  is marked busy while paused-then-resuming flushes its buffer.
- **Contrast preference:** if `prefers-contrast: more` is honoured, `border.subtle` promotes to
  `border.strong`, `text.tertiary` promotes to `text.secondary`, and the failure wash drops to
  plain canvas with the glyph carrying the state (values: `no-preference`, `more`, `less`,
  `custom`).

## 13. Anti-Patterns

Product-calibrated; each carries the reason it was rejected *for this product*.

**Do**
- Keep every canvas warm: #f4f0ed console, #f6eedb marketing — the cream cast is the brand's
  first recognisable trait after the wordmark.
- Set identifiers (document IDs, function names, table names, timestamps) in mono and make them
  selectable — the console is a window onto code artifacts.
- Use exactly one indigo filled action per view; everything else is a hairline button.
- Wash failing log rows in #fad4ca and pair with the x-circle glyph and red text — three
  redundant signals, zero reliance on colour alone.
- Keep the green deployment pill visible in every console view; environment identity outranks
  tidiness.
- Reserve the gas-stripe ribbon for hero artwork, OG images, and the announcement chip.
- Print keyboard hints in palette footers — the interface teaches its own shortcuts.
- Match skeleton geometry to final rows (36px grid rows, 28px log rows) — reactive data arrives
  fast, and a spinner would be slower than the data.
- Use hairlines, not shadows, for console separation; the one sanctioned shadow is the palette
  overlay.
- Right-align every numeric column with tabular figures; durations and quotas compare visually.
- Keep log rows at 28px and prune columns (Timestamp, ID, Status, Function, Message) — density
  comes from layout, never from sub-12px type.

**Don't**
- Don't use the gas accents (yellow #f3b01c, red #ed3431, plum #8d2a76) as button fills, links,
  or status colours — they are illustration, not interaction; interaction is indigo.
- Don't put pure #ffffff page backgrounds anywhere; white is a card on a warm canvas.
- Don't use pure black #000000 for large surfaces; dark starts at #1c1a19 and hero dark at
  #2b1d1d.
- Don't introduce a second sans family or a rounded display face; one grotesque plus one mono.
- Don't exceed 16px radius or pill-ify console controls; the squared look is deliberate.
- Don't animate subscription updates — content changes in place; animating live data performs a
  delay the backend doesn't have.
- Don't render a "Refresh" control for reactive queries; the controls are Pause/Resume.
- Don't blank the log stream on reconnect; keep rendered rows with a stale watermark.
- Don't stack two filled CTAs side by side in the console (a filled action plus icon actions is
  the ceiling).
- Don't use placeholder text as the only label on the filter inputs; visible labels or labelled
  toolbars are required.
- Don't centre numeric columns or use proportional figures for durations and quotas.
- Don't import marketing dark-hero styling into console chrome; the console's dark mode is its
  own authored ramp, not the hero band.

## 14. Quick Reference & Verification Gate

**Colour (role → hex):**

| Role | Light | Dark |
|---|---|---|
| surface.canvas | #f4f0ed | #1c1a19 |
| surface.raised | #fefcfb | #262321 |
| surface.overlay | #fefcfb | #2a2523 |
| surface.inset | #f6f4f0 | #201d1b |
| surface.hover / selected | #f5f3ef / #efece6 | #302c29 / #35302c |
| border.subtle / strong / focus | #e5e0d8 / #8a8378 / #3f5294 | #3a3532 / #57514c / #93a7e8 |
| accent.action / onAction / subtle | #3f5294 / #ffffff / #e9ebf5 | #5a6cb0 / #ffffff / #333c5e |
| text.primary / secondary / tertiary / disabled | #1c1917 / #57534e / #79716b / #a9a29b | #f4f0ed / #c9c2ba / #948d86 / #6b645e |
| status.success / warning / error / info | #0a602a / #8a5606 / #a83226 / #3f5294 | #6fce8f / #e5a020 / #ff9d93 / #93a7e8 |
| brand.ribbon / brand.chip | #f3b01c·#ed3431·#8d2a76 / chip ink #2b1d1d | same (illustration only) |

**Type ramp (flat):** Display 56/700 · Heading 40/700 · Section 32/700 · Page title 24/700 ·
Stat value 20/600 tabular · Section [S] 18/600 · Body 16/400 [F] · Body 14/400 [S] · Row primary
14/500 · Row secondary 13/400 · Grid cell 13 (mono for IDs/logs) · Log line 13 mono ·
Grid header 12/500 · Meta 12 · Stat label 11/500 +0.05em.

**Spacing + radius (flat):** 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64; radius 4 / 6 / 8 / 12 / 16 /
full; density rows 28 [D] / 36–40 [S]; top bar 56px.

**Component → token map:**

| Component | Consumes |
|---|---|
| Top bar | surface.raised, border.subtle, text.primary, accent.action, brand.chip |
| Sidebar | surface.raised, surface.hover, surface.selected, text.primary/secondary, border.subtle |
| Deployment pill | deployment.pill-fill (green.200), deployment.pill-ink (green.700), border.subtle |
| Data grid | surface.raised, surface.inset, border.subtle, text.primary/secondary, text.tertiary |
| Log stream | surface.inset, log.row.failure-wash (red.200), status.error/success, text.primary |
| Command palette | surface.overlay, border.subtle, text.primary/secondary, focus.ring, radius.xl |
| Pricing card | surface.raised (cream.250 tint), border.subtle, pricing.badge-ink (amber.700), accent.action |
| Settings form | surface.raised, text.primary/secondary, border.strong (inputs), accent.action (Save) |
| History feed | surface.raised, status.info (actor links), text.secondary, border.subtle |

**Pre-ship checklist.** 1 Zero raw hex outside L1. 2 No token resolves to a component name.
3 Every contrast pairing computed, passing, unrounded. 4 Every semantic role has a value in
every shipped mode (light + dark console). 5 Every fetching surface has loading/empty/error/
offline specified. 6 Every component row lists disabled and loading states. 7 Row, header,
toolbar and pagination heights agree per surface. 8 Reduced-motion variant written for every
authored motion (palette, dialog, pricing lift). 9 Every control keyboard-reachable with a
visible focus indicator. 10 Dark authored, not filtered, with border strength exceeding light's.
11 No unoverridden stock-library default inside a committed surface. 12 Nothing came from a
marketing page into console chrome (and vice versa: no console indigo on marketing hero art).
