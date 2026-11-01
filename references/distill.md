# Distill — strip to essence, remove complexity

Refine command. `distill` asks one question of every element on a surface: **does this earn its
place?** It removes what is decoration, redundancy, or unearned capability — and it never removes
capability the user depends on.

## The distinction that makes `distill` safe

Removal is only legitimate when the *thing being removed* was not carrying weight. NN/g's Kaplan
gives the mechanism: "**making important information stand out does not always mean adding emphasis
to that information** (e.g., a bright color or a heavier font weight). **Removing nonessential
elements can be equally or even more effective** at making important information visually salient."
Her worked example: dashboard numbers set large and clean read better than the same numbers beside
decorative money icons — the icons made the numbers *harder* to find.

So distillation is not deletion for its own sake. It is **substitution of emphasis**: what goes
away must be non-load-bearing, and what remains must read more clearly than before.

## What a legitimate simplification looks like

| Remove | Legitimate because | The signal that it was non-load-bearing |
|---|---|---|
| A container wrapping one paragraph | Space and a divider already group it; nested boxes are the last resort | Removing it loses no grouping and the eye still lands in the same place |
| A second font family | One family is the product default; a second must earn the contrast | No semantic role disappears — nothing was mono because it *is* code |
| A hover-only affordance | Focus and touch must reach the same content anyway | The action is still reachable by keyboard after removal |
| A decorative illustration in an empty state | Carbon allows images; it "should be skipped by screen readers" and costs a network request | The heading + subheading + action still teach the shape and the next step |
| A duplicated status | Two places reporting the same fact is one more thing to keep in sync | No decision depended on the second copy |
| An unlabelled secondary action | Labels exist to name the action | Nothing discoverable was lost — the action was invisible anyway |
| Motion on a state that already changes colour | Colour and opacity carry the change | No user loses the signal; `prefers-reduced-motion` already removed it |
| A field with no validation rule and no default | If it is never invalid and never prefilled, it is decoration | Nothing is stored, nothing is read |

## What is a loss of capability

| Do not remove | Why it is load-bearing |
|---|---|
| Any of the four states — loading, empty, error, offline/stale | "A page that removes the skeleton but has no failure state isn't complete" (Polaris). A removed error state is a blank pane |
| `tabular-nums` on a numeric column | Column alignment *is* the scanability of the table |
| The keyboard path for anything | WCAG 2.2 SC 2.1.1 is **Level A**: all functionality operable by keyboard |
| Roving tabindex in a grid or toolbar | Otherwise every cell is a tab stop — 20 stops per row is a trap, not a shortcut |
| A permission-denied state with a route back | A denial with no path forward is a dead end; it is an authorisation boundary, not an empty state |
| Undo on an optimistic update | If it cannot be undone it must wait for confirmation — that is the capability being removed if you drop it |
| Confirmation on an irreversible action | `alertdialog` + named object + least destructive focus (`modals-dialogs-drawers.md`) |
| An age-of-data notice where the user might act on the value | Auto-update where stale data is useless; show the timestamp where the user might act on it |
| `aria-rowcount` / `aria-rowindex` after virtualising | Without them a screen reader hears "row 40," not "row 40 of 9,000" |
| Reserved space for async regions | Removing the skeleton is the direct cause of CLS |
| `scroll-padding` on a scroll container | The cited fix for sticky chrome hiding the focused element (SC 2.4.11) |
| A token layer | Distillation of *content* never means flattening primitive → semantic → component |
| A density class that a large dataset requires | An index of 40+ rows is Dense; the same route with 6 rows is Standard. The class is derived from the job |

**The test:** ask "what breaks if this is gone?" If the answer names a *user capability, a
conformance requirement, or a correctness property* — it stays. If the answer is "it looks a bit
emptier" — it goes.

## Procedure

1. **Get pixels.** Distillation judged from code is guessing. Render and screenshot
   (`render-loop.md`).
2. **Squint.** Blur 5–10px to check grouping; 20px to expose what is actually dominating. Kaplan's
   "worth removing" list is whatever a blurred pass reveals as loud.
3. **Greyscale.** Turn colour off. If the hierarchy survives, colour was decoration — and the
   accent budget shrinks. If it collapses, colour was doing the work that weight, size, position,
   or space should have done.
4. **Inventory by role.** For each element, name its job in one phrase. Elements whose job is
   "decorative," "consistent," or "to fill space" are candidates. Elements whose job is "identifies
   the record," "commits the change," or "recovers from failure" are not.
5. **Remove in one pass, re-render, compare.** Distillation that needs two passes is usually
   removing the wrong thing.
6. **Re-run the floor.** Every removal is checked against `craft-floor.md` and the accessibility
   gate — `accessibility-web.md`, `production-launch-checklist.md`.
