# Loading, skeletons, progress

Applies to: any async region in a logged-in product surface — route loads, table and list fetches, widget grids, mutations, saves.

## The time budget

Three perceptual limits, from Jakob Nielsen's 1993 *Usability Engineering* essay [S1]:

| Limit | Perception | Required feedback |
|---|---|---|
| **0.1s** | Instantaneous; user feels they are manipulating the object directly | None beyond showing the result |
| **1.0s** | Flow of thought uninterrupted, but the user notices the delay | None formally required; they lose the feeling of directly operating on the data |
| **10s** | Attention held on the dialogue | **Past 10s a percent-done indicator is required**, plus "a clearly signposted way for the user to interrupt the operation" [S1] |

The same essay warns against over-shooting in the other direction: for operations taking **2–10 seconds**, "a true percent-done indicator may be overkill and, in fact, putting one up would violate the principle of display inertia (flashing changes on the screen so rapidly that the user cannot keep pace or feels stressed)" [S1].

NN/g's later guidance (Katie Sherwin, 2014) splits the middle band by indicator type [S2]:

- **Under 1.0s** — no indicator. A looped animation here is distracting; the user cannot keep up and may feel anxious about what flashed.
- **2–10s** — looped animation (spinner). It says only that work is happening, not how long it will take.
- **10s or more** — percent-done. This is the most informative form and the one the 10s limit obliges.

**Not use:** static indicators ("Loading…", "Please wait") — they carry no state, so a hung request looks identical to a working one [S2]. **Not use:** "don't click again" warnings — they beg the user to read a threat they will not read, and the fix is to show that the first click was accepted [S2].

**Interrupt affordance is part of the 10s obligation**, not an optional extra [S1]. NN/g concurs: "For actions that take a little while, give users the option to stop the process, in case they decide they cannot wait. Otherwise, your design may be hijacking control of the system" [S2].

## Why a bare centred spinner on a blank page is a defect

- Carbon's loading pattern: "For full-screen loads, skeleton states are preferred over indicators to create a smoother experience" [S3].
- Carbon's loading component: a loading indicator is for "the entire page or a key section… after a user submits or saves data"; use it when "the expected wait time exceeds three seconds" [S4].
- A spinner with nothing else on screen tells the user nothing about scope, position, or progress. If it is also unbounded, "users cannot be sure if the system is still working or if it's stopped, so they may decide to abandon the task entirely" [S2].
- An unbounded spinner is the default failure mode of shipped component libraries. Polaris documents it plainly: the spinner "continues spinning indefinitely until you remove it. It doesn't automatically stop after a timeout or show error states. You must implement timeout logic and error handling yourself" [S5].

The measurable payoff is real: a University of Nebraska-Lincoln study cited by NN/g found users who saw a moving progress bar "experienced higher satisfaction and were willing to wait on average 3 times longer than those who did not see any progress indicators" [S2].

## Skeleton rules

Carbon's skeleton states are "simplified versions of components used on an initial page load… They should only appear for only a few seconds, disappearing once components and content populate the page" [S3].

Where skeletons are allowed:

- **Container-based components** — tiles, structured lists.
- **Data-based components** — data tables, cards [S3].

Where they are not:

- **Action components** — buttons, input fields, checkboxes, toggles [S3].
- **Toast notifications, overflow menus, dropdown items, modals, and loaders** — never. "Elements inside a modal may have a skeleton state, but the modal itself should not" [S3].

Motion is not decoration here: skeleton states "use motion to convey that the page is not stuck and that data is still being loaded", which reduces user uncertainty [S3].

**Not found:** an explicit rule that skeleton placeholders must be dimensionally identical to the final content. No primary source states this as a requirement. The closest substantiated version is Carbon's progressive-loading guidance that a 600×600px image may be represented as "a 600 x 600px area of white space until the full image loads" [S3] — i.e. reserve the box so nothing shifts. Settling it as a general rule would need Carbon's loading-pattern GitHub issue history or a layout-stability requirement in a spec (CLS guidance is the nearest formal candidate, and neither Carbon nor Polaris cites it for skeletons).

