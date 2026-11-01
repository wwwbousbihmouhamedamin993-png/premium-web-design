# Dashboard composition

For logged-in B2B SaaS product surfaces (analytics, admin, operations). Not marketing pages.
As-of: 2026-10-05.

## Framing: decide which kind of dashboard you are building first

IBM Carbon splits dashboards into exactly two kinds, and the kind determines every layout decision
downstream. Carbon's own framing: presentation dashboards "show viewers the current status of key
performance indicators (KPIs) relevant to the business problem"; exploration dashboards "allow users
to interact with the data to discover insights and identify patterns," with actions including
"search, sort and filter data, roll up, and drill down" ([Carbon, Dashboards]).

Nielsen Norman Group draws a parallel line: dashboards exist in **operational** form (critical info
quickly, while the user is in a time-sensitive task) and **analytical** form (at-a-glance info that
supports decisions but has no time sensitivity). NN/g defines a dashboard as "collections of data
visualizations, presented in a single-page view that imparts at-a-glance information on which users
can act quickly," and stresses that dashboards "are focused on a single task: communicating critical
information" ([NN/g, Dashboards]).

Checkable rule: a logged-in B2B dashboard is one of Presentation (status) or Exploration
(search/sort/filter/roll up/drill down). If the surface has no filters, no drill-down, and no linked
charts, it is Presentation — and it must be readable without interaction. Do not add interaction
affordances (date pickers, filter chips, zoom) to a Presentation dashboard just because the data is
available; that converts it into a worse Exploration dashboard.

## Presentation dashboards

### One metric dominates per view

Carbon's hierarchy rule: "Prioritize data by importance, then create a clear visual hierarchy. The
most important data should have the highest contrast and occupy the largest area"
([Carbon, Dashboards]).

Derived rule for B2B product surfaces: **exactly one metric owns the top of the view.** It gets the
largest type, the strongest contrast, and the most space. Supporting metrics are subordinate. A
leading KPI row of four identical tiles satisfies no one's decision need — it is a metrics list, not
a dashboard, and it tells the reader which of the four to look at only if they already knew.

Supporting reasoning from primary sources:

- NN/g: dashboards are "focused on a single task: communicating critical information"
  ([NN/g, Dashboards]). Four equal tiles delegate that task back to the reader.
- Carbon: "Limit the number of metrics. Non-essential information should be provided as needed.
  Design a dashboard to reduce a page's complexity by stripping away anything that could distract a
  user from interpreting the information" ([Carbon, Dashboards]).
- Stephen Few, on working memory: "short-term memory is where the real work of sense-making is
  done... this is a pretty hard constraint that only holds from three to seven chunks of data at a
  time." Few's operational rule: "If you want someone to make sense of the graph as a whole, then
  you must limit the number of data components that encode distinct meanings to seven at most — and
  safer yet, to no more than five" ([Few, Tapping the Power of Visual Perception]).

**Not found:** a researched threshold on how many tiles a dashboard row may contain, and a study
directly testing "four identical KPI tiles communicate nothing." What would settle it: a usability
study varying tile count and tile-size congruence and measuring time-to-first-correct-decision. Until
then, use the Few 5-to-7 chunk ceiling as the outer bound and treat the one-dominant-metric rule as a
composition requirement from Carbon's hierarchy clause, not a measured effect.

### Reading order: the F-pattern

Carbon: "Most people in the west read left to right, then top to bottom. This is known as the
F-shaped pattern. Place the most important at the top of the page and follow the F-pattern for the
remaining elements, finishing with the least important information" ([Carbon, Dashboards]).

NN/g's 2017 revisit of the F-pattern adds the caveat Carbon does not carry: the pattern applies to
the *content area* of a page, and it is "the default pattern when there are no strong cues to attract
the eyes towards meaningful information." First lines and first few words receive more fixations than
subsequent ones ([NN/g, F-Shaped Pattern]).

Checkable rule: order the dashboard by importance top-to-bottom, left-to-right. Do not put a
secondary metric above the dominant one because it happens to be easier to compute. In a left-rail
layout, the F-pattern applies within the content column, not to the rail.

### Whitespace is comprehension, not decoration

Carbon: white space "either sets elements apart or brings them together to distinguish a point's
priority... it provides relief and breathing room," citing Human Factors International research that
"white space increases comprehension by almost 20 percent" ([Carbon, Dashboards]).

