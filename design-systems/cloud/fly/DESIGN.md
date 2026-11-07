# Design System — Fly.io Dashboard (fly.io/dashboard)

<!-- premium-web-design:design-system 2 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: fly.io official site CSS (violet primitive ramp #7C3AED family, Fricolage Grotesque / Mackinac / Fragment Mono type stack, gradient wash pair #F5F3FF→#EEF2FF, night dev-tools set #0F0A20 — rung 2, extracted from the production stylesheet at fly.io/phx/assets/app-*.css), screens/ captures of the live dashboard (fly.toml configuration, Machines list with process-group drawer, Machine detail, Managed Postgres cluster overview, billing chooser, Activity feed) downloaded from official changelog posts — rung 3 grounding, plus fly.io og image (marketing gradient + Mackinac serif + watercolor balloon art). Ladder: rung 1 missed (no sibling spec); rung 2 supplied the primitive palette, type stack and brand posture; rung 3 grounded the dashboard-specific surfaces (the marketing stylesheet alone under-specifies table rows, status pills and drawers). -->
<!-- Surface classes: 15 routes classified; density classes F/S/D assigned (F sign-up/launch wizard/destructive confirmations; S app overview, machines, machine detail, fly.toml config, certificates, volumes, secrets, activity, Postgres overview, billing, org settings; D metrics, logs and errors, audit/registry tables) -->

## 1. Design Posture & Atmosphere

Fly.io's pitch is physical: run your app on hardware-isolated VMs in cities close to your users.
The dashboard inherits that geography-as-product framing but refuses the usual cloud-console
drama. Its posture is **a ground-control postcard** — the canvas is a soft paper-white lavishly
washed with violet gradients (the same family as the brand balloon), cards sit on it like
index cards pinned to a board, and every identifier — machine ID, version, image digest, IP,
lease token — renders in a crisp monospace as if typed on a field tag. Whimsy lives in the
brand layer: watercolor balloons, islands, planets and a purple elephant populate marketing
surfaces, docs heroes and og images. Inside the product those paintings stop at the frame;
data surfaces are calm, letter-spaced, and ruthlessly tabular. After eight hours on call the
dashboard reads as a well-lit flight operations room with postcards on the wall — not as a
nightclub, and not as a beige enterprise admin.

The central colour decision mirrors sibling consoles but inverts their polarity: the brand is
an unapologetic violet (`#7C3AED` drives primary buttons, links, focus rings, selection pills
and sparklines) laid over a canvas that is **lavender-tinted white, not grey, not dark**.
Where AWS goes slate-blue and GCP goes card-heavy material, Fly goes warm-paper violet with
one saturated indigo exception — the process-group drawer header — that reads as a deliberate
"focus hood" over the page. Status is quiet: a mint wash pill with a green dot says Deployed;
a grey pill says Suspended; nothing blinks. Theloudest element on any screen is a 28px tabular
numeral in a stat tile or a violet sparkline.

Contrary to the popular impression of a "dark purple" cloud product, the shipped dashboard is
**light-only**: the deep purples (`#110E1A`, `#121226`, `#281950`) belong to the marketing
gradient, the og images and the embedded developer-tools surfaces (terminal, Grafana metrics),
not to the product chrome. No official dark mode had shipped as of this writing — community
threads in November 2025 and September 2026 still request one, and the surviving community
userstyle explicitly preserves the violet branding while darkening the canvas. The spec below
therefore describes a single-mode system with two *guest* dark surfaces (Grafana embeds and
terminal panels) whose palette is anchored, fenced, and forbidden from leaking back.

**Key Characteristics**
- Canvas is never neutral: a `#F9F9FD` paper base carries a soft violet-to-indigo gradient
  wash (`#F5F3FF` → `#EEF2FF`) radiating from the top corners; cards are pure `#FFFFFF` and
  never pick up the tint — the tint is the room, the cards are the paper.
- **Violet is the verb and the brand here** (unlike Cloudflare's split): `#7C3AED` paints
  primary buttons, links, active tabs, selection pills, focus rings and sparklines alike.
  Accent budget: one filled violet CTA per view [F/S]; a single alternate blue `#2563EB` is
  reserved for informational reloads ("new data arrived" banners), never for primary flow.
- Type is three-stack: **Fricolage Grotesque** (variable, self-hosted) for all UI text,
  **Mackinac** serif for marketing display moments only, **Fragment Mono** for every
  identifier — machine IDs, versions, image refs, IPs, leases, region codes' neighbours.
  14px is the dashboard body size; 16px appears only in focused flows.
- Identifiers are sacred: machine `e820213c24d438`, cluster `dzx6qo6m6mnrjpv5`, version `v2`,
  image `docker-hub-mirror.fly.io/library/nginx:alpine` — all Fragment Mono, all copyable,
  none translated into "friendly names".
- Status is a dot + word + wash pill (Deployed, Ready, Complete, Suspended, Uncordoned);
  regions are flag + IATA chip (ORD, GRU, DFW); versions are tiny `v2`/`v8` violet chips.
  Colour never carries status alone.
- Depth is hairlines on paper: 1px `#E1E4EF` strokes separate cards; shadows exist only on
  popovers, dropdowns and the drawer (levels 3–4). The gradient canvas itself does the lifting.
- Rows are 48px standard, 32px dense; chrome (breadcrumb bar, toolbar, pagination) always
  matches the row height of the table it serves.
- One saturated exception: the right-side inspector/drawer opens with an indigo `#4F46E5`
  header band and white type — the only place a second saturated hue leads a surface.
- Stat tiles pair an 11px uppercase letter-spaced label with a 28px tabular value and a
  violet sparkline; cost is always shown with currency and unit ("$282 USD", "0.02 of 2 vCPU").
- Marketing's dark gradient (`#121226` → `#282045`), watercolor art and Mackinac serif never
  enter product tokens; the guest dark surfaces (`#0F0A20` night, `#ECE9F7` ink) are fenced.
- Motion is nearly invisible: 120ms exits, 180ms entrances, 240ms drawer/dialog slides; hover
  fills are instant; reduced motion collapses everything to a 150ms crossfade.
- Empty states name the missing thing and offer the exact fixing action ("Launch a database",
  "Attach a certificate"); skeletons mirror final card geometry, never a lone spinner.

## 2. Token Architecture

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to
a **primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value* (`violet.600`), referenced only by L2.
  Violet ramp: `violet-800 #5B21B6` · `violet-700 #6D28D9` · `violet-600 #7C3AED` (brand
  primary) · `violet-500 #8B5CF6` · `violet-400 #A78BFA` · `violet-300 #C4B5FD` ·
  `violet-200 #DDD6FE` · `violet-100 #EDE9FE` · `violet-50 #F5F3FF`; indigo family
  `indigo-600 #4F46E5` (drawer header), `indigo-50 #EEF2FF`, `indigo-700 #3730A3`,
  `indigo-alt-600 #2563EB` (informational action); ink ramp `ink-950 #110E1A` ·
  `ink-900 #281950` · `ink-700 #2A1863` · `ink-500 #564B80` · `slate-violet-600 #706781` ·
  `slate-violet-500 #837EA6` · `slate-violet-400 #9698B6` · `slate-violet-350 #A39AC1` ·
  `slate-violet-300 #756B93`; paper ramp `paper-0 #FFFFFF` · `paper-25 #FCFCFF` ·
  `paper-50 #FAF9FF` · `paper-75 #F9F9FD` · `paper-100 #F5F3FF` · `paper-150 #F1F2F9`;
  hairlines `line-200 #E1E4EF` · `line-violet-200 #D9D0F0` · `line-violet-150 #D4CEEA` ·
  `line-lav-100 #E6E0ED`; night set `night-950 #0F0A20` · `night-ink #ECE9F7` ·
  `night-muted #9D95BB`; status `green-800 #166534` · `green-700 #15803D` · `green-600 #16A34A`
  · `green-500 #059669` · `green-100 #DCFCE7` · `amber-800 #854D0E` · `amber-700 #B45309` ·
  `amber-600 #D97706` · `yellow-100 #FEF9C3` · `rose-700 #BE123C` · `rose-600 #E11D48` ·
  `rose-100 #FFE4E6` · `rose-200 #FECDD3` · `blue-800 #1E40AF` · `blue-600 #2563EB` ·
  `blue-100 #DBEAFE`; marketing-only `dusk-950 #121226` · `dusk-900 #282045` ·
  `orchid-500 #B54FF3` · `code-violet #874BEE` · `sp-purple #7738EC`. Banned:
  component-named primitives (a `drawer-header` colour) — one value, many roles.
- **L2 Semantic** — role names (`surface.canvas`, `surface.raised`, `text.primary`,
  `accent.action`, `border.focus`, `status.success.ink`, `night.surface`). The only layer a
  component may consume. The product ships **one mode (light)**; every role therefore carries
  exactly one value and the mode axis is inert (§11). Guest surfaces (Grafana embeds, terminal)
  consume the fenced `night.*` roles and nothing else; those roles never bind to product
  components and product roles never bind inside guest surfaces.
- **L3 Component** — only for deliberate deviation, pointing at L2 or L1, never at a raw value
  and never at a sibling component's token: `nav.item → surface.selected pill + text.onSubtle`
  · `machine.id → Fragment Mono + accent.action ink + copy affordance` · `chip.version →
  accent.subtle fill + accent.onSubtle ink, radius.xs` · `chip.region → paper-150 fill +
  text.secondary ink + flag glyph` · `stat.tile → text.primary 28px tabular value +
  text.secondary uppercase label + accent.action sparkline` · `drawer.processGroup →
  indigo-600 header + paper-0 body` · `banner.stale → blue-100 wash + blue-800 ink +
  accent.alt action` · `button.danger → rose-100 fill + rose-700 ink` ·
  `code.field → paper-0 inset + line-200 border + Fragment Mono` ·
  `skeleton → paper-100 blocks with sweep`.

**Rules.** Every token has a determinable type (colour, dimension, font-family, duration,
easing) or it is invalid; names are case-sensitive and free of `$`, `{`, `}` and dots; circular
references are an error. Because the product ships light-only, the "every role in every mode"
rule is satisfied by the mode set itself — but the moment a dark mode lands (community demand
is explicit and on record), every role above must gain a night value before it ships; a role
absent in dark resolves to its light value and fails contrast, which is precisely the failure
the community userstyle fights today. Animatable tokens (skeleton sweep, drawer slide) are
declared with explicit syntax and inheritance flags; initial values are computationally
independent, so percentage-based initial values are illegal.

**Layer order (low → high):** `reset → primitives → semantic → components → utilities`. Order
beats specificity entirely, so a stray un-layered declaration inside a component file would
outrank the whole system; anything a consumer must override without forcing priority lives in
the top layer. A lint rule flags any raw colour consumed directly by a component, and a second
rule flags any `night.*` role referenced outside the two guest surfaces — the fence is
mechanical, not aspirational.

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` | #F9F9FD | — (light-only) | page base; violet wash gradient painted over it (§1) |
| `surface.raised` | #FFFFFF | — | cards, tables, drawers, popovers |
| `surface.wash` | #F5F3FF | — | decorative gradient endpoint, empty-state fills, hover |
| `surface.inset` | #F1F2F9 | — | wells, code-field backdrops, skeleton base |
| `surface.hover` | #F5F3FF | — | row/menu hover fill (instant, no transition) |
| `surface.selected` | #EDE9FE | — | active nav pill, selected row |
| `border.subtle` | #E1E4EF | — | 1px card/table hairlines (decorative grouping) |
| `border.strong` | #706781 | — | input borders, dividers that must read as boundaries |
| `border.focus` | #7C3AED | — | 2px ring, 2px offset; never removed |
| `accent.action` | #7C3AED | — | primary CTA, links, active tab underline, selection |
| `accent.actionHover` | #6D28D9 | — | hover/active fill of primary CTA |
| `accent.onAction` | #FFFFFF | — | text/icons on filled violet |
| `accent.subtle` | #EDE9FE | — | version chips, tinted icon chips, checkbox fill |
| `accent.onSubtle` | #5B21B6 | — | ink on tinted chips/pills |
| `accent.alt` | #2563EB | — | informational reload actions only (stale-data banner) |
| `accent.header` | #4F46E5 | — | drawer header band, focus hood |
| `text.primary` | #281950 | — | headings, row titles, stat values |
| `text.secondary` | #706781 | — | body support, labels, table headers |
| `text.tertiary` | #837EA6 | — | metadata, timestamps; ≥3:1 floor holds (2.814 at #9698B6 fails) |
| `text.disabled` | #A39AC1 | — | exempt from SC 1.4.3 (inactive); pairs with reason-on-hover |
| `night.surface` | #0F0A20 | #0F0A20 | guest: terminal, Grafana embed backdrop |
| `night.ink` | #ECE9F7 | #ECE9F7 | guest: primary text on night surface |
| `night.muted` | #9D95BB | #9D95BB | guest: secondary text on night surface |
| `night.accent` | #8B5CF6 | #8B5CF6 | guest: links/highlights inside night surfaces |
| `status.success.ink` / `.wash` / `.dot` | #166534 / #DCFCE7 / #16A34A | — | Deployed, Ready, Complete, started machines |
| `status.warning.ink` / `.wash` / `.dot` | #854D0E / #FEF9C3 / #D97706 | — | pending certs, lease expiring |
| `status.error.ink` / `.wash` / `.dot` | #BE123C / #FFE4E6 / #E11D48 | — | failed deploys, crashed machines |
| `status.info.ink` / `.wash` / `.dot` | #1E40AF / #DBEAFE / #2563EB | — | running tasks, notices |

Dark canvas for guest surfaces is not pure black: `#0F0A20` is a violet-night. Depth in the
light product comes from the gradient wash plus 1px strokes, never shadows; guest night
surfaces use luminance steps (`night-950` wells under `night-ink` text) and carry zero shadows.

**Contrast gate — computed (WCAG 2.1 relative-luminance formula, unrounded):**

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| `text.primary` | #281950 | `surface.raised` | #FFFFFF | 15.612:1 | 4.5:1 | PASS |
| `text.primary` | #281950 | `surface.canvas` | #F9F9FD | 14.866:1 | 4.5:1 | PASS |
| `text.primary` | #281950 | `surface.wash` | #F5F3FF | 14.234:1 | 4.5:1 | PASS |
| `text.secondary` | #706781 | `surface.raised` | #FFFFFF | 5.322:1 | 4.5:1 | PASS |
| `text.tertiary` | #837EA6 | `surface.raised` | #FFFFFF | 3.818:1 | 3:1 house floor | PASS |
| `text.disabled` | #A39AC1 | `surface.raised` | #FFFFFF | 2.642:1 | exempt (SC 1.4.3 inactive UI) | PASS w/ note |
| `accent.onAction` | #FFFFFF | `accent.action` | #7C3AED | 5.699:1 | 4.5:1 | PASS |
| `accent.action` (link) | #7C3AED | `surface.raised` | #FFFFFF | 5.699:1 | 4.5:1 | PASS |
| `accent.action` (link) | #7C3AED | `surface.canvas` | #F9F9FD | 5.426:1 | 4.5:1 | PASS |
| `accent.onSubtle` | #5B21B6 | `accent.subtle` | #EDE9FE | 7.566:1 | 4.5:1 | PASS |
| `accent.alt` (link) | #2563EB | `surface.raised` | #FFFFFF | 5.169:1 | 4.5:1 | PASS |
| `border.strong` | #706781 | `surface.raised` | #FFFFFF | 5.322:1 | 3:1 | PASS |
| `border.focus` | #7C3AED | `surface.raised` | #FFFFFF | 5.699:1 | 3:1 | PASS |
| `status.success.ink` | #166534 | `status.success.wash` | #DCFCE7 | 6.492:1 | 4.5:1 | PASS |
| `status.warning.ink` | #854D0E | `status.warning.wash` | #FEF9C3 | 6.379:1 | 4.5:1 | PASS |
| `status.error.ink` | #BE123C | `status.error.wash` | #FFE4E6 | 5.235:1 | 4.5:1 | PASS |
| `status.info.ink` | #1E40AF | `status.info.wash` | #DBEAFE | 7.149:1 | 4.5:1 | PASS |
| `night.ink` | #ECE9F7 | `night.surface` | #0F0A20 | 16.195:1 | 4.5:1 | PASS |
| `night.muted` | #9D95BB | `night.surface` | #0F0A20 | 6.869:1 | 3:1 house floor | PASS |
| `status.success.dot` | #16A34A | `surface.raised` | #FFFFFF | 3.296:1 | 3:1 (glyph) | PASS |
| `status.warning.dot` | #D97706 | `surface.raised` | #FFFFFF | 3.186:1 | 3:1 (glyph) | PASS |
| `status.error.dot` | #E11D48 | `surface.raised` | #FFFFFF | 4.697:1 | 3:1 (glyph) | PASS |

Rejected candidates recorded with numbers: `text.tertiary` at the production muted
`#9698B6` computes **2.814:1** — fails the 3:1 muted-text floor, so the spec tunes the role to
`#837EA6` (3.818:1); `text.disabled` stays at `#A39AC1` (2.642:1) under the SC 1.4.3
inactive-component exemption but must always surface the reason on hover/focus. `border.strong`
inherited `#706781` after `#9698B6` failed the same gate. The production success ink `#15803D`
on `#DCFCE7` computes 4.567:1 — technically passing but inside the rounding trap, so the spec
binds the darker `#166534` (6.492:1) instead.

## 4. Typography

**Families.** UI **Fricolage Grotesque** (variable woff2, self-hosted and preloaded; weights
400/500/600/700; fallback: system humanist sans stack) — the friendly-but-precise grotesque
that carries every product surface. Display **Mackinac** (serif; medium 500 and bold 700,
self-hosted; marketing headlines and og art only — it never renders inside a data surface).
Numeric/code **Fragment Mono** (400 only, self-hosted) for identifiers, image refs, versions,
IPs, lease tokens, region codes' neighbours, log lines and terminal output. *Monospace is for
identifiers and code, never a costume* — prose in Fragment Mono is a defect.

**One ramp table per class, not one blended table.**

- **[F] Focused, 16px base** — sign-up, launch wizard, destructive confirmations:

| Role | Size/Line | Weight | Tracking | Numerals | Use |
|---|---|---|---|---|---|
| Display | 32/38 | 600 | −0.01em | — | wizard step titles, sign-up hero |
| Heading | 20/28 | 600 | 0 | — | form-group titles |
| Body | 16/24 | 400 | 0 | — | instructions, explanations |
| Label | 14/20 | 500 | 0 | — | field labels above inputs |
| Meta | 13/18 | 400 | 0 | tabular | hints, timeout formats, proration notes |

- **[S] Standard, 14px base** — the dashboard default (app overview, machines, config,
  Postgres, billing, activity):

| Role | Size/Line | Weight | Tracking | Numerals | Use |
|---|---|---|---|---|---|
| Page title | 24/30 | 600 | −0.01em | — | "Machines", "Billing" |
| Section title | 16/22 | 600 | 0 | — | card titles: "Deployment strategy", "Recent Events" |
| Body | 14/21 | 400 | 0 | — | card explanatory copy (1.5 leading) |
| Row primary | 14/20 | 500 | 0 | — | table first cell, list titles |
| Row secondary | 13/18 | 400 | 0 | tabular | sizes, relative times ("3 days ago") |
| Stat value | 28/32 | 600 | −0.01em | tabular | "0.8%", "8.5%", "$282", "17d 19h+" |
| Stat label | 11/14 | 500 | +0.05em, uppercase | — | "CPU USAGE", "EST. MONTHLY COST" |
| Meta | 12/16 | 400 | 0 | tabular | helper text under fields, event counts |

- **[D] Dense, 13px base, data surfaces only** — metrics panels, logs, registry/audit tables:

| Role | Size/Line | Weight | Tracking | Numerals | Use |
|---|---|---|---|---|---|
| Grid header | 12/16 | 500 | +0.04em, uppercase | — | "MACHINE", "REGION", "SIZE/CPU" |
| Grid cell text | 13/18 | 400 | 0 | — | non-numeric cells |
| Grid cell numeric | 13/18 | 400 | 0 | tabular | counts, sizes, percentiles |
| Log line | 12.5/18 | 400 | 0 | tabular | Fragment Mono, night surface |
| Inline help | 12/16 | 400 | 0 | — | chart footnotes, query hints |

*Prose inside a dense screen still steps up to the [S] Body role.*

**Invariants.** `tabular-nums` on every comparable value — cost, timestamps, sizes, counts,
percentiles, machine IDs. Right-align numerics, left-align text, never centre a numeric column.
Fixed stepped sizes; no fluid type. Measure ≤80 characters for prose [F/S] (§13); data surfaces
unconstrained. Identifiers always Fragment Mono at the surrounding size minus 0.5–1px optical
compensation, never bolded.

## 5. Spacing Scale & Density Scales

**Spacing base: 4px grid; 8px comfortable [F/S], 4px [D].** `space.0` 0 · `1` 4px icon-to-label
· `2` 8px control padding [D] · `3` 12px cell padding [S], table column gaps · `4` 16px card
padding [D] + inline gaps between sibling cards · `6` 24px card padding [S] + form row gaps ·
`8` 32px page gutter [F/S] + card stack separation · `12` 48px section separation on long
settings pages · `16` 64px rarely, marketing-adjacent pages only. *No `17px`. No `23px`. If a
layout needs an off-scale value, the layout is wrong.*

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | sign-up, launch wizard, destructive confirmations |
| `standard` | 48px (44 min) | 14px | 12px | 32px | app overview, machines, machine detail, fly.toml, Postgres overview, billing, activity |
| `dense` | 32px | 13px | 8px | 16px | metrics panels, logs & errors, registry/audit tables |

- Density comes from row height, column pruning and leading — never from type too small to
  read. A 13px tabular numeral in a dense Grafana-style table is correct; the same numeral as
  a billing line item is a defect.
- **Never switch mid-page.** The Machines list is standard top to bottom; the Metrics page is
  dense top to bottom. Switching across routes with different jobs is legitimate — it should
  feel like a different room.
- **Chrome follows rows.** Breadcrumb bar, table toolbar and pagination heights match the
  table's row height (48px standard, 32px dense).
- Whitespace budget: Focused 55–70% · Standard 40–55% (the Postgres overview sits near the
  airy end at ~55%) · Dense 25–40%. *House heuristic — validated against screens/ captures.*

## 6. Radius Scale

`none` 0 · `xs` 4px version chips, inline code, region flags · `sm` 6px inputs, selects,
steppers · `md` 8px buttons, table row-action buttons, banners · `lg` 14px cards, stat tiles,
drawers, dialogs, popovers · `full` 9999px status pills, org avatars, dot glyphs. **One radius
per component family**, never mixed ad-hoc: every card on a page is `lg`, every button `md`.
Nested radii obey `radius_inner = radius_outer − padding` — a `full` pill inside a `lg` card
uses its own full radius; a chip inside a 24px-padded card never exceeds 10px.

## 7. Elevation

**Strategy: hairlines-first paper.** Light product surfaces carry 1px `border.subtle` strokes
and no shadow through levels 0–2; shadows arrive only when an element detaches from the board
(popover, dropdown, drawer, dialog). Levels, low → high: **0** canvas (`#F9F9FD` + wash, no
shadow) · **1** card/stat tile (1px `border.subtle`, radius.lg, zero shadow) · **2** sticky
breadcrumb bar (paper-0 fill + `border.subtle` + the faintest 1px 2% ink shadow for lift) ·
**3** popover/dropdown/right drawer (shadow 0 8px 24px at 12% ink + `border.subtle`; the
process-group drawer adds its indigo header band) · **4** dialog/scrim (40% `#110E1A` scrim +
shadow 0 16px 48px at 18% ink). Guest night surfaces (terminal, Grafana) use luminance steps
and 1px `#9D95BB`-at-20% keylines with zero shadows — a drop shadow is invisible on
`#0F0A20`.

## 8. Motion

`instant` 0ms (hover fills, selection, tab underline) · `fast` 120ms ease-out (exits [D]:
row menus, tooltip fade) · `base` 180ms decelerate ([D] entrances, banner slide-down, chip
appear) · `slow` 240–300ms decelerate ([F/S] entrances, drawer slide-in, dialog scale-fade).

- Entrances decelerate, exits accelerate. Symmetric ease-in-out on both directions is a defect.
- Animate transform and opacity only — never width, height, top, left. The drawer slides on
  transform; the stale-data banner drops on transform+fade.
- No bounce on irreversible moments: not on "Change my repository", not on Scale plan
  confirmation, not on machine stop.
- Deploy/restore progress uses a 1.5s linear indeterminate sweep at 40% opacity — the only
  permitted loop — and it must be interruptible by screen reader announcement (§13).
- **Reduced motion is a real variant**: drawer slide, banner drop and dialog transitions
  collapse to a ≤150ms opacity crossfade; the indeterminate sweep becomes a static 40% fill
  with a text percentage. Vestibular triggers (scaling/panning large objects) are what get
  neutralised, not every fade.

## 9. Imagery & Art Direction

**Policy, not asset list.**

- **Brand moment:** the watercolor whimsy pack — balloons, floating islands, planets, the
  purple elephant, hand-lettered Mackinac headlines over a dusk gradient (`#121226` →
  `#282045`) — belongs to marketing pages, og/twitter cards, docs heroes and empty-state
  illustrations **only**. One saturation moment per surface. Its palette (dusk purples,
  watercolor greens and pinks, orchid `#B54FF3`) **never leaks into UI tokens** — the product
  ramp stays violet-on-paper; a watercolor pink in a data table is a review-blocking defect.
- **Iconography:** geometric 16px glyphs on a 20px chip grid. Product nav icons sit inside
  tinted chips (`accent.subtle` fill, `accent.onSubtle` glyph); machine-action toolbar icons
  are bare 16px strokes (`text.secondary`, `border.strong` chip on hover); drawer/dialog
  closes are bare glyphs. Filled variants only for status dots. Icon-only controls always
  carry a tooltip naming the action (§10, §13).
- **Photography:** none. Fly.io sells infrastructure, not offices.
- **Illustration:** the watercolor pack (above) plus tiny spot glyphs (balloon, globe) for
  empty states. Illustration never substitutes for the recovery CTA: every empty state pairs
  the art with "what's missing + the button that fixes it".
- **Third-party marks:** region flags render as emoji chips inside `paper-150` fills; GitHub
  and registry logos render monochrome inside committed surfaces; framework illustrations in
  guides (bookshelf watercolors) stay in docs, never the dashboard.

## 10. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| Top nav bar | S | guest/auth, org | idle | skip-to-content first | Dashboard · What's New · Resources · Account |
| Breadcrumb/status bar | S | org›app›page, org›app›resource | loading, stale | focus follows route | "Deployed" / "Suspended" pill rides right edge |
| Sidebar | S | app nav, Postgres nav, account nav | selected pill, hover, collapsed | arrow keys + tab | grouped: Overview / fly.toml / Machines / Volumes ⏵ Activity / Metrics / Logs & Errors ⏵ Certificates / Registry / Secrets / Tokens / Settings |
| Data table | S/D | machines list, billing orgs, certificates | hover, selected, loading skeleton, empty, error | header focusable, row actions via menu key | mono ID + version chip + region chip + relative time |
| Row action menu | S/D | icon buttons + kebab | focus-trap, disabled-with-reason | Esc closes | Stop, Clone, Restart, Terminal, Metrics |
| Stat tile | S | numeric, percent, cost, duration | loading, stale, error | — | label uppercase + 28px tabular value + sparkline |
| Card | S | config section, event feed, backup list | loading, empty, error | — | "Controls how a new release replaces the previous one" |
| Drawer/inspector | S | process group, machine create | open, saving, error, dirty-guard | Esc closes, focus returns | indigo header "Process group"; footer Cancel/Save |
| Dialog | F | destructive confirm, token reveal | scrim, confirming, blocked | focus-trap, Esc | restates resource name: "Scale plan for {app}?" |
| Form controls | F/S | input, select, stepper, checkbox | default, focus ring, error, disabled-with-reason | labeled, tabbable | "Timeout format: 5m, 300s, etc. Default: 5 minutes." |
| Status pill | S/D | Deployed, Ready, Complete, Suspended, Uncordoned | static | — | dot + word, wash fill, never colour alone |
| Version/region chip | S/D | v2 · v8 · ORD · GRU · DFW | static | — | flag glyph + IATA code |
| Code field | S/D | image ref, app id, lease | copy affordance, copied, overflow-ellipsis | copy on Enter | Fragment Mono + hash glyph + copy button |
| Banner (stale data) | S | "Release #11 just arrived — your config has been updated." | visible, dismissed | dismiss focusable | blue wash + "Load latest" accent.alt button |
| Progress banner | S | scale plan | running, complete "2/2 done", failed | — | "View details" / "Dismiss" ride right |
| Event feed entry | S | release, scale, settings change | avatar, expanded diff ("and 4 more") | expand on Enter | "Release by {user} — HTTP service v1 — 2 minutes ago" |
| Org avatar tile | S | letter on violet gradient | — | — | first letter of org name |
| Danger wash button | F/S | "Change my repository" | confirm double-press | — | rose wash, names consequence in body copy |
| Command palette | S/D | global actions | recent commands, no-results | global hotkey | "Type a command or search…" |
| Terminal panel (guest) | D | machine console | connected, reconnecting, closed | — | night surface, Fragment Mono, copy-safe |
| Metrics panel (guest) | D | Grafana embeds | loading, no-data, error | — | percentiles legend: p0.5/p0.95/p0.99/p0.999 |

**Every fetching surface also designs:** loading (skeleton mirroring final card/table geometry
— card outlines with `paper-100` blocks and a 1.2s sweep, never a centred spinner on blank
canvas), empty (name the missing resource + the CTA that fixes it: "No machines yet — Deploy
your first machine"), error (what happened + retry with backoff note), offline/stale (known
data greyed via `text.disabled` + the stale banner with "Load latest").

**Contracts this table encodes:** one primary filled violet CTA per view [F/S] (dense toolbars
may run a primary plus icon actions); every icon-only control carries a tooltip; a disabled
control states why on focus or hover ("Suspended apps can't be scaled — resume first"); a
button never changes width between idle and loading — reserve space with a fixed min-width and
swap label for a spinner; destructive actions restate the resource name and require a
typed or double confirmation when irreversible.

## 11. Light / Dark Strategy

- **Posture: A — light-only product** with two fenced **guest** dark surfaces (terminal
  panels, embedded Grafana metrics). Rationale: the shipped dashboard has no dark mode as of
  2026-11-01 (community threads of Nov 2025 and Sep 2026 still request it; the popular
  community userstyle exists precisely because it doesn't ship, and it preserves violet
  branding while darkening). The "dark purple Fly" impression comes from marketing gradients
  and the terminal — not the product chrome.
- **Mechanism:** single mode; every semantic role carries one light value. When a dark mode
  ships it must be authored, not filtered: a `night` surface ramp anchored at `#0F0A20`
  (never pure black), a *stronger* hairline (a 1px `#E1E4EF` on white reads as delicate; on
  violet-night it disappears, so dark borders must step up to a `#9D95BB`-at-40% equivalent),
  and role re-binding — never a per-component palette. No role may exist in only one mode at
  that point; the current `night.*` guest roles prove the vocabulary exists.
- **`color-scheme`** set to light on the root so UA chrome, form controls and scrollbars match
  the paper canvas; the guest terminal panels declare dark locally so their scrollbars and
  form controls follow.
- **A mode meta declaration belongs in the head before any stylesheet** to prevent a flash of
  the wrong scheme on slow connections.
- **Guest surfaces are quarantined:** `night.*` roles render only inside the terminal panel
  and Grafana embeds; product components may not consume them and guest panels may not consume
  product roles. Grafana's own dark palette is treated as an artwork frame — the Fly page
  around it stays light.
- Org-tinting is not a Fly pattern (single brand, no white-label tenants); if it ever ships,
  colour tokens only — radii, type and layout frozen.

## 12. Density-Mode Strategy

- **Default mode per surface class:** `standard` for every app-level page (the machines
  table's 48px rows and 14px body define the house feel); `dense` only where the job is
  scanning — metrics, logs, registry; `focused` for sign-up, the launch wizard and destructive
  confirmations. The boundary is the job: browse/configure → standard; observe/scan → dense;
  decide/commit → focused.
- **Mechanism:** a density attribute on the app root rescales row height, cell padding, gutter
  and body size together as one token axis — spacing tokens do not change per screen size,
  only per density mode. A mid-page density change is a defect; the Postgres overview's
  airy stat tiles are standard-mode spacing, not a separate mode.
- **Container queries drive reflow**, not viewport media queries: a stat-tile row collapses
  from five tiles to a 2×3 grid based on its container's measure; `cq*` units are never used
  where a missing container would silently resolve them to small-viewport units.
- Style queries that branch on the density marker require the marker to be a registered
  custom property with explicit syntax and inheritance; unregistered properties match nothing.
- **Offer the density switch as an accessibility affordance** on tables (standard ↔ compact),
  not as a user preference toy: users with visual field loss need the rescale (W3C SC 2.5.8
  note endorses a density-control mechanism).

## 13. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA (7:1) for the stat-value numerals and page titles on
  canvas (achieved: 14.866:1 and 15.612:1 respectively).
- **Target size:** 44×44px design target for primary controls [F/S] (nav items, primary CTA,
  sidebar rows); 24×24px hard minimum everywhere — the 16px row-action icon buttons carry an
  invisible 24px hit area with the spacing exception verified (centred 24px circles never
  intersect). Zoom does not excuse it.
- **Keyboard:** every function operable — machines table rows, row-action menus (focus-trap,
  Esc returns to trigger), drawer (Esc closes, focus returns to opener), command palette
  (global hotkey, focus-trap); focus indicator is the 2px `border.focus` ring with 2px offset,
  visible on canvas, cards and wash fills alike (5.699:1, ≥3:1 required); the focused row is
  never hidden under the sticky breadcrumb bar — scroll-padding matches bar height.
- **Contrast:** text ≥4.5:1 (computed in §3, all pass); UI boundaries and focus ≥3:1;
  `text.tertiary` deliberately tuned from the production `#9698B6` (2.814:1 fail) to
  `#837EA6` (3.818:1). **Colour independence:** every status pairs a dot *and* a word
  (Deployed, Suspended); deltas and machine states carry direction/shape glyphs; region chips
  pair flag + IATA code so colour-blind users read the code.
- **Motion:** the §8 reduced-motion variant per component; the deploy progress sweep is
  announced via polite live region, not just animated.
- **Text:** prose measure ≤80 characters (settings explainers, card copy at 14/21 stays under
  80ch in a 2/3 column); 1.5 leading on body; 200% resize without horizontal scroll — tables
  scroll inside their own region, page layout reflows.
- **Semantics:** real button/link/input elements; tables are tables (headers associated with cells);
  headings match visual rank (page title → section title → card title); `aria-live="polite"`
  on the stale-data banner and deploy progress; `aria-busy` on loading regions; the machine ID
  code field exposes its full value to assistive tech even when visually ellipsised.
- **Contrast preference:** `prefers-contrast: more` promotes `border.subtle` → `border.strong`
  and `text.secondary` → `text.primary`; values honoured: `no-preference`, `more`.

## 14. Anti-Patterns

**Do**
- Keep the canvas tinted (`#F9F9FD` + wash) and cards pure white — the tint is the room; it
  makes white cards read as paper without shadows.
- Render every machine ID, version, image ref, IP and lease in Fragment Mono with a copy
  affordance — operators paste these into terminals dozens of times a day.
- Pair every status dot with its word and wash — "Deployed" not just green.
- Give dense surfaces (metrics, logs) their own room: 32px rows, 13px base, uppercase grid
  headers, chrome matching row height.
- Name the cost precisely: "$282 USD", "0.02 of 2 vCPU", "437 MB of 10 GB" — currency, unit,
  denominator.
- Use the indigo drawer header (`#4F46E5`) as the single "focus hood" moment; it tells the
  operator where the mutation will land.
- Keep the informational blue (`#2563EB`) for "new data arrived" reloads only — violet stays
  the primary verb.
- Show relative times ("3 days ago") with absolute timestamps on hover/focus — audit needs
  both.
- Reserve hover fills as instant state changes; motion belongs to entrances/exits only.
- Pair illustration with the recovery CTA in every empty state — art never replaces the verb.
- Keep Grafana and terminal quarantined in their night surfaces; the light page frames them.
- Hold button widths fixed between idle and loading; swap label for spinner, never reflow.

**Don't**
- No dark-mode cosplay inside the light product — no charcoal sidebars "because cloud". The
  night set is fenced to terminal/Grafana guests.
- No watercolor art, Mackinac serif or dusk gradients inside data surfaces — the brand moment
  stops at the product frame.
- No second filled CTA beside the violet one; a blue button belongs to a reload banner, not a
  competing action.
- No `#9698B6` metadata text at any size — it computes 2.814:1 and fails; use the tuned
  tertiary `#837EA6`.
- No colour-only status, ever — a green dot without its word is a defect.
- No centred spinner on a blank page; skeletons mirror final geometry.
- No `alert()`/`confirm()` for destructive flows — the dialog restates the resource name and
  consequence.
- No hover-only affordances on touch targets; every row action is also reachable by keyboard
  menu.
- No placeholder-as-label in the launch wizard — labels persist above inputs; hints live
  underneath in Meta style.
- No tiny-type density cheating: 13px is the dense floor, and it never applies to billing or
  consent copy.
- No marketing og-gradient purple (`#121226`/`#282045`) repurposed as a UI surface colour —
  dusk primitives are marketing-only by rule.
- No silent disabled controls: a suspended app's Scale button explains itself on focus.

## 15. Quick Reference & Verification Gate

**Colour (light-only product; guest night set fenced):**
`surface.canvas #F9F9FD` · `surface.raised #FFFFFF` · `surface.wash #F5F3FF` ·
`surface.inset #F1F2F9` · `surface.hover #F5F3FF` · `surface.selected #EDE9FE` ·
`border.subtle #E1E4EF` · `border.strong #706781` · `border.focus #7C3AED` ·
`accent.action #7C3AED` · `accent.actionHover #6D28D9` · `accent.onAction #FFFFFF` ·
`accent.subtle #EDE9FE` · `accent.onSubtle #5B21B6` · `accent.alt #2563EB` ·
`accent.header #4F46E5` · `text.primary #281950` · `text.secondary #706781` ·
`text.tertiary #837EA6` · `text.disabled #A39AC1` · `status.success #166534/#DCFCE7/#16A34A` ·
`status.warning #854D0E/#FEF9C3/#D97706` · `status.error #BE123C/#FFE4E6/#E11D48` ·
`status.info #1E40AF/#DBEAFE/#2563EB` · `night.surface #0F0A20` · `night.ink #ECE9F7` ·
`night.muted #9D95BB` · `night.accent #8B5CF6` · scrim `#110E1A` at 40%.

**Type ramp:** Fricolage Grotesque 400/500/600/700 (UI) · Mackinac 500/700 (marketing display
only) · Fragment Mono 400 (identifiers). [F] 32/20/16/14/13 · [S] 24/16/14/13/28-stat/11-label/
12-meta · [D] 12-header/13-cell/12.5-log/12-help. `tabular-nums` on all comparable values.

**Spacing + radius:** 4px base; gutter 32/24/16 by mode; card pad 24 [S], 16 [D]; rows 48 [S],
32 [D]. Radius: 4 chips/code · 6 inputs · 8 buttons/banners · 14 cards/drawers · full pills.

**Component → token map:** top nav → `surface.raised + border.subtle + text.secondary/icons` ·
breadcrumb bar → `surface.raised + text.secondary + status pill` · sidebar →
`surface.canvas-transparent + surface.selected pill + accent.onSubtle ink` · data table →
`surface.raised + border.subtle row rules + Row primary/secondary + mono identifier` ·
stat tile → `surface.raised + Stat label + Stat value + accent.action sparkline` ·
card → `surface.raised + border.subtle + Section title + Body` · drawer →
`accent.header band + surface.raised body + md buttons` · status pill →
`status.*.wash + status.*.ink + status.*.dot` · code field → `surface.raised inset +
border.subtle + Fragment Mono` · banner → `status.info.wash + status.info.ink + accent.alt` ·
skeleton → `surface.inset blocks, sweep` · terminal → `night.*` only.

**Agent prompt block.** Build against the semantic tokens only — never raw hex in components.
Canvas: `surface.canvas` with the violet wash gradient (`surface.wash` → `#EEF2FF` family
endpoint declared once at root); cards: `surface.raised`, radius.lg, `border.subtle` 1px, no
shadow below level 3. Text: `text.primary` headings/values, `text.secondary` support,
`text.tertiary` metadata ≥3:1, `text.disabled` only with reason-on-hover. One
`accent.action` filled CTA per view; focus ring `border.focus` 2px/2px; hover fills instant.
Identifiers in Fragment Mono with copy affordance; numerics right-aligned with tabular
figures; rows 48px [S]/32px [D]; chrome heights match rows. Status always dot+word+wash;
regions flag+code; versions as xs chips in `accent.subtle`/`accent.onSubtle`.

1. *App overview (Postgres cluster)* — `surface.canvas` page; header card with cluster name in
   24px `text.primary` + version chip + mono ID + "Ready" pill; five stat tiles
   (radius.lg, `space.6` padding, uppercase 11px `text.secondary` label, 28px tabular
   `text.primary` value, `accent.action` sparkline, 12px `text.tertiary` footnote); three
   content cards (Recent Events / Recent Backups / Environment & Plan) with 48px event rows,
   `border.subtle` separators; cost block inside Environment card: 28px tabular "$282" +
   "USD" in `text.secondary` + "View billing →" link in `accent.action`; one filled
   `accent.action` "Connect" + one outlined "Scale"; no shadow above level 1.
2. *Machines data row* — 48px height; columns: Machine (Fragment Mono, `accent.action` ink,
   version chip), Region (flag+code chip), Size/CPU (Fragment Mono `text.primary`), Created
   (relative, `text.secondary`), row actions (16px icon buttons with 24px hit areas +
   tooltips); header row uppercase 12px `text.secondary` with tracking, height = 48px;
   hover fill `surface.hover` instant; focus ring `border.focus`; pagination bar 48px.
3. *Process-group drawer* — right slide-in 440px, level 3; header band `accent.header` with
   white 16px title + close; body `surface.raised` with labeled selects/steppers
   (`border.strong` borders, `border.focus` rings); footer: ghost Cancel + filled
   `accent.action` Save; Esc closes, focus returns to trigger; dirty-state guard confirms
   before close.

**Pre-ship checklist.**
1. Zero raw hex outside L1. 2. No token resolves to a component name. 3. Every contrast
pairing computed, passing, unrounded (§3 table is the record). 4. Every semantic role has a
value in every shipped mode (light-only today; dark must complete the set before shipping).
5. Every fetching surface has loading/empty/error/offline specified. 6. Every component row
lists disabled and loading states. 7. Row, header, toolbar and pagination heights agree.
8. Reduced-motion variant written for every authored motion. 9. Every control keyboard-
reachable with a visible focus indicator. 10. Dark (guest surfaces) authored, not filtered,
with border strength exceeding light's. 11. No unoverridden stock library default inside a
committed surface (Grafana chrome is a guest, not a default). 12. Nothing came from a
marketing page (og/dusk/watercolor excluded from tokens). 13. The §9 brand-moment palette
appears nowhere in the UI token layers. 14. `night.*` roles appear in exactly two guest
surfaces and nowhere else.
