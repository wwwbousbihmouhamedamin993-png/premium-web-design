# Internationalisation and RTL

Applies to: any product surface with more than one locale, and any surface that will get one. RTL
is not a translation task — it is a layout-task, and it is cheapest to get right by never writing
`left`/`right` in the first place.

## The string expansion budget

This is the number most teams guess at and few source. W3C's *Text size in translation* article
republishes IBM's *Guidelines to design global solutions* expected expansion rates for English into
European languages [S1]:

| Characters in the English source | Average expected expansion |
|---|---|
| Up to 10 | **200–300%** |
| 11–20 | 180–200% |
| 21–30 | 160–180% |
| 31–50 | 140–160% |
| 51–70 | 150–170% |
| Over 70 | **130%** |

Read that table twice. **Short strings expand hardest.** "Export" is in the top row at up to 300% —
and that is exactly the length of a button label, a column header, and a chart legend. W3C's worked
example: the Flickr string "392 views" translated into Italian "visualizzazioni" has a ratio of
**3** [S1]. The layout guidance: "the more flexibly you can design your layout, the better. **Allow
text to reflow and avoid small fixed-width containers or tight squeezes** where possible … Separate
presentation and content, so that font sizes, line heights, etc. can be easily adapted for
translated text" [S1].

**Design consequences for a console (house judgement, not sourced):** never size a button, column
header, or filter chip by its English content — use a minimum inline size generous enough for ~2× the
source label, or size from the translated string set via pseudo-localisation during design; fixed
column widths are the classic failure, so use `min-width` with fluid growth or `table-layout: fixed`
with percentages so a translation redistributes rather than overflows; and reserve label space for
the *longest* supported locale, not the source locale.

**Not found:** an expansion budget sourced for CJK or RTL targets specifically. W3C notes Chinese
and Korean source strings "will typically be longer in the translation than the original", so the
table's direction reverses when English is the target [S1] — but no per-locale budget table exists
beyond this one.

## Pluralisation: a ternary is a bug

English has two cardinal forms; Chinese has one; **Arabic has six** [S2]. English has four ordinal
forms — `th`, `st`, `nd`, `rd` — "while both Chinese and Arabic only have one form for ordinal
numbers" [S2]. CLDR's tags are `zero`, `one`, `two`, `few`, `many`, `other`, where `other` is
"required—general plural form—also used if the language only has a single form" [S3]. CLDR warns
its categories "do not necessarily match the traditional grammatical categories" but are
"determined by changes required in a phrase or sentence if a numeric placeholder changes value"
[S3] — a `few` form is not a noun plural, it is a phrase rewrite.

**Why `count === 1 ? "1 item" : "n items"` fails:** it encodes English's two-form assumption, and
breaks on the parts of English MDN calls out — the plural form may affect **nouns** ("dog"/"dogs",
but not "fish"/"sheep"), **verbs** ("1 dog **is** happy" / "10 dogs **are** happy"), and
**pronouns** ("play with **it**" / "play with **them**") [S2]. A ternary cannot reorder a sentence,
so even a perfect `one`/`other` pair fails the moment the words around the count change.

`Intl.PluralRules.prototype.select()` returns the category tag for a single number;
`selectRange()` for a range [S2]. Baseline widely available since September 2019 [S2].

```js
const form = new Intl.PluralRules(locale).select(count);   // "one" | "other" | "few" | …
label = forms[form].replace("{n}", count);
```

For ordinals, `new Intl.PluralRules("en", { type: "ordinal" }).select(22)` returns `two` for the
`nd` suffix [S2]. **House rule (judgement, not sourced):** any surface shipping to Polish, Arabic,
Russian, Welsh, Irish, Slovenian or Romanian must carry *all six* category keys in its catalogue, even
if some are unreachable in the source language — a missing key falls back to English text mid-page.

ICU's framing of the single-unit rule is the other half: "a message has to be written and translated
as a single unit, typically a string with placeholder syntax for the variable elements. If the
user-visible string were concatenated directly from fragments and formatted elements, then
translators would not be able to rearrange the pieces" [S4]. **Concatenation kills translation** —
`label + " " + count + " " + noun` is untranslatable; `{count, plural, one {# item} other {# items}}`
is not.

## Locale formatters: never build these by hand

| Need | API | Evidence |
|---|---|---|
| Numbers, currency, percent | `Intl.NumberFormat` | `de-DE` EUR → `123.456,79 €`; `ja-JP` JPY → `￥123,457` (no minor unit); `en-IN` at 3 significant digits → `1,23,000` [S5] |
| Dates and times | `Intl.DateTimeFormat` | `en-US` → `12/20/2020`; `["ban","id"]` → `20/12/2020` [S6] |
| Relative time | `Intl.RelativeTimeFormat` | `en` short `format(-1,"day")` → `"1 day ago"`; `es` with `numeric:"auto"`, `format(2,"day")` → `"pasado mañana"` [S7] |
| Locale-aware sorting | `Intl.Collator.prototype.compare` | `de`: `["Z","a","z","ä"]` → `["a","ä","z","Z"]`; `sv` → `["a","z","Z","ä"]` [S8] |

