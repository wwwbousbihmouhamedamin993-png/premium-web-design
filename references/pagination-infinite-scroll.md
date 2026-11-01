# Pagination, Infinite Scroll, and End States

Framing: for logged-in B2B surfaces the question is not "infinite scroll vs pagination" as an aesthetic. It is **how does the user get back to the row they were looking at, and how do they know when there is nothing more**. Nielsen Norman Group's finding is that classic infinite scroll "results in a lack of landmarks to help users orient themselves" and is specifically not recommended when users will "find something specific," "compare items in a long list," or "inspect only a few items at the top of the list."

## Offset vs cursor pagination

| | Offset (`?offset=100&limit=50`) | Cursor (`?after=<opaque>`) |
| --- | --- | --- |
| Random access to page N | Yes, if total count known | No, walk forward/back |
| Consistency under writes | Duplicates and skips when rows are inserted/deleted between requests | Stable by construction |
| Needs total count | Yes, for page numbers | No — hasNext is enough |
| Cacheable | Keyed on offset; offset is a pure function of position | Keyed on opaque cursor; cursor validity is server-owned |

Shopify's `s-table` takes the cursor shape: `paginate`, `hasPreviousPage`, `hasNextPage`, `onPreviousPage`, `onNextPage`, plus a `paginationLabel` such as `` `Page ${currentPage} of ${totalPages}` ``. Their migration example puts `cursor` and `direction` in URL search params and clears them whenever sort or filters change.

**The rule that matters more than the mechanism:** reset the cursor whenever the query changes. Shopify: "Reset its cursor whenever sorting, filters, or search changes; a cursor from the old query doesn't identify a page in the new result set," and "The route uses that value for its backend query, removes cursors from the previous result order, and reloads the table."

TanStack's client-side equivalent is an auto-reset: "By default, `pageIndex` is reset to `0` when page-altering state changes occur, such as when the `data` is updated, filters change, grouping changes, etc. This behavior is automatically disabled when `manualPagination` is true" — so with server pagination you own the reset. AG Grid has the same failure mode: "The `endRow` requested by the grid may not actually exist in the data so the correct `lastRowIndex` should be supplied in the response to the grid."

## Infinite scroll and its accessibility problems

NN/g enumerates five, all of which apply verbatim to a table body:

