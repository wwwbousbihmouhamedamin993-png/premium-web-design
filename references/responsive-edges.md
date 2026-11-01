# Responsive edges

Applies to: a data-heavy authenticated app whose hardest problem is not "does it look good at
375px" but "does the 24-column table stay legible between a split-pane and a 3440px display."

## The floor and the ceiling are conformance, not taste

The narrow end has a hard number. SC **1.4.10 Reflow** (Level **AA**) requires content to be
presented "without loss of information or functionality, and without requiring scrolling in two
dimensions" at **320 CSS pixels** width for vertical content, or **256 CSS pixels** height for
horizontal content [S1]. 320 CSS px "is equivalent to a starting viewport width of 1280 CSS pixels
wide at **400% zoom**" [S1].

The data-table carve-out is explicit and narrow. Two-dimensional layout is acceptable for "images
required for understanding (such as maps and diagrams), video, games, presentations, **data tables
(not individual cells)**, and interfaces where it is necessary to keep toolbars in view while
manipulating content" [S1]. But: "sections of content within the two-dimensional layout, such as
**each cell within a table**, would still need to meet this success criterion" [S1].

So the honest statement of the floor: **at 320px the page must not require two-dimensional
scrolling; the table body may scroll horizontally; individual cells may not.** A cell that can only
be read by scrolling sideways inside the cell fails 1.4.10.

At the top end there is no WCAG number. **Not found:** any sourced maximum content width, maximum
column count, or guidance on very wide viewports in WCAG 2.2 or web.dev. A ceiling is a house
decision and should be recorded as one.

## Viewport units: the short-viewport case

A logged-in console is a three-region layout with independently scrolling panes, so `vh` is
usually the wrong unit — it is the viewport, not the pane.

MDN's `length` reference defines the family: `vh` "represents a percentage of the height of the
viewport's initial containing block", `vh` **is equivalent to `lvh`** (the large viewport size),
and `svh`, `lvh`, `dvh` cover the small, large and dynamic viewport sizes [S2]. Same pattern for
`vw`/`svw`/`lvw`/`dvw` and `vmin`/`vmax` [S2].

The distinction that matters for a console:

- **`dvh`** tracks the viewport as it actually is, including collapsing browser chrome on mobile.
- **`svh`** is the smallest the viewport gets — stable, no jump when chrome hides. Use it for
  anything that must not resize: a dialog body height, a fixed-height toolbar, a virtualised list's
  height.
- **`vh` == `lvh`** [S2], so legacy `100vh` layouts in an app shell jump when mobile chrome
  collapses.

**House rule (judgement, not sourced):** inside a scrollable pane use the pane's own measured
height (or `100%` of a sized container), never `vh`. Reserve `dvh`/`svh` for full-screen surfaces
only, and use `svh` for a full-screen surface that must not reflow.

## Landscape and short viewports

SC **1.3.4 Orientation** (Level **AA**): "Content does not restrict its view and operation to a
single display orientation, such as portrait or landscape, unless a specific display orientation is
essential" [S3]. W3C's rationale is a mechanical one — "Some users may have their devices mounted
in a fixed orientation (e.g. on the arm of a power wheelchair)" [S3].

Landscape phone ≈ 844×390 CSS px on a current handset. **That is under the 400px-tall threshold at
which a three-region console stops working**, and it is the hardest real case, because it is
narrow *and* short. At 390px of height: a 56px header, a 40px filter bar, a 48px column-header
row, and a 56px bulk-action bar leaves roughly 190px of table body — four or five rows.

Requirements that follow:

- **The app shell's scroll container must not be the document.** If the page scrolls as a whole,
  a short viewport means the table header scrolls away and focus goes under the sticky bar —
  failing **SC 2.4.11 Focus Not Obscured (Minimum)** (Level **AA**) [S4]. W3C names "sticky
  footers, sticky headers, and non-modal dialogs" as the obscuring content and prescribes "scroll
  padding" [S4].
- **Every height that must survive the fold is `block-size`-declared, not derived.** The bulk
  action bar is the usual culprit: it appears on selection and pushes the table down.
- **Do not gate on `(orientation: portrait)`** to decide whether a feature exists. Gate on available
  space; orientation is a hint, and the AA criterion is about *restricting* view and operation.

## Container queries vs media queries

The rule, in two rows (see `references/responsive-container-queries.md` for the full mechanism):

| Question | Use |
|---|---|
| Does the **component** have room to reflow? | `@container` |
| Does the **page** need different regions (sidebar collapses, nav moves)? | `@media` |

