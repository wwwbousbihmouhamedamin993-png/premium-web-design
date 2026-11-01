# Charts and data visualization

Logged-in product surfaces: operational and analytical dashboards, detail panels, empty and
loading states. Not marketing infographics.
As-of: 2026-10-05.

## Pick the chart from the task, not from the shape of the data

NN/g's rule: before choosing a chart, answer one question — what is the goal, what point are you
making? "In the vast majority of cases, use bar charts, line charts, or scatterplots." Charts
requiring the reader to assess angle, area, or volume are the harder cases: pie, bubble, mosaic,
unit/waffle, Sankey, dendrograms, stacked area. "If your goal can be achieved with one of the basic
charts, opt for them" ([NN/g, Choosing Chart Types]).

The perceptual reason, from the research review: visual channels are ranked by the precision with
which a viewer can state the ratio between two depicted values, "more precise ways of communicating
numbers are at the top and less precise ways at the bottom. It should be clear from the figure that
the 1:7 ratio can be relatively precisely extracted for position, but that task is a bit tougher for
area, and far more difficult for intensity" ([Franconeri et al. 2021, Fig. 2]).

Cleveland & McGill's ordering, as reproduced in Munzner's UBC lecture notes: position along a common
scale; position along nonaligned scales; length, direction, angle; area; volume, curvature; shading
and colour saturation ([Munzner, Lecture 5: Perception]). NN/g states the operational consequence:
"people are quite adept at estimating how lengths compare, and we can also accurately estimate
position in a 2D space... these two preattentive attributes are ideal for quantitative
representation" ([NN/g, Dashboards]). Limit series count using Few's memory ceiling — "limit the
number of data components that encode distinct meanings to seven at most — and safer yet, to no more
than five" ([Few, Tapping the Power of Visual Perception]).

**Not found:** the numeric error magnitudes from Cleveland & McGill (1984), *JASA* 79(387):531–554.
The PDF copies available online are image-only scans with no text layer, and the journal page is
paywalled. What would settle it: the paper's Table 1, or the open-access replication in Heer &
Bostock (2010), *Crowdsourcing Graphical Perception*, CHI 2010. Ship the ordering, not the numbers,
until you have opened one of those.

Also **not found:** a measured threshold for how many series a chart may carry before accuracy
collapses. Friendly's lecture notes record the design of the Cleveland & McGill experiments — five
bar types (adjacent, separated, aligned stacked, unaligned stacked, divided), 50 graphs, accuracy as
log2(|judged % − true %| + 1/8) — and report that the Heer & Bostock crowdsourced replication
"largely confirmed Cleveland & McGill with respect to relative order," with the added area-judgment
tasks "shown to give even larger errors" ([Friendly, Human Factors 2x2]). That is a ranking result,
not a series-count limit.

## Colour encoding

Use colour for categories, never for magnitude. NN/g: "people do not perceive different colors as
being in a particular order, so color should not be used to communicate information about
quantitative values or magnitude" ([NN/g, Dashboards]).

- **Categorical** (no inherent order) — Carbon's sequence of 14 categorical steps, "curated to
  maximize contrast between neighboring colors to help with visual differentiation." Carbon
  provides 1-colour-group overrides (Purple 70, Blue 80, Cyan 50, Teal 70) "if the exact number of
  data categories is predictable" ([Carbon, Color palettes]).
- **Sequential** (ordered magnitude) — Carbon monochromatic ramps, 10 steps. "In light themes, the
  darkest color denotes the largest values. In dark themes, the lightest color denotes the largest
  values" ([Carbon, Color palettes]).
