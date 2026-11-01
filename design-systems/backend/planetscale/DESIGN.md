# Design System — PlanetScale

<!-- premium-web-design:design-system 1 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: PlanetScale sibling spec @ premium-marketing-design/design-systems/devtools/planetscale/DESIGN.md (rung 1 — palette, type, posture raw materials from the marketing site), PlanetScale product evidence @ app.planetscale.com via official blog + docs screenshots (console behavior, density, components) -->
<!-- Surface classes: 10 routes classified (marketing home / product / pricing / docs, database overview, branches, deploy requests, connect dialog, web console, insights); density classes [F/S/D] assigned -->

## 1. Design Posture & Atmosphere

PlanetScale is a MySQL-compatible (Vitess), sharded-Postgres (Neki), and Postgres hosting platform whose whole identity is **database branching** — development branches, deploy requests, safe migrations — so the interface reads like Git hosting transplanted into a database control room. The visual metaphor is an **instrument panel with a terminal accent**: near-black canvases on observability surfaces, white canvases on data-management surfaces, monospaced identifiers everywhere, one orange action per viewport, and status told through disciplined green/blue/red marks rather than decoration. Eight hours inside it feel calm and dry: no gradients, no illustration, no marketing warmth — hairline-bordered panels, generous whitespace between regions, and dense mono metrics where data lives.

The brand signature is the **monospace voice**. The 2026 marketing site sets every string — nav, headlines, body, buttons — in the monospace stack with an amber announcement band and an orange accent bar prefixing headlines. The product splits the duty: system sans carries labels and prose; the monospace stack carries every identifier and measurement (branch names, shard ranges like `20-40`, latencies `p50: 0 ms`, region slugs `AWS us-east-1`, SQL diff lines). Chroma is budgeted: orange is reserved for the single filled CTA and the accent bar; green marks healthy topology nodes and the plan badge; blue owns links, focus rings, selection borders and donut gauges; red is quarantined inside destructive diff rows and delete actions; purple marks internal routing (load balancers); amber exists only as the announcement highlight and the Neki product tag.

Against its category defaults (Neon, Supabase, Cockroach Cloud — colorful gradient dashboards), PlanetScale is the austere one: flat surfaces, 1px hairlines instead of shadows, pills only where they mean "button" or "status", and a density that leans terminal — topology graphs, shard lists, and diff panels reward scanning, not browsing.

**Key Characteristics**
- Two shipped modes, both authored: product data surfaces run light (`#ffffff` canvas); observability/overview surfaces and the 2026 marketing site run dark (`#111111` canvas, theme-color `#111111`).
- Dark canvas is exactly `#111111`, never pure black; raised panels step to `#1a1a1a`; depth comes from these steps plus 1px hairlines — no drop shadows on data surfaces.
- One orange fill (`#f35815`) per viewport maximum: the primary CTA. Its label is dark `#111111` (5.59:1), never white.
- Headlines on marketing pages are prefixed by a 2px-wide, ~24px-tall vertical orange accent bar — the system's only decorative mark.
- Monospace stack (`ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace`) is the brand family; product UI labels use the system sans stack. Identifiers are *always* mono.
- `tabular-nums` mono for every comparable value: rows/s, GB, p50/p95, table counts, shard names, connection counts.
- Pills (9999px) mark buttons on dark surfaces and status badges (`Default`, `RO`, `Scaler`, `NEW`); light-mode buttons and inputs are 4px-rounded rectangles; cards are 0–6px.
- Status never travels alone: green primary/replica nodes carry icons, "Safe migrations" pairs a shield glyph, RO badges are labeled pills, diff deletions are red rows with minus-prefixed SQL.
- Row rhythm: standard tables ~44px rows, 12–16px cell padding; dense shard lists and logs ~32px rows, 8px padding; chrome heights match the rows they head.
- Buttons state intent in verb-first mono/sans microcopy: "New branch", "Create deploy request", "Get connection strings", "Open web console".
- Blue is the interaction hue on both modes: links (`#0b6ec5` light, `#47b7f8` dark), active-tab underline, selected-node border, gauge rings.
- Link color is the *only* blue text role; blue fills are reserved for badges (`RO`) and gauges, never buttons.
- Announcement band: full-width amber `#fbca00` strip, `#111111` mono text, the action phrase boxed in a dark inline pill.
- Customer logo grid renders partner logos in native color inside hairline cells — deliberately the most colorful region of the marketing site.
- Region slugs ("AWS us-east-1 · Availability zone C") are set as sans secondary text directly beneath node titles — geography is metadata, never a map or globe.
- Replication lag is a first-class datum: dotted connector lines between nodes carry mono lag values (`0s`, `2s`) at the midpoint, green when healthy.

