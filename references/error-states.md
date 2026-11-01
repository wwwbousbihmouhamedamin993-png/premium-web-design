# Error states

Applies to: field-level validation, form submission, section and page failures, background job failures.

## Framing

Carbon's own docs list an **"Error states (future)"** pattern — it does not yet exist [S1]. So this file is assembled from Carbon's error-management empty states, Carbon's form and notification guidance, and NN/g's error-message research. Expect gaps, and see **Not found**.

The governing heuristic is Nielsen's ninth: *Help users recognize, diagnose, and recover from errors* [S2]. Every rule below is a way to satisfy one of those three verbs.

## Error surfaces

| Surface | Scope | Anchor | Rule |
|---|---|---|---|
| **Inline field error** | One input | Directly below the field | Show as soon as the field loses focus; do not wait for submit [S3] |
| **Validation summary** | Whole form | Top of form, above the first field | Never the *only* indication; always pair with inline errors [S4] |
| **Inline notification** | A region or the form | Next to the related items; top or bottom of a form | Keep under two lines [S5] |
| **Toast** | System-level, not tied to one section | Top right | Max three lines; fixed width, do not stretch [S5] |
| **Banner** | System or product level, not task-specific | Top of the content area it relates to | Only one at a time; not sticky; scrolls with content [S5] |
| **Section / partial-page error** | One widget or panel of many | Inside the failing region | Failure is contained; siblings stay usable [S6] |
| **Page error** | The route could not render | Centred in the content area | Name the cause and the exit [S7] |

Carbon's type list: inline, toast, actionable, callout, banner, notification panel, modal [S5]. Polaris' `s-banner` covers the page-wide case with tones `info | success | warning | critical | auto` [S6].

## Carbon's four recoverable failure classes

Carbon names four classes inside its error-management empty states, and prescribes two messages for each — why there is no data, and what the user can do [S1]:

| Class | Explain why | Explain what the user can do |
|---|---|---|
| **Permissions** | The user does not have permission to view the data | Suggest steps or process to request access |
| **Systems** | Problems with a related system prevent the data from being supplied | Explain steps the user can take to learn what happened, e.g. viewing an activity log |
| **Configuration** | Further configuration may be needed to access the data | Provide an explanation and the first step to take |
| **Action not supported** | e.g. an unsupported file type was uploaded | Explain what is supported |

Carbon's requirement on wording: messages "should be expressed in plain language (no codes), precisely indicate the problem, and constructively suggest a solution" [S1]. "A higher level of specificity is helpful here, with the aim that the user will be able to address the issue comfortably themselves" [S1].

Note the asymmetry: permissions and configuration are the user's to fix. Systems may not be. A systems error that offers a Retry button as the only remedy, with no indication of scope or cause, fails "diagnose".

## Writing the message

Four NN/g requirements, in order of how often they are broken [S2]:

1. **Display the error close to its source.** "Reduce cognitive load by displaying an error indicator adjacent to the interface where the error occurred. Proximity helps users associate the error message content with the interface elements needing attention" [S2].
2. **Use noticeable, redundant, accessible indicators.** "Text and highlights that are bold, high-contrast, and red are conventional error-message visuals. Use this styling for the message and for the affected elements needing correction." And: "never use exclusively color or animation to indicate errors" [S2]. NN/g notes roughly 350 million people worldwide have a colour-vision deficiency [S2].
3. **Concisely and precisely describe the issue.** "Generic messages such as *An error occurred* lack context." But also: "beware of excessive technical precision and accuracy that can undermine understandability. The user's mental model of how the system works likely differs from the conceptual model of how it was coded" [S2].
4. **Offer constructive advice.** "Merely stating the problem is also not enough; offer some potential remedies" [S2].

Tone rules [S2]:

- "Write with a positive and nonjudgmental tone of voice. Don't use phrasing that blames users or implies they are doing something wrong, such as *invalid*, *illegal*, or *incorrect*. The proper usage of any system lies with its creators and not with the system's users, so the system must gracefully adapt and not shift blame."
- "Avoid humor since it can become stale if users encounter the error frequently."
- "Hide or minimize the use of obscure error codes or abbreviations; show them for technical diagnostic purposes only." NN/g names the 404 page as violating the plain-language guideline [S2].

