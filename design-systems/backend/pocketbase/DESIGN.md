# Design System — PocketBase

<!-- premium-web-design:design-system 1 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: PocketUI admin-UI source (github.com/pocketbase/pocketbase ui/src/css — vars.css, base.css, fonts.css, layout.css, toast.css) supplied the token primitives, type scale, radii, motion and density values verbatim (ladder rung 2, official product source — rung 1 sibling catalogs had no pocketbase entry); sampled pixels of the five verified captures in screens/ grounded the marketing canvas blue, chip washes and row pitches (ladder rung 3); GitHub discussion #7652 confirmed the v0.23+/v0.37 accent shift from blue to monochrome -->
<!-- Surface classes: 5 routes classified (marketing overview, docs, collections dashboard, record editor, logs); density classes F/S/D assigned -->

## 1. Design Posture & Atmosphere

PocketBase ships an entire backend — embedded SQLite, auth, realtime subscriptions, file storage —
as one executable, and its admin dashboard inherits that thesis: one room, no corridors, nothing
decorative. The interface is a compact machine panel in a light workshop. White canvas, a
240px sidebar wearing the palest grey in the system, hairline dividers, and a single near-black
charcoal that owns every primary action. Blue is present but demoted: it labels information and
pickers (the datetime picker's segmented buttons, text links, the API console accents) and never
competes with charcoal for "go". After eight hours of editing collection schemas and scrolling
logs, the eye registers zero noise — the register is "well-machined tool", not "dashboard
theatre". The single visual metaphor: **a one-room workshop bench** — every tool within reach,
each labelled once, no drawers of drawers.

Against its category (Supabase's dark neon studio, Firebase's grey Google chrome, Appwrite's
violet shell), PocketBase is the smallest and the quietest: a 14px IBM Plex Sans base, 45px
controls, two font weights, two radii, one shadow. The v0.23+/v0.37 UI rework deliberately moved
the primary accent from blue to monochrome charcoal — the admin surface now reads as ink on paper
with blue reserved for information. Marketing surfaces (pocketbase.io) are the brand's one
colourful gesture: a light blue canvas (#B2D5E1, sampled #B2D5E1–#B5D8E3) with a fine topographic
contour pattern, the PB tile logo, and charcoal buttons — a poster pinned above the workbench,
never bleeding into it.

**Key Characteristics**
- One primary fill per viewport: charcoal #25272D in light, #3B3B3B in dark; "New Record",
  "Live demo", "Save" all wear it. Secondary actions are grey fills or outlined, never a second
  saturated colour.
- Blue is an information colour, not an action colour: #3376E5 info, #1055C9 link/accent, the
  datetime picker's segmented buttons, text links at 6.635:1. Accent budget: 1 charcoal fill +
  ≤2 blue links per viewport region.
- Status is a wash, never a shout: chips and toasts pair a 20%-tint wash (#D3EEE2 success, #FAE3D6
  warning, #F3D7DC danger, #D6E4FA info) with ordinary ink text and a status-coloured glyph —
  sampled "True" chip: #D5EFE4 wash, #4A4D50-range ink.
- Canvas is white #FFFFFF; the sidebar and wells sit one step down at #F8F9FA with a 1px #E4E8EC
  divider; hover fills #F8F9FA, selected fills #E4E8EC (sampled #F6F7F9/#E8EAEE on the live demo).
- Exactly two type weights ship — 400 and 600 — in IBM Plex Sans (UI) and IBM Plex Mono
  (identifiers, filter expressions, API rules, log lines), self-hosted WOFF2.
- Base type 14px/22px (13px small, 15px large); headings run 26/32 down to 16/24, all weight 400 —
  hierarchy comes from size, not boldness. Global letter-spacing 0.004em normalises Plex rendering.
- Controls are 45px tall (52 large, 35 small, rescaling to 40/47/30 under 900px); inputs pad 13px;
  the records grid rows measure a sampled 46px pitch.
- Radius is a two-value system: 5px on every control, chip and code block; 15px on large panels
  and auth cards. Nothing else.
- Depth is one soft shadow (0 8px 5px -5px at 10% ink) plus scroll-edge shadows on sticky
  containers; dark mode swaps shadows for a five-step surface ramp over #1B1B1B.
- Identifiers — record ids like WyAw4bDrwvs6gGl, filter expressions, API rules, log lines — are
  always mono in grey chips or plain mono text; mono is never a costume for prose.
- Motion is 150ms base, 70ms press, 200ms modal slide, 1.1s loader spin; entrances decelerate,
  exits accelerate, nothing bounces.
- The wordmark is set in Plex Sans 600 with "Pocket" at 400 ("PocketBase"); the PB mark is two
  overlapping white tiles with 2px ink borders. One lockup per screen, header only.

## 2. Token Architecture

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by *value*: `ink.900` #25272D, `ink.hint` #687278,
  `ink.disabled` #A2A9AE, `grey.0` #FFFFFF, `grey.98` #F8F9FA, `grey.90` #E4E8EC, `grey.86`
  #DCE0E5, `grey.83` #D3D9DF, `grey.80` #CCD4DB, `blue.info` #3376E5, `blue.accent` #1055C9,
  `green.success` #22A96D, `orange.warning` #E57534, `red.danger` #C33751, `canvas.night` #1B1B1B,
  `ink.night` #EBEBEB, `space.13`, `radius.5`, `duration.150`. Dark status primitives:
  `green.night` #27865D, `orange.night` #CF4E17, `red.night` #BB303E, `blue.night` #4273BD.
  Referenced only by L2. Banned: component-flavoured naming — one value, many roles.
- **L2 Semantic** — role names: `surface.canvas`, `surface.raised`, `surface.overlay`,
  `surface.inset`, `surface.hover`, `surface.selected`, `border.subtle`, `border.strong`,
  `border.focus`, `accent.action`, `accent.onAction`, `accent.subtle`, `accent.link`,
  `text.primary`, `text.secondary`, `text.tertiary`, `text.disabled`, `status.success`,
  `status.warning`, `status.danger`, `status.info` (each status pairing colour + wash). The only
  layer a component may consume. Derived washes are computed mixes of a status primitive with the
  canvas (20% colour / 80% canvas light; 55% colour / 45% canvas dark), not stored literals.
- **L3 Component** — only for deliberate deviation; points at L2 or L1, never a raw value, never a
  sibling component's token. Examples: `record-id.chip.typeface` → the mono family primitive;
  `toast.bar.accent` → `status.*`; `table.header.fill` → `surface.inset`; `picker.segment.fill` →
  `status.info`.

**Rules.** Every token has a determinable type or it is invalid; names case-sensitive, free of
`$`, `{`, `}`, `.`; no circular references — a loop is an authoring error and must fail the build.
Every semantic token carries a value in **every** shipped mode: the map in §3 is complete in both
light and dark, so a role with no dark value fails loudly instead of silently resolving. The one
deliberate single-mode role is `accent.link` (light-only; dark links render as `text.primary`
with underline — see §10). Animatable tokens (the four durations, the loader rotation) are
registered custom properties with explicit syntax and inheritance declarations; percentage and
relative units are illegal as their initial values.

**Layer order (low → high):** reset → primitives → semantic → component → utilities. Layer order
beats specificity entirely, and a stray un-layered declaration would outrank this whole system —
anything a consumer must override without forcing sits in the utilities layer at the top. (The
product's own theme override hook — repointing the primary-colour custom property at the root —
works because it targets the primitive layer before semantic resolution.)

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` / `surface.raised` / `surface.overlay` / `surface.inset` | #FFFFFF / #FFFFFF / #FFFFFF / #F8F9FA | #1B1B1B / #2B2B2B / #363636 / #202020 | canvas · panels & records grid · menus, dialogs, tooltips · sidebar, wells, table header band |
| `surface.hover` / `surface.selected` | #F8F9FA / #E4E8EC | #202020 / #2B2B2B | row and sidebar item fills; selection also keeps a filled icon + ink text — never colour alone |
| `border.subtle` / `border.strong` / `border.focus` | #E4E8EC / #687278 / #1055C9 | #2B2B2B / #8D8D8D / #EBEBEB | 1px hairlines; subtle is decorative-only (1.423:1); strong carries SC 1.4.11 boundaries; focus ≥3:1 in both modes |
| `accent.action` / `accent.onAction` / `accent.subtle` | #25272D / #FFFFFF / #E4E8EC | #3B3B3B / #EBEBEB / #2B2B2B | the charcoal primary fill (one per viewport) · its label · secondary button fill (ink label) |
| `accent.link` (light-only) / `accent.marketing` (marketing-only) | #1055C9 / #B2D5E1 | — / #B2D5E1 | links at 6.635:1; dark links render as `text.primary` + underline; marketing canvas never carries white text (1.556:1) |
| `text.primary` / `text.secondary` / `text.tertiary` / `text.disabled` | #25272D / #687278 / #A2A9AE / #A2A9AE | #EBEBEB / #8D8D8D / #646464 / #646464 | ink ramp; two readable inks only — tertiary is the non-essential grey (N/A cells, disabled); no third readable tier |
| `status.success` (fg + wash) | #22A96D on #D3EEE2 | #27865D on #22563F | glyph = check; chip/toast text is always ink, not the status colour |
| `status.warning` (fg + wash) | #E57534 on #FAE3D6 | #CF4E17 on #7E3719 | glyph = triangle |
| `status.danger` (fg + wash) | #C33751 on #F3D7DC | #BB303E on #73272E | glyph = alert |
| `status.info` (fg + wash) | #3376E5 on #D6E4FA | #4273BD on #304B74 | glyph = info; also the datetime-picker segment fill |

Dark canvas is **not** pure black: #1B1B1B, stepping +2/+7/+12/+14/+16% white to #202020, #2B2B2B,
#363636, #3B3B3B, #3F3F3F. Depth in dark comes from these surface steps and 1px strokes, never
shadows; the stock dark selection blend #4D4D4D (2.038:1) is superseded by `surface.selected`
+ weight.

**Contrast gate — computed, unrounded.** Body ≥4.5:1; large text (≥24px or ≥18.5px bold) and UI
boundaries/focus ≥3:1 (WCAG 2.2, SC 1.4.3 / 1.4.11).

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| text.primary (L) | #25272D | surface.canvas (L) | #FFFFFF | 14.928:1 | 4.5 | PASS |
| text.secondary (L) | #687278 | surface.canvas (L) | #FFFFFF | 4.922:1 | 4.5 | PASS |
| text.secondary (L) | #687278 | surface.inset (L) | #F8F9FA | 4.669:1 | 4.5 | PASS |
| text.tertiary (L) | #A2A9AE | surface.canvas (L) | #FFFFFF | 2.380:1 | 3 (house floor) | RESTRICTED — non-essential values only (N/A cells, disabled); readable metadata uses secondary |
| text.disabled (L) | #A2A9AE | surface.canvas (L) | #FFFFFF | 2.380:1 | exempt | PASS — SC 1.4.3 exempts inactive UI; never for readable text |
| accent.onAction (L) | #FFFFFF | accent.action (L) | #25272D | 14.928:1 | 4.5 | PASS |
| text.primary on secondary fill (L) | #25272D | accent.subtle (L) | #E4E8EC | 12.122:1 | 4.5 | PASS |
| border.strong (L) | #687278 | surface.canvas (L) | #FFFFFF | 4.922:1 | 3 | PASS |
| border.focus (L) | #1055C9 | surface.canvas (L) | #FFFFFF | 6.635:1 | 3 | PASS |
| status.success ink (L) | #25272D | success wash (L) | #D3EEE2 | 12.154:1 | 4.5 | PASS |
| status.warning ink (L) | #25272D | warning wash (L) | #FAE3D6 | 12.101:1 | 4.5 | PASS |
| status.danger ink (L) | #25272D | danger wash (L) | #F3D7DC | 11.064:1 | 4.5 | PASS |
| status.info ink (L) | #25272D | info wash (L) | #D6E4FA | 11.613:1 | 4.5 | PASS |
| text.primary (D) | #EBEBEB | surface.canvas (D) | #1B1B1B | 14.448:1 | 4.5 | PASS |
| text.secondary (D) | #8D8D8D | surface.canvas (D) | #1B1B1B | 5.190:1 | 4.5 | PASS |
| text.secondary (D) | #8D8D8D | surface.raised (D) | #2B2B2B | 4.266:1 | 4.5 | RESTRICTED — hint text never set on raised steps; steps up to primary there |
| text.disabled (D) | #646464 | surface.canvas (D) | #1B1B1B | 2.911:1 | exempt | PASS — inactive UI exemption, as light |
| accent.onAction (D) | #EBEBEB | accent.action (D) | #3B3B3B | 9.396:1 | 4.5 | PASS |
| border.strong (D) | #8D8D8D | surface.raised (D) | #2B2B2B | 4.266:1 | 3 | PASS |
| border.focus (D) | #EBEBEB | surface.canvas (D) | #1B1B1B | 14.448:1 | 3 | PASS |
| status.success ink (D) | #EBEBEB | success wash (D) | #22563F | 7.129:1 | 4.5 | PASS |
| status.warning ink (D) | #EBEBEB | warning wash (D) | #7E3719 | 7.197:1 | 4.5 | PASS |
| status.danger ink (D) | #EBEBEB | danger wash (D) | #73272E | 8.557:1 | 4.5 | PASS |
| status.info ink (D) | #EBEBEB | info wash (D) | #304B74 | 7.388:1 | 4.5 | PASS |
| onAction on info fill | #FFFFFF | status.info fill | #3376E5 | 4.318:1 | 4.5 | RESTRICTED — passes 3:1 as UI component/large text; body-size text uses wash+ink instead |
| onAction on success fill | #FFFFFF | status.success fill | #22A96D | 3.015:1 | 3 (UI component) | RESTRICTED — same rule |
| onAction on warning fill | #FFFFFF | status.warning fill | #E57534 | 3.032:1 | 3 (UI component) | RESTRICTED — same rule |
| onAction on danger fill | #FFFFFF | status.danger fill | #C33751 | 5.269:1 | 4.5 | PASS |
| marketing ink on brand canvas | #25272D | accent.marketing | #B2D5E1 | 9.595:1 | 4.5 | PASS |

Rejected pairings recorded so they are never re-proposed: the stock focus ring (25% slate over
white ≈ #D1D6DC) at 1.462:1 on canvas — fails SC 2.4.7/1.4.11 expectations, superseded by
`border.focus`; the stock dark selection blend #4D4D4D at 2.038:1; status-coloured icons on their
own washes — success 2.455:1, warning 2.458:1, dark success 1.884:1, dark warning 1.943:1, dark
danger 1.751:1 — icons always ride beside ink labels and are never the sole signal; body-size
white text on success/warning/info fills (3.015/3.032/4.318:1, all under 4.5) — status buttons
either use ink-on-wash or restrict white to UI-component/large-text contexts; white text on the
marketing blue canvas (1.556:1) — the canvas takes ink only.

## 4. Typography

**Families.** UI: **IBM Plex Sans** (400 regular, 600 semibold; regular/semibold italics also
ship), self-hosted WOFF2 with latin-ext/cyrillic subsets, loaded with block display, fallback
system-ui, sans-serif, emoji. A global 0.004em letter-spacing normalises Plex rendering between
browser engines. Numeric/code: **IBM Plex Mono** (400, 600), self-hosted WOFF2, swap display,
fallback ui-monospace, monospace, emoji — for record ids, filter expressions, API rules, JSON
previews, log lines, file keys, raw timestamps. *Monospace is for identifiers and code, never a
costume.* Only two weights exist: anything authored at 500 renders as a synthesised faux-weight
and is banned.

**One ramp table per class, not one blended table.**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| **[F] Focused, 15px base — auth/installer, settings detail** | | | | | | |
| Title | 18px | 400 | 24px | 0 | default | auth card heading (the source h5 tier) |
| Section title | 16px | 600 | 24px | 0 | default | card titles on auth/settings |
| Body | 15px | 400 | 24px | 0.004em global | default | installer/auth prose |
| Label | 14px | 600 | 22px | 0 | default | field labels, checkbox labels |
| Meta | 13px | 400 | 16px | 0 | tabular | helper text under fields |
| **[S] Standard, 14px base — dashboard, settings, docs** | | | | | | |
| Page title | 26px | 400 | 32px | 0 | default | view headings (h1 tier) |
| Section title | 22px | 400 | 28px | 0 | default | panel headings (h3 tier) |
| Body | 14px | 400 | 22px | 0.004em global | default | descriptive prose, settings copy |
| Row primary | 14px | 400 (600 selected) | 22px | 0 | tabular | records grid primary cell |
| Row secondary | 13px | 400 | 16px | 0 | tabular | sub-cell, expanded summary |
| Stat value | 18px | 600 | 24px | 0 | tabular | dashboard counters |
| Meta | 13px | 400 | 16px | 0 | tabular | timestamps, "N/A" cells at tertiary ink |
| **[D] Dense, 13px base — logs, large grids** | | | | | | |
| Grid header | 13px | 600 | 16px | 0 | default | column headings (normal case, with type icon) |
| Grid cell text | 13px | 400 | 16px | 0 | default | dense cell values |
| Grid cell numeric | 13px | 400 | 16px | 0 | tabular | counts, sizes |
| Identifier | 13px | 400 (IBM Plex Mono) | 16px | 0 | tabular | record id chips, file keys |
| Log line | 13px | 400 (IBM Plex Mono) | 16px | 0 | tabular | logs viewer lines |
| Inline help | 12px | 400 | 16px | 0 | default | hint text under grids |

Prose inside a dense screen (empty-state copy, explainer paragraphs) still steps up to 14/22
Standard body — density never shrinks prose below 13px.

**Invariants.** Tabular numerals on every comparable value — record counts, log timestamps, file
sizes, request counts, ids. Right-align numerics, left-align text, never centre a numeric column.
Fixed stepped sizes only (14/13/15 + the heading tier); no fluid scaling between steps. Measure
≤80 characters: docs prose and settings copy target 65–80ch (the 840px wrapper enforces it);
records grids are unconstrained.

## 5. Spacing Scale & Density Scales

**Spacing base: 4px grid; the shipped scale is coarse by design.** `space.0` 0 · `space.1` 4px
icon-to-label gap · `space.2` 8px chip padding, icon gaps · `space.3` 13px input/control padding
(the source input padding — deliberately between steps, kept verbatim) · `space.4` 16px card
padding [D] · `space.5` 20px compact section gap, mobile page gutter · `space.6` 30px page
gutter and section gap [S/F] (the source spacing unit) · `space.8` 40px modal padding ·
`space.12` 60px auth-card breathing room. Wrapper widths: 430px small, 840px standard (docs
prose), 1150px wide tables. *No 17px. No 23px. If a layout needs an off-scale value, the layout
is wrong.*

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 15px | 13px | 30px | auth/installer, settings detail, docs prose |
| `standard` | 44px (sampled 46px) | 14px | 13px | 30px | collections dashboard, record editor, settings |
| `dense` | 32px | 13px | 8px | 20px | logs viewer, large record grids, backup tables |

- Density comes from row height, column pruning and leading — never from type too small to read.
  A 13px mono id chip in the records grid is correct; the same size for the settings-page intro
  paragraph is a defect.
- **Never switch mid-page.** The records grid is standard edge to edge; the logs viewer is dense
  edge to edge. Switching across routes with different jobs is legitimate and should feel like a
  different room.
- **Chrome follows rows.** Toolbar, bulk bar and pagination heights match the grid's row height
  (44/44/44 standard, 32/32/32 dense); the 45px control height is the standard-mode chrome
  rhythm. A 45px toolbar over 32px log rows is a rhythm break.
- Under 900px the shipped UI rescales spacing (30→20px, 20→15px) and control heights (45→40px);
  this spec carries those exact values as the compact-density axis rather than a viewport rule.
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40% (house heuristic; the
  sampled records grid measures ~45%, the docs page ~50%).

## 6. Radius Scale

`none` 0 table cells, log lines, code blocks in the logs viewer · `sm` 5px — every control,
button, input, chip, inline code chip, toast, dropdown, segment (the source's single control
radius) · `lg` 15px — large panels, auth cards, modals on marketing-scale viewports (the source's
large radius) · `full` 9999px — avatars, toggle tracks, pills. **One radius per component
family**: controls are all 5px, large surfaces all 15px, never mixed ad-hoc. Nested radii obey
`radius_inner = radius_outer − padding`: a 15px modal with 40px padding carries 0px inner blocks
unless they are themselves 5px controls; a 5px chip inside a 5px input keeps 5px at the shared
edge only when the padding is 0.

## 7. Elevation

**One strategy per mode, never mixed.** Light uses a single soft ambient shadow plus
scroll-edge shadows on sticky containers; dark uses surface-luminance steps and keylines.

| Level | Light | Dark |
|---|---|---|
| 0 canvas | #FFFFFF, no shadow | #1B1B1B, no shadow |
| 1 card/panel | shadow 0 8px 5px -5px rgba(34,36,36,0.10) + 1px `border.subtle` | one surface step up (#2B2B2B) + 1px `border.subtle` |
| 2 sticky header/toolbar | level-1 shadow; while content scrolls beneath, scroll-edge shadow 0 2px 8px 1px rgba(34,36,36,0.15) (bottom: 0 -2px 8px 1px) | surface step + 1px `border.strong` bottom keyline (scroll state flips the keyline on, not a bigger shadow) |
| 3 overlay (dropdown, popover, toast) | level-1 shadow; side scroll-edges 3px 0 5px / -3px 0 5px at 0.2 | #363636 + 1px `border.strong` |
| 4 dialog | level-3 shadow + scrim rgba(70,90,115,0.25) | #2B2B2B + scrim rgba(18,18,18,0.5) + 1px `border.strong` |

The scroll-edge shadow is a signature move: sticky sidebars and headers reveal a directional
hairline shadow only when their content actually overflows, via scroll-state container queries —
static chrome stays shadowless. Dark keeps the same soft shadows at 0.3–0.45 alpha for overlays
(the source darkens rather than deletes them) but the ramp, not the shadow, is the primary depth
carrier; a tooltip surfaces as translucent #161616-equivalent at 0.9 alpha over content.

## 8. Motion

`instant` 0ms · `fast` 70ms (press/active feedback — the source active speed) · `base` 150ms
(hover fills, dropdown open, toast entrance — translateY(10px)→0 with fade, decelerate) ·
`slow` 200ms (modal entrance, sidebar slide, accordion expand — decelerate) · loader 1.1s linear
rotation (spinner glyph in buttons and loading blocks).

- Entrances decelerate, exits accelerate. The toast entrance is the canonical curve; its exit
  quickens, it does not reverse the same easing. A symmetric ease-in-out on both directions is a
  defect.
- Animate transform and opacity only — never width, height, top, left. Accordion expand animates
  a grid-track/opacity pair, not a measured height; hover is a background token swap, not a
  height animation.
- No bounce on irreversible moments: delete-collection confirm, superuser delete, migration apply
  land with a straight decelerate and no overshoot.
- Reduced motion is a real variant, not a blanket off-switch: authored movement (toast slide,
  modal pop, sidebar slide) crossfades under ~150ms; the 1.1s loader spin swaps to a two-frame
  opacity pulse — it is a status indicator and must stay perceivable, but the rotation (a large
  continuously panning element) is exactly the vestibular trigger to neutralise.

## 9. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell (top bar + sidebar) | S | expanded · compact (<900px) | hover, active collection, scrolled (edge shadow), busy | tab order, arrows within collections list | sidebar search placeholder "Search collections…" names scope |
| Collections sidebar group | S | user collections · system group (collapsed) | hover, selected (#E4E8EC + filled icon), dragging, empty | arrows move, Enter opens | system group collapsed by default; "+ New collection" is the fixing CTA |
| Data table (records grid) | S/D | standard grid · dense grid | hover, selected row, loading skeleton, empty, error, offline-stale | arrows move cells, space selects, Enter expands | id chip in mono; empty state: "No records yet" + "New record" |
| Filter/search bar | S/D | free-text term · filter expression | drafting, applied, invalid (inline reason), cleared | Enter applies, Esc clears | placeholder "Search term or filter…"; expression renders in mono |
| Record editor (panel) | S | create · edit · readonly | open, saving, dirty (unsaved dot), invalid field, error | Esc closes (confirm on dirty), tab traverses fields | title "Edit posts record" names the collection; required fields carry the asterisk + reason |
| Bulk bar | S/D | selection actions | appears on select, busy, blocked (count 0) | Enter confirms, Esc deselects | verb + count: "Delete 3 records" — never colour alone |
| Row action menu | S | single-row · batch | open, focus-trapped, item disabled with reason | Esc closes, arrows navigate | verbs only: "Duplicate", "Delete…" |
| Settings accordion | F/S | collapsed group · expanded | open, saving, error, blocked | Enter toggles, arrows between headers | header names the setting; save is per-panel, disabled until dirty with reason on focus |
| API rules field (mono editor) | S | per-action rule | empty (inherits lockless default), valid, invalid (inline), superusers-only | tab in, Esc out | placeholder states the default; "Set superusers only" is a named toggle, not an icon |
| Toast | S | info · success · warning · danger | entering, persisting, dismissing | Esc dismisses, focus on action | icon strip in status colour + ink message; message names what happened, link names the fix |
| Dialog (create/edit collection) | F/S | create · edit · confirm-destructive | open, submitting, invalid tab, blocked | focus trap, Esc = cancel (destructive requires typing) | destructive names the object: 'Delete collection "posts"?' |
| Datetime picker | S | date grid · time segments | open, selected (blue segment), cleared, disabled | arrows move days, Enter selects | "Clear" and "Today" as named text links |
| Member row (superusers) | S | owner · invited · disabled | hover, removing, pending | row menu via kebab | role named in text; removal confirms with the email |
| Log entry (logs viewer) | D | by level (info/warning/error) | expanded (inline JSON in mono), filtered-out, error-flagged | Enter expands | level glyph + timestamp + message; error rows carry the wash, never colour alone |
| Docs header search | F | site scope | closed, open, no results, searching | global focus, arrows, Enter | placeholder "Search…" states the site scope |

**Every fetching surface also designs:** loading (skeleton rows matching the final 44/32px
geometry with the 1.1s loader reserved in the toolbar — never a centred spinner on a blank page),
empty (names what is missing plus the CTA that fixes it: "No collections yet — New collection"),
error (what happened + the failed request + Retry), offline/stale (cached list greyed with a
banner "Offline — showing cached data"; realtime subscriptions resume automatically on reconnect,
which is the product's own superpower and must be visible: a reconnection toast, not silent
healing).

**Contracts this table encodes:** one charcoal primary fill per view (dense toolbars may run the
primary plus icon actions); every icon-only control carries a tooltip or visible label (the kebab
says "More"); a disabled control states *why* on focus or hover ("Read-only superuser"); a button
never changes width between idle and loading — the spinner reserves the label's space; destructive
actions always confirm in a real dialog naming the object.

## 10. Light / Dark Strategy

- **Posture: C dual-parity.** The admin UI ships both modes with equal completeness (the source
  defines a full dark remap under the root scheme marker); light is the default. The marketing
  site is light-only by design — its blue canvas is the brand's daylight signature.
- **Mechanism:** semantic roles remapped per mode via the root scheme attribute; **no role absent
  in either mode** except `accent.link`, which is light-only by decision: dark links render as
  `text.primary` with underline because the source's unremapped accent blue would fail contrast
  on #1B1B1B — and colour is never the only link affordance.
- **`color-scheme`** is set at the root so UA chrome, form controls and scrollbars follow the
  mode.
- **The scheme meta tag** is declared in the head before any stylesheet to prevent a flash of the
  wrong scheme.
- **Dark is authored, not inverted:** its own five-step ramp (#1B1B1B → #3F3F3F), its own border
  strength (decorative hairlines #2B2B2B; meaningful boundaries #8D8D8D — a hairline that reads as
  delicate on white reads as invisible on near-black), its own status set (six darkened status
  primitives), its own scrim. `light-dark()` notation is progressive enhancement only, never the
  mechanism.
- Org-tinting is a real, shipped capability: the product honours a root-level override of the
  primary-colour custom property (documented for brand theming). It changes colour tokens only —
  radii, type sizes, spacing and layout are frozen so a theme swap cannot move anything. The
  override re-points the L1 primitive; every L2 semantic resolves through it unchanged.

## 11. Density-Mode Strategy

- **Default mode per surface class:** Focused for auth/installer and settings detail; Standard
  for the collections dashboard, record editor and docs; Dense for the logs viewer and large
  record grids. The boundary is the job: configuring and reading = Standard/Focused; scanning
  and comparing many rows = Dense.
- **Mechanism:** a density marker at the application root rescales row height, cell padding,
  gutter and base body size together as one token axis — the source's own compact values
  (30→20px spacing, 45→40px controls, 14→13px type) are the dense stop. Spacing tokens do not
  change with screen size; density is not a media query.
- **Container queries for reflow:** a panel reflows to its container, not the viewport; size
  queries fail closed with no eligible container, and container units silently resolve to
  small-viewport units there — so container units are never used where that fallback would be
  wrong. The scroll-edge shadows already run on scroll-state container queries, so the mechanism
  is native to this system.
- **Style queries** compare computed values, so the density marker is registered with an explicit
  syntax and inheritance declaration before any style query reads it.
- **The switch is offered as an accessibility affordance**, not a preference: the W3C note on
  SC 2.5.8 endorses "a mechanism to control the density of layout" for users with visual field
  loss. Dense is the default only on data surfaces; every data surface exposes the switch back to
  Standard.

## 12. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum. AAA where cheap: 7:1 on body prose in Focused surfaces
  (14.928:1 available); SC 2.4.11 focus-not-obscured under all sticky chrome (the scroll-edge
  shadow pattern keeps the focused row visible by construction).
- **Target size:** ≥24×24 CSS px hard minimum (the 24px-diameter circle exception respected);
  45px controls and 44px rows exceed it; 32px dense rows keep full-width hit targets with ≥8px
  separation. Zoom does not excuse target size.
- **Keyboard:** every function operable without a pointer (SC 2.1.1); Esc closes menus, dialogs
  and the record panel (with confirm on dirty state); focus is trapped in dialogs and returned on
  close. **Focus indicator:** the stock 2px dotted 25%-slate ring (1.462:1 on white) is replaced
  by a 2px solid `border.focus` ring at 2px offset — 6.635:1 light, 14.448:1 dark — never
  suppressed without an equal or stronger replacement.
- **Contrast:** text ≥4.5:1 (computed in the §3 gate); boundaries and focus ≥3:1. **Colour
  independence:** every status pairs colour with a glyph and ink text (True/False chips carry the
  word); selection adds a filled icon + weight; log levels carry the glyph even when filtered.
- **Motion:** the §8 reduced-motion variant applies per component; the loader spin swaps to an
  opacity pulse.
- **Text:** ≤80-character measure on prose (the 840px wrapper), 1.5+ leading (22/14 ≈ 1.57),
  200% resize without horizontal scroll — grids honour it via column wrap, not clipping.
- **Semantics:** real interactive elements with correct roles; the records grid exposes
  row/column semantics; toasts announce politely (a live region); loading grids set a busy marker;
  the record panel moves focus in on open and restores it on close.
- **Contrast preference:** if `prefers-contrast: more` is honoured, text.secondary → text.primary,
  decorative hairlines step up to `border.strong`, and the focus ring thickens to 3px. Values
  honoured: `no-preference`, `more`.

## 13. Anti-Patterns

**Do**
- Put every primary action in charcoal and let blue mean information — the monochrome-primary
  split is the whole grammar of the v0.37 UI; one filled CTA per view.
- Render record ids, filter expressions, API rules and log lines in IBM Plex Mono — they are the
  payload of a backend console, and the chip treatment (grey fill, 5px radius) keeps them
  scannable.
- Pair status washes with ink text and a status-coloured glyph — the toast's icon-strip pattern —
  never status-coloured body text.
- Keep the two-weight discipline: 400 for everything, 600 for emphasis and labels; hierarchy by
  size, not boldness.
- Use the scroll-edge shadow pattern on every sticky container so depth appears only when content
  actually scrolls.
- Build skeletons at the exact final row geometry (44px standard / 32px dense) before data
  arrives.
- Give every empty state a named CTA ("New collection", "New record", "Import collection").
- Keep the sidebar at 240px on #F8F9FA with the 1px #E4E8EC divider — it is the only inset zone
  in the shell; wells and table header bands share its step.
- Right-align and tabulate every numeric column; ids and timestamps render in mono chips.
- Expose the density switch on data surfaces as an accessibility affordance, with the shipped
  compact values as the dense stop.
- Honour the root primary-colour override for org theming — colour tokens only, geometry frozen.
- Match toolbar, bulk-bar and pagination heights to the grid's row height.

**Don't**
- No blue primary buttons — blue is info/link/picker territory; a blue "Save" would re-shuffle the
  entire grammar the v0.37 rework established.
- No white text at body size on success/warning/info fills (3.015/3.032/4.318:1 — all fail 4.5);
  use ink-on-wash chips or restrict white to UI-component/large-text contexts.
- No status-coloured icons as the sole signal — success/warning icons on their washes measure
  1.884–2.458:1; the glyph always rides with a word.
- No pure-black dark canvas (#000000 appears nowhere; wells bottom out at #1B1B1B).
- No third font weight — 500 renders as a synthesised faux-weight on a two-weight family.
- No marketing blue canvas, contour pattern, gopher mascot or hero type inside the product shell —
  the poster stays above the workbench.
- No gradients or drop shadows heavier than the single 0.10-alpha ambient layer; depth is fills,
  steps and hairlines.
- No hover-only affordances; everything reachable by pointer is reachable by keyboard with a
  visible (≥3:1) focus ring — the stock dotted 25%-slate ring is banned (1.462:1).
- No placeholder-as-label on API rules, filter expressions or schema fields — persistent labels,
  because the values are code.
- No whole-page spinners; the shell stays put while the region skeleton loads.
- No blocking browser dialogs; delete-collection is a real dialog that names the object and makes
  you type.
- No tiny type as a density strategy — density comes from rows and padding; prose never drops
  below 13px, and hint text never lands on raised steps in dark (4.266:1 there).
- No mid-page density switches; the logs viewer is dense edge to edge or it is wrong.

## 14. Quick Reference & Verification Gate

**Colour (role → light / dark):** canvas #FFFFFF / #1B1B1B · raised #FFFFFF / #2B2B2B · overlay
#FFFFFF / #363636 · inset #F8F9FA / #202020 · hover #F8F9FA / #202020 · selected #E4E8EC /
#2B2B2B · border subtle #E4E8EC / #2B2B2B · border strong #687278 / #8D8D8D · border focus
#1055C9 / #EBEBEB · accent action #25272D / #3B3B3B · onAction #FFFFFF / #EBEBEB · accent subtle
#E4E8EC / #2B2B2B · link #1055C9 / primary+underline · marketing canvas #B2D5E1 · text primary
#25272D / #EBEBEB · secondary #687278 / #8D8D8D · tertiary+disabled #A2A9AE / #646464 · success
#22A96D on #D3EEE2 / #27865D on #22563F · warning #E57534 on #FAE3D6 / #CF4E17 on #7E3719 ·
danger #C33751 on #F3D7DC / #BB303E on #73272E · info #3376E5 on #D6E4FA / #4273BD on #304B74 ·
scrim rgba(70,90,115,0.25) / rgba(18,18,18,0.5).

**Type ramp:** IBM Plex Sans 26/32 Page title · 22/28 Section title · 18/24 [F] Title, Stat
value · 16/24 [F] Section title · 15/24 [F] Body · 14/22 Body, Row primary, [F] Label · 13/16 Row
secondary, Meta, [D] grid cells, Identifier, Log line (mono), Inline help at 12/16. IBM Plex Mono
400/600 for ids, rules, expressions, logs.

**Spacing + radius:** 4 / 8 / 13 / 16 / 20 / 30 / 40 / 60 · radius 0 / 5 / 15 / full · rows 44px
S, 32px D · gutters 30 S/F, 20 D · wrappers 430 / 840 / 1150 · sidebar 240px · controls 45/52/35.

**Component → token map:** Data table consumes surface.canvas, surface.inset (header band),
surface.hover/selected, border.subtle, text.primary/secondary, the mono identifier primitive,
radius.none, level-0. Record editor consumes surface.raised, level-1, radius.lg, text.primary,
status.danger (required/invalid), border.focus. Toast consumes the status wash + ink + status
glyph, radius.sm, level-3. Sidebar consumes surface.inset, border.subtle, surface.hover/selected,
text.primary/secondary. Datetime picker consumes status.info fill (white labels at ≥3:1
UI-component sizes), surface.overlay, radius.sm, border.focus. Dialog consumes surface.overlay
(#2B2B2B dark), level-4 + scrim, radius.lg, accent.action confirm. Filter bar consumes
surface.canvas input fill (grey.90), border.strong, mono expression text.

**Pre-ship checklist.**
1. Zero raw hex outside L1.
2. No token resolves to a component name.
3. Every contrast pairing computed, passing, unrounded (§3 gate is the source of truth).
4. Every semantic role has a value in both shipped modes (accent.link's light-only status is
   documented, not silent).
5. Every fetching surface has loading/empty/error/offline specified.
6. Every component row lists disabled and loading states.
7. Row, header, toolbar and pagination heights agree (44/44/44 or 32/32/32).
8. Reduced-motion variant written for every authored motion, including the loader spin.
9. Every control keyboard-reachable with the ≥3:1 focus ring (the stock dotted ring is banned).
10. Dark authored, not filtered, with meaningful border strength (#8D8D8D) exceeding the
    decorative hairline's.
11. No unoverridden stock default inside a committed surface (the dotted focus ring, 500-weight
    synthesis and white-on-status body text are the usual survivors).
12. Nothing came from a marketing page — the blue canvas, contour pattern and mascot stay on
    pocketbase.io; the console runs on ink and paper.
