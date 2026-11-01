# Date & time pickers

Applies to: scheduling surfaces, billing cycles, trial end dates, audit filters, reminder fields,
timezone-crossing products.

## Choose the control by what the user knows

GOV.UK's dates pattern is the clearest statement of this decision
(https://design-system.service.gov.uk/patterns/dates/). It names four date types and then says: "The way you
should ask users for dates depends on the types of date you're asking for."

| Date type | Control | Why |
|---|---|---|
| Memorable (DOB, marriage) | 3 text fields: day / month / year | user knows it |
| From a document or card | Fields matching the **original's format** | "This makes it easier to copy the date across accurately" |
| Approximate ("December 2017") | Year / month granularity only | user doesn't know the day |
| Relative ("4 days from today", "1 day before") | Text or select | user thinks in deltas |

And the calendar, which is the one most product surfaces get wrong by default:

> "Only use a calendar control if users need to:
> - pick a date in the near future or recent past
> - know the day of the week, or the week of the month, as well as the date
> - be able to see dates in relation to other dates
>
> Never make a calendar control that depends on JavaScript as the only input option. Allow users to
> enter the date into a text input as well as use the control."

*(https://design-system.service.gov.uk/patterns/dates/)*

The JAWS-and-calendar consequence: a calendar for a memorable date like a date of birth is a
keyboard-and-screen-reader maze. Its component guidance is explicit — "Use the date input component when
you're asking users for a date they'll already know, or can look up **without using a calendar**. Do not use
the date input component if users are unlikely to know the exact date"
(https://design-system.service.gov.uk/components/date-input/).

## Date vs datetime vs time vs range

| Need | Control | Verified constraints |
|---|---|---|
| A calendar day | 3 fields (`type="text"`, `inputmode="numeric"`), `type="date"` if native is acceptable | `min`/`max` accept a date; `step` counts **days** |
| A day + wall-clock time | `type="datetime-local"` | `min`/`max` accept a date and time; `step` counts **seconds** |
| Time only | `type="time"` | `min`/`max` accept a time; `step` counts **seconds** |
| A span | two independent date inputs | — |

Constraint table from MDN (https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation):

| Attribute | Input types | Violation |
|---|---|---|
| `min` / `max` | `date`, `month`, `week`, `datetime-local`, `time` | `rangeUnderflow` / `rangeOverflow` |
| `step` | `date` = days · `month` = months · `week` = weeks · `datetime-local`/`time` = seconds | `stepMismatch` |

`step` on `datetime-local` counting **seconds** is the trap: a naive `step="3600"` looks like hours but is
expressed in seconds and interacts with `min`.

GOV.UK's date input uses plain text inputs with `inputmode="numeric"` rather than `type="date"`, and GOV.UK
Frontend v4.1.0 "Removed `pattern="[0-9]*"` from input elements"
(https://design-system.service.gov.uk/components/date-input/).

**Why 3 fields, not one field with a placeholder:** the day/month/year split lets a user enter what they
know and leave the rest. Error summary links point at "the first field that contains an error"
(https://design-system.service.gov.uk/components/error-summary/).

Two date-input rules that come from research (https://design-system.service.gov.uk/components/date-input/):

- **Accept month names.** "Findings from the Apply for teacher training service showed that hundreds of
users were inputting months using full or abbreviated month names and getting an error. They changed the
component to accept month names … Since changing the service the number of errors has dropped dramatically."
The pattern page adds: "Some users with dyscalculia may struggle to convert month names into numbers, but
accepting full or abbreviated month names may help these users."
- **Choose example dates that reveal the order.** "Use 13 or more for the day and 9 or less for the
month — for example '27 3 2007'. This helps users enter the date in the correct order and shows them they do
not need to include leading zeroes." Any example in hint text must also be valid for the question.

## Calendar dialog: the keyboard contract

A calendar is a grid inside a dialog. Both contracts must hold or it is unusable.

**Dialog layer** (https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/):
- Role `dialog`, `aria-modal="true"`, `aria-labelledby` pointing at the visible title.
- `Tab` and `Shift+Tab` cycle **within** the dialog and do not escape it.
- `Escape` closes and focus returns to the invoking element.
- "It is strongly recommended that the tab sequence of all dialogs include a visible element with role
`button` that closes the dialog."
- **The condition on `aria-modal`:** "mark a dialog modal **only** when both: application code
prevents all users from interacting in any way with content outside of it; **and** visual styling obscures
the content outside of it." A calendar dialog that blocks the field behind it but leaves the page clickable
has severe negative ramifications for users of some assistive technologies.

**Grid layer** (https://www.w3.org/WAI/ARIA/apg/patterns/combobox/examples/combobox-datepicker/ and the APG
Date Picker Dialog example):

| Key | Action |
|---|---|
| `Space` / `Enter` on the choose-date button | Open the dialog; focus the selected date, or today if empty/invalid |
| `Down Arrow` / `Alt+Down Arrow` (combobox variant) | Open the dialog |
| Arrows | ±1 day (Left/Right), ±1 week (Up/Down) |
| `Home` / `End` | First / last day of the current week |
| `Page Up` / `Page Down` | Previous / next month; focus the same day-number, or the last day if absent |
| `Shift+Page Up` / `Shift+Page Down` | Previous / next year, same fallback |
| `Space` / `Enter` on a day | Select, close, return focus to the button, **update its accessible name** |
| `Escape` | Close without changing the value |

Three details that make the difference between working and not:

1. **Roving tabindex.** Exactly one cell is in the tab sequence; the rest are `tabindex="-1"`. This is
why `Tab` inside the dialog moves between the toolbar buttons and one cell, not across 42 days.
2. **`aria-selected` on exactly one cell.** "Only set on the cell containing the currently selected
date; no other cells have `aria-selected` specified."
3. **Live regions.** The month/year heading carries `aria-live="polite"` so screen readers announce
the new month on `Page Up`; a second `aria-live="polite"` region announces the grid keyboard help when focus
enters the calendar.

**Abbreviated weekday headers need `abbr`.** "An alternative column header name can be provided to screen
readers by applying the `abbr` attribute to the `th` elements." A `th` reading "Su Mo Tu We Th Fr Sa" is
unusable. Also: "Update the accessible name of the 'Choose Date' button to include the selected date" — so
that on close, focus returning to the button confirms what was chosen.

## Timezone handling and ambiguity

**Not found:** GOV.UK's dates and date-input guidance, and APG's combobox/dialog patterns, contain no
timezone guidance — no UTC-vs-local rule, no user-timezone default, no DST-boundary advice. GOV.UK's dates
pattern only says "If the day of the week is important, show this as well." What would settle it: an
authoritative treatment of IANA zone display for scheduling surfaces, e.g. the HTML spec's Temporal proposal
or a resolved W3C position on timezone-recording inputs. Until then, treat the following as this skill's
decision rules, flagged as judgement rather than sourced fact:

- **Date-only means date-only.** A billing period, renewal date, or anniversary stores and displays a
calendar date. Never widen a date-only field into a timestamp; that creates a phantom off-by-one for anyone
west of UTC.
- **Every timestamp crosses a zone boundary. Name the zone in the label or hint**, not only in
surrounding prose. A time field with no zone is ambiguous the moment two people look at it.
- **Scheduling surfaces store an absolute instant and render in the viewer's zone.** Pick the zone at
the top of the flow ("Europe/London"), restate the resolved instant under the picker, and render
consistently in one zone thereafter.
- **DST gaps are real.** A wall-clock schedule on a spring-forward day may not exist in the user's
zone. Resolve the instant server-side, then display what actually happened.
- **Never derive a date from a timestamp silently.** `toISOString().slice(0,10)` is a UTC date
presented as a local one.

## Relative time ("in 3 days")

Two directions, and they are different features.

**Asking for it (input).** GOV.UK: "You may need to ask for dates that are relative to today's date or
another date … let users enter or select relative dates like 'tomorrow' or '1 day before'. If the day of the
week is important, show this as well" (https://design-system.service.gov.uk/patterns/dates/).

**Showing it (output).** Absolute timestamps in a product surface are unreadable: "3 days" beats
"2026-10-08T14:30:00Z". Pair the relative form with the absolute one wherever the value is acted on — a
tooltip or secondary line — because "in 3 days" is ambiguous about the calendar date it resolves to, and it
silently becomes wrong as time passes.

**Not found:** no numeric threshold for the relative↔absolute switch point (the common "under 7 days"
rule of thumb) appears in any primary source consulted. What would settle it: a documented decision from a
design system with published testing. Until then, pick a threshold per surface and record it.

## Review checklist

- [ ] Control matches what the user knows (memorable / approximate / relative / pick-from-a-set).
- [ ] A JavaScript calendar is never the only input path.
- [ ] Day/month/year error summary link targets the first *errored* field.
- [ ] Month names accepted, full or abbreviated.
- [ ] Example date in hint uses day ≥ 13 and month ≤ 9.
- [ ] Date-only fields are not widened to timestamps; zone is named on any time input.
- [ ] Calendar dialog: `aria-modal` only with both true blocking and visual obscuring.
- [ ] Exactly one grid cell in the tab sequence; `aria-selected` on exactly one cell.
- [ ] Weekday headers carry `abbr`; month/year heading is a live region.
- [ ] Relative timestamps render alongside an absolute value where they are acted upon.

## Sources

- Ask users for dates — GOV.UK Design System — https://design-system.service.gov.uk/patterns/dates/ — accessed 2026-10-05
- Date input — GOV.UK Design System — https://design-system.service.gov.uk/components/date-input/ — accessed 2026-10-05
- Error summary — GOV.UK Design System — https://design-system.service.gov.uk/components/error-summary/ — accessed 2026-10-05
- Combobox Pattern — WAI-ARIA Authoring Practices Guide (W3C) — https://www.w3.org/WAI/ARIA/apg/patterns/combobox/ — accessed 2026-10-05
- Date Picker Combobox Example — WAI-ARIA Authoring Practices Guide (W3C) — https://www.w3.org/WAI/ARIA/apg/patterns/combobox/examples/combobox-datepicker/ — accessed 2026-10-05
- Dialog (Modal) Pattern — WAI-ARIA Authoring Practices Guide (W3C) — https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ — accessed 2026-10-05
- Date Picker Dialog Example — WAI-ARIA Authoring Practices Guide (W3C) — https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/datepicker-dialog/ — accessed 2026-10-05
- Using HTML form validation and the Constraint Validation API — MDN Web Docs — https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation — accessed 2026-10-05
