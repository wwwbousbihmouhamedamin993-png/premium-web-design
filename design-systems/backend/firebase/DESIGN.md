# Design System — Firebase

<!-- premium-web-design:design-system 1 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: Firebase brand guidelines, firebase.google.com/brand-guidelines (colour + logo rules — ladder rung 2, public documentation); sampled pixels of verified console captures in screens/ (density, accent scarcity, shell greys — rungs 1-3); Google Material Design + Google Cloud console shell (type, elevation, component posture — rung 2) -->
<!-- Surface classes: 6 routes classified; density classes F/S/D assigned -->

## 1. Design Posture & Atmosphere

Firebase's product surface is Google's grey instrument shell wearing one flame. The console
(console.firebase.google.com) is a Material-Density workbench: white panels on a cool grey chrome,
hairline dividers, a calm blue that carries every action, and a strict scarcity of amber. The brand
yellow-orange-red exists only at the edges — the flame mark, product-icon circles, chart series,
plan badges — so that after eight hours of reading Firestore documents or scrolling Functions logs
the eye is never scorched; warmth signals identity, not interactivity. The emotional register is
"trustworthy infrastructure": quiet, engineered, exhaustedly neutral, closer to a flight deck than
a dashboard.

Against its category (Supabase's dark neon studio, PlanetScale's slate console, Appwrite's violet
marketing shell), Firebase sits deliberately oldest and calmest: light-first, grey-first, type at
14px, rows at 40px, and density pushed further down (32px) only where data genuinely warrants it.
The single visual metaphor is an **instrument panel with a pilot's badge**: uniform chrome that
recedes, labelled switches that never surprise, and exactly one brand insignia per viewport — the
flame — placed like a tail-fin, never like a button.

Marketing surfaces (homepage, pricing) invert the register: near-black canvas sampled at #1E1E1E,
generous 32/40 display type in Google Sans, one orange fill for the primary call to action. That
dark register is authored here as the dark mode of the same token system, so the console and the
marketing shell share one ramp — the brand grey scale — with no inversion shortcuts.

**Key Characteristics**
- Depth is hairlines first: 1px dividers at #E0E0E0 on light, #5F6368 on dark; shadows only in light
  mode, two-layer Google-style ambient pairs, never heavier than level 3.
