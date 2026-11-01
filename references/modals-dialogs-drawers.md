# Modals, dialogs, drawers

Overlay surfaces are the most over-used pattern in logged-in product UI. The standards give a
narrow definition of a dialog; almost every "modal" in a B2B console fails it. This file decides
*which* surface to reach for, then builds the dialog correctly.

Out of scope here: mobile sheets and gestures, marketing modals.

## Pick the surface first

A dialog is defined by the accessibility layer, not by the visual one. A `dialog` is "a window
overlaid on either the primary window or another dialog window"; windows under a modal dialog are
inert, meaning users cannot interact with content outside an active dialog (APG, Dialog (Modal)
Pattern). Modal dialogs contain their tab sequence, and — unlike most non-modal dialogs — **provide
no means for moving keyboard focus outside the dialog window without closing it** (APG).

| Need | Correct surface | Why |
|---|---|---|
| Multi-field task, deep-linkable, browser-back must work | **Route** | A modal has no URL, no back, no deep link |
| Inspect/compare against the record behind it | **Side panel / drawer** | Keeps the trigger context visible and focusable-adjacent |
| A few fields where the record stays as reference | **Drawer** | Context preserved, dismissal trivial |
| One or two values, reversible | **Inline edit / disclosure** | No new surface, no focus jump |
| Short focused task, must finish or abandon now | **`role="dialog"`** | Inert context is the point |
| Irreversible action acknowledgement | **`role="alertdialog"`** | "A special-case dialog role designed specifically for dialogs that divert users' attention to a brief, important message" (APG, Alert and Message Dialogs) |
| Short label/definition for an element | **Tooltip** | Tooltip widgets "do not receive focus" (APG, Tooltip) |

**A modal is for a short focused interruptive task with a clear exit.** Anything that scrolls,
anywhere a user might want to leave and come back to, is a panel or a route.

**Not found:** no normative source sets a maximum dialog height, field count, or duration before a
dialog should become a route. Settling that requires either a design-system decision recorded in
`DESIGN.md` or a usability test — not a spec citation.

## Anatomy (required, not optional)

- The dialog container has `role="dialog"`; all elements required to operate it are descendants of
  that element (APG).
- `aria-modal="true"` on the container (APG).
- Either `aria-labelledby` pointing at a visible title, or `aria-label` (APG).
- Optionally `aria-describedby` pointing at the element(s) describing the primary purpose or
  message. **Omit it** when the dialog body contains semantic structures — lists, tables, multiple
  paragraphs — that must be perceived in order, because the description is announced as a single
  unbroken string (APG).
- Mark a dialog modal **only when both**: (1) application code prevents all users interacting with
  content outside it, and (2) visual styling obscures the content outside it. `aria-modal="true"`
  "can prevent users of some assistive technologies from perceiving content outside the dialog",
  so a false-modal marked as modal causes "severe negative ramifications" (APG).
- Legacy `aria-hidden` fallback, if used at all: set `aria-hidden="true"` on **each** element
  containing a portion of the inert layer, and never make the dialog a descendant of an
  `aria-hidden="true"` element (APG).

### Keyboard

| Key | Behavior (APG, Dialog (Modal)) |
|---|---|
| `Tab` | Next tabbable element inside the dialog; from the last, wraps to the first |
| `Shift`+`Tab` | Previous tabbable element inside; from the first, wraps to the last |
| `Escape` | Closes the dialog |

"It is strongly recommended that the tab sequence of all dialogs include a visible element with
role `button` that closes the dialog, such as a close icon or cancel button" (APG). Values above 0
on `tabindex` are "strongly discouraged" (APG).

### Initial focus

APG's four cases, in order of preference:

| Dialog content | Initial focus |
|---|---|
| Large content; focusing the first interactive element would scroll content out of view | Static element at the top with `tabindex="-1"` — e.g. the title or first paragraph — and omit `aria-describedby` |
| Semantic structures needing in-order perception (list, table, several paragraphs) | Static element at the start with `tabindex="-1"`; omit `aria-describedby` |
| Final step of a non-reversible process (deleting data, completing a financial transaction) | **The least destructive action**; the Alert Dialog Pattern is often employed here (APG) |
| Only offers more information or continues processing | The most frequently used control, e.g. OK or Continue (APG) |

