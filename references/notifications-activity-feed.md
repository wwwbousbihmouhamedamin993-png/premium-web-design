# Notifications and activity feeds

Framing: the notification inbox and the activity log are different surfaces with different jobs, and
conflating them is the most common structural mistake. NN/g's taxonomy is the cleanest available cut:
an **indicator** makes an element stand out, a **validation** is an error about a user's input, and a
**notification** is "informational messages that alert the user of general occurrences within a
system… they usually inform the user of a change in the system state or of an event that may be of
interest" (NN/g, Indicators, Validations, and Notifications). Only the third belongs in the inbox.

## Activity log vs notification

| | **Notification inbox** | **Activity / audit log** |
|---|---|---|
| Content | Items addressed *to this user* | Every event, for anyone with read access |
| Cardinality | Filtered, often grouped | Complete, chronological, immutable |
| Owner | Per-user read state and settings | Shared; read state per-user at most |
| Retention | Weeks, then archived or pruned | Long, exportable, the compliance record |
| Route | `/notifications` | `/activity` or an admin sub-tab |
| Marking read | Core mechanic | Rarely a row-level action |
| Failure mode | Notification fatigue (NN/g's "Alert Fatigue") | An unreadable wall of rows — see `data-tables.md` |

Rule: **if the item is addressed to someone by name, it is a notification. If it merely happened, it is
activity.** Overlap is fine; the two surfaces must not be the same list.

## Grouping and unread

Group by day at minimum ("Today", "Yesterday", a date), then by object when volume justifies it ("in
*Acme Corp*"). Carbon's notification anatomy is Icon, Title, Body, Close button — a group header is a
container concern, not a notification variant (Carbon, Notification).

**Unread is conveyed by weight and a marker — never by colour alone.** NN/g names the mechanism:
"Typographical variations can also be used as indicators; examples include the common convention of
**boldfacing unread email messages** or color-coding stock symbols." NN/g also constrains where an
indicator may live: indicators "are **contextual**… associated with a UI element or with a piece of
content, and should be shown in close proximity to that element"; "are **conditional** — they are not
always present"; and "are **passive**. They do not require that a user take action." An unread dot on
the bell satisfies all three. Cap the badge: Carbon's header rule is about ordering rather than
magnitude — "Notifications should be 3rd from the right when paired with the account and switcher icon"
(Carbon, UI shell header).

## Categories and per-category settings

The inbox is a **rendered view of a preference set**. Design both halves, or you ship settings that
cannot express the inbox. A workable default set: **mentions and assignments** (someone names you on a
record) and **approvals requested** (a `Decide` item waiting on you) are in-app always on with email default
on; **comments and replies** and **status changes on watched records** are in-app with email default off;
**assignments and due dates** are in-app with email default on; **billing and security** go to the account
owner on both channels and are not disableable.

**Per-user, not per-workspace.** Stripe's model is the precedent: "If multiple team members have access to
your account, **each one can set their own notification preferences**," for both email and SMS (Stripe,
Account checklist). Notification settings belong to a person, not to a tenant or project. Two hard rules
follow: **some channels are not user-disableable** — security and billing events stay on, rendered as
non-toggleable rows with the reason inline, never as switches that lie; and **a category with everything
off needs a fallback** — if in-app is off, the inbox is no longer the source of truth, so say where it will
appear, or do not offer the switch.

Carbon's `actionable` variant is the pattern for a notification that **carries a decision** — "Actionable
notifications allow for interactive elements within a notification styled like an inline or toast
notification" — and it belongs in the inbox row, never in a toast. For system-generated classifications on
objects (order status, sync state), use a **badge** instead: Shopify defines the badge as "a compact visual
indicator" for "object states, order statuses, or system-generated classifications," and is explicit that
"for user-created labels, categories, or tags, use `chip` instead" (Shopify, Badge).

## The inbox surface

Structure: **a list route, not a popover.** A bell with an unread dot that opens a popover is a
notification *indicator*; the inbox is a separate destination where items are read, filtered, archived,
and marked read at volume. Carbon's own framing: notifications "are disruptive and should be used
sparingly," and while Carbon supports only inline, toast, actionable, and modal variants, "some product
teams also support banners and notification centers."

Each row: actor avatar or initial, a verb-phrase accessible title ("Priya commented on *Q3 Forecast*"),
timestamp, and — for anything actionable — the action itself, plus mark read/unread, archive, and a link
to the object.

Carbon's notification **statuses** map to severity, not to inbox categories: Informational (Blue),
Success (Green), Warning (Yellow), Error (Red). Note Carbon's carve-out, which the inbox adopts: "All
notification variants, **except for callout**, typically serve as feedback after an action or task is
completed. The callout variant is unique, as it provides guidance before users begin a task." Inbox rows
report events; they do not guide.

## Marking read

Mechanics: mark read when the row becomes visible; mark read when the user follows the link to the object;
a per-row "Mark as read/unread" so the row is actionable **without** navigating; one "mark all read"
control at the top, **never** automatic and never destructive; and optimistic flips with a revert message
on failure.

Read state is **per user and never shared**. Marking read must not delete; archiving must not imply read.
Unread to read is one-way in most inboxes, but "mark as unread" must exist — it is the only way back to a
thread the user could not finish.

**Not found:** no primary source consulted specifies whether opening an inbox marks all visible items
read or only the focused one, nor an unread-count cap, nor an auto-archive window. State the choice in
`DESIGN.md`.

## Pagination of a feed

An inbox is a scroll-loaded stream of `article`s, and APG's **feed** pattern is built for it: "A feed is a
section of a page that automatically loads new sections of content as the user scrolls. The sections of
content in the feed are presented in `article` elements." It is deliberately "a **structure, not a
widget**," which is what lets assistive technologies default to reading mode. Using it obliges you to:
put `role="feed"` on the container and `role="article"` on each item; support `Page Down`/`Page Up` to
move between articles and `Control`+`End`/`Home` to move past and before the feed (APG); **set
`aria-busy="true"` before adding or removing articles and `false` when done**, and avoid mutating the
middle of the feed (WAI-ARIA 1.3); make each article focusable — `tabindex="-1"` or `0` — and scroll it
into view on focus (WAI-ARIA 1.3); and document the keyboard interface, which APG calls "especially
important" precisely because the feed role has no established convention to inherit.

`aria-busy` is load-bearing. WAI-ARIA 1.3: when true, "assistive technologies can ignore changes to
content that is an accessibility descendant of that element and then process all changes made during
the busy period as a **single, atomic update** when `aria-busy` becomes `false`." Without it, an
append-per-page-load feed is announced as a dozen separate insertions. If the total is known, expose
position: `aria-posinset` "defines an element's number or position in the current set" and
`aria-setsize` "defines the number of items in the current set"; "**If the total number of items is
unknown, authors SHOULD set the value of `aria-setsize` to -1**" (WAI-ARIA 1.3). Neither is needed
"if all items in a set are present in the DOM."

Cursor resets, scroll restoration, and the end state are in `pagination-infinite-scroll.md`. The one
addition specific to notifications: **a live inbox that appends above the user's position moves the
content they were reading.** Anchor arrivals to a "3 new notifications" control instead of inserting
them into a scrolled list.

## Live regions

- **`role="status"`** for "you have new notifications" — implicit `aria-live="polite"` and implicit
  `aria-atomic="true"`; authors "SHOULD ensure an element with `role="status"` does not receive focus as a
  result of change in status" (WAI-ARIA 1.3). This is what satisfies WCAG 2.2 SC 4.1.3 Status Messages
  (Level AA).
- **`role="alert"`** (implicit `aria-live="assertive"`, implicit `aria-atomic="true"`) for nothing here.
  An arriving comment is not an alert.
- **`role="log"`** if the inbox doubles as a streaming console. WAI-ARIA 1.3 defines it as "a type of live
  region where new information is added in meaningful order and old information can disappear. Examples
  include chat logs, messaging history, game log, or an error log," with implicit `aria-live="polite"` —
  and the constraint: "new information is added **only to the end** of the log, not at arbitrary points."
  An inbox that prepends newer items at the top is not a `log`.

Put the region in the DOM once and change its text; never rebuild the element per announcement.

**Not found:** no primary source consulted specifies an unread-count cap, an auto-archive window, or a
maximum items per inbox group. Settle them in `DESIGN.md`.

## Sources

- [Feed Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/feed/) — W3C WAI-ARIA Authoring Practices Guide, accessed 2026-10-05
- [WAI-ARIA 1.3 — `feed` role](https://www.w3.org/TR/wai-aria-1.3/#feed) — W3C Working Draft, accessed 2026-10-05
- [WAI-ARIA 1.3 — `log` role](https://www.w3.org/TR/wai-aria-1.3/#log) — W3C Working Draft, accessed 2026-10-05
- [WAI-ARIA 1.3 — `status` role](https://www.w3.org/TR/wai-aria-1.3/#status) — W3C Working Draft, accessed 2026-10-05
- [WAI-ARIA 1.3 — `alert` role](https://www.w3.org/TR/wai-aria-1.3/#alert) — W3C Working Draft, accessed 2026-10-05
- [WAI-ARIA 1.3 — `aria-busy` state](https://www.w3.org/TR/wai-aria-1.3/#aria-busy) — W3C Working Draft, accessed 2026-10-05
- [WAI-ARIA 1.3 — `aria-posinset` property](https://www.w3.org/TR/wai-aria-1.3/#aria-posinset) — W3C Working Draft, accessed 2026-10-05
- [WAI-ARIA 1.3 — `aria-setsize` property](https://www.w3.org/TR/wai-aria-1.3/#aria-setsize) — W3C Working Draft, accessed 2026-10-05
- [Notification](https://carbondesignsystem.com/components/notification/usage/) — Carbon Design System (IBM), accessed 2026-10-05
- [UI shell header](https://www.carbondesignsystem.com/building-blocks/core/components/ui-shell-header/guidelines) — Carbon Design System (IBM), accessed 2026-10-05
- [Badge](https://shopify.dev/docs/api/app-home/latest/web-components/feedback-and-status-indicators/badge) — Shopify Polaris, accessed 2026-10-05
- [Indicators, Validations, and Notifications: Pick the Correct Communication Option](https://www.nngroup.com/articles/indicators-validations-notifications/) — Nielsen Norman Group, accessed 2026-10-05
- [Alert Fatigue in User Interfaces](https://www.nngroup.com/videos/alert-fatigue-user-interfaces/) — Nielsen Norman Group, accessed 2026-10-05
- [Account checklist](https://docs.stripe.com/get-started/account/checklist) — Stripe Documentation, accessed 2026-10-05