# Forms & validation

Applies to: every form in a logged-in product — settings saves, onboarding, checkout, admin create/edit,
inline row edits.

## The baseline: validate on submit, never on blur

GOV.UK is unambiguous and it is the strongest available evidence on this, because the pattern has been used
across UK government services "on a number of services over an extended period of time"
(https://design-system.service.gov.uk/patterns/validation/).

> Do not validate when the user moves away from a field. Wait until they try to move to the next
> part of the service — usually by clicking the 'continue' or 'submit' button at the bottom of the
> page.

> Generally speaking, avoid validating the information in a field before the user has finished
> entering it. This sort of validation can cause problems — especially for users who type more
> slowly. *(both from GOV.UK, validation pattern)*

The single documented exception is the character count, which errors **as the user exceeds the limit**
rather than on submit, and only because "it's important that users do not spend time and effort writing out
a response that turns out to be too long"
(https://design-system.service.gov.uk/components/character-count/).

| Trigger | Verdict | Source |
|---|---|---|
| On blur / on focus loss | Rejected as default. Only add with research showing it solves more problems than it causes. | GOV.UK validation pattern |
| On every keystroke (`input`) | Rejected. Charcount is the one carve-out. | GOV.UK character count |
| On change (`change`, fires on blur) | Equivalent to blur for validation purposes — same trap. | — |
| On submit, validate everything | **The default.** Validate every field, show all errors at once. | GOV.UK validation pattern |
| After a failed submit, revalidate on input for that field | Correct. Once a field has errored, clear the error as they fix it. | GOV.UK character count (border stays) |

**Never validate a field the user has not left.** A red border appearing mid-word is the single most
reliable way to teach a user to ignore your error styling.

## The error summary pattern

GOV.UK states: **"Always show an error summary when there is a validation error, even if there's only
one."** You must (https://design-system.service.gov.uk/components/error-summary/):

1. Move keyboard focus to the error summary — govuk-frontend's JS does this automatically.
2. Include the heading **"There is a problem"**.
3. Link to each answer that has a validation error.
4. Word the summary messages **identically** to the inline messages beside each input.

Structure: `role="alert"` sits on a **nested** div, not the component root. GOV.UK Frontend v4.4.0 moved it
there after a JAWS failure where the whole summary was not read
(https://design-system.service.gov.uk/components/error-summary/).

Placement: "Put the error summary at the top of the `main` container. If your page includes breadcrumbs or a
back link, place it below these, but above the `<h1>`." Same page.

Also prepend **`Error: `** to the `<title>` so screen readers announce it immediately
(https://design-system.service.gov.uk/patterns/validation/).

### Where each summary link points

This is a checkable rule and a common bug source.

| Answer shape | Link target |
|---|---|
| Single field (text input, textarea, select, file upload, charcount) | that field's `id` |
| Multi-field group (day / month / year) | **the first field that contains an error** |
| Multi-field group, error location unknown | the first field |
| Radio or checkbox group | the first radio or checkbox |

*(all four from https://design-system.service.gov.uk/components/error-summary/)*

## Inline messages, not summaries alone

An error summary is an index, never the message itself. Every errored field also gets an error message
component **above** the field; the character count message sits **below** the field so the two never collide
(https://design-system.service.gov.uk/components/error-summary/, /components/character-count/).

Write each message to:
- **Match the label.** Error messages "should directly include language from the question or
fieldset legend" (https://design-system.service.gov.uk/components/error-message/).
- **Be clear and concise** — what went wrong and how to fix it, plain English, positive language.
- **Be consistent** — same string in the summary and inline.
- **Be specific per state.** "Make sure errors follow GOV.UK guidance … and have specific error
messages for specific error states."

Numeric templates worth copying verbatim (https://design-system.service.gov.uk/components/text-input/):
`Hours worked a week must be a whole number, like 30` · `must be 16 or more` · `must be 99 or fewer` · `must
be between 16 and 99` · `must include pence, like 123.45 or 156.00`.

## Turning off native HTML5 validation

GOV.UK instructs: add **`novalidate`** to the `<form>`, and **do not add `required`** to input fields.
Reasons given: the visual style, placement and content of HTML5 error messages "cannot be made consistent
with the GOV.UK Design System", and the GOV.UK error message + summary components are known accessible
(https://design-system.service.gov.uk/patterns/validation/).

MDN confirms the mechanism (https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation):

- `checkValidity()` = **static** validation. `reportValidity()` or submitting = **interactive**.
- "If the `novalidate` attribute is set on the `<form>` element, interactive validation of the
constraints doesn't happen."
- `form.submit()` does **not** trigger validation. Call `click()` on a submit button instead.
- `minlength` / `maxlength` are only checked on user-provided input, not programmatic values.

GOV.UK explicitly flags the unresolved case: "We'd like to expand the guidance … We'd also like to know
about any research into whether not adding `required` to form fields causes problems for screen reader
users." If you remove `required`, verify this yourself.

## Server-side validation is not optional

> You'll always need to carry out server side validation, even if you use client side validation …
> the user can bypass client side validation, or JavaScript can fail to load.

MDN gives the same warning with three concrete bypasses: devtools edits, hand-crafted HTTP requests, and
programmatic value setting (https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation).
Server rules must be consistent with client rules — GOV.UK notes "carrying out both kinds of validation
means you have to check their rules do not conflict."

Always validate server-side. Build the error summary **from the server response**, not from a client-side
guess.

**Disabling submit until valid — Not found:** no primary source consulted addresses it. What would settle
it: documented guidance from a design system covering pre-submit gating. GOV.UK's pattern is
submit-always-then-validate, and its evidence base argues against pre-emptive gating. Disabling the submit
button is defensible only where a server-side invariant exists (e.g. a required payment token) — and even
then, prefer allowing the click and returning a summary error.

## Validation rules worth copying

Validate (GOV.UK validation pattern):

- information that **cannot be correct** (month `13`)
- information **too ambiguous** to use
- **missing** required information

Do *not* error on (same page):

- harmless formatting variance — postcodes with or without spaces, names with apostrophes or
diacritics
- **unwanted characters**: ignore rather than reject. "You should ignore unwanted characters entered …
as part of numbers and codes, such as postcodes or card details … before or after an answer, as users might
have copied and pasted them in by accident … by dictation software"
- a prefix/suffix the user typed into a field that already shows one: "Allow for this in your
validation and do not show an error" (https://design-system.service.gov.uk/components/text-input/)

This last rule is the difference between a validation layer and a hostility generator. Reject only what you
cannot use.

## Multi-step form state

**Sequential, fixed order → step by step, one question per screen.** Reserve the task list for genuinely
non-sequential work. GOV.UK: use the task list only when users "do not want to, or cannot, complete all the
tasks in one sitting" or "need to be able to choose the order they complete the tasks in", and do not use it
"for a long service that needs to be completed in a specific order"
(https://design-system.service.gov.uk/components/task-list/). Try to simplify the flow first. Do not use the
task list to show answers — that is a Summary list.

**State model.** Keep per step: `values`, `touched`, `errors`, `submitAttempted`. Rules that follow from the
baseline above:

- Persist values across steps — re-show the page "with the form fields as the user filled them in" so
users "avoid re-entering information".
- Never clear a step's values on validation failure.
- Mark a step visited before showing its errors; never show errors for a step the user has not reached
or submitted.
- Persist progress server-side when the journey spans sessions — GOV.UK points to "letting users save
their progress, and then … continue where they left off".
- Re-enter the step at the first field with an error, matching the summary-link rule above.

**One question per page** is GOV.UK's default, and it drives a labelling rule that repeats across
components: when a page holds a single question, make the `<label>` or `<legend>` the page heading so screen
reader users hear the question once (https://design-system.service.gov.uk/patterns/question-pages/). With
multiple questions on a page, do not.

## Pre-submit rules worth reusing

- Order radio and checkbox options alphabetically by default; most-to-least common only where clearly
better, and for radios "with extreme caution as it can reinforce bias"
(https://design-system.service.gov.uk/components/radios/).
- **Never pre-select** radios or checkboxes in a question — it makes it "more likely that users will …
submit the wrong answer". Pre-selection *is* correct for settings selects
(https://design-system.service.gov.uk/components/select/).
- Conditional reveal (`data-aria-controls`) may only reveal **questions**, never non-question content,
and should stay simple. Known WCAG 2.2 SC 4.1.2 gap: "Users are not always notified when a conditionally
revealed question is shown or hidden" (https://design-system.service.gov.uk/components/checkboxes/). Log a
4.1.2 audit result either way.

## Sources

- Help users to recover from validation errors — GOV.UK Design System — https://design-system.service.gov.uk/patterns/validation/ — accessed 2026-10-05
- Error summary — GOV.UK Design System — https://design-system.service.gov.uk/components/error-summary/ — accessed 2026-10-05
- Error message — GOV.UK Design System — https://design-system.service.gov.uk/components/error-message/ — accessed 2026-10-05
- Character count — GOV.UK Design System — https://design-system.service.gov.uk/components/character-count/ — accessed 2026-10-05
- Text input — GOV.UK Design System — https://design-system.service.gov.uk/components/text-input/ — accessed 2026-10-05
- Checkboxes — GOV.UK Design System — https://design-system.service.gov.uk/components/checkboxes/ — accessed 2026-10-05
- Radios — GOV.UK Design System — https://design-system.service.gov.uk/components/radios/ — accessed 2026-10-05
- Select — GOV.UK Design System — https://design-system.service.gov.uk/components/select/ — accessed 2026-10-05
- Task list — GOV.UK Design System — https://design-system.service.gov.uk/components/task-list/ — accessed 2026-10-05
- Step by step navigation — GOV.UK Design System — https://design-system.service.gov.uk/patterns/step-by-step-navigation/ — accessed 2026-10-05
- Using HTML form validation and the Constraint Validation API — MDN Web Docs — https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation — accessed 2026-10-05
