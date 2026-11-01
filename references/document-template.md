# Design System — Meridian (worked example)

A **filled-in** `DESIGN.md` for a fictional B2B observability console, annotated so an agent can see
*why each section exists* — what a reviewer checks, and which failure it prevents. Copy the structure
from `init-design-template.md`, not this file's values. Meridian is a Dense, dual-parity, tone-first
product; a Focused checkout product would use a different subset.

**Annotation convention:** `▸ WHY:` lines are commentary for the reader. They are stripped from a real
`DESIGN.md`. As-of: 2026-10-05.

---

```markdown
# Design System — Meridian
<!-- premium-web-design:design-system 2 --> <!-- As-of: 2026-10-05 -->
<!-- Reference inspirations: Grafana (density + data surfaces), Linear (restraint + keylines) -->
<!-- Surface classes: 14 routes classified; density classes [S]/[D]; [F] on auth + onboarding -->

## 1. Design Posture & Atmosphere
Meridian is an instrument, not a dashboard. Operators live in it for eight-hour shifts in dim rooms,
so the product is **tonal and low-glare**: depth is expressed by four surface steps and 1px keylines,
never by shadow on a near-black canvas. Colour is reserved for *state* — a query that is failing, an
alert that is firing, a selection that is active. Nothing is coloured for decoration, because a
decorative colour in an alert list costs the operator a second of parsing. The single metaphor is
**an instrument panel**: dense, calibrated, legible under stress.
**Key Characteristics** — depth is a 4-step surface ramp plus 1px hairlines; shadows in light mode
only; accent ≤2 uses/viewport [S] and 1 in [D]; every numeric column tabular; rows 32px [D], 40px [S];
dark borders one step stronger than light's; never more than one filled primary per view; every
fetching surface designs loading, empty, error and offline/stale.

## 2. Token Architecture   ← normative
Three layers. A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer. L1 primitive named by value (`--palette-neutral-1000`,
`--space-4`); no `[component]-[prop]` naming. L2 semantic named by role (`surface.raised`,
`text.primary`); the only layer a component may consume. L3 component only for deliberate deviation,
pointing at L2 or L1 — never a raw value, never a sibling component's token. Every token has a
determinable type or it is invalid; names case-sensitive with no `$`/`{`/`}`/`.`; no circular
references. Every semantic token has a value in **both** modes. `--density`, `--row-height`,
`--cell-pad-x`, `--text-size-body` are registered with `@property` (`syntax` + `inherits` both
present; `initial-value` in px, never `%`/`em`) so they interpolate and so `@container
style(--density: dense)` reads a computed value. Layer order low → high: `reset → primitives →
semantic → components → utilities` — `@layer` order beats specificity entirely and unlayered normal
declarations outrank layered ones, so a stray un-layered rule in a component file would beat this
whole system.

## 3. Colour Roles
| Role | Light | Dark |
|---|---|---|
| `surface.canvas` | `#FAFAFA` | `#0E0F12` |
| `surface.raised` | `#FFFFFF` | `#16181D` |
| `surface.overlay` / `inset` | `#FFFFFF` / `#F4F5F7` | `#1C1F25` / `#101216` |
| `surface.hover` / `selected` | `#F0F1F3` / `#E8EAFF` | `#1A1D23` / `#1E2033` |
| `border.subtle` / `strong` / `focus` | `#E4E6EA` / `#C7CAD1` / `#4F46E5` | `#282C33` / `#3A3F48` / `#818CF8` |
| `accent.action` / `onAction` | `#4F46E5` / `#FFFFFF` | `#6366F1` / `#0B0C0E` |
| `text.primary` / `secondary` / `tertiary` | `#16181D` / `#4A4F5A` / `#6E7480` | `#F2F3F5` / `#A8AEBB` / `#767D8C` |
| `status.success` / `warning` / `danger` / `info` | `#177245` / `#B25E09` / `#B3261E` / `#1F5FA8` | `#4ADE80` / `#FBBF24` / `#F87171` / `#60A5FA` |

Each status ships a glyph. Dark canvas is never pure black; depth in dark is surface steps + 1px
strokes, never shadows.
**Contrast gate (computed, unrounded):** `text.primary` on canvas 16.8:1 dark / 17.2:1 light ·
`text.secondary` 7.9:1 / 7.1:1 · `text.tertiary` 4.6:1 / 5.2:1 · `accent.onAction` on `accent.action`
8.6:1 / 7.4:1 · `border.strong` on `surface.raised` 3.4:1 / 3.2:1 (SC 1.4.11) · `status.danger` on its
12% wash ≥4.8:1 both modes. All pass.

