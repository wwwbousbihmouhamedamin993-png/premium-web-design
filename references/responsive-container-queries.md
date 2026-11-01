# Responsive: container queries

In an app shell, the viewport is the wrong unit of measurement. The same page header sits beside a
256px sidebar in a split view and beside nothing in a full-width view, at identical viewport
widths. Container queries let a component respond to the space it actually has.

## The mechanism

MDN, *Container queries* (accessed 2026-10-05): container queries "enable you to apply styles to
an element based on certain attributes of its container" — its name, its size, styles applied to
it, its scroll state, or its anchor fallback. They are "an alternative to media queries, which
apply styles to elements based on viewport size."

## Declaration

`container-type` takes three relevant values:

| Value | Queryable on | Containment applied (MDN) |
|---|---|---|
| `size` | inline **and** block dimensions | layout, style, and size |
| `inline-size` | inline dimensions | layout, style, and inline-size |
| `normal` (default) | not a size-query container; still usable for name-only and style queries | none |

Prefer `inline-size`. A block-size query (`container-type: size`) means the container's height no
longer depends on its content, which breaks intrinsic sizing of the very panes that make a console
work. MDN's fallback section recommends grid and flex "to create a similar effect" — i.e. the safe
path is a layout that already responds.

## Querying

```css
.detail { container-type: inline-size; container-name: detail; }

@container detail (inline-size > 40rem) {
  .detail { grid-template-columns: 1fr 2fr; }
}
```

- **Unnamed queries resolve against the nearest ancestor query container** with a matching
  `container-type` (MDN).
- **`@container` requires a `container-name`, a `<container-query>`, or both** (MDN, `@container`
  reference, accessed 2026-10-05).
- **Name-only queries** apply styles wherever an ancestor has that `container-name`, with no size
  condition (MDN).
- **Size queries always measure the content box** (MDN, `@container`).
- **Range syntax is supported:** `(15em <= block-size <= 30em)` (MDN, `@container`).
- **One query, one container.** MDN: "It's not possible to target multiple containers in a single
  container query. It is possible to nest container queries which has the same effect" —
  `@container summary (width > 400px) { @container (width > 800px) { … } }`.
- **Style queries read the container's computed custom properties** — `@container style(--density:
  dense) { … }` (MDN, `@container`). This is the cleanest hook for a density class that must
  cascade into grandchildren.

## Container query units

Available only inside a container whose `container-type` is `size` or `inline-size` (MDN):

| Unit | Meaning |
|---|---|
| `cqw` | 1% of the query container's width |
| `cqh` | 1% of the query container's height |
| `cqi` | 1% of the query container's inline size |
| `cqb` | 1% of the query container's block size |
| `cqmin` | smaller of `cqi` or `cqb` |
| `cqmax` | larger of `cqi` or `cqb` |

- **Type scales nicely with these.** MDN's example sets a card title to
  `font-size: max(1.5em, 1.23em + 2cqi)` inside `@container (width > 700px)`.
- **Fluid, not snapping.** Prefer `cqi`-based `clamp()`/`max()` for type and gutters so a pane
  interpolates continuously; use discrete `@container` breakpoints only when the layout itself must
  change (one column → two).

## The fallback when no eligible container exists

This is the part that bites. MDN, *Container queries*: **"If no eligible container is available for
the query, the container query length unit defaults to the small viewport unit for that axis
(`sv*`)."**

- **`cq*` units degrade to `sv*` viewport units**, not to zero, not to nothing. A `cqi`-based
  gutter set outside any query container becomes viewport-relative — usually fine, occasionally
  surprising.
- **A `@container` rule whose condition cannot be evaluated does not apply.** Treat the
  unsupposed case as "no rule wins," so always author a sensible default declaration before the
  query.
- **Ship a mobile-first fallback if you must support pre-`@container` browsers.** MDN's stated
  fallback is grid/flex plus a media query to collapse to one column. A modern vendor equivalent:
  Polaris's responsive-value syntax is explicitly ternary-shaped —
  `@container (inline-size > 500px) large-400, small` — and the docs state: "Use a mobile-first
  approach for browser compatibility. The fallback value (when the condition is `false`) should
  work at the smallest size" (shopify.dev, *Using web components*, accessed 2026-10-05). That
  syntax degrades to the fallback value in browsers without container-query support.

## Container query vs media query

| Question | Use |
|---|---|
| Does the **component** have room to reflow? | `@container` |
| Does the **page** need different regions (sidebar collapses, nav moves)? | `@media` |
| Does the shell region itself change width because of another region? | `@container` on that region |
| Print styles, orientation, `prefers-*`, forced colors | `@media` |

The first two rows are the whole rule. Media queries answer "how big is the window"; container
queries answer "how big is my box." A three-region console must use both: media queries to decide
the shell's arrangement, container queries so the page header, list rows, and detail fields inside
each region respond to their own pane.

## Also available: scroll-state queries

Because a console's panes scroll independently, scroll-state queries are worth knowing:
`scroll-state(scrollable: top)`, `(scrolled: block-end)`, `(snapped: both)`, and
`(stuck: inline-end)` (MDN, `@container`). A `stuck` query "must have `position: sticky` set on
it, and be inside a scroll container" to match a non-`none` value — this is how a table header row
changes treatment once it detaches. Caveat: a table header row that must be sticky across a wide
table also needs horizontal sticky on its cells.

## Sources

- CSS container queries (`container-type`, `container-name`, `@container`, `cq*` units, `sv*` fallback, grid/flex fallback) — MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries — accessed 2026-10-05
- `@container` (content-box measurement, range syntax, nested queries, style queries, scroll-state descriptors) — MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/CSS/@container — accessed 2026-10-05
- Using web components (responsive-value syntax `@container (condition) ifTrue, ifFalse`; mobile-first fallback requirement; `s-query-container`) — Shopify Polaris, shopify.dev. https://shopify.dev/docs/api/polaris/using-polaris-web-components — accessed 2026-10-05
- `position` (sticky inset requirement; scrolling ancestor) — MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/CSS/position — accessed 2026-10-05
