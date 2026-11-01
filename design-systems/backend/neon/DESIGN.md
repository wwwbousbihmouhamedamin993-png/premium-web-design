# Design System — Neon (Serverless Postgres)

<!-- premium-web-design:design-system 1 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: premium-marketing-design sibling spec (devtools/neon, rung 1 — raw palette family, Inter + Geist Mono, pill-vs-rectangle tension), design-extractor.com/gallery/neon extraction (marketing token values, radius ladder, elevation recipe), pixel-sampled console screenshots in screens/ (dashboard, branches, tables, SQL editor, schema diff, create-project) for the product-surface ramp, accent scarcity and density. Sibling catalog metadata listed canvas as #285d49; that value is the muted visualization green, not a canvas — corrected here against sampled evidence. -->
<!-- Surface classes: 9 routes classified; density classes F/S/D assigned (F onboarding + create-project, S project dashboard + branch overview, D branches table + tables editor + monitoring + SQL editor results) -->

## 1. Design Posture & Atmosphere

Neon is serverless Postgres with branching: separate storage and compute, instant branch
creation, scale to zero. Its two surfaces share one psychology. The marketing site (neon.com)
is a **black server room after dark** — a pure black void where the only light sources are
white type and a single electric green that reads as terminal output. The console
(console.neon.tech) is the **operator's desk in that same room**: one step back from pure
black to an elevated dark gray, hairline-drawn panels, monospaced identifiers everywhere, and
the green spent like an indicator lamp — on status dots, the auth toggle, chart series, focus
— never on large fills. After eight hours in the console nothing glares: the canvas is a
steady dark gray, accents stay under a dozen small elements per screen, and the loudest thing
on screen is usually a number.

Against its category's defaults (Supabase's emerald-on-slate, Firebase's blue material
console, PlanetScale's light minimalism), Neon sits **dark-only, near-monochrome, and
type-driven**. Display headlines are set in a light weight where competitors go bold —
emphasis is achieved by colour contrast (muted gray lead phrase, white continuation) rather
than weight. Depth comes from tonal surface steps plus 1px hairlines plus a 5%-white ring,
never from visible drop shadows. Density is Standard on dashboards, Dense on tables,
monitoring and query results, and the two-tone headline recipe (gray lead, white payload) is
the single strongest brand signature. The visual metaphor: **an instrument panel in a dark
server room** — every light is a status, every number is a measurement, and the room itself
stays black.

**Key Characteristics**
- Two canvases, one system: marketing canvas is pure black `#000000`; console canvas is an
  elevated dark gray `#181818` (pixel-sampled family `#161616–#191919` across screens).
- One brand accent: green `#34d59a` (sampled in-console renderings `#34c18e–#38c38f`).
  Accent budget: status dots, one toggle, chart series, focus ring, the logo — roughly 6–10
  small green elements per viewport, never a green fill behind text.
- Secondary hues are strictly rationed: blue `#34a0ff` only for compute units and links,
  pink `#ff467d` only for destructive actions, yellow `#ffed9c` only for annotations.
- Depth = tonal steps (`#0c0d0d`, `#18191b`, `#262626`) + 1px hairlines + a 1px ring of white
  at 5%; shadows are black-on-black soft ambients used only on floating layers.
- Shape dichotomy is the brand rule: **pills mean "click me", rectangles mean content** —
  9999px pill for CTAs, search and status badges; 4–8px rectangles for cards, inputs, panels.
- Inter 400/500 does all interface talking on marketing (display set at 400; emphasis by
  colour, not weight); the console adds 600 for page titles and primary controls.
- Geist Mono is the identity font for data: connection strings, branch IDs, SQL, giant ghosted
  section numerals (up to 128px at 10% opacity), mono eyebrows, stat values.
- Two-tone headline recipe: 44px/400, −1.76px tracking, lead phrase in `#797d86`,
  continuation in `#ffffff`.
- Identifiers are always monospaced: branch names (`br-divine-river-a5kxcqo9`), table names,
  timestamps, connection strings; metrics are always tabular numerals (`.25 CU`, `0.02 h`,
  `29.38 MiB`, `51ms`).
- Charts use a fixed two-series pair — brand green + compute blue — never a rainbow.
- Console sidebar is grouped and uppercase-labelled: PROJECT, BRANCH, RESOURCES.
- Status is a dot + word pill (`ACTIVE` green dot, `IDLE` gray dot), never colour alone.
- Whitespace is generous on marketing (128px section rhythm); the console is compact but
  never cramped — 40px standard rows, 32px dense rows.
- No gradients in product UI; glow belongs to imagery and the og graphics only.