Hard-coded formatting is a defect the sources demonstrate: `de-DE` and `ja-JP` disagree on decimal
separator, group separator, symbol placement, and *whether a currency has a minor unit at all* [S5];
`en-IN` groups as `1,23,000` where `en-US` gives `1,234` [S5]. Two places in a console building a
currency string by hand will disagree on the same page.

**Relative time needs `numeric: "auto"` or it lies.** Spanish with `numeric:"auto"` renders
`format(2,"day")` as "**pasado mañana**" where `numeric:"always"` gives "in 2 days" [S7]. For
yesterday/today/tomorrow columns that is what makes Spanish and Portuguese correct.

**Sorting is not `<` or `>`.** "The results provided by `Intl.Collator.prototype.compare()` vary
between languages. In order to get the sort order of the language used in the user interface of your
application, make sure to specify that language … using the locales argument" [S8]. **So a name
column sorted with default `Array.prototype.sort()` is wrong in every locale, including English** —
it sorts code units, putting `"Z"` before `"a"` [S8]. Column sort must go through a `Collator` built
once per active locale and memoised, not rebuilt per comparison.

## RTL: logical properties, not RTL overrides

The CSS Logical Properties module exists for this: properties "define direction-relative equivalents
to their corresponding physical properties" [S9]. Values that once only accepted `top`, `bottom`,
`left`, `right` "now also accept flow-relative logical values (`block-start`, `block-end`,
`inline-start`, `inline-end`)" [S9]. MDN's stated purpose: "content translated into languages with
different writing modes will be rendered as intended" [S9].

| Physical — do not write | Logical — write this |
|---|---|
| `margin-left`, `padding-right` | `margin-inline-start`, `padding-inline-end` |
| `left: 0`, `right: 0` | `inset-inline-start: 0`, `inset-inline-end: 0` |
| `width`, `height` | `inline-size`, `block-size` |
| `border-left: 1px solid` | `border-inline-start: 1px solid` |
| `border-top-left-radius` | `border-start-start-radius` |
| `text-align: left` | `text-align: start` |

**The one-direction things that must stay physical (house judgement, not sourced):** shadows with an
x-offset, scrollbar gutters (`scrollbar-gutter: stable`), caret position, gradient angles, and
anything driven by `Math.sign()` or a mouse x-coordinate. **Mirroring is not symmetry** —
directional icons (chevron, back arrow, undo, scrubber) must flip; sequence-denoting icons must not.
Logical properties handle the container; icons are a per-asset decision with no sourced rule.
**House rule (judgement):** treat every icon as directional unless it is a glyph (a clock, a
magnifier), and flip with CSS `transform: scaleX(-1)` under `[dir="rtl"]` on the one icon component
rather than shipping two asset sets.

**Direction is inherited, and `dir` is not optional.** If an element has no `dir`, "it generally
inherits the direction of its parent element"; if no ancestor sets one, "the default is
**left-to-right**" [S10]. Omitting `dir` does **not** enable automatic detection [S10] — so
`<html lang="ar">` without `dir="rtl"` renders Arabic in an LTR page.

## Bidirectional text in a data-dense UI

This is where B2B consoles break, because table cells hold **mixed-direction data**: an Arabic
display name beside an email, a Hebrew customer name in an ID, an amount with an Arabic-Indic digit
run.

MDN on `<bdi>`: it "tells the browser's bidirectional algorithm to treat the text it contains in
isolation from its surrounding text. It's particularly useful when a website dynamically inserts some
text and doesn't know the directionality of the text being inserted" [S11]. **Wrap every
user-supplied name cell in `<bdi>`, or set `dir="auto"`.**

`dir="auto"` lets the user agent "determine the base direction from the text, generally using the
first character with a strong directionality (skipping `<bdi>`, `<script>`, `<style>`, `<textarea>`,
and elements with valid `dir` attributes)" [S10], and MDN scopes it precisely: "The `auto` value
should be used for data with an unknown directionality, like **data coming from user input or
external data**" [S10]. For `<textarea>` and `<pre>` the direction is determined per paragraph [S10].
One exception: `<input type="tel">` uses left-to-right direction regardless [S10].

Where the author *does* know the direction and wants to force an embedding, the CSS is
`unicode-bidi`, which with `direction` "determines how bidirectional text in a document is handled",
with values `normal`, `isolate`, `embed`, `bidi-override`, `isolate-override`, `plaintext` [S12].
**Use `isolate`, never `bidi-override`** — override discards the character's own directionality and
is for terminal control sequences, not names. The classic visual bug — a column of emails or URLs in
an RTL page showing its trailing punctuation at the wrong end — is fixed by isolating the value, not
by reversing it.

## Locale-aware data plumbing

- **Store and transport canonically; render with `Intl`.** ISO dates in, `Intl.DateTimeFormat` out;
  major units in integers, `Intl.NumberFormat` out.
