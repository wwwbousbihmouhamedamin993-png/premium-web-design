# Data Tables (Dense Class)

Framing: a logged-in B2B data table is a **tool for scanning, comparing, and acting on records**, not a marketing surface. The W3C ARIA Authoring Practices (APG) draws the line that matters: a `table` role is "a static tabular structure… it is not an interactive widget. Thus, its cells are not focusable or selectable," and "each widget contained in a table is a separate stop in the page tab sequence." A `grid` role is "a composite widget so it… always contains multiple focusable elements" and "only one of the focusable elements contained by the grid is included in the page tab sequence" (W3C APG, Grid and Table patterns). If a row contains a link, a checkbox, and a menu button, you have an interactive grid. Use `role="grid"`.

## Checkable rules

1. **Every cell is focusable, or contains something focusable.** One exception: "if column or row header cells do not provide functions, such as sort or filter, they do not need to be focusable" (APG Grid). Non-interactive headers stay plain `<th>`.
2. **Label the grid.** `aria-labelledby` on the grid pointing at the visible heading, otherwise `aria-label`. Add `aria-describedby` for a description or caption (APG Grid, Roles/States/Properties).
3. **Sortable headers carry `aria-sort`.** Values are `ascending`, `descending`, `other`, `none` (default) (APG Grid and Table Properties). ARIA has **no way to indicate sort level** for multi-key sorts, so "there is limited value to applying `aria-sort` with a value other than `none` to more than one column or row" (same source). Mark the primary sort key; leave the rest `none` or show the ordinal in visible text.
4. **Selection is `aria-selected="true"`** on the selected row/cell. If column selection is supported, all cells in the column get `aria-selected="true"` (APG Grid).
5. **Every column must map to a decision.** Identify (name/ID), Compare (a second or third attribute), or Sort (a value people order by). A column that maps to no decision belongs in the column chooser, the row detail, or nowhere. Shopify makes the same point from the other direction: "Aim for the minimum columns needed to support user tasks, and consider whether some data could be revealed on demand" (Shopify, `s-table` best practices).
6. **Align by data type.** Text left, numbers right, currency right. Shopify's `s-table` header `format` values are `'base'` (text), `'numeric'` and `'currency'`, the latter two both right-aligned (Shopify `s-table` docs).
7. **Numeric columns need tabular figures.** `font-variant-numeric: tabular-nums` activates "the set of figures where numbers are all of the same size, allowing them to be easily aligned like in tables" (OpenType `tnum`) (MDN, `font-variant-numeric`). The property inherits, so set it on the numeric cell class.
8. **Row height is a density decision, not a spacing decision.** AG Grid's default row height "is based on the theme (42px for Quartz)" (AG Grid, Row Height). Airtable grid views ship four row heights — Short, Medium, Tall, Extra Tall — with "Short (the most dense option, and the default height for new views)" where "each record shows one line of text and small attachment thumbnails" (Airtable). Neither vendor publishes a px value for the densest step; **Not found:** a vendor-stated pixel floor for dense data-table rows. What would settle it: a design system's published table spec, e.g. Polaris `DataTable` `increasedTableDensity` pixel metrics — the prop exists but I did not open a page stating its resulting row height.
9. **Dense rows do not shrink targets below the accessibility floor.** WCAG 2.2 SC 2.5.8 (Level AA) requires pointer targets "at least 24 by 24 CSS pixels," with a spacing exception for undersized targets placed so a 24px-diameter circle on each bounding box does not intersect another target (W3C WCAG 2.2 Understanding, Target Size (Minimum)). The Essential exception explicitly contemplates "an interactive data visualization where targets are necessarily dense," and the doc recommends "a mechanism to control the density of layout."
10. **Keep the header visible, or reduce the data set.** Shopify's `s-table` "doesn't support sticky headers that remain visible during scrolling. If merchants need to reference column headers while viewing data further down the table, consider using pagination to keep datasets smaller" (Shopify `s-table` Limitations). If you do pin the header, `position: sticky` needs at least one non-`auto` inset or it behaves as `relative`, always creates a stacking context, and offsets the repaint to the nearest scrolling ancestor — MDN warns this "can lead to jank and… accessibility concerns for people with sensitivities" (MDN, `position`).
11. **Page above roughly 50–100 rows.** Shopify: "Use pagination for datasets with more than 50-100 rows, or consider whether filtering or search would help" (Shopify `s-table` best practices).
12. **Narrow widths: degrade to a list, and re-declare which controls live where.** `s-table variant="auto"` renders "as a table on wide screens and as a list on narrow screens," and a narrow container inside a wide viewport stays a table (Shopify `s-table`). Column meaning is preserved by `listSlot` on each header: `primary`, `secondary`, `kicker`, `inline`, `labeled` (default). Critically: "The table header row isn't rendered in the narrow list layout, so don't put the only sort controls in sortable headers" (Shopify, Migrate IndexTable) — move them to the filter/sort slot.