## 2. Token Architecture

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to
a **primitive**; nothing skips a layer.
- **L1 Primitive** — literal values named by value, referenced only by L2:
  `void #000000` · `well #0c0d0d` · `raised #18191b` · `cardwell #111315` · `statpanel #0d221a`
  · `console.canvas #181818` · `console.raised #262626` · `console.hairline #303030`
  · `hairline #303236` · `ring.white05` white at 5% · `green.brand #34d59a` ·
  `green.signal #38a57d` · `green.mint #cae6dc` · `green.deep #285d49` · `teal.viz #1fd9c4` ·
  `yellow.note #ffed9c` · `red.alert #ff3621` · `pink.destructive #ff467d` ·
  `pink.text #ff8fae` · `blue.compute #34a0ff` · ink ramp `#ffffff #efeff1 #e4e5e7 #d7d8db
  #c9cbcf #afb1b6 #94979e #797d86 #61646b` · `on.primary #0c0d0d`.
  Banned: component-named primitives (`--card-bg`, `--tooltip-color`) — one value, many roles.
- **L2 Semantic** — role names (`surface.canvas`, `surface.raised`, `text.primary`,
  `accent.action`, `status.error`, `chart.series1`). The only layer a component may consume.
  Every role carries its value in §3; the product ships one mode (dark), so each role has
  exactly one shipped value — the Light column records "—" by definition.
- **L3 Component** — only deliberate deviation, pointing at L2 or L1:
  `branch.badge-default → surface.selected + text.secondary (uppercase mono)` ·
  `compute.cu → blue.compute + tabular numerals` · `diff.added → green.brand wash 12%` ·
  `diff.removed → red.alert wash 18%` · `editor.comment → purple.ink #c678dd` ·
  `chart.series1 → green.brand` · `chart.series2 → blue.compute` ·
  `sidebar.heading → text.tertiary + 10px uppercase + +8% tracking`.
  Never a raw value, never a sibling component's token.

**Rules.** Every token has a determinable type (colour, dimension, font-family, duration,
cubic-bezier) or it is invalid; names are case-sensitive and free of `$`, `{`, `}` and dots;
circular references are an error. Every semantic token resolves in the shipped mode — the
console and marketing share one semantic vocabulary with two context bindings
(`surface.canvas` binds to `void` on marketing, `console.canvas` in the console); a role that
cannot exist in a context is documented, never silently absent. Animatable tokens (drawer
offset, dropdown height, chart draw) are registered with explicit syntax and inheritance
declarations; initial values are computationally independent, so percentages are illegal as
initial values.

**Layer order (low → high):** `reset → primitives → semantic → components → utilities`.
Order beats specificity entirely, so a stray un-layered rule inside a component file would
outrank the whole system; anything a consumer must override without `!important` lives in the
top layer.

## 3. Colour Roles

Neon ships **dark-only** (see §10). The Light column records "—" because no light mode exists;
the Dark column is normative. Where marketing and console differ, both values are listed in
the Dark cell and the Notes column names the context.

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` | — | #181818 console · #000000 marketing | app background; console steps off pure black, marketing is the void |
| `surface.raised` | — | #262626 console · #18191b marketing | cards, panels, table headers |
| `surface.overlay` | — | #1f1f22 console · #18191b marketing | popovers, dropdown menus, command palette |
| `surface.inset` | — | #111315 marketing · #161616 console | code wells, editor gutters, stat panel wells |
| `surface.hover` | — | white at 5% over any surface | row and item hover fill |
| `surface.selected` | — | #262626 console · white at 8% marketing | active sidebar item, selected row, checked cell wash |
| `border.subtle` | — | #303030 console · #303236 marketing | 1px hairlines; decorative, never the sole control boundary |
| `border.strong` | — | #797d86 | 1px boundaries that must pass 3:1 (inputs on focus-adjacent states) |
| `border.focus` | — | #38a57d | 2px focus ring, 2px offset (4px on the logo) |
| `accent.action` | — | #ffffff | filled CTA pill (white fill, dark label) |
| `accent.onAction` | — | #0c0d0d | label on white pill; hovers to #c9cbcf fill |
| `accent.brand` | — | #34d59a | green: status dots, toggle-on, chart series 1, logo, active indicators |
| `accent.subtle` | — | green.brand at 12% | selected rows in diff views, soft washes |
| `accent.outline` | — | #61646b | outlined CTA pill border (border brightens to white on hover) |
| `text.primary` | — | #ffffff | headings, row labels, values, buttons |
| `text.secondary` | — | #c9cbcf | body copy, descriptions; also the white-pill hover fill |
| `text.tertiary` | — | #94979e | meta, inactive nav, placeholders; brightens to white on hover |
| `text.muted-strong` | — | #797d86 | heading lead-ins, input focus borders, two-tone headline lead |
| `text.faint` | — | #61646b | fine print — marketing context only (see gate row 22) |
| `text.disabled` | — | #5c5f66 | inactive controls only; exempt from SC 1.4.3, never body copy |
| `status.success` | — | #34d59a | with a dot/check glyph; `ACTIVE` compute pill |
| `status.warning` | — | #ffed9c | annotation yellow, rare; with a triangle glyph |
| `status.error` | — | glyph #ff467d · text #ff8fae | destructive fill pink `#ff467d` (white label); error text uses the lighter pink (gate row 12–13) |
| `status.info` | — | #34a0ff | compute blue doubles as info; with an info glyph |
| `chart.series1` | — | #34d59a | primary metric series |
| `chart.series2` | — | #34a0ff | secondary metric series; chart pair is fixed product-wide |
| `editor.syntax` | — | keywords #e5734f · comments #c678dd · strings #98c379 | SQL editor palette on the inset well |

