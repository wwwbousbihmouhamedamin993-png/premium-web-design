# Roles and permissions matrix

Reference for the permission model behind a settings tree. Vendor names, counts and limits are
attributed to the vendor that documents them; nothing here is a universal RBAC claim.

## The vocabulary

GitHub states the definition most precisely, and it is the one to borrow:

> "A permission is the ability to perform a specific action. For example, the ability to delete an
> issue is a permission. **A role is a set of permissions you can assign to individuals or teams.**"
> ([Roles in an organization](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/roles-in-an-organization))

Stripe adds the tier that makes a matrix readable — the **job**:

> "A **permission** [is] access to one kind of data or action… A **job** [is] a group of permissions
> that covers a task a team member performs… **Jobs are the unit you work with most** when you configure
> a custom role. A **role** is a named set of jobs and permissions that you assign to a team member."
> ([Custom roles](https://docs.stripe.com/get-started/account/teams/custom-roles))

Three tiers, then: **permission → job → role**. A matrix with only permissions produces a
thousand-cell grid nobody reads.

## Scope levels and principal types

| Vendor | Scopes, as documented |
|---|---|
| GitHub | **repository-level**, **team-level**, **organization-level**. Team-level roles "give permissions to manage a team" (team maintainer); organization-level roles manage "the organization and the organization's repositories, teams, and settings" |
| Slack | **workspace** and **organization** (Enterprise), plus per-object roles: channel managers, multi-channel and single-channel guests, user groups |
| Stripe | **account** and **organization**; Connect adds a platform/connected-account split, and roles can be scoped to connected accounts |

([GitHub, Roles in an organization](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/roles-in-an-organization),
[Slack, Types of roles in Slack](https://slack.com/help/articles/360018112273-Types-of-roles-in-Slack),
[Stripe, User roles](https://docs.stripe.com/get-started/account/teams/roles))

Not all principals are people. GitHub makes outside collaborators a distinct principal type, not a
role: "A person who has access to one or more organization repositories but is **not explicitly a
member** of the organization, such as a consultant or temporary employee." Slack adds **invited
members**, who can be added to channels, mentioned and sent DMs before acceptance and "receive email
notifications until they create their account". Stripe's machine principal is the **agent-tagged API
key**, "an autonomous agent, an AI system that operates independently", subject by default to approval
rules. Sources: [GitHub](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/roles-in-an-organization),
[Slack, Invited members](https://slack.com/help/articles/360024686174-Invited-members-in-Slack),
[Stripe, API keys](https://docs.stripe.com/keys).

**Rule:** every grant resolves to (role, scope, principal type) — person / team / IdP group / service
account / agent — because the same capability behaves differently per type. SSO authentication is not
required for GitHub outside collaborators.

## Which axis to present

Both directions ship; pick by who is asking. **Capability-by-role** (capabilities as rows, one column
per role) is how GitHub's audit-log `action` facet works: `repo.create` is the `create` operation on
the `repo` category, and actions group into filterable categories
([Audit log](https://docs.github.com/en/enterprise-cloud@latest/admin/concepts/security-and-compliance/audit-log-for-an-enterprise),
[Searching the audit log](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/searching-the-audit-log-for-your-enterprise)).
**Role-by-capability** is how Stripe publishes every role, as "Some of what this role **can** do" /
"Some of what this role **can't** do"
([User roles](https://docs.stripe.com/get-started/account/teams/roles)). **Job-first** is Stripe's
custom-role editor: pick a base role, check jobs, then open a job to downgrade an individual
permission from `write` to `read` ([Custom roles](https://docs.stripe.com/get-started/account/teams/custom-roles)).

| Question | Presentation |
|---|---|
| "Can I do X?" (one user) | role-by-capability, one role |
| "Who can do X?" (all users) | capability-by-role, one capability |
| "I want A and B but not C" | job-first editor on a base role |

**Not found:** vendor guidance on when to present which axis. What would settle it: a vendor design
system or accessibility doc naming a matrix presentation rule. The table above is this skill's rule.

## Denials are content, not absence

Render a denial as a checked-off cell with its reason. Documented examples, all from
[Stripe, User roles](https://docs.stripe.com/get-started/account/teams/roles):

- **Administrator** cannot delete the default bank account; cannot change the account owner.
- **IAM Administrator** "can remove any user, including Administrators and Super Administrators" but
  "can't assign a user to the Administrator or Super Administrator role" — remove escalators, never
  grant escalators.
- **Super Administrator** can assign Super Administrator to others and "Change the account owner".
- **Account Owner** is "a special type of Administrator that can perform all actions, including
  closing the account. **There can only be one Owner for an account.**"
- **Developer** "can create secret keys, which grant access to almost all API resources" but "can't
  invite team members or change the account owner".
- **Support Communications** can manage support requests and do "Anything outside the scope of
  managing support requests" — i.e. nothing else.
- **Terminal Specialist** "can't view or manage payments, products, or customers".
- **Dispute Analyst** cannot "Create or refund payments"; **Refund Analyst** cannot "Create payments".

GitHub's carve-outs are equally deliberate: the **GitHub App manager** role "does not grant users
access to install and uninstall GitHub Apps on an organization"; **billing managers** "can manage the
billing settings for your organization, such as payment information", "a useful option if members of
your organization don't usually have access to billing resources"; **security managers** gain "read
permission for all repositories in the organization" bundled with security-settings management — a
documented case of a narrow capability widening resource scope
([Roles in an organization](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/roles-in-an-organization)).

## Multiplicity, and the traps vendors state in prose

> "If you assign a user multiple roles, they're assigned **all** the permissions of each individual
> role. Be cautious of conflicts and unintended authority." … "These roles can invite users to your
> account. **If an attacker compromises a user with one, they can invite additional users under their
> control.**" ([Stripe, User roles](https://docs.stripe.com/get-started/account/teams/roles))

Continuity and floors, all vendor-stated: organization owners "should be limited, but to **no less
than two people**" ([GitHub](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/roles-in-an-organization));
"every org must have at least **one** individually assigned super admin. If you just have one
individually assigned super admin, you **can't edit or revoke** their super admin permissions"
([Okta, Super administrators](https://help.okta.com/en-us/content/topics/security/administrators-super-admin.htm));
and a delegation boundary — Org Owners and Org Admins "can view a list of custom roles… but **can't
create or edit them**" ([Slack, Create custom roles](https://slack.com/help/articles/29800891169939-Create-custom-roles)).

**Rules:** model the union of multiple roles visibly and warn when it includes an inviter role; block
any edit that would leave a tenant with zero owners/super admins, and say why; make revocation of a
delegation right a distinct, separately-granted action.

## Custom roles

| Vendor | Model | Documented limits |
|---|---|---|
| GitHub | Custom org roles "grant an organization member the ability to administer certain **subsets of settings** without granting full administrative control" | Enterprise Cloud only; example given: a role containing just "View organization audit log" |
| Slack | "delegate specific tasks (like managing guests or viewing analytics)"; name + description + permission checkboxes | Enterprise only; assignable to individuals **or IDP groups**; only Org Primary Owner and org-level Roles Admins may create/edit |
| Stripe | Copy a built-in role, remove jobs, lower permissions; "**A custom role is independent of its base role after you create it.** If Stripe adds permissions to the base role, those permissions don't appear in your custom role automatically" | **Private preview**; Support Specialist is the only base role; remove-only; max **50 custom roles per account**; assignable only in the creating account/organization; can't test in a sandbox before live |
| Okta | "custom roles that limit an admin's access to a subset of permissions **and resources**" | assignable to users, groups, and apps |

Sources: [GitHub](https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/roles-in-an-organization),
[Slack](https://slack.com/help/articles/29800891169939-Create-custom-roles),
[Stripe](https://docs.stripe.com/get-started/account/teams/custom-roles),
[Okta, Work with the admin component](https://help.okta.com/oie/en-us/content/topics/security/custom-admin-role/work-with-admin.htm).

Three design facts: Slack's 19 system roles are **named after single jobs** (Analytics Admin, Audit
Logs Admin, Content Admin, DLP Admin, Export Admin, Integrations Admin, Legal Holds Admin, Roles
Admin, Security Admin, Users Admin, Workflow Admin…) — names that name a job scale better than names
that name a level ([Types of roles](https://slack.com/help/articles/360018112273-Types-of-roles-in-Slack));
detachment must be explicit, so the editor shows "your base role changed" as an actionable diff; and
group principals are first class.

## Scope-within-a-scope

| Case | Vendor precedent |
|---|---|
| One resource type | GitHub billing manager — billing settings only |
| A subset of settings | GitHub custom org roles; Slack custom roles |
| One product | Stripe Connect roles "only available if you use Connect"; Identity roles "only available if you use Identity"; Tax form roles "only available if you use 1099s" |
| Connected accounts | Stripe Connect Onboarding Analyst "can't do anything on the platform account except view and edit connected accounts" |
| A set of users | Okta custom roles limit permissions *and resources*; Stripe IAM Administrator can remove "any user, including Administrators and Super Administrators" |
| Org inside a parent | GitHub enterprise-level SAML "will override your organization-level SAML configuration"; Slack splits org vs workspace for the same settings with different permissions ([session duration](https://slack.com/help/articles/115005223763-Manage-session-duration)) |
| Provisioned, not invited | GitHub Enterprise Managed Users: "Managed user accounts are provisioned using SCIM, not invited" ([inviting users](https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization)) |

**Rules:** a nested scope must be visible in the breadcrumb *and* the matrix title — "Security
manager (org `acme`)"; feature-scoped roles appear only when the feature is on, and their absence is
labelled a plan gap, not a permissions gap; a parent-level setting that overrides children warns on
the child screen and links to the parent; provisioned principals never render invitation
affordances.

## Sources

- https://docs.github.com/en/organizations/managing-peoples-access-to-your-organization-with-roles/roles-in-an-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/enterprise-cloud@latest/admin/concepts/security-and-compliance/audit-log-for-an-enterprise — GitHub — accessed 2026-10-05
- https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/searching-the-audit-log-for-your-enterprise — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization — GitHub — accessed 2026-10-05
- https://docs.stripe.com/get-started/account/teams/roles — Stripe — accessed 2026-10-05
- https://docs.stripe.com/get-started/account/teams/custom-roles — Stripe — accessed 2026-10-05
- https://docs.stripe.com/keys — Stripe — accessed 2026-10-05
- https://slack.com/help/articles/360018112273-Types-of-roles-in-Slack — Slack — accessed 2026-10-05
- https://slack.com/help/articles/29800891169939-Create-custom-roles — Slack — accessed 2026-10-05
- https://slack.com/help/articles/360024686174-Invited-members-in-Slack — Slack — accessed 2026-10-05
- https://slack.com/help/articles/115005223763-Manage-session-duration — Slack — accessed 2026-10-05
- https://help.okta.com/en-us/content/topics/security/administrators-super-admin.htm — Okta — accessed 2026-10-05
- https://help.okta.com/oie/en-us/content/topics/security/custom-admin-role/work-with-admin.htm — Okta — accessed 2026-10-05