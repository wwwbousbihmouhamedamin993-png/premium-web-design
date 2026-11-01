# Base Web (Uber) — System-Doc Standard Reference

Source: base.uber.com — Uber's React design system (Base Web) used across the driver, eater,
and internal enterprise products. Load this spec for the style-extension API and enterprise
density handling. Do not load it for visual direction.

## Why it matters here

Base Web's defining answer is different from every other system here: instead of theming
layers, it gives every component an *overrides API* — a structured escape hatch per sub-part —
so product teams customize any component's internals without forking it. It is the best public
example of "the component library supplies the how, never the direction" made literal in code.

## The overrides API (steal this shape)

Every component accepts overrides addressed to its named sub-parts (`Root`, `Input`,
`InputWrapper`, `Thumb`…), each taking `style`, `props`, or a full component replacement. The
discipline worth copying into any wrapper-component strategy:

- Customization targets *named parts*, not brittle selectors — no descendant-selector soup.
- Token-consumed styles are the default path; full replacement is the documented last resort.
- The component's spec enumerates its parts, so "where can I restyle this?" is a documentation
  question, not a source-diving question.

## Token architecture

Two layers, flatter than Fluent or Spectrum: primitives (Uber Move type family, monochrome
grays, the accent ramp, semantic colors `negative` / `warning` / `positive` / `accent`) and
component-level style objects. Uber's brand is nearly monochrome — black `#000000` on white
with the accent reserved for interactive affordances — which keeps the alias layer small and
proves you don't need a 15-step brand ramp to ship an enterprise system.

## Typography

Uber Move (display) / Uber Move Text (body) — one family split by role. Numeric size steps
(`font-100` ≈ 12px up through `font-950` display sizes) with paired line heights; weights 400 /
500 / 600. Mono for numerals in data contexts.

## Density (enterprise consoles)

Base Web's Table and data components are the reference for this skill's Dense class done in a
component library: row heights tokenized (compact ≈ 36px, standard ≈ 48px+ with denser sub-48
options), 13–14px body, 1px row separators instead of card shadows, and column-level state
handling (sorting, selection, pinned columns) enumerated in the spec rather than improvised.

## State conventions

Hover/active are token-driven tints (a few percent of ink over the surface — same state-layer
idea as Fluent, expressed as filled tokens). Focus is a high-contrast outline with offset,
always visible under keyboard interaction. Disabled drops contrast but keeps hue. Invalid
fields carry both border color *and* a message slot — color alone never carries the error.

## Documentation practice

Base Web docs show, per component, the accessibility contract (roles, keyboard map) and a live
"overrides" example for every sub-part. The pairing is the practice: every extension point is
documented *with* its a11y obligations, so customization can't silently break keyboard support.

## Verify at source

Exact size-step px values and current type metrics — re-verify at base.uber.com before a build
depends on them. The overrides architecture, monochrome alias strategy, and density mechanics
above are stable.