Dark canvas is **not pure black in the console**: it sits in the `#161616–#262626` step family
(sampled); marketing alone uses the void. Depth in dark comes from surface steps and 1px
strokes, never from visible shadows.

**Contrast gate — computed, unrounded (4.499:1 fails). Body text ≥4.5:1; large text (≥24px,
or ≥18.5px bold) ≥3:1; UI boundaries and focus indicators ≥3:0 non-text** (W3C SC 1.4.3,
1.4.11). Ratios computed with the WCAG 2.x relative-luminance formula.

| Pairing | Ratio | Required | Verdict |
|---|---|---|---|
| text.primary #ffffff on console.canvas #181818 | 17.756:1 | 4.5:1 | PASS |
| text.primary #ffffff on console.raised #262626 | 15.134:1 | 4.5:1 | PASS |
| text.secondary #c9cbcf on console.canvas #181818 | 10.930:1 | 4.5:1 | PASS |
| text.secondary #c9cbcf on console.raised #262626 | 9.316:1 | 4.5:1 | PASS |
| text.tertiary #94979e on console.canvas #181818 | 6.071:1 | 4.5:1 | PASS |
| text.tertiary #94979e on console.raised #262626 | 5.174:1 | 4.5:1 | PASS |
| accent.onAction #0c0d0d on accent.action pill #ffffff | 19.462:1 | 4.5:1 | PASS |
| accent.brand #34d59a on console.canvas #181818 (non-text) | 9.411:1 | 3:1 | PASS |
| accent.brand #34d59a on marketing.canvas #000000 (non-text) | 11.130:1 | 3:1 | PASS |
| border.strong #797d86 on console.raised #262626 | 3.669:1 | 3:1 | PASS |
| border.strong #797d86 on console.canvas #181818 | 4.304:1 | 3:1 | PASS |
| border.focus #38a57d on console.canvas #181818 | 5.789:1 | 3:1 | PASS |
| border.focus #38a57d on marketing.canvas #000000 | 6.846:1 | 3:1 | PASS |
| status.success #34d59a dot on console.canvas #181818 | 9.411:1 | 3:1 | PASS |
| status.error text #ff8fae on console.canvas #181818 | 8.280:1 | 4.5:1 | PASS |
| status.error glyph/fill #ff467d on console.canvas #181818 | 5.432:1 | 3:1 non-text | PASS |
| status.warning #ffed9c on console.canvas #181818 | 15.089:1 | 4.5:1 | PASS |
| status.info #34a0ff on console.canvas #181818 | 6.442:1 | 4.5:1 | PASS |
| chart.series1 #34d59a on console.raised #262626 | 8.021:1 | 3:1 non-text | PASS |
| chart.series2 #34a0ff on console.raised #262626 | 5.490:1 | 3:1 non-text | PASS |
| text.primary #ffffff on marketing.canvas #000000 | 21.000:1 | 4.5:1 | PASS |
| text.secondary #c9cbcf on marketing.canvas #000000 | 12.927:1 | 4.5:1 | PASS |
| text.tertiary #94979e on marketing.canvas #000000 | 7.180:1 | 4.5:1 | PASS |
| text.faint #61646b on marketing.canvas #000000 | 3.543:1 | 3:1 house floor (large/legal) | PASS |
| text.faint #61646b on console.canvas #181818 | 2.996:1 | 3:1 house floor | FAIL — restricted |
| border.subtle #303236 on marketing.canvas #000000 | 1.635:1 | decorative only | DOCUMENTED |
| border.subtle #303030 on console.canvas #181818 | 1.345:1 | decorative only | DOCUMENTED |

