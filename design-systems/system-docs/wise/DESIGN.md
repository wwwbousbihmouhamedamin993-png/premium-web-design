# Wise — System-Doc Standard Reference

Source: wise.design — Wise's design system ("a unified system of foundations, components, and
patterns built to make global money fair and accessible"). Load this spec for money-surface
state transparency and a consumer fintech brand system that stays loud without slop. For
Wise-the-product visual direction, see `design-systems/fintech/wise`.

## Why it matters here

Wise is the reference for the hardest brief in this skill's territory: a brand-bold consumer
fintech where every screen renders money. Its signature answer is *transparency as a design
token problem* — fees, rates, and arrival times are first-class UI elements with designed
states, not fine print.

## Token architecture

- Small, high-voltage palette: **Forest Green** (`#163300`, the deep brand ink) and **Bright
  Green** (`#9FE870`, the signature accent) carry the brand, with a white/cream canvas and a
  handful of supporting hues for semantics. Two brand colors, strict roles: dark green is
  canvas/ink for emphasis moments, bright green is the accent for actions and highlights —
  a live demo of this skill's accent-scarcity rule at consumer-brand intensity.
- The accent is *energetic on light and dark alike* because it's a tint, not a saturated
  primary — worth studying when a brand hue must survive both canvas polarities.
- Semantic money colors (success, pending, error) are separate from brand colors, so a green
  "arrived" state never blurs into brand-green chrome.

## Typography

Wise Sans (custom display face, tightly tracked, slightly quirky) for headlines; a neutral
text face (Inter-class) for body and data. The pairing rule to copy: *personality lives in
display sizes only* — the money numbers and transaction rows stay in the neutral face with
tabular numerals so amounts align and read as facts.

## Money-surface states (steal this)

Wise's pattern library treats transfer status as designed surfaces, not badges:
- **Settlement states are staged** — estimated arrival, in progress, arrived — each with its
  own visual weight, so the user's eye can triage at a glance.
- **Fee/rate transparency components** put the number, the comparison (mid-market rate), and
  the timestamp together in one component, making "what am I paying" legible before commit.
- **Long-running states** (a transfer taking days) keep the context alive with progress
  treatment rather than collapsing to a static checkmark.
This is the consumer-grade counterpart to the money-app patterns in the mobile skill — when
building billing, invoices, or transfer surfaces on the web, enumerate the same states.

## Components & states

Interactive states follow the tint model: hover/active shift surface steps, focus is a
high-contrast ring, disabled drops contrast while keeping hue. Borders and soft shadows are
used sparingly and generously rounded — the brand's softness is carried by radius and color
temperature, not by blur-heavy shadows (which keeps it fast on low-end devices).

## Illustration & imagery

Wise's system treats illustration as a brand channel with palette-bound constraints: floating
hands and objects in brand hues, always on canvas colors, never stock photography. The
transferable rule: bind illustration to the token palette so brand energy can't drift into
inconsistent art direction.

## Documentation practice

wise.design is organized as foundations → components → patterns with visible design-team
commentary ("inspiration from the design team") — the rationale travels with the rule. Copy
the practice: a rule plus one sentence of *why* survives handoff; a rule alone invites
relitigating.

## Verify at source

wise.design is public; exact supporting hexes (yellows/blues) and Wise Sans metrics should be
re-verified there before a build depends on them — the two brand greens above are stable
public brand values. Structural rules above are stable.
