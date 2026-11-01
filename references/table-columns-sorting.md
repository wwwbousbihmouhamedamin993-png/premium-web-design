# Columns: Sizing, Sorting, Choosing

Framing: a data table's column model has three surfaces — the header row, a chooser, and the width system. Each is a different decision. Sizing is about fitting content; sorting is about ordering; the chooser is about which columns exist at all.

## Sizing

- **Every column declares `minWidth`, `maxWidth`, and a base `width` or `flex`.** AG Grid defaults are documented: if "a column has no width or flex properties set, it will default to 200px" (AG Grid, Column Sizing). TanStack Table's defaults are `size: 150, minSize: 20, maxSize: Number.MAX_SAFE_INTEGER` (TanStack Table, Column Sizing).
- **Use `flex` for the elastic columns, fixed `width` for the pinned ones.** Flex divides remaining space in proportion to flex value; AG Grid's worked example: "if the grid has a total width of 450px… `width: 150`, `flex: 1`, `flex: 2` → final sizes will be: 150px, 100px, 200px" (AG Grid, Column Sizing). Two constraints from the same page: "The flex config does **not** work with a `width` config in the same column" and "If you manually resize a column with flex either via the API or by dragging the resize handle, flex will automatically be disabled for that column."
- **Resizing is on by default; opt out per column with `resizable: false`** (AG Grid: "Column resizing is enabled by default for all columns"). Resizing must also work from the keyboard — AG Grid: column headers resize with `⌥ Alt` + `←` / `→`. TanStack's `columnResizeMode` defaults to `"onEnd"`, meaning "the `column.getSize()` API will not return the new column size until the user has finished resizing."
- **Shift-drag should conserve total width, not steal it.** AG Grid: "If you hold the `⇧ Shift` key while dragging the resize handle, the column will take space away from the column adjacent to it. This means the total width for all columns will be constant." Make this the default via `colResizeDefault='shift'`.
- **User widths are owned by the user.** AG Grid's "Column Width Ownership" section: "Continuous sizing never changes the width of a column the user has sized themselves. A column becomes theirs through a header drag resize, a keyboard resize or a double-click auto-size… Their width is then treated as fixed." Release ownership with `api.resetColumnState()`, which "also resets sort, order, visibility and pivot state."
- **Auto-size only from rendered rows.** AG Grid is explicit: "The grid works out the best width by considering the virtually rendered rows only. For example, if your grid has 10,000 rows, but only 50 rendered due to virtualisation of rows, then only these 50 will be considered." The rendered set is "all the rows you can see on the screen through the vertical scroll plus a small buffer (default buffer size is 20)." Column virtualisation does the same horizontally — "a grid of 1,000 columns may have only 10 rendered."

**Persisting the model.** Column width, order, visibility, and sort are one serialisable state object — treat them as such, and make it restorable. AG Grid: "The Side Bar state can be saved and restored as part of Grid State," and the same is true of column state and of pinned rows. For a logged-in surface, keep the state in the URL where it affects results (sort definitely) and in user or view settings where it affects presentation (widths, order, hidden columns). Shopify puts the sort key in the URL as a stable compound value — "store a stable value such as `title-asc` or `updated-desc` in the same URL or route state as the filters" — because a bare direction flag loses the column on reload.

**Not found:** a vendor-stated default column width in px for Shopify Polaris `DataTable`/`s-table`. What would settle it: Polaris theming tokens on openpolaris.shopify.com, which I could not open (the docs host returned a references index rather than the component page).

## Sorting

- **Cycle order: ascending → descending → none.** AG Grid: "By default the sorting order is as follows: **ascending -> descending -> none**." Override per column with `sortingOrder`; AG Grid's own example uses `['asc', 'desc']`, `['desc', null]`, and `['asc']` on different columns.
- **Only make a column sortable if it is meaningful to sort.** AG Grid enables sorting by default on every column and lets you opt out with `sortable: false` (Row Sorting). Invert that default: opt columns in. Notion makes the same distinction at the value-type level — "Different properties sort by different logic, depending on their value type. Text properties such as `Name` and `Text` sort alphabetically. Number properties sort numerically. For `Select` and `Multi-select` properties, you get to define what sorting order means" (Notion Help Center).
- **Multi-sort needs a discoverable modifier and a visible ordinal.** AG Grid: "The default action for multiple column sorting is for the user to hold down `⇧ Shift` while clicking the column header. To change the default action to use the `^ Ctrl` key instead set the property `multiSortKey='ctrl'`." Force it with `alwaysMultiSort`, forbid it with `suppressMultiSort`. Show sort priority as a number badge — `aria-sort` cannot express it: "ARIA does not provide a way to indicate levels of sort for data sets that have multiple sort keys" (APG, Grid and Table Properties).
- **Sort the raw value, not the formatted string.** Shopify: "Keep numeric values as numbers in your data model so sorting and totals don't operate on formatted strings" (Migrate DataTable).
- **Locale matters for text.** AG Grid: "By default, sorting is not locale-specific and strings are compared using their Unicode code point order… If you need to make your sort locale-specific you can configure this by setting the grid option `accentedSort = true`," and locale-aware sorting is slower. Decide once per surface, not per column.
- **Header sort state:** `aria-sort="ascending" | "descending" | "none"` on the `th`. APG's sortable-table example uses `aria-sort="none"` on a sortable-but-unsorted column and the direction values on sorted ones.
- **Secondary sort control for narrow layouts.** Shopify's guidance, because the header row disappears in list layout: "don't put the only sort controls in sortable headers. The example uses a labeled `s-select` in the filters slot, which remains available in both layouts."

