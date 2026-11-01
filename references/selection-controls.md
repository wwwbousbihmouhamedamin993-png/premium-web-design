# Selection controls

Applies to: checkbox, radio, switch, segmented control, combobox — and the rule that keeps them from being
confused with each other.

## Pick the control by cardinality, then by cardinality of *application*

| Control | Selection model | State count | Semantics announced | Primary use |
|---|---|---|---|---|
| Checkbox | 0..n of a visible set | checked / unchecked / **mixed** | "checked" | batch multi-select, filter facets, row selection |
| Radio | exactly 1 | checked / unchecked | "checked" | 2–7 options, settings where seeing all options matters |
| Switch | exactly 1 binary | on / off **only** | "on"/"off" | a preference that applies immediately |
| Segmented control | exactly 1 | one segment active | "checked" or "pressed" | 2–5 short peer views of the same data |
| Combobox | 1 (or 0..n tokens) | per-option selected | name + value | 8+ options, or options unknown to the user |

GOV.UK gives the checkbox/radio split as a hard rule:
- Checkboxes: "select multiple options from a list" **or** "toggle a single option on or off"
(https://design-system.service.gov.uk/components/checkboxes/)
- Radios: "Use the radios component when users can only select one option from a list." "Do not use
the radios component if users might need to select more than one option"
(https://design-system.service.gov.uk/components/radios/)
- Select: "should only be used as a last resort in public-facing services because research shows that
some users find selects very difficult to use" (https://design-system.service.gov.uk/components/select/)

## The rule that carries the most weight: never mix control types in one group

GOV.UK, stated for radios and again for checkboxes, independently: "Do not assume that users will know how
many options they can select based on the visual difference between radios and checkboxes alone." *(both
https://design-system.service.gov.uk/components/radios/ and /components/checkboxes/)*

Two readings, both binding:

1. **Within one group, the control type carries no instruction** — so the group needs a hint. Add
"Select one option" to radios, "Select all that apply" to checkboxes.
2. **Never place radios and checkboxes in the same fieldset or list.** A shared list where some rows
are single-choice and some are multi-choice communicates nothing. Split them into two labelled groups or
choose one model.

A third mixing axis to avoid: a switch *inside* a list of checkboxes for the same purpose. If the rows are
toggles, they are all switches; if the rows are selections, they are all checkboxes.

## Instant binary state (switch) vs batched multi-select (checkbox)

These diverge on **when the change takes effect**, which is the real design question, not the marking.

- **Switch = instant.** Flipping it applies. A switch next to a "Save" button that reads "Save" is a
defect — the user expects the change already happened.
- **Checkbox = batched.** Checking several boxes changes nothing until the form is submitted.
- **Radio = usually batched**, but choosing a radio is a *selection*, not an application, unless the
surface is explicitly live.

APG on why the distinction matters (https://www.w3.org/WAI/ARIA/apg/patterns/switch/):

> "Switches can only be used for binary input while checkboxes and toggle buttons allow implementations
> the option of supporting a third middle state. … Since switch, checkbox, and toggle button all offer
> binary input, they are often functionally interchangeable. Choose the role that best matches both the
> visual design and semantics of the user interface."

APG's own test is the screen-reader string. For turning lights on and off, "**Lights switch on**" is more
user-friendly than "Lights checkbox checked". But the same input inside a group labelled "Which of the
following must be included in your pre-takeoff procedures?" reads better as "Lights checkbox checked".

**APG, important:** "it is critical the label on a switch does not change when its state changes." A switch
labelled "Notifications: off" then "Notifications: on" breaks the control. The label states what is
controlled; the state is announced separately.

Switch state semantics, same source: role `switch`; `aria-checked="true"` when on, `"false"` when off;
`Space` changes state and `Enter` is optional. If built on `<input type="checkbox">`, "it uses the HTML
`checked` attribute instead of the `aria-checked` property." Group a set of switches in an element with
`role="group"` carrying `aria-labelledby`, **or** in an HTML `<fieldset>` with a `<legend>`.

## Indeterminate / mixed state

APG's checkbox pattern defines three states, and the mixed state is a *group* aggregate
(https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/): `aria-checked="true"` when all options in the group
are checked, `"mixed"` when some are, `"false"` when none are.

- Checking the parent checks all children; unchecking unchecks all.
- Some implementations remember which children were checked when the parent was last mixed, so a third
activation restores that set. **Optional** — GOV.UK has no equivalent behaviour, and it is not free.

**Do not use `switch` for a select-all control.** A switch is binary only and has no mixed state, so a
partial selection cannot be represented. Use a checkbox with `aria-checked="mixed"`.

In HTML the property is set via the DOM, not an HTML attribute — **Not found:** a citation for the property
name in this session. Settled by MDN
`https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/indeterminate`.

## Semantics: the attribute names, verified

| Control | Container role | Item role | State | Keyboard |
|---|---|---|---|---|
| Checkbox | `role="group"` + `aria-labelledby`, **or** `<fieldset>`/`<legend>` | `checkbox` | `aria-checked` `true`/`false`/`mixed` | `Space` changes state |
| Radio | `radiogroup` | `radio` | `aria-checked` `true`/`false` | `Space` checks; arrows move **and** check; `Tab` in/out |
| Switch | `role="group"` + `aria-labelledby`, **or** `<fieldset>`/`<legend>` | `switch` | `aria-checked` `true`/`false` | `Space`; `Enter` optional |

*(https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/, /patterns/radio/, /patterns/switch/)*

Radio group focus rules, verbatim from APG: on `Tab` into the group, "if a radio button is checked, focus is
set on the checked button. If none of the radio buttons are checked, focus is set on the first radio button
in the group." Arrows wrap: on the last button, focus moves to the first. APG flags that this "differs
slightly from the behavior provided by some browsers" when using `Shift+Tab`.

In a toolbar, the radio interaction changes: arrow keys move focus **without** changing the checked button,
and `Space`/`Enter` do the checking — because "users need to be able to navigate among all toolbar elements,
including the radio buttons, without changing which radio button is checked"
(https://www.w3.org/WAI/ARIA/apg/patterns/radio/).

## Segmented control

**Not found:** GOV.UK Design System, ARIA APG, and MDN have no component named "segmented control",
and no numeric thresholds for its width or item count. Settled by searching the ARIA APG pattern index
(`https://www.w3.org/WAI/ARIA/apg/patterns/`) and GOV.UK's component list.

What the primary sources do support, and what this skill commits to:

- **Markup as a radio group.** It is single-choice among peers, so `radiogroup` + `radio` +
`aria-checked` is the correct role set. APG explicitly notes that "radio buttons in a toolbar are frequently
styled in a manner that appears more like toggle buttons" — a segmented control is that styling.
- **If it toggles multiple views simultaneously, use `role="group"` of toggles with `aria-pressed`,
not radios.** A segmented control where two segments can be lit at once is a toolbar of toggle buttons, and
labelling it a radiogroup lies about it.
- **The trigger is the option count.** GOV.UK's radio guidance is built around short visible option
lists, and its select guidance is built around the problem of too many options
(https://design-system.service.gov.uk/components/select/). Segmented controls sit in the gap: use them only
when every option stays legible without truncation.
- GOV.UK's inline-radio rule is the closest documented analogue: "Only use inline radios when: the
question only has two options; both options are short"
(https://design-system.service.gov.uk/components/radios/). A segmented control should clear that same bar,
with a higher ceiling for labelled segments since segments can carry their own labels.

## Checkbox-specific rules worth keeping

- **Always position checkboxes to the left of their labels.** "This makes them easier to find,
especially for users of screen magnifiers" (both the checkbox and radio pages).
- **Never pre-select** checkboxes or radios in a question — it makes it "more likely that users will
not realise they've missed a question … submit the wrong answer". Pre-selection is correct for settings
selects, wrong for questions.
- **Order alphabetically** by default; most-to-least-common only where clearly better, and for radios
"with extreme caution as it can reinforce bias".
- **Provide a "none" option** when "none" is a valid answer, placed **last** and separated by a
divider — "The text is usually the word 'or'". The label must repeat the question: for "Will you be
travelling to any of these countries?" write "No, I will not be travelling to any of these countries." Then
add `data-behaviour="exclusive"` to uncheck the others.
- **Exclusive behaviour needs a no-JS fallback error.** "If JavaScript is unavailable, and a user
selects both the 'none' checkbox and another checkbox, display an error message".
- **Conditional reveal may only reveal questions**, never non-question content. Known gap: "Users are
not always notified when a conditionally revealed question is shown or hidden. This fails WCAG 2.2 success
criterion 4.1.2 Name, Role, Value." Keep revealed content simple — GDS testing found no difficulty with
simple questions, and confusion with complicated ones.
- **Small checkboxes are correct on filter surfaces.** "On a page of search results, the main user
need is to see the results. Using smaller checkboxes lets users see and change search filters without
distracting them from the main content." GOV.UK adds that small checkboxes "work well on information dense
screens in services designed for repeat use, like caseworking systems", where "the risk that they will not
be noticed is lower because users return to the screen multiple times". That caveat is about repeat-use
density, not a licence to relax contrast or hit targets.

## Combobox

Full semantics are in `command-palette.md`. The selection-relevant facts from APG
(https://www.w3.org/WAI/ARIA/apg/patterns/combobox/):

- A combobox is a **single-select** widget; "selection follows focus in the popup".
- **Editable vs select-only.** Select-only: "the only way users can set its value is by selecting a
value in the popup" — APG notes an HTML `select` with `size="1"` is presented to assistive technologies as a
select-only combobox in some browsers. Editable: the value may be an arbitrary string, or restricted to a
discrete allowed set.
- **Why not a listbox or menu button:** "One feature that distinguishes combobox from both listbox
and menu button is that the user's choice can be presented as a value in an editable field, which gives
users the ability to select some or all of the value for copying to the clipboard." And: "a menu button
cannot be marked required, and while it has an accessible name, it does not have a value so is not suitable
for conveying the user's choice in its collapsed state."
- **The undo argument for combobox over single-select listbox:** comboboxes "can be implemented so
users can explore the set of allowed choices without losing a previously made choice … users can navigate
the set of available choices in a combobox popup or menu and then press `escape`, which closes the popup or
menu without changing previous input. In contrast, navigating among options in a single-select listbox
immediately changes its value, and `Escape` does not provide an undo mechanism."

## Sources

- Checkboxes — GOV.UK Design System — https://design-system.service.gov.uk/components/checkboxes/ — accessed 2026-10-05
- Radios — GOV.UK Design System — https://design-system.service.gov.uk/components/radios/ — accessed 2026-10-05
- Select — GOV.UK Design System — https://design-system.service.gov.uk/components/select/ — accessed 2026-10-05
- Switch Pattern — WAI-ARIA Authoring Practices Guide (W3C) — https://www.w3.org/WAI/ARIA/apg/patterns/switch/ — accessed 2026-10-05
- Checkbox Pattern — WAI-ARIA Authoring Practices Guide (W3C) — https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/ — accessed 2026-10-05
- Radio Group Pattern — WAI-ARIA Authoring Practices Guide (W3C) — https://www.w3.org/WAI/ARIA/apg/patterns/radio/ — accessed 2026-10-05
- Combobox Pattern — WAI-ARIA Authoring Practices Guide (W3C) — https://www.w3.org/WAI/ARIA/apg/patterns/combobox/ — accessed 2026-10-05
- Developing a Keyboard Interface — WAI-ARIA Authoring Practices Guide (W3C) — https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/ — accessed 2026-10-05
