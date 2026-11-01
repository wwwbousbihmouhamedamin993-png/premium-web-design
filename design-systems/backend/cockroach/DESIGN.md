# Design System — CockroachDB

<!-- premium-web-design:design-system 1 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: CockroachDB Cloud console via the published Cockroach Labs design-token package v1.15.0 (density/type ground truth), cockroachlabs.com Continuum-era shell (colour + voice). Ladder: rung 2 (official tokens: npm token package, live marketing-site CSS variables, open-source console wiring) with rung 3 screenshot triangulation for geometry and accent scarcity. Rung 1 (sibling libraries) holds no CockroachDB entry. -->
<!-- Surface classes: 15 routes classified; density classes [F/S/D] assigned -->

## 1. Design Posture & Atmosphere

CockroachDB is a distributed SQL database whose product surfaces exist to make an invisible,
multi-region system legible: clusters, nodes, replicas, statements, sessions, metrics. The console
therefore reads as a **flight instrument for data infrastructure** — a white, quietly engineered
canvas where a single purple action, blue links, and a disciplined status vocabulary carry all the
colour the eye needs. After eight hours of latency hunting, nothing shouts: the loudest object on a
statements page is the data itself, rendered in tabular numerals and mono SQL text. The 2026
"Continuum" brand world that wraps the product is the opposite register — a digital-black stage
with bio-green highlights, electric-purple calls to action, and mono-uppercase eyebrows — and the
two registers are kept strictly apart: the dark stage sells, the white instrument operates.

The category default for database consoles is a grey-blue admin panel with generous chrome and
 timid typography. CockroachDB's console breaks from it in three ways: a **purple primary action**
(where peers use blue fills), a **blue link-and-info intent** that doubles as the focus colour, and
a metrics chart palette engineered as first-class tokens. Density is honest: SQL activity pages are
true data surfaces with sortable columns, inline distribution bars, and mono statement text, while
organization settings relax to a standard register with real whitespace.

The single visual metaphor: **a ledger sheet bolted into an instrument panel**. Tables are the
house of the product; charts, filters and time-range controls are the dials around them; the
marketing site is the hangar wall outside, painted black with lime signal paint.

