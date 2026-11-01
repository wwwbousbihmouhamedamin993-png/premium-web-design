# Typography for web product UI

Marketing pages get expressive type: fluid sizes, display weights, generous leading. Product UI gets
the opposite — a **small fixed stepped ramp** that never resizes, because a data table that reflows
its type at a breakpoint is a table the user can no longer scan vertically. This file owns type
sizes, line heights, fonts, and loading. Density classes and row heights are in
`information-density.md`.

## Fixed stepped sizes — fluid type is a marketing technique

This is the load-bearing distinction, and it comes from Carbon's own split. The **productive** type set
ships inside product; the **expressive** set is for editorial and web pages. Carbon sets the split by
base size — productive uses "a base type size of 14px, while the expressive set uses a base type size of
16px" — then draws the line that matters: "**The productive type set uses fixed headings.** Product pages
have a higher density of information housed inside containers for space efficiency, and in these
situations fixed type styles are a must," while "The expressive type set… The remaining headings are
**fluid**… can extrapolate/stretch in between sizes for smooth transitions." And: "Fixed means they are
not responsive. **The type size remains constant regardless of break point**," with the instruction "**Do
not use these styles inside a container**" (all Carbon Design System, *Type sets*, accessed 2026-10-05).

Carbon is unusually direct about the consequence of mixing: "People unconsciously use type size as a
signal of hierarchy, and each type set has been designed with expectations about hierarchy in mind.
**Mixing type styles within a component could jumble the hierarchy and create confusion**" (Carbon,
*Typography — style strategies*, accessed 2026-10-05).

**The rule:** inside a logged-in product surface, no font size is a function of viewport width. If a
size must differ between a wide table and a narrow drawer, that is a **density class** change
(`information-density.md`) or a container query on a container token — not `clamp()` with `vw`.

## The product ramp

Fixed, four steps plus the code face. Values are the house ramp, calibrated against Carbon's
productive set, which supplies `label-01` 12px/16px, `body-compact-01` 14px/18px, `body-01` 14px/20px,
`heading-compact-01` 14px/18px at 600, and `code-01` 12px (Carbon, *Type sets*, accessed 2026-10-05).

| Token | Size | Line height | Weight | Product use |
|---|---|---|---|---|
| `--text-xs` | 12px | 16px | 400 | Field labels, helper text, error text, table micro-labels, badges |
| `--text-sm` | 14px | 20px | 400 | Default UI body: table cells, list rows, nav items, button labels |
| `--text-md` | 16px | 24px | 400 | Record-page field values, settings prose, Focused-class form body |
| `--text-lg` | 20px | 28px | 600 | Page title, record name, section heading |
| `--text-mono` | 12px | 16px | 400 | IDs, hashes, code, raw values, Dense timestamps |

**Line height is coupled to size, not global.** Every step has an explicit line height, and they are
not a constant ratio: 12/16 = 1.33, 14/20 = 1.43, 16/24 = 1.5, 20/28 = 1.4. Small text needs
proportionally more leading than large text because the relationship between x-height and line box is
what carries legibility at 12px. Never ship a bare `line-height: 1.5` on everything.

**Weight discipline.** Two functional weights in product: 400 and 600. Carbon: "use IBM Plex Light,
Regular, and SemiBold for digital experiences. **The semibold weight is ideal for section headers, but
should not be used for long text**" (Carbon, *Typography — overview*, accessed 2026-10-05). Three
weights max; a weight appearing nowhere else is a bug.

**Pair compact heading with compact body.** Carbon's `heading-compact-01` (14px, 600) pairs with
`body-compact-01` (14px/18px); pairing a 14px semibold heading with 16px body destroys the weight
contrast that made it a heading (Carbon, *Type sets*, accessed 2026-10-05).

**Never mix density classes on one screen.** A 12px Dense table beside 16px prose without a reason is
a class violation — see `information-density.md`.

## Tabular numerals, measure, and wrapping

In a data table, digits must occupy equal width or columns visibly wobble. MDN: `tabular-nums` activates
"the set of figures where numbers are all of the same size, **allowing them to be easily aligned like in
tables**. It corresponds to the OpenType values `tnum`" (MDN, *`font-variant-numeric`*, accessed
2026-10-05). Apply `.numeric { font-variant-numeric: tabular-nums; }` to every numeric table cell, currency,
count, quantity, percentage, ID, hash, version string, and metric-tile value (`metrics-stat-tiles.md`) — not
to prose, dates in running text, or badge labels that never repeat. The font must actually contain `tnum`:
it is an OpenType feature, not a CSS-generated effect, and system fonts vary, so **verify the rendered
widths** rather than trusting the declaration. Also relevant: `slashed-zero` (same MDN page) — where `0` and
`O` appear in adjacent columns (SKUs, hostnames, hex IDs) it removes a real class of error. Apply it to
the mono token, not globally.

