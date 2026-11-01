# Web Vitals as design constraints

Applies to: every logged-in product surface. LCP, INP and CLS are not an engineering afterthought —
they are decided by choices made in the design file: which element is the biggest, how tall the
skeleton is, whether a row animates open, whether a dialog mounts before its content arrives.

## The three gates

| Metric | Good | Poor | Judged at | Source |
|---|---|---|---|---|
| LCP — Largest Contentful Paint | ≤ **2.5 s** | > 4.0 s | 75th percentile of page loads, segmented mobile/desktop | [S1][S2] |
| INP — Interaction to Next Paint | ≤ **200 ms** | > 500 ms | 75th percentile, segmented mobile/desktop | [S1][S3] |
| CLS — Cumulative Layout Shift | ≤ **0.1** | > 0.25 | 75th percentile, segmented mobile/desktop | [S1][S4] |

The thresholds apply to all pages and a page is judged as passing only if it "meets the
recommended targets at the 75th percentile for all three" [S1].

Two facts that set expectations before any design work:

- **90% of a user's time on a page is spent *after* it loads** — Chrome usage data, cited by
  web.dev [S3]. Responsiveness is therefore a whole-session property, not a load property. INP
  "observes the latency of all interactions a user has made with the page" and reports a single
  value [S3].
- **LCP includes TTFB**: "It is important to note that LCP includes any unload time from the
  previous page, connection set up time, redirect time, and other Time To First Byte (TTFB)
  delays" [S2]. On a logged-in surface, where auth and data waterfalls are on the critical path,
  this is where LCP actually goes to die.

## CLS: the metric that is pure design

CLS is "a unitless value based on a calculation of how much content is shifting and by how far" [S4].
web.dev names the causes, and every one is a design decision: "Images without dimensions. Ads,
embeds, and iframes without dimensions. Dynamically injected content such as ads, embeds, and
iframes without dimensions. Web fonts." [S4] The stated purpose is to quantify "how often users
experience unexpected layout shifts", and unexpected movement "can make them click the wrong link or
button … a sudden shift in layout makes the user confirm a large order they intended to cancel"
[S4]. On a B2B console the specific harm is clicking **Delete** on a row that has moved, or
**Approve** on a request that shifted under the cursor.

### The rule: every async region declares its final size

web.dev's remedy is unambiguous: "**reserve sufficient space in the viewport for it in advance (for
example, using a placeholder or skeleton UI)** so that when it loads, it does not cause content in
the page to surprisingly shift around. Alternatively, ensure the element is not part of the
document flow by overlaying the content" [S4]. For lists that genuinely grow, the fix is a **fixed
size container**, with this warning: "Remember to disable any links and controls until the transition
has completed to prevent accidental clicks or taps while the new content is coming in" [S4].

Two **house rules (judgement, not sourced)**: (1) **skeleton geometry must equal the resolved
geometry** — same row height, column widths, resolved row count, chart height; a 40px skeleton row
where the real row is 48px produces the shift it was meant to prevent (`loading-skeletons.md`
records that no primary source states dimension-identity as a requirement — only reserve-the-box
[S4]); (2) **reserve the empty state too** — zero rows and twenty rows are both possible results, so
a count-dependent height needs a min-height covering the empty case.

The exemption that matters for lists: **"layout shifts that occur within 500 milliseconds of user
input are not counted towards CLS"** [S4]. That is a reporting exemption, not a licence — a row-insert
shift after a "Load more" click still moves the target the user is about to aim at. web.dev's own
recommendation is to have the user initiate the load and "it's recommended to prefetch the content
before the user interaction so that it shows up immediately" [S4].

**Images and iframes:** "Always include **width and height** attributes on your images and video
elements. Alternatively, reserve the required space with **CSS aspect-ratio** or similar. This
approach ensures that the browser can allocate the correct amount of space in the document while the
image is loading." [S4]

### Fonts: `font-display` is a CLS and LCP decision

web.dev's two failure modes: **delayed text rendering** — "If a web font has not loaded, browsers
typically delay text rendering. In many situations, this delays First Contentful Paint (FCP). In some
situations, this delays Largest Contentful Paint (LCP)" [S5] — and **layout shifts** — "The practice of
font swapping has the potential to cause layout shifts and impact Cumulative Layout Shift (CLS).
These layout shifts occur when a web font and its fallback font take up different amounts of space"
[S5].

