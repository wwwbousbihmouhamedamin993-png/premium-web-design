# Text inputs

Applies to: single-line text capture in settings, checkout, onboarding, admin create/edit, search inputs,
inline table edits.

## Anatomy

Every text input is the same six parts, in this order:

```
  Label            persistent, visible, sentence case, no trailing colon
  Hint             optional; one short sentence; no links
  Error message    appears above the field, only when errored
  Input            the <input> itself
  Counter          optional; below the field; live-updating
  Prefix / suffix  optional; outside the input box
```

"All text inputs must have labels, and in most cases the label should be visible. You should align labels
above the text input they refer to. They should be short, direct and written in sentence case. Do not use
colons at the end of labels." — https://design-system.service.gov.uk/components/text-input/ Hint rules and
error-above/count-below ordering — https://design-system.service.gov.uk/components/character-count/

Wire the accessible name and descriptions explicitly:

```html
<label for="full-name">Full name</label>
<p id="full-name-hint">As it appears on your passport</p>
<input id="full-name" name="fullName" type="text"
       autocomplete="name" aria-describedby="full-name-hint">
```

`aria-describedby` chains **hint then error** when both exist
(https://design-system.service.gov.uk/components/error-summary/ shows
`aria-describedby="full-name-input-error"`; the checkbox example shows `aria-describedby="nationality-hint
nationality-error"`).

## Persistent label vs placeholder-as-label

