# API keys and webhooks

Developer-facing settings surfaces. Vendor states, limits and retry behaviour cited.

## Secret shown once — three different rules

| Case | Rule (Stripe) |
|---|---|
| Live-mode key **Stripe created for you** (default key, scheduled rotation) | Revealable: "In live mode, Stripe displays it one time before you save it… you can reveal only API keys that Stripe creates for you" |
| Live-mode key **you created yourself** | "If you create a secret key yourself, you can't reveal it after you've seen it once" |
| Sandbox | "In sandbox mode, you can always see all of your API keys" |

Publishable keys are exempt ("shown by default"). Recovery is impossible: "We can't recover keys that
you've forgotten or lost access to. If you lose a key, rotate or delete it and create another." The
interaction ends in an explicit **Hide live key**
([Stripe, API keys](https://docs.stripe.com/keys)). The creation dialog has three fields that must
exist: verification code by email or SMS → `Continue`; **Key name**; then "Click the key value to copy
it"; "**Save the key value. You can't retrieve it later.**"; and **Add a note** — "enter the location
where you saved the key". Masked keys show only a tail: GitHub's credential list shows "only the last
several characters of each token or key"
([GitHub, SAML access](https://docs.github.com/enterprise-cloud@latest/organizations/granting-access-to-your-organization-with-saml-single-sign-on/viewing-and-managing-a-members-saml-access-to-your-organization)).

**Rules:** the once-only reveal is a modal with a blocked close until the operator confirms a storage
location — the note field is what makes the loss recoverable, so it is not decoration. Show the
environment (`live mode` / `sandbox`) in the banner, because the rules differ.

## Key types, scope, lifetimes

Stripe's four types ([API keys](https://docs.stripe.com/keys)): publishable `pk_…` — safe to expose,
"can't perform sensitive operations"; restricted `rk_…` — "permissions you control"; secret `sk_…` —
"**unrestricted** permissions on all Stripe APIs… we don't recommend using secret keys for new use
cases"; organization `sk_org_…` — operates across multiple accounts. RAK permissions are per-resource
tri-state **Read / Write / None**, "The default value for all permissions is `None`", plus a separate
connected-accounts permission; "**Write permissions imply read permissions**"; an under-permissioned
key yields an "invalid request error"; creation verifies with two-factor; cloning (**Duplicate key**)
carries over every permission
([Restricted API keys](https://docs.stripe.com/keys/restricted-api-keys)). Stripe's own comparison is
the model for a permissions-review UI: secret key = "Full access to every API resource" / "A bad actor
can do anything in your account" / "Use sparingly and protect aggressively"; restricted key = "Only the
permissions you assign" / "A bad actor can do only what the key allows" / "**Preferred**".

GitHub narrows by credential class instead: GitHub Apps installable by repo admins only "if the app
does not request organization resources"; OAuth apps "must be approved"; PATs blockable entirely or
made approval-gated
([About programmatic access](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/about-programmatic-access-in-your-organization)).
Its lifetime policy is a state machine with a specific shape: the default maximum for fine-grained PATs
is **366 days**, classic PATs "do not have an expiration requirement", non-compliant tokens are
"**blocked**" but — crucially — "**Setting this policy does not revoke or disable these tokens**…
Users will learn that their existing token is non-compliant when API calls for your organization are
**rejected**." So: `compliant` → `over-lifetime` → blocked at request time. Show the
blocked-and-still-present list; a row reading "lifetime: 366 days" hides the failure
([PAT policy](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/setting-a-personal-access-token-policy-for-your-organization)).

## Approval workflows for keys

**GitHub fine-grained PATs.** **Require administrator approval** is "the default value"; tokens created
by org owners skip it; public reads never need approval; "Only fine-grained personal access tokens, not
personal access tokens (classic), are subject to approval." Cadence is a digest: "GitHub will notify
organization owners with a **daily email** about all fine-grained personal access tokens that are
awaiting approval", and the requester is emailed on approve or deny. Queue: `Settings` → `Personal
access tokens` → **Pending requests**; detail shows "the access and permissions that the token is
requesting"; actions **Approve** / **Deny**, with "optionally enter the reason that you denied the
token. This reason will be shared in the notification that is sent to the token owner." Bulk via filters
**Owner** / **Repository** / **Permissions** → **Approve…** / **Deny…**. API constraint: "these endpoints
can only be called by GitHub Apps, and cannot be called with personal access tokens or OAuth apps"
([PAT policy](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/setting-a-personal-access-token-policy-for-your-organization),
[Managing PAT requests](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/managing-requests-for-personal-access-tokens-in-your-organization)).

**GitHub OAuth apps.** Restrictions are "**enabled by default**" for new orgs; owners "receive a
notification of pending requests"; review at `Settings` → **Third-party Access** → **OAuth app policy**
→ **Review** → **Grant access**. First-time enablement is destructive and enumerated: other OAuth apps
"immediately lose access", SSH keys created before February 2014 lose access, "Hook deliveries from
private organization repositories will no longer be sent to unapproved OAuth apps", and "users can
still authorize **privileged** OAuth apps". Revocation side effect: pre-existing webhooks "will no
longer be dispatched (these hooks will be **disabled, but not deleted**)"
([About OAuth app access restrictions](https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/about-oauth-app-access-restrictions),
[Approving OAuth apps](https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/approving-oauth-apps-for-your-organization)).

**Slack app approval** adds automation states: "Requests can be **approved, restricted, dismissed, or
flagged for human review**"; settings **Require approved apps**, **Allow members to request apps for
approval** (optional required comments), **Select App Managers** — "By default, any app requests that
need review are sent to Workspace Owners via Slack notifications"; and the scope semantics: "you are
approving **the scopes it will use**"
([Manage app approval](https://slack.com/help/articles/222386767-Manage-app-approval-for-your-workspace)).

**Stripe two-party approvals** are the richest state machine
([Approvals](https://docs.stripe.com/account/approvals)): seven approvable actions (bank account
add/update/delete; **admin invited to account**; payment intent created; refund created; subscription
created or canceled; credit note created; customer balance transaction created); conditions combinable
with `and`/`or` (**amount**, **actor** incl. agent-tagged keys, **rate limit**); two distinct controls —
**Require approval** ("The action is paused until a reviewer approves it") vs **Block** ("rejected
outright"); reviewers by person or role, with "**Only individually assigned team members receive email
notifications**"; per-rule "**custom justification instructions**" shown to requesters; "**Only one
active rule can apply to a given action**"; "Requests that haven't been approved within **14 days expire
automatically**"; "**A user can't approve their own request**". Agent keys are gated automatically:
tagging a RAK (`Authorizing agent access to your account`) applies default rules for **Refund is
created** and **Subscription is canceled**, and the API returns an **`approval_required`** error. Event
stream: `created`, `approved`, `rejected`, `canceled`, `expired`, `succeeded` ("the approved action
completed successfully"), `failed`. Edge case: "On single-user accounts, you can only save two-party
approval rules where the actor condition is set to `agent-tagged API keys`."

**Rules:** approval is a queue with `expired` as a real terminal state; require-approval and block are
never merged; denial captures a reason delivered to the requester; self-approval is blocked with the
reason shown; "blocked by policy" is distinguished from "invalid".

## Key rotation

"Rotating an API key **revokes it and generates a replacement key that's ready to use immediately**";
replacement names fixed (secret → `Secret key`, restricted → keeps its name). Flow: overflow → **Rotate
key** → **Expiration** dropdown (**Now** deletes the old key; a time shows remaining validity) →
**Rotate API key** → copy → note → **Done**
([API keys](https://docs.stripe.com/keys)). Four facts that must reach the UI:

- **Grace period:** "both the old and new keys work for **up to 7 days**… If you need more than 7 days,
  create a new key manually, migrate to it, then expire the old one when you're done."
- **Monitor before revoking:** "expire it only after its request volume has been at zero for a few hours
  or days." Per-key logs: overflow → **View request logs**.
- **Triggers:** key lost; key compromised; "a team member with access to the key leaves your organization
  or changes roles"; policy interval. Expiry is a separate action, and "**You can't expire a publishable
  key.**"
- **`Limited access`** is its own state: a key "hasn't been used to create transfers, payouts, or update
  payout destinations for over **180 days**" loses those abilities, remedied by **Restore access**.

**Access policies** ("have replaced IP address restrictions"): **IP addresses** (IPv4/CIDR) and
**Advanced** (ASNs to allow, countries to allow, sources to block — anonymous VPNs, public proxies,
residential proxies, Tor exit nodes; "Selecting multiple rules combines them using **AND** logic"),
recommended on all live keys because a blocked request notifies the owner. Deletion has a wide blast
radius: "Deleting an access policy immediately removes it from all API keys it was applied to. Those
keys allow requests from any source until you apply another policy to them."

**Rules:** rotation is two-phase and time-boxed (create → migrate → verify zero traffic → expire),
never one click; the grace window shows on the key row with an accelerate action; `limited access` is
distinct from `expired` and `revoked` and has a one-click remedy; deleting an access policy is treated
as security-relevant because it widens access everywhere at once.

## Endpoints and delivery states

Stripe: "You can register up to **16 webhook endpoints** with Stripe. Registered webhook endpoints must
be publicly accessible **HTTPS** URLs." Creation: Workbench → Webhooks → **Create an event
destination** → account → API version → event types → **Continue** → **Webhook endpoint** → **Endpoint
URL** + description → "a signing secret beginning with `whsec_` appears. Click **Reveal secret**". One
endpoint may serve several event types. Three delivery states are named: "whether they're **Delivered,
Pending, or Failed**", with per-event "HTTP status code of the delivery attempt and the time of
pending future deliveries". Failure taxonomy, vendor-diagnosed
([Receive Stripe events](https://docs.stripe.com/webhooks)):

| Status | Diagnosis |
|---|---|
| `200` | successful delivery |
| Unable to connect | "unable to establish a connection… make sure that your host domain is publicly accessible" |
| `3xx` | "**We consider redirect responses to webhook requests as failures.** Set the destination to the URL resolved by the redirect" |
| `4xx` | "can't or won't process the request… make sure your endpoint… accepts a **POST** HTTP method" |
| `5xx` | destination server error while processing |
| TLS error | certificate chain issue; "Stripe requires TLS version **v1.2** or higher" |
| Timed out | "return a successful response immediately" |

Retry: "up to **three days** with an exponential back off in live mode"; sandbox differs — "We retry
event deliveries created in a sandbox **three times** over the course of a few hours"; disabled
destinations stop retries, but disable-then-re-enable restores them. Manual resend windows differ by
surface: Dashboard **Resend** "up to **15 days**", CLI `stripe events resend` "up to **30 days**".
Recovery listing uses `ending_before`, `types[]`, `delivery_success=false`, and "Stripe only returns
events created in the last **30 days**"
([Process undelivered events](https://docs.stripe.com/webhooks/process-undelivered-events)).

GitHub inverts the model: "**GitHub does not automatically redeliver failed deliveries.**" Manual only,
"for the past **3 days**", via `Recent deliveries` → delivery **GUID** → **Redeliver**; and "If webhooks
are not active, the 'Recent Deliveries' section will not be present." Response contract: "respond with
a **2XX response within 10 seconds**… GitHub terminates the connection and considers the delivery a
failure" — as does Stripe: "Quickly returns a successful status code (2xx) before any complex logic".
Its endpoint creation form is **Payload URL**, **Content type** (`application/json` or
`application/x-www-form-urlencoded`), **Secret**, event selection and an **Active** checkbox — then
"GitHub will send you a simple **ping event**". Scoped by role: repository webhooks need repository
owner or admin; organization webhooks need an organization owner; Marketplace/Sponsors webhooks are
owned by the app or account owner, with app managers also able to act
([Redelivering webhooks](https://docs.github.com/en/webhooks/testing-and-troubleshooting-webhooks/redelivering-webhooks),
[Best practices](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks),
[Creating webhooks](https://docs.github.com/en/webhooks/using-webhooks/creating-webhooks)).

**Rules:** three named states minimum, plus HTTP status and next-retry time on Pending and Failed
rows; surface the redirect case explicitly (operators assume 3xx is success); the retry window is
readable and environment-specific — never quote the live 3-day window for a sandbox endpoint; resend
window is labelled with its own date arithmetic; the ping acknowledgement is visible on a new endpoint.

## Signing verification UX

GitHub's contract ([Validating webhook deliveries](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries)):
header **`X-Hub-Signature-256`**; "GitHub uses an HMAC hex digest"; "The hash signature **always starts
with `sha256=`". Three steps — create a secret token ("a random string of text with high entropy"),
store it ("Never hardcode a token into an application or push a token to any repository"), validate.
Encoding: "ensure that you handle the payload as **UTF-8**. Webhook payloads can contain unicode
characters." Comparison: "**Never use a plain `==` operator.** Instead consider using a method like
`secure_compare` or `crypto.timingSafeEqual`, which performs a 'constant time' string comparison".
**Published test vectors**: secret `It's a Secret to Everybody`, payload `Hello, World!` →
`sha256=757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17`. Replay: use
`X-GitHub-Delivery` "to ensure that each delivery is unique per event", with the caveat "If you request
a redelivery, the `X-GitHub-Delivery` header will be the same as in the original delivery". Never put
credentials in the URL — "do **not** include sensitive information in your payload URL" — and
defence in depth via `GET /meta` IP allow-listing, since "GitHub occasionally makes changes to its IP
addresses" ([Best practices](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks)).

Stripe adds a raw-body requirement that must be stated verbatim in the receiving docs:

> "**Don't manipulate the raw body request.** Stripe requires the raw body of the request to perform
> signature verification… **Any manipulation to the raw body of the request causes the verification to
> fail.**"

Verification uses the JSON payload, the **`Stripe-Signature`** header and the `whsec_` secret; and
"Webhook signing secrets aren't API keys — they're per-webhook secrets"
([Receive Stripe events](https://docs.stripe.com/webhooks), [API keys](https://docs.stripe.com/keys)).

**Rules:** ship test vectors so a handler is verifiable before go-live; the signing secret is
per-endpoint and follows the once-only reveal rule; put the constant-time comparison warning inside
the code sample, not in prose above it; ship replay-dedup guidance together with the redelivery caveat.

## Not found

- **Not found:** a documented maximum number of webhook endpoints for GitHub (Stripe's is 16). What
  would settle it: a GitHub docs page stating an endpoint cap.
- **Not found:** a documented signing-secret rotation procedure or grace period (Stripe documents a
  7-day grace period for API keys only). What would settle it: a Stripe webhooks page on rotating
  `whsec_` secrets.
- **Not found:** Stripe webhook *health alerts* content — `https://docs.stripe.com/stripe-health-alerts`
  returned 404. What would settle it: its current canonical URL.

## Sources

- https://docs.stripe.com/keys — Stripe — accessed 2026-10-05
- https://docs.stripe.com/keys/restricted-api-keys — Stripe — accessed 2026-10-05
- https://docs.stripe.com/account/approvals — Stripe — accessed 2026-10-05
- https://docs.stripe.com/webhooks — Stripe — accessed 2026-10-05
- https://docs.stripe.com/webhooks/process-undelivered-events — Stripe — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/about-programmatic-access-in-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/setting-a-personal-access-token-policy-for-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/managing-requests-for-personal-access-tokens-in-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/about-oauth-app-access-restrictions — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/approving-oauth-apps-for-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/webhooks/using-webhooks/creating-webhooks — GitHub — accessed 2026-10-05
- https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks — GitHub — accessed 2026-10-05
- https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries — GitHub — accessed 2026-10-05
- https://docs.github.com/en/webhooks/testing-and-troubleshooting-webhooks/redelivering-webhooks — GitHub — accessed 2026-10-05
- https://docs.github.com/enterprise-cloud@latest/organizations/granting-access-to-your-organization-with-saml-single-sign-on/viewing-and-managing-a-members-saml-access-to-your-organization — GitHub — accessed 2026-10-05
- https://slack.com/help/articles/222386767-Manage-app-approval-for-your-workspace — Slack — accessed 2026-10-05