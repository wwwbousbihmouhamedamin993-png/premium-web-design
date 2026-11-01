# Focus management

Focus is the keyboard user's cursor and the screen reader's reading position. Every overlay,
composite widget, and route transition is a chance to lose it.

## Focus trap in dialogs

From APG's Dialog (Modal) Pattern: "modal dialogs contain their tab sequence. That is, `Tab` and
`Shift`+`Tab` do not move focus outside the dialog. However, unlike most non-modal dialogs, modal
dialogs do not provide means for moving keyboard focus outside the dialog window without closing the
dialog."

| Key | Behavior (APG) |
|---|---|
| `Tab` | Next tabbable element inside; wraps from last to first |
| `Shift`+`Tab` | Previous tabbable element inside; wraps from first to last |
| `Escape` | Closes the dialog |

Implement the trap by making everything outside the dialog **inert**, not by intercepting `Tab` and
rewriting `document.activeElement`. Traps belong in the inert subtree, never in a keydown listener.

## `inert`

`inert` is a boolean **global attribute**: "the element and all of its flat tree descendants become
*inert*" (MDN). An inert subtree is removed from the tab order and the accessibility tree, cannot
be focused, does not fire `click`, is not searchable by find-in-page, and disallows text selection
and editing (MDN).

Two things to know. First, modal `<dialog>`s opened with `showModal()` "escape inertness, meaning
that they don't inherit inertness from their ancestors, but can be made inert by having the
`inert` attribute explicitly set on themselves. No other element can escape inertness" (MDN) — a
nested modal works, a nested popover does not. Second, `inert` gives no visual signal: MDN puts it
on the author to "clearly indicate the content parts that are active and those that are inert", so
dim or blur the inert region yourself. Since `inert` also disables clicks, a scrim inside the inert
region cannot carry the light-dismiss handler. For a `showModal()` dialog the browser does the
inertness for you (MDN, `<dialog>`); otherwise set `inert` on the app-shell siblings.

## Focus return on close

- "When a dialog closes, focus returns to the element that invoked the dialog" (APG, Dialog Modal).
  Two documented exceptions: the invoking element no longer exists → move focus to something
  providing logical workflow; or the design makes a different target more logical when the user is
  "very unlikely users need to immediately re-invoke the dialog" **and** "the task completed in the
  dialog is directly related to a subsequent step in the work flow". APG's example: an "Add Rows"
  dialog returns focus to the first cell of the first new row (APG). Native `<dialog>` records the
  "previously focused element" on show and runs the focusing steps for it on close (HTML Standard
  §4.11.4).
- The failure mode APG names: without managed focus, "browsers move focus to the body element,
  effectively causing a loss of focus within the user interface" (APG, Keyboard Interface).
  **Deleting a row must move focus to the next row, or the previous one if it was last.** APG's
  persistence rule: "It is essential that there is always a component within the user interface that
  is active (`document.activeElement` is not null or is not the body element) and that the active
  element has a visual focus indicator."

## Roving tabindex

Composite widgets — radio group, tabs, toolbar, menu, grid, listbox, tree — expose **one** tab stop.
"the tab sequence should include only one focusable element of a composite UI component. Once a
composite contains focus, keys other than `Tab` and `Shift`+`Tab` enable the user to move focus among
its focusable elements" (APG, Keyboard Interface).

Algorithm (APG):

1. On load/create: `tabindex="0"` on the element that should initially be in the tab sequence,
   `tabindex="-1"` on every other focusable element in the composite.
2. When an arrow key moves focus inside: `tabindex="-1"` on the element that had `0`; `tabindex="0"`
   on the element that will receive focus; call `element.focus()`.
3. If a specific element must be focused next time focus enters the composite, check that target for
   `tabindex="0"` when the composite loses focus and move `0` to it if not.

Benefit APG names: the user agent then "scroll[s] the newly focused element into view".

| `tabindex` value | Effect (APG) |
|---|---|
| absent or invalid | Default focus behaviour; in HTML only form controls and anchors with `href` are in the tab sequence |
| `0` | In the tab sequence, at its DOM position |
| `-1` | Not in the tab sequence, but focusable with `element.focus()` |
| `1`–`32767` | "Authors are strongly advised **NOT** to use these values" |

## `aria-activedescendant` as the alternative

Where the container role supports it, `aria-activedescendant` moves the *reported* active element
without moving DOM focus: the container is the single tab stop and its `aria-activedescendant` names
the active descendant. One DOM-relationship condition must hold (APG): the referenced element is a
DOM descendant of the referencing element; or the referencing element has `aria-owns` including that
ID; or the referencing element has role `combobox`, `textbox`, or `searchbox` **and** `aria-controls`
pointing to an element supporting `aria-activedescendant`, where the referenced element is a
descendant of that controlled element or the controlled element's `aria-owns` includes it.

Because DOM focus stays on the container, **you** must draw the visual focus indicator on the active
descendant and scroll it into view (APG). And on pointer activation authors "should take the same
steps to set the correct `tabindex` or `aria-activedescendant` … as they would for keyboard
navigation" (APG) — pointer/keyboard state mismatch is the most common bug here.

## Skip links

WCAG 2.2 **SC 2.4.1 Bypass Blocks** (Level A): "A mechanism is available to bypass blocks of content
that are repeated on multiple web pages" — nav, headers, and ad frames are the named examples; a
small repeated item like a single link is not. Skip links are explicitly **out of scope** for
SC 1.4.13, because a hidden component made visible on focus "do[es] not present additional content"
(Understanding SC 1.4.13).

