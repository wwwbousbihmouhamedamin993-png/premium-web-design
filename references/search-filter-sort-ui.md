# Search, filter & sort UI

Applies to: in-app search, admin record lists, log and event search, settings search, any "list + narrow"
surface.

## Search-as-you-type vs explicit search

Two different products. Pick by result-set size and interaction cost.

**Search-as-you-type (instant results)** suits large, homogeneous collections where the user knows roughly
what exists: colleagues, invoices, log lines, records. It makes the search box a *navigation* surface, not a
query form. NN/g's recommendation for exactly this case — an intranet people-finder — is a single search
field with "no scoping options before or after it", suggestions appearing as the user types, and: "**Speedy
response time, preferably on the order of 0.1 seconds**, is imperative."
(https://www.nngroup.com/articles/suggested-employee-search/)

**Explicit search (submit)** suits narrow scopes, costly queries, or when results need to be faceted — i.e.
anything where a keystroke must not trigger a round trip.

NN/g on when instant is wrong: "In many cases, both advanced and scoped searches have been replaced by
faceted search. The key difference is that faceted search allows users to narrow their options **after**
they submit their query, rather than before" (https://www.nngroup.com/articles/state-ecommerce-search/).

Three as-you-type techniques, distinct — do not conflate them
(https://uxmag.com/articles/designing-search-as-you-type-suggestions):

| Technique | What appears | Best for |
|---|---|---|
| **Auto-complete** | inline completion string in the field | known-item search |
| **Auto-suggest** | dropdown of reformulated queries | exploratory search |
| **Instant results** | the results themselves, bypassing the results page | promoting specific items |

UX Magazine: "Auto-complete is better suited for known-item search and simple information retrieval tasks.
Auto-suggest works well for exploratory search and complex information seeking tasks. And instant results
provide a direct channel from queries to answers."

**Not found:** a single numeric debounce threshold in any primary source. UX Magazine notes Google's
observed typing rhythm — people "type slowly, but read quickly, typically taking 300 milliseconds between
keystrokes, but only 30 milliseconds … to glance at another part of the page"
(https://web.archive.org/web/20120812045644/http://www.google.com/insidesearch/features/instant/about.html)
— implying a debounce at or above the read time. Choose your own and record it.

Search input mechanics are in `text-inputs.md`: `type="search"`, persistent label (not placeholder),
`inputmode="numeric"` where the query may be numeric.

## Filter chips, facets, and the active-filter summary

### Filter vs facet

NN/g distinguishes these, and the difference is a budget decision, not a synonym
(https://www.nngroup.com/articles/filters-vs-facets/): a **filter** "means anything that analyzes a set of
content and excludes some items"; **faceted navigation** "is composed of multiple filters that
comprehensively describe a set of content."

Faceted navigation "is thus more flexible and more useful than systems which provide only one or two
different types of filters, especially for extremely large content sets" — but: "this type of structure is
significantly more expensive to create and maintain … and both existing and future content must have
metadata applied for each facet." Its interaction cost is higher too: "A simple filter can often be easier
to understand and faster to use."

So: ship a handful of filters first. Do not build facets because the data model makes it easy.

### Naming and ordering filters

NN/g (https://www.nngroup.com/articles/filter-categories-values/):

- A truly usable faceted search provides filter categories and values that are "**appropriate,
predictable, free of jargon, and prioritized**."
- "Avoid filter categories with vague labels like Item Type. Words like Category, Format, Content
Type, or Genre are better, because they feel a bit more specific and tailored to the current item."
- Order categories by importance: "consider placing the most general, high-level filter categories at
the top of the list, and the more specific ones towards the bottom." Relevance to users is the ultimate
criterion.
- Within a category: numeric values "from lowest to highest (for price ranges) or vice versa (for
average customer ratings)"; word values "alphabetically if users are likely to know the names".
- Concrete beats abstract: a participant "seemed to better describe what she was looking for, so the
participant paid more attention to it" — specificity raises attention.

GOV.UK adds an accessibility corollary: "Users should be able to roughly predict what filter values they'll
find within each filter category … particularly important on mobile, where many designs use collapsed
accordions to contain their filter values."

### Facets need counts, and the count must be honest

NN/g: facets "often also show the number of elements available under each filter, and thus help users avoid
zero-search results" (https://www.nngroup.com/articles/applying-filters/). The batch-filtering disadvantage
is that it "is a risk that users will select a combination of criteria that leads to zero results. Delaying
the presentation of results makes it difficult to give users continuous feedback about which filters are
available or disabled and how many results there are."

So a count per facet value is a correctness feature, not decoration. Zero-count values should be disabled or
removed rather than left clickable.

### Chips vs sidebar vs tray

| Surface | Placement | Sourced basis |
|---|---|---|
| Dense desktop list / data table | left sidebar, checkboxes | GOV.UK: small checkboxes "work well on information dense screens in services designed for repeat use, like caseworking systems"; standard checkboxes on "a page of search results" keep filters from distracting from results |
| Mobile | overlay "tray" over the results | NN/g: "facet controls appear in a vertical panel overlaid on top of the results screen. The results are always visible in the background" (https://www.nngroup.com/articles/mobile-faceted-search/) |
| Toolbar / chips | inline row of active filters | **Not found** — NN/g's course listing names "applied-filter chips" as a topic but the consulted text gives no layout rule. Settled by the course content at https://www.nngroup.com/contents/self-paced-courses/filters-and-sorting-the-complete-design-guide/ |

GOV.UK's mobile-relevant finding is not the tray itself but the simultaneous display: showing filters and
results "at the same time makes it easier for users to understand how the filter controls affect the results
set". A mobile filter screen with no results behind it forces the user to navigate back and forth to learn
whether a filter worked — "a tedious cycle of pogo-sticking between the results and the filters."

Also: **the total result count must stay visible** while filters are open. And use words, not icons: "the
labels commonly used for faceted navigation — narrow your results, refine, and filter — are far more
understandable than cryptic icons, and definitely worth the extra space."

### Active-filter summary

Persist query state where users can see and undo it. NN/g: "Maintain context by displaying the current query
(and allow it to be edited in place) … the state of any other navigational context such as current facet
selections, and the number of matching results"
(https://uxmag.com/articles/designing-search-results-pages/).

Concretely: show the query, every applied filter with its value, the match count, and a way to remove each
filter independently. A search box that clears the moment you apply a filter destroys that context.

## Filter update timing: batch vs interactive

This is the highest-impact decision on a filter surface, and it depends on **user intent and speed**, not
preference (https://www.nngroup.com/articles/applying-filters/).

| | Interactive (update on each selection) | Batch (Apply button) |
|---|---|---|
| User is | **exploratory** — learning the space | **decisive** — knows their criteria |
| Feeds on | facets changing as they select | fewer round trips |
| Risk | many queries, more waiting | zero-result dead end |
| Use when | results return in **under ~1 second** after each filter value | site is "likely to be slow at least occasionally" |

NN/g's threshold: "If you expect the queries to be instantaneous (and the new results to be shown less than
one second after each filter was specified) then interactive filtering will be less offensive even for users
in search mode. If however your site is likely to be slow at least occasionally, then batch filtering can
save the users some wait time." And: "This is the recommended approach on mobile devices, even with the new
tray design pattern" — but batch "implies that you're failing your exploratory users."

Two refinements NN/g gives for interactive filtering:

- **Dim-and-replace, don't flash.** "Many effective faceted navigation systems dim the results set and
show a progress indicator before displaying the new results. This way, the change that users detect is a
single dimmed area (instead of individual items seemingly flashing on and off the screen)."
- **Idle-then-update.** "If a user hasn't made another selection or moved the mouse after a certain
amount of time (**1–2 seconds**), then display the new results. The system should still give immediate
feedback (e.g. a progress indicator) to acknowledge that the first selection was received."

## Clearing filters

**Not found:** NN/g's filter articles give no explicit rule on a "clear all" control's placement,
label, or confirmation. What would settle it: a documented pattern in a design system with published testing.

Sourced adjacent guidance that does bear on it: results must never leave the user disoriented —
Houseoffraser.co.uk "disappoints, after the filters are applied: the page scrolls back to the top of the
results … users who are still looking at the filters … lose their place on the page"
(https://www.nngroup.com/articles/applying-filters/). So a "clear all" affordance should live in the filter
surface that stays on screen, not below the results it just replaced. And it must not break NN/g's own
scroll condition: "If users are still engaged with the filters area … it's a good sign that they're ready
for the results" — detected by mouse or keyboard movement, "with a time limit … as a fallback".

## Sort controls

**Not found:** NN/g's filter and search articles do not specify sort-control label conventions,
placement, or default-sort selection rules; sort appears only in the paid report's contents ("Sorting
products") and as a course topic. Settle with a design system that publishes sort conventions, or with your
own recorded decision.

What is sourced and applies: sort is navigation context that must survive filtering. Preserve it in the
active-filter summary above, and use `<select>` — GOV.UK's select guidance notes that "if you use the
component for settings, you can make an option pre-selected by default" (a sort control is a setting, so a
default sort is correct there, unlike a question).

## The zero-result state

Sourced, and the most commonly under-built state on a filter surface. NN/g found "in our first study, 27% of
task failures were a result of not being able to locate a suitable item on … site, even though all of our
tasks were designed so there was always at least one item available" — caused by "too many options, with no
way to narrow choices" (https://www.nngroup.com/articles/state-ecommerce-search/).

A zero-result state must therefore name the query and applied filters, state the match count (0), and offer
the narrowest possible next step — remove one filter, or clear all. Batch filtering makes this worse, not
better, because the user gets no signal until the end.

## Review checklist

- [ ] Instant vs explicit search chosen deliberately; instant implies sub-second response.
- [ ] Facets only where a filter would not suffice; metadata cost accepted.
- [ ] Filter categories concrete, ordered by relevance, values ordered (numeric ascending, words alphabetical).
- [ ] Every facet value carries an honest count; zero-count values not clickable.
- [ ] Filters and results simultaneously visible, including on mobile via a tray.
- [ ] Total result count visible while filters are open.
- [ ] Batch vs interactive matches measured result latency; Apply button where batch.
- [ ] Dim-and-replace on update, not per-item flashing.
- [ ] Active-filter summary shows query + filters + count, each removable.
- [ ] Zero-result state offers a concrete next step.
- [ ] Sorting preserved through filter changes.

## Sources

- Suggested-Employee Search—The Best Intranet Design — Nielsen Norman Group — https://www.nngroup.com/articles/suggested-employee-search/ — accessed 2026-10-05
- The State of Ecommerce Search — Nielsen Norman Group — https://www.nngroup.com/articles/state-ecommerce-search/ — accessed 2026-10-05
- Filters vs. Facets: Definitions — Nielsen Norman Group — https://www.nngroup.com/articles/filters-vs-facets/ — accessed 2026-10-05
- Defining Helpful Filter Categories and Values for Better UX — Nielsen Norman Group — https://www.nngroup.com/articles/filter-categories-values/ — accessed 2026-10-05
- User Intent Affects Filter Design — Nielsen Norman Group — https://www.nngroup.com/articles/applying-filters/ — accessed 2026-10-05
- Mobile Faceted Search with a Tray: New and Improved Usability — Nielsen Norman Group — https://www.nngroup.com/articles/mobile-faceted-search/ — accessed 2026-10-05
- Filters and Sorting: The Complete Design Guide — Nielsen Norman Group — https://www.nngroup.com/contents/self-paced-courses/filters-and-sorting-the-complete-design-guide/ — accessed 2026-10-05
- Designing Search: As-You-Type Suggestions — UX Magazine — https://uxmag.com/articles/designing-search-as-you-type-suggestions — accessed 2026-10-05
- Designing Search: Results Pages — UX Magazine — https://uxmag.com/articles/designing-search-results-pages — accessed 2026-10-05
- About Google Instant (archived) — Google — https://web.archive.org/web/20120812045644/http://www.google.com/insidesearch/features/instant/about.html — accessed 2026-10-05
- Checkboxes — GOV.UK Design System — https://design-system.service.gov.uk/components/checkboxes/ — accessed 2026-10-05
- Select — GOV.UK Design System — https://design-system.service.gov.uk/components/select/ — accessed 2026-10-05
