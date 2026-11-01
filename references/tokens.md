# Tokens — the three-layer architecture, registration, mode remapping, density, drift

The reference behind the `tokens` command. Covers why the architecture exists, how to register tokens
so the platform enforces their type, how light/dark and density remap through the same layer, and how
to find drift before it ships.

As-of: 2026-10-05.

## Why three layers — and what is actually standard

The W3C Design Tokens Format Module 2025.10 is explicit that this structure is not its business: token
groups "are arbitrary," and tools "SHOULD NOT" infer type or purpose from them. So the
primitive → semantic → component taxonomy is **this skill's rule**. What the spec *does* mandate:

- A token must have a determinable `$type` or it is invalid, and tools **MUST NOT** guess the type
  from the value.
- Names are **case-sensitive** and **MUST NOT** contain `$`, `{`, `}`, or `.`.
- **Circular references MUST be detected and reported as an error** — `space.md → space.lg → space.md`
  is a broken system, not a lazy one.

Adopt the layers because they make mode and density one switch. Not because a committee said so.

## Layer 1 — Primitive

Literal values, no meaning, referenced only by Layer 2. Name a primitive by its **value**, never its
use: `--palette-neutral-1000`, `--space-4`, `--radius-md`, `--duration-base`, `--ease-decelerate`.

`--card-bg`, `--tooltip`, `--input-border` are the classic trap — one value serving several roles,
guaranteed to diverge. `--surface-raised` is the role; `--palette-neutral-1000` is the value.

**Why OKLCH, and the two gotchas.** Relative colors in OKLCH resolve channels unitless, so percentage
arithmetic on them is invalid; alpha defaults to the origin colour's alpha; and Safari 16.4+ needs
explicit `deg` on hue, which forces an `@supports` fork (MDN, *Using relative colors*). Write light
ramps in OKLCH with explicit hue angles; let the hue axis carry the fork.

## Layer 2 — Semantic

The only layer a component consumes. Name by **role and intent** — every name answerable to "what job
does this do?", never "where does it live?". `surface.raised` is answerable. `dropdown.bg` is not.

```
--surface-canvas / raised / overlay / inset / hover / selected
--border-subtle / strong / focus
--text-primary / secondary / tertiary / disabled / on-action
--accent-action / on-action / subtle
--status-success / warning / danger / info
--space-inline-compact / --space-block-section     ← density-aware, see below
--radius-control / --radius-surface / --radius-overlay
--text-size-body / --row-height / --cell-padding-x / --density
```

**Every semantic token needs a value in every shipped mode.** A role with a light value and no dark
value is not "fine, it inherits" — it resolves to the light value in dark mode and fails contrast.
Enumerate the mode table; a hole in it is a bug.

## Layer 3 — Component (optional, narrow)

Only for deliberate deviation: `--button-primary-bg: var(--accent-action)`. A component token points at
a **semantic token or a primitive** — never at a sibling component's token, never at a raw literal. Two
components needing "the slightly different blue" get two semantic roles, not one shared component
token; sharing it means changing the first silently moves the second.

> **The consumption rule.** A component consumes semantic tokens only. A semantic token resolves to a
> primitive. Nothing skips a layer.

## Register the tokens that move

Unregistered custom properties are strings: the browser cannot interpolate them, so a transition snaps
at 50% instead of animating (MDN, *Registering custom properties in CSS*).

```css
@property --row-height {
  syntax: "<length>";   /* syntax AND inherits are both required, or the whole rule is invalid */
  inherits: true;       /* true: cascades down the tree. false: narrows recalculation */
  initial-value: 40px;  /* must be computationally independent — % and em are illegal */
}
```

- Registered properties interpolate smoothly; unregistered ones animate discretely.
- `inherits: false` narrows recalculation — right for a density marker read only at the root.
- **`initial-value` cannot use `%` or `em`**: `10px` and `2in` are computationally independent, `3em` is
  not, because it depends on the parent's font-size.
- **With `@container` style queries, registration is load-bearing**: style queries compare *computed*
  values, and an unregistered property's computed value is whatever token stream it happens to hold.
- Multiple valid `@property` rules for one name: last in stylesheet order wins; a JS
  `CSS.registerProperty()` with the same name beats the CSS one.

## Layer order

Declaration precedence is a separate axis from specificity, and `@layer` beats specificity **entirely**
— once layer order is established, specificity and order of appearance are ignored. Consequences:

- **Unlayered normal declarations outrank layered ones.** A stray un-layered rule in a component file
  will beat the whole design system.
- `!important` inverts layer order, so `!important` in a low layer beats a higher layer's normal
  declaration. Treat any `!important` in token or component CSS as a defect.