Preserve the user's work [S2]: "Let users correct errors by editing their original action instead of starting over. For example, display the original text entered into a text field even if it does not match the requirements for that field and allow the user to modify it." And reduce correction effort: "If possible, guess the correct action and let users pick it from a small list of fixes. For example, instead of just saying *City and ZIP code don't match,* let users click on a button for the city that matches the ZIP code they entered" [S2].

## Length limits

| Surface | Limit | Source |
|---|---|---|
| Inline notification | "Keep the message under two lines" | Carbon [S5] |
| Toast | "should not exceed three lines"; "Removing the timestamp provides space for a third line of content" | Carbon [S5] |
| Banner (Polaris) | No limit stated; "Very long banner messages will wrap to multiple lines, creating tall banners that dominate the screen" is listed as a component limitation | Polaris [S6] |
| Actionable notification label | "Limit action labels to two words or less" | Carbon [S5] |

Carbon also warns on density: multiple toasts "stack vertically, with the newest appearing at the top" and toasts have "a fixed width and should not be expanded to fit the content area" [S5].

**Not found:** a sourced character limit for form error text — Carbon gives line counts for notifications and a word count for action labels only.

## What must never appear

Grounded in NN/g [S2] and Carbon's plain-language rule [S1]:

- **Raw server strings** — stack traces, ORM or SQL fragments, JSON payloads, exception class names. "Hide or minimize the use of obscure error codes or abbreviations; show them for technical diagnostic purposes only" [S2]. If support needs it, surface it as a copyable reference ID, not as the message.
- **Generic "something went wrong" / "An error occurred."** NN/g calls this out by name: generic messages "lack context" [S2]. Error codes as primary content fail for the same reason — codes are diagnostic, not explanatory [S2].
- **Blame.** "invalid", "illegal", "incorrect" [S2].
- **Premature errors.** "Presenting errors too early is a hostile pattern. It's like grading a test before the student has had a chance to answer." NN/g's failure case: a Texas vehicle-registration page shows an error when an empty email field loses focus, "which suggests the user did something wrong by merely exploring the interface" [S2].
- **Tooltips as the error channel.** Three reasons from NN/g: alert icons are hard to notice on visually dense interfaces; users may not realise a message is displayed; it adds unnecessary effort for critical information [S4].
- **Timed dismissal on critical messages.** Carbon: "Don't use notifications that dismiss on a timer for critical or emergency messages. Some users with disabilities need more time to read or interact" — citing WCAG 2.1 SC 2.2.4 (AAA) [S5].
- **A modal for anything short.** Modals "are disruptive" and "the error message appears in a window that must be dismissed before fixing the error, forcing users to remember complex instructions" [S4].
- **Errors on untouched fields.** BestBuy's checkout raised an error on Email after the user navigated away, then raised another on Phone Number "although the user had not started typing in that field" [S4].

## Field-level validation sequence

**Timing conflict — resolve it deliberately.** Carbon says "We recommend validating the user's data before form submission. This type of real-time, inline validation (a.k.a. client-side validation) should happen as soon as the field loses focus" [S3]. GOV.UK says the opposite: "Do not validate when the user moves away from a field" (`forms-validation.md`). Both are defensible and both are primary. NN/g's constraint is the one that reconciles them: "Presenting errors too early is a hostile pattern" — but immediately adds "do consider inline, real-time errors for error-prone interactions where users are unlikely to enter the correct information on their first try" [S2]. So: validate on submit by default, and validate on blur **only** for fields with a known high error rate (email format, password rules, card number). Pick one and apply it across the product; mixing per-form is the defect.

1. **Validate on submit, or on blur for demonstrably error-prone fields.** Carbon's form component lists a distinct `Error` state — "When the user input is invalid or a required text input has not been filled in… This state requires a user response before data can be submitted or saved" — and a `Warning` state for "an exception condition… that might not be an error but can cause problems if not resolved" [S9].
2. **State the rule, not the verdict.** Carbon's example: if the limit is 16 characters and the user typed six, the text reads "Password must be at least 16 characters" [S3].
3. **Confirm success for expensive-to-get-right fields.** NN/g endorses live feedback on complex inputs — "instant inline validation (which appears as the field value is being typed) will prevent users from guessing or checking multiple times" — but caps it: "you don't need to show a success message when the only requirement on the field is that it is filled in" [S4].
4. **Server-side errors come back as inline, too.** Carbon: when the form is submitted and the page reloads with detected errors, "use an inline notification as well as inline error messaging wherever possible. Inline error messages should disappear when the form criteria is met" [S3].
5. **Let layout absorb the message.** Carbon: in a two-column form, "if the left column form item becomes invalid and pushes form content down to accommodate space for an error message, then the accompanying right form item will also grow" — the row responds as a group [S9]. Do not overlay or absolutely position error text over the next field.

