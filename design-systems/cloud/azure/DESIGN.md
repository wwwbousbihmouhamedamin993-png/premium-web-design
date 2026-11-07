# Design System — Microsoft Azure (Portal)

<!-- premium-web-design:design-system 2 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: Fluent 2 official token export @fluentui/tokens 1.0.0-alpha.24 (colour ramps, type ramp, radius, spacing, curves, durations — rung 2, authoritative npm source; no sibling-library spec exists for azure — rung 1 missed), Azure portal VM-overview and resource-group blades from learn.microsoft.com official screenshot media + azure.microsoft.com captures (shell, density, chrome — rung 3 grounding; top-bar blue #0078D4 and selected-row grey #EDEBE9 verified by pixel sampling of verified screenshots) -->
<!-- Surface classes: 8 routes classified; density classes S+D assigned (F reserved for marketing entry, sign-in and support-wizard flows) -->

## 1. Design Posture & Atmosphere

The Azure portal is mission control for someone else's production estate. Its emotional register is
confident, institutional calm: a solid band of Azure blue pinned across the top of the world, a white
blade canvas below it, near-black ink, and colour that appears only when infrastructure has a state
worth reporting. After eight hours the surface stays quiet — the eye never hunts, because every
resource answers the same three questions in the same order: what exists, what state is it in, what
can I do to it. Where AWS is a ledger sheet, Azure is an **instrument panel behind a concierge desk**:
a dense, sober working surface (blades, grids, Essentials key-value panels) with an ever-present
helper layer (global search, Copilot, contextual command bars) hovering one keystroke away.

Against its category defaults, Azure sits in the middle: less austere than the AWS console's
hairline rectangles (its chrome is unmistakably branded — the blue top bar survives in every theme),
less carded and pastel than GCP's home. The single visual metaphor is the **blade**: a full-height
pane that slides in over the workspace, carries one resource's whole life (overview, activity,
access, settings), and stacks left-to-right like folios. Navigation is a permanent blue header plus
a collapsible white service rail; nothing inside a blade is ever branded again.

**Key Characteristics**

- The brand lives in exactly one place inside the product: the 48px global top bar, solid
  #0078D4 with white ink in **both** themes (pixel-verified). Inside a blade, the portal could be
  any infrastructure vendor.