- One accent fill per viewport: a single blue filled call to action (#1A73E8 light / #8AB4F8 dark);
  amber (#FFC400) is never an action colour — it marks identity, plan badges and chart series only.
- Rows are 40px in Standard surfaces, 32px in Dense data grids (sampled 34px pitch in the Firestore
  document list); toolbar, header and pagination heights match the row height exactly.
- Canvas is white panels floating on a grey #F5F5F5 chrome; the grey is `surface.inset`, not canvas.
- Three typefaces, three jobs: Google Sans (display, page titles), Roboto (all UI text, 14px base),
  Roboto Mono (document IDs, collection paths, query strings, log lines).
- Every comparable value is tabular: counts, timestamps, usage deltas, quota bars, invoice rows.
- Status colour never travels alone: a glyph, a shape or a signed delta rides with green, amber,
  red and blue alike.
- Radius is disciplined: 4px controls, 8px cards and dialogs, 9999px pills and product-icon circles.
- Amber identity on light backgrounds is text-safe only in darkened form (#8F5300 for headings);
  raw #FFC400 appears as fill, never as text on white.
- Brand-blue heritage surfaces (#039BE5, sampled on the pricing "No-cost" card) carry white text at
  large sizes only; normal-size text on that fill is forbidden.
- Dark mode is authored from the brand grey ramp (canvas #1F1F1F, raised #303030) with zero shadows.
- The product-icon system sits logos on amber or yellow circles over dark or neutral chrome — never
  more than one Firebase lockup in one place (brand rule).
- Density is a token axis, not a media query: one root marker rescales row height, cell padding,
  gutter and body size together.

## 2. Token Architecture

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by value: `brand.yellow` #FFC400, `brand.orange` #FF9100,
  `brand.red` #DD2C00, `grey.10` #1F1F1F … `grey.100` #FFFFFF, `blue.action` #1A73E8,
  `blue.heritage` #039BE5, `status.green.700`, `space.3`, `radius.md`, `duration.base`. Referenced
  only by L2. Banned: component-flavoured naming (`--card-bg`, `--tooltip-colour`) — one value,
  many roles.
- **L2 Semantic** — role names: `surface.canvas`, `surface.raised`, `text.primary`,
  `accent.action`, `status.error`. The only layer a component may consume.
- **L3 Component** — only for deliberate deviation; points at L2 or L1, never at a raw value, never
  at a sibling component's token. Examples: `data-grid.header.background` → `surface.inset`;
  `log-line.typeface` → the mono family primitive; `usage-tile.chart.series-2` → `brand.orange`.

**Rules.** Every token has a determinable type or it is invalid; names are case-sensitive and free
of `$`, `{`, `}` and `.` separators in the serialized registry; no circular references — a loop
`surface.inset → grey.95 → surface.inset` is an authoring error and must fail the build. Every
semantic token carries a value in **every** shipped mode: a role with no dark value resolves to its
light value and fails contrast, so the mode map below is complete by construction. Animatable
tokens (the four durations, the two scrim opacities) are registered with explicit syntax and
inheritance declarations; percentage and relative units are illegal as initial values there.

**Layer order (low → high):** reset → primitives → semantic → component → utilities. Layer order
beats specificity entirely, and an un-layered stray declaration would outrank this whole system —
anything a consumer must override without forcing sits in the utilities layer at the top.

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` / `surface.raised` / `surface.overlay` / `surface.inset` | #FFFFFF / #FFFFFF / #FFFFFF / #F5F5F5 | #1F1F1F / #303030 / #474747 / #161616 | canvas · cards & panels · menus & dialogs · chrome gutters, wells, table headers |
| `surface.hover` / `surface.selected` | #F1F3F4 / #E8EAED | #2A2A2A / #3C4043 | selection also carries a 3px left edge and 500 weight — never colour alone |
| `border.subtle` / `border.strong` / `border.focus` | #E0E0E0 / #5F6368 / #0B57D0 | #5F6368 / #C7C7C7 / #8AB4F8 | 1px hairlines; focus indicators ≥3:1 on both canvases |
| `accent.action` / `accent.onAction` / `accent.subtle` | #1A73E8 / #FFFFFF / #E8F0FE | #8AB4F8 / #202124 / #283A4E | one filled action per view; budget: 1 blue fill + ≤2 blue text links per viewport region |
| `accent.brand` (amber fill) / `accent.brandInk` | #FFC400 / #1F1F1F ink | #FFC400 / #1F1F1F ink | flame, product-icon circles, chart series 1, plan badge; never body text on light |
| `accent.brandDeep` (amber text on light) | #8F5300 | #FFC400 | identity headings on light chrome; normal-size safe |
| `accent.heritage` (brand surface blue) | #039BE5 | #039BE5 | large-fill marketing cards only; white text large-size only (3.077:1) |
| `text.primary` / `text.secondary` / `text.tertiary` / `text.disabled` | #202124 / #5F6368 / #757575 / #9AA0A6 | #F2F2F2 / #ABABAB / #8F8F8F / #5F6368 | ink ramp; disabled text is exempt from the 4.5 gate (inactive UI) but keeps ≥3:1 against its fill |
| `status.success` / `status.warning` / `status.error` / `status.info` (fg on wash) | #0D652D on #E6F4EA / #8A5300 on #FEF7E0 / #C5221F on #FCE8E6 / #0B57D0 on #E8F0FE | #5BB974 on #1E3327 / #FDD663 on #382C10 / #F28B82 on #3B1B1A / #8AB4F8 on #283A4E | each ships a glyph — check, triangle, alert, info — never colour alone |

Dark canvas is **not** pure black: #1F1F1F (brand Grey 10; homepage samples #1E1E1E), wells sink to
#161616, dialogs sit at #303030–#474747. Depth in dark comes from surface steps and 1px strokes,
never shadows.

**Contrast gate — computed, unrounded.** Body ≥4.5:1; large text (≥24px or ≥18.5px bold) ≥3:1; UI
boundaries and focus indicators ≥3:1 (WCAG 2.2, SC 1.4.3 / 1.4.11).

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| text.primary (L) | #202124 | surface.canvas (L) | #FFFFFF | 16.099:1 | 4.5 | PASS |
| text.secondary (L) | #5F6368 | surface.canvas (L) | #FFFFFF | 6.050:1 | 4.5 | PASS |
| text.tertiary (L) | #757575 | surface.canvas (L) | #FFFFFF | 4.608:1 | 4.5 | PASS |
| text.primary (D) | #F2F2F2 | surface.canvas (D) | #1F1F1F | 14.724:1 | 4.5 | PASS |
| text.secondary (D) | #ABABAB | surface.canvas (D) | #1F1F1F | 7.178:1 | 4.5 | PASS |
| text.tertiary (D) | #8F8F8F | surface.canvas (D) | #1F1F1F | 5.097:1 | 3 (house floor) | PASS |
| text.primary (D) | #F2F2F2 | surface.raised (D) | #303030 | 11.789:1 | 4.5 | PASS |
| text.secondary (D) | #ABABAB | surface.raised (D) | #303030 | 5.747:1 | 4.5 | PASS |
| accent.onAction (L) | #FFFFFF | accent.action (L) | #1A73E8 | 4.505:1 | 4.5 | PASS |
| accent.onAction (D) | #202124 | accent.action (D) | #8AB4F8 | 7.639:1 | 4.5 | PASS |
| accent.brandInk | #1F1F1F | accent.brand | #FFC400 | 10.320:1 | 4.5 | PASS |
| accent.brandDeep (L) | #8F5300 | surface.inset (L) | #F1F3F4 | 5.541:1 | 4.5 | PASS |
| border.strong (L) | #5F6368 | surface.raised (L) | #FFFFFF | 6.050:1 | 3 | PASS |
| border.strong (D) | #C7C7C7 | surface.raised (D) | #303030 | 7.807:1 | 3 | PASS |
| border.focus (L) | #0B57D0 | surface.canvas (L) | #FFFFFF | 6.386:1 | 3 | PASS |
| border.focus (D) | #8AB4F8 | surface.raised (D) | #303030 | 6.263:1 | 3 | PASS |
| status.success fg (L) | #0D652D | success wash (L) | #E6F4EA | 6.341:1 | 4.5 | PASS |
| status.warning fg (L) | #8A5300 | warning wash (L) | #FEF7E0 | 5.906:1 | 4.5 | PASS |
| status.error fg (L) | #C5221F | error wash (L) | #FCE8E6 | 4.920:1 | 4.5 | PASS |
| status.info fg (L) | #0B57D0 | info wash (L) | #E8F0FE | 5.573:1 | 4.5 | PASS |
| status.success fg (D) | #5BB974 | surface.raised (D) | #303030 | 5.428:1 | 4.5 | PASS |
| status.warning fg (D) | #FDD663 | surface.raised (D) | #303030 | 9.412:1 | 4.5 | PASS |
| status.error fg (D) | #F28B82 | surface.raised (D) | #303030 | 5.525:1 | 4.5 | PASS |
| onAction on heritage fill | #FFFFFF | accent.heritage | #039BE5 | 3.077:1 | 3 (large text only) | PASS — restricted: ≥24px or ≥18.5px bold |

Rejected pairings recorded so they are never re-proposed: white on `accent.heritage` at body size
(3.077:1, fails 4.5); raw `accent.brand` #FFC400 as text on white (1.54:1, fails everything — fill
only); the sampled marketing amber heading #D08828 on grey chrome (2.608:1, fails 3:1 even at
display size — use `accent.brandDeep` #8F5300); #039BE5 as a body-size text link on white (3.077:1
— links use `accent.action`); success #188038 on its wash (4.420:1, fails — superseded by #0D652D).

## 4. Typography

**Families.** UI: **Google Sans** (400/500/700) for display, page titles and stat values; **Roboto**
(400/500/700) for every other UI string. Served from Google Fonts static hosting as WOFF2, the four
core weights preloaded; fallback Roboto, Arial, sans-serif. Numeric/code: **Roboto Mono** (400/500)
for document IDs, collection and field paths, query previews, build hashes, raw timestamps and log
lines. *Monospace is for identifiers and code, never a costume* — prose never renders in Roboto Mono.

**One ramp table per class, not one blended table.**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| **[F] Focused, 16px base** | | | | | | |
| Display | 32px | 400 (Google Sans) | 40px | -0.25 | tabular | pricing hero, onboarding |
| Heading | 24px | 400 (Google Sans) | 32px | 0 | tabular | section openers |
| Body | 16px | 400 | 24px | 0 | default | reading prose, 1.5 leading |
| Label | 14px | 500 | 20px | 0.1 | default | form labels, card titles |
| Meta | 14px | 400 | 20px | 0 | tabular | dates, captions |
| **[S] Standard, 14px base** | | | | | | |
| Page title | 24px | 400 (Google Sans) | 32px | 0 | tabular | console page headers |
| Section title | 16px | 500 (Google Sans) | 24px | 0 | tabular | card titles, panel headers |
| Body | 14px | 400 | 20px | 0 | default | descriptive text |
| Row primary | 14px | 400 (500 selected) | 20px | 0 | tabular | table primary cell |
| Row secondary | 12px | 400 | 16px | 0 | tabular | sub-cell, email under name |
| Stat value | 24px | 400 (Google Sans) | 32px | 0 | tabular | usage figures |
| Stat label | 11px | 500 | 16px | 0.4 uppercase | default | tile captions |
| Meta | 12px | 400 | 16px | 0 | tabular | timestamps, quota notes |
| **[D] Dense, 13px base — data surfaces only** | | | | | | |
| Grid header | 12px | 500 | 16px | 0.2 uppercase | default | column headings |
| Grid cell numeric | 13px | 400 | 20px | 0 | tabular | counts, sizes, costs |
| Grid cell text | 13px | 400 | 20px | 0 | default | document field values |
| Log line | 12px | 400 (Roboto Mono) | 16px | 0 | tabular | Functions logs, query strings |
| Identifier | 13px | 400 (Roboto Mono) | 20px | 0 | tabular | doc IDs, collection paths |
| Inline help | 12px | 400 | 16px | 0 | default | hint text under grids |

Prose inside a dense screen (explainer paragraphs, empty-state copy) still steps up to 14/20
Standard body — density never shrinks prose below 13px.

**Invariants.** Tabular numerals on every comparable value — request counts, stored bytes, invoice
amounts, timestamps, deltas, document counts, user IDs. Right-align numerics, left-align text,
never centre a numeric column. Fixed stepped sizes only; no fluid scaling between steps. Measure
≤80 characters: 65–80ch in Focused/Standard prose; unconstrained in Dense grids.

## 5. Spacing Scale & Density Scales

**Spacing base: 4px grid; 8px comfortable in F/S, 4px in D.** `space.0` 0 · `space.1` 4px
icon-to-label gap · `space.2` 8px control padding [D], icon gaps [S] · `space.3` 12px cell padding
[S] · `space.4` 16px card padding [S], page gutter [D] · `space.6` 24px card padding [F], section
gap, page gutter [S] · `space.8` 32px section gap [S], page gutter [F] · `space.12` 48px region
separation · `space.16` 64px marketing regions only. *No 17px. No 23px. If a layout needs an
off-scale value, the layout is wrong.*

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | docs reading, pricing, onboarding, project creation |
| `standard` | 40px | 14px | 12–16px | 24px | project overview, Auth users, settings detail |
| `dense` | 32px | 13px | 8px | 16px | Firestore data viewer, Functions logs, usage/billing tables |

- Density comes from row height, column pruning and leading — never from type too small to read.
  A 13px tabular numeral in the Firestore grid is correct; the same numeral in the project-creation
  form is a defect. Sampled ground truth: 34px row pitch in the captured Firestore document list
  (32px row + hairline), 56px two-line menu items in the filter dialog.
- **Never switch mid-page.** The Firestore viewer is dense edge to edge; switching across routes
  with different jobs is legitimate and should feel like a different room.
- **Chrome follows rows.** Table toolbars, batch bars and pagination bars are 40px in Standard and
  32px in Dense — a 40px toolbar over 32px rows is a rhythm break. The global app bar (56px) and
  breadcrumb row (sampled ~58px, specified 56px) sit above table chrome and do not scale with it.
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40% (house heuristic, validated
  against the sampled captures: the console data viewer measures ~28% whitespace).

## 6. Radius Scale

`none` 0 table cells, log lines · `xs` 2px status dots, tag outlines · `sm` 4px buttons, inputs,
selects, chips, inline code chips · `md` 8px cards, panels, dialogs, menus, snackbars · `lg` 16px
marketing hero cards only · `full` 9999px pills, avatars, product-icon circles, toggle tracks.
**One radius per component family** — cards are all 8px, controls all 4px, never mixed ad-hoc.
Nested radii obey `radius_inner = radius_outer − padding`: an 8px card with 8px padding carries a
0px inner well; an 8px dialog with 16px padding carries 0px inner blocks unless they are themselves
4px controls.

## 7. Elevation

**One strategy per mode, never mixed.**

| Level | Light | Dark |
|---|---|---|
| 0 canvas | #FFFFFF, no shadow | #1F1F1F, no shadow |
| 1 card/panel | shadow 0 1px 2px rgba(60,64,67,0.30), 0 1px 3px rgba(60,64,67,0.15) + 1px `border.subtle` | one surface step up (#303030) + 1px `border.subtle` #5F6368 |
| 2 sticky header/toolbar | shadow 0 1px 2px rgba(60,64,67,0.30), 0 2px 6px 2px rgba(60,64,67,0.15) + `border.subtle` | #303030 + 1px `border.strong` bottom keyline |
| 3 overlay (menus, popovers) | shadow 0 1px 3px rgba(60,64,67,0.30), 0 4px 8px 3px rgba(60,64,67,0.15) | #474747 + 1px `border.strong` |
| 4 dialog | level-3 shadow + scrim rgba(32,33,36,0.50) | #303030 + scrim rgba(0,0,0,0.60) + 1px `border.strong` |

Dark uses **zero shadows** — a drop shadow is invisible on a near-black canvas; the sampled dark
pricing shell confirms fills, not shadows, carry depth.

## 8. Motion

`instant` 0ms · `fast` 120ms ease-out (Dense exits, row-action dismissal) · `base` 180ms
decelerate (Dense entrances, menu open, snackbar in) · `slow` 240–300ms decelerate (Focused/Standard
entrances, dialogs, drawer slide).

- Entrances decelerate, exits accelerate. A symmetric ease-in-out on both directions is a defect.
- Animate transform and opacity only — never width, height, top or left. Row hover is a background
  token swap, not a height animation.
- No bounce on irreversible moments: the delete-collection confirm, plan downgrade and project
  delete land with a straight decelerate and no overshoot.
- Reduced motion is a real variant, not a blanket off-switch: authored movement crossfades under
  ~150ms; the large chart draw-in and the hero parallax on marketing surfaces are what get
  neutralised (scaling and panning large objects are the vestibular triggers), not every fade.

## 9. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell/sidebar | S | rail (collapsed) · full nav | hover, active project, collapsed, busy | tab order, arrow moves between groups | project switcher names the live project |
| Data table (Firestore doc grid) | D | collection view · query result view | hover, selected (3px edge + weight), loading skeleton, empty, error | arrows move cells, space selects, Enter opens | "Add document" is the fixing CTA when empty |
| Filter/search bar (query builder) | D | one condition · multi-condition | drafting, applied (chip), invalid, cleared | Enter applies, Esc dismisses | query preview renders in mono; "Clear / Cancel / Apply" |
| Row action menu (kebab) | D/S | single-row · batch | open, focus-trapped, item disabled with reason | Esc closes, arrows navigate | verbs only: "Delete documents…" |
| Stat tile (usage) | S | single metric · sparkline pair | fresh, stale ("as of 2h ago"), quota exceeded | focusable as one unit | label names metric + window: "Reads · 30 days" |
| Drawer/inspector (document editor) | S | read · edit | open, saving, dirty (unsaved dot), error | Esc closes after confirm on dirty | "Save" disabled until dirty; dirty dot before the title |
| Dialog | F/S | create · confirm-destructive · form | open, submitting, error, blocked | focus trap, Esc = cancel (not on destructive without typed confirm) | destructive names the object: "Delete collection "cities"?" |
| Plan/seat control (Spark/Blaze) | S | current plan · upgrade card | active, confirming, prorating, blocked (billing missing) | Enter opens plan sheet | "names cost + effective date": "Blaze — pay as you go, active now" |
| Member row (IAM/users) | S | owner · editor · viewer | hover, pending invite, removing | row menu via kebab or shift-tab | role named in text, not colour |
| Audit/usage entry | D | billing line · functions log line | expanded, filtered-out, error-flagged | Enter expands | timestamp + verb + object, tabular amounts |
| Command palette (project/docs search) | S | project scope · docs scope | closed, open, no results, searching | global key opens, arrows, Enter | placeholder states the scope: "Search this project" |

**Every fetching surface also designs:** loading (skeleton rows matching final 32/40px geometry
with shimmer — never a centred spinner on a blank page), empty (names what is missing plus the CTA
that fixes it: "No documents yet — Add document"), error (what happened, the request ID, a Retry),
offline/stale (cached values greyed with an "offline — showing cached data" banner; live values
resume automatically).

**Contracts this table encodes:** one primary filled CTA per view (blue; dense toolbars may run the
primary plus icon actions); every icon-only control carries a tooltip (the kebab says "More
options"); a disabled control states why on focus or hover ("Add a billing account to enable
Blaze"); a button never changes width between idle and loading — the spinner reserves the label's
space.

## 10. Light / Dark Strategy

- **Posture: C dual-parity.** The console ships light-first (its working canvas is white-on-grey,
  sampled); the marketing shell ships dark-first (sampled #1E1E1E). Both are authored here from one
  primitive ramp so either mode is a first-class render of the same system.
- **Mechanism:** semantic roles remapped per mode; **no role absent in either mode.** The only
  single-mode roles are the marketing-only hero treatments, which live outside the product shell.
- **`color-scheme`** is set at the root so UA chrome, form controls and scrollbars follow the mode.
- **The scheme meta tag** is declared in the head before any stylesheet to prevent a flash of the
  wrong scheme.
- **Dark is authored, not inverted:** its own ramp (#161616 → #1F1F1F → #303030 → #474747), its own
  border strength (keylines step from #5F6368 to #C7C7C7 — a hairline that reads as delicate on
  white reads as invisible on near-black), zero shadows. `light-dark()` notation is progressive
  enhancement only, never the mechanism.
- Org-tinting is not offered: Firebase's brand is Google's, and the amber/blue split does the
  differentiating work. If a white-label need ever arises, colour tokens alone may swap; radii,
  type sizes and layout are frozen so a theme swap cannot move anything.

## 11. Density-Mode Strategy

- **Default mode per surface class:** Focused for docs reading, pricing and onboarding; Standard
  for project overview, Auth users and settings; Dense for the Firestore data viewer, Functions
  logs, and usage/billing tables. The boundary is the job: browsing and deciding = Standard;
  scanning and comparing = Dense.
- **Mechanism:** a density marker at the application root rescales row height, cell padding,
  gutter and base body size together as one token axis. Spacing tokens do not change with screen
  size — density is not a media query.
- **Container queries for reflow:** a grid reflows to its container, not the viewport; size queries
  fail closed with no eligible container, and container units silently resolve to small-viewport
  units there — so container units are never used where that fallback would be wrong.
- **Style queries** compare computed values, so the density marker is registered with an explicit
  type and inheritance declaration before any style query reads it.
- **The switch is offered as an accessibility affordance**, not a preference: the W3C note on SC
  2.5.8 endorses "a mechanism to control the density of layout" for users with visual field loss.
  Dense is the default only on data surfaces; every data surface exposes the switch back to Standard.

## 12. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum. AAA where cheap: 7:1 on primary reading text in Focused surfaces;
  SC 2.4.11 focus not obscured on all sticky-chrome surfaces.
- **Target size:** ≥24×24 CSS px hard minimum (the 24px-diameter circle exception respected); 44px
  is the design target for primary controls in F/S. Dense rows keep 32px height with full-width hit
  targets and ≥8px horizontal separation. Zoom does not excuse target size.
- **Keyboard:** every function operable without a pointer (SC 2.1.1); focus indicator visible
  (SC 2.4.7) — 2px `border.focus` ring at 2px offset, never suppressed without an equal or stronger
  replacement; the focused row is never entirely hidden under the sticky toolbar (SC 2.4.11).
- **Contrast:** text ≥4.5:1 (computed in the §3 gate); boundaries and focus ≥3:1. **Colour
  independence:** every status pairs colour with a glyph; selection adds a 3px edge plus weight;
  deltas carry a signed direction marker (+/− with arrow); the amber chart series differ by pattern
  as well as hue.
- **Motion:** the §8 reduced-motion variant applies per component; chart draw-ins and marketing
  parallax collapse to crossfades.
- **Text:** ≤80-character measure, 1.5 leading on prose, 200% resize without horizontal scroll
  (SC 1.4.8) — the data grids honour this via column wrap, not clipping.
- **Semantics:** real interactive elements (button, link, input) with correct roles; headings match
  visual rank; live regions announce deployment and build status politely; a loading grid sets its
  busy marker; the document drawer moves focus in on open and restores it on close.
- **Contrast preference:** `prefers-contrast: more` swaps text.secondary → text.primary, raises all
  hairlines to `border.strong`, and thickens the focus ring to 3px. Values honoured: `no-preference`,
  `more`.

## 13. Anti-Patterns

**Do**
- Put every action in blue and let amber mean identity only — the two-accent split is the system's
  whole grammar; one filled CTA per view, two text links max per region.
- Render all identifiers (document IDs, collection paths, build hashes) in Roboto Mono with
  tabular figures — they are the actual payload of a backend console.
- Right-align and tabulate every number column; sort icons live in the header, never the cell.
- Build skeletons at the exact final row geometry (32px dense / 40px standard) before data arrives.
- Pair every status colour with a glyph — check, warning triangle, alert, info — in every mode.
- Match toolbar, header and pagination heights to row height (40/40/40 or 32/32/32).
- Author dark from the brand grey ramp with keylines, never from a filter over the light theme.
- Give every empty state a named CTA ("Add document", "Create database", "Enable providers").
- Explain every disabled control on focus or hover; a silently dead primary is a defect.
- Keep hairlines at 1px and do the depth work with fills and steps; shadows max out at level 3.
- Show one Firebase lockup per view — product icons ride amber circles, per brand rules.
- Expose the density switch on every data surface as an accessibility affordance.

**Don't**
- No amber text on white or grey — raw #FFC400 as text fails at every size; use `accent.brandDeep`.
- No amber action buttons, ever — the "Get started" orange is a marketing-register fill and stays
  on marketing surfaces.
- No pure-black dark canvas (#000000 appears nowhere as a surface; wells bottom out at #161616).
- No shadows in dark mode; a drop shadow on near-black is invisible and expensive.
- No marketing gradients, hero type or full-bleed photography inside the product shell.
- No two filled primaries side by side; a second emphasis is always an outline or text link.
- No toolbar of unlabelled icon buttons — every icon carries a tooltip or visible label.
- No hover-only affordances; everything reachable by focus must be reachable by keyboard.
- No placeholder-as-label in form fields (project IDs, security rules, collection names all need
  persistent labels).
- No whole-page spinners; the shell stays put while the region skeleton loads.
- No blocking browser dialogs; destructive confirms are real dialogs that name the object.
- No 12px body type as a density strategy — density comes from rows, padding and column pruning;
  prose never drops below 13px even in logs.
- No mid-page density switches; the Firestore viewer is dense edge to edge or it is wrong.
- No heritage blue #039BE5 under body-size white text; that fill is for large type only.

## 14. Quick Reference & Verification Gate

**Colour (role → light / dark):** canvas #FFFFFF / #1F1F1F · raised #FFFFFF / #303030 · overlay
#FFFFFF / #474747 · inset #F5F5F5 / #161616 · hover #F1F3F4 / #2A2A2A · selected #E8EAED / #3C4043 ·
border subtle #E0E0E0 / #5F6368 · border strong #5F6368 / #C7C7C7 · border focus #0B57D0 / #8AB4F8 ·
accent action #1A73E8 / #8AB4F8 · onAction #FFFFFF / #202124 · accent subtle #E8F0FE / #283A4E ·
brand amber #FFC400 both modes · brandDeep text #8F5300 / #FFC400 · heritage fill #039BE5 both ·
text primary #202124 / #F2F2F2 · secondary #5F6368 / #ABABAB · tertiary #757575 / #8F8F8F ·
disabled #9AA0A6 / #5F6368 · success #0D652D on #E6F4EA / #5BB974 on #1E3327 · warning #8A5300 on
#FEF7E0 / #FDD663 on #382C10 · error #C5221F on #FCE8E6 / #F28B82 on #3B1B1A · info #0B57D0 on
#E8F0FE / #8AB4F8 on #283A4E.

**Type ramp:** Google Sans 32/40 Display · 24/32 Page title, Heading, Stat value · 16/24 Section
title, [F] Body · 16/20 [F] Label, [S] Body · 14/20 Row primary, Meta [F] · 13/20 Grid cells,
Identifier (mono) · 12/16 Row secondary, Meta [S], Grid header, Log line (mono), Inline help ·
11/16 Stat label.

**Spacing + radius:** 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 · radius 0 / 2 / 4 / 8 / 16 / full ·
rows 40px S, 32px D · gutters 32 F, 24 S, 16 D.

**Component → token map:** Data table consumes surface.canvas, surface.inset (header),
surface.hover/selected, border.subtle, text.primary/secondary, accent.action (links), Roboto Mono
identifier, radius.none, level-0. Dialog consumes surface.overlay, level-4, radius.md, text.primary,
accent.action (confirm), scrim token. Stat tile consumes surface.raised, level-1, radius.md, Google
Sans stat value, brand.amber (sparkline series 1), brand.orange (series 2). Sidebar consumes
surface.canvas, surface.hover, border.subtle, text.secondary → primary on active. Row menu consumes
surface.overlay, level-3, radius.sm, surface.hover. Plan control consumes accent.brand badge,
status.info wash for prorating notes, text.secondary for cost metadata.

**Pre-ship checklist.**
1. Zero raw hex outside L1.
2. No token resolves to a component name.
3. Every contrast pairing computed, passing, unrounded (§3 gate is the source of truth).
4. Every semantic role has a value in both shipped modes.
5. Every fetching surface has loading/empty/error/offline specified.
6. Every component row lists disabled and loading states.
7. Row, header, toolbar and pagination heights agree (40/40/40 or 32/32/32).
8. Reduced-motion variant written for every authored motion.
9. Every control keyboard-reachable with a visible focus indicator.
10. Dark authored, not filtered, with border strength exceeding light's.
11. No unoverridden stock Material default inside a committed surface (ripples, default blues below
    #1A73E8 saturation, 16px Material body on data grids are the usual survivors).
12. Nothing came from a marketing page — the marketing register (dark hero, orange CTA) stays out
    of the console shell except where §10 maps it to dark mode.
