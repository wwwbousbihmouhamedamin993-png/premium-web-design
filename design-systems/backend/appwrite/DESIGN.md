# Design System — Appwrite Console

<!-- premium-web-design:design-system 1 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: Appwrite rebrand "Meet the new Appwrite" (posture + illustration motifs), shipped console token CSS on cdn.appwrite.io (colour + shell, both themes), console-hero screenshots (density/type verification). Spec supplied by rung 2 (official brand post + shipped CSS tokens) and verified by rung 3 (pixel sampling of the official console hero and browser captures of appwrite.io); rung 1 sibling catalogs had no appwrite entry. -->
<!-- Surface classes: 3 route groups classified; density classes F/S/D assigned (F onboarding/auth-entry, S project overview + resources, D logs/activity/tables) -->

## 1. Design Posture & Atmosphere

Appwrite is the open-source Firebase alternative: auth, databases, storage, functions, messaging and
sites behind one platform. The console is the room a developer lives in while their backend runs, so
the surface behaves like a **calm instrument panel with a brand pulse** — near-neutral zinc surfaces
do all of the structural work, and the single pink accent is spent the way a pulse line is spent:
rare, thin, and exactly where the product's heartbeat is (the primary CTA, the onboarding progress
bar, the outbound traffic series). After eight hours the console still reads as a tool, not a
campaign; the poster world — dark canvas, Aeonik Pro display type, pink gradient headlines, terminal
underscores — stops at the sign-in boundary and never leaks into project screens.

Against its category's defaults (Firebase's blue-teal material console, Supabase's dark emerald
dashboard), Appwrite sits **light-first and almost colourless**: white canvas, hairline-separated
cards instead of shadows, a zinc ink ramp, and one rose-pink action colour. Depth is expressed by
border and by two quiet surface steps, not by elevation. Density is Standard by default (40px rows,
14px body) and goes Dense only where the job is volume — activity, realtime, functions logs. The
visual metaphor: **a server room instrument panel wearing a brand wristband** — everything
neutral except the one strap of pink that tells you whose panel it is.

**Key Characteristics**
- Canvas is pure white in light mode; separation comes from 1px `#e7e7ea` hairlines, not shadows.
- Dark canvas is `#19191c` (never pure black) with a 3-step surface ramp `#141416 → #19191c → #1d1d21`.
- One accent fill per viewport: the console overview shows exactly one pink button ("Add app") plus
  the onboarding progress bar — never two competing pink fills.
- The brand pink ships in three jobs: `#fd366e` vivid (non-text fills, progress, focus in dark),
  `#db0060` action (text-bearing CTA fill, white label at 5.02:1), `#cd0071` / `#e80080` chart-brand.
- Legacy theme carries the older identity: canvas `#eef1f5`, navy sidebar `#1c2b3e`, primary `#f02e65`,
  8px radius — retained for self-hosted installs, not the design target.
- Charts pair magenta outbound with teal inbound (light `#cd0071`/`#009588`, dark `#e80080`/`#00bb7f`);
  the pair is fixed across every usage screen.
- Identifiers are monospace: project IDs, hostnames, table row paths, log lines, chart axis numerals.
- Stat strip, not stat cards: one full-width usage band with 5 measures separated by hairlines.
- Row rhythm 40px (Standard); toolbar and pagination match row height.
- Terminal underscores (`_`) after headings are a brand signature, marketing surfaces only.
- Marketing uses Aeonik Pro display + Inter; the console is Inter-only plus a system mono stack.
- Deltas always carry a direction glyph plus sign (`↗ +20.7%`), green or red never alone.
- Every list row keeps a quiet secondary line (13px muted) under the primary label.
- Radius is one rounded family: 6px inputs, 10px buttons/cards, 16px overlays.