- Name every layer — anonymous layers (`@layer { … }`) can never be appended to later.

```
@layer reset, primitives, semantic, components, utilities;
```

Anything a consumer must override without `!important` belongs in the top layer.

**Where Tailwind fits.** v4's `@theme` **must be top-level**: it cannot nest inside a selector or a
media query. So `[data-theme="dark"]` and `[data-density="dense"]` remapping cannot live in `@theme`.
Put the mode/density *mapping* on `:root` / `[data-theme]` as ordinary custom properties and bridge
with `@theme inline` — the `inline` option makes utilities reference the theme variable's value
directly instead of the variable, which is what stops resolution collapsing to a fallback.

## Mode remapping

**Explicit ramps (default).**

```css
:root { --surface-canvas: var(--palette-neutral-0); }
[data-theme="dark"] { --surface-canvas: var(--palette-neutral-1000); }
```

Fully supported, fully inspectable, and the only mechanism to use when the host stack's theme directive
is top-level-only.

**`light-dark()` (progressive enhancement only).** MDN records it as **Baseline 2024, newly
available** — not widely available. Never the primary path. It also needs `color-scheme` to choose the
branch, and `color-scheme` "repaints UA-provided parts of the canvas… it does not affect the default
color scheme for the overall document" — a UA-chrome switch wearing a theming hat. Set
`<meta name="color-scheme">` in the head **before** the stylesheet to prevent a flash.

Native controls, scrollbars and form widgets follow `color-scheme`; the document's own surfaces do not.
Authoring dark mode means writing a second surface ramp with its own border strength — not filtering the
light one.

## The derived-scale pattern

Only two mechanisms ship. Both are "one base, derive the rest".

**One base token plus derived multipliers.** shadcn/ui exposes a single `--radius` and derives the whole
radius scale with `calc()`. Same shape for spacing, type and shadows:

```css
:root { --space-unit: 4px; }
--space-1: calc(var(--space-unit) * 1);
--space-4: calc(var(--space-unit) * 4);
```

**One base spacing value.** Tailwind exposes `--spacing: 0.25rem` and derives the entire spacing scale
from it.

**There is no standardized density or scale mode.** Both patterns ship *as* the mechanism, not as a
spec of one. Any density mode you build is yours — and it must be a token axis, not a media query:
Carbon's spacing tokens "do not change values based on the screen size," so rescaling on viewport is
the wrong lever, and it also breaks whenever the component lives in a sidebar whose width has nothing
to do with the viewport.

## Density mode

Density is a **declared property of a surface**, and it is the axis most often faked with type size. The
lever is row height, then column count, then leading.

```css
@property --density { syntax: "*"; inherits: true; initial-value: standard; }

:root {
  --density: standard;  --row-height: 40px;  --cell-pad-x: 16px;
  --text-size-body: 14px;  --space-inline: 8px;
}
[data-density="dense"] {
  --density: dense;     --row-height: 32px;  --cell-pad-x: 12px;
  --text-size-body: 13px;  --space-inline: 4px;
}
```

Rules that keep it honest:

- **Rescale row height, padding and gutter together.** Changing only the font size buys no density and
  costs legibility. A 13px tabular numeral in a dense table is correct; the same numeral in a Focused
  form is a defect.
- **Never mid-page.** "Avoid changing information density within a single page, otherwise your app can
  feel disjointed" (shopify.dev, *Layout*). Switching across routes with different jobs is legitimate.
- **Chrome follows rows.** Carbon requires the column header, toolbar, batch bar and pagination to
  match the table's row height. A 40px toolbar over 32px rows is a rhythm break.
- **Style queries let a component read the mode** — `@container style(--density: dense)` — but they
  compare computed values, so `--density` must be registered with `@property`.
- **Offer the switch as an accessibility affordance.** W3C's note on SC 2.5.8 endorses "a mechanism to
  control the density of layout… beneficial for a wide range of users," naming users with visual field
  loss explicitly.
- **`cq*` units are not density.** `cqi/cqw/cqmin/cqmax` fall back to small-viewport units when no
  container is eligible, silently. Use `@container` breakpoints for layout; use the density axis for
  compression.

## Drift detection

Four sweeps, all mechanical. Each should fail a review or a build.

**1. Layer skipping — raw literals in components.**
```
rg -n '#[0-9a-fA-F]{3,8}\b' src/ --glob '!src/styles/tokens*' --glob '!**/*.test.*'
rg -n 'rgba?\(|hsla?\(|oklch\(' src/components/
```