The three periods per MDN's `font-display` reference [S6]: **block** — render an invisible fallback
face until the font loads; **swap** — render the fallback face; **failure** — treat as a failed load.

| Value | Block period | Swap period | Character |
|---|---|---|---|
| `block` | 2–3 s | infinite | Text invisible first, then webfont |
| `swap` | 0 ms | infinite | Fallback visible immediately, swaps in later |
| `fallback` | 100 ms | 3 s | Short block, short swap window |
| `optional` | 100 ms | **none** | No swap; a late font is simply not used |
| `auto` | varies | varies | User agent decides |

Browser defaults matter: **Chromium and Firefox block text rendering for up to 3 seconds**;
**Safari blocks indefinitely** [S5]. Unconfigured, body text can be invisible for three seconds —
which delays LCP, not just aesthetics.

web.dev's recommendations, and the trade each encodes [S5]: **`optional`** for maximum performance —
"text render is delayed for no longer than 100ms and there's assurance that there isn't font-swap
related layout shifts", costing the webfont if it arrives late. **`swap`** to show text fast and
still use a webfont — deliver the font early enough to avoid a shift, at the cost of "the jarring
shift when the font arrives late". **`block`** to always show the webfont — still shifts, because
the fallback's space was reserved, but "the text itself won't be seen to shift." web.dev's overall
judgement: `swap` "delays text render the least. Thus, it can be the preferred approach for
situations where it's important that text is displayed as quickly as possible, but ultimately gets
rendered as a web font" [S5]. It also proposes the split: **`swap` for branding, `optional` for body
text** [S5]. The CLS mitigation it names is **`size-adjust`** [S5], plus `unicode-range` subsetting —
web.dev's own example serves per-script `woff2` subsets (`U+0900-097F` devanagari, `U+0100-024F`
latin-ext, …) under one family [S5].

**House rule (judgement, not sourced):** `swap` for the product's display face, `optional` for body
copy, `size-adjust` on every fallback metric. A three-second block on body text over a slow VPN is
worse than a fallback face.

## INP: the metric design can only influence, never promise

INP is "a stable Core Web Vital metric that assesses responsiveness using data from the Event Timing
API" [S3]. Its anatomy: input delay → event handler callbacks → presentation delay, with the metric
reporting latency until "the browser is next able to paint a frame" [S3]. **The visual response to
a click is the whole measure** — a filter that applies on the client is measured *after* paint, so a
fast-feeling result is not a fast INP.

**INP is a field metric.** "The best way to measure your website's INP is by gathering metrics from
actual users in the field", and field RUM identifies the specific responsible interaction, its
lifecycle position, and its type (click, keypress, tap) [S3]. In-page the value is the **98th
percentile** across all interactions on unload [S3], and events **below 104 milliseconds are not
reported** by default [S3]. Chrome usage data shows **90% of a user's time on a page is spent after
it loads** [S3] — responsiveness is a whole-session property.

**TBT is the lab proxy, with web.dev's caveat:** "Total Blocking Time (TBT) may be a reasonable proxy
metric for INP, but **it's not a substitute for INP in and of itself**" [S3]. The documented lab
strategy is to follow common user flows and interact "as it loads—when the main thread is often
busiest" [S3].

What design controls here: **every async response needs a synchronous visual acknowledgement**,
because INP measures to the next paint — a button that awaits a fetch before changing anything has
an INP floor equal to the round trip. Interaction cost is **per-event**, and a console generates
many candidates: row click, row checkbox, row action menu, filter change, sort, pagination.
**Charts are the usual offender** — a tile that synchronously lays out thousands of points inside
the click handler owns the worst interaction on the page.

## LCP: which element is yours

LCP "reports the render time of the largest image, text block, or video visible in the viewport,
relative to when the user first navigated to the page" [S2]. Candidates per the LCP API as reported
by web.dev [S2]: `<img>`; `<image>` inside `<svg>`; `<video>` (poster or first frame, whichever is
earlier); an element with a background image loaded via `url()` (not a gradient); and **block-level
elements containing text nodes or inline-level children**.

Exclusions that matter here: elements at `opacity: 0`, elements that **cover the full viewport**
(treated as background), and **low-entropy placeholder images or skeletons** [S2]. That last one is
the design consequence worth having: a dimensionally correct skeleton is *excluded* from LCP, which
is what you want — the shell does not win the LCP element and the real content does.