## 2. Token Architecture   ← normative

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a **primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value*: `gray.50…gray.900`, `blue.50…blue.950`, `orange.50…orange.950`, `green.50…green.950`, `red.50…red.950`, `yellow.50…yellow.950`, `purple.50…purple.950`, `neki #fbca00`, `white #ffffff`, `black #000000`, `radius.xs 2px`, `radius.sm 4px`, `space.1…space.16`. Referenced only by L2. Banned: component-named primitives (`card-bg`, `tooltip-color`) — one value, many roles.
- **L2 Semantic** — role names: `surface.canvas`, `surface.raised`, `surface.overlay`, `surface.inset`, `surface.hover`, `surface.selected`, `border.subtle`, `border.strong`, `border.focus`, `accent.action`, `accent.onAction`, `accent.subtle`, `text.primary`, `text.secondary`, `text.tertiary`, `text.disabled`, `text.link`, `status.success`, `status.warning`, `status.error`, `status.info`, plus their `wash` companions. The only layer a component may consume.
- **L3 Component** — only for deliberate deviation (e.g. `topbar.height`, `topology.node-border-selected`); points at L2 or L1, never a raw value, never a sibling component's token. The registered L3 set is deliberately short: topbar height, tab-rail height, topology node geometry, drawer width, diff line height — five families, each overridable in one place.

**Rules.** Every token has a determinable type or it is invalid; names are case-sensitive and free of `$`, `{`, `}`, `.`; circular references are an error. Every semantic token carries a value in **every** shipped mode — a role with no dark value resolves to its light value and fails contrast (PlanetScale ships both modes everywhere; there are no single-mode roles). Animatable tokens must be registered with both `syntax` and `inherits` declared or the registration is invalid, and `initial-value` must be computationally independent, so `%`/`em` are illegal as initial values.

**Layer order (low → high)** `[reset] → [primitives] → [semantic] → [components] → [utilities]`. Layer order beats specificity entirely, and an un-layered normal declaration outranks every layered one — a stray un-layered rule inside a component file would defeat this whole system, so anything a consumer must override without escalation sits in the top layer.

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` | `#ffffff` product · `#fafafa` marketing | `#111111` | product data pages white; marketing gray-50; dark never pure black |
| `surface.raised` | `#ffffff` | `#1a1a1a` | cards, topology node cards, drawers (hairline-delimited, no shadow) |
| `surface.overlay` | `#ffffff` | `#1a1a1a` | dialogs, connect modal |
| `surface.inset` | `#fafafa` | `#111111` | code blocks, diff wells, filter inputs |
| `surface.hover` | `#ebebeb` 60% | `#2b2b2b` | rows, menu items |
| `surface.selected` | `#ddf2ff` (blue.100) | `#08204e` (blue.950) | selected framework card, selected shard row |
| `border.subtle` | `#e1e1e1` | `#2b2b2b` | decorative hairlines, card edges (non-essential boundaries) |
| `border.strong` | `#818181` | `#818181` | 1px boundaries that must read at 3:1 on raised |
| `border.focus` | `#0b6ec5` | `#47b7f8` | focus ring + selected-node outline, ≥3:1 |
| `accent.action` | `#f35815` | `#f35815` fills; `#fafafa` raised pill is the dark-mode primary button | budget: 1 fill per viewport |
| `accent.onAction` | `#111111` | `#111111` on orange · `#111111` on raised pill | never white on orange |
| `accent.subtle` | `#ffe8d8` (orange.100) | `#3c1403` (orange.900) | highlight washes |
| `text.primary` | `#111111` | `#fafafa` | headings, body |
| `text.secondary` | `#414141` | `#a1a1a1` | body-strong, row secondary on dark |
| `text.tertiary` | `#737373` | `#818181` | captions, timestamps ("3 minutes ago") |
| `text.disabled` | `#a1a1a1` | `#616161` | inactive components (SC 1.4.3 exempt; still ≥3:1 dark) |
| `text.link` | `#0b6ec5` | `#47b7f8` | the only blue text role |
| `status.success` | `#13862e` (green.600) | `#27b648` (green.500) | healthy nodes, Scaler badge text, "8 shards" dot |
| `status.warning` | `#7d5903` (yellow.600) | `#f2b600` (yellow.300) | throttling notices, deploy warnings |
| `status.error` | `#d92038` (red.600) | `#ff455d` (red.500) | destructive diff, delete actions |
| `status.info` | `#0b6ec5` | `#47b7f8` | RO badges, gauge rings, replication lag |
| `brand.routing` | `#8467f3` (purple.500) | `#b7a5fb` on `#27124a` chip | load balancers, internal routing nodes — never a button or link |
| `brand.product-tag` | `#fbca00` on `#111111` text | same | Neki engine tag, "NEW" chip, announcement band |
| washes | success `#effff3` · warning `#fffbe4` · error `#ffe5e9` · info `#ddf2ff` | success `#0a2b13` · warning `#281e03` · error `#341418` · info `#08204e` | each status ships a glyph — never colour alone |

