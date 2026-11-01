# Design System — MongoDB Atlas

<!-- premium-web-design:design-system 1 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: MongoDB LeafyGreen UI kit (token sources: palette ramps, type scale, spacing, radius, shadows, focus rings — ladder rung 2, github.com/mongodb/leafygreen-ui packages/palette + packages/tokens), MongoDB brand pages + marketing site (colour, shell, display type — rung 2), Atlas console / docs / pricing captures in screens/ (surface grounding, pixel sampling — rung 3). Rung 1 (sibling catalogs) had no mongodb-atlas spec. -->
<!-- Surface classes: 12 routes classified; density classes [S/D] assigned, [F] reserved for auth and checkout -->
<!-- Palette provenance: every L1 hex below is the published LeafyGreen palette value; #FDFFF5 marketing ivory and #00684A console primary verified by pixel-sampling screens/product.png and screens/dashboard.png -->

## 1. Design Posture & Atmosphere

Atlas is a control tower for data infrastructure. The console surface is a quiet, white
operations ledger: ink `#001E2B` on `#FFFFFF`, hairline-separated cards, one dark-green filled
action per view, and page titles set in a serif that lends editorial gravity to what is
otherwise an instrument panel. The marketing surface is its stage twin — near-black navy
`#001E2B` canvases, neon `#00ED64` accents, condensed uppercase display type — used to sell the
same machine the console lets you operate. After eight hours in the console the palette never
shouts: warning yellow appears as a banner, metric tiles tick with tabular numerals, and the
eye settles on exactly one saturated element per screen.

The product sits against its category's defaults by being *typographically confident and
chromatically strict*. Where peer consoles drown users in grey-on-grey, Atlas keeps a real ink
colour, a real serif, and a two-regime green system: neon `#00ED64` exists only on dark or for
brand moments, while the light console's primary actions are the deep `#00684A`. Density is
moderate standard (13px body, 40–44px rows) that drops to a true dense mode (12–13px, 28–32px
rows) inside collections browsing and metrics — a different room, not a squeezed page.

