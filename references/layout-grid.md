# Layout grid: CSS grid and flex for app layouts

App layouts are two-dimensional regions containing one-dimensional stacks. Grid owns the frame;
flex owns the rows inside each region. MDN is the primary reference for both mechanisms; Carbon's
2x Grid supplies the spacing geometry that keeps regions aligned.

## Grid for regions, flex for content

MDN: flexbox "is a one-dimensional layout model for distributing space between items," contrasted
with grid, "which controls columns and rows together" (MDN, *Basic concepts of flexbox*). Use
accordingly:

- **Grid** — shell regions, list+detail splits, card galleries, the detail pane's internal
  two-column form+aside.
- **Flex** — a page header's title-left/actions-right, a toolbar's search-grow/controls-fixed, a
  settings section's label-then-control, a sidebar's vertical stack of items.

## The shell as one grid

```
grid-template-areas:
  "header header"
  "nav    main";
grid-template-columns: var(--nav-w) 1fr;
grid-template-rows: var(--header-h) 1fr;
height: 100dvh;
```

Three-region console frame (rail / list / detail):

```
grid-template-areas:
  "header header header"
  "nav    list   detail";
grid-template-columns: var(--nav-w) minmax(320px, 1fr) minmax(0, 2fr);
```

- **`minmax()` is how a region gets a floor and a ceiling.** MDN: `minmax()` solves "we may want
  our rows to never collapse smaller than 100 pixels, but if our content stretches to 300 pixels
  in height, then we would like the row to stretch" — `grid-auto-rows: minmax(100px, auto)`.
- **Mixing absolute and flexible tracks is normal for shells.** MDN's `500px 1fr 2fr` example:
  "the first track is `500px`, so the fixed width is taken away from the available space. The
  remaining space is divided… and assigned in proportion."
- **Let the content column shrink, not the frame.** A detail pane with long IDs and code needs
  `minmax(0, 2fr)`, not `2fr`, so overflowing text cannot force the grid wider than the viewport.
- **`repeat()` compresses long track lists.** `repeat(3, 1fr)` for uniform columns;
  `20px repeat(6, 1fr) 20px` for fixed edges with a fluid middle; `repeat(5, 1fr 2fr)` for a
  repeating mixed pattern (MDN).

## Padding is a fixed value, not a scale step

Carbon's 2x Grid: "Padding is always a fixed multiple of mini units: **16 pixels at all standard
breakpoints**. Always align type to the edge of box padding." The grid's basic unit is the
**8-pixel square mini unit**, and Carbon's documented breakpoints are:

| Breakpoint | Value | Columns | Column size | Padding | Margin |
|---|---|---|---|---|---|
| Small | 320 | 4 | 25% | 16px | 0 |
| Medium | 672 | 8 | 12.5% | 16px | 16px |
| Large | 1056 | 16 | 6.25% | 16px | 16px |
| X-Large | 1312 | 16 | 6.25% | 16px | 16px |
| Max | 1584 | 16 | 6.25% | 16px | 24px |

Gutters: "The margin around each grid box matches its padding, for a total gutter of **32
pixels**" (Carbon, *2x Grid*).

## Key lines

Carbon: "ensure the overall layout has visible key lines: vertical and horizontal lines on which
multiple objects align. Horizontal and vertical alignment are equally critical. When present, the
eye can follow content more easily." A list column and the detail pane's field labels should share
a left edge — that shared edge is the key line.

## Sticky headers and footers

- **`position: sticky` needs an inset.** MDN: "At least one `inset` property… needs to be set to a
  non-`auto` value for the axis on which the element needs to be made sticky. If both `inset`
  properties for an axis are set to `auto`, on that axis the `sticky` value will behave as
  `relative`."
- **Sticky binds to the nearest scrolling ancestor.** MDN: a sticky element "sticks" to its
  nearest ancestor that has a "scrolling mechanism" (created when `overflow` is `hidden`, `scroll`,
  `auto`, or `overlay`), "even if that ancestor isn't the nearest actually scrolling ancestor."
  This is the single most common console bug: the header sticks to a wrapper instead of the
  viewport.