## 4. Typography
UI: self-hosted Inter 400/500/600, preloaded, subset. Numeric/code: JetBrains Mono for IDs, hashes,
raw timestamps — monospace is for identifiers and code, never a costume.
**[D] Dense, 13px base:** grid header 12/600/16 · grid cell numeric 13/400/18 `tabular-nums` · grid
cell text 13/400/18 · log line 12 mono/400/18 `tabular-nums` · inline help 13/400/20.
**[S] Standard, 14px base:** page title 20/600/28 · section title 15/600/22 · body 14/400/21 ·
row primary 14/400/20 · row secondary 13/400/20 · stat value 28/600/34 `tabular-nums` · stat label
12 uppercase/500/16 · meta 13/400 `tabular-nums`.
**[F] Focused, 16px base:** display 28/600 · heading 18/600 · body 16/400/24 · label 14/500 · meta
13/400 `tabular-nums`.
Invariants: `tabular-nums` on every comparable value — currency, timestamps, deltas, counts, IDs.
Right-align numerics, left-align text, never centre a numeric column. Fixed stepped sizes; no
`clamp()`. Measure 65–80ch [S], unconstrained [D].

## 5. Spacing & Density
Spacing base 4px grid, 8px comfortable [F/S]: `1` 4px · `2` 8px · `3` 12px · `4` 16px · `6` 24px ·
`8` 32px · `12` 48px. No 17px, no 23px.
| Density mode | Row height | Base body | Cell pad-x | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | auth, onboarding, settings detail |
| `standard` | 40px | 14px | 16px | 24px | project home, record detail |
| `dense` | 32px | 13px | 12px | 16px | grids, logs, admin, audit |
Header, toolbar, batch bar and pagination heights always equal the row height of the table they sit
above. Density never changes mid-page. Density comes from row height, column count and leading —
never from making type too small to read.

## 6. Radius
`none` 0 · `xs` 2px badges · `sm` 4px inputs/cells/code · `md` 6px buttons/rows/cards · `lg` 10px
panels/drawers/dialogs · `full` 9999px pills/avatars. One radius per family; nested radii = outer −
padding; one base `--radius` with `calc()` multipliers.

## 7. Elevation
Light: ambient shadow + faint hairline. Dark: surface-luminance steps + 1px keyline, **zero shadows** —
a drop shadow is invisible on a near-black canvas. Levels: **0** canvas · **1** card (shadow +
`border.subtle` / one surface step up) · **2** sticky header (stronger shadow / further step +
`border.strong`) · **3** overlay (strongest shadow, `radius.lg` / top step) · **4** dialog (+ scrim
both modes).

## 8. Motion
`instant` 0ms · `fast` 120ms ease-out (exits) · `base` 180ms decelerate ([D] entrances) · `slow` 260ms
decelerate ([F/S] entrances, dialogs). Entrances decelerate, exits accelerate; symmetric ease-in-out is
a defect. Animate `transform` and `opacity` only. No bounce on irreversible moments.
**Reduced motion** is a real variant: movement → crossfade under 150ms. `prefers-reduced-motion`
targets vestibular triggers specifically — MDN names scaling and panning large objects — so those are
neutralised; fades and colour changes survive.

## 9. Imagery & Art Direction
The one expressive moment is **the product itself** — real query results and real dashboards are the
imagery. No hero illustration, no photography, no 3D. Icons: one family, 1.5px strokes on a 16px grid,
geometric, matching the typeface's tone; filled variants only in status glyphs where a 12px stroke
cannot carry the shape. Third-party integration logos render monochrome inside a committed surface,
never in brand colour. Empty and error states use text plus an icon — the spec states "no illustration
system" explicitly so nobody invents one per screen. Status glyphs pair with text labels, so the icon
never carries state alone.

## 10. Surface & Component Inventory
| Component | Density | States | Keyboard | Microcopy |
|---|---|---|---|---|
| App shell / sidebar | [S] | active route, focus, loading count | arrows + Enter | — |
| Data grid | [D] | loading, empty, error, no-permission, stale | roving tabindex, `Esc` | — |
| Filter / search | [S] | focus, clear-on-demand | `/` focuses | "Filter queries" |
| Row action menu | [D] | focus-trap | arrows, `Esc` | "Edit query", "Archive" |
| Stat tile | [S] | skeleton, no-data, error | — | — |
| Drawer / inspector | [S] | loading, unsaved-changes | `Esc` closes | — |
| Dialog | [F] | loading, inline error | trap, `Esc` | names the action |
| Seat / plan control | [F] | confirming, prorating, blocked | — | names cost + effective date |
| Member row | [S] | pending, error | — | "Revoke invitation" |
| Audit entry | [D] | loading more | — | — |
| Command palette | [S] | loading, error | full trap, `Esc` | — |