## 2. Token Architecture

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.
- **L1 Primitive** — literal values named by value, referenced only by L2: `zinc.50 #fafafa` …
  `zinc.950 #09090b`, `brand.vivid #fd366e`, `brand.action #db0060`, `brand.magenta-light #cd0071`,
  `brand.magenta-dark #e80080`, `brand.legacy #f02e65`, `teal.600 #009588`, `teal.400-dark #00bb7f`,
  `status.*` scales, `neutral.border-light #e7e7ea`, `neutral.border-dark #222224`,
  `neutral.canvas-dark #19191c`, `neutral.card-dark #1d1d21`, `neutral.well-dark #141416`.
  Banned: component-named primitives (`--card-bg`, `--tooltip-color`) — one value, many roles.
- **L2 Semantic** — role names (`surface.canvas`, `text.primary`, `accent.action`, `status.error`).
  The only layer a component may consume. Every role carries a light **and** dark value in §3.
- **L3 Component** — only deliberate deviation, pointing at L2: `sidebar.active → surface.wash`,
  `stat.value → text.primary + tabular numerals`, `chip.mono → text.tertiary + mono family`,
  `chart.seriesOutbound → chart.brand`, `chart.seriesInbound → chart.teal`. Never a raw value,
  never a sibling component's token.

**Rules.** Every token has a determinable type (colour, dimension, font-family, duration) or it is
invalid; names are case-sensitive and free of `$`, `{`, `}`; circular references are an error.
Every semantic token resolves in **both shipped modes** — the light and dark columns in §3 are
complete by definition; a role that cannot exist in a mode (none currently) would need a documented
reason. Animatable tokens (progress-bar fill, drawer offset) are registered with explicit syntax and
inheritance declarations, and their initial values are length-independent — percentages are illegal
as initial values.

**Layer order (low → high):** `reset → primitives → semantic → components → utilities`. Order beats
specificity, so a stray un-layered rule inside a component file would outrank the whole system;
anything a consumer must override without `!important` lives in the top layer.

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` | #ffffff | #19191c | app background; light canvas is white, separated by hairlines |
| `surface.raised` | #ffffff | #1d1d21 | cards, panels, stat strip |
| `surface.overlay` | #ffffff | #1d1d21 | popovers, dropdown menus |
| `surface.well` | #f4f4f5 | #141416 | terminal drawer, code blocks, wells |
| `surface.wash` | #f4f4f5 | #2d2d31 | hover fills, selected rows, status washes |
| `surface.hover` | #f4f4f5 | #2d2d31 | row/list hover fill |
| `surface.selected` | #e4e4e7 | #2d2d31 | active sidebar item, active tab pill |
| `border.subtle` | #e7e7ea | #222224 | 1px hairlines; decorative, not a contrast boundary |
| `border.strong` | #71717b | #71717b | 1px boundaries that must pass 3:1 |
| `border.focus` | #db0060 | #fd366e | focus ring, 2px offset ring |
| `accent.action` | #db0060 | #db0060 | filled CTA fill (text-bearing) |
| `accent.onAction` | #ffffff | #ffffff | label on action and vivid fills |
| `accent.vivid` | #fd366e | #fd366e | progress bar, toggle-on, non-text brand fills |
| `accent.subtle` | #fd366e at 15% on white | #fd366e at 15% on #19191c | pink washes, chart area fill |
| `accent.legacy` | #f02e65 | #f02e65 | legacy theme primary only, not the design target |
| `text.primary` | #09090b | #fafafa | headings, row labels, stat values |
| `text.secondary` | #52525c | #d4d4d8 | body copy, descriptions |
| `text.tertiary` | #71717b | #9f9fa9 | meta, placeholders, unit suffixes |
| `text.disabled` | #a1a1aa | #52525c | inactive controls only (SC-exempt, never body copy) |
| `status.success` | #008138 | #00c758 | with a check glyph, never colour alone |
| `status.warning` | #b75000 | #ffd236 | with a triangle glyph |
| `status.error` | #c20039 | #fb2c36 | with an alert glyph; solid button = #e40014 fill + #ffffff label (light), #82181a fill + #ffffff label (dark) |
| `status.info` | #0069a4 | #77d4ff | with an info glyph |
| `chart.brand` | #cd0071 | #e80080 | outbound series, primary metric |
| `chart.teal` | #009588 | #00bb7f | inbound series, secondary metric |
| `chart.aux1`–`aux5` | #f05100 #009588 #104e64 #fcbb00 #f99c00 | #1447e6 #00bb7f #f99c00 #ac4bff #ff2357 | multi-series, ordered |

Dark canvas is **not** pure black: it sits in the `#141416–#2d2d31` range. Depth in dark comes from
surface steps and 1px strokes, never shadows.

