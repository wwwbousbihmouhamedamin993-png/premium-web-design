# Spectrum (Adobe) — System-Doc Standard Reference

Source: spectrum.adobe.com — Adobe's design system across Creative Cloud, Experience Cloud, and
Document Cloud. Load this spec for t-shirt scaling, semantic color slots, and the strongest
public per-component accessibility documentation. Do not load it for visual direction.

## Why it matters here

Spectrum's defining answer is *scaling by construction*: every component is sized in `em`
against a t-shirt root scale, so an entire screen can change density by changing one root
token. That is the cleanest public implementation of this skill's density-class idea.

## T-shirt scale system (steal this)

Components ship in `s / m / l / xl` (and `cta` for buttons). A component's internal paddings,
font sizes, icon sizes, and control heights are all `em`-based off its own size, so one root
font-size token re-scales everything beneath it. Consequences to copy:

- No component carries a pixel font size; it carries a relative token.
- Density changes are a root-token decision, reviewable in one place.
- Mixed-density layouts (a Dense table inside a Standard page) stay type-consistent because
  both derive from the same ramp at different roots.

## Color: ramps, slots, semantics

Adobe grounds the color system explicitly in **visual perception, inclusive design, and
accessibility** (per the live Color fundamentals page) — ramps exist to make contrast
guaranteeable, not to look calibrated. Consequences worth copying: pick semantic slots before
hexes, and treat any color choice that can't state its contrast outcome as undecided.

- Color ramps (gray, red, orange, yellow, chartreuse, celery, green, seafoam, cyan, blue,
  indigo, purple, fuchsia, magenta) in numbered steps 100–1400 — primitives only.
- **Semantic slots** are the working vocabulary: `negative` (error red), `notice` (warning
  yellow), `positive` (success green), `info` (blue), each resolved to a ramp step per theme.
- Visual states also ride slots: hover/active variants are explicit darker/lighter steps, and
  disabled reduces contrast while keeping hue — never gray-out-by-opacity.

## Typography

Adobe Clean / Adobe Clean Han, with numeric sizes (`text-size-75` ≈ 12px, `text-size-100` ≈
14px, `text-size-200` ≈ 16px, `text-size-300` ≈ 18px, up through display sizes). The ramp is
line-height-paired: every size token ships with its leading, so call-site leading decisions
don't exist. Emphasize via weight 700, never via a second family.

## State matrix discipline (steal this)

Spectrum documents, per component, the full set: default, hover, active, focus-visible,
keyboard focus, selected, disabled, read-only, invalid, mixed (for tri-state checkboxes),
placeholder. Selection and focus are *separate* states that can coexist — a selected item with
keyboard focus shows both treatments. When building any component here, enumerate against this
list; anything unlisted gets designed before build, per non-negotiable #4.

## Focus treatment

A 2px solid focus ring in a static blue reserved for focus only — its color never appears in
brand UI, so the ring is unambiguous everywhere. Applied with 1px offset outside the component
edge. `focus-visible` semantics: pointer interactions never show the ring.

## Accessibility documentation (steal this practice)

Every component page carries an Accessibility section written as implementation requirements:
expected ARIA roles, keyboard interaction tables (key → behavior), and screen-reader
announcement expectations. The keyboard tables are the transferable artifact — when building a
widget (menu, combobox, tabs), write the key→behavior table first and treat it as the spec.

## Documentation practice

Spectrum separates *token* docs (what exists) from *usage* docs (when to use which level) and
marks deprecated tokens with their replacement inline. Adopt the pairing: a token without a
usage note is unshippable.

## Verify at source

Exact ramp hexes and the current Adobe Clean metrics drift with releases — re-verify at
spectrum.adobe.com before a build depends on them. The scale mechanics, state list, and doc
structure above are stable.
