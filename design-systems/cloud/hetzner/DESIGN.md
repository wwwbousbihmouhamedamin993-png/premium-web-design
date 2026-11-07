# Design System — Hetzner Cloud Console

<!-- premium-web-design:design-system 2 -->
<!-- As-of: 2026-11-02 -->
<!-- Reference inspirations: Hetzner press kit brand values (hetzner.com/pressroom, rung 2 — official red/grey hexes), Hetzner Cloud Console production stylesheet tokens extracted verbatim (console.hetzner.cloud app bundle, rung 2 — brand/grey/green/orange/red scales, semantic layers, fonts, radii, shadows, row metrics), verified docs-hosted console screenshots (rung 3 grounding) -->
<!-- Surface classes: 12 routes classified; density classes S + D assigned (F reserved for auth/checkout) -->

## 1. Design Posture & Atmosphere

The Hetzner Cloud Console is a **ledger sheet with a German accent** — a functional, frugal, honestly
engineered workspace where a server is a row with a name, an IPv4, a status dot, an hourly cent-rate
and a kebab menu. Hetzner sells "fair prices, run in our own data centers", and the console inherits
that posture: nothing ornamental, everything measured, every screen answering "what do I have, where
does it run, what does it cost per hour". After eight hours the surface should feel like a well-kept
warehouse ledger — dry, legible, unexhausting — with the brand red spent as carefully as the budget
it reports.

Against its category defaults, Hetzner sits at the *most utilitarian* end of the cloud-console
spectrum: less stylised than DigitalOcean, far less layered than AWS, and deliberately narrower in
chromatic range than GCP. The single visual metaphor is a **stock ledger**: uppercase column heads
rule every data surface, identifiers and addresses render in monospace, and status is a small
glyph-plus-word — running, stopped, errored — never colour alone.