**Contrast gate — computed, unrounded. Body text ≥4.5:1; large text (≥24px, or ≥18.5px bold) ≥3:1;
UI boundaries and focus indicators ≥3:1** (W3C SC 1.4.3, 1.4.11).

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| text.primary (light) | #09090b | surface.canvas | #ffffff | 19.895:1 | 4.5:1 | PASS |
| text.secondary (light) | #52525c | surface.canvas | #ffffff | 7.720:1 | 4.5:1 | PASS |
| text.tertiary (light) | #71717b | surface.canvas | #ffffff | 4.827:1 | 4.5:1 | PASS |
| text.secondary (light, on card) | #52525c | surface.raised | #ffffff | 7.720:1 | 4.5:1 | PASS |
| text.tertiary (light, on card) | #71717b | surface.raised | #ffffff | 4.827:1 | 4.5:1 | PASS |
| accent.onAction (light) | #ffffff | accent.action | #db0060 | 5.023:1 | 4.5:1 | PASS |
| accent.onAction (light) | #ffffff | accent.vivid | #fd366e | 3.542:1 | 4.5:1 body / 3:1 large | FAIL body; PASS large text only |
| border.strong (light) | #71717b | surface.raised | #ffffff | 4.827:1 | 3:1 | PASS |
| status.success (light) | #008138 | surface.wash | #f4f4f5 | 4.552:1 | 4.5:1 | PASS |
| status.warning (light) | #b75000 | surface.wash | #f4f4f5 | 4.592:1 | 4.5:1 | PASS |
| status.error text (light) | #c20039 | surface.wash | #f4f4f5 | 5.698:1 | 4.5:1 | PASS |
| status.info (light) | #0069a4 | surface.wash | #f4f4f5 | 5.372:1 | 4.5:1 | PASS |
| text.primary (dark) | #fafafa | surface.canvas | #19191c | 16.806:1 | 4.5:1 | PASS |
| text.secondary (dark) | #d4d4d8 | surface.canvas | #19191c | 11.868:1 | 4.5:1 | PASS |
| text.tertiary (dark) | #9f9fa9 | surface.canvas | #19191c | 6.688:1 | 4.5:1 | PASS |
| text.tertiary (dark, on card) | #9f9fa9 | surface.raised | #1d1d21 | 6.405:1 | 4.5:1 | PASS |
| accent.onAction (dark) | #ffffff | accent.action | #db0060 | 5.023:1 | 4.5:1 | PASS |
| border.strong (dark) | #71717b | surface.raised | #1d1d21 | 3.480:1 | 3:1 | PASS |
| status.success (dark) | #00c758 | surface.wash | #2d2d31 | 6.080:1 | 4.5:1 | PASS |
| status.warning (dark) | #ffd236 | surface.wash | #2d2d31 | 9.485:1 | 4.5:1 | PASS |
| status.error (dark) | #fb2c36 | surface.canvas | #19191c | 4.607:1 | 4.5:1 | PASS |
| status.error wash-row text (dark) | #ffa3a3 | surface.wash | #2d2d31 | 7.196:1 | 4.5:1 | PASS |
| status.info (dark) | #77d4ff | surface.wash | #2d2d31 | 8.258:1 | 4.5:1 | PASS |
| border.focus (light) | #db0060 | surface.canvas | #ffffff | 5.023:1 | 3:1 | PASS |
| border.focus (dark) | #fd366e | surface.canvas | #19191c | 4.953:1 | 3:1 | PASS |
| chart.brand (light) | #cd0071 | surface.raised | #ffffff | 5.477:1 | 3:1 non-text | PASS |
| chart.teal (light) | #009588 | surface.raised | #ffffff | 3.714:1 | 3:1 non-text | PASS |
| chart.brand (dark) | #e80080 | surface.canvas | #19191c | 3.962:1 | 3:1 non-text | PASS |
| chart.teal (dark) | #00bb7f | surface.canvas | #19191c | 7.029:1 | 3:1 non-text | PASS |

