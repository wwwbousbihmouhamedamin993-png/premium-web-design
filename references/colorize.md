# Colorize — semantic colour, accent scarcity, surface steps

Enhance command. `colorize` decides what colour *means* in this product and makes every surface
obey it. The goal is not a nicer palette; it is that a mode change, a rebrand, or an accessibility
fix becomes one edit rather than a hunt.

## 1. Three token layers, always

| Layer | Question it answers | Who may use it | Example |
|---|---|---|---|
| **Primitive** | What colour is this, physically? | Token authors only | `--primitive-blue-600` |
| **Semantic** | What role does this colour play? | Any component | `--color-action-bg` |
| **Component** | How does *this component* use it? | That component only | `--button-primary-bg` |

**This is a house rule, not a standard.** The W3C Design Tokens Format Module states that token
*groups* carry no semantics — groups "are arbitrary" and tools "SHOULD NOT" use group names to
infer a token's type or purpose. A conforming implementation may call its layers `color`,
`palette`, or `theme1` and mean nothing by them. The primitive → semantic → component split exists
because it makes the right thing easy to type and the wrong thing grep-able.

Name by **role**, never by appearance: `--color-action-bg` survives a rebrand, `--blue-600` becomes
a lie, and `--card-bg` is worse than both — a component-named primitive cannot be remapped (it
spawns `--card-bg-nested`), duplicates the mode branch, and inverts the dependency so deleting a
component deletes colour decisions. Component-layer tokens are still legitimate as a **local alias
inside one component's scope**, never promoted to the shared layer.

## 2. Ship every surface as a pair

```
--color-surface:     /* the background            */
--color-on-surface:  /* text + icons sitting on it */
```

The pairing makes contrast enforceable by construction instead of by audit; Material's `on-*` slots
and `contentColorFor()` are the same commitment as an API. Pair `surface`/`on-surface`,
`surface-raised`/`on-surface-raised`, `surface-sunken`/`on-surface-sunken`, plus `border-subtle` and
`border-strong`.

**Contrast floor, and do not round it.** Body text ≥ 4.5:1; large text and non-text UI ≥ 3:1
(WCAG 2.2 SC 1.4.3 and 1.4.11). W3C is explicit that computed values "should not be rounded" —
4.499:1 fails and must not be rounded up. Large text is ≥ 24px, or ≥ 18.5px bold.

Status colours are four, never eight — success, warning, danger, info — each with `bg` / `on-bg` /
`border`. If you need a fifth, you need a second dimension (severity × lifecycle), not a fifth hue.
**Status is never colour alone** (SC 1.4.1): every state pairs colour with an icon, label, or shape.
NN/g reserves warm bright colours "for warnings or errors."

## 3. Accent scarcity

The accent is the scarcest resource in the interface, and the constraint is what makes it mean
something. NN/g's ceiling for uncomplicated designs: "limit your color use to 2 primary and 2
secondary colors," and "**If everything is contrasted, then nothing stands out**."

Applied to product:

- **One accent hue.** It marks the primary action, the active nav item, the focused field, the
  selected row. If it also paints every link, every chart series, and every badge, it marks nothing.
- **≤ 2 accent uses per viewport** [Focused/Standard]. Dense surfaces may carry one status accent
  for selection or an active filter — still one hue.
- **In dark mode, restrict further**: desaturated or lightened, because saturated hues glow on a
  dark ground and shift perceived hue.
- Count accent usages on one screen. More than roughly three visible is a finding.

Destructive is never the primary accent and never wears the same weight as a safe action.

## 4. Dark is not a filter

**Dark mode is a second theme with its own surface ramp, border weight, shadow behaviour, and accent
budget — not an inversion.** Light colours fed through `filter: invert()` or a lightness flip are
technically inverted and perceptually wrong, because dark mode's problems are not hue problems.

Material names the mechanism: "**Shadows are less effective in an app using a dark theme**, because
they will have less contrast with the dark background colors." Darken the ground and every depth cue
built from shadow vanishes silently. Hence:

| Property | Light | Dark | Why |
|---|---|---|---|
| Ground | White / near-white | Dark grey, **not pure black** | Shadow visibility and eye strain (`#0E0E10`–`#141416` for app chrome) |
| Surface ramp | Shadow + subtle tint | **Lighter surface per step** | M3 encodes elevation mainly as tonal overlays |
| Borders | Very subtle | **Stronger** than intuition suggests | Borders become the primary separator once shadows are gone |
| Accent | Saturated brand hue | Desaturated / lightened | Glow and hue shift on dark ground |
| Scrims | Black at low alpha | Black at **higher** alpha | Less light to darken |
| Charts | Series separated by hue | Need lightness separation too | Hue-only palettes collapse on dark |

**Elevation in dark mode is lightness.** The ramp must be monotonic — step 4 always lighter than
step 3 (`elevation-layers.md`).

Architecture: primitives once, semantics declared **twice**, components referencing semantics only.
No `.dark .button { … }` anywhere. In Tailwind v4 the mode dimension **cannot live in `@theme`** —
`@theme` variables must be top-level and cannot nest under media queries — so it lives in `:root` /
`.dark` with `@theme inline` bridging. Set `color-scheme` on `:root` (MDN: the browser looks to the
root element for the initial canvas and root scrollbars) and put `<meta name="color-scheme">` in
`<head>` **before any stylesheet**. The FOUC-free toggle is a synchronous, non-module, non-defer
inline script in `<head>` that updates both the root class and the meta tag's `content`, with CSS
defaulting to `prefers-color-scheme`.

