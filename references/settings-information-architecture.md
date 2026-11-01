# Settings information architecture

Reference for designing the settings tree of a logged-in B2B SaaS product. Vendor behaviour is
attributed to the vendor that documents it; the design rules are this skill's, not theirs.

## The four-level split

Real products do not have one "Settings" page. They split by **whose** setting it is and **how many
of them exist**.

| Level | Owner of the decision | Stripe's name | Slack's name |
|---|---|---|---|
| The person | Only this user | Personal | (per-user profile) |
| The tenant | Admins of one account/org | Account | Workspace / Organization |
| The feature | Admins of one product surface | Product | per-feature settings (Channels, Apps and workflows) |
| The device | The user's own client | (sessions, under personal details) | Desktop / Mobile session duration |

Stripe splits its Dashboard settings into exactly three categories: **Personal, Account, Product**
([Stripe, Dashboard basics](https://docs.stripe.com/dashboard/basics)). Under *Account* it lists
account details, personal details (password, communication preferences, **active sessions**), PCI
compliance, documents, early access, plus **Team and security** (invite team members) and Branding.
Under *Product* it lists ten destinations, one per product: Billing, Financial connections, Radar,
Card issuing, Identity verification, Sigma, Connect, Payments, Tax, Data pipeline.

Slack makes the same split a **nav shape**, not a page: workspace admins go `Admin` → `Workspace
settings`; Enterprise org admins go `org name` → `Tools & settings` → `Organization settings`, then
a left sidebar of `Settings`, `Security`, `Security settings`, `SSO Settings`, `Audit logs`,
`Roles & permissions`, `Authentication security`
([Slack, Manage session duration](https://slack.com/help/articles/115005223763-Manage-session-duration),
[Slack, Manage single sign-on settings](https://slack.com/help/articles/220403548-Manage-single-sign-on-settings),
[Slack, Create custom roles](https://slack.com/help/articles/29800891169939-Create-custom-roles)).
GitHub uses the same two-hop entry — org name → `Settings` → a left sidebar whose named sections
include `People`, `Code and automation`, `Third-party Access`, `Personal access tokens`,
`Organization security`, `Security & analysis`, `Authentication security`
([GitHub, Creating webhooks](https://docs.github.com/en/webhooks/using-webhooks/creating-webhooks),
[GitHub, Approving OAuth apps](https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/approving-oauth-apps-for-your-organization),
[GitHub, Enforcing SAML SSO](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/enforcing-saml-single-sign-on-for-your-organization),
[GitHub, Setting a PAT policy](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/setting-a-personal-access-token-policy-for-your-organization),
[GitHub, Accessing the audit log](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/accessing-the-audit-log-for-your-enterprise)).

**Rule:** name the level in the label. "Account settings", "Workspace settings", "Product settings".
A user asking "where do I change this?" is asking which level owns it.

## Grouping and labelling

- **Group by job, not by object type.** Slack's own admin taxonomy is job-shaped: *Manage members,
  Manage channels, Manage billing payments & plans, Workspace settings & permissions, Workspace
  customization, Enterprise settings & permissions, Manage apps & workflows, Configure access &
  security, Slack data & analytics* — exactly nine groups
  ([Slack, Workspace administration](https://slack.com/help/categories/200122103-workspace-administration)).
  Note that *members*, *channels*, and *apps* are objects, but each group is phrased as a verb
  phrase. Billing is the only noun group, and it is a noun because the object is money.
- **Never cap the group count.** GitHub's org settings sidebar carries more than ten named
  sections; Slack's help taxonomy carries 9 groups containing hundreds of articles.
  ([GitHub, Managing organization settings](https://docs.github.com/en/organizations/managing-organization-settings))
- **One group owns one permission tier.** Stripe puts "invite team members" under *Team and
  security*, not under *People*, because inviting is an access action
  ([Stripe, Dashboard basics](https://docs.stripe.com/dashboard/basics)).

## Page vs inline toggle

Use an inline toggle only when the setting is **reversible in one click, needs no other field, and
is readable in place**. Everything else earns a page.

- Slack documents the toggle-shaped settings as *rows with an Edit affordance*, not switches:
  session duration is `Edit` next to **Desktop session duration** / **Mobile session duration**;
  2FA is `Edit` next to **Two-factor authentication for email sign-in**; SSO is `Edit` next to each
  of **Require SSO authentication**, **Sync user profiles**, **Email address changes**, **Display
  name changes** ([Slack, Manage session duration](https://slack.com/help/articles/115005223763-Manage-session-duration),
  [Slack, Mandatory 2FA](https://slack.com/help/articles/212221668-Mandatory-workspace-two-factor-authentication),
  [Slack, Manage SSO settings](https://slack.com/help/articles/220403548-Manage-single-sign-on-settings)).
  The reason is checkable: each of those opens a **sub-dialog or sub-page with its own Save**, and
  each has consequence text that must be read before committing.
- Slack's genuinely inline surfaces are the *filter* facets (members → `Filter` → **Two-factor
  (2FA)**) and *checkbox* permission rows (Permissions tab → Invitations → **Require admin
  approval**) ([Slack, Mandatory 2FA](https://slack.com/help/articles/212221668-Mandatory-workspace-two-factor-authentication),
  [Slack, Require admin approval for invitations](https://slack.com/help/articles/115004854783-Require-admin-approval-for-invitations-to-Slack)).
- GitHub documents an explicit **Check**-then-**Save** form for every security toggle, and the
  destructive one gets a named confirmation button: *Remove members and require SAML single
  sign-on* ([GitHub, Enforcing SAML SSO](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/enforcing-saml-single-sign-on-for-your-organization)).

## Dangerous settings placement

- Put irreversible settings **last in their group, in a visually distinct zone**, never inline
  beside a safe neighbour.
- GitHub files `Archive an organization` and `Delete organization` under *Manage organization
  settings*, as siblings of benign actions like *Renaming an organization* — the group does not
  isolate them; ordering and weight must
  ([GitHub, Managing organization settings](https://docs.github.com/en/organizations/managing-organization-settings)).
  Slack files `Transfer ownership of a workspace or org` and `Delete a workspace` in the same
  *Workspace settings & permissions* group as ~50 benign items
  ([Slack, Workspace administration](https://slack.com/help/categories/200122103-workspace-administration)).
- Name the consequence in the label: `Delete workspace`, not `Remove`.
- Ownership transfer is a separate group from deletion in both vendors' taxonomies.
  **Not found:** any vendor statement that a destructive action must be visually isolated from its
  group. What would settle it: a design-system or accessibility guideline (e.g. a W3C/ARIA or
  vendor design system doc) naming destructive placement; none of the fetched pages address it.

## Search within settings

- **Not found:** a vendor-documented "search settings" affordance. What would settle it: a product
  help page or docs page describing a settings search box. Neither Slack's workspace-administration
  category, Stripe's Dashboard basics, nor GitHub's org settings index documents one.
- What does exist is **object search scoped to the tenant**, and it is a different tool:
  Stripe's Dashboard search spans payments, customers, invoices, payouts, products and connected
  accounts, accepts `field:value` filters (`amount:`, `country:`, `status:`, `last4:`, `receipt:`)
  and `-` negation, and can search **across every account in an organization**
  ([Stripe, Perform searches in the Dashboard](https://docs.stripe.com/dashboard/search)).
  GitHub's audit-log search is a qualifier language over log entries, not a settings search
  ([GitHub, Searching the audit log](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/searching-the-audit-log-for-your-enterprise)).
- Stripe documents a precision cost worth designing around: "the more terms you provide your search
  query, the fewer the number of results"
  ([Stripe, Dashboard search](https://docs.stripe.com/dashboard/search)). Show a result count and
  offer a widening control.
- **Recency beats taxonomy for the top of the tree.** Stripe's Dashboard has a **Shortcuts**
  section that shows pinned and most recently visited pages
  ([Stripe, Dashboard basics](https://docs.stripe.com/dashboard/basics)).

## Settings depth and the 3-click rule

Skill rule (`craft-floor.md`): every route reachable in ≤ 3 clicks from the nav root. Vendor reality
is deeper, which is why the vendors add shortcuts and search rather than flattening the tree.

- Measured against the fetched paths: Stripe's key rotation is **Settings → (product) → API keys →
  overflow menu → Rotate key → confirmation** = 5 interactions
  ([Stripe, API keys](https://docs.stripe.com/keys)). GitHub's token approval is **Settings →
  Personal access tokens → Pending requests → token → Approve** = 4
  ([GitHub, Managing requests for PATs](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/managing-requests-for-personal-access-tokens-in-your-organization)).
- Compensation patterns actually shipped: a **Shortcuts/recents** section (Stripe), a
  **searchable index of pending work** (GitHub `Pending requests`, Slack `Invitations → Pending`),
  and **deep links from notification emails** (GitHub: "If you deny the request, in the confirmation
  box, optionally enter the reason… this reason will be shared in the notification that is sent to
  the token owner").
- **Rule:** anything an admin does more than weekly gets a shortcut, a pending-work surface, or an
  emailed deep link — the tree may stay deep.

## Checkable rules

1. Every settings entry names its level (Personal / Account / Workspace / Product).
2. Group labels are job-shaped verb phrases; no arbitrary cap on group count.
3. Any setting that opens a Save has its own row + Edit, not a bare switch, when it has consequence
   text or dependent fields.
4. Irreversible actions are last in their group, styled distinctly, and named as consequences.
5. A tenant-wide search exists and spans the tenant's accounts/objects, with a visible result count.
6. A recents/shortcuts surface exists at the top of the tree.
7. Depth > 3 is compensated by shortcuts, pending-work queues, or emailed deep links — never by
   flattening the taxonomy into an unlabelled list.

## Sources

- https://docs.stripe.com/dashboard/basics — Stripe — accessed 2026-10-05
- https://docs.stripe.com/dashboard/search — Stripe — accessed 2026-10-05
- https://slack.com/help/categories/200122103-workspace-administration — Slack — accessed 2026-10-05
- https://slack.com/help/articles/115005223763-Manage-session-duration — Slack — accessed 2026-10-05
- https://slack.com/help/articles/220403548-Manage-single-sign-on-settings — Slack — accessed 2026-10-05
- https://slack.com/help/articles/212221668-Mandatory-workspace-two-factor-authentication — Slack — accessed 2026-10-05
- https://slack.com/help/articles/115004854783-Require-admin-approval-for-invitations-to-Slack — Slack — accessed 2026-10-05
- https://slack.com/help/articles/29800891169939-Create-custom-roles — Slack — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-organization-settings — GitHub — accessed 2026-10-05
- https://docs.github.com/en/webhooks/using-webhooks/creating-webhooks — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/approving-oauth-apps-for-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/enforcing-saml-single-sign-on-for-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/setting-a-personal-access-token-policy-for-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/accessing-the-audit-log-for-your-enterprise — GitHub — accessed 2026-10-05