## Progressive loading

Carbon's ordering for a batched page load [S3]:

| Batch | Contents |
|---|---|
| Primary | Page basic structure (skeleton versions of container components), data-based text skeletons, **non-data text rendered for real** |
| Later | Images, content outside the viewport, interactive (action-based) components |

Non-data text — headings, labels, static copy — should be real in the first batch. It costs nothing and it gives the user something to read.

Carbon also allows Load more as a progressive mechanism for long lists backed by a database [S3].

## Indicator choice matrix

| Situation | Indicator | Source rule |
|---|---|---|
| Data fetch replacing a known layout (table, card grid, tile) | Skeleton | [S3] [S4] |
| Full-page submit/save, whole app processing | Full-screen loading indicator + semi-transparent overlay | [S4] |
| Single component processing (invite sent, row updated) | Inline loading | [S3] [S6] |
| Work is measurable (n of m records, bytes) | Progress bar / percent-done | [S1] [S2] |
| Work will exceed ~10s | Percent-done **plus** a cancel/interrupt control | [S1] |
| Page or filter change, slow multi-source view | Skeleton + progressive batches | [S3] |
| Save after button click | Small inline spinner inside/near the trigger, button disabled | [S4] |

Carbon's inline loading component has four states — inactive, active, finished, error — and the finished state "is active for 1.5 seconds before calling an optional function `onSuccess`" [S6]. Its label must change with state: "Saving…" → "Saved", and on error it must change to tell the user a failure occurred [S6]. Two prohibitions: no inline loading for full page loads (use skeletons), and no inline loading on more than one item or action at a time, "unless on initial page load or refresh" [S6].

Carbon: "Refrain from using multiple loading indicators simultaneously, as it may overwhelm users" [S4]. If a process runs longer than a few minutes, move to a notification [S3].

Polaris: "Display spinners when loading takes longer than 500ms" [S5] — tighter than Carbon's three-second floor [S4]. Where they conflict, the stricter one wins; the two are measuring different things (action feedback vs. page-level load).

## Partial and stale data

Showing real data immediately and upgrading it in place is better than blocking, and it must be labelled.

- NN/g on live regions: for content that "gets updated too… real-time sports scores, news crawlers, and stock market tickers", use `aria-live="off"` — do not announce every tick [S7].
- Set `aria-busy="true"` on the region being replaced, then `false` when the new content is in place; this stops the screen reader announcing partial updates [S8].
- Where the figure shown is older than the server's, mark it. web.dev's offline guidance treats "show the last time they were updated" as a legitimate first-class treatment for data where age matters [S9].

## Announcing async state

Every async state change needs a programmatic signal, not just paint.

- WCAG 4.1.3 Status Messages (AA): status messages must be "programmatically determined through role or properties such that they can be presented to the user by assistive technologies without receiving focus" [S10]. Named examples include a busy icon announced as "application busy", "Searching...", "18 results returned", and "No results returned" [S10].
- `aria-live="polite"` — announce at the next graceful opportunity. Default for load completions and counts [S7].
- `aria-live="assertive"` — interrupt immediately, potentially clearing the speech queue. MDN's warning applies directly to loading UI: "Because an interruption may disorient users or cause them to not complete their current task, don't use the `assertive` value unless the interruption is imperative" [S7].
- Put `aria-live` on an **empty** element in the markup, then write the announcement into it on update. The element is not given focus [S7].
- Carbon: "A screen reader should notify a user if an application is loading, busy, gets stuck, or if a process fails" [S3]. Note *gets stuck* and *fails* — a timeout or failure needs its own announcement, which the spinner will not make for you.

## Failure is part of loading

Polaris' migration note states the obligation plainly: "A page that removes the skeleton but has no failure state isn't complete" [S11]. Every skeleton and every spinner needs a defined terminal: loaded, empty, or error. Ship the timeout yourself; the component will not [S5].

