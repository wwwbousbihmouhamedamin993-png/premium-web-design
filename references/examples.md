# Before / after — the eight highest-frequency failures

Eight violations that account for most of what a logged-in B2B product gets wrong. Each pair shows the
failure, the fix, and the rule. The floor is `craft-floor.md`. Density tags: `[F] Focused ·
[S] Standard · [D] Dense`. Every "after" is a token-based, framework-neutral sketch — adapt selectors
to the host stack, keep the structure. As-of: 2026-10-05.

---

## 1. Marketing aesthetics inside the product

**Before.** The logged-in dashboard was designed like the pricing page: gradient text on the hero
metric, a radial glow behind the card grid, glassmorphism on content cards, a purple/cyan AI palette.

```css
.page-title { background: linear-gradient(90deg,#7c3aed,#06b6d4);
              -webkit-background-clip: text; color: transparent; }
.card { background: rgba(255,255,255,.65); backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(124,58,237,.25); }
.page::before { content:""; position:absolute; inset:0;
  background: radial-gradient(600px at 20% 0%, rgba(124,58,237,.18), transparent); }
```

**After.** Depth from surface steps and hairlines. Accent at most twice, on the primary action and the
one live status.

```css
.page-title { color: var(--text-primary); font-size: var(--text-size-page-title); }
.card { background: var(--surface-raised); border: 1px solid var(--border-subtle); }
/* accent budget: .btn--primary { background: var(--accent-action) } — the only fill */
```

**Why.** Public marketing pages belong to `premium-marketing-design`. Inside the app a glow competes
with the data. NN/g caps colour-driven hierarchy: no more than 3 contrast variations and no more than
2 big elements — "if everything is contrasted, then nothing stands out."

## 2. Nested cards

**Before.** A record page wrapped three fields in a card, inside a card, inside a page panel.

```html
<section class="panel"><div class="card"><div class="card"><div class="card">
  <h3>Billing address</h3><p>…</p></div></div></div></section>
```

**After.** One container; grouping done with space and a divider.

```html
<section class="panel"><h3>Billing address</h3><p>…</p><hr class="rule" /></section>
```

**Why.** Nested cards 2–3 deep mean the structural split is overdue. Alignment does the grouping;
whitespace separates groups; nested boxes are the last resort. One card per container, always.

## 3. The stat-card row

**Before.** Four identical KPI tiles in a row, same weight as everything else, each in its own card.

```html
<div class="grid-4">
  <div class="card"><span class="label">MRR</span><b>$48,210</b></div>
  <div class="card"><span class="label">Active seats</span><b>312</b></div>
  <div class="card"><span class="label">Churn</span><b>1.4%</b></div>
  <div class="card"><span class="label">Open tickets</span><b>27</b></div>
</div>
```

**After.** One dominant metric; three supporting values in a quiet definition list — no boxes, one rule
between.

```html
<section class="summary">
  <div class="summary__lead">
    <span class="label">Monthly recurring revenue</span>
    <b class="metric">$48,210</b>
    <span class="delta">▲ 6.2% vs previous 30 days</span>
  </div>
  <dl class="summary__support">
    <div><dt>Active seats</dt><dd>312</dd></div>
    <div><dt>Churn</dt><dd>1.4%</dd></div>
    <div><dt>Open tickets</dt><dd>27</dd></div>
  </dl>
</section>
```

**Why.** When every number shouts, nothing communicates. Kaplan's corrective for complex applications:
"making important information stand out does not always mean adding emphasis… **removing nonessential
elements can be equally or even more effective**." Every delta names its baseline period; every figure
is `tabular-nums`.

## 4. A spinner on a blank page

**Before.**

```html
<div class="page"><div class="spinner"></div></div>
```

**After.** A skeleton with the real geometry, plus a busy region for assistive tech.

```html
<div class="page" aria-busy="true" aria-live="polite">
  <div class="skeleton skeleton--h1"></div>
  <table class="grid"><tbody>
    <tr><td><div class="skeleton skeleton--cell"></div></td>
        <td><div class="skeleton skeleton--cell"></div></td></tr>
    <!-- one row per expected row, same heights as the real table -->
  </tbody></table>
</div>
```

**Why.** A centred spinner on a blank page says nothing about what is arriving and guarantees a layout
shift when data lands. Polaris on `SkeletonPage`: "Keep the page structure stable and replace the
region when data arrives." A skeleton is the only correct answer for a whole-page fetch; a spinner is
correct inside a small region that keeps its own shape.

## 5. Tiny type as density

**Before.** "We need more rows on screen," answered with 9px table text.

```css
.table { font-size: 9px; line-height: 1.1; }  /* 40 rows visible */
```

**After.** Density from row height, column count and leading. Narrow viewports drop columns, not type.

```css
.table { font-size: 13px; line-height: 1.4; }
[data-density="dense"]   .table tr { height: 32px; }  /* 28–32px [D] */
[data-density="standard"] .table tr { height: 40px; } /* 40–44px [S] */
@media (max-width: 720px) { .col--last-seen { display: none; } }
```

**Why.** A 13px tabular numeral in a dense table is correct; a 9px one is unreadable and is
degradation, not density. Density comes from row height, column pruning and tight leading. Note that a
generic detector flags this as `tiny-interface-text` and is **wrong at [D]** — the floor's per-density
override table marks it advisory there on purpose.

## 6. A non-tabular numeric column

**Before.** A revenue column where digits jitter, because the font's default figures are proportional
and `font-variant-numeric` was never set.

```css
td.amount { text-align: right; }  /* right-aligned, still proportional figures */
```

