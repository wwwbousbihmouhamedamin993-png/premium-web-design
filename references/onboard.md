# Onboard — first-run flows, empty states, activation

Refine command. `onboard` gets a signed-in user to their first real output, then removes every
remaining reason they fail to return. It is not a wizard skill; it is the work of the first session
and the first failures.

## The frame: pull, not push

NN/g's distinction is the whole command. **Push revelations** deliver information out of context,
uninvited; **pull revelations** arrive when the user reaches for them. Push interruptions "interrupt
users who are attempting to do something else at that moment, they don't tend to be memorable, and
they also don't result in better task performance." The mechanism NN/g names is the paradox of the
active user: "Users want to start using the product right away. They don't want to spend time
studying how to use your app… The interruption posed by a tutorial is unwanted, so users skip it."

Their architecturally instructive positive example: ArcGIS's onboarding "wasn't activated
automatically the first time the user logged in but rather was made available in the sidebar,"
making it possible to revisit the tutorial when the information was actually needed.

| | Contextual (pull) | Blocking (push) |
|---|---|---|
| Trigger | The user reaches the surface that needs the knowledge | Login, or an arbitrary timer |
| Delivery | Inline at the point of need, dismissible | Modal or full-screen takeover |
| Justified when | The knowledge is needed right now | The action is irreversible or billable without it |
| Fails when | Absent — the user never discovers the feature | The user has a task and you are delaying it |

## 1. Define time-to-first-value before drawing anything

Name the one moment the product is worth paying for, then instrument it. A checklist that does not
terminate in that moment is busywork with checkboxes. Per product shape
(`saas-onboarding-playbooks.md`): first record imported → report produced; first connection verified
against live data; first workflow run completed; first dashboard with non-zero data; first shared
object with a second person in it.

**No numeric target here.** No primary source consulted specifies a time-to-first-value target, a
trial-to-paid milestone list, or an activation-rate benchmark. Whatever number `DESIGN.md` records is
the product's decision — do not source it to a general standard.

## 2. Audit every first-run surface for its empty state

Every surface that fetches has an empty state, and the first-run one is the onboarding surface.
Carbon's framing: empty states "provide opportunities to communicate what the user would see if they
had data, while providing constructive guidance about next steps" — but "more content doesn't
necessarily mean it's a better solution as there is a cognitive cost for having more content on the
page."

What an actionable empty state carries (`empty-states.md`):

1. **What's missing, stated positively** — "Start by adding data assets" over "You don't have any
   data assets." Polaris from the other side: a heading saying only "No products" "leaves merchants
   guessing."
2. **Why it is empty and what populates it.**
3. **One action** — a primary button, a link in the copy, or a pointer to the control itself, which
   also teaches where things live.
4. Optional secondary action, and optional image. Carbon: "If space is limited, use just text."

**Replace, don't overlay.** An empty state replaces the element that would show — including the
table's column headers and footer — so "a screen reader [does not read] the entire table before
getting to the message that there is no content."

**Filtered-out is a different state from empty.** "An empty resource and a filter that matched
nothing need different wording. For a filtered result, tell merchants how to change the filter."
Shipping one generic "no results" for both tells a user with 4,000 records that they have none.

**Never declare emptiness before the fetch finishes.** Polaris' table empty state renders "only when
the body has no rows **and the table isn't loading**" — loading wins until the request resolves.
Gate on request completion, never on "array is falsy."

**Permission-restricted is not an error and not emptiness.** It is an authorisation boundary that
needs a route back (`roles-permissions-matrix.md`, `harden.md`).

## 3. The setup checklist, when the product needs one

Stripe's account checklist is the strongest published example: a single named destination, a
short bounded item list where each item pairs action with *why*, guidance on where the item is
done, and a terminal condition so completion means something.

| Element | Rule |
|---|---|
| Progress | A count ("4 of 7 complete") plus a meter, in normal flow — not a toast, not a percentage in a modal |
| Order | Prerequisites first, locked with the reason inline |
| Every item | One action, one destination. An item needing two things is two items |
| Blocker vs polish | Visually distinct |
| Completed | Collapse to a compact confirmed list, expandable for re-verification |
| Exit | Always dismissible, always resumable — a blocking checklist is a `Decide`-surface failure |
| Empty | Never show a checklist with nothing to do; hide it |

**Persist server-side if it gates access.** A checklist that gates a product must survive a device
clear; a checklist that only guides may persist in `localStorage`. And if an item has a real-world
consequence — a connected account, an enabled feature — **the resource is the source of truth, not
the checkbox.** Derive completion by inspecting the resource. A checkbox the client can set is a
checkbox the client can lie with.

## 4. Multi-step flows: resumable, per-step committed

For integration and setup wizards: one connection step per screen; test the connection before
requesting a broad OAuth scope; a failed step 3 of 5 must not lose steps 1–2; progress shown
through the whole flow ("Step 3 of 5"), not only in the completion dialog; each step's failure
specific and retryable — never one generic error at the end of a five-step flow; the consequence of
each scope request named at the point of consent.