Polaris' `SkeletonPage` mapping is the useful precedent for keeping structure stable: title → real route heading when known, body → labelled spinner inside a stable `s-section` ("Keep the page structure stable and replace the region when data arrives"), and actions → "Hide unavailable actions or render real disabled actions with an explanation. Don't display controls that look actionable but have no outcome" [S11].

## Not found

- **A numeric minimum skeleton display duration.** Carbon says "a few seconds" [S3]; no source gives a figure.
- **The rule that skeletons must match final content dimensions.** See above — substantiated only for reserved image boxes [S3].
- **A sourced threshold at which a determinate bar should be faked.** NN/g recommends starting animation slower and accelerating, because "exceeding customer expectations always creates more satisfaction than disappointing customers" [S2] — but publishes no numbers.
- **Whether an uncancellable >10s operation is acceptable in B2B admin.** Nielsen's 10s rule assumes an interrupt path [S1]; no source addresses long-running batch jobs that cannot be cancelled.

## Sources

- **[S1]** https://www.nngroup.com/articles/response-times-3-important-limits/ — Nielsen Norman Group, Jakob Nielsen, "Response Times: The 3 Important Limits" (Jan 1993; web update 2014). 0.1s / 1.0s / 10s limits; percent-done required past 10s plus a signposted interrupt; 2–10s display-inertia caution. Accessed 2026-10-05.
- **[S2]** https://www.nngroup.com/articles/progress-indicators/ — Nielsen Norman Group, Katie Sherwin, "Progress Indicators Make a Slow System Less Insufferable" (Oct 2014). Indicator-type bands; looped vs percent-done; ban on static indicators and don't-click-again warnings; Nebraska study; cancel affordance. Accessed 2026-10-05.
- **[S3]** https://carbondesignsystem.com/building-blocks/core/patterns/loading/ — IBM Carbon Design System, "Loading" pattern (last updated Aug 11, 2026). Skeleton scope and bans; progressive-loading batches; Load more; WCAG loading/busy reference. Accessed 2026-10-05.
- **[S4]** https://carbondesignsystem.com/building-blocks/core/components/loading/guidelines/ — IBM Carbon Design System, "Loading" component guidelines (last updated Sep 28, 2026). Three-second threshold; full-screen vs inline sizing; overlay behaviour; multiple-indicator ban. Accessed 2026-10-05.
- **[S5]** https://shopify.dev/docs/api/app-home/latest/web-components/feedback-and-status-indicators/spinner — Shopify, Polaris web components: Spinner (v1.1). 500ms guidance; indeterminate-only; no timeout or error state; scoping and labelling. Accessed 2026-10-05.
- **[S6]** https://carbondesignsystem.com/building-blocks/core/components/inline-loading/guidelines/ — IBM Carbon Design System, "Inline loading" component guidelines (last updated Sep 30, 2026). Four states; 1.5s success state; label copy; prohibitions. Accessed 2026-10-05.
- **[S7]** https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-live — Mozilla Developer Network, "ARIA: aria-live attribute" (last modified Sep 23, 2025). polite/assertive/off semantics; assertive warning; empty-element pattern; live-update use for tickers. Accessed 2026-10-05.
- **[S8]** https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-busy — Mozilla Developer Network, "ARIA: aria-busy attribute" (last modified Jun 23, 2025). Defer announcements until loading completes. Accessed 2026-10-05.
- **[S9]** https://web.dev/articles/offline-ux-design-guidelines — Google / web.dev, Kurtuldu & Steiner, "Offline UX design guidelines" (Nov 10, 2016). Last-updated display; not blocking content; syncing on reconnection. Accessed 2026-10-05.
- **[S10]** https://www.w3.org/WAI/WCAG21/Understanding/status-messages.html — W3C WAI, Understanding SC 4.1.3 Status Messages (Level AA; page updated May 11, 2026). "application busy" and "18 results returned" examples; sufficient techniques ARIA19/ARIA22/ARIA23/ARIA25; failure F103. Accessed 2026-10-05.
- **[S11]** https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/skeleton-page — Shopify, "Migrate SkeletonPage from Polaris React". Structure-stability mapping; no-outcome-controls ban; failure state required. Accessed 2026-10-05.
