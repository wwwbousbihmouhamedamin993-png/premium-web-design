# Harden — errors, edge cases, permissions, offline, long lists

Fix command. `harden` assumes the happy path works and attacks everything else. The scope is the
surface's failure modes, not its features.

**The stated weakness of the industry is here.** Carbon's own documentation lists Error states and
Onboarding as *"(future)"* patterns, so there is no mature vendor spec to copy — this playbook is
assembled from primary sources with the gaps declared (`error-states.md`).

## 1. Enumerate the failure surface first

For every route and every data region, write the list. Nothing else can proceed without it:

| Axis | Cases to name |
|---|---|
| Request | Slow, failed, timed out, partially returned, cancelled by the user, retried |
| Data | Empty, filtered-to-nothing, one row, 100k rows, malformed, stale |
| Identity | Signed out mid-task, session expired, no permission, wrong workspace |
| Network | Offline, captive portal, VPN reachable-but-API-unreachable, flaky |
| Input | Too long, wrong format, at the boundary, unicode and RTL, duplicate on submit |
| Entitlement | Quota exceeded, trial expiring, plan downgraded, read-only, feature not in plan |
| Environment | 320px viewport, 200% zoom, `forced-colors`, `prefers-reduced-motion`, no JS |

A row that cannot be named cannot be hardened.

## 2. Errors: recognize, diagnose, recover

Nielsen's ninth heuristic is the frame — every rule serves one of those three verbs. Errors must be
"expressed in plain language (no codes), precisely indicate the problem, and constructively suggest
a solution" (Carbon).

**Never appears** (`error-states.md`): raw server strings (stack traces, ORM fragments, JSON
payloads, exception class names); generic "something went wrong"; error codes as primary content;
blame ("invalid", "illegal", "incorrect"); premature errors on untouched fields; tooltips as the
error channel; timed dismissal on critical messages; a modal for anything short. If support needs
the diagnostic, surface it as a **copyable reference ID**, not as the message.

**Timing — pick one and apply it product-wide.** Carbon recommends validating as soon as a field
loses focus; GOV.UK says never validate on blur. NN/g reconciles them: "Presenting errors too early
is a hostile pattern" but "do consider inline, real-time errors for error-prone interactions where
users are unlikely to enter the correct information on their first try." Default: validate on
submit; validate on blur only for demonstrably error-prone fields. Mixing per-form is the defect.

**Severity maps to surface.** NN/g: messages needing minimal interaction get labels, toasts, or
banners; modals "should be reserved for severe errors." Repeated failure is a design defect — three
or more occurrences in one attempt signals a deeper issue with the messages, the design, or the
requirements.

**Announce, don't just paint.** SC 4.1.3 Status Messages (AA): status must be "programmatically
determined through role or properties such that they can be presented to the user by assistive
technologies **without receiving focus**." Put `aria-live` on an **empty** element in markup and
write the text into it on update. Reserve `assertive` for imperative interruptions.

**Operations over 10s** show percent-done and a cancel control. Response-time ladder: 0.1s feels
instantaneous · 1.0s keeps flow of thought intact · 10s holds attention.

## 3. Offline and stale

**Detection is a hint for the UI, never a gate on functionality.** MDN on `navigator.onLine`: the
property is "inherently unreliable, and you should not disable features based on the online status,
only provide hints when the user may seem offline" — LAN counts as online, and on Windows reachability
of a Microsoft home server can be blocked by a VPN while the internet works.

Two affordances, not interchangeable:

- **Current-state notice** — the connection is bad *now*: "You seem to have a bad network
  connection… Messages will be sent when the network is restored."
- **Age-of-data notice** — the record may be out of date: show the last update time.

The governing contrast: **auto-update where stale data is useless; show the timestamp where the
user might act on it.** A B2B record list is the second case. Also required: tell the user both the
application's state and the actions they can still take; make clear whether the fault is "The
network is down" (theirs) or "You are disconnected" (yours); use per-element state rather than one
global grey-out, since "using grayed UI to show that your app is offline can cause confusion about
what the app can do while offline"; never convey state with colour or an icon alone; and prefer
action-based language, because "Non-technical audiences often misunderstand the word 'offline'."

**Don't block content.** "Avoid network requests that block content. Let the user continue to browse
your app and queue tasks that will be performed and synced when the connection has improved"
(web.dev). A full-screen modal blocking on a sync is the failure being described.
`registration.sync` is the queue — **limited availability, secure context (HTTPS) only** — so gate
it and keep a foreground retry path.

