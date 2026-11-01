# Layout — grid, rhythm, hierarchy, alignment

Enhance command. `layout` fixes the *frame*: regions, tracks, spacing rhythm, and what the eye
lands on first. It does not decide the direction — that is `screen.md` and
`signature-moves.md`. If the structure is still undecided, stop and run `screen.md` step 5.

## 1. Establish what is already decided

The surface's **mode** (Operate / Read / Decide / Support) and its **density class** (Focused /
Standard / Dense). Both come from the context script's output and the brief. Every spacing and
measure rule below is class-relative, and the class table itself lives in `craft-floor.md` —
read it there rather than trusting a copy. One class per surface; a screen that mixes 12px table
text with 16px prose side by side is two regions pretending to be one.

## 2. Name the composition before the CSS

Derive 5–7 materially different structures from the usage scene (list-first, table-first,
master-detail, panel-over-list, wizard, workspace-with-rail, command-bar-centric), pick one, and
name the category default you are refusing. Then identify the template: Homepage, Index,
Details, Settings — each with its own body shape and page-header action budget
(`page-composition.md`). Splitting rule: a route doing more than two major jobs gets split, and
cards nested two or three deep mean the split is overdue.

## 3. Grid owns regions, flex owns rows

Grid for shell regions, list+detail splits, card galleries. Flex for a page header's
title-left/actions-right, a toolbar's search-grow/controls-fixed, a settings section's
label-then-control, a sidebar's vertical stack (`layout-grid.md`).

- Shell as one grid with `grid-template-areas`; `100dvh` for the frame.
- `minmax(0, 2fr)` for the content column so long IDs cannot force the grid wider than the
  viewport. `minmax()` is how a region gets a floor and a ceiling.
- `repeat()` for long track lists; `subgrid` when a nested region must align to the parent's lines
  (a detail pane's field rows against the list's column boundaries).
- `flex: none` on every fixed-width icon slot and trailing action. Gap alone does not align
  columns across repeated rows.

## 4. Establish key lines

Alignment does the grouping. A list column and the detail pane's field labels share a left edge;
whitespace separates groups. Carbon's 2x Grid requires "visible key lines: vertical and horizontal
lines on which multiple objects align." Type sits **against** the padding edge, never inside it.
Nested boxes are the last resort, not the first.

## 5. Spacing: parent-owned, one scale

- Spacing on the 4px base scale (8px comfortable, 4px Dense). No `17.0`, no `23.0`.
- **Parent-owned spacing**, not per-item margins — Carbon's Stack delegates positioning to the
  parent, which is what makes density swappable at one breakpoint.
- Within a section, space is one step; between sections, two or more. If every gap is distinct, no
  gap reads as structural. More space above a heading than below it.
- Carbon's tokens are fixed multiples of 2/4/8, and its own FAQ is the rule that matters:
  "the tokens themselves do not change values based on the screen size" — jump a step at
  breakpoints, never interpolate.
- Whitespace budget by class: Focused 55–70% · Standard 40–55% · Dense 25–40% (house heuristic,
  `information-density.md`). Below the floor reads cramped; above it reads empty.
- Content gets a max measure in Focused/Standard: 65–80ch for prose. Unconstrained for grids and
  tables in Dense (`craft-floor.md`).

## 6. One dominant element per view

Weight, size, position, space — in that order of durability. NN/g caps size-based hierarchy at
three sizes and big elements at two; Kaplan's corrective is the one consoles need: "**removing
nonessential elements can be equally or even more effective** at making important information
visually salient." Colour is a lever but never the only one (`visual-hierarchy.md`).

**Reading order must match DOM order.** WCAG 2.2 SC 2.4.3 requires focus in an order that
"preserves meaning and operability"; W3C's sufficient technique is C27, matching DOM to visual
order. Heading tags must match the visual heading rank.

## 7. Write the adaptation contract

