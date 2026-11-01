# Multi-tenant workspaces

Framing: a tenant switcher is the highest-consequence control in the product. Getting it wrong means
the user believes they are acting in one customer's data while acting in another's. Three rules follow:
**the current tenant must be unmissable, the switch must be deliberate, and isolation must be visible
rather than implied.**

## The two-level hierarchy

Stripe's terminology separates container from business cleanly: a **tenant / organisation / workspace**
holds business entities, and Stripe is explicit that an organization "acts as a **container structure**
to view and manage the operation of its separate businesses" — and "**an organization doesn't conduct its
own business through Stripe.**" An **account** is where work happens: it "processes payments and has
balances, customers, subscriptions, and more." In your product the workspace owns membership, settings,
and billing; the project or account owns the data. Getting the levels backwards produces a UI where
changing a workspace setting changes someone's actual records.

Google Cloud's `projects` make the split from the infrastructure side, naming four roles one object
plays: "The primary service container… **The trust boundary**: Projects serve as an isolation layer. By
default, resources in one project don't have access to resources in another… **The billing unit**… **The
policy attachment point**" (Google Cloud, Create projects). Four jobs, one record — a useful checklist
for what a tenant-level object must actually own.

## The switcher pattern

Carbon's UI shell header is the reference placement, and its reasoning is explicit: for each shell
component "left-to-right translates to product-to-global… **Elements on the right side of the header, such
as the switcher, are the most global in their scope and span multiple products**," and "**The switcher
should always be positioned as the furthest right icon. This ensures the icon does not shift when navigating
across systems.**" On content: "Recommended uses for this component include **recently used apps, frequently
used apps, or all apps attached to the user's account.**" Stripe uses the same corner-anchored name: "To
switch the account you're currently viewing in the Dashboard, click the name of your current Stripe account
in the upper-left corner and then select the account to switch to."

The trigger carries name + avatar + chevron, never an icon alone — two similarly-named tenants become
indistinguishable. The current tenant is named in full in normal flow, persistent, not only inside the
trigger. The list shows recently used first, then alphabetical, with search past roughly ten entries.
Switching is instant and closes the menu, with **no confirmation** — a switch is not destructive. Each row
shows the user's role in that tenant ("Admin"), because it changes what the next screen can do. A tenant
the user cannot access is shown **disabled with the reason**, never hidden: a member of twelve workspaces
who can see four must know eight exist. Last-used persists per user, and the tenant lives in the URL so a
shared link opens the right one. Never bury the switcher in a settings page — it is the one control that
changes what every other control acts on.

## Tenant context propagation

The tenant id must be carried in a way that cannot silently disagree with the UI.

- **URL is the source of truth for the visible tenant.** `/acme/settings`, not
  `/settings?tenant=acme` on a route whose siblings are not. Every in-app link must be
  tenant-prefixed; a link that drops the prefix lands somewhere that looks right and is the wrong
  tenant.
- **The server resolves the tenant from the path, then authorises.** Never trust a client-supplied
  tenant header alone.
- **Every API call carries the tenant**, with membership and role re-checked server-side per call.
- **Caches are tenant-keyed.** A query cache keyed only on resource id is the classic cross-tenant
  leak; key on `(tenant, resource)` or scope the store per tenant.
- **Background jobs, exports, webhooks, and emails capture the tenant at enqueue time**, not at
  delivery time. A report rendered under the wrong tenant is a disclosure bug.
- **On switch, tear down tenant-scoped state**: in-flight fetches, optimistic caches, unsaved draft
  buffers, expanded tree nodes, scroll positions.
- **Draft text is per tenant.** Losing a paragraph someone wrote in the wrong workspace because a
  switch happened is the bug users report loudest.

## Per-tenant versus global settings

**Tenant-scoped, edited by tenant admins:** name, logo and description; members, roles and invitations;
data retention, region and encryption policy (often gated); the audit log, viewable per tenant.
**Org- or plan-level:** billing and plan (billing admin); SSO and SCIM provisioning (org admin);
cross-tenant consolidated reporting, on an org-level surface writable only by org admins. **User-scoped:**
notification preferences, which belong to the individual — Stripe: "If multiple team members have access to
your account, **each one can set their own notification preferences**."

The boundary rule: **a setting that changes only that person's notifications is personal, not
tenant-wide.** Everything that changes how other members experience the product is tenant-wide.
Getting this backwards is the most-reported settings complaint pattern in B2B products.

## Data isolation as a UI concern

Isolation is enforced server-side, but the UI must not *misrepresent* it.

- **Make the boundary visible on the record**, not only in the URL. In a support console the tenant is
  a persistent context strip, not a breadcrumb the user scrolls past.
- **Cross-tenant views are a separate surface with a distinct frame.** An org-level dashboard mixing
  tenants must be visually unmistakable — a scope label or banner — so a screenshot of it is never
  mistaken for a single-tenant view.
