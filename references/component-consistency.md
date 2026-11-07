# Component consistency

A design system rots from the inside: not from a missing token, but from a second button, a third
radius, and a wrapper that quietly reverts to the library default. This file is the discipline that
keeps one committed surface looking like one product.

As-of: 2026-10-05.

House process: the extraction/wrapper rules below are this skill's own. The CSS and WCAG facts are
sourced.

---

## The wrapper-component rule

> **A stock default surviving inside a committed surface is a lapse.**

Once `DESIGN.md` commits to a direction, every surface that renders inside it must render *in* it.
Importing a component library is not adopting its design — it is borrowing its behaviour. What you
must override is not optional polish; unoverridden defaults are how a "Linear-inspired" product ends
up with 8px radii, a 44px tap target in a dense table, and `#3b82f6` because that is what the library
ships.

**Concretely, on every stock component you adopt, replace:**

| Default to replace | With | Why |
|---|---|---|
| Library's own font stack | `var(--font-sans)` | One family per product; a second font is a decision |
| Library's palette | the Layer 2 semantic roles | Otherwise theme switches miss it |
| Library's default radius | `var(--radius-control)` / `--radius-surface` | Radius is a system decision, not a library one |
| Library's default size | the density-class size | A 40px default in a dense table breaks the rhythm |
| Library's focus ring | `:focus-visible` + `var(--border-focus)` | The library ring will not be 3:1 on your surfaces |
| Library's disabled treatment | your muted pair **plus a reason** | Stock disabled is silent |
| Library's icon set | the one committed family | Two icon families in one product is visible at a glance |

If you cannot override a default, say so in `DESIGN.md` as a known constraint with the file path —
silently shipping it is the failure.

## Drift detection

**Four mechanical sweeps.** These catch most drift before a human does.

**1. Duplicate implementations and agent "shadow primitives".**
```
rg -n 'function (Button|Card|Badge|Avatar|Modal)\b|const (Button|Card|Badge)\s*=' src/
rg -n '<(button|input|select|dialog)\b' src/ --glob '!src/components/ui/**'
```
Two components with the same role name and different markup are the standard human failure; coding
agents fail one level lower by writing **shadow primitives** — raw `<button className="...">` or
`<dialog>` tags with inline token/Tailwind reconstructions inside feature routes instead of importing
from `@/components/ui/*`. Merge duplicate wrappers, and enforce the boundary mechanically in ESLint
(scoped to `src/**/*.{tsx,jsx}`, ignoring `src/components/ui/**`):
```json
{
  "rules": {
    "no-restricted-syntax": [
      "error",
      {
        "selector": "JSXOpeningElement[name.name=/^(button|input|select|dialog)$/]",
        "message": "Import canonical primitives from @/components/ui/* instead of authoring raw shadow elements in feature routes."
      }
    ]
  }
}
```

**2. Radius spread.**
```
rg -no 'border-radius:\s*[^;]+' src/ | sort | uniq -c | sort -rn
```
Every value must map to a radius token. A raw `10px` next to `--radius-lg: 10px` is drift; it will
diverge the moment the token changes.

**3. Raw literals and primitive leakage.**
```
rg -n '#[0-9a-fA-F]{3,8}\b' src/components/
rg -n 'var\(--(palette|space-[0-9]|radius-|duration-|ease-)' src/components/
```
Zero hits in both. See `tokens.md` § *Drift detection*.

**4. Icon-family spread.**
```
rg -no 'from ["'"'"'][a-z@/-]*icon[a-z@/-]*["'"'"']|lucide-react|@heroicons|react-icons|phosphor' src/ | sort | uniq -c
```
More than one answer means one icon family, one stroke weight.

**Three rendered checks** catch what greps cannot:

- **Greyscale pass.** Desaturate the surface. If two icons, two badges, or two links become
  indistinguishable, colour was doing work weight and shape should do.
- **Stacked-render pass.** Render the same component in three places at once, side by side. Drift is
  invisible in isolation and obvious in a row.
- **Mode-and-density pass.** Toggle theme and density. A stock default that does not respond to either
  is an unoverridden default — the wrapper rule's most common violation.

## One radius per family

Radius is not a per-component choice; it is a **family** assignment. One token per family, never
mixed ad-hoc:

| Family | Token | Applied to |
|---|---|---|
| Controls | `--radius-control` | Buttons, inputs, selects, toggles |
| Surfaces | `--radius-surface` | Cards, panels, list containers, table wrapper |
| Overlays | `--radius-overlay` | Menus, popovers, drawers, dialogs |
| Media | `--radius-media` | Avatars, thumbnails, images |
| Capsules | `--radius-full` | Pills, badges, icon buttons |

Three rules follow:

- **A family never mixes.** A 6px button next to an 8px input reads as two products; both take
  `--radius-control`.
- **Nested radii obey `radius_inner = radius_outer − padding`.** A 6px chip inside a 10px card with 4px
  padding gets 6px. This is the concentric-radius invariant; violating it is the visual tell of
  assembled-in-a-hurry UI.
- **Derived, not authored.** One base `--radius` plus `calc()` multipliers is the shipped pattern
  (shadcn/ui, *Theming*); Tailwind exposes the same idea as a single base spacing value. A hand-written
  ladder of radii drifts the moment someone adds a step.

## One icon family, one stroke weight

- **One family, committed, everywhere.** Two families side by side is one of the most reliably
  visible signs of an unowned product.
- **One stroke weight**, constant across sizes — typically 1.5px on a 24px grid. Weight changes for
  hierarchy are an exception you must name, not a default.
- **Fixed square boxes** at each optical size (16 / 20 / 24 / 32), so a state change never shifts
  layout.