Margins, padding and borders are not counted in LCP size, and for text only "the smallest rectangle
that can contain all text nodes" [S2]. So the LCP element on a route is most likely the **page
heading plus its first paragraph**, or a **lead chart image** — not a table. A webfont-gated heading
puts LCP on the font critical path.

## Animating, code splitting, skipping render work

**Properties that cost layout.** "Some values, such as `box-shadow` and `box-sizing`, trigger
re-layout, paint, and composite. **Changing the top and left properties also cause layout shifts,
even when the element being moved is on its own layer. Avoid animating using these properties.**"
[S4] The positive form: "**Stick to transform and opacity changes for your animations.**" — "Today
there are only two properties for which that is true - transforms and opacity" [S7]. Promote
sparingly — `.moving-element { will-change: transform; }`, with the warning that "layers require
memory and management" [S7] — and use the **FLIP principle** to remap expensive animations onto
transforms and opacity [S7]. Note `will-change` can name a property, `scroll-position`, or `contents`
[S8], and MDN warns that a transform creates a stacking context and a containing block for
positioned descendants [S9] — which is why an animated parent silently breaks `position: fixed`
children.

**Not found:** any primary source stating that `width`, `height`, `margin`, `padding` or `top`/`left`
"cause layout" as a blanket rule. The sources here name `top`, `left`, `box-shadow`, `box-sizing`
specifically [S4][S7]. A blanket list would need the "High-performance animations" reference that
[S4] itself cites but which was not fetched.

**Code splitting.** "**Split the JavaScript bundle to only send the code needed for the initial
route** when the user loads an application. This minimizes the amount of script that needs to be
parsed and compiled… Popular module bundlers like webpack, Parcel, and Rollup allow you to split your
bundles using **dynamic imports**" [S10]. Raw stakes: "Over 50% of users abandon a website if it
takes longer than 3 seconds to load" [S10]. Two **house rules (judgement, not sourced):** anything
not needed to paint the first screen of a route must not be in its initial bundle (editors, chart
renderers, export/CSV generation, the command-palette index, print styles, locale data, inactive
i18n dictionaries); and deferring is not free if it delays first interaction — web.dev's own example
loads the module *on submit*, not on load [S10], so trigger the split at the user's action and show
the acknowledgement immediately.

**`content-visibility`.** MDN documents `content-visibility: auto` as letting "the user agent skip
an element's rendering work (including layout and painting) until it is needed — which makes the
initial page load much faster" [S11]; it is Baseline-new since September 2024 and fires
`contentvisibilityautostatechange` when rendering work starts or stops being skipped, the hook for
pausing a `<canvas>` chart's animation loop [S11]. **House rule (judgement, not sourced):** correct
for below-the-fold regions of a long settings page and collapsed panes; **not** for a virtualised
list's rendered window or anything whose size must be known for scrollbar stability — the skipped
subtree has no layout, so reserving space for it defeats the purpose and getting it wrong produces
exactly the shift CLS measures.

## Virtualisation

web.dev's framing: "Super large tables and lists can slow down your site's performance
significantly," defining the technique as "**List virtualization, or 'windowing', is the concept of
only rendering what is visible to the user**" — "The number of elements that are rendered at first
is a very small subset of the entire list and the 'window' of visible content moves when the user
continues to scroll" [S12]. Recycled nodes keep the rendered element count tied to window size
[S12].

Virtualisation is a CLS *and* an accessibility problem. **CLS:** the scroll container needs an
explicit height or the window grows as you scroll — `FixedSizeList` takes `height`, `width`,
`itemSize` and `itemCount` explicitly for exactly this reason [S12]. **Accessibility:** windowing
removes nodes from the accessibility tree, so a virtualised table needs a non-windowed accessible
representation plus roving tabindex (see `accessibility-web.md`, SC 2.4.3) rather than Tab-per-row.

**Not found:** a sourced numeric threshold — "virtualise above N rows" or "above N thousand DOM
nodes". web.dev describes the technique and when it is needed ("many rows", "super large tables")
without publishing a figure [S12]. A house number needs this product's own measurement, not a
citation.

## Field vs lab

| Question | Field (RUM/CrUX) | Lab (Lighthouse, DevTools) |
|---|---|---|
| Over the gate for real users? | Yes — p75, segmented mobile/desktop [S1] | No |
| Which interaction caused the worst INP? | Yes — with type and lifecycle context [S3] | No — TBT is a proxy only [S3] |
| Why is INP bad? | Context only | Reproduce manually: flows, interact during load [S3] |
| Is LCP slow because of TTFB? | Yes [S2] | Partly — lab misses real TTFB [S2] |
| Did a specific layout shift happen? | Yes, with the shifted elements [S4] | Only for what the trace captured |

