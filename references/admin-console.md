# Admin console

Reference for the logged-in admin surface: the status strip, the outstanding-task queues, and the
line between an admin console and an end-user dashboard. Vendor behaviour is attributed.

## What an admin console is for

An end-user dashboard answers *"how is my work going?"*. An admin console answers three different
questions, and only these three:

1. **Is the tenant healthy?** — posture, plan, licence, spend, service state.
2. **What is waiting for me?** — approvals, invitations, failed deliveries, flagged content.
3. **Who can do what?** — members, roles, scopes, sessions.

Slack's workspace-administration taxonomy is exactly this shape: *Manage members*, *Manage
channels*, *Manage billing payments & plans*, *Workspace settings & permissions*, *Workspace
customization*, *Enterprise settings & permissions*, *Manage apps & workflows*, *Configure access &
security*, *Slack data & analytics* — nine groups
([Slack, Workspace administration](https://slack.com/help/categories/200122103-workspace-administration)).
Note that analytics is **inside** the admin surface, not a separate product area.

Stripe keeps the same split but names it differently: the *Home* page is business performance
("analytics and charts about your business performance") plus **notifications like unresolved
disputes or identity verifications**, with a **Your overview** widget picker (Add / Remove /
Apply / Edit); admin configuration lives under Settings → Account / Product; task-oriented product
surfaces live under a *Products* section
([Stripe, Dashboard basics](https://docs.stripe.com/dashboard/basics)).

**Rule:** if a screen serves an end user's daily work and an admin's oversight at the same time,
split it. Stripe's Home is a *business* overview; an admin's configuration is one hop away in
Settings, not interleaved.

## At-a-glance status

The status strip should carry only what changes a decision.

- **Plan / licence state.** Slack gates features by plan and states the gate on the feature itself
  ("Available on all plans", "Available on Business+ and Enterprise plans"), so the console must be
  able to answer "is this a settings gap or a plan gap?"
  ([Slack, Manage SSO settings](https://slack.com/help/articles/220403548-Manage-single-sign-on-settings)).
- **Security posture with numbers, not adjectives.** GitHub's *Authentication security* section
  shows **counts** of user tokens and keys authorized for SSO, and only then offers the bulk action
  ([GitHub, Viewing and managing a member's SAML access](https://docs.github.com/enterprise-cloud@latest/organizations/granting-access-to-your-organization-with-saml-single-sign-on/viewing-and-managing-a-members-saml-access-to-your-organization)).
- **Notification surfacing is a first-class widget.** Stripe's Home "surfaces important
  notifications, like unresolved disputes or identity verifications"
  ([Stripe, Dashboard basics](https://docs.stripe.com/dashboard/basics)).
- **Service status.** Both vendors run a separate status domain rather than embedding state in the
  console: `slack-status.com`, linked from the help centre footer, and `status.stripe.com`
  ([Slack, Workspace administration](https://slack.com/help/categories/200122103-workspace-administration),
  https://status.stripe.com/ — accessed 2026-10-05).
- **Recent activity is the admin's landing content.** GitHub's enterprise audit log is the canonical
  "what just happened" surface, reached from enterprise `Settings` → `Audit log`
  ([GitHub, Accessing the audit log](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/accessing-the-audit-log-for-your-enterprise)).
  Slack's admin dashboard equivalent is *Audit logs* under `Security`, plus a *Security Detections*
  tab for anomaly events ([Slack, Audit logs in Slack](https://slack.com/help/articles/360000394286-Audit-logs-in-Slack)).
- **Configure the status strip.** Stripe lets the admin Add or Remove overview widgets
  ([Stripe, Dashboard basics](https://docs.stripe.com/dashboard/basics)). **Not found:** any vendor
  statement on whether an admin's status strip should be configurable per-role. What would settle
  it: a vendor help page on admin dashboard personalization; only Stripe's per-user Home
  customization is documented.

## Outstanding tasks

The console's highest-value region is a queue of decisions waiting on *this* admin. Vendor-documented
queue types, each with its own state model:

| Queue | Vendor-documented states | Where it lives |
|---|---|---|
| Approval requests for sensitive actions | pending → approved (action completes) / denied (no changes); **auto-expire after 14 days**; a user can't approve their own request | Stripe `Settings > Approvals > Requests`, filterable by status ([Stripe, Set up two-party approvals](https://docs.stripe.com/account/approvals)) |
| Agent-key approval requests | `created`, `approved`, `rejected`, `canceled`, `expired` (after 14 days), `succeeded`, `failed` | Stripe webhook events `v2.core.approval_request.*` ([Stripe, Approvals](https://docs.stripe.com/account/approvals)) |
| App / OAuth access requests | pending → Review → Grant access / Deny, with an optional denial reason shared to the requester; daily email digest of pending fine-grained token requests | GitHub `Settings > Third-party Access > OAuth app policy`, `Settings > Personal access tokens > Pending requests` ([GitHub, Approving OAuth apps](https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/approving-oauth-apps-for-your-organization), [GitHub, Managing PAT requests](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/managing-requests-for-personal-access-tokens-in-your-organization)) |
| Invitations | pending (extend / resend / delete) and invite links (deactivate / renew expired); expiry at **30 days** | Slack `Admin > Workspace settings > People > Invitations`, two tabs |
| Flagged content | flag submitted → assigned → dismissed / hidden / replaced / restored; optional required note; History tab of decisions | Slack `Organization settings > Security > Flagged content` ([Slack, Review flagged content](https://slack.com/help/articles/25273135315347-Review-flagged-content-in-Slack)) |
| Security anomaly events | anomaly entry → *Sign Out Of Slack* action, or an automatic anomaly-event response | Slack *Security Detections* tab ([Slack, Audit logs](https://slack.com/help/articles/360000394286-Audit-logs-in-Slack)) |

Rules the queues force:

- **Every queue item names its age and its expiry.** Slack: "Invitations and invite links will expire
  after 30 days" ([Slack, Manage pending invitations](https://slack.com/help/articles/360060363633-Manage-pending-invitations-and-invite-links-for-your-workspace)).
  Stripe: requests expire at 14 days ([Stripe, Approvals](https://docs.stripe.com/account/approvals)).
  GitHub: invitations expire at 7 days, releasable into a **Failed invitations** view for retry or
  cancel ([GitHub, Inviting users](https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization)).
- **A denial must accept a reason that reaches the requester.** GitHub: "optionally enter the reason
  that you denied the token. This reason will be shared in the notification that is sent to the
  token owner." Stripe: "custom justification instructions" are defined per rule and shown to the
  requester when they request a sensitive action ([Stripe, Approvals](https://docs.stripe.com/account/approvals)).
- **Route the queue to a named audience.** Slack lets admins choose whether invitation requests go to
  all admins by Slack notification or to a **specific channel**, and appoint **app managers** to
  handle app requests ([Slack, Require admin approval for invitations](https://slack.com/help/articles/115004854783-Require-admin-approval-for-invitations-to-Slack),
  [Slack, Manage app approval](https://slack.com/help/articles/222386767-Manage-app-approval-for-your-workspace)).
- **Support bulk selection.** GitHub's token-request queue documents filters (Owner, Repository,
  Permissions) and bulk **Approve…** / **Deny…** ([GitHub, Managing PAT requests](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/managing-requests-for-personal-access-tokens-in-your-organization)).
- **The queue must be permission-aware.** Slack's *Audit logs* is reachable by Org Owners and members
  with the **Audit Logs Admin** system role; exporting search-query logs requires a custom role
  carrying both **Access search query logs** and **Read audit logs**
  ([Slack, Audit logs](https://slack.com/help/articles/360000394286-Audit-logs-in-Slack)). An admin
  sees a queue filtered to what they may act on, never a global list with disabled buttons.
- **Never let a queue be the only path to a destructive action.** GitHub's SSO-authorization revoke
  offers three granularities: per member, per credential type, and bulk across all members — each a
  distinct action, not one scary button
  ([GitHub, Viewing and managing a member's SAML access](https://docs.github.com/enterprise-cloud@latest/organizations/granting-access-to-your-organization-with-saml-single-sign-on/viewing-and-managing-a-members-saml-access-to-your-organization)).

## Scoped admin search

- **Search must be scoped to what this admin may see, and must say so.** Stripe: after adding
  accounts to an organization, "your team members can search across all of the accounts they have
  access to", and results display from all of those accounts by default
  ([Stripe, Dashboard search](https://docs.stripe.com/dashboard/search)). "All of the accounts they
  have access to" is the sentence a scope indicator should be able to reproduce.
- **Facet-first beats text-first in admin surfaces.** GitHub's audit log: "You can search directly
  from the user interface by using the **Filters** dropdown, or by typing a search query… You cannot
  search for entries using text" — filter chips first, query language second
  ([GitHub, Searching the audit log](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/searching-the-audit-log-for-your-enterprise)).
  Slack's audit-log **Filter** offers exactly four facets: **Date range, Acting user, Affects (user,
  workspace, or organization), Events** ([Slack, Audit logs](https://slack.com/help/articles/360000394286-Audit-logs-in-Slack)).
- Members list filters are the other canonical scoped search: Slack members → `Filter` → under
  **Authentication**, check **Two-factor (2FA)** ([Slack, Mandatory 2FA](https://slack.com/help/articles/212221668-Mandatory-workspace-two-factor-authentication)).
- Filter rows on the pending-token queue by **Owner / Repository / Permissions**, not by name
  ([GitHub, Managing PAT requests](https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/managing-requests-for-personal-access-tokens-in-your-organization)).

## Admin console vs end-user dashboard

| | End-user dashboard | Admin console |
|---|---|---|
| Primary verb | do / review my work | configure / approve / investigate |
| Home content | my tasks, my records | posture, queues, recent activity |
| Identity | one user's permissions | a role **plus a scope** (org, workspace, IdP group) |
| Vocabulary | product nouns (invoice, channel, repo) | governance nouns (role, scope, policy, session) |
| Navigation | product surfaces | settings tree + queues + audit log |
| Consequence of a wrong click | recoverable edit | sends emails, removes members, rotates a key |

Evidence for the split, per vendor:

- Slack runs **two** consoles with different entry points and different permissions: workspace
  `Admin` → `Workspace settings` for Workspace Owners/Admins, and `Tools & settings` →
  `Organization settings` for Org Owners/Admins; invitations are managed from the manage-members page
  at workspace level and from the admin dashboard at org level
  ([Slack, Manage pending invitations](https://slack.com/help/articles/360060363633-Manage-pending-invitations-and-invite-links-for-your-workspace)).
  Slack also restricts what each tier may touch: Workspace Admins "can't access the Billing page or
  manage billing details"; Org Owners "can view a list of custom roles… but can't create or edit
  them" ([Slack, Types of roles in Slack](https://slack.com/help/articles/360018112273-Types-of-roles-in-Slack),
  [Slack, Create custom roles](https://slack.com/help/articles/29800891169939-Create-custom-roles)).
- Stripe gates admin work by role *and* plan: IAM Administrator "can't do anything beyond access
  management"; by default only team members with the **Administrator** role can create or edit
  approval rules; Security history sits under `Settings > Team and security`
  ([Stripe, User roles](https://docs.stripe.com/get-started/account/teams/roles), [Stripe, Approvals](https://docs.stripe.com/account/approvals)).
- Okta's rule is the cleanest statement of the boundary: "Users and groups with assigned admin roles
  have access to the Admin Console. They also have access to the permissions resources that are
  included in the assignment."
  ([Okta, Work with the admin component](https://help.okta.com/oie/en-us/content/topics/security/custom-admin-role/work-with-admin.htm))

**Rules**

1. The console's home states posture + queues + recent activity. It does not replay product work.
2. Every queue item carries age, expiry, and a named next action.
3. Denials capture a reason that is delivered to the requester.
4. Queues and search results are scoped to the acting admin's grants; the scope is stated in words.
5. Destructive incident actions come in at least two granularities (one member / one credential type /
   all members) rather than a single global button.
6. An admin console and an end-user dashboard never share a home screen.

## Sources

- https://docs.stripe.com/dashboard/basics — Stripe — accessed 2026-10-05
- https://docs.stripe.com/dashboard/search — Stripe — accessed 2026-10-05
- https://docs.stripe.com/account/approvals — Stripe — accessed 2026-10-05
- https://docs.stripe.com/get-started/account/teams/roles — Stripe — accessed 2026-10-05
- https://slack.com/help/categories/200122103-workspace-administration — Slack — accessed 2026-10-05
- https://slack.com/help/articles/360018112273-Types-of-roles-in-Slack — Slack — accessed 2026-10-05
- https://slack.com/help/articles/29800891169939-Create-custom-roles — Slack — accessed 2026-10-05
- https://slack.com/help/articles/360024686174-Invited-members-in-Slack — Slack — accessed 2026-10-05
- https://slack.com/help/articles/360060363633-Manage-pending-invitations-and-invite-links-for-your-workspace — Slack — accessed 2026-10-05
- https://slack.com/help/articles/115004854783-Require-admin-approval-for-invitations-to-Slack — Slack — accessed 2026-10-05
- https://slack.com/help/articles/222386767-Manage-app-approval-for-your-workspace — Slack — accessed 2026-10-05
- https://slack.com/help/articles/25273135315347-Review-flagged-content-in-Slack — Slack — accessed 2026-10-05
- https://slack.com/help/articles/212221668-Mandatory-workspace-two-factor-authentication — Slack — accessed 2026-10-05
- https://slack.com/help/articles/360000394286-Audit-logs-in-Slack — Slack — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/approving-oauth-apps-for-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/managing-requests-for-personal-access-tokens-in-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/searching-the-audit-log-for-your-enterprise — GitHub — accessed 2026-10-05
- https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/accessing-the-audit-log-for-your-enterprise — GitHub — accessed 2026-10-05
- https://docs.github.com/enterprise-cloud@latest/organizations/granting-access-to-your-organization-with-saml-single-sign-on/viewing-and-managing-a-members-saml-access-to-your-organization — GitHub — accessed 2026-10-05
- https://help.okta.com/oie/en-us/content/topics/security/custom-admin-role/work-with-admin.htm — Okta — accessed 2026-10-05
- https://help.okta.com/en-us/content/topics/security/administrators-super-admin.htm — Okta — accessed 2026-10-05
- https://status.stripe.com/ — Stripe — accessed 2026-10-05