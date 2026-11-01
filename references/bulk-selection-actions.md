# Bulk Selection and Actions

Framing: bulk selection is a **state machine over row identity**, and the only hard question is what "select all" means. Everything else — bar placement, indeterminate state, clearing on page change — follows from getting that one answer right and from never storing selection in the DOM.

## Selection models

| Model | Mechanism | Keyboard | When it fits |
| --- | --- | --- | --- |
| Single row | Radio or row click | Arrow keys within the grid | Detail-picker, "which row is active" |
| Multi-select (discrete) | Checkbox per row | `Space` toggles focused row | Default for B2B bulk work |
| Range select | Shift-click / Shift-arrow extends | `Shift` + arrows extend selection | Dense scanning of a contiguous run |
| Select-all-filtered | Header checkbox scoped to filter result set | Vendor-specific | Bulk operations on a saved view |
| Select-all-matching | Header checkbox scoped to the entire query, not the page | Vendor-specific | Email, export, tag — rarely archive/delete |

AG Grid's vocabulary: `rowSelection.mode` is `'singleRow'` or `'multiRow'`; in `'multiRow'`, "Users can hold `⇧ Shift` and then click a checkbox to add a range of adjacent rows to the selection." Rows can also be selected "by focusing a row and pressing `␣ Space`."

W3C APG's cell-level equivalents for a `role="grid"`: `Shift` + `Space` "Selects the row that contains the focus. If the grid includes a column with checkboxes for selecting rows, this key can serve as a shortcut for checking that box even if the focus is not on the checkbox," `^ Ctrl` + `Space` selects the column, `^ Ctrl` + `A` selects all cells, and the four `Shift` + arrow combinations extend by one cell.

## The select-all scope question

This is the decision. AG Grid exposes it as three values of `rowSelection.selectAll`:

- `'all'` — (default) "Selecting the header checkbox selects all **selectable** rows in the grid."
- `'filtered'` — "Selecting the header checkbox will select all rows that satisfy the currently active filter."
- `'currentPage'` — "Selecting the header checkbox will select all rows that satisfy the currently active filter on the current page."

Shopify's migration guidance is the sharpest statement of the risk: "The example selects only the current page. If the existing app supports selecting every result across pages, then keep that as a **distinct app-owned mode with an explicit result count and backend query**. Don't infer cross-page selection from the visible IDs."

**Rules:**

1. **Default to page scope.** It is honest, cheap, and reversible. Cross-page scope requires a backend query you control.
2. **If you offer "all N matching", name the N.** Never say "All" with no count. Polaris React's own index table takes a `selectedItemsCount` that accepts the string `'All'` alongside a number — the mechanism for saying something other than a count exists, but the count still has to come from somewhere.
3. **Changing the query changes what "all" means — clear or reconcile.** Shopify's example keys a `selectionScope` string from `['query', 'status', 'sort', 'cursor', 'direction']` and clears `selectedIds` when it changes, and separately reconciles to the current `pageIds` on every page change. Their instruction: "Clear or reconcile selection when the active query or page changes, including through browser Back or Forward navigation."
4. **Unselectable rows count as unselectable, not as un-selected.** AG Grid: "when `rowSelection.isRowSelectable` is defined, the header checkbox will only select selectable rows." Rows where selection is impossible "cannot be selected at all, whether using the UI or the API."
5. **Disable the control rather than hide it when a row is not selectable** — AG Grid distinguishes `checkboxes: false` (removes them) from a function returning `false` ("a selectable row for which the function returns `false` shows a **disabled checkbox** rather than removing it"), plus `hideDisabledCheckboxes: true` for the third behaviour.

## The three-state header checkbox

- `checked` when every selectable row on the page is selected.
- `indeterminate` when some but not all are.
- Unchecked otherwise.

Shopify: "Set `allOnPageSelected` when every page ID exists in `selectedIds`. Set `someOnPageSelected` when at least one, but not every, page ID is selected… Use `indeterminate` on the select-all `s-checkbox` for the partial state. Give every row checkbox an accessibility label that includes the resource name." TanStack Table exposes the same pair as `table.getIsAllRowsSelected()` / `table.getIsSomeRowsSelected()`.

Accessibility: `aria-selected="true"` on the selected row or cell; if the grid supports column selection, "all cells in the column have `aria-selected` set to `true`" (APG, Grid pattern).

## Bulk action bar placement