## Partial and page-level failure

**Partial-page.** Contain the failure. Polaris on dashboards and repeated widgets: if several widgets fail, repeated identical empty/error states lose their signal — "an empty state that uses just text may be preferable" [S1]. One failing widget should not disable or blank its siblings.

**Page error.** NN/g's failure-mode catalogue: users arrived at a no-results page and "did not even realize that the search engine hadn't found any results. Instead they waste valuable time scanning irrelevant ads or related links" [S9]. A page error must be visually unmistakable, name the cause, and offer the exit.

**For total failure only**, NN/g allows one unusual tactic — "Mitigate total failure with novelty" — with an explicit ceiling: it applies "when the system becomes incapable of serving users in any functional capacity… there is no recourse but to wait or try again later", these moments "should be rare and avoided at all costs", and the goal is to blunt the negativity bias. Their examples are ChatGPT's downtime content and Twitter's retired Fail Whale [S2]. Do not extend this to a failed save on a settings page.

**Repeated failure is a design defect.** NN/g: "When users encounter the same error repeatedly (3 or more times in a single form-filling attempt), it indicates a deeper issue in the user interface — unclear error messages, a mismatch between the design and users' needs, or overly complex requirements in the form." Their remedy is to add help — Quicken linked to a contact form — and to review analytics for the error pattern [S4].

## Announcing errors

WCAG 2.1 SC 4.1.3 Status Messages (AA) applies to errors: status must be "programmatically determined through role or properties such that they can be presented to the user by assistive technologies without receiving focus" [S5]. W3C's example for this exact case: "text is added to the existing form which reads '5 errors on page'" [S5].

Sufficient techniques W3C names [S5]:

- ARIA22 / `role="status"` for success and results messages.
- ARIA19 / `role="alert"` or a live region for warnings and the existence of errors, combined with G83 (identify unfilled required fields), G84 (value not in the allowed list), G85 (input outside required format), G177 (suggested correction text), G194 (spell checking).
- Failure F103: status messages that cannot be programmatically determined through role or properties.

Carbon's notification accessibility adds: "Don't use notifications that dismiss on a timer for critical or emergency messages" (SC 2.2.4, AAA) and "Users should be able to manage or limit noncritical notifications" (SC 2.2.3, AAA) [S5]. Both are AAA — record the decision rather than claiming conformance.

Carbon's `aria-live` / W3C reference is cited in its own notifications pattern [S5]. For the announcement mechanics: put `aria-live` on an **empty** element in markup and write the text into it on update — the element is not given focus — and reserve `assertive` for cases where "an interruption… is imperative" [S8].

## Severity mapping

NN/g: "Design errors based on their impact… Differentiate between these 'good to know' messages from those posing a barrier to the user's progress. Conditionally displayed labels, toast notifications, or banners can be used for issues needing minimal user interaction, whereas modal dialogs require the user's attention and resolution and should be reserved for severe errors" [S2].

Carbon's error status is red with an `error filled` icon; warning is yellow with `warning filled`; success green with `checkmark filled`; informational blue with `information filled` [S5]. Polaris' `s-banner` tone set: `info`, `success`, `warning`, `critical`, `auto` [S6].

Escalation ladder: inline → inline notification → toast (system-level only) → banner (one at a time) → modal (severe only) [S5].

## Related

- `forms-validation.md` — validation timing and the error summary pattern, including the GOV.UK position.
- `toasts-notifications.md` — live-region mechanics, duration, stacking, and the banner/toast split.
- `loading-skeletons.md` — the failure branch of async states; every skeleton needs a defined terminal.

## Not found

