# Design System — Supabase (Postgres Development Platform)

<!-- premium-web-design:design-system 2 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: premium-marketing-design sibling spec (devtools/supabase, rung 1 — Circular family, brand green #3ECF8E, charcoal marketing canvas, anti-bold display; sibling pill-button claims corrected against the 2026-11 capture: marketing CTAs are 6–8px rounded rectangles, not 9999px pills), the supabase/supabase open-source UI packages (packages/ui + packages/config OKLCH token system: five theme inputs derive every semantic colour; apps/studio fonts.css: Inter body, Manrope headings, Source Code Pro mono, normal weight 450; globals.css: 13px dense grid text, radius ladder scaled 4/3, datatable row height 28px), supabase.com/brand-assets (#3ECF8E, #249361, #1C1C1C/#1E1E1E), and screens/ captures (Studio dark create-project form, Studio dark Supavisor pooling panel, Studio light pooler settings, homepage hero, pricing cards). -->
<!-- Surface classes: 9 routes classified; density classes F/S/D assigned (F create-project + destructive dialogs + org onboarding; S project home + reports + settings + org usage; D table editor + SQL editor results + logs explorer + auth users + storage browser) -->

## 1. Design Posture & Atmosphere

Supabase is a Postgres backend platform — database, auth, storage, edge functions, realtime —
managed from a web Studio. The product has two faces that share one green. The marketing site
(supabase.com) is a **poster pinned to a dark engine-room wall**: a charcoal canvas
(#1E1E1E-family), a two-tone headline whose second line is the only loud green on screen, and
product panels that are dark cards with line-art and one large brand-green surface (the Postgres
elephant on solid #3ECF8E). The Studio (supabase.com/dashboard) is the **engine-room console**
itself: a near-black canvas carrying a barely-perceptible green tint (#131413 computed from the
open-source OKLCH theme), hairline-separated form rows, deep-green action plates, and data
surfaces that drop to 28px rows and 13px text when the product is showing tables, SQL results or
logs. After eight hours in the Studio nothing glares: the accent stays on buttons, toggles, focus
rings and status glyphs; the loudest thing on a data screen is a number in a mono face.

Against its category's defaults (Firebase's light material console, Neon's black instrument
panel, PlanetScale's pale minimalism), Supabase sits **dark-default dual-mode, one-accent,
engineering-flats**. It is the only major backend console that ships a full light mode with the
dark mode as the root default — and the mode flip is authored, not filtered: in light mode the
brand green itself darkens (#0E7E4E for text and small indicators, #006338-family plates) because
the marketing green fails contrast on a near-white canvas. Density is Standard on project pages,
Focused on the create-project form and dialogs, and Dense in every data grid — the table editor
ships 28px rows, the single hardest density commitment in the category. The visual metaphor:
**a dark cockpit bolted onto the engine room** — marketing paints the room, the Studio flies it.

**Key Characteristics**
- Two canvases, one system: Studio dark canvas `#131413`, Studio light canvas `#FDFDFD`;
  marketing canvas `#1E1E1E`-family charcoal. Depth in dark comes from tonal steps
  (`#131413 → #181A19 → #1B1D1C → #1E201F`) plus 1px hairlines, never from colored shadows.
- One brand green `#3ECF8E` (brand-assets confirmed) — the logo, active indicators, toggles-on,
  the marketing headline payload, and one large product-panel surface. Accent budget: 4–8 small
  green elements per Studio viewport; the green is never body-text colour.
- Two greens do two jobs: `#3ECF8E` is brand/indicator green; the **action plate** is deep
  `#006338` (dark) / `#0E7E4E` (light) with near-white ink — buttons are darker than the accent.
- Mode flip re-authors the green: light mode swaps brand-as-text to `#0E7E4E` (5.0:1); the raw
  `#3ECF8E` on light canvas is 1.96:1 and is banned from light-mode text and small glyphs.
- Ink ramp (dark): `#EDEFEE` primary, `#BCBDBC` secondary, `#989A99` tertiary — a slightly
  green-tinted white family; light mirrors it with `#030303 / #4B4B4B / #717171`.
- Studio typography: **Inter** variable for everything (normal weight 450 — the shipped default),
  **Manrope** for headings, **Source Code Pro** for identifiers, SQL, connection strings,
  timestamps and log lines. Marketing sets **Circular** 400/500 with uniform negative tracking.
- Type ramp steps: 13 / 15 / 16 / 18 / 22 / 28 / 34px in Studio (`text-sm 13` is the dense base,
  `15` the standard base); marketing adds 24 / 36 / 48 / 72px display steps.
- Dense data surfaces commit to **28px rows and 13px text** (shipped row-height token), with
  tabular numerals right-aligned in every grid; prose inside a dense screen steps back up to 15px.
- Hairline vocabulary: borders are foreground-derived overlays — subtle ~7.5% white (dark),
  control/input ~13.5%, hover ~28%; they are decorative separators, never the sole control cue.
- Shape ladder (Studio): 3px badges/inline code · 5px inputs and buttons · 6px menus/panels ·
  8px cards · 11px dialogs · 9999px pills/avatars/toggles. Marketing feature panels use 16px.
- Status colouring is anchored and glyph-paired: amber `#F2AF48` warning (triangle), red
  `#B54A46` destructive (filled plate, light ink 4.51:1), violet `#9B8FF0` info — plus a green
  check for success. Violet is reserved for "no additional charge" badges; never a chart rainbow.
- Forms are label-left / control-right rows split by hairlines (the entire Studio settings
  grammar); uppercase mono eyebrows (SECURITY OPTIONS, ADVANCED CONFIGURATION) mark disclosure.
- Feedback is skeleton-first: a 2s linear shimmer sweep on loading geometry — never a centred
  spinner on a blank page.
- Marketing CTAs are 6–8px rounded rectangles (green plate + ghost), not pills; pills in Studio
  are reserved for badges, avatars and toggles.

## 2. Token Architecture

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.
- **L1 Primitive** — literal values named by *value*, referenced only by L2:
  `canvas-dark #131413` · `canvas-light #FDFDFD` · `card-dark #181A19` · `card-light #FFFFFF`
  · `popover-dark #1B1D1C` · `panel-dark #1E201F` · `brand #3ECF8E` · `brand-deep-dark #006338`
  · `brand-deep-light #0E7E4E` · `brand-ink-dark #EDEFEE` · `brand-ink-light #FAFCFB`
  · `green-wash-dark #006239` · `green-soft-light #72E3AD` · `amber #F2AF48` · `amber-deep #DB8E00`
  · `red #B54A46` · `red-text-dark #F16A50` · `red-text-light #CA3214` · `violet #9B8FF0`
  · `violet-deep-light #6C5EBA` · ink ramp dark `#EDEFEE #BCBDBC #989A99 #7E7E7E #A0A0A0`
  · ink ramp light `#030303 #4B4B4B #717171 #C7C7C7` · chart hues `#72C7BA #F9C789 #ADDB67
  #C792EA #F78C6C` · violet-link `#7A66FF`.
  Banned: component-named primitives (a `--card-bg`-style name) — one value, many roles.
- **L2 Semantic** — role names (`surface.canvas`, `surface.raised`, `text.primary`,
  `accent.action`, `status.error`, `border.focus`). The only layer a component may consume.
  Every role carries a value in both shipped modes (§3); the system derives both modes from five
  theme inputs — spot hue (157.5° green), neutral chroma, canvas lightness, elevation step
  (dark 2.5% / light 2.4% per level), and a contrast knob — so a mode is a re-binding of the same
  roles, never a second vocabulary.
- **L3 Component** — only deliberate deviation, pointing at L2 or L1:
  `form.row → surface.canvas + border.subtle hairline + text.primary label` ·
  `grid.cell → 13px text + tabular numerals + 28px row` ·
  `admonition.warning → amber glyph + amber-deep text + amber wash 10%` ·
  `badge.preview → text.tertiary + border.subtle + full radius` ·
  `skeleton → panel-dark + shimmer sweep` · `log.line → Source Code Pro 13px on surface.canvas`.
  Never a raw value, never a sibling component's token.

**Rules.** Every token has a determinable type (colour, dimension, font-family, duration,
easing) or it is invalid; names are case-sensitive and free of `$`, `{`, `}` and dots; circular
references are an error. Every semantic token has a value in **every** shipped mode — the
dual-mode posture (§11) makes this a hard invariant: a role that resolves only in dark fails the
gate. Animatable tokens (skeleton sweep position, popover scale, dialog fade) are registered as
custom properties with explicit syntax and inheritance declarations; initial values are
computationally independent, so percentages are illegal as initial values.

**Layer order (low → high):** `reset → primitives → semantic → components → utilities`.
Order beats specificity entirely, so a stray un-layered rule inside a component file would
outrank the whole system; anything a consumer must override without forcing priority lives in
the top layer.

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` | #FDFDFD | #131413 | app background; near-white / green-tinted near-black, never pure white or pure black |
| `surface.raised` | #FFFFFF | #181A19 | cards, panels, table headers — one elevation step above canvas |
| `surface.overlay` | #FFFFFF | #1B1D1C | popovers, dropdown menus, dialogs, command palette |
| `surface.inset` | black 1.2% | black 12% | sunk fields, filled inputs, code wells |
| `surface.hover` | black 5% | white 5% | row and item hover fill, composited over the local surface |
| `surface.selected` | green-soft wash 12% | green wash (#006239) | selected rows, active cells, checked items |
| `border.subtle` | #EAEAEA | #232423 | 1px hairlines between rows and panels; decorative only (1.19:1) |
| `border.strong` | #DBDBDB | #303231 | input and control boundaries; hover chrome strengthens to the 28% step |
| `border.focus` | #8CD8B4 pair | #317A55 pair | 2px ring at 55% brand-bright, always paired with a border colour shift (see gate) |
| `accent.action` | #0E7E4E | #006338 | filled CTA plate; hover lightens one step, never re-hues |
| `accent.onAction` | #FAFCFB | #EDEFEE | label on the green plate |
| `accent.brand` | #0E7E4E as text · #3ECF8E as mark | #3ECF8E | logo, toggles-on, active indicators; raw brand green is text-legal in dark only |
| `accent.subtle` | green-soft washes (#72E3AD family) | #006239 wash | soft brand backgrounds, selected states, brand borders at 30% |
| `text.primary` | #030303 | #EDEFEE | headings, row labels, values, button labels |
| `text.secondary` | #4B4B4B | #BCBDBC | body copy, descriptions, inactive-but-loaded data |
| `text.tertiary` | #717171 | #989A99 | meta, placeholders, inactive nav; 4.80:1 light / 6.52:1 dark |
| `text.disabled` | #C7C7C7 | #7E7E7E | inactive controls only; SC-1.4.3-exempt, never body copy |
| `status.success` | #0E7E4E | #4ACD8B | check glyph or dot; never colour alone |
| `status.warning` | #AC5800 | #F2AF48 | triangle glyph; amber wash backgrounds carry dark ink (9.67:1) |
| `status.error` | fill #AB413E · text #CA3214 | fill #B54A46 · text #F16A50 | destructive plate carries light ink 4.51:1; error text uses the lighter step (6.08:1 dark / 5.19:1 light) |
| `status.info` | #6C5EBA | #9B8FF0 | violet; also the "no additional charge" badge hue |
| `chart.series1–5` | same hues, deepened for white | #72C7BA #F9C789 #ADDB67 #C792EA #F78C6C | fixed five-hue code palette; green is series 1 |

Dark canvas is **not pure black and not gray**: it is a green-tinted near-black `#131413`
(computed from the theme's 157.5° spot hue at near-zero chroma). Depth in dark comes from
surface steps and 1px strokes, never from visible shadows.

**Contrast gate — computed, unrounded (4.499:1 fails).** Body text ≥4.5:1; large text (≥24px, or
≥18.5px bold) ≥3:1; UI boundaries and focus indicators ≥3:1 non-text (W3C SC 1.4.3, 1.4.11).
Ratios computed with the WCAG 2.x relative-luminance formula.

| Pairing | Ratio | Required | Verdict |
|---|---|---|---|
| text.primary #030303 on surface.canvas #FDFDFD (light) | 20.276:1 | 4.5:1 | PASS |
| text.primary #EDEFEE on surface.canvas #131413 (dark) | 15.989:1 | 4.5:1 | PASS |
| text.primary #EDEFEE on surface.raised #181A19 (dark) | 15.144:1 | 4.5:1 | PASS |
| text.secondary #4B4B4B on surface.canvas #FDFDFD (light) | 8.576:1 | 4.5:1 | PASS |
| text.secondary #BCBDBC on surface.canvas #131413 (dark) | 9.799:1 | 4.5:1 | PASS |
| text.tertiary #717171 on surface.canvas #FDFDFD (light) | 4.798:1 | 4.5:1 | PASS |
| text.tertiary #989A99 on surface.canvas #131413 (dark) | 6.523:1 | 4.5:1 | PASS |
| text.tertiary #989A99 on surface.raised #181A19 (dark) | 6.178:1 | 4.5:1 | PASS |
| accent.onAction #FAFCFB on accent.action #0E7E4E (light) | 4.955:1 | 4.5:1 | PASS |
| accent.onAction #EDEFEE on accent.action #006338 (dark) | 6.398:1 | 4.5:1 | PASS |
| accent.brand #3ECF8E on dark canvas #131413 (non-text) | 9.252:1 | 3:1 | PASS |
| accent.brand #3ECF8E on light canvas #FDFDFD (as text) | 1.962:1 | 4.5:1 | FAIL — restricted |
| status.success #4ACD8B glyph on dark canvas #131413 | 9.143:1 | 3:1 non-text | PASS |
| status.success #0E7E4E on light canvas #FDFDFD | 5.019:1 | 4.5:1 | PASS |
| status.warning #F2AF48 on dark canvas #131413 | 9.674:1 | 3:1 non-text | PASS |
| status.warning #AC5800 on light canvas #FDFDFD | 4.975:1 | 4.5:1 | PASS |
| status.error text #F16A50 on dark canvas #131413 | 6.083:1 | 4.5:1 | PASS |
| status.error text #CA3214 on light canvas #FDFDFD | 5.190:1 | 4.5:1 | PASS |
| status.error fill #B54A46 with #EDEFEE ink (dark) | 4.509:1 | 4.5:1 | PASS |
| status.info #9B8FF0 on dark canvas #131413 | 6.667:1 | 4.5:1 | PASS |
| status.info #6C5EBA on light canvas #FDFDFD | 5.230:1 | 4.5:1 | PASS |
| border.focus ring composite #317A55 on dark canvas #131413 | 3.558:1 | 3:1 non-text | PASS |
| border.focus ring composite #8CD8B4 on light canvas #FDFDFD | 1.639:1 | 3:1 non-text | FAIL — paired |
| border.strong #303231 on dark canvas #131413 | 1.430:1 | decorative | DOCUMENTED |
| border.subtle #232423 on dark canvas #131413 | 1.185:1 | decorative | DOCUMENTED |
| border.subtle #EAEAEA on light canvas #FDFDFD | 1.183:1 | decorative | DOCUMENTED |

The two non-passing rows are managed by restriction, not by redefining the palette: raw brand
green `#3ECF8E` is banned as text and small-glyph colour in light mode — light-mode brand-as-text
is `#0E7E4E` (5.019:1) and the light focus ring's 1.639:1 composite is never a lone indicator:
light-mode focus always pairs the ring with the control's border shifting to `#0E7E4E`, which
alone clears 3:1. `border.strong` hairlines (1.43:1) are deliberately low-contrast tonal
separators; every control that relies on its boundary for identification also carries a label,
placeholder or value, and hover/focus chrome strengthens to the 28% step (2.32:1) plus ring.
`text.disabled` (~2.8:1 both modes) is SC-exempt inactive-component text only.

## 4. Typography

**Families.** Studio UI **Inter** (variable, self-hosted woff2, weights 100–900 with 450 as the
shipped normal weight), fallback system sans. Headings **Manrope** (variable 200–800). Numeric
and code **Source Code Pro** (variable 200–900) for identifiers, SQL, connection strings,
hostnames, timestamps, log lines and the pricing numerals. Marketing sets **Circular** (400/500,
self-hosted) with Source Code Pro for code fragments. *Monospace is for identifiers and code,
never a costume* — a mono word inside a sans sentence is a defect unless it is an identifier
(exception: marketing prices, where the mono digits are the brand's numerals).

**One ramp table per class, not one blended table.**

- **F Focused, 16px base** — create-project form, destructive dialogs, org onboarding:
| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Title | 22px | 600 Manrope | 30px | 0 | — | "Create a new project" |
| Body | 16px | 450 | 24px (1.5) | 0 | — | intro copy under the title |
| Label | 14px | 500 | 20px | 0 | — | "Organization", "Project name", buttons |
| Helper | 13px | 400 | 20px | 0 | — | "Select the region closest to your users…" |
| Eyebrow | 12px | 500 mono | 16px | +8% uppercase | — | "SECURITY OPTIONS", "ADVANCED CONFIGURATION" |

- **S Standard, 15px base** — project home, reports, settings, org usage:
| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Page title | 22px | 600 Manrope | 30px | 0 | — | "Database", "Authentication" |
| Section title | 18px | 600 Manrope | 26px | 0 | — | "Connection pooling configuration" |
| Body | 15px | 450 | 22px (1.47) | 0 | — | descriptions, helper prose |
| Row primary | 14px | 500 | 20px | 0 | tabular | list labels, plan names |
| Row secondary | 13px | 400 | 20px | 0 | tabular | sub-values, dates, counts |
| Stat value | 34px | 600 Manrope | 40px | 0 | tabular | report figures |
| Stat label | 12px | 500 | 16px | +6% uppercase | — | "DATABASE SIZE", "EGRESS" |
| Button | 14px | 500 | 20px | 0 | — | "Save", "Cancel", "Create new project" |

- **D Dense, 13px base, data surfaces only** — table editor, SQL results, logs, auth users:
| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Grid header | 13px | 500 | 18px | 0 | — | column names |
| Grid cell text | 13px | 400 | 18px | 0 | — | cell prose, enums |
| Grid cell numeric | 13px | 400 | 18px | 0 | tabular | counts, sizes, latencies |
| Grid cell identifier | 13px | 400 | 18px | 0 | mono | table names, UUIDs, hosts |
| Log line | 13px | 400 | 20px | 0 | mono | log explorer rows, query history |
| Badge | 11px | 500 | 16px | 0 | — | "Supavisor", "Shared Pooler", "Default", "Preview" |
| Inline help | 12px | 400 | 16px | 0 | — | hints under dense controls |

Prose inside a dense screen still steps up to Body 15px.

**Marketing ramp (poster surface):** display 72px/400 with −0.5px tracking, second line in brand
green · headline 48px/400 · section title 24px/500 · body 16px/400 (1.5) · nav link 14px/400 ·
price value 40px/400 mono · plan name 15px/500 uppercase · button 14px/500 · micro 12px.
Marketing display is set at 400 — emphasis comes from the two-tone colour recipe, never bold.

**Invariants.** Tabular numerals on every comparable value — row counts, latency (the SQL
editor's "51ms"), egress, MAU, sizes, prices, timestamps. Right-align numerics, left-align text,
never centre a numeric column. Fixed stepped sizes; no fluid type. Measure ≤80 characters:
65–80ch in F/S prose and marketing body, unconstrained in dense grids and code.

## 5. Spacing Scale & Density Scales

**Spacing base: 4px grid; a 2px micro step exists for dense chrome.** `space.0` 0 · `0.5` 2px
icon-to-label in dense toolbars and badges · `1` 4px control gaps, badge padding · `2` 8px
control padding in D, button vertical padding · `3` 12px cell padding in S · `4` 16px card
padding in S, page gutter in D · `6` 24px card padding in F, panel padding · `8` 32px section
gap in S · `12` 48px region separation · `16` 64px marketing rhythm · `32` 128px marketing
section beat. No 17px. No 23px. If a layout needs an off-scale value, the layout is wrong.

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | 40px control rows | 16px | 24px | 32px | create-project, destructive dialogs, onboarding |
| `standard` | 40–44px | 15px | 12–16px | 24px | project home, reports, settings, org usage |
| `dense` | 28px | 13px | 8px | 16px | table editor, SQL results, logs, auth users, storage |

- Density comes from row height, column pruning and leading — never from type too small to read.
  A 13px tabular numeral in the table editor is correct; the same numeral in the create-project
  form is a defect.
- **Never switch mid-page.** The create-project form is Focused end to end; the table editor is
  Dense end to end. Switching across routes with different jobs is legitimate — it should feel
  like a different room.
- **Chrome follows rows.** The table editor's toolbar, filter bar and pagination match the 28px
  row rhythm; the SQL editor's results header matches its result rows. A 40px toolbar over 28px
  rows is a rhythm break.
- Settings pages are a two-column hairline grammar: label column left (S Row primary), control
  column right, rows separated by `border.subtle`, section eyebrows in uppercase mono.
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40%. House heuristic — the
  pool-configuration panel sits near 50% (helper prose is generous), the table editor near 25%.

## 6. Radius Scale

`none` 0 · `xs` 3px badges, tags, inline code chips · `sm` 5px inputs, buttons, menu items,
selects · `panel` 6px dropdown menus, popovers, small panels · `md` 8px cards, panels, admonitions
· `lg` 11px dialogs, sheets, command palette · `full` 9999px pills, avatars, toggles, status dots.
(The Studio ladder is the default web curve scaled by 4/3: 2.67 / 5.33 / 8 / 10.67 — rounded to
3 / 5 / 8 / 11; marketing feature panels use `xl` 16px.) **One radius per component family**,
never mixed ad-hoc: every Studio button is 5px, every Studio card 8px, every dialog 11px — a
pill CTA inside Studio chrome is a defect (pills belong to badges, avatars and toggles). Nested
radii obey `radius_inner = radius_outer − padding` (an 3px code chip inside an 8px panel with 4px
padding is correct).

## 7. Elevation

**Choose one strategy, never mix paradigms.** Dark elevation is **tonal first**: surfaces step
lighter as they rise (`#131413 → #181A19 → #1B1D1C → #1E201F`), edges are 1px foreground-derived
hairlines, and genuinely floating layers add a soft black ambient (`rgba(0,0,0,0.2–0.5)` with a
large blur) that reads as separation, not colour. Light elevation inverts the direction — higher
surfaces brighten toward white (`#FDFDFD → #FFFFFF`) — with the same hairlines.

Levels, low → high: **0** canvas (no shadow, hairline only) · **1** card/panel (one tonal step +
`border.subtle`) · **2** sticky header/toolbar (canvas background + hairline bottom edge +
`border.strong` on scroll) · **3** popover/menu (overlay step + `border.strong` + soft ambient +
2px entrance shadow) · **4** dialog (overlay step + scrim `rgba(0,0,0,0.5)` dark / 0.4 light +
strongest ambient). Skeletons are geometry, not elevation: they render the final shape of the
loading surface at `surface.raised` with a shimmer sweep.

## 8. Motion

`instant` 0ms · `fast` 120ms ease-out (hover fills, hairline strengthening, tooltip out, dense
exits) · `base` 180ms decelerate (menus, popovers, toggles, [D] entrances) · `slow` 280ms
decelerate (dialogs, sheets, drawer slides). The working curve is the standard
`(0.4, 0, 0.6, 1)` family; entrances decelerate, exits accelerate — symmetric ease-in-out on both
directions of the same transition is a defect.
- Loading runs on a dedicated 2s linear shimmer sweep across skeleton geometry; badge attention
  loops (a 3s ease-in-out shimmer/pulse) exist only for upgrade/pending badges.
- Animate transform and opacity only — never width, height, top, left (the shimmer's background
  sweep is the one sanctioned background-position loop, on a composited skeleton layer).
- No bounce on irreversible moments: not on "Delete table", not on project pause, not on a
  downgrade confirmation.
- The Save button swaps its label into reserved space while persisting; it never changes width
  between idle and loading.
- **Reduced motion is a real variant**, not motion-off everywhere: the shimmer becomes a static
  10% wash, badge loops freeze at rest state, dialogs and popovers become ≤150ms crossfades.
  What must be neutralised is scaling and panning of large objects, not every fade.

## 9. Imagery & Art Direction

- **Brand moment:** the marketing product panel — a large solid brand-green field with the
  Postgres elephant in dark ink (screens/product.png). This is the single sanctioned saturation
  surface in the system; its palette never leaks into Studio tokens. One saturation moment per
  marketing viewport; none inside Studio chrome.
- **Iconography:** Lucide-class thin-stroke line icons, 1px strokes on a 16px grid, shipped at
  12 / 16 / 18px; geometric, monochrome in the ink ramp, with brand green reserved for
  active/brand contexts. Icon-only controls always carry a tooltip (§10).
- **Photography:** none in product. Marketing uses no lifestyle photography either — trust is
  carried by customer wordmarks rendered monochrome at uniform height in the logo wall.
- **Illustration:** marketing product cards use dark line-art and wireframe diagrams (network
  globes, terminal frames) in graphite on near-black; docs illustrations use mono uppercase
  labels with a single amber accent on black. Illustration never appears inside Studio data
  chrome except small empty-state glyphs.
- **Empty / error art:** a glyph + one sentence + the recovery CTA ("No tables yet — Create a
  table"); illustration never substitutes for the recovery action. If a surface has no
  illustration system, the empty state is text-only — per-screen invention is banned.

## 10. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell/sidebar | S | org view, project view | default, hover, active, collapsed | Tab top-down; headings not focusable | project name + env badge, "Table editor", "SQL Editor" |
| Org/project switcher | S | dropdown trigger with plan badge | closed, open, searching | Enter opens, Esc closes, arrows navigate | "My Free Org · Free" |
| Data table (table editor) | D | grid view, spreadsheet edit | loading (ghost rows), empty, error, cell editing, row selected | arrows move cells, Enter edits, Esc cancels | "Filters · Sort · Add record · Delete" |
| SQL editor | D | query tabs, results pane | running, results, error, saved/history | shortcut-run, tab arrows | "Run · 51ms · 10 rows" |
| Logs explorer | D | timestamp filter, severity | streaming, paused, empty, error | arrows scroll rows | "Last hour · Refresh" |
| Form row (settings) | S/F | label-left control-right | idle, edited (red label underline), saving, error | Tab into control, Enter submits | "Pool Size 15" |
| Admonition | S/F | info (violet), note, warning (amber) | static, with action | action focusable | "Pool mode is permanently set to Transaction on port 6543" |
| Dialog | F | confirmation, destructive | open, confirming (typed confirmation), closed | focus trap, Esc closes | "These settings cannot be changed after the project is created" |
| Button | S/F/D | primary solid, default, danger, ghost | idle, hover, focus ring, loading (label swap), disabled with reason | Enter activates; visible ring | "Create new project", "Cancel", "Save" |
| Badge | S/D | brand pill, neutral outline, preview | static | read-only | "Supavisor", "Shared Pooler", "Preview" |
| Toggle | S | on/off switch | on (green), off, disabled | Space toggles | "Enable Row Level Security" |
| Usage meter | S | linear bar + value | ok, nearing quota, exceeded | read-only | "8 GB of 500 MB — Upgrade" |
| Command palette | S | global actions + docs search | open, querying, no results | shortcut-invoked, arrows, Esc | "Search docs and guides…" |
| Filter/search bar | D | column filters, free text | idle, focused, filled, no-results | shortcut-invoked, Esc clears | "Search for a table…" |
| Loading skeleton | all | table, panel, chart | shimmering, static (reduced motion) | — | — |

Every fetching surface also designs: **loading** — skeleton matching final geometry (ghost grid
rows, ghost chart axes; never a centred spinner on a blank page); **empty** — what is missing
plus the CTA that fixes it ("No tables yet — Create a table"); **error** — what happened plus
recovery ("Couldn't load logs — Retry"); **offline/stale** — last known values stay visible
dimmed to `text.tertiary` with a "Showing cached usage" note.

**Contracts this table encodes:** one primary filled CTA per view in F/S (dense toolbars may run
a primary plus icon actions); every icon-only control carries a label or tooltip; a disabled
control states why on focus or hover ("Create new project" disables with the missing-field
reason, never silently); a button never changes width between idle and loading — label space is
reserved; the edited-field red underline (form row) is always paired with a save-time message,
never colour alone.

## 11. Light / Dark Strategy

- **Posture: C dual-parity, dark-rooted.** Both modes ship everywhere; the root defaults mirror
  the dark theme and the marketing site pins its own charcoal. Reason: the developer audience
  lives in dark editors, but Supabase is one of the few backend consoles that maintains a full
  light mode — the docs product shots, the light Studio settings surfaces and the brand site all
  prove both modes are first-class.
- **Mechanism:** semantic roles remapped per mode from the five theme inputs (§2); **no role
  absent in either mode.** The green family re-authors per mode: dark keeps `#3ECF8E` as text-
  legal brand and uses `#006338` plates; light darkens both (`#0E7E4E`) for AA.
- **`color-scheme`** is set at the root per mode so UA chrome, form controls and scrollbars
  render natively (dark scrollbar on the dark Studio, light on light).
- **The scheme meta tag sits in the head before the stylesheet** so neither mode flashes wrong
  on load; the site also declares its dark theme colour in the document head.
- **Dark is authored, not inverted:** its own surface ramp, its own border strength (the dark
  hairline family is a foreground-overlay tuned for near-black — a light-mode hairline copied
  into dark would vanish), its own error-text step (`#F16A50` for text on dark vs `#CA3214` on
  light). Progressive single-syntax colour functions are unnecessary here; each mode is a full
  authored set.
- Org tinting is not offered. Brand colour changes ship as token releases, not runtime themes.

## 12. Density-Mode Strategy

- **Default mode per surface class:** Standard on project home, reports, settings and org usage;
  Dense on table editor, SQL results, logs explorer, auth users and storage; Focused on
  create-project, destructive dialogs and onboarding. The boundary is the job: reading status →
  S; scanning volume → D; acting once → F.
- **Mechanism:** a density attribute on the app root rescales row height, cell padding, gutter
  and body size together as one token axis — spacing tokens do not change values per screen
  size; density is not a media query.
- **Container queries for reflow:** panels and the table editor reflow to their container, not
  the viewport; size queries fail closed with no eligible container, and container-query units
  silently resolve to small-viewport units there — so those units are never used where that
  fallback would be wrong.
- **Style queries** compare computed values, so the density marker is registered as a custom
  property with concrete syntax and inheritance before any style query reads it.
- **The switch is offered as an accessibility affordance**, not a preference: a density control
  honours users with visual field loss who need roomier rows, per the W3C note on SC 2.5.8. In
  the Studio the practical form is column pruning plus row-height relief on data grids, never
  shrinking type below the 13px dense floor.

## 13. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA (7:1) for stat values and the two-tone marketing headline
  payload where feasible.
- **Target size:** ≥24×24 CSS px hard minimum; 28px is the shipped dense control height
  (inputs, grid rows) and 40–44px the design target for primary controls in F/S. The spacing
  exception applies to dense grid row targets — a 24px circle centred on each target's bounding
  box must not intersect another's. Zoom does not excuse it.
- **Keyboard:** every function operable (SC 2.1.1) — sidebar, table editor cell navigation, SQL
  tabs, filter bars and dialogs are fully keyboard-driven; focus indicator visible (SC 2.4.7):
  the 2px brand-bright ring at 55% **paired with a border colour shift**, never removed without
  a stronger replacement; the focused item is never entirely hidden by a sticky header (SC
  2.4.11).
- **Contrast:** text ≥4.5:1 (§3 gate); UI boundaries and focus ≥3:1 — the low-contrast hairline
  family is decorative-only by rule. **Colour independence:** every status pairs colour with a
  glyph (amber triangle, red plate, violet dot, green check) or a word pill; the edited-field
  red underline is paired with a message; deltas carry a sign or direction glyph.
- **Motion:** the §8 reduced-motion variant per component; the shimmer and badge loops have
  static equivalents.
- **Text:** ≤80-character measure (marketing body 16px at ~65ch; Studio helper prose constrained
  to the label column), 1.5 leading on body, 200% resize without horizontal scroll (SC 1.4.8).
- **Semantics:** real buttons, links and inputs; the sidebar is a navigation landmark with
  grouped lists; headings match visual rank (page title h1, panels h2); live regions announce
  query completion and save results politely; the loading grid region is marked busy.
- **Contrast preference:** if `prefers-contrast: more` is honoured, hairlines upgrade to
  `border.strong`, `text.tertiary` steps to `text.secondary`, and the focus ring solidifies to
  full-opacity brand-bright.

## 14. Anti-Patterns

Product-calibrated; each ban carries the reason it was rejected *for this product*.

**Do**
- Spend green like a signal: buttons, toggles, focus rings, active indicators, status glyphs —
  4–8 small green elements per Studio viewport. Scarcity is what keeps `#3ECF8E` legible as brand.
- Keep the two-green division absolute: `#3ECF8E` for brand and indicators, `#006338`/`#0E7E4E`
  plates for actions. A bright-green button plate in Studio chrome is a defect.
- Re-author the green in light mode (#0E7E4E family) instead of filtering — the raw brand green
  fails light-canvas contrast by design.
- Set Studio body at Inter 450 with Manrope 600 headings; never reach for 700+ weights.
- Use Source Code Pro for every identifier, connection string, price digit and log line.
- Commit to 28px rows and 13px text in data grids, with tabular numerals right-aligned.
- Achieve depth with tonal steps + hairlines; reserve soft black ambients for floating layers only.
- Build settings as label-left/control-right hairline rows with uppercase mono section eyebrows.
- Use skeleton geometry with the 2s shimmer for every loading surface.
- Pair every status colour with a glyph or word pill.
- Reserve violet for info and "no additional charge"; keep the five-hue chart palette fixed.
- Keep the create-project form Focused end to end — it is the one slow, spacious surface.

**Don't**
- No brand-green text or small glyphs on light surfaces (1.96:1) — use the darkened light green.
- No Circular inside the Studio, no Inter on the marketing poster — the families do not cross.
- No marketing aesthetics inside Studio chrome: no 72px display type, no two-tone headlines, no
  green product-panel fields inside data screens.
- No gradients in chrome — surfaces are flat tonal steps; glow belongs to marketing art only.
- No visible coloured shadows; depth is tonal, not shadowed.
- No pills as CTAs in Studio chrome — 5px rectangles are the button family there.
- No card inflation: settings stay hairline rows, not floating card grids.
- No stat-card dashboards: usage reads as metered bars with tabular values, not greeting cards.
- No modals as connective tissue; destructive confirmation is a typed-confirmation dialog, and
  blocking `alert()`-style dialogs are banned.
- No hover-only affordances on data rows — row menus are focusable and keyboard-reachable.
- No placeholder-as-label: "Project name" persists as the label even while the placeholder shows.
- No whole-page spinners; skeletons match final geometry.
- No tiny type as a density strategy: 13px is the dense floor, for numerals and identifiers, and
  prose inside dense screens steps up to 15px.
- No row-height or toolbar heights off the row rhythm — chrome follows the 28px dense row.

## 15. Quick Reference & Verification Gate

**Colour (role → value; light / dark):**

| Role | Token | Light | Dark |
|---|---|---|---|
| Canvas | surface.canvas | #FDFDFD | #131413 |
| Raised | surface.raised | #FFFFFF | #181A19 |
| Overlay | surface.overlay | #FFFFFF | #1B1D1C |
| Hairline | border.subtle | #EAEAEA | #232423 |
| Control boundary | border.strong | #DBDBDB | #303231 |
| Focus ring | border.focus (55% ring + border shift) | #8CD8B4 pair | #317A55 pair |
| Action fill | accent.action | #0E7E4E | #006338 |
| On-action label | accent.onAction | #FAFCFB | #EDEFEE |
| Brand mark/indicator | accent.brand | #0E7E4E text · #3ECF8E mark | #3ECF8E |
| Brand wash | accent.subtle | #72E3AD washes | #006239 |
| Primary ink | text.primary | #030303 | #EDEFEE |
| Secondary ink | text.secondary | #4B4B4B | #BCBDBC |
| Tertiary ink | text.tertiary | #717171 | #989A99 |
| Success | status.success | #0E7E4E | #4ACD8B |
| Warning | status.warning | #AC5800 | #F2AF48 |
| Error fill / text | status.error | #AB413E / #CA3214 | #B54A46 / #F16A50 |
| Info | status.info | #6C5EBA | #9B8FF0 |
| Charts | chart.series1–5 | deepened set | #72C7BA #F9C789 #ADDB67 #C792EA #F78C6C |

**Type ramp (flat):** F Title 22/600 Manrope · F Body 16/450 · S Page title 22/600 Manrope ·
S Body 15/450 · S Row primary 14/500 tabular · S Stat value 34/600 Manrope tabular ·
D Grid header 13/500 · D Cell numeric 13/400 tabular · D Identifier 13/400 mono ·
D Log line 13/400 mono · Marketing display 72/400 Circular · price 40/400 mono.
Inter (450) everywhere in Studio; Manrope 600 for Studio headings; Source Code Pro for
identifiers and code; Circular only on marketing.

**Spacing + radius (flat):** base 4px (2px micro) · scale 0/2/4/8/12/16/24/32/48/64/128 ·
rows 28px D / 40–44px S · gutters 16px D / 24px S · radii 3/5/6/8/11/9999 (marketing panels 16).

**Component → token map:** primary button consumes `accent.action` + `accent.onAction` +
`radius.sm` + `border.focus` pair on focus; form row consumes `surface.canvas` +
`border.subtle` + `text.primary` label + red underline paired with message; data table consumes
28px rhythm + `border.subtle` grid lines + tabular numerals + `surface.raised` header;
admonition consumes `status.*` glyph + text step + 10% wash; badge consumes `text.tertiary` +
`border.subtle` + `radius.full`; skeleton consumes `surface.raised` + shimmer loop; sidebar
consumes `surface.canvas` + `text.tertiary` items (primary on active) + 12px uppercase headings.

**Agent prompt block.** Build surfaces against these tokens, cited by name, never by hex:
`surface.canvas #FDFDFD/#131413` · `surface.raised #FFFFFF/#181A19` · `border.subtle
#EAEAEA/#232423` · `border.strong #DBDBDB/#303231` · `accent.action #0E7E4E/#006338` ·
`accent.onAction #FAFCFB/#EDEFEE` · `accent.brand #3ECF8E` (dark text-legal; light uses
#0E7E4E) · `text.primary #030303/#EDEFEE` · `text.secondary #4B4B4B/#BCBDBC` · `text.tertiary
#717171/#989A99` · `status.warning #AC5800/#F2AF48` · `status.error #AB413E+#CA3214 /
#B54A46+#F16A50` · `status.info #6C5EBA/#9B8FF0`. Ramp: 13/15/16/18/22/34 (Manrope 600 titles,
Inter 450 body, Source Code Pro identifiers). Spacing 4px base; radii 3/5/6/8/11/9999.

1. **Create-project form (Focused)** — `surface.canvas` background, hairline-separated
   label/control rows (`border.subtle`), 22px Manrope 600 title in `text.primary`, helper text
   in `text.secondary`, uppercase mono eyebrows, one `accent.action` fill ("Create new
 project") bottom-right with `accent.onAction` label, ghost Cancel beside it; amber warning
   admonition carries its triangle glyph; focus ring `border.focus` paired with border shift.
2. **Table editor data grid (Dense)** — 28px rows end to end, header/toolbar/pagination all 28px;
   `text.primary` cells at 13px with `tabular-nums` on every numeric column, mono for
   identifiers; `border.subtle` grid lines; hover fill `surface.hover`; selection `accent.subtle`
   wash; toolbar runs one `accent.action` "Add record" plus icon actions with tooltips.
3. **Light-mode settings panel (Standard)** — `#FDFDFD` canvas, `surface.raised` panel with
   `border.subtle` hairline; brand-as-text is the darkened green; Save consumes `accent.action`
   #0E7E4E with #FAFCFB label; the raw marketing green never appears as text.

**Pre-ship checklist.** 1 Zero raw hex outside L1. 2 No token resolves to a component name.
3 Every contrast pairing computed, passing, unrounded — the two restricted pairings (raw brand
green on light canvas, lone light focus ring) are honoured by their pairing rules. 4 Every
semantic role has a value in every shipped mode (dual-parity posture C documented in §11).
5 Every fetching surface has loading/empty/error/offline specified. 6 Every component row lists
disabled and loading states. 7 Row, header, toolbar and pagination heights agree (28px D /
40–44px S). 8 Reduced-motion variant written for every authored motion, including the shimmer.
9 Every control keyboard-reachable with a visible focus indicator. 10 Both modes authored, not
filtered, with per-mode border strength and error-text steps. 11 No unoverridden stock library
default inside a committed surface. 12 Nothing in the Studio came from the marketing poster —
display type, two-tone headlines and green panel art stay on supabase.com. 13 The §9 brand-moment
palette (the large green product-panel field) appears nowhere in the UI token layers.