The one failing pairing is intentional and documented: the shipped brand fill `#fd366e` with a white
label computes to 3.542:1, which fails body-size text. The system therefore splits the accent —
text-bearing filled controls use `accent.action #db0060` (5.023:1), while `accent.vivid #fd366e` is
restricted to non-text fills (progress, toggles) and to labels at large-text sizes. `border.subtle`
hairlines (1.234:1 light) are decorative separators, never the only boundary of an interactive
control — any control that relies on its border for identification upgrades to `border.strong`.
`text.disabled` (2.563:1 light) is SC-exempt inactive-component text only.

## 4. Typography

**Families.** UI **Inter** (400/500/600), self-hosted woff2, preloaded, fallback Arial/system
sans-serif. Display **Aeonik Pro** (400/500/600), self-hosted woff2, fallback system stack — display
marketing surfaces only, never inside the console. Numeric/code: **system mono stack**
(ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas) for project IDs, hostnames, resource paths,
log lines, and chart axis numerals. Monospace is for identifiers and code, never a costume.

**One ramp table per class, not one blended table.**

- **F Focused, 16px base** — onboarding checklists, auth-entry screens, empty-org states:
| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Display | 32px | 600 | 40px | -0.5% | — | page hero (marketing: Aeonik Pro) |
| Heading | 24px | 600 | 32px | -0.25% | — | section hero, "Get started" panel |
| Body | 16px | 400 | 24px (1.5) | 0 | — | onboarding copy |
| Label | 14px | 500 | 20px | 0 | — | form labels, buttons |
| Meta | 13px | 400 | 16px | 0 | tabular | helper text, step counts |

- **S Standard, 14px base** — project overview, resources, settings (the console default):
| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Page title | 18px | 600 | 24px | -0.25% | — | project name "Refetch" |
| Section title | 16px | 600 | 24px | 0 | — | "Bandwidth over time", "Apps" |
| Body | 14px | 400 | 22px | 0 | — | descriptions, empty states |
| Row primary | 14px | 500 | 20px | 0 | tabular | list row labels |
| Row secondary | 13px | 400 | 20px | 0 | tabular | row sublines: hostname, region, date |
| Stat value | 28px | 600 | 34px | -0.5% | tabular | "150.0 MB", "23.9 K" |
| Stat unit | 13px | 400 | 20px | 0 | — | "MB", "K" suffixes |
| Stat label | 13px | 400 | 16px | 0 | — | "Bandwidth", "Requests" |
| Meta | 12px | 500 | 16px | +2% uppercase | — | sidebar group headings "CONNECT/BUILD" |

- **D Dense, 12–13px base** — activity, realtime connections, functions logs, wide tables:
| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Grid header | 12px | 500 | 16px | 0 | — | column headings (uppercase reserved to marketing tables) |
| Grid cell text | 13px | 400 | 20px | 0 | — | resource names |
| Grid cell numeric | 13px | 500 | 20px | 0 | tabular, mono | sizes, counts, timestamps |
| Log line | 13px | 400 | 20px | 0 | mono | function execution logs |
| Inline help | 12px | 400 | 16px | 0 | — | hints under dense controls |

Prose inside a dense screen still steps up to Body 14px.

**Invariants.** Tabular numerals on every comparable value — bandwidth, request counts, storage,
deltas, timestamps, project IDs (mono numerals are inherently tabular). Right-align numerics,
left-align text, never centre a numeric column. Fixed stepped sizes; no fluid type. Measure ≤80
characters: 65–80ch in F/S prose, unconstrained in D logs.

## 5. Spacing Scale & Density Scales

