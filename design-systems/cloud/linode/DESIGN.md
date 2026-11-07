# Design System — Akamai Cloud Manager (Linode)

<!-- premium-web-design:design-system 2 -->
<!-- As-of: 2026-11-02 -->
<!-- Reference inspirations: Akamai Design Language System (@linode/design-language-system official token release — rung 2), linode/manager open-source theme source (packages/ui foundations — rung 2), Cloud Manager light+dark surfaces verified from official repo PR screenshots (rung 2 artifacts); rung 1 had no sibling spec; rung 3 reverse-engineering was not needed -->
<!-- Surface classes: 12 routes classified; density classes S + D assigned (F reserved for auth/checkout) -->

## 1. Design Posture & Atmosphere

The Akamai Cloud Manager (cloud.linode.com, born as Linode Cloud Manager) is a network operations
ledger, not a showroom. A compute instance, a volume, a firewall, a NodeBalancer — each is a row
with a label, an IP, a region, a status dot, and a kebab menu. The canvas is a faint cool gray, the
panels are pure white with 1px hairlines, every corner is square, and the single filled color in a
resting viewport is the Akamai websafe blue action. After eight hours the surface should feel like
a well-kept terminal with manners: nothing decorates, everything measures, and the eye always has a
hairline or a tabular numeral to hold onto.

Against its category, this console sits deliberately plainer than the hyperscalers' glass cockpits
and more austere than DigitalOcean's: no illustration system, no rounded cards, no marketing
gradients inside the shell — but with real engineering furniture underneath (tag chips on every
resource, region pickers with flags, hourly/tabular pricing, type-to-confirm destroys, a global
command search). The one visual metaphor is the **ledger**: resources are line items, create flows
are order forms that name hardware and price before anything is provisioned, and destructive
actions quote the exact object back to you before they fire.

The identity is dual-branded by design: the product speaks Akamai (websafe blue action, near-black
global chrome, Nunito Sans) while the legacy Linode green survives only in the brand molecule icon
and the tricolor brand gradient — a green→teal→blue hairline at the top of the app bar and the
"in-progress" state of progress bars. That gradient and that icon are the entire licensed
saturation budget; everything else is ink, hairline, blue, and status.

**Key Characteristics** —
- Square-cornered ledger: the token system's default radius is 0 — panels, inputs, buttons and
  dialogs are all sharp; rounding exists only for 2px tag chips, 3px region flags, and full-circle
  status dots/avatars.
- One accent fill per viewport: the primary action renders `accent.action` blue `#0174bc` (light) /
  `#5bb3ea` with dark ink (dark); every other control is outline, text, or icon.
- Global chrome is near-black `#232326` (56px top bar + product search) over a 232px light side
  menu (48px collapsed) — verified in both modes; the dark mode side menu is `#343438`.
- Canvas is cool paper `#f7f7fa`, panels pure `#ffffff`; dark canvas is authored gray
  `#343438` → raised `#3d3d42` — never pure black, never inverted.
- Data tables are the atom: 40px rows, filled header band `#e5e5ea`, zebra rows at the canvas tone,
  hover wash `#edf8ff`, sortable column headers with icons, kebab row menus.
- Status is a pill of neutral ink with a 16px colored dot — colour never carries the status word.
- Tag chips are first-class: pale blue chips with blue text, `+n` overflow counters, removable in an
  inline editor.
- Money, IPs, transfer counts, and timestamps always render in tabular numerals, right-aligned.
- Region is always named with a flag glyph plus "City, Country" ("US, East Wenatchee, US";
  "PL, Krakow").
- Drawers, not dialog chains: create/reserve flows open a right-side panel with a title, fields,
  a price line, and Cancel + primary; confirmation dialogs are reserved for irreversible moments.
- Notification banners carry a 48px colored left band + tinted background + status icon, with body
  text always in primary ink.
- The brand gradient `270deg #00b050 → #12a594 → #009cde` appears only as the app-bar top hairline
  and the in-progress progress bar; it never fills a control.
- Type is Nunito Sans 400/600/700/800 with Fira Code for identifiers; body 14px/20px; page titles
  24px/30px at ≥1280px viewports (20px below).
- Density is a mode: 14px standard lists and forms, 12–13px console/log surfaces; chrome heights
  always match the row height of the surface they serve.

## 2. Token Architecture   ← normative

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value*, mirroring the official palette families:
  `neutrals.[step]` (5–100 plus `black`/`white`, cool gray ramp), `brand.[step]` (Akamai blues
  5–100), `green.[step]`, `red.[step]`, `orange.[step]`, `amber.[step]`, `yellow.[step]`,
  `lime.[step]`, `teal.[step]`, `cyan.[step]`, `ultramarine.[step]`, `violet.[step]`,
  `purple.[step]`, `magenta.[step]`, `pink.[step]`, `brown.[step]`; spacing `space.s0–s96`
  (0/2/4/6/8/12/16/20/24/28/32/36/40/48/64/72/96); type sizes 12–36px with paired line heights
  16–42px; weights 400/600/700/800. Primitives are referenced only by L2. Banned:
  `[component]-[prop]` naming (`--card-bg`, `--tooltip`) — one value, many roles.
- **L2 Semantic** — role names (`surface.canvas`, `surface.raised`, `text.primary`,
  `accent.action`, `accent.onAction`, `border.subtle`, `status.success`, `status.error` …),
  resolved per mode. The only layer a component may consume.
