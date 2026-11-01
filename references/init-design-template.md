# DESIGN.md Output Template (Framework-Neutral)

The exact section structure for the `DESIGN.md` written in Phase 2 of `init`. Every `[...]` becomes a
real, product-specific value; **zero generic placeholders survive review.** Token architecture,
density strategy and anti-patterns exist because those are where a web design system silently decays.

> **Strict neutrality:** pure design spec — hex, px, ratios, curves, role names. **No CSS selectors,
> no framework imports, no component-library prop names, no JSX/TSX/Vue/Svelte syntax.** A line that
> would not survive a print belongs in the adapter, not here.
>
> **House rule, flagged once:** the primitive → semantic → component taxonomy below is **this skill's
> rule, not a standard**. The W3C Design Tokens Format Module 2025.10 calls token groups "arbitrary"
> and says tools "SHOULD NOT" infer type or purpose from them, while *requiring* a determinable
> `$type`, case-sensitive names free of `$`, `{`, `}`, `.`, and error detection on circular references.
> The structure is ours; the type discipline is theirs. As-of: 2026-10-05.

---

```markdown
# Design System — [Product Name]

<!-- premium-web-design:design-system 2 -->
<!-- As-of: [YYYY-MM-DD] -->
<!-- Reference inspirations: [App] (density/type), [App] (colour + shell) -->
<!-- Surface classes: [n] routes classified; density classes [F/S/D] assigned -->

## 1. Design Posture & Atmosphere
[2–3 paragraphs: emotional register, how the surface feels after eight hours, where this product sits
against its category's defaults, and the single visual metaphor — "instrument panel", "ledger sheet",
"terminal with manners". Ground it in the Phase 1 usage scene.]
**Key Characteristics** — 10–15 bullets, each carrying a concrete value, e.g. "Depth is a 4-step
surface ramp plus 1px hairlines; shadows exist only in light mode." / "One accent fill per viewport in
[S]; rows are 40px [S], 32px [D]."

## 2. Token Architecture   ← normative
**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a
**primitive**; nothing skips a layer.
- **L1 Primitive** — literal values named by *value* (`[palette].[step]`, `[scale].[n]`), referenced
  only by L2. Banned: `[component]-[prop]` naming (`--card-bg`, `--tooltip`) — one value, many roles.
- **L2 Semantic** — role names (`surface.canvas`, `text.primary`, `accent.action`). The only layer a
  component may consume.
- **L3 Component** — only for deliberate deviation; points at L2 or L1, never a raw value, never a
  sibling component's token.
**Rules.** Every token has a determinable type or it is invalid; names case-sensitive, no `$`, `{`,
`}`, `.`; no circular references (`[a] → [b] → [a]` is an error). Every semantic token has a value in
**every** shipped mode — a role with no dark value resolves to its light value and fails contrast.
Register animatable tokens with `@property`: it needs **both** `syntax` and `inherits` or the whole
rule is invalid, and `initial-value` must be computationally independent, so `%`/`em` are illegal.
**Layer order (low → high)** `[reset] → [primitives] → [semantic] → [components] → [utilities]`.
`@layer` order beats specificity entirely and unlayered normal declarations outrank layered ones, so a
stray un-layered rule in a component file would beat this whole system; anything a consumer must
override without `!important` sits in the top layer.

## 3. Colour Roles
| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` / `raised` / `overlay` / `inset` | | | canvas · cards · overlays · wells |
| `surface.hover` / `surface.selected` | | | Interaction fills |
| `border.subtle` / `strong` / `focus` | | | 1px hairlines; `border.focus` ≥3:1 |
| `accent.action` / `onAction` / `subtle` | | | Accent budget: [n] per viewport |
| `text.primary` / `secondary` / `tertiary` / `disabled` | | | Ink ramp |
| `status.success` / `warning` / `error` / `info` | | | Each ships a glyph — never colour alone |
Dark canvas is **not** pure black: `[range]`. Depth in dark comes from surface steps and 1px strokes,
never shadows.
**Contrast gate — compute each ratio; do not assert it, and do not round. 4.499:1 fails. Large text is
≥24px or ≥18.5px bold. Body ≥4.5:1; UI boundaries and focus indicators ≥3:1** (W3C, SC 1.4.3, 1.4.11).
Gate rows: `text.primary`/`secondary`/`tertiary` on `surface.canvas`; `accent.onAction` on
`accent.action`; `border.strong` on `surface.raised`; `status.*` on its wash. Columns: foreground, hex,
background, hex, ratio, required, verdict.