**Spacing base: 4px grid; 8px comfortable in F/S, 4px in D.** `space.0` 0 · `1` 4px icon-to-label ·
`2` 8px control padding in D · `3` 12px cell padding in S · `4` 16px card padding in S / page gutter
in D · `6` 24px card padding in F + section gap · `8` 32px section gap in S · `12` 48px region
separation · `16` 64px rarely (marketing). No 17px. No 23px. If a layout needs an off-scale value,
the layout is wrong.

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | onboarding, auth entry, settings detail |
| `standard` | 40px | 14px | 12–16px | 24px | project overview, resources, docs |
| `dense` | 32px | 12–13px | 8px | 16px | activity, realtime, logs, wide tables |

- Density comes from row height, column pruning and leading — never from type too small to read. A
  13px tabular numeral in a dense table is correct; the same numeral in a Focused form is a defect.
- **Never switch mid-page.** The console overview is Standard end to end; the activity page is Dense
  end to end. Switching across routes with different jobs is legitimate — it should feel like a
  different room.
- **Chrome follows rows.** The usage strip, filter bar and pagination match the table's 40px (S) or
  32px (D) rhythm. A 40px toolbar over 32px rows is a rhythm break.
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40%. House heuristic — validated
  against the console hero: the S overview lands near 50% (white space around one full-width stat
  band and the apps grid), the D surfaces near 30%.

## 6. Radius Scale

`none` 0 · `xs` 2px badges/tags · `sm` 6px inputs, dense cells, inline code · `md` 10px buttons,
rows, cards (the shipped base radius, 0.625rem) · `lg` 16px dialogs, drawers, popovers · `full`
9999px pills, avatars, the project switcher chip. **One radius per component family** — buttons and
cards are always `md`, dialogs always `lg`, never mixed ad-hoc. Nested radii obey
`radius_inner = radius_outer − padding` (a `sm` input inside an `md` card is correct: 10 − 4 = 6).
The legacy theme's 8px base is grandfathered to self-hosted installs only; new surfaces use 10px.

## 7. Elevation

**Choose one strategy, never mix paradigms.** Light: 1px hairlines carry all structure; shadows
exist only for elements that float above the page. The shipped light shadow is a two-layer soft
ambient (`0 1px 2px` + `0 6px 18px` at ~5% ink) plus a faint hairline. Dark: surface-luminance steps
plus 1px keylines, zero shadows — a drop shadow is invisible on `#19191c`.

Levels, low → high: **0** canvas (no shadow, both modes) · **1** card/panel (hairline in light; one
step up to `#1d1d21` + `#222224` keyline in dark) · **2** sticky header/toolbar (hairline + canvas
blur in light; `#1d1d21` + `border.strong` in dark) · **3** overlay/popover (two-layer shadow,
`radius.lg` in light; `#1d1d21` + `border.strong` in dark) · **4** dialog/terminal drawer (strongest
shadow + scrim in light; top step `#2d2d31` + scrim in dark).

## 8. Motion

`instant` 0ms · `fast` 120ms ease-out (exits in D, hover fills, tooltip out) · `base` 180ms
decelerate (D entrances, row reveals, chart draw) · `slow` 240–300ms decelerate (F/S entrances,
dialogs, terminal drawer slide-up).
- Entrances decelerate, exits accelerate. Symmetric ease-in-out on both directions is a defect.
- Animate transform and opacity only — never width, height, top, left.
- No bounce on irreversible moments: not on "Delete database", not on a plan downgrade, not on key
  revocation.
- The progress bar fill animates transform-based only; its length change is a transform, not width.
- **Reduced motion is a real variant**, not motion-off everywhere: the chart draw becomes a single
  150ms crossfade, the drawer slide becomes a crossfade, spinner glyphs freeze at rest orientation.
  What must be neutralised is scaling and panning of large objects, not every fade.

