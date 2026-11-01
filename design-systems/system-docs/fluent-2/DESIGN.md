# Fluent 2 (Microsoft) — System-Doc Standard Reference

Source: fluent2.microsoft.design — Microsoft's cross-surface design system (web, Windows, iOS,
Android). Load this spec for the state-layer model, the type ramp, and the double-ring focus
treatment. Do not load it for visual direction.

## Why it matters here

Fluent 2 is the best public example of a *state-layer* system: instead of authoring a new
background color per component state, every interactive surface gets a translucent overlay whose
opacity encodes the state. One mechanism, every component, themable for free.

## Token architecture

Three layers, matching this skill's non-negotiable #5:

1. **Global tokens** — raw ramps: brand color ramp in steps 10–160, neutral ramp, plus duration
   and curve primitives. Never used directly in components.
2. **Alias tokens** — semantic roles (`colorNeutralForeground1`, `colorBrandBackground`,
   `colorNeutralBackground1`…`6` for surface steps). Typography aliases double as the ramp:
   `caption1`/`caption2` (12px), `body1`/`body2` (14/16px), `subtitle1`/`subtitle2` (20px),
   `title1`–`title3` (20/24/28px), `titleLarge` (40px), `display` (68px).
3. **Component tokens** — per-component overrides (`buttonMinWidth`, `toastTitleFontSize`) so a
   single component can be tuned without touching aliases.

Brand color is a *slot*, not a color: swap the brand ramp and every alias re-derives. Theme
switching is alias re-mapping only.

## The state-layer model (steal this)

For every interactive component on a neutral surface:

- **Hover:** brand ramp step 10 as a translucent overlay (~5% alpha over the resting surface).
- **Pressed:** brand step 30 (~10–14% alpha) — a visibly darker layer, not a shadow change.
- **Selected:** brand step 10 as a solid-tinted background, persisting while hovered.
- **Disabled:** grayed foreground + border, background unchanged — state reads from content
  contrast, not surface mutation.

The mechanism generalizes: define one overlay recipe per state, apply it through the alias
layer, and any new component inherits correct states before its first design review.

## Focus treatment (steal this)

Double-ring focus, unlike single-ring web defaults: a 2px inner stroke in the foreground color
plus a 2px outer stroke in the background color. Result: visible on any canvas, light or dark,
without per-theme tuning. Implement as one `box-shadow` pair from two tokens
(`strokeColorFocusInner`, `strokeColorFocusOuter`), never per-component colors.

## Radius, spacing, elevation

- 4px base grid; spacing aliases (`spacingS` 8px, `spacingM` 12px, `spacingL` 16px, `spacingXL`
  20px).
- Radius is a named scale, not a per-component value: `small` 4px, `medium` 6px, `large` 8px,
  `xLarge` 12px, `circle` full. Components consume the scale.
- Elevation uses shadow + border pairs per level (shadow16 for dialogs, shadow8 for cards,
  shadow2/4 for menus) — shadows are always paired with a 1px border so they hold on dark.

## Motion

The live motion doc states four principles — motion must be **functional, natural, consistent,
and appealing** — and builds its guidance around duration and easing choice. Duration tokens
from 50ms (ultra-fast: hovers, toggles) through 100ms (fast: buttons, reveals) to 250–400ms
(entrances of large surfaces). Two curve families only: a decelerate curve for entrances and an
accelerate curve for exits — the same rule this skill's `animate` playbook enforces. Entrances
translate a few px + fade; never scale-spring.

## Density

Fluent UI React ships a compact mode driven by component tokens (row heights drop from 44px to
32px, control heights from 32px to 24px). Density is a mode over the alias layer, not a fork —
the same mechanism this skill's density classes expect.

## Documentation practice

Every component doc lists its tokens explicitly and marks which states it implements. Use as
the bar when running `audit` on states: if a component's state list can't be read off its spec,
the spec is incomplete.

## Verify at source

Brand ramp hexes (web default brand-80 ≈ `#0F6CBD` at transcription) and exact overlay alphas
are themable and versioned — re-verify at fluent2.microsoft.design before a build depends on
them. Motion principles verified against the live docs; structural rules above are stable.