MDN: container queries "enable you to apply styles to an element based on certain attributes of its
container" and "are an alternative to media queries, which apply styles to elements based on
viewport size" [S5].

For a console this is not optional. The same table header sits beside a 256px sidebar in a split
view and beside nothing in a full-width view, **at identical viewport widths**. A media query
cannot distinguish them. Declare `container-type: inline-size` on each pane and let the header, the
row template, and the detail field grid respond to their own box.

Two failure modes to design around:

- `container-type: size` means the container's block size no longer depends on its content — which
  breaks intrinsic sizing of the panes a console is made of. Prefer `inline-size`.
- MDN: "**If no eligible container is available for the query, the container query length unit
  defaults to the small viewport unit for that axis (`sv*`).**" [S5] So `cq*` units outside any
  query container silently become viewport-relative, and a `@container` rule whose condition cannot
  be evaluated simply does not apply. Always author the default declaration first.

Range syntax is available for media queries and interchangeable with `min-`/`max-` prefixes:
`@media (30em <= width <= 50em)` [S6].

## Dropping columns, not shrinking type

The failure mode this section exists to prevent: at narrow widths the designer reduces the table's
font-size to fit. That trades a text-legibility problem and a **SC 1.4.4 Resize Text** (Level **AA**)
risk — text must be resizable "up to 200 percent without loss of content or functionality" [S7] —
for a layout "win". Do not.

**The precedence order when space is short (house judgement, not sourced):**

1. **Drop the lowest-value columns first**, by user frequency, not by position. Right-most columns
   are conventionally lowest-frequency and are the first to go — but that must be confirmed against
   actual usage, not assumed.
2. **Then collapse multi-column groups into one cell** (e.g. `name@company.com` in one cell, not
   two), using the isolation technique in `i18n-rtl.md` for mixed-direction values.
3. **Then move secondary fields into a row detail pane** on selection.
4. **Then allow horizontal scroll of the table as a whole** — permitted at 320px by the 1.4.10
   exception [S1] — with the table itself scrollable and each cell still readable without
   two-dimensional scrolling.
5. **Never reduce type size** as a layout mechanism. If the design system has a dense density
   class, that is the sanctioned lever, and it is a token change, not a per-table override.

Whatever you drop, the values must remain reachable — 1.4.10's per-cell rule [S1] and 1.4.4's
no-loss-of-functionality rule [S7] both require that a dropped column's data is available
somewhere.

## Touch vs pointer

Two media features decide this, and both are Baseline widely available since December 2018 [S8]
[S9]:

- **`pointer`** — whether the user has a pointing device and how accurate it is: `none`,
  **`coarse`** (a finger on a touchscreen), `fine` (a mouse) [S8].
- **`hover`** — whether the primary input can hover: `none`, `hover` [S9]. MDN notes `hover: none`
  covers "many mobile devices [that] emulate hovering when the user performs an inconvenient long
  tap" [S9].

Consequences:

- **Do not gate functionality on `hover`.** Hover-revealed row actions, hover tooltips, and
  hover-only column resize handles must have a coarse-pointer equivalent. `@media (hover: hover)`
  to *add* hover affordance [S9]; never `@media (hover: none)` to *remove* the only route to a
  value.
- **Target size.** The AA gate is **24×24 CSS px** (SC **2.5.8 Target Size (Minimum)**, Level
  **AA**), with the spacing-circle exception [S10]; 44×44 is **SC 2.5.5, Level AAA** [S11]. A row
  action menu at 16px with a 24px-diameter circle free around it passes 2.5.8 [S10]. But on a
  coarse pointer the honest target is 44 — see `accessibility-web.md`.
- **Use `@media (pointer: coarse)` for the hit area, not the visual size.** MDN's own example sizes
  a checkbox at 15×15px for `pointer: fine` and 30×30px with a 2px border for `pointer: coarse`
  [S8] — i.e. the visual affordance itself grows, not only a transparent padding layer.

## Very wide screens, and breakpoint discipline

**Content max-width (house judgement, not sourced).** A settings form or prose block stretched to
2560px is unreadable — the eye cannot find the start of the next line. Cap the *content* measure.
**Not found:** any primary source publishing a numeric content max-width for a B2B application shell.
It is a house number; record it in the layout tokens file.

**Tables should be full-bleed, not max-width.** A table is not prose; capping it at 1280px on a
3440px display wastes the display and forces horizontal scroll for no reason. Content column centred
and capped; tables and other data surfaces span the shell's content area edge to edge, with their own
background token so the cap reads as a shape. Extra width goes into **more or wider columns**,
never into tracking-out body text. At very wide widths, cap the column count and let the remainder
of the row breathe — do not add filler columns. **Not found:** a sourced maximum column count for a
data table. **House judgement:** if a table exceeds the shell's content area at a wide viewport, the
fix is to surface more columns — a console's density is information per pixel, and horizontal scroll
on a 3440px display is a design failure, not a density success.

