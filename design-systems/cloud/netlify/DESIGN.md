# Design System — Netlify (app.netlify.com)

<!-- premium-web-design:design-system 2 -->
<!-- As-of: 2026-11-02 -->
<!-- Reference inspirations: Netlify app shipped stylesheet app.netlify.com assets (Facets primitive scales as rgb-triplet tokens, semantic role aliases for light and dark, focus-ring tokens, button system with pill radius and stripe-loading — rung 2, extracted from the production CSS the app ships today), netlify.com marketing stylesheet (Figtree / Instrument Sans / Martian Mono families, brand teal #00C7B7, navy #060B10 — rung 2), Netlify blog "A Spark of Inspiration: Netlify's New Logo" (spark identity, 2023 rebrand — rung 2), screens/ verified captures of the app's deploys screen, deploy log, AI deploy diagnostics and site-configuration form plus netlify.com homepage and pricing (rung 3 grounding; sampled pixels confirm the teal-100 button fill, the #181A1C code block, the red-000 error wash and the dark-teal log canvas). Ladder: rung 1 missed (no sibling spec for netlify); rung 2 supplied the spec; rung 3 grounded it. -->
<!-- Surface classes: 12 routes classified; density classes F/S/D assigned (F auth + destructive confirms + plan change; S team overview + site overview + site configuration + forms + domain management + members; D deploy logs + function logs + log explorer + deploy tables + audit) -->

## 1. Design Posture & Atmosphere

Netlify is the platform where a `git push` becomes a live URL; its app is the room where you watch
that happen. The posture is **the launch console for the web**: a bright, near-white workspace
organised around one repeated drama — the deploy — where every surface exists to answer "did it
ship, and if not, why not". The canvas is white and a 2%-ink tint; cards sit on 1px hairlines; the
action colour is the brand teal itself, which is the system's central and unusual decision: unlike
consoles that keep brand and verb apart, Netlify lets one family carry both. The app-scale teal
`#02807D` fills primary actions while the marketing-scale teal `#00C7B7` stays on the marketing
site and the logo spark; after eight hours of on-call log-reading, the loudest thing on screen is
a status pill or a line number in teal.

The second face is the **log canvas**: deploy logs, function logs and build logs flip to a dark
blue-teal well (`#0D1E24`) inside the light shell, mono type, teal line numbers, a dark-teal
selection wash. This is the one place Netlify inverts — logs are read in long sittings, and the
inversion marks them as machine territory, not page territory. Dark mode proper is an authored
theme, not a filter: a blue-black canvas (`#0A1016`, studio variant `#030F14`), white ink, teal
lifted to `#14D8D4` so the verb stays teal.

Against its category (AWS's slate-grey density, GCP's card-heavy material surfaces, Azure's
fluent panels, Cloudflare's blue-on-white quiet), Netlify's app is the **friendliest of the
consoles**: pill-shaped buttons (the only major console whose default button is a full pill),
sentence-case headings, a star mascot allowed exactly one celebratory corner, easter-egg "Play
game" panels on finished deploys. Whimsy is budgeted; the data surfaces themselves are dry. The
visual metaphor, stated plainly: **mission control with a smile** — precise mono for machines,
rounded geometry for humans, and teal meaning "go".

**Key Characteristics**
- Two canvases, one shell: light app default (white raised surfaces on a `#FAFAFA` page tint =
  2% `#181A1C` over white) and an authored dark theme (canvas `#0A1016`; studio variant `#030F14`);
  the log well is a third, always-dark surface (`#0D1E24`) inside the light shell.
- **Teal is both brand and verb:** app action teal `#02807D` (light) / `#14D8D4` (dark); the
  standard primary button inverts the formula — light-teal `#8EFBF7` fill with dark-teal `#014847`
  label; marketing teal `#00C7B7` never enters app UI tokens.
- Interface typeface is the **system UI stack** (no webfont in the app shell) at a 14px base,
  weights 400/500/600 only; marketing site carries the display identity: Figtree for display,
  Instrument Sans for text, Martian Mono for code moments.
- Mono (`ui-monospace` stack) is reserved for identifiers: commit hashes, deploy IDs, log lines,
  code blocks, the marketing `fetch https://netlify.ai` bar — never a costume.
- Signature control: the **pill button** — default 36px min-height, 14px label, full-pill radius;
  sizes 36/28/24px; saving state is a 1s diagonal stripe sweep, never a width change.
- Status is a **wash + ink + glyph** pill: green Complete, red failure banner, gold warning —
  colour never travels alone.
- Deploy rows are two-line (~64px): title + mono `branch@sha` line, right-aligned tabular time and
  "Deployed in 2m 29s"; list chrome (search, filters, Trigger deploy) sits in one row band.
- Shape ladder: 4px xs chips/inputs-micro · 6px inputs, small controls · 12px dialogs, popovers ·
  16px cards/panels · full pill for buttons, status badges, avatars.
- Focus is a 2px teal ring (`#02807D` light, `#8EFBF7` dark) plus offset; hover fills are 3-4% ink
  tints, never shadows.
- Motion budget: 0.2s ease on interactive colour; entrances decelerate; the only loop is the
  loading stripe sweep; celebration confetti exists and is confined to first-success moments.
- Density: standard rows 40-44px, dense log lines 24px, two-line deploy rows 64px; chrome always
  matches the row band it fronts.
- Whimsy budget: one mascot, one easter egg per context; a "Play game" panel may appear where a
  deploy succeeded — never on a data table, never on failure.

## 2. Token Architecture   ← normative

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value* (`facets.teal.600`), referenced only by L2.
  The app ships its primitives as rgb-triplet scales ("Facets"); this spec records them as hex.
  Neutrals light: `neutral-000 #FFFFFF` · `100 #F6F6F7` · `200 #E9EBED` · `300 #D1D5DA` ·
  `400 #9DA7B2` · `500 #778089` · `600 #545A61` · `700 #353A3E` · `800 #181A1C`. Neutrals dark:
  `night-000 #FFFFFF` · `100 #E6ECF2` · `200 #ABB5BF` · `300 #7E8792` · `400 #4D565F` ·
  `500 #3B434C` · `600 #272F38` · `700 #1E242C` · `800 #12181F` · `900 #060B10`. Teal:
  `teal-000 #DEFFFE` · `100 #8EFBF7` · `200 #32E6E2` · `300 #14D8D4` · `400 #05BDBA` ·
  `500 #04A29F` · `600 #02807D` · `700 #016968` · `800 #014847` · `900 #0C2A2A`. Green:
  `green-000 #E7FCE9` · `100 #BEF9C6` · `300 #64D87F` · `500 #31A855` · `600 #228240` ·
  `700 #1A6B34` · `800 #0F4A21`. Red: `red-000 #FBEEED` · `100 #FBD3D0` · `400 #FE8382` ·
  `500 #FE4E5C` · `600 #D62740` · `700 #AF2536` · `800 #800A20`. Gold: `gold-000 #FDF5D8` ·
  `100 #F6E0A5` · `300 #FBB13D` · `400 #F98E21` · `500 #D5771A` · `600 #A85D13` · `800 #603408`.
  Blue: `blue-000 #EDF4FF` · `100 #CDE2FF` · `500 #5D8DF5` · `600 #316BF4` · `700 #2E51ED` ·
  `800 #2036A1` · `900 #1B205B`. Accents: `purple-500 #9B80ED` · `purple-600 #775CE7` ·
  `pink-500 #DF5ADC`. Marketing-only (excluded from app tokens): `brand-teal #00C7B7`,
  `brand-navy #060B10`. Banned: component-named primitives — one value, many roles.
- **L2 Semantic** — role names (`surface.canvas`, `text.primary`, `accent.action`,
  `border.focus`, `status.error.ink`). The only layer a component may consume. Every role carries
  a value in **both** shipped modes (§3); dark is a re-binding of the same primitive pool, not a
  second vocabulary. Mode is declared once on the app root; a role with no dark value is invalid
  by definition. A secondary brand theme (studio) re-binds a subset of primitives to the newer
  Hues scale and tightens the focus ring to 2px — it changes colour bindings only, never geometry.
- **L3 Component** — only for deliberate deviation, pointing at L2 or L1, never at a raw value and
  never at a sibling component's token: `button.primary.standard → accent.subtle fill +
  accent.onAction label, hover accent.bright` · `button.primary.action → accent.action fill +
  onAction label` · `log.well → surface.inset + mono 13px + status.info numerals` ·
  `badge.status → status.*.wash fill + status.*.ink label + glyph` ·
  `code.block → surface.code + text.inverse` · `skeleton → surface.hover with 1s stripe sweep` ·
  `deploy.row → 64px two-line + mono identifier + tabular right column`.

**Rules.** Every token has a determinable type (colour, dimension, font-family, duration, easing)
or it is invalid; names are case-sensitive and free of `$`, `{`, `}` and dots; circular references
are an error. Every semantic token resolves in both modes — the studio theme is a colour-only
re-binding and is forbidden from moving radii, type sizes or spacing. Animatable tokens (the
stripe sweep, dialog fade) are declared with explicit syntax and inheritance behaviour;
initial values are computationally independent, so percentage-based initial values are illegal.

**Layer order (low → high):** `reset → primitives → semantic → components → utilities`. Order
beats specificity entirely, so a stray un-layered declaration in a component file would outrank
the whole system; anything a consumer must override without forcing priority lives in the top
layer. A lint rule flags any raw hex consumed by a component; the only sanctioned literal
exceptions are pure white and pure black for content that must stay literal (log gutters, scrim).

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` | #FAFAFA | #0A1016 | page background; 2% #181A1C tint over white / blue-black, never pure |
| `surface.raised` | #FFFFFF | #12181F | cards, panels, table base, sidebar |
| `surface.overlay` | #FFFFFF | #1E242C | popovers, command palette, drawers |
| `surface.inset` | #0D1E24 | #0D1E24 | log wells, code blocks — dark in both modes |
| `surface.code` | #181A1C | #161B1E | inline code / snippet blocks |
| `surface.hover` | #F7F8F8 (3% ink) | #1A2129 (4% white) | interaction fill on rows and items |
| `surface.selected` | #EFF1F1 (6% ink) | #27303A (10% white) | selected row, active nav item |
| `border.subtle` | #E9EBED | #272F38 | 1px hairlines, card edges, dividers |
| `border.strong` | #778089 | #7E8792 | 1px outlines that must read (inputs, outline buttons) |
| `border.focus` | #02807D | #8EFBF7 | 2px focus ring + 2px offset |
| `accent.action` | #02807D | #14D8D4 | primary action fill, links, active nav |
| `accent.onAction` | #FFFFFF | #0C2A2A | label on accent.action fill |
| `accent.subtle` | #8EFBF7 | #0F5149 | standard primary button fill, AI-button fill |
| `accent.onSubtle` | #014847 | #8EFBF7 | label on accent.subtle fill |
| `accent.bright` | #32E6E2 | #14D8D4 | hover on standard primary fill |
| `text.primary` | #181A1C | #FFFFFF | loud ink; headings, row titles |
| `text.secondary` | #353A3E | #E6ECF2 | body ink |
| `text.tertiary` | #545A61 | #ABB5BF | muted ink, secondary row line, help |
| `text.disabled` | #778089 | #4D565F | placeholder, disabled labels — 3:1 floor, carries no information |
| `text.inverse` | #FFFFFF | #FFFFFF | ink on inset/code wells |
| `status.success.ink` | #1A6B34 | #31A855 | on success wash / dark canvas; check glyph always |
| `status.success.wash` | #E7FCE9 | #0F2A1A | Complete pills, passing checks |
| `status.warning.ink` | #A85D13 | #F98E21 | on warning wash; triangle glyph always |
| `status.warning.wash` | #FDF5D8 | #2E2005 | quota/build warnings |
| `status.error.ink` | #AF2536 | #FE4E5C | failure banners, destructive labels |
| `status.error.wash` | #FBEEED | #2C0D12 | failed deploys, form errors |
| `status.info.ink` | #2E51ED | #5D8DF5 | informational pills, build metadata |
| `status.info.wash` | #EDF4FF | #101B33 | beta tags, hints |
| `fill.danger` | #D62740 | #800A20 | destructive button fill (hover #AF2536 light / #AF2536 dark) |

Dark canvas is **not** pure black: `#0A1016` app / `#030F14` studio (a blue-black, never `#000`).
Depth in dark comes from surface steps (`#12181F` → `#1E242C`) and 1px strokes (`#272F38`), never
shadows. The marketing palette (`#00C7B7` teal, `#060B10` navy) is confined to §9's brand moment.

**Contrast gate — computed, not asserted; unrounded; 4.499:1 fails.** Large text ≥24px or
≥18.5px bold; body ≥4.5:1; UI boundaries and focus indicators ≥3:1.

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| text.primary | #181A1C | surface.canvas | #FAFAFA | 16.719:1 | 4.5 | PASS |
| text.primary (on raised) | #181A1C | surface.raised | #FFFFFF | 17.451:1 | 4.5 | PASS |
| text.secondary | #353A3E | surface.canvas | #FAFAFA | 11.017:1 | 4.5 | PASS |
| text.tertiary | #545A61 | surface.canvas | #FAFAFA | 6.680:1 | 4.5 | PASS |
| text.disabled / placeholder | #778089 | surface.raised | #FFFFFF | 4.013:1 | 3.0 (house floor; exempt inactive) | PASS (placeholder-only use) |
| accent.onSubtle | #014847 | accent.subtle | #8EFBF7 | 8.564:1 | 4.5 | PASS |
| accent.onAction | #FFFFFF | accent.action | #02807D | 4.788:1 | 4.5 | PASS |
| accent.action as link text | #02807D | surface.canvas | #FAFAFA | 4.587:1 | 4.5 | PASS |
| border.focus | #02807D | surface.canvas | #FAFAFA | 4.587:1 | 3.0 | PASS |
| border.strong | #778089 | surface.raised | #FFFFFF | 4.013:1 | 3.0 | PASS |
| status.success.ink | #1A6B34 | status.success.wash | #E7FCE9 | 6.100:1 | 4.5 | PASS |
| status.error.ink | #AF2536 | status.error.wash | #FBEEED | 5.908:1 | 4.5 | PASS |
| status.warning.ink | #A85D13 | status.warning.wash | #FDF5D8 | 4.535:1 | 4.5 | PASS |
| status.info.ink | #2E51ED | status.info.wash | #EDF4FF | 5.400:1 | 4.5 | PASS |
| DARK text.primary | #FFFFFF | surface.canvas | #0A1016 | 19.115:1 | 4.5 | PASS |
| DARK text.secondary | #E6ECF2 | surface.canvas | #0A1016 | 16.061:1 | 4.5 | PASS |
| DARK text.tertiary | #ABB5BF | surface.canvas | #0A1016 | 9.187:1 | 4.5 | PASS |
| DARK accent.onAction | #0C2A2A | accent.action | #14D8D4 | 8.551:1 | 4.5 | PASS |
| DARK status.error.ink | #FE4E5C | surface.canvas | #0A1016 | 5.879:1 | 4.5 | PASS |
| DARK status.success.ink | #31A855 | surface.canvas | #0A1016 | 6.247:1 | 4.5 | PASS |
| DARK border.strong | #7E8792 | surface.raised | #12181F | 4.904:1 | 3.0 | PASS |
| DARK border.focus | #8EFBF7 | surface.canvas | #0A1016 | 15.740:1 | 3.0 | PASS |
| log text | #E6ECF2 | surface.inset | #0D1E24 | 14.365:1 | 4.5 | PASS |

Known rejections encoded above: the app's lighter steps fail where this spec requires pass —
`#9DA7B2` (the shipped outline-button gray) computes 2.441:1 on white and is demoted to
decorative-only; `#228240` on its green wash computes 4.498:1 and is rejected for `#1A6B34`;
`#D62740` on its red wash computes 4.393:1 and is rejected for `#AF2536`; the shipped light
focus teal `#05BDBA` computes 2.335:1 and the focus role uses `#02807D` instead.

## 4. Typography

**Families.** UI: the system UI stack (SF Pro on macOS, Segoe UI on Windows, Roboto on Android),
weights 400/500/600 — no webfont is loaded inside the app shell; the marketing site is the brand
voice with Figtree (display, 400-700, self-hosted, preloaded, system-ui fallback), Instrument Sans
(text) and Martian Mono (code/id moments, ui-monospace fallback). Numeric/code: the system
monospace stack (`ui-monospace`, Menlo, Cascadia Mono, Consolas) for commit hashes, deploy IDs,
log lines, code and raw timestamps. *Monospace is for identifiers and code, never a costume.*

**One ramp table per class, not one blended table.**

- **[F] Focused, 16px base:**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Display | 40-56px | 600 | 1.1 | -0.01em | default | auth hero, marketing-crossover headers |
| Heading | 24px | 600 | 1.3 | -0.01em | default | dialog titles, plan change |
| Body | 16px | 400 | 1.5 | 0 | default | form help, confirmation copy |
| Label | 14px | 500 | 1.4 | 0 | default | field labels, buttons |
| Meta | 12-13px | 400 | 1.4 | 0 | tabular | timestamps, proration detail |

- **[S] Standard, 14px base:**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Page title | 20-24px | 600 | 1.3 | -0.01em | default | "Deploys for brave-curie-12345" |
| Section title | 16px | 600 | 1.4 | 0 | default | card headings, sidebar sections |
| Body (1.5) | 14px | 400 | 1.5 | 0 | default | descriptions, empty-state copy |
| Row primary | 14px | 500 | 1.4 | 0 | default | deploy title, table primary cell |
| Row secondary | 13px | 400 | 1.4 | 0 | default | "chore: update homepage copy" |
| Stat value | 24-32px | 600 | 1.2 | 0 | tabular | bandwidth, build minutes |
| Stat label | 11-12px | 500 | 1.3 | +0.04em, uppercase | tabular | "BANDWIDTH USED" |
| Meta | 12px | 400 | 1.4 | 0 | tabular | "Today at 5:35 PM" |

- **[D] Dense, 12-13px base, data surfaces only:**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Grid header | 12px | 500, uppercase | 1.3 | +0.04em | tabular | log-explorer column heads |
| Grid cell numeric | 12-13px | 400 | 1.4 | 0 | tabular | durations, counts, sizes |
| Grid cell text | 13px | 400 | 1.4 | 0 | default | table text cells |
| Log line | 13px mono | 400 | 24px fixed | 0 | tabular | deploy/function log lines |
| Inline help | 12px | 400 | 1.4 | 0 | default | inline hint under a field |

*Prose inside a dense screen (a legal note under a log, a billing explainer in a table drawer)
still steps up to 14px/1.5.*

**Invariants.** Tabular numerals on every comparable value — deploy durations, timestamps,
bandwidth figures, counts, IDs. Right-align numerics, left-align text, never centre a numeric
column. Fixed stepped sizes; no fluid interpolation. Measure ≤80 characters (SC 1.4.8); 65-80ch
for [F/S] prose, unconstrained in [D] logs and tables.

## 5. Spacing Scale & Density Scales   ← two axes, never one

**Spacing base: 4px grid; 8px comfortable [F/S], 4px [D].** `space.0` 0 · `1` 4px icon-to-label ·
`2` 8px control padding [D], button-label gaps · `3` 12px cell padding [S], button padding-y
small · `4` 16px card padding [S], button padding (default pill: 8px 16px), page gutter ·
`6` 24px card padding [F] + section gap · `8` 32px section gap [S] · `12` 48px region separation ·
`16` 64px rarely. *No `17px`. No `23px`. If a layout needs an off-scale value, the layout is
wrong.*

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 16-24px | 32px | auth, destructive confirms, plan change |
| `standard` | 40-44px (deploy row 64px two-line) | 14px | 12-16px | 24px | team home, site overview, site configuration, forms |
| `dense` | 24px log line / 28-32px table row | 12-13px | 8px | 16px | deploy logs, function logs, log explorer, audit |

- Density comes from **row height, column pruning and leading** — never from type too small to
  read. A 13px tabular numeral in a dense log is correct; the same numeral in a Focused form is a
  defect.
- **Never switch mid-page.** A deploy-log screen is dense end to end; a settings page is standard
  end to end. Switching across routes with different jobs is legitimate — it should feel like a
  different room.
- **Chrome follows rows.** Search bar, filter row and pagination heights match the table's row
  band (one 40-44px band above the deploy list; log toolbars 32-40px over 24px log lines).
- Whitespace budget: Focused 55-70% · Standard 40-55% · Dense 25-40%. *House heuristic, not a
  vendor figure — validated against screens/dashboard.webp and screens/docs.webp.*

## 6. Radius Scale

`none` 0 log gutters, table fills · `xs` 4px chips, micro controls, tag tokens · `sm` 6px inputs,
selects, small buttons, inline code · `md` 8px list rows, menu items · `lg` 12px dialogs,
popovers, toasts, drawers · `xl` 16px cards, panels, hero product frames · `full` pill (9999px)
**every button**, status badges, avatars, toggle tracks. One radius per component family, never
mixed ad-hoc; nested radii obey `radius_inner = radius_outer − padding` (a chip inside a 16px card
at 8px inset takes a 8px-4px = 4px radius).

## 7. Elevation

**Choose one strategy, never mix paradigms.** Light: hairline borders do the work; shadows are
whisper-quiet and reserved for elements that truly float. Dark: surface-luminance steps + 1px
keylines, zero shadows. Levels, low → high: **0** canvas (no shadow) · **1** card/panel —
`border.subtle` hairline, shadow only under genuinely floating cards · **2** sticky top bar and
expanded row bands — hairline + faint shadow while stuck · **3** overlay/popover/command palette —
`radius.lg`, stronger shadow, `border.subtle` · **4** dialog — strongest shadow + scrim (70%
`#353A3E` light / 70% black darker). Log wells are not elevation — they are `surface.inset`,
flush.

## 8. Motion

`instant` 0ms · `fast` 120ms ease-out (exits [D]) · `base` 180ms decelerate ([D] entrances,
popovers) · `slow` 240-300ms decelerate ([F/S] entrances, dialogs) · `interactive` 0.2s ease for
button/control colour transitions (the app's shipped value).

- Entrances decelerate, exits accelerate. Symmetric ease-in-out on both directions is a defect.
- Animate transform and opacity only — never width, height, top, left.
- **Loading is a stripe sweep, not a spinner swap:** buttons keep their exact width and sweep a
  repeating diagonal band (15px pitch, 30% white over the fill, 1s linear infinite) while saving;
  skeletons match final geometry for page-level loads.
- No bounce on irreversible moments: not on "Delete deploy", not on a downgrade confirm.
- The one celebration — confetti on first-success moments — is a bounded one-shot animation with
  fixed duration; it never loops and never runs on data screens.
- **Reduced motion is a real variant:** the stripe sweep freezes to a 54%-opacity fill, confetti
  and entrance transforms collapse to a ~150ms crossfade; large scaling/panning movements are
  neutralised entirely.

## 9. Imagery & Art Direction   ← the one licensed saturation moment

- **Brand moment:** the navy-to-teal gradient stage (`#060B10` → teal bloom) with the spark
  wordmark, the orange star mascot and hand-drawn product doodles — marketing hero, og image,
  empty-state illustrations at most one per surface. Its palette (`#00C7B7`, `#060B10`,
  mascot orange `#FAB23D`) **never leaks into app UI tokens**; inside the app the mascot is the
  only figure allowed full saturation, and only in success/easter-egg corners.
- **Iconography:** geometric outline set, ~1.5px strokes on a 16/20px grid, rounded joins matched
  to the pill-button geometry; filled variants only for status glyphs (check, triangle, octagon)
  and the active nav marker. Icon-only controls always carry a tooltip label (§10).
- **Photography:** none in product. Third-party logos (GitHub, provider logos) render in
  monochrome inside committed surfaces, never in their brand colour, except the deploy-provider
  mark beside a deploy origin where it is content, not decoration.
- **Illustration / 3D:** flat doodle-style line illustration (white-on-navy in marketing, ink-on-
  white in app empty states). No 3D, no gradients inside data surfaces. Performance budget for
  any animated illustration belongs in the adapter; the spec records the visual policy only.
- **Empty / error art:** an empty deploys list shows the doodle + "what's missing" + the exact CTA
  (connect a repo, trigger a deploy). A failed deploy shows the red wash banner + "Why did it
  fail?" recovery affordance — art never substitutes for the recovery CTA.

## 10. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell / sidebar | S | team scope, site scope | default, hover, active (teal ink + marker), collapsed | Tab order top-bar → nav → content; active item announced | "Deploys", "Site configuration", "Forms" |
| Data table (deploys) | S/D | deploy list, members, domains | loading, empty, error, row hover/selected, locked | arrow keys between rows; Enter opens | "Search by branch name or deploy ID" |
| Filter/search bar | S | text search, status select, time frame | idle, focused, filtered, cleared | / focuses search; Esc clears | "Filter: Any status / Any time frame" |
| Row action menu | S/D | split-button caret, kebab | open, focus-trap, Esc closes, destructive items confirmed | arrow keys, Esc | "Trigger deploy", "Retry", "Lock to stop auto publishing" |
| Stat tile | S | bandwidth, build minutes, sites | loading, delta up/down, quota near-limit | tabbable, value + label read together | "Bandwidth used" + sign-glyph deltas |
| Deploy log well | D | deploy log, function log | streaming, complete, failed, selected-lines, maximized | scroll, arrow lines, copy shortcut | "Deploy log" + "Maximize log" |
| Drawer/inspector | S | deploy preview drawer, AI diagnosis | open, pinned, closed, busy | Esc closes; focus returns to trigger | "Why did it fail?" |
| Dialog | F | destructive confirm, form modal | open, confirming, blocked, error | focus-trap, Esc cancels, Enter confirms labelled action | "Delete deploy? This cannot be undone." |
| Plan/seat control | F | plan card, seat add/remove | current, upgrading, prorating, blocked, confirm | full form flow | names cost + effective date: "$20/month with unlimited members" |
| Member row | S | invite pending, active, role select | role change confirm, remove confirm, disabled | row menu via keyboard | "Invite members" |
| Audit entry | D | timestamped event list | loading, filtered, empty | arrow-key navigation | actor + action + target + time |
| Command palette | S | global search/actions | open, no results, recent | Cmd/Ctrl+K, arrows, Enter | "Search sites, teams and actions" |
| Status badge | S/D | Complete, Failed, Building, Enqueued | static only (link inside row) | not focusable (row is) | word + glyph, never colour alone |
| Token/tag input | S | branches, domains, emails | idle, focused (teal ring), chip remove, overflow | Backspace removes last chip | "Let me add individual branches" |

**Every fetching surface also designs:** loading (skeleton matching final row geometry — never a
centred spinner on a blank page), empty (what's missing + the CTA that fixes it), error (what
happened + how to recover: "Deploy failed" + Retry + Why did it fail?), offline/stale (cached list
with a stale banner stating data age).

**Contracts this table encodes:** one primary filled CTA per view [F/S] (dense log toolbars may
run a primary plus icon actions); every icon-only control carries a label or tooltip; a disabled
control states *why* on focus or hover ("Lock to stop auto publishing" explains the lock); a
button never changes width between idle and loading — the stripe sweep reserves the space.

## 11. Light / Dark Strategy

- **Posture: C dual-parity.** The app ships light-first (the default for every route) and an
  authored dark theme; marketing is dark-only. Reason: the app is read all day in offices; the
  brand stage is dark but the working canvas is not.
- **Mechanism:** semantic roles remapped per mode from one primitive pool; **no role absent in
  either mode.** No single-mode roles exist; the log well and code block keep dark values in light
  mode by design (machine territory), and their role values are identical in both modes.
- **`color-scheme`** set on the root so UA chrome, form controls and scrollbars follow the mode.
- **`<meta name="color-scheme">` in the head before the stylesheet**, to prevent a flash of the
  wrong scheme.
- **Dark is authored, not inverted:** blue-black canvas `#0A1016` (studio `#030F14`), its own
  surface ramp (`#12181F` → `#1E242C`), stronger hairlines (`#272F38`) because a 1px line that
  reads as delicate on white is invisible on near-black, hover fills rebuilt as 4% white instead
  of 3% ink, and teal lifted two steps (`#14D8D4`) so the action colour keeps its brightness.
  The dark danger ink lightens to `#FE4E5C`; the light one stays `#AF2536`.
- A second brand binding (studio theme) re-points a subset of primitives to the newer Hues scale
  (teal toward `#09A995`/`#10DDC4`, warm-gray neutrals) and sets the focus ring to exactly 2px.
  It changes colour bindings only; radii, type sizes and layout are frozen so a theme swap cannot
  move anything.

## 12. Density-Mode Strategy

- **Default mode per surface class:** team/site overview, configuration and forms are `standard`
  (the boundary: a screen whose primary job is reading rows and editing fields); deploy logs,
  function logs, log explorer and audit are `dense` (the job is scanning machine output); auth,
  destructive confirms and plan change are `focused` (the job is one decision).
- **Mechanism:** a density marker at the app root rescales row height, cell padding, gutter and
  body size together as a token axis — never a media query; the spacing scale itself does not
  change values per screen size.
- **Container queries for reflow:** components reflow to their container, not the viewport; size
  queries fail closed with no eligible container, so `cq*` units are never used where that
  fallback would be wrong (log wells sized by their panel, not the window).
- **Style queries** compare computed values, so the density marker is registered as a typed
  custom property before any style query consumes it.
- **Offer the switch as an accessibility affordance**, not a preference: the log-explorer density
  toggle exists for users with visual field loss per W3C's note on SC 2.5.8.

## 13. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA (7:1) for body prose in help centres and billing copy.
- **Target size:** ≥24×24 CSS px hard minimum (the micro button is exactly 24px); 44px design
  target for primary controls [F]; spacing exception honoured — a 24px circle centred on each
  target never intersects a neighbour's. *Zoom does not excuse it.*
- **Keyboard:** every function operable; focus indicator = 2px `border.focus` ring with 2px
  offset, never suppressed without a stronger replacement; the focused row is never entirely
  hidden behind the sticky top bar (scroll-margin on anchors).
- **Contrast:** text ≥4.5:1 (computed gate, §3); UI boundaries and focus indicators ≥3:1;
  **colour independence:** every status pairs colour with a glyph and a word (Complete +
  check + green; Failed + octagon + red); deltas carry a sign or direction glyph.
- **Motion:** the reduced-motion variant from §8 per component — stripe sweep freezes, confetti
  collapses to crossfade, entrance transforms neutralised.
- **Text:** ≤80-character measure, 1.5 leading on prose, 200% resize without horizontal scroll;
  log lines are exempt from measure but keep 24px fixed leading.
- **Semantics:** real buttons/links/inputs; nav landmarks for the sidebar; headings matching
  visual rank; `aria-live="polite"` on deploy-status changes ("Deploy failed for Acme Website");
  `aria-busy` on a streaming log region; log wells exposed as scrollable regions with named roles.
- **Contrast preference:** `prefers-contrast: more` promotes `border.subtle` to `border.strong`
  values and raises hairline strength in dark; token changes: `no-preference` / `more` honoured.

## 14. Anti-Patterns

**Do** —
1. Keep the deploy row's two-line anatomy everywhere: title line, mono `branch@sha` line,
   right-aligned tabular time — the list is the product.
2. Pair every status with glyph + word + colour; the Complete pill is a wash, not a filled bar.
3. Use the stripe sweep (space reserved, width frozen) for every saving state.
4. Reserve mono for identifiers: hashes, IDs, log lines, code — labels never.
5. Use the dark log well inside the light shell to mark machine output; never mix prose into it.
6. Keep exactly one filled primary per view; the standard primary (light-teal fill, dark label)
   is the default and the action primary (teal fill, white label) is for the single job of the
   screen ("Preview", "Trigger deploy").
7. Match chrome heights to the row band they front (40-44px standard, 32-40px over logs).
8. Ground empty states: name the missing thing and ship the exact CTA that fixes it.
9. Give destructive actions a focused confirm that restates the resource ("Delete deploy
   brave-curie-12345?").
10. Let the mascot and confetti live only in success corners; a failure screen is dry.
11. Compute the gate table on every token change; 4.499:1 fails and ships back.
12. Freeze geometry across themes — the studio colour re-binding may not move a single px.

**Don't** —
1. No marketing aesthetics inside the product: no navy gradient stages, no mascot in data tables.
2. No `#00C7B7` in app tokens — it is the marketing teal; the app speaks `#02807D`/`#14D8D4`.
3. No filled square buttons — buttons are pills; a rectangular button reads as foreign.
4. No two primaries side by side; the split button's caret is a menu, not a second action.
5. No card inflation: one hairline card per logical group; the summary block is one card.
6. No modals as connective tissue; settings live on settings pages, confirms live in dialogs.
7. No toolbar of unlabelled icons; every icon control has a label or tooltip.
8. No hover-only affordances; row actions are reachable by keyboard and visible on focus.
9. No placeholder-as-label; "Search by branch name or deploy ID" is a hint beside a real label.
10. No whole-page spinners; skeletons match final geometry.
11. No tiny type as a density strategy; dense means 12-13px floor with tabular numerals, not 10px.
12. No disabled primary sitting silently dead — state the blocker on focus ("Auto publishing is
    on. Deploys from main are published automatically.").
13. No shadows for depth in dark mode; luminance steps and 1px strokes only.
14. No `alert()`/`confirm()`; failures render in the failure surface with a recovery path.

## 15. Quick Reference & Verification Gate

**Colour (role → hex).** Light: canvas `#FAFAFA` · raised `#FFFFFF` · inset `#0D1E24` · hover
`#F7F8F8` · selected `#EFF1F1` · border subtle `#E9EBED` / strong `#778089` / focus `#02807D` ·
action `#02807D` · onAction `#FFFFFF` · subtle `#8EFBF7` · onSubtle `#014847` · bright `#32E6E2` ·
text `#181A1C` / `#353A3E` / `#545A61` / disabled `#778089` · success `#1A6B34` on `#E7FCE9` ·
warning `#A85D13` on `#FDF5D8` · error `#AF2536` on `#FBEEED` · info `#2E51ED` on `#EDF4FF` ·
danger fill `#D62740`. Dark: canvas `#0A1016` · raised `#12181F` · overlay `#1E242C` · hover 4%
white · selected 10% white · border subtle `#272F38` / strong `#7E8792` / focus `#8EFBF7` ·
action `#14D8D4` · onAction `#0C2A2A` · text `#FFFFFF` / `#E6ECF2` / `#ABB5BF` / disabled
`#4D565F` · success `#31A855` · warning `#F98E21` · error `#FE4E5C` · info `#5D8DF5` · danger fill
`#800A20`.

**Type ramp.** App: system UI stack; base 14px [S] / 12-13px [D] / 16px [F]; weights 400/500/600;
mono system stack for identifiers; log line 13px/24px mono. Marketing: Figtree display /
Instrument Sans text / Martian Mono code.

**Spacing + radius.** 4px grid; steps 0/4/8/12/16/24/32/48/64; gutters 32 [F] / 24 [S] / 16 [D];
radii 4/6/8/12/16/pill (every button a pill).

**Component → token map.** Primary button (standard): `accent.subtle` + `accent.onSubtle`, hover
`accent.bright`, radius pill, min-height 36/28/24, saving = stripe sweep. Action button:
`accent.action` + `accent.onAction`. Danger button: `fill.danger` + `text.inverse`. Input:
`surface.raised` + `border.strong` + focus ring `border.focus` + `text.disabled` placeholder.
Sidebar item: `text.secondary`, hover `surface.hover`, active `accent.action` ink + marker.
Deploy row: `surface.raised`, title `text.primary`, hash/log line `text.tertiary` mono, time
tabular `text.tertiary`. Log well: `surface.inset` + `text.inverse` mono + `status.info.ink`
numerals + selection wash `#0D554F`. Badge: `status.*.wash` + `status.*.ink` + glyph. Card:
`surface.raised` + `border.subtle` + radius 16. Dialog: `surface.raised` + radius 12 + scrim 70%
`#353A3E`.

**Agent prompt block.**
Build any Netlify app surface with these roles only — never raw hex:
1. Colours: canvas #FAFAFA / #0A1016; raised #FFFFFF / #12181F; text #181A1C / #FFFFFF, secondary
   #353A3E / #E6ECF2, tertiary #545A61 / #ABB5BF; action teal #02807D / #14D8D4; onAction
   #FFFFFF / #0C2A2A; subtle fill #8EFBF7 / #0F5149 with label #014847 / #8EFBF7; borders
   #E9EBED-#778089 / #272F38-#7E8792; focus ring #02807D / #8EFBF7 at 2px + 2px offset; success
   #1A6B34-on-#E7FCE9 / #31A855; warning #A85D13-on-#FDF5D8 / #F98E21; error #AF2536-on-#FBEEED /
   #FE4E5C; info #2E51ED-on-#EDF4FF / #5D8DF5; log well #0D1E24 with #E6ECF2 mono; danger fill
   #D62740 / #800A20.
2. Type: system UI stack, weights 400/500/600 only; base 14px standard, 16px focused, 12-13px
   dense; headings 20-24px/600 sentence case; tabular numerals on every comparable value; mono
   stack for hashes, IDs and log lines (13px/24px).
3. Spacing: 4px grid — 4, 8, 12, 16, 24, 32, 48, 64; gutters 32/24/16 by density; standard rows
   40-44px (deploy row 64px two-line), log lines 24px; chrome heights match rows.
4. Shape: inputs 6px, rows 8px, dialogs 12px, cards 16px, buttons/badges/avatars full pill.
5. Motion: 0.2s ease control transitions; 180ms decelerate entrances; saving = 1s diagonal stripe
   sweep at fixed width; reduced motion freezes the sweep to 54% opacity and crossfades ≤150ms.

**Example component prompts.**
1. *Deploys list (primary surface)* — `surface.canvas` page, one `surface.raised` summary card
   (radius 16, `border.subtle`, `space.4` padding), title role in `text.primary`, site URL as
   `accent.action` link; one `accent.action` split button "Trigger deploy"; search + filters in a
   single 44px band; rows 64px two-line with `text.primary` title, `text.tertiary` mono hash,
   right-aligned tabular "Today at 5:35 PM / Deployed in 2m 29s"; hover `surface.hover`; focus
   ring `border.focus`; no shadow above level 1.
2. *Deploy log (data row, dense)* — `surface.inset` background, 24px mono lines, line numbers in
   `status.info.ink` right-aligned, selection wash `#0D554F`, toolbar 40px with "Preview" as
   `accent.action` fill + `accent.onAction` label, icon actions labelled by tooltip; streaming
   state sets `aria-busy`, complete state renders the word with the check glyph.
3. *Status badge* — pill, `status.*.wash` fill, `status.*.ink` 12px/500 word + glyph; never
   colour alone; inside rows it is not independently focusable.

**Pre-ship checklist.**
1. Zero raw hex outside L1. 2. No token resolves to a component name. 3. Every contrast pairing
computed, passing, unrounded. 4. Every semantic role has a value in every shipped mode (light,
dark, studio binding). 5. Every fetching surface has loading/empty/error/offline specified.
6. Every component row lists disabled and loading states. 7. Row, header, toolbar and pagination
heights agree. 8. Reduced-motion variant written for every authored motion. 9. Every control
keyboard-reachable with a visible focus indicator. 10. Dark authored, not filtered, with border
strength exceeding light's. 11. No unoverridden stock library default inside a committed surface.
12. Nothing came from a marketing page. 13. The §9 brand-moment palette (#00C7B7, #060B10,
mascot orange) appears nowhere in the UI token layers.