## 9. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell/sidebar | S | collapsed rail, expanded | default, hover, active, collapsed | Tab order top-down; section headings not focusable | "CONNECT / BUILD / DEPLOY / OBSERVE / PROTECT" |
| Project switcher | S | org + project breadcrumb pill | closed, open, Pro badge | Enter opens, Esc closes, arrows navigate | "Refetch / Refetch · Pro" |
| Data table | S/D | resources, members, keys | loading, empty, error, row hover, selected, disabled | arrows move row focus, Enter opens | "Name · Created · Actions" |
| Filter/search bar | S | header search, table filter | idle, focused, filled, no-results | trigger via the platform search shortcut | "Search… ⌘K" |
| Row action menu | S/D | kebab menu per row | focus-trapped open, Esc closes | arrows + Enter, Esc exits | "Rename · Duplicate · Delete" |
| Stat strip | S | 5 measures + range switch | loading (skeleton), stale | left/right cycles measures | "Bandwidth · Requests · Storage · Executions · Compute" |
| Usage chart | S | area, line | loading, empty ("no traffic yet"), error | legend toggles series | "Bandwidth over time · Inbound / Outbound" |
| Terminal drawer | S | bottom sheet in overview | collapsed, expanded, running, exited | open/close via footer toggle | "Terminal" |
| Dialog | F/S | confirm, form, connect flow | open, busy, error, Esc-dismissed | focus trap, Esc closes, Enter confirms | "Connect · Copy your project ID" |
| Plan/seat control | S | plan badge, upgrade row | current, upgradeable, blocked, prorating | Enter opens billing | "Pro — usage resets 1 Nov" |
| Member row | S | role select, remove | pending invite, active, revoked | role select via arrows | "Owner · Admin · Developer" |
| Audit/Activity entry | D | event line with actor | expanded detail, filterable | Enter expands | "User created API key · 2m ago" |
| Command palette | S | global actions + navigation | open, querying, no-results | shortcut-invoked, arrows, Esc | "Jump to… Search documentation" |

Every fetching surface also designs: **loading** — skeleton matching final geometry (the stat strip
renders 5 grey value blocks, tables render 8 ghost rows; never a centred spinner on a blank page);
**empty** — what is missing plus the CTA that fixes it ("No apps yet — Add your first app");
**error** — what happened plus recovery ("Couldn't load usage — Retry"); **offline/stale** — the
last known values stay visible, dimmed to `text.tertiary`, with a "Showing cached usage" note.

**Contracts this table encodes:** one primary filled CTA per view in F/S (dense toolbars may run a
primary plus icon actions); every icon-only control carries a label or tooltip (the header's
notification and help icons do); a disabled control states why on focus or hover; a button never
changes width between idle and loading — the spinner replaces the label inside reserved space.

## 10. Light / Dark Strategy

- **Posture: C dual-parity.** The console ships light and dark at token parity; the marketing site is
  dark-only poster surface and is out of the product's token scope. Reason: developers live in the
  console at all hours, and the platform's screenshots (docs, og imagery) are dark — the console must
  hold both.
- **Mechanism:** semantic roles remapped per mode exactly as the two §3 columns define; no role is
  absent in either mode. The legacy theme (`#eef1f5` canvas, `#1c2b3e` sidebar, `#f02e65` primary)
  is a third, opt-in palette that reuses the same semantic role names.
- **`color-scheme`** is set on the root so UA chrome, form controls and scrollbars follow the mode.
- **The scheme meta tag sits in the head before the stylesheet** so the console never flashes the
  wrong scheme on load.
- **Dark is authored, not inverted:** its own surface ramp `#141416 → #19191c → #1d1d21 → #2d2d31`,
  its own border strength (`#222224` subtle — and because a hairline that reads as delicate on white
  reads as invisible on near-black, any boundary that matters upgrades to `#71717b` strong), its own
  chart palette (`#e80080`/`#00bb7f`), and zero shadows. `light-dark()` colour functions are
  progressive enhancement only; the two full token sets are the baseline.
- Org-level tinting is not offered; a theme swap changes colour tokens only, and radii, type sizes
  and layout are frozen so no swap can move geometry.

## 11. Density-Mode Strategy

- **Default mode per surface class:** Standard everywhere in the console except tables/logs
  (Dense) and onboarding/auth-entry (Focused). The boundary is the job: reading status → S; scanning
  volume → D; acting once → F.
