# Metrics and stat tiles

The KPI tile on a logged-in B2B product surface: the label/value/delta/trend/timestamp unit that
appears above a chart, in a list row, or in an alert header.
As-of: 2026-10-05.

## Anatomy

Carbon's definition of the atomic unit: "A key performance indicator (KPI) consists of a number with
a single word description. Examples include '15,250 browsers', '$1.3M revenue', or 'Total 450'"
([Carbon, Chart anatomy]). One number, one descriptor — the descriptor is the label.

The full tile is six slots. Every one is optional except the first two; a tile missing slot 3 or 4 is
incomplete, not minimalist.

| # | Slot | Job | Fails when |
| --- | --- | --- | --- |
| 1 | **Label** | Names the metric and its unit ("Monthly active workspaces") | Acronyms, or a title that only makes sense to the team that built it |
| 2 | **Value** | The current figure, formatted and rounded for reading | Six significant figures on a currency figure — Few's mock example of hues used to encode "$6,848.70 at the low end to $419,867.24 at the high end (ignoring the inappropriate six decimal digits of precision)" ([Few, Tapping the Power of Visual Perception]) |
| 3 | **Delta** | Change vs a named baseline, with sign or direction | A bare "+12%" with no baseline; or a bare "12%" and no direction |
| 4 | **Trend** | Shape over time — a sparkline or direction icon | Rendered at a size where the shape cannot be read |
| 5 | **Timestamp** | When the value was computed, and its freshness | Absent on anything that refreshes |
| 6 | **Comparison period** | Which window slot 3 is measured against ("vs previous 7 days") | Absent — the single most common failure |

Carbon on titles generally: they "should be descriptive and qualitative" and "should also reflect the
main insight the data reveals" ([Carbon, Chart anatomy]). On legends, titles and axis labels: "Use
clear language and avoid acronyms" ([Carbon, Legends]).

## Deltas need a baseline period and a direction convention

A delta is a ratio between two numbers. Ship the denominator or the delta is unreadable. NN/g: "If I
told you that the completion rate for checking out in an ecommerce app was 24%, what would that mean?
Nothing, unless I also told you that the completion rate had been 17% in the previous year. **People
need to compare a number against another number in order to interpret it**" ([NN/g, Choosing Chart
Types]).

Checkable rules:

- The comparison period sits in the tile, not in a tooltip or a global filter that may have changed.
  Write "vs previous 7 days", not "vs prev." and never leave it implicit.
- Prefer absolute change alongside percent change when the base is small. A 300% rise on a
  four-event base is a different fact from a 300% rise on a mature metric, and the percent alone
  hides that.
- Smoothing window must match the metric's cadence. A "last 24h" delta on a daily-refreshed warehouse
  metric is a comparison against partial data.
- **Not found:** a sourced convention for whether the tile should show absolute delta, percent
  delta, or both. What would settle it: a study or design-system ruling on percent-delta
  misinterpretation at small bases. In the absence of one, ship both with the base visible on hover
  and in the accessible description.

### Direction convention

Carbon's differential indicator is the vendor pattern, and it is explicit about the sign: "While
typographic indicators can work with just a plus or minus sign, they are most often paired with
arrows or caret icons in our system for better clarity." Colour: "Differential indicators are either
displaying a positive or a negative value. Color is optional in these situations as long as the value
has either a '+' or '-' in front of it, a chevron icon, or an arrow icon. **Unless the data involves
temperature**, positive values are represented by the green spectrum and negative values are
represented by the red spectrum" ([Carbon, Status indicators]).

Checkable rules:

- Green/red polarity is the default. Temperature (latency, °C, disk, page weight) inverts it — falling
  latency is good — and the tile must say which convention it is using, because "up" and "good" are
  not the same axis.
- Direction is always present as glyph (▲ ▼ + −), never as colour alone. See accessibility below.
- Consolidating several statuses into one indicator: "use the highest-attention color to represent the
  group" ([Carbon, Status indicators]).

## Red/green alone is not accessible

WCAG 1.4.1 Use of Color (Level A) is unambiguous: "Color is not used as the only visual means of
conveying information, indicating an action, prompting a response, or distinguishing a visual
element." The Understanding doc's named failure cases include exactly this shape — "Mary's sales are
in red, Tom's are in blue" — and it notes that a lightness difference can substitute for a hue
difference only when the relative luminance difference reaches 3:1 or greater ([W3C, use of color]).

Carbon's operational version: "Relying solely on color to convey status is insufficient... status
indicators should rely on at least two of the following elements: color, shape, or symbol." And for
contrast: "ensure that there's at least a 3:1 contrast between colors used for status indicators, as
well as between the indicator and the page background. If the contrast is sufficient, even in
grayscale, users should still be able to differentiate statuses without relying solely on color"
([Carbon, Status indicators]).

The grayscale test is the cheap one to run: desaturate the tile screenshot. If positive and negative
become indistinguishable, the tile fails.

Evidence that redundancy beats either channel alone, from an actual study (96 participants, four
mobile list/table designs varying indicator strategy): "Users are roughly 37% faster at finding items
within a list on a web page when visual indicators vary both in color and icon compared to text
alone." Text-only indicators were "57% slower" than the best condition; icon-only was "marginally
faster" than color-only overall and "significantly better than color on 2 out of 4 metrics" for
stock-performance tables, where users had to infer that red meant a decrease and green an increase
([NN/g, Visual Indicators to Differentiate Items in a List]).