- **L3 Component** — only for deliberate deviation; points at L2 or L1, never a raw value, never a
  sibling component's token (e.g. `table.headerFilled.background` → `surface.inset`;
  `sidenav.selectedPill.background` → `accent.action`).

**Rules.** Every token has a determinable type (color, dimension, font-family, font-style, shadow,
duration) or it is invalid; names are case-sensitive and free of `$`, `{`, `}`, `.`; circular
references (`a → b → a`) are errors. Every semantic token carries a value in **every** shipped mode
— the product ships light, dark, and a system-following preference, and the official token release
authors both modes of every alias, so no role is single-mode. Animatable tokens are registered with
both `syntax` and `inherits`; `initial-value` must be computationally independent, so `%`/`em` are
illegal there.

**Layer order (low → high)** `[reset] → [primitives] → [semantic] → [components] → [utilities]`.
Layer order beats specificity entirely, and unlayered normal declarations outrank layered ones —
a stray un-layered rule in a component file would beat this whole system; anything a consumer must
override without `!important` sits in the top layer.

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` | `#f7f7fa` (`neutrals.5`) | `#343438` (`neutrals.100`) | Page ground; also the zebra-row tone under raised rows |
| `surface.raised` | `#ffffff` | `#3d3d42` | Cards, panels, table rows, drawers, dialogs |
| `surface.overlay` | `#ffffff` | `#3d3d42` | Menus, popovers, dropdowns, toasts |
| `surface.inset` | `#ededf2` (`neutrals.10`) | `#515157` | Filled table headers, wells, filter trays |
| `surface.hover` | `#edf8ff` (`brand.10`) | `#47474d` | Row/menu/item hover fill |
| `surface.selected` | `#ceedfe` (`brand.30`) | `#515157` | Selected rows, active side-nav item wash |
| `border.subtle` | `#d6d6dd` (`neutrals.30`) | `#515157` | 1px hairlines, dividers, card frames |
| `border.strong` | `#83838c` (`neutrals.60`) | `#a3a3ab` (`neutrals.50`) | Input frames, emphasis strokes |
| `border.focus` | `#0174bc` | `#5bb3ea` | Focus ring, selected radio/checkbox, ≥3:1 |
| `accent.action` | `#0174bc` (`brand.90`) | `#5bb3ea` (`brand.60`) | Primary fill; hover `#009cde` / `#96cff0`; budget: 1 fill + ≤2 glyph uses per viewport |
| `accent.onAction` | `#ffffff` | `#343438` | Ink on the fill (dark mode fills are light, ink goes dark) |
| `accent.subtle` | `#edf8ff` (`brand.10`) | `#47474d` | Secondary-button hover wash, info washes |
| `accent.link` | `#0174bc` (`brand.90`) | `#7dcdff` (`brand.55`) | Text links; hover `#009cde` / `#96cff0` |
| `text.primary` | `#343438` (`neutrals.100`) | `#ffffff` | Headings, row primaries, banner bodies |
| `text.secondary` | `#696970` (`neutrals.70`) | `#a3a3ab` (`neutrals.50`) | Descriptions, hints, placeholders |
| `text.tertiary` | `#83838c` (`neutrals.60`) | `#83838c` | Decorative meta only; 3:1 house floor (see gate) |
| `text.disabled` | `#a3a3ab` (`neutrals.50`) | `#83838c` | Inactive components (exempt) |
| `text.inverse` | `#d6d6dd` (`neutrals.30`) | `#d6d6dd` | Text/icons on the `#232326` global chrome |
| `status.success` | dot `#00b050` / text `#138246` on wash `#dff3df` | dot `#00b050` / ink-text on `#343438` | Active, running, available |
| `status.warning` | band/icon `#fecb34` / text ink `#343438` on wash `#ffecbc` | `#fecb34` on `#343438` | Degraded, migrating; amber never carries text |
| `status.error` | glyph `#d63c42` / text `#b82329` on wash `#ffe5e5` | text `#eb9091` on `#343438` | Failed, expired; danger button `#b82329` |
| `status.info` | glyph `#4067e5` / text `#3451b2` on wash `#e6edfe` | glyph `#8da4ef` on `#343438` | Tips, notices; banner band `#4067e5` |

Dark canvas is **not** pure black: the authored ramp runs `#232326` (global chrome) → `#343438`
(canvas) → `#3d3d42` (raised) → `#515157` (inset/selected). Depth in dark comes from surface steps
and 1px strokes, never shadows; dark border strength exceeds light's (see gate rows 21–22).

**Contrast gate — computed ratios, unrounded; 4.499:1 fails. Body ≥4.5:1; UI boundaries and focus
indicators ≥3:1** (W3C, SC 1.4.3, 1.4.11). Large text is ≥24px or ≥18.5px bold.

| # | Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | `text.primary` light | `#343438` | `surface.canvas` | `#f7f7fa` | 11.591:1 | 4.5 | PASS |
| 2 | `text.primary` light | `#343438` | `surface.raised` | `#ffffff` | 12.394:1 | 4.5 | PASS |
| 3 | `text.secondary` light | `#696970` | `surface.canvas` | `#f7f7fa` | 5.094:1 | 4.5 | PASS |
| 4 | `text.secondary` light | `#696970` | `surface.raised` | `#ffffff` | 5.447:1 | 4.5 | PASS |
| 5 | `text.tertiary` light | `#83838c` | `surface.canvas` | `#f7f7fa` | 3.513:1 | 3.0 floor | PASS (non-informative meta only) |
| 6 | `accent.onAction` light | `#ffffff` | `accent.action` | `#0174bc` | 4.970:1 | 4.5 | PASS |
| 7 | `accent.onAction` light | `#ffffff` | `accent.action` hover | `#009cde` | 3.084:1 | 4.5 | FAIL (hover state — see note a) |
| 8 | `accent.link` light | `#0174bc` | `surface.canvas` | `#f7f7fa` | 4.648:1 | 4.5 | PASS |
| 9 | `accent.link` light | `#0174bc` | `surface.raised` | `#ffffff` | 4.970:1 | 4.5 | PASS |
| 10 | `border.strong` light | `#83838c` | `surface.raised` | `#ffffff` | 3.757:1 | 3.0 | PASS |
| 11 | `border.focus` light | `#0174bc` | `surface.canvas` | `#f7f7fa` | 4.648:1 | 3.0 | PASS |
| 12 | `status.success` text | `#138246` | white (canvas context) | `#ffffff` | 4.873:1 | 4.5 | PASS |
| 13 | `status.success` dot on wash | `#00b050` | `#dff3df` | — | 2.460:1 | 3.0 | FAIL (see note b) |
| 14 | `status.warning` text (ink) | `#343438` | `#ffecbc` wash | — | 10.610:1 | 4.5 | PASS |
| 15 | `status.warning` chip icon | `#3d3d42` | `#fecb34` chip | — | 7.100:1 | 3.0 | PASS |
| 16 | `status.error` glyph | `#d63c42` | `#ffe5e5` wash | — | 3.837:1 | 3.0 | PASS |
| 17 | `status.error` text | `#b82329` | `#ffe5e5` wash | — | 5.314:1 | 4.5 | PASS |
| 18 | `status.info` glyph | `#4067e5` | `#e6edfe` wash | — | 4.175:1 | 3.0 | PASS |
| 19 | `status.info` text | `#3451b2` | `#e6edfe` wash | — | 6.039:1 | 4.5 | PASS |
| 20 | `text.inverse` on chrome | `#d6d6dd` | global header | `#232326` | 10.838:1 | 4.5 | PASS |
| 21 | `text.primary` dark | `#ffffff` | `surface.canvas` dark | `#343438` | 12.394:1 | 4.5 | PASS |
| 22 | `text.primary` dark | `#ffffff` | `surface.raised` dark | `#3d3d42` | 10.799:1 | 4.5 | PASS |
| 23 | `text.secondary` dark | `#a3a3ab` | `surface.canvas` dark | `#343438` | 4.948:1 | 4.5 | PASS |
| 24 | `text.secondary` dark | `#a3a3ab` | `surface.raised` dark | `#3d3d42` | 4.312:1 | 4.5 | FAIL (see note c) |
| 25 | `accent.onAction` dark | `#343438` | `accent.action` dark | `#5bb3ea` | 5.360:1 | 4.5 | PASS |
| 26 | `accent.onAction` dark | `#343438` | hover dark | `#96cff0` | 7.366:1 | 4.5 | PASS |
| 27 | `accent.link` dark | `#7dcdff` | `surface.raised` dark | `#3d3d42` | 6.196:1 | 4.5 | PASS |
| 28 | `border.strong` dark | `#a3a3ab` | `surface.raised` dark | `#3d3d42` | 4.312:1 | 3.0 | PASS |
| 29 | `border.focus` dark | `#5bb3ea` | `surface.canvas` dark | `#343438` | 5.360:1 | 3.0 | PASS |
| 30 | `status.error` dark | `#eb9091` | `surface.raised` dark | `#3d3d42` | 4.593:1 | 3.0 | PASS |
| 31 | `status.warning` dark | `#fecb34` | `surface.canvas` dark | `#343438` | 8.149:1 | 3.0 | PASS |
| 32 | `status.success` dark dot | `#00b050` | `surface.raised` dark | `#3d3d42` | 3.767:1 | 3.0 | PASS |
| 33 | `status.info` dark glyph | `#8da4ef` | `surface.canvas` dark | `#343438` | 5.128:1 | 3.0 | PASS |

Gate notes:
a) The primary button's shipped hover fill `#009cde` drops the white label to 3.084:1 — above the
   3:1 non-text floor but below body-text AA. This is the one computed AA gap inherited from the
   official tokens. Spec remedy: the resting fill `#0174bc` is the default; hover changes are always
   accompanied by the pointer and the pressed state returns to `#0174bc` (4.970:1); labels stay
   600-weight white and are never the sole carrier of state.
b) The green `#00b050` never renders as text or as an icon sitting directly on its tinted wash
   (`#dff3df`): banners set status text in primary ink `#343438` (10.638:1 on the wash) and reserve
   green for the left band, border, and icon chip; success *text* `#138246` is legal only on
   white/canvas contexts (4.873:1).
c) Dark secondary text `#a3a3ab` passes on the dark canvas (4.948:1) but fails on raised panels —
   on `surface.raised` dark, secondary text steps up to `#d6d6dd` (7.468:1). Dark `text.tertiary`
   `#83838c` is confined to canvas-level meta (3.299:1) and never used on raised surfaces (2.875:1).
`text.disabled` (2.342–2.505:1) is confined to genuinely inactive components (SC 1.4.3 exemption).

## 4. Typography

**Families.** UI: **Nunito Sans** — self-hosted woff2, weights 400 regular, 600 semibold, 700 bold,
800 extrabold, fallback generic sans; the product's own stylesheet declares it as the base family.
Numeric/code: **Fira Code** (400, 13px/20px) for identifiers, image/instance IDs, LISH/console
output, and code snippets — monospace is for identifiers and code, never a costume. No display
face exists in the product; the marketing layer's Akamai faces never enter the shell.