The single visual metaphor: **an instrument panel with a maître d'** — dense read-only telemetry
presented through warm, unambiguous human copy ("You can deploy only one Free cluster per Atlas
project"), serif headlines, and a strict escort of one primary action per view.

**Key Characteristics**

- Dark canvas is `#001E2B` — LeafyGreen's literal "black"; pure `#000000` appears only inside
  dark-mode shadows, never as a surface.
- Two green regimes, never mixed: `#00ED64` on dark/brand surfaces, `#00684A` for every filled
  primary in the light console. White-on-`#00ED64` is banned (1.579:1 — computed in §3).
- Accent budget: exactly one filled primary per viewport in [S]; dense toolbars may add icon
  actions but no second fill. Red text-buttons are reserved for terminal operations.
- Rows are 40–44px [S]; sidebar items 32px; dense grids 28–32px. Body base is 13px (LeafyGreen
  body1 13/20) — a compact standard, not a shrunken one.
- Page titles in MongoDB Value Serif (~28px); everything functional in Euclid Circular A;
  Source Code Pro reserved for connection strings, identifiers, and code.
- Status is never colour alone: every state pairs a wash (`#E3FCF7` family) with a dark
  foreground (`#00684A` family) and a glyph.
- Light mode owns shadows (3-step ramp); dark mode replaces them with surface steps
  (`#001E2B → #112733 → #1C2D38`) plus 1px keylines.
- Spacing rides a 4px grid with 17 named steps (1–1800 scale); no off-scale values.
- Radius families: 6px controls, 8px cards, 12px overlays, 24px marketing panels, full pills.
- Focus is a two-step ring: 2px canvas gap then 4px `#016BF8` (light) / `#0498EC` (dark).
- Motion budget 100/150/300/500ms; entrances decelerate, exits accelerate.
- The marketing body uses a warm mint-ivory `#FDFFF5` (sampled), never plain white, so light
  marketing sections read as a different room from the white console.
- Yellow `#FFC010` is an attention instrument — warning accents and tutorial highlights — not a
  decorative colour.
- Lowercase mono eyebrow labels (`MONGODB ATLAS`, `RECOMMENDED`) in green or dark-navy mark
  brand sections on both polarities.

## 2. Token Architecture   ← normative

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value*: `gray.dark2`, `green.base`, `space.300`,
  `radius.150`. Referenced only by L2. Banned: component-flavoured naming (`card-bg`,
  `tooltip-color`) — one value, many roles.
- **L2 Semantic** — role names (`surface.canvas`, `text.primary`, `accent.action`). The only
  layer a component may consume. Every semantic role exists in **both** shipped modes.
- **L3 Component** — only for deliberate deviation; points at L2 or L1, never a raw value, never
  a sibling component's token. Example: the cluster-card metric tile maps
  `sparkline.positive → status.success.foreground` and `sparkline.negative → a dedicated amber`,
  rather than inventing new hexes.

**Rules.** Every token has a determinable type (`color`, `dimension`, `duration`, `fontFamily`,
`shadow`) or it is invalid; names are case-sensitive and free of `$`, `{`, `}`, `.`; circular
references (`accent.action → accent.subtle → accent.action`) are errors. Every semantic token has
a value in **every** shipped mode — Atlas ships light and dark console themes plus the fixed
marketing theme; a role with no dark value would resolve to its light value and fail contrast.
Animatable tokens (e.g. an animatable ring width) are registered with both `syntax` and
`inherits`, and `initial-value` must be computationally independent — no `%` or `em`.

**Layer order (low → high)** `reset → primitives → semantic → components → utilities`.
Layer order beats specificity entirely and unlayered normal declarations outrank layered ones,
so a stray un-layered rule in a component file would beat this whole system; anything a consumer
must override without `!important` (the per-org accent inside shared embeds) sits in the top
layer.

**Mode mechanics.** Mode (light/dark) and density are attributes on the application root;
semantic remapping happens there. The marketing theme is *not* a third mode — it is a frozen
org-tinted variant that changes colour tokens only (ivory canvas, condensed display) and leaves
radii, type sizes, and layout frozen so a theme swap cannot move anything (see §10, §11).

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` / `raised` / `overlay` / `inset` | `#FFFFFF` · `#FFFFFF` · `#FFFFFF` · `#F9FBFA` | `#001E2B` · `#112733` · `#1C2D38` · `#112733` | canvas · cards & cluster tiles · dialogs & menus · sidebar, wells; docs shell uses `#001E2B` canvas with `#112733` sidebar |
| `surface.hover` / `surface.selected` | `#E8EDEB` / `#E3FCF7` | `#1C2D38` / `#023430` | Interaction fills; selected sidebar item pairs `#E3FCF7` with `#00684A` text |
| `border.subtle` / `strong` / `focus` | `#E8EDEB` / `#3D4F58` / `#016BF8` | `#3D4F58` / `#5C6C75` / `#0498EC` | 1px hairlines; `subtle` is decorative only in light — real boundaries use `strong`; `focus` ≥3:1 (4.709 / 5.495) |
| `accent.action` / `onAction` / `subtle` | `#00684A` console · `#00ED64` dark-brand / `#FFFFFF` · `#001E2B` / `#E3FCF7` | `#00ED64` / `#001E2B` / `#023430` | Accent budget: 1 filled primary per viewport; onAction swaps per action fill |
| `text.primary` / `secondary` / `tertiary` / `disabled` | `#001E2B` · `#5C6C75` · `#889397` · `#889397` | `#E8EDEB` · `#C1C7C6` · `#889397` · `#5C6C75` | Ink ramp; disabled pairs with `#E8EDEB`/`#1C2D38` fills and is inactive-component exempt |
| `link` | `#016BF8` | `#0498EC` | Underline on hover; never recoloured inside status washes |
| `status.success` / `warning` / `error` / `info` | `#00684A` on `#E3FCF7` / `#944F01` on `#FEF7DB` / `#970606` on `#FFEAE5` / `#1254B7` on `#E1F7FF` | `#C0FAE6` on `#023430` / `#FFC010` on `#4C2100` / `#FF6960` on `#5B0000` / `#C3E7FE` on `#0C2657` | Each ships a glyph — never colour alone; error glyph `#DB3030` (light) / `#FF6960` (dark) |
| Marketing canvas (`org-tinted`) | `#FDFFF5` body · `#001E2B` hero | — | Frozen marketing theme; ink `#001E2B`, single-mode by design |

Dark canvas is **not** pure black: `#001E2B` canvas through `#1C2D38` overlays — a 3-step ramp.
Depth in dark comes from surface steps and 1px strokes, never shadows (the L1 shadow token is
explicitly transparent in dark).

**Contrast gate — computed 2026-11-01, unrounded; 4.499:1 fails. Large text is ≥24px or
≥18.5px bold. Body ≥4.5:1; UI boundaries and focus indicators ≥3:1.**

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| `text.primary` | `#001E2B` | `surface.canvas` | `#FFFFFF` | 17.205:1 | 4.5 | PASS |
| `text.primary` (marketing ink) | `#001E2B` | ivory canvas | `#FDFFF5` | 17.040:1 | 4.5 | PASS |
| `text.secondary` | `#5C6C75` | `#FFFFFF` | `#FFFFFF` | 5.445:1 | 4.5 | PASS |
| `text.tertiary` | `#889397` | `#FFFFFF` | `#FFFFFF` | 3.150:1 | 3.0 muted floor (house; not body) | PASS — restricted to ≥12px meta/uppercase labels; fails body, never used for body |
| `accent.onAction` (brand) | `#001E2B` | `accent.action` | `#00ED64` | 10.894:1 | 4.5 | PASS |
| `accent.onAction` (console) | `#FFFFFF` | `accent.action` | `#00684A` | 6.820:1 | 4.5 | PASS |
| `border.strong` | `#3D4F58` | `surface.raised` | `#FFFFFF` | 8.544:1 | 3.0 | PASS |
| `border.focus` | `#016BF8` | `#FFFFFF` | `#FFFFFF` | 4.709:1 | 3.0 | PASS |
| `link` | `#016BF8` | `#FFFFFF` | `#FFFFFF` | 4.709:1 | 4.5 | PASS |
| `status.success` text | `#00684A` | wash | `#E3FCF7` | 6.344:1 | 4.5 | PASS |
| `status.warning` text | `#944F01` | wash | `#FEF7DB` | 5.785:1 | 4.5 | PASS |
| `status.error` text | `#970606` | wash | `#FFEAE5` | 7.742:1 | 4.5 | PASS |
| `status.error` glyph (non-text) | `#DB3030` | `#FFFFFF` | `#FFFFFF` | 4.690:1 | 3.0 | PASS |
| `status.info` text | `#1254B7` | wash | `#E1F7FF` | 6.364:1 | 4.5 | PASS |
| `text.primary` (dark) | `#E8EDEB` | `#001E2B` | `#001E2B` | 14.538:1 | 4.5 | PASS |
| `text.secondary` (dark) | `#C1C7C6` | `#001E2B` | `#001E2B` | 10.038:1 | 4.5 | PASS |
| `text.tertiary` (dark) | `#889397` | `#001E2B` | `#001E2B` | 5.462:1 | 4.5 | PASS |
| `link` (dark) | `#0498EC` | `#001E2B` | `#001E2B` | 5.495:1 | 4.5 | PASS |
| `status.error` text (dark) | `#FF6960` | wash | `#5B0000` | 5.150:1 | 4.5 | PASS |
| `accent.onAction` (dark) | `#001E2B` | `#00ED64` | `#00ED64` | 10.894:1 | 4.5 | PASS |
| `text.tertiary` on inset | `#3D4F58` | `#F9FBFA` | `#F9FBFA` | 8.222:1 | 4.5 | PASS |
| BANNED pairing (documented) | `#FFFFFF` | `#00ED64` | `#00ED64` | 1.579:1 | 4.5 | FAIL — `accent.action #00ED64` always takes `#001E2B` ink |
| Disabled (inactive exemption) | `#889397` | `#E8EDEB` | `#E8EDEB` | 2.661:1 | exempt (inactive component) | PASS-BY-EXEMPTION — disabled controls also state the reason in text on focus/hover |

## 4. Typography

**Families.** UI **Euclid Circular A** (400 regular, 500 medium, 600 semibold; self-hosted,
preloaded; fallback Helvetica Neue, Helvetica, Arial, sans-serif). Display **MongoDB Value
Serif** (400/600) for console page titles, marketing headlines, and the logotype. Numeric/code
**Source Code Pro** (400/500; fallback Menlo, monospace) for connection strings, cluster IDs,
hashes, raw timestamps, and code blocks. *Monospace is for identifiers and code, never a
costume.* Marketing display adds **MongoDB Value Sans Bold Condensed** — uppercase condensed
hero lines on dark canvases only, never inside the console.

**One ramp table per class, not one blended table.** Columns: role, size, weight, line height,
tracking, numerals, use.

- **[S] Standard — console default, 13px base (LeafyGreen body1):**

  | Role | Size | Weight | Line height | Tracking | Numerals | Use |
  |---|---|---|---|---|---|---|
  | Page title | 28px | 400 | 34px | −0.01em | — | Value Serif; "Database Deployments" |
  | Section title | 16px | 600 | 24px | 0 | — | Card and panel headings |
  | Body (1.5) | 13px | 400 | 20px | 0 | — | Descriptions, banner copy |
  | Row primary | 13px | 500 | 20px | 0 | — | Table/list primary cells, cluster names |
  | Row secondary | 13px | 400 | 20px | 0 | — | Secondary cells, `text.secondary` |
  | Stat value | 13px | 500 | 20px | 0 | tabular-nums | Connections, Data Size, ops counts |
  | Stat label | 11px | 600 | 16px | +0.04em uppercase | — | Tile labels ("DATA SIZE") |
  | Meta | 12px | 400 | 20px | 0 | — | Timestamps, "Last 16 minutes" |

- **[D] Dense — collections browser, metrics tables, logs, 12–13px base:**

  | Role | Size | Weight | Line height | Tracking | Numerals | Use |
  |---|---|---|---|---|---|---|
  | Grid header | 12px | 600 | 16px | +0.02em uppercase | — | Column headers |
  | Grid cell text | 13px | 400 | 20px | 0 | — | Document field values |
  | Grid cell numeric | 13px | 400 | 20px | 0 | tabular-nums, right-aligned | Index sizes, counts |
  | Log line | 13px | 400 | 20px | 0 | tabular-nums | Source Code Pro |
  | Inline help | 12px | 400 | 20px | 0 | — | Hints under inputs |

  *Prose inside a dense screen still steps up to 13px/20px body — dense never means unreadable.*

- **[F] Focused — auth, account signup, checkout, 16px base:**

  | Role | Size | Weight | Line height | Tracking | Numerals | Use |
  |---|---|---|---|---|---|---|
  | Display | 36px | 600 | 44px | −0.01em | — | Value Serif; "Start for Free" |
  | Heading | 22px | 600 | 30px | 0 | — | Form section headings |
  | Body | 16px | 400 | 28px | 0 | — | LeafyGreen body2 |
  | Label | 14px | 500 | 20px | 0 | — | Input labels (always above, never placeholder-as-label) |
  | Meta | 12px | 400 | 20px | 0 | — | Legal, disclaimer (LeafyGreen disclaimer) |

**Invariants.** `tabular-nums` on every comparable value — hourly prices ("$0.011/hour"), data
sizes ("0.0 B / 512.0 MB"), connections ("12.0"), timestamps, counts, IDs. Right-align numerics,
left-align text, never centre a numeric column. Fixed stepped sizes; no fluid `clamp()` between
steps. Measure ≤80 characters — 65–80ch for [F/S] prose; unconstrained inside [D] tables.

## 5. Spacing Scale & Density Scales   ← two axes, never one

**Spacing base: 4px grid; 8px comfortable [F/S], 4px [D].** The named steps (LeafyGreen spacing
scale) are: `space.0` 0 · `25` 1px hairline nudges · `50` 2px · `100` 4px icon-to-label ·
`150` 6px · `200` 8px control padding [D] · `300` 12px cell padding [S] · `400` 16px card
padding [S] / page gutter [D] · `500` 20px · `600` 24px card padding [F] + section gap ·
`800` 32px section gap [S] · `900` 36px · `1000` 40px toolbar inset · `1200` 48px region
separation · `1400` 56px top-bar height · `1600` 64px rarely · `1800` 72px marketing regions.
*No `17px`. No `23px`. If a layout needs an off-scale value, the layout is wrong.*

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | Auth, signup, billing checkout |
| `standard` | 40–44px | 13px | 12–16px | 24px | Project home, Database Deployments, settings |
| `dense` | 28–32px | 12–13px | 8px | 16px | Collections browser, metrics tables, logs, activity feed |

- Density comes from **row height, column pruning and leading** — never from type too small to
  read. A 13px tabular numeral in a dense metrics table is correct; the same numeral dropped to
  11px to fit is a defect.
- **Never switch mid-page.** The Database Deployments page is standard end-to-end; opening the
  collections browser swaps to dense as a distinct surface. "Avoid changing information density
  within a single page, otherwise your app can feel disjointed" (shopify.dev, *Layout*).
- **Chrome follows rows.** Console top bars (56px) and card toolbars (40–44px) match the row
  height of the content they govern; a 40px toolbar over 32px dense rows is a rhythm break.
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40%. *House heuristic —
  validated against screens/dashboard.png (console ≈48% on standard) and screens/product.png.*

## 6. Radius Scale

`none` 0 · `xs` 2px mono code chips, inline code tags (`M0`) · `sm` 4px dense inputs, tags ·
`md` 6px buttons, inputs, select controls, table rows · `lg` 8px cards, cluster tiles, metric
tiles · `xl` 12px dialogs, popovers, menus · `2xl` 24px marketing panels and hero cards ·
`full` 9999px pills (FREE/SHARED badges, avatars, icon buttons, announcement chips). Marketing
heroes additionally use oversized 24–64px scalloped bottom corners on dark bands — a brand
shape, banned inside the console. **One radius per component family**, never mixed ad-hoc.
Nested radii obey `radius_inner = radius_outer − padding` (a 12px dialog containing an 8px
inset panel leaves 4px padding).

## 7. Elevation

**Choose one strategy, never mix paradigms.** Light: multi-layer ambient shadows. Dark:
surface-luminance steps + 1px keylines, with the L1 shadow explicitly transparent. Published
ramp (LeafyGreen shadows, ink `#001E2B`):

- **0** canvas — no shadow, both modes.
- **1** card/panel — light `0 2px 4px 1px rgba(0,30,43,0.15)`; dark none, one surface step up
  (`#001E2B → #112733`) + `border.subtle`.
- **2** sticky header/toolbar, hover-raised cards — light `0 18px 18px -15px rgba(0,30,43,0.2)`;
  dark `0 18px 18px -15px rgba(0,0,0,0.45)` + `border.strong`.
- **3** overlay (menus, popovers) — light `0 8px 20px -8px rgba(0,30,43,0.6)`, `radius.xl`;
  dark `0 8px 20px -8px rgba(0,0,0,0.6)` + `border.strong`.
- **4** dialog — level-3 shadow + 32% black scrim (`rgba(0,30,43,0.32)` equivalent); the Connect
  and IP-Access-List dialogs sit here.
- **overflow** — `0 2px 4px 1px rgba(92,108,117,0.3)` for scroll shadows on inner containers.

## 8. Motion

`instant` 0ms · `fast` 100ms ease-out (hover tints, tooltip exits, [D] exits) · `base` 150ms
decelerate (default; [D] entrances, banner slide-ins) · `slow` 300ms decelerate ([F/S]
entrances, dialogs, drawers) · `slowest` 500ms decelerate (full-page view transitions only).

- Entrances decelerate, exits accelerate. Symmetric ease-in-out on both directions is a defect.
- Animate `transform` and `opacity` only — never `width`, `height`, `top`, `left`. Sparklines
  interpolate path data at 150ms; the yellow tutorial highlight fades at `fast`.
- No bounce on irreversible moments: cluster termination, user deletion, IP-access-list removal.
  Confirmation dialogs scale in at `slow`, dismiss at `fast`.
- **Reduced motion is a real variant, not `animation: none` everywhere:** movement → crossfade
  under ~150ms. Targets vestibular triggers specifically — scaling and panning of large objects
  (full-page transitions, hero marquees on marketing) must be neutralised; small fades may stay.

## 9. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell/sidebar | S/D | Collapsed, expanded | Default, hover, active (`#E3FCF7`+`#00684A`), disabled count badge | Tab through groups; arrow keys inside nav | Section eyebrows "SERVICES", "SECURITY" |
| Top bar & switcher | S | Org, project scope | Default, open menu, loading orgs | Tab; Enter opens; Esc closes | "Sonali's Org" / project name |
| Cluster card | S | Free, Shared, Dedicated, Infinite | Running (green dot), pending (spinner), terminated, error | Card focus ring; Enter opens actions | "Cluster0" + FREE/SHARED pills |
| Data table | D | Collections, indexes | Loading skeleton, empty, error, row hover/selected | Arrow keys, Enter, Space select | "Browse Collections" |
| Filter/search bar | S/D | Deployments search, query bar | Empty, filled, invalid syntax, results count | Focus, Esc clears | "Find a database deployment…" |
| Row action menu | S/D | Inline `…` overflow | Focus-trap on open; Esc closes; arrow navigation | Full keyboard | "Connect", "View Monitoring", "Browse Collections" |
| Stat tile | S/D | With sparkline, bare | Live (150ms tick), stale (grey + "Last 16 minutes"), no-data | Tab to tile; tooltip on focus | "Connections 12.0" tabular |
| Drawer/inspector | S | Right drawer, bottom sheet | Open, closing, resized | Esc closes; focus returns to trigger | "Connect to Cluster0" |
| Dialog | F | Confirm, form (IP entry) | Open, submitting, error inline, disabled submit | Focus trap, Esc cancels, Enter submits | "Add IP Access List Entry" / "Confirm" |
| Stepper wizard | S | 3-step connect flow | Current, complete (green check), error, disabled future | Arrow between steps | "Set up connection security" |
| Plan/tier control | S | M0→M10 tier picker, Atlas Core tabs | Confirming, prorating, blocked (downgrade limits) | Radio semantics; arrows | "Free forever" / "Starts at $56.94/month" — names cost + effective date |
| Member row | S | Org users list | Inviting, active, pending, revoked | Row actions via menu key | "Invite to Organization" |
| Audit entry | D | Activity feed lines | Expanded, collapsed | Enter expands | Actor + verb + target + timestamp |
| Command palette ("Goto") | S | Global launcher | Closed, open, no results | Global hotkey, Esc | "Goto" — jump to any project resource |
| Notification banner | S | Warning (yellow), info (blue), success (green) | Persistent, dismissible ("Do not show me again") | Dismiss is a real button | "Current IP Address not added. You will not be able to connect…" |

**Every fetching surface also designs:** loading (skeleton matching final geometry — cluster
card skeletons mirror the real card's 8px radius and hairline, never a centred spinner on a
blank page); empty (what's missing + the CTA that fixes it — "Add an IP address / Configure
which IP addresses can access your cluster / [Add IP Address]"); error (what happened + retry
path, inline in the card); offline/stale (metric tiles pin the last value with a grey tint and
the fetch timestamp instead of zeroing).

**Contracts this table encodes:** one primary filled CTA per view [F/S] (dense toolbars may run
a primary plus icon actions); every icon-only control carries a label or tooltip; a disabled
control states *why* on focus or hover rather than sitting silently dead; a button never changes
width between idle and loading — reserve the space; destructive red is a text-button, and
cluster termination additionally requires typing the cluster name.

## 10. Light / Dark Strategy

- **Posture: C dual-parity.** The Atlas console ships light and dark (LeafyGreen `Mode.Light` /
  `Mode.Dark` token sets, light default); the docs shell and marketing site are dark-first.
  Every semantic role has a value in both console modes; the marketing ivory canvas is a frozen
  org-tinted variant, not a third mode.
- **Mechanism:** semantic roles remapped per mode at the application root; no role absent in
  either mode. Single-mode roles: marketing display constants (condensed display family, ivory
  canvas) are pinned to the marketing theme and never render inside the console.
- **`color-scheme`** set on the root so UA chrome, form controls and scrollbars follow the
  active console mode. It "repaints UA-provided parts of the canvas… does not affect the default
  color scheme for the overall document".
- **A `color-scheme` meta in the head before the stylesheet**, to prevent a flash of the wrong
  scheme on docs and marketing (both dark) and in dark-console sessions.
- **Dark is authored, not inverted:** its own surface ramp (`#001E2B → #112733 → #1C2D38`), its
  own border strength — *higher* than light (`subtle` is `#3D4F58` on dark vs `#E8EDEB` on
  light, because a hairline that reads as delicate on white disappears on near-black) — and its
  own shadow policy (L1 transparent). Status flips to light-foreground-on-dark-wash
  (`#C0FAE6` on `#023430`, 11.753:1). `light-dark()` is progressive enhancement only; the
  explicit remap table is the source of truth.
- Org-tinting (marketing ivory) changes colour tokens only; radii, type sizes and layout are
  frozen so a theme swap cannot move anything.

## 11. Density-Mode Strategy

- **Default mode per surface class:** console project pages standard (≥2 parallel information
  needs, 40–44px rows); collections browser, metrics, logs, activity feed dense (scan-and-compare
  jobs, 28–32px rows); auth and billing checkout focused (single task, 16px body). The boundary
  is the page's job, not the viewport.
- **Mechanism:** a density attribute on the application root rescales row height, cell padding,
  gutter and body size together via the token axis. Carbon's spacing tokens "do not change
  values based on the screen size" (shadcn/ui, *Theming*) — density is a **token axis, not a
  media query**.
- **Container queries for reflow:** container queries are Baseline widely available and measure
  the *content box*, so the cluster card reflows (metrics 5-across → 2-across) to its container,
  not the viewport. Size queries fail closed with no eligible container, and `cq*` units
  silently resolve to small-viewport units there — `cq*` units are never used where that
  fallback would be wrong.
- **Style queries** comparing computed values require the density marker to be a registered
  custom property with `syntax` and `inherits`.
- **Offer the switch as an accessibility affordance**, not a preference: W3C's note on SC 2.5.8
  endorses "a mechanism to control the density of layout," naming users with visual field loss.
  Atlas exposes density in display preferences; persistence is per-user, per-device.

## 12. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA 1.4.6 (7:1 body) on docs article text where the palette
  already exceeds it (17.205:1 light, 14.538:1 dark).
- **Target size:** ≥24×24 CSS px minimum, or the spacing exception — a 24px-diameter circle
  centred on each target's bounding box must not intersect another's. 44px is the design target
  for primary controls [F/S] (the console's Create/Connect buttons ≈40–44px); 24px is the hard
  floor for dense-row icon actions. *Zoom does not excuse it.*
- **Keyboard:** every function operable (SC 2.1.1) — the Goto palette, row menus, steppers and
  dialogs are fully keyboard-driven; focus indicator is the 2-step ring, never removed without a
  stronger replacement (SC 2.4.7); the focused row is never entirely hidden behind the sticky
  top bar — scroll-margin is mandatory (SC 2.4.11).
- **Contrast:** text ≥4.5:1 (§3 gate, computed); UI boundaries and focus indicators ≥3:1.
  **Colour independence:** every status pairs colour with an icon, label or shape — the yellow
  banner carries an information glyph + sentence, pills carry words ("FREE", "SHARED"), and
  metric deltas carry direction glyphs with sign.
- **Motion:** the reduced-motion variant from §8 per component; cluster-card live regions pause
  polling animations under reduced motion.
- **Text:** ≤80-character measure, 1.5 leading on prose, 200% resize without horizontal scroll
  (SC 1.4.8) — console grids scroll in their own region, never the page.
- **Semantics:** real buttons, links and inputs; correct roles for menus, steppers, tabs
  (Data Services / App Services / Charts); headings matching visual rank (serif page title is
  the h1); `aria-live="polite"` on metric tiles and cluster-state changes; `aria-busy` on
  loading card skeletons.
- **Contrast preference:** if `prefers-contrast: more` is honoured, `border.subtle` promotes to
  `#5C6C75`, `text.tertiary` promotes to `#5C6C75`, and the focus ring widens to 3px — no other
  token changes.

## 13. Anti-Patterns

Product-calibrated. Each carries the reason it was rejected *for this product*.

**Do**

1. Keep exactly one filled primary per view (`#00684A` console / `#00ED64` dark-brand) — the
   accent budget is what makes the operations surface scannable after hours.
2. Set page titles in Value Serif — it is Atlas's editorial signature and costs nothing at rest.
3. Reserve Source Code Pro for connection strings, IDs, and code; the query bar and metric
   values stay in Euclid with tabular numerals.
4. Pair every status wash with its dark foreground and a glyph — the yellow banner's sentence
   ("You will not be able to connect to databases from this address.") is the model.
5. Use skeletons that mirror final geometry (8px cards, hairlines) — never a bare spinner page.
6. Write empty states as instruction + action ("Add an IP address" → [Add IP Address]) with the
   icon-illustration above.
7. Use steppers for provisioning flows (connect = 3 steps with green completion checks).
8. Render all comparable numbers as tabular-nums and right-align them in tables.
9. Keep the 1px hairline economy: cards separated by `#E8EDEB` strokes and level-1 shadows, not
   nested grey panels.
10. Give terminal actions typed confirmation (cluster termination) and red *text* buttons, not
    red fills.
11. Keep marketing's mono eyebrow labels (`MONGODB ATLAS`) uppercase, tracked, and rare — one
    per section.
12. Sample the real canvases before inventing neutrals: `#FFFFFF` console, `#F9FBFA` sidebar,
    `#FDFFF5` marketing body, `#001E2B` dark — four different "whites and blacks" by intent.

**Don't**

1. Never put white text on `#00ED64` — 1.579:1; the fill always takes `#001E2B` ink.
2. Never use the neon green as a filled button inside the light console — it obliterates the
   primary hierarchy (console primaries are `#00684A`).
3. Don't import the condensed uppercase display into console surfaces — it is a brand voice, not
   an interface voice.
4. Don't build stat-card dashboards with no path to the underlying data — every tile drills in.
5. Don't use modals as connective tissue; the Connect dialog is one task with an end, and
   navigation stays in the shell.
6. Don't place two filled primaries side by side — "Upgrade" (in-card) and "Create" (page) never
   co-occupy a viewport at full fill.
7. Don't ship unlabelled icon toolbars — the cluster card's `…` is the only icon-only control and
   it is tooltiped.
8. Don't use placeholder-as-label; forms use persistent top labels (signup card, IP dialog).
9. Don't dump the whole page into a spinner; block only the fetching region.
10. Don't use native `alert`/`confirm` — all confirmations are authored dialogs with the
    resource name in the title.
11. Don't shrink type to fit density — the 12px meta floor is absolute; prune columns instead.
12. Don't let a disabled primary sit silently dead — state the blocker ("Add your IP address to
    enable Connect") on focus or hover.
13. Don't reuse the tutorial-highlight yellow (`#FFC010` wash) as decoration; it means *attention
    here* or *warning* and nothing else.
14. Don't introduce a new neutral grey — the eight-step gray ramp plus ink covers every value.

## 14. Quick Reference & Verification Gate

**Colour (role → light / dark):** `surface.canvas` `#FFFFFF` / `#001E2B` · `surface.inset`
`#F9FBFA` / `#112733` · `surface.hover` `#E8EDEB` / `#1C2D38` · `surface.selected` `#E3FCF7` /
`#023430` · `border.subtle` `#E8EDEB` / `#3D4F58` · `border.strong` `#3D4F58` / `#5C6C75` ·
`accent.action` `#00684A` (console) `#00ED64` (brand) / `#00ED64` · `accent.onAction` `#FFFFFF`
(console) `#001E2B` (brand) / `#001E2B` · `accent.subtle` `#E3FCF7` / `#023430` ·
`text.primary` `#001E2B` / `#E8EDEB` · `text.secondary` `#5C6C75` / `#C1C7C6` ·
`text.tertiary` `#889397` / `#889397` · `link` `#016BF8` / `#0498EC` · success `#00684A`/`#E3FCF7`
· `#C0FAE6`/`#023430` · warning `#944F01`/`#FEF7DB` · `#FFC010`/`#4C2100` · error
`#970606`/`#FFEAE5` · `#FF6960`/`#5B0000` · info `#1254B7`/`#E1F7FF` · `#C3E7FE`/`#0C2657` ·
marketing ivory `#FDFFF5` (fixed).

**Type ramp (flat):** 36 Display serif [F] · 28 Page title serif [S] · 22 Heading [F] · 18 large
· 16 Body [F] · 14 Label [F] · 13 Body/Row [S·D] · 12 Meta/Inline help · 11 Stat label
(uppercase) — Source Code Pro for identifiers; tabular-nums on all comparable values.

**Spacing + radius (flat):** 1 · 2 · 4 · 6 · 8 · 12 · 16 · 20 · 24 · 32 · 36 · 40 · 48 · 56 ·
64 · 72px on a 4px grid; radius 0/2/4/6/8/12/24/full; rows 40–44 [S], 28–32 [D]; gutter 24 [S],
16 [D], 32 [F].

**Component → token map (which semantic tokens each component consumes):**

- **Cluster card** — `surface.raised`, `border.subtle`, `text.primary/secondary`, `accent.action`
  (Connect = primary; Browse Collections = outline), `status.success.foreground` (running dot),
  `text.tertiary` (meta timestamps), `space.400/600/800`, `radius.lg`, shadow level 1.
- **Stat tile** — `text.secondary` (label), `text.primary` tabular (value), sparkline tokens
  `status.success/info/warning.foreground`, `surface.inset` well, shadow level 0.
- **Notification banner** — wash + foreground from `status.*`, left keyline `status.*.glyph`,
  `radius.md`, dismiss in `text.secondary`.
- **Dialog** — `surface.overlay`, scrim 32% ink, `radius.xl`, focus ring token, primary
  `accent.action` + secondary outline, `text.error` for destructive confirm.
- **Sidebar** — `surface.inset`, item `text.secondary` → hover `surface.hover`, active
  `surface.selected` + `#00684A` label, section eyebrow `text.tertiary` uppercase, `radius.md`.
- **Pill badge** — `accent.subtle`/`status.*` wash, dark foreground, `radius.full`, 11px
  uppercase 600.

**Pre-ship checklist.** 1 Zero raw hex outside L1. 2 No token resolves to a component name.
3 Every contrast pairing computed, passing, unrounded (§3). 4 Every semantic role has a value in
every shipped mode (console light, console dark, marketing frozen). 5 Every fetching surface has
loading/empty/error/offline specified. 6 Every component row lists disabled and loading states.
7 Row, header, toolbar and pagination heights agree. 8 Reduced-motion variant written for every
authored motion. 9 Every control keyboard-reachable with a visible focus indicator. 10 Dark
authored, not filtered, with border strength exceeding light's. 11 No unoverridden stock library
default inside a committed surface. 12 Nothing came from a marketing page — the condensed
display and ivory canvas stay out of the console; the console's one-primary budget stays in.
