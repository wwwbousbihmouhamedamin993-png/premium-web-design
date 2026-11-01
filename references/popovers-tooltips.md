# Popovers, tooltips, menus, disclosures

Four surfaces, one confusion. Each has a distinct ARIA role, a distinct focus contract, and a
distinct dismissal contract. Picking the wrong one produces a component that a keyboard cannot
operate.

## Which one

| Surface | Role | Focus | Dismissal | Content rule |
|---|---|---|---|---|
| **Tooltip** | `tooltip` | Never receives focus (APG) | `Escape`, blur, mouse-out | A *description* of the trigger. Referenced with `aria-describedby` |
| **Popover** (non-menu, non-modal) | Dialog or region per content | Moves focus into itself if it has controls | `Escape`, outside click, close control | Rich content, not a description |
| **Menu** | `menu` / `menuitem` | Focus **moves into** the menu, lands on first item | `Escape` returns focus to the opener; activating an item closes the menu unless it opened a submenu | A list of actions |
| **Disclosure** | `button` + `aria-expanded` | Stays on the button | `Enter` / `Space` toggles | Content the user chose to reveal in place |

The HTML spec draws the same line for `<dialog>`: "context menus, tooltips, and popup listboxes are
not dialog boxes, so abusing the dialog element to implement these patterns is incorrect" (WHATWG
HTML).

## Tooltips

ARIA: a tooltip is "a contextual popup that displays a description for an element"; the container
gets `role="tooltip"` and the trigger references it with `aria-describedby` (APG; WAI-ARIA 1.3
`tooltip` role).

Three hard rules from APG and WCAG 2.2 SC 1.4.13:

- **Tooltip widgets do not receive focus** (APG). If your tooltip needs a link or a button in it,
  APG says a hover layer containing focusable elements "can be made using a non-modal dialog" —
  i.e. you need a popover, not a tooltip.
- **Focus stays on the trigger** while the tooltip is displayed; a focus-opened tooltip is
  dismissed on `onBlur` (APG).
- **Hover-opened tooltips stay open while the pointer is over the trigger *or the tooltip***
  (APG). `Escape` dismisses (APG).

WCAG 2.2 **SC 1.4.13 Content on Hover or Focus** (Level AA) requires all three, and its Understanding
doc names "custom tooltips, sub-menus, and other nonmodal popups that display on hover and focus"
explicitly as in scope:

| Requirement | Normative text | Test |
|---|---|---|
| **Dismissible** | "A mechanism is available to dismiss the additional content without moving pointer hover or keyboard focus" — exempt only if the content communicates an input error, or does not obscure or replace other content | Hover a trigger, press `Escape` without moving the mouse |
| **Hoverable** | "the pointer can be moved over the additional content without the additional content disappearing" | Move diagonally from trigger to tooltip; content stays |
| **Persistent** | Content "remains visible until the hover or focus trigger is removed, the user dismisses it, or its information is no longer valid" | No auto-dismiss timer on a hover layer |

Exemptions worth knowing: content controlled entirely by the user agent (the `title` attribute's
native tooltip) is out of scope, and skip links revealed on focus are not "additional content" so
they are also out of scope (WCAG 2.2 Understanding SC 1.4.13).

**The hard rule for product work: nothing important may be hover-only.** WCAG's own Understanding
note is the citation: "Content which can be triggered via pointer hover should also be able to be
triggered by keyboard focus. Refer to Success Criterion 2.1.1 Keyboard." Every hover affordance —
icon-only buttons, truncated labels, chart segments, table-cell explanation — needs a focus and/or
click path to the same content. In a Dense console, an icon-only icon button with no tooltip and no
accessible name is a defect twice over.

Note: the APG tooltip pattern is explicitly flagged as **work in progress without task force
consensus** (issue 128), and the APG has no tooltip example yet (issue 127). Treat APG's tooltip
text as direction, not consensus.

**Not found:** no normative source specifies a tooltip show-delay or hide-delay duration. The
`title`-attribute-style hover delay is a design decision; the only sourced timing guidance is the
suggestion that a timed auto-dismiss conflicts with SC 1.4.13 Persistent. Record a delay in
`DESIGN.md` if you ship one.

## Menus

APG Menu Button: the trigger has `role="button"`, `aria-haspopup` set to `menu` or `true`,
`aria-expanded` toggling, and the popup has `role="menu"`.