- **A character limit for form or field error messages.** Carbon gives lines for notifications and words for action labels only [S5].
- **Carbon's "Error states" pattern does not exist** — it is listed as "(future)" on both the empty-states page [S1] and the notifications page [S5]. Any Carbon-attributed error taxonomy is assembled from other pages, not from a canonical error-state doc.
- **A standard retry affordance spec.** NN/g requires a percent-done indicator past 10s and a signposted interrupt [S10]; nothing specifies how Retry should look or what it should say.
- **A sourced rule on whether a page error should preserve the navigation shell.** No source in this set addresses it.
- **Timeout thresholds for any request.** Out of scope for the sources gathered; no error-message guideline sets one.

## Sources

- **[S1]** https://carbondesignsystem.com/building-blocks/core/patterns/empty-states/ — IBM Carbon Design System, "Empty states" pattern (last updated Aug 11, 2026). Four error-management classes; plain-language/no-codes rule; repetition advice; "Error states (future)" listing. Accessed 2026-10-05.
- **[S2]** https://www.nngroup.com/articles/error-message-guidelines/ — Nielsen Norman Group, Tim Neusesser & Evan Sunwall, "Error-Message Guidelines" (May 14, 2023). Visibility / communication / efficiency sections; tone and blame rules; preserve input; novelty-in-total-failure; 404 and colour-vision figures. Accessed 2026-10-05.
- **[S3]** https://carbondesignsystem.com/building-blocks/core/patterns/forms/ — IBM Carbon Design System, "Forms" pattern (last updated Aug 11, 2026). Client-side validation on blur; password-length example; server-side inline notification plus inline errors; submit-button disabling rules. Accessed 2026-10-05.
- **[S4]** https://www.nngroup.com/articles/errors-forms-design-guidelines/ — Nielsen Norman Group, Rachel Krause, "10 Design Guidelines for Reporting Errors in Forms" (Feb 3, 2019; last reviewed Dec 12, 2024). Validation summaries not sole indicator; no tooltips for errors; no premature validation; 3-or-more-repeated-errors rule; modal cost. Accessed 2026-10-05.
- **[S5]** https://carbondesignsystem.com/building-blocks/core/patterns/notifications/ — IBM Carbon Design System, "Notifications" pattern (last updated Aug 12, 2026). Statuses and icons; seven types with duration rules; two-line inline and three-line toast limits; severity ladder; SC 2.2.4 and 2.2.3 accessibility notes; "Error states (future)". Accessed 2026-10-05.
- **[S6]** https://shopify.dev/docs/api/app-home/latest/web-components/feedback-and-status-indicators/banner — Shopify, Polaris web components: Banner (v1.1). Tone set; one-item-per-banner rule; CTA required for info/warning/critical; long-message wrapping limitation; dismissibility and queueing limitations. Accessed 2026-10-05.
- **[S7]** https://carbondesignsystem.com/building-blocks/core/components/loading/guidelines/ — IBM Carbon Design System, "Loading" component guidelines (last updated Sep 28, 2026). Consulted for the failure branch of async states. Accessed 2026-10-05.
- **[S8]** https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-live — Mozilla Developer Network, "ARIA: aria-live attribute" (last modified Sep 23, 2025). polite / assertive semantics; assertive interruption warning. Accessed 2026-10-05.
- **[S9]** https://carbondesignsystem.com/building-blocks/core/components/form/guidelines/ — IBM Carbon Design System, "Form" component guidelines (last updated Sep 30, 2026). Input states including Error and Warning; two-column row-grow behaviour. Accessed 2026-10-05.
- **[S10]** https://www.nngroup.com/articles/response-times-3-important-limits/ — Nielsen Norman Group, Jakob Nielsen, "Response Times: The 3 Important Limits" (Jan 1993). 10s limit, percent-done requirement, signposted interrupt. Accessed 2026-10-05.
- **[S11]** https://www.w3.org/WAI/WCAG21/Understanding/status-messages.html — W3C WAI, Understanding SC 4.1.3 Status Messages (Level AA; page updated May 11, 2026). "5 errors on page" example; ARIA19/ARIA22/G177/G83-G85 techniques; failure F103. Accessed 2026-10-05.
- **[S12]** https://www.nngroup.com/articles/search-no-results-serp/ — Nielsen Norman Group, Kathryn Whitenton, "3 Guidelines for Search Engine 'No Results' Pages" (Jan 5, 2014). The unnoticed-message failure mode. Accessed 2026-10-05.