Important provenance note: the underlying HFI newsletter cites Lin (2004), "Evaluating older adults'
retention in hypertext perusal," and states that "Use of whitespace between paragraphs and in the
left and right margins increased comprehension by almost 20%" ([HFI, Yeah, but can you give me a
reference?]). That is a text-reading study, not a dashboard study. Use it as directional support for
generous whitespace, not as a dashboard effect size.

### Consistent colour assignment

Carbon: "Always use consistent colors for each data set within a dashboard" ([Carbon, Dashboards]).
Reinforced by NN/g's dashboards article: because people do not perceive colors as being in a
particular order, "color should not be used to communicate information about quantitative values or
magnitude" ([NN/g, Dashboards]).

## Exploration dashboards

Carbon's three rules ([Carbon, Dashboards]):

1. **Consistency is key** — all charts use the same layout and spacing, legends in the same position
   relative to the charting area, and one measurement system throughout (do not switch imperial to
   metric).
2. **Linked charts** — mirror filter and zoom actions; when a user manipulates one chart, charts
   showing related data sets update automatically.
3. **Annotation** — use annotations to highlight trends, averages, peaks and valleys; annotations
   should help users interpret fluctuations and must not obstruct the data.

## Layout patterns

| Decision | Presentation | Exploration |
| --- | --- | --- |
| Dominant element | One oversized KPI, largest type, highest contrast | A trend chart that establishes shape before any interaction |
| Secondary row | 3–5 subordinate metrics, deltas + timestamps | Filter/sort controls above the chart area |
| Interaction | None required; readable on first paint | Search, sort, filter, roll up, drill down |
| Charts | One or two; single-series | Multiple, linked, cross-filtering |
| Legends | Prefer direct labels; drop if only one series | Same position in every chart |
| Gridlines/axes | Muted or removed if data labels carry values ([Few via NN/g]) | Kept when scale itself is the message |
| Empty/stale state | Say what is missing and when | Keep the control chrome visible so the view is operable |

Tufte on gridlines, from the book text: "One of the more sedate graphical elements, the grid should
usually be muted or completely suppressed so that its presence is only implicit — lest it compete
with the data," and "Dark gridlines are chartjunk. They carry no information, clutter up the
graphic, and generate graphic activity unrelated to data information." Tufte quantifies the cost on
one multi-window plot: "The space occupied by the doubled grid lines consumes 18 per cent of the area
of this otherwise most ingenious design" ([Tufte, VDQI 2nd ed., ch. 2–3]).

## Sources

- Carbon Design System, "Dashboards," data visualization. https://carbondesignsystem.com/building-blocks/data-visualization/dashboards/ — IBM. Accessed 2026-10-05.
- Carbon Design System, "Chart anatomy," data visualization. https://carbondesignsystem.com/building-blocks/data-visualization/chart-anatomy/ — IBM. Accessed 2026-10-05.
- Nielsen Norman Group, "Dashboards: Making Charts and Graphs Easier to Understand" (Page Laubheimer, June 18, 2017). https://www.nngroup.com/articles/dashboards-preattentive/ — Nielsen Norman Group. Accessed 2026-10-05.
- Nielsen Norman Group, "F-Shaped Pattern of Reading on the Web: Misunderstood, But Still Relevant" (Kara Pernice, Nov 12, 2017; reviewed Aug 19, 2026). https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/ — Nielsen Norman Group. Accessed 2026-10-05.
- Stephen Few, "Tapping the Power of Visual Perception," Perceptual Edge, Sept 4, 2004. https://www.perceptualedge.com/articles/ie/visual_perception.pdf — Perceptual Edge. Accessed 2026-10-05.
- Human Factors International, "Yeah, but can you give me a reference? 2.0," Kath Straub, Dec 2005. http://www.humanfactors.com/newsletters/yeah_but_can_you_give_me_a_reference.asp — Human Factors International. Accessed 2026-10-05.
- Edward R. Tufte, *The Visual Display of Quantitative Information*, 2nd ed., Graphics Press, 2001, chs. 2–3 excerpt (course-uploaded copy of printed pages 50–77 and 107–121). https://lmscontent.embanet.com/USC/CMGT587/Tufte%20Ch2%20and%205.pdf — Graphics Press. Accessed 2026-10-05.