| Key (APG Menu Button / Menu and Menubar) | Behavior |
|---|---|
| `Enter` / `Space` on button | Opens the menu, focus on first item |
| `Down Arrow` on button *(optional)* | Opens the menu, focus on first item |
| `Up Arrow` on button *(optional)* | Opens the menu, focus on **last** item |
| `Down` / `Up Arrow` in menu | Next / previous item, optionally wrapping |
| `Right Arrow` in menu on item with submenu | Opens submenu, focus on first item |
| `Left Arrow` in submenu | Closes submenu, returns focus to the parent `menuitem` |
| `Home` / `End` *(only when arrow wrapping is unsupported)* | First / last item |
| Printable character *(optional)* | Focus next item whose label begins with that character |
| `Escape` | Closes the menu containing focus and returns focus to the element or context it was opened from |
| `Tab` | Moves focus **out** of the menu or menubar and closes all menus and submenus |

Two facts people get wrong: menus are **composite widgets**, so `Tab` and `Shift`+`Tab` do not move
focus among menu items (APG, Keyboard Interface); and "Tab and Shift + Tab do not move focus into a
menu" — a menu is not visually persistent, so the author is responsible for moving focus into an
item when it opens (APG, Menu and Menubar). APG also notes the convention of appending `…` to a menu
item that opens a dialog.

Disabled menu items are focusable but not activatable (APG, Menu and Menubar). Separators are not
focusable (APG).

## Disclosure

Smallest of the four. `role="button"` on the control; `aria-expanded` `true` when content is
visible, `false` when hidden; `aria-controls` optionally pointing at the controlled region.
`Enter` and `Space` toggle (APG, Disclosure (Show/Hide)). Content stays in place — no overlay, no
focus move, no z-index.

Use a disclosure before you invent a popover: FAQ answers, advanced settings groups, and
"show raw JSON" all belong here.

## Positioning and collision

Manual flip logic is where popovers break. The platform now does it:

- **Popover API**: open popovers "appear above all other elements in the top layer, and won't be
  influenced by parent elements' position or overflow styling" (MDN, `popover` attribute). That
  alone kills the `overflow: hidden` clipping class of bugs.
- `popover="auto"` is light-dismissed by clicking outside or `Escape`, and only one auto popover is
  shown at a time unless nested; `"manual"` never light-dismisses; `"hint"` is for hover/focus
  driven surfaces and does not close auto popovers (MDN).
- **CSS anchor positioning** tethers an element to its trigger and "provides CSS-only mechanisms to
  specify a set of alternative positions … when the default rendering position causes it to
  overflow its containing block and/or be rendered offscreen, the browser will try rendering the
  anchored element in the alternative positions instead" (MDN, CSS anchor positioning).
- Collision handling in practice: `position-try-fallbacks` lists fallback positions "in the order
  provided, until it finds a value that stops it from overflowing its container or the viewport"
  (MDN). Baseline 2026 (MDN) — treat as progressive enhancement over a JS positioning layer.

**Not found:** no normative source mandates a specific gap, width, or arrow offset between trigger
and popover. Settle those in `DESIGN.md`; verify collision by scrolling the trigger to each viewport
edge.

## Sources

- [Tooltip Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/) — W3C WAI ARIA Authoring Practices Guide, accessed 2026-10-05
- [Menu Button Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/) — W3C WAI ARIA Authoring Practices Guide, accessed 2026-10-05
- [Menu and Menubar Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/) — W3C WAI ARIA Authoring Practices Guide, accessed 2026-10-05
- [Disclosure (Show/Hide) Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/) — W3C WAI ARIA Authoring Practices Guide, accessed 2026-10-05
- [Developing a Keyboard Interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/) — W3C WAI ARIA Authoring Practices Guide, accessed 2026-10-05
- [Understanding SC 1.4.13 Content on Hover or Focus](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html) — W3C WCAG 2.2, accessed 2026-10-05
- [Web Accessibility for Rich Internet Applications (WAI-ARIA) 1.3](https://www.w3.org/TR/wai-aria-1.3/#tooltip) — W3C, accessed 2026-10-05
- [`popover` HTML global attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/popover) — MDN Web Docs (Mozilla), accessed 2026-10-05
- [CSS anchor positioning](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_anchor_positioning) — MDN Web Docs (Mozilla), accessed 2026-10-05
- [`position-try-fallbacks`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position-try-fallbacks) — MDN Web Docs (Mozilla), accessed 2026-10-05
- [HTML Standard §4.11.4 The `dialog` element](https://html.spec.whatwg.org/multipage/interactive-elements.html#the-dialog-element) — WHATWG, accessed 2026-10-05