**Never use a placeholder as the label.** GOV.UK lists three reasons
(https://design-system.service.gov.uk/components/text-input/):

1. "it vanishes when the user starts typing, which can cause problems for users with memory conditions
or when reviewing answers"
2. "not all screen readers read it out"
3. "its browser default styles often do not meet WCAG 2.2 success criterion 1.4.3 Contrast (minimum)"

The same page forbids placeholder text "in place of a label, **or for hints or examples**". A placeholder is
legitimate only for a format *example* when a visible hint does not carry it — and never as the only source
of the field's purpose. One-question-per-page: when a page holds a single question, make the `<label>` the
page heading so screen reader users hear it once; with multiple questions on a page, do not.

## Input types and mobile keyboards

Choose `type` for constraint semantics; choose `inputmode` for the on-screen keyboard. They are independent
and both earn their place.

| `type` | Constraint it adds (MDN) | Violation |
|---|---|---|
| `email` | must be a syntactically valid email address, `username@hostname.tld` | `typeMismatch` |
| `url` | must be an absolute URL per the URL Living Standard | `typeMismatch` |
| `tel`, `password`, `text` | none intrinsic | — |

*(https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation)* MDN cautions: "most input
types don't have intrinsic constraints, as some are barred from constraint validation or have a sanitization
algorithm transforming incorrect values to a correct default." So `type="tel"` gives you a keyboard, not
validation. Do not assume `type` validated your field.

| `inputmode` | Keyboard | Rule |
|---|---|---|
| `numeric` | numeric keypad, no decimal | Whole numbers only. |
| `decimal` | numeric keypad **with** decimal separator | Numbers that may include decimals. |
| *(omitted)* | default text keyboard | When the number may be **negative**. |

GOV.UK, verbatim: "Some devices do not allow users to enter negative values using the on-screen keypad. If
you want to give users the option to enter a negative number, use `input type="text"` without the
`inputmode` attribute." — https://design-system.service.gov.uk/components/text-input/ (guidance changed Jun
2026 per that page's change log).

`spellcheck="false"` for reference numbers, names, email addresses, and identifiers (same page).

Avoid `type="number"` in product forms: GOV.UK links "the problems we discovered with input type='number'".
**Not found:** the specific defects — that GDS blog post at `https://designnotes.blog.gov.uk/` was not
fetched.

## Autocomplete tokens

`autocomplete` meets **WCAG 2.2 SC 1.3.5 Identify Input Purpose** — GOV.UK recommends the attribute for
exactly this reason, e.g. `autocomplete="bday-day"`
(https://design-system.service.gov.uk/components/text-input/).

The value is `off`, `on`, or a space-separated `<token-list>`
(https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/autocomplete).

Groups and their tokens, all from the MDN `autocomplete` reference page:

- **Named group** (first if present): `section-*`
- **Grouping**: `shipping`, `billing`
- **Recipient type**: `home`, `work`, `mobile`, `fax`, `pager`
- **Digital contact**: `tel`, `tel-country-code`, `tel-national`, `tel-area-code`, `tel-local`,
`tel-local-prefix`, `tel-local-suffix`, `tel-extension`, `email`, `impp`
- **Name**: `name`, `honorific-prefix`, `given-name`, `additional-name`, `family-name`,
`honorific-suffix`, `nickname`, `username`
- **Password / auth**: `current-password`, `new-password`, `one-time-code`, `webauthn` (last token)
- **Organisation**: `organization`, `organization-title`
- **Address**: `street-address`, `address-line1`–`3`, `address-level1`–`4`, `country`, `country-name`,
`postal-code`
- **Payment**: `cc-name`, `cc-given-name`, `cc-additional-name`, `cc-family-name`, `cc-number`,
`cc-exp`, `cc-exp-month`, `cc-exp-year`, `cc-csc`, `cc-type`, `transaction-currency`, `transaction-amount`
- **Other**: `language`, `bday`, `bday-day`, `bday-month`, `bday-year`, `sex`, `url`, `photo`

Four rules from that page:

- **Prefer the coarse token.** "Using `name` rather than breaking the name down into its components
is generally preferred because it avoids dealing with the wide diversity of human names and how they are
structured."
- **Disambiguate repeats with a section token.** `autocomplete="shipping postal-code"` vs
`"billing postal-code"` gives distinct values; repeated groups get a `section-*` prefix.
- **Hidden inputs take token lists only.** On `<input type="hidden">`, `on` and `off` are not allowed.
- **MDN explicitly advises against disabling it.** "Users with cognitive disabilities may rely on
autocomplete to recall personal information, and users with motor impairments benefit from reduced typing.
Browsers may also ignore `autocomplete="off"` on login fields to support password managers." Use `off` only
where genuinely necessary — CAPTCHA or one-time-token fields.

## Masking

**Do not mask.** Masked inputs break paste, produce impossible cursors, and reject valid input. The
alternative GOV.UK prescribes is acceptance, not restriction: "accepting information in different formats,
as long as it's not ambiguous", ignoring "unwanted characters" users pasted in by accident or dictated
(https://design-system.service.gov.uk/patterns/validation/).

Fixed-width inputs are the sanctioned way to signal expected length *without* blocking other input: use them
"for content that has a specific, known length. Postcode inputs should be postcode-sized, phone number
inputs should be phone number-sized." Use width-override classes when the field should be fluid
(https://design-system.service.gov.uk/components/text-input/).

Prefixes and suffixes have one hard rule: **"Do not rely on prefixes or suffixes alone, because screen
readers will not read them out."** Say the unit in the label or hint too — e.g. label "Cost, in pounds" with
a `£` prefix. Also: "Some users have been observed clicking on prefixes, on the assumption that this would
do something" — don't make the affix look like a control.

## Character counters

Test without one first. GOV.UK: "Only use the character count component when there is a good reason for
limiting the number of characters users can enter" — evidence users will over-enter, or a legal/technical
limit (https://design-system.service.gov.uk/components/character-count/).

**The counter does not restrict input.** "The user can enter more than the character limit, but are told
they've entered too many characters. This lets them type or copy and paste their full answer, then edit it
down." This is why it is the one place where live validation is defensible.

| Attribute | Effect |
|---|---|
| `data-maxlength="200"` | character limit |
| `data-maxwords="150"` | word limit — often more useful for long prose |
| `data-threshold="85"` | reveal the count only past 85% of the limit |
| *(no JS)* | a static message still states the limit |

Placement is load-bearing: the count goes **below** the textarea, "clearly separate from any hint text or
error message above the textarea", and below the fold it stays visible when the user scrolls to submit.

The error border is deliberately asymmetric: "The input shows a red border only when the user tries to enter
more than the character limit. If the number of characters is within the limit, the input does not show this
border even when there's been an error. We felt it might cause the user difficulty if the border disappeared
once they started typing."

Accessibility: sighted users see the count update as they type; screen reader users "hear the count
announcement when they stop typing". When the limit is likely to bite, set it **higher** than most users
need.

Known issue to carry into review: the component "counts some characters as multiple characters — for
example, emojis and some non-Latin characters."

## Copy/paste tolerance

Non-negotiable. GOV.UK: "Users often need to copy and paste information into a text input, so do not stop
them from doing this" (https://design-system.service.gov.uk/components/text-input/). The consequences are
stated as reasons:

- `maxlength` gives no feedback that text is truncated — "especially true where the text has been
copied and pasted from elsewhere. This can cause users to accidentally provide incorrect or incomplete
information."
- A restrictive maximum "can stop users from formatting information in their usual way. For example,
putting spaces in a postcode or commas in a large number."
- "Some assistive technologies do not tell users if an input has a `maxlength` set or if the user has
passed the limit. Voice control software may insert additional spaces into the input."

Therefore: **do not use `maxlength` on product fields.** If a technical limit exists, state it in the hint,
permit more input, and only error if the value is still over the limit *after normalisation* — then use the
character count component. MDN adds that `maxlength` and `minlength` "are only checked on user-provided
input. They are not checked if a value is set programmatically"
(https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation).

## Sources

- Text input — GOV.UK Design System — https://design-system.service.gov.uk/components/text-input/ — accessed 2026-10-05
- Character count — GOV.UK Design System — https://design-system.service.gov.uk/components/character-count/ — accessed 2026-10-05
- Help users to recover from validation errors — GOV.UK Design System — https://design-system.service.gov.uk/patterns/validation/ — accessed 2026-10-05
- Error summary — GOV.UK Design System — https://design-system.service.gov.uk/components/error-summary/ — accessed 2026-10-05
- `autocomplete` — HTML attribute — MDN Web Docs — https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/autocomplete — accessed 2026-10-05
- Using HTML form validation and the Constraint Validation API — MDN Web Docs — https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation — accessed 2026-10-05
