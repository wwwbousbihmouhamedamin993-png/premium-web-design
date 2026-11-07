# Design System — DigitalOcean Cloud Console

<!-- premium-web-design:design-system 2 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: DigitalOcean kraken-v2 brand token foundation (official generated design-tokens endpoint, rung 2), DigitalOcean console UI verified from docs-hosted control-panel screenshots + 1440px live captures (rung 3 grounding) -->
<!-- Surface classes: 12 routes classified; density classes S + D assigned (F reserved for auth/checkout) -->

## 1. Design Posture & Atmosphere

The DigitalOcean Cloud Console is a developer's utility bench, not a dashboard showpiece. It is a
flat, white, hairline-ruled workspace where a droplet, a Kubernetes pool, or an App Platform service
is a row with a name, an IP, a cost, and a kebab menu. After eight hours the surface should feel
invisible in the way a good text editor is invisible: nothing decorates, everything measures. The
register is quiet, technical, and dry-witted — the mascot and the ocean stay at the front door
(marketing) while the product rooms are achromatic with one blue working accent.

Against its category defaults, DigitalOcean sits on the friendly-and-frugal end of cloud consoles:
simpler than the hyperscalers' multi-pane cockpits, closer to a hosting panel in shape, but with
real engineering furniture underneath — tabular costs, region pickers, plan radio cards, hourly
pricing with per-unit sub-rates. The single visual metaphor is a **work order sheet**: each resource
is a line item, each create flow is a form that names the hardware and the price before anything is
ordered.

The brand foundation behind it (the 2023+ "kraken-v2" token system, published by DigitalOcean as a
generated token file) is a deep-ink + foam-teal + cerulean palette on Inter, dual-mode by
construction. The console today ships the light mode of that foundation with the legacy primary
blue retained as the action color; the oceanic dark art direction is the marketing layer's voice,
not the product's.

**Key Characteristics** —
- Flat light product surface: white canvas, 1px hairlines at 1px `scale.100`, shadows only for
  floating layers — no card drop shadows in the default view.
- One accent fill per viewport: the primary action button renders `accent.action` blue; everything
  else is outline, ghost, or text.
- Action blue is the historical `primary.blue.200` `#0069ff`, still a live primitive in the official
  token foundation; text links step to `cerulean.600` where 4.5:1 is required.
- Ink ramp is teal-tinted: `deep.00` `#000a0a` primary on white reads as near-black with a faint
  ocean cast — the brand's fingerprint inside an otherwise neutral surface.
- Rows are the atom: 44px standard list rows, 32px dense grid rows; toolbar, header and pagination
  heights always match the row height.
- Money is always tabular: hourly rates, monthly caps, per-unit sub-rates (`$0.0316/hr`,
  `$0.0158/vCPU`) right-align in `tabular-nums`.
- Plan pickers are radio cards — hardware named first, price second, selected card gains a blue
  1px border and a pale cerulean wash.
- Region/size sliders use blue filled tracks with white round thumbs ringed in the track color.
- Status colors are muted botanicals from the official palette — algae green, tentacle amber,
  coral red — never neon; each pairs a glyph + label with the color.
- Destructive moments (destroy/rebuild) swap the whole confirmation surface to coral wash, and the
  confirm button labels the exact object being destroyed.
- Density is a mode, not a vibe: create wizards and detail panes are Standard 14px; resource lists
  and log surfaces run Dense 12–13px.
- Shadows, where allowed at levels 2–4, are blue-tinted — the official shadow ramps are
  `rgba(0, 12, 42, 0.20–0.32)`, never neutral gray.
- Marketing's ocean gradient, foam-teal pills, Plus Jakarta Sans display face and shark mascot are
  the one licensed saturation zone and never leak into console tokens (§9, §14).

## 2. Token Architecture   ← normative

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value*, after DigitalOcean's own published foundation:
  `deep.[step]` (teal-tinted ink), `scale.[step]` (neutral gray), `foam.[step]` (brand teal),
  `cerulean.[step]` (working blue), `algae.[step]` (success green), `tentacle.[step]` (warning
  amber), `coral.[step]` (error red), `kelp.[step]`, `violet.[step]`, `wave.[step]` (extended
  hues), `primary.blue.200` (`#0069ff`), `primary.cyan` (`#45cac1`), `primary.green.200`
  (`#00c483`), `primary.teal.200` (`#00afce`), `primary.terracota` (`#d74623`). Steps are 0–1000
  for deep/scale/foam/cerulean, 50–900 for hue families. Primitives are referenced only by L2.
  Banned: `[component]-[prop]` naming (`--card-bg`, `--tooltip`) — one value, many roles.
