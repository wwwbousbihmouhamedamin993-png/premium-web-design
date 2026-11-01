# Toasts, banners, inline messages

Transient messages are where product UI loses the most trust: the toast that vanished before it was
read, the error that needed a decision but offered only "OK", the stack of five notifications
covering the button you were about to press.

## Route the message by what it is

| Signal | Surface | Semantics |
|---|---|---|
| Result of a completed action, nothing to decide | **Toast** | `role="status"` |
| Ongoing background progress | **Banner / progress strip** (persistent region) | `role="status"` on the strip |
| Problem with one field or one object | **Inline message** next to the field or row | `aria-describedby` on the control, plus visible text |
| Problem that blocks the whole view | **Alert banner** in normal flow, or `alertdialog` | `role="alert"` for immediate notification |
| Problem that requires a choice | **Dialog** — never a toast | `alertdialog` if it must be acknowledged |
| Something the user asked to be told about (email, billing) | **Notification centre** (route) | Announced once, on demand forever after |

The test for toast vs dialog: **if the user must decide, it is a dialog.** A toast that disappears
while the user is reading the question it asked is a bug, not a design.

## Role and live-region semantics

- `status`: "a type of live region whose content is advisory information for the user but is not
  important enough to justify an alert"; elements with `role="status"` have **implicit
  `aria-live="polite"` and implicit `aria-atomic="true"`**. Authors **SHOULD** ensure an element
  with `role="status"` does not receive focus as a result of a change in status (WAI-ARIA 1.3).
- `alert`: "a special type of **assertive** live region that is intended to cause immediate
  notification"; assistive technologies immediately notify the user and "could potentially clear
  the speech queue of previous updates" (WAI-ARIA 1.3). Reserve it for errors that stop the user.
- `aria-live` values are a recommendation to the user agent, not a guarantee, and AT may override
  them — e.g. presenting a change immediately when it follows a key press or click (WAI-ARIA 1.3).

WCAG 2.2 **SC 4.1.3 Status Messages** (Level AA) is the reason the toast container must exist in
the DOM before the message arrives: status messages must be "programmatically determined through
role or properties such that they can be presented to the user by assistive technologies **without
receiving focus**". A toast that steals focus fails; a toast that appears only as a visually
rendered blip fails.

## Duration

- **Informational confirmations auto-dismiss.** The message is a receipt, not content.
- **Errors never auto-dismiss.** They persist until dismissed or resolved, because they carry
  content the user has to act on (see also SC 1.4.13's exemption, which treats input-error content
  as legitimately non-dismissible).
- **Anything with an action never auto-dismisses** while that action is on screen.

WCAG 2.2 **SC 2.2.1 Timing Adjustable** (Level A) governs time limits set by content: the user must
be able to turn the limit off, adjust it to at least ten times the default, or be warned and given
**at least 20 seconds** to extend it (W3C, Understanding SC 2.2.1). An auto-dismissing message that
is the only route to information is a time limit; an auto-dismissing receipt is not.

**Not found:** no normative source specifies a toast duration in milliseconds, a hover-to-pause
requirement, or a stacking limit. Settle those in `DESIGN.md` and state them as decisions, not
standards.

## Undo

The cheapest fix for a scary action is undo, not a dialog.

- APG records the platform convention for undo as `Control`+`Z` on Windows/Linux and `Command`+`Z`
  on macOS, and notes that this is a *convention authors assign*, not browser behavior
  (APG, Developing a Keyboard Interface).
- A toast with Undo should keep focus on the trigger, not move it to the toast button —
  `role="status"` is not supposed to take focus (WAI-ARIA 1.3). Wire the keyboard shortcut and
  leave the pointer affordance as the discoverable path.
- If the action cannot be undone, that is exactly when the dialog ladder in
  `modals-dialogs-drawers.md` applies.

**Not found:** APG's key-assignment table covers undo for *author-defined shortcuts*; it does not
prescribe that a toast expose an undo affordance, nor how long it must remain actionable. That is a
product decision.

## Stacking

- One toast region per surface, anchored in one corner, **max three visible**. Collapse the rest
  into a count ("+2 more") so the region never covers the primary action.
- Newest replaces-oldest in the same slot for the same severity; lower severity never pushes higher
  severity out.
- Toasts render above dialog content when the message concerns the dialog; they never render above
  a `role="alert"` dialog's own message.
- The region's stacking position is a fixed token from `z-index-layers.md` — not a per-component
  number.

**Not found:** no source above specifies a stacking or concurrency limit; the max-three rule is a
house convention recorded here so it is at least consistent across surfaces.

## Banner vs toast

A banner is a **region in normal flow** that stays until the condition clears — degraded service,
expired certificate, an unacknowledged policy change. It does not float, does not overlap content,
and does not steal focus. A toast is a transient receipt in a fixed screen region.

Choosing a banner for a one-shot success message wastes screen space permanently; choosing a toast
for a service outage loses the message. Rule of thumb: *would the user be annoyed to miss it?*
Banner. *Would the user be annoyed to read it twice?* Toast.

## Sources

- [Web Accessibility for Rich Internet Applications (WAI-ARIA) 1.3](https://www.w3.org/TR/wai-aria-1.3/#status) — W3C, accessed 2026-10-05
- [WAI-ARIA 1.3 — `aria-live` property](https://www.w3.org/TR/wai-aria-1.3/#aria-live) — W3C, accessed 2026-10-05
- [Understanding SC 4.1.3 Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html) — W3C WCAG 2.2, accessed 2026-10-05
- [Understanding SC 2.2.1 Timing Adjustable](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html) — W3C WCAG 2.2, accessed 2026-10-05
- [Understanding SC 1.4.13 Content on Hover or Focus](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html) — W3C WCAG 2.2, accessed 2026-10-05
- [Developing a Keyboard Interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/) — W3C WAI ARIA Authoring Practices Guide, accessed 2026-10-05