1. **Difficulty refinding content** — "in an infinite list of items, it is hard to remember the location of any specific item and return to it," and when the site doesn't save the user's spot, "users will find themselves at the top of the list, having to scroll down through screenfuls and screenfuls of already seen content."
2. **Illusion of completeness** — "the user may assume that the end of the content stream has been reached as new content loads in the background, below the fold. Usually, this problem arises when there is no indication that additional content is loading." (NN/g's dedicated article defines the illusion as happening "when the visual design fails to guide users toward additional content that is present off-screen.")
3. **Inability to reach the footer** — in a table, the analogue is the pagination bar, the totals row, and any footer controls.
4. **Accessibility problems** — "For keyboard-only users, infinite scrolling complicates navigating the web… such users have to 'tab' through content link by link and therefore face a lengthy task if they want to navigate to the end of an infinite scroll. On the other hand, screen-reader users will only see the first 'chunk' of the list, without being able to trigger the loading of new content."
5. **Increased page load** — with scroll restoration, "there could be a ton of content to be loaded whenever the user returns to a list."

The `feed` role is the ARIA answer for scroll-loaded article streams, and it is **not** the answer for a data grid. APG's feed pattern is explicitly contrasted with the grid: the feed pattern's value "is that a feed is a **structure, not a widget**," so assistive tech defaults to reading mode; a grid is a widget that requires application mode. NN/g's article notes the same distinction. If you use `feed`, you owe it: `role="feed"` on the container, `role="article"` per item, `aria-labelledby` per article, `aria-posinset`, `aria-setsize` (`-1` if total unknown), and `aria-busy="true"` during DOM updates — "it is extremely important that `aria-busy` is set to `false` when the operation is complete."

## "Load more" — the compromise

NN/g's verdict: a Load More button "stops the constant flow of new content and thereby enables users to access the footer section," is "a clear indication that there is more content to discover, and that the user did not yet see all the content," and "offer a way to load less content upfront." The cost: "interaction cost increases — users have to click the Load More button to load more content. Even the small interruption of clicking Load More might make users consume less content and cause them to switch tasks."

Also worth knowing: NN/g describes a fourth variant, "infinite scrolling with **integrated pagination**" (page-number landmarks injected into a continuous scroll, as Google Shopping's mobile page did), which "has the potential to reduce some of the usability issues created by classic infinite scrolling" but "can't solve all of them," has no user-testing data behind it, and "could be that, at least for a while, it confuses more than helps users because of its low familiarity."

## A real end state

An end state is not optional in a data surface. It means all of:

- **A visible, static end marker.** "Showing 1–50 of 1,204" plus a disabled or absent next control. Airtable ships this exact string in its record preview: "You will see the total count of records as 'Showing the first 1,000 of XX,XXX records'" once a view exceeds the preview threshold.
- **An explicit total, when the backend can produce one.** AG Grid's `rowSummary` panel renders "the row range summary (e.g. `1 to 10 of 50`)"; `pageSummary` gives first/previous/next/last plus an editable page number, and `pageNumbers` renders "numbered page buttons for direct navigation, with ellipses for large page counts (e.g. `1 … 9 10 11 … 51`)" — opt-in via `PaginationPageNumbersModule`.
- **A last-page truth, not a guess.** AG Grid's server-side pagination example notes "the last page arrow is greyed out as the last row index is only supplied to the grid when the last row has been reached" — i.e. unknown-total mode disables "last" until proven.
- **A degraded state for when the total is unknown.** TanStack: "If you don't know the page count, you can just pass in `-1` for the `pageCount`, but the `getCanNextPage` and `getCanPreviousPage` row model functions will always return `true` in this case." Mirror that in the UI: say "more results" rather than a fake page number.
- **Skip affordance where volume warrants it.** Airtable: "Consider using the search bar to find a specific record or create a view that filters out more records to create a more narrow dataset."

## Preserving scroll and filter state

The rule from NN/g's failure case: **saving position is what separates acceptable infinite scroll from unacceptable infinite scroll.** Implement all five:

1. **Put view state in the URL.** Shopify's `updateView` writes `query`, `status`, `sort`, `cursor`, `direction` into URL search params so browser Back/Forward restores the exact result set. Shopify's test list includes "Reload and use browser navigation after sorting, and confirm that the selected order is restored from URL state."
2. **Restore scroll position on return.** NN/g's diagnosis of the broken case is that Back "took the user to the top of the page and gave them the cumbersome task of finding their old position."
3. **Treat the filter/sort control as the primary instrument, not pagination.** For goal-oriented B2B work, a saved view with a filter usually beats any scrolling strategy. NN/g is blunt that infinite scroll is "also not a good fit if you have a large user group from areas with low bandwidth or if your website is visited frequently by users with accessibility needs."
4. **Show what is loaded vs what exists.** Airtable's preview model is a usable pattern for very large views: any view with more than 5000 *visible* records "will initially load with a 1000-record preview," the count line tells the truth, and "Load all records" is an explicit user act. Note the cost: "Extensions cannot be run while a view is in preview," and "the view preview will reset if you refresh your browser."
5. **Don't scroll-jank on page change — but do move.** AG Grid defaults to scrolling to the top on a page change and offers `suppressScrollOnNewData=true` to stop it; and NN/g's pagination research is that pages should be stable landmarks. Pick one deliberately: for a table where rows are compared across pages, keep position; for a search results list, go to top.

## Decision table for logged-in B2B

| Situation | Choose |
| --- | --- |
| Under ~50 rows, no server paging needed | Render all, no pagination chrome |
| Bounded result set, users jump to a page | Numbered pagination with a known total |
| Large set, cursor-addressable, sequential review | Prev/next cursor + range summary + explicit end state |
| Live tail / activity log where recency is the point | Infinite scroll **with** an end marker and a "jump to latest" |
| Goal-oriented finding of a specific record | Filter/search first; paginate the narrowed set |
| Load more than a page is acceptable, load time is not | "Load more" button with running count |

## Sources

- Nielsen Norman Group, "Infinite Scrolling: When to Use It, When to Avoid It" (Tim Neusesser, 4 Sep 2022) — https://www.nngroup.com/articles/infinite-scrolling-tips/ — Nielsen Norman Group — accessed 2026-10-05
- Nielsen Norman Group, "The Illusion of Completeness: What It Is and How to Avoid It" (Kim Flaherty, 17 Jan 2016) — https://www.nngroup.com/articles/illusion-of-completeness/ — Nielsen Norman Group — accessed 2026-10-05
- W3C ARIA Authoring Practices, "Feed Pattern" — https://www.w3.org/WAI/ARIA/apg/patterns/feed/ — W3C — accessed 2026-10-05
- AG Grid, "Row Pagination" — https://www.ag-grid.com/javascript-data-grid/row-pagination/ — AG Grid — accessed 2026-10-05
- AG Grid, "SSRM Pagination" — https://www.ag-grid.com/javascript-data-grid/server-side-model-pagination/ — AG Grid — accessed 2026-10-05
- AG Grid, "Infinite Row Model" — https://www.ag-grid.com/javascript-data-grid/infinite-scrolling/ — AG Grid — accessed 2026-10-05
- TanStack Table v8, "Pagination Guide" — https://tanstack.com/table/v8/docs/guide/pagination — TanStack — accessed 2026-10-05
- Shopify, "Table" (`s-table`) — https://shopify.dev/docs/api/app-home/web-components/layout-and-structure/table — Shopify — accessed 2026-10-05
- Shopify, "Migrate DataTable from Polaris React" — https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/data-table — Shopify — accessed 2026-10-05
- Shopify, "Migrate IndexTable from Polaris React" — https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/index-table — Shopify — accessed 2026-10-05
- Airtable, "Getting started with Airtable views" — https://support.airtable.com/docs/getting-started-with-airtable-views — Airtable — accessed 2026-10-05