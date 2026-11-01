# Lightning Design System (Salesforce SLDS) — System-Doc Standard Reference

Source: lightningdesignsystem.com — Salesforce's system for the world's largest enterprise CRM
surface. Load this spec for enterprise density, token versioning/deprecation discipline, and
utility-class architecture at scale. Do not load it for visual direction.

## Why it matters here

SLDS is the canonical proof that the Dense class can be a *system* property rather than a
per-screen hack: thousands of admin-console screens, one density model, one token pipeline —
including a formal versioning and deprecation policy no other public system documents as well.

## Token architecture and versioning (steal this)

- CSS custom properties in the `--slds-*` / `--slds-c-*` (component-scoped) namespaces, in the
  same primitive → alias → component layering this skill mandates (non-negotiable #5).
- Tokens are *versioned*: each release documents additions, deprecations, and removals, and
  deprecated tokens ship with their replacement named inline. This is the reference to copy
  whenever this skill's `tokens` command establishes or repairs a token system — a token set
  without a deprecation path becomes unrefactorable within a year.
- Hook into `migrate`-style work: deprecation lists are the changelog a refactor needs.

## Density as a system property (steal this)

- Row heights and control heights are tokenized density tiers (compact ≈ 25–32px rows,
  standard ≈ 32–44px depending on surface), selectable per container — a table can be Dense
  inside a Standard page without forking styles.
- 12–13px body with 1px separators and zebra-free row hover tints; density comes from row
  height and padding tokens, never from shrinking type below the ramp.
- This is the implementation model behind this skill's density-class table: declare the class,
  resolve it through tokens, and forbid call-site magic numbers.

## Typography

Salesforce Sans with a fixed numeric ramp (12px body up to 28–32px headers) where each step
pairs size + line height; weight 700 for emphasis instead of size jumps inside tables. Small
caps / uppercase 11–12px section labels are the standard enterprise "eyebrow" pattern.

## State conventions

Hover/active as brand-tinted backgrounds from tokens; selected rows carry a persistent tint
plus a left accent border; focus uses a high-contrast ring with offset and is documented
per-component alongside keyboard maps. Disabled keeps hue at reduced contrast. Errors combine
border color, icon, and message text — never color alone.

## Utility-class layer

SLDS ships a utility-class layer (spacing, text, grid) alongside components. The governance
rule worth stealing: utilities are for *layout and one-offs*, components for *behavior-bearing
UI* — and the docs say which to prefer, so the utility layer doesn't swallow the system.

## Documentation practice

SLDS documents every component's anatomy (regions, slots), variants, and states with usage
guidance per variant, and marks components "(future)" when planned but unbuilt — public
honesty this skill's own non-negotiables cite. Anatomy diagrams are the transferable artifact:
when specing a complex component (modal, card, path), draw the region breakdown before the
pixels.

## Verify at source

Exact hexes (brand blue ≈ `#0176D3` at transcription) and density pixel values shift across
SLDS 2 releases — re-verify at lightningdesignsystem.com before a build depends on them. The
versioning policy, density model, and anatomy-doc structure above are stable.