- **State by tint, not by swapping glyphs.** Inactive = muted token; active = accent token or the
  family filled variant. Swapping `icon-edit` for `icon-edit-filled` on hover is drift.
- **Every icon-only control carries a label or a tooltip.** An unlabelled icon is a hidden affordance.

## Prop API consistency

Shared components drift through their *interfaces* before their styles. The rules:

- **One name per concept, across every component.** If `size="sm"` means 28px in the button and 32px
  in the badge, the token is `--size-control-sm` / `--size-badge-sm` and the prop is `size` in both,
  resolving to the right family. Ambiguous shared names are the defect.
- **Variants are an enum, closed.** If a variant is not in the list, the component does not accept it.
  A `variant` prop that forwards arbitrary strings is how five shades of "secondary" appear.
- **Same concept, same prop name, everywhere.** `onDismiss` never becomes `onClose` in one component.
  `disabled` never becomes `readonly` for the same interaction.
- **Boolean props are booleans.** No `isDisabled={true}` alongside `disabled` in the same codebase.
- **Sizing comes from the density axis, not from props.** A `density="compact"` prop is a smell if the
  app already has a root density mode — it creates a second axis that can disagree with the first.
- **Slots over configuration.** Five boolean props (`showIcon`, `showChevron`, `showBadge`, …) should
  be a `slots` object or composition. Boolean prop sets are how a component ends up with 32 variants
  and no tests.

## Extract, or keep it local

Default to **local**. Extraction is a commitment, and premature extraction is the most expensive kind
of slop: a shared component with two call sites has frozen the *least common denominator* of two
designs and called it a system.

**Extract when all four hold:**

1. **Third use.** Not two. Two sites can be genuinely different things wearing the same name.
2. **Identical semantics, not identical pixels.** Same role — "a thing the user can cancel" — even if
   one instance renders larger. If the roles differ, they are different components.
3. **Full state coverage.** Every extracted component ships default / hover / focus-visible / active /
   disabled / loading / error, and the second call site is actually exercised in those states. A
   component extracted without a loading state forces the next caller to reach inside it.
4. **A stable vocabulary.** You can name it without a conversation. "Button", "Field", "StatusBadge",
   "DataTable". If you are tempted to name it `Card3`, do not extract.

**Keep it local when:**

- It appears once, and its appearance is a *decision*, not a pattern.
- It exists to serve one screen's composition and will be deleted with that screen.
- Extracting it would require a `variant` prop to express the difference — the difference is the
  point.
- Its states are not designed yet. An extracted component with undesigned states spreads the debt.

**Reversal is the real test.** A wrongly extracted component is more expensive than no component,
because two screens now depend on it. When in doubt: build it twice, ship it twice, and promote it on
the third use. The third use is also the moment you know what the shared surface actually is.

## Known drift is documented, never blessed

When the codebase is already inconsistent:

- **The rule is the majority behaviour, confirmed.** The exceptions are listed as drift with file
  paths. Never document a violation as the rule, and never silently bless an exception by omitting it.
- **A tie is unresolved.** Two equally-used patterns means no rule exists. Mark it unresolved with the
  two candidates and a recommendation, and hand the decision to the user.
- **DESIGN.md that disagrees with the shipped UI is worse than no DESIGN.md.** Every future session
  trusts the file.

See `document.md` for the full reverse-engineering procedure.

## Not found

- **A standard or vendor criterion for when a component should be extracted.** The third-use rule is
  this skill's heuristic; the most common published advice is design-system-agnostic and unmeasurable.
  Settled by: none — judge by whether the two call sites share semantics, which is checkable.
- **A sourced rule for icon stroke weight consistency.** Vendors ship different defaults (1.5px vs 2px
  at 24px) and none publishes a rationale to cite. Settled by: none — pick one weight, hold it.
- **A sourced rule that nested radii must equal outer radius minus padding.** It is the concentric-radius
  invariant this skill inherits from `premium-mobile-design`, used here as house guidance. Settled by:
  none — verify visually.
- **A measurement for how much prop-API inconsistency costs.** No source. Treat the four mechanical
  sweeps as the practical bar.

## Sources

All accessed 2026-10-05. Parenthetical = what the citation carries in this file.

- **Theming** — shadcn/ui. (One base `--radius` with derived `calc()` multipliers; one base spacing value driving the scale.) https://ui.shadcn.com/docs/theming
- **Registering custom properties in CSS** — MDN, Mozilla. (Custom properties are unregistered strings until `@property` supplies a type; registered interpolate, unregistered animate discretely; `@property` requires `syntax` AND `inherits`.) https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Properties_and_values_API/Registering_properties
- **Design Tokens Format Module 2025.10** — W3C Design Tokens Community Group. (Groups arbitrary; tools SHOULD NOT infer type/purpose; `$type` determinable or invalid; names case-sensitive excluding `$`/`{`/`}`/`.`; circular refs MUST error.) https://www.designtokens.org/TR/2025.10/format/
- **Understanding SC 1.4.11 Non-text Contrast** — W3C WAI. (Control boundaries, state indicators and focus indicators need 3:1 against adjacent colours; a stock focus ring is not automatically compliant.) https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- **WCAG 2.2** — W3C. (SC 2.4.7 Focus Visible; SC 2.5.8 Target Size (Minimum).) https://www.w3.org/TR/WCAG22/
- **Data table** — Carbon Design System, IBM. (Row heights, and the requirement that header/toolbar/pagination match row size — the density-axis argument for sizing from tokens, not props.) https://carbondesignsystem.com/components/data-table/usage/
- **Design tokens** (token layering and role naming; separation of token from component) — Polaris Design System, Shopify. https://polaris.shopify.com/design/design-tokens
- Density classes, one-primary-per-view, disabled-must-explain-why, label-your-icon-controls — house floor: `references/craft-floor.md`.