The brand palette is austere and pre-dates the console: an official primary red (#d50c2d in print,
shipped in-product as #d50c2e), two press-kit greys (#3c3c3b, #f5f5f5) and white. The console builds
a complete dual-mode token system on top — a 350°-hue red scale, neutral grey and dark-grey ramps, a
green/orange/red status trio, and one stray Hetzner yellow (#fdc200) held in reserve. Type is
Montserrat for headings, Inter for everything else, Hack for the embedded web terminal. The red is
the *only* loud thing in the room, and it appears once per view.

**Key Characteristics** —

- Canvas is never pure white: the working canvas is #f5f5f5 with #ffffff cards; dark canvas is
  #141414, not black. Both press-kit greys (#f5f5f5, #3c3c3b) survive inside the product tokens.
- One accent fill per viewport: the red primary button (or the red link) — never both competing.
  Accent budget: 1 saturated fill + status glyphs per view.
- Uppercase 12px column headers on every data table — the console's strongest stylistic signature.
- Rows are 40px standard (10px vertical padding), 32px dense; header, toolbar and pagination match
  the row height so the horizontal rules run unbroken edge to edge.
- Identifiers are monospace: IPv4/IPv6, MAC addresses, server IDs, ISO images, log lines and the
  embedded web console all render in Hack.
- Status is a glyph + word + colour triple: running (green #16a54d), warning/pending (orange),
  errored (red), inactive (grey #b8b8b8). Never colour alone.
- Radii are small and disciplined: 6px is the workhorse (buttons, cards, cells, inputs); 12px for
  side sheets and large panels; 999px pills for badges only.
- Shadows exist in light mode only (three quiet levels, ~10% black); dark mode separates surfaces
  with luminance steps and 1px keylines, zero shadows.
- Depth is a 6-step surface ramp per mode (light: #f5f5f5 canvas → white layers; dark: #141414 →
  #3d3d3d) plus 1px hairlines — never stacked drop shadows.
- Type is stepped, never fluid: 10 / 12 / 13 / 14 / 16 / 18 / 20 / 24 / 30 / 36px; no fluid sizing.
- Headings are Montserrat (500–600); body, rows and controls are Inter (400–600); the two never mix
  inside a paragraph. Montserrat never sets body copy.
- Spacing sits on a 4px grid with a 10px intra-component gap; page gutter 24px (a measured 25px in
  production normalises to the grid).
- The web terminal is a first-class surface: full-bleed Hack mono on near-black, its own scrollbar,
  immune to theme accenting.
- Hetzner yellow #fdc200 exists in the token file but is confined to brand/spotlight moments — it
  never appears as a status or action colour in the console.

## 2. Token Architecture   ← normative

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value*: `brand.50` … `brand.900` (350°-hue red scale),
  `grey.50` … `grey.900` (neutral light surfaces), `darkgrey.100` … `darkgrey.900` (neutral dark
  surfaces), `green.100` … `green.900` (143° hue), `orange.100` … `orange.900` (37° hue), `red.100`
  … `red.900` (0° hue), `yellow.brand` #fdc200, plus type sizes, weights, spacing steps, radii.
  Referenced only by L2. Banned: component-prop naming (`--card-bg`, `--tooltip-color`) — one value,
  many roles.
- **L2 Semantic** — role names: `surface.canvas`, `surface.raised`, `surface.overlay`, `surface.inset`,
  `surface.hover`, `surface.selected`, `border.subtle`, `border.strong`, `border.focus`,
  `accent.action`, `accent.onAction`, `accent.link`, `text.primary`, `text.secondary`, `text.tertiary`,
  `text.disabled`, `text.link`, `status.success`, `status.warning`, `status.error`, `status.neutral`
  (each with `…Wash` / `…Text` / `…Glyph` companions). The only layer a component may consume.
- **L3 Component** — only for deliberate deviation, e.g. `terminal.background` (points at
  `darkgrey.900`, not a raw hex), `table.headerLabel` (points at `text.secondary` + uppercase
  treatment), `badge.new.background` (brand gradient). Points at L2 or L1; never a raw value; never a
  sibling component's token.

**Rules.** Every token has a determinable type (colour, dimension, font-family, duration, shadow,
radius) or it is invalid; names are case-sensitive and free of `$`, `{`, `}`, `.`; circular references
are an error. Every semantic token has a value in **every** shipped mode — the console ships light,
dark and auto, so each L2 role carries a light and a dark resolution; a role with no dark value
resolves to its light value and fails contrast. Animatable tokens (focus ring spread, row hover fill)
are registered with syntax + inherits declared and a computationally independent initial value —
percent-based initial values are illegal.

**Layer order (low → high)** `reset → primitives → semantic → components → utilities`. Layer order
beats specificity entirely, and a stray un-layered declaration would outrank this whole system —
anything a consumer must override without `!important` sits in the top layer. The auto theme mode
resolves primitives before semantics: the semantic layer never branches, only the primitive binding
does.

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` | #f5f5f5 | #141414 | page background both modes (press grey survives) |
| `surface.raised` | #ffffff | #262626 | cards, table rows, panels |
| `surface.overlay` | #ffffff | #303030 | dropdowns, popovers, select menus |
| `surface.inset` | #ededed | #1a1a1a | wells, code blocks, terminal gutters |
| `surface.hover` | #e8e8e8 | #2b2b2b | row/menu hover fill (1px hairline visible beneath) |
| `surface.selected` | #fee7eb | #3a2028 | selected row: brand-100 wash / dark red-tinted step |
| `border.subtle` | #e8e8e8 | #303030 | 1px hairlines, card edges, row separators |
| `border.strong` | #595959 | #8a8a8a | 1px emphasis rules, table head underline |
| `border.focus` | #d50c2e | #f55b75 | 1px focus ring ≥3:1; never removed without replacement |
| `accent.action` | #d50c2e | #c10b29 | primary fill (brand-500 / brand-600) |
| `accent.onAction` | #fee7eb | #fee7eb | text on primary fill (brand-100, both modes) |
| `accent.subtle` | #fef1f3 | #3a2028 | brand washes, selected states, badge backgrounds |
| `text.link` | #d50c2e | #f55b75 | link text (5.36:1 / 5.82:1 on their canvases) |
| `text.primary` | #383838 | #ededed | ink ramp head (grey-900 / darkgrey-100) |
| `text.secondary` | #595959 | #cccccc | labels, column heads, supporting copy |
| `text.tertiary` | #8a8a8a | #8a8a8a | meta, timestamps; never body copy; ≥3:1 floor |
| `text.disabled` | #8a8a8a | #595959 | pairs with a stated reason on focus/hover |
| `status.success` | #117939 text · #e9fcf0 wash · #16a54d glyph | #3ee57e text · #344e3e wash | running, active, healthy |
| `status.warning` | #7a4e06 text · #fdefd8 wash · #dc8c0a glyph | #f7bc5e text · #51483b wash | pending, low disk, snapshot expiry |
| `status.error` | #cc0000 text · #ffe5e5 wash · #d40c2e glyph | #ff6679 text · #45232b wash | errored, deleted, failed |
| `status.neutral` | #595959 text · #f5f5f5 wash · #b8b8b8 glyph | #cccccc text · #303030 wash | stopped, inactive, queued |

Dark canvas is **not** pure black: #141414 canvas stepping to #3d3d3d at the highest surface. Depth in
dark comes from surface steps and 1px strokes, never shadows. The console's own icon palette anchors
status glyphs at #17a64e (running), #f5a524 (clock/warning), #d40c2e (error) and #b8b8b8 (paused) —
all always accompanied by a text label.

**Contrast gate — computed, unrounded.** Body ≥4.5:1; large text ≥3:1; UI boundaries and focus
indicators ≥3:1 (W3C, SC 1.4.3 / 1.4.11). 4.499:1 fails.

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| text.primary (L) | #383838 | surface.canvas | #f5f5f5 | 10.76:1 | 4.5 | pass |
| text.primary (L) | #383838 | surface.raised | #ffffff | 11.73:1 | 4.5 | pass |
| text.secondary (L) | #595959 | surface.canvas | #f5f5f5 | 6.42:1 | 4.5 | pass |
| text.secondary (L) | #595959 | surface.raised | #ffffff | 7.0:1 | 4.5 | pass |
| text.tertiary (L) | #8a8a8a | surface.raised | #ffffff | 3.45:1 | 3.0 | pass — meta only, never body |
| accent.onAction | #fee7eb | accent.action (L) | #d50c2e | 4.55:1 | 4.5 | pass |
| text.link (L) | #d50c2e | surface.raised | #ffffff | 5.36:1 | 4.5 | pass |
| text.link (L) | #d50c2e | surface.canvas | #f5f5f5 | 4.91:1 | 4.5 | pass |
| border.strong (L) | #595959 | surface.raised | #ffffff | 7.0:1 | 3.0 | pass |
| border.focus (L) | #d50c2e | surface.raised | #ffffff | 5.36:1 | 3.0 | pass |
| status.success text (L) | #117939 | success wash | #e9fcf0 | 5.15:1 | 4.5 | pass |
| status.warning text (L) | #7a4e06 | warning wash | #fdefd8 | 6.34:1 | 4.5 | pass |
| status.error text (L) | #cc0000 | error wash | #ffe5e5 | 4.93:1 | 4.5 | pass |
| text.primary (D) | #ededed | surface.canvas | #141414 | 15.74:1 | 4.5 | pass |
| text.primary (D) | #ededed | surface.raised | #262626 | 12.93:1 | 4.5 | pass |
| text.secondary (D) | #cccccc | surface.canvas | #141414 | 11.47:1 | 4.5 | pass |
| text.secondary (D) | #cccccc | surface.raised | #262626 | 9.42:1 | 4.5 | pass |
| text.tertiary (D) | #8a8a8a | surface.raised | #262626 | 4.38:1 | 3.0 | pass — meta only |
| text.link (D) | #f55b75 | surface.canvas | #141414 | 5.82:1 | 4.5 | pass |
| accent.onAction (D) | #fee7eb | accent.action (D) | #c10b29 | 5.33:1 | 4.5 | pass |
| border.strong (D) | #8a8a8a | surface.raised | #262626 | 4.38:1 | 3.0 | pass |
| status.success text (D) | #3ee57e | success wash | #344e3e | 5.51:1 | 4.5 | pass |
| status.warning text (D) | #f7bc5e | warning wash | #51483b | 5.26:1 | 4.5 | pass |
| status.error text (D) | #ff6679 | error wash | #45232b | 4.86:1 | 4.5 | pass |

Two observed production pairings were recalibrated by this spec and ship no further: brand-700 green
(#16a54d) on its own 95%-lightness wash computes to 3.01:1 and orange-700 (#dc8c0a) on its wash to
2.37:1 — both fail SC 1.4.3 for text, so status *text* steps to the darker scale entries above and
the 700-step values are demoted to glyph/dot fills (3:1 non-text budget) always paired with a word.

## 4. Typography

**Families.** UI **Inter** — weights 400 (body), 500 (labels, row primaries), 600 (buttons, stat
values); self-hosted as woff2, preloaded for 400/500/600; fallback `sans-serif`. Display
**Montserrat** — weights 500 and 600 for page titles, section titles, dialog headlines, empty-state
headlines and hint headers; never body, never data. Numeric/code **Hack** — 400 only — for IPv4/IPv6,
MACs, server/volume IDs, ISO names, log lines, and the embedded web console; *monospace is for
identifiers and code, never a costume.* Both display and UI families ship a shared fallback so a
Montserrat heading degrades to Inter, not to a system serif.

**One ramp table per class, not one blended table.** Columns: role, size, weight, line height,
tracking, numerals, use.

- **[F] Focused, 16px base** — auth, checkout, destructive-confirm detail:

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Display | 36px | Montserrat 600 | 1.2 | -0.01em | default | auth/checkout hero line |
| Heading | 24px | Montserrat 600 | 1.25 | -0.005em | default | dialog/step title |
| Body | 16px | Inter 400 | 1.5 | default | default | form prose, explanations |
| Label | 14px | Inter 500 | 1.4 | default | default | field labels |
| Meta | 13px | Inter 400 | 1.4 | default | default | helper text, price footnotes |

- **[S] Standard, 14px base** — project home, resource detail, settings:

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Page title | 24px | Montserrat 600 | 1.25 | -0.005em | default | "Servers", project name |
| Section title | 18px | Montserrat 500 | 1.25 | default | default | card/panel headings |
| Body | 14px | Inter 400 | 1.5 | default | default | descriptions, empty-state copy |
| Row primary | 14px | Inter 500 | 1.4 | default | default | server name, volume name |
| Row secondary | 13px | Inter 400 | 1.4 | default | default | location, image, attached-to |
| Stat value | 20px | Inter 600 | 1.3 | default | tabular | traffic, cost, count |
| Stat label | 12px | Inter 500 | 1.3 | 0.04em, uppercase | default | tile captions |
| Meta | 12px | Inter 400 | 1.4 | default | default | created date, ID prefixes |

- **[D] Dense, 13px base, data surfaces only** — server/volume/LB tables, activity log, metrics:

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Grid header | 12px | Inter 600 | 1.3 | 0.04em, uppercase | default | column heads |
| Grid cell numeric | 13px | Inter 400 | 1.35 | default | tabular | price, size, traffic |
| Grid cell text | 13px | Inter 400 | 1.35 | default | default | names, statuses |
| Grid identifier | 13px | Hack 400 | 1.35 | default | tabular | IPs, IDs, MACs |
| Log line | 12px | Hack 400 | 1.45 | default | tabular | activity entries, console |
| Inline help | 12px | Inter 400 | 1.4 | default | default | form hints below fields |

*Prose inside a dense screen (a description panel beside the table) still steps up to the 14px [S]
body role.*

**Invariants.** `tabular-nums` on every comparable value — hourly/ monthly prices, traffic GB,
timestamps, request counts, port numbers, IP octets. Right-align numerics, left-align text, never
centre a numeric column. Fixed stepped sizes only; no fluid `clamp()` sizing. Measure ≤80 characters —
65–80ch [F/S], unconstrained inside [D] cells.

## 5. Spacing Scale & Density Scales   ← two axes, never one

**Spacing base: 4px grid; 8px comfortable [F/S], 4px [D].** Production measures 25/15/10px outer
gaps; the scale normalises them onto the grid.

`space.0` 0 · `1` 4px icon-to-label · `2` 8px control padding [D] · `2.5` 10px intra-component gap
(production's `gap-between`/`gap-outer` compact) · `3` 12px cell padding [S], badge padding (4px 10px)
· `4` 16px card padding [S] / compact gutter · `5` 20px table cell horizontal padding (production
20px, kept) · `6` 24px page gutter + card padding [F] + section gap · `8` 32px section gap [S] ·
`12` 48px region separation · `16` 64px rarely (marketing-adjacent auth only). *No 25px. No 17px. If
a layout needs an off-scale value, the layout is wrong.*

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | Login, checkout, delete-server confirm |
| `standard` | 40px | 14px | 12–16px (10px vert. observed) | 24px | Project home, resource detail, settings |
| `dense` | 32px | 13px | 8px (6px vert.) | 16px | Resource tables, activity log, metrics, terminal |

- Density comes from **row height, column pruning and leading** — never from type too small to read.
  A 13px tabular cent-rate in a dense table is correct; the same numeral in a Focused form is a
  defect.
- **Never switch mid-page.** A server detail page is standard top to bottom; its attached-networks
  table may be dense only as a visually complete sub-surface with its own ruled header. Switching
  across routes with different jobs is legitimate — it should feel like a different room.
- **Chrome follows rows.** Toolbar, filter bar, batch bar and pagination heights match the table's
  row height (40px standard / 32px dense). A 48px toolbar over 40px rows is a rhythm break.
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40%. *House heuristic — validate by
  screenshot.*

## 6. Radius Scale

`none` 0 table cells, terminal, full-bleed panels · `xs` 2px tiny status dots' containers, inline
code chips · `sm` 4px inputs, dense cells, checkboxes · `md` 6px buttons, cards, rows, select boxes,
tooltips (production's dominant radius, 60%+ of uses) · `lg` 12px side sheets, large panels, project
badges · `full` 999px status pills, avatars, icon buttons. **One radius per component family** —
buttons are always `md`, side sheets always `lg`; never mixed ad-hoc. Nested radii obey
`radius_inner = radius_outer − padding`.

## 7. Elevation

**Choose one strategy, never mix paradigms.** Light: multi-layer ambient shadows + hairline. Dark:
surface-luminance steps + 1px keylines, **zero shadows** — a drop shadow is invisible on #141414.

Levels, low → high: **0** canvas (no shadow, both modes) · **1** card/row (light: `0 1px 3px
rgba(0,0,0,0.10), 0 1px 2px rgba(0,0,0,0.06)` + `border.subtle`; dark: one step up, keyline) ·
**2** sticky header/toolbar, hover popovers (light: `0 4px 6px rgba(0,0,0,0.10), 0 2px 4px
rgba(0,0,0,0.06)` + `border.strong`; dark: step up + `border.strong`) · **3** dropdown/side sheet
(light: `0 20px 25px rgba(0,0,0,0.10), 0 10px 10px rgba(0,0,0,0.04)` + `border.strong`, `radius.lg`;
dark: top step + `border.strong`) · **4** dialog (level 3 + scrim `rgba(0,0,0,0.5)` light /
`rgba(0,0,0,0.7)` dark). Inputs additionally accept a 2px-deep inset well (`inset 0 2px 4px
rgba(0,0,0,0.05)`) in light mode. Focus is never a shadow: it is a 1px ring in `border.focus`
(spread via ring, not blur).

## 8. Motion

`instant` 0ms (state text, badge flips) · `fast` 120ms ease-out (exits [D], row hover fill 150ms
measured) · `base` 180ms decelerate ([D] entrances, menu/ppopover fade-slide) · `slow` 240–300ms
decelerate ([F/S] entrances, side sheet slide-in, dialog scale-fade).

- Entrances decelerate, exits accelerate. Symmetric ease-in-out on both directions is a defect.
- Animate `transform` and `opacity` only — never width, height, top, left. Table row hover is a fill
  fade, not a geometry change; box-shadow transitions 150ms on card hover.
- No bounce on irreversible moments: not on the delete-server confirm, not on a downgrade or
  power-off. A 240ms fade to the confirmation state, then done.
- **Reduced motion is a real variant**, not `animation: none` everywhere: movement → crossfade under
  ~150ms; the side sheet and terminal cursor keep their positions while losing travel; polling
  spinners become static labels ("Refreshing…").

## 9. Imagery & Art Direction

- **Brand moment:** the login/entry surface and empty-state art — datacenter photography (Hetzner's
  own Nuremberg/Falkenstein/Helsinki halls) and the red wordmark, plus the reserved Hetzner yellow
  #fdc200 in spotlight/celebration moments. Its palette **never leaks into UI tokens**: yellow and
  photographic hues appear nowhere in §3. One saturation moment per surface, not a recurring accent.
- **Iconography:** single custom set, 16px on a 16px grid with 1–1.5px strokes, geometric and
  slightly condensed to match Inter's tone; status glyphs may fill (`hc`-style status icons) but stay
  ≤16px. Filled variants only where a stroke cannot carry 16px. Icon-only controls still carry a
  label (§10).
- **Photography:** real datacenter and hardware photos for brand/empty moments; no stock people, no
  abstract gradients. Third-party OS logos (Debian, Ubuntu, Fedora) render as small monochrome or
  official-mark circles inside the committed image-picker surface — never re-coloured.
- **Illustration / 3D:** none. The console does not use illustration; empty states are text + CTA.
- **Empty / error art:** no illustration substitutes for the recovery CTA — an empty servers list is
  one line of explanation, a dashed-border "Add Server" action, and the docs link. An unspecified gap
  here invites per-screen invention; the rule is text-first, always with an escape hatch.

## 10. Surface & Component Inventory

One row per real component; a component without documented disabled and loading states is unfinished.

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell/sidebar | S | collapsed, project-switcher | hover, active nav, loading | full nav, `Tab` order top-down | project name + env badge |
| Data table | D | servers, volumes, LBs, networks, snapshots | hover, selected, loading skeleton, empty, error, stale | arrows + `Space` select, `Esc` clear | "Name", uppercase heads |
| Filter/search bar | S/D | text filter, status chips, label filter | focused, filled, cleared | `/` focus, `Esc` reset | "Filter by name or label…" |
| Row action menu | D | kebab per row | focus-trap, hover, disabled items, `Esc` close | arrows, `Enter`, `Esc` | "Power off", "Rebuild", "Delete" |
| Stat tile | S | traffic, cost, resource count | loading, delta-up/down | focusable, labelled | "Traffic this month" |
| Drawer/inspector (side sheet) | S | detail, create-form, labels | open, dirty, saving, error | `Esc` close, focus returned | "Edit Server" |
| Dialog | F | confirm-destructive, input | scrim click blocked on destructive, confirming, error | focus-trap, `Esc` cancels | names resource + cost + effective date |
| Plan/size control | F/S | shared vs dedicated CPU radio cards | selected, disabled (unavailable in location), price hover | arrows within radio group | "CX22 — €3.79/mo, 2 vCPU, 4 GB" |
| Member row | S | project members, permission select | pending invite, removing, error | row focus, menu | role + email |
| Audit entry | D | activity log line | expandable, loading older | `Enter` expand | "User X created server Y" |
| Status badge | D | running/stopped/error/pending | static, spinner-pending | non-interactive, labelled | word + glyph, never colour alone |
| Command palette / global search | S | resource jump, docs search | open (`Ctrl+K`), no results, recents | full keyboard, `Esc` | "Search resources…" |
| Web terminal | D | embedded console per server | connecting, connected, disconnected, reconnect | terminal-native; `Esc` exits focus | "Console — hack mono, near-black" |
| Pagination + page size | D | tables | disabled ends, current page | arrows, `Enter` | "Page 2 of 14 · 20 per page" |

**Every fetching surface also designs:** loading (skeleton matching final row geometry — row-height
placeholders, never a centred spinner on a blank page), empty (what's missing + the CTA that fixes
it: "No servers yet — Create your first server"), error (what happened + retry: "Could not load
volumes — Retry"), offline/stale (banner stating last-known data age, actions queued not lost).

**Contracts this table encodes:** one primary filled CTA per view [F/S] (dense toolbars may run a
primary plus icon actions); every icon-only control carries a label or tooltip; a disabled control
states *why* on focus or hover ("Unavailable in Falkenstein"); a button never changes width between
idle and loading — the spinner reserves the label's space.

## 11. Light / Dark Strategy

- **Posture: C dual-parity** — the console ships light, dark and auto (`auto` follows the OS until
  the user pins a mode). Reason: engineers run consoles in dark rooms; the token system is built
  symmetric, and both press-kit greys anchor one mode each (#f5f5f5 light canvas, #3c3c3b adjacent to
  the dark ramp).
- **Mechanism:** semantic roles remapped per mode via a root attribute (`light` / `dark` / `auto`);
  the primitive bindings branch, the semantic layer never does. **No role absent in either mode.**
  The only near-single-mode role is `accent.onAction` (#fee7eb in both — deliberately identical).
- **`color-scheme`** set on the root so UA chrome, form controls, scrollbars and the terminal's
  native widgets follow the pinned mode. It repaints UA-provided parts of the canvas only.
- **`<meta name="color-scheme">` in the head before the stylesheet**, to prevent a flash of the wrong
  scheme on the login round-trip.
- **Dark is authored, not inverted:** its own ramp (#141414 → #3d3d3d), its own stronger keylines
  (#8a8a8a borders vs light's #e8e8e8 hairlines — a delicate line on white is invisible on #141414),
  zero shadows, scrim deepened 0.5 → 0.7. Brand red shifts darker for fills (#c10b29) and lighter for
  text (#f55b75) — the same hue value, two jobs.
- Org-tinting (D) is not offered; a tenant white-label would change colour tokens only, with radii,
  type sizes and layout frozen so a theme swap cannot move anything.

## 12. Density-Mode Strategy

- **Default mode per surface class:** Standard everywhere except resource tables/logs/metrics
  (Dense) and auth/checkout/destructive confirms (Focused). The boundary is the job: reading and
  deciding → Standard; comparing many rows → Dense; committing → Focused.
- **Mechanism:** a density attribute on the app root rescales row height, cell padding, gutter and
  body size together as one token axis — spacing tokens do not change per screen size; density is
  not a media query.
- **Container queries for reflow:** panels reflow to their container, not the viewport; `cq*` units
  are never used where the no-eligible-container fallback (small-viewport units) would be wrong —
  table columns use fixed + proportional tracks instead.
- **Style queries** compare computed values, so the density marker is registered as a typed custom
  property before any style query consumes it.
- **Offer the switch as an accessibility affordance**, not a preference: Dense ↔ Standard is
  available on every data surface for users with visual field loss, persisted per user.

## 13. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA (7:1) on body text in Focused surfaces.
- **Target size:** ≥24×24 CSS px hard minimum (2.5.8 spacing exception honoured); 40px row-height
  click targets and 32px+ buttons are the design target for primary controls [F/S]. *Zoom does not
  excuse it.*
- **Keyboard:** every function operable; focus indicator visible — a 1px `border.focus` ring plus
  2px offset, never removed without a stronger replacement; the focused row never hidden by the
  sticky table header (scroll-margin equal to header height).
- **Contrast:** text ≥4.5:1 (computed §3); UI boundaries and focus ≥3:1. **Colour independence:**
  every status pairs colour with glyph and word; power state deltas carry direction glyphs
  (power-on/power-off arrows), cost deltas a sign.
- **Motion:** the §8 reduced-motion variant per component; the terminal cursor blink is exempt as
  user-content but pauses when unfocused.
- **Text:** ≤80-character measure, 1.5 leading on prose, 200% resize without horizontal scroll on
  Standard surfaces; dense tables scroll horizontally *as tables*, not page-wide.
- **Semantics:** real buttons/links/inputs; table markup with scoped headers; headings match visual
  rank (page title → section titles); `aria-live="polite"` for power-state changes and billing
  updates; `aria-busy` on loading regions; the terminal is an off-by-default application role with
  documented focus entry/exit.
- **Contrast preference:** `prefers-contrast: more` promotes `text.secondary` → `text.primary`
  values and doubles hairline strength to `border.strong`.

## 14. Anti-Patterns

**Do** —

1. Spend red once per view — one primary button or one link cluster; rationale: the brand's only
   saturated colour dies by dilution.
2. Uppercase every table column head at 12px/600 — it is the console's legibility signature and
   costs nothing in a hairline-ruled table.
3. Render every IP, ID and MAC in Hack mono with `tabular-nums` — copy-paste fidelity is a hoster's
   contract with its user.
4. Pair every status with glyph + word + colour — red-green colour blindness is non-negotiable in a
   monitoring surface.
5. Keep the canvas off-white (#f5f5f5) and cards white — depth must stay readable without shadows.
6. Match toolbar/pagination height to row height — an unbroken rule reads as one instrument.
7. Show the hourly and monthly price together on every paid control — Hetzner's "fair prices" claim
   is audited inside the product.
8. Name the location on every resource row (Falkenstein, Nuremberg, Helsinki) — geography is a
   first-class attribute, not metadata.
9. Use #141414, never #000000, for dark canvas — pure black crushes the ramp and makes keylines
   invisible.
10. Keep the terminal mono and near-black regardless of theme — it represents a remote machine, not
    the console.
11. Reserve #fdc200 and photography for brand/empty moments — scarcity is what makes them land.
12. State why a control is disabled on focus/hover — a dead "Create Load Balancer" button with no
    reason reads as a bug.

**Don't** —

1. Don't use pure #ff0000 or the print red #d50c2d interchangeably with the token red — the console
   red is #d50c2e and fills use the 600-step in dark; off-by-one reds fragment the brand.
2. Don't set body or data text in Montserrat — it is display-only; Inter does the work.
3. Don't ship two primary filled buttons in one viewport — the second action becomes a secondary.
4. Don't stack shadows for depth in dark mode — use a surface step; shadows don't render on #141414.
5. Don't drop the uppercase treatment from column headers "for a modern look" — it is the table's
   voice.
6. Don't replace status words with dots — a green dot without "running" fails 1.4.1 and 1.4.11.
7. Don't tint the brand red toward pink for marketing vibes inside the product — the 350° hue is
   fixed; only lightness steps (§3) are permitted.
8. Don't put a card inside a card inside a card — one raised surface per layer; use hairlines for
   further subdivision.
9. Don't use alert()/confirm() for destructive flows — the delete dialog names the resource, its
   cost and the recovery horizon (none).
10. Don't shrink type below 12px to fit a table — prune columns; 10px is reserved for icon glyphs.
11. Don't centre numeric columns or let prices render in proportional figures — auditors diff these
    numbers.
12. Don't let the marketing site's gradient/photography language bleed into product surfaces — the
    console is achromatic plus one red.

## 15. Quick Reference & Verification Gate

**Colour (flat).** Light: canvas #f5f5f5 · raised #ffffff · overlay #ffffff · inset #ededed · hover
#e8e8e8 · selected #fee7eb · border.subtle #e8e8e8 · border.strong #595959 · border.focus #d50c2e ·
accent.action #d50c2e · onAction #fee7eb · link #d50c2e · text #383838 / #595959 / #8a8a8a · success
#117939/#e9fcf0 · warning #7a4e06/#fdefd8 · error #cc0000/#ffe5e5 · neutral #595959/#f5f5f5.
Dark: canvas #141414 · raised #262626 · overlay #303030 · inset #1a1a1a · hover #2b2b2b · selected
#3a2028 · border.subtle #303030 · border.strong #8a8a8a · border.focus #f55b75 · accent.action
#c10b29 · onAction #fee7eb · link #f55b75 · text #ededed / #cccccc / #8a8a8a · success
#3ee57e/#344e3e · warning #f7bc5e/#51483b · error #ff6679/#45232b · neutral #cccccc/#303030.

**Type ramp (flat).** Montserrat 600: 36/24 display-heading; Montserrat 500: 18 section.
Inter 600: 20 stat, buttons; Inter 500: 14 row-primary, 12 uppercase labels; Inter 400: 16 [F] body,
14 [S] body, 13 rows, 12 meta. Hack 400: 13 identifiers, 12 log/console.

**Spacing + radius (flat).** 4 / 8 / 10 / 12 / 16 / 20 / 24 / 32 / 48 / 64px. Radius 2 / 4 / 6
(workhorse) / 12 / 999px. Row 40px [S], 32px [D]; chrome follows rows. Gutter 24px.

**Component → token map.** Primary button: `accent.action` + `accent.onAction` + `radius.md`.
Secondary button: `surface.raised` + `border.strong` + `text.primary`. Table: `surface.raised` rows
on `surface.canvas`, `border.subtle` rules, `text.secondary` uppercase heads, `text.primary` row
primary, Hack identifiers. Status badge: `status.*Text` on `status.*Wash` + `radius.full`. Side
sheet: `surface.raised`/`radius.lg` + level-3 elevation. Terminal: `darkgrey.900` + Hack +
`border.subtle`. Dialog: level-4 + `radius.lg` + scrim. Focus everywhere: `border.focus` ring.

**Agent prompt block.**

- Tokens: consume semantic roles only — surface.canvas #f5f5f5/#141414, surface.raised #ffffff/
  #262626, accent.action #d50c2e/#c10b29, accent.onAction #fee7eb, text.primary #383838/#ededed,
  text.secondary #595959/#cccccc, text.tertiary #8a8a8a, border.subtle #e8e8e8/#303030,
  border.strong #595959/#8a8a8a, border.focus #d50c2e/#f55b75, status success/warning/error/neutral
  text+wash pairs per §3. Type: Montserrat display 36/24/18 (weights 600/500), Inter UI 16/14/13/12
  (weights 400–600), Hack mono for identifiers/logs. Spacing 4/8/10/12/16/20/24/32/48. Radius 2/4/6/
  12/999. Rows 40px [S], 32px [D]; chrome matches row height.
- Worked prompt 1 — *Servers list surface*: `surface.canvas` background; table on `surface.raised`
  with `border.subtle` hairlines; 12px Inter 600 uppercase column heads in `text.secondary` with
  0.04em tracking; 40px rows; name in `text.primary` 14px/500, IPv4 in Hack 13px, price right-aligned
  `tabular-nums`; status badge = glyph + word on `status.*Wash`; one `accent.action` "Create Server"
  button, `radius.md`; skeleton rows match final geometry; empty state names the fix.
- Worked prompt 2 — *Delete-server dialog*: level-4 elevation, `radius.lg`, scrim rgba(0,0,0,0.5)
  light / 0.7 dark; Montserrat 600 heading; body names resource name, location, monthly cost and the
  irreversibility in `text.primary` 16px; destructive confirm button `accent.action` with
  `accent.onAction` label, never red-on-red gradient; focus-trapped, `Esc` cancels, focus returns to
  the row's kebab.
- Worked prompt 3 — *Web terminal*: full-bleed #141414 panel, Hack 12px, 1.45 line height,
  `border.subtle` 1px frame; no theme accenting; connecting/disconnected states as inline `text
  .secondary` labels; reduced-motion keeps cursor static when unfocused.

**Pre-ship checklist.** 1 Zero raw hex outside L1. 2 No token resolves to a component name. 3 Every
contrast pairing computed, passing, unrounded. 4 Every semantic role has a value in every shipped
mode (light, dark, auto). 5 Every fetching surface has loading/empty/error/offline specified. 6 Every
component row lists disabled and loading states. 7 Row, header, toolbar and pagination heights agree.
8 Reduced-motion variant written for every authored motion. 9 Every control keyboard-reachable with a
visible focus indicator. 10 Dark authored, not filtered, with border strength exceeding light's. 11 No
unoverridden stock library default inside a committed surface. 12 Nothing came from a marketing page.
13 The §9 brand-moment palette (Hetzner yellow, photographic hues) appears nowhere in the UI token
layers.
