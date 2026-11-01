# Virtualization and Windowed Lists

Framing: virtualization is a **performance technique with an accessibility bill**, and the bill is paid in the DOM. A windowed grid renders only the visible slice; everything below the fold is, to a screen reader, nonexistent unless you describe it explicitly. Decide to virtualise knowing what you will have to maintain by hand afterwards.

## When to virtualise

Virtualise when the **rendered row count is the bottleneck**, not when the record count is large. Rough triggers:

- Rows are cheap and the set is small — do not virtualise. TanStack: "If your table will only ever have a few thousand rows or less, client-side pagination can still be a viable option," and it "is designed to scale up to 10s of thousands of rows with decent performance." Their official pagination example "loads 100,000 rows and still performs well, albeit with only handful of columns."
- The set is unbounded, or rows are expensive (images, nested editors, per-row charts) — virtualise or server-page.
- Row height is fixed and known — virtualise freely.
- **Variable row height — virtualise only with care.** AG Grid: "You cannot use variable row height when using either the Viewport Row Model or the Infinite Row Model. This is because these row models need to work out the position of rows that are not loaded and hence need to assume the row height is fixed." Even where it is allowed, AG Grid describes lazy height calculation as unavoidable instability: "The vertical scroll range… will change dynamically to fit the rows. If scrolling by dragging the scroll thumb with the mouse, the scroll thumb will not follow the mouse. It will either lag behind or jump ahead" and "If scrolling up and showing rows for the first time… the row positions will jump… These behaviours are a necessary outcome of lazy height calculation. It is not possible to avoid these effects."

TanStack's framing of the choice is the right posture for a logged-in surface: virtualization or pagination is a UI/UX decision, not a performance detail — "The UI/UX of both virtualization and pagination have their own trade-offs, so see which one works best for your use-case."

**Dense class implication:** fixed row height is not negotiable. If the Dense class ships 28–32px rows, windowing and Dense compose; variable-height cards and windowing do not.

## Windowing mechanics that matter for a table

- **Render window + buffer.** AG Grid: the rendered set is "all the rows you can see on the screen through the vertical scroll plus a small buffer (default buffer size is 20)."
- **Column windowing too.** "Column Virtualisation renders only the columns the horizontal scroll position makes visible, so a grid of 1,000 columns may have only 10 rendered, and the grid can measure only what it renders."
- **Block cache, with an eviction bound.** In AG Grid's Infinite Row Model, `maxBlocksInCache` sets how many blocks survive; "as you scroll down, previous blocks will be discarded and will be loaded again if the user scrolls back up." Consequences that bite: auto-measured widths come out wrong (see below), and "when performing multiple row selections using shift-click, it is possible that not all rows are available in memory if the configured value of `maxBlocksInCache` doesn't cover the range. In this case multiple selections will not be allowed."
- **Scroll anchoring.** Anchor on a **row ID**, never on a pixel offset: prepend/append changes the pixel math, and evicted-then-reloaded rows change heights. When a row's data arrives, its identity is what re-establishes position — AG Grid's loading-spinner recipe keys off row ID for exactly this reason ("if the data is loading, then the `rowNode` will have no ID, so if you use the ID as the value, the cell will get refreshed when the ID is set").
- **Auto-size cannot see what isn't rendered.** AG Grid: "The grid works out the best width by considering the virtually rendered rows only. For example, if your grid has 10,000 rows, but only 50 rendered due to virtualisation of rows, then only these 50 will be considered for working out the width to display." For columns: "To size them, either set `suppressColumnVirtualisation=true` so every column is rendered and measured in one go, or keep virtualisation and use Continuous Auto-Sizing with scroll-driven re-sizes." A third cost, from the row-height page: "Columns with Auto Height will always be rendered because the grid needs to set the height of the row… and stops Column Virtualisation for these columns which can negatively impact rendering performance."

## Sticky header and sticky rows in a virtualised table

The header row must live **outside the windowing region** — it is not a row in the model, so it is never recycled. Inside a scroll container, `position: sticky; top: 0` is the mechanism; MDN: at least one inset on the axis must be non-`auto` "or the `sticky` value will behave as `relative`", and a sticky element "sticks to its nearest ancestor that has a 'scrolling mechanism'." MDN also flags the repaint cost: as the user scrolls "the browser must repaint the sticky or fixed content in a new location… which can lead to jank and, more importantly, accessibility concerns for people with sensitivities," mitigated by `will-change: transform`.

For sticky *rows* (pinned totals, pinned group parents), AG Grid splits them out of the viewport entirely: pinned rows "appear fixed at the top (or bottom) of the grid, as well as remaining in the main viewport," and are styled distinctly by default. Two constraints if you pin data rows:

- AG Grid's accessibility guidance recommends disabling sticky group rows outright: "By default, when grouping, the current parent of rows becomes 'sticky' to the top of the grid while scrolling. This causes the rows to be in 'incorrect order' and result in inconsistent announcements for row indices when parsed by screen readers. To disable Group Sticky Rows, set `suppressGroupRowsSticky`."
- Pinned rows supplied as data (`pinnedTopRowData` / `pinnedBottomRowData`) "cannot be sorted," "are not filtered," "cannot be grouped," and "cannot be selected."

## The accessibility cost of virtualisation

Screen readers "assume all elements of the grid are loaded when the page is loaded and they appear in the DOM in order of their visual appearance" (AG Grid). Virtualisation breaks two of those assumptions. The repairs:

1. **Fix DOM order.** "By default, rows and columns can appear out of order in the DOM. This 'incorrect order' can result in inconsistent results when parsed by screen readers. To force row and column order, enable … `ensureDomOrder: true`." Trade-off: "Animations won't work properly when the DOM order is forced, so ensure they are not enabled."
2. **Declare the true size.** `aria-rowcount` for the total row count and `aria-rowindex` on every rendered row, so the reader hears "row 1,204 of 9,000" rather than "row 40." APG's data grid example 3 states the mechanism directly: "As navigating up or down scrolls the visible set of rows, the `aria-rowindex` value of the row containing the focus informs the screen reader of the number of that row within the total set of rows." `aria-colcount` / `aria-colindex` do the same for horizontally windowed columns; APG warns that inconsistent values "could cause screen reader table reading functions to skip cells or simply stop functioning."
3. **Or don't virtualise.** AG Grid's recommendation is blunt: "The best way to do this is to use pagination. This way you can reduce the initial loading time and memory footprint while ensuring all elements for these rows are loaded for screen readers. If your requirement is to use scrolling instead of pagination, you can disable row virtualisation at the expense of increasing the memory footprint."

Known limits even after all of that, per AG Grid: some screen readers "have trouble navigating the tags when the structure of the grid gets more complex (eg. grouped columns)," some "will not recognise changes that happen to an element that is currently focused (including children of this element)" — so a sort-state change on the focused header may go unannounced until focus moves — and with the Server-Side Row Model "announcing the row count in the grid… is not supported. This is because the row count cannot be known in all the scenarios where SSRM is in use."

**What virtualisation changes for the reader, not just the browser.** The reader loses the ability to browse the whole set by moving through it — there is no "next row" past the rendered window, because that row is not there. APG's answer is that every windowed surface is still a `grid` with a full `aria-rowcount`, and the row index attributes are what restore the sense of a whole. Without them the table is not a smaller table; it is a different, broken widget.

**Interaction cost.** Every non-native behaviour you add to a windowed region has to be reimplemented against recycling: hover affordances cannot rely on the row staying mounted, and context menus on a recycled row must resolve the current row ID at open time, not at render time. AG Grid's docs treat hover-adjacent column affordances as a grid feature rather than a styling trick — the column menu, the resize handle, the checkbox column — which is a hint about how much of this is genuinely hard.

**Budget:** each of these is a per-frame correctness concern, not a one-time fix. If the surface needs a11y conformance as a hard requirement, prefer pagination. Virtualise when performance forces it, and pay for `ensureDomOrder`, the index attributes, and screen-reader testing.

## Sources

- AG Grid, "Accessibility" — https://www.ag-grid.com/javascript-data-grid/accessibility/ — AG Grid — accessed 2026-10-05
- AG Grid, "Column Sizing" (auto-sizing and virtualisation limits) — https://www.ag-grid.com/javascript-data-grid/column-sizing/ — AG Grid — accessed 2026-10-05
- AG Grid, "Row Height" (variable height, lazy calculation, auto height) — https://www.ag-grid.com/javascript-data-grid/row-height/ — AG Grid — accessed 2026-10-05
- AG Grid, "Infinite Row Model" (block cache, cache tuning, loading) — https://www.ag-grid.com/javascript-data-grid/infinite-scrolling/ — AG Grid — accessed 2026-10-05
- AG Grid, "Row Pinning" — https://www.ag-grid.com/javascript-data-grid/row-pinning/ — AG Grid — accessed 2026-10-05
- TanStack Table v8, "Pagination Guide" (virtualization vs pagination) — https://tanstack.com/table/v8/docs/guide/pagination — TanStack — accessed 2026-10-05
- W3C ARIA Authoring Practices, "Data Grid Examples" — https://www.w3.org/WAI/ARIA/apg/patterns/grid/examples/data-grids — W3C — accessed 2026-10-05
- W3C ARIA Authoring Practices, "Grid and Table Properties" — https://www.w3.org/WAI/ARIA/apg/practices/grid-and-table-properties/ — W3C — accessed 2026-10-05
- MDN, "position" — https://developer.mozilla.org/en-US/docs/Web/CSS/position — Mozilla — accessed 2026-10-05