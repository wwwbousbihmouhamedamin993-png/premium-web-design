# Colour token system

A colour token system exists to make one decision once — *what colour means in this product* — and
have every surface obey it. The failure mode is the opposite: a palette of pretty hex values each
component reaches for directly, so a mode change, rebrand, or accessibility fix becomes a hunt
across every stylesheet.

## The three-layer model is a HOUSE RULE, not a standard

State this plainly to anyone who asks "is this what the spec says?": **it is not.** The W3C Design
Tokens Format Module (2025.10) is explicit that token *groups* carry no semantics: groups "are
arbitrary," and tools "SHOULD NOT" use group names to infer a token's type or purpose (W3C Design
Tokens Community Group, *Design Tokens Format Module*, accessed 2026-10-05). A conforming
implementation is free to call its layers `color`, `colour`, `palette`, or `theme1` and mean nothing by
them. So the primitive → semantic → component split below is **this skill's mandated house rule**,
adopted because it makes the right thing easy to type and the wrong thing grep-able.

| Layer | Question it answers | Who may use it | Example |
|---|---|---|---|
| **Primitive** | What colour is this, physically? | Token authors only | `--primitive-blue-600: oklch(0.55 0.17 255)` |
| **Semantic** | What role does this colour play? | Any component | `--color-action-bg: var(--primitive-blue-600)` |
| **Component** | How does *this component* use it? | That component only | `--button-primary-bg: var(--color-action-bg)` |

## Role-based naming, and the trap

Name by **role**, never by appearance. `--color-action-bg` survives a rebrand. `--blue-600` becomes a
lie the moment the brand hue shifts, and `--card-bg` is worse than both.

**Why a component-named primitive is a trap.** The moment a token is named for a component, three
things happen at once:

1. **It cannot be remapped.** `--card-bg` implies the card's background, so when a card appears on a
   nested surface you need `--card-bg-nested` — and now the card owns surface knowledge it should have
   borrowed.
2. **It duplicates the mode branch.** If `--card-bg` is declared in `:root` and again in `.dark`, every
   new card means two more declarations and two more chances to miss one.
3. **It leaks the wrong direction of dependency.** Components depend on semantics; if components own
   colour, the palette depends on the component inventory, and deleting a component deletes colour
   decisions.

Component-layer tokens are still legitimate — but only as a *local alias* inside one component's scope,
so a reviewer can see which semantic roles that component consumes. Never promote one to the shared
layer.

## Semantic surface / foreground pairing

Ship every surface as a **pair**, never a lone background:

```css
--color-surface:     /* the background            */
--color-on-surface:  /* text + icons sitting on it */
```

The pairing rule makes contrast enforceable by construction instead of by audit. Material makes the same
structural commitment with its `on-*` slots: "Use on-primary on top of primary, and on-primary-container
on top of primary-container" (Android Developers, *Material Design 3 in Compose*, accessed 2026-10-05).
Android's `contentColorFor()` exists purely to look up the correct foreground for a given surface — the
pairing *is* the API.

| Pair | Purpose |
|---|---|
| `surface` / `on-surface` | Default page and card background |
| `surface-raised` / `on-surface-raised` | Menus, popovers, dialogs |
| `surface-sunken` / `on-surface-sunken` | Wells, inset code blocks, table stripes |
| `border-subtle`, `border-strong` | Separating without shouting; focused/active boundaries |

**Contrast floor, and do not round it.** WCAG 2.2 requires 4.5:1 for text (AA), 3:1 for large text and
non-text UI (AA), and 7:1 for AAA; 4.499:1 fails and must not be rounded up to pass (W3C, *WCAG 2.2*,
accessed 2026-10-05). Non-text contrast (SC 1.4.11) governs icon glyphs, focus indicators, and control
boundaries at 3:1 — W3C's worked examples measure a focus ring at exactly 3:1 and a down-arrow icon at
4.7:1 (W3C WAI, *Understanding SC 1.4.11*, accessed 2026-10-05).

## Status colours: four, never eight

Success, warning, danger, and info each need **three** slots on the same pairing logic:

```
--color-danger-bg  --color-danger-on-bg  --color-danger-border
```

- **Status is never the only carrier.** WCAG SC 1.4.1 Use of Color governs this; every status must be
  reinforced by text, icon shape, or position. NN/g makes the same point about hierarchy: "Do not rely
  only on color to communicate visual hierarchy" (Nielsen Norman Group, *Visual Hierarchy in UX:
  Definition*, accessed 2026-10-05).
- **Danger red is reserved.** NN/g: "Reserve warm bright colors, like red, for warnings or errors."
- **No invented statuses.** If you need a fifth, you need a second dimension (severity × lifecycle), not
  a fifth hue.

## Accent scarcity

The accent is the scarcest resource in the interface, and the constraint is what makes it mean
something. NN/g's ceiling for uncomplicated designs: "limit your color use to 2 primary and 2 secondary
colors," and "Don't use too many contrast variations. Use no more than 3 contrast variations… If
everything is contrasted, then nothing stands out" (NN/g, *Visual Hierarchy*, accessed 2026-10-05). In
product, **one accent**: it marks the primary action, the active nav item, the focused field, the selected
row. If the accent also paints every link, every chart series, and every badge, it marks nothing. In dark
mode, restrict it further — see `dark-mode.md`.

## Deriving ramps without hand-writing hex