Dark canvas is **not** pure black: `#111111` canvas with `#1a1a1a` raised, one step apart, separated by `#2b2b2b` hairlines. Depth in dark comes from surface steps and 1px strokes, never shadows. The purple family (`#8467f3` light / `#4b3990`-range dark) and the Neki yellow `#fbca00` are product-identity accents: purple marks load balancers/internal routing in topology, amber marks the announcement band and "NEW" tags — neither is a button color.

**Contrast gate — computed ratios (relative-luminance method, unrounded to 2 dp; 4.499:1 fails):**

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| text.primary (light) | `#111111` | surface.canvas (product) | `#ffffff` | 18.88:1 | 4.5 | pass |
| text.primary (light, marketing) | `#111111` | surface.canvas | `#fafafa` | 18.09:1 | 4.5 | pass |
| text.secondary (light) | `#414141` | `#fafafa` | `#fafafa` | 9.78:1 | 4.5 | pass |
| text.tertiary (light) | `#737373` | `#fafafa` | `#fafafa` | 4.54:1 | 4.5 | pass |
| text.primary (dark) | `#fafafa` | surface.canvas | `#111111` | 18.09:1 | 4.5 | pass |
| text.secondary (dark) | `#a1a1a1` | `#111111` | `#111111` | 7.30:1 | 4.5 | pass |
| text.tertiary (dark) | `#818181` | `#111111` | `#111111` | 4.85:1 | 4.5 | pass |
| accent.onAction | `#111111` | accent.action | `#f35815` | 5.59:1 | 4.5 | pass |
| accent.onAction (dark pill) | `#111111` | accent.action raised | `#fafafa` | 18.09:1 | 4.5 | pass |
| border.strong (light) | `#818181` | surface.raised | `#ffffff` | 3.90:1 | 3.0 | pass |
| border.strong (dark) | `#818181` | surface.raised | `#1a1a1a` | 4.47:1 | 3.0 | pass |
| border.focus (light) | `#0b6ec5` | `#ffffff` | `#ffffff` | 5.18:1 | 3.0 | pass |
| border.focus (dark) | `#47b7f8` | `#111111` | `#111111` | 8.45:1 | 3.0 | pass |
| status.success (dark) | `#27b648` | `#111111` | `#111111` | 7.08:1 | 4.5 text / 3.0 glyph | pass |
| status.success (light) | `#13862e` | `#ffffff` | `#ffffff` | 4.69:1 | 4.5 | pass |
| status.error (light) | `#d92038` | `#ffffff` | `#ffffff` | 4.98:1 | 4.5 | pass |
| status.error (dark) | `#ff455d` | `#111111` | `#111111` | 5.63:1 | 4.5 | pass |
| status.warning (dark) | `#f2b600` | `#111111` | `#111111` | 10.31:1 | 4.5 | pass |
| status.info / text.link (light) | `#0b6ec5` | `#ffffff` | `#ffffff` | 5.18:1 | 4.5 | pass |
| status.info / text.link (dark) | `#47b7f8` | `#111111` | `#111111` | 8.45:1 | 4.5 | pass |

Rejected pairings (computed, do not ship): white `#fafafa` text on orange `#f35815` = 3.23:1 (fails 4.5) — the orange button always carries `#111111`; green.500 `#27b648` glyph on white = 2.67:1 (fails 3.0) — light mode uses green.600; `#c1c1c1` as a boundary on white = 1.80:1 — gray-300 is decorative-only; `#414141` border on `#1a1a1a` = 1.70:1 — dark boundaries use `#818181`.

## 4. Typography

