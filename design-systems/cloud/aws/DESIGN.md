# Design System — AWS Management Console

<!-- premium-web-design:design-system 2 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: CloudScape visual refresh (colour + shell — rung 2, official token export @cloudscape-design/design-tokens 3.0.117), AWS console EC2/S3/Lambda resource tables (density/type — rung 2 docs + rung 3 screenshot grounding) -->
<!-- Surface classes: 5 route groups classified; density classes S+D assigned (F reserved for sign-in/wizard entry flows) -->

## 1. Design Posture & Atmosphere

The AWS console is a control tower for fleets, not a showcase for the company that built it. Its
register is utilitarian calm: a near-white canvas, near-black ink, exactly one blue reserved for
the thing you can do next, and status colours that only appear when infrastructure actually has a
state worth reporting. After eight hours in it, the eye fatigue is low — the console earns its
keeping in tens of thousands of table cells, and every token decision bends toward scanning 200
rows at 14px without distortion. Density is a first-class axis: the same service ships a comfortable
reading mode and a compact mode, and operators switch between them the way a pilot switches panel
layouts.

Against its category defaults (GCP's carded pastels, Azure's left-weighted portals), AWS sits on
the austere end: containers are flat white rectangles separated by 1px hairlines and generous
gaps, shadows barely exist, and the only saturated field in the entire product UI is the primary
button. The visual metaphor is a **ledger sheet with a switchboard's keyboard** — every surface
answers "what exists, what state is it in, what can I do to it", in that order, in that type ramp.
The famous orange smile and squid-ink navy belong to the brand chrome (top nav, marketing) and are
never allowed to leak into resource surfaces; inside a service page, AWS could be any
infrastructure vendor, which is exactly the point.

**Key Characteristics**

- Depth is a 4-step surface ramp plus 1px hairlines; containers in light mode carry **no shadow at
  all** — a shadow appears only on the active/expanded container and on overlays.
- One accent fill per viewport: the primary button in `accent.action`; links share the same blue so
  affordance colour is 1:1 with interactivity.