The two non-passing rows are managed by restriction, not by redefining the palette:
`text.faint` is banned inside the console (fine print there steps up to `text.tertiary`,
6.071:1) and exists only on the marketing void where it clears 3:1 for its large/legal use.
`border.subtle` hairlines are decorative separators — any control that relies on its border
for identification upgrades to `border.strong` or carries a text label. `text.disabled`
(#5c5f66, ~2.6:1) is SC-exempt inactive-component text only.

## 4. Typography

**Families.** UI **Inter** (400/500 marketing; console adds 600), self-hosted woff2,
preloaded, fallback system sans. Numeric/code **Geist Mono** (400/500/600) for identifiers,
connection strings, branch and table names, timestamps, SQL, mono eyebrows and ghosted
section numerals; fallback ui-monospace stack. *Monospace is for identifiers and code, never
a costume* — a mono word inside a sans sentence is a defect unless it is an identifier.
Display emphasis on marketing is achieved with colour (gray lead → white payload), never by
bolding; large display sizes are set at 400.

**One ramp table per class, not one blended table.**

- **F Focused, 16px base** — onboarding, create-project form, restore flows, dialogs:
| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Title | 24px | 600 | 32px | −0.4px | — | "Create project", dialog titles |
| Heading | 16px | 500 | 24px | 0 | — | form group headings "Region" |
| Body | 16px | 400 | 24px (1.5) | 0 | — | helper copy under fields |
| Label | 14px | 500 | 20px | 0 | — | field labels, buttons |
| Meta | 13px | 400 | 18px | 0 | — | "Select the region closest to your application." |

- **S Standard, 14px base** — project dashboard, branch overview, settings (console default):
| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Page title | 24px | 600 | 32px | −0.4px | — | "Branch Overview", "Monitoring" |
| Section title | 16px | 500 | 24px | 0 | — | "Compute settings", "RAM", "CPU" |
| Body | 14px | 400 | 22px | 0 | — | descriptions, checklist sublines |
| Row primary | 14px | 500 | 20px | 0 | tabular | branch names, table row labels |
| Row secondary | 13px | 400 | 20px | 0 | tabular | "0.02 h", "29.38 MiB", dates |
| Stat value | 28px | 500 | 34px | −0.4px | tabular | usage figures on the dashboard |
| Stat label | 12px | 500 | 16px | +8% uppercase | — | "CONNECTIONS COUNT", "PERCENTAGE" |
| Sidebar item | 13px | 400 | 20px | 0 | — | Dashboard, Branches, SQL Editor |
| Sidebar heading | 10px | 500 | 16px | +8% uppercase | — | "PROJECT", "BRANCH", "RESOURCES" |
| Button | 14px | 500 | 20px | −0.2px | — | "Create child branch", "Refresh" |

- **D Dense, 12–13px base** — branches table, tables editor, monitoring charts, SQL results:
| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Grid header | 13px | 500 | 18px | 0 | — | "Branch · Parent · Compute hours · Primary compute · Data size" |
| Grid cell text | 13px | 400 | 18px | 0 | — | cell prose |
| Grid cell numeric | 13px | 500 | 18px | 0 | tabular | ".25 CU", "29.38 MiB", "51ms", "10 rows" |
| Grid cell identifier | 13px | 400 | 18px | 0 | mono | "br-divine-river-a5kxcqo9", "playing_with_neon" |
| Log/code line | 13px | 400 | 20px | 0 | mono | SQL editor, query history |
| Badge | 10–11px | 500 | 14px | +4% uppercase | — | "DEFAULT", "ACTIVE", "IDLE", "SCALE" |
| Inline help | 12px | 400 | 16px | 0 | — | hints under dense controls |

Prose inside a dense screen still steps up to Body 14px.

**Marketing ramp (poster surface, not the console):** hero display 56px/400/1.15 with −4%
tracking; display-lg 48px/500; title 28px/400; two-tone headline 44px/400/−1.76px; body 16px;
button 15px; nav link 13px; mono eyebrow 12px/500/+10%; mono display 128px/400 at low
opacity; micro 10px/500.

**Invariants.** Tabular numerals on every comparable value — compute hours, data sizes,
connection counts, timings, row counts, percentages. Right-align numerics, left-align text,
never centre a numeric column. Fixed stepped sizes; no fluid type. Measure ≤80 characters:
65–80ch in F/S prose, unconstrained in dense tables and code.

## 5. Spacing Scale & Density Scales

**Spacing base: 4px grid; 8px comfortable in F/S, 4px in D.** `space.0` 0 · `1` 4px
icon-to-label and badge gaps · `2` 8px control padding in D, status-dot gap · `3` 12px cell
padding in S, sidebar item padding · `4` 16px card padding in S, page gutter in D · `6` 24px
card padding in F, panel padding in S · `8` 32px section gap in S · `12` 48px region
separation · `16` 64px · `24` 96px (rare, marketing) · `32` 128px marketing section rhythm —
the vertical beat that protects the poster feel. No 17px. No 23px. If a layout needs an
off-scale value, the layout is wrong.

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | onboarding, create project, restore, dialogs |
| `standard` | 40px | 14px | 12–16px | 24px | project dashboard, branch overview, settings |
| `dense` | 32px | 12–13px | 8px | 16px | branches table, tables editor, monitoring, SQL results |

- Density comes from row height, column pruning and leading — never from type too small to
  read. A 13px tabular numeral in the branches table is correct; the same numeral in the
  create-project form is a defect.
- **Never switch mid-page.** The branch overview is Standard end to end; the branches table is
  Dense end to end. Switching across routes with different jobs is legitimate — it should feel
  like a different room.
- **Chrome follows rows.** The toolbar above the tables editor and the monitoring time-range
  strip match the table's row rhythm (32px in D). A 40px toolbar over 32px rows is a rhythm
  break.
- Marketing whitespace budget is its own world: 128px section padding, hairline-separated
  header/footer only. Console whitespace budget: Focused 55–70% · Standard 40–55% · Dense
  25–40%. House heuristic — validated against screens: the monitoring page lands near 30%
  (chart panels dominate), the branch overview near 55%.

## 6. Radius Scale

`none` 0 · `xs` 4px badges, tags, dense cells, inline code, ghost buttons (marketing default)
· `sm` 5–6px inputs, console buttons, menu items · `md` 8px console cards, panels, editor
containers · `lg` 10px marketing cards · `xl` 16px marketing feature panels, dialogs · `full`
9999px pills — CTAs, search fields, status badges, avatars, the org/project switcher.
**One radius per component family**, never mixed ad-hoc: every CTA is a pill, every content
container is a rectangle in its family's size — "pills mean 'click me' and rectangles mean
'content'" is a brand rule, not a preference. Nested radii obey
`radius_inner = radius_outer − padding` (an `xs` code chip inside an `md` panel is correct:
8 − 4 = 4). Avoid `lg`/`xl` unless the surface genuinely needs the softness.

## 7. Elevation

**Choose one strategy, never mix paradigms.** Neon's dark elevation is **tonal first**:
surfaces step lighter as they rise (`#0c0d0d → #18191b → #262626`), edges are 1px hairlines,
and cards carry a 1px ring of white at 5% that catches the "room light". Shipped soft shadows
are black-on-black ambients reserved for genuinely floating layers —
`rgba(0,0,0,0.2) 0 2px 10px` for menus, `rgba(0,0,0,0.4) 0 8px 20px` for dialogs — invisible
as colour, functional as edge separation; frosted inputs add a 16px backdrop blur.

Levels, low → high: **0** canvas (no shadow, hairline only) · **1** card/panel (one tonal
step + hairline + 5% ring) · **2** sticky header/sidebar (hairline bottom edge, canvas
background) · **3** popover/dropdown menu (tonal step + soft ambient + `border.strong`) ·
**4** dialog/Schema Diff modal (strongest ambient + scrim, `xl` radius on marketing, `md` in
console). Glow belongs to imagery and the og graphics; it is never a CSS shadow.

## 8. Motion

The shipped curve is a 0.2s standard ease (`cubic-bezier(0.4, 0, 0.2, 1)`); the scale maps to:
`instant` 0ms · `fast` 120ms ease-out (hover fills, tooltip out, dense exits) · `base` 200ms
standard ease (buttons, menus, toggles, [D] entrances) · `slow` 300ms decelerate (marketing
mega-dropdown height transition, dialogs, drawer slides).
- Entrances decelerate, exits accelerate. Symmetric ease-in-out on both directions is a
  defect (the shipped dropdown height transition is the one sanctioned 0.3s exception).
- Animate transform and opacity only — never width, height, top, left, except the sanctioned
  marketing dropdown height animation, which is outside product surfaces.
- No bounce on irreversible moments: not on "Delete 1 record", not on branch deletion, not on
  compute suspension.
- The query-run state swaps the Run button label into reserved space; the button never changes
  width between idle and running.
- **Reduced motion is a real variant**, not motion-off everywhere: chart draws become a single
  150ms crossfade, the dropdown becomes a crossfade, spinner glyphs freeze at rest
  orientation. What must be neutralised is scaling and panning of large objects, not every
  fade.

## 9. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell/sidebar | S | expanded, icon rail | default, hover, active, collapsed | Tab order top-down; group headings not focusable | "PROJECT · BRANCH · RESOURCES" |
| Org/project switcher | S | breadcrumb pill with plan badge | closed, open, plan badge | Enter opens, Esc closes, arrows navigate | "Evan's org · SCALE" |
| Data table | S/D | branches list, members, keys | loading, empty, error, row hover, selected, disabled | arrows move row focus, Enter opens | "Branch · Parent · Compute hours · Primary compute · Data size" |
| Status pill | S/D | ACTIVE (green dot), IDLE (gray dot), DEFAULT badge | on, off, disabled | read-only; skipped in tab order | "ACTIVE", "IDLE", "DEFAULT" |
| Filter/search bar | S/D | table search, header search | idle, focused, filled, no-results | shortcut-invoked, Esc clears | "Search..." |
| Row action menu | S/D | kebab per row | focus-trapped open, Esc closes | arrows + Enter, Esc exits | "Rename · Duplicate · Delete" |
| Branch overview checklist | S | numbered next-step card | pending, done (check), dismissed | Enter activates step action | "Restored the snapshot to this new branch" |
| Primary pill CTA | F/S | white pill, outlined pill | idle, hover (#c9cbcf), focus ring, loading (label swap) | Enter activates; visible ring | "Create child branch 2/10", "Compare" |
| Destructive button | S/D | pink fill | idle, confirming (typed confirmation), disabled | Enter opens confirm dialog | "Delete 1 record" |
| Compute endpoint chip | S/D | branch + compute pill | RW/RO, ACTIVE, IDLE, suspended | Enter opens endpoint drawer | "RW · IDLE" |
| Monitoring chart panel | D | RAM, CPU, connections, buffer cache | loading (skeleton axes), empty ("no data yet"), error | legend toggles series | "CONNECTIONS COUNT · ACTIVE IDLE TOTAL" |
| Time-range control | D | segmented pill | Last hour, Last day, Last 7 days, custom | arrows move segment | "Last hour · Refresh" |
| SQL editor | D | query tabs, Saved/History rail | running, connected, error, results paging | shortcut-run, tab arrows | "Run · Explain · Analyze · Connected (3 queries) · 51ms 10 rows" |
| Tables editor | D | data view, studio view | editing cell, selected row, bulk selected | Enter edits, Esc cancels | "Filters · Columns · Add record · Delete 1 record" |
| Schema Diff dialog | F | branch 1 vs branch 2 | comparing, empty diff, error | focus trap, Esc closes | "Compare · Latest available data (head)" |
| Create-project form | F | name, region, version, auth toggle | validating, creating, error | logical tab order | "my-app · AWS US East 1 (N. Virginia) · Enable Neon Auth" |
| Toggle | F/S | on/off switch | on (green), off, disabled | Space toggles | "Enable Neon Auth" |
| Command palette | S | global actions + navigation | open, querying, no-results | shortcut-invoked, arrows, Esc | "Jump to... Search documentation" |

Every fetching surface also designs: **loading** — skeleton matching final geometry (chart
panels render ghost axes and gridlines, tables render 8 ghost rows; never a centred spinner
on a blank page); **empty** — what is missing plus the CTA that fixes it ("No branches yet —
Create your first branch"); **error** — what happened plus recovery ("Couldn't load
monitoring — Retry"); **offline/stale** — last known values stay visible dimmed to
`text.tertiary` with a "Showing cached usage" note.

**Contracts this table encodes:** one primary filled CTA per view in F/S (dense toolbars may
run a primary plus icon actions — the tables editor's white "Add record" beside the pink
"Delete 1 record" is the sanctioned dense exception: add is primary, delete is destructive,
never two neutrals); every icon-only control carries a label or tooltip; a disabled control
states why on focus or hover ("Protect" renders disabled with its shield glyph while the plan
lacks the feature); a button never changes width between idle and loading.

## 10. Light / Dark Strategy

- **Posture: B dark-only.** Both the marketing site and the console ship a single dark mode.
  Reason: the brand is "the dark server room" — the og imagery, the wordmark rendering, the
  product screenshots and the console all assume a dark canvas; a light mode would break the
  single visual metaphor the product is known by.
- **Mechanism:** semantic roles are bound once (§3 Dark column); there is no per-mode remap.
  No role is absent in the shipped mode. Marketing and console differ only in the context
  binding of `surface.canvas`/`surface.raised`/`border.subtle` (void-and-hairline vs
  elevated-gray), which is a documented L2 context binding, not a second mode.
- **`color-scheme`** is set dark at the root so UA chrome, form controls and scrollbars render
  dark natively.
- **The scheme meta tag sits in the head before the stylesheet** so neither surface ever
  flashes light on load.
- **Dark is authored, not inverted:** its own surface ramp, its own border strength (the
  console hairline `#303030` is stronger than a light-mode hairline would be — a delicate
  line on white would vanish here), its own error-text variant (`#ff8fae` for text, `#ff467d`
  for fills), and black-on-black soft shadows that work only because surfaces step lighter
  than the canvas. `light-dark()` colour functions are unnecessary for a dark-only product;
  if a light mode ever ships it must be a full authored set, not a filter.
- Org tinting is not offered. Brand colour changes ship as token releases, not runtime themes.

## 11. Density-Mode Strategy

- **Default mode per surface class:** Standard on the project dashboard, branch overview and
  settings; Dense on branches table, tables editor, monitoring and SQL results; Focused on
  onboarding, create-project and restore flows. The boundary is the job: reading status → S;
  scanning volume → D; acting once → F.
- **Mechanism:** a density attribute on the app root rescales row height, cell padding, gutter
  and body size together as one token axis — spacing tokens do not change values per screen
  size; density is not a media query.
- **Container queries for reflow:** panels and the tables editor reflow to their container,
  not the viewport; size queries fail closed with no eligible container, and container query
  units silently resolve to small-viewport units there — so container query units are never
  used where that fallback would be wrong.
- **Style queries** compare computed values, so the density marker is registered as a custom
  property with concrete syntax and inheritance before any style query reads it.
- **The switch is offered as an accessibility affordance**, not a preference: a density
  control honours users with visual field loss who need roomier rows, per the W3C note on SC
  2.5.8. In the console the practical form is column pruning plus row-height relief on data
  tables, never shrinking type below the D floor.

## 12. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA contrast (7:1) for the two-tone headline payload and
  stat values where feasible.
- **Target size:** ≥24×24 CSS px hard minimum, 44px design target for primary controls in F/S
  (pills measure 38–44px tall); the spacing exception applies to the dense status dots — a
  24px circle centred on each target's bounding box must not intersect another's. Zoom does
  not excuse it.
- **Keyboard:** every function operable (SC 2.1.1) — sidebar, switcher, tables editor cell
  navigation, query tabs and the Schema Diff dialog are fully keyboard-driven; focus indicator
  visible (SC 2.4.7): the 2px `#38a57d` ring at 2px offset, never removed without a stronger
  replacement; the focused item is never entirely hidden by the sticky header (SC 2.4.11).
- **Contrast:** text ≥4.5:1 (all ink roles pass — §3 gate); UI boundaries and focus ≥3:1
  (border.strong and border.focus pass; border.subtle is decorative-only). **Colour
  independence:** every status pairs colour with a word pill or glyph (`ACTIVE`/`IDLE` carry
  both a dot and a word); chart series carry labelled legends, not colour alone; deltas carry
  a sign and direction glyph.
- **Motion:** the §8 reduced-motion variant per component; no parallax on marketing.
- **Text:** ≤80-character measure (marketing body 16px at ~65ch), 1.5 leading on body, 200%
  text resize without horizontal scroll (SC 1.4.8).
- **Semantics:** real buttons, links and inputs; the sidebar is a navigation landmark with
  grouped lists; headings match visual rank (page title h1, panels h2); live regions announce
  query completion and usage refreshes politely; the loading tables region is marked busy.
- **Contrast preference:** if `prefers-contrast: more` is honoured, hairlines upgrade to
  `border.strong`, `text.tertiary` steps to `text.secondary`, and the 5% ring doubles to 10%.

## 13. Anti-Patterns

Product-calibrated; each ban carries the reason it was rejected *for this product*.

**Do**
- Spend green like an indicator lamp: dots, toggle, focus, chart series, logo — 6–10 small
  elements per viewport. The green IS the brand; scarcity is what makes it read as signal.
- Keep the shape dichotomy absolute: pills for clickables, rectangles for content.
- Set marketing display type at 400 and emphasise with the two-tone colour recipe.
- Use Geist Mono for every identifier, connection string and code surface.
- Bind metrics to tabular numerals and right-align them.
- Achieve depth with tonal steps + hairlines + the 5% white ring.
- Keep the two chart series fixed: brand green + compute blue, product-wide.
- Label every status with a word pill, not a colour alone.
- Reserve destructive pink for exactly one element per view.
- Group the sidebar (PROJECT / BRANCH / RESOURCES) and keep group headings at 10px uppercase.
- Match toolbar and pagination heights to table row heights.
- Protect the 128px marketing section rhythm; it is the poster's heartbeat.

**Don't**
- No green fills behind body text or large green surfaces — the accent is not a background.
- No gradients in product UI; glow belongs to imagery and og graphics only.
- No visible coloured drop shadows; depth is tonal, not shadowed.
- No light mode, no "auto" theme toggle — the room is dark; shipping half a palette breaks it.
- No mixing radii ad-hoc: a rounded-card button next to a pill button in the same toolbar is
  a defect (except the sanctioned dense toolbar: white primary + pink destructive).
- No marketing poster aesthetics inside the console: no 128px section padding, no ghost
  numerals, no two-tone headlines on data screens.
- No card inflation: information-dense panels stay panels, not floating card grids.
- No stat-card dashboards: usage reads as one measurement strip with tabular values, not a
  grid of greeting cards.
- No modals as connective tissue; the Schema Diff dialog is a tool, not a navigation pattern.
- No hover-only affordances on data rows — row menus are focusable and keyboard-reachable.
- No placeholder-as-label in forms ("my-app" is sample value copy, the label "Project name"
  persists).
- No whole-page spinners; skeletons match final geometry.
- No `alert()`-style blocking dialogs for confirmations; destructive flows use an in-product
  confirm with typed or explicit confirmation.
- No tiny type as a density strategy: 13px is the dense floor, and it is for numerals and
  identifiers, not prose.

## 14. Quick Reference & Verification Gate

**Colour (role → value; single dark mode; context noted):**

| Role | Token | Value |
|---|---|---|
| Canvas (console) | surface.canvas | #181818 |
| Canvas (marketing) | surface.canvas | #000000 |
| Raised (console) | surface.raised | #262626 |
| Raised (marketing) | surface.raised | #18191b |
| Inset well | surface.inset | #111315 |
| Hairline (console) | border.subtle | #303030 |
| Hairline (marketing) | border.subtle | #303236 |
| Strong boundary | border.strong | #797d86 |
| Focus ring | border.focus | #38a57d |
| Action fill | accent.action | #ffffff |
| On-action label | accent.onAction | #0c0d0d |
| Brand accent | accent.brand | #34d59a |
| Destructive fill | status.error fill | #ff467d |
| Error text | status.error text | #ff8fae |
| Warning | status.warning | #ffed9c |
| Info / compute blue | status.info | #34a0ff |
| Primary ink | text.primary | #ffffff |
| Secondary ink | text.secondary | #c9cbcf |
| Tertiary ink | text.tertiary | #94979e |
| Muted-strong | text.muted-strong | #797d86 |
| Faint (marketing only) | text.faint | #61646b |
| Chart series 1 | chart.series1 | #34d59a |
| Chart series 2 | chart.series2 | #34a0ff |

**Type ramp (flat):** F Title 24/600 · F Body 16/400 · S Page title 24/600 · S Body 14/400 ·
S Row primary 14/500 tabular · S Stat value 28/500 tabular · S Sidebar item 13/400 ·
D Grid header 13/500 · D Cell numeric 13/500 tabular · D Identifier 13/400 mono ·
D Code line 13/400 mono · Marketing display 56/400 · two-tone headline 44/400 · mono display
128/400. Inter everywhere; Geist Mono for identifiers, code, eyebrows, ghost numerals.

**Spacing + radius (flat):** base 4px · scale 0/4/8/12/16/24/32/48/64/96/128 · section
rhythm 128px marketing · rows 40px S / 32px D · gutters 24px S / 16px D · radii 4/5–6/8/10/16/
9999 · pills for CTAs and badges, rectangles for content.

**Component → token map:** white pill CTA consumes `accent.action` + `accent.onAction` +
`radius.full` + `border.focus` on focus; data table consumes `surface.raised` (header) +
`surface.canvas` (rows) + `border.subtle` (grid lines) + `text.primary`/`text.secondary` +
tabular numerals + `radius.xs` badges; status pill consumes `status.success`/`neutral` dot +
`text.primary` word + `surface.raised` pill + `radius.full`; monitoring panel consumes
`surface.raised` + `border.subtle` + `text.secondary` labels + `chart.series1/2`; SQL editor
consumes `surface.inset` + `editor.syntax` + mono family; sidebar consumes `surface.canvas` +
`text.tertiary` items (white on active/hover) + 10px uppercase headings; destructive button
consumes `status.error` fill + `#ffffff` label + confirm contract.

**Pre-ship checklist.** 1 Zero raw hex outside L1. 2 No token resolves to a component name.
3 Every contrast pairing computed, passing, unrounded — the two restricted pairings
(text.faint, border.subtle) are honoured by their usage rules. 4 Every semantic role has a
value in the shipped mode (dark-only posture B documented in §10). 5 Every fetching surface
has loading/empty/error/offline specified. 6 Every component row lists disabled and loading
states. 7 Row, header, toolbar and pagination heights agree (40px S / 32px D). 8 Reduced-motion
variant written for every authored motion. 9 Every control keyboard-reachable with a visible
focus ring. 10 Dark authored, not filtered, with console border strength exceeding what a
light hairline would be. 11 No unoverridden stock library default inside a committed surface.
12 Nothing in the console came from a marketing page — poster devices (ghost numerals,
two-tone headlines, 128px rhythm) stay on neon.com.