One skip link as the first focusable element in the DOM, visually hidden until focused, targeting the
main region with `tabindex="-1"` so focus lands there. Not `display: none` or `visibility: hidden` —
it must be reachable by `Tab`. **Not found:** neither APG nor WCAG specifies a required skip-link
label or offset.

## `:focus-visible`

`:focus-visible` "applies while an element matches `:focus` and the user agent determines via
heuristics that the focus should be made evident on the element" — it lets you restyle the
indicator without changing *when* it appears (MDN). Browsers use heuristics: a pointer-clicked button
generally shows no ring, a text input needing input does (MDN).

- **Never `outline: none` without a replacement** — removing focus styles "makes keyboard navigation
  inaccessible for sighted users" (MDN). Style with `:focus-visible` rather than `:focus` if you do
  not want rings on pointer clicks; `:focus` "always targets the currently focused element" (MDN).
- Focus styles are required whenever focus is **managed via scripts**, not only when keyboard-driven
  (MDN).

| Criterion | Requirement |
|---|---|
| **SC 2.4.7 Focus Visible** (AA) | A mode of operation exists where the keyboard focus indicator is visible. It "must not be time limited": when shown, it must remain visible |
| **SC 2.4.13 Focus Appearance** (AAA) | Indicator area at least the area of a **2 CSS pixel** thick perimeter of the unfocused component, contrast at least **3:1** between the same pixels focused and unfocused. Exceptions: UA-determined indicators; or author-modified indicator and background both untouched. MDN ties SC 1.4.11 Non-text Contrast to the same 3:1 |
| **SC 2.5.8 Target Size (Minimum)** (AA) | Pointer targets at least **24 × 24 CSS pixels**, or satisfy Spacing (24px-diameter circles centred on bounding boxes do not intersect another target), Equivalent (another control on the page), Inline (in a sentence, constrained by line-height), User Agent Control, or Essential |

A focus ring narrower than 2px that only changes colour on a dark surface fails 2.4.13 even when
2.4.7 passes.

## Reading order must match DOM order

- "The default order of elements in the tab sequence is the order of elements in the DOM. The DOM
  order also determines screen reader reading order. It is important to keep the keyboard tab sequence
  and the screen reader reading order aligned, logical, and predictable" (APG). "The most robust
  method of manipulating the order of the tab sequence while also maintaining alignment with the
  reading order that is currently available in all browsers is rearranging elements in the DOM" —
  reach for `tabindex` only when DOM order genuinely cannot express it.
- WCAG 2.2 **SC 2.4.3 Focus Order** (A): "focusable components receive focus in an order that
  preserves meaning and operability."
- WCAG 2.2 **SC 2.4.11 Focus Not Obscured (Minimum)** (AA): "When a user interface component
  receives keyboard focus, the component is not entirely hidden due to author-created content."
  Note 2: content the user opened may obscure it, but "if the user can reveal the focused component
  without advancing the keyboard focus, the component with focus is not considered visually hidden".
  Sticky headers and bottom toolbars are the usual offenders.
- APG predictability: move focus in the page language's reading order; finish a section's elements
  before leaving it; avoid perceived-backward jumps; be consistent across pages; and "do not set
  initial focus when the page loads" except for a single primary function or frequent-use page.
- Focus is a pointer with one point at a time; selection persists after focus leaves. "The selected
  state must be visually distinct from the focus indicator" (APG) — a selected table row cannot use
  the same fill as the focus ring. Selection-following-focus is often good (tabs, single-select
  listbox) but "can be devastating" when showing a panel triggers a network request or page refresh.

## Verify

1. Open each overlay: `Tab` cycles only inside it; `Escape` closes it. On close, focus is on the
   trigger or the documented next-step target — never on `<body>`.
2. Delete a table row: focus moves to the next (or previous) row. Walk a composite with arrows;
   `Tab` exits in one press.
3. Tab from load: skip link is first, becomes visible, lands on main.
4. Keyboard-only pass: every icon button and truncated label has a ring ≥2px and ≥3:1 contrast. Zoom
   to 200% and tab: no focused item fully hidden behind sticky chrome.
5. Screen reader: reading order matches visual order; toast announcements arrive without focus moving.

## Sources

- [Dialog (Modal) Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) — W3C WAI ARIA Authoring Practices Guide, accessed 2026-10-05
- [Developing a Keyboard Interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/) — W3C WAI ARIA Authoring Practices Guide, accessed 2026-10-05
- [`inert` HTML global attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert) — MDN Web Docs (Mozilla), accessed 2026-10-05
- [`<dialog>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog) — MDN Web Docs (Mozilla), accessed 2026-10-05
- [`:focus-visible` CSS pseudo-class](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:focus-visible) — MDN Web Docs (Mozilla), accessed 2026-10-05
- [HTML Standard §4.11.4 The `dialog` element](https://html.spec.whatwg.org/multipage/interactive-elements.html#the-dialog-element) — WHATWG, accessed 2026-10-05
- [Understanding SC 2.4.1 Bypass Blocks](https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html) — W3C WCAG 2.2, accessed 2026-10-05
- [Understanding SC 2.4.3 Focus Order](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html) — W3C WCAG 2.2, accessed 2026-10-05
- [Understanding SC 2.4.7 Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html) — W3C WCAG 2.2, accessed 2026-10-05
- [Understanding SC 2.4.11 Focus Not Obscured (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html) — W3C WCAG 2.2, accessed 2026-10-05
- [Understanding SC 2.4.13 Focus Appearance](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html) — W3C WCAG 2.2, accessed 2026-10-05
- [Understanding SC 2.5.8 Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) — W3C WCAG 2.2, accessed 2026-10-05
- [Understanding SC 1.4.13 Content on Hover or Focus](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html) — W3C WCAG 2.2, accessed 2026-10-05