- Canvas and containers are both #ffffff in light mode — hierarchy comes from hairlines and gaps,
  not grey-vs-white layering (this is the 2024+ visual refresh posture; the older grey canvas
  #f2f3f3 is retired).
- Tables are the centre of gravity: rows 48px comfortable / 40px compact, 14px body, right-aligned
  tabular numerals, header rows that never scroll away.
- Status ships as icon + label + colour; a green dot alone is never the whole message.
- Brand chrome is physically separate: the global top bar is dark navy #232f3e with white text,
  visibly a different room from the content canvas.
- Radii are large and soft (16px containers, 20px pill buttons, 8px inputs) — the roundness reads
  friendlier than the ledger metaphor suggests, and it is applied consistently per family.
- Motion is nearly subliminal: 115–250ms, decelerate curves, and a hard 0ms mode for reduced
  motion rather than a softened one.
- Minimum text size is 12px; nothing in the product UI renders smaller, ever.
- Dark mode is fully authored (separate ramp, separate status hues) but dark is opt-in per visual
  mode; light is the shipped default.
- Monospace is strictly identifiers: resource IDs, ARNs, hashes, log lines, code cells.
- Empty states name the missing resource and hand you the exact creation CTA; a blank table is
  never a blank page.

## 2. Token Architecture   ← normative

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value* (`blue.600`, `ink.900`, `wash.green`), referenced
  only by L2. Banned: `[component]-[prop]` naming — one value, many roles. (CloudScape's own export
  names a token `color-background-button-primary-default`; that component-flavoured name is the
  historical shape this spec's L2 replaces with `accent.action`.)
- **L2 Semantic** — role names (`surface.canvas`, `text.primary`, `accent.action`). The only layer a
  component may consume.
- **L3 Component** — only for deliberate deviation; points at L2 or L1, never a raw value, never a
  sibling component's token. Example: the global top bar consumes `chrome.nav` (which resolves to
  the brand primitive `navy.squid`), because the nav is brand territory, not product UI.

**Rules.** Every token has a determinable type or it is invalid; names case-sensitive, no `$`, `{`,
`}`, `.`; no circular references. Every semantic token has a value in **every** shipped mode — both
visual modes (light, dark) are fully populated below; no role resolves to its light value in dark.
Animatable tokens (the two easing curves, the three durations) are registered with explicit type
and inheritance declarations or the registration is invalid; an initial value must be
computationally independent, so percentage or em-based initial values are illegal.

**Layer order (low → high)** `[reset] → [primitives] → [semantic] → [components] → [utilities]`.
Layer order beats specificity entirely, and an un-layered normal declaration outranks everything
layered — so a stray un-layered rule in a service-team stylesheet would beat this whole system;
anything a consumer must override without `!important` sits in the top layer. This matters double
at AWS scale: dozens of service teams ship UI into one shell, and the layer contract is what keeps
a 2021-era service page from overwriting the 2026 refresh.

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` | #ffffff | #161d26 | Page background; equal to container in light |
| `surface.raised` | #ffffff | #1b232d | Cards, dropdowns, popovers (dark steps one level up) |
| `surface.overlay` | #ffffff | #232b37 | Modals, dialogs, toolbars on scroll |
| `surface.inset` | #f3f3f7 | #131920 | Hovered list rows, code wells, filter chips |
| `surface.hover` | #f0fbff | #1b232d | Interactive fill — a blue whisper in light |
| `surface.selected` | #f0fbff | #001129 | Selected nav item, selected table row, matched option |
| `border.subtle` | #c6c6cd | #424650 | 1px container hairlines and dividers (decorative) |
| `border.strong` | #8c8c94 | #656871 | 1px control outlines — inputs, normal buttons |
| `border.focus` | #006ce0 | #42b4ff | Focus indicator, ≥3:1 against every surface it lands on |
| `accent.action` | #006ce0 | #42b4ff | Primary button fill, active toggles, selection borders |
| `accent.onAction` | #ffffff | #0f141a | Text/icon on the accent fill |
| `accent.subtle` | #d1f1ff | #006ce0 | Accent washes: drag placeholders, toggles-on tint |
| `text.primary` | #0f141a | #ebebf0 | Headings and body ink |
| `text.secondary` | #424650 | #c6c6cd | Body secondary, form labels |
| `text.tertiary` | #656871 | #8c8c94 | Breadcrumb current, empty hints, placeholder |
| `text.disabled` | #8c8c94 | #8c8c94 | Same value both modes; paired with disabled fill |
| `status.success` | #00802f | #2bb534 | Green — passing checks, running instances |
| `status.warning` | #855900 | #fbd332 | Amber — degraded, pending, partial |
| `status.error` | #db0000 | #ff7a7a | Red — failed, stopped-with-error |
| `status.info` | #006ce0 | #42b4ff | Blue — neutral notice, shares accent hue |
| `status.wash.success` | #effff1 | #001401 | Flash bars, alerts, banner fills |
| `status.wash.warning` | #fffef0 | #191100 | |
| `status.wash.error` | #fff5f5 | #1f0000 | |
| `status.wash.info` | #f0fbff | #001129 | |
| `chrome.nav` | #232f3e | #232f3e | Global top bar — brand navy, identical in both modes |
| `chrome.onNav` | #f9f9fa | #f9f9fa | Text/icons on the navy bar |
| `chrome.hero` | #0f141a | #0f141a | Console home hero band — near-black slate |

Dark canvas is **not** pure black: #161d26, stepping to #1b232d and #232b37. Depth in dark comes
from surface steps and 1px strokes, never shadows (`shadow.card` is `none` in both modes; the dark
`container.active` shadow is a faint #192534 keyline, not a glow).

The AWS brand orange #ff9900 and the smile mark are **marketing/brand assets only**; they appear in
the logo lockup and on aws.amazon.com, and nowhere in this token table. The legacy console blue
#0972d3 and legacy grey canvas #f2f3f3 are retired by the visual refresh — `accent.action` is
#006ce0 as of the current token export.

**Contrast gate — computed per WCAG 2.2 relative-luminance formula, unrounded; large text is
≥24px or ≥18.5px bold; body ≥4.5:1; UI boundaries and focus ≥3:1.**

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| `text.primary` L | #0f141a | `surface.canvas` L | #ffffff | 18.497:1 | 4.5:1 | PASS |
| `text.secondary` L | #424650 | `surface.canvas` L | #ffffff | 9.444:1 | 4.5:1 | PASS |
| `text.tertiary` L | #656871 | `surface.canvas` L | #ffffff | 5.567:1 | 4.5:1 | PASS |
| `text.disabled` L | #8c8c94 | `surface.canvas` L | #ffffff | 3.337:1 | 3:1 (house floor; disabled exempt) | PASS |
| `accent.onAction` L | #ffffff | `accent.action` L | #006ce0 | 4.975:1 | 4.5:1 | PASS |
| `border.strong` L | #8c8c94 | `surface.raised` L | #ffffff | 3.337:1 | 3:1 | PASS |
| `status.success` L | #00802f | wash L | #effff1 | 4.903:1 | 4.5:1 | PASS |
| `status.warning` L | #855900 | wash L | #fffef0 | 6.038:1 | 4.5:1 | PASS |
| `status.error` L | #db0000 | wash L | #fff5f5 | 4.893:1 | 4.5:1 | PASS |
| `status.info` L | #006ce0 | wash L | #f0fbff | 4.725:1 | 4.5:1 | PASS |
| `text.primary` D | #ebebf0 | `surface.canvas` D | #161d26 | 14.278:1 | 4.5:1 | PASS |
| `text.secondary` D | #c6c6cd | `surface.canvas` D | #161d26 | 9.985:1 | 4.5:1 | PASS |
| `accent.onAction` D | #0f141a | `accent.action` D | #42b4ff | 8.107:1 | 4.5:1 | PASS |
| `status.error` D | #ff7a7a | wash D | #1f0000 | 7.859:1 | 4.5:1 | PASS |
| `status.success` D | #2bb534 | wash D | #001401 | 7.053:1 | 4.5:1 | PASS |
| `status.warning` D | #fbd332 | wash D | #191100 | 12.898:1 | 4.5:1 | PASS |
| `status.info` D | #42b4ff | wash D | #001129 | 8.276:1 | 4.5:1 | PASS |
| `border.strong` D | #656871 | `surface.raised` D | #1b232d | 3.519:1 | 3:1 | PASS |
| `chrome.onNav` | #f9f9fa | `chrome.nav` | #232f3e | 14.838:1 | 4.5:1 | PASS |

`border.subtle` (#c6c6cd on white, 1.699:1) is intentionally below 3:1: hairlines separate content
that is already separated by gaps and type; the *control* boundary role (`border.strong`, 3.337:1)
carries the non-text-contrast obligation. A divider that must communicate a boundary alone uses
`border.strong`.

## 4. Typography

**Families.** UI **Open Sans** — weights 300 (display only), 400 (all body), 700 (headings,
emphasis, buttons); self-hosted by the shell; fallback `'Helvetica Neue', Roboto, Arial, sans-serif`.
The AWS brand lockup and global nav wordmark render in **Amazon Ember** (proprietary; falls back to
the same stack) — Ember is brand chrome, not product UI. Numeric/code: **Monaco, Menlo, Consolas**
monospace for resource IDs, ARNs, hashes, log lines, code cells. *Monospace is for identifiers and
code, never a costume.*

**One ramp table per class, not one blended table.** Columns: role, size, weight, line height,
tracking, numerals, use.

- **[S] Standard, 14px base (console default):**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Display (hero stat) | 42px | 700 | 48px | −0.25px | tabular | Console home hero, dashboard number highlights |
| Page title | 24px | 700 | 30px | normal | default | Service pages, h1 |
| Container title | 20px | 700 | 24px | normal | default | Card/panel headers, h2 |
| Section title | 18px | 700 | 22px | normal | default | Key/value titles, help panel, h3 |
| Sub-section | 16px | 700 | 20px | normal | default | h4, tab labels |
| Body | 14px | 400 | 20px | normal | default | Primary prose and table cells |
| Row secondary | 12px | 400 | 16px | normal | default | Sub-text in rows, field descriptions |
| Stat value | 14–42px | 700 | ×1.2 | normal | tabular | KPI tiles on dashboards |
| Stat label | 12px | 400 | 16px | +0.4px uppercase | default | Tile captions |
| Meta | 12px | 400 | 16px | normal | tabular | Timestamps, breadcrumbs-current, constraints |
| Log line (mono) | 12px | 400 | 16px | normal | tabular | CloudWatch log events, code |
| Inline help | 12px | 400 | 16px | normal | default | Field hints, wizard captions |

- **[D] Dense, 12–13px base (compact table mode, data surfaces only):**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Grid header | 12px | 700 | 16px | +0.2px | default | Compact table headers |
| Grid cell text | 12–13px | 400 | 16px | normal | default | Compact rows |
| Grid cell numeric | 12–13px | 400 | 16px | normal | tabular | Sizes, counts, costs, IPs |
| Log line (mono) | 12px | 400 | 16px | normal | tabular | Dense log viewers |
| Inline help | 12px | 400 | 16px | normal | default | *Prose inside a dense screen still steps up to 14px.* |

**Invariants.** `tabular-nums` on every comparable value — currency, timestamps, deltas, counts,
instance IDs, ARNs. Right-align numerics, left-align text, never centre a numeric column. Fixed
stepped sizes (12 / 14 / 16 / 18 / 20 / 24 / 42px); no fluid scaling. Measure ≤80 characters;
65–80ch in standard prose, unconstrained in dense data cells. Minimum rendered size 12px.

## 5. Spacing Scale & Density Scales   ← two axes, never one

**Spacing base: 4px grid; 8px comfortable standard, 4px compact.** The scale ships two register
variants (comfortable / compact); compact is the console's dense mode. `space.0` 0 ·
`xxxs` 2px · `xxs` 4px icon-to-label, button vertical padding (compact: 2px) · `xs` 8px control
padding, cell padding compact · `s` 12px cell padding standard, embedded-card horizontal padding ·
`m` 16px card vertical padding, gutter compact · `l` 20px card horizontal padding, button horizontal
padding · `xl` 24px section gap · `xxl` 32px region separation · `xxxl` 40px page section spacing
(compact: 32px). *No 17px. No 23px. If a layout needs an off-scale value, the layout is wrong.*
Component-level paddings on the same grid: button 20px horizontal × 4px vertical (compact 16×2);
card 20px horizontal × 16px vertical; embedded card 12×10; field label gap 12px horizontal, 5px
vertical.

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| focused | — | 16px | 24px | 32px | Sign-in, account/region picker dialogs, wizard review steps |
| standard | 48px | 14px | 12–20px | 24px | Console home, service landing, resource detail, help panel |
| dense | 40px | 12–13px | 8px | 16px | Resource tables, CloudWatch logs, metric grids |

- Density comes from **row height, column pruning and leading** — never from type too small to
  read. A 13px tabular numeral in a dense table is correct; the same numeral in a focused form is a
  defect.
- **Never switch mid-page.** A service page is one mode; a route change to the compact tables view
  is a different room and that is legitimate.
- **Chrome follows rows.** Table toolbar, filter bar and pagination strip heights match the table's
  row height — a 48px toolbar over 40px compact rows is a rhythm break.
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40%. *House heuristic — validate
  by screenshot.*

## 6. Radius Scale

`none` 0 (table cells, dividers) · `xs` 4px badges, focus rings on small controls · `sm` 8px
inputs, dropdowns, embedded cards, alerts-on-media · `md` 12px alerts and flash bars · `lg` 16px
containers, panels, dialogs, drawers · `full` 20px buttons, toggle pills, icon buttons. **One
radius per component family**, never mixed ad-hoc: every button is 20px, every input 8px, every
container 16px. Nested radii obey `radius_inner = radius_outer − padding`.

## 7. Elevation

**Strategy: hairline-first.** Light mode's resting container has *no shadow* — separation is the
1px `border.subtle` plus the page gutter. Elevation exists only for transient surfaces.

Levels, low → high:

- **0** canvas and resting containers — no shadow, both modes; container border 1px.
- **1** active/expanded container (e.g. a card in a dashboard being rearranged) — `0 1px 1px 1px
  #e9ebed, 0 6px 36px rgba(0,7,22,0.10)` light / `0 1px 1px 1px #192534, 0 6px 36px rgba(0,4,12,1)`
  dark.
- **2** dropdowns, popovers, select menus — level-1 shadow plus `border.strong` keyline.
- **3** drawers, split panels, help panel — strongest shadow, `radius.lg`, border 1px
  `border.subtle`.
- **4** modal dialogs — level-3 shadow plus a scrim (dark translucent overlay) between dialog and
  page.

Dark mode: surface-luminance steps (#161d26 → #1b232d → #232b37) do the work shadows cannot on a
near-black canvas; every level-2+ surface additionally carries a keyline.

## 8. Motion

`instant` 0ms (reduced-motion substitute) · `fast` 115ms — hovers, tooltips, toggles, control state
changes · `base` 165ms — entrances of popovers, drawers, flash bars (expressive curve) · `slow`
250ms — dialogs, wizard transitions, large panel reveals (complex curve).

- Curves: decelerate for entrances and interactive response
  `cubic-bezier(0, 0, 0, 1)`; expressive elements use `cubic-bezier(0.84, 0, 0.16, 1)`.
- Entrances decelerate, exits are faster or instant; symmetric ease-in-out on both directions is a
  defect.
- Animate `transform` and `opacity` only — never `width`, `height`, `top`, `left`.
- No bounce on irreversible moments: not on "Terminate instance", not on "Delete bucket".
- **Reduced motion is a real variant, not a softened one:** every duration resolves to 0ms — the
  motion system defines the disabled value alongside the default value, so no authored animation
  survives the preference. Fades collapse to instant state changes; scaling and panning of large
  objects are fully neutralised.

## 9. Imagery & Art Direction

- **Brand moment:** the console home hero band (near-black slate #0f141a, white Ember-style
  lockup, service shortcuts) is the single expressive surface; its deep-slate palette is a fixed
  token pair (`chrome.hero` + `chrome.onNav`), never sampled into UI tokens. Marketing
  photography (data centres, customers) lives on aws.amazon.com only and never renders inside a
  service page. "None" for every other product surface.
- **Iconography:** CloudScape icon set — 2px strokes on a 16px grid with a 24px large variant,
  geometric, open-source, matched to Open Sans's tone. Status glyphs are filled circles with white
  marks (check, exclamation, x, i) at 16–20px. Icon-only controls always carry a label or tooltip
  (§10 contracts).
- **Photography:** none in product UI. Third-party logos (marketplace AMI vendors) render inside
  committed tiles at natural aspect, never as free-floating colour.
- **Illustration / 3D:** none in the console shell. Data visualisation is the console's licensed
  expressiveness: charts use a fixed 5-hue categorical palette (blue, red, green, purple, pink)
  tuned per visual mode, with greyscale fallback series — the chart palette is a separate token
  namespace and never borrows `accent.action`.
- **Empty / error art:** no illustration system; empty states are typographic — bold "No [resource]"
  headline, one sentence naming what is missing, and the exact primary CTA that creates it. An
  error flash bar names the failing call and offers Retry; illustration never substitutes for the
  recovery CTA.

## 10. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| Global nav (top bar) | std | light/dark brand navy | default, search open, account menu open, region banner | Tab through all; Esc closes menus | Region selector, account ID, "Sign out" |
| Side navigation | std | service-level, collapsible, dense variant | collapsed, expanded, item hover, item selected, disabled | Arrow keys traverse; Enter selects | Service task names, never abbreviations |
| Resource header | std | with status badge, with inline edit | default, editing, saving, error | Esc cancels inline edit | Resource name + ID (mono) |
| Data table | std/dense | selectable, sortable, sticky header, striped-none | hover, selected, sorting asc/desc, loading, empty, no-results | Space toggles select; arrows move | Column labels noun-style; "x selected" |
| Filter/search bar (property filter) | std | token-based, free-text | editing token, applied count, clear-all | Enter applies token | "Filter resources by property" |
| Pagination | std/dense | simple, full | page change, per-page menu | arrows move pages | "Page 3 of 12" |
| Flash bar (notifications) | std | info/success/warning/error, dismissible, sticky | entering, dismissed, actioned | Esc dismisses; action focusable | One sentence + verb action link |
| Alert (inline) | std | info/success/warning/error | default, with header, dismissed | — | Header noun + body sentence |
| Primary button | std | normal, link, icon | default, hover, active, loading (spinner + reserved width), disabled (reason on hover) | Space/Enter activate; disabled explains why | Verb phrases: "Launch instance", "Create bucket" |
| Select / autocomplete | std | single, multiselect, tokens | open, filtered, matched-highlight, disabled, loading options | Type-ahead; arrows; Esc | Placeholder names the property |
| Input / textarea | std | default, with constraint text, copyable (mono) | focus, error, warning, disabled, read-only | standard | Constraint text states rule: "Must be 3–63 characters" |
| Date/time picker | std | absolute, relative ("past 2 weeks") | calendar open, relative menu | arrows on grid | Relative presets first |
| Drawer / split panel | std | right panel, resizable | open, resizing, closed, wide/narrow | Esc closes | Panel title mirrors selection |
| Help panel | std | global right rail | open, section expanded, link out | Esc closes | Task-oriented help, linked to docs |
| Modal dialog | std | confirm, form | open, form-invalid, waiting | focus-trap; Esc; Enter confirms | Title = action; body names consequence |
| Status pill / badge | std/dense | success/warning/error/info, label or icon+label | default, loading (spinner) | — | Label from resource state enum |
| Stat tile (KPI) | std | single value, delta, sparkline | loading skeleton, stale (cached marker) | — | Label uppercase; delta carries sign glyph |
| Row action menu | std/dense | kebab per row | open, focus-trapped, item disabled | Esc closes; arrows traverse | Verbs; destructive separated |
| Audit / event entry | std | event log row | expanded detail | arrows traverse | Event name + time + actor |
| Command bar / search (global) | std | omnibox on nav | open, results, no-results | ⌘/Ctrl+K style entry | "Search resources, services, docs" |
| Wizard (multi-step) | std/focused | create-resource flows | step active, validation error, review, submitting | Next/Prev; step links | Step titles as tasks: "1. Choose AMI" |

**Every fetching surface also designs:** loading (skeleton or in-table spinner matching final
geometry — table shows a loading state in-place, never a blank page); empty ("No buckets yet" +
"Create bucket" CTA); error (flash bar: what call failed + Retry); offline/stale (banner: "Showing
cached values from HH:MM" — regional outages get a dedicated status link).

**Contracts this table encodes:** one primary filled CTA per view (dense toolbars may run a
primary plus icon actions); every icon-only control carries a label or tooltip; a disabled control
states *why* on focus or hover; a button never changes width between idle and loading — the spinner
replaces the label inside reserved space; destructive actions are separated, tinted red, and
confirmed with a dialog that names the exact resource.

## 11. Light / Dark Strategy

- **Posture: C dual-parity.** The console ships fully authored light and dark visual modes;
  light is default. Dark is an appearance preference, not a marketing theme.
- **Mechanism:** semantic roles remapped per mode; every role in §3 has both values — none absent.
  The two brand-chrome roles (`chrome.nav`, `chrome.onNav`) are *intentionally mode-stable* so the
  shell identity never shifts.
- **`color-scheme`** is set on the root so UA chrome, form controls and scrollbars follow the
  active mode; the meta equivalent is declared in the document head before styles load to prevent
  a flash of the wrong scheme.
- **Dark is authored, not inverted:** its own surface ramp (#161d26 → #1b232d → #232b37), its own
  status hues (dark error is a lighter #ff7a7a, dark warning a bright #fbd332 — dark modes need
  lighter, not deeper, status inks), and its own border strength (#656871 controls vs light's
  #8c8c94 — *weaker* absolute contrast but tuned to the dark ramp; hairlines read stronger
  relative to the dark canvas). Washes invert to near-black tints of each hue instead of
  near-white.
- The brand orange never becomes a dark-mode accent either — dark mode is the same blue-accent
  system on a dark ramp.

## 12. Density-Mode Strategy

- **Default mode per surface class:** standard everywhere; dense (compact) on data surfaces —
  resource tables, log viewers, metric grids. The boundary is the surface's job: reading and
  deciding = standard; scanning and comparing = dense.
- **Mechanism:** a density attribute at the app root rescales the entire spacing register
  (comfortable/compact token variants) — row height, cell padding, gutters, button padding and
  spacing scale all move together. Spacing token *names* never change; only their resolved values
  do. The axis is a token register, not a viewport query.
- **Container-based reflow** decides when a table offers its compact variant and when a side
  panel's width forces column pruning; components measure their content box, not the viewport, so
  a table inside a split panel densifies without the page mode changing.
- **The switch is an accessibility affordance**, not a preference: operators with visual field
  loss and low-vision users get comfortable mode as a first-class control (CloudScape exposes
  density per table), and the choice persists per user.

## 13. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA body-text contrast (7:1) on all standard-mode prose
  (achieved: 18.5:1 primary, 9.4:1 secondary).
- **Target size:** ≥24×24 CSS px hard minimum; 44px design target for primary controls in focused
  mode; icon buttons in dense toolbars keep ≥24px hit areas with spacing separation. Zoom does not
  excuse it.
- **Keyboard:** every function operable without a pointer; tables support arrow navigation;
  dialogs focus-trap and restore focus on close; the focused item is never entirely hidden by the
  sticky table header or flash bar (scroll-padding matches chrome heights).
- **Focus indicator:** 2px `border.focus` ring with a 4px radius (or full pill on buttons),
  visible on every interactive element, ≥3:1 against any surface it lands on (#006ce0 on white =
  4.975:1; #42b4ff on dark canvas = 7.436:1).
- **Contrast:** text ≥4.5:1 (all gate rows pass); UI boundaries ≥3:1 via `border.strong`. **Colour
  independence:** every status pairs colour with an icon glyph and a text label ("Running", not a
  green dot); cost deltas carry an explicit sign; sort direction carries a glyph.
- **Motion:** the 0ms reduced-motion variant from §8 applies to every authored animation —
  tooltips, flash bars, wizard transitions, skeleton shimmer.
- **Text:** ≤80-character measure; 200% resize without horizontal scroll in standard mode; 12px
  floor never broken.
- **Semantics:** real buttons, links and inputs; headings match visual rank (24→20→18→16→14);
  live regions announce async results politely; tables announce row count and selection state;
  loading regions flagged busy.
- **Contrast preference:** `prefers-contrast: more` is honoured by switching to the high-contrast
  visual mode variant — borders step from `border.subtle` to `border.strong` everywhere, focus
  rings gain an outer white keyline, and disabled text stays ≥4.5:1.

## 14. Anti-Patterns

**Do**

1. Reserve blue for action: #006ce0 means "clickable/do it now" — nothing else. Rationale: in a
   200-row table, affordance colour must be noise-free.
2. Keep containers flat with 1px hairlines; spend shadows only on transient surfaces. Rationale:
   8-hour sessions make resting shadows look like dirt.
3. Match toolbar/filter/pagination heights to row height per density. Rationale: chrome rhythm is
   what makes dense mode feel engineered rather than squeezed.
4. Right-align and tabular-nums every numeric column. Rationale: cost and size columns are the
   console's most-compared data.
5. Pair every status colour with a glyph and a state word. Rationale: statuses must survive
   greyscale printing, colour vision deficiency and screenshots.
6. Use mono only for identifiers and logs. Rationale: mono body text reads as an error.
7. Name the resource in every confirm dialog ("Delete bucket `logs-prod-3`?"). Rationale: fleet
   operators act on the wrong resource only when the UI lets them.
8. Offer compact density as a persisted, user-owned control on every data surface. Rationale: it
   is an accessibility affordance, not a taste option.
9. Keep brand orange and the smile out of service pages. Rationale: the console is a tool; brand
   saturation on every screen is category malpractice at this density.
10. In dark mode, use lighter (not deeper) status inks and near-black washes. Rationale: red-on-
    near-black fails both contrast and legibility if you reuse light values.
11. Skeleton-match loading geometry inside tables. Rationale: layout shift in a dense grid
    destroys scan position.
12. Keep 12px as the absolute floor, with 14px as the standard body. Rationale: density comes from
    row height, never from shrinking type past readability.

**Don't**

1. No marketing aesthetics inside product UI — no hero photography, no gradient washes, no
   customer-logo walls in service pages.
2. No stat-card dashboards as a substitute for tables — the console's home tile grid is capped;
   every service page leads with the resource table.
3. No modals as connective tissue — multi-step work uses drawers and wizards, not stacked dialogs.
4. No two primary fills side by side; one `accent.action` per viewport.
5. No toolbar of unlabelled icons — every icon control has a label or tooltip.
6. No hover-only affordances — row actions are visible (kebab), not revealed on hover alone.
7. No placeholder-as-label — every input has a persistent label; constraints render as hint text.
8. No whole-page spinners — tables load in place with skeletons matching final geometry.
9. No `alert()`-style dialogs — asynchronous failures are flash bars with Retry; confirms are
   resource-named dialogs.
10. No tiny type as a density strategy — compact mode moves padding and rows, never below 12px.
11. No disabled primary button without an explanation on hover/focus — "Select an instance to
    connect".
12. No legacy-token drift: the retired grey canvas #f2f3f3, the old primary #0972d3, and the old
    border radius family do not re-enter new screens; service-team overrides go through the token
    layers, not hardcoded hex.
13. No chart palette leakage — data-vis hues (red.300, teal.400, …) never style buttons or links.

## 15. Quick Reference & Verification Gate

**Flat colour reference (role → hex).** Light: canvas/raised/overlay #ffffff · inset #f3f3f7 ·
hover/selected #f0fbff · border.subtle #c6c6cd · border.strong #8c8c94 · border.focus #006ce0 ·
accent.action #006ce0 · accent.onAction #ffffff · accent.subtle #d1f1ff · text.primary #0f141a ·
text.secondary #424650 · text.tertiary/disabled #656871/#8c8c94 · success #00802f · warning #855900
· error #db0000 · info #006ce0 · washes #effff1 / #fffef0 / #fff5f5 / #f0fbff · chrome.nav #232f3e ·
chrome.onNav #f9f9fa. Dark: canvas #161d26 · raised #1b232d · overlay #232b37 · inset #131920 ·
hover #1b232d · selected #001129 · border.subtle #424650 · border.strong #656871 · border.focus
#42b4ff · accent.action #42b4ff · accent.onAction #0f141a · accent.subtle #006ce0 · text.primary
#ebebf0 · text.secondary #c6c6cd · text.tertiary #8c8c94 · success #2bb534 · warning #fbd332 ·
error #ff7a7a · info #42b4ff · washes #001401 / #191100 / #1f0000 / #001129.

**Flat type ramp (standard):** 42/48 700 display · 24/30 700 page title · 20/24 700 container title
· 18/22 700 section title · 16/20 700 sub-section · 14/20 400 body · 12/16 400 meta/row-secondary ·
mono 12/16 logs and IDs. Dense: 12–13/16 everything; 700 headers.

**Flat spacing + radius:** scale 2 · 4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 (compact: 0 · 2 · 4 · 8 ·
12 · 16 · 20 · 24 · 32); button 20×4 (compact 16×2); card 20×16 (embedded 12×10). Radius: badge 4 ·
input/dropdown 8 · alert 12 · container/panel 16 · button/toggle 20.

**Component → token map.** Primary button: `accent.action` + `accent.onAction`, radius full,
`border.focus` ring on focus. Table row: `surface.raised` (transparent on white canvas), 48/40px
height, `surface.hover` on hover, `surface.selected` + 2px `accent.action` left border when
selected, `border.subtle` row hairlines. Container: `surface.canvas` + 1px `border.subtle`,
radius 16, padding 20×16, container title 20/700. Flash bar: `status.wash.*` + `status.*` ink +
status glyph, radius 12. Input: `surface.raised` + 1px `border.strong`, radius 8, focus =
`border.focus`, error text `status.error` on `status.wash.error` hint row. Global nav: `chrome.nav`
+ `chrome.onNav`. Status pill: `status.*` text on `status.wash.*`, radius badge, glyph + label.

**Agent prompt block.**

- Role→hex (light): surface.canvas #ffffff, surface.inset #f3f3f7, surface.hover/selected #f0fbff,
  border.subtle #c6c6cd, border.strong #8c8c94, border.focus #006ce0, accent.action #006ce0,
  accent.onAction #ffffff, text.primary #0f141a, text.secondary #424650, text.tertiary #656871,
  status.success #00802f, status.warning #855900, status.error #db0000, status.info #006ce0,
  status.wash.success #effff1, status.wash.warning #fffef0, status.wash.error #fff5f5,
  status.wash.info #f0fbff, chrome.nav #232f3e, chrome.onNav #f9f9fa.
- Dark: surface.canvas #161d26, surface.raised #1b232d, surface.overlay #232b37, border.subtle
  #424650, border.strong #656871, accent.action #42b4ff, accent.onAction #0f141a, text.primary
  #ebebf0, text.secondary #c6c6cd, status.success #2bb534, status.warning #fbd332, status.error
  #ff7a7a.
- Type: Open Sans; 42/700/48, 24/700/30, 20/700/24, 18/700/22, 16/700/20, 14/400/20, 12/400/16;
  mono for IDs and logs only; minimum 12px.
- Spacing: 4px base; use scale 2/4/8/12/16/20/24/32/40 only. Buttons 20px horizontal, 4px vertical.
  Cards 20×16. Radius: badge 4, input 8, alert 12, container 16, button 20.
- Density: standard rows 48px body 14px; dense rows 40px body 12–13px; never mix modes mid-page;
  toolbar = row height.

**Example component prompts.**

1. *Resource table surface* — `surface.canvas` background; containers separated by 1px
   `border.subtle`, radius 16, no shadow; page title 24/700 in `text.primary`; one `accent.action`
   fill (the "Create" button) top-right of the toolbar; table rows 48px standard / 40px dense,
   body 14px standard / 13px dense, numerics right-aligned tabular; hover `surface.hover`;
   selected `surface.selected` with 2px `accent.action` leading edge; focus ring `border.focus`;
   header, filter toolbar and pagination match row height.
2. *Async failure* — flash bar at page top: `status.wash.error` fill, radius 12, `status.error`
   glyph, `text.primary` sentence naming the failed operation, "Retry" as a link in
   `accent.action`; dismissible with Esc; announced politely; motion `base` entrance, 0ms under
   reduced motion.
3. *Confirm deletion* — modal at level 4 with scrim, radius 16, `surface.overlay`; title = the
   verb; body names the exact resource in mono; Cancel secondary, destructive button red-tinted;
   focus-trapped, Enter does not trigger the destructive control by default.

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
10. Dark authored, not filtered, with its own ramp and status hues.
11. No unoverridden stock default inside a committed surface.
12. Nothing came from a marketing page — brand orange and photography stay out of service UI.
13. The §9 brand-moment palette (chrome.hero slate) appears nowhere in the UI token layers.
14. Data-vis chart hues never style non-chart controls.
15. Legacy values (#0972d3 primary, #f2f3f3 canvas) verified absent.
