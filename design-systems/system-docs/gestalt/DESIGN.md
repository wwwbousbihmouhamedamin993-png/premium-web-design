# Gestalt (Pinterest) — System-Doc Standard Reference

Source: gestalt.pinterest.systems — Pinterest's design system, dark-first, powering a
consumer-scale product. Load this spec for dark-first token structure and the per-component
accessibility + localization documentation pattern. Do not load it for visual direction.

## Why it matters here

Pinterest ships dark mode as a *first-class default*, not a theme bolt-on, and Gestalt's docs
treat accessibility and localization as sections every component must have — the two doc
practices most product teams skip, both directly load-bearing for this skill's non-negotiables.

## Dark-first token architecture

- Semantic tokens (`color-background-default`, `color-text-default`, `color-text-subtle`,
  `color-border-container`…) resolve per theme; components consume only semantics.
- Dark is the reference theme: light mode is the derived mapping. Practical consequence — if a
  semantic token can't be resolved in dark mode, it's not a real semantic; that's the audit
  question to ask of any token set.
- Brand red `#E60023` is treated as an *accent with a budget* — interactive emphasis only,
  never ambient decoration — the same scarcity rule this skill's `colorize` playbook enforces.
- Elevation in dark mode comes from surface luminance steps plus 1px borders, not shadows —
  matching the craft floor's rule that depth holds on dark via contrast, not blur.

## Typography

Pinterest Sans, weights 400/500/600/700, numeric ramp from 12px captions through 16px body to
display sizes with paired line heights. Color contrast tiers (`default` / `subtle` /
`disabled`) are tokens, so "secondary text" is a resolved color, not an ad-hoc gray.

## Component state conventions

Interactive components document hover, active, focus-visible, selected, disabled, and (where
relevant) error states with token-driven treatments. Hover is a subtle surface tint; selected
persists through hover without a separate color; focus uses a visible ring distinct from
selection. The Gestalt discipline to copy: **state treatments are resolved from semantic
tokens, so a new theme can't desynchronize states from surfaces.**

## Accessibility documentation (steal this practice)

Every component page carries an Accessibility section covering roles, keyboard behavior, and
screen-reader announcements, plus ARIA props exposed as first-class component props. Use as the
bar when running `audit`/`a11y`: a component whose docs can't state its announcement behavior
isn't done.

## Localization documentation (steal this practice)

Every component page documents localization constraints: minimum sizes under string expansion
(German/Arabic growth), RTL mirroring behavior, locale-aware number and date handling where
relevant. Wire into `i18n-rtl` work: enumerate per component which strings can expand and what
wrapping rule applies, instead of discovering it in translation QA.

## Motion

Tokenized durations (~100–500ms) with a small easing set, applied to entrance/exit and state
transitions; a `useReducedMotion` hook makes reduced-motion a first-class API consumed per
component, not a global afterthought — the enforcement mechanism this skill's `animate`
playbook asks for.

## Verify at source

**Access note:** Gestalt's foundations pages moved behind Okta sign-in after the last public
snapshot — this spec reflects that last public state; verify current values manually in a
browser if a build needs exact Pinterest Sans metrics or semantic-token hexes. The dark-first
structure and the per-component doc requirements above are stable.