**Families.** Brand/UI monospace: `ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace` — weights 400/500/600(/700 emphasis); the entire marketing site is set in it (body 16px, tracking −0.006em). Product UI: `ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif` — weights 400/500/600 — carries labels, prose, and navigation in the console. Numeric/code: the monospace stack for every identifier (branch, database, org, shard), region slug, SQL line, metric value, timestamp, and password/connection string. *Monospace is for identifiers, measurements and code — and, on marketing pages, the whole voice; it is not a costume for long product prose.*

**One ramp per class:**

- **[F] Focused, 16px base** (auth, connect dialog, settings detail, docs prose):

| Role | Family | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|---|
| Display | sans | 32px | 600 | 40px | −0.02em | — | dialog/section headline |
| Heading | sans | 24px | 600 | 32px | −0.015em | — | grouped-form heading |
| Body | sans | 16px | 400 | 24px | 0 | — | instructions, descriptions |
| Label | sans | 14px | 500 | 20px | 0 | — | field labels, radio card names |
| Meta | mono | 13px | 400 | 18px | 0 | tabular | connection strings, helper IDs |

- **[S] Standard, 14px base** (database overview, branches, deploy requests, org pages):

| Role | Family | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|---|
| Page title | sans | 20px | 600 | 28px | −0.01em | — | "Branches", database name |
| Section title | sans | 16px | 600 | 24px | 0 | — | "Metrics and performance" |
| Body | sans | 14px | 400 | 21px | 0 | — | descriptions |
| Row primary | sans | 14px | 500 | 20px | 0 | — | branch row lead cell |
| Row secondary | sans | 13px | 400 | 18px | 0 | — | region, "branched from main 3 minutes ago" |
| Stat value | mono | 24px | 500 | 32px | 0 | tabular | 11 tables · 23.3 billion · 187.0 GB |
| Stat label | sans | 12px | 500 | 16px | +0.04em, uppercase | — | ROW READS · STORAGE |
| Meta | sans | 12px | 400 | 16px | 0 | tabular | "updated hourly" |

- **[D] Dense, 12–13px base, data surfaces only** (shard list, web console output, query insights tables, schema diff):

| Role | Family | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|---|
| Grid header | sans | 12px | 500 | 16px | +0.02em, uppercase | — | Branch · Region · Updated · Created |
| Grid cell numeric | mono | 13px | 400 | 20px | 0 | tabular | lag `0s`, rows/s, GB |
| Grid cell text | sans | 13px | 400 | 18px | 0 | — | shard list secondary text |
| Log line | mono | 12px | 400 | 18px | 0 | — | console query output |
| Inline help | sans | 12px | 400 | 16px | 0 | — | hints under fields |

Prose inside a dense screen still steps up to the [S] body size. Marketing pages run the mono ramp instead: body 16px/24px weight 400 tracking −0.006em, subhead 18px, heading-sm 24px/32px weight 600, heading 32px/40px weight 600 — the hero line and nav share the same family at different weights, so the site reads as one continuous terminal page.

**Invariants.** `tabular-nums` on every comparable value — currency, timestamps, deltas, counts, rows/s, GB, shard ranges — right-align numeric columns, left-align text, never centre a numeric column. Branch/database/shard names render in mono even inside sans sentences (e.g. "branched from `main`"). Fixed stepped sizes only, no fluid interpolation. Measure ≤80 characters (SC 1.4.8); 65–80ch for [F/S] prose, unconstrained for [D] logs and diff lines.

## 5. Spacing Scale & Density Scales   ← two axes, never one

**Spacing base: 4px grid; 8px comfortable in [F/S], 4px in [D].** `space.0` 0 · `space.1` 4px icon-to-label · `space.2` 8px control padding [D], button gaps · `space.3` 12px cell padding [S], card padding [D] · `space.4` 16px card padding [S] / page gutter · `space.6` 24px card padding [F] + section gap · `space.8` 32px section gap [S] · `space.12` 48px region separation · `space.16` 64px rarely (marketing band separation). *No 17px. No 23px. If a layout needs an off-scale value, the layout is wrong.*

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | Auth, connect dialog, settings detail, docs prose |
| `standard` | 44px | 14px | 12–16px | 24px | Database overview, branches, deploy requests, org members |
| `dense` | 32px | 12–13px | 8px | 16px | Shard list, web console, query insights, schema diff, logs |