**House rule (judgement, not sourced):** a console cannot be declared performant on lab numbers
alone. The gate is field p75 for all three metrics on the five heaviest routes, segmented by device
class, with a lab budget (TBT, throttled LCP) as the CI regression tripwire.

## Design-review checklist

- [ ] Every async region declares its final size; the skeleton matches the resolved geometry.
- [ ] Empty state has a reserved height, not a collapse to zero.
- [ ] Every `<img>`/`<video>` has `width`/`height`, or a reserving `aspect-ratio`.
- [ ] `font-display` set deliberately; fallbacks carry `size-adjust`; `@font-face` sets are `unicode-range`-subset.
- [ ] No transition or keyframe on `top`, `left`, `width`, `height`, `margin`, `padding`.
- [ ] Every click has a synchronous visual response before any await.
- [ ] Anything below-the-fold in the route is dynamically imported.
- [ ] Virtualised containers declare an explicit height.
- [ ] No intended LCP candidate is `opacity: 0`, full-viewport, or a low-entropy placeholder.

## Sources

All web.dev and MDN pages below, **accessed 2026-10-05**. Brackets give the claim each supports.

- **[S1]** https://web.dev/articles/vitals — web.dev (Google), *Web Vitals*, updated 31 Oct 2024. [CWV set; LCP ≤2.5 s, INP ≤200 ms, CLS ≤0.1; p75 segmented mobile/desktop; pass requires all three]
- **[S2]** https://web.dev/articles/lcp — web.dev (Google), *Largest Contentful Paint (LCP)*, updated 4 Sep 2025. [LCP candidate elements; exclusions (opacity 0, full-viewport, low-entropy placeholders); size rules; TTFB included, causing field/lab divergence]
- **[S3]** https://web.dev/articles/inp — web.dev (Google), *Interaction to Next Paint (INP)*, updated 2 Sep 2025. [Event Timing API; 200 ms/500 ms; 90% of time post-load; 98th percentile in-page; 104 ms floor; field-only; TBT caveat; manual lab diagnosis]
- **[S4]** https://web.dev/articles/optimize-cls — web.dev (Google), *Optimize Cumulative Layout Shift*. [0.1 good / >0.25 poor; four common causes; reserve space with placeholder or skeleton; fixed-size container; 500 ms post-input exemption; width/height or aspect-ratio; `top`/`left` cause shifts]
- **[S5]** https://web.dev/articles/font-best-practices — web.dev (Google), *Best practices for fonts*, updated 4 Oct 2022. [Chromium/Firefox 3 s block, Safari indefinite; five `font-display` values with periods; `swap` branding / `optional` body; `size-adjust`; `unicode-range`]
- **[S6]** https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display — MDN Web Docs, *font-display descriptor*, Baseline since Jan 2020. [the three periods and five keyword values]
- **[S7]** https://web.dev/articles/stick-to-compositor-only-properties-and-manage-layer-count — web.dev (Google), *Stick to compositor-only properties…*. [only `transform`/`opacity`; `will-change: transform`; layer memory cost; FLIP remapping]
- **[S8]** https://developer.mozilla.org/en-US/docs/Web/CSS/will-change — MDN Web Docs, *will-change*, Baseline since Jan 2020. [`auto`, `scroll-position`, `contents`, `<custom-ident>`]
- **[S9]** https://developer.mozilla.org/en-US/docs/Web/CSS/transform — MDN Web Docs, *transform*, Baseline since Sep 2015. [stacking context and containing block for positioned descendants]
- **[S10]** https://web.dev/articles/reduce-javascript-payloads-with-code-splitting — web.dev (Google), *Reduce JavaScript payloads with code splitting*. [>50% abandonment past 3 s; split to initial route; dynamic `import()`]
- **[S11]** https://developer.mozilla.org/en-US/docs/Web/CSS/content-visibility — MDN Web Docs, *content-visibility*, Baseline-new since Sep 2024. [skips layout and paint until needed; `contentvisibilityautostatechange`]
- **[S12]** https://web.dev/articles/virtualize-long-lists-react-window — web.dev (Google), *Virtualize large lists with react-window*. [windowing definition and node recycling; `FixedSizeList` props]