**After.**

```css
.amount, .mono-id, .timestamp { font-variant-numeric: tabular-nums; }
.amount { text-align: right; }  .label { text-align: left; }
```

**Why.** `tabular-nums` activates "the set of figures where numbers are all of the same size, allowing
them to be easily aligned like in tables" (OpenType `tnum`) — MDN, `font-variant-numeric`, Baseline
widely available. The property inherits, so set it on the cell class, not per cell. Right-align
numbers, left-align text, never centre a numeric column. Use a monospace face for identifiers, hashes
and raw timestamps — not for prose.

## 7. A hover-only affordance

**Before.** Row actions exist only on `:hover`, so they are invisible to keyboard and touch users.

```css
.row-actions { opacity: 0; }
.row:hover .row-actions, .row:focus-within .row-actions { opacity: 1; }
```

**After.** Always present, enhanced by hover, reachable by focus and touch.

```css
.row-actions { opacity: 1; }   /* default: visible, never hover-gated */
@media (hover: hover) { .row:hover .row-actions { background: var(--surface-hover); } }
.row:focus-within { outline: 2px solid var(--border-focus); outline-offset: -2px; }
```

**Why.** Hover may reveal; focus and touch must reach the same content — and WCAG is explicit that
hover styling is optional and not required to identify the hover state. The `hover` media feature
exists precisely because the primary input may have no hover capability at all (`hover: none`). Never
remove `:focus-visible`. On touch, actions live in an always-available row menu.

## 8. A disabled primary button with no explanation

**Before.**

```html
<button class="btn btn--primary" disabled>Upgrade plan</button>
```

**After.** Say why, and offer the fix. Prefer making it actionable.

```html
<button class="btn btn--primary" aria-describedby="seat-why"
        onclick="location.href='/settings/billing/seats'">Upgrade plan</button>
<p id="seat-why" class="field-help field-help--warn">
  <svg aria-hidden="true">…</svg> You've used all 10 seats on Team. Add seats to upgrade.
</p>
```

Where the action truly cannot be enabled, keep it disabled **and** expose the reason:

```html
<button class="btn btn--primary" disabled aria-describedby="mfa-why">Verify identity</button>
<p id="mfa-why" class="field-help">Two-factor enrolment is required before this action.</p>
```

**Why.** An unexplained disabled primary is a dead end at the exact moment the user decided to act.
Polaris: "Hide unavailable actions or render real disabled actions with an explanation. Don't display
controls that look actionable but have no outcome." Status here is never colour alone — warning ships
with an icon and text.

---

**Cross-cutting: three habits that fix most of the above.** Declare the density class before writing
type or spacing; one class per surface, with row height, gutter and type size from one scale. Render it
and look at it — `render-loop.md`, minimum two critique–fix passes on real pixels. Run the four drift
sweeps in `tokens.md`.

## Sources

This file cites the skill's own floor rather than re-deriving it. All rules below come from **Craft floor — `references/craft-floor.md`**, accessed 2026-10-05: density classes (Focused 16px / Standard 14-15px / Dense 12-13px; row heights 28-32 / 40-44px); whitespace budget by class; "Density comes from row height, column pruning, and tight leading — never from type small enough that a first-time user must zoom"; "Tabular numerals for anything comparable"; "Right-align numbers, left-align text"; "Never center a numeric column"; "Nothing important depends on hover"; "A disabled control says why on focus or hover, rather than being silently dead"; "One primary (filled) CTA per view [F/S]"; "Every surface that fetches has all four: loading (skeleton shaped like the real content — never a centred spinner on a blank page), empty, error, offline/stale"; the Refuse list (marketing aesthetics inside the product, card inflation, stat-card dashboard, tiny type as a density strategy, a disabled primary button as the only affordance); and the per-density detector override table marking `tiny-interface-text` advisory at [D].

Vendor and standards evidence behind those rules, all accessed 2026-10-05:

- **`font-variant-numeric`** (`tabular-nums`; Baseline widely available since January 2020) — MDN Web Docs, Mozilla. https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variant-numeric
- **Understanding SC 2.4.7 Focus Visible; SC 1.4.11 Non-text Contrast** (3:1 for focus indicators and control boundaries) — W3C WAI. https://www.w3.org/TR/WCAG22/ · https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- **Loading pattern** (skeletons over spinners; progressive loading; keep page structure stable) — Carbon Design System, IBM. https://carbondesignsystem.com/building-blocks/core/patterns/loading/
- **Spinner** (500ms guidance; indeterminate only; no timeout or error state) — Shopify Polaris web components. https://shopify.dev/docs/api/app-home/latest/web-components/feedback-and-status-indicators/spinner
- **SkeletonPage** ("Keep the page structure stable and replace the region when data arrives"; "Hide unavailable actions or render real disabled actions with an explanation") — Shopify Polaris. https://polaris.shopify.com/components/feedback-and-indicators/skeleton-page
- **Visual Hierarchy in UX** ("if everything is contrasted, then nothing stands out"; caps of 3 contrast variations and 2 big elements) — Nielsen Norman Group, Kelley Gordon, 2021-01-17. https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
- **8 Design Guidelines for Complex Applications** ("making important information stand out does not always mean adding emphasis… removing nonessential elements can be equally or even more effective") — Nielsen Norman Group, Kate Kaplan, 2020-11-08. https://www.nngroup.com/articles/complex-application-design/
- **Data table** (row sizes xs 24 / sm 32 / md 40 / lg 48 / xl 64) — Carbon Design System, IBM. https://carbondesignsystem.com/components/data-table/usage/