- Canvas and containers are both #FFFFFF in light mode — hierarchy comes from 1px hairlines
  (#D1D1D1) and gaps; a grey fill is reserved for *selection* (#EBEBEB) and never used as a
  surface layer.
- One accent fill per viewport in [S]: the primary command (Create, Review + create) in
  `accent.action`; links share the same blue, so affordance colour is 1:1 with interactivity.
- Rows are the centre of gravity: resource lists run 32px rows, 14px body, right-aligned
  tabular numerics, header rows that stick.
- Status ships as icon + label + colour; a green dot alone is never the whole message ("Running"
  renders as plain ink text, the glyph carries the hue).
- Density is an explicit axis: 40px comfortable rows in blade overviews, 28–32px rows in resource
  grids and activity logs, switched per route class, never mid-page.
- Radii are small and square-ish: 4px on controls, 8px on cards and panels — the roundness of
  Fluent 2 applied one family at a time.
- Motion is short and decelerate-only on entrance: 100–300ms from the official Fluent duration
  set; blades slide, everything else fades.
- Minimum product text size is 12px (captions/meta); 10px exists in the ramp but is reserved for
  step-function labels and badges, never for content.
- Monospace (Consolas) is strictly identifiers: subscription IDs, JSON View, connection strings,
  log lines.
- Dark mode is fully authored with its own inverted surface step (layers get *darker*, not
  lighter, as they rise) and an upgraded accessible stroke #ADADAD; dark is opt-in per user
  preference, light ships as default.
- Empty states name the missing resource and hand the exact creation CTA; a blank grid is never a
  blank page.
- Marketing surfaces (azure.microsoft.com) may spend saturation — 3D renders, gradients, navy
  bands (#00355E) — but that palette is quarantined from the portal token layers.

## 2. Token Architecture   ← normative

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value* (`blue.500`, `grey.38`, `red.tint40`),
  referenced only by L2. Banned: `[component]-[prop]` naming — one value, many roles. (Fluent's
  own alias layer names a token `colorBrandBackground`; this spec's L2 replaces that
  component-flavoured shape with `accent.action`.)
- **L2 Semantic** — role names (`surface.canvas`, `text.primary`, `accent.action`). The only
  layer a component may consume.
- **L3 Component** — only for deliberate deviation; points at L2 or L1, never a raw value, never
  a sibling component's token. The global top bar consumes `chrome.topbar` (resolving to the
  brand primitive `blue.500`) because the top bar is brand territory, not product UI; the Copilot
  control consumes `chrome.assistant` for the same reason.

**Rules.** Every token has a determinable type or it is invalid; names are case-sensitive and free
of `$`, `{`, `}`, `.`; circular references are an error. Every semantic token has a value in
**every** shipped mode — both themes (light, dark) are fully populated in §3; no role falls back
to its light value in dark. Animatable tokens (the two curves, the three durations) are registered
with explicit syntax and inheritance declarations or the registration is invalid; an initial value
must be computationally independent, so percentage or em-based initial values are illegal.

**Layer order (low → high)** `[reset] → [primitives] → [semantic] → [components] → [utilities]`.
Layer order beats specificity entirely, and an un-layered normal declaration outranks everything
layered — so a stray un-layered rule in a resource-provider stylesheet would beat this whole
system. This matters double at Azure scale: dozens of resource-provider teams ship UI into one
shell, and the layer contract is what keeps a legacy provider's blade from overwriting the
current shell. Anything a consuming team must override without `!important` sits in the top layer.

## 3. Colour Roles

Primitives below come from the official Fluent 2 token export (grey ramp, shared status colours)
plus the portal's legacy brand ramp (centred on #0078D4, the official shared *blue* primary —
distinct from the newer v9 web-brand #0F6CBD, which the portal has not adopted).

| Primitive ramp | Values (subset) |
|---|---|
| `blue.*` | 500 #0078D4 · 600 #106EBE (hover) · 700 #005A9E (pressed) · 800 #004578 · 400 #2B88D8 · 300 #71AFE5 · tint40 #A9D3F2 · tint50 #D0E7F8 · tint60 #F3F9FD · shade30 #004377 · shade40 #002440 |
| `grey.*` | 14 #242424 · 26 #424242 · 38 #616161 · 44 #707070 · 74 #BDBDBD · 82 #D1D1D1 · 88 #E0E0E0 · 90 #E6E6E6 · 92 #EBEBEB · 94 #F0F0F0 · 96 #F5F5F5 · 98 #FAFAFA |
| `navy.*` | 700 #00355E (marketing band) · 600 #025797 (selected marketing chip) |
| `green.*` | primary #107C10 · tint20 #359B35 · tint60 #F1FAF1 · shade40 #052505 |
| `red.*` | primary #D13438 · tint20 #DC5E62 · tint60 #FDF6F6 · shade40 #3F1011 |
| `orange.*` | primary #DA3B01 · tint20 #E36537 · tint60 #FDF6F3 · shade40 #411200 |
| `yellow.*` | primary #FDE300 (glyph only) · tint60 #FFFEF5 |

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` / `raised` / `overlay` / `inset` | #FFFFFF / #FFFFFF / #FFFFFF / #FAFAFA | #292929 / #1F1F1F / #141414 / #1F1F1F | canvas · blade content · flyout/dialog · wells. Dark steps *darker* as layers rise; borders carry separation |
| `surface.hover` / `surface.selected` | #F5F5F5 / #EBEBEB | #333333 / #3D3D3D | Interaction fills; selected service-menu row + selected table row |
| `border.subtle` / `strong` / `focus` | #D1D1D1 / #616161 / #0078D4 | #525252 / #ADADAD / #479EF5 | 1px hairlines; `focus` 2px; strong ≥3:1 in both modes |
| `accent.action` / `onAction` / `subtle` | #0078D4 / #FFFFFF / #D0E7F8 | #115EA3 / #FFFFFF / #002440 | Accent budget: 1 primary fill per viewport [S]; `subtle` = filter-chip and info washes |
| `chrome.topbar` / `chrome.assistant` | #0078D4 / #FFFFFF | #0078D4 / #FFFFFF | Brand territory; assistant = Copilot pill on blue |
| `text.primary` / `secondary` / `tertiary` / `disabled` | #242424 / #424242 / #616161 / #BDBDBD | #FFFFFF / #D6D6D6 / #ADADAD / #575757 | Ink ramp; disabled is exempt from contrast (inactive UI) and always paired with a disabled-state icon |
| `status.success` / `warning` / `error` / `info` | #107C10 / #DA3B01 / #D13438 / #0078D4 | #359B35 / #E36537 / #DC5E62 / #3595DE | Each ships a glyph — never colour alone. Washes: light tint60 (#F1FAF1, #FDF6F3, #FDF6F6, #F3F9FD); dark shade40 (#052505, #411200, #3F1011, #002440). Caution-level *yellow* #FDE300 is a glyph fill only, never text |

Dark canvas is **not** pure black: the range is #292929 (rest) → #141414 (deepest overlay), and
the top bar stays #0078D4. Depth in dark comes from the downward surface steps and 1px strokes,
never shadows.

**Contrast gate — computed ratios, unrounded.** Body ≥4.5:1; UI boundaries and focus indicators
≥3:1; disabled text is exempt (inactive UI) and recorded only.

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| text.primary (L) | #242424 | surface.canvas (L) | #FFFFFF | 15.52:1 | 4.5 | PASS |
| text.secondary (L) | #424242 | surface.canvas (L) | #FFFFFF | 10.05:1 | 4.5 | PASS |
| text.tertiary (L) | #616161 | surface.canvas (L) | #FFFFFF | 6.19:1 | 4.5 | PASS |
| accent.onAction (L) | #FFFFFF | accent.action (L) | #0078D4 | 4.53:1 | 4.5 | PASS |
| text.primary (D) | #FFFFFF | surface.canvas (D) | #292929 | 14.55:1 | 4.5 | PASS |
| text.secondary (D) | #D6D6D6 | surface.canvas (D) | #292929 | 10.01:1 | 4.5 | PASS |
| text.tertiary (D) | #ADADAD | surface.canvas (D) | #292929 | 6.48:1 | 4.5 | PASS |
| accent.onAction (D) | #FFFFFF | accent.action (D) | #115EA3 | 6.66:1 | 4.5 | PASS |
| border.strong (L) | #616161 | surface.raised (L) | #FFFFFF | 6.19:1 | 3.0 | PASS |
| border.strong (D) | #ADADAD | surface.raised (D) | #1F1F1F | 6.36:1 | 3.0 | PASS |
| border.focus (L) | #0078D4 | surface.canvas (L) | #FFFFFF | 4.53:1 | 3.0 | PASS |
| border.focus (D) | #479EF5 | surface.canvas (D) | #292929 | 5.18:1 | 3.0 | PASS |
| status.success (L) glyph | #107C10 | wash #F1FAF1 | #F1FAF1 | 5.03:1 | 3.0 | PASS |
| status.error (L) glyph | #D13438 | wash #FDF6F6 | #FDF6F6 | 4.62:1 | 3.0 | PASS |
| status.warning (L) glyph | #DA3B01 | wash #FDF6F3 | #FDF6F3 | 4.27:1 | 3.0 | PASS |
| status.info (L) glyph | #0078D4 | wash #F3F9FD | #F3F9FD | 4.27:1 | 3.0 | PASS |
| status.success (D) glyph | #359B35 | wash #052505 | #052505 | 4.63:1 | 3.0 | PASS |
| status.error (D) glyph | #DC5E62 | wash #3F1011 | #3F1011 | 4.50:1 | 3.0 | PASS |
| status.warning (D) glyph | #E36537 | wash #411200 | #411200 | 4.72:1 | 3.0 | PASS |
| status.info (D) glyph | #3595DE | wash #002440 | #002440 | 4.90:1 | 3.0 | PASS |

Disabled text (#BDBDBD on #FFFFFF = 1.88:1; #575757 on #292929 = 2.01:1) is recorded as exempt:
it always co-travels with a disabled icon and a tooltip that states why.

## 4. Typography

**Families.** UI **Segoe UI** (Segoe UI Variable on Windows 11), self-hosted on non-Windows
clients as *Segoe UI Web (West European)*, fallback stack system sans; numeric **Bahnschrift →
Segoe UI** for large stat values; code **Consolas, Courier New** for identifiers, subscription
GUIDs, connection strings, JSON View and log lines. *Monospace is for identifiers and code, never
a costume.* Segoe UI renders slightly narrow: do not compensate with negative tracking.

**One ramp table per class, not one blended table.** Columns: role, size, weight, line height,
tracking, numerals, use. Sizes/weights/line heights below are the official Fluent 2 ramp values
(fontSizeBase100–600, Hero700–1000; weights 400/500/600/700).

- **[F] Marketing/entry, 16px base (fontSizeBase400):**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Display XL | 68px | 600 | 92px | -0.01em | — | Homepage hero only (hero1000) |
| Display | 40px | 600 | 52px | -0.005em | — | Section hero (hero900) |
| Title | 32px | 600 | 40px | 0 | — | Page hero (hero800) |
| Heading | 24px | 600 | 32px | 0 | — | Section heading (base600) |
| Body | 16px | 400 | 22px | 0 | lining | Lead paragraph (base400) |
| Body small | 14px | 400 | 20px | 0 | lining | Card copy (base300) |
| Label | 14px | 600 | 20px | 0 | — | Button/link label (body1Strong) |
| Meta | 12px | 400 | 16px | 0.01em | lining | Eyebrow, legal (caption1) |

- **[S] Standard blade, 14px base (fontSizeBase300):**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Page title | 20px | 600 | 28px | 0 | — | Blade title (subtitle1) |
| Section title | 16px | 600 | 22px | 0 | — | Essentials, tab groups (subtitle2) |
| Body | 14px | 400 | 20px | 0 | lining | Blade prose, descriptions (body1) |
| Row primary | 14px | 400/600 | 20px | 0 | lining | Resource name (links #0078D4) |
| Row secondary | 12px | 400 | 16px | 0 | lining | Region, tier beneath name (caption1) |
| Stat value | 24px | 600 | 32px | 0 | tabular | Metric tiles (base600) |
| Stat label | 12px | 600 | 16px | 0.02em uppercase | — | Metric name (caption1Strong) |
| Meta | 12px | 400 | 16px | 0.01em | lining | Breadcrumb tail, timestamps (caption1) |

- **[D] Dense data surfaces, 12–13px base, grids/logs only:**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Grid header | 12px | 600 | 16px | 0 | — | Column headers (caption1Strong) |
| Grid cell text | 13px | 400 | 18px | 0 | lining | Resource names, states |
| Grid cell numeric | 13px | 400 | 18px | 0 | tabular | Counts, sizes, costs — right-aligned |
| Log line | 12px | 400 | 16px | 0 | tabular | Activity log, JSON View (Consolas) |
| Inline help | 12px | 400 | 16px | 0 | lining | Field hints (caption1) |

*Prose inside a dense screen still steps up to 14px.* No content below 12px, ever; 10px
(fontSizeBase100) exists in the ramp for badge counters and axis labels only.

**Invariants.** `tabular-nums` on every comparable value — currency, timestamps, deltas, counts,
IDs, GUIDs. Right-align numerics, left-align text, never centre a numeric column. Fixed stepped
sizes; no fluid clamp() scaling. Measure ≤80 characters (SC 1.4.8); 65–80ch [F], blade body
prose 60–80ch, unconstrained [D].

## 5. Spacing Scale & Density Scales   ← two axes, never one

**Spacing base: 4px grid; 8px comfortable [S], 4px [D].** The scale is the official Fluent set:
`space.0` 0 · `xxs` 2px chip/label micro-gaps · `xs` 4px icon-to-label, control padding [D] ·
`sNudge` 6px inline icon nudges · `s` 8px control padding [D], cell gaps · `mNudge` 10px ·
`m` 12px cell padding [S] · `l` 16px card padding [S] / page gutter [D] · `xl` 20px ·
`xxl` 24px card padding [F] + section gap · `xxxl` 32px section gap [S] / hero gutters [F].
*No 17px. No 23px. If a layout needs an off-scale value, the layout is wrong.*

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | Marketing entry, sign-in, support wizards |
| `standard` | 40–44px | 14px | 12px | 24px | Blade overviews, Essentials, service dashboards |
| `dense` | 28–32px | 12–13px | 8px | 16px | Resource grids, activity log, cost tables |

- Density comes from **row height, column pruning and leading** — never from type too small to
  read. A 13px tabular numeral in a dense grid is correct; the same numeral in an [S] Essentials
  panel is a defect.
- **Never switch mid-page.** A blade is one density for its whole life; switching across routes
  with different jobs is legitimate and should feel like a different room.
- **Chrome follows rows.** Command bar (44px), filter bar (32px) and pagination (32px) heights
  agree with the row rhythm they govern; a 44px command bar over 28px grid rows is a rhythm break
  only when they sit in the same visual group — the portal's command bar intentionally sits
  outside the grid card, separated by a hairline.
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40%. *House heuristic, not a
  vendor figure — validate by screenshot.*

## 6. Radius Scale

`none` 0 blades, tables, full-bleed panels · `xs` 2px dense chips, tag counters · `sm` 4px
buttons, inputs, selects, command-bar items, dropdowns (Fluent medium — the portal's workhorse
radius) · `md` 6px stat tiles, hover cards · `lg` 8px cards, dialogs, flyouts, marketing product
cards (Fluent xlarge) · `full` 9999px pills, avatars, category chips, Copilot pill. **One radius
per component family**, never mixed ad-hoc: every input in a form is `sm`; every card in a group
is `lg`. Nested radii obey `radius_inner = radius_outer − padding`.

## 7. Elevation

**Strategy: multi-layer ambient + key shadows in light; surface steps + keylines in dark — one
paradigm per mode, never mixed.** Fluent's shadow tokens pair an ambient layer (even, 0.12 alpha
family) with a key layer (directional, 0.14 alpha family) in light; dark shifts to 0.24/0.28 and
relies primarily on the surface step.

- **Level 0 — canvas/blade body:** no shadow, both modes; separation via `border.subtle`.
- **Level 1 — cards, stat tiles, tiles in dashboards:** shadow 0 1px 2px rgba(0,0,0,0.14) +
  0 0 2px rgba(0,0,0,0.12); dark: one step down to `surface.raised` + `border.subtle`.
- **Level 2 — command bar, sticky headers, pinned tiles:** shadow 0 2px 4px rgba(0,0,0,0.14) +
  0 0 2px rgba(0,0,0,0.12); dark: `surface.raised` + `border.strong` keyline.
- **Level 3 — flyouts, dropdowns, service-menu flyout:** shadow 0 8px 14px rgba(0,0,0,0.24) +
  0 0 2px rgba(0,0,0,0.20); dark: `surface.overlay` #141414 + `border.strong`.
- **Level 4 — dialogs:** level-3 shadow + scrim rgba(0,0,0,0.4) light / rgba(0,0,0,0.5) dark.

A shadow is invisible on #292929 — in dark, elevation that *rises* renders **darker** (#292929 →
#1F1F1F → #141414) with a stronger keyline, which is the authored inversion this spec keeps.

## 8. Motion

`instant` 50ms (state ticks, selection fills) · `fast` 100ms (hover/exit fades [D]) · `base`
150ms (dropdowns, tooltips, [D] entrances) · `slow` 300ms (blade slide-in, dialog, [F/S]
entrances; 400–500ms reserved for marketing hero reveals). Curves from the official set:
entrances **decelerate** cubic-bezier(0.1, 0.9, 0.2, 1); exits **accelerate**
cubic-bezier(0.8, 0, 0.78, 1); symmetric ease cubic-bezier(0.33, 0, 0.67, 1) only for
position-neutral crossfades.

- Entrances decelerate, exits accelerate; symmetric ease-in-out on both directions is a defect.
- Animate `transform` and `opacity` only — never width, height, top, left. Blades slide as a
  whole pane; their content fades 50ms later.
- No bounce on irreversible moments: not on Delete confirmation, not on subscription downgrade.
- **Reduced motion is a real variant**, not an `animation: none` sweep: blade slides, tile
  re-layouts and chart draw-ons collapse to a ≤150ms crossfade; only large scaling/panning
  movement must be neutralised, not every fade.

## 9. Imagery & Art Direction

**Policy, not asset list.**

- **Brand moment:** the marketing hero (azure.microsoft.com) — abstract 3D renders and gradient
  fields in the cyan/violet/purple family — is the single expressive surface. Its palette is
  quarantined: **never leaks into portal UI tokens** (no gradient, no violet, inside a blade).
  Inside the portal the one saturation moment per viewport is the primary command fill.
- **Iconography:** Fluent product/service icons — flat two-tone blue-family glyphs on a 32px grid
  (16px inside command bars), geometric, matched to Segoe UI's tone. Resource-provider icons are
  always the official glyph, never recoloured. Icon-only controls still carry a tooltip label
  (§10).
- **Photography:** none inside the portal; marketing uses customer-story photography with a
  consistent blue-violet grade. Third-party logos (Linux distros, databases) render as-is at
  small sizes inside service rows — they are *data*, not decoration.
- **Illustration / 3D:** portal empty states use small line illustrations plus the recovery CTA;
  if a provider ships no illustration, the empty state is text + CTA — an unspecified gap must
  not invite per-screen invention.
- **Charts:** metric tiles (CPU, availability) use the brand blue ramp; status thresholds colour
  only the breach segment, with the axis and labels staying neutral ink.

## 10. Surface & Component Inventory

One row per real component; a component without documented disabled and loading states is
unfinished.

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell (top bar) | — | light/dark | — | `G+`/ search focus | "Search resources, services, and docs (G+/)" |
| Service rail (hub menu) | S | collapsed icon rail / expanded labels | hover, selected #EBEBEB, pinned | Arrow nav; `–` collapses | "All service menus" |
| Breadcrumb | S | — | link, current | Enter opens parent | "Home > Virtual machines > myVM1" |
| Blade (page container) | S | root blade / stacked child | loading, loaded, error, closed | `Esc` closes top blade | Resource name + star/favourite |
| Command bar | S/D | icon+label, icon-only w/ tooltip | rest, hover, disabled ("why" tooltip), loading | Tab order = visual order | "Create", "Refresh", "Delete" |
| Filter/search bar | D | filter chips, free-text | active chip (blue wash), cleared | Enter applies | "Filter for any field...", "Subscription equals all" |
| Data grid (resource list) | D | sortable headers, checkbox select, group-by | row hover #F5F5F5, selected, loading skeleton, empty, error | Shift+Arrow range select | "Showing 1 to 2 of 2 records" |
| Row action menu | D | "…" overflow | focus-trap, `Esc` closes, disabled items w/ reason | Arrow + Enter | "Delete", "Move", "Lock" |
| Essentials panel | S | collapsed 2-row / expanded | expand/collapse, loading skeleton | Chevron toggles | "Essentials", "View Cost", "JSON View" |
| Stat tile (metric) | S | small/expanded, pinned | loading shimmer, no-data ("No events"), stale | Pin icon on focus | "CPU (average)", "VM Availability (Preview)" |
| Tab set (Properties/Monitoring) | S | underline tabs | selected, hover, disabled w/ count | Arrow keys move | "Monitoring", "Capabilities (8)" |
| Dialog | — | confirm, wizard step | scrim, focus-trap, `Esc` = cancel | Focus moves in; `Esc` cancels | "Delete resource group?", names cost + effective date |
| Create wizard | S | Basics/Tags/Review+create tabs | validating, error per field, submit loading | Next/Back; summary on last tab | "Review + create", "Validation passed" |
| Cost/subscription control | S | — | confirming, prorating, blocked (policy) | — | Names cost + effective date before commit |
| Activity log entry | D | expandable | status glyph + label, timestamp tabular | Enter expands | "Delete virtual machine (Succeeded)" |
| Command palette (search) | — | all-scope results | typeahead, no results, recent | `G+/` opens; `Esc` closes | "Search resources, services, and docs" |

**Every fetching surface also designs:** loading (shimmer skeletons matching final geometry —
never a centred spinner on a blank page), empty (what's missing + the creation CTA that fixes
it), error (what happened + Retry + support correlation), offline/stale (banner naming the last
refresh time; "cached" never silently passes as live).

**Contracts this table encodes:** one primary filled CTA per view [S] (command bars may run the
primary plus icon actions); every icon-only control carries a tooltip; a disabled control states
*why* on focus or hover (e.g. greyed "Hibernate" with "Not supported for this size" tooltip);
a button never changes width between idle and loading — the label is reserved before the
spinner appears.

## 11. Light / Dark Strategy

- **Posture: C — dual parity.** The portal ships light as default with a full dark theme
  (Settings > Appearance, plus Auto); both are first-class, and the blue top bar is theme-proof.
- **Mechanism:** semantic roles remapped per mode; **no role absent in either mode.** The one
  intentional constant is `chrome.topbar` (#0078D4 with white ink — 4.53:1 in both), because the
  brand chrome must not flicker across theme switches.
- **`color-scheme`** is set at the document root so UA chrome, form controls and scrollbars
  follow the active theme; a `<meta name="color-scheme">` equivalent ships before styles so the
  first paint is never the wrong scheme.
- **Dark is authored, not inverted:** its own downward surface ramp (#292929 → #1F1F1F →
  #141414), its own stronger border pair (#525252 hairline, #ADADAD accessible stroke — a hairline
  that reads as delicate on white reads as invisible on #292929), its own status tints (#359B35
  family), zero shadows. `light-dark()` where available is progressive enhancement only.
- The dark theme's accessible stroke (#ADADAD, 6.48:1 on raised) is deliberately much stronger
  than light's #D1D1D1 hairline (1.36:1, decorative only): light puts 3:1 duties on #616161,
  dark on #ADADAD.

## 12. Density-Mode Strategy

- **Default mode per surface class:** blades and overviews = `standard` (40–44px rows); resource
  grids, activity logs, cost analysis = `dense` (28–32px rows). The boundary is the route's job:
  reading vs scanning.
- **Mechanism:** a density setting at the app root rescales row height, cell padding, gutter and
  body size together as one token axis — Carbon's rule that spacing tokens "do not change values
  based on the screen size" applies; density is never a media query.
- **Container queries for reflow:** grids reflow to their pane, not the viewport, so a blade
  snapped to half-screen keeps its column plan; `cq*` units are never used where the
  no-eligible-container fallback would be wrong.
- **Style queries** compare computed values, so the density marker is a registered property with
  explicit syntax and inheritance.
- **Offer the switch as an accessibility affordance**, not a preference: W3C's SC 2.5.8 note
  endorses "a mechanism to control the density of layout," naming users with visual field loss.
  The portal's own "compact density" experiments ship exactly this.

## 13. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA (SC 1.4.6 contrast ≥7:1) for body prose in documentation
  surfaces, where #242424 on #FFFFFF already computes 15.52:1.
- **Target size:** ≥24×24 CSS px hard minimum (SC 2.5.8); design target 32×32 for command-bar
  icon buttons and service-rail items [S/D], 44×44 for primary controls [F]. Zoom does not excuse
  it.
- **Keyboard:** every function operable (SC 2.1.1) — the portal's own contract: `G+/` global
  search, `Esc` pops the top blade, arrow-key nav in grids and menus, full focus order = visual
  order. Focus indicator visible (SC 2.4.7): 2px `border.focus` ring (#0078D4 light 4.53:1,
  #479EF5 dark 5.18:1), never removed without a stronger replacement; the focused row is never
  entirely hidden behind the sticky command bar (SC 2.4.11).
- **Contrast:** text ≥4.5:1 (all ink ramps pass — §3); UI boundaries and focus ≥3:1. **Colour
  independence:** every status pairs colour with a glyph and a label ("Succeeded", "Failed",
  "Running"); deltas carry a sign or direction glyph; provisioning state is always text.
- **Motion:** the §8 reduced-motion variant per component; no auto-playing carousels in product.
- **Text:** ≤80-character measure (SC 1.4.8), 1.5 leading on prose, 200% resize without
  horizontal scroll in blade prose.
- **Semantics:** real buttons/links/inputs; blades are labelled dialogs in the accessibility tree
  with the resource name; headings match visual rank (blade title = level 1, Essentials = level
  2); `aria-live="polite"` announces provisioning-state changes and validation results;
  `aria-busy` on loading grids.
- **Contrast preference:** `prefers-contrast: more` upgrades hairlines #D1D1D1 → #616161, raises
  text.tertiary to text.secondary, and swaps the focus ring to the accessible stroke family.

## 14. Anti-Patterns

Product-calibrated; each carries the reason it was rejected *for this product*.

**Do**

1. Keep every blade's structure identical: title → command bar → filter → content. Operators
   navigate by muscle memory between 10,000+ resource types.
2. Show provisioning state as text + glyph ("Running" with the dot), because colour alone fails
   everywhere it matters (accessibility, screenshots, printing).
3. Reserve Consolas for identifiers and JSON View — a subscription GUID in Segoe UI is unreadable
   at 13px; prose in Consolas is unreadable everywhere.
4. Pin the Essentials panel's two most important keys (Status, Location) even when collapsed.
5. Use the full-blue fill exactly once per viewport; every other action is outline or icon.
6. Make disabled commands explain themselves — greyed "Hibernate" carries "Not supported for
   this VM size" on hover/focus.
7. Match skeleton geometry to final content geometry; a shimmer that reflows on load is a bug.
8. Keep the top bar blue in both themes so the brand chrome never flickers on theme switch.
9. Right-align every numeric column and give it tabular numerals — cost tables are scanned
   column-wise, not row-wise.
10. Prefer stacking a child blade over a modal for resource details — depth is navigable history
    (`Esc` pops), not an interrupt.
11. Design the empty grid as an onboarding step: "No resource groups in this subscription" +
    the exact Create CTA.
12. Quarantine marketing navy #00355E and gradient art to azure.microsoft.com; a blade canvas
    stays achromatic.

**Don't**

1. No marketing aesthetics inside the product: no hero gradients, no rounded 24px corners, no
   oversized display type on blade canvases.
2. No card inflation: a blade is not a dashboard of stat cards; metrics tiles exist only where
   telemetry is the content.
3. No whole-page spinners — skeletons match final geometry, per region.
4. No two primary fills side by side; the Copilot pill is chrome-level, not a competing CTA.
5. No unlabelled icon toolbars: every icon command has a tooltip and (in [S]) a label.
6. No hover-only affordances: row actions are reachable by keyboard and visible focus.
7. No placeholder-as-label: floating placeholders vanish; Essentials keys are persistent labels.
8. No `alert()`/`confirm()`-style native interrupts; destructive actions get the dialog with the
   resource name spelled out.
9. No tiny type as a density strategy — density comes from rows and pruning; 10px is for badge
   counters only.
10. No disabled primary button with no explanation — "Review + create" disabled always names the
    failing validation.
11. No yellow (#FDE300) as text or fill on white — it is a glyph fill only; caution text is
    #DA3B01 or neutral ink.
12. No mid-blade density switches, no mixed radii inside one component family, no shadow on dark
    surfaces (steps + keylines carry depth), no pure black (#000000) canvas anywhere.

## 15. Quick Reference & Verification Gate

**Colour (role → hex):** canvas #FFFFFF / #292929 · raised #FFFFFF / #1F1F1F · overlay #FFFFFF /
#141414 · inset #FAFAFA / #1F1F1F · hover #F5F5F5 / #333333 · selected #EBEBEB / #3D3D3D ·
border.subtle #D1D1D1 / #525252 · border.strong #616161 / #ADADAD · border.focus #0078D4 /
#479EF5 · accent.action #0078D4 / #115EA3 · onAction #FFFFFF / #FFFFFF · accent.subtle #D0E7F8 /
#002440 · topbar #0078D4 / #0078D4 · text #242424·#424242·#616161·#BDBDBD / #FFFFFF·#D6D6D6·
#ADADAD·#575757 · success #107C10 / #359B35 · warning #DA3B01 / #E36537 · error #D13438 /
#DC5E62 · info #0078D4 / #3595DE.

**Type ramp:** 68/92·600 displayXL [F] · 40/52·600 display [F] · 32/40·600 title1 · 28/36·600
title2 · 24/32·600 title3 + stat value · 20/28·600 subtitle1 = [S] page title · 16/22·600
subtitle2 = section title · 16/22·400 body2 [F] · 14/20·400 body1 = [S] base · 13/18·400 [D]
cell · 12/16·400 caption1 = [S] meta + [D] header(600) · 10/14 caption2 = badge counters only.
Weights 400/500/600/700; mono Consolas; numeric Bahnschrift.

**Spacing + radius:** 2·4·6·8·10·12·16·20·24·32 on a 4px grid (densities per §5). Radius 0 ·
2 · 4 (controls) · 6 (tiles) · 8 (cards/panels) · 9999 (pills).

**Component → token map:** blade → surface.canvas + border.subtle + text.primary + accent.action
(one fill) · command bar → surface.raised + border.subtle + text.primary, disabled text.disabled
+ tooltip · grid rows → surface.canvas, hover surface.hover, selected surface.selected, numerics
tabular · filter chip → accent.subtle wash + accent.action text · Essentials → surface.canvas +
border.subtle dividers + text.secondary labels · status row → status.* glyph + text.primary
label · top bar → chrome.topbar + onAction ink · Copilot pill → chrome.assistant.

**Agent prompt block.**

```
ROLE → HEX (light / dark):
surface.canvas   #FFFFFF / #292929     surface.raised  #FFFFFF / #1F1F1F
surface.overlay  #FFFFFF / #141414     surface.hover   #F5F5F5 / #333333
surface.selected #EBEBEB / #3D3D3D     border.subtle   #D1D1D1 / #525252
border.strong    #616161 / #ADADAD     border.focus    #0078D4 / #479EF5
accent.action    #0078D4 / #115EA3     accent.onAction #FFFFFF / #FFFFFF
accent.subtle    #D0E7F8 / #002440     chrome.topbar   #0078D4 / #0078D4
text.primary     #242424 / #FFFFFF     text.secondary  #424242 / #D6D6D6
text.tertiary    #616161 / #ADADAD     text.disabled   #BDBDBD / #575757
status.success   #107C10 / #359B35     status.warning  #DA3B01 / #E36537
status.error     #D13438 / #DC5E62     status.info     #0078D4 / #3595DE
FONT: Segoe UI (Segoe UI Variable on Win11); mono Consolas. 4px grid.
TYPE: 68/92·600 [F hero] 40/52·600 32/40·600 24/32·600 20/28·600 [S title]
      16/22·600 14/20·400 [S base] 13/18 [D cell] 12/16 [meta] — tabular-nums on numerics.
SPACE: 2 4 6 8 10 12 16 20 24 32. RADIUS: 0/2/4/6/8/pill.
MOTION: 100ms out (exit) · 150ms decelerate (menus) · 300ms decelerate (blades);
        curves decelerate cubic-bezier(0.1,0.9,0.2,1), accelerate cubic-bezier(0.8,0,0.78,1).
```

**Example component prompts.**

1. *Resource blade (primary surface)* — `surface.canvas` background, radius 0 (full-bleed pane),
   24px padding around the title block, 16px inner gutters; blade title in `text.primary` at
   20px/600 with the provider icon at 32px; one `accent.action` fill (the Create/Save command);
   command bar separated by `border.subtle`; no shadow above level 1; breadcrumb in
   `text.secondary` with links in `accent.action`.
2. *Resource grid row (data row)* — 32px dense row height; `tabular-nums` on every numeric cell,
   right-aligned; checkbox column 40px wide; resource name in `accent.action` link ink, state
   cell as status glyph + `text.primary` label; hover `surface.hover`, selected
   `surface.selected`; header, filter bar and pagination heights agree with the row rhythm;
   focus ring `border.focus`.
3. *Essentials panel* — `surface.canvas`, `border.subtle` top and bottom hairlines, 12px label
   column in `text.secondary`, values in `text.primary`; links `accent.action`; collapsed state
   keeps Status + Location visible; "JSON View" opens the Consolas identifier surface.

**Pre-ship checklist.** 1 Zero raw hex outside L1. 2 No token resolves to a component name.
3 Every contrast pairing computed, passing, unrounded. 4 Every semantic role has a value in every
shipped mode. 5 Every fetching surface has loading/empty/error/offline specified. 6 Every
component row lists disabled and loading states. 7 Row, header, toolbar and pagination heights
agree. 8 Reduced-motion variant written for every authored motion. 9 Every control
keyboard-reachable with a visible focus indicator. 10 Dark authored, not filtered, with the
accessible stroke exceeding light's hairline strength. 11 No unoverridden stock library default
inside a committed surface. 12 Nothing came from a marketing page — marketing's navy and
gradients stay out of the token layers. 13 The §9 brand-moment palette (cyan/violet 3D renders,
#00355E band) appears nowhere in the UI token layers.
