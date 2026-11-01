# Design System — Hasura

<!-- premium-web-design:design-system 1 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: Hasura open-source console theme source (colour + shell — ladder rung 2: official repo theme files read verbatim), hasura.io 2026 brand CSS (brand accent + display type — ladder rung 2), official docs console screenshots + 1440px captures (density + chrome sampling — ladder rung 3 grounding). Rung 1 (sibling catalogs) missed: no prior hasura spec existed. -->
<!-- Surface classes: 12 routes classified; density classes [F/S/D] assigned -->

## 1. Design Posture & Atmosphere

Hasura's product surface is the **Hasura console** — the admin UI that ships with the open-source
GraphQL engine and Hasura DDN: a data browser, an API Explorer hosting GraphiQL, a permissions
editor, metadata/Actions/Remote Schemas builders, and monitoring. The console reads as an
**engine-room control board bolted to a paper workbench**: one 50px bar of dark slate chrome
(`#43495A`) carrying uppercase letter-spaced navigation, framing a pale blue-gray work canvas
(`#F8FAFB`) where dense forms and data tables do their work. The emotional register is utilitarian
and slightly retro — a 14px humanist sans (Gudea), tiny bold uppercase section labels, a hard 4px
yellow underline under the one active tab. After eight hours of permission editing, nothing glows,
nothing bounces, nothing tries to be liked; the eye is spent on table geometry and GraphQL syntax,
not on chrome.