Beyond ~10 seconds, an estimate is required (NN/g: "If the result will take more than 10 seconds to
appear, you should also show users an estimate"). Their four reasons progress indicators help are
worth keeping in the copy — reassurance that the system is working, something to look at, a reason
to wait, and reduced perception of time.

## 5. Split the screen when the surface is doing two jobs

Onboarding and first-run work is the most common source of over-packed routes. Use `page-composition.md`
and `visual-hierarchy.md` to split:

- A route doing more than two major jobs gets split. Nested cards 2–3 deep mean the split is overdue.
- The checklist belongs in the shell-adjacent region or a panel — not competing with the work area
  for the same visual weight. One dominant element per view.
- Polaris's Index template repeats the create action in both the page header and the empty state, so
  the entry point exists in two places without duplicating the primary-button budget.
- Settings is Focused class with a guarded save bar; onboarding is Focused class with no save
  semantics. Two different rooms.

## 6. In-product guidance versus a docs link

Both, because they fail in opposite directions. Guidance handles the 90% case and risks going
stale; a docs link handles the long tail and risks losing context. Rules: at most one contextual
hint per surface, placed next to the control it describes and never covering it; every hint
dismissible and staying dismissed; a hint must be specific — "Add a receiving address to enable
webhooks", not "Learn more". A support article that exists only in external docs for a step that
blocks use is a `Decide`-surface violation: the user cannot complete their own action without
leaving the product.

## Verify

- Delete all data (or use a fresh account) and walk every route: nothing renders a bare table, a
  centred spinner, or "Nothing here yet."
- Every empty state names the cause and offers exactly one primary action.
- Filter to an impossible combination and confirm the copy says the filter matched nothing.
- Throttle the network until the request is slow: no "no results" flashes before data resolves.
- Deny the current role and confirm a designed permission state with a request-access path.
- Return after a week: the checklist shows real progress, and nothing greets you with a modal.
- Render Focused class at 320px and check the measure holds 60–70ch, centred.

## Exit criteria

Time-to-first-value named and instrumented. Every fetching surface has a first-run empty state that
teaches the shape and offers one action. Checklists are resumable, dismissible, and server-derived
where they gate access. Push surfaces reduced to what genuinely blocks. Multi-step flows recover per
step. Documentation links are specific and non-blocking.

## Not found

- **A numeric time-to-first-value target, trial-to-paid milestone list, or activation benchmark.**
  Explicitly flagged as absent in `saas-onboarding-playbooks.md`; no primary source was consulted.
  Settled by: the product's own funnel data.
- **Whether illustrations and animation belong in a B2B product empty state.** Carbon permits both
  and warns only about repetition; no source sets a rule by product maturity or audience
  (`empty-states.md`).
- **A sourced character or word budget for empty-state copy.** Carbon and Polaris both say
  "concise" with no figure.

## Sources

Primary reference: `saas-onboarding-playbooks.md` (push vs pull, time-to-first-value, the checklist
pattern, wizard mechanics, persistence, guidance vs docs links). Supporting: `empty-states.md` (the
taxonomy, anatomy, replace-don't-overlay, filtered vs empty, accessibility), `page-composition.md`
(templates, action budgets), `visual-hierarchy.md` (one dominant element, DOM order),
`roles-permissions-matrix.md` (denials are content), `loading-skeletons.md` (loading vs empty),
`production-launch-checklist.md`, `i18n-rtl.md`.

External pages cited above, all previously opened by this skill:

- Onboarding Tutorials vs. Contextual Help (push interruptions; paradox of the active user;
  ArcGIS sidebar onboarding) — Nielsen Norman Group.
  https://www.nngroup.com/articles/onboarding-tutorials/ — accessed 2026-10-05.
- Designing Empty States in Complex Applications: 3 Guidelines (communicate system status;
  discoverability; direct pathways; the "No records" before-fetch failure) — Nielsen Norman Group.
  https://www.nngroup.com/articles/empty-state-interface-design/ — accessed 2026-10-05.
- Progress Indicators Make a Slow System Less Insufferable (estimate beyond 10s; four reasons
  indicators help) — Nielsen Norman Group. https://www.nngroup.com/articles/progress-indicators/ —
  accessed 2026-10-05.
- Empty states (three types; four error-management classes; anatomy; replace not overlay;
  decorative images skipped by screen readers; tertiary button under repetition) — Carbon Design
  System (IBM). https://carbondesignsystem.com/building-blocks/core/patterns/empty-states/ —
  accessed 2026-10-05.
- Polaris Empty state web component (heading/graphic/subheading/action slots; empty vs filtered
  wording; renders only when not loading; "up to two actions") — Shopify, shopify.dev.
  https://shopify.dev/docs/api/app-home/latest/web-components/feedback-and-status-indicators/empty-state
  — accessed 2026-10-05.
- Polaris Index and Settings templates (create action in header and empty state; Save Bar API) —
  Shopify, shopify.dev. https://shopify.dev/docs/api/app-home/patterns/templates/resource-index ·
  https://shopify.dev/docs/api/app-home/patterns/templates/settings — accessed 2026-10-05.
- Account checklist (single named destination; persisted checkbox state; action-plus-reason items) —
  Stripe Documentation. https://docs.stripe.com/get-started/account/checklist — accessed 2026-10-05.
- Understanding SC 4.1.3 Status Messages ("No results returned" named as a status message) —
  W3C WAI. https://www.w3.org/WAI/WCAG21/Understanding/status-messages.html — accessed 2026-10-05.
- `rel` (`noopener` / `noreferrer` semantics for docs links) · `aria-live` — MDN.
  https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel — accessed 2026-10-05.

**House process, not sourced fact:** the section ordering, the split-the-screen criteria in step 5,
the verification sequence, and the exit criteria. The push/pull distinction, the checklist anatomy,
and the empty-state rules are cited to their vendors; no activation metric is invented.