## 4. Permissions, entitlements, and long lists

**A denial is content, not absence.** A permission-denied pane with no route back is a dead end and
reads as a bug. It needs the cause, the request-access path, and who to ask. Carbon's class splits
the copy: permissions and configuration are the user's to fix; **systems errors may not be** — a
systems error whose only remedy is a Retry button, with no scope or cause, fails "diagnose."
Use the three-tier vocabulary from `roles-permissions-matrix.md` — permission → job → role — so the
matrix stays readable; a matrix of only permissions produces a thousand-cell grid nobody reads.
Denials are enumerated in the UI, not silently filtered, and scope-within-a-scope is visible on the
row. Entitlement surfaces (`usage-limits-quotas.md`): usage against a limit **before** it is hit;
when hit, inline on the thing that broke — never a modal; trial ending with the exact end date, the
plan that will start, and the charge; never a silent hard cancel.

Virtualise when the **rendered row count** is the bottleneck, not when the record count is large.
Fixed row height virtualises freely; **variable row height virtualises only with care** — AG Grid:
"You cannot use variable row height when using either the Viewport Row Model or the Infinite Row
Model… these row models need to work out the position of rows that are not loaded and hence need to
assume the row height is fixed." Three costs that bite:

- **Auto-size cannot see what isn't rendered** — "The grid works out the best width by considering the
  virtually rendered rows only."
- **Block eviction breaks shift-click selection** when `maxBlocksInCache` does not cover the range.
- **The DOM is the accessibility bill.** Screen readers "assume all elements of the grid are loaded
  when the page is loaded"; fix DOM order with `ensureDomOrder: true` (traded against animations)
  and declare the true size with `aria-rowcount` plus `aria-rowindex` on every rendered row.
  AG Grid recommends disabling sticky group rows outright — they put rows "in 'incorrect order' and
  result in inconsistent announcements for row indices."

Past the threshold in `craft-floor.md`, an unbounded scroll with no floor is a defect: pagination or
infinite scroll needs a real end state (`pagination-infinite-scroll.md`).

## 5. Secrets, keys, and irreversible actions

Developer-facing settings are where hardening is least optional (`api-keys-webhooks.md`). The
once-only reveal is a modal whose close is **blocked until the operator confirms a storage
location** — the note field is what makes a lost key recoverable, so it is not decoration. Show the
environment in the banner, because the rules differ: Stripe reveals live keys **it created for you**
but "if you create a secret key yourself, you can't reveal it after you've seen it once," and
sandbox keys are always visible. Publishable keys are exempt; masked keys show only a tail.

For irreversible actions, climb the destructive-confirmation ladder only as far as irreversibility
demands (`modals-dialogs-drawers.md`): 0 undo-first · 1 inline confirm with Undo · 2 `alertdialog`
with the safest action focused · 3 `alertdialog` naming the affected object · 4 type-to-confirm.
Never `window.alert()`/`confirm()`.

## Verify

- Kill the network mid-request at three points: before, during, after the response starts.
- Force a permission denial for the current role on every region; confirm a path back exists.
- Exceed a quota and confirm the message is inline on the thing that broke.
- Load a 9,000-row list with the screen reader on: row indices must announce as "row N of 9,000."
- Sort a virtualised table and confirm focus does not reset to the top.
- Force `forced-colors: active`, `prefers-reduced-motion: reduce`, 320px, and 200% zoom.
- Paste a 2,000-character name, an RTL string, and a `+35%` expansion into every field and cell.
- Trigger the same error three times in one attempt and read the messages as a new user would.
- Confirm every operation over 10s has a cancel and an estimate.

## Exit criteria

Failure surface enumerated and each case designed. No raw server string or generic message anywhere.
Error timing consistent product-wide. Offline handled as hints, never as feature gates, with both
notices distinguished. Denials designed with routes back. Long lists windowed with correct ARIA
counts, or paginated with a real end state. Secrets once-only with a storage-location note.
Irreversible actions at the right rung of the ladder. `accessibility-web.md` and
`production-launch-checklist.md` green.

## Not found

- **A comprehensive vendor error-state specification.** Carbon's Error states pattern is documented
  as *"(future)"* on its own empty-states page, so no fuller error taxonomy exists in the primary
  source this file is built on (`empty-states.md`). Settled by: a dated vendor design-system
  release that ships the pattern.