- **Mechanism:** a density attribute on the app root rescales row height, cell padding, gutter and
  body size together as one token axis — Carbon's rule that spacing tokens do not change per screen
  size holds here; density is not a media query.
- **Container queries for reflow:** components reflow to their container, not the viewport; size
  queries fail closed with no eligible container and the `cq` units silently resolve to
  small-viewport units there, so they are never used where that fallback would be wrong (the stat
  strip reflows on a container query scoped to the strip itself).
- **Style queries** compare computed values, so the density marker is a registered custom property
  with an explicit syntax and inheritance declaration.
- **The switch is offered as an accessibility affordance**, not a preference: W3C's SC 2.5.8 note
  endorses a mechanism to control layout density for users with visual field loss; the console
  exposes it in settings per user, not per project.

## 12. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA (1.4.6 contrast ≥7:1) on body copy in onboarding prose.
- **Target size:** ≥24×24 CSS px hard minimum with the spacing exception; 44px is the design target
  for primary controls in F/S (the console's 40px rows and buttons sit inside a 44px hit area via
  padding). Zoom does not excuse it.
- **Keyboard:** every function operable without a pointer (SC 2.1.1); focus indicator visible
  (SC 2.4.7) — a 2px `border.focus` ring offset 2px, never outline-suppressed without a stronger
  replacement; the focused row is never entirely hidden behind the sticky header or the terminal
  drawer (SC 2.4.11).