## Column chooser

- **Choosers are dialogs or docked panels; both are legitimate.** AG Grid ships both: the "Column Chooser is a dialog that displays the grid's columns, allowing users to show, hide and reorder them," opened via `api.showColumnChooser()`; and "The same column selection panel is also available docked to the side of the grid as part of the Columns Tool Panel."
- **Selected = visible.** AG Grid: "**Pivot Mode Off**: When pivot mode is off, selecting a column toggles the visibility of the column. A selected column is visible and an unselected column is hidden."
- **Never let the chooser drop the identity column.** TanStack Table: "By default, all columns can be hidden or shown. If you want to prevent certain columns from being hidden, you set the `enableHiding` column option to `false` for those columns," and the checkbox should be `disabled={!column.getCanHide()}`. Shopify: the primary cell must keep a real resource URL ("Preserve a real resource URL").
- **Render from the visible-column APIs.** TanStack: `table.getAllColumns` and `row.getAllCells` "will not take column visibility into account. Instead, you need to use the 'visible' variants of these APIs, such as `table.getVisibleLeafColumns` and `row.getVisibleCells`." Missing this is the most common chooser bug.
- **Search inside the chooser once there are more than a handful of columns.** AG Grid's chooser has a column filter section (suppressible via `suppressColumnFilter`) and its labels must stay legible: "Column selection rows have a fixed height, so renderer content should remain inline and fit within the configured list item height."
- **Keep chooser state out of the shared config by default.** AG Grid separates panel layout from grid layout (`suppressSyncLayoutWithGrid`) and supports deferred apply with explicit `Apply` / `Cancel` so multiple changes commit in one update.

## Hiding low-priority columns at narrow widths

Priority tiers, highest first: identity (name/ID), one status enum, the two numbers people sort by, everything else.

1. Pin identity and the primary numeric; drop the tail.
2. Notion's model is the cleanest statement: view settings include "**Property visibility:** Show or hide database properties for each view" — per view, not per user (Notion Help Center).
3. Shopify's list variant is the responsive floor: `variant="auto"` becomes a list at narrow widths, and `listSlot` decides placement. Critically, "Omitting `listSlot` doesn't hide a column; its value uses the default `labeled` placement" (Migrate DataTable) — omission is not hiding.
4. When a column is hidden but still part of the model, tell assistive tech. AG Grid's data grid example 3: "When one or more columns are hidden, screen reader users can be aware of the hidden columns because those column numbers are not present as users navigate across a row" — which only works if you maintain `aria-colcount` and `aria-colindex` on the remaining cells (APG, Grid and Table Properties).
5. Reordering is a power-user affordance, not a default. Shopify: the table header row "isn't rendered in the narrow list layout," so a drag handle in the header is unreachable there.

## Sources

- AG Grid, "Column Sizing" — https://www.ag-grid.com/javascript-data-grid/column-sizing/ — AG Grid — accessed 2026-10-05
- AG Grid, "Row Sorting" — https://www.ag-grid.com/javascript-data-grid/row-sorting/ — AG Grid — accessed 2026-10-05
- AG Grid, "Column Chooser" — https://www.ag-grid.com/javascript-data-grid/column-chooser/ — AG Grid — accessed 2026-10-05
- AG Grid, "Columns Tool Panel" — https://www.ag-grid.com/javascript-data-grid/tool-panel-columns/ — AG Grid — accessed 2026-10-05
- TanStack Table v8, "Column Sizing Guide" — https://tanstack.com/table/v8/docs/guide/column-sizing — TanStack — accessed 2026-10-05
- TanStack Table v8, "Column Visibility Guide" — https://tanstack.com/table/v8/docs/guide/column-visibility — TanStack — accessed 2026-10-05
- W3C ARIA Authoring Practices, "Grid and Table Properties" — https://www.w3.org/WAI/ARIA/apg/practices/grid-and-table-properties/ — W3C — accessed 2026-10-05
- W3C ARIA Authoring Practices, "Data Grid Examples" — https://www.w3.org/WAI/ARIA/apg/patterns/grid/examples/data-grids — W3C — accessed 2026-10-05
- Shopify, "Table" (`s-table`) — https://shopify.dev/docs/api/app-home/web-components/layout-and-structure/table — Shopify — accessed 2026-10-05
- Shopify, "Migrate DataTable from Polaris React" — https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/data-table — Shopify — accessed 2026-10-05
- Shopify, "Migrate IndexTable from Polaris React" — https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/index-table — Shopify — accessed 2026-10-05
- Notion Help Center, "Views, filters, sorts & groups" — https://www.notion.com/help/views-filters-and-sorts — Notion — accessed 2026-10-05