- **A sourced character limit for form error text.** Carbon gives line counts for notifications and
  a word count for action labels only (`error-states.md`).
- **A normative row count at which virtualization becomes required.** TanStack's guidance is
  qualitative ("a few thousand rows or less" for client-side pagination); no standard sets a
  threshold.
- **A bounded retry policy.** No primary source consulted specifies a backoff ceiling or a
  user-facing maximum retry count.

## Sources

Primary references: `error-states.md` (error surfaces, Carbon's four failure classes, what must
never appear, validation timing, announcing errors), `offline-stale-sync.md` (`navigator.onLine`
reliability, the two notices, background sync, web.dev's guidance), `roles-permissions-matrix.md`
(permission → job → role, scopes, denials as content), `virtualization-lists.md` (when to
virtualise, windowing mechanics, the accessibility cost), `api-keys-webhooks.md` (secret shown once,
key types, rotation, delivery states). Supporting: `empty-states.md`, `loading-skeletons.md`,
`pagination-infinite-scroll.md`, `usage-limits-quotas.md`, `modals-dialogs-drawers.md`,
`data-tables.md`, `production-launch-checklist.md`, `accessibility-web.md`, `forms-validation.md`,
`i18n-rtl.md`.

External pages cited above, all previously opened by this skill. Accessed 2026-10-05.

| Source | Used for | Publisher |
|---|---|---|
| `navigator.onLine` ("inherently unreliable… should not disable features based on the online status") · `navigator.connection` / `NetworkInformation` (limited availability) · Background Synchronization API (limited availability; secure context only) · `aria-live` — https://developer.mozilla.org/en-US/docs/Web/API/Navigator/onLine · https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/sync | offline detection reliability, sync queue, announcements | MDN |
| Handle intermittent connectivity — https://web.dev/articles/offline ("Don't block content"; the two notices; per-element state; whose fault; grey-out confusion) | §3 | Google / web.dev |
| Response Times: The 3 Important Limits — https://www.nngroup.com/articles/response-times-3-important-limits (0.1 s / 1.0 s / 10 s; percent-done beyond ~10 s) and Error Message Guidance — https://www.nngroup.com/articles/error-message-guidelines/ (proximity; redundant indicators; precisely describe; offer remedies; no blame; preserve work; repeated failure; severity → surface) | §2, §5 | Nielsen Norman Group |
| Empty states — https://carbondesignsystem.com/building-blocks/core/patterns/empty-states/ (four recoverable failure classes; plain-language rule; specificity) | §2, §4 | Carbon Design System (IBM) |
| Roles in an organization — https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/roles-in-an-organization and Custom roles — https://docs.stripe.com/get-started/account/teams/custom-roles (permission → job → role; scopes; outside collaborators) | §4 | GitHub Docs · Stripe Docs |
| API keys — https://docs.stripe.com/keys (live-mode reveal only for keys Stripe created; self-created keys not revealable; sandbox always visible; recovery impossible) and Restricted API keys — https://docs.stripe.com/keys/restricted-api-keys (tri-state Read/Write/None, default `None`, write implies read) | §5 | Stripe Documentation |
| Alert and Message Dialogs Pattern — https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/ (`alertdialog`; least destructive action focused; focus returns to the invoker) | §5 | W3C WAI ARIA APG |
| Row height — https://www.ag-grid.com/javascript-data-grid/row-height/ and Accessibility — https://www.ag-grid.com/javascript-data-grid/accessibility/ (variable row height limits; buffer; `maxBlocksInCache`; auto-size; `ensureDomOrder`; `aria-rowcount`/`aria-rowindex`; sticky group rows) · https://tanstack.com/table (pagination viable to a few thousand rows) | §4 | AG Grid · TanStack |
| Understanding SC 4.1.3 Status Messages (AA) · SC 3.3.1 Error Identification (A) · SC 1.4.10 Reflow · SC 2.2.2 Pause, Stop, Hide — https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html | §2, §1 | W3C WAI |

**House process, not sourced fact:** the failure-surface enumeration table in step 1, the
per-topic ordering, the verification sequence, and the exit criteria. Every threshold referenced
(10s, 24×24, 320px, 200%) is cited or routed to the file that cites it; no retry ceiling or
virtualization threshold was invented.