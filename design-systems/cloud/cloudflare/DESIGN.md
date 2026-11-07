# Design System — Cloudflare Dashboard (dash.cloudflare.com)

<!-- premium-web-design:design-system 2 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: Cloudflare Kumo, the open-source dash component library (density/type posture, semantic surface ladder, 14px content rule, instant-hover rule, concentric-radius rule — oklch theme verified against packages theme source, rung 2), Cloudflare blog "Thinking about color" (10 hues × 10 luminosity steps, 4.5:1 bolding threshold, rung 2) and "Dark Mode for the Cloudflare Dashboard" (authored dark via luminosity reversal, off-black canvas, outline-icon nav, rung 2), brand constants #F6821F / #F38020 / #FBAD41 (rung 2), screens/ captures of the live dash (DNS records, Security Overview, Network Analytics, Networking Overview, plan change) and cloudflare.com (rung 3 grounding). Ladder: rung 1 missed (no sibling spec); rung 2 supplied the spec; rung 3 grounded it. -->
<!-- Surface classes: 12 routes classified; density classes F/S/D assigned (F destructive confirmations + plan change; S zone overview + security overview + settings + account home; D DNS records + analytics tables + log explorer + audit log + member lists) -->

## 1. Design Posture & Atmosphere

The Cloudflare dashboard is the control console for the network that fronts roughly a fifth of the
web: zones, DNS, TLS, WAF, caching, Workers, analytics. Its posture is **the instrument panel for
the internet** — a light, near-monochrome workspace where every coloured thing means something.
The canvas is an off-white `#FBFBFB`; cards float on 1px hairlines rather than shadows; the action
colour is a confident electric blue `#056DFF`, not the brand orange. That inversion is the system's
central decision: **orange is the brand, blue is the verb.** Orange (#F6821F) belongs to the
logo, the proxy cloud, marketing moments and celebration surfaces; buttons, links and focus rings
speak blue. After eight hours on-call, nothing in the dash glows, bounces, or begs — the loudest
element on a data screen is a tabular numeral in a chart legend.

The second face is the **authored dark mode**: a near-black `#030303` canvas (pure black was
rejected as "too intense" by the team that built it), surfaces raised by luminosity steps and
1px strokes, hues flipped by lightness while keeping their hue angle so a blue CTA stays a blue
CTA. Dark is not a filter — nav icons switch from outline to filled only for the selected app,
hairlines strengthen, and a 30% black drop plus a 10% white edge replace the light-mode shadow.
Mode, not brand, is the biggest visual switch a user can throw; a FedRAMP token theme exists as
the org-tinted proof that geometry never moves when colour does.

Against its category (AWS's blue-on-slate density, GCP's card-heavy material console, Azure's
grey-blue fluent panels), Cloudflare's dash is the **lightest and quietest of the big-three
consoles**: white canvas, hairline separators, sentence-case headings, one filled CTA per view,
and data surfaces that drop to 28px rows and 12–13px text only where the job is scanning. The
visual metaphor, stated plainly: **air-traffic control for your zone** — calm surfaces, a
signature orange-cloud toggle for what rides the network, and numbers that are always tabular.

**Key Characteristics**
- Two canvases: light `#FBFBFB` and authored dark `#030303` (never pure black, never pure white);
  depth is a luminosity-step ramp plus 1px hairlines — light mode allows small shadows, dark mode
  adds a 10% white keyline edge to every raised surface.
- **Orange is the brand, blue is the verb:** brand orange `#F6821F` paints the logo, the proxy
  cloud and marketing moments; the action blue `#056DFF` (light) / `#0462E5` (dark) paints
  primary buttons, focus rings and selection. Accent budget: one filled blue CTA per view [S/D];
  orange appears in UI only as the proxy toggle and badge fills.
- Interface typeface is **Inter** at 14px base (16px reserved for headings), weights 400/500/600
  only — 600 replaces bold everywhere; global tracking −0.01em, never adjusted further; headings
  are always sentence case.
- 10-hue × 10-step colour scales (each hue's 5 darkest steps pair with white text, 5 lightest
  with black) — chart palettes are drawn from these scales, never free-picked.
- Signature control: the **proxy cloud toggle** — filled orange cloud = Proxied, outline grey
  cloud = DNS only. Colour is never the only cue; the label always rides beside the glyph.
- Rows: 40px standard tables, 28–32px dense grids; chrome (header, toolbar, pagination) always
  matches row height. Buttons: 36px default, 26px compact, 20px micro.
- Shape ladder: 4px small controls and inline code · 6px compact buttons/inputs · 8px buttons,
  cards, inputs · 12px dialogs, popovers, toasts · full pills for badges and status.
- Badges are pills with tint fills and dark semantic ink; a dashed-outline pill marks beta;
  zone status pairs a coloured dot with a word (Active, Pending, Moved).
- Hover is **instant** — no colour transition on hover; entrances animate 180ms decelerate,
  dialogs 240ms; reduced motion collapses movement to a 150ms crossfade.
- Feedback surfaces are geometric skeletons matching final layout; the empty state names what is
  missing and carries the CTA that fixes it; destructive flows restate the resource name.
- Charts use scale-derived hues (blue pass, red drop, orange mitigated) with glyph-paired
  legends; totals render as 24–32px tabular numerals.
- Whitespace budget: Standard 40–55%, Dense 25–40%; prose measure ≤80ch; data surfaces
  unconstrained.

## 2. Token Architecture

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value* (`palette.step`), referenced only by L2.
  Light-mode ramp: `ink-950 #0A0A0A` · `ink-900 #18181B` · `ink-500 #737373` · `ink-420 #8C8C8C`
  · `ink-350 #A1A1A1` · `ink-300 #D4D4D4` · `ink-0 #FFFFFF`; canvases `paper-25 #FBFBFB`,
  `paper-0 #FFFFFF`, `paper-100 #F8F8F8`, `paper-150 #F7F7F7`, `paper-200 #F5F5F5`,
  `paper-250 #F2F2F2`, `paper-300 #E5E5E5`, `paper-350 #E9E9E9`; brand `orange-500 #F6821F`,
  `orange-300 #FBAD41`, `orange-250 #FFB11B`; action `blue-550 #056DFF`, `blue-650 #0462E5`,
  `blue-700 #1447E6`, `blue-850 #193CB8`, `blue-400 #56A2FF`; status `green-600 #009669`,
  `green-800 #005F46`, `green-400 #00D294`, `green-100 #EBFDF1`, `green-150-wash #0F1D15` (dark
  wash), `amber-500 #FA8900`, `amber-800 #8F5000`, `amber-400 #FF8B1F`, `amber-100 #FFFAEA`,
  `red-550 #FB2C36`, `red-650 #E40016`, `red-750 #BF000F`, `red-400 #FF6568`, `red-50 #FFF3F3`,
  `sky-450 #00A5EA`; dark ramp `night-1000 #030303`, `night-950 #060606`, `night-880 #0B0B0B`,
  `night-900 #0F0F0F`, `night-800 #18181B`, `night-700 #262626`, `night-650 #6B6B6B`,
  `night-600 #525252`, `night-500 #737373`, `night-350 #A1A1A1`, `night-150 #E9E9E9`,
  `night-330 #333333`; dark washes `amber-wash-dark #2A1C0A`, `red-wash-dark #270D0D`,
  `info-wash-dark #12192B`. Banned: component-named primitives (a card-background name) — one
  value, many roles.
- **L2 Semantic** — role names (`surface.canvas`, `surface.raised`, `text.primary`,
  `accent.action`, `border.focus`, `status.error.ink`). The only layer a component may consume.
  Every role carries a value in **both** shipped modes (§3); both modes derive from the same
  primitive pool by luminosity reversal that preserves hue and saturation, so a mode flip is a
  re-binding of roles, never a second vocabulary. Mode and theme are declared on a root
  attribute (`mode: light|dark`; `theme: default|fedramp`); tokens resolve per mode through
  paired custom properties, and no role may exist in only one mode.
- **L3 Component** — only for deliberate deviation, pointing at L2 or L1, never at a raw value
  and never at a sibling component's token: `proxy-toggle → orange-500 fill vs paper-300 outline
  + status label` · `dns.row → 32px row + tabular numerals + border.subtle separator` ·
  `badge.beta → transparent fill + dashed border.strong + link-blue ink` ·
  `stat.tile → text.primary value at 24–32px + text.secondary label` ·
  `skeleton → paper-300 / night-700 with sweep` · `log.line → mono 13px on surface.canvas` ·
  `chart.series → scale hues only, legend glyph + label`.

**Rules.** Every token has a determinable type (colour, dimension, font-family, duration, easing)
or it is invalid; names are case-sensitive and free of `$`, `{`, `}` and dots; circular references
are an error. Every semantic token resolves in both modes and both themes — the FedRAMP theme
changes colour values only and is forbidden from moving radii, type sizes or spacing. Animatable
tokens (skeleton sweep, dialog fade) are declared with explicit syntax and inheritance; initial
values are computationally independent, so percentage-based initial values are illegal.

**Layer order (low → high):** `reset → primitives → semantic → components → utilities`. Order
beats specificity entirely, so a stray un-layered declaration inside a component file would
outrank the whole system; anything a consumer must override without forcing priority lives in the
top layer. A lint rule flags any raw colour consumed directly by a component — the primitive
exceptions are pure white and pure black for content that must stay literal (chart gridlines,
scrim).

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` | #FBFBFB | #030303 | page background; off-white / off-black, never pure |
| `surface.raised` | #FFFFFF | #0F0F0F | cards, panels, table base |
| `surface.overlay` | #F7F7F7 | #262626 | popovers, menus, selects |
| `surface.inset` | #F2F2F2 | #0B0B0B | recessed wells, segmented-tab tracks, code wells |
| `surface.hover` | #F5F5F5 | #262626 | row/item hover fill and tint; readable text on it steps up to the primary ink role |
| `surface.selected` | #F5F5F5 | #262626 | selected rows/segments, active nav item fill |
| `border.subtle` | #E9E9E9 | #262626 | 1px hairline separators; decorative only (1.21:1 / 1.27:1) |
| `border.strong` | #8F8F8F | #6B6B6B | committed control boundaries, input edges; ≥3:1 gate |
| `border.focus` | #262626 | #E9E9E9 | 2px focus ring ink, paired with `accent.action` ring on primary controls |
| `accent.action` | #056DFF | #0462E5 | filled CTA plate, primary selection; hover darkens to #1447E6 both modes |
| `accent.onAction` | #FFFFFF | #FFFFFF | ink on the action plate and on destructive plate |
| `accent.subtle` | #EFF6FF | #12192B | info washes, link-card hovers, selected-filter fills |
| `accent.brand` | #F6821F | #F6821F | logo, proxy cloud, orange badges (#FFB11B fill + black ink); never body text in light |
| `text.primary` | #18181B | #F5F5F5 | body and row ink |
| `text.strong` | #0A0A0A | #FAFAFA | headings, stat values |
| `text.secondary` | #737373 | #A1A1A1 | descriptions, captions, table meta |
| `text.tertiary` | #8C8C8C | #737373 | placeholder-adjacent meta only; 3:1 house floor, never body copy |
| `text.disabled` | #D4D4D4 | #525252 | disabled controls (inactive-component exemption; state must be stated in text) |
| `status.success` | #009669 | #00D294 | solid dots/glyphs; light-mode label ink is `status.success.ink` |
| `status.success.ink` | #005F46 | #A4F4CF | success text on wash or canvas |
| `status.warning` | #FA8900 | #DB6809 | warning solid; too light for solo use on light canvas — always glyph+label |
| `status.warning.ink` | #8F5000 | #FF8B1F | warning text on wash/canvas (calibrated; upstream step #BD6500 fails 4.5) |
| `status.error` | #FB2C36 | #E40016 | destructive plate is #E40016 in both modes; solid dots pass 3:1 in light |
| `status.error.ink` | #BF000F | #FF6568 | danger text on wash/canvas |
| `status.info` | #00A5EA | #00A5EA | info dots/links in charts; solo use dark mode only |
| `link.default` | #193CB8 | #56A2FF | inline links and info text; underlined in prose |

Dark canvas is **not** pure black: `#030303` canvas, `#0F0F0F` raised, `#262626` tint/hairline —
depth in dark comes from surface steps plus a 1px `#333333` edge and a 10% white keyline, never
from colour-cast shadows.

**Contrast gate — computed, unrounded.** Body ≥4.5:1; UI boundaries and focus ≥3:1; large text
≥24px or ≥18.5px at 600 weight.

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| `text.primary` (L) | #18181B | `surface.canvas` (L) | #FBFBFB | 17.11:1 | 4.5 | PASS |
| `text.secondary` (L) | #737373 | `surface.canvas` (L) | #FBFBFB | 4.57:1 | 4.5 | PASS |
| `text.tertiary` (L) | #8C8C8C | `surface.canvas` (L) | #FBFBFB | 3.24:1 | 3.0 (house meta floor) | PASS — meta/labels only, banned from body |
| `text.primary` (D) | #F5F5F5 | `surface.canvas` (D) | #030303 | 18.88:1 | 4.5 | PASS |
| `text.secondary` (D) | #A1A1A1 | `surface.canvas` (D) | #030303 | 7.94:1 | 4.5 | PASS |
| `text.tertiary` (D) | #737373 | `surface.canvas` (D) | #030303 | 4.35:1 | 3.0 (house meta floor) | PASS — also clears 4.5-adjacent use at 14px |
| `text.secondary` (L) | #737373 | `surface.hover` (L) | #F5F5F5 | 4.34:1 | 4.5 | FAIL for body — hover/tint surfaces carry `text.primary` (#18181B, 16.26:1) for anything readable; secondary allowed only for supplementary meta |
| `accent.onAction` | #FFFFFF | `accent.action` (L) | #056DFF | 4.53:1 | 4.5 | PASS |
| `accent.onAction` | #FFFFFF | `accent.action` (D) | #0462E5 | 5.39:1 | 4.5 | PASS |
| `accent.onAction` | #FFFFFF | `accent.action` hover | #1447E6 | 6.82:1 | 4.5 | PASS |
| `accent.onAction` | #FFFFFF | destructive plate | #E40016 | 4.89:1 | 4.5 | PASS — destructive plate uses the deep step in **both** modes; the bright #FB2C36 with white ink is 3.82:1 and is banned as a plate |
| `border.strong` (L) | #8F8F8F | `surface.raised` (L) | #FFFFFF | 3.23:1 | 3.0 | PASS |
| `border.strong` (D) | #6B6B6B | `surface.raised` (D) | #0F0F0F | 3.59:1 | 3.0 | PASS |
| `border.focus` (L) | #262626 | `surface.raised` (L) | #FFFFFF | 19.79:1 | 3.0 | PASS |
| `border.focus` (D) | #E9E9E9 | `surface.raised` (D) | #0F0F0F | 15.80:1 | 3.0 | PASS |
| `status.success.ink` (L) | #005F46 | success wash (L) | #EBFDF1 | 7.26:1 | 4.5 | PASS |
| `status.warning.ink` (L) | #8F5000 | warning wash (L) | #FFFAEA | 6.08:1 | 4.5 | PASS (upstream #BD6500 = 4.01:1 fails — replaced) |
| `status.error.ink` (L) | #BF000F | danger wash (L) | #FFF3F3 | 6.02:1 | 4.5 | PASS |
| `link.default` (L) | #193CB8 | info wash (L) | #EFF6FF | 8.10:1 | 4.5 | PASS |
| `status.success.ink` (D) | #A4F4CF | success wash (D) | #0F1D15 | 13.59:1 | 4.5 | PASS |
| `status.warning.ink` (D) | #FF8B1F | warning wash (D) | #2A1C0A | 7.09:1 | 4.5 | PASS |
| `status.error.ink` (D) | #FF6568 | danger wash (D) | #270D0D | 6.39:1 | 4.5 | PASS |
| `link.default` (D) | #56A2FF | info wash (D) | #12192B | 6.72:1 | 4.5 | PASS |
| `status.success` solid (L) | #009669 | `surface.canvas` (L) | #FBFBFB | 3.63:1 | 3.0 | PASS (dot/glyph) |
| `status.error` solid (L) | #FB2C36 | `surface.canvas` (L) | #FBFBFB | 3.69:1 | 3.0 | PASS (dot/glyph) |
| `status.warning` solid (L) | #FA8900 | `surface.canvas` (L) | #FBFBFB | 2.35:1 | 3.0 | FAIL solo — warning solid never appears without a glyph + label in light mode |
| `status.info` solid (L) | #00A5EA | `surface.canvas` (L) | #FBFBFB | 2.67:1 | 3.0 | FAIL solo — info solid restricted to dark mode and chart series with legend |
| `accent.brand` as text (L) | #F6821F | `surface.canvas` (L) | #FBFBFB | 2.49:1 | 4.5 | FAIL as text — orange ink is decorative/logo-only in light; dark mode orange text passes (7.97:1) |

## 4. Typography

**Families.** UI: **Inter** variable, weights 400 (body) / 500 (emphasis, buttons, labels) /
600 (headings — bold is banned; 600 is the ceiling), self-hosted, preloaded with the app shell,
fallback system-ui. Feature settings pin `cv02 cv03 cv04 calt`; global tracking −0.01em and never
adjusted per element. Numeric/code: **system monospace stack** (ui-monospace, SF Mono, Menlo,
Consolas) for identifiers, zone names, IPs, record contents, hashes, raw timestamps and log
lines; inline mono shrinks to 0.9em so it optically matches the surrounding 14px. Monospace is
for identifiers and code, never a costume.

**One ramp table per class, not one blended table.**

- **[F] Focused, 16px base** — onboarding, destructive confirmations, plan change:

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Display | 30px | 600 | 1.2 | −0.01em | — | dialog titles, plan change headline |
| Heading | 20px | 600 | 1.3 | −0.01em | — | section headings in focused flows |
| Body | 16px | 400 | 1.5 | −0.01em | — | confirmation copy, explanations |
| Label | 14px | 500 | 1.45 | −0.01em | — | form labels, button ink |
| Meta | 13px | 400 | 1.45 | −0.01em | — | helper text under fields |

- **[S] Standard, 14px base** — zone overview, security overview, settings, account home:

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Page title | 24px | 600 | 1.25 | −0.01em | — | "DNS records for example.com" |
| Section title | 18px | 600 | 1.35 | −0.01em | — | card headings |
| Body | 14px | 400 | 1.5 | −0.01em | — | descriptions, empty-state copy |
| Row primary | 14px | 400–500 | 1.45 | −0.01em | — | table cell text, list item titles |
| Row secondary | 13px | 400 | 1.45 | −0.01em | — | sub-labels, record content mono |
| Stat value | 24–32px | 600 | 1.2 | −0.01em | tabular | traffic totals, request counts |
| Stat label | 13px | 500 | 1.45 | +0.01em | — | uppercase eyebrows above stats are banned — sentence case only |
| Meta | 12px | 400 | 1.4 | −0.01em | — | timestamps, "3 rules allowed" |

- **[D] Dense, 12–13px base, data surfaces only** — DNS records grid, log explorer, audit log,
  analytics tables:

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Grid header | 12px | 500 | 1.4 | −0.01em | — | column heads, sentence case |
| Grid cell numeric | 13px | 400 | 1.4 | −0.01em | tabular | TTL, counts, packets |
| Grid cell text | 13px | 400 | 1.4 | −0.01em | — | names, types, statuses |
| Log line | 12px | 400 | 1.5 | 0 | tabular | mono, no negative tracking |
| Inline help | 12px | 400 | 1.45 | −0.01em | — | hints inside dense panels |

Prose inside a dense screen (an explainer paragraph on the log explorer) still steps up to 14px.

**Invariants.** `tabular-nums` on every comparable value — currency, timestamps, deltas, counts,
zone IDs. Right-align numerics, left-align text, never centre a numeric column. Fixed stepped
sizes; no fluid scaling between steps. Measure ≤80 characters for prose (65–80ch [F/S]);
data surfaces are unconstrained. Headings sentence case always; product names keep their
capitalisation ("Magic Transit", "Workers").

## 5. Spacing Scale & Density Scales

**Spacing base: 4px grid; 8px rhythm [F/S], 4px [D].** `space.0` 0 · `space.1` 4px icon-to-label ·
`space.2` 8px control padding [D], tight intra-card gaps · `space.3` 12px cell padding [S],
button inline padding [base] · `space.4` 16px card padding [S] + page gutter [D] · `space.5`
20px large-control padding · `space.6` 24px card padding [F] + section gap · `space.8` 32px
section gap [S] · `space.12` 48px region separation. No 17px, no 23px — if a layout needs an
off-scale value, the layout is wrong. Vertical spacing runs slightly tighter than horizontal
around text blocks to compensate for line-height air.

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | destructive confirmations, plan change, onboarding |
| `standard` | 40–44px | 14px | 12–16px | 24px | zone overview, security overview, settings, account home |
| `dense` | 28–32px | 12–13px | 8px | 16px | DNS records, log explorer, audit log, analytics tables, member lists |

- Density comes from row height, column pruning and leading — never from unreadable type. A
  13px tabular numeral in the DNS grid is correct; the same numeral in the plan-change dialog is
  a defect.
- **Never switch mid-page.** The DNS grid is dense edge to edge; switching to standard inside the
  same scroll is a rhythm break. Switching across routes with different jobs is legitimate — the
  log explorer should feel like a different room from the zone overview.
- **Chrome follows rows.** Table header, filter toolbar, batch bar and pagination heights match
  the row height of their table: 32px header over 32px rows [D]; 40px toolbar over 40px rows [S].
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40% — validated against the
  screens/ captures.

## 6. Radius Scale

`none` 0 table edges and log gutters · `xs` 2px status dots and tiny tags · `sm` 4px micro
buttons (20px), inline code, checkboxes · `md` 6px compact controls (26px buttons, small inputs)
· `lg` 8px default buttons (36px), inputs, cards, panels, table shells · `xl` 12px dialogs,
popovers, toasts, drawers · `full` pills for badges, status, avatars, and the toggle track.
One radius per component family — buttons are 8px at every size above compact; a card that nests
an 8px inner button obeys the concentric rule: `radius_inner = radius_outer − padding` (a 12px
popover with 4px padding wraps 8px children).

## 7. Elevation

**One strategy per mode, never mixed paradigms.**

- **Light** — multi-layer shadow + faint hairline: level 1 shadow is a 12%-black 1px edge plus an
  8%-black drop; hairline borders and shadows never combine on the same element (an element with
  a visible border uses the border alone; an elevated floating surface uses the shadow ring).
- **Dark** — surface-luminance steps + 1px strokes + a 10% white edge highlight; shadows remain
  available as a 30% black drop for true overlays but never carry depth alone.
- Levels, low → high: **0** `surface.canvas` (no shadow) · **1** `surface.raised` cards/panels
  (shadow-xs + `border.subtle`) · **2** sticky table header/toolbar (edge + drop + `border.subtle`
  bottom stroke separating it from scrolling content) · **3** `surface.overlay` popovers/menus
  (stronger drop, 12px radius) · **4** dialog/scrim (strongest drop, 12px radius, scrim at 50%
  black in light, 60% in dark).

## 8. Motion

`instant` 0ms — **all hover and focus colour changes; a 300ms hover transition is a defect** ·
`fast` 120ms ease-out — [D] exits, tooltip dismissal · `base` 180ms decelerate — [D] entrances,
popover open, row expansion · `slow` 240ms decelerate — [F/S] entrances, dialog open/close.

- Entrances decelerate, exits accelerate; symmetric ease-in-out on both directions is a defect.
- Animate transform and opacity only — never width, height, top, left; collapsible panels keep
  their inner content width fixed while closing so surrounding layout never reflows.
- Overlays stay mounted through their exit animation — unmounting on state change kills the
  closing animation.
- No bounce on irreversible moments: not the confirm-delete dialog, not the plan downgrade.
- **Reduced motion is a real variant:** the dashboard's few large movements (skeleton sweep,
  dialog scale, chart draw-in) collapse to a ~150ms crossfade; fades themselves remain. The
  trigger set is scaling and panning of large objects, not every fade.

