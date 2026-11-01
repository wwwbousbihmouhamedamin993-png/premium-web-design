# SaaS onboarding playbooks

Framing: onboarding is not a wizard. It is the work of getting a signed-in user to their first real
output, then removing every remaining reason they fail to return. The most useful distinction in the
primary literature is NN/g's between **push revelations** (information delivered out of context,
uninvited) and **pull revelations** (the user reaches for it when they need it). Push revelations
"interrupt users who are attempting to do something else at that moment, they don't tend to be memorable,
and they also don't result in better task performance" (NN/g, Onboarding Tutorials vs. Contextual Help).

## Time-to-first-value, before any checklist

Define the one moment the product is worth paying for, then instrument it. A checklist that does not
terminate in that moment is busywork with checkboxes.

| Product shape | First real value | Instrument as |
|---|---|---|
| Data tool | First record imported, a report produced | Import completed → report viewed |
| Integration product | First connection verified against live data | Connection verified |
| Workflow product | First workflow run that completed | First successful run |
| Analytics | First dashboard with non-zero data | Dashboard rendered with real rows |
| Collaboration | First shared object with a second person | Second member active |

**Not found:** no primary source consulted specifies a numeric time-to-first-value target, a
trial-to-paid milestone list, or an activation-rate benchmark. Any number in `DESIGN.md` is your
product's decision; do not source it to a general standard.

## The setup checklist pattern