- Density comes from **row height, column pruning and leading** — never from type too small to read. A 13px tabular numeral in the shard list is correct; the same numeral in the connect dialog is a defect.
- **Never switch mid-page.** A deploy-request page is standard-density throughout; its diff well is dense by role, not by accident. Switching across routes with different jobs is legitimate — the overview page should feel like a different room from the branches table.
- **Chrome follows rows.** Tab bar, filter bar, and pagination heights match the table's row height (44px chrome over 44px rows; 32px over 32px). A 44px toolbar over 32px shard rows is a rhythm break.
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40%. *House heuristic — validated against screenshots: the dark overview page sits ≈45%, the shard drawer ≈35%, the branches table ≈50%.*
- Measured anchors from screenshots: the branches table's header band and filter bar share the 44px rhythm; the shard drawer's list rows measure ≈32px with 8px padding; topology node cards pad 12px with 8px title-to-meta gaps.
- The deploy-request page keeps standard density for its prose and controls while the diff well alone runs dense — a role-scoped exception, not a mid-page density switch.

## 6. Radius Scale

`none` 0 — topology node cards, table containers on dark · `xs` 2px — small tags, diff line markers · `sm` 4px — inputs, light-mode buttons ("New branch" charcoal button, "Connect"), light cards, framework cards · `md` 6px — drawers, dropdown panels, stat tiles · `full` 9999px — dark-mode primary buttons ("New branch", "View all query insights"), branch/status pills (`Default`, `RO`, `Scaler`, `NEW`), avatar, plan badge. **One radius per component family**, never mixed ad-hoc: dark buttons are always pills, light buttons are always 4px. Nested radii obey `radius_inner = radius_outer − padding`.

## 7. Elevation

**Strategy: flat + hairline, one shadow exception.** PlanetScale surfaces are border-separated, not shadow-elevated — panels sit directly on canvas, delineated by 1px `border.subtle`. Levels, low → high: **0** canvas (no shadow, both modes) · **1** raised card/panel — surface step (`#1a1a1a` on dark, white with `border.subtle` on light) · **2** sticky top bar/tab rail — surface step + `border.subtle` bottom hairline · **3** drawer/overlay — `border.strong` hairline plus the system's only shadow (0 8px 24px black 25%) and a scrim at 60% black behind modal overlays · **4** dialog (connect modal, password dialog) — scrim + shadow, `radius.md`. No glows, no layered ambient shadows, no elevation on tables or topology nodes. Dropdown menus sit at level 3 with the same shadow token — one blur, one offset, everywhere.

## 8. Motion

`instant` 0ms · `fast` 120ms ease-out (exits, dense-surface hover, tab switches) · `base` 180ms decelerate (drawer entrances, dropdowns, [D] entrances) · `slow` 240–300ms decelerate ([F/S] entrances, dialog fade+scale 0.96→1).

- Entrances decelerate, exits accelerate; symmetric ease-in-out on both directions is a defect.
- Animate `transform` and `opacity` only — never width, height, top, left. Drawer slides 16px in from the right edge with fade.
- Live metrics (gauges, latency sparklines) update in place without entrance animation; gauge ring sweeps interpolate stroke opacity at `base` (180ms) — they never spin or pulse to fake activity.
- No bounce on irreversible moments — deploying a schema change confirms statically, then shows progress as a status line.
- Topology node selection: border color/weight swap at `fast`; no pulse loops on idle nodes.
- **Reduced motion is a real variant, not a blanket none:** movement → crossfade under ~150ms; scaling/panning of large objects (topology zoom, drawer slide) neutralises entirely per the vestibular guidance; metric fades may persist.

