# Usage, limits and quotas

Reference for the metered-usage surface: meters, warning thresholds, hard caps and overage.
Stripe's alert and threshold mechanics are Stripe's; GitHub's budget thresholds are GitHub's.

## Usage is a mechanism, not an entitlement

Keep three axes apart, because collapsing them produces wrong UI:

| Axis | Question | Stripe mechanism |
|---|---|---|
| Entitlement | "may this customer use feature X at all?" | [Entitlements](https://docs.stripe.com/billing/entitlements) — one Active Entitlement per feature |
| Allowance | "how much of X is included?" | Included quantity / free units in the price |
| Meter | "how much of X has been consumed this period?" | [Billing Meters](https://docs.stripe.com/billing/subscriptions/usage-based/monitor) |

An entitlement is boolean. A quota is a number. A meter is a running total against that number.
Soft warning and hard cap are then two *behaviours* on top, not a third axis.

## The three documented alert use cases

Stripe names exactly three workflows for usage alerts, and they map cleanly onto three UI
behaviours ([Monitor usage with alerts](https://docs.stripe.com/billing/subscriptions/usage-based/monitor)):

| Documented use case | Mechanism | UI |
|---|---|---|
| "Email users: Allow customers to configure usage limits, and send an email when they hit their limit" | Alert fires, nothing changes | Soft warning |
| "Deprovision access: Grant customers a free number of usage units to your service, and remove access when they exceed the limit" | Alert triggers your de-provisioning | Hard cap |
| "Notify the sales team of an upsell: Alert your sales team of an enterprise opportunity when a self-serve user exceeds a usage threshold" | Alert is internal | Internal signal, no customer surface |

A cap is not an alert with louder styling. Cap means the product stops; alert means the product
continues. If a meter is over the limit and the customer can still act, it is a warning.

## Alert thresholds: vendor-documented numbers

Stripe alert alerts are configured per meter with a `usage_threshold[gte]` value and a
`recurrence`; the documented alert type "One-time per-customer usage alert … triggers when a
customer exceeds the specified usage level for the first time, and only triggers one time per
customer, regardless of future usage" ([Set up usage alerts](https://docs.stripe.com/billing/subscriptions/usage-based/alerts)).

Hard limits on the mechanism:

- "You can create a maximum of **25 alerts** for each combination of a specific meter and
  customer."
- "We evaluate alerts when you report usage data after you create the alert. However, the
  evaluation **includes usage data that you reported before you created the alert**." A newly
  created alert can fire instantly on back-dated usage.
- "Alerts currently don't work with test clocks."
- A meter must exist before an alert can be created.

GitHub publishes its thresholds openly, which makes them a usable reference point for copy:
budget alerts fire at "**75%, 90%, and 100%** of the budget amount", and a separate set of
"included usage alerts" fires when "the included usage for your plan reaches **90% and 100%**"
during a billing period ([Budgets and alerts](https://docs.github.com/en/billing/concepts/budgets-and-alerts)).
Three tiers is the documented pattern: heads-up, act-now, breached.

## The three customer-facing surfaces

Stripe's mechanics imply three distinct surfaces. Ship all three; each answers a different question.

1. **The meter (passive).** Current consumption against allowance, with the reset date.
   Stripe's data is genuinely behind: "Stripe processes meter events asynchronously, so aggregated
   usage in meter event summaries and on upcoming invoices might not immediately reflect recently
   received meter events" ([Record usage for billing](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage)).
   Stripe's alternative product exists precisely because "Billing Meters only reconciles usage at
   invoice time" ([Basic usage-based billing](https://docs.stripe.com/billing/subscriptions/usage-based)).
   Label the number as approximate when it is not invoice-final.
2. **The warning (threshold crossing).** Inline at the point of use, plus out-of-band. GitHub
   ships both channels: alerts are "shown in the GitHub UI and sent by email" and also raise "a
   banner on GitHub". Each email "identifies the account, the product, the approximate usage
   compared to the included allowance, and the current billing period" and links to the budgets
   page.
3. **The cap (enforcement).** The action is refused and a recovery path is offered — buy more,
   raise a limit, request an increase. GitHub documents the request path: "When a member exhausts
   a Copilot AI credits budget, they can ask you to increase it."

## Soft warning vs hard cap: the documented distinction

GitHub states the rule by product class, and it is the cleanest available statement of intent
([Budgets and alerts](https://docs.github.com/en/billing/concepts/budgets-and-alerts)):

> "For most license-based products such as GitHub Copilot, GitHub Team, and GitHub Enterprise,
> **setting a budget does not prevent usage over the budget amount but does provide alerts**. …
> For metered products such as GitHub Actions, Copilot AI credits, or cloud sandboxes, you can set
> budgets to **prevent usage once the budget threshold is reached**."

And the consequence when a cap is on: "Members are now blocked from using all GitHub-hosted
runners until the next billing cycle or until the 'Actions' product budget is increased"
([Setting up budgets](https://docs.github.com/en/billing/how-tos/set-up-budgets)). The reset
condition is part of the message.

There is a fifth, harsher variant. GitHub: "If your account does not have a valid payment method
on file, **usage is blocked once you use up your quota**"
([About billing for GitHub Actions](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)).
Metered product, no payment method, quota gone: the product stops. That is a payment state
surfacing through a usage surface, and the UI should say so rather than showing a generic limit
error.

## Alert configuration gotchas that shape the UI

From Stripe's thresholds docs ([Set up thresholds](https://docs.stripe.com/billing/subscriptions/usage-based/thresholds)):

- Monetary thresholds are "a positive integer in the smallest currency unit… Set the value to at
  least **50 currency units**."
- "Subscriptions are only allowed a **single** monetary threshold" and "Subscription items are
  only allowed a **single** usage threshold." Two meters of the same kind cannot both trigger an
  invoice.
- "Thresholds don't apply to trial subscriptions." Trial meters must not show an invoice trigger.
- "Billing thresholds aren't evaluated in the **24 hours** before a subscription ends."
- "Invoiced amounts or usage might be slightly higher than the specified thresholds because
  invoices aren't issued at the exact moment a specified threshold is reached." Never display
  "you will be invoiced exactly $X" off a threshold.
- Usage thresholds are API-only: "Stripe doesn't support setting usage thresholds in the Dashboard."

## Overage: three shapes

Stripe's pricing models are "flat rate, per-seat, tiered, usage-based", and the usage-based family
is "fixed fee and overage, pay as you go, and credit burndown"
([Recurring pricing models](https://docs.stripe.com/products-prices/pricing-models)). Overage, in
the tiered sense, has two rate shapes that produce opposite-looking bills:

- **Graduated**: each tier prices only its own units. 6 fonts at 7 / 6.50 USD = 35 + 6.50 = 41.50 USD.
- **Volume**: the end-of-period tier prices *everything*. Same 6 fonts = 6 × 6.50 = 39 USD.

Volume pricing can make the bill go *down* as usage goes up, and with a threshold already invoiced
it can produce a negative line: Stripe's worked example has a customer 5,000 USD invoiced, then
consuming one more unit so the total drops to 4,000.40 USD and the customer is "owed" 999.60 USD
credited to their balance. A meter UI for a volume-tiered product must show the current tier
recalculation, not a running sum.

## Quota display rules

1. Always show three numbers together: used, included, and reset date. Any one alone is
   unactionable.
2. Label pre-invoice usage as provisional. Stripe's own pipeline is asynchronous.
3. Warning and cap are different components with different copy. Cap copy must state when access
   returns (reset, payment, or manual approval).
4. Thresholds are guarantees of *direction*, not of *amount* or *timing*. Never quote a future
   invoice total off a threshold.
5. One meter per kind per object at the invoice-trigger level. If the product needs two, use alerts
   for the second.
6. If a meter can be blocked for non-payment, the cap state must distinguish "over your allowance"
   from "no valid payment method".

**Not found:** a vendor-documented standard for how many warning thresholds a product should
show, or any published guidance on meter refresh intervals. Settling it would require an
authoritative usability standard; the only sourced thresholds here are GitHub's 75/90/100 and
90/100 sets.

## Sources

- https://docs.stripe.com/billing/subscriptions/usage-based/monitor — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/usage-based/alerts — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/usage-based/thresholds — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/usage-based — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/usage-based/manage-billing-setup — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/entitlements — Stripe — accessed 2026-10-05
- https://docs.stripe.com/products-prices/pricing-models — Stripe — accessed 2026-10-05
- https://docs.stripe.com/subscriptions/pricing-models/tiered-pricing — Stripe — accessed 2026-10-05
- https://docs.github.com/en/billing/concepts/budgets-and-alerts — GitHub — accessed 2026-10-05
- https://docs.github.com/en/billing/how-tos/set-up-budgets — GitHub — accessed 2026-10-05
- https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions — GitHub — accessed 2026-10-05