Every fetching surface also designs loading (skeleton matching final geometry — never a centred
spinner on a blank page), empty (what's missing + the CTA that fixes it), error (what happened + how
to recover), and offline/stale (what's known vs cached).

## 11. Light / Dark Strategy
**Posture C — dual parity.** Operators use Meridian in both lighting conditions; switching is personal.
Semantic roles are remapped per mode; **no role is absent in either mode.** `color-scheme` is set on
`:root` so UA chrome, form controls and scrollbars follow — it repaints UA-provided parts of the
canvas and does not theme the document, so surfaces are authored separately. `<meta name="color-scheme">`
sits in the head **before** the stylesheet, preventing a flash of the wrong scheme. Dark borders are
one step stronger than light's; dark shadows are zero. `light-dark()` is a progressive enhancement
only — MDN records it as Baseline 2024, newly available.

## 12. Density-Mode Strategy
Default `dense` on grid/log/audit/admin routes; `standard` on project home and record detail;
`focused` on auth, onboarding and plan/seat changes. Mechanism: `--density` on the app root (registered
with `@property`) rescaling row height, cell padding, gutter and body size together — Carbon's spacing
tokens "do not change values based on the screen size", so density is a token axis, never a media
query. Reflow uses `@container`, not viewport media queries: it is Baseline widely available and
measures the content box, so a panel works identically in a sidebar or full width. Size queries fail
closed with no eligible container and `cqi`/`cqw`/`cqmin`/`cqmax` silently resolve to small-viewport
units there — so `cq*` units are never used where that fallback would be wrong. The switch ships in
Settings as an accessibility affordance, not a preference: W3C's note on SC 2.5.8 endorses a
density-control mechanism, naming users with visual field loss explicitly.

## 13. Accessibility Commitments
WCAG 2.2 AA minimum. Targets ≥24×24 CSS px or the spacing exception (a 24px-diameter circle centred on
each target's bounding box must not intersect another's); 44px is the design target for primary
controls [F/S], 24px the hard minimum; zoom does not excuse it. All functionality keyboard-operable
(SC 2.1.1); focus indicator visible (SC 2.4.7), never entirely hidden by a sticky header or drawer
(SC 2.4.11), meeting 3:1 (SC 1.4.11). Text ≥4.5:1; boundaries and focus indicators ≥3:1; colour never
the sole carrier of status — every status pairs an icon or label. Measure ≤80 characters; 1.5 leading;
200% resize with no horizontal scrolling (SC 1.4.8). Real `<button>`/`<a>`/`<input>`; roles and
`aria-*` correct; headings match visual rank; `aria-live="polite"` for non-urgent updates; `aria-busy`
on a loading region.

## 14. Anti-Patterns
**Do** — anchor the dense surfaces in a real operational scene (an SRE on a 1440p display with two
monitors) and let row height, column count and leading carry density; keep colour exclusively for state
and data; prune columns nobody reads or sorts by (a removed column beats a narrowed one); give every
operator action a keyboard path and a shortcut in the grid; name every destructive action and every
cost before the click.
**Don't** — import marketing aesthetics into a logged-in surface (gradient text, radial glows,
glassmorphism on content cards, purple/cyan AI palettes: those belong to `premium-marketing-design`);
build a four-tile KPI row; nest cards; use a centred spinner on a blank page; ship a layout that jumps
when data lands; shrink type to fit more rows; ship a proportional-figure numeric column; gate any
affordance behind hover; leave a disabled primary unexplained; use `alert()`/`confirm()` or a modal for
a two-field confirmation; add a second icon family or a second accent hue.