## 9. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell / top bar | S | marketing (dark) · console (light/dark) | default, org-menu-open, loading | Tab order logo → org → db → tabs; menus on Enter/Arrow | org / database breadcrumb switcher |
| Database tab rail | S | Overview · Deploy requests · Branches · Insights · Console · Backups · Settings | active (blue underline), inactive, hover | Arrow-key roving, Home/End | — |
| Branch table | S | production tree (indented), flat dev list | loading skeleton, empty, row hover | Row focus, Enter opens branch | "Filter branches..." |
| Filter/search bar | S/D | table filter, shard filter, table filter on branch page | focused, filled, clearing | Slash focuses, Esc clears | "Filter tables..." / "Filter shards..." |
| Row action menu | S | branch row: Delete · Set as default | focus-trap, Esc closes, disabled states why | Arrow roving, Esc | "Delete branch"; disabled explains protection |
| Stat tile | S | count (Tables 11) · donut gauge (Row reads/writes, Storage) · delta tile (Created/Altered/Dropped tables, red wash on drop) | loading (skeleton), stale ("Usage as of 2 hours ago") | — | "Monthly usage resets in 5 days. Manage plan" |
| Drawer/inspector | S | node metrics (Primary), shard list, shard detail | open, loading, error, Esc-closed | Esc closes; focus returns to trigger | "Shards — 8 shards on main-next" |
| Dialog / connect modal | F | framework picker grid, password reveal, delete confirm | step 1 of flow, selected (blue border), submitting | Radio-card roving, Enter selects | "Select your language or framework" |
| Deploy request diff | D | CREATE/ALTER (+green) · DROP (−red wash) | collapsed table header, expanded, changes-only filter | Table header toggles with Enter | "Drop the stars table" |
| Plan/seat control | S | plan pill (Scaler) + Upgrade link | current, upgradeable, blocked (deleted) | Link focusable | "Scaler · Upgrade" |
| Member row | S | org members list | role dropdown, remove confirm | Enter opens role menu | role name + email |
| Audit/insights entry | D | query insights rows (statement, count, latency) | hover, expanded, empty | Enter expands | "View all query insights" |
| Web console | D | query editor + results grid | running, results, error banner, no-rows | Query submit, results grid arrows | "Open web console" |
| Topology graph | S | load balancers → primary → replicas (+shard ring) | node hover, selected (blue border), degraded (red dot) | Arrow between nodes, Enter opens drawer | "Load balancers — 3 across 3 availability zones" |
| Password/connect dialog | F | connection string, password reveal, language picker | generating, revealed (blur toggle), copied | Enter generates; Esc closes | "Create a password" |
| Region selector | S | dropdown in create flows, pricing form | open, filtered, selected | Arrow roving, type-ahead | "AWS us-east-1" |
| Announcement band | S (marketing) | single promotional strip | default, dismissed | Dismiss on Enter | "Neki, sharded Postgres, is now available. Learn more" |

**Every fetching surface also designs:** loading = skeleton matching final geometry (table shows gray-100/gray-800 row bands, never a centred spinner on a blank page); empty = what is missing plus the CTA that fixes it ("No branches yet — New branch"); error = what happened plus recovery ("Couldn't load insights — Retry"); stale = "Usage as of 2 hours ago (updated hourly)" naming the data's age instead of pretending freshness.

**Contracts this table encodes:** one primary filled CTA per view [F/S] (dense toolbars may run a primary plus icon actions); every icon-only control carries a tooltip ("Close drawer"); a disabled control states why on focus/hover (deletion-protected branch names why Delete is unavailable); a button never changes width between idle and loading — "Create deploy request" reserves its label space with an inline progress swap.

## 10. Light / Dark Strategy

- **Posture: C — dual-parity, surface-split.** Product data-management surfaces (branches, deploy requests, org, settings) are authored light (`#ffffff` canvas, charcoal `#111111`–`#1a1a1a` primary buttons); observability surfaces (database overview, topology, insights, connect modal) and the 2026 marketing site are authored dark (`#111111`). Both are first-class authored themes, documented side by side in §3; neither is a filtered copy.
- **Mechanism:** semantic roles remapped per mode; no role absent in either mode — every row in the §3 table has both columns filled. Orange, purple and Neki amber are mode-invariant; blues and greens swap ramp stops (blue.600↔blue.400, green.600↔green.500, red.600↔red.500) to hold contrast.
- **`color-scheme`** is set on the root element per surface class so UA chrome, form controls and scrollbars follow the authored mode; it repaints UA-provided parts of the canvas and does not theme the document by itself.
- **A mode meta tag sits in the head before the stylesheet** to prevent a flash of the wrong scheme on dark-first routes (the shipped theme-color is `#111111`).
- **Dark is authored, not inverted:** its own surface ramp (`#111111/#1a1a1a/#2b2b2b`), its own border strength — dark `border.strong` must exceed light's effective contrast (`#818181` scores 4.47:1 on `#1a1a1a` vs 3.90:1 light), its own accent stops, no shadows except the overlay exception. `light-dark()` may express the pairing but is progressive enhancement only.
- Org-tinting is not a shipped capability; if ever introduced it changes colour tokens only — radii, type sizes and layout are frozen so a theme swap cannot move anything.
- **Mode is per-surface-class, not per-user-toggle in the product:** a route is authored light or dark and stays that way within a session; the marketing site honours the visitor's mode preference through its dark-class mechanism, so the same semantic roles serve both behaviours.

## 11. Density-Mode Strategy