- **L2 Semantic** — role names (`surface.canvas`, `text.primary`, `accent.action`,
  `status.warning`), resolved per mode. The only layer a component may consume.
- **L3 Component** — only for deliberate deviation; points at L2 or L1, never a raw value, never a
  sibling component's token (e.g. `plan-card.borderSelected` → `border.focus`).

**Rules.** Every token has a determinable type (color, dimension, font-family, duration, shadow) or
it is invalid; names are case-sensitive and free of `$`, `{`, `}`, `.`; circular references
(`a → b → a`) are errors. Every semantic token carries a value in **every** shipped mode — the
console ships light, and the brand foundation already authors the dark counterpart of every role,
so no role is single-mode; a future dark mode inherits authored values rather than inverting.
Animatable tokens are registered with both `syntax` and `inherits`; `initial-value` must be
computationally independent, so `%`/`em` are illegal there.

**Layer order (low → high)** `[reset] → [primitives] → [semantic] → [components] → [utilities]`.
Layer order beats specificity entirely, and unlayered normal declarations outrank layered ones — a
stray un-layered rule in a component file would beat this whole system; anything a consumer must
override without `!important` sits in the top layer.

## 3. Colour Roles

| Role | Light | Dark (authored, not yet exposed in console) | Notes |
|---|---|---|---|
| `surface.canvas` | `#ffffff` | `#000000` (`deep.50`) | Console page ground |
| `surface.raised` | `#f4f5f5` (`deep.1000`) | `#000f0f` (`deep.100`) | Cards, panels, config rows |
| `surface.overlay` | `#ffffff` | `#081f1e` (`deep.200`) | Menus, popovers, dialogs |
| `surface.inset` | `#e5eceb` (`deep.950`) | `#13302e` (`deep.300`) | Wells, code blocks, log trays |
| `surface.hover` | `#f1f2f2` (`scale.50`) | `#1f403e` (`deep.400`) at 60% | Row/menu hover fill |
| `surface.selected` | `#e8f1fc` (`cerulean.50`) | `#0c3158` (`cerulean.800`) | Selected card/row wash |
| `border.subtle` | `#dde0e0` (`scale.100`) | `#1f403e` (`deep.400`) | 1px hairlines, dividers |
| `border.strong` | `#818a8b` (`scale.400`) | `#4d716e` (`deep.600`) | 1px emphasis, input frames |
| `border.focus` | `#0069ff` (`primary.blue.200`) | `#2e85e0` (`cerulean.400`) | Focus ring, ≥3:1 |
| `accent.action` | `#0069ff` (`primary.blue.200`) | `#2e85e0` (`cerulean.400`) | Primary fill; budget: 1 fill + ≤2 glyph uses per viewport |
| `accent.onAction` | `#ffffff` | `#000a0a` (`deep.00`) | Ink on the fill |
| `accent.subtle` | `#e8f1fc` (`cerulean.50`) | `#06182c` (`cerulean.900`) | Info wash, selected state |
| `accent.link` | `#1862b0` (`cerulean.600`) | `#8dbaf1` (`cerulean.200`) | Body-size text links |
| `text.primary` | `#000a0a` (`deep.00`) | `#f4f5f5` (`deep.1000`) | Headings, row primaries |
| `text.secondary` | `#586667` (`scale.600`) | `#6f908c` (`deep.700`) | Descriptions, sub-text |
| `text.tertiary` | `#4d716e` (`deep.600`) | `#9db5b2` (`deep.800`) | Meta, captions |
| `text.disabled` | `#9ba3a4` (`scale.300`) | `#4d716e` (`deep.600`) | Inactive components (exempt) |
| `status.success` | `#6c7e35` glyph / `#525f28` text on `#f2f4e6` (`algae.50`) | `#879b42` glyph on `#1d210e` | Active, available, running |
| `status.warning` | `#b0843a` glyph / `#84632c` text on `#fbf5e8` (`tentacle.50`) | `#daa549` glyph on `#2c210f` | Degraded, migration, caps |
| `status.error` | `#b2543e` glyph / `#843a29` text on `#f8ebe7` (`coral.50`) | `#a54a34` glyph on `#210f0a` | Failed, destroyed |
| `status.info` | `#1e7adb` glyph / `#124984` text on `#e8f1fc` (`cerulean.50`) | `#5198fb` glyph on `#06182c` | Tips, in-progress |