Author primitives with relative colour or `color-mix()` so one hue yields a whole ramp. `color-mix()`
defaults to **Oklab** when no interpolation method is given (W3C, *CSS Color Module Level 5*, §3,
accessed 2026-10-05) — so `color-mix(in oklab, var(--brand) 25%, black)` is the default, not the
exception. MDN's own reasoning: `sRGB` "is neither linear-light nor perceptually uniform, and produces
poorer results such as overly dark or grayish mixes" (MDN, *Creating color palettes with the CSS
color-mix() function*, accessed 2026-10-05). In OKLCH, relative syntax gives the perceptual lightness
lever: `oklch(from var(--base) calc(l + 0.15) c h)` (MDN, *`oklch()`*, accessed 2026-10-05). OKLCH is
"both perceptually uniform and chroma-preserving," which is exactly what ramp generation needs (W3C,
*CSS Color 5*, §4.9).

**Four traps, all load-bearing** (MDN, *Using relative colors* and *CSS Color 5* §4.1, accessed 2026-10-05):
channel keywords resolve to **unitless numbers**, so percentage arithmetic is invalid (`calc(l + 10%)`
fails; use `calc(l + 0.1)`); an omitted alpha defaults to **the origin colour's alpha**, not opaque, so a
derived hover state can silently inherit transparency; `@supports` **cannot test through a custom
property** — probe the function form directly; and Safari 16.4+ requires explicit `deg` in hue
arithmetic (`calc(h + 180deg)`), forcing an `@supports` fork for hue-derivation patterns.

## Register the tokens that need to animate or be queried

Wrap tokens read by `@container` style queries, transitioned, or read from JavaScript in `@property` with
**both** `syntax` and `inherits` — a rule missing either descriptor is invalid (MDN, *Registering
properties*, accessed 2026-10-05). Registration also converts a discrete, unregistered custom property
into one that interpolates smoothly and is validated at computed-value time. Plain custom properties are
fine for colours that only CSS reads and never animate.

Keep the split visible in the cascade with `@layer reset, tokens, primitives, semantic, components;` —
layer order beats selector specificity outright, and unlayered normal declarations outrank every layered
normal declaration (MDN, *`@layer`*, accessed 2026-10-05). Component CSS appended later still wins by
position instead of `!important`.

## Checkable rules

- Grep for raw hex, `rgb(`, `hsl(`, `oklch(` outside the primitive file. Any hit is a defect.
- Grep for `--card-bg`, `--panel-bg`, `--modal-bg` style names in the shared layer. Component names
  there are a defect.
- Every `--color-*-bg` has a matching `--color-*-on-bg`. Unpaired backgrounds are defects.
- Every text pair measures ≥ 4.5:1; every icon, focus ring, control boundary ≥ 3:1. Record the measured
  ratio — do not eyeball it.
- No status is carried by hue alone.
- Count accent usages on one screen. More than roughly three visible is a finding.

**Not found:** no primary source specifies a required number of colour tokens, a required contrast
headroom above the WCAG minimum for UI chrome, or an accent-usage ceiling. The four-slot
surface/raised/sunken/border set, the three-slot status set, and the accent ceiling are house rules. What
would settle them: a product decision recorded in `DESIGN.md`, plus measured contrast ratios per token
pair.

## Sources

- Design Tokens Format Module (token groups arbitrary; tools SHOULD NOT infer type/purpose) — W3C Design Tokens Community Group. https://www.designtokens.org/TR/2025.10/format/ — accessed 2026-10-05
- CSS Color Module Level 5 §3, §4.1, §4.9 (`color-mix()` defaults to Oklab; relative colour alpha defaults to the origin colour; OKLCH is perceptually uniform and chroma-preserving) — W3C. https://www.w3.org/TR/css-color-5/ — accessed 2026-10-05
- `color-mix()` · `oklch()` (relative syntax; channels resolve to unitless numbers; alpha defaults to the origin colour) · Using relative colors (Safari 16.4+ `deg` requirement; `@supports` fork) · Creating color palettes with the CSS `color-mix()` function (sRGB is neither linear-light nor perceptually uniform) · `@property` / Registering properties (`syntax` + `inherits` required; interpolation on registration) · `@layer` (unlayered normal outranks layered normal) — MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/color-mix · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/oklch · https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Colors/Using_relative_colors · https://developer.mozilla.org/en-US/docs/Web/CSS/blog/color-palettes-css-color-mix/ · https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Properties_and_values_API/Registering_properties · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer — accessed 2026-10-05
- Web Content Accessibility Guidelines (WCAG) 2.2 (SC 1.4.1, 1.4.3, 1.4.6, 1.4.11 contrast thresholds; do not round) — W3C. https://www.w3.org/TR/WCAG22/ — accessed 2026-10-05
- Understanding SC 1.4.11 Non-text Contrast (3:1 for icons, focus indicators, control boundaries; worked examples at 3:1 and 4.7:1) — W3C Web Accessibility Initiative. https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — accessed 2026-10-05
- Material Design 3 in Compose (`on-*` role pairing; `contentColorFor()`) — Android Developers. https://developer.android.com/develop/ui/compose/designsystems/material3 — accessed 2026-10-05
- Visual Hierarchy in UX: Definition (2 primary + 2 secondary colour ceiling; ≤3 contrast variations; "Do not rely only on color"; reserve red for warnings/errors) — Nielsen Norman Group. https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ — accessed 2026-10-05