**One ramp table per class, not one blended table.**

- **[F] Focused, 16px base** (login, payment/upgrade checkout):

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Display | 26px | 800 | 32px | 0 | default | Auth/checkout headline |
| Heading | 18px | 700 | 24px | 0 | default | Form section titles |
| Body | 16px | 400 | 24px | 0 | default | Form prose, legal |
| Label | 14px | 600 | 16px | 0 | default | Field labels, buttons |
| Meta | 12px | 400 | 16px | 0 | tabular | "billed hourly" helper notes |

- **[S] Standard, 14px base** (resource lists, detail pages, create flows, billing, settings):

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Page title | 24px | 700 | 30px | 0 | default | Route title (20px/26px below 1280px viewports) |
| Section title | 18px | 700 | 24px | 0 | default | Panel headers, drawer/dialog titles |
| Subsection title | 16px | 700 | 20px | 0 | default | Card/panel sub-headers |
| Body | 14px | 400 | 20px | 0 | default | Descriptions, prose, banner text |
| Row primary | 14px | 600 | 16px | 0 | tabular when numeric | Resource labels, side-nav items, table cells (entered text 400) |
| Row secondary | 14px | 400 | 16px | 0 | tabular when numeric | Specs line, dropdown items, pagination |
| Stat value | 26px | 800 | 32px | 0 | tabular-nums | KPI figures, promo banners |
| Stat label | 12px | 800 | 16px | +0.37px, uppercase | default | Overline captions for content blocks |
| Meta | 12px | 400 | 16px | 0 | tabular for timestamps | Created dates, IDs, helper text |
| Field label | 14px | 700 | 16px | 0 | default | Form labels, table headers |

- **[D] Dense, 12–13px base** (LISH/Weblish consoles, event feeds, long log surfaces, firewall
  rule tables, monitoring graphs):

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Grid header | 12px | 700 | 16px | 0 | default | Column headers (icon sizes 12/16/20px states) |
| Grid cell numeric | 13px | 400 | 16px | 0 | tabular-nums | IPs, costs, transfer, counts |
| Grid cell text | 13px | 400 | 16px | 0 | default | Names, tags, regions |
| Log line | 13px | 400 | 20px | 0 | tabular-nums | Fira Code console/log rows |
| Inline help | 12px | 600 | 16px | 0 | default | Warning messages under fields |

Prose inside a dense screen still steps up to 14px Body.

**Invariants.** `tabular-nums` on every comparable value — monthly/hourly cost, IPv4 addresses,
transfer GB, timestamps, counts, resource IDs. Right-align numerics, left-align text, never centre
a numeric column. Fixed stepped sizes; no fluid type. Measure ≤80 characters (SC 1.4.8); 65–80ch
[F/S], unconstrained [D]. Page content column is capped at 1280px wide, centered beside the side
menu.

## 5. Spacing Scale & Density Scales   ← two axes, never one

**Spacing base: 4px grid with a 2px micro-step; 8px comfortable [F/S], 4px [D]** — matching the
official spacing steps (0/2/4/6/8/12/16/20/24/28/32/36/40/48/64/72/96). `space.s0` 0 · `s4` 4px
icon-to-label · `s8` 8px control padding [D] · `s12` 12px cell padding [S] · `s16` 16px card
padding [S] / page gutter · `s24` 24px card padding [F] + section gap · `s32` 32px section gap [S]
· `s48` 48px region separation · `s64–s96` rare. *No `17px`. No `23px`. If a layout needs an
off-scale value, the layout is wrong.*

**Structural constants:** global top bar 56px; side menu 232px pinned / 48px collapsed; content
column max 1280px; buttons 34px tall; table rows 40px; checkboxes/radios and their icons at
16px/20px scales.

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | Login, payment/upgrade checkout |
| `standard` | 40px | 14px | 12–16px | 24px | Resource lists, detail pages, create flows, billing, settings |
| `dense` | 28–32px | 12–13px | 8px | 16px | Consoles (LISH/Weblish), event feeds, logs, firewall rules, monitoring graphs |

- Density comes from **row height, column pruning and leading** — never from type too small to
  read. A 13px tabular IPv4 in a dense firewall table is correct; the same numeral in a checkout
  form is a defect.
- **Never switch mid-page.** Switching across routes with different jobs is legitimate — the create
  flow (S) and the console (D) should feel like different rooms.
- **Chrome follows rows.** Header, toolbar, batch bar and pagination heights always match the
  table's row height — a 40px toolbar over 32px dense rows is a rhythm break.
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40%. *House heuristic — validate
  by screenshot.*

## 6. Radius Scale

`none` 0 — the system default: panels, inputs, buttons, cards, dialogs, tables (verified in the
official token release: default radius 0) · `xs` 2px tag chips, badges, breadcrumbs-collapsed ·
`sm` 3px region-flag images only · `full` 9999px status dots, avatars, circular icon buttons.
**One radius per component family**, never mixed ad-hoc. Nested radii obey
`radius_inner = radius_outer − padding` (a 0-outer card with square children needs nothing; a full
dot inside a square cell stays full).

## 7. Elevation

**Light: flat hairlines for static layers + two authored shadows for floaters; Dark: surface-step
luminance + 1px keylines (same shadow geometry, black-based).** Levels, low → high:

- **0** `surface.canvas` — no shadow, no border.
- **1** card/panel — 1px `border.subtle` (`#d6d6dd` / `#515157`), no shadow (the resting panel).
- **2** sticky header/toolbar/app bar — 1px `border.subtle` +
  `0 2px 8px 0 rgba(58,59,63,0.18)` (dark: `rgba(0,0,0,0.18)`); the inverted variant
  `0 -2px 8px 0 …` serves elements hanging *above* their anchor.
- **3** dropdown/popover/banner — `0 2px 8px 0 rgba(58,59,63,0.18)` + 1px `border.subtle`;
  right/left drawers `-16px 0 32px 0` / `16px 0 32px 0 rgba(61,61,66,0.18)`.
- **4** dialog/modal — `0 16px 32px 0 rgba(58,59,63,0.18), 0 4px 8px 0 rgba(58,59,63,0.08)` + scrim
  (page dimming) `#232326` at 24% light / 84% dark.

Shadow colour is always the neutral gray-blue `rgba(58,59,63,…)`/`rgba(61,61,66,…)` (dark:
pure black) at the authored opacities — never brand blue, never the status hues.

## 8. Motion

`instant` 0ms · `fast` 120ms ease-out (exits [D], menu close, chip removal) · `base` 200ms
ease-in-out (hover fills, icon-colour transitions, [D] entrances — the authored curve observed in
the product's own theme source) · `slow` 400ms cubic-bezier(0.4, 0, 0.2, 1) ([F/S] entrances,
accordion/panel expansion, drawer slide).

- Entrances decelerate, exits accelerate. Symmetric ease-in-out on both directions of a large
  surface is a defect.
- Animate `transform` and `opacity` only — never `width`, `height`, `top`, `left`. Colour/fill
  transitions at 200ms are the sanctioned exception for icon states.
- No bounce on irreversible moments: not on the destroy confirmation, not on an unreserve.
- Progress is honest: provisioning runs a determinate progress affordance whose in-progress line is
  the brand gradient and whose terminal states are `status.success`/`status.error` lines.
- **Reduced motion is a real variant**, not animation-off everywhere: movement → crossfade under
  ~150ms; scaling and panning of large objects are what must be neutralised for vestibular safety
  (the LISH console and drawer slides are the main triggers here).

## 9. Imagery & Art Direction   ← the one licensed saturation moment

- **Brand moment:** the legacy Linode green molecule icon (three-node network glyph) owns the empty
  states and the loading circle animation, and the tricolor brand gradient
  (`270deg, #00b050 0%, #12a594 51%, #009cde 100%`) owns the app-bar top hairline and the
  in-progress progress bar. These are the only saturated brand gestures inside the shell; their
  palette **never leaks into UI tokens** — no gradient fills, no green actions.
- **Iconography:** the product's own line icon set, stroke-based on 16px/20px grids (12px for
  inline states), monochrome in `#3d3d42`/`#ffffff`; hover steps icons to `accent.link`, active to
  `accent.action`. Filled variants only where a stroke cannot carry 12px. Icon-only controls still
  carry a label or tooltip (§10).
- **Photography:** none in product UI.
- **Illustration / 3D:** none in the shell; empty states are icon + title + description + CTA, so
  nothing is invented per screen. Third-party app logos (marketplace/Quick Deploy cards) render in
  native colour inside white cards — this is the sanctioned exception, committed to the card
  surface only.
- **Empty / error art:** the empty landing shows the brand icon in a white circle, a one-line value
  proposition, a single primary CTA, and Getting-Started doc links; illustration never substitutes
  for the recovery CTA.

## 10. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell (global bar + side menu) | S | Light, dark; 232px pinned / 48px collapsed menu | Hover, active route pill, focus ring, beta chips | Tab order, menu groups expand/collapse | "Search Products, IP Addresses, Tags…" |
| Global command search | S | Header search, entity jump list | Focus, results, no-results, recent | Slash focuses, arrows navigate, Enter opens | "Search Products, IP Addresses, Tags…" |
| Data table (resource list) | S/D | Plain, zebra, sortable headers, grouped | Hover, selected, loading skeleton, empty, error, stale | Arrow keys, Enter opens, kebab focus-trap | "IP Address · Assigned Resource · Region · Tags" |
| Filter/search bar | S/D | Text query + label/tag filters | Focus, filled, cleared, no-results | Slash focuses, Esc clears | "Search by label, IP, or tag" |
| Row action menu | S/D | Kebab per row | Focus-trap, Esc closes, disabled items explain | Arrow navigate, Esc | "Edit · Resize · Rebuild · Delete" |
| Status pill | S/D | Dot + neutral label; dot hue by status | Loading, unknown | Focusable with text label | "Running", "Offline", "Provisioning" |
| Tag chip | S | Removable, read-only, +n overflow | Hover reveal remove, focus, error | Backspace removes in editor | "production ×" |
| Drawer (create/reserve/detail) | S | Right side panel, wide/narrow | Open, Esc, focus returns to trigger, price line | Esc closes, focus trap | "Reserve an IP Address — $10/mo." |
| Dialog | S | Confirm destructive, form | Focus-trap, Esc (destructive names the object) | Tab, Esc, Enter | "Unreserve 198.19.44.34 — this action can't be undone." |
| Notification banner | S | Info, warning, success, error, tip, beta | Dismissible, with links, 48px left band | Esc dismisses, links focusable | "Partner Referrals Beta now available — Learn more" |
| Toast | S | Info, warning, success, error | Auto-dismiss, stacked | Focusable, Esc dismisses | "Linode created successfully." |
| Breadcrumb | S | App title + segments, truncation | Hover to link blue, collapsed menu | Tab through segments | "Linodes / Create / One-Click" |
| Plan/region picker | S | Selects with flags, radio rows, upgrade paths | Hover, selected, disabled (unavailable region) explains | Arrow keys move radio | "PL, Krakow (pl-labkrk-2) — $10/mo." |
| Pagination | D/S | Page numbers, per-page, counts | Hover, disabled, current | Tab, Enter | "1–25 of 312" |
| Console (LISH/Weblish/Glish) | D | Full-screen pane, Ctrl+Alt+Del | Connected, disconnected, reconnect | Console focus, send keys | "Send Ctrl+Alt+Del" |
| Event/audit feed row | D | Timestamped entries, entity links | Unread emphasis, empty, error | Tab through entity links | "You resized linode-01 (2 GB → 4 GB)" |
| Member/permission row | S | Role select, remove, grants | Disabled for owner, pending | Role select keyboard-operable | "Owner cannot be removed" |