- **Diverging** (signed distance from a midpoint) — Carbon offers red–cyan ("natural association with
  temperature... use for data representing hot-vs-cold") and purple–teal ("good for data with no
  temperature associations, such as performance, sales, and rates of change"). Note: diverging
  palettes "do not differentiate between light and dark themes" ([Carbon, Color palettes]).
- **Status** — separate alert palette: red = danger or error, orange = serious warning, yellow =
  regular warning, green = normal or success ([Carbon, Color palettes]).
- Gradients are discouraged: "Multiple gradients are often inaccessible and are discouraged in our
  system. Gradients should not be used to represent any meaningful progression or divergence. Never
  use a gradient in place of a sequential palette" ([Carbon, Color palettes]).

Colour vs shape when both axes are taken: "Plotting the groups as categorically different colors is
often the first choice because the visual system processes color differences more efficiently than
shape differences across the two-dimensional visual plane." Colour coding produced far better
performance than shape coding when viewers compared average heights of multiple coded point clouds in
a scatterplot ([Franconeri et al. 2021, citing Correll et al. 2012]). But redundant encoding is not
free insurance: because colour is already dominant, "redundant encoding does not substantially
improve visual processing efficiency... unless the viewer has color-vision impairment"
([Franconeri et al. 2021, citing Gleicher et al. 2013]).

## Axes, gridlines, and the truncated axis

Carbon's position, which is the one to adopt: "Always start numerical axes at zero for part-to-whole
and comparisons charts, such as bar and area chart. Truncating the Y axis can distort the
perception, making a small difference look big and significant... When an axis starts at non-zero,
percentage differences between bars are exaggerated." For line charts and scatter plots "cropping the
Y axis helps users more easily identify the direction of change," because they communicate trends
rather than relative size ([Carbon, Axes and labels]).

Carbon's other axis rules, all checkable: never interpolate across unavailable periods and label both
endpoints of the gap; never change tick increments to fit data availability (use an axis break, drawn
as a sinusoid, minimum 16px on X and a fixed 16px on Y); semibold the label whenever data crosses
into a new time cycle so it becomes a landmark label ([Carbon, Axes and labels]).

Truncation is not a preference, it is a measured failure. Across five studies, y-axis truncation led
viewers to perceive illustrated differences as larger; "83.5% of participants across these 5 studies
showed a truncation effect." The effect persisted after viewers were taught about truncation, and
graph literacy did not predict it — "PhD students in both quantitative fields and the humanities
were susceptible to the truncation effect" ([Yang et al. 2021]).

Stacked bars are the other trap: only the baseline segments are position-coded and therefore
precise; "The black & dark gray bars have the same value differences among them, but the differences
are only visible across the black bars" ([Franconeri et al. 2021, Fig. 2]). NN/g goes further:
"Research shows that stacked bar charts are in fact very hard to understand — they are among the
charts with the highest error rates. That is why we strongly recommend that you stay away from
them" ([NN/g, Choosing Chart Types]).

## 3D is never worth it

"Plotting a 2-variable chart in 3D is often done to (arguably) improve aesthetics, but will make the
chart much more difficult to interpret quickly and accurately, as it distorts the shapes and
alignment of the visual features showing data... 3D bar charts are also more difficult to properly
interpret than their 2D counterparts, as they can make it much harder to see which value the top of a
bar represents, and how it aligns with the gridlines." In a 3D pie, "each square centimeter that is
'further away' from the viewer therefore represents more of the area... than an equivalent square
centimeter in the 'front'" ([NN/g, Dashboards]).

The mechanism, from the review: if a viewer pulls values from the 2D image rather than recovering 3D
geometry, "the values in the 'front' will be inflated because of the perspective projection,"
because static 2D projections do not reliably lead to recovery of 3D structure ([Franconeri et al.
2021]). Same failure in 2D icon arrays: encode one-dimensional values as height but the reader
estimates the 2D area, turning a 1:2 ratio into something nearer 1:4, or 1:16 if the icons imply
volume — and "people do indeed make this error, even when the numeric data are printed saliently near
the visual representation" ([Franconeri et al. 2021]).

## Label density and legends

- Carbon: "Avoid filling the chart frame with too many elements, as it impacts the user's ability to
  interpret the data" ([Carbon, Chart anatomy]). Title should be "descriptive and qualitative" and
  "reflect the main insight the data reveals."
- Direct labels beat legends. "One study found that people answered questions about data both faster
  and more accurately when the data were directly labeled in graphs compared with when there was a
  legend" ([Franconeri et al. 2021, citing Lohse 1993]). Carbon's rule is the same: "When possible,
  avoid using a legend and label data representations directly. Legends rely on visual association,
  which can make a chart more difficult to understand," and "Your chart doesn't need a legend if it
  only presents one data category" ([Carbon, Legends]). Exception both sources concede: a legend that
  indexes values labels cannot, e.g. an alphabetical key beside a map.
- Carbon legend geometry: two lines by default; "View more" may expand to 30% of the chart height;
  beyond 30%, scroll. Position bottom or top when space is scarce, left for type alignment, right
  when space is plentiful. Hidden legends are "discouraged... and is inaccessible" except on mobile
  ([Carbon, Legends]).
- Concrete label-density limit, circular charts only: "When the graphic translation of the data is
  less than 3 degrees, a callout is used to clearly associate the label with the slice. If the data
  translates as less than 1 degree, a slice will not be rendered on the chart" ([Carbon, Chart
  anatomy]). The 1-degree case also means the value is not keyboard- or tooltip-reachable — a data
  table is the only access path.
- Non-text marks need 3:1 contrast against adjacent colours. WCAG 1.4.11 applies to "parts of
  graphics required to understand the content," and the Understanding doc's worked example is a
  multi-line chart: "The lines should have 3:1 contrast against their background." Computed values are
  not rounded — 2.999:1 fails ([W3C, non-text contrast]).

## Sparklines