Container queries for anything inside a resizable layout; viewport media queries only for
page-level reflow. Reflow floor: no two-dimensional scrolling at 320 CSS px width / 256 CSS px
height, except genuinely 2D content (tables, maps, video, toolbar-bound editors) — the heading,
filters, and pagination around them still reflow. Narrow widths **drop columns, not type size**.
`cq*` units need a fallback. The page never scrolls sideways: overflow lives in a named scroll
region with `min-width: 0`.

## 8. Render and look

`render-loop.md`, minimum two passes: default, populated, dark, narrow container width, 200% zoom.
Then the layout-specific tests: squint (blur 5–10px for grouping, 20px to expose unintended
hierarchy), greyscale (does the hierarchy survive without colour?), and a keyboard pass to confirm
focus walks the visual order and no sticky header swallows it.

## 9. Detector advisories for this command

These layout findings flip by class and are **advisory at the noted class**, not failures —
`craft-floor.md` carries the full table, and `detector-integration.md` the mechanics:

| Finding | Advisory at |
|---|---|
| `monotonous-spacing` | Dense — even rhythm is correct in tables |
| `line-length-too-long` | Dense — full-width is correct in tables |
| `cramped-padding` | Dense — tight row padding is correct |
| `identical-card-grids` | Standard — legal in a settings or feature index |
| `nested-cards` | nowhere — fails at every class |
| `modal-abuse` | Standard — legal for a scoped configuration dialog |

## Exit criteria

Class declared and applied; one dominant element per view; key lines visible; spacing on the
scale with parent-owned rhythm; measure set in Focused/Standard; container contract written;
render loop converged; no `z-index` used to fix a colour precedence.

## Not found

- **A sourced maximum number of regions per route, or a page-composition formula.** The
  one-screen-one-job rule and the >2-jobs split threshold are house judgement.
- **A sourced whitespace-per-class budget.** The 55–70 / 40–55 / 25–40 figures are this skill's
  heuristic, flagged as such in `information-density.md`; no primary source was consulted.

## Sources

Sibling reference files this playbook routes to: `craft-floor.md` (density table, spacing scale,
verify/refuse floor), `layout-grid.md` (grid/flex mechanics, Carbon 2x Grid geometry, sticky and
scroll containment), `whitespace-hierarchy.md` (spacing scale, the three jobs of space, section
rhythm), `visual-hierarchy.md` (hierarchy levers, caps, DOM-order conformance), `page-composition.md`
(the four templates, action budgets), `information-density.md` (class mechanics, whitespace budget),
`responsive-container-queries.md`, `render-loop.md`.

External pages cited above, all previously opened by this skill:

- 2x Grid (mini unit, padding, gutters, key lines, vertical rhythm, type against the padding edge)
  and Spacing (scale, Stack, relationship/hierarchy/grouping, breakpoint FAQ) — Carbon Design
  System (IBM). https://carbondesignsystem.com/elements/2x-grid/overview/ ·
  https://carbondesignsystem.com/elements/spacing/overview/ — accessed 2026-10-05.
- Visual Hierarchy in UX: Definition · 8 Design Guidelines for Complex Applications ·
  Short-Term Memory and Web Usability — Nielsen Norman Group.
  https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ ·
  https://www.nngroup.com/articles/complex-application-design/ — accessed 2026-10-05.
- Understanding SC 2.4.3 Focus Order · SC 1.4.10 Reflow — W3C WAI.
  https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html ·
  https://www.w3.org/WAI/WCAG22/Understanding/reflow.html — accessed 2026-10-05.
- CSS grid · flexbox · container queries — MDN. https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Basic_concepts_of_grid_layout ·
  https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox ·
  https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries — accessed 2026-10-05.

**House process, not sourced fact:** the 5–7-structure derivation, the ">2 major jobs" split
threshold, the one-dominant-element rule as applied per template, the density-to-layout mapping in
step 9, and the sequence of the eight steps above. These are this skill's workflow; the
measurements they lean on are cited or routed to the file that cites them.