Against its category defaults (Supabase's saturated green glassmorphism, Firebase's pastel cards,
Neon's dark-first glow), Hasura sits deliberately **drier and flatter**: white cards on a
blue-tinted paper canvas, hairline borders, shadows reserved for genuine overlays, and exactly one
yellow signal per viewport. The visual metaphor is a **"ledger sheet under a steel ruler"** —
precise columns, mono-spaced identifiers, status inks that carry a glyph, and a chrome bar that
stays dark and quiet so the yellow action state is unmistakable.

The 2026 brand layer around the product (hasura.io marketing, DDN pricing) is a different room:
near-black navy (`#000615`), a lime accent (`#B6FC34`), a blue action (`#3970FD`), Funnel Display
headlines. This spec keeps those two worlds separated on purpose — brand accent lives on marketing
surfaces; the console's working palette is slate, yellow, teal, and GraphQL magenta. One wordmark,
two climates.

**Key Characteristics**

- Chrome is a single 50px dark-slate top bar (`#43495A`); it never scrolls and never changes height
  across routes. A secondary sub-sidebar (white) carries in-section tabs (GraphiQL / REST).
- Exactly **one yellow fill per viewport** [S]: the primary button (`#FEC53D` fill, `#43495A`
  label). The active nav tab is a **4px yellow underline** (`#FFC627`) plus yellow text on slate —
  an indicator, not a fill.
- Everything on the chrome bar is **uppercase, bold, 14px, +1px letter-spacing**, text `#DEDEDE`
  (6.673:1 on `#43495A`). Section micro-labels on light canvas repeat the same treatment at 12–14px.
- Body base is 14px Gudea on `#F8FAFB` canvas; ink `#4D4D4D` (8.074:1). The console declares a
  1350px minimum content width — desktop-first, no responsive collapse.
- Code, GraphQL syntax, and identifiers are monospace (Overpass Mono); the GraphQL magenta
  `#E535AB` is reserved for GraphQL-domain decoration (explorer keywords, heart-branding), never
  body text on white (3.868:1 — non-text only).
- Teal `#1CD3C6` and cyan `#33E0FF` are **tier accents for the slate chrome** (enterprise/Pro
  signals, focus on dark surfaces): 4.780:1 and 5.663:1 on `#43495A` — legal there, banned on light
  canvas.
- The modernized control layer uses a slate-indigo fill `#314158` with white label (10.357:1) for
  quiet primary controls where yellow would be too loud.
- Data-table hover is a **pale green wash `#EBF7DE`** — the one warm-cool crossover the legacy
  palette allows; selection pairs it with a left ink bar, never color alone.
- Sub-sidebar active section header sits on a **pale amber wash `#FFF3D5`** (sampled from shipped
  console), keeping the yellow family continuous from chrome to content.
- Radius family is deliberately small: 2–5px on interactive surfaces, pills only for badges.
  Nothing in the product exceeds 8px except full-round pills.
- Shadows exist on light overlays only, in three verified strengths; dark mode replaces shadow with
  surface steps plus 1px keylines (zero shadows).
- Status inks are deepened for AA text (`#1F7A33` success, `#92400E` warning, `#C62F2B` error,
  `#16697F` info) while the legacy glyph fills (`#5CB85C`, `#F0AD4E`, `#D9534F`, `#5BC0DE`) survive
  only as non-text dots and icons at ≥3:1 against their washes.
- Dark mode (`#0F172A` canvas, `#E2E8F0` ink) is an authored variant of the modern component layer
  — declared per appearance so native controls follow; yellow actions shift to `#F8C533`.
- Numerals that compare — response time, response size, row counts, versions — are tabular figures,
  right-aligned; a monitoring stat reads "348 ms / 184 bytes" the way a ledger reads a total.

## 2. Token Architecture

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value*, referenced only by L2:
  `slate.800 #43495A`, `slate.700 #515766`, `slate.600 #767E93`, `ink.700 #4D4D4D`,
  `ink.800 #272B36`, `ink.500 #909090`, `chrome.text #DEDEDE`, `steel.600 #3B5F93`,
  `yellow.500 #FFC627`, `yellow.600 #FEC53D`, `yellow.400 #F8C533`, `amber.wash #FFF3D5`,
  `teal.500 #1CD3C6`, `cyan.400 #33E0FF`, `indigo.900 #314158`, `indigo.700 #526C91`,
  `indigo.950 #2C3C52`, `indigo.wash.100 #F5F9FE`, `indigo.wash.200 #EAF3FF`,
  `magenta.500 #E535AB`, `magenta.700 #C2268F`, `green.wash #EBF7DE`, `green.700 #1F7A33`,
  `green.500 #5CB85C`, `amber.text #92400E`, `amber.500 #F0AD4E`, `red.700 #C62F2B`,
  `red.500 #D9534F`, `blue.ink #16697F`, `blue.400 #5BC0DE`, `paper.50 #F8FAFB`,
  `paper.100 #F2F2F2`, `paper.200 #F8F8F8`, `line.subtle #DAE0E8`, `line.divider #E5E5E5`,
  `line.chrome #788095`, `night.canvas #0F172A`, `night.raised #1E293B`, `night.overlay #334155`,
  `night.ink #E2E8F0`, `night.ink.2 #94A3B8`, `night.ink.3 #64748B`, `night.line #64748B`,
  `night.line.strong #CBD5E1`, `lime.brand #B6FC34`, `cobalt.brand #3970FD`,
  `void.brand #000615`.
  Banned: component-derived names (`--header-bg`, `--tooltip-color`) — one value, many roles.
- **L2 Semantic** — the only layer a component may consume: `surface.canvas`, `surface.raised`,
  `surface.overlay`, `surface.inset`, `surface.hover`, `surface.selected`, `chrome.bar`,
  `chrome.hover`, `chrome.text`, `chrome.indicator`, `border.subtle`, `border.strong`,
  `border.focus`, `accent.action`, `accent.onAction`, `accent.indicator`, `accent.wash`,
  `control.fill`, `control.onFill`, `tier.accent`, `graph.accent`, `text.primary`,
  `text.secondary`, `text.tertiary`, `text.disabled`, `status.success`, `status.warning`,
  `status.error`, `status.info` (+ `.wash`, `.glyph` siblings per status), `brand.canvas`,
  `brand.accent`, `brand.action`.
- **L3 Component** — only for deliberate deviation, pointing at L2/L1: `console.topBar`,
  `console.navActive`, `console.subSidebar`, `table.rowHover`, `table.headerRow`,
  `explorer.panel`, `explorer.tabRow`, `permission.editorCell`, `stat.tile`, `toast.surface`.
  Never a raw value; never a sibling component's token.

**Rules.** Every token has a determinable type or it is invalid; names are case-sensitive and free
of `$`, `{`, `}`, `.`; circular references are an error. Every semantic token carries a value in
**both** shipped modes (light, dark) — a role without a dark value would resolve to its light value
and fail contrast. Animatable tokens are registered with both a syntax descriptor and an inherits
flag, or the registration is invalid; initial values must be computationally independent (no
percentage or font-relative units). Layer order, low → high: `reset → primitives → semantic →
components → utilities`; layer order beats specificity entirely, and an un-layered stray rule in a
component file would outrank this whole system — anything a consumer must override without forced
priority sits in the top layer.

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` / `surface.raised` / `surface.overlay` / `surface.inset` | `#F8FAFB` / `#FFFFFF` / `#FFFFFF` / `#F2F2F2` | `#0F172A` / `#1E293B` / `#334155` / `#0B1220` | canvas · cards · flyouts · wells; dark overlay keylined |
| `surface.hover` / `surface.selected` | `#EBF7DE` / `#FFF3D5` | `#1E293B` / `#263244` | row hover (pale green) · selected/active-section wash (pale amber) |
| `chrome.bar` / `chrome.hover` / `chrome.text` / `chrome.indicator` | `#43495A` / `#515766` / `#DEDEDE` / `#FFC627` | same in both modes | 50px top bar; hover fill; nav text; 4px active underline |
| `border.subtle` / `border.strong` / `border.focus` | `#DAE0E8` / `#43495A` / `#314158` | `#334155` / `#64748B` / `#33E0FF` | 1px hairlines; decorative / boundary ≥3:1 / focus ≥3:1 |
| `accent.action` / `accent.onAction` / `accent.wash` | `#FEC53D` / `#43495A` / `#FFF3D5` | `#F8C533` / `#43495A` / `#2B2515` | one fill per viewport [S]; label on fill 5.672:1 |
| `control.fill` / `control.onFill` | `#314158` / `#FFFFFF` | `#526C91` / `#FFFFFF` | quiet primary controls (modern layer) |
| `tier.accent` (on chrome only) / `graph.accent` | `#1CD3C6` + `#33E0FF` / `#E535AB` | `#1CD3C6` + `#33E0FF` / `#E535AB` | enterprise/Pro signals on slate; GraphQL-domain decoration |
| `text.primary` / `text.secondary` / `text.tertiary` / `text.disabled` | `#4D4D4D` / `#667182` / `#909090` / `#B0B5BC` | `#E2E8F0` / `#94A3B8` / `#64748B` / `#475569` | ink ramp; tertiary is meta-only at the 3:1 house floor |
| `status.success` / `status.warning` / `status.error` / `status.info` | `#1F7A33` / `#92400E` / `#C62F2B` / `#16697F` | `#D0E7B8` / `#EEE0BD` / `#F7D3D3` / `#BEDDEA` | text on `.wash` siblings `#E6F2E7` / `#FDF3E1` / `#FBEAEA` / `#E3F1F6` (dark toast pairs `#192614` / `#2B2515` / `#2D1A1A` / `#11242D`) |
| `brand.canvas` / `brand.accent` / `brand.action` | n/a (marketing only) | `#000615` / `#B6FC34` / `#3970FD` | 2026 brand layer; never enters the console |

Dark canvas is **not** pure black: it is slate `#0F172A` stepped through `#1E293B` (raised) and
`#334155` (overlay). Depth in dark comes from those surface steps plus 1px keylines
(`border.strong #64748B`, 3.751:1 on canvas) — never shadows; `#1E293B` against `#0F172A` is only
1.220:1, so a dark raised card without its keyline is a defect.

**Contrast gate — computed ratios, unrounded. 4.499:1 fails. Body ≥4.5:1; UI boundaries and focus
indicators ≥3:1.** Tertiary text is held to a 3:1 house floor (inactive-interface text is exempt
from the 4.5 body rule; muted text stays legible anyway).

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| `text.primary` | `#4D4D4D` | `surface.canvas` | `#F8FAFB` | 8.074:1 | 4.5 | PASS |
| `text.primary` | `#4D4D4D` | `surface.raised` | `#FFFFFF` | 8.977:1 | 4.5 | PASS |
| `text.secondary` | `#667182` | `surface.canvas` | `#F8FAFB` | 4.720:1 | 4.5 | PASS |
| `text.secondary` | `#667182` | `surface.raised` | `#FFFFFF` | 4.915:1 | 4.5 | PASS |
| `text.tertiary` (meta only) | `#909090` | `surface.raised` | `#FFFFFF` | 3.193:1 | 3.0 house floor | PASS |
| `text.tertiary` (meta only) | `#909090` | `surface.canvas` | `#F8FAFB` | 3.049:1 | 3.0 house floor | PASS |
| `chrome.text` | `#DEDEDE` | `chrome.bar` | `#43495A` | 6.673:1 | 4.5 | PASS |
| `accent.onAction` | `#43495A` | `accent.action` | `#FEC53D` | 5.672:1 | 4.5 | PASS |
| `accent.onAction` | `#43495A` | `accent.action` dark | `#F8C533` | 5.568:1 | 4.5 | PASS |
| `accent.indicator` | `#FFC627` | `chrome.bar` | `#43495A` | 5.711:1 | 3.0 (non-text) | PASS |
| `control.onFill` | `#FFFFFF` | `control.fill` | `#314158` | 10.357:1 | 4.5 | PASS |
| `text.secondary` dark | `#94A3B8` | `surface.canvas` dark | `#0F172A` | 6.963:1 | 4.5 | PASS |
| `text.primary` dark | `#E2E8F0` | `surface.raised` dark | `#1E293B` | 11.866:1 | 4.5 | PASS |
| `border.strong` | `#43495A` | `surface.canvas` | `#F8FAFB` | 8.575:1 | 3.0 | PASS |
| `border.strong` dark | `#64748B` | `surface.canvas` dark | `#0F172A` | 3.751:1 | 3.0 | PASS |
| `border.focus` dark | `#33E0FF` | `chrome.bar` | `#43495A` | 5.663:1 | 3.0 | PASS |
| `status.success` | `#1F7A33` | success wash | `#E6F2E7` | 4.684:1 | 4.5 | PASS |
| `status.warning` | `#92400E` | warning wash | `#FDF3E1` | 6.443:1 | 4.5 | PASS |
| `status.error` | `#C62F2B` | error wash | `#FBEAEA` | 4.700:1 | 4.5 | PASS |
| `status.info` | `#16697F` | info wash | `#E3F1F6` | 5.408:1 | 4.5 | PASS |
| `status.success` dark | `#D0E7B8` | toast dark | `#192614` | 11.895:1 | 4.5 | PASS |
| `status.warning` dark | `#EEE0BD` | toast dark | `#2B2515` | 11.633:1 | 4.5 | PASS |
| `status.error` dark | `#F7D3D3` | toast dark | `#2D1A1A` | 11.939:1 | 4.5 | PASS |
| `status.info` dark | `#BEDDEA` | toast dark | `#11242D` | 11.202:1 | 4.5 | PASS |
| `tier.accent` (text use) | `#1CD3C6` | `chrome.bar` | `#43495A` | 4.780:1 | 4.5 | PASS |
| `graph.accent` (non-text) | `#E535AB` | `surface.raised` | `#FFFFFF` | 3.868:1 | 3.0 non-text | PASS |
| `graph.accent` (text, dark) | `#E535AB` | `surface.canvas` dark | `#0F172A` | 4.615:1 | 4.5 | PASS |

Rejected pairings, computed and refused: legacy secondary `#767E93` on canvas = 3.875:1 (demoted to
decorative dividers, replaced by `#667182`); legacy tertiary `#909090` intent at `#9CA3AF` on white
= 2.539:1 (refused); white label on legacy success fill `#5CB85C` = 2.481:1 and danger `#D9534F`
= 3.962:1 (glyph fills may not carry labels; deep inks or dark chips instead); `#606060` on
`#FFC627` banner = 4.000:1 (refused; `#43495A` on `#FFC627` = 5.711:1 is the shipped pairing);
cyan `#33E0FF` on light canvas = 1.514:1 (never on light).

## 4. Typography

**Families.** UI: **Gudea** (400 regular, 700 bold; 300/600 declared for the modern layer), loaded
from a public font host rather than self-hosted, not preloaded, fallback stack 'Helvetica Neue',
Helvetica, sans-serif. Numeric/code: **Overpass Mono** (300–700) for GraphQL syntax, endpoints,
headers, hashes, raw timestamps, versions. Expressive/secondary: **Poppins** (400, 600) for
illustrative moments in onboarding. *Monospace is for identifiers and code, never a costume — a
JSON payload in Gudea is a defect; a table column header in mono is also a defect.*

The marketing brand layer uses **Funnel Display** for display headlines, **Inter** for body, and
**Fira Code** for inline code — deliberately confined to `brand.` surfaces; it never appears inside
the console.

**One ramp table per class, not one blended table.**

- **[S] Standard — console default, 14px base:**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Page title | 20px | 700 | 1.3 | 0 | — | "Add a New Table", section landing titles |
| Section title | 14px | 700 | 1.4 | +1px, uppercase | — | "CONFIGURE FIELDS", sidebar heads |
| Body (1.5) | 14px | 400 | 1.5 | 0 | — | form help, descriptions, `#4D4D4D` |
| Row primary | 14px | 400 | 1.45 | 0 | — | data-table cell text |
| Row secondary | 12px | 400 | 1.45 | 0 | — | sub-text under row primary, `#667182` |
| Stat value | 16px | 700 | 1.3 | 0 | tabular | response time/size, counts |
| Stat label | 12px | 700 | 1.3 | +0.5px, uppercase | — | "RESPONSE TIME", "RESPONSE SIZE" |
| Meta | 12px | 400 | 1.4 | 0 | tabular when compared | version strings, timestamps, `#909090` |

- **[D] Dense — GraphiQL, browse-rows, logs, metadata grids, 12–13px base, data surfaces only:**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Grid header | 12px | 700 | 1.4 | +0.5px, uppercase | — | "ENABLE / KEY / VALUE" column heads |
| Grid cell text | 13px | 400 | 1.5 | 0 | — | request-header keys, permission cells |
| Grid cell numeric | 13px | 400 | 1.5 | 0 | tabular | row counts, limits |
| Log line (mono) | 13px | 400 | 1.6 | 0 | tabular | event/log rows, editor lines |
| Inline help | 12px | 400 | 1.45 | 0 | — | "(You can add foreign keys later as well)" |

Prose inside a dense screen (a permissions explanation, an error body) still steps up to 14px/1.5.

- **[F] Focused — onboarding overlays, welcome/upgrade dialogs, 16px body:**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Display | 25px | 400 | 1.25 | 0 | — | welcome-panel greeting |
| Heading | 20px | 700 | 1.3 | 0 | — | dialog titles |
| Body | 16px | 400 | 1.5 | 0 | — | dialog/step copy |
| Label | 14px | 700 | 1.4 | 0 | — | form labels inside dialogs |
| Meta | 12px | 400 | 1.4 | 0 | — | fine print, dismiss hints |

**Invariants.** `tabular` figures on every comparable value — response times, sizes, deltas, counts,
versions, IDs. Right-align numerics, left-align text, never centre a numeric column. Fixed stepped
sizes only; no fluid interpolation between steps. Measure ≤80 characters: 65–80ch in [F/S] prose
panels, unconstrained inside editor panes [D].

## 5. Spacing Scale & Density Scales

**Spacing base: 4px grid; 8px comfortable [F/S], 4px [D].** `space.0` 0 · `1` 4px icon-to-label ·
`2` 8px control padding [D] · `3` 12px cell padding [S] · `4` 16px card padding [S] / page gutter ·
`6` 24px panel padding [F] + section gap · `8` 32px section gap [S] · `12` 48px region separation ·
`16` 64px rarely. Shipped console measures confirm the grid: nav-item padding 16/10px, section
heads 15–20px gutters, dropdown rows 6/15px, panel interiors 15–25px. *No `17px`. No `23px`. If a
layout needs an off-scale value, the layout is wrong.*

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | onboarding overlays, welcome/upgrade dialogs, auth moments |
| `standard` | 40–44px | 14px | 12–16px | 24px | data manager, actions/remote-schema builders, metadata pages |
| `dense` | 28–32px | 12–13px | 8px | 16px | GraphiQL editor, browse rows, request-headers grid, monitoring logs |

- Density comes from **row height, column pruning and leading** — never from type too small to
  read. A 13px tabular numeral in a dense table is correct; the same numeral in a focused dialog is
  a defect.
- **Never switch mid-page.** The GraphiQL route is dense edge to edge; the data-manager route is
  standard edge to edge. Switching across routes with different jobs is legitimate — it should feel
  like a different room.
- **Chrome follows rows.** The 50px top bar is the fixed anchor; within a dense route, sub-tab
  rows, toolbar and pagination match the 28–32px row rhythm; within a standard route they match
  40–44px. A 50px toolbar over 32px sub-rows inside one pane is a rhythm break.
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40%. Console data pages measure
  in the low 40s (standard); the GraphiQL route in the high 20s (dense) — validated by screenshot.

## 6. Radius Scale

`none` 0 (chrome bars, table cells, full-bleed panels) · `xs` 2px (legacy panels, tooltip cards) ·
`sm` 4px (inputs, dense cells, inline code chips, small ghost buttons) · `md` 5px (buttons, dialogs,
onboarding cards — the shipped console value) · `lg` 8px (large modals, drawers, marketing-adjacent
panels) · `full` 9999px pills (notification badge, plan badges, round icon buttons, the classic
20px-round share button). **One radius per component family**: buttons are all `md`, inputs all
`sm`, dialogs all `md`–`lg` by size, pills only where the shape itself means "chip/badge". Nested
radii obey `radius_inner = radius_outer − padding`.

## 7. Elevation

**One strategy per mode, never mixed.** Light: hairline-bordered surfaces; shadows reserved for
genuinely floating layers, in three verified strengths. Dark: surface-luminance steps + 1px
keylines, **zero shadows** — a drop shadow is invisible on `#0F172A`.

- **0** — `surface.canvas` (no shadow, both modes).
- **1** — card/panel: 1px `border.subtle` hairline, no shadow (the console's resting card). The
  floating onboarding card variant: `0 0 20px 0 rgba(0,0,0,0.10)`.
- **2** — sticky flyout/inspector pinned to an edge: `-3px 4px 10px 0 rgba(0,0,0,0.10)` (shipped
  notification-panel and right-inspector shadow) + `border.subtle`.
- **3** — popover/dropdown: `0 3px 20px 0 rgba(0,0,0,0.24)` (shipped popup shadow) + `border.strong`
  where it overlaps chrome.
- **4** — dialog: `0 3px 20px 0 rgba(0,0,0,0.24)` + scrim rgba(0,0,0,0.4), `md`–`lg` radius.
- Dark mirrors the levels with surface steps: 1 raised `#1E293B` + `#334155` keyline, 2 further
  step `#263244`, 3 overlay `#334155` + `border.strong #64748B`, 4 overlay + scrim.

## 8. Motion

`instant` 0ms · `fast` 120ms ease-out (exits [D], hover/focus tints) · `base` 180ms decelerate
([D] entrances, dropdowns, panel slides) · `slow` 240–300ms decelerate ([F/S] entrances, dialogs,
inspector drawers).

- Entrances decelerate, exits accelerate. Symmetric ease-in-out on both directions is a defect.
- Animate `transform` and `opacity` only — never width, height, top, left. The legacy 500ms color
  transition on nav items is recalibrated to 180ms.
- No bounce on irreversible moments: dropping a table, revoking a role, downgrading a plan.
- The pulsing primary CTA (1s infinite pulse on the legacy share button) is banned; a CTA is static.
- **Reduced motion is a real variant**, not a global kill: movement → crossfade under ~150ms; the
  progress-bar indeterminate animation swaps to a two-state opacity pulse; large scaling/panning
  surfaces (the homepage marquee equivalent, if ever shipped in-product) are the specific
  vestibular triggers to neutralise.

## 9. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell / top bar | S | collapsed sidebar (50px icon rail) | default, route-active (4px yellow underline), version banner (yellow `#FFC627`/slate text; red `#D9534F` for vulnerable) | tab order left→right; Enter activates | single-word uppercase tabs: API · DATA · ACTIONS · REMOTE SCHEMAS · EVENTS · MONITORING |
| Sub-sidebar tabs | S/D | GraphiQL/REST pair | active (ink underline), inactive | arrow keys within group | GraphiQL, REST, Allow List, Security |
| Data table (browse rows / metadata) | D/S | sortable, selectable, paginated | hover `#EBF7DE`, selected + left ink bar, loading skeleton, empty, error | arrows + Enter; header focus shows sort state | "Track", "Browse Rows", "Modify" |
| Filter/search bar | S | table filter, metadata search | idle, filled, cleared, error | `/` focuses; Esc clears | "Search tables…", "Enter Key" / "Enter Value" |
| Row action menu | D | dropdown on chrome (`#515766` fill) or on canvas (white) | open, focus-trapped, Esc closes, item hover/checked | arrows + Enter + Esc | "Delete", "Permissions", "Relationships" |
| Stat tile (monitoring) | S | single metric, sparkline | loading, stale (labeled "cached"), error | tab to value; tooltip on focus | "RESPONSE TIME — 348 ms", "RESPONSE SIZE — 184 bytes" |
| Drawer/inspector | S | right rail 260px, minimised 69px strip | open, minimised, closed | Esc closes; focus returns to trigger | task steps, "Docs" links |
| Dialog | F | onboarding card, PRO/upgrade popup (540px), confirm | open, scrim, Esc dismiss (confirm requires explicit choice) | focus trap; Esc; Enter = primary | "Add Table", "Upgrade", confirm names the object |
| Plan/seat control | S | plan badge pill, usage row | current, upgrade-cta, blocked (feature locked → `tier.accent` signal) | tab; Enter opens plan detail | "DDN Free / Base / Advanced", "$5/active model/month*" |
| Member row | S | list row with role select | loading, confirmed, pending, error | tab; role select via arrows | role names; "Remove" names the member |
| Audit entry (event/log line) | D | event row, webhook delivery | success/warn/error glyph + text ink, retry action | row focus; Enter expands payload | "Event delivered", "Retry" |
| Command palette | D | GraphiQL docs/search pane | open (focus in field), results, no-results | keyboard-first; Esc closes | "Search schema…", "No results for …" |

**Every fetching surface also designs:** loading (skeleton matching final row/table geometry — never
a centred spinner on a blank page; the legacy indeterminate top progress bar may accompany a
skeleton, not replace it) · empty ("No tables or views in this schema" + the CTA that fixes it:
"Add Table") · error (what happened + recover: "Connection failed — Retry / Check env vars") ·
offline/stale (what's known vs cached: "Showing cached metadata from 12:04 — Reload").

**Contracts this table encodes:** one primary filled CTA per view [F/S] (the yellow button); dense
toolbars may run the primary plus icon actions · every icon-only control carries a tooltip · a
disabled control states why on focus/hover · a button never changes width between idle and loading
— reserve the space.

## 10. Light / Dark Strategy

- **Posture: C dual-parity** (light default, dark authored). The console ran light-only for a
  decade; dark was added to the modernized component layer with a real slate ramp — it ships as an
  equal mode, and new components must define both.
- **Mechanism:** semantic roles remapped per mode; **no role absent in either mode.** Single-mode
  roles: `chrome.*` (the slate bar is deliberately identical in both modes — it is the product's
  constancy anchor) and `brand.*` (marketing-only tokens, dark-canvas values by definition).
- `color-scheme` declared per appearance (`light` on light scopes, `dark` on dark scopes) so native
  controls, scrollbars and form fields follow; the stylesheet carries a meta declaration **before**
  any CSS so the wrong scheme never flashes.
- **Dark is authored, not inverted:** its own ramp (`#0F172A → #1E293B → #263244 → #334155`), its
  own border strength (`#64748B` keylines at 3.751:1 — stronger than light's decorative
  `#DAE0E8`, which would vanish), its own shadow policy (zero), and status pairs rebuilt as pastel
  inks on hue-dark toast surfaces (all ≥11.2:1). The modern-layer primary fill flips from
  slate-indigo `#314158` to a lighter `#526C91`; yellow actions brighten `#FEC53D → #F8C533`.
- Org-tinting (D) is permitted for self-hosted deployments changing **colour tokens only**; radii,
  type sizes and layout are frozen so a theme swap cannot move anything.

## 11. Density-Mode Strategy

- **Default mode per surface class:** console data/API/metadata pages — `standard` (14px base,
  40–44px rows); GraphiQL, browse-rows, logs, permission matrices — `dense` (12–13px, 28–32px
  rows); onboarding and upgrade dialogs — `focused` (16px). The boundary is the route's job:
  reading data vs editing data vs deciding.
- **Mechanism:** a density marker on the app root rescales row height, cell padding, gutter and
  body size **together as a token axis** — spacing tokens do not change per screen size; density is
  not a media query.
- **Container queries for reflow:** `@container` measures the *content box*, so a table reflows to
  its pane, not the viewport; size queries fail closed with no eligible container, and `cq*` units
  silently resolve to small-viewport units there — never used where that fallback would be wrong.
- **Style queries** compare *computed* values, so the density marker must be a registered custom
  property with a determinable type.
- **Offer the switch as an accessibility affordance**, not a preference: W3C's SC 2.5.8 note
  endorses "a mechanism to control the density of layout" for users with visual field loss — the
  console ships a standard/dense toggle in view settings, and the choice persists.

## 12. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA for text contrast on static reading surfaces (onboarding
  copy, error bodies) where the palette already clears 7:1 (`text.primary` 8.074:1).
- **Target size:** ≥24×24 CSS px hard minimum (SC 2.5.8); 44px the design target for primary
  controls [F/S] — the 50px chrome and 40–44px standard rows make nav targets compliant by
  construction; dense rows keep icon actions at 28px rows with ≥24px hit circles. Zoom does not
  excuse it.
- **Keyboard:** every console function operable (SC 2.1.1) — tab browsing, permission editing,
  query running; focus indicator visible (SC 2.4.7): 2px `border.focus` (`#314158` light,
  `#33E0FF` on chrome/dark, both ≥3:1) replacing the default ring, never suppressed without a
  stronger replacement; focused rows never fully hidden behind the sticky top bar (SC 2.4.11 —
  scroll-margin equals chrome height + 8px).
- **Contrast:** text ≥4.5:1 (computed in §3; nothing ships at 4.499); boundaries and focus ≥3:1.
  **Colour independence:** active tab = 4px underline + yellow text + bold (shape + colour + weight);
  status pairs glyph with ink; deltas carry sign or direction; the vulnerable-version banner pairs
  red fill with a warning glyph and words.
- **Motion:** the §8 reduced-motion variant per component; no vestibular scaling/panning in-product.
- **Text:** ≤80-character measure in prose panels, 1.5 leading on body, 200% resize without
  horizontal scroll outside editor panes (SC 1.4.8); the editor pane is exempt as a data surface.
- **Semantics:** real button/link/input elements; table roles for data grids with headers bound to
  cells; headings matching visual rank (page title → section title); `aria-live="polite"` for
  metadata-sync and query-result updates; `aria-busy` on loading regions.
- **Contrast preference:** `prefers-contrast: more` promotes `border.subtle #DAE0E8 → #A8B0BD`,
  `text.tertiary #909090 → #667182`, and thickens focus rings to 3px; values tracked as the four
  standard preferences.

## 13. Anti-Patterns

**Do**

1. Keep the one-yellow-fill budget: a single `#FEC53D` fill per viewport [S]; every other action is
   hairline, text, or icon — the yellow must mean "the" action.
2. Set nav and section labels in 14px/700 uppercase with +1px tracking on slate — it is the
   console's voice, and it is how the product reads "Hasura" at a glance.
3. Pair `#43495A` label text on yellow fills (5.672:1) — the shipped, computed pairing; never white
   on yellow (1.9:1).
4. Use Overpass Mono for GraphQL, endpoints, headers, hashes, versions; tabular numerals for every
   compared quantity.
5. Draw data-row hover as the pale green `#EBF7DE` wash and selection as wash + left ink bar —
   shape plus colour.
6. Keyline every dark raised surface; `#1E293B` on `#0F172A` alone is 1.220:1.
7. Reserve teal/cyan for the slate chrome (tier signals, focus on dark) — computed legal there,
   computed illegal on light canvas.
8. Keep the 50px chrome height sacred across routes; sub-toolbars follow the active density's row
   rhythm.
9. Match skeletons to final geometry — the request-headers grid shows header row + two empty rows,
   not a spinner.
10. Write empty states as diagnosis + CTA: "No tables or views in this schema" → "Add Table".
11. Deepen status text inks (`#1F7A33`, `#92400E`, `#C62F2B`, `#16697F`) for words; keep legacy
    bright fills for non-text glyphs at ≥3:1.
12. Separate brand from product: lime/cobalt on `#000615` stays on marketing routes; the console
    never inherits it.

**Don't**

1. Don't put teal `#1CD3C6` or cyan `#33E0FF` text or fills on light canvas — 1.5–3.7:1, computed
   refuse; they belong on slate.
2. Don't set GraphQL magenta `#E535AB` as body text on white (3.868:1) — decoration and dark-surface
   text only; use `#C2268F` when magenta must carry words on light (5.293:1).
3. Don't import the 2026 lime brand accent `#B6FC34` into console chrome — it destroys the yellow
   accent budget and the brand layer's meaning.
4. Don't run two filled CTAs side by side; the legacy pattern of a yellow button plus a filled
   indigo button in one toolbar is a hierarchy defect.
5. Don't inflate data pages into stat-card dashboards — monitoring gets a stat **row**, not a grid
   of glass tiles.
6. Don't use modals as connective tissue; permission editing stays in-place with inline validation,
   and confirmations name the object ("Delete table profiles?").
7. Don't leave a toolbar of unlabelled icons — every icon-only action has a tooltip or text label
   (the sub-tab row carries words, and it stays that way).
8. Don't build hover-only affordances in the permissions editor; every reveal also works on focus.
9. Don't use placeholder text as the only label ("Enter Key" is a hint beside a visible label,
   never the label itself).
10. Don't ship whole-page spinners; the console's surfaces are skeletons with final geometry.
11. Don't use `alert`/`confirm` for destructive flows — dialogs with named objects and typed
    consequences.
12. Don't shrink type below 12px to fit density, and don't stack a 50px toolbar over 32px rows in
    one pane — density switches happen between routes, never mid-page.

## 14. Quick Reference & Verification Gate

**Colour (light):** canvas `#F8FAFB` · raised `#FFFFFF` · inset `#F2F2F2` · chrome `#43495A` ·
chrome text `#DEDEDE` · indicator `#FFC627` · action `#FEC53D` / onAction `#43495A` · control
`#314158`/white · ink `#4D4D4D` / `#667182` / `#909090` · hover `#EBF7DE` · active wash `#FFF3D5` ·
tier teal `#1CD3C6` · cyan `#33E0FF` · GraphQL `#E535AB` · success `#1F7A33` · warning `#92400E` ·
error `#C62F2B` · info `#16697F` · line `#DAE0E8`.
**Colour (dark):** canvas `#0F172A` · raised `#1E293B` · overlay `#334155` · ink `#E2E8F0` /
`#94A3B8` / `#64748B` · action `#F8C533` / onAction `#43495A` · control `#526C91`/white · keyline
`#64748B` · focus `#33E0FF` · status `#D0E7B8` / `#EEE0BD` / `#F7D3D3` / `#BEDDEA` on `#192614` /
`#2B2515` / `#2D1A1A` / `#11242D`.

**Type:** Gudea 400/700 (fallback 'Helvetica Neue', Helvetica) · Overpass Mono for code/identifiers ·
Poppins 400/600 expressive · [S] 20/14/14/12 with 14px body 1.5 · [D] 12–13px, mono log lines 13/1.6 ·
[F] 25/20/16/14/12 · tabular numerals on every compared value.

**Spacing + radius:** 4px grid (8 [F/S], 4 [D]) · steps 4/8/12/16/24/32/48 · radius 0/2/4/5/8/full ·
chrome 50px · rows 40–44 [S], 28–32 [D].

**Component → token map:** top bar = `chrome.bar + chrome.text + chrome.indicator` · primary button
= `accent.action + accent.onAction + radius.md` · quiet control = `control.fill + control.onFill` ·
data table = `surface.raised + border.subtle + surface.hover + text.primary/secondary + radius.sm` ·
sub-sidebar = `surface.raised + text.secondary + surface.selected(#FFF3D5)` · inspector = level 2
shadow + `border.subtle + surface.raised` · dialog = level 4 + scrim + `radius.md` · stat tile =
`text.primary + text.secondary + tabular` · tier signal = `tier.accent` (chrome only) · explorer =
mono family + `graph.accent` decoration · toasts = `status.*` + wash.

**Pre-ship checklist.** 1 Zero raw hex outside L1. 2 No token resolves to a component name. 3 Every
contrast pairing computed, passing, unrounded. 4 Every semantic role has a value in both modes
(except documented chrome/brand single-modes). 5 Every fetching surface has loading/empty/error/
offline specified. 6 Every component row lists disabled and loading states. 7 Row, header, toolbar
and pagination heights agree per route. 8 Reduced-motion variant written for every authored motion. 9
Every control keyboard-reachable with a visible ≥3:1 focus indicator. 10 Dark authored, not
filtered, with border strength exceeding light's decorative hairline. 11 No unoverridden stock
default inside a committed surface. 12 Nothing came from a marketing page — the console palette is
sourced from the shipped product, not the brand site.
