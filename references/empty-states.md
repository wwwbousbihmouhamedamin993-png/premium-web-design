# Empty states

Applies to: tables, lists, dashboards, tiles, side panels, search results — anywhere a resource can be blank.

## Framing

An empty state is not a gap to be filled with an illustration. It is the one place in the product where the system gets to explain what lives here and how to make the first thing happen. Carbon's framing: empty states "provide opportunities to communicate what the user would see if they had data, while providing constructive guidance about next steps" [S1].

The governing constraint is cognitive cost, not delight. Carbon: "More content doesn't necessarily mean it's a better solution as there is a cognitive cost for having more content on the page. This is especially true when users first engage with your product, so save the more involved educational moments for primary features and more complex situations" [S1].

## The taxonomy

Carbon names **three** basic empty-state types [S1]:

| Type | Use cases | Goal | When to use |
|---|---|---|---|
| **No data** | First time use, no data yet | User understands what will appear once data is added, and how to add it themselves | Simpler situations, or secondary features where bite-sized information is preferable |
| **User action** | No search results; confirmation of process completion | User understands how to adjust search terms or filters, or that they finished successfully | Interaction-triggered feedback |
| **Error management** | Permissions issue; systems issue; configuration required | User understands the problem and, if corrective action exists, knows what to do | Something is amiss; a higher level of detail and specificity better supports the user |

Carbon's in-depth alternatives — **in-line documentation**, **onboarding**, and **starter content** — are additions for first use, not a fourth type. Its rule of thumb: "a primary resource on a page could benefit from a more educational approach, while basic empty states may suffice for secondary resources" [S1].

The taxonomy extends cleanly to the states a B2B product actually hits. Two additions beyond Carbon's three, marked as such:

| State | Trigger | Distinguishing feature |
|---|---|---|
| **Filtered out** | Facets or filters exclude everything | The data exists; the view is wrong. Say so and offer the way back |
| **Permission-restricted** | Role lacks the grant | Not an error and not emptiness — an authorisation boundary. Fold into error management if you use Carbon's taxonomy |

**Filtered out** is a separate case because the remedy is different. Polaris is explicit: "An empty resource and a filter that matched nothing need different wording. For a filtered result, tell merchants how to change the filter" [S4]. Shipping a generic "no results" for both is a real defect — it tells a user with 4,000 records that they have none.

**Permission-restricted** sits inside Carbon's error-management class, where the prescribed copy is "the user does not have permission to view the data" plus the instruction to "suggest steps or process to request access" [S1].

## Carbon's four recoverable failure classes

Carbon splits error-management empty states into four, each with a prescribed pair of messages [S1]:

| Error type | Explain why there is no data | Explain what the user can do |
|---|---|---|
| **Permissions issue** | The user does not have permission to view the data | Suggest steps or process to request access |
| **Systems issue** | Problems with a related system are preventing the data from being supplied | Explain steps the user can take to learn what has happened, e.g. viewing an activity log |
| **Configuration required** | Further configuration may be needed to access the data | Provide an explanation and the first step the user should take |
| **Action not supported** | e.g. the user attempts to upload an unsupported file type | Explain what file types are supported |

Carbon invokes Nielsen's ninth heuristic here — *Help users recognize, diagnose, and recover from errors* — and restates the requirement as plain: error messages "should be expressed in plain language (no codes), precisely indicate the problem, and constructively suggest a solution" [S1].

Carbon's design intent for this class: "A higher level of specificity is helpful here, with the aim that the user will be able to address the issue comfortably themselves" [S1].

## What an actionable empty state must contain

From Carbon's anatomy [S1] and Polaris' structure [S4]:

1. **What's missing, stated positively.** Carbon's title guidance: "A short and concise explanation. Where possible, write this as a positive statement. In this example, 'Start by adding data assets' feels more positive than 'You don't have any data assets.'" Polaris says the same from the other side: "A heading that says only 'No products' leaves merchants guessing. Name the cause in the heading and put the next step in the action" [S1] [S4].
2. **Why it is empty, and what populates it.** Carbon's body "should explain clearly the next action to populate the space. You may also explain why the space is empty and include the benefit of taking this step" [S1].
3. **The action.** Three permitted forms per Carbon: a primary action button beneath the copy, a primary action link inside the copy, or a pointer to the UI element itself — "Direct the user to the UI element… This has the benefit of teaching the user where elements are and how they will perform tasks in the future" [S1].
4. **Optional secondary action.** "If there is a secondary action, such as referencing documentation for further reading, include it as a link below the copy" [S1].
5. **Optional image.** Related to the situation, sized to the space; "If space is limited, use just text" [S1].

Polaris mirrors this with named slots — `heading`, optional `graphic`, optional `subheading`, one `primary-action`, one `secondary-actions` — and caps it: "up to two actions" [S4].

**Not found:** a sourced character or word count for the title or body. Carbon says "keep words to a minimum so they are fast to read and act upon" [S1] with no figure.

## Placement and layout rules

**Replace, don't overlay.** "Empty states should replace the element that would ordinarily show. For example, an empty state for a table would replace the table and the column headers and footer should not be present. This practice avoids having a screen reader read the entire table before getting to the message that there is no content" [S1]. The same applies to search: "if you search for something and there are no results, any underlying content should be replaced by the empty state message" [S1]. Polaris implements this as a component in the table body that "renders only when the body has no rows and the table isn't loading, and it spans every column" [S4].

