# Toolkit — Bklit UI (bklit.com)

Load when a surface genuinely needs a chart. **First read `charts-data-viz.md` to decide whether it
does** — most dashboard needs are stat-tile needs, not charting needs (`metrics-stat-tiles.md`).

## What it is

Bklit UI is a set of data-visualisation components distributed on a **shadcn registry** under the
`@bklit` namespace, open source and a Vercel OSS Program participant. Trusted by teams at Motion,
Vercel, Prisma, Supabase, Cal.com and OpenPanel. It also publishes its own agent skill.

Install a chart:

```
npx shadcn@latest add @bklit/line-chart
```

Install the agent skill, so the assistant reads your project's real configuration instead of guessing:

```
npx skills add bklit/bklit-ui
```

## The token architecture is the valuable part

This is what to copy even if you never install a Bklit component — it is a clean two-layer chart
token model that slots straight into the three-layer system in `color-token-system.md`:

- **Series palette tokens** `--chart-1` … `--chart-5` for categorical series.
- **Sequential scale tokens** `--chart-scale-01` … `--chart-scale-05` for heatmaps and choropleths.
- A **`chartCssVars`** helper for type-safe theming, rather than raw string colour references.

The separation matters and matches `charts-data-viz.md`: *categorical* encoding and *sequential*
encoding are different jobs and must not share one ramp. A sequential ramp applied to categories
invents an ordering that isn't in the data. If you adopt this, keep the two token families distinct
in `DESIGN.md`.

## Composition pattern

Charts are composed as a root chart plus children, in a fixed order:

```
LineChart → Grid → Line → XAxis → ChartTooltip
```

That ordering is not cosmetic — grid and axes before the mark, tooltip last as the interactive
layer. Adopt the shape so charts read consistently across a product.

## Chart catalog (16 documented types)

Area · Bar · Line · Live Line · Composed · Scatter · Candlestick · Pie · Ring · Radar · Gauge ·
Heatmap · Funnel · Sankey · Sunburst · Choropleth — plus a Profit/Loss Line variant.

Utilities: Legend, Grid, Background, Reference Area, Projection Line, Tooltip, Brush, X Axis, Y Axis,
Custom Indicator, and the `useChart` hook.

**"Live Line Chart" and "Brush" are the two most product-relevant and most often missed.** A live
streaming chart and a range brush are dense-surface instruments; the rest are largely analytics
surfaces. Chart choice by task still governs — see `charts-data-viz.md`.

## Tooling worth copying regardless

- **Studio** — tune props visually and copy the generated code, which keeps the chart in the same
  authoring loop as the rest of the surface instead of in a chart-builder tab.
- **Animation controls** — enter-animation defaults and a `revealSignature` replay pattern, plus
  custom tooltip content and `indicatorColor` for candlestick marks.

## The floor still applies

A charting library does not exempt a chart from `craft-floor.md`:

- Non-text contrast ≥ 3:1 applies to **chart marks**, not just text and borders.
- Chart colour is never the only encoding — pair with position, shape, or label, which is the
  colour-blind-safe rule in `metrics-stat-tiles.md`.
- Axes are not truncated without consequence. `charts-data-viz.md` documents the measured effect.
- Animations are `transform`/`opacity` only, and reduced motion is a real variant.
- A dashboard where every visual shouts communicates nothing — one dominant metric per view.

## Not found

- **No published bundle size or performance budget** for any chart type on the pages read.
- **No accessibility conformance statement** for the chart components — no WCAG level is claimed in
  the pages read. Treat chart a11y as unverified and audit the rendered SVG yourself against
  `accessibility-web.md`.
- **No documented default palette values** for `--chart-1`…`--chart-5` or the scale tokens on the
  pages read; a token inspector on a rendered chart would settle it.
- **No documented guidance on which chart types are performance-safe at high series counts.**

## Sources

| Source | Publisher | URL | Accessed |
|---|---|---|---|
| Bklit UI homepage and component catalog | Bklit | https://bklit.com/ | 2026-10-05 |
| Skills (project-aware agent context, tokens, composition) | Bklit UI | https://bklit.com/docs/skills | 2026-10-05 |

Chart names, token names, `chartCssVars`, `revealSignature`, `indicatorColor`, and the install
commands are quoted from those pages.