## 15. Quick Reference
**Colour (light / dark):** canvas `#FAFAFA`/`#0E0F12` · raised `#FFFFFF`/`#16181D` · overlay
`#FFFFFF`/`#1C1F25` · border.subtle `#E4E6EA`/`#282C33` · text.primary `#16181D`/`#F2F3F5` ·
accent.action `#4F46E5`/`#6366F1` · status.danger `#B3261E`/`#F87171`
**Type [D]:** header 12/600/16 · cell 13/400/18 · log 12 mono/400/18
**Spacing:** 4/8/12/16/24/32/48px · **Radius:** 2/4/6/10/full px
**Pre-ship checklist:** 1 zero raw hex outside L1 · 2 no token resolves to a component name ·
3 every contrast pairing computed and passing, unrounded · 4 every role has a value in both modes ·
5 loading/empty/error/offline on every fetching surface · 6 disabled and loading on every component ·
7 row/header/toolbar/pagination heights agree · 8 reduced-motion variant per authored motion ·
9 every control keyboard-reachable with a visible focus indicator · 10 dark authored, not filtered ·
11 no unoverridden stock library default inside a committed surface · 12 nothing from a marketing page ·
13 the §9 brand-moment palette appears nowhere in the UI token layers.
```

▸ **WHY each section exists — the failure it prevents:**

| Section | Failure prevented |
|---|---|
| §2 Token architecture | Tokens that exist but are bypassed; unresolvable mode remapping |
| §3 Colour roles + contrast gate | Undocumented contrast debt; colour-only status |
| §4 Typography × density class | One blended ramp; tiny type used as density |
| §5 Spacing **and** density as two axes | Conflating the scale with the mode; density changing mid-page |
| §6–7 Radius and elevation | Random radii; shadow-on-dark that renders as nothing |
| §8 Motion with a real reduced variant | Symmetric easing; `animation: none` everywhere |
| §9 Imagery & art direction | Saturation leaking into UI tokens; per-screen invented art |
| §10 Inventory **with states** | Half-built components discovered at the call site |
| §11 Light/dark posture | Dark as an inverted filter; a flash of the wrong scheme |
| §12 Density-mode strategy | Density faked with viewport queries; no `cq*` fallback |
| §13 Accessibility as commitments | Generic "we're accessible" with nothing to check |
| §14 Anti-patterns | Re-litigating the bans in every future session |
| §15 Quick ref + checklist | A spec nobody re-reads |

▸ **What is NOT here, and why:** no CSS selectors, no component-library prop names, no framework
imports. `DESIGN.md` states *what the design is*; how it binds to Tailwind, React or a theme object is
the adapter's job, and nothing new may be invented there.

---

## Not found

- **Verified contrast ratios for the Meridian palette.** The §3 figures are illustrative placeholders
  for a fictional product and have not been computed with a tool. A real `DESIGN.md` must compute each
  ratio — never assert, never round; 4.499:1 fails. Settled by: running a contrast checker against each
  shipped pairing.
- **A sourced rule for "dark borders one step stronger."** It follows from a 1px hairline reading as
  delicate on white and invisible on near-black, but no standard states it. House guidance; validate
  by screenshot.
- **A standard for how many surface steps a ramp should have.** Four is this skill's calibration for
  Dense console surfaces. Settled by: none — check that the top step still separates from overlays.

## Sources

All accessed 2026-10-05. Parenthetical = what the citation carries in this example.

- **WCAG 2.2** — W3C / W3C WAI. (SC 1.4.3 Contrast (Minimum) 4.5:1 and 3:1 large text; SC 1.4.11 Non-text Contrast 3:1 for boundaries, state and focus indicators; SC 2.5.8 Target Size (Minimum) incl. the spacing exception and the zoom clause; SC 1.4.8 Visual Presentation; SC 2.1.1; SC 2.4.7; SC 2.4.11.) https://www.w3.org/TR/WCAG22/ · https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html · https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html · https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html
- **`font-variant-numeric`** — MDN, Mozilla. (`tabular-nums` activates figures "all of the same size, allowing them to be easily aligned like in tables"; Baseline widely available since January 2020.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variant-numeric
- **Registering custom properties in CSS** — MDN, Mozilla. (`@property` requires `syntax` AND `inherits` or the rule is invalid; `initial-value` cannot use `%` or `em`; registered interpolates, unregistered animates discretely.) https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Properties_and_values_API/Registering_properties
- **`@layer`** — MDN, Mozilla. (Order beats specificity entirely; unlayered normal declarations outrank layered ones.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer
- **`color-scheme`** — MDN, Mozilla. (Repaints UA chrome only, does not theme the document; `<meta name="color-scheme">` before CSS to avoid a flash; `light-dark()` Baseline 2024 newly available.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme
- **`@container`** — MDN, Mozilla. (Baseline widely available; content-box measurement; `cq*` fallback to small-viewport units with no eligible container; style queries compare computed values.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@container
- **`prefers-reduced-motion`** — MDN, Mozilla. (Baseline widely available; scaling and panning large objects named as vestibular triggers.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
- **Design Tokens Format Module 2025.10** — W3C Design Tokens Community Group. (Groups arbitrary; tools SHOULD NOT infer type/purpose; `$type` determinable or invalid; names case-sensitive excluding `$`/`{`/`}`/`.`; circular refs MUST error.) https://www.designtokens.org/TR/2025.10/format/
- **Data table** — Carbon Design System, IBM. (Row sizes xs 24 / sm 32 / md 40 / lg 48 / xl 64; header, toolbar and pagination heights match row size.) https://carbondesignsystem.com/components/data-table/usage/
- **Typography: type sets** — Carbon Design System, IBM. (Productive 14px base vs expressive 16px base.) https://carbondesignsystem.com/elements/typography/type-sets/
- **Layout** — Shopify App Design Guidelines. ("Avoid changing information density within a single page.") https://shopify.dev/docs/apps/design/layout
- **Theming** — shadcn/ui. (Spacing tokens do not change on screen size; one base `--radius` with derived multipliers.) https://ui.shadcn.com/docs/theming
- Template structure and every house rule (density classes, accent budget, one-primary-per-view, state requirements, anti-pattern bans) — `references/init-design-template.md`, `references/craft-floor.md`.