- **Cap prose measure at 65–80 characters.** WCAG 2.2 SC 1.4.8 Visual Presentation (AAA) requires a
  mechanism for "Width is no more than 80 characters or glyphs (40 if CJK)," plus non-justified text,
  "Line spacing (leading) is at least space-and-a-half within paragraphs," and paragraph spacing "at least
  1.5 times larger than the line spacing" (W3C WAI, *Understanding SC 1.4.8*, accessed 2026-10-05).
- **Never justify.** The same SC requires non-justified text, and Carbon states `body-01` is "always
  left-aligned" (Carbon, *Type sets*, accessed 2026-10-05). Table cells do not need a measure — a cell is one
  line by definition, so `max-width: 70ch` on a cell is a defect.
- **`text-wrap` where it helps, only where it helps.** `balance` — "this value is only supported for blocks
  of text spanning a limited number of lines (**six or less for Chromium and ten or less for Firefox**)" —
  fits page titles and record names. `pretty` — "the user agent will use a slower algorithm that favors
  better layout over speed… where the number of orphans should be kept to a minimum" — fits prose in
  Focused surfaces. **Never apply either globally:** browsers cap the line count and fall back to `wrap`, so
  a global `* { text-wrap: balance }` costs layout time and changes nothing past six lines, and `pretty` in
  a table is real cost on a 1,000-row grid (all MDN, *`text-wrap`*, accessed 2026-10-05).

## Font families

**`system-ui` for product.** MDN notes `system-ui` "is intended to make UI elements look like native
apps, and **not for typesetting large paragraphs of text**," warning that some platforms' default UI
fonts render Latin poorly in CJK contexts (MDN, *`<generic-family>`*, accessed 2026-10-05). For a
logged-in product, "not for large paragraphs" is exactly right. Set `--font-ui: system-ui, sans-serif;`
— the advantage is not aesthetic but performance: a system stack makes **zero network requests for the
primary face**, removing an entire class of layout shift.

**`font-optical-sizing` — leave it `auto`.** MDN: the initial value is `auto`, "optical sizing is enabled
by default for fonts that have an optical size variation axis," and it is Baseline *Widely available*,
"available across browsers since March 2020" (MDN, *`font-optical-sizing`*). The mechanism matters here:
"small text sizes are often rendered with thicker strokes and larger serifs, whereas larger text is often
rendered more delicately." The product ramp spans 12px to 20px — exactly the range where optical sizing
earns its keep. Set `font-optical-sizing: none` only when a brand requires a single master.

**`font-size-adjust` for fallback matching — Baseline 2024 Newly available.** MDN: it "is intended for
adjusting fallback fonts to have similar metrics as the first-choice font," is part of Interop 2024
(web.dev, *CSS font-size-adjust is now in Baseline*), and computes `u = (m / m′) s` where `m` is the
desired metric ratio, `m′` the chosen font's actual ratio, and `s` the `font-size` (MDN,
*`font-size-adjust`*). MDN's worked example: a 12px font with cap-height ratio 0.20 falling back to one
at 0.15 renders at `16px` — the fallback is scaled to match the primary's cap height. So a value
matching your primary's `ex-height` or `cap-height` ratio keeps the fallback from shifting layout during
load. Because it is only *Newly available*, treat it as progressive enhancement.

## `font-display`: choose per role

MDN's timeline is the model — three periods: the **font block period** (text renders with an *invisible*
fallback), the **font swap period** (a *visible* fallback), then the **font failure period** (treated as a
failed load). Period lengths are set by `font-display` (MDN, *`font-display`*, accessed 2026-10-05).

| Value | Block period | Swap period | Role in a product |
|---|---|---|---|
| `auto` | Varies by browser | Varies by browser | Never specify — non-deterministic |
| `block` | Short (~3s recommended) | Infinite | Logo/wordmark text where the face *is* the message |
| `swap` | Extremely small | Infinite | Brand headings, visually distinctive text |
| `fallback` | Extremely small (~100ms) | Short (~3s) | **Body text** — read immediately, tolerate a late swap |
| `optional` | Extremely small (~100ms) | **None** | Above-the-fold critical text; no swap, so no shift |