- **Sticky always creates a stacking context** (MDN), so `z-index` on a sticky header is not
  competing with siblings, only with its own containing block.
- **Sticky has a repaint cost.** MDN, on performance and accessibility: "the browser must repaint
  the sticky or fixed content in a new location… the browser may not be able to manage repaints at
  60 fps." MDN's mitigation: `will-change: transform`. Keep sticky elements few and small.
- **A sticky header must not eat focus.** WCAG 2.2 SC 2.4.11 Focus Not Obscured (Minimum) names
  "sticky footers, sticky headers, and non-modal dialogs" as the typical causes of failure when
  "a sticky footer or header completely hid[es] focused elements" (W3C, failure F110). The stated
  fix is CSS `scroll-padding` (technique C43) on the scroll container.

## Scroll containment

Scroll containment is what makes a console feel solid instead of jittery: one scrollbar per
region, and the page itself does not scroll.

- **`overflow` values, per MDN:** `visible` (default; "The element box is not a scroll
  container"), `hidden` (clipped, no scrollbars, still programmatically scrollable), `scroll`
  ("The element is always a scroll container — even when there is no overflowing content"),
  `auto` (a scroll container only when overflowing), `clip` ("The element box is not a scroll
  container… and programmatic scrolling is not supported").
- **`hidden` still scrolls on focus, `clip` does not.** MDN: with `clip`, "hidden focusable
  content still receives keyboard focus, but that content will not scroll into view, making it
  inaccessible to keyboard users." Never `clip` a scrollable region containing focusables.
- **Scrolling regions need to be keyboard-reachable.** MDN: "In some browsers, scrolling content
  areas are not keyboard-focusable, so they cannot be scrolled by a keyboard-only user. To ensure
  all keyboard-only users can scroll the container, enable the element to receive focus by setting
  `tabindex="0"`… set an appropriate WAI-ARIA role… such as `role="region"`, and an accessible
  name using the `aria-label` or `aria-labelledby` attribute."
- **Every value except `visible` and `clip` creates a new block formatting context** (MDN) — the
  mechanism that prevents margin collapse through a scroll container's edges.

## Flex rules that matter in an app shell

- **`flex: 1` is `1 1 0`** — items start at minimum size and share free space. **`flex: auto`** is
  `1 1 auto`; **`flex: none`** is `0 0 auto`, for the fixed-width icon or fixed-width filter slot
  that must not shrink (MDN).
- **Alignment properties live on the container.** `align-items` and `justify-content` are set on
  the flex container, not the items; per-item override is `align-self` (MDN).
- **`justify-items` is ignored in flexbox** (MDN) — reaching for it is a bug, not a no-op.
- **Nested grids don't align by default.** MDN: with a nested grid, "it has not inherited the
  `gap` of the parent and the lines in the nested grid do not align to the lines in the parent
  grid." Use `grid-template-columns: subgrid` when the nested tracks must align to the parent — the
  case for a detail pane whose field rows must line up with the list's column boundaries.

## Sources

- Basic concepts of CSS grid layout (`fr`, `repeat()`, `minmax()`, subgrid, gaps, grid areas) — MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Basic_concepts_of_grid_layout — accessed 2026-10-05
- Basic concepts of flexbox (`flex` shorthand, alignment, initial values) — MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox — accessed 2026-10-05
- `position` (sticky: inset requirement, scrolling ancestor, stacking context, repaint cost) — MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/CSS/position — accessed 2026-10-05
- `overflow` (scroll container semantics, keyboard accessibility of scroll regions) — MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/CSS/overflow — accessed 2026-10-05
- 2x Grid (mini unit, padding, gutters, breakpoints, key lines, hybrid boxes) — Carbon Design System (IBM). https://carbondesignsystem.com/elements/2x-grid/overview/ — accessed 2026-10-05
- Understanding SC 2.4.11 Focus Not Obscured (Minimum) — W3C Web Accessibility Initiative. https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html — accessed 2026-10-05