**Key Characteristics** —
- Two shipped shells, one system: product console is light-only (canvas #ffffff); the Continuum
  marketing shell is dark-only (canvas #000000 with deep-green #101913 cards). A token role never
  crosses shells.
- Primary action is a purple fill #6933ff with white text (5.97:1) — exactly one filled primary
  control per view; secondary actions are outlined or text-only.
- Links, focus rings and the info intent share one blue #0055ff (5.61:1 on white); hover deepens to
  #0037a5 (10.05:1).
- Status vocabulary is four intents with a wash-plus-dark-text recipe: success #237300 on #e3f5e0,
  warning #b26000 on #fff4e1 (body-size text darkens to #644004, 8.47:1), danger #cd2939 on
  #ffe9eb, info #0037a5 on #e1ecff. Every status also ships a glyph — never colour alone.
- Neutrals are a 10-step cool-grey ramp #ffffff → #060c12 (never pure black text; primary ink is
  #242a35 at 14.41:1).
- Interface type is Source Sans Pro at 400/500/600/700; identifiers, SQL, hashes and timestamps are
  Roboto Mono. Marketing swaps to Geist and Geist Mono at the same discipline: mono for eyebrows,
  prices, and any figure a user might compare.
- Data tables run 14px body text, tabular numerals, right-aligned numeric columns; rows 44px
  standard, 32px in dense metric grids.
- Controls are 40px tall with a 2px base radius — crisp, machine-like, no pill shapes inside the
  product shell; pills (9999px) exist only in the marketing shell.
- Charts draw from a dedicated nine-hue metrics palette (#003ebd, #2aaf44, #00a2ff, #c813fe,
  #c9cc01, #26dcab, #050f6d, #e38c09, #d93946) with light washes for area fills; chart colour is
  series identity, not decoration.
- Accent scarcity: one purple fill, one status colour block, one focus ring per viewport. The
  marketing shell allows exactly one lime highlight phrase per headline and one purple pill per
  section.
- Depth in the console is a 1px hairline system (#e7ecf3) plus one faint ambient shadow on floating
  cards; the dark shell uses surface steps (#000000 → #101913 → #323232 strokes) and zero shadows.
- Motion is restrained: 120ms exits, 180–200ms entrances, decelerate curves, no bounce anywhere.
- Destructive actions are red #ff3b4e fills with white text reserved for terminal confirms; the
  readable destructive voice is #cd2939 text on #ffe9eb washes.

## 2. Token Architecture   ← normative

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value* (`neutral.5`, `purple.600`, `size.14`), referenced
  only by L2. Banned: component-prop naming (`card-bg`, `tooltip-colour`) — one value, many roles.
- **L2 Semantic** — role names (`surface.canvas`, `text.primary`, `accent.action`). The only layer a
  component may consume.
- **L3 Component** — only for deliberate deviation; points at L2 or L1, never a raw value, never a
  sibling component's token.

**Rules.** Every token has a determinable type or it is invalid; names are case-sensitive with no
`$`, `{`, `}`, `.` inside a single name segment; no circular references (`a → b → a` is an error).
Every semantic token has a value in **every** shipped mode of its shell — a role with no value
resolves to nothing and fails contrast. Animatable tokens declare both a syntax type and an
inheritance flag, and their initial values must be computationally independent, so percentage or
font-relative units are illegal in them.

**Layer order (low → high)** `reset → primitives → semantic → components → utilities`. Layer order
beats specificity entirely, and an un-layered normal declaration outranks every layered one, so a
stray un-layered rule in a component file would silently beat this whole system; anything a
consumer must override without priority hacks sits in the top layer.

**L1 Primitive roster (product shell).**
- `neutral.0` #ffffff · `neutral.1` #f5f7fa · `neutral.2` #e7ecf3 · `neutral.3` #d6dbe7 ·
  `neutral.4` #c0c6d9 · `neutral.5` #7e89a9 · `neutral.6` #475872 · `neutral.7` #394455 ·
  `neutral.8` #242a35 · `neutral.9` #060c12
- `purple.1` #e6ddff · `purple.2` #cbbcfc · `purple.5` #6933ff · `purple.6` #501fe5 ·
  `purple.7` #300d8f · `purple.9` #190f33
- `blue.1` #e1ecff · `blue.2` #89b0ff · `blue.5` #0055ff · `blue.6` #0037a5 · `blue.7` #0c1628
- `green.1` #e3f5e0 · `green.2` #a5dd8d · `green.5` #37a806 · `green.6` #237300 · `green.7` #123d00
- `orange.1` #fff4e1 · `orange.2` #ffd099 · `orange.5` #ffa53b · `orange.6` #b26000 ·
  `orange.7` #644004
- `red.1` #ffe9eb · `red.2` #f8bfc6 · `red.5` #ff3b4e · `red.6` #cd2939 · `red.7` #99000f
- `chart.1…9` #003ebd #2aaf44 #00a2ff #c813fe #c9cc01 #26dcab #050f6d #e38c09 #d93946; washes
  `chart.wash.1…9` #eaf1ff #e0fbe5 #e7f6ff #f7edff #f8f9e1 #d5faf0 #edefff #fff0da #ffe4e7
- `size.12/14/16/20/24/28` px type sizes; `lh.16/20/24/32/48/64` px line heights; weights 400/500/600/700

**L1 Primitive roster (marketing shell).**
- `ink.0` #000000 · `ink.950` #101913 · `ink.800` #323232 · `ink.500` #4a4a46 · `ink.400` #888884
- `lime.1` #d7eea9 · `lime.3` #aede54 · `lime.7` #43541f
- `violet.1` #c8acff · `violet.4` #9059ff · `violet.7` #502482 · `violet.9` #190f33
- `cyan.1` #dffbff · `cyan.3` #60ecff · `cyan.7` #144f6b
- `bone.1` #f9f8f3 · `bone.3` #e5e4dc · `bone.5` #f2f2ee

**L2 Semantic (product shell, light mode — the only shipped product mode).** See §3 table.
**L2 Semantic (marketing shell, dark mode — the only shipped marketing mode).** See §3 table.

**L3 Component examples.** The primary button resolves `background: accent.action` (never
`purple.5` directly) so a brand shift moves one semantic token. The statements table resolves row
text through `text.primary`/`text.secondary` and SQL literals through `code.text`; its inline
latency bars resolve `chart.1` and `chart.wash.1`. A component token never points at another
component's token.

## 3. Colour Roles

Product shell (light, the shipped mode):

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` / `raised` / `overlay` / `inset` | #ffffff / #ffffff / #ffffff / #f5f7fa | not shipped (light-only shell) | canvas · cards · dialogs · wells; canvas and raised are both white, separated by hairlines |
| `surface.hover` / `surface.selected` | #f5f7fa / #e1ecff | not shipped | row hover fill · selected-row info wash |
| `border.subtle` / `strong` / `focus` | #e7ecf3 / #7e89a9 / #0055ff | not shipped | 1px hairlines; `border.strong` for non-text boundaries; focus ≥3:1 |
| `accent.action` / `onAction` / `subtle` | #6933ff / #ffffff / #e6ddff | not shipped | Accent budget: 1 filled control per viewport; hover #501fe5; disabled fill #cbbcfc |
| `link.action` / `link.hover` | #0055ff / #0037a5 | not shipped | also the info intent; 5.61:1 on canvas |
| `text.primary` / `secondary` / `tertiary` / `disabled` | #242a35 / #394455 / #475872 / #7e89a9 | not shipped | ink ramp; disabled is exempt text, ≥3:1 house floor |
| `status.success` / `warning` / `error` / `info` | #37a806 / #ffa53b / #ff3b4e / #0055ff | not shipped | base hues; each ships a glyph — never colour alone |
| `status-text.success` / `warning` / `error` / `info` | #237300 / #b26000 / #cd2939 / #0037a5 | not shipped | readable text on matching washes |
| `status-wash.success` / `warning` / `error` / `info` | #e3f5e0 / #fff4e1 / #ffe9eb / #e1ecff | not shipped | badge and inline-alert fills |
| `code.text` / `code.wash` | #394455 / #f5f7fa | not shipped | SQL, identifiers, hashes; mono only |

Dark shell (marketing — shipped dark-only). Product roles do not resolve here and vice versa:

| Role | Light | Dark | Notes |
|---|---|---|---|
| `mkt.canvas` / `mkt.raised` / `mkt.card` | none (dark-only shell) | #000000 / #0a0a0a / #101913 | hero stage · nested strips · plan and feature cards |
| `mkt.text.primary` / `secondary` | none | #ffffff / #888884 | 21:1 and 5.90:1 on #000000 |
| `mkt.accent.action` / `mkt.onAction` | none | #9059ff / #ffffff | pill CTA; see gate note 4.15:1 |
| `mkt.highlight` | none | #aede54 | one lime phrase per headline; 13.38:1 on black |
| `mkt.data.accent` / `mkt.link` | none | #60ecff / #aede54 | mono data figures and inline links on dark |
| `mkt.stroke` | none | #323232 | 1px dividers between dark sections |
| `mkt.card-text` | none | #f2f2ee | body on #101913 cards, 15.99:1 |

The dark canvas is **not** pure-black text on white inverted: the marketing canvas is true #000000
but text ink #ffffff and the card layer #101913 (a green-tinted near-black) carry depth; the
product shell never uses black ink, stopping at #242a35. Depth in the dark shell comes from surface
steps and 1px #323232 strokes, never shadows.

**Contrast gate — computed, unrounded. 4.499:1 fails. Large text is ≥24px or ≥18.5px bold. Body
≥4.5:1; UI boundaries and focus indicators ≥3:1.**

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| text.primary | #242a35 | surface.canvas | #ffffff | 14.41:1 | 4.5 | PASS |
| text.secondary | #394455 | surface.canvas | #ffffff | 9.85:1 | 4.5 | PASS |
| text.tertiary | #475872 | surface.canvas | #ffffff | 7.22:1 | 4.5 | PASS |
| text.disabled | #7e89a9 | surface.canvas | #ffffff | 3.48:1 | 3.0 muted floor | PASS (exempt text only; never body) |
| accent.onAction | #ffffff | accent.action | #6933ff | 5.97:1 | 4.5 | PASS |
| border.strong | #7e89a9 | surface.raised | #ffffff | 3.48:1 | 3.0 | PASS |
| link.action | #0055ff | surface.canvas | #ffffff | 5.61:1 | 4.5 | PASS |
| status-text.success | #237300 | status-wash.success | #e3f5e0 | 5.22:1 | 4.5 | PASS |
| status-text.warning | #b26000 | status-wash.warning | #fff4e1 | 4.22:1 | 4.5 | FAIL below 4.5 — badges/glyph context only; body-size warning text must use #644004 (8.47:1 on the same wash) |
| status-text.error | #cd2939 | status-wash.error | #ffe9eb | 4.56:1 | 4.5 | PASS |
| status-text.info | #0037a5 | status-wash.info | #e1ecff | 8.44:1 | 4.5 | PASS |
| white on error fill | #ffffff | #ff3b4e | — | 3.51:1 | 4.5 | FAIL for body text — destructive fill reserved for large/bold labels and non-text emphasis; readable destructive voice is #cd2939 on wash |
| white on success fill | #ffffff | #37a806 | — | 3.10:1 | 4.5 | FAIL for body text — success uses wash + #237300 text instead of filled buttons |
| mkt.text.primary | #ffffff | mkt.canvas | #000000 | 21.00:1 | 4.5 | PASS |
| mkt.highlight | #aede54 | mkt.canvas | #000000 | 13.38:1 | 4.5 | PASS |
| mkt.accent.action | #ffffff | #9059ff | — | 4.15:1 | 4.5 | FAIL below 4.5 — marketing pill labels are ≥14px mono medium; AA-compliant swap is #000000 on #9059ff (5.06:1) or the product pairing #ffffff on #6933ff (5.97:1) |
| mkt.text.secondary | #888884 | mkt.canvas | #000000 | 5.90:1 | 4.5 | PASS |
| mkt.card-text | #f2f2ee | mkt.card | #101913 | 15.99:1 | 4.5 | PASS |
| mkt.data.accent | #60ecff | mkt.canvas | #000000 | 14.94:1 | 4.5 | PASS |

## 4. Typography

**Families.** UI: **Source Sans Pro**, weights 400/500/600/700, self-hosted, fallback sans-serif —
the console interface face. Numeric/code: **Roboto Mono** for SQL text, identifiers, hashes, raw
timestamps, node IDs. Marketing shell: **Geist** (400/500) with **Geist Mono** for eyebrows,
prices, and data figures; docs shell renders **Inter** with a mono companion for code. *Monospace
is for identifiers and code, never a costume* — marketing may set eyebrows in mono as a brand
voice, but prose never goes mono.

**One ramp table per class, not one blended table.**

- **[F] Focused — marketing shell, 16px base:**
  | Role | Size | Weight | Line height | Tracking | Numerals | Use |
  |---|---|---|---|---|---|---|
  | Hero headline | 64–72px | 400 | 1.05 | −1% | — | homepage/section hero, white with one lime phrase |
  | Section headline | 40px | 400 | 1.15 | −0.5% | — | feature sections |
  | Eyebrow | 13px | 500 | 1.4 | +8%, uppercase | mono | Geist Mono label above headlines |
  | Body | 16px | 400 | 1.6 | 0 | — | paragraphs on dark canvas |
  | Data figure | 28–48px | 400 | 1.2 | 0 | mono, tabular | prices, multipliers (Geist Mono) |
  | Button label | 14px | 500 | 1.2 | 0, mono | — | pill CTAs (Geist Mono) |
- **[S] Standard — console default, 14px base:**
  | Role | Size | Weight | Line height | Tracking | Numerals | Use |
  |---|---|---|---|---|---|---|
  | Page title | 24px | 600 | 1.2 | −0.25% | — | "Statements", "Sessions", "Metrics" |
  | Section title | 20px | 600 | 1.3 | 0 | — | panel headings |
  | Card title | 16px | 600 | 1.5 | 0 | — | chart/card headings |
  | Body | 14px | 400 | 1.7 | 0 | — | descriptions, empty states |
  | Row primary | 14px | 400/500 | 1.5 | 0 | tabular | table cell text |
  | Row secondary | 12px | 400 | 1.5 | 0 | tabular | muted cell detail |
  | Stat value | 24px | 600 | 1.2 | 0 | tabular-nums | capability/usage tiles |
  | Stat label | 12px | 500 | 1.4 | +4%, uppercase | — | labels under stat values |
  | Meta | 12px | 400 | 1.5 | 0 | tabular | timestamps, counts, "Last cleared …" |
- **[D] Dense — console data surfaces only, 12–13px base:**
  | Role | Size | Weight | Line height | Tracking | Numerals | Use |
  |---|---|---|---|---|---|---|
  | Grid header | 12px | 500 | 1.4 | +4%, uppercase | — | STATEMENT, LATENCY, ROWS AFFECTED |
  | Grid cell numeric | 13px | 400 | 1.4 | 0 | tabular-nums | counts, durations, percentages |
  | Grid cell text | 13px | 400 | 1.4 | 0 | — | names, regions |
  | SQL line (mono) | 12px | 400 | 1.5 | 0 | tabular | Roboto Mono statement text |
  | Inline help | 12px | 400 | 1.5 | 0 | — | hint text under filters |

  *Prose inside a dense screen still steps up to 14px/1.7.*

**Invariants.** `tabular-nums` on every comparable value — latencies, execution counts, rows
affected, bytes, vCPU-hour prices, timestamps, node IDs. Right-align numerics, left-align text,
never centre a numeric column. Fixed stepped sizes (12/14/16/20/24/28); no fluid interpolation.
Measure ≤80 characters: 65–80ch [F/S] prose; unconstrained [D] tables. Docs prose holds 72ch.

## 5. Spacing Scale & Density Scales   ← two axes, never one

**Spacing base: 4px grid; 8px comfortable [F/S], 4px [D].** `space.0` 0 · `1` 4px icon-to-label ·
`2` 8px control padding [D] · `3` 12px cell padding [S] · `4` 16px card padding [S] / page gutter ·
`6` 24px card padding [F] + section gap · `8` 32px section gap [S] · `12` 48px region separation ·
`16` 64px marketing hero padding. *No 17px. No 23px. If a layout needs an off-scale value, the
layout is wrong.*

**Density mode — the rescaling axis.**
| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` [F] | — | 16px | 24px | 32–64px | marketing home, product, pricing, auth |
| `standard` [S] | 44px | 14px | 12px | 24px | cluster overview, databases, org settings, docs pages |
| `dense` [D] | 32px | 12–13px | 8px | 16px | SQL statements, sessions, insights, metrics grids, jobs |

- Density comes from **row height, column pruning and leading** — never from type too small to
  read. A 13px tabular numeral in a statements table is correct; the same numeral in an
  organization-settings form is a defect.
- **Never switch mid-page.** A statements page is dense top to bottom — filters, table and
  pagination all speak 32px; the settings page is standard throughout. Switching across routes with
  different jobs is legitimate and should feel like a different room.
- **Chrome follows rows.** The search/filter bar, app-name selector and pagination on a data page
  match the table's row height (44px standard bands, 40px controls nested in them, 32px dense). A
  44px toolbar over 32px rows is a rhythm break.
- Whitespace budget: [F] 55–70% · [S] 40–55% · [D] 25–40%. Validated against screenshots: the
  statements page sits near 30%, org settings near 50%.

## 6. Radius Scale

`none` 0 · `xs` 2px console buttons, inputs, checkboxes (the kit's base control radius) ·
`sm` 4px badges, tags, dense cells, inline code · `md` 8px console cards, table containers,
dialogs · `lg` 16px docs callouts, marketing wide panels · `xl` 24px marketing plan cards, hero
data cards · `full` 9999px marketing pill buttons and avatars. **One radius per component family**,
never mixed ad-hoc: console controls are uniformly 2px so precision reads; marketing surfaces go
soft so the black stage feels designed. Nested radii obey `radius_inner = radius_outer − padding`
(a 24px plan card holding a 9999px pill uses the pill directly; an 8px card holding an input uses
4–6px).

## 7. Elevation

**One strategy per shell, never mixed paradigms.**
- Product shell (light): **hairline-first**. Level **0** canvas #ffffff, no shadow. Level **1**
  card/panel: white surface + 1px #e7ecf3 stroke; floating cards add one faint ambient shadow
  (offset 0, blur 2, ink #060c12 at 6%). Level **2** sticky header/toolbar: white + stronger
  hairline #d6dbe7 + shadow (0, 2, 8, 8%). Level **3** overlay (dropdowns, drawers): shadow
  (0, 4, 16, 12%) + #d6dbe7 stroke. Level **4** dialog: shadow (0, 8, 32, 16%) over a scrim of
  #475872 at 80% opacity.
- Marketing shell (dark): **zero shadows** — a drop shadow is invisible on #000000. Depth is the
  surface ladder #000000 → #0a0a0a → #101913 plus 1px #323232 keylines; the plan cards and data
  cards float purely by their lighter step.
- Levels never skip: a dropdown sits at level 3, never "a bit more shadow" of level 1.

## 8. Motion

`instant` 0ms · `fast` 120ms ease-out (exits [D]) · `base` 180ms decelerate ([D] entrances, dropdowns)
· `slow` 240–300ms decelerate ([F/S] entrances, dialogs, drawers).

- Entrances decelerate, exits accelerate. Symmetric ease-in-out on both directions is a defect.
- Animate transform and opacity only — never width, height, top, left. Table sort and filter
  changes are instant value swaps with at most a 120ms row fade.
- No bounce on irreversible moments: not on "Delete organization", not on cluster teardown, not on
  plan downgrades.
- The marketing shell's ambient marquees and gradient drifts are decoration with a reduced-motion
  contract: under reduced motion they freeze to their rest frame rather than crossfading.
- **Reduced motion is a real variant**, not an off switch everywhere: movement collapses to
  crossfade under ~150ms; large scaling and panning motions are the vestibular triggers to
  neutralise, not every fade.

## 9. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell / console nav | S | org-nav rail, cluster switcher | hover, active cluster, collapsed | Tab order, arrow keys in switcher | "Clusters", "Access", "Billing" |
| Data table (statements/sessions) | D | sortable, paginated, column selector | loading skeleton, empty, error, stale, sorted asc/desc | header focus + Enter sorts; row Enter opens detail | "20 of 24 statements", "Last cleared Mar 12, 2020 at 10:48 PM" |
| Filter/search bar | D | text search, app-name select, time-range picker, refresh | focused, applied, cleared | / focuses search; Esc clears | "Search Statement", "App: ALL", "Past 30 Minutes" |
| Row action menu | D | "…" overflow per row | open, focus-trapped, Esc closes | Esc closes, arrows traverse | "View details", "Cancel session" |
| Stat tile | S | capability count, usage, spend | loading, empty, error, delta up/down | tile focusable; delta labelled | "$203/mo based on 2 vCPU · 100 GB" |
| Drawer / session inspector | D | right sheet over table | loading, error, closing | Esc closes; focus returns to row | "Session details", "Statement fingerprint" |
| Dialog | S/F | confirm, form, cookie consent | scrim, open, closed, busy | Esc cancels; initial focus on safe control | "Delete organization — this cannot be undone" |
| Plan / cluster-tier control | F | Basic, Standard, Advanced cards | selected, comparing, prorating, blocked | radio semantics; arrows move | "$0.092 per vCPU-hour — $203/mo based on 2 vCPU · 100 GB" |
| Member row | S | org access list | pending, active, role menu, remove | row menu on Enter | "Role: Database Admin — change role" |
| Audit entry | S | event log line | expanded detail, filterable | expandable on Enter | "Cluster created by … · 2 min ago" |
| Command palette (docs search) | S | Ctrl K overlay | open, no results, recent | Ctrl K opens; Esc closes; arrows navigate | "Search… Ctrl K" |
| Chart card | D | time series, custom chart | loading skeleton matching plot geometry, empty ("no data in range"), error, stale | range picker focusable | "avg(jobs_row_level_ttl_rows_deleted)" |

**Every fetching surface also designs:** loading (skeleton matching final table/card geometry —
never a centred spinner on a blank page), empty (what's missing + the CTA that fixes it: "No
statements in this window — widen the time range"), error (what happened + how to recover: "Could
not reach the cluster — retry"), offline/stale (what's known vs cached: "Showing data from 4 min
ago — last refresh failed").

**Contracts this table encodes:** one primary filled CTA per view [F/S]; dense toolbars may run a
primary plus icon actions. Every icon-only control ("…", pencil, trash) carries a tooltip naming
the action. A disabled control states *why* on focus or hover rather than sitting silently dead.
A button never changes width between idle and loading — reserve the space.

## 10. Light / Dark Strategy

- **Posture:** split-shell — **A light-only** for the product console (verified: the shipped token
  set defines a single white-background mode) and **B dark-only** for the Continuum marketing
  shell. The reason: operators spend hours in the console, where light chrome and printed-style
  tables maximise legibility; the brand stage is authored dark for launch energy. No theme toggle
  ships in either shell today, so no role carries a phantom dark value.
- **Mechanism:** each shell owns a complete semantic role set (§3 tables); roles remap per shell,
  never per user preference. **No role is absent in its own shell** — product roles all resolve in
  light; marketing roles all resolve in dark. The single-mode roles above are listed with their
  shell and the reason (shipped product is light-only; shipped marketing is dark-only).
- **`color-scheme`** declared at the document root of each shell ("light" for the console, "dark"
  for marketing) so UA chrome, form controls and scrollbars follow the shell.
- **A scheme meta tag sits in the head before the stylesheet** in both shells, to prevent a flash
  of the wrong scheme.
- **Dark is authored, not inverted:** the marketing shell has its own surface ramp (#000000 /
  #0a0a0a / #101913), its own stroke strength (#323232 — stronger than any console hairline
  relative to canvas), and its own shadow policy (none). Text on dark is #ffffff, never grey
  inverted ink below 5.90:1.
- No org-tinted theme ships. If one is ever proposed, colour tokens may change but radii, type
  sizes and layout are frozen so a theme swap cannot move anything.

## 11. Density-Mode Strategy

- **Default mode per surface class:** [S] 44px rows for cluster overview, databases, settings, docs
  — the boundary is "a human reads a handful of records"; [D] 32px rows for statements, sessions,
  insights, metrics, jobs — the boundary is "an operator scans hundreds of records"; [F] for
  marketing and auth where nothing is scanned.
- **Mechanism:** a density marker on the app root rescales row height, cell padding, gutter and
  base body size together as tokens — density is a **token axis, not a media query**; spacing
  tokens themselves do not change with screen size.
- **Container queries drive reflow:** components measure their content box, so a chart card reflows
  to its panel, not the viewport. Size queries fail closed with no eligible container and viewport
  units silently substitute there — those units are never used where that fallback would be wrong.
- **Style queries** compare computed values, so the density marker must be a registered custom
  property with a concrete syntax before any style query can key off it.
- **The switch is an accessibility affordance**, not a preference: a density control satisfies
  users with visual field loss who need denser or looser layout; the console exposes Standard and
  Dense on every data surface.

## 12. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA for text contrast on the console canvas where feasible
  (text.primary already measures 14.41:1).
- **Target size:** ≥24×24 CSS px, or the spacing exception — a 24px-diameter circle centred on each
  target must not intersect another's. 44px is the design target for primary controls [F/S]; the
  40px control height plus 4px rhythm clears it; 24px is the hard minimum for dense-row icon
  actions. Zoom does not excuse it.
- **Keyboard:** every function operable — table headers (sort), row menus, time-range picker,
  column selector, chart scrubbing. Focus indicator is the #0055ff ring (3.97:1 on white ≥3:1) and
  never suppressed without a stronger replacement; the focused row is never entirely hidden by the
  sticky header or toolbar (SC 2.4.11).
- **Contrast:** text ≥4.5:1 (gate table §3); UI boundaries and focus ≥3:1. **Colour independence:**
  every status pairs colour with a glyph — READY badge, up/down delta arrows with sign, warning
  triangle, error octagon; latency bars pair fill with a numeric value in the same cell.
- **Motion:** the reduced-motion variant from §8 per component; marquees freeze, drawers crossfade.
- **Text:** ≤80-character measure, 1.5+ leading on prose, 200% resize without horizontal scroll on
  [S/F] surfaces (tables scroll within their own region).
- **Semantics:** real buttons, links and inputs; headers match visual rank; sort buttons expose
  state; loading regions announce busy; non-urgent metric refreshes announce politely.
- **Contrast preference:** if the user asks for more contrast, borders step from #e7ecf3 to
  #7e89a9 and text.secondary darkens to text.primary; values honoured: no-preference, more, less,
  custom.

## 13. Anti-Patterns

**Do** —
1. Keep SQL, hashes, node IDs and timestamps in Roboto Mono — identifiers are the product's nouns.
2. Right-align and tabulate every numeric column; a latency column in proportional figures is a bug.
3. Spend the purple once per view: the primary action, nothing else.
4. Use blue for every navigational and informational affordance (links, focus, info notes) so
   "blue = go/read" is learnable.
5. Pair each status with its wash and dark-text recipe from §3 — light fills, dark ink, glyph.
6. Match toolbar and pagination heights to the table's row height — chrome follows rows.
7. Draw charts only from the nine-hue metrics palette with washes for areas; series identity is
   tokenised.
8. Freeze marketing geometry when porting marketing patterns inward — the pill and the black stage
   stay outside the console.
9. Reserve red #ff3b4e for terminal-destructive moments; the everyday destructive voice is
   #cd2939 on wash.
10. Skeleton-match loading geometry to final table geometry on every data surface.
11. State why a control is disabled ("Diagnostics requires an Enterprise licence") on focus/hover.
12. Keep the two shells' canvases pure: #ffffff product, #000000/#101913 marketing — no
    in-between greys as full-page backgrounds.

**Don't** —
1. **No red or orange as the brand accent.** The roach logo notwithstanding, red is the danger
   intent and orange is warning; a red primary button collides with teardown flows.
2. No marketing aesthetics inside the product: no black canvases, lime text, mono eyebrows or pill
   buttons in the console.
3. No card inflation: a metric is a tile or a row, not a shadowed poster.
4. No stat-card dashboards as a substitute for sortable tables — overview tiles link into data
   surfaces, they don't replace them.
5. No modals as connective tissue; inspectors are drawers, confirms are one-shot dialogs.
6. No two filled primaries side by side; secondary actions outline or go text-only.
7. No toolbar of unlabelled icons — every icon control has a name (tooltip or visible).
8. No hover-only affordances on dense rows; the "…" menu is always visible.
9. No placeholder-as-label; the search field keeps its visible label and helper.
10. No whole-page spinners; skeletons match final geometry.
11. No native alert/confirm for destructive flows — the confirm dialog names cost and consequence.
12. No tiny type as a density strategy — density comes from rows, padding and column pruning.
13. No white-on-status-fill body text (#ffffff on #37a806 measures 3.10:1) — use the wash recipes.
14. No black-on-purple pill text swap in the console: the product pairing is white on #6933ff,
    which passes at 5.97:1.

## 14. Quick Reference & Verification Gate

**Flat colour reference (role → hex).** Product light: canvas #ffffff · inset #f5f7fa · hover
#f5f7fa · selected #e1ecff · border.subtle #e7ecf3 · border.strong #7e89a9 · focus/link #0055ff ·
accent.action #6933ff · onAction #ffffff · text.primary #242a35 · text.secondary #394455 ·
text.tertiary #475872 · text.disabled #7e89a9 · success #37a806/#237300/#e3f5e0 · warning
#ffa53b/#b26000/#fff4e1 · error #ff3b4e/#cd2939/#ffe9eb · info #0055ff/#0037a5/#e1ecff. Marketing
dark: canvas #000000 · card #101913 · stroke #323232 · text #ffffff/#888884 · highlight #aede54 ·
action #9059ff · data accent #60ecff · card text #f2f2ee.

**Flat type ramp.** Console: 24/600 page title · 20/600 section · 16/600 card title · 14/400 body
(1.7) · 13/400 dense cell · 12/500 uppercase headers+stat labels · mono 12–13 for SQL and
identifiers. Marketing: 64–72 hero · 40 section · 16 body · 13 mono eyebrow · mono data figures.

**Flat spacing + radius.** 4/8/12/16/24/32/48/64 · rows 44 [S] / 32 [D] · controls 40 · radius 2
console controls / 4 badges / 8 console cards / 16 docs panels / 24 marketing cards / full pills.

**Component → token map.** Primary button: accent.action + onAction + radius.xs + border.focus.
Data table: surface.canvas rows on surface.raised, border.subtle hairlines, text.primary/
secondary, code.text for SQL, status-* badges, chart.1 bars. Filter bar: surface.canvas +
border.subtle inputs, text.secondary labels, 40px controls. Stat tile: surface.raised +
text.secondary label + 24px tabular value + border.subtle. Drawer: surface.overlay + border.subtle
+ shadow level 3. Dialog: surface.overlay + border.strong + scrim #475872 at 80%. Chart card:
surface.raised + chart.1…9 series + chart.wash areas + border.subtle. Marketing pill CTA:
mkt.accent.action + mkt.onAction + radius.full. Marketing plan card: mkt.card + mkt.card-text +
mkt.highlight eyebrow + radius.xl.

**Pre-ship checklist.** 1 Zero raw hex outside L1. 2 No token resolves to a component name. 3 Every
contrast pairing computed, passing, unrounded (warning-on-wash and status-fill exceptions carry
their documented mitigation). 4 Every semantic role has a value in its shipped shell. 5 Every
fetching surface has loading/empty/error/offline specified. 6 Every component row lists disabled
and loading states. 7 Row, header, toolbar and pagination heights agree. 8 Reduced-motion variant
written for every authored motion. 9 Every control keyboard-reachable with a visible focus
indicator. 10 Dark shell authored, not filtered, with stroke strength exceeding the light shell's.
11 No unoverridden stock-library default inside a committed surface (Ant-like control defaults are
re-tokenised: radius 2, 40px height, ramp text colours). 12 Nothing came from a marketing page —
marketing evidence only informs the marketing shell roles.
