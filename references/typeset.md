# Typeset — type ramp, measure, leading, numerals

Enhance command. `typeset` fixes the type system of an existing surface: sizes, leading, measure,
numerals, families. It never picks the direction (`screen.md`) and never sets a density class —
it applies the one already declared.

## 1. Fixed stepped sizes. Fluid type is a marketing technique.

**Inside a logged-in product surface, no font size is a function of viewport width.** `clamp()`,
`vw`, and `vh` inside a `font-size` are defects here, not techniques. This is Carbon's own split:
the **productive** type set ships inside product with "a base type size of 14px" while the
**expressive** set is 16px; productive headings are fixed — "Product pages have a higher density
of information housed inside containers for space efficiency, and in these situations fixed type
styles are a must" — and "**The type size remains constant regardless of break point**." The
expressive set's remaining headings are the fluid ones, and Carbon says "**Do not use these styles
inside a container**."

If a size must differ between a wide table and a narrow drawer, that is a **density class** change
or a container query on a container token — not interpolation.

The consequence of mixing is a hierarchy failure, not a style choice: "People unconsciously use
type size as a signal of hierarchy… **Mixing type styles within a component could jumble the
hierarchy and create confusion**" (Carbon, *Typography — style strategies*).

## 2. Per-class base sizes

The class is already declared; these are its base sizes. The full table — including row height and
measure — is `craft-floor.md`, and it is authoritative.

| Class | Surfaces | Base body | Row height | Measure |
|---|---|---|---|---|
| **Focused** | Auth, onboarding, checkout, single-form flows, settings detail | 16px | — | 60–70ch, centered |
| **Standard** | Project home, card+list feeds, record detail | 14–15px | 40–44px | 65–80ch |
| **Dense** | Data tables, admin consoles, observability, logs, trading, IDE-like | 12–13px | 28–32px | full-width |

Carrying the class rules into type:

- **[F]** 16px base. Never below 14px for anything a first-time user must read.
- **[S]** 14–15px base; 13px for secondary metadata only.
- **[D]** 12–13px permitted **for data surfaces only** — tables, logs, metrics, code. Prose inside
  a dense screen still steps up to 14px+. Dense is not a licence to make help text unreadable.
- **Never justify body text.** WCAG 2.2 SC 1.4.8 requires non-justified text; Carbon's `body-01`
  is "always left-aligned."

## 3. The ramp: stepped, coupled leading, two weights

Fixed steps plus the code face, calibrated against Carbon's productive set (`label-01` 12/16,
`body-compact-01` 14/18, `body-01` 14/20, `heading-compact-01` 14/18 at 600, `code-01` 12):

| Token | Size | Line height | Weight | Product use |
|---|---|---|---|---|
| `--text-xs` | 12px | 16px | 400 | Field labels, helper text, error text, table micro-labels, badges |
| `--text-sm` | 14px | 20px | 400 | Default UI body: table cells, list rows, nav items, button labels |
| `--text-md` | 16px | 24px | 400 | Record-page field values, settings prose, Focused-class form body |
| `--text-lg` | 20px | 28px | 600 | Page title, record name, section heading |
| `--text-mono` | 12px | 16px | 400 | IDs, hashes, code, raw values, Dense timestamps |

- **Line height couples to size, never global.** 12/16 = 1.33, 14/20 = 1.43, 16/24 = 1.5,
  20/28 = 1.4. Never ship a bare `line-height: 1.5` on everything.
- **Two functional weights: 400 and 600.** Carbon: semibold "is ideal for section headers, but
  should not be used for long text." Three weights max.
- **Pair compact heading with compact body.** A 14px semibold heading with 16px body destroys the
  weight contrast that made it a heading.
- Tracking: negative on large display, slightly positive on small uppercase labels, default on
  body. Wide letter spacing on body text is its own defect class.
- One family is the default — `system-ui`, which makes zero network requests for the primary face.
  A second family only when it earns the contrast: a monospace for code, identifiers, and figures.

## 4. Tabular numerals

**Every comparable figure gets `font-variant-numeric: tabular-nums`.** MDN: `tabular-nums`
activates "the set of figures where numbers are all of the same size, **allowing them to be
easily aligned like in tables**" — it is the OpenType `tnum` feature, not a CSS-generated effect.

```css
.numeric { font-variant-numeric: tabular-nums; }
```

Applies to: every numeric table cell, currency, counts, quantities, percentages, IDs, hashes,
version strings, and metric-tile values. Does not apply to prose paragraphs, dates in running
text, or badges that never repeat. Because `tnum` is a font feature and system fonts vary, **verify
the rendered digit widths** rather than trusting the declaration; render `1 8 111 0` and confirm
equal width. Where `0` and `O` sit in adjacent columns (SKUs, hostnames, hex IDs), apply
`slashed-zero` to the mono token, not globally.

