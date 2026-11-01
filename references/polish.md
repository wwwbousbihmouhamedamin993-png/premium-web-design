# Polish — final quality pass before shipping

Refine command. `polish` runs last. It is the pass that removes the last visible roughness from a
surface that is already correct — not the pass that decides what the surface is.

## Scope: three things `polish` does not do

1. **It does not re-litigate direction.** The structure, hierarchy, mode, density class, template,
   and boundary choice were committed in `screen.md` (or inherited from the incumbent screen).
   `polish` does not split a route, re-tier the density class, replace a table with a list, or move
   a primary action. If one of those is genuinely wrong, stop and route to `layout.md`,
   `density` (`information-density.md`), or `screen.md`. A polish pass that reshuffles the
   composition is an unreviewed redesign wearing a small diff.
2. **It does not add features.** No new field, filter, column, empty state, toast, keyboard
   shortcut, or onboarding step is introduced here. Adding capability is `screen.md`, `table`,
   `form`, `onboard.md`, or `harden.md`.
3. **It does not fix copy that needs a product decision.** A label that is merely unclear is
   `clarify.md`. A label whose *wording* is a product or legal decision — what a plan is called,
   what a destructive action will actually destroy — is escalated, not guessed.

What remains is: alignment, rhythm, consistency, state completeness, interaction feel, and the
last 10% of craft.

## 1. Confirm the pass is legal

Before touching anything: density class declared and still correct; brief satisfied; render loop
converged (minimum two passes, `render-loop.md`); `craft-floor.md` loaded. Polish before the
structure is committed is how generic screens get finished instead of decided.

## 2. Alignment and rhythm

The most common residual defect is a 2px disagreement nobody named.

- Key lines visible: a list column and the detail pane's field labels share a left edge; toolbar,
  pagination, and table chrome align to the same edges.
- Section rhythm: more space above a heading than below it. Within a section, one spacing step;
  between sections, two or more. Every gap distinct means no gap reads as structural.
- Optical alignment: type sits **against** the padding edge, never inside it. Height is
  content-driven — never a fixed-height box clipping a taller locale string.
- Card internals: equal internal padding everywhere; nothing hangs 4px outside a sibling.
- Nested rounded corners concentric — the corner gap must match the straight-edge gap.

## 3. Component consistency

The wrapper-component rule: one shared component per pattern, restyled through tokens, never a
stock default sitting inside a committed screen. Check for drift (`component-consistency.md`):

- One radius per family; `border-radius` literals outside the token file are defects.
- One icon family, one stroke weight. Mixing outline and filled reads as two products.
- One primary (filled) CTA per view; secondary and tertiary step down.
- Every control has hover, focus-visible, active, and disabled states. `:focus-visible` is never
  removed. A disabled control says why on focus or hover rather than being silently dead.
- A button never changes width between idle and loading — reserve the space.

## 4. Interaction feel

- Motion is asymmetric: decelerate in, accelerate out. Symmetric ease-in-out on both directions is a
  defect. Only `transform` and `opacity` animate; animate a zero-blur shadow, not `box-shadow` with
  a blur, if the ring must move.
- One authored moment per view. Playful physics belong to marketing and empty moments, never to a
  confirm dialog.
- `prefers-reduced-motion: reduce` is a real variant, not `animation: none` everywhere: movement
  becomes a crossfade or an instant cut, opacity under ~150ms, spinner rotation and colour
  transitions kept.
- Focus ring holds 3:1 against adjacent colours **and still holds it under a dim overlay**.
- Hit areas: size the hit area to 24×24 CSS px minimum with padding or a pseudo-element rather than
  relying on the spacing exception — the exception passes an audit and fails real hands. Dense rows
  get a full-row interactive target, not a 12px glyph.

## 5. Overflow, clipping, long strings

- No sideways page scroll. Overflow lives in a named scroll region with `min-width: 0`.
- Nothing clipped by a positioned ancestor: menus, popovers, and tooltips render outside the
  clipping container, or the container gets `overflow: visible`.
- Text does not touch the viewport edge. Content does not overflow its container at 320 CSS px.
- **Test at +35% string expansion** with real-feeling demo data — long customer names, two-line
  titles, decimals, 40-row tables. Never `Lorem`.
- Images and avatars sit in a fixed aspect-ratio box defined before load, with `width`/`height`
  set. Zero layout shift.

## 6. States, once more