## 9. Imagery & Art Direction

**Policy, not asset list.**

- **Brand moment:** the marketing site (cloudflare.com) — full-bleed orange canvas with halftone
  texture, white display headline, white pill CTA. Inside the dash, the one sanctioned saturation
  moment is the **orange proxy cloud** and occasional promo/tour cards (the orange-gradient
  dashboard-tour tile); their palette never leaks into UI tokens. Data surfaces are achromatic
  plus status hues.
- **Iconography:** a single 24px-grid line-icon family (Phosphor-class strokes ≈1.5px at 24px),
  geometric, matched to Inter's tone; 16px optical size inline with text. In dark mode nav icons
  render as outlines — only the selected app switches to filled, and hover shows fill. Icon-only
  controls always carry a tooltip label.
- **Photography:** none in product UI. Third-party logos (registrar partners, integrations) render
  monochrome inside a committed surface, never in brand colour.
- **Illustration:** flat geometric brand illustration reserved for marketing and empty-state art in
  focused surfaces; never inside dense data surfaces.
- **Empty / error art:** the empty state names what is missing ("No DNS records on this zone") and
  carries the fixing CTA ("Add record") — illustration never substitutes for the recovery action.
  If no illustration ships for a surface, a typographic empty state is the default; per-screen
  invention is banned.

