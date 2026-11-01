# Geist (Vercel) — System-Doc Standard Reference

Source: vercel.com/geist — Vercel's design system (Geist Sans, Geist Mono, and the component
kit). Verified against the live docs. Load this spec for monochrome discipline, class-based
typography consumption, and perceptual color spaces. For Vercel-the-product visual direction,
see `design-systems/devtools/vercel`.

## Why it matters here

Geist is the strongest public proof that a near-monochrome system can carry an entire product
line: color exists, but *ink and surface do the design work*, and every rule below serves
legibility and speed first.

## Token architecture

- **10 color scales**, each a named ramp from 100 to 1000 (plus extended steps to 1200 for
  reds/blues), published in **P3 with sRGB fallbacks** — Geist is a public exemplar of
  gamut-aware tokens: define the wide-gamut value and the fallback together, never ship one.
- **Six-step gray scale** with explicit interaction derivations: hover and active are
  *documented members of the scale*, not ad-hoc opacities. Copy the idea — an interaction
  tint that exists as a named token can't drift per component.
- **Two background colors** (light and dark) and everything else derives from the gray scale —
  surfaces are steps of one ramp, which is why dark mode costs Geist nothing.

## Typography (verified)

Geist Sans / Geist Mono, consumed as **Tailwind classes that pre-set the full combination of
`font-size`, `line-height`, `letter-spacing`, and `text-wrap`** — text-wrap (balance/pretty)
is baked into the class, so headline balancing (this skill's typeset rules) happens by
construction instead of per-element. Text styles run from `text-xs`-scale captions through
display sizes with tightened tracking as size grows. Steal the packaging: a type ramp that
ships as one class per role eliminates the four-property drift problem.

## Grid & layout (verified)

Geist's grid doc leads with a *non-responsive* baseline grid with auto-flowing cells before
adding responsive behavior — layout is composed from cells, not bespoke flexbox. Fixed
container widths with 1px hairline dividers between cells; depth comes from borders, never
shadows (matching the monochrome ink-on-surface model).

## Components & states

Geist's component set (Button, Input, Modal, Drawer, Toast, Tabs, Segmented Control, Select,
Switch, Badge, Avatar,…) uses the same 6-step gray mechanics: hover shifts one gray step,
active shifts two, focus is a visible ring, disabled drops contrast while keeping hue. No
color enters until semantics demand it (error red, warning amber, success green).

## Motion

Geist ships motion guidance with its components (drawer/modal transitions, toast timing) in
the restrained band — 150–300ms, decelerate entrances, transform/opacity only. Use as the
calibration point for the *restrained instrument* posture: Geist motion is what "fast" feels
like, this skill's marketing motion reference is what "alive" feels like.

## Documentation practice

Docs separate foundations (Colors, Typography, Grid, Icons, Materials) from components, and
each foundation page states its rules as mandatory usage guidance. The section list itself is
the bar: if a project's DESIGN.md lacks a Grid or Icons foundation, that's a gap to name.

## Verify at source

vercel.com/geist is fully public and current — re-verify exact hexes and class names there
before a build depends on them. Structural rules above are stable.