**2. Primitive leakage — components reading Layer 1.**
```
rg -n 'var\(--(palette|space-[0-9]|radius-[a-z]|duration-|ease-)' src/components/
```

**3. Cross-component references.**
```
rg -n 'var\(--[a-z]+-[a-z]+-[a-z]+-' src/components/ | grep -v -- '--<own-name>-'
```

**4. Unregistered animated tokens.** Any custom property used in a `transition` or `animation` should
be registered with `@property`, or it snaps instead of animating.

Then two rendered checks:

- **Mode parity.** Toggle the theme. Any element whose role has no dark value shows the light value —
  grep the mode table for holes first.
- **Density parity.** Toggle density on one Dense route and one Standard route. Row, toolbar and
  pagination heights must all move together, or the rhythm broke.

## Not found

- **A standardized density-mode token model.** No CSS or design-system specification defines one. W3C
  endorses *providing* a density control without specifying tokens. Settled by: none; the
  `:root` + `@property` pattern above is house mechanism.
- **A standardized primitive→semantic→component taxonomy.** The DTCG format module deliberately declines
  it. Settled by: none — ours is a design decision with a stated rationale.
- **A source for `--row-height: 40px / 32px` as a *whole-surface* density contract.** Carbon publishes
  row heights (xs 24 / sm 32 / md 40 / lg 48 / xl 64) for tables specifically; mapping them onto entire
  surfaces is this skill's judgement. Settled by: measuring the three classes against production
  consoles.
- **A rule for when a component token is warranted.** The narrow rule above ("deliberate deviation from
  the semantic default") is house guidance. Settled by: none — require the deviation to be named.

## Sources

All accessed 2026-10-05. Parenthetical = what the citation carries in this file.

- **Design Tokens Format Module 2025.10** — W3C Design Tokens Community Group. (Groups arbitrary; tools SHOULD NOT infer type/purpose; `$type` determinable or invalid; tools MUST NOT guess type from value; names case-sensitive excluding `$`/`{`/`}`/`.`; circular refs MUST error.) https://www.designtokens.org/TR/2025.10/format/
- **Registering custom properties in CSS** — MDN, Mozilla. (`@property` needs `syntax` AND `inherits` or the rule is invalid; `initial-value` computationally independent, no `%`/`em`; registered interpolates, unregistered animates discretely; `inherits:false` narrows recalculation; last rule in stylesheet order wins; JS `CSS.registerProperty()` beats CSS registration.) https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Properties_and_values_API/Registering_properties
- **`@property` at-rule** — MDN, Mozilla. (`initial-value` optional only for `syntax: "*"`; unknown descriptors ignored without invalidating the rule.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@property
- **`@layer`** — MDN, Mozilla. (Order beats specificity entirely; unlayered normal declarations outrank layered ones; `!important` reverses; anonymous layers cannot be appended to later.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer
- **`color-scheme`** — MDN, Mozilla. (Repaints UA-provided parts of the canvas only; does not theme the document; `<meta name="color-scheme">` before CSS to avoid a flash; `light-dark()` Baseline 2024 newly available.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme
- **Using relative colors** — MDN, Mozilla. (OKLCH relative-colour channels resolve unitless, so percentage arithmetic is invalid; alpha defaults to the origin's alpha; Safari 16.4+ needs `deg` hue units, requiring an `@supports` fork.) https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Colors/Using_relative_colors
- **`@container`** — MDN, Mozilla. (Baseline widely available; size queries measure the content box; `cqi`/`cqw`/`cqmin`/`cqmax` resolve to small-viewport units when no eligible container exists; style queries compare computed values.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@container
- **Theme variables** — Tailwind CSS v4, Tailwind Labs. (`@theme` generates utilities; `:root` for plain CSS variables; `@theme` top-level; `@theme inline` when a theme variable references another.) https://tailwindcss.com/docs/theme
- **Theming** — shadcn/ui. (Single `--radius` base with derived `calc()` multipliers; single `--spacing: 0.25rem` driving the scale; spacing tokens "do not change values based on the screen size.") https://ui.shadcn.com/docs/theming
- **Understanding SC 2.5.8 Target Size (Minimum)** — W3C WAI. (Density-control mechanism endorsed; users with visual field loss named.) https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- **Layout** — Shopify App Design Guidelines. ("Avoid changing information density within a single page.") https://shopify.dev/docs/apps/design/layout
- **Data table** — Carbon Design System, IBM. (Row sizes xs 24 / sm 32 / md 40 / lg 48 / xl 64; header, toolbar and pagination heights match row size.) https://carbondesignsystem.com/components/data-table/usage/