Stripe's account checklist is the strongest published example, and its structure is directly copyable:
a **single named destination** — "Complete this checklist before taking your Stripe account live"; a
**persisted progress** model — "As you complete each item and check it off, **the state of each
checkbox is stored within your browser's cache**. You can refer back to this page at any time to see
what you've completed so far"; a **short, bounded item list** where each item pairs action with *why*
(Stripe recommends passkeys or security keys because they "are resistant to phishing. SMS-based 2FA is
vulnerable to SIM-swapping and interception, so use it only as a last resort"); **guidance on where the
item is done**, not just that it must be done; and a **terminal condition**, so completion is meaningful
rather than open-ended.

Note the persistence mechanism and its limit: browser cache is local and device-bound, and clearing it
loses the state. **A checklist that gates access to a product must persist server-side**; a checklist
that only guides may persist locally. Decide which you are building before you write the store.

Structural rules: progress is a count ("4 of 7 complete") plus a meter, in normal flow — never a toast or
a percentage in a modal. Prerequisites come first, locked, with the reason inline ("Connect Slack to
enable alerts"). Every item is one action and one destination; an item needing two things is two items.
Blockers are visually distinct from polish, because a must-do-before-use item is not the same class as an
optimisation. Completed items collapse to a compact confirmed list, still expandable for re-verification.
The checklist is always dismissible and always resumable — a blocking checklist is a `Decide`-surface
failure (`craft-floor.md`). And never render a checklist with nothing to do; hide it.

## Contextual versus blocking onboarding

| | Contextual (pull) | Blocking (push) |
|---|---|---|
| Trigger | The user reaches the surface that needs the knowledge | Login, or an arbitrary timer |
| Delivery | Inline, at the point of need, dismissible | Modal or full-screen takeover |
| Justified when | The knowledge is needed right now | The action is irreversible or billable without it |
| Fails when | Absent — the user never discovers the feature | The user has a task and you are delaying it |

NN/g's evidence for blocking: tutorials "interrupt users, don't necessarily improve task performance, and
are quickly forgotten." The mechanism they name is the paradox of the active user: "Users want to start
using the product right away. They don't want to spend time studying how to use your app… The interruption
posed by a tutorial is unwanted, so users skip it." Their positive example is architecturally instructive:
ArcGIS's onboarding "wasn't activated automatically the first time the user logged in but rather was made
available in the sidebar," making it "possible for the user to revisit the tutorial later, when they
inevitably forgot much of the information."

NN/g's three jobs for a new surface are the checklist's smaller sibling — an empty state should
"communicate system status to the user," "help users discover unused features and increase learnability of
the application," and "provide direct pathways for getting started with key tasks." And the failure to
avoid: declaring emptiness before the fetch finishes, then replacing it — users "initially encounter an
inaccurate system-status message 'No records.' This information would be highly useful if, in fact, there
were no records. However, after a few seconds of waiting, the system replaces the inaccurate
system-status message with the requested items." Loading is not empty; see `loading-skeletons.md`.

## The deployment and integration wizard

An integration wizard is a sequenced, resumable, per-step-committing flow.

- **One connection step per screen.** "Paste your API key", then "Choose the project", then "Map
  fields", then "Sync now", then "Done" — each independently committed and re-enterable.
- **Test the connection before asking for scope.** Never request a broad OAuth scope before proving the
  credential works.
- **Every step's state is recoverable.** A failed step 3 of 5 must not lose steps 1–2. This is a
  resumable process, not a modal wizard.
- **Show progress through the whole flow, persistently** — "Step 3 of 5" in the flow header, not only
  in the completion dialog.
- **A long-running step shows a live indicator with an estimate.** NN/g: "If the result will take more
  than 10 seconds to appear, you should also show users an estimate of when the computer will be
  finished." Their four reasons progress indicators help are worth keeping in the copy: they "reassure the
  user that the system is working and reduce the user's uncertainty," "give the user something to look at
  while waiting," "offer a reason to wait for the system to finish," and "can reduce users' perception of
  time."
- **Each step's failure is specific and retryable** — which step, what failed, what to change. Never a
  generic error at the end of a five-step flow.
- **Name the consequence of each scope request** at the point of consent, per `craft-floor.md`'s
  consequence-before-click rule.

## Trial-to-paid milestones

The trial is a `Decide` surface with a countdown. Design these as discrete, user-visible moments:

| Milestone | What the user is shown |
|---|---|
| Trial created | Exact duration, what happens at the end, the card on file or its absence |
| First use | Value confirmation, not upgrade pressure |
| Feature limits approached | Usage against limit, *before* it is hit |
| Limit hit | What stopped working, how to raise the limit, what happens next |
| Trial ending | Remaining time, the exact end date, the plan that will start, and the charge |
| Cancel intent | Confirmation that access continues until the end date |
| Post-cancel | The end date, what is lost, and the restore path |

Two hard rules: **never hard-cancel a trial silently** — the user must have had a real, dated notice
before anything is charged; and **a limit message is inline on the thing that broke**, not a modal (see
`usage-limits-quotas.md`).

## Checklist persistence across sessions

Match the store to the stakes. `localStorage` or cache survives a reload but is lost on a device clear
and is not portable — use it for non-blocking hints only. Server, per user, survives everything and is
portable across devices — use it for anything gating access. Server, per workspace, shares progress with
the team, which suits config steps where one person's completion helps everyone. The URL carries the
shareable "state" of a wizard, for a flow someone returns to by link.

If a checklist item has a real-world consequence — a connected account, an enabled feature — the
**resource** is the source of truth, not the checkbox. Derive completion by inspecting the resource, the
way Stripe's items are each independently verifiable in the Dashboard. A checkbox the client can set is a
checkbox the client can lie with.

## In-product guidance versus docs links

Both. They fail in opposite directions.

| | In-product guidance | Docs link |
|---|---|---|
| Best for | The 90% case; the thing being done right now | The long tail; configuration reference; API detail |
| Failure | Clutters the surface; goes stale | Sends the user out of their work; context is lost |
| Test | Did it prevent a mistake before it happened? | Did the user come back to the task? |

Rules: **at most one contextual hint per surface**, placed next to the control it describes, never
covering it. Every hint is dismissible and stays dismissed. A hint must be specific — "Add a receiving
address to enable webhooks", not "Learn more". A docs link opens in a new tab with
`rel="noopener noreferrer"`; MDN defines `noreferrer` as "No `Referer` header will be included.
Additionally, has the same effect as `noopener`." A support article that exists only in external docs
for a step that blocks use is a `Decide`-surface violation: the user cannot complete their own action
without leaving the product.

## Sources

- [Onboarding Tutorials vs. Contextual Help](https://www.nngroup.com/articles/onboarding-tutorials/) — Nielsen Norman Group, accessed 2026-10-05
- [Designing Empty States in Complex Applications: 3 Guidelines](https://www.nngroup.com/articles/empty-state-interface-design/) — Nielsen Norman Group, accessed 2026-10-05
- [Progress Indicators Make a Slow System Less Insufferable](https://www.nngroup.com/articles/progress-indicators/) — Nielsen Norman Group, accessed 2026-10-05
- [Account checklist](https://docs.stripe.com/get-started/account/checklist) — Stripe Documentation, accessed 2026-10-05
- [`rel` HTML attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel) — MDN, accessed 2026-10-05