## 10. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell / sidebar | S | account rail + zone rail; grouped nav (Protect & Connect / Build / Analyze) | active (filled), hover, collapsed | arrows traverse; Tab reaches skip link | product names, sentence case; "New"/"Beta" pill markers |
| Zone switcher | S | account home top bar | open, filtered, recent zones | type-ahead, Enter selects | zone name + plan pill |
| Quick search (command palette) | S | global ⌘K launcher | loading, empty ("No results for …"), recent | full keyboard, Esc closes | "Search zones, DNS, Workers…" |
| Data table | S/D | striped (elevated even rows), compact header; sticky columns with 24px gradient fade | hover, selected, loading skeleton, empty, error, offline-stale | arrows between cells, Space selects, Enter opens | column heads sentence case; count line "8 records" |
| Proxy status toggle | S/D | Proxied (orange fill) / DNS only (grey outline) | on, off, pending, blocked by plan | Space toggles, focus ring 2px | label always visible: "Proxied" / "DNS only" |
| Filter/search bar | S/D | free-text + facet chips | active, filled, cleared | Enter applies, Esc clears | "Search DNS Records", "Add filter" |
| Row action menu | S/D | kebab overflow | focus-trap open, Esc closes, disabled items state why | arrows, Enter, Esc | "Edit", "Delete", "Duplicate" |
| Stat tile | S | with sparkline / plain; selected tile carries blue outline | loading, stale ("Last updated …") | tabbable, value announced | "Total requests", tabular value |
| Timeseries chart | S/D | line, stacked bar, sankey, map | loading, partial ("Some data delayed"), empty range | legend items tabbable; table fallback | legend glyph + label; "Drop"/"Pass" |
| Drawer / inspector | S | right-side record editor | open, dirty, saving, error | Esc closes with dirty-confirm | "Edit DNS record" |
| Dialog | F | confirmation, form, destructive | open, closing, blocking | focus-trap, Esc (except blocking), Enter submits | destructive names the resource: "Delete A record www?" |
| Plan / seat control | F | plan card + "Change" button | confirming, prorating, blocked (states why), success | tab order card → CTA | names cost + effective date |
| Member row | D | list row with role select | pending invite, removing, role-changed | row actions keyboard-reachable | role names sentence case |
| Audit entry | D | log line + expandable diff | expanded, filtered | Enter expands | actor + action + resource + time, tabular |
| Toast | S | success, warning, error, with action | auto-dismiss 6s, hover pauses | arrow to action | "DNS record created" + Undo |
| Badge / status pill | S/D | semantic tints, dashed beta, dot+word zone status | static, hover-linked | non-interactive (or link) | "Active", "Pending", "Moderate", "Beta" |

