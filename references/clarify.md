# Clarify — UX copy, labels, error messages, destructive confirms

Fix command. `clarify` fixes what the interface *says*. It is the smallest diff in this skill and
the one most often skipped, because bad copy compiles.

## The one rule that covers most of it

**No bare "Submit". No bare "OK". No bare "Error".** A label that does not name the action makes
the user read the surrounding context to work out what the button does — which is the definition of
an affordance that has failed. Labels name the action: "Create project", "Invite member", "Delete
workspace", not "OK". Every `craft-floor.md` control rule and every Polaris action-slot constraint
resolves to the same requirement.

The button's cost is also its label's job: a destructive action never wears the same weight as a
safe one, and the confirm dialog's primary button names the destruction ("Delete workspace"), not
the acknowledgement.

## Plain-language rules

Every rule here is traceable to Carbon, NN/g, or GSA — this is the least judgement-heavy command in
the skill.

- **Plain language, no codes.** Error messages "should be expressed in plain language (no codes),
  precisely indicate the problem, and constructively suggest a solution" (Carbon).
- **Never blame.** Not *invalid*, not *illegal*, not *incorrect*. "The proper usage of any system
  lies with its creators and not with the system's users, so the system must gracefully adapt and
  not shift blame" (NN/g). Carbon's form example: "Password must be at least 16 characters" — the
  rule, not the verdict.
- **Never mock.** On a no-results page, users "may not be able to tell whether you are laughing with
  them, or laughing at them" (NN/g). Carbon: "Be respectful of the user and don't joke or use
  flippant language," and no-result pages repeat the failure often enough for a joke to go stale.
- **Generic messages are not messages.** NN/g names the failure directly: generic messages such as
  *An error occurred* "lack context." But also beware over-precision — "beware of excessive
  technical precision and accuracy that can undermine understandability. The user's mental model of
  how the system works likely differs from the conceptual model of how it was coded."
- **Length.** GSA's plain-language guidance: keep paragraphs to about **150 words**, never over
  **250**. Carbon's surface-specific limits: inline notification under two lines; toast no more
  than three lines; notification action labels two words or less. **No sourced character limit
  exists for form error text** — Carbon gives line counts and a word count only.
- **No em-dash tic.** The detector's `em-dash-overuse` rule exists because a dash in every sentence
  is a recognizable generation habit. Use a full stop between separate thoughts.

## Labels and helpers

| Surface | Rule | Example |
|---|---|---|
| Primary button | Names the action and its object | "Create project" not "OK"; "Send invite" not "Submit" |
| Cancel | Names the escape | "Cancel" is acceptable — the action is genuinely to do nothing |
| Destructive button | Names the loss | "Delete workspace", "Revoke key", "Remove member" |
| Link that navigates | Names the destination | "View audit log" not "Click here" / "Learn more" |
| Field label | Persistent, above or beside the control | Never placeholder-as-label — a field that empties on focus forgets its name |
| Helper text | Specific to this field's rule | "Add a receiving address to enable webhooks" not "Learn more" |
| Empty state heading | Names the cause in the heading | "Start by adding data assets" over "No products" |
| Table column header | The actual data name | Not "Field 1"; must match the record detail's wording |
| Nav item | The user's word for the destination | List and detail share vocabulary — same words, same order, same casing |
| Icon-only control | Tooltip plus accessible name | An icon with no label is a hidden affordance |
| Count / status badge | Carries text, not colour alone | "3 errors", "Read-only", "Trial ends 14 Mar" |

**One contextual hint per surface**, placed next to the control it describes and never covering it,
dismissible, and staying dismissed (`saas-onboarding-playbooks.md`).

**Redundancy is a defect.** The detector's `repeated-container-text` rule fires when the same label
appears in several slots of one card — four bits of text explaining the same field. Ship it once,
where it matters.

## Error messages: the shape

Every error answer three questions in order, and answers them near the source:

1. **What happened** — specific, in the user's vocabulary, no code.
2. **Why** — the cause the user can act on.
3. **What to do next** — a concrete step, a link, or a suggested correction.

Placement: adjacent to the interface where the error occurred, because "proximity helps users
associate the error message content with the interface elements needing attention." A validation
summary is never the *only* indication — always pair it with inline errors. Preserve the user's
work: "display the original text entered into a text field even if it does not match the
requirements for that field and allow the user to modify it," and where possible "guess the correct
action and let users pick it from a small list of fixes."

Status must be announced, not just painted — SC 4.1.3 (AA): programmatically determinable "through
role or properties such that they can be presented to the user by assistive technologies **without
receiving focus**."

## Destructive confirmations: the copy ladder

Climb only as far as irreversibility demands. Levels 0–1 need no dialog at all
(`modals-dialogs-drawers.md`):

| Level | Irreversibility | Copy requirement |
|---|---|---|
| 0 — Undo-first | Fully reversible | Act immediately; the button is "Archive", not "Delete"; offer Undo |
| 1 — Reversible but surprising | Soft delete, archive, state toggle | Inline confirm row naming what moves to trash |
| 2 — Costly to reverse | Billing change, permission removal | `alertdialog`; name the cost and the effective date; safest action focused |
| 3 — Destructive | Deletion, revocation, termination | `alertdialog`; **name the affected object**; least destructive action focused |
| 4 — Irreversible, high blast radius | Destroy workspace, rotate a production secret | `alertdialog` + type-to-confirm; state that it cannot be undone |