**Breakpoint discipline (house judgement, not sourced).** Break on the layout's needs, not device
names — there is no sourced list of device widths worth citing, so derive breakpoints from the
container measurements at which the layout actually breaks. Prefer fluid `clamp()`/`min()`/`max()`
and `fr`-based tracks so the layout interpolates between breakpoints; reserve discrete
`@container`/`@media` steps for structural change (one column → two, sidebar collapses). Test at the
four widths that break things: **320** (the AA floor [S1]), **256px height** (the landscape-phone case
[S1]), the narrowest realistic pane, and the widest supported display. Declare
`<meta name="viewport">` with `width=device-width` — MDN documents `width` as "the (minimum) pixel
width of the viewport", settable to a whole number from 1 to 10000 or to `device-width` [S12].

## Checklist

- [ ] Verified at 320px wide with no two-dimensional page scrolling; any horizontal scroll is inside a table or map, and each cell still reads without sideways scrolling.
- [ ] Verified at 256px viewport height — no landscape-only orientation lock, nothing requires portrait.
- [ ] Each pane is a `container-type: inline-size` context; components respond to `@container`, not `@media`.
- [ ] Default declaration authored before every `@container` block; `cq*` units only inside a declared container.
- [ ] Narrow widths drop columns; no type-size reduction used as a layout lever.
- [ ] Dropped columns' values reachable elsewhere; density changes go through a token, not a local override.
- [ ] Every height that must survive a short viewport is declared; no `100vh` inside a scrollable pane.
- [ ] No functionality gated on `hover`; row actions have a coarse-pointer route.
- [ ] Hit areas ≥24×24 at fine pointers, ≥44×44 for primary touch actions.
- [ ] Content measure capped; tables and other data surfaces allowed full width within the shell.
- [ ] `scroll-padding-block-start` set on every scrollable region so sticky headers never obscure focus.

## Sources

All pages **accessed 2026-10-05**. Brackets give the claim each supports.

- **[S1]** https://www.w3.org/WAI/WCAG22/Understanding/reflow.html — W3C WAI, *SC 1.4.10 Reflow, Level AA*. [320/256 CSS px; 1280px-at-400%-zoom equivalence; "data tables (not individual cells)" exception and the per-cell carve-back]
- **[S2]** https://developer.mozilla.org/en-US/docs/Web/CSS/length — MDN, *length*. [`vh`/`vw`/`vmin`/`vmax`; `vh` == `lvh`; the `sv`/`l`/`d` families]
- **[S3]** https://www.w3.org/WAI/WCAG22/Understanding/orientation.html — W3C WAI, *SC 1.3.4 Orientation, Level AA*. [no orientation lock unless essential; fixed-orientation mounting]
- **[S4]** https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html — W3C WAI, *SC 2.4.11 Focus Not Obscured (Minimum), Level AA*. [sticky headers/footers, non-modal dialogs, cookie banners; scroll padding]
- **[S5]** https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries — MDN, *Container queries*. [what a container query targets; alternative to viewport media queries; `container-type`; `cq*` defaulting to `sv*`]
- **[S6]** https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries — MDN, *Using media queries*. [range syntax; equivalence to `min-`/`max-`; inclusive vs strict]
- **[S7]** https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html — W3C WAI, *SC 1.4.4 Resize Text, Level AA*. [200% without loss; author must not obstruct UA scaling]
- **[S8]** https://developer.mozilla.org/en-US/docs/Web/CSS/@media/pointer — MDN, *pointer*, Baseline since Dec 2018. [`none`/`coarse`/`fine`; fine-vs-coarse checkbox sizing example]
- **[S9]** https://developer.mozilla.org/en-US/docs/Web/CSS/@media/hover — MDN, *hover*, Baseline since Dec 2018. [`hover: none` covers long-tap emulation; gate added affordances with `hover: hover`]
- **[S10]** https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — W3C WAI, *SC 2.5.8 Target Size (Minimum), Level AA*. [24×24 CSS px with the spacing-circle exception]
- **[S11]** https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html — W3C WAI, *SC 2.5.5 Target Size (Enhanced), Level AAA*. [44×44 CSS px and its four exceptions]
- **[S12]** https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/viewport — MDN, *meta name="viewport"*. [`width` as "(minimum) pixel width of the viewport", 1–10000, `device-width`; establishes `vw`]