Tufte's own definition, from his site: "Sparklines are small, intense, word-sized graphics with
typographic resolution. Sparklines can be placed anywhere that words or numbers or graphics can be
placed... Sparklines have a data-ink or data-pixel ratio = 1.0, consisting entirely of data, with no
non-data at all. Thus sparklines have no frames, tic marks, and non-data paraphernalia. Sparklines
often get their quantitative scaling context from nearby words, numbers and graphics; sparklines are
directly quantified by numbers on or near the sparkline itself" ([Tufte, History of Sparklines]).

Note the last clause carefully: a sparkline does not carry its own scale. The number beside it does
the quantifying. Ship a sparkline only alongside its value and, where the shape matters, its baseline
period.

## Small multiples

**Not found:** a primary source on small-multiple arrays for dashboard design — the specific claim
Tufte attaches to them and a defensible array-size ceiling. The secondary literature and gist-level
restatements agree that Tufte advocates "small multiple arrays" and high data density, but I did not
open a Tufte page or paper stating it, so it does not go in the skill as a citation. What would
settle it: Tufte's *Envisioning Information* (Graphics Press, 1990) or the small-multiples chapter
in *Visual Explanations* (1997), read directly.

Operationally, until then, borrow the constraints that are sourced: keep the panel count inside
Few's 5-to-7 ceiling, and hold every panel to the same scale so small multiples are actually
comparable.

## Sources

- Franconeri, S. L., et al. "The Science of Visual Data Communication: What Works." *Psychonomic Science & Review* (2021). https://friendly.github.io/6135/papers/Franconeri-etal-2021-WhatWorks.pdf — Springer. Accessed 2026-10-05.
- Carbon Design System, "Color palettes," data visualization. https://carbondesignsystem.com/building-blocks/data-visualization/color-palettes/ — IBM. Accessed 2026-10-05.
- Carbon Design System, "Axes and labels," data visualization. https://carbondesignsystem.com/building-blocks/data-visualization/axes-and-labels/ — IBM. Accessed 2026-10-05.
- Carbon Design System, "Legends," data visualization. https://carbondesignsystem.com/building-blocks/data-visualization/legends/ — IBM. Accessed 2026-10-05.
- Carbon Design System, "Chart anatomy," data visualization. https://carbondesignsystem.com/building-blocks/data-visualization/chart-anatomy/ — IBM. Accessed 2026-10-05.
- Nielsen Norman Group, "Choosing Chart Types: Consider Context" (Kate Moran, Jan 30, 2022). https://www.nngroup.com/articles/choosing-chart-types/ — Nielsen Norman Group. Accessed 2026-10-05.
- Nielsen Norman Group, "Dashboards: Making Charts and Graphs Easier to Understand" (Page Laubheimer, June 18, 2017). https://www.nngroup.com/articles/dashboards-preattentive/ — Nielsen Norman Group. Accessed 2026-10-05.
- Nielsen Norman Group, "Clutter-Free: One of the 3 Cs for Better Charts" (Kate Moran, Feb 6, 2022). https://www.nngroup.com/articles/clutter-charts/ — Nielsen Norman Group. Accessed 2026-10-05.
- Yang, B. W., Vargas Restrepo, C., Stanley, M. L., & Marsh, E. J. "Truncating Bar Graphs Persistently Misleads Viewers." *Journal of Applied Research in Memory and Cognition* (2021). https://gwern.net/doc/psychology/cognitive-bias/2021-yang-4.pdf — Elsevier. Accessed 2026-10-05.
- Edward R. Tufte, "History of Sparklines," ET Notebooks. https://www.edwardtufte.com/notebook/ — Graphics Press. Accessed 2026-10-05.
- Edward R. Tufte, *The Visual Display of Quantitative Information*, 2nd ed., Graphics Press, 2001, chs. 2–3 excerpt. https://lmscontent.embanet.com/USC/CMGT587/Tufte%20Ch2%20and%205.pdf — Graphics Press. Accessed 2026-10-05.
- Stephen Few, "Tapping the Power of Visual Perception," Perceptual Edge, Sept 4, 2004. https://www.perceptualedge.com/articles/ie/visual_perception.pdf — Perceptual Edge. Accessed 2026-10-05.
- Tamara Munzner, "Lecture 5: Perception," CPSC 533C, University of British Columbia, Sept 25, 2006. https://www.cs.ubc.ca/~tmm/courses/cpsc533c-06-fall/slides/percep.pdf — UBC. Accessed 2026-10-05.
- Michael Friendly, "Human Factors Research: How to Tell What Works," lecture notes, Psy 6135, York University. https://friendly.github.io/6135/lectures/HumanFactors-2x2.pdf — York University. Accessed 2026-10-05.
- W3C, "Understanding SC 1.4.11: Non-text Contrast," WCAG 2.2. https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — W3C. Accessed 2026-10-05.