- **Cross-tenant actions confirm with the tenant named**: "Delete 4 records from **Acme Corp**", not
  "Delete 4 records".
- **Never offer autofill that crosses tenants.** Suggestions drawn from another tenant's records are a
  leak with a keyboard.
- **Sign out of one tenant is not sign out of all** — unless it is. Say which.
- **Destructive and export actions name their blast radius**: how many records, in which tenant,
  whether reversible. This is `craft-floor.md`'s consequence-before-click rule on the tenant axis.

## Cross-tenant administration (Stripe Organizations as the model)

Stripe's Organizations is the published reference for centralising administration over multiple
accounts: "**Centralize reporting, operations, and team management** across your enterprise," letting a
business "Gauge [its] entire business' performance," see "all of your transactions, disputes, invoices,
connected accounts, customers, and more," "Download unified reports across currencies," and "**Search
globally**" across "all of the accounts they have access to." Account groups add named subsets for
analysis — "**Account groups work like tags: each account can belong to multiple groups simultaneously**,"
filterable across "Dashboard pages, list views, Sigma queries, and Report." Resource sharing lets accounts
"build a shared customer base while safeguarding proprietary and sensitive data," but Stripe labels that
capability **"Public preview"** on the page checked — do not present it as GA on the strength of this.

The architectural lesson: **an organization is a navigation and reporting container, never a place where
work happens.** An org-level surface answers "how is my whole portfolio doing" and carries no create/edit
affordances on any account's data. The operational constraints are what shape the UI:

- **Scale limit**: "You can add up to **75 accounts**," and "each account can belong to only one
  organization." One parent per child — a hard constraint your switcher and any move UI must respect and,
  where relevant, explain.
- **Elevation required**: "The person who creates the organization must be a **Super Administrator** in
  each account added to the organization." Adding a tenant is privileged and often cross-team, so it is an
  invite-and-approve flow, not a silent append. An Administrator who is not Super Admin "can send an
  **invite to the Super Administrator**."
- **Irreversible edge**: "If you remove every account from an organization, Stripe **permanently closes**
  it." That is a destructive confirm.
- **Hidden side effect on removal**: "If you remove an account from an organization, we automatically
  remove the account from all data pipelines in the organization," and you "must assign account-level roles
  to any users who inherited them from the organization." Again consequence-before-click.
- **Identity consolidation**: "You must **Consolidate the IdPs** of any accounts with SSO enabled before you
  add them," and after creation "SSO configuration for all accounts transfers to the organization,"
  requiring an IdP attribute statement change from `Stripe-Role-acct_id` to `Stripe-Role-org_id`. Stripe
  names the failure mode: "Failure to update your SSO integration can result in **restricted user access**."
  Every tenant-adding screen must state this *before* the action, not after the lockout.

## Naming collisions

Four collisions recur. When an organisation and an account share a name, switcher rows look identical —
show a distinguishing attribute per row (avatar, plan, region, member count). When two accounts are both
called "Staging", enforce uniqueness within the organisation at creation and show the conflict in the
field, not at submit. When a rename would break bookmarked links, follow Google Cloud's split: the
project "name" is editable "at any time" while the "ID" is "**permanent**" and the name "**isn't used by
any** Google APIs" — so the UI edits the name and never the id. And when one org is named differently in
billing, admin, and email, there must be a single source of truth for the display name.

Google Cloud adds one more rule, directly applicable: "**Don't include sensitive information**, for
example, personally identifiable information or security data, in your project name, project ID, or
other resource names," because the id "appears in the name of many other resources."

**Not found:** no primary source consulted specifies a maximum tenants per user, a tenant-switch
frequency limit, or a required session behaviour on tenant change. State any such limits in
`DESIGN.md`.

## Sources

- [Stripe Organizations](https://docs.stripe.com/get-started/account/orgs) — Stripe Documentation, accessed 2026-10-05
- [Supported Organization setups](https://docs.stripe.com/get-started/account/orgs/setup) — Stripe Documentation, accessed 2026-10-05
- [Build an organization](https://docs.stripe.com/get-started/account/orgs/build) — Stripe Documentation, accessed 2026-10-05
- [Multiple separate accounts](https://docs.stripe.com/get-started/account/multiple-accounts) — Stripe Documentation, accessed 2026-10-05
- [Account checklist](https://docs.stripe.com/get-started/account/checklist) — Stripe Documentation, accessed 2026-10-05
- [UI shell header](https://www.carbondesignsystem.com/building-blocks/core/components/ui-shell-header/guidelines) — Carbon Design System (IBM), accessed 2026-10-05
- [Create projects](https://cloud.google.com/resource-manager/docs/creating-managing-projects) — Google Cloud Documentation, accessed 2026-10-05