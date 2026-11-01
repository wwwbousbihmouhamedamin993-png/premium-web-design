# Plan changes: upgrade, downgrade, seats

Reference for the plan-change surface of a logged-in B2B product. Proration behaviour and its
limits are Stripe's; GitHub's plan-change table is GitHub's. Neither is a universal rule.

## Preview-confirm is mandatory, not a nicety

Stripe's proration docs state the design requirement directly:

> "Use this information to **confirm the changes with the customer before modifying the
> subscription**. Because Stripe prorates to the second, prorated amounts might change between
> the time they're previewed and the time the update is made."
> ([Prorations](https://docs.stripe.com/billing/subscriptions/prorations))

The fix is a pinned date on both calls: "pass in a `subscription_details.proration_date` value
when creating a preview. When you update the subscription, pass the same date." Without the pin,
the number the customer approved and the number they are charged are different numbers.

**Design consequence:** the confirmation step is a screen, not a spinner. It carries the line
items, the effective date, and the total.

## The three proration behaviours

`proration_behavior` has exactly three values, and "The default parameter for
`proration_behavior` is `create_prorations`":

| Value | Effect | UI meaning |
|---|---|---|
| `create_prorations` (default) | Proration invoice items created when applicable | "Billed at your next invoice" |
| `always_invoice` | "calculates the proration, then immediately generates an invoice" | "Charged today, $X" |
| `none` | No proration; "customers are billed the full amount at the new price when the next invoice is generated" | "No charge today" |

"No parameter turns off all future prorations for a subscription." Disabling prorations
indefinitely means sending `none` on every request that would prorate.

## What the line items must say

Stripe's own proration preview returns descriptions written for humans, not for engineers:
`"Unused time on Silver plan after 01 Sep 2020"` (credit, −166) and `"Remaining time on Gold plan
after 01 Sep 2020"` (debit, +541), with the full-period item rendered as `"1 × Gold product (at
$32.52 / month)"`. Both prorations carry `discountable: false`.

Render line items in that shape: **period affected × amount, with credit and debit visually
distinct.** A single net number ("+$5.00") hides the mechanism and reads as a surprise. The
worked example in Stripe's docs is a 10 → 20 USD monthly upgrade mid-period: `−5 USD` unused time
plus `+10 USD` remaining time equals `+5 USD`.

Two vendor caveats worth surfacing in the copy:

- "Negative prorations aren't automatically refunded and positive prorations aren't immediately
  billed, although you can do both manually."
- Discounts do not apply to the proration lines themselves, because they are `discountable=false`.

## Immediate vs period end

Stripe and GitHub agree on the shape and disagree on the default.

GitHub publishes it as a contract ([Impact of changing your plan on billing](https://docs.github.com/en/billing/concepts/impact-of-plan-changes)):

- Upgrade: billed and applied **immediately**, prorated.
- Downgrade or cancel: takes effect **at the end of the current cycle**, no proration.
- Add seats: immediate, prorated, access granted immediately.
- Remove seats: next cycle, no proration.

Stripe's default is the opposite for downgrades. The portal's "Manage downgrades" toggle defaults
to "Update immediately", and when enabled it "automatically creates and attaches a subscription
schedule" so the change lands at period end — constrained to "the end of a billing period between
prices that have the same product" ([Configure the customer portal](https://docs.stripe.com/customer-management/configure-portal)).

**Rule:** the effective date is the single most important string on the change screen, and it
differs per direction. Never let "Upgrade" and "Downgrade" share one confirmation template.

## Seat and quantity changes

Stripe's per-seat model is one price with a `quantity`; changing quantity is a proration trigger
alongside price and item changes. Two footguns the docs call out: "You must specify the
subscription item to replace the current price with the new price. Failing to do so results in
*adding* the new price so both prices are active"; and "Updating a subscription price automatically
reverts the quantity to the default value of `1`" ([Change the price of existing subscriptions](https://docs.stripe.com/billing/subscriptions/change-price)).
A seat count silently collapsing to 1 is the failure mode to design against.

GitHub's removal semantics are the ones customers argue about: "Remove users or seats: The user's
access is revoked immediately, but you'll still be billed for the full billing cycle. Removing a
user won't reduce your current bill." Seat removal and seat reduction are **two different actions**
— one is a permission change, one is a money change, and only one of them lowers the bill.

## Switching plan during a trial

> "When a customer uses the portal to upgrade or downgrade a subscription with a trial, the
> subscription's trial **ends immediately** when switching to the new price."
> ([Integrate the customer portal](https://docs.stripe.com/customer-management/integrate-customer-portal))

That was universal until a configuration option arrived: set
`features.subscription_update.trial_update_behavior` to `continue_trial` to keep the trial active.
Default behaviour, previously: "all trials ended when a subscription was upgraded or downgraded in
the customer portal" ([Changelog](https://docs.stripe.com/changelog/clover/2025-09-30/customer-portal-trial-behavior)).
A trial-ending plan switch therefore triggers an immediate charge, so the confirmation screen must
say so and state the amount taken today.

Switching to a price with a **different billing interval** moves the billing date: "switching a
customer from one monthly subscription to another doesn't change the billing dates. However,
switching a customer from a monthly subscription to a yearly subscription moves the billing date to
the date of the switch."

## Downgrade consequences and the data-loss warning

No vendor bills for a downgrade's data loss; they document it. GitHub's downgrade flow is the
clearest worked example ([Downgrading your account's plan](https://docs.github.com/en/billing/how-tos/manage-plan-and-licenses/downgrade-plan)):

- "After an organization's plan is downgraded, the organization will lose access to any
  functionality that is not included in the new plan."
- "Downgrading from GitHub Enterprise Cloud **disables any SAML settings**. If you later purchase
  GitHub Enterprise, you will need to reconfigure SAML."
- A domain-takeover hazard: "If you published a GitHub Pages site in a private repository and
  added a custom domain, remove or update your DNS records before downgrading… to avoid the risk of
  a domain takeover."

Its confirmation copy is the pattern: "Read the information about the features your organization
will no longer have access to on your next billing date, then click **I understand. Downgrade my
organization**."

**Rules for the downgrade screen:**

1. Enumerate what stops working, by feature, not by plan tier.
2. Name anything destructive or externally visible (SAML, DNS, custom domains, webhooks) and say
   whether it is reversible.
3. Require an explicit acknowledgement. A checkbox or a typed confirmation, not a silent submit.
4. State the date, twice: "on your next billing date."

## Failed payment on a plan change

By default the change applies regardless: "By default, Stripe applies updates regardless of
whether payment on the new invoice succeeds. If payment fails, rolling back the updates is a manual
process." With `payment_behavior=pending_if_incomplete`, "changes normally only apply if payment on
the resulting invoice succeeds" ([Pending updates](https://docs.stripe.com/billing/subscriptions/pending-updates)).

A pending update expires: its `expires_at` "matches the first occurrence of either the trial end or
the earliest `items.current_period_end`… if either time is within 23 hours of the update request.
Otherwise, the expiration is 23 hours from the update request." So a failed upgrade can silently
evaporate — the UI needs an explicit "upgrade not applied, your card failed" state, not a spinner
that resolves to "still on the old plan".

## Checkable rules

1. Preview, then confirm, with the preview date pinned. No exceptions.
2. Show credit and debit as separate lines with their periods; show the net as a summary, never as
   the only number.
3. Upgrades: state the amount charged today and the date access starts. Downgrades: state the date
   access ends and enumerate the losses.
4. Seat add and seat remove are different screens. One costs money now; the other stops access now
   and saves money later.
5. Any plan switch during a trial must state whether the trial survives. Under Stripe's portal
   default it does not.
6. An interval change (monthly → yearly) moves the next billing date. Show the new date.
7. Gate the confirm button on an acknowledgement of consequences, not on a click.

**Not found:** a vendor-documented rule for what happens to customer data on downgrade in general.
Settling it would require a per-vendor retention/deletion policy document; GitHub documents
specific settings loss but not a general data-retention contract.

## Sources

- https://docs.stripe.com/billing/subscriptions/prorations — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/change-price — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/pending-updates — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/subscription-schedules — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/billing-cycle — Stripe — accessed 2026-10-05
- https://docs.stripe.com/customer-management/configure-portal — Stripe — accessed 2026-10-05
- https://docs.stripe.com/customer-management/integrate-customer-portal — Stripe — accessed 2026-10-05
- https://docs.stripe.com/changelog/clover/2025-09-30/customer-portal-trial-behavior — Stripe — accessed 2026-10-05
- https://docs.stripe.com/subscriptions/pricing-models/per-seat-pricing — Stripe — accessed 2026-10-05
- https://docs.github.com/en/billing/concepts/impact-of-plan-changes — GitHub — accessed 2026-10-05
- https://docs.github.com/en/billing/concepts/billing-cycles — GitHub — accessed 2026-10-05
- https://docs.github.com/en/billing/how-tos/manage-plan-and-licenses/downgrade-plan — GitHub — accessed 2026-10-05