Dark canvas is **not** plain inverted white: the authored dark ramp runs `#000000` canvas →
`#000f0f` raised → `#081f1e` overlay, with border strength *raised* relative to light
(`deep.400` hairlines, stronger than light's `scale.100`). Depth in dark comes from surface steps
and 1px strokes, never shadows.

**Contrast gate — computed ratios, unrounded; 4.499:1 fails. Body ≥4.5:1; UI boundaries and focus
indicators ≥3:1** (W3C, SC 1.4.3, 1.4.11). Large text is ≥24px or ≥18.5px bold.

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| `text.primary` | `#000a0a` | `surface.canvas` | `#ffffff` | 20.042:1 | 4.5 | PASS |
| `text.secondary` | `#586667` | `surface.canvas` | `#ffffff` | 5.981:1 | 4.5 | PASS |
| `text.tertiary` | `#4d716e` | `surface.canvas` | `#ffffff` | 5.381:1 | 4.5 | PASS |
| `text.secondary` | `#586667` | `surface.raised` | `#f4f5f5` | 5.475:1 | 4.5 | PASS |
| `text.tertiary` | `#4d716e` | `surface.raised` | `#f4f5f5` | 4.926:1 | 4.5 | PASS |
| `accent.onAction` | `#ffffff` | `accent.action` | `#0069ff` | 4.704:1 | 4.5 | PASS |
| `accent.link` | `#1862b0` | `surface.raised` | `#f4f5f5` | 5.633:1 | 4.5 | PASS |
| `border.strong` | `#818a8b` | `surface.raised` | `#f4f5f5` | 3.236:1 | 3.0 | PASS |
| `border.focus` | `#0069ff` | `surface.canvas` | `#ffffff` | 4.704:1 | 3.0 | PASS |
| `status.success` glyph | `#6c7e35` | `status.success` wash | `#f2f4e6` | 4.035:1 | 3.0 | PASS |
| `status.warning` glyph | `#b0843a` | `status.warning` wash | `#fbf5e8` | 3.114:1 | 3.0 | PASS |
| `status.error` glyph | `#b2543e` | `status.error` wash | `#f8ebe7` | 4.261:1 | 3.0 | PASS |
| `status.info` glyph | `#1e7adb` | `status.info` wash | `#e8f1fc` | 3.788:1 | 3.0 | PASS |
| `status.success` text | `#525f28` | `status.success` wash | `#f2f4e6` | 6.232:1 | 4.5 | PASS |
| `status.warning` text | `#84632c` | `status.warning` wash | `#fbf5e8` | 5.083:1 | 4.5 | PASS |
| `status.error` text | `#843a29` | `status.error` wash | `#f8ebe7` | 6.885:1 | 4.5 | PASS |
| `status.info` text | `#124984` | `status.info` wash | `#e8f1fc` | 7.967:1 | 4.5 | PASS |
| `text.primary` dark | `#f4f5f5` | `surface.canvas` dark | `#000000` | 19.226:1 | 4.5 | PASS |
| `text.secondary` dark | `#6f908c` | `surface.raised` dark | `#000f0f` | 5.621:1 | 4.5 | PASS |
| `border.strong` dark | `#4d716e` | `surface.raised` dark | `#000f0f` | 3.630:1 | 3.0 | PASS |

Gate notes: `accent.action` as *small* link text passes on canvas (4.704:1) but fails on raised
(4.306:1 < 4.5) — small links on `surface.raised` use `accent.link`; `#0069ff` remains legal for
large/bold link text (≥3.0 everywhere) and for all fills and focus rings. `text.disabled` at
2.571:1 is confined to genuinely inactive components (SC 1.4.3 exemption) and never to informative
text.

## 4. Typography

**Families.** UI: **Inter** — self-hosted woff2 (weights 400 regular, 500 medium, 600 semibold),
fallback "Inter Fallback" then generic sans; DigitalOcean's own pages declare Inter as the base
family with Plus Jakarta Sans reserved for display. Numeric/code: **JetBrains Mono** (weights 400,
500) for console/log output, code snippets, SSH strings and connection commands — monospace is for
identifiers and code, never a costume. Plus Jakarta Sans is the marketing display face and appears
nowhere in the console.

**One ramp table per class, not one blended table.**

- **[F] Focused, 16px base** (auth/login, checkout of paid plans):

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Display | 36px | 600 | 40px | −0.01em | default | Sign-in headline |
| Heading | 24px | 600 | 32px | 0 | default | Form section titles |
| Body | 16px | 400 | 24px | 0 | default | Form prose, legal |
| Label | 14px | 500 | 20px | 0 | default | Field labels, buttons |
| Meta | 12px | 400 | 16px | 0 | tabular | Helper text, "billed hourly" notes |

- **[S] Standard, 14px base** (create wizards, resource detail, billing, settings):

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Page title | 24px | 600 | 32px | 0 | default | Route title (matches official heading ramp 24/32) |
| Section title | 16px | 600 | 24px | 0 | default | Card/panel headers |
| Body | 14px | 400 | 20px | 0 | default | Prose, descriptions |
| Row primary | 14px | 500 | 20px | 0 | tabular when numeric | Resource names, plan names |
| Row secondary | 13px | 400 | 18px | 0 | tabular when numeric | Specs line "2 vCPU · 4 GB · 120 GB" |
| Stat value | 24px | 600 | 32px | 0 | tabular-nums | Cost totals, graph figures |
| Stat label | 11px | 600 | 16px | +0.04em, uppercase | default | Stat captions, column caps |
| Meta | 12px | 400 | 16px | 0 | tabular for timestamps | Created dates, IDs, helper text |

- **[D] Dense, 12–13px base** (resource lists, firewalls, logs, monitoring):

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Grid header | 12px | 600 | 16px | +0.02em, uppercase | default | Column headers |
| Grid cell numeric | 13px | 400 | 18px | 0 | tabular-nums | IP, cost, size, count |
| Grid cell text | 13px | 400 | 18px | 0 | default | Names, tags, regions |
| Log line | 13px | 400 | 20px | 0 | tabular-nums | JetBrains Mono console/log rows |
| Inline help | 12px | 400 | 16px | 0 | default | Field hints under cells |

Prose inside a dense screen still steps up to 14px Body.

**Invariants.** `tabular-nums` on every comparable value — hourly/monthly cost, transfer GB,
timestamps, counts, droplet IDs. Right-align numerics, left-align text, never centre a numeric
column. Fixed stepped sizes; no fluid type. Measure ≤80 characters (SC 1.4.8); 65–80ch [F/S],
unconstrained [D].

## 5. Spacing Scale & Density Scales   ← two axes, never one

**Spacing base: 4px grid; 8px comfortable [F/S], 4px [D]** — matching the official foundation's
published spacing steps (0/2/4/8/12/16/24/40). `space.0` 0 · `space.1` 4px icon-to-label ·
`space.2` 8px control padding [D] · `space.3` 12px cell padding [S] · `space.4` 16px card padding
[S] / page gutter · `space.6` 24px card padding [F] + section gap · `space.8` 32px section gap [S]
· `space.10` 40px region separation (official step) · `space.12` 48px rare · `space.16` 64px
rarely. *No `17px`. No `23px`. If a layout needs an off-scale value, the layout is wrong.*

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | Auth, plan checkout |
| `standard` | 44px | 14px | 12–16px | 24px | Create wizards, resource detail, billing, settings |
| `dense` | 32px | 13px | 8px | 16px | Droplet/K8s/DB lists, firewalls, logs, monitoring graphs |

- Density comes from **row height, column pruning and leading** — never from type too small to
  read. A 13px tabular numeral in a dense droplet list is correct; the same numeral in a checkout
  form is a defect.
- **Never switch mid-page.** Switching across routes with different jobs is legitimate — the
  create wizard (S) and the droplet list (D) should feel like different rooms.
- **Chrome follows rows.** Header, toolbar, batch bar and pagination heights always match the
  table's row height — a 44px toolbar over 32px dense rows is a rhythm break.
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40%. *House heuristic — validate
  by screenshot.*

## 6. Radius Scale

`none` 0 · `xs` 2px tags/status dots · `sm` 4px inputs, buttons, dense cells, inline code ·
`md` 8px cards, plan radio-cards, option tiles, popovers (verified 8px in the create-droplet plan
picker) · `lg` 12px drawers, dialogs · `full` 9999px pills, avatars, region flags. **One radius per
component family**, never mixed ad-hoc. Nested radii obey `radius_inner = radius_outer − padding`
(a 4px input inside an 8px card with 4px padding has no visible inner radius).

## 7. Elevation

**Light: flat hairlines for static layers + blue-tinted multi-layer shadows for floaters; Dark:
surface-luminance steps + 1px keylines, zero shadows.** Levels, low → high:

- **0** `surface.canvas` — no shadow, no border.
- **1** card/panel — 1px `border.subtle`, no shadow (the console's default raised panel).
- **2** sticky header/toolbar — 1px `border.subtle` + `0 1px 4px rgba(0, 12, 42, 0.20)`.
- **3** dropdown/popover — `0 4px 12px rgba(0, 12, 42, 0.24)` + 1px `border.strong`, `radius.md`.
- **4** dialog — `0 8px 24px rgba(0, 12, 42, 0.32)` + scrim `rgba(0, 10, 20, 0.5)`, `radius.lg`.

Shadow color is always the official blue-black `rgba(0, 12, 42, …)` at steps 0.20/0.24/0.28/0.32 —
never neutral gray, never brand blue. In dark mode levels 1–4 become surface steps
(`deep.100 → deep.200 → deep.300`) with `border.strong` keylines; scrim lightens to
`rgba(0, 26, 31, 0.6)`.

## 8. Motion

`instant` 0ms · `fast` 120ms ease-out (exits [D], menu close, row deselect) · `base` 180ms
decelerate ([D] entrances, drawer slide, popover open) · `slow` 240–300ms decelerate ([F/S]
entrances, dialogs, wizard step transitions).

- Entrances decelerate, exits accelerate. Symmetric ease-in-out on both directions is a defect.
- Animate `transform` and `opacity` only — never `width`, `height`, `top`, `left`.
- No bounce on irreversible moments: not on the destroy confirmation, not on a plan downgrade.
- Progress is honest: droplet/cluster creation shows a determinate progress affordance with the
  resource name, not a spinner against a blank page.
- **Reduced motion is a real variant**, not animation-off everywhere: movement → crossfade under
  ~150ms; scaling and panning of large objects are what must be neutralised for vestibular safety.

## 9. Imagery & Art Direction   ← the one licensed saturation moment

- **Brand moment:** the oceanic dark hero — deep-sea gradient (black → deep teal → foam), wireframe
  terrain renders, Plus Jakarta Sans display type, and the shark mascot — lives on marketing
  surfaces only. Its palette (`foam.*` glows, gradient stops `rgba(201, 238, 242, 0.75)` →
  `rgba(48, 203, 217, 0.6)` → `rgba(135, 155, 66, 0.3)`) **never leaks into UI tokens**; the
  console's only saturated moments are the blue action and status botanicals.
- **Iconography:** DigitalOcean's own line icon set, 1.5px strokes on a 16px/24px grid, geometric
  and slightly rounded — matched to Inter's tone. Resource category icons (droplet, kubernetes
  helm, database cylinder) render at 20px with `text.secondary`; filled variants only where a
  stroke cannot carry 16px. Icon-only controls still carry a label or tooltip (§10).
- **Photography:** none in product UI.
- **Illustration / 3D:** none in the console; 3D renders and gradient art are marketing-only. No
  per-screen empty-state illustration system exists — empty states use text + CTA, so nothing is
  invented per screen.
- **Empty / error art:** an empty droplet list shows a short explanation ("Droplets are Linux
  virtual machines…") and the create CTA; illustration never substitutes for the recovery CTA.
- Third-party logos (distro marks, marketplace one-clicks) render inside committed light chips at
  native color only when officially required; otherwise monochrome.

## 10. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell/sidebar | S | Expanded, collapsed, project-scoped | Hover, active route, focus ring | Tab order, arrow keys in project menu | "Projects — pick a project" |
| Data table (resource list) | D | Plain, grouped by project, sortable columns | Hover, selected, loading skeleton, empty, error, stale | Arrow keys, Space select, Enter open | "Sort by name" |
| Filter/search bar | D/S | Text query + facet chips (region, image, tag) | Focus, filled, cleared, no-results | Slash focuses, Esc clears | "Filter by name, tag, or IP" |
| Row action menu | D | Kebab per row | Focus-trap, Esc closes, disabled items explain | Arrow navigate, Esc | "Resize · Rebuild · Power off · Destroy" |
| Plan/size picker | S | Radio cards + category tabs + sliders | Hover, selected, disabled (unavailable region) explains | Arrow keys move radio | "$32.00/mo — 2 vCPU, 4 GB RAM" |
| Stat tile / graph card | S | Line, bar, range switcher | Loading, no-data, stale | Range switcher tabbable | "Bandwidth — last 14 days" |
| Drawer/inspector (resource detail) | S | Right drawer, full detail page | Open, Esc, focus returns to trigger | Esc closes, focus trap | "Droplet detail" |
| Dialog | S | Confirm destructive, form | Focus-trap, Esc (unless destructive confirms by typing) | Tab, Esc, Enter | "Destroy droplet? Type its name to confirm" |
| Tag pill | D | Add, removable | Hover reveal remove, focus | Backspace removes in editor | "webserver ×" |
| Notification banner | S | Info, warning, error, success | Dismissible, auto-linked to resource | Esc dismisses, link focusable | "Power off complete — view droplet" |
| Code snippet block | S/D | One-line, multi-line | Copied confirmation (width never changes) | Copy button reachable | "Copy" → "Copied" |
| Member row (team settings) | S | Role select, remove | Disabled for owner, pending invite | Role select keyboard-operable | "Owner cannot be removed" |

**Every fetching surface also designs:** loading (skeleton matching final geometry — row-shaped
bars at the real row height, never a centred spinner on a blank page), empty (what's missing + the
CTA that fixes it), error (what happened + "Retry"), offline/stale (a banner names the data age;
cached rows stay visible).

**Contracts this table encodes:** one primary filled CTA per view [F/S] (dense toolbars may run a
primary plus icon actions); every icon-only control carries a label or tooltip; a disabled control
states *why* on focus or hover ("Resize unavailable while droplet is powered off"); a button never
changes width between idle and loading — reserve the space with a fixed min-width.

## 11. Light / Dark Strategy

- **Posture:** **A light-only** for the console (shipped reality), on a **dual-parity brand
  foundation** — the official token system authors both modes of every primitive, so dark values
  above are authored, not guessed. Reason: the console's audience and the docs' screenshots are
  uniformly light; a half-shipped dark mode would fragment the support surface.
- **Mechanism:** semantic roles remapped per mode via the standard light/dark resolution; **no role
  absent in either mode** — the table in §3 carries authored values for both columns.
- **`color-scheme`** set at the root so UA chrome, form controls and scrollbars follow the shipped
  mode; it repaints UA-provided parts of the canvas only, not the document's own theme.
- **The mode meta declaration ships in the head before the stylesheet** to prevent a flash of the
  wrong scheme.
- **Dark is authored, not inverted:** own surface ramp (`#000000 → #000f0f → #081f1e → #13302e`),
  own border strength — *higher* than light (`deep.400` hairlines vs light's `scale.100`, because a
  delicate 1px line on white reads as invisible on near-black) — own shadow policy (zero shadows,
  surface steps instead). `light-dark()` in the foundation is progressive enhancement only.
- Org-tinting is not offered; team workspaces share one theme so a theme swap can never move
  geometry.

## 12. Density-Mode Strategy

- **Default mode per surface class:** Standard for create/detail/billing/settings; Dense for
  resource lists, firewalls, logs, monitoring. Boundary: if the route's primary job is *scanning
  many comparable rows*, it is Dense; if it is *deciding and configuring*, it is Standard.
- **Mechanism:** a density attribute at the app root rescales row height, cell padding, gutter and
  body size together as one token axis — spacing tokens do not change per screen size. It is a
  property of the route, not a media query.
- **Container queries for reflow:** reflow responds to the container's content box so table cards
  reflow inside their column, not to the viewport; size queries fail closed with no eligible
  container (units silently resolve to small-viewport units there), so container units are never
  used where that fallback would be wrong.
- **Style queries** compare computed values, so the density marker must be a registered custom
  property for style-based branching to work.
- **Offer the switch as an accessibility affordance**, not a preference: a denser/roomier toggle in
  table toolbars serves users with visual field loss (W3C's SC 2.5.8 note endorses a layout-density
  control); the setting persists per user, never per theme.

## 13. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA for measure and leading on prose (SC 1.4.8) where surfaces
  are text-dominant.
- **Target size:** ≥24×24 CSS px hard minimum (SC 2.5.5's 44×44 is AAA, not AA); 44px is the design
  target for primary controls [F/S], 24px for dense-row kebabs and checkboxes. The spacing exception
  applies: a 24px-diameter circle centred on each target's bounding box must not intersect
  another's. Zoom does not excuse it.
- **Keyboard:** every function operable (SC 2.1.1); focus indicator visible (SC 2.4.7) — a 2px
  `border.focus` ring offset 2px, never removed without a stronger replacement; the focused row is
  never entirely hidden by a sticky header or toolbar (SC 2.4.11).
- **Contrast:** text ≥4.5:1; UI boundaries and focus indicators ≥3:1 (SC 1.4.11) — computed in §3.
  **Colour independence:** every status pairs colour with an icon and a label ("Active", "Offline");
  deltas carry a sign or direction glyph; power state adds a dot + word.
- **Motion:** the reduced-motion variant from §8 ships per component.
- **Text:** ≤80-character measure, 1.5 leading on body prose, 200% resize without horizontal scroll
  (SC 1.4.8).
- **Semantics:** real button/link/input elements; correct table semantics for resource lists;
  headings matching visual rank; polite live announcements for "Droplet created" toasts; busy
  state on loading regions.
- **Contrast preference:** `prefers-contrast: more` swaps `border.subtle → border.strong`,
  `text.tertiary → text.secondary`, and raises focus-ring width to 3px (values:
  `no-preference`, `more`, `less`, `custom`).

## 14. Anti-Patterns

**Do** —
1. Name the hardware before the price in every create flow ("2 vCPU, 4 GB RAM — $32.00/mo"): the
   product's contract is predictable economics.
2. Keep the whole list row clickable with a visible hover fill at `surface.hover`; the kebab is the
   secondary path.
3. Render every cost, transfer and timestamp in `tabular-nums`, right-aligned.
4. Use the blue-tinted official shadow ramps for floaters; keep static panels at 1px hairlines.
5. Pair every status with a glyph + label; the tag pill pairs text with a removable affordance.
6. Give disabled plan cards a reason on hover ("Not available in this region").
7. Keep toolbar, header and pagination heights equal to the table's row height.
8. Reserve button width through the loading state; show progress inside the button.
9. Type-to-confirm on destroy: the dialog demands the resource's exact name.
10. Keep the ink ramp teal-tinted (`deep.*`) so the brand fingerprint survives neutrality.
11. Use JetBrains Mono for console output, SSH commands and code snippets only.
12. Offer the density switch on table toolbars as an accessibility affordance.

**Don't** —
1. Don't bring the ocean gradient, foam-teal pills, Plus Jakarta Sans, or the shark mascot into the
   console — the brand moment ends at the marketing boundary.
2. Don't replace the blue action with the marketing foam teal inside product UI; `#0069ff` is the
   console's action contract.
3. Don't inflate lists into stat-card dashboards; a droplet list is a table, not a wall of tiles.
4. Don't stack two filled primary CTAs side by side; secondary actions are outline or text.
5. Don't use modals as connective tissue between steps — wizards use pages, not dialog chains.
6. Don't ship hover-only affordances; every hover state has a focus twin.
7. Don't use placeholder text as the field label.
8. Don't show a whole-page spinner; skeletons match final geometry.
9. Don't fire native alert/confirm for destructive flows; the typed-name dialog is the pattern.
10. Don't shrink type below 13px to cram columns — prune columns, not legibility.
11. Don't leave a disabled primary button silent; it explains on focus.
12. Don't mix radius families inside one component (an 8px card with 4px and 12px children is a
    defect; nested radii subtract padding).

## 15. Quick Reference & Verification Gate

**Colour (role → hex, light / dark):** canvas `#ffffff`/`#000000` · raised `#f4f5f5`/`#000f0f` ·
overlay `#ffffff`/`#081f1e` · inset `#e5eceb`/`#13302e` · hover `#f1f2f2`/`deep.400@60%` ·
selected `#e8f1fc`/`#0c3158` · border.subtle `#dde0e0`/`#1f403e` · border.strong
`#818a8b`/`#4d716e` · border.focus `#0069ff`/`#2e85e0` · accent.action `#0069ff`/`#2e85e0` ·
onAction `#ffffff`/`#000a0a` · accent.subtle `#e8f1fc`/`#06182c` · accent.link `#1862b0`/`#8dbaf1` ·
text.primary `#000a0a`/`#f4f5f5` · text.secondary `#586667`/`#6f908c` · text.tertiary
`#4d716e`/`#9db5b2` · text.disabled `#9ba3a4`/`#4d716e` · success `#6c7e35`/`#879b42` · warning
`#b0843a`/`#daa549` · error `#b2543e`/`#a54a34` · info `#1e7adb`/`#5198fb`.

**Type ramp:** Inter 400/500/600 self-hosted; JetBrains Mono 400/500 for code/log identifiers.
[F] 36/40 · 24/32 · 16/24 · 14/20 · 12/16. [S] 24/32 title · 16/24 section · 14/20 body · 14/20
row · 13/18 row-secondary · 24/32 stat (tabular) · 11/16 caps label · 12/16 meta. [D] 12/16
caps header · 13/18 cells (tabular numerics) · 13/20 mono log · 12/16 inline help.

**Spacing + radius:** 4px base; steps 0/4/8/12/16/24/32/40/48/64; [F] pad 24 gutter 32 · [S] pad
16 gutter 24 · [D] pad 8 gutter 16. Radius: 0/2/4/8/12/full; one radius per component family.

**Component → token map:** resource table → `surface.canvas`, `border.subtle`, `text.primary`,
`text.secondary`, `surface.hover`, `status.*` glyph+text, JetBrains Mono for log cells ·
plan card → `surface.raised`, `border.subtle`, `border.focus` on selection, `surface.selected`
wash, `text.primary` name + `text.secondary` specs, `accent.action` price emphasis · primary
button → `accent.action` + `accent.onAction`, `radius.sm` · dialog → `surface.overlay`,
`radius.lg`, level-4 shadow + scrim · banner → `status.*` wash + text pair, `radius.sm`.

**Agent prompt block.** Build DigitalOcean console surfaces with these roles only:
surface.canvas `#ffffff`, surface.raised `#f4f5f5`, surface.inset `#e5eceb`, surface.hover
`#f1f2f2`, surface.selected `#e8f1fc`, border.subtle `#dde0e0`, border.strong `#818a8b`,
border.focus `#0069ff`, accent.action `#0069ff` (onAction `#ffffff`), accent.link `#1862b0`,
text.primary `#000a0a`, text.secondary `#586667`, text.tertiary `#4d716e`, success `#6c7e35`
(wash `#f2f4e6`, text `#525f28`), warning `#b0843a` (wash `#fbf5e8`, text `#84632c`), error
`#b2543e` (wash `#f8ebe7`, text `#843a29`), info `#1e7adb` (wash `#e8f1fc`, text `#124984`).
Type: Inter 400/500/600, JetBrains Mono for code/logs; Standard base 14px, Dense base 13px, page
title 24/32. Spacing on the 4px grid (pad 16 [S], 8 [D]; gutters 24/16). Radius 4 inputs/buttons,
8 cards, 12 dialogs. Rows 44px [S] / 32px [D]; chrome matches row height. Shadows only for
floaters, always `rgba(0, 12, 42, 0.20–0.32)`. Motion 120/180/240ms, transform/opacity only,
decelerate entrances.

**Example component prompts.**
1. *Resource list (Droplets) [Dense]* — `surface.canvas` ground; rows 32px with 8px cell padding;
   header row 32px in 12px caps `text.tertiary`; name cell `text.primary` 13px + specs line
   `text.secondary`; IP and cost right-aligned in tabular-nums; status = algae glyph + "Active"
   label + green dot; row hover `surface.hover`; kebab opens a focus-trapped menu; skeleton rows
   match 32px geometry while loading; empty state names the gap with a "Create Droplet" primary.
2. *Plan picker (create wizard) [Standard]* — 44px+ radio cards at `radius.md`, 1px
   `border.subtle`; selected card gains `border.focus` + `surface.selected` wash; category tabs
   underline in `accent.action`; price line "$32.00/mo" 14px semibold with "$0.0438/hr" meta in
   tabular-nums; disabled cards explain region availability on hover; one primary "Create" button
   in `accent.action` at the wizard footer.
3. *Destructive dialog [Standard]* — `surface.overlay`, `radius.lg`, level-4 shadow + scrim;
   title "Destroy droplet?" in `text.primary`; body names the resource and the irreversibility in
   `text.secondary`; input demands the exact droplet name; confirm button fills `status.error`
   tone with white onAction only when the typed name matches; Esc closes, focus returns to the row.

**Pre-ship checklist.** 1 Zero raw hex outside L1. 2 No token resolves to a component name.
3 Every contrast pairing computed, passing, unrounded. 4 Every semantic role has a value in every
shipped mode (light shipped; dark authored). 5 Every fetching surface has loading/empty/error/
offline specified. 6 Every component row lists disabled and loading states. 7 Row, header, toolbar
and pagination heights agree. 8 Reduced-motion variant written for every authored motion. 9 Every
control keyboard-reachable with a visible focus indicator. 10 Dark authored, not filtered, with
border strength exceeding light's. 11 No unoverridden stock library default inside a committed
surface. 12 Nothing came from a marketing page. 13 The §9 brand-moment palette (ocean gradient,
foam glow stops, mascot) appears nowhere in the UI token layers.
