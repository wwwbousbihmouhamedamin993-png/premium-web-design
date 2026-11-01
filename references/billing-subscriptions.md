# Billing and subscriptions

Reference for the state machine behind a signed-in billing surface. Vendor state names and
counts are attributed to the vendor that documents them. Stripe's eight subscription statuses
are Stripe's model; they are not a universal subscription taxonomy.

## The rule that outranks every other rule here

Subscription status and product access are two different decisions, and Stripe's docs only
instruct revocation for one of the eight states:

> "Revoke access to your product when the subscription is `unpaid` because Stripe already
> attempted and retried payment while the subscription was `past_due`."
> ([How subscriptions work](https://docs.stripe.com/billing/subscriptions/overview))

No equivalent instruction exists for `past_due`. Any UI that greys out the product during a
dunning window is making a product decision Stripe does not document. Decide it explicitly and
write it down.

## The eight states (Stripe)

Stripe documents exactly eight subscription statuses
([Subscription object](https://docs.stripe.com/api/subscriptions/object), [How subscriptions
work](https://docs.stripe.com/billing/subscriptions/overview)).

| Status | Stripe's definition | Access Stripe instructs | UI it earns |
|---|---|---|---|
| `trialing` | "currently in a trial period and you can safely provision your product" | Provision | Trial badge, countdown, "no card charged yet" |
| `active` | "in good standing" | Provision | The default; no status chrome at all |
| `past_due` | "Payment on the latest finalized invoice either failed or wasn't attempted" | Provision (no revocation instructed) | Past-due banner, retry countdown, update-payment CTA. Service stays on |
| `unpaid` | Stripe "already attempted and retried payment while the subscription was `past_due`" | **Revoke** | Access-restricted state with restore path |
| `incomplete` | "must make a successful payment within 23 hours"; invoice stays `open` | Not provisioned | 23-hour activation window countdown |
| `incomplete_expired` | "didn't make a successful payment within 23 hours"; "doesn't bill customers" | None | Terminal state, "start again" path. Docs: "create a new subscription for them" |
| `canceled` | "canceled… `auto_advance=false`… This is a terminal state that can't be updated" | None at period end | Ended state; read-only billing history |
| `paused` | trial ended "without a default payment method" with `end_behavior.missing_payment_method` set to `pause`; "Invoices are no longer created" | None until resumed | Resume-with-payment-method prompt |

Two traps in this table:

- **`active` does not mean paid.** Stripe: "`active` doesn't necessarily indicate that all
  outstanding invoices associated with the subscription have been paid."
- **`canceled` is reached at period end, not at cancel time.** Canceling at period end sets
  `cancel_at_period_end=true`; the status stays `active` until the period closes.

## `paused` is not `pause_collection`

Stripe draws the line explicitly. `pause_collection`: "the subscription remains `active` and
invoices continue to generate, but Stripe doesn't collect payment. Your customer retains access
to the service during this time." `paused`: "Invoices are no longer created for the
subscription" ([Pause payment collection](https://docs.stripe.com/billing/subscriptions/pause-payment)).
Two different screens: "payment on hold, service continues" versus "service stopped, add a card
to resume."

## Payment outcome maps to status

| Payment outcome | PaymentIntent | Invoice | Subscription |
|---|---|---|---|
| Success | `succeeded` | `paid` | `active` if governing invoices settled |
| Card error | `requires_payment_method` | `open` | `incomplete` |
| Needs authentication | `requires_action` | `open` | `incomplete` |

([How subscriptions work](https://docs.stripe.com/billing/subscriptions/overview))

Delayed-confirmation methods (ACH and similar) break this: "a subscription can move directly to
`active` after creation and bypass `incomplete`. If the payment fails later, Stripe voids the
invoice but the subscription remains `active`." A `void` invoice does not block a subscription.

## Status resolution is a setting, not a constant

Stripe defaults to resolving status from **the most recent non-voided invoice**; the alternative
is **all invoices**, which blocks `active` while any applicable invoice is outstanding. "Stripe
checks applicable invoices from the previous 37 months." Changing the setting "doesn't
immediately reevaluate existing subscriptions." The UI consequence: a customer can be `active`
while an old invoice is still open, so invoice history and status badge can legitimately disagree.

## Plan comparison surface

Stripe's customer portal renders a product catalog with exactly four customer-visible attributes:
"Product name and description", "Quantity restrictions per product", and "Price amount, currency,
and billing interval" — and the portal caps plan switching at "a maximum of 10 products"
([Integrate the customer portal](https://docs.stripe.com/customer-management/integrate-customer-portal),
[Provide a customer portal](https://docs.stripe.com/customer-management)). Build the comparison
table from those four and nothing else; feature matrices are marketing copy, not catalog data.

## Seats and quantities

Stripe models per-seat as a flat-rate price with a `quantity`: "Each pricing unit represents one
user" ([Set up per-seat pricing](https://docs.stripe.com/subscriptions/pricing-models/per-seat-pricing)).
GitHub counts licenses by consumption instead: "The number of unique users across your
deployments. Each user only consumes one license, no matter how many GitHub Enterprise Server
instances the user uses" ([Billing for GitHub Enterprise](https://docs.github.com/en/billing/concepts/enterprise-billing/billing-for-enterprises)).
Two different "seats used" numbers; never label them the same thing.

Seat removal has a money consequence worth surfacing. GitHub: "Remove users or seats: The user's
access is revoked immediately, but you'll still be billed for the full billing cycle. Removing a
user won't reduce your current bill." ([Billing cycles](https://docs.github.com/en/billing/concepts/billing-cycles))

## Trial countdown

Stripe's `customer.subscription.trial_will_end` webhook fires per the Dashboard "Trial ending
events" setting, "which defaults to 3 days before the trial ends. If the trial is shorter than the
configured interval, it triggers immediately." Stripe's own reminder emails are a separate system:
"Sent 7 days before the trial ends" ([Configure trial offers](https://docs.stripe.com/billing/subscriptions/trials),
[Automate customer emails](https://docs.stripe.com/billing/revenue-recovery/customer-emails)).
Trial length is capped: "The trial period must be 730 days (2 years) or less."
([Free trial periods](https://docs.stripe.com/billing/subscriptions/trials/free-trials))

GitHub has a fourth countdown state documented: "If the authorization is unsuccessful, the chosen
service will not be activated and the account may be locked"
([How billing works](https://docs.github.com/en/billing/get-started/how-billing-works)).

## Canceled-but-running

Stripe's portal documents it as expected behavior: "After canceling, customers can still renew
subscriptions until the billing period ends" ([Configure the customer portal](https://docs.stripe.com/customer-management/configure-portal)).
Cancellation also flips every `open` and `draft` invoice for that subscription to
`auto_advance=false`, "pauses automatic collection… and prevents automatic reminder emails from
sending" ([Cancel subscriptions](https://docs.stripe.com/billing/subscriptions/cancel)).

Reactivation has a hard deadline: "You can reactivate the subscription at any time up to the end of
the period." After `canceled`, "you can no longer update the subscription except for its `metadata`
and `cancellation_details`" — resubscription requires collecting new payment information.

GitHub publishes the same shape as a table, and it is the clearest statement of the industry
norm available ([Impact of changing your plan on billing](https://docs.github.com/en/billing/concepts/impact-of-plan-changes)):

| Scenario | When billing is affected | Proration | When access changes |
|---|---|---|---|
| Upgrade plan | Immediate | Yes | Immediately |
| Downgrade or cancel | End of current cycle | No | End of current cycle |
| Add paid seats/licenses | Immediate (prorated) | Yes | Immediately |
| Remove paid seats/licenses | Next billing cycle | No | End of cycle, unless revoked manually |

## Checkable rules

1. A status badge with no consequence attached is decoration. Every state maps to a banner, a
   countdown, a CTA, or nothing.
2. Never render "Payment failed" as an error state that hides the product. `past_due` keeps access.
3. Render the 23-hour `incomplete` window as a countdown, not as a generic pending state; it is
   the only state with a hard, vendor-defined deadline on first payment.
4. Cancel-at-period-end is a **scheduled** state, visually distinct from canceled. It needs an
   undo affordance and a date.
5. Persist entitlements, not status. Stripe: "We recommend you persist these entitlements
   internally for faster resolution" ([Entitlements](https://docs.stripe.com/billing/entitlements)).
6. Show the next renewal date and the amount on the same row. Billing period is anchored by
   `billing_cycle_anchor`, which "sets the day of month for `month` and `year` intervals"
   ([Set the subscription billing renewal date](https://docs.stripe.com/billing/subscriptions/billing-cycle)).

**Not found:** a vendor-documented set of UI states that maps 1:1 onto all eight subscription
statuses, or an authoritative count of billing states across vendors. Settling it would require
surveying each vendor's subscription state machine and reconciling their vocabularies.

## Sources

- https://docs.stripe.com/billing/subscriptions/overview — Stripe — accessed 2026-10-05
- https://docs.stripe.com/api/subscriptions/object — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/cancel — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/pause-payment — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/trials — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/trials/free-trials — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/billing-cycle — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/entitlements — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/revenue-recovery/customer-emails — Stripe — accessed 2026-10-05
- https://docs.stripe.com/customer-management/configure-portal — Stripe — accessed 2026-10-05
- https://docs.stripe.com/customer-management/integrate-customer-portal — Stripe — accessed 2026-10-05
- https://docs.stripe.com/customer-management — Stripe — accessed 2026-10-05
- https://docs.stripe.com/subscriptions/pricing-models/per-seat-pricing — Stripe — accessed 2026-10-05
- https://docs.github.com/en/billing/concepts/impact-of-plan-changes — GitHub — accessed 2026-10-05
- https://docs.github.com/en/billing/concepts/billing-cycles — GitHub — accessed 2026-10-05
- https://docs.github.com/en/billing/concepts/enterprise-billing/billing-for-enterprises — GitHub — accessed 2026-10-05
- https://docs.github.com/en/billing/get-started/how-billing-works — GitHub — accessed 2026-10-05