Durations from MDN's `FontFace.display` docs (accessed 2026-10-05): block "recommends 3 seconds for the
block period"; fallback "recommends 100 ms or less for the block period and 3 seconds for the swap
period"; optional "recommends 100 ms or less"; swap "a 0 second block period and an infinite swap period".
web.dev reaches the same assignment and names the two failure modes: FOIT "delays First Contentful Paint
(FCP)" and sometimes LCP; swapping "can cause layout shifts and impact Cumulative Layout Shift (CLS)"
(web.dev, *Best practices for fonts*). Its mixed strategy: "use `font-display: swap` for branding and
other visually distinctive page elements. Use `font-display: optional` for fonts used in body text."

Three mechanical facts that catch teams. **`font-display` is per `@font-face`, not per family** — set it
on every face. **Preload plus `fallback`/`optional` eliminates jank:** "Since Chrome 83, `link
rel="preload"` and `font-display: optional` can be combined to remove layout jank completely" (web.dev,
*Prevent layout shifting and flashes of invisible text (FOIT) by preloading optional fonts*, accessed
2026-10-05) — but with the corollary that "if the web font isn't downloaded within 100ms, then the
fallback font is used and **no swapping occurs**," so a cold first visit may never show the brand face.
That asymmetry is why `optional` suits product body text and not marketing headlines. And **add
`size-adjust` to the fallback face** — web.dev names it as the CLS mitigation.

## Verify

- Grep for `clamp(`, `vw`, `vh` inside any `font-size`. In a product surface, every hit is a finding.
- Confirm no rule sets `font-size` without a paired `line-height` token.
- Render mixed-width numbers (`1`, `8`, `111`, `0`) and confirm equal digit widths. Unequal means the
  loaded face has no `tnum`. Check `0` vs `O` in any ID or SKU column.
- Measure prose line length at the widest breakpoint. Over 80ch is a finding.
- Confirm no `text-align: justify` anywhere.
- Tab through on a slow 3G profile with the cache cleared; watch for invisible text or table reflow.
- Count distinct font weights in use. More than three is a finding.

**Not found:** no primary source specifies a required font-size step count for product UI, a minimum
product body size, or a required optical-size axis per size. The five-step ramp, the two-weight
discipline, and the 65–80ch measure target are house rules calibrated against Carbon's productive set
and SC 1.4.8's 80-character ceiling. What would settle them: legibility testing with real users and a
`DESIGN.md` decision.

## Sources

- Type sets (productive base 14px / expressive base 16px; productive headings fixed, expressive fluid; "do not use [fluid] inside a container"; fixed = constant regardless of break point; compact heading pairs with compact body; `body-01` always left-aligned; productive token values) — Carbon Design System (IBM). https://carbondesignsystem.com/elements/typography/type-sets/ — accessed 2026-10-05
- Typography — style strategies ("Mixing type styles within a component could jumble the hierarchy and create confusion") · Typography — overview (productive vs expressive intent; Light/Regular/SemiBold; semibold not for long text) — Carbon Design System (IBM). https://www.carbondesignsystem.com/building-blocks/foundations/typography/style-strategies · https://carbondesignsystem.com/elements/typography/overview/ — accessed 2026-10-05
- `font-variant-numeric` (`tabular-nums` aligns figures like in tables; `tnum`; `slashed-zero`) · `font-display` (three-period timeline) · `FontFace.display` (recommended periods: ~3s block; ~100ms fallback block and 3s fallback swap; 0s swap block) · `font-optical-sizing` (initial `auto`; Baseline Widely available since March 2020) · `font-size-adjust` (Baseline 2024 Newly available; `u = (m / m′) s`; 12px→16px cap-height example) · `<generic-family>` (`system-ui` not for large paragraphs) · `text-wrap` (`balance` limited to six lines Chromium / ten Firefox; `pretty` favours layout over speed) — MDN. https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variant-numeric · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@font-face/font-display · https://developer.mozilla.org/en-US/docs/Web/API/FontFace/display · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-optical-sizing · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-size-adjust · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/generic-family · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap — accessed 2026-10-05
- Best practices for fonts (FOIT delays FCP/LCP; swapping impacts CLS; swap for branding, optional for body text; `size-adjust` mitigation) · Prevent layout shifting and FOIT by preloading optional fonts (Chrome 83 + preload + `optional` removes jank; 100ms no-swap consequence) · CSS font-size-adjust is now in Baseline (Interop 2024) — web.dev. https://web.dev/articles/font-best-practices · https://web.dev/articles/preload-optional-fonts · https://web.dev/blog/font-size-adjust — accessed 2026-10-05
- Understanding SC 1.4.8 Visual Presentation (≤80 characters or glyphs, 40 if CJK; non-justified; line spacing ≥ space-and-a-half; paragraph spacing ≥ 1.5× line spacing) — W3C Web Accessibility Initiative. https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html — accessed 2026-10-05