Polish does not design states, but it verifies each one is reachable and consistent:
loading skeleton shaped like the real content (never a centred spinner on a blank page), empty
state with a cause and a CTA, error with recovery, offline/stale showing what is known versus
cached. Async status announced via role or live region, not only painted (SC 4.1.3, AA).

## 7. Detector advisories for this command

Findings in the polish band that are per-class advisory rather than failures:
`monotonous-spacing`, `cramped-padding`, `line-length-too-long` in Dense; `modal-abuse` in
Standard (scoped configuration dialogs are legal). `nested-cards`, `gradient-text`,
`radial-gradient-background-halo`, `low-contrast-text`, and `justified-text` fail at every class.
Full table and exit-code mechanics:
`detector-integration.md`; per-density rulings: `craft-floor.md`.

## 8. Close out

- Render and look again — light, dark, narrow container, 200% zoom. A fresh pass must find nothing.
- Run the mechanical grep list from `critique.md` over the changed files; fix real hits.
- Run the project's analyzer, lint, and tests.
- `npx impeccable detect` on the changed files; reconcile every finding as fixed or recorded
  (`detector-integration.md`).
- Record durable system decisions in the project's `DESIGN.md` — a radius rule, a row-height
  decision, or a token that survived this pass becomes a document, not tribal memory.

## Exit criteria

No direction changed, no feature added. Alignment and rhythm consistent across the surface; shared
components reused without drift; every control state present; motion asymmetric with a real
reduced-motion variant; no clipping or overflow at 320px or +35% strings; all four states
reachable; render loop green in both modes; detector reconciled; project checks clean.

## Not found

- **A sourced definition of "polish" or a numeric polish-completeness score.** No standard, design
  system, or study consulted here defines a final-pass rubric. The three prohibitions in the Scope
  section, the ordering of steps 2–6, and the exit criteria are house process. `critique.md`'s
  pillar table is the scored instrument when a number is wanted — it is explicitly weighted by
  judgement.
- **A sourced optical-alignment tolerance.** "Looks 2px off" is a judgement call; Carbon's
  "optical spacing" note permits deviation from the unit where the unit cannot hold, with no
  numeric tolerance given.

## Sources

Sibling reference files this playbook routes to: `craft-floor.md` (verify/refuse floor, density
table, per-density detector overrides), `critique.md` (scored review, slop detector, mechanical
grep list), `render-loop.md` (render and look), `component-consistency.md` (wrapper rule, drift
detection, radius and icon families), `layout-grid.md` (key lines, sticky, scroll containment),
`whitespace-hierarchy.md` (spacing, rhythm, optical alignment), `color-token-system.md`,
`dark-mode.md`, `elevation-layers.md`, `radius-motion-tokens.md` (motion, asymmetric durations,
reduced motion), `responsive-edges.md`, `web-vitals-performance.md` (CLS from reserved space),
`document.md` (recording durable decisions).

External pages cited above, all previously opened by this skill:

- 2x Grid (key lines; type against the padding edge; optical spacing vs the mini unit; vertical
  rhythm) · Spacing (relationship, hierarchy, grouping without a box) — Carbon Design System (IBM).
  https://carbondesignsystem.com/elements/2x-grid/overview/ ·
  https://carbondesignsystem.com/elements/spacing/overview/ — accessed 2026-10-05.
- `box-shadow` (zero offset + zero blur = equal-size outline) · `position` (sticky: inset
  requirement, scrolling ancestor, repaint cost) · `overflow` (scroll container semantics; `clip`
  still scrolls to focus) · `prefers-reduced-motion` (two values; vestibular triggers) — MDN.
  https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/box-shadow —
  accessed 2026-10-05.
- Shape (optical roundness: outer radius − padding = inner radius) — Material Design 3.
  https://m3.material.io/styles/shape/corner-radius-scale — accessed 2026-10-05.
- Understanding SC 2.4.7 Focus Visible · SC 2.4.11 Focus Not Obscured · SC 2.4.13 Focus Appearance
  (AAA) · SC 1.4.11 Non-text Contrast · SC 2.5.8 Target Size (Minimum) · SC 4.1.3 Status Messages —
  W3C WAI. https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — accessed 2026-10-05.
- Web Vitals · CSS for Web Vitals (reserve space for async regions) — Google / web.dev.
  https://web.dev/articles/vitals · https://web.dev/articles/css-web-vitals — accessed 2026-10-05.

**House process, not sourced fact:** the three prohibitions, the pass ordering, the per-band
detector rulings, the exit criteria, and the "polish before structure is committed is how generic
screens get finished" claim. Every threshold referenced is cited or routed to the file that cites
it.