Polaris's Settings example is the model for level 3: a confirm carrying a critical tone and the
explicit sentence "This action cannot be undone." The consequence-before-click rule applies in the
body text: the cost, the effective date, and what breaks are visible **before** the commit.

**Type-to-confirm is not a substitute for clarity.** It exists for level 4 only; using it at level 3
teaches users that dialogs are obstacles.

## Internationalised copy

- **No string concatenation.** Compose with ICU message format; every user-visible string goes
  through a catalog, not a literal in a component.
- **Locale formatters for every date, number, and currency.** Never hand-formatted.
- **Plurals via ICU**, never an `if (count === 1)` in the component.
- **Budget +35% expansion** in every button, header, and table cell. Truncation is a decision with
  a tooltip or an overflow affordance, not a silent cut.
- **RTL**: label direction and punctuation follow the locale, not the source string
  (`i18n-rtl.md`).

## Verify

- Grep the codebase for `Submit`, `OK`, `Cancel` variants, `Error`, `Lorem`, and raw server strings
  reaching the DOM.
- Read every button aloud: does it name the action? Would it be unambiguous with the surrounding
  text removed?
- Turn colour off: does every status still read?
- Fill a form with wrong values: is each message specific, blame-free, and adjacent to its field?
- Trigger three errors in one attempt and read them as a new user would.
- Toggle a destructive action: does the dialog name the affected object and the irreversibility?
- Set the browser to German and to Arabic; check truncation, plural forms, and mixed-direction
  runs. Set a +35% expansion.
- Check no paragraph exceeds 150 words and none exceeds 250.

## Detector advisories

`repeated-container-text`, `em-dash-overuse`, `marketing-buzzword` ("supercharge", "world-class"),
`aphoristic-cadence` (slogan-like contrasts), and `theater-slop-phrase` ("theater") are the
copy-band findings. None carries a density exception — they fail at every class. Mechanics:
`detector-integration.md`.

## Exit criteria

No bare "Submit"/"OK"/"Error" anywhere. Every control names its action; every icon-only control has
a name. Every error specific, blame-free, actionable, adjacent to its source, and announced.
Destructive actions at the right rung with the affected object named. No concatenation, no hardcoded
strings, locale formatters and ICU plurals throughout. +35% and RTL verified.

## Not found

- **A sourced character or word budget for field labels, button labels, or form error text.** Carbon
  and Polaris constrain structure and provide line and word counts for *notifications* only; no
  primary source sets a label-length figure. What would settle it: a `DESIGN.md` decision plus a
  readability test on real content.
- **A sourced sentence-length or reading-grade target for UX microcopy.** GSA's 150/250-word
  paragraph rule is the closest cited guidance; it addresses paragraphs, not interface sentences.
- **A normative rule for when type-to-confirm is warranted.** The ladder is house judgement
  calibrated against `alertdialog`'s requirement that the least destructive action be focused
  (APG).

## Sources

Primary references: `error-states.md` (Carbon's four failure classes, plain-language requirement,
NN/g tone and message rules, what must never appear, length limits), `modals-dialogs-drawers.md`
(dialog surface choice, anatomy, initial focus, the destructive-confirmation ladder), `forms-validation.md`
(validation timing, error summary pattern), `empty-states.md` (headings that name the cause),
`saas-onboarding-playbooks.md` (one hint per surface, specific hints), `i18n-rtl.md`,
`page-composition.md` (action budgets), `craft-floor.md` (labels name the action), `data-tables.md`
(column naming), `app-shell-navigation.md` (nav vocabulary), `usage-limits-quotas.md`.

External pages cited above, all previously opened by this skill:

- Empty states (positive-statement headings; "don't joke or use flippant language"; specificity;
  the four error-management classes and their prescribed copy) — Carbon Design System (IBM).
  https://carbondesignsystem.com/building-blocks/core/patterns/empty-states/ — accessed 2026-10-05.
- Error Message Guidance — Nielsen Norman Group.
  https://www.nngroup.com/articles/error-message-guidelines/ — accessed 2026-10-05.
- 3 Guidelines for Search Engine "No Results" Pages (do not mock the user) — Nielsen Norman Group.
  https://www.nngroup.com/articles/search-no-results-serp/ — accessed 2026-10-05.
- Clear and short (plain language): 150-word paragraphs, 250-word hard ceiling — U.S. GSA /
  Digital.gov. https://digital.gov/guides/plain-language/writing/clear-short — accessed 2026-10-05.
- Alert and Message Dialogs Pattern (least destructive action focused on the final step of a
  non-reversible process; focus returns to the invoker) — W3C WAI ARIA Authoring Practices Guide.
  https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/ — accessed 2026-10-05.
- Polaris Settings template ("Reset all settings" confirmed with a critical-tone modal and "This
  action cannot be undone"; "Don't include any actions at the bottom of the page") — Shopify,
  shopify.dev. https://shopify.dev/docs/api/app-home/patterns/templates/settings — accessed 2026-10-05.
- Understanding SC 4.1.3 Status Messages (AA) · SC 3.3.1 Error Identification (A) — W3C WAI.
  https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html —
  https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html — accessed 2026-10-05.
- WCAG APG Alert dialog / Inline form error guidance — W3C WAI.
  https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html — accessed 2026-10-05.

**House process, not sourced fact:** the label and helper table's example phrasings, the three-step
error shape, the copy ladder's wording requirements, the verification grep list, and the exit
criteria. Carbon's and NN/g's wording rules, GSA's word counts, and APG's focus behaviour are cited.