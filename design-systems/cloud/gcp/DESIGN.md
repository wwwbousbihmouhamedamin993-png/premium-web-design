# Design System — Google Cloud Console

<!-- premium-web-design:design-system 2 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: Google Material Design / Google product token documentation (colour + shell — rung 2: Google grey/blue ramps, Google Sans Text, M3 elevation), Google Cloud console screenshots — Logs Explorer + BigQuery Studio + marketing pages (density/type grounding — rung 3) -->
<!-- Surface classes: 4 route groups classified (console product pages, data/log surfaces, marketing landing, sign-in/billing entry); density classes S+D assigned (F reserved for sign-in, billing checkout, wizard review) -->

## 1. Design Posture & Atmosphere

The Google Cloud console is a Material Design instrument panel that has been laundering its own
saturation for a decade. Everything is white — white canvas, white cards, white left nav, white top
bar — and the near-black grey ink (#202124) does almost all of the communicative work. Colour is
rationed: one blue family owns every affordance (links, active tabs, primary fills, focus rings),
and the famous Google red/yellow/green quartet survives inside the product only as tiny 24px
product icons in the left nav and as chart series. After eight hours the surface reads as a very
clean, very quiet spreadsheet host — which is the point, because the console's real payload is tens
of thousands of table cells, log lines and metric points at 12–14px.

Against its category defaults (AWS's hairline containers, Azure's left-weighted grey portal), GCP
sits in the middle: more rounded and friendlier than AWS (8px controls, pill chips, 500-weight
labels), far quieter than Azure's portal. The visual metaphor is a **drafting table with a conductor's
baton** — drafting table because every resource surface is structured drawing (panels, gutters,
hairlines), conductor's baton because one blue gesture points at the single next action ("Run
query", "Create"). Data surfaces tip toward density without ever leaving Material's comfort: the
Logs Explorer packs a query editor, histogram and log stream into one white shell whose only
decoration is a blue bar chart.

**Key Characteristics**

- White-on-white layering: canvas #ffffff, cards #ffffff, separation by 1px #dadce0 hairlines and
  16px gutters — resting containers carry **no shadow at all**.
- One accent family per viewport: `accent.action` #1a73e8 (Google Blue 600) owns links, primary
  fills, active tabs and focus; nothing else in the UI is saturated.
- Text ink is grey, not black: #202124 primary, #5f6368 secondary, #80868b tertiary — never #000.
- The brand quartet (#4285f4 / #ea4335 / #fbbc04 / #34a853) renders **only** inside product icons,
  charts and the marketing logo — never as a button fill.
- Status always ships as glyph + word + colour; severity chips in logs are outlined pills, not dots.
- Left nav is 280px white with full-colour 24px product icons; it collapses to a 56px grey icon rail.
- Controls are soft but not pill-shaped in product UI: 8px radius on buttons, inputs and chips;
  pills are reserved for marketing CTAs and filter chips.
- Google Sans (display/headings) + Google Sans Text (UI) + Roboto Mono (queries, logs, IDs) —
  geometric, friendly, never condensed.
- Rows are 48px standard, 32–40px dense; tabular numerals on every timestamp, count and cost.
- Motion is Material's 200ms decelerate emphasis curve; exits 100ms; reduced motion resolves to 0ms.
- Dark mode is fully authored (canvas #202124, accent #8ab4f8) but light is the shipped default.
- Marketing pages (cloud.google.com) are a different room: 24px-radius media cards, 64px Google Sans
  display numerals, pill buttons — their palette never leaks into console tokens.

## 2. Token Architecture   ← normative

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value* (`grey.900`, `blue.600`, `green.800`,
  `wash.green.50`), referenced only by L2. The primitive ramps are the published Google colour
  ramps: grey (#ffffff → #202124), blue (#e8f0fe → #174ea6), green, yellow, red, plus the brand
  quartet held aside as `brand.blue/red/yellow/green`. Banned: `[component]-[prop]` naming — one
  value, many roles. (Google's own production CSS names tokens like `gm-ink-1`/`gm-rule`; those
  single-purpose names are the historical shape this spec's L2 replaces with `text.primary` /
  `border.subtle`.)
- **L2 Semantic** — role names (`surface.canvas`, `text.primary`, `accent.action`). The only layer a
  component may consume. Every role listed in §3 has a value in **both** shipped modes.
- **L3 Component** — only for deliberate deviation; points at L2 or L1, never a raw value, never a
  sibling component's token. Example: the query editor consumes `code.ink` → `text.primary` and
  `code.string` → `green.800` as an L3 exception because syntax colouring is a deliberate
  deviation from the ink ramp.

**Rules.** Every token has a determinable type or it is invalid; names are case-sensitive, no `$`,
`{`, `}`, `.`; circular references are an error. Every semantic token carries a value in every
shipped mode — a role with no dark value resolves to its light value and fails contrast. Animatable
tokens (the two easing curves, three durations) are registered with an explicit type and an
inheritance declaration or the registration is invalid, and an initial value must be
computationally independent — so percentage- or em-based initial values are illegal on them.

**Layer order (low → high)** `[reset] → [primitives] → [semantic] → [components] → [utilities]`.
Layer order beats specificity entirely, and an un-layered normal declaration outranks everything
layered — a stray un-layered rule in a service team's stylesheet would beat this whole system.
This matters double at Google scale: hundreds of product surfaces ship into one shell, and the
layer contract is what keeps a 2019-era service page from overwriting the current refresh.

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` | #ffffff | #202124 | Page background — light canvas is pure white |
| `surface.raised` | #ffffff | #292a2d | Cards, panels, dropdowns (dark steps one level up) |
| `surface.overlay` | #ffffff | #35363a | Dialogs, menus on scroll |
| `surface.inset` | #f8f9fa | #171717 | Table header rows, code wells, wells, grey 50 |
| `surface.hover` | #f1f3f4 | #303134 | Interactive fill on rows, nav items, list tiles |
| `surface.selected` | #e8f0fe | #3c475b | Selected nav item, selected row, active tab wash (blue 50 / 26% blue-300 on canvas) |
| `border.subtle` | #dadce0 | #3c4043 | 1px hairlines — card outlines, dividers (decorative) |
| `border.strong` | #80868b | #9aa0a6 | Control outlines that must carry a boundary alone |
| `border.focus` | #1a73e8 | #8ab4f8 | Focus indicator, ≥3:1 on every surface it lands on |
| `accent.action` | #1a73e8 | #8ab4f8 | Primary fill ("Run query"), links, active tabs, toggles-on |
| `accent.onAction` | #ffffff | #202124 | Text/icon on the accent fill |
| `accent.subtle` | #e8f0fe | #2d333d | Accent washes: selected chips, drag placeholders |
| `text.primary` | #202124 | #e8eaed | Headings, body ink (grey 900 — never #000000) |
| `text.secondary` | #5f6368 | #bdc1c6 | Secondary body, form labels, nav items, timestamps |
| `text.tertiary` | #80868b | #9aa0a6 | Placeholder, disabled-adjacent hints, inactive meta |
| `text.disabled` | #9aa0a6 | #9aa0a6 | Paired with disabled fill; inactive-component exemption |
| `status.success` | #137333 | #81c995 | Green 800 — running, passing checks |
| `status.warning` | #a15c00 | #fdd663 | Deep amber — degraded, pending, quota pressure |
| `status.error` | #c5221f | #f28b82 | Red 700 — failed, stopped-with-error |
| `status.info` | #174ea6 | #8ab4f8 | Blue 900 — neutral notice |
| `status.wash.success` | #e6f4ea | #20342c | Banner and flash fills |
| `status.wash.warning` | #fef7e0 | #3a2f17 | |
| `status.wash.error` | #fce8e6 | #3a2422 | |
| `status.wash.info` | #e8f0fe | #233a52 | |
| `chrome.nav` | #ffffff | #292a2d | Top bar + left nav — white in light, stepped in dark |
| `chrome.onNav` | #5f6368 | #e8eaed | Nav labels, icons; the Google logo keeps brand colour |
| `brand.blue` / `brand.red` / `brand.yellow` / `brand.green` | #4285f4 / #ea4335 / #fbbc04 / #34a853 | same | Logo mark, product icons, chart series — **never a UI fill** |

Dark canvas is **not** pure black: #202124, stepping to #292a2d and #35363a. Depth in dark comes
from surface steps and 1px strokes, never shadows.

Two deliberate corrections against stock Google values, both forced by the gate below: the warning
ink deepens from the stock yellow-900 #b06000 (which measures 4.336:1 on its own yellow-50 wash) to
#a15c00 (4.843:1); and status inks on washes use the console's darker banner tones (green 800, red
700, blue 900) rather than the mid-tones the brand uses for large iconography. `border.subtle`
#dadce0 on white measures 1.373:1 and is intentionally below 3:1 — hairlines separate content that
is already separated by gaps and type; the *control boundary* role (`border.strong`, 3.684:1)
carries the non-text-contrast obligation. A divider that must communicate a boundary alone uses
`border.strong`.

**Contrast gate — computed per WCAG 2.2 relative-luminance formula, unrounded; large text is
≥24px or ≥18.5px bold; body ≥4.5:1; UI boundaries and focus ≥3:1.**

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| `text.primary` L | #202124 | `surface.canvas` L | #ffffff | 16.099:1 | 4.5:1 | PASS |
| `text.secondary` L | #5f6368 | `surface.canvas` L | #ffffff | 6.050:1 | 4.5:1 | PASS |
| `text.tertiary` L | #80868b | `surface.canvas` L | #ffffff | 3.684:1 | 3:1 house floor (muted/placeholder) | PASS |
| `text.disabled` L | #9aa0a6 | `surface.canvas` L | #ffffff | 2.641:1 | exempt (inactive component) | PASS (exempt) |
| `accent.onAction` L | #ffffff | `accent.action` L | #1a73e8 | 4.505:1 | 4.5:1 | PASS |
| `accent.action` L (links) | #1a73e8 | `surface.canvas` L | #ffffff | 4.505:1 | 4.5:1 | PASS |
| `border.strong` L | #80868b | `surface.raised` L | #ffffff | 3.684:1 | 3:1 | PASS |
| `border.focus` L | #1a73e8 | `surface.canvas` L | #ffffff | 4.505:1 | 3:1 | PASS |
| `status.success` L | #137333 | wash L | #e6f4ea | 5.242:1 | 4.5:1 | PASS |
| `status.warning` L | #a15c00 | wash L | #fef7e0 | 4.843:1 | 4.5:1 | PASS |
| `status.error` L | #c5221f | wash L | #fce8e6 | 4.920:1 | 4.5:1 | PASS |
| `status.info` L | #174ea6 | wash L | #e8f0fe | 6.846:1 | 4.5:1 | PASS |
| `chrome.onNav` L | #5f6368 | `chrome.nav` L | #ffffff | 6.050:1 | 4.5:1 | PASS |
| Stat numeral (marketing display) | #34a853 | white | #ffffff | 3.056:1 | 3:1 (large ≥24px only) | PASS (large) |
| `text.primary` D | #e8eaed | `surface.canvas` D | #202124 | 13.357:1 | 4.5:1 | PASS |
| `text.secondary` D | #bdc1c6 | `surface.canvas` D | #202124 | 8.898:1 | 4.5:1 | PASS |
| `text.tertiary` D | #9aa0a6 | `surface.canvas` D | #202124 | 6.097:1 | 4.5:1 | PASS |
| `accent.onAction` D | #202124 | `accent.action` D | #8ab4f8 | 7.639:1 | 4.5:1 | PASS |
| `accent.action` D (links) | #8ab4f8 | `surface.canvas` D | #202124 | 7.639:1 | 4.5:1 | PASS |
| `border.strong` D | #9aa0a6 | `surface.raised` D | #292a2d | 5.435:1 | 3:1 | PASS |
| `border.focus` D | #8ab4f8 | `surface.canvas` D | #202124 | 7.639:1 | 3:1 | PASS |
| `status.success` D | #81c995 | wash D | #20342c | 6.748:1 | 4.5:1 | PASS |
| `status.warning` D | #fdd663 | wash D | #3a2f17 | 9.366:1 | 4.5:1 | PASS |
| `status.error` D | #f28b82 | wash D | #3a2422 | 6.040:1 | 4.5:1 | PASS |
| `status.info` D | #8ab4f8 | wash D | #233a52 | 5.540:1 | 4.5:1 | PASS |
| `chrome.onNav` D | #e8eaed | `chrome.nav` D | #292a2d | 11.906:1 | 4.5:1 | PASS |
| `text.primary` D on raised | #e8eaed | `surface.raised` D | #292a2d | 11.906:1 | 4.5:1 | PASS |

Note on the newer Material 3 refresh tone: some 2024+ Google surfaces migrate the primary fill to
#0b57d0; #ffffff on #0b57d0 measures 6.386:1 and is an approved L3 swap for `accent.action` on
refreshed surfaces only — it never appears mixed with #1a73e8 fills inside one viewport.

## 4. Typography

**Families.** UI **Google Sans Text** — weights 400 (all body), 500 (labels, buttons, nav, table
headers), 700 (emphasis, dense headers); served by Google's font CDN (effectively self-hosted by
the shell), fallback `'Google Sans', Roboto, 'Helvetica Neue', Arial, sans-serif`. Headings and
marketing display render in **Google Sans** (the geometric display cut — 400/500 weights only;
Google headlines are never bold-black). Legacy surfaces render body in **Roboto** 400/500 —
treated as a fallback face, not a second system. Numeric/code: **Roboto Mono** 400/500 for query
editors, log lines, resource IDs, hashes, raw timestamps and JSON payloads. *Monospace is for
identifiers and code, never a costume.*

**One ramp table per class, not one blended table.** Columns: role, size, weight, line height,
tracking, numerals, use.

- **[S] Standard, 14px base (console default):**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Page title | 24px | 400 | 32px | normal | default | Service pages ("Logs Explorer") — Google Sans |
| Section title | 16px | 500 | 24px | normal | default | Panel headings, card titles ("Create new") |
| Body | 14px | 400 | 20px | normal | default | Primary prose, descriptions |
| Label / button | 14px | 500 | 20px | normal | default | Buttons, nav items, form labels, tabs |
| Row primary | 14px | 400 | 20px | normal | default | Table primary cell |
| Row secondary | 12px | 400 | 16px | normal | default | Sub-text, field descriptions |
| Stat value | 24–48px | 400 | ×1.2 | −0.25px | tabular | KPI numerals — Google Sans |
| Stat label | 12px | 400 | 16px | +0.1px | default | Tile captions, sentence case (Google does not shout) |
| Meta | 12px | 400 | 16px | normal | tabular | Timestamps, breadcrumbs-current, constraints |
| Link | 14px | 400/500 | 20px | normal | default | `accent.action`, may carry external-link glyph |

- **[D] Dense, 12–13px base (data surfaces only — tables, logs, metrics):**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Grid header | 12px | 500 | 16px | +0.2px | default | Column labels, uppercase-free |
| Grid cell text | 13px | 400 | 20px | normal | default | Compact rows |
| Grid cell numeric | 13px | 400 | 20px | normal | tabular | Counts, sizes, costs, IPs |
| Log line (mono) | 13px | 400 | 20px | normal | tabular | Logs Explorer entries, query text — Roboto Mono |
| Inline help | 12px | 400 | 16px | normal | default | *Prose inside a dense screen still steps up to 14px.* |

**Invariants.** `tabular-nums` on every comparable value — currency, timestamps, deltas, counts,
project numbers, instance IDs. Right-align numerics, left-align text, never centre a numeric
column. Fixed stepped sizes (12 / 13 / 14 / 16 / 24 / 32 / 48px); no fluid scaling inside the
console — marketing display sizes (64px hero numerals) live outside the token ramp. Measure ≤80
characters; 65–80ch in standard prose, unconstrained in dense data cells. Minimum rendered size
12px; 13px is the dense-mode body floor.

## 5. Spacing Scale & Density Scales   ← two axes, never one

**Spacing base: 4px grid; 8px comfortable standard, 4px dense.** `space.0` 0 · `1` 4px
icon-to-label, chip inner padding · `2` 8px control padding dense, card gaps · `3` 12px cell
padding, card padding dense · `4` 16px card padding standard, content gutter, section gap ·
`6` 24px section gap, page title block · `8` 32px region separation · `12` 48px rarely (marketing
sections only). *No 17px. No 23px. If a layout needs an off-scale value, the layout is wrong.*
Concrete shell dimensions: left nav 280px expanded / 56px icon rail; top bar 64px; page content
gutter 16px on data surfaces, 24px on reading surfaces; card-to-card gap 16px.

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| focused | — | 16px | 24px | 32px | Sign-in, billing checkout, wizard review steps |
| standard | 48px | 14px | 12–16px | 24px | Project home, resource detail, IAM list, service landing |
| dense | 32–40px | 12–13px | 8px | 16px | Resource tables, Logs Explorer stream, metric grids, query results |

- Density comes from **row height, column pruning and leading** — never from type too small to
  read. A 13px tabular numeral in a dense log table is correct; the same numeral in a focused
  form is a defect.
- **Never switch mid-page.** A service page is one mode; moving to the log stream is a different
  room, and that is legitimate.
- **Chrome follows rows.** Table toolbar, filter strip and pagination heights match the table's row
  height — a 48px toolbar over 32px dense rows is a rhythm break.
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40%. *House heuristic — validate
  by screenshot.*

## 6. Radius Scale

`none` 0 (table cells, dividers, code wells) · `xs` 4px checkboxes, dense inline controls · `sm`
8px buttons, inputs, selects, console cards, dropdowns, dialogs — **the product-UI workhorse** ·
`lg` 16px marketing cards, banners, promo wells · `full` pill — marketing CTAs, filter chips,
severity chips, avatars, toggle thumbs. **One radius per component family**, never mixed ad-hoc:
every console button is 8px, every console card 8px, every filter chip a pill. Nested radii obey
`radius_inner = radius_outer − padding`.

## 7. Elevation

**Strategy: hairline-first.** A resting console container has *no shadow* — separation is the 1px
`border.subtle` plus the gutter. Material's famous elevation stack is reserved for transient
surfaces (its own guidance: cards at rest are flat in the current console refresh).

Levels, low → high:

- **0** canvas and resting cards — no shadow, both modes; card border 1px `border.subtle`.
- **1** hover-lifted menus, autocomplete dropdowns, date pickers — `0 1px 3px rgba(60,64,67,0.30),
  0 4px 8px 3px rgba(60,64,67,0.15)` light / surface step to `surface.raised` + 1px
  `border.subtle` dark.
- **2** sticky table header and the top bar on scroll — `0 1px 2px rgba(60,64,67,0.30),
  0 2px 6px 2px rgba(60,64,67,0.15)` / one further surface step + keyline.
- **3** right-side drawers, inspectors, side panels — level-1 shadow, `radius.sm`, 1px hairline.
- **4** modal dialogs — strongest shadow plus scrim `rgba(32,33,36,0.5)` light / `rgba(0,0,0,0.6)`
  dark.

Dark mode: surface-luminance steps (#202124 → #292a2d → #35363a) do the work shadows cannot on a
near-black canvas; every level-2+ surface additionally carries a keyline.

## 8. Motion

`instant` 0ms (reduced-motion substitute) · `fast` 100ms — exits, hover fills, chip toggles ·
`base` 200ms — entrances: menus, drawers, panels, ripple settle (Material emphasis decelerate
curve `cubic-bezier(0.2, 0, 0, 1)`) · `slow` 300ms — dialogs, nav rail collapse, full-page
transitions (same decelerate curve).

- Entrances decelerate, exits are faster (100ms, standard acceleration); symmetric ease-in-out on
  both directions is a defect.
- Animate `transform` and `opacity` only — never `width`, `height`, `top`, `left`. The nav rail
  collapses via transform, not width.
- No bounce on irreversible moments: not on "Delete dataset", not on "Stop VM".
- **Reduced motion is a real variant, not a softened one:** every duration resolves to 0ms; fades
  collapse to instant state changes; scaling and panning of large objects are fully neutralised.

## 9. Imagery & Art Direction

- **Brand moment:** the marketing shell (cloud.google.com home) is the single licensed saturation
  moment — abstract 3D gradient renders on 24px-radius dark cards, 64px Google Sans display
  numerals, the multicolour Google Cloud mark. Its palette (deep blues, iridescent gradients,
  near-black card fields) is a fixed marketing namespace and **never samples into console tokens**.
  "None" for every console surface.
- **Iconography:** Material Symbols / Material Icons — 2px strokes on a 24px grid, outlined style,
  geometric, matched to Google Sans Text's tone. The left nav's product icons are the exception:
  full-colour 24px GCP product marks (the one place the brand quartet legitimately renders in
  product chrome). Status glyphs are filled icons at 16–20px. Icon-only controls always carry a
  label or tooltip (§10 contracts).
- **Photography:** none in product UI. Marketing photography (customers, data centres, events)
  lives on cloud.google.com only.
- **Illustration / 3D:** none in the console shell. Data visualisation is the console's licensed
  expressiveness: chart series use the brand quartet plus purple (#4285f4, #ea4335, #fbbc04,
  #34a853, #9334e6) — blue first — with the histogram selection band #aecbfa; the chart palette is
  a separate token namespace and never borrows `accent.action` fills for non-chart controls.
- **Empty / error art:** no illustration system in console surfaces; empty states are typographic —
  a 16px/500 heading naming the missing resource ("No datasets in this project"), one sentence,
  and the exact primary CTA that creates it. An error banner names the failing call and offers
  Retry; illustration never substitutes for the recovery CTA.

## 10. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| Top bar | std | light/dark | default, search open, project picker open | Tab through; Esc closes menus | Project selector, org name, search field |
| Left nav / product list | std | 280px, 56px icon rail | expanded, collapsed, item hover, item selected | Arrows traverse; Enter selects | Product names, never abbreviations |
| App-shell notice bar | std | info/warning (quota, billing) | default, dismissed | Esc dismisses | One sentence + action link |
| Data table | std/dense | selectable, sortable, sticky header | hover, selected, sorting asc/desc, loading, empty, no-results | Space toggles; arrows move | Column labels noun-style; "x selected" |
| Filter/search bar | std | free-text, token chips | editing, applied count, clear-all | Enter applies; Esc clears | "Filter by text or property" |
| Row action menu (kebab) | std/dense | per-row | open, focus-trapped, item disabled | Esc closes; arrows traverse | Verbs; destructive separated |
| Stat tile (KPI) | std | single value, delta, sparkline | loading skeleton, stale marker | — | Label sentence case; delta carries sign glyph |
| Query editor | dense | LQL/SQL, multi-line | editing, running, error underline, history | Tab indents; Ctrl+Enter runs | "Run query" primary fill |
| Log stream | dense | timestamped rows, severity chips | expanding, filter active, auto-scroll | Arrows traverse rows | Mono timestamp + severity chip + payload |
| Histogram / timeline chart | std/dense | time range brush | brushing, zoomed, empty | Arrows move brush | Range label in tabular mono |
| Drawer / inspector | std | right panel, resizable | open, resizing, closed | Esc closes | Title mirrors selection |
| Dialog | std/focused | confirm, form | open, invalid, waiting | focus-trap; Esc; Enter confirms | Title = action; body names consequence |
| Chips (filter/created) | std | outlined, filled-selected | default, selected, dismissed | Backspace removes | Property + value tokens |
| Primary button | std | filled, outlined, text | default, hover, active, loading (spinner + reserved width), disabled (reason on hover) | Space/Enter activate | Verb phrases: "Create instance", "Run query" |
| Select / autocomplete | std | single, multi | open, filtered, matched-highlight, disabled | Type-ahead; arrows; Esc | Placeholder names the property |
| Input / textarea | std | default, copyable (mono) | focus, error, warning, disabled, read-only | standard | Constraint text states the rule |
| Status pill / severity chip | dense | success/warning/error/info | default, loading | — | Label from resource state enum |
| IAM member row | std | user/group/service account | hover, selected, role editing | arrows traverse | Member email + role chip |
| Audit / activity entry | std | event log row | expanded detail | arrows traverse | Event name + time + actor |
| Global search | std | omnibox in top bar | open, results, no-results | Ctrl+K style entry | "Search products, resources, docs" |
| Wizard (multi-step) | focused | create-resource flows | step active, validation error, review, submitting | Next/Prev; step links | Step titles as tasks: "1. Select a template" |

**Every fetching surface also designs:** loading (skeleton or in-table spinner matching final
geometry — tables load in place, never a blank page); empty ("No datasets yet" + "Create dataset"
CTA); error (banner: what call failed + Retry); offline/stale (banner: "Showing cached values from
HH:MM" — regional outages get a dedicated status link).

**Contracts this table encodes:** one primary filled CTA per view (dense toolbars may run a
primary plus icon actions); every icon-only control carries a label or tooltip; a disabled control
states *why* on focus or hover; a button never changes width between idle and loading — the
spinner replaces the label inside reserved space; destructive actions are separated, tinted red,
and confirmed with a dialog that names the exact resource ("Delete dataset `names_2014`?").

## 11. Light / Dark Strategy

- **Posture: C dual-parity.** The console ships fully authored light and dark modes; light is the
  shipped default and the mode every screenshot and marketing asset assumes.
- **Mechanism:** semantic roles remapped per mode; every role in §3 has both values — none absent.
  `chrome.nav` remaps (white → #292a2d) because the chrome participates in the canvas ramp, unlike
  AWS's fixed navy bar.
- **`color-scheme`** is set on the root so UA chrome, form controls and scrollbars follow the
  active mode; the meta equivalent is declared in the document head before styles load to prevent
  a flash of the wrong scheme.
- **Dark is authored, not inverted:** its own surface ramp (#202124 → #292a2d → #35363a), its own
  status hues (dark error is a lighter #f28b82, dark warning a bright #fdd663 — dark modes need
  lighter, not deeper, status inks), and its own accent (#8ab4f8 with near-black ink on it, not
  white-on-blue). Washes invert to near-black tints of each hue. Hairlines strengthen in absolute
  terms (#9aa0a6 controls) because a #3c4043 line that reads as delicate on white reads as
  invisible on near-black only when it must divide like-for-like luminance.
- The brand quartet keeps the same values in dark mode — it renders inside icons and charts, which
  were tuned for both canvases.

## 12. Density-Mode Strategy

- **Default mode per surface class:** standard everywhere; dense on data surfaces — resource
  tables, log streams, query results, metric grids. The boundary is the surface's job: reading and
  deciding = standard; scanning and comparing = dense.
- **Mechanism:** a density attribute at the app root rescales row height, cell padding, gutter and
  body size together. Spacing token *names* never change; only their resolved values do. The axis
  is a token register, not a viewport query — spacing values do not change based on screen size.
- **Container-based reflow** decides when a table prunes columns and when a side panel's width
  forces the dense register; components measure their content box, not the viewport, so a table
  inside a split panel densifies without the page mode changing.
- **The switch is an accessibility affordance**, not a preference: operators with visual field
  loss get standard density as a first-class, persisted control on every data surface.

## 13. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA body-text contrast (7:1) on standard-mode prose (achieved:
  16.1:1 primary, 6.05:1 secondary).
- **Target size:** ≥24×24 CSS px hard minimum; 44px design target for primary controls in focused
  mode; icon buttons in dense toolbars keep ≥24px hit areas with spacing separation. Zoom does not
  excuse it.
- **Keyboard:** every function operable without a pointer; tables support arrow navigation; the
  query editor is a real editing surface with Tab indent and a visible caret; dialogs focus-trap
  and restore focus on close; the focused item is never entirely hidden by the sticky top bar or
  table header (scroll-padding matches chrome heights).
- **Focus indicator:** 2px `border.focus` ring at ≥3:1 on every surface it lands on (#1a73e8 on
  white = 4.505:1; #8ab4f8 on dark canvas = 7.639:1), never suppressed.
- **Contrast:** text ≥4.5:1 (gate rows pass); UI boundaries ≥3:1 via `border.strong`. **Colour
  independence:** every status pairs colour with an icon glyph and a state word ("Running", not a
  green dot); severity ships as word chips; cost deltas carry an explicit sign; sort direction
  carries a glyph.
- **Motion:** the 0ms reduced-motion variant from §8 applies to every authored animation —
  ripples, drawers, skeletons, histogram brushes.
- **Text:** ≤80-character measure; 200% resize without horizontal scroll in standard mode; 12px
  floor never broken.
- **Semantics:** real buttons, links and inputs; headings match visual rank (24 → 16 → 14);
  live regions announce async results politely ("Query completed, 349 results"); tables announce
  row count and selection state; loading regions flagged busy.
- **Contrast preference:** `prefers-contrast: more` steps every `border.subtle` hairline up to
  `border.strong`, strengthens chip outlines, and keeps placeholder text ≥4.5:1.

## 14. Anti-Patterns

**Do**

1. Reserve blue for action: #1a73e8 means "clickable/do it now". Rationale: in a 200-row table,
   affordance colour must be noise-free.
2. Keep cards flat — white on white with 1px #dadce0 hairlines and no resting shadow. Rationale:
   the console's calm is its brand; shadows under every card are 2016-era drift.
3. Match toolbar/filter/pagination heights to row height per density. Rationale: chrome rhythm is
   what makes dense mode feel engineered rather than squeezed.
4. Right-align and tabular-numeral every numeric column. Rationale: timestamps and costs are the
   console's most-compared data.
5. Pair every status colour with a glyph and a state word. Rationale: statuses must survive
   greyscale screenshots, CVD and compressed captures.
6. Use Roboto Mono only for identifiers, queries and log lines. Rationale: mono body text reads as
   an error.
7. Name the resource in every confirm dialog ("Delete dataset `names_2014`?"). Rationale: fleet
   operators act on the wrong resource only when the UI lets them.
8. Keep the left nav's product icons full-colour while everything around them stays grey. Rationale:
   the colourless shell makes 24px product icons scannable landmarks.
9. In dark mode, use lighter (not deeper) status inks and near-black washes. Rationale: reusing
   light values on near-black fails both contrast and legibility.
10. Skeleton-match loading geometry inside tables and log streams. Rationale: layout shift in a
    dense grid destroys scan position.
11. Keep 12px as the absolute floor, 14px as the standard body. Rationale: density comes from row
    height, never from shrinking type past readability.
12. Quote logs and queries in mono with syntax-tinted literals (strings green 800). Rationale: it
    is the one place colour carries meaning inside a data surface, and it is conventional.

**Don't**

1. No marketing aesthetics inside product UI — no gradient 3D renders, no dark promo cards, no
   customer-logo walls in console pages.
2. No stat-card dashboards as a substitute for tables — KPI tiles cap at one row; resource tables
   lead.
3. No modals as connective tissue — multi-step work uses drawers and wizards, not stacked dialogs.
4. No two primary fills side by side; one `accent.action` per viewport.
5. No brand-quartet fills: #4285f4/#ea4335/#fbbc04/#34a853 style icons and charts, never buttons.
6. No toolbar of unlabelled icons — every icon control has a label or tooltip.
7. No hover-only affordances — row actions are visible (kebab), not revealed on hover alone.
8. No placeholder-as-label — every input has a persistent label; constraints render as hint text.
9. No whole-page spinners — tables and log streams load in place with skeletons matching final
   geometry.
10. No `alert()`-style dialogs — async failures are banners with Retry; confirms are resource-named
    dialogs.
11. No tiny type as a density strategy — dense mode moves padding and rows, never below 12px.
12. No pure black (#000000) canvas or text in dark mode — the ramp starts at #202124 and ink stays
    grey.
13. No pill radius in product UI — pills belong to marketing CTAs and filter chips; console buttons
    are 8px.
14. No legacy drift: the pre-refresh #4285f4 button fill and #f5f5f5 canvases do not re-enter new
    screens; service-team overrides go through the token layers, not hardcoded hex.

## 15. Quick Reference & Verification Gate

**Flat colour reference (role → hex).** Light: canvas/raised/overlay #ffffff · inset #f8f9fa ·
hover #f1f3f4 · selected #e8f0fe · border.subtle #dadce0 · border.strong #80868b · border.focus
#1a73e8 · accent.action #1a73e8 · accent.onAction #ffffff · accent.subtle #e8f0fe · text.primary
#202124 · text.secondary #5f6368 · text.tertiary #80868b · text.disabled #9aa0a6 · success #137333
· warning #a15c00 · error #c5221f · info #174ea6 · washes #e6f4ea / #fef7e0 / #fce8e6 / #e8f0fe ·
chrome.nav #ffffff · chrome.onNav #5f6368 · brand #4285f4/#ea4335/#fbbc04/#34a853. Dark: canvas
#202124 · raised #292a2d · overlay #35363a · inset #171717 · hover #303134 · selected #3c475b ·
border.subtle #3c4043 · border.strong #9aa0a6 · border.focus #8ab4f8 · accent.action #8ab4f8 ·
accent.onAction #202124 · accent.subtle #2d333d · text.primary #e8eaed · text.secondary #bdc1c6 ·
text.tertiary #9aa0a6 · success #81c995 · warning #fdd663 · error #f28b82 · info #8ab4f8 · washes
#20342c / #3a2f17 / #3a2422 / #233a52.

**Flat type ramp (standard):** 24/32 400 Google Sans page title · 16/24 500 section title · 14/20
400 body · 14/20 500 label · 12/16 400 row-secondary and meta · 24–48/×1.2 400 tabular stat value.
Dense: 12/16 500 grid header · 13/20 400 cells · 13/20 400 Roboto Mono log lines.

**Flat spacing + radius:** scale 4 · 8 · 12 · 16 · 24 · 32 · 48; nav 280px (rail 56px), top bar
64px, gutters 16/24px, card padding 16px, card gap 16px. Radius: checkbox 4 · button/input/card/
dialog 8 · marketing card 16 · chip/pill full.

**Component → token map.** Primary button: `accent.action` fill + `accent.onAction` label, radius
sm, `border.focus` ring on focus. Outlined button: transparent fill, 1px `border.subtle`,
`text.primary` label; hover `surface.hover`. Card: `surface.raised` + 1px `border.subtle`, radius
sm, padding `space.4`, no shadow. Table row: 48px standard / 32–40px dense, `surface.hover` on
hover, `surface.selected` when selected, `border.subtle` row hairlines, header row
`surface.inset`. Query editor: `surface.inset` well, Roboto Mono 13px `text.primary`, string
literals green 800, line numbers `text.tertiary`. Log row: 40px dense, mono timestamp
`text.secondary`, severity chip outlined `status.*`. Chip: pill, 1px `accent.action` outline +
`accent.action` label when interactive; `accent.subtle` fill when selected. Left nav item: 40px
tall, 14px/500 `chrome.onNav`, selected `surface.selected` + `accent.action` label. Banner:
`status.wash.*` fill + `status.*` glyph and title + `text.primary` body, radius sm.

**Agent prompt block.**

- Role→hex (light): surface.canvas #ffffff, surface.inset #f8f9fa, surface.hover #f1f3f4,
  surface.selected #e8f0fe, border.subtle #dadce0, border.strong #80868b, border.focus #1a73e8,
  accent.action #1a73e8, accent.onAction #ffffff, text.primary #202124, text.secondary #5f6368,
  text.tertiary #80868b, status.success #137333, status.warning #a15c00, status.error #c5221f,
  status.info #174ea6, status.wash.success #e6f4ea, status.wash.warning #fef7e0,
  status.wash.error #fce8e6, status.wash.info #e8f0fe, chrome.nav #ffffff, chrome.onNav #5f6368.
- Dark: surface.canvas #202124, surface.raised #292a2d, surface.overlay #35363a, border.subtle
  #3c4043, border.strong #9aa0a6, accent.action #8ab4f8, accent.onAction #202124, text.primary
  #e8eaed, text.secondary #bdc1c6, status.success #81c995, status.warning #fdd663,
  status.error #f28b82, status.info #8ab4f8.
- Type: Google Sans Text UI / Google Sans headings / Roboto Mono for IDs, queries, logs; 24/32
  400 page title, 16/24 500 section, 14/20 400 body, 12/16 400 meta; minimum 12px.
- Spacing: 4px base; use scale 4/8/12/16/24/32/48 only. Cards 16px padding, 16px gaps. Nav 280px,
  top bar 64px. Radius: buttons/inputs/cards 8px, chips and marketing pills full.
- Density: standard rows 48px body 14px; dense rows 32–40px body 13px; never mix modes mid-page;
  toolbar = row height. Brand quartet only in icons and charts — never as a fill.

**Example component prompts.**

1. *Resource table surface (Compute Engine / Cloud SQL / GKE list)* — `surface.canvas` background;
   card container `surface.raised` + 1px `border.subtle`, radius sm, no shadow; page title 24/400
   Google Sans in `text.primary`; one `accent.action` fill (the "Create instance" button)
   top-right; table rows 48px standard / 32px dense, body 14px standard / 13px dense, numerics
   right-aligned tabular; header row `surface.inset` 12px/500; hover `surface.hover`; selected
   `surface.selected`; focus ring `border.focus`; toolbar and pagination match row height; empty
   state names the resource and carries the create CTA.
2. *Log stream panel (Logs Explorer)* — dense mode: 40px rows, Roboto Mono 13/20; timestamp column
   `text.secondary` tabular; severity as outlined `status.*` chip; payload `text.primary` with
   string literals green 800; left filter panel 320px with `surface.hover` rows and
   `surface.selected` active filters; histogram bars chart-blue #4285f4 with #aecbfa selection
   band; "Run query" is the viewport's only `accent.action` fill; sticky results header matches
   row height.
3. *Confirm deletion* — dialog at level 4 with scrim `rgba(32,33,36,0.5)`, radius sm,
   `surface.overlay`; title = the verb ("Delete dataset"); body names the exact resource in mono;
   Cancel outlined, destructive button red-tinted (`status.error` ink on `status.wash.error`);
   focus-trapped, Esc closes, Enter does not trigger the destructive control by default.

**Pre-ship checklist.**

1. Zero raw hex outside L1.
2. No token resolves to a component name.
3. Every contrast pairing computed, passing, unrounded (§3).
4. Every semantic role has a value in both visual modes.
5. Every fetching surface has loading/empty/error/offline specified.
6. Every component row lists disabled and loading states.
7. Row, header, toolbar and pagination heights agree per density.
8. Reduced-motion variant written for every authored motion (0ms register).
9. Every control keyboard-reachable with a visible focus indicator.
10. Dark authored, not filtered, with its own ramp and lighter status inks.
11. No unoverridden stock default inside a committed surface.
12. Nothing came from a marketing page — gradient renders, pill CTAs and display numerals stay out
    of console surfaces.
13. The §9 brand-moment palette (dark promo cards, iridescent gradients) appears nowhere in the UI
    token layers.
14. Chart hues never style non-chart controls; the brand quartet never fills a button.
15. Warning ink verified at #a15c00 on washes (stock #b06000 measured 4.336:1 and was rejected).