Pair with alignment: numerics right-aligned on the decimal, text left-aligned, never a centred
numeric column (`craft-floor.md`).

## 5. Measure

Cap prose at **65–80 characters**. WCAG 2.2 SC 1.4.8 Visual Presentation (AAA) requires a mechanism
for "Width is no more than 80 characters or glyphs (40 if CJK)," plus non-justified text, "Line
spacing (leading) is at least space-and-a-half within paragraphs," and paragraph spacing "at least
1.5 times larger than the line spacing."

- Focused: 60–70ch, centred. Standard: 65–80ch. Dense: full-width — the constraint does not apply
  to grids and tables.
- A table cell is one line by definition; `max-width: 70ch` on a cell is a defect.
- Use `text-wrap: balance` on page titles and record names only, `pretty` on Focused prose only.
  Never globally: browsers cap the line count (six lines in Chromium, ten in Firefox) and fall back
  to `wrap`, so a global rule costs layout time and changes nothing past that.

## 6. Verify

- Grep for `clamp(`, `vw`, `vh` inside any `font-size`. Every hit in a product surface is a finding.
- Confirm no rule sets `font-size` without a paired `line-height` token.
- Render mixed-width numbers and confirm equal digit widths; check `0` vs `O` in ID/SKU columns.
- Measure prose line length at the widest breakpoint. Over 80ch is a finding.
- Confirm no `text-align: justify` anywhere.
- Count distinct weights in use. More than three is a finding.
- Tab through on a slow 3G profile with the cache cleared; watch for invisible text and table reflow.

## 7. Detector advisories for this command

`tiny-interface-text` is **advisory in Dense**, where 12–13px data type is legal, and a **failure
in Focused and Standard** — the detector reads "increase the size so people can read without
zooming," which is correct in a Focused form and wrong in a Dense console.
`line-length-too-long` is advisory in Dense. `justified-text` and `tight-leading` fail at every
class. Mechanics and the full table: `detector-integration.md`, `craft-floor.md`.

## Exit criteria

No viewport-derived type size anywhere; every step carries its own line-height token; two weights
maximum; numerals tabular and verified at rendered widths; measure within class; no justified text;
`clamp()`/`vw` grep clean.

## Not found

- **A required font-size step count, a minimum product body size, or a required optical-size axis.**
  No primary source sets these. The five-step ramp, the two-weight discipline, and the 65–80ch
  target are house rules calibrated against Carbon's productive set and SC 1.4.8's 80-character
  ceiling. Settled by: legibility testing with real users plus a `DESIGN.md` decision.
- **A normative minimum font size for Dense surfaces.** WCAG sets contrast and reflow, not type
  size; the 12–13px Dense range is house judgement and the project's `DESIGN.md` overrides it.

## Sources

Primary reference: `typography-web.md` (the full ramp, `font-variant-numeric`, `font-display`
periods, `font-optical-sizing`, `font-size-adjust`, measure and `text-wrap`). Supporting:
`information-density.md` (class mechanics, row heights), `craft-floor.md` (per-class rules),
`metrics-stat-tiles.md`, `data-tables.md`.

External pages cited above, all previously opened by this skill:

- Type sets (productive 14px / expressive 16px; productive headings fixed, expressive fluid; "do not
  use [fluid] inside a container"; compact heading pairs with compact body; `body-01` always
  left-aligned) · Typography — style strategies ("Mixing type styles within a component could
  jumble the hierarchy") · Typography — overview (semibold for section headers, not long text) —
  Carbon Design System (IBM). https://carbondesignsystem.com/elements/typography/type-sets/ —
  accessed 2026-10-05.
- `font-variant-numeric` (`tabular-nums` aligns figures like in tables; `tnum`; `slashed-zero`) ·
  `text-wrap` (`balance` limited to six lines in Chromium / ten in Firefox) ·
  `<generic-family>` (`system-ui` not for typesetting large paragraphs) · `font-display` /
  `FontFace.display` (three-period timeline) — MDN.
  https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variant-numeric ·
  https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/text-wrap — accessed 2026-10-05.
- Understanding SC 1.4.8 Visual Presentation (≤80 characters or glyphs, 40 if CJK; non-justified;
  leading ≥ space-and-a-half; paragraph spacing ≥1.5×) — W3C WAI.
  https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html — accessed 2026-10-05.
- Web Vitals / fonts (swapping impacts CLS; preload + `font-display: optional` removes jank) —
  web.dev. https://web.dev/articles/font-best-practices — accessed 2026-10-05.

**House process, not sourced fact:** the five-token product ramp and its line-height pairings, the
400/600 two-weight discipline, the per-class type table's application order, the verification
sequence in step 6, and the density-to-finding mapping in step 7. The Carbon token values, the
`font-variant-numeric` mechanism, and SC 1.4.8 are cited.