**In the toolbar slot above the table, replacing the filter controls while rows are selected.** Shopify's composition renders `<s-stack slot="bulkActions">` for the action set and, in the migration example, a `<s-box slot="filters" padding="small" background="strong">` holding the count and actions — the same slot the search and filters occupied.

```
[ 2 of 3 selected                    ] [ Archive products ]
─────────────────────────────────────────────────────────
[ ☐ ][ Product                ][ Status ][ ⋯ ]
[ ☑ ][ Mountain View          ][ Active ][ ⋯ ]
[ ☑ ][ Ocean Sunset           ][ Active ][ ⋯ ]
```

Checkable rules:

1. **The count and the actions travel together.** Shopify: "Keep the count and actions together in a responsive toolbar so they wrap instead of colliding at a narrow app width."
2. **Swap, don't stack.** "When `selectedIds.size` is greater than zero, replace the normal filter controls with a bulk-action area."
3. **The bar is the only place select-all lives in narrow layouts.** "Keep page-level select-all in the primary table header; that header isn't available in the narrow list layout, so apps that need select-all there should surface the same control in the bulk-action bar."
4. **Destructive actions confirm before firing.** Shopify's pattern uses a modal before a delete bulk action: "Use the Modal API to confirm destructive bulk actions before executing them."
5. **On success: clear selection, refresh, confirm.** "After success, clear selection, refresh the data, and show confirmation." On failure: "preserve selection so that the user can retry."
6. **Guard double submission.** Shopify sets a `bulkPending` flag that drives a loading state on the action button, and their test list includes "repeated submission protection."

## Selection across pagination

Selection is keyed by **stable row ID**, never by index. AG Grid's Infinite Row Model is blunt about why: "Selection works on the rows in infinite scrolling by using the **Row IDs** of the Row Nodes. If you do not provide Keys for the Row Nodes, the index of the Row Node will be used. Using the index of the row breaks down when (server-side) filtering or sorting, as these change the index of the Rows. For this reason, if you do not provide your own Row IDs, then selection is cleared if sort or filter is changed." TanStack makes the same point about `getRowId`, and warns about a subtler variant: with `manualPagination`, "`getSelectedRowModel` will only return selected rows on the current page because table row models can only generate rows based on the `data` that is passed in. Row selection state, however, can contain row ids that are not present in the `data` array just fine."

Behaviour to implement deliberately:

- **Same page, no change.** Selection survives re-sort within a page if IDs are stable.
- **New page, same query.** Either keep it (IDs still valid) or prune to the new page — Shopify prunes: "setSelectedIds(new Set([...current].filter(id => pageIds.includes(id))))". Pruning is simpler to explain; keeping it is better when you offer cross-page selection.
- **Query changed.** Clear. See rule 3 above.
- **Selection after action.** Clear on success, keep on failure.

**Not found:** a vendor statement of which default Airtable, Notion, or Linear take for selection persistence across pages. What would settle it: each product's bulk-action help article, or a recording of the behaviour. Airtable's views article covers view configuration and row height but not selection scope.

## Sources

- AG Grid, "Multi-Row Selection" — https://www.ag-grid.com/javascript-data-grid/row-selection-multi-row/ — AG Grid — accessed 2026-10-05
- AG Grid, "Row Selection" — https://www.ag-grid.com/javascript-data-grid/row-selection/ — AG Grid — accessed 2026-10-05
- AG Grid, "Infinite Row Model" (selection section) — https://www.ag-grid.com/javascript-data-grid/infinite-scrolling/ — AG Grid — accessed 2026-10-05
- AG Grid, "Accessibility" — https://www.ag-grid.com/javascript-data-grid/accessibility/ — AG Grid — accessed 2026-10-05
- W3C ARIA Authoring Practices, "Grid (Interactive Tabular Data and Layout Containers) Pattern" — https://www.w3.org/WAI/ARIA/apg/patterns/grid/ — W3C — accessed 2026-10-05
- TanStack Table v8, "Row Selection Guide" — https://tanstack.com/table/v8/docs/guide/row-selection — TanStack — accessed 2026-10-05
- Shopify, "Migrate IndexTable from Polaris React" — https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/index-table — Shopify — accessed 2026-10-05
- Shopify, "Index table" pattern — https://shopify.dev/docs/api/app-home/patterns/compositions/index-table — Shopify — accessed 2026-10-05