**Every fetching surface also designs:** loading (skeleton matching final geometry — the DNS grid
loads row-shaped bars, never a centred spinner on a blank page), empty (what's missing + the CTA
that fixes it), error (what happened + retry + support link), offline/stale (banner "Showing data
as of 14:32 — live data unavailable").

**Contracts this table encodes:** one primary filled CTA per view [F/S]; dense toolbars may pair
the primary ("Add record") with bordered secondaries ("Filters", "Export"); every icon-only
control carries a tooltip; a disabled control states why on focus ("Upgrade to Pro to edit
Worker routes") rather than sitting silently dead; a button never changes width between idle and
loading — the spinner reserves the label's space.

## 11. Light / Dark Strategy

- **Posture: C dual-parity.** Both modes are first-class, light is the default for new sessions,
  and the user's choice persists (appearance card in the profile; historically stored with the
  session). Reason: operators run the dash at 3 a.m.
- **Mechanism:** semantic roles remapped per mode through paired custom properties resolved by
  the root mode attribute; **no role absent in either mode** — the luminosity-reversal rule
  guarantees every hue role re-binds instead of disappearing. No mode-conditional component
  styling is permitted anywhere below the token layer.
- **`color-scheme`** is set on the root element so UA chrome, form controls and scrollbars follow
  the mode; it repaints UA-provided parts of the canvas and does not theme the document itself —
  the semantic layer does that.
- **A mode meta declaration sits in the document head before the stylesheet** to prevent a flash
  of the wrong scheme on first paint.
- **Dark is authored, not inverted:** its own surface ramp (`#030303 → #0F0F0F → #262626`), its
  own border strength (dark hairlines are *stronger*: a hairline that reads as delicate on white
  disappears on near-black, so dark line tokens step up), its own shadow policy (white edge +
  30% black drop), and its own icon policy (outlines with selected-fill only). `light-dark()`
  pairing is progressive enhancement for the token layer, not the mechanism the root attribute
  drives.
- **Org-tinted theme (D) exists and proves the freeze:** the FedRAMP theme re-binds colour
  primitives only; radii, type sizes, spacing and layout geometry are frozen so a theme swap
  cannot move anything.

## 12. Density-Mode Strategy

- **Default mode per surface class:** Standard is the default for zone/account surfaces; Dense is
  the default wherever the job is scanning rows (DNS records, logs, audit, analytics tables); the
  boundary is the job, not the viewport.
- **Mechanism:** a density attribute on the app root rescales row height, cell padding, gutter
  and body size together as a token axis — spacing tokens do not change per screen size or media
  query; the axis is declared once at the root and inherited.
- **Container queries for reflow:** components reflow to their container, not the viewport — the
  analytics grid's chart column collapses to a stacked layout when its card narrows, regardless
  of window size. Size queries fail closed with no eligible container, so container units are
  never used where that fallback would be wrong.
- **Style queries** compare computed values, so the density marker is a registered custom
  property with declared syntax and inheritance.
- **The switch is an accessibility affordance, not a preference:** dense tables can be stepped to
  standard row height per user; W3C guidance on target size endorses exactly such a density
  control for users with visual field loss.

## 13. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA contrast (7:1) for body copy in reading surfaces
  (documentation cards, empty-state prose).
- **Target size:** ≥24×24 CSS px hard minimum (SC 2.5.8); 36px buttons and 40px rows are the
  design target [F/S]; dense grids keep 28–32px rows with full-width row hit areas. Zoom does not
  excuse it.
- **Keyboard:** every function operable (SC 2.1.1) — the command palette, row menus, drawer and
  dialogs are fully keyboard-driven; focus indicator is the 2px `border.focus` ring, never
  suppressed without a stronger replacement; the focused row is never entirely hidden behind the
  sticky header (SC 2.4.11) — sticky containers scroll the focused cell into view.
- **Contrast:** text ≥4.5:1 (gate table §3, computed); UI boundaries and focus indicators ≥3:1 —
  which is why `border.strong` exists as a committed-boundary token distinct from the decorative
  hairline. **Colour independence:** every status pairs colour with a glyph or word ("Proxied",
  "Active", "Pending"); chart deltas carry direction glyphs; the proxy toggle's two states differ
  by fill *and* label.
- **Motion:** the §8 reduced-motion variant per component; no parallax anywhere.
- **Text:** ≤80-character measure for prose, 1.5 leading, 200% resize without horizontal scroll
  (SC 1.4.8) — tables scroll horizontally inside their own region, never the page.
- **Semantics:** real buttons, links and inputs; table regions expose row/column roles; headings
  match visual rank; live regions announce "zone created" class updates politely; loading regions
  set busy state.
- **Contrast preference:** `prefers-contrast: more` promotes `border.strong` to `text.secondary`
  strength and removes tint fills behind text; honoured on all data surfaces.

## 14. Anti-Patterns

**Do**
1. Keep orange for the brand and blue for actions — the dash reads calmer and the CTA is always
   findable.
2. Set body copy at 14px and reserve 16px+ for headings — the 14px rule is the system's density
   backbone.
3. Use 600 for headings and 500 for emphasis — bold is banned; the ladder has exactly three
   weights.
4. Make hover changes instant — perceived responsiveness of a console is set by hover latency.
5. Pair every status colour with a glyph or word — colour alone fails 1.4.1 and the dark canvas.
6. Keep tabular numerals on every count, TTL, timestamp and currency — columns must align.
7. Match chrome heights to row heights — a 40px toolbar over 32px rows is a rhythm break.
8. Keep the dashed-outline pill as the only beta marker — it is recognisable without colour.
9. Reserve the orange-gradient moment for promo/tour cards and never let it touch data surfaces.
10. State why a control is disabled, on focus — the plan-gated features are the classic case.
11. Author dark mode with its own ramp and edge highlights — a filtered dark mode washes out.
12. Use the concentric-radius rule when nesting — outer = inner + padding, always.

**Don't**
1. No marketing aesthetics inside the product: no full-bleed orange canvases, no halftone
   textures, no display typography in data surfaces.
2. No card inflation — cards sit on hairlines; a card inside a card is banned (headings go
   outside the card).
3. No stat-card dashboards as page filler — stats live in tiles with sparklines tied to charts.
4. No modals as connective tissue — flows use drawers and pages; dialogs are for confirmation and
   blocking choices.
5. No two filled primaries side by side; ghost/bordered secondaries take the rest.
6. No toolbar of unlabelled icons — every icon-only control has a tooltip.
7. No hover-only affordances — touch and keyboard must reach every action.
8. No placeholder-as-label — labels sit above inputs; placeholder text is example content.
9. No whole-page spinners — skeletons match final geometry.
10. No native confirm/alert — destructive flows get a dialog naming the resource.
11. No tiny type as a density strategy — density comes from row height and pruning.
12. No slow colour transitions, no bounce on irreversible actions, no un-themed raw hues inside
    components (the lint rule is part of the spec, not a nicety).
13. No `#BD6500`-class warning ink on light washes — the calibrated `#8F5000` step replaces it
    (4.01:1 fails; 6.08:1 passes).

## 15. Quick Reference & Verification Gate

**Colour (role → hex, light / dark):** canvas `#FBFBFB / #030303` · raised `#FFFFFF / #0F0F0F` ·
overlay `#F7F7F7 / #262626` · inset `#F2F2F2 / #0B0B0B` · hover/tint `#F5F5F5 / #262626` ·
hairline `#E9E9E9 / #262626` · strong boundary `#8F8F8F / #6B6B6B` · focus `#262626 / #E9E9E9` ·
action `#056DFF / #0462E5` (hover both `#1447E6`) · onAction `#FFFFFF` · brand `#F6821F` ·
primary ink `#18181B / #F5F5F5` · secondary `#737373 / #A1A1A1` · tertiary `#8C8C8C / #737373` ·
disabled `#D4D4D4 / #525252` · success `#009669/#005F46 · #00D294/#A4F4CF` · warning
`#FA8900/#8F5000 · #DB6809/#FF8B1F` · error `#FB2C36/#BF000F · #E40016/#FF6568` · info
`#00A5EA · link #193CB8/#56A2FF`.

**Type ramp:** Inter 400/500/600, tracking −0.01em; 12 / 13 / 14 base / 16 / 18 / 20 / 24 / 30;
16px+ headings only; mono for identifiers at 0.9em inline, 12–13px in logs.

**Spacing + radius:** 4px grid; 8/12/16/24/32/48 in use; rows 40px [S] / 28–32px [D]; buttons
36px (26 compact, 20 micro); radii 2 / 4 / 6 / 8 / 12 / pill; concentric nesting subtracts
padding.

**Component → token map:** button-primary → `accent.action + accent.onAction + radius.lg` ·
button-secondary → `surface.raised + border.strong ring + surface.hover on hover` ·
button-destructive → `status.error plate (#E40016) + accent.onAction` · table row →
`surface.raised + border.subtle + surface.hover/selected` · stat tile → `text.strong value +
text.secondary label` · badge → tint fill + status ink + `full` radius · proxy toggle →
`accent.brand vs paper-300 + label` · dialog → `surface.raised + radius.xl + scrim` · skeleton →
`paper-300 / night-700` · log line → mono on `surface.canvas`.

**Agent prompt block.**
Tokens: canvas `#FBFBFB/#030303`; raised `#FFFFFF/#0F0F0F`; action blue `#056DFF/#0462E5`, hover
`#1447E6`; brand orange `#F6821F` (logo/proxy/promo only, never light-mode text); primary ink
`#18181B/#F5F5F5`; secondary `#737373/#A1A1A1`; hairline `#E9E9E9/#262626` (decorative);
committed boundary `#8F8F8F/#6B6B6B`; focus ring `#262626/#E9E9E9` 2px; success
`#009669/#00D294`, warning `#FA8900/#DB6809` (light solid never solo), error plate `#E40016`
both modes; links `#193CB8/#56A2FF`. Type: Inter, 400/500/600 only, −0.01em, 14px base, 16px+
headings only, sentence case, tabular numerals on all comparable values, mono for identifiers.
Space: 4px grid; rows 40px standard / 28–32px dense; buttons h36 (26/20 compact); gutters 24 [S]
/ 16 [D]. Radii: 8 default, 12 dialogs/popovers, 4 micro/inline-code, pill badges; outer = inner
+ padding when nesting. Motion: hover instant; entrances 180ms decelerate; dialogs 240ms;
reduced motion → 150ms crossfade. Cite token names, never raw hex, in prompts below.

**Example component prompts.**
1. *Zone overview (Security class)* — `surface.canvas` background; page title 24px 600 in
   `text.primary`; content cards on `surface.raised` with `border.subtle` hairlines and 8px
   corners, `space.6` padding; one `accent.action` filled CTA top-right; stat tiles carry 28px
   tabular values over `text.secondary` labels; chart series use scale hues with glyph-paired
   legends; no shadow above level 1.
2. *DNS records grid (Dense)* — 32px rows on `surface.raised`; 13px cells, tabular numerals for
   TTL and counts, right-aligned; 12px sentence-case headers on a 32px header matching row
   height; hover fill `surface.hover`; selected row `surface.selected`; sticky columns end in a
   24px gradient fade to the row background; the proxy column pairs the orange cloud glyph with
   its word; row menu opens a focus-trapped popover, Esc closes.
3. *Delete-record dialog (Focused)* — `surface.raised` plate, 12px corners, scrim at 50/60%;
   title names the resource ("Delete A record for www.example.com?"); body 16px; destructive
   button uses `status.error` plate with white ink (4.89:1) and a bordered Cancel; focus starts
   on Cancel; Enter does nothing until the resource name is repeated in the confirm field for
   account-level resources.

**Pre-ship checklist.** 1 Zero raw hex outside L1. 2 No token resolves to a component name.
3 Every contrast pairing computed, passing, unrounded — including the two solo-solid
restrictions recorded in §3. 4 Every semantic role has a value in every shipped mode and theme
(default + FedRAMP). 5 Every fetching surface has loading/empty/error/offline specified.
6 Every component row lists disabled and loading states. 7 Row, header, toolbar and pagination
heights agree. 8 Reduced-motion variant written for every authored motion. 9 Every control
keyboard-reachable with a visible focus indicator. 10 Dark authored, not filtered, with border
strength exceeding light's and the outline-icon nav rule intact. 11 No unoverridden stock
library default inside a committed surface. 12 Nothing came from a marketing page — the §9
brand-moment palette appears nowhere in the UI token layers. 13 Hover transitions are absent
(instant) everywhere. 14 Warning text uses the calibrated deep step, never the 4.01:1 upstream
value.
