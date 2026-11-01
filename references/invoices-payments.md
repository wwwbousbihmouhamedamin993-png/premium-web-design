# Invoices, payments and tax

Reference for the billing-history surface: invoice states, receipts, payment failure, tax IDs and
tax registration. All state vocabularies are vendor-attributed.

## The five invoice states

Stripe documents exactly five, and publishes the permitted action per state
([How invoicing works](https://docs.stripe.com/billing/invoices/workflow), [Invoice
object](https://docs.stripe.com/api/invoices/object)):

| Status | Stripe's description | Available actions |
|---|---|---|
| `draft` | "The invoice isn't ready to use. All invoices start in `draft` status." | Edit anything; finalize to `open`; delete if not tied to a subscription |
| `open` | "finalized and awaiting payment" | Send; edit *some* elements; move to `paid`, `void`, or `uncollectible` |
| `paid` | "This invoice is paid" | Move back to `open` by unapplying payments; detach payments |
| `void` | "This invoice is canceled" | "No further actions" |
| `uncollectible` | "The customer is unlikely to pay the invoice" | Move to `void` or `paid` |

Stripe calls both `paid` and `void` terminal, yet also documents moving a `paid` invoice back to
`open`. Treat unapplying payments as a support action, not a customer action.

**Badge is not status.** Stripe's Dashboard shows one status with several badges. On an `open`
invoice it "can display a different badge, such as `Past due` or `Retrying`", with "an explanatory
tooltip"; and a pending payment "shows the `Pending` badge in the list of invoices. However, its
details page shows the `Open` badge." List and detail disagreeing is deliberate: one badge cannot
express pending-vs-open, so the list adds a transient state and the detail page stays canonical.
Never render an invoice as unpaid before an attempt exists: "An invoice is not attempted until **1
hour** after the `invoice.created` webhook, for example, so you might not want to display that
invoice as unpaid to your users."

Proration invoices and full-period invoices share the status vocabulary but not the shape. Stripe's
`billing_reason` enum is the label to render:
`subscription_create` ("A new subscription was created"), `subscription_cycle` ("A subscription
advanced into a new period"), `subscription_update` ("A subscription was updated" — the proration
case), `subscription_threshold` ("A subscription reached a billing threshold"), `upcoming`
("Reserved for upcoming invoices created through the Create Preview Invoice API"), `manual`,
`quote_accept`, and `subscription` ("No longer in use").

A period-start invoice shows a service period matching the interval; a proration invoice shows
partial-period lines with descriptive text. Render the service period per line, not one for the whole
invoice. Preview invoice IDs are "prefixed with `upcoming_in`", so a preview must never read as a
charge.

## Receipts

"Customers can view their receipts online through a web browser, and optionally download receipts as
PDFs" ([Receipts and paid invoices](https://docs.stripe.com/receipts)). Rules with UI weight:

- **Nothing is sent on failure.** "For payments, receipts are only sent if the payment succeeds."
- **Receipt links expire at 30 days.** "If a receipt link has expired, Stripe asks the customer to
  provide the email address associated with the original transaction." An app linking to
  `receipt_url` needs an expired-link fallback, or old rows dead-end.
- **Receipt history is capped at 10** on a payment's detail page, and **invoice receipts differ
  from payment receipts** — "which include more detail than standard receipts". Two download
  actions, two documents.
- **Delayed-confirmation methods delay receipts.** ACH, Bacs, bank transfers, Boleto, Canadian
  pre-authorized debits, Konbini, OXXO, Pay by Bank and SEPA Direct Debit "can take longer to
  trigger receipts". A missing receipt is not an error. `invoice.paid` and
  `invoice.payment_succeeded` are also different events.

## Failed and late payment

Stripe's retry behaviour is configurable, so the UI must be told which policy is live
([Automate payment retries](https://docs.stripe.com/billing/revenue-recovery/smart-retries)):

- Recommended default "8 tries within 2 weeks" for Smart Retries; windows are 1 week, 2 weeks,
  3 weeks, 1 month, 2 months. Custom schedules allow "up to three retries, each with a specific
  number of days after the previous attempt".
- `next_payment_attempt` "indicates the date when Stripe will attempt the next collection";
  `attempt_count` shows "how many attempts have been made so far". Both belong in a dunning banner.
- No retries when: "No payment methods are available", the issuer returned "a hard decline code",
  the card is "India-issued", or the Connect account has been disconnected. Hard declines still
  increment `attempt_count` and still schedule retries, but "the payment only executes if you
  obtain a new payment method." Attempt count is not a proxy for progress.
- After retries end, four outcomes: cancel to `canceled`; mark `unpaid` ("Invoices continue to be
  generated and stay in a draft state"); leave `past_due` ("Invoices continue to be generated and
  charge the customer based on retry settings"); or `paused` if eligible.
- Retry payment-method precedence is a four-step documented order — subscription
  `default_payment_method`, subscription `default_source`, customer
  `invoice_settings.default_payment_method`, legacy customer `default_source` — with the trap:
  "When you update payment methods after a failed payment attempt, update the field where the
  previous payment failed." Updating the wrong level keeps failing silently.
- Hosted recovery links expire: one is invalidated when "It's been 30 days since we sent the trial
  ending email", the status "changes to `cancelled`, `incomplete_expired`, or `unpaid`", the customer
  supplied a payment method, or the renewal period expired
  ([Automate customer emails](https://docs.stripe.com/billing/revenue-recovery/customer-emails)).

### Uncollectible and its reason field

`uncollectible` is an accounting write-off, not a customer-facing punishment. Its reason changes
behaviour: "An uncollectible invoice remains outstanding only when its reason is
`max_payment_attempts` or `payment_not_received`. Other reasons, such as `user_forgiven`, don't
block the subscription from becoming active" ([How subscriptions
work](https://docs.stripe.com/billing/subscriptions/overview)). Render the reason: only
`max_payment_attempts` and `payment_not_received` imply the customer should act.

## Tax IDs: valid but unverified is a real state

Stripe has four verification statuses — `pending`, `verified`, `unverified`, `unavailable`
([Tax ID object](https://docs.stripe.com/api/tax_ids/object)). The distinction that matters
([Collect customer tax IDs](https://docs.stripe.com/tax/checkout/tax-ids)): "Stripe verifies that
the provided tax IDs are formatted correctly, but **not that they are valid**", and "Stripe Tax
applies the reverse charge or zero rate according to applicable laws when the tax ID has the
required number format, **regardless of the government verification result**".

So a tax ID can be format-valid, treated as reverse-charge by the tax engine, and still read
`unverified`. A green verified badge and a zero-tax invoice are independent outcomes. Async
validation exists for only three types: "Australian Business Numbers (ABNs), European Value Added
Tax (EU VAT), and United Kingdom Value Added Tax (GB VAT) numbers." Further UI rules from the same
source: "Customers can only enter one tax ID."; Checkout "doesn't display the tax ID collection
form" when tax IDs are already saved; "The `checkout.session.completed` event can arrive before the
authority verification finishes", so `pending` is a normal first paint; the portal's "Tax ID"
toggle defaults to **Off**. `unavailable` means "you must manually verify the tax ID" — a dead end
needing a human path, not a retry loop.

## Tax registration badges

Stripe Tax groups location statuses into exactly five
([Register for sales tax, VAT, and GST](https://docs.stripe.com/tax/registering)): **Needs
attention** ("You need to make a decision or take action for this location" — threshold exceeded,
setup incomplete, or unsubmitted draft application); **Collecting tax** ("You have an active
registration in this location and your tax setup is complete"); **Not collecting tax** (expired
registration, no registration without threshold breach, or threshold status undeterminable);
**Issue** ("There's a problem with your registration application that requires your attention");
and **Registration in progress** ("currently being processed… You'll be notified when the
registration is complete"). Each registration separately carries **Collecting**, **Scheduled**, or
**Expired** — two vocabularies at two levels, and "a location can include multiple registrations",
so a location badge never maps 1:1 to a registration.

Warn before the click: expiration "is permanent" and a registration "can't" be paused. Copy
constraint Stripe imposes on its own UI: "**Guide, don't advise**: don't tell the user which
jurisdictions they must register in or that they're legally obligated — route that determination to
their tax advisor."

## Checkable rules

1. Badge is not status. Model a transient badge (`Pending`, `Retrying`, `Past due`) separately from
   the canonical status on the detail page, and never render an invoice as unpaid before an attempt
   exists; Stripe waits 1 hour.
2. Show the service period per line so proration invoices read as adjustments, not charges, and give
   every invoice row a PDF/receipt action with a 30-day-link fallback.
3. Show `next_payment_attempt` and `attempt_count` in the dunning banner, and say what happens when
   retries end.
4. Render `uncollectible` with its reason. Never imply customer fault.
5. Tax ID verification status and tax outcome are separate fields; `unverified` on a valid-format
   ID is expected, and `pending` is a settled state, not a loading state.
6. Location-level and registration-level tax statuses are different enums. Pick one per surface
   and label it. Warn before expiring a registration: it is permanent and un-pausable.
7. A tax rate that does not divide evenly is not an error. Stripe reports "a 66.55 EUR subtotal and
   12.65 EUR of tax" for a tax-inclusive 79.20 EUR at 19%, making "the applied rate appear to be
   19.01%, even though the applied rate is 19%" ([Calculate tax](https://docs.stripe.com/tax/calculating)).

**Not found:** vendor-documented standards for invoice list density, billing-history pagination
defaults, or a canonical invoice badge set across vendors. Settling it would require comparing each
vendor's Dashboard billing screens, which no vendor documents.

## Sources

- https://docs.stripe.com/billing/invoices/workflow — Stripe — accessed 2026-10-05
- https://docs.stripe.com/api/invoices/object — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/overview — Stripe — accessed 2026-10-05
- https://docs.stripe.com/receipts — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/revenue-recovery/smart-retries — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/revenue-recovery/customer-emails — Stripe — accessed 2026-10-05
- https://docs.stripe.com/customer-management/configure-portal — Stripe — accessed 2026-10-05
- https://docs.stripe.com/api/tax_ids/object — Stripe — accessed 2026-10-05
- https://docs.stripe.com/tax/checkout/tax-ids — Stripe — accessed 2026-10-05
- https://docs.stripe.com/tax/registering — Stripe — accessed 2026-10-05
- https://docs.stripe.com/tax/calculating — Stripe — accessed 2026-10-05