7. **Record what was load-bearing.** If something resisted removal and its reason was not obvious,
   that reason belongs in the project's `DESIGN.md`.

## Refuse

The temptation `distill` exists to resist is subtractive overreach — reaching for `craft-floor.md`'s
Refuse list by omission instead of addition. Stealing density from a Dense surface's type size
("it's cleaner at 12px everywhere"), removing a border because a shadow is present, dropping an
error state because the flow is usually successful, or deleting a permission check because the
internal audience does not need it. Each is a loss of capability wearing a simplification's clothes.

Also refuse: hard-capping a nav list to look tidy. An over-short menu forces abstract choices;
grouping, labelling, search, and recency beat arbitrary limits (NN/g on short-term memory). And
refuse distillation that lands on a marketing aesthetic — removing the chrome and leaving a hero
band is a different skill's output.

## Detector advisories

Distillation is the command most likely to *create* findings, not resolve them: `nested-cards`,
`repeated-container-text` (the same label in several slots of one container), `marquee`,
`pulsing-dot`, and `image-hover-transform` all appear when one removes a container and leaves its
inhabitants doubled. Re-run `npx impeccable detect` after, not before (`detector-integration.md`).

## Exit criteria

Every remaining element has a named job. No container holds one paragraph. One family, or a second
with a stated role. Hover-only affordances gone — keyboard and touch reach everything. All four
states present and reachable. Accessibility gate and `production-launch-checklist.md` green after
the removals. Re-render shows the intended job *more* prominent than before.

## Not found

- **A sourced rule for how many elements a surface may contain, or a quantitative measure of
  "visual complexity."** No standard, vendor guideline, or study consulted here supplies an element
  budget or a complexity index. The two tables above are house judgement built on cited mechanisms
  (Kaplan's removal-as-emphasis; Carbon's grouping and proximity rules; WCAG's criterion levels).
  Settled by: task-success and time-on-task data from a usability study on the specific surface.
- **A sourced threshold for when an empty state's illustration should be dropped.** Carbon permits
  illustrations and warns only about repetition; no source rules on this.

## Sources

Sibling reference files this playbook routes to: `craft-floor.md` (Refuse list, verify rules),
`visual-hierarchy.md` (levers, squint/greyscale tests, Kaplan's removal-as-emphasis), `whitespace-hierarchy.md`
(what space does; when whitespace replaces a container), `page-composition.md` (templates and
action budgets), `component-consistency.md`, `elevation-layers.md` (border vs shadow), `color-token-system.md`,
`empty-states.md` (illustration guidance), `modals-dialogs-drawers.md` (destructive-confirmation
ladder), `error-states.md`, `offline-stale-sync.md` (age-of-data notices), `virtualization-lists.md`
(`aria-rowcount`/`aria-rowindex`), `accessibility-web.md`, `production-launch-checklist.md`,
`render-loop.md`, `information-density.md`.

External pages cited above, all previously opened by this skill:

- 8 Design Guidelines for Complex Applications (guideline 8: make important information visually
  salient; removal as an alternative to emphasis; the money-icon example) — Nielsen Norman Group.
  https://www.nngroup.com/articles/complex-application-design/ — accessed 2026-10-05.
- Visual Hierarchy in UX: Definition (squint test; blur radii; grouping via proximity; add
  containers only when whitespace is insufficient, "use them sparingly") — Nielsen Norman Group.
  https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ — accessed 2026-10-05.
- Short-Term Memory and Web Usability (why "cap menus at 7 items" is a misreading) — Nielsen Norman
  Group. https://www.nngroup.com/articles/short-term-memory-and-web-usability/ — accessed 2026-10-05.
- Spacing ("Space can also be used to denote groups of associated information… without having to use
  lines or other graphical elements as a divider"; "Sections of a UI are allowed to be dense") —
  Carbon Design System (IBM). https://carbondesignsystem.com/elements/spacing/overview/ —
  accessed 2026-10-05.
- Empty states (illustrations "should be skipped by screen readers"; a text-only empty state can be
  preferable under repetition) — Carbon Design System (IBM).
  https://carbondesignsystem.com/building-blocks/core/patterns/empty-states/ — accessed 2026-10-05.
- Understanding SC 2.1.1 Keyboard (Level A) · SC 2.4.11 Focus Not Obscured (scroll-padding) ·
  SC 1.4.10 Reflow · Understanding SC 2.5.8 Target Size (Minimum) — W3C WAI.
  https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html —
  https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html — accessed 2026-10-05.
- Web Vitals (reserve space for async regions; CLS consequences of an unexpected shift) — Google /
  web.dev. https://web.dev/articles/vitals — accessed 2026-10-05.

**House process, not sourced fact:** the two tables (legitimate simplification vs loss of
capability), the seven-step procedure, the Refuse additions, and the exit criteria. Every
conformance criterion and vendor statement in them is cited or routed to the file that cites it.