## Column type → treatment

| Column type | Align | Figures | Sorting default | Notes |
| --- | --- | --- | --- | --- |
| Identifier (name, SKU, ID) | left | `tabular-nums` if alphanumeric ID | often default sort | Anchor link; the row's `rowheader` |
| Status / enum | left, with chip | — | sort by enum's declared order | Enum order is author-controlled, not alphabetical |
| Quantity, count | right | `tabular-nums` | numeric, desc default | Right-align is what makes the digits compare |
| Money | right | `tabular-nums` | numeric, desc default | Format in app code, not in the grid |
| Date / timestamp | left or right, consistently | — | newest first default | Fix the format and timezone per view |
| Prose / description | left, truncated | — | rarely sortable | Candidate for hidden-by-default |

Shopify is explicit that formatting belongs outside the grid: "Format money with the merchant's locale and currency before rendering it. Keep numeric values as numbers in your data model so sorting and totals don't operate on formatted strings" (Shopify, Migrate DataTable).

## Anatomy

```
[ toolbar: search | filters | sort | column chooser | density ]
[ select-all ☐ ][ col headers …………………… ][ pinned last col ]
[ ☐ ][ row 1 cells, cell 1 is the rowheader / link ][ ⋯ ]
[ ☐ ][ row 2 ………………………………………… ][ ⋯ ]
[ rowSummary: 1–50 of 1,204   ‹ prev  next ›  page size ]
```

Row count and column count must be announced correctly when the DOM holds fewer than the whole set: set `aria-rowcount` / `aria-colcount` to the totals (or `-1` if unknown) on the element with role `table`/`grid`, and `aria-rowindex` / `aria-colindex` on each rendered row or cell. Indices "Number[] starts with 1, not 0" (APG Grid and Table Properties). APG warns: "Missing or inconsistent values of `aria-rowindex` could have devastating effects on assistive technology behavior… could cause screen reader table reading functions to skip rows or simply stop functioning."

The first column is the row's identity, so mark it `rowheader` — that is what lets a screen reader announce "Mountain View, row 12" as the user arrows across cells (APG: `rowheader` "if the cell contains title or header information for the row"). Shopify keeps the same discipline in the dense case: the primary cell carries the thumbnail and the real link, and the pattern is to "reveal row actions on hover" while keeping the actions keyboard-reachable.

Row interaction must not be hover-only or click-only. Shopify's `clickDelegate` on a row is honest about its limits: "This is a click-only affordance, and does not introduce any keyboard or screen reader affordances. Which is why the target element must be in the table; so that keyboard and screen reader users can interact with it normally." Put the real control in the primary cell and let the row click delegate to it.

## Sources

- W3C ARIA Authoring Practices, "Grid (Interactive Tabular Data and Layout Containers) Pattern" — https://www.w3.org/WAI/ARIA/apg/patterns/grid/ — W3C — accessed 2026-10-05
- W3C ARIA Authoring Practices, "Table Pattern" — https://www.w3.org/WAI/ARIA/apg/patterns/table/ — W3C — accessed 2026-10-05
- W3C ARIA Authoring Practices, "Grid and Table Properties" — https://www.w3.org/WAI/ARIA/apg/practices/grid-and-table-properties/ — W3C — accessed 2026-10-05
- W3C WCAG 2.2, "Understanding SC 2.5.8 Target Size (Minimum)" — https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — W3C — accessed 2026-10-05
- Shopify, "Table" (`s-table`) — https://shopify.dev/docs/api/app-home/web-components/layout-and-structure/table — Shopify — accessed 2026-10-05
- Shopify, "Migrate DataTable from Polaris React" — https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/data-table — Shopify — accessed 2026-10-05
- Shopify, "Migrate IndexTable from Polaris React" — https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/index-table — Shopify — accessed 2026-10-05
- Shopify, "Index table" pattern — https://shopify.dev/docs/api/app-home/patterns/compositions/index-table — Shopify — accessed 2026-10-05
- AG Grid, "Row Height" — https://www.ag-grid.com/javascript-data-grid/row-height/ — AG Grid — accessed 2026-10-05
- Airtable, "Getting started with Airtable views" — https://support.airtable.com/docs/getting-started-with-airtable-views — Airtable — accessed 2026-10-05
- MDN, "font-variant-numeric" — https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric — Mozilla — accessed 2026-10-05
- MDN, "position" — https://developer.mozilla.org/en-US/docs/Web/CSS/position — Mozilla — accessed 2026-10-05