Prevalence figures disagree, so do not quote one as fact. Carbon states color-blindness "affects 8%
of all men and 0.4% of women" ([Carbon, Accessibility]). Franconeri et al. state color-vision
impairments "are estimated to affect 4% of the global population... or roughly 300 million people,"
citing Olson & Brewer (1997), and identify protanopia (red-green) as the most common form
([Franconeri et al. 2021]). NN/g gives "up to 4.5% of the general population... around 8% vs. 0.5%"
for men vs women, adding that "exact numbers vary by ethnicity" ([NN/g, Dashboards]). Either way the
design conclusion is identical: assume a double-digit slice of B2B buyers cannot resolve red from
green.

## Why identical tiles flatten hierarchy

Four tiles with the same label size, same value size, same padding, and same delta treatment
communicate no ranking among themselves. The reader's eye has no signal to stop on, so the row
behaves as a single undifferentiated block and the reader must read all four labels to know which
one is theirs — the exact behaviour a dashboard is meant to prevent.

What the primary sources require instead:

- Carbon, Presentation dashboards: "The most important data should have the highest contrast and
  occupy the largest area" ([Carbon, Dashboards]). Identical tiles make every tile equal-area and
  equal-contrast, which is a direct violation.
- Carbon, Presentation dashboards: "Prioritize data by importance, then create a clear visual
  hierarchy," ordered by the F-pattern — most important at the top, then left to right, least
  important last ([Carbon, Dashboards]).
- NN/g: dashboards "are focused on a single task: communicating critical information" ([NN/g,
  Dashboards]). Four equal tiles push the ranking decision onto the reader.
- Few, on memory: "you must limit the number of data components that encode distinct meanings to
  seven at most — and safer yet, to no more than five" ([Few, Tapping the Power of Visual Perception]).

Concrete remedies, in order of leverage:

1. Give one tile a larger value type and more space. Break the grid for it rather than for the others.
2. Reduce the rest. Four tiles → one dominant plus three supporting, or three total.
3. If a row of equals is genuinely the answer, the surface is a metrics list, not a dashboard. Say so
   in the page title and stop calling it an overview.
4. Reach for colour only as reinforcement: NN/g's method is to build the chart in grayscale first,
   then colour the series that carries the takeaway ([NN/g, Contrast]). That works for tiles too — one
   accent, everything else neutral.

**Not found:** a study measuring comprehension or time-to-decision for congruent vs non-congruent KPI
tile rows. What would settle it: a between-subjects test varying only tile size congruence with task
time and first-look fixation location as outcomes. The hierarchy rule above is Carbon's stated
requirement, not a measured effect.

## Freshness

**Not found:** a sourced rule for when a metric tile must show a timestamp, what staleness threshold
triggers a stale treatment, or whether the threshold should be absolute or a multiple of the metric's
own cadence. Carbon's guidance is silent on this and NN/g's dashboard article does not address it.
What would settle it: an operations-source SLO or observability-vendor standard (OpenTelemetry
semantic conventions for metric staleness, or an IBM Equal Access requirement) opened directly.
Ship the timestamp unconditionally and pick the staleness threshold from the product's own refresh
cadence — and record that the threshold itself is unsourced.

## Sources

- Carbon Design System, "Chart anatomy," data visualization. https://carbondesignsystem.com/building-blocks/data-visualization/chart-anatomy/ — IBM. Accessed 2026-10-05.
- Carbon Design System, "Dashboards," data visualization. https://carbondesignsystem.com/building-blocks/data-visualization/dashboards/ — IBM. Accessed 2026-10-05.
- Carbon Design System, "Legends," data visualization. https://carbondesignsystem.com/building-blocks/data-visualization/legends/ — IBM. Accessed 2026-10-05.
- Carbon Design System, "Status indicators," patterns. https://carbondesignsystem.com/building-blocks/core/patterns/status-indicators/ — IBM. Accessed 2026-10-05.
- Carbon Design System, "Accessibility," foundations. https://carbondesignsystem.com/building-blocks/foundations/accessibility/ — IBM. Accessed 2026-10-05.
- Nielsen Norman Group, "Choosing Chart Types: Consider Context" (Kate Moran, Jan 30, 2022). https://www.nngroup.com/articles/choosing-chart-types/ — Nielsen Norman Group. Accessed 2026-10-05.
- Nielsen Norman Group, "Dashboards: Making Charts and Graphs Easier to Understand" (Page Laubheimer, June 18, 2017). https://www.nngroup.com/articles/dashboards-preattentive/ — Nielsen Norman Group. Accessed 2026-10-05.
- Nielsen Norman Group, "Visual Indicators to Differentiate Items in a List" (Aurora Harley, Aug 7, 2016). https://www.nngroup.com/articles/visual-indicators-differentiators/ — Nielsen Norman Group. Accessed 2026-10-05.
- Nielsen Norman Group, "Contrast: One of the 3Cs for Better Charts" (Kate Moran, Feb 13, 2022). https://www.nngroup.com/articles/contrast-charts/ — Nielsen Norman Group. Accessed 2026-10-05.
- W3C, "Understanding SC 1.4.1: Use of Color," WCAG 2.2. https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html — W3C. Accessed 2026-10-05.
- Franconeri, S. L., et al. "The Science of Visual Data Communication: What Works." *Psychonomic Science & Review* (2021). https://friendly.github.io/6135/papers/Franconeri-etal-2021-WhatWorks.pdf — Springer. Accessed 2026-10-05.
- Stephen Few, "Tapping the Power of Visual Perception," Perceptual Edge, Sept 4, 2004. https://www.perceptualedge.com/articles/ie/visual_perception.pdf — Perceptual Edge. Accessed 2026-10-05.