## 4. Typography
**Families.** UI `[family, weights, self-hosted, preloaded, fallback]`; numeric/code `[family]` for
identifiers, hashes, raw timestamps. *Monospace is for identifiers and code, never a costume.*
**One ramp table per class, not one blended table.** Columns: role, size, weight, line height, tracking,
numerals, use.
- **[F] Focused, 16px base:** Display · Heading · Body · Label · Meta.
- **[S] Standard, 14–15px base:** Page title · Section title · Body (1.5) · Row primary · Row
  secondary · Stat value (`tabular-nums`) · Stat label (uppercase, slight positive tracking) · Meta.
- **[D] Dense, 12–13px base, data surfaces only:** Grid header · Grid cell numeric (`tabular-nums`) ·
  Grid cell text · Log line (mono) · Inline help. *Prose inside a dense screen still steps up to
  [size].*
**Invariants.** `tabular-nums` on every comparable value — currency, timestamps, deltas, counts, IDs
("all of the same size, allowing them to be easily aligned like in tables", MDN). Right-align numerics,
left-align text, never centre a numeric column. Fixed stepped sizes; no `clamp()`. Measure ≤80
characters (SC 1.4.8); 65–80ch [F/S], unconstrained [D].

## 5. Spacing Scale & Density Scales   ← two axes, never one
**Spacing base: 4px grid; 8px comfortable [F/S], 4px [D].** `space.0` 0 · `1` 4px icon-to-label ·
`2` 8px control padding [D] · `3` 12px cell padding [S] · `4` 16px card padding [S] / page gutter ·
`6` 24px card padding [F] + section gap · `8` 32px section gap [S] · `12` 48px region separation ·
`16` 64px rarely. *No `17px`. No `23px`. If a layout needs an off-scale value, the layout is wrong.*
**Density mode — the rescaling axis.**
| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | Auth, checkout, settings detail |
| `standard` | 40–44px | 14–15px | 12–16px | 24px | Project home, record detail |
| `dense` | 28–32px | 12–13px | 8px | 16px | Tables, admin, logs, observability |
- Density comes from **row height, column pruning and leading** — never from type too small to read. A
  13px tabular numeral in a dense table is correct; the same numeral in a Focused form is a defect.
- **Never switch mid-page.** "Avoid changing information density within a single page, otherwise your
  app can feel disjointed" (shopify.dev, *Layout*). Switching across routes with different jobs is
  legitimate — it should feel like a different room.
- **Chrome follows rows.** Header, toolbar, batch bar and pagination heights always match the table's
  row height (Carbon, *Data table*). A 40px toolbar over 32px rows is a rhythm break.
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40%. *House heuristic, not a vendor
  figure — validate by screenshot.*

## 6. Radius Scale
`none` 0 · `xs` 2px badges/tags · `sm` 4px inputs, dense cells, inline code · `md` 6px buttons, rows,
cards · `lg` 10px panels, drawers, dialogs · `full` 9999px pills, avatars, icon buttons. **One radius
per component family**, never mixed ad-hoc. Nested radii obey `radius_inner = radius_outer − padding`.

## 7. Elevation
**Choose one strategy, never mix paradigms.** Light: multi-layer ambient shadows + faint hairline.
Dark: surface-luminance steps + 1px keylines, **zero shadows** — a drop shadow is invisible on a
near-black canvas. Levels, low → high: **0** canvas (no shadow, both modes) · **1** card/panel (shadow +
`border.subtle` / one surface step up) · **2** sticky header/toolbar (stronger shadow / further step +
`border.strong`) · **3** overlay (strongest shadow, `radius.lg` / top step + `border.strong`) · **4**
dialog (strongest shadow + scrim / top step + scrim).

## 8. Motion
`instant` 0ms · `fast` 120ms ease-out (exits [D]) · `base` 180ms decelerate ([D] entrances) · `slow`
240–300ms decelerate ([F/S] entrances, dialogs).
- Entrances decelerate, exits accelerate. Symmetric ease-in-out on both directions is a defect.
- Animate `transform` and `opacity` only — never `width`, `height`, `top`, `left`.
- No bounce on irreversible moments: not a confirm dialog, not a downgrade.
- **Reduced motion is a real variant**, not `animation: none` everywhere: movement → crossfade under
  ~150ms. `prefers-reduced-motion` is Baseline widely available and targets vestibular triggers
  specifically — MDN names **scaling and panning large objects**, so those are what must be
  neutralised, not every fade.