**Forced colors is the test that catches shadow-only components:** `box-shadow` is forced to `none`
under `forced-colors: active`, so any component whose only depth cue is a shadow becomes completely
flat in Windows High Contrast. Borders must exist independently of shadows in **both** modes.

## 5. Register what animates or is queried

Wrap tokens read by `@container` style queries, transitioned, or read from JavaScript in
`@property` with **both** `syntax` and `inherits` — a rule missing either descriptor is invalid.
Keep the split visible with `@layer reset, tokens, primitives, semantic, components;` — layer order
beats selector specificity outright.

Radius and motion are audited alongside colour because all three are pure appearance
(`radius-motion-tokens.md`): one `--radius` base with `calc()` multipliers, `inner radius = outer −
padding` for nested corners, and asymmetric decelerate-in / accelerate-out motion.

## 6. Verify

- Grep for raw hex, `rgb(`, `hsl(`, `oklch(` outside the primitive file. Any hit is a defect.
- Grep for `--card-bg`, `--panel-bg`, `--modal-bg` in the shared layer.
- Every `--color-*-bg` has a matching `--color-*-on-bg`.
- Measure every text pair (≥ 4.5:1) and every icon, focus ring, control boundary (≥ 3:1) — record
  the computed ratio; do not eyeball it.
- Screenshot the surface ramp: step 4 must be lighter than step 3, always.
- Load with the OS dark and no stored preference — first paint must already be dark. Hard-reload
  with a stored `dark` preference while the OS is light; any white flash is a FOUC bug.
- Enable `forced-colors: active` and confirm no component becomes invisible.
- Check every chart series against its actual dark background, individually.
- Count accent usages per screen.

## 7. Detector advisories for this command

`gradient-text`, `ai-color-palette`, `cream-palette`, `dark-glow`,
`radial-gradient-background-halo`, and `low-contrast-text` are **failures at every class** —
marketing and neon defaults do not become correct by changing density. The colour-within-product rules carry no per-class exception.
Mechanics: `detector-integration.md`.

## Exit criteria

Three layers declared; no raw hex outside primitives; no component-named shared tokens; every
surface paired with its foreground; accent budget honoured and counted; dark mode a real second
theme with a monotonic ramp and stronger borders; no component CSS branching on mode; both modes
measured; forced-colors pass.

## Not found

- **A required number of colour tokens, a contrast headroom above the WCAG minimum for UI chrome,
  or an accent-usage ceiling.** The four-slot surface/raised/sunken/border set, the three-slot
  status set, and the ≤2-per-viewport accent limit are house rules. Settled by: a product decision
  in `DESIGN.md` plus measured ratios per token pair.
- **A canonical storage key or precedence order for pinned-vs-system theme, or a required number of
  steps in a dark surface ramp** (`dark-mode.md`). House conventions.

## Sources

Primary reference: `color-token-system.md` (three-layer model, role naming, surface pairing,
status slots, accent scarcity, relative-colour derivation, `@property`, `@layer`). Supporting:
`dark-mode.md` (the full mode remap, `color-scheme`, the FOUC-free toggle, forced colors),
`elevation-layers.md` (surface ramp, shadow mechanics, why borders are not a fallback),
`radius-motion-tokens.md`, `tokens.md`.

External pages cited above, all previously opened by this skill:

- Design Tokens Format Module (token groups arbitrary; tools SHOULD NOT infer type/purpose) — W3C
  Design Tokens Community Group. https://www.designtokens.org/TR/2025.10/format/ — accessed 2026-10-05.
- CSS Color Module Level 5 §3, §4.1, §4.9 (`color-mix()` defaults to Oklab; relative colour alpha
  defaults to the origin colour; OKLCH is perceptually uniform and chroma-preserving) — W3C.
  https://www.w3.org/TR/css-color-5/ — accessed 2026-10-05.
- Material Design 3 in Compose (`on-*` role pairing; `contentColorFor()`) — Android Developers.
  https://developer.android.com/develop/ui/compose/designsystems/material3 — accessed 2026-10-05.
- Dark theme (shadows less effective on dark; dark grey not black; elevation overlays lighten with
  elevation) — Material Components for Android.
  https://github.com/material-components/material-components-android/blob/master/docs/theming/Dark.md
  — accessed 2026-10-05.
- dark-mode guide (root `color-scheme`, `<meta>` before CSS, inline non-module non-defer script,
  listen for OS change) — GoogleChrome/modern-web-guidance.
  https://github.com/GoogleChrome/modern-web-guidance/blob/main/guides/user-experience/dark-mode/guide.md
  — accessed 2026-10-05.
- `color-scheme` · `prefers-color-scheme` · `forced-colors` · `prefers-contrast` · `light-dark()` ·
  `@layer` · `@property` — MDN. https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme ·
  https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/forced-colors —
  accessed 2026-10-05.
- Understanding SC 1.4.1 Use of Color · SC 1.4.3 Contrast (Minimum) · SC 1.4.11 Non-text Contrast —
  W3C WAI. https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html ·
  https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — accessed 2026-10-05.
- Visual Hierarchy in UX: Definition (colour ceilings; "do not rely only on color"; reserve red for
  warnings/errors) — Nielsen Norman Group.
  https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ — accessed 2026-10-05.

**House process, not sourced fact:** the three-layer mandate, the ≤2-accent budget, the dark-canvas
hex range for app chrome, the six-row "what changes per mode" summary's product-specific values, the
verification sequence, and the no-per-class-exception ruling in step 7. The DTCG statement that
groups are arbitrary is cited precisely so the house rule is not mistaken for a standard.