- **Default mode per surface class:** console database pages → standard (44px rows); shard list, web console, query insights, logs → dense (32px); connect dialog, settings detail, auth → focused. The boundary is the job: scanning many records is dense; deciding one thing is focused.
- **Mechanism:** a density marker at the application root rescales row height, cell padding, gutter and body size together as one token axis — spacing tokens do not change values per screen size or viewport; density is a deliberate axis, not a media query.
- **Container queries drive reflow:** components measure their content box, so a stat-tile row reflows to its container, not the viewport. Size queries fail closed with no eligible container, and container-query units silently resolve to small-viewport units there — container units are never used where that fallback would be wrong.
- **Style queries** compare computed values, so the density marker must be a registered custom property for style-based branching to work.
- **The dense switch is offered as an accessibility affordance**, not a preference: a layout-density control honours users with visual field loss (W3C's SC 2.5.8 note endorses exactly this mechanism).
- The web console and shard list open dense by default because their job is comparison across many records; the database overview opens standard because its job is one glanceable decision.

## 12. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum across both modes; AAA (SC 1.4.6 7:1) is already met by `text.primary` (18.09–18.88:1) and `text.secondary` (7.30:1 dark) where used for body copy.
- **Target size:** ≥24×24 CSS px hard minimum (SC 2.5.8) with the spacing exception respected; 44×44 is the design target for primary controls in [F/S] — tab stops, "New branch", drawer close. *Zoom does not excuse it.*
- **Keyboard:** every function operable (SC 2.1.1) — branch rows, topology nodes, framework radio-cards, shard list; focus indicator visible (SC 2.4.7) using `border.focus` (blue ring 2px + 2px offset), never outline removal without a stronger replacement; the focused row is never entirely hidden behind the sticky tab rail (SC 2.4.11).
- **Contrast:** text ≥4.5:1 (gate table §3, computed); UI boundaries and focus indicators ≥3:1. **Colour independence:** every status pairs colour with a glyph or label — green nodes carry the primary/replica icon, RO badges are labeled pills, diff lines carry the SQL verb itself, latency dots sit beside `p50:`/`p95:` labels; deltas carry a sign.
- **Motion:** the §8 reduced-motion variant per component; topology zoom is the neutralised scaling trigger.
- **Text:** ≤80-character measure on [F/S] prose, 1.5 leading on body, 200% resize without horizontal scroll (SC 1.4.8); dense logs scroll, they do not reflow away.
- **Semantics:** real buttons/links/inputs; the tab rail is a tablist, drawers are dialogs with labelled state, `aria-live="polite"` announces deploy-request status changes, `aria-busy` on loading insight tables.
- **Contrast preference:** `prefers-contrast: more` promotes `border.subtle`→`border.strong`, `text.tertiary`→`text.secondary`, and thins translucent washes to their solid ramp stops (values honoured: `no-preference`, `more`, `less`, `custom`).
- **Locale/format:** relative timestamps ("3 minutes ago") carry absolute values in tooltips; byte and count formats use the en-US grouping shipped today (23.3 billion, 187.0 GB) with tabular figures so columns stay aligned under translation.

## 13. Anti-Patterns

**Do**
- Set identifiers, metrics, and all SQL in the mono stack — the Git-for-databases mental model is carried by type (branch names read as refs).
- Keep the orange fill to one per viewport: it marks the single conversion or creation action ("Get in touch", "New branch"); everything else is ghost, hairline, or text.
- Prefix marketing headlines with the 2px orange accent bar — it replaces icons, badges, and colored headings as the decorative voice.
- Build hierarchy with surface steps and 1px hairlines on dark (`#111111` → `#1a1a1a` → `#2b2b2b`), never with shadows.
- Pair every status with a glyph: shield for production, check-circle for safe migrations, dot for the "8 shards" chip, RO pill for read-only replicas.
- Reserve pills for buttons on dark surfaces and for status badges everywhere; keep light-mode buttons at 4px.
- Match chrome height to row height (44px tab rail over standard tables, 32px over dense shard lists).
- Use tabular mono numerals for every stat, lag, and byte figure; right-align them in tables.
- Name data age on stale surfaces ("Usage as of 2 hours ago (updated hourly)") instead of hiding it.
- Keep replication lag and latency visible at the place where the thing is rendered — dotted connector midpoints on topology, drawer headers on metrics — so numbers never float without an owner.
- Show skeleton geometry for loading tables (gray-100/gray-800 bands) matching final row heights.
- State why a destructive control is disabled ("Deletion protection is enabled for this branch").
- Give every destructive action a confirming dialog that names the object ("Drop the stars table").

**Don't**
- No white text on the orange fill (3.23:1 — computed fail); the orange CTA is always `#111111` on `#f35815`.
- No blue as a filled button background — blue is links, focus, selection borders, RO badges, and gauges only.
- No green.500 on light canvases (2.67:1) — light mode uses green.600 for text/icons.
- No proportional font on identifiers, and no mono on long-form settings prose — the split in §4 is the contract.
- No gradients, glows, illustration, or photography inside the product; the customer logo grid is the only full-colour imagery, on marketing pages only.
- No amber as a surface fill (cards, buttons, panels) — `#fbca00`/`#f2b600` belong to the announcement band and tags.
- No card inflation: a stats row is hairline-separated tiles on the same canvas, not a bento of tinted cards.
- No stat-card dashboards with decorative sparklines that carry no axis or unit — every gauge names its unit (GB, rows/s).
- No modals as connective tissue: branch → deploy request is a page, not a wizard stack; modals are single-decision.
- No two primary actions side by side; "Connect" and "New branch" never compete in one view.
- No hover-only affordances — row menus expose on focus, and every icon control has a label or tooltip.
- No tiny type as a density strategy — 12px is the dense floor, and dense mode also rescales padding and rows.
- No `alert()`/`confirm()` for destructive flows — the confirming dialog names the object and consequence.
- No whole-page spinners; skeletons match final geometry.
- No decoration borrowed from the marketing voice inside product surfaces — the accent bar and amber band stay on the marketing site, mono-with-sans is the product's voice.
- No keyboard traps in the drawer/dialog pair: focus returns to the triggering node or row when a metrics drawer or connect dialog closes.

## 14. Quick Reference & Verification Gate

**Colour (role → light / dark):** canvas `#ffffff`·`#fafafa` / `#111111` · raised `#ffffff` / `#1a1a1a` · inset `#fafafa` / `#111111` · hover `#ebebeb` / `#2b2b2b` · selected `#ddf2ff` / `#08204e` · border.subtle `#e1e1e1` / `#2b2b2b` · border.strong `#818181` / `#818181` · border.focus `#0b6ec5` / `#47b7f8` · accent.action `#f35815` (both; dark raised pill `#fafafa`) · onAction `#111111` (both) · text `#111111·#414141·#737373·#a1a1a1` / `#fafafa·#a1a1a1·#818181·#616161` · link `#0b6ec5` / `#47b7f8` · success `#13862e` / `#27b648` · warning `#7d5903` / `#f2b600` · error `#d92038` / `#ff455d` · info `#0b6ec5` / `#47b7f8` · brand extras purple `#8467f3` / `#4b3990`, neki amber `#fbca00` (band/tags only).

**Type ramp:** [F] 32/24/16/14/13 · [S] 20/16/14/13/12 (stat value mono 24) · [D] 12–13 · marketing mono 16 base, headings 24–32 weight 600, tracking −0.006em. Weights: sans 400/500/600, mono 400/500/600.

**Spacing + radius:** base 4px; scale 0/4/8/12/16/24/32/48/64 · density rows 44px [S] / 32px [D] · radius none 0, xs 2, sm 4, md 6, full pill.

**Component → token map:** top bar consumes surface.canvas, border.subtle, text.primary/secondary, accent.action+onAction · tables consume surface.canvas/raised, border.subtle, text.primary/secondary/tertiary, surface.hover · stat tiles consume surface.raised, border.subtle, text.primary (mono value), text.tertiary (label), status.info (gauge ring) · drawer consumes surface.raised, border.strong, text.primary/secondary, status.* · dialog consumes surface.overlay, border.focus (selected radio card), text.primary/secondary · diff consumes surface.inset, status.error+error wash, status.success+success wash, text.primary mono · plan pill consumes status.success wash+text, text.link (Upgrade).

**Pre-ship checklist.**
1. Zero raw hex outside L1.
2. No token resolves to a component name.
3. Every contrast pairing computed, passing, unrounded (§3 gate; 4.499:1 fails).
4. Every semantic role has a value in both shipped modes.
5. Every fetching surface has loading/empty/error/stale specified.
6. Every component row lists disabled and loading states.
7. Row, tab-rail, filter-bar and pagination heights agree per density.
8. Reduced-motion variant written for every authored motion (incl. topology zoom).
9. Every control keyboard-reachable with a visible focus indicator.
10. Dark authored, not filtered, with border strength exceeding light's.
11. No unoverridden stock default inside a committed surface.
12. Nothing came from a marketing page into the product spec except the brand tokens it legitimately shares.
