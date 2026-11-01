# Entitlements and feature gating

Reference for gating a logged-in product by commercial state. Entitlement lifecycle, feature-flag
vocabulary and gating consequences are each vendor-attributed.

## The distinction to hold onto

Stripe separates two things that products routinely merge:

- **Subscription status** — the eight states in
  [Billing and subscriptions](billing-subscriptions.md). One per subscription.
- **Entitlement** — "An entitlement represents a customer's access to a feature." One per
  customer *per feature*, created when the subscription is first activated, retained while the
  subscription holds, de-provisioned on lapse
  ([Entitlements](https://docs.stripe.com/billing/entitlements)).

Consequence for the UI: the number of gated things is the number of features, not the number of
plans. A three-tier plan with eleven features produces eleven gate checks. Gate on entitlements;
render plan as context.

## Entitlement lifecycle, in Stripe's words

| Moment | Entitlement behaviour | Source |
|---|---|---|
| Subscription first activated | "Stripe creates entitlements for the features that they're subscribed to" | Entitlements |
| Feature attached to a product later | "Existing subscriptions will create active entitlements for any product feature changes **at the start of the next billing period**" | Entitlements |
| Subscription maintained | "As long as a customer maintains an active subscription for a feature, they retain an active entitlement" | Entitlements |
| Upgrade, downgrade, cancel | "Stripe updates the customer's entitlements based on your mapped features" | Entitlements |
| Cancel or failed-payment cancellation | Revoked features "no longer appear in `entitlements.data`" | Entitlements |

That second row is the one that breaks naive implementations. **Feature changes are scheduled, not
instant.** Turning on a feature for existing customers takes effect at the *start of the next
billing period*. A settings screen that says "changes take effect immediately" would be lying; say
"takes effect on <date>". Stripe's webhooks carry the whole picture in one object:
`entitlements.active_entitlement_summary.updated` fires "each time a customer's active entitlements
change, for example when a subscription is created, updated, or canceled."

## Read-side limits that shape architecture

- **The summary webhook truncates.** "The entitlement summary's `entitlements.data` array contains
  a maximum of **10 entitlements**. If a customer has more than 10 active entitlements, use the
  `entitlements.url` field in the payload to fetch the complete, paginated list."
- **Cache locally.** Stripe: "We recommend you persist these entitlements internally for faster
  resolution."
- **Read on startup.** The List Active Entitlements API is suggested "on application startup, for
  authorization checks, or to reconcile state after a webhook delivery failure" — which makes it a
  reconciliation path, not a per-request dependency.
- **Gate keys are stable.** Each entitlement returns the `lookup_key` you defined when creating the
  feature; Stripe's examples use `premium-support` and `advanced-reporting`. "Because the
  `lookup_key` is unique to each feature, you can't reuse it across different features." Renaming a
  key in code is a breaking change for every persisted cache.

## Feature flags are a different mechanism

A feature flag decides whether code runs for a cohort. An entitlement decides whether a customer
is *owed* a feature. Mixing them produces gates that break on the wrong schedule.

LaunchDarkly's vocabulary is the reference for the flag side ([Flag types](https://docs.launchdarkly.com/home/flags/types),
[Creating new flags](https://docs.launchdarkly.com/home/flags/new)):

- Exactly four flag types: **boolean**, **string**, **number**, **JSON**. Boolean is "the most
  common and simple flag type, having two possible variations" and cannot gain a third.
- Templates encode intent: **Release** ("a temporary boolean flag designed for feature releases…
  serves `false` to all targets"), **Kill switch** ("a permanent flag that enables or disables
  non-core functionality"), **Experiment**, and **N-stage migration**.
- Flags have a lifecycle — "Click **Temporary** to change the flag from temporary to permanent" —
  and temporary flags are meant to be cleaned up. Entitlements are not.
- **Key permanence:** "After you save the flag key, you cannot modify it." Renamable display name,
  immutable key.
- **Client-side exposure is opt-in:** "By default, flags are only available to server-side SDKs."
  A browser-rendered gate needs an explicit choice, and "If a client-side or mobile SDK tries to
  evaluate a feature flag that is not available to it, then LaunchDarkly serves the **fallback
  value**." That fallback is what a locked UI shows; choose it deliberately.
- **A client-side-bound flag is a security decision.** "A leaked mobile SDK key allows the holder
  to circumvent JavaScript's Secure Mode. This can give them access to the value of every flag for
  any context, even without knowing the SDK key."
- Default capacity: "LaunchDarkly allows you to create **5,000 feature flags per project**. You
  can create more upon request." **Rule:** a client-side flag is a *hint*; the server re-checks the
  entitlement. Rendering a locked button is presentation. Rendering a locked *result* is a
  security bug.

## The three gated UI states

Gating produces three distinct surfaces. The difference is what happens next.

| State | Condition | Surface | Next action offered |
|---|---|---|---|
| **Locked** | No entitlement for the feature | Feature visible, control disabled, explanation with the plan that includes it, upgrade CTA | Upgrade / contact sales |
| **Trial** | Entitlement exists via a trial | Fully functional, plus the remaining time and the charge date | Add payment method, or end trial |
| **Expired** | Entitlement was de-provisioned | Read-only or blocked, framed as "your plan doesn't include this", never as "your session expired" | Resubscribe |

Copy rules that follow from the sources:

- **Locked** must name the feature that is missing and the tier that provides it. GitHub's
  downgrade flow is the model of consequence-first copy: "Read the information about the features
  your organization will no longer have access to on your next billing date."
- **Expired** must not look like an auth failure. GitHub has a distinct locked-account state ("If
  the authorization is unsuccessful, the chosen service will not be activated and the account may
  be locked") — a payment-authorization failure needing different copy from a plan downgrade.
- **Trial** should state the conversion date and amount. Stripe's reminder cadence gives a
  precedent: `trial_will_end` "defaults to 3 days before the trial ends", Stripe's own emails go
  out "7 days before the trial ends".

## Scheduled vs immediate: get this right per operation

| Operation | Effect timing | Source |
|---|---|---|
| Feature attached to a product (existing subs) | Start of next billing period | Stripe Entitlements |
| Portal upgrade/downgrade during trial | Trial "ends immediately" | Stripe portal integration |
| Portal downgrade with Manage downgrades on | End of billing period, via an attached schedule | Stripe portal config |
| Update with `payment_behavior=pending_if_incomplete` | Only on successful payment of the new invoice | Stripe pending updates |
| Pending update expiry | Trial end or earliest `current_period_end` if within 23 hours, else 23 hours from the request | Stripe pending updates |
| Trial-offer transition to post-trial price | `billing_cycle_anchor` resets to `now` by default, generating "a full-amount invoice with no proration"; set `unchanged` to prorate instead | Stripe trial offers |

The last row is the pattern for every scheduled effect: **two named options, each with a stated
money consequence.** A UI that offers only the default hides the choice that exists.

GitHub adds the customer-side framing of the same split: plan upgrades are "Immediately" while
downgrades and cancellations land "End of current cycle"
([Impact of changing your plan on billing](https://docs.github.com/en/billing/concepts/impact-of-plan-changes)).

## Limit-reached and upgrade-prompt surfaces

Two different prompts that are easy to conflate:

- **Limit reached** (quota): the customer has the feature but has used it up. Prompt is
  *increase usage / buy more*, not *upgrade plan*. See
  [Usage, limits and quotas](usage-limits-quotas.md).
- **Feature not entitled**: the customer lacks the feature entirely. Prompt is *upgrade or
  contact sales*.

An upsell prompt on a quota breach is a category error and reads as upsell pressure at the moment
the customer hits a wall. Stripe's third documented alert use case is the internal counterpart:
"Notify the sales team of an enterprise opportunity when a self-serve user exceeds a usage
threshold." That is an internal surface with different privacy and tone requirements.

## Checkable rules

1. Gate on entitlements; display plan. One check per feature, not per plan.
2. Cache entitlements locally and reconcile at startup — do not gate on a live API call.
3. Handle the 10-entitlement webhook truncation or the gate will fail for large customers.
4. Treat `lookup_key` and flag keys as immutable identifiers. Renaming is a breaking change.
5. Never render a feature as available on the strength of a client-side flag alone, and choose
   flag fallback values to match the locked state.
6. "Changes take effect immediately" is false for product-feature changes; state the effective date.
7. Three gated states, three distinct components: locked, trial, expired. Do not reuse one.
8. Quota breaches upsell capacity. Missing entitlements upsell plan. Never mix.
9. Every gated surface needs the CTA's destination pre-verified — a locked button pointing at a
   checkout flow that cannot complete the purchase is worse than no button.

**Not found:** a vendor-documented specification for feature-gated UI states (locked/trial/expired)
or for upgrade-prompt copy patterns. Stripe and GitHub document entitlements, flags and downgrade
consequences; neither publishes a gated-component specification. Settling it would require adopting
a design system's own patterns as primary evidence.

## Sources

- https://docs.stripe.com/billing/entitlements — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/overview — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/pending-updates — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/trials — Stripe — accessed 2026-10-05
- https://docs.stripe.com/billing/subscriptions/usage-based/monitor — Stripe — accessed 2026-10-05
- https://docs.stripe.com/customer-management/integrate-customer-portal — Stripe — accessed 2026-10-05
- https://docs.stripe.com/customer-management/configure-portal — Stripe — accessed 2026-10-05
- https://docs.launchdarkly.com/home/flags/types — LaunchDarkly — accessed 2026-10-05
- https://docs.launchdarkly.com/home/flags/new — LaunchDarkly — accessed 2026-10-05
- https://docs.launchdarkly.com/home/flags — LaunchDarkly — accessed 2026-10-05
- https://docs.github.com/en/billing/concepts/impact-of-plan-changes — GitHub — accessed 2026-10-05
- https://docs.github.com/en/billing/how-tos/manage-plan-and-licenses/downgrade-plan — GitHub — accessed 2026-10-05
- https://docs.github.com/en/billing/get-started/how-billing-works — GitHub — accessed 2026-10-05