- **Contrast:** text ≥4.5:1 (both modes' ink ramps pass; see the §3 gate); UI boundaries and focus
  indicators ≥3:1. **Colour independence:** every status pairs colour with an icon, label or shape;
  deltas carry a direction glyph plus sign; the two chart series also differ in dash pattern on
  hover-legend focus, so the magenta/teal pair is never the only carrier of meaning.
- **The vivid-pink exception is contained:** white labels on `#fd366e` render only at large-text
  sizes or as non-text fills; every body-size label on a pink fill sits on `#db0060` (5.023:1).
- **Motion:** the §8 reduced-motion variant ships per component.
- **Text:** ≤80-character measure, 1.5 leading on prose, 200% resize without horizontal scroll
  (SC 1.4.8); the stat strip's tabular values resize without truncating their labels.
- **Semantics:** real button/link/input elements; the sidebar is a navigation landmark with list
  semantics; headings match visual rank; usage updates announce via polite live regions; a loading
  region carries the busy state.
- **Contrast preference:** if the user requests more contrast, `border.subtle` upgrades to
  `border.strong`, `text.tertiary` becomes `#52525c` (light) / `#d4d4d8` (dark), and the accent
  stays `#db0060`; the supported media values are no-preference, more, less, custom.

## 13. Anti-Patterns

**Do**
1. Spend pink once per viewport — the overview's single "Add app" fill is the whole budget; the
   progress bar joins only because it is thin and non-text.
2. Separate light-mode surfaces with 1px `#e7e7ea` hairlines — the canvas is white on white by
   design, and borders are the structure.
3. Set every identifier in mono — project IDs, hostnames, row paths, log lines.
4. Keep the chart pair fixed — magenta outbound, teal inbound, everywhere, both modes.
5. Match chrome heights to row heights — 40px toolbars over 40px rows, 32px over 32px.
6. Render skeletons in final geometry — 5 grey stat blocks before the numbers arrive.
7. Pair every status colour with a glyph — a check, a triangle, an alert, an info dot.
8. Keep deltas signed and directed — an up-right arrow plus "+20.7%", never colour alone.
9. Dim stale data instead of blanking it — cached usage stays at `text.tertiary` with a note.
10. Reserve the terminal underscore for marketing headings — "Authentication_" lives on posters only.
11. Upgrade any border that identifies a control to `border.strong` — decorative hairlines are not
    boundaries.
12. Author dark explicitly — new ramps, new borders, new charts; never filter the light theme.

**Don't**
1. No white body-size labels on the vivid pink — 3.542:1 fails; text-bearing fills use `#db0060`.
2. No card inflation — the usage band is one strip with hairline dividers, not five floating cards.
3. No stat-card dashboards — one strip, five measures, one range switch.
4. No modals as connective tissue — the terminal is a drawer, resources are routes.
5. No two pink primaries side by side — if two fills compete, one downgrades to `surface.wash`.
6. No unlabelled icon toolbars — every icon-only control carries a tooltip at minimum.
7. No hover-only affordances — row actions are reachable by keyboard focus, not just pointer.
8. No placeholder-as-label — inputs keep persistent labels; the search field keeps its visible text.
9. No whole-page spinners — skeletons match the geometry they replace.
10. No native alert/confirm dialogs — destructive flows use the in-product dialog with typed
    confirmation for database drops.
11. No tiny type as a density strategy — Dense goes to 12px headers and 13px cells, never below.
12. No pure-black dark canvas and no navy sidebar in new surfaces — `#19191c` and the zinc shell are
    the system; the navy `#1c2b3e` sidebar belongs to the legacy theme only.
13. No marketing gradients or glow fields inside the console — the radial pink glows live on the
    poster surfaces, which end at the sign-in boundary.

## 14. Quick Reference & Verification Gate

**Colour (role → light / dark):** canvas `#ffffff` / `#19191c` · raised `#ffffff` / `#1d1d21` ·
well `#f4f4f5` / `#141416` · wash `#f4f4f5` / `#2d2d31` · border subtle `#e7e7ea` / `#222224` ·
border strong `#71717b` / `#71717b` · focus `#db0060` / `#fd366e` · action `#db0060` / `#db0060` ·
vivid `#fd366e` / `#fd366e` · ink `#09090b` / `#fafafa` · ink-2 `#52525c` / `#d4d4d8` · ink-3
`#71717b` / `#9f9fa9` · success `#008138` / `#00c758` · warning `#b75000` / `#ffd236` · error
`#c20039` / `#fb2c36` · info `#0069a4` / `#77d4ff` · chart `#cd0071`+`#009588` / `#e80080`+`#00bb7f`.

**Type ramp:** F 16px base (Display 32/24/16/14/13) · S 14px base (18/16/14/13/13-stat/12) ·
D 12–13px base (12/13 grid, 13 mono log) · UI Inter 400/500/600 · display Aeonik Pro 400/500/600 ·
identifiers mono.

**Spacing + radius:** 4px grid, 8px comfortable (F/S), 4px dense · rows 40px S / 32px D · gutters
32/24/16 by mode · radius 2/6/10/16/full, base 10px.

**Component → token map:** Sidebar = canvas + wash(selected) + text.primary/tertiary + Meta ramp ·
Stat strip = raised + text.primary(stat)/tertiary(label) + border.subtle + tabular numerals ·
Chart = raised + chart.brand/teal + text.tertiary axes (mono) · CTA button = accent.action +
accent.onAction · Progress = accent.vivid + accent.subtle track · Table = canvas rows +
border.subtle rules + hover wash + Row ramps · Dialog = overlay + radius.lg + scrim · Terminal
drawer = surface.well + mono · Status badge = status wash + status colour + glyph.

**Pre-ship checklist.**
1. Zero raw hex outside L1 primitives.
2. No token resolves to a component name.
3. Every contrast pairing computed, passing, unrounded — the documented vivid-pink large-text
   exception is the only non-4.5 pairing and it never carries body-size text.
4. Every semantic role has a value in both shipped modes.
5. Every fetching surface has loading/empty/error/offline specified.
6. Every component row lists disabled and loading states.
7. Row, header, toolbar and pagination heights agree.
8. Reduced-motion variant written for every authored motion.
9. Every control keyboard-reachable with a visible focus indicator.
10. Dark authored, not filtered, with `border.strong` doing work that light delegates to hairlines.
11. No unoverridden stock default inside a committed surface.
12. Nothing came from a marketing page — the console spec is grounded in the console hero and
    shipped console tokens; posters supplied brand posture only.