**Alignment.** Left-aligned as a block. The one exception: in a small tile, the image centres above left-aligned text and action — "This exception was made to prevent the empty state looking too much like content, where it could be skipped over" [S1].

**Button hierarchy under repetition.** "In situations where there could be multiple empty states showing at once, we recommend using a tertiary button for the call to action. This avoids scenarios with multiple primary action buttons in the UI" [S1]. On a dashboard where several widgets fail simultaneously, that generalises further: "the repetition of the empty state may not have the same impact if you use illustrative icons. In this case, an empty state that uses just text may be preferable" [S1].

## Do not

- "Don't cover multiple options in one empty state. If there are multiple things a user can do, pick the most important and keep the focus on that action" [S1]
- "Don't use product-specific terms that the user may not yet understand" [S1]
- "Don't include content that is about other areas of the app. Be contextual" [S1]
- "Don't lead the user into a dead end. If there are useful next steps, include them" [S1]
- "Be respectful of the user and don't joke or use flippant language" [S1] — and note NN/g's parallel warning on no-results pages: users "may not be able to tell whether you are laughing with them, or laughing at them" [S3]

## Search-no-results specifics

NN/g's three guidelines for a zero-result state [S3]:

1. **Clearly explain that there are no matching results.** Their failure mode is real and measured: a test user "completely overlooked" a no-results message because it was "small, lightweight, and squeezed in between the site logo and the first bold heading" — the eyetracking gazeplot recorded no fixations on it. Users arrive with a strong expectation of a specific results layout and skip anything outside it.
2. **Offer starting points for moving forward.** Specifically: restating the original query, a search box with the original query still in it, suggestions for similar queries that do return results, spelling corrections, and advice on modifying queries.
3. **Don't mock the user.**

## Accessibility

- Carbon: empty-state illustrations are decorative and "should be skipped by screen readers. A decorative image… should be given either an empty `alt` tag or their `role` is assigned `presentation`. As an empty `alt` tag is more widely supported, we recommend you align with the WCAG guidance and avoid assigning `role` to `presentation` until support is more ubiquitous" [S1].
- The zero-result message is a status message and needs programmatic exposure. WCAG 4.1.3 names it directly: "brief text messages displayed *about* the completion or status of the search, such as 'Searching...', '18 results returned' or 'No results returned' would be status updates if they do not take focus or cause a page refresh" [S5]. Use `aria-live="polite"` [S6].
- Polaris limits worth knowing before you build a variant: the component "has no tones or variants. For status messaging that isn't about absent content, use banner" [S4]; and outside a table it "doesn't detect emptiness. Render it conditionally when your data set is empty" [S4].

## Empty vs loading

An empty state and a loading state are not interchangeable, and conflating them is a common bug. Polaris' table-scoped empty state renders "only when the body has no rows **and the table isn't loading**" [S4] — the loading state wins until the request resolves. Any empty-state component must be gated on request completion, not on "array is falsy".

## Not found

- **A character/word budget for empty-state copy.** Carbon and Polaris both say "concise" with no figure.
- **Whether illustration and animation belong in a B2B product empty state.** Carbon permits both and warns only against repetition [S1]; no source sets a rule of thumb by product maturity or audience.
- **A standard treatment for the empty state after all items are deleted** (distinct from never-populated). Carbon lists "cleared or deleted data" under in-line documentation use cases [S1] but does not differentiate the copy or treatment from first run.
- **Carbon's error-states pattern is documented as "(future)"** on the empty-states page [S1] — so a fuller error taxonomy does not yet exist in the source this file is built on.

## Sources

- **[S1]** https://carbondesignsystem.com/building-blocks/core/patterns/empty-states/ — IBM Carbon Design System, "Empty states" pattern (last updated Aug 11, 2026). Three types; four error-management classes; anatomy; do/don't; alignment and repetition rules; decorative-image accessibility; in-depth alternatives. Accessed 2026-10-05.
- **[S2]** https://carbondesignsystem.com/building-blocks/core/components/loading/guidelines/ — IBM Carbon Design System, "Loading" component guidelines (last updated Sep 28, 2026). Consulted for the loading-vs-empty boundary. Accessed 2026-10-05.
- **[S3]** https://www.nngroup.com/articles/search-no-results-serp/ — Nielsen Norman Group, Kathryn Whitenton, "3 Guidelines for Search Engine 'No Results' Pages" (Jan 5, 2014). Three guidelines; eyetracking oversight failure; no-mocking caution. Accessed 2026-10-05.
- **[S4]** https://shopify.dev/docs/api/app-home/latest/web-components/feedback-and-status-indicators/empty-state — Shopify, Polaris web components: Empty state (v1.1). Heading/graphic/subheading/action slots; say-why-then-what; empty vs filtered; table-body rendering; no tones. Accessed 2026-10-05.
- **[S5]** https://www.w3.org/WAI/WCAG21/Understanding/status-messages.html — W3C WAI, Understanding SC 4.1.3 Status Messages (Level AA; page updated May 11, 2026). "No results returned" named as a status message. Accessed 2026-10-05.
- **[S6]** https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-live — Mozilla Developer Network, "ARIA: aria-live attribute" (last modified Sep 23, 2025). polite / assertive / off semantics; empty-element announcement pattern. Accessed 2026-10-05.