- **Native date input already does this.** For `<input type="date">`, "the **displayed** date format
  will differ from the actual value — the displayed date is formatted based on the **locale of the
  user's browser**, but the parsed value is always formatted `yyyy-mm-dd`" [S13]. Let the native
  control do it rather than pairing a localised text field with a hand-built calendar.
- **Time zone and locale are separate axes.** Formatting with `Intl.DateTimeFormat` but no explicit
  `timeZone` renders in the runtime's zone — a silent data-integrity bug in an audit log.
  **House rule (judgement, not sourced):** pass an explicit `timeZone` and label it in the UI for
  audit logs and billing.
- **Personal names.** W3C's diagnosis: "people who create web forms, databases, or ontologies are
  often unaware how different people's names can be in other countries. They build their forms or
  databases in a way that assumes too much on the part of foreign users" [S14] — while explicitly
  declining to prescribe: "This article doesn't provide all the answers – the best answer will vary
  according to the needs of the application" [S14]. So a single "Full name" field is defensible; a
  fixed `First`/`Last`/`Middle` triplet is not. **Not found:** a sourced requirement that B2B admin
  forms use a single unstructured name field — W3C declines to prescribe.
- **Sort the whole table, not just the sorted column.** A locale-collated sort of one column against
  code-unit-sorted others produces a table whose visual order disagrees with its stated sort.

## Checklist

- [ ] No `left`/`right` in any CSS outside a `[dir="…"]`-scoped override; logical properties everywhere else.
- [ ] `dir` set on `<html>` alongside `lang`; `dir="auto"` or `<bdi>` on every user-supplied name cell.
- [ ] `unicode-bidi: isolate`, never `bidi-override`, on forced-direction values.
- [ ] Every count-bearing string uses `Intl.PluralRules`, not a ternary; all six CLDR category keys present in the catalogue.
- [ ] No string concatenation around a placeholder — single-unit message with named arguments.
- [ ] Every number, currency, percent, date, and relative time via `Intl.*`; nothing hand-formatted.
- [ ] Every user-visible sort through a memoised `Intl.Collator` for the active locale.
- [ ] Column headers, buttons, and chips sized for ~2–3× the source string, or pseudo-localised during design.
- [ ] Audit-log and billing timestamps carry an explicit `timeZone` and a visible label.
- [ ] Name fields are not assumed to decompose into first/last.
- [ ] Directional icon set reviewed and marked as mirroring or not.

## Sources

All pages **accessed 2026-10-05**. Brackets give the claim each supports.

- **[S1]** https://www.w3.org/International/articles/article-text-size.en.html — W3C International, *Text size in translation*. [IBM expansion table; Flickr ratio-3 example; reflow and separate-presentation guidance]
- **[S2]** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/PluralRules — MDN, *Intl.PluralRules*, Baseline since Sep 2019. [2/6/1 cardinal forms for English/Arabic/Chinese; four English ordinal forms; six CLDR tags; `select()`/`selectRange()`; effects on nouns, verbs, pronouns]
- **[S3]** https://cldr.unicode.org/index/cldr-spec/plural-rules — Unicode CLDR, *Plural Rules*. [the six tags; `other` as required general form; categories determined by placeholder substitution, not grammar]
- **[S4]** https://unicode-org.github.io/icu/userguide/format_parse/messages/ — Unicode ICU, *Formatting Messages*. [message-as-single-unit rule; concatenation defeats translator rearrangement]
- **[S5]** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat — MDN, *Intl.NumberFormat*, Baseline since Sep 2017. [`de-DE`/`ja-JP`/`en-IN` examples; currency style; `maximumSignificantDigits`]
- **[S6]** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat — MDN, *Intl.DateTimeFormat*, Baseline since Sep 2017. [`en-US` vs `ban`/`id` fallback; `style`; locale arrays]
- **[S7]** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat — MDN, *Intl.RelativeTimeFormat*, Baseline since Sep 2020. [`style`/`numeric`; Spanish `numeric:"auto"` → "pasado mañana"]
- **[S8]** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Collator — MDN, *Intl.Collator*, Baseline since Sep 2017. [`de` vs `sv` sort orders; `caseFirst`; pass the UI language]
- **[S9]** https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values — MDN, *CSS logical properties and values*. [flow-relative equivalents; block/inline axes; writing-mode dependence]
- **[S10]** https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/dir — MDN, *dir global attribute*. [`ltr`/`rtl`/`auto`; first strong character; omission ≠ detection; LTR default; `<input type="tel">` exception]
- **[S11]** https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/bdi — MDN, *bdi element*, Baseline since Jan 2020. [isolate from surrounding bidirectional context; unknown-directionality inserts]
- **[S12]** https://developer.mozilla.org/en-US/docs/Web/CSS/unicode-bidi — MDN, *unicode-bidi*. [interaction with `direction`; the six values]
- **[S13]** https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/date — MDN, *input type="date"*, Baseline since Apr 2021. [display follows browser locale, parsed value always `yyyy-mm-dd`]
- **[S14]** https://www.w3.org/International/questions/qa-personal-names — W3C International, *Personal names around the world*. [name-decomposition assumptions break internationally; explicit refusal to prescribe]