## 9. Imagery & Art Direction   ← the one licensed saturation moment
**Policy, not asset list.** Where the product earns expressiveness, and where it must stay achromatic.
Every rule here is checkable at review; a rule that cannot be checked does not belong.
- **Brand moment:** [the single expressive surface — hero illustration, photographic packshot,
  abstract render] and the rule that its palette **never leaks into UI tokens**. One saturation
  moment per surface, not a recurring accent. "None" is a valid and common answer for product UI.
- **Iconography:** [library or custom], [weight]px strokes on a [n]px grid, geometric — matched to
  the typeface's tone. Filled variants only where a stroke cannot carry [size]px. Icon-only controls
  still carry a label (§10).
- **Photography:** [subjects and treatments — or "none"]. Third-party logos render monochrome inside
  a committed surface, never in their brand colour.
- **Illustration / 3D:** [policy — or "none"]. If present, the performance budget (poster image
  first, DPR clamp, pause off-screen) belongs in the adapter; the spec records only the visual policy.
- **Empty / error art:** illustration never substitutes for the recovery CTA; if no illustration
  system exists, say so — an unspecified gap invites per-screen invention.

## 10. Surface & Component Inventory
One row per real component; a component without documented disabled and loading states is unfinished.
Columns: component, density, variants, states, keyboard, primary microcopy. Rows: `App shell/sidebar` ·
`Data table` · `Filter/search bar` · `Row action menu` · `Stat tile` · `Drawer/inspector` · `Dialog` ·
`Plan/seat control` · `Member row` · `Audit entry` · `Command palette`. Example: the row-action menu's
states are focus-trap and `Esc`; the plan control's are confirming, prorating, blocked, and its
microcopy "names cost + effective date".
**Every fetching surface also designs:** loading (skeleton matching final geometry — never a centred
spinner on a blank page), empty (what's missing + the CTA that fixes it), error (what happened + how to
recover), offline/stale (what's known vs cached).
**Contracts this table encodes:** one primary filled CTA per view [F/S] (dense toolbars may run a
primary plus icon actions); every icon-only control carries a label or tooltip; a disabled control
states *why* on focus or hover rather than sitting silently dead; a button never changes width between
idle and loading — reserve the space.

## 11. Light / Dark Strategy
- **Posture:** `[A light-only · B dark-only · C dual-parity · D org-tinted]` and the reason.
- **Mechanism:** semantic roles remapped per mode; **no role absent in either mode.** List any
  single-mode role and say why.
- **`color-scheme`** set on `:root` so UA chrome, form controls and scrollbars follow. It "repaints
  UA-provided parts of the canvas… does not affect the default color scheme for the overall document".
- **`<meta name="color-scheme">` in the head before the stylesheet**, to prevent a flash of the wrong
  scheme. Both facts: MDN, `color-scheme`.
- **Dark is authored, not inverted:** its own surface ramp, its own border strength (usually higher — a
  1px hairline that reads as delicate on white reads as invisible on near-black), its own shadow
  policy. **`light-dark()` is progressive enhancement only** — Baseline 2024, newly available (MDN).
- Org-tinting (D) changes colour tokens only; radii, type sizes and layout are frozen so a theme swap
  cannot move anything.

## 12. Density-Mode Strategy
- **Default mode per surface class**, with the boundary that put it there.
- **Mechanism:** a density attribute/hook at the app root rescaling row height, cell padding, gutter
  and body size together. Carbon's spacing tokens "do not change values based on the screen size"
  (shadcn/ui, *Theming*) — so density is a **token axis, not a media query**.
- **Container queries for reflow:** `@container` is Baseline widely available and measures the *content
  box*, so a component reflows to its container, not the viewport. Size queries fail closed with no
  eligible container, and `cqi/cqw/cqmin/cqmax` silently resolve to small-viewport units there — so
  `cq*` units are never used where that fallback would be wrong.
- **Style queries** (`@container style(--x: y)`) compare *computed* values, so the density marker must
  be registered with `@property` (MDN, `@container`).
- **Offer the switch as an accessibility affordance**, not a preference: W3C's note on SC 2.5.8 endorses
  "a mechanism to control the density of layout," naming users with visual field loss.

## 13. Accessibility Commitments
- **Target:** WCAG 2.2 AA minimum; [AAA criteria] elsewhere.
- **Target size:** ≥24×24 CSS px, or the spacing exception — a 24px-diameter circle centred on each
  target's bounding box must not intersect another's. SC 2.5.5 at 44×44 is **AAA, not AA**: 44px is
  the design target for primary controls [F/S], 24px the hard minimum. *Zoom does not excuse it.*
- **Keyboard:** every function operable (SC 2.1.1); focus indicator visible (SC 2.4.7), never
  `outline: none` without a stronger `:focus-visible` replacement; the focused item never entirely
  hidden by a sticky header, footer or persistent overlay (SC 2.4.11).
- **Contrast:** text ≥4.5:1; UI boundaries and focus indicators ≥3:1 (SC 1.4.11). **Colour
  independence:** every status pairs colour with an icon, label or shape; deltas carry a sign or
  direction glyph.
- **Motion:** the reduced-motion variant from §8, per component.
- **Text:** ≤80-character measure, 1.5 leading, 200% resize without horizontal scroll (SC 1.4.8).
- **Semantics:** real `<button>`/`<a>`/`<input>`; correct roles; headings matching visual rank;
  `aria-live="polite"` for non-urgent updates; `aria-busy` on a loading region.
- **Contrast preference:** if `prefers-contrast: more` is honoured, state the token changes (values:
  `no-preference`, `more`, `less`, `custom` — MDN).

## 14. Anti-Patterns
Product-calibrated. Each carries the reason it was rejected *for this product*, not a generic ban.
**Do** — 10–12 concrete mandates, each with its rationale.
**Don't** — 10–12 bans: marketing aesthetics inside the product, card inflation, stat-card dashboards,
modals as connective tissue, two primaries side by side, a toolbar of unlabelled icons, hover-only
affordances, placeholder-as-label, whole-page spinners, `alert()`/`confirm()`, tiny type as a density
strategy, a disabled primary with no explanation — plus whatever *this* product is prone to.

## 15. Quick Reference & Verification Gate
Flat colour reference (role → hex, both modes) · flat type ramp · flat spacing + radius · a
component → token map (which semantic tokens each component consumes).
**Agent prompt block.** A verbatim-consumable preamble for a coding agent: role→hex list, type ramp,
spacing + radius, and the two worked prompts below — written as instructions, not prose. Prompts cite
**token names, never raw hex**; a prompt that names a hex value bypasses the §2 architecture.
**Example component prompts.** Two or three, in this spec's own voice, e.g.:
1. *[Primary surface]* — `surface.canvas` background, `radius.lg` corners, `space.6` padding; heading
   role in `text.primary`; one `accent.action` fill; `border.subtle` hairline; no shadow above level 1.
2. *[Data row]* — [density] row height; `tabular-nums` on every numeric cell; header, toolbar and
   pagination heights equal to row height; hover fill `surface.hover`; focus ring `border.focus`.
**Pre-ship checklist.** 1 Zero raw hex outside L1. 2 No token resolves to a component name.
3 Every contrast pairing computed, passing, unrounded. 4 Every semantic role has a value in every
shipped mode. 5 Every fetching surface has loading/empty/error/offline specified. 6 Every component row
lists disabled and loading states. 7 Row, header, toolbar and pagination heights agree. 8 Reduced-motion
variant written for every authored motion. 9 Every control keyboard-reachable with a visible focus
indicator. 10 Dark authored, not filtered, with border strength exceeding light's. 11 No unoverridden
stock library default inside a committed surface. 12 Nothing came from a marketing page.
13 The §9 brand-moment palette appears nowhere in the UI token layers.
```

---

## Adapter stub — `DESIGN-[framework].md`

*Phase 3 only, when the host has a stack to bind to. Keep it short.*

```markdown
# Implementation Adapter — [Framework] (for DESIGN.md v[n])
<!-- premium-web-design:adapter 1 -->
<!-- Every value below traces to DESIGN.md. Nothing new is introduced here. -->

## 1. Token host
[Where Layer 1 + Layer 2 live in this stack.]

## 2. Why mode and density live on the root element
[If the stack's theme directive is top-level only — Tailwind v4 `@theme` is — mode and density
attributes must be set on `:root` / `[data-theme]`, with `@theme inline` bridging, because `@theme`
cannot nest inside a selector or a media query.]

## 3. Component bindings
| DESIGN.md component | Host component | Overrides required | Stock defaults to replace |
|---|---|---|---|
[*A stock default surviving inside a committed surface is a lapse — see `component-consistency.md`.*]

## 4. Wiring
[Meta tag order, theme persistence, density persistence, import site of the token file.]

## 5. Validation
[The project's own typecheck / lint / build commands, and the expected zero-error result.]

## 6. Quick Start — token emission
The adapter is the only place framework syntax is permitted. Emitted from DESIGN.md §2–§6; nothing new
is introduced, and the block is regenerated when DESIGN.md changes — never hand-edited. Colour alone
is not enough: emit the type ramp, spacing scale and radii too, or consumers drift to arbitrary values.

```css
:root {
  /* L1 primitives — value-named, referenced only by L2 */
  /* L2 semantic roles — the only layer components consume */
  --surface-canvas: #…;
  --text-primary: #…;
  --accent-action: #…;
  /* + text ramp, spacing scale, radii */
}
```

```css
@theme inline { /* v4: `@theme` is top-level and cannot nest inside a selector; `inline` when a
                   variable references another variable */
  --color-canvas: var(--surface-canvas);
  --color-text-primary: var(--text-primary);
  --color-accent-action: var(--accent-action);
}
```
```

---

## Not found

- **A sourced padding/gutter table per density class.** The §5 values are this skill's calibration.
  Settled by: measuring three production systems per class.
- **A sourced contrast gate for `text.tertiary`.** WCAG exempts text that is "part of an inactive user
  interface component" from SC 1.4.3, so a 3:1 floor for muted text is house practice, not a standard
  threshold. Settled by: none; keep muted text ≥3:1 anyway.
- **Whether an org-tinted theme should ever ship.** No source addresses it. Treat as a product decision
  and freeze geometry so it stays reversible.

## Sources

All accessed 2026-10-05. Parenthetical = what the citation carries in this template.

- **Design Tokens Format Module 2025.10** — W3C Design Tokens Community Group. (Groups arbitrary; tools SHOULD NOT infer type/purpose; `$type` determinable or invalid; names case-sensitive excluding `$`/`{`/`}`/`.`; circular refs MUST error.) https://www.designtokens.org/TR/2025.10/format/
- **Registering custom properties in CSS** — MDN, Mozilla. (`@property` needs `syntax` AND `inherits` or the rule is invalid; `initial-value` computationally independent, no `%`/`em`; registered interpolates, unregistered animates discretely.) https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Properties_and_values_API/Registering_properties
- **`@layer`** — MDN, Mozilla. (Order beats specificity entirely; unlayered normal declarations outrank layered ones; `!important` reverses.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer
- **`color-scheme`** — MDN, Mozilla. (Repaints UA chrome only; does not theme the document; `<meta name="color-scheme">` before CSS to avoid a flash; `light-dark()` Baseline 2024 newly available.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme
- **`@container`** — MDN, Mozilla. (Baseline widely available; content-box measurement; `cq*` falls back to small-viewport units with no eligible container; style queries compare computed values.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@container
- **`font-variant-numeric`** — MDN, Mozilla. (`tabular-nums` activates figures "all of the same size, allowing them to be easily aligned like in tables"; Baseline widely available since January 2020.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variant-numeric
- **`prefers-reduced-motion`** — MDN, Mozilla. (Baseline widely available; scaling and panning large objects named as vestibular triggers.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
- **`prefers-contrast`** — MDN, Mozilla. (`no-preference` / `more` / `less` / `custom`; `custom` matches the `forced-colors: active` palette.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-contrast
- **WCAG 2.2** — W3C / W3C WAI. (SC 1.4.3 incl. the inactive-component exemption; SC 1.4.11 3:1 non-text contrast; SC 2.5.8 target size; SC 1.4.8 measure ceiling; SC 2.1.1; SC 2.4.7; SC 2.4.11.) https://www.w3.org/TR/WCAG22/ · https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html · https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html · https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html
- **Typography: type sets** — Carbon Design System, IBM. (Productive 14px base vs expressive 16px base.) https://carbondesignsystem.com/elements/typography/type-sets/
- **Data table** — Carbon Design System, IBM. (Header/toolbar/pagination heights match row height.) https://carbondesignsystem.com/components/data-table/usage/
- **Layout** — Shopify App Design Guidelines. ("Avoid changing information density within a single page.") https://shopify.dev/docs/apps/design/layout
- **Theming** — shadcn/ui. (Spacing tokens do not change on screen size; one base `--radius` with derived multipliers.) https://ui.shadcn.com/docs/theming
- **Theme variables** — Tailwind CSS v4, Tailwind Labs. (`@theme` top-level; `@theme inline` when a theme variable references another.) https://tailwindcss.com/docs/theme
- Three-layer taxonomy, density classes, whitespace budgets, wrapper-component rule — house rules: `references/craft-floor.md`, `references/tokens.md`, `references/component-consistency.md`.