### Focus on close

"When a dialog closes, focus returns to the element that invoked the dialog" — unless the invoking
element no longer exists (then focus something that provides logical workflow), or the workflow
design makes another target more logical: the user is very unlikely to need to re-invoke the dialog,
**and** the task completed in the dialog feeds a direct next step. The APG example: a toolbar's
"Add Rows" dialog that prompts for a row count returns focus to the first cell of the first new
row (APG).

## Native `<dialog>` beats a div

Use the platform element. `<dialog>` "is available across browsers since March 2022" (MDN).

- `showModal()` makes the rest of the page inert, puts the dialog in the top layer, records the
  previously focused element, and runs the dialog focusing steps; `show()` is the non-modal path
  (WHATWG HTML, *The `dialog` element*; MDN).
- `showModal()` dialogs get `aria-modal="true"` implicitly; `show()` and `open` yield
  `aria-modal="false"` (MDN).
- **Never put `tabindex` on `<dialog>`** — "Do not add the `tabindex` property to the `<dialog>`
  element as it is not interactive and does not receive focus" (MDN).
- Use `autofocus` on the element the user must interact with first; "the `<dialog>` element itself
  may provide the best initial focus placement" when the content renders dynamically (MDN).
- Use `::backdrop` for the scrim — it is the pseudo-element behind a `showModal()` dialog (MDN).
- `closedby` values: `any` (includes light dismiss), `closerequest` (platform action or developer
  mechanism), `none`. With no valid `closedby`, a `showModal()` dialog behaves as `closerequest`,
  so Escape closes it (MDN).
- Do not abuse it: "context menus, tooltips, and popup listboxes are not dialog boxes, so abusing
  the dialog element to implement these patterns is incorrect" (WHATWG HTML).

## Scroll containment

The HTML spec is unusually direct: "in general, scrollable dialogs are **not expected** by users"
and "adding large text nodes directly to dialog elements is particularly bad as this is likely to
cause the dialog element itself to overflow" (WHATWG HTML, *The `dialog` element*). Overflow
"cannot be avoided" under high text zoom (WHATWG HTML).

Working shape: fixed height on the dialog shell, one inner scroll container, sticky header and
footer outside that container, long-form content in a route or a full-height panel instead.

## The destructive-confirmation ladder

Climb only as far as the irreversibility demands. Levels 0–1 need no dialog at all.

| Level | Irreversibility | Treatment |
|---|---|---|
| 0 — Undo-first | Fully reversible | Act immediately; offer Undo |
| 1 — Reversible but surprising | Soft delete, archive, state toggle | Act immediately; inline confirm row with Undo/Cancel |
| 2 — Costly to reverse | Billing change, permission removal | `alertdialog`, safest action focused |
| 3 — Destructive | Deletion, revocation, termination | `alertdialog`, name the affected object; least destructive action focused |
| 4 — Irreversible and high-blast-radius | Destroy workspace, rotate production secret | `alertdialog` + type-to-confirm |

`alertdialog` differs from `dialog` in one required way: "The element with role `alertdialog` has a
value set for `aria-describedby` that refers to the element containing the alert message"
(APG). Keyboard behavior is the modal dialog table above (APG).

Never `window.alert()` / `window.confirm()` — they are outside any design system and carry no
labeling contract.

## Sources

- [Dialog (Modal) Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) — W3C WAI ARIA Authoring Practices Guide, accessed 2026-10-05
- [Alert and Message Dialogs Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/) — W3C WAI ARIA Authoring Practices Guide, accessed 2026-10-05
- [Tooltip Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/) — W3C WAI ARIA Authoring Practices Guide, accessed 2026-10-05
- [`<dialog>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog) — MDN Web Docs (Mozilla), accessed 2026-10-05
- [HTML Standard §4.11.4 The `dialog` element](https://html.spec.whatwg.org/multipage/interactive-elements.html#the-dialog-element) — WHATWG, accessed 2026-10-05