**Every fetching surface also designs:** loading (skeleton matching final geometry — row-shaped
bars at the real 40px row height, never a centred spinner on a blank page), empty (brand icon +
value line + the CTA that fixes it), error (what happened + "Retry"), offline/stale (a banner names
the data age; cached rows stay visible).

**Contracts this table encodes:** one primary filled CTA per view [F/S] (dense toolbars may run a
primary plus icon actions); every icon-only control carries a label or tooltip; a disabled control
states *why* on focus or hover ("Reserve unavailable — no regions with capacity"); a button never
changes width between idle and loading — reserve the space; destructive confirms quote the exact
object (IP, label, count) in title and body.

## 11. Light / Dark Strategy

- **Posture:** **C dual-parity** — the product ships light, dark, and a system-following preference
  (user choice persisted in account preferences; verified in the open-source theme source, which
  registers `light` and `dark` themes and resolves `system` against the OS preference).
- **Mechanism:** semantic roles remapped per mode; **no role absent in either mode** — the §3 table
  carries authored values for both columns. Dark mode inverts the accent relationship, not the
  palette: fills become light (`#5bb3ea`) and their ink becomes dark (`#343438`).
- **`color-scheme`** set at the root so UA chrome, form controls and scrollbars follow the active
  mode; it repaints UA-provided parts of the canvas only, not the document's own theme.
- **The mode declaration ships in the head before the stylesheet** to prevent a flash of the wrong
  scheme; the running app also tags the body with the active mode for embedded tooling.
- **Dark is authored, not inverted:** its own gray ramp (`#232326 → #343438 → #3d3d42 → #515157`),
  its own border strength (subtle `#515157` ≈ 1.983:1 on canvas dark vs light subtle 1.352:1 —
  dark hairlines are *stronger*, because a delicate 1px line on white reads as invisible on dark),
  and its own scrim (84% vs 24%). `light-dark()` is progressive enhancement only.
- Org-tinting is not offered; a single product identity per account so a theme swap can never move
  geometry. Radii, type sizes and layout are frozen across modes.

## 12. Density-Mode Strategy

- **Default mode per surface class:** Standard for lists/detail/create/billing; Dense for consoles,
  event feeds, logs, firewall rules, monitoring. Boundary: if the route's primary job is *scanning
  many comparable rows*, it is Dense; if it is *deciding and configuring*, it is Standard; if it is
  *authenticating or paying*, it is Focused.
- **Mechanism:** a density switch at the app root rescales row height, cell padding, gutter and
  body size together as one token axis — spacing tokens do not change per screen size. It is a
  property of the route, not a media query.
- **Container queries for reflow:** reflow responds to the container's content box so table panels
  reflow inside the 1280px content column, not to the viewport; size queries fail closed with no
  eligible container (units silently resolve to small-viewport units there), so container units are
  never used where that fallback would be wrong.
- **Style queries** compare computed values, so the density marker must be a registered custom
  property for style-based branching to work.
- **Offer the switch as an accessibility affordance**, not a preference: a denser/roomier control
  on table toolbars serves users with visual field loss (W3C's SC 2.5.8 note endorses a
  layout-density mechanism); the setting persists per user, never per theme.

## 13. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA for measure and leading (SC 1.4.8) on text-dominant panels.
- **Target size:** ≥24×24 CSS px hard minimum (SC 2.5.5's 44×44 is AAA, not AA); 34px buttons and
  40px rows are the design targets, 24px for dense-row kebabs and checkboxes. The spacing exception
  applies: a 24px-diameter circle centred on each target's bounding box must not intersect
  another's. Zoom does not excuse it.
- **Keyboard:** every function operable (SC 2.1.1); focus indicator visible (SC 2.4.7) — a 2px
  `border.focus` ring (light `#0174bc`, dark `#5bb3ea`, both ≥4.6:1), never removed without a
  stronger replacement; the focused row is never entirely hidden by a sticky header or toolbar
  (SC 2.4.11).
- **Contrast:** text ≥4.5:1; UI boundaries and focus indicators ≥3:1 (SC 1.4.11) — computed in §3,
  with the two documented exceptions (rows 7 and 13) and their remedies.
- **Colour independence:** every status pairs the 16px dot with a text label in neutral ink
  ("Running", "Offline"); deltas carry a sign or direction glyph; the amber warning is always paired
  with an icon chip or band so hue alone never signals severity.
- **Motion:** the reduced-motion variant from §8 ships per component (drawer slides, console
  focus, progress fills).
- **Text:** ≤80-character measure, 1.5 leading on body prose, 200% resize without horizontal scroll
  (SC 1.4.8).
- **Semantics:** real button/link/input elements; correct table semantics for resource lists;
  headings matching visual rank (page title → section → subsection); polite live announcements for
  "Linode created" toasts and event-feed updates; busy state on loading regions.
- **Contrast preference:** if `prefers-contrast: more` is honoured, `border.subtle → border.strong`
  and `text.tertiary → text.secondary` in both modes, and the focus ring widens to 3px (values:
  `no-preference`, `more`, `less`, `custom`).

## 14. Anti-Patterns

**Do** —
1. Keep the whole list row clickable with a hover wash at `surface.hover`; the kebab is the
   secondary path — the ledger stays scannable.
2. Render every IP, cost, transfer and timestamp in tabular numerals, right-aligned: the product's
   contract is precise infrastructure accounting.
3. Pair every status with a neutral-ink label + 16px dot; colour alone never carries state.
4. Name the object in every destructive confirm ("Unreserve 198.19.44.34 — this action can't be
   undone") before enabling the action.
5. Use drawers for create/reserve flows with a visible price line; the user should see what a thing
   costs before it is provisioned.
6. Keep toolbar, header and pagination heights equal to the table's 40px row height.
7. Reserve button width through the loading state; show progress inside the control.
8. Render regions as flag + "City, Country" ("US, East Wenatchee, US") everywhere a region is named.
9. Keep the global command search one keystroke away; it is the shell's connective tissue.
10. Use Fira Code only for identifiers, console output and code; Nunito Sans everywhere else.
11. Keep the brand gradient confined to the app-bar hairline and the in-progress bar.
12. Offer the density switch on heavy table surfaces as an accessibility affordance.

**Don't** —
1. Don't resurrect the legacy Linode green as an action colour — `#0174bc`/`#5bb3ea` is the action
   contract; green means "running" or the brand icon, nothing else.
2. Don't round corners: a 6px button inside this system reads as a different product. Chips (2px),
   flags (3px) and full circles are the only rounding.
3. Don't fill anything with the brand gradient, and don't tint panels with status hues.
4. Don't set text in amber `#fecb34` — on white it is 1.521:1; warnings use ink text on the amber
   wash or an amber chip with dark icon.
5. Don't colour status text in its own hue on tinted washes (green-on-green is 2.460:1); banners
   use primary ink.
6. Don't stack two filled primaries in one view; secondary actions are outline or text.
7. Don't replace drawer flows with modal chains — modals are for confirmations only.
8. Don't ship hover-only affordances; every hover state has a focus twin at `border.focus`.
9. Don't use placeholder text as the field label; the product labels fields in 700-weight ink.
10. Don't show a whole-page spinner; skeletons match the final 40px row geometry.
11. Don't fire native alert/confirm for destructive flows; the quoted-object dialog is the pattern.
12. Don't shrink type below 12px (13px body in dense cells) to cram columns — prune columns, not
    legibility; and don't leave a disabled primary silent — it explains on focus.
13. Don't darken `text.secondary` on dark raised panels by hand — step to `#d6d6dd` (the authored
    remedy), never to a raw value.

## 15. Quick Reference & Verification Gate

**Colour (role → hex, light / dark):** canvas `#f7f7fa`/`#343438` · raised `#ffffff`/`#3d3d42` ·
overlay `#ffffff`/`#3d3d42` · inset `#ededf2`/`#515157` · hover `#edf8ff`/`#47474d` · selected
`#ceedfe`/`#515157` · border.subtle `#d6d6dd`/`#515157` · border.strong `#83838c`/`#a3a3ab` ·
border.focus `#0174bc`/`#5bb3ea` · accent.action `#0174bc`/`#5bb3ea` · onAction
`#ffffff`/`#343438` · accent.subtle `#edf8ff`/`#47474d` · accent.link `#0174bc`/`#7dcdff` ·
text.primary `#343438`/`#ffffff` · text.secondary `#696970`/`#a3a3ab` · text.tertiary
`#83838c`/`#83838c` · text.disabled `#a3a3ab`/`#83838c` · text.inverse `#d6d6dd` both · global
chrome `#232326` both · success dot `#00b050` (text `#138246` light) · warning band `#fecb34` ·
error glyph `#d63c42` (text `#b82329` light, `#eb9091` dark) · info `#4067e5` (dark glyph
`#8da4ef`) · washes `#dff3df`/`#ffecbc`/`#ffe5e5`/`#e6edfe`.

**Type ramp:** Nunito Sans 400/600/700/800 self-hosted; Fira Code 400 for code/identifiers.
[F] 26/32 · 18/24 · 16/24 · 14/16 · 12/16. [S] 24/30 title · 18/24 section · 16/20 subsection ·
14/20 body · 14/16 row · 26/32 stat (tabular) · 12/16 overline (uppercase, +0.37px) · 14/16 field
label · 12/16 meta. [D] 12/16 grid header · 13/16 cells (tabular numerics) · 13/20 mono log ·
12/16 inline help.

**Spacing + radius:** 4px base grid, steps 0/2/4/6/8/12/16/20/24/28/32/36/40/48/64/72/96; [F] pad
24 gutter 32 · [S] pad 16 gutter 24 · [D] pad 8 gutter 16; top bar 56px, side menu 232/48px,
content ≤1280px, buttons 34px, rows 40px. Radius 0 default · 2px chips · 3px flags · full dots.

**Component → token map:** data table → `surface.raised` rows on `surface.canvas`, zebra at canvas
tone, filled header `surface.inset` + `text.primary`, hover `surface.hover`, sort icons
`text.secondary→accent.link` · primary button → `accent.action` + `accent.onAction`, radius 0 ·
side nav → canvas `surface.canvas`/`#343438`, selected wash `surface.selected`, selected pill
`accent.action` + white · drawer/dialog → `surface.raised`, level 3/4 shadow, scrim `#232326`
24%/84% · banner → `status.*` wash + band + icon chip, text `text.primary` · status pill →
`text.secondary` label + 16px `status.*` dot · tag chip → `#f7f7fa` fill, `border.strong` frame,
`text.primary` text, hover `#edf8ff` · link → `accent.link`, hover to `#009cde`/`#96cff0`.

**Agent prompt block.** Build Akamai Cloud Manager surfaces with these roles only:
surface.canvas `#f7f7fa`/`#343438`, surface.raised `#ffffff`/`#3d3d42`, surface.inset
`#ededf2`/`#515157`, surface.hover `#edf8ff`/`#47474d`, surface.selected `#ceedfe`/`#515157`,
border.subtle `#d6d6dd`/`#515157`, border.strong `#83838c`/`#a3a3ab`, border.focus
`#0174bc`/`#5bb3ea`, accent.action `#0174bc`/`#5bb3ea` (onAction `#ffffff`/`#343438`),
accent.link `#0174bc`/`#7dcdff`, text.primary `#343438`/`#ffffff`, text.secondary
`#696970`/`#a3a3ab` (dark raised → `#d6d6dd`), global chrome `#232326` with `#d6d6dd` text.
Status: success dot `#00b050` text `#138246` (white only) wash `#dff3df`; warning band `#fecb34`
wash `#ffecbc` ink text; error glyph `#d63c42` text `#b82329`/`#eb9091` wash `#ffe5e5`; info
`#4067e5` text `#3451b2` wash `#e6edfe` (dark glyph `#8da4ef`). Type: Nunito Sans 400/600/700/800,
Fira Code for code/IDs; Standard 14px base, Dense 13px, page title 24/30 (20/26 under 1280px).
Spacing 4px grid (pad 16 [S], 8 [D]; gutters 24/16); radius 0 everywhere except 2px chips/3px
flags/full dots; rows 40px [S] / 28–32px [D]; chrome matches row height; buttons 34px; shadows
`0 2px 8px rgba(58,59,63,0.18)` floaters, `0 16px 32px rgba(58,59,63,0.18), 0 4px 8px
rgba(58,59,63,0.08)` dialogs; scrim `#232326` 24%/84%; motion 120/200/400ms, transform/opacity
only, decelerate entrances.

**Example component prompts.**
1. *Resource list (Linodes / Reserved IPs) [Standard]* — `surface.canvas` ground with the content
   column ≤1280px; title row 24/30 `text.primary` + one `accent.action` filled CTA at 34px;
   table header band `surface.inset` with 14/700 `text.primary` column caps; 40px rows on
   `surface.raised` with zebra stripes at the canvas tone; name cell `text.primary` 14/600 +
   region "flag + City, Country" and specs in `text.secondary`; IPs right-aligned tabular;
   status = `#00b050` dot + "Running" in `text.secondary`; tag chips 2px radius pale-blue; row
   hover `surface.hover`; kebab opens a focus-trapped menu; skeleton rows match 40px geometry
   while loading; empty state = brand icon + value line + primary CTA.
2. *Reserve drawer [Standard]* — right side panel on `surface.raised`, 1px `border.subtle`, level-3
   drawer shadow, radius 0; title 18/24 `text.primary` with a 20px close icon; fields with
   `border.strong` frames (hover `#3d3d42`, focus `border.focus`), labels 14/700, hints
   `text.secondary`; region row shows flag + "PL, Krakow (pl-labkrk-2)"; price line "$10 / mo." in
   tabular numerals; footer = `accent.link` Cancel + one `accent.action` fill; Esc closes, focus
   returns to the trigger.
3. *Destructive dialog [Standard]* — `surface.raised`, radius 0, level-4 shadow + `#232326` 24%
   scrim; title "Unreserve 198.19.44.34" 18/700 in `text.primary`; body names the consequence and
   the irreversibility in 14/400 `text.secondary`; footer `accent.link` Cancel + `accent.action`
   Unreserve; for destroys, the confirm fills the danger tone `#b82329` with white ink only when
   the typed label matches; Esc closes, focus returns to the row.

**Pre-ship checklist.** 1 Zero raw hex outside L1. 2 No token resolves to a component name.
3 Every contrast pairing computed, passing, unrounded (documented exceptions 7/13 carry their
remedies). 4 Every semantic role has a value in every shipped mode (light, dark, system). 5 Every
fetching surface has loading/empty/error/offline specified. 6 Every component row lists disabled
and loading states. 7 Row, header, toolbar and pagination heights agree. 8 Reduced-motion variant
written for every authored motion. 9 Every control keyboard-reachable with a visible focus
indicator. 10 Dark authored, not filtered, with border strength exceeding light's (subtle 1.983 vs
1.352; strong 4.312 vs 3.757). 11 No unoverridden stock library default inside a committed surface.
12 Nothing came from a marketing page. 13 The §9 brand-moment palette (Linode molecule green, the
tricolor gradient) appears nowhere in the UI token layers.
