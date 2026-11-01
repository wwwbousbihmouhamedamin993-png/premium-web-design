# Member invitations

The invitation lifecycle as a designed state machine. Vendor states, expiries and limits are cited to
the vendor that documents them.

## The five-state model (GitHub, documented)

| State | What the admin can do | Vendor wording |
|---|---|---|
| **Pending** | Edit or cancel any time before acceptance; resend; extend | "You can edit or cancel an invitation any time before the user accepts" |
| **Accepted** | Roles editable afterwards | "After a team member accepts their invite, you can edit their role at any time from your Team settings" (Stripe) |
| **Expired** | Expires automatically after **7 days**; retry or cancel individually **or in bulk** from a *Failed invitations* view | "If an invitee does not accept the invitation within seven days, the pending invitation expires automatically" |
| **Failed** | Same *Failed invitations* view | "Failed invitations to outside collaborators can also be found in this view" |
| **Blocked** | Cannot be accepted while a precondition holds | "If an invitee's personal account has been flagged, the invitee won't be able to accept any new or pending invitations" |

([GitHub, Inviting users](https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization),
[Stripe, Start a team](https://docs.stripe.com/get-started/account/teams))

GitHub's UI collapses *expired* and *failed* into one view. Defensible — both are "not pending, needs
a decision" — but the data model must not collapse them, because only a genuinely failed send is
retryable.

## Vendor expiries differ; so do the verbs

| Vendor | Expiry | Verbs on pending |
|---|---|---|
| GitHub | **7 days** | edit, cancel, retry (bulk) |
| Slack | **30 days** — "Invitations and invite links will expire after 30 days" | **Extend Invitation**, **Resend Invitation**, **Delete Invitation**; invite links: **Deactivate**, or "renew expired links if you'd like to keep using them" |
| Stripe | **10 days** — "Invites to your Stripe account expire after 10 days" | edit role after acceptance; no documented resend or extend |

Sources: [GitHub](https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization),
[Slack, Manage pending invitations](https://slack.com/help/articles/360060363633-Manage-pending-invitations-and-invite-links-for-your-workspace),
[Stripe](https://docs.stripe.com/get-started/account/teams).

**Rule:** render expiry as a countdown on the row ("expires in 3 days") and offer *Extend* before
*Resend* — resending a link about to expire is worse than extending it.

## Invited ≠ member

Slack documents pre-acceptance behaviour in detail, and it changes what a row can show: an invited
member can be added to channels, mentioned, and sent DMs **before accepting**, "receive email
notifications until they create their account", and "do not yet have an active Slack account"
([Slack, Invited members](https://slack.com/help/articles/360024686174-Invited-members-in-Slack),
[Types of roles](https://slack.com/help/articles/360018112273-Types-of-roles-in-Slack)). Billing is
gated: "If you're on a paid plan, you will not be billed for invited members until they become active
in Slack." Content is withheld in some cases — invited members "can't see the contents of messages or
reply by email if their email address is on a social domain (for example, Gmail), their email address
does not match the domain of the sender, or if your workspace or Enterprise organization is
HIPAA-enabled." Paid plans get a **Notify pending members** action on any message.

Design consequence: the row needs the *invited address* and the *identity they will land on* side by
side. GitHub documents the mismatch: if invited by email, "the invitee will only be able to accept the
invitation if the email address matches with a **verified** email address associated with the
invitee's personal account on GitHub."

## Preconditions as UI states, not error toasts

| Precondition | Vendor wording | UI treatment |
|---|---|---|
| No unused licence (paid per-user) | "an unused license must be available before you can invite a new member" — and the same for **reinstate** | Disable the primary action; state the seat count, not just "not allowed" |
| Rate limit | "you can only create **50** organization invitations within a 24-hour period. If your organization is more than one month old or on a paid plan, the limit is **500** invitations per 24 hour period" | Show remaining quota in the composer |
| 2FA required first | "users that you invite must enable two-factor authentication **before accepting** the invitation" | Mark the row *blocked — 2FA required*, not *failed* |
| Email must match verified address | see above | Show the mismatch inline at send |
| Flagged account | see above | Blocked, and offer no retry — retry cannot succeed |

Sources: [GitHub, Inviting users](https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization),
[GitHub, About SAML SSO](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-identity-and-access-management-with-saml-single-sign-on)
(for the related "active SAML session" credential rule).

**Rate limit as a state.** The ceiling moves (50 → 500 by org age or plan), so display *remaining* and
the window ("43 of 50 in the next 24 hours"). Bulk retry is the documented remedy, which makes it the
recovery affordance for a quota-exhausting admin. The primary action becomes disabled with the reason
inline — not a toast. **Not found:** vendor UI patterns for presenting a quota. What would settle it:
a vendor help page or design-system doc on quota presentation.

## Approval gate before the invitation exists

Slack documents a pre-invitation state, *requested*, distinct from *pending*
([Require admin approval for invitations](https://slack.com/help/articles/115004854783-Require-admin-approval-for-invitations-to-Slack)):

- "By default, members (but not guests) can invite new members… invitations must be requested and
  approved" when **Require admin approval** is set.
- "When an invitation request is approved or denied, the member who requested it will be notified."
- Routing is configurable: "choose where invitation requests are sent — to all admins via Slack
  notification or **to a specific channel**."
- "Only owners and admins can manage guest accounts, and they will always need to approve members'
  requests to invite guests."
- Enterprise override: "When a custom invitation request management app is installed to an org,
  invitation requests will be sent to Org Owners and Admins. Workspace Owners and Admins will no
  longer receive invitation requests."

So the pipeline is **request → approve/deny → invitation sent → pending → accepted**, and the queue
holding `request` items is not the queue holding `pending` items: two tabs, potentially two owners.

## Reinstate vs start fresh

GitHub makes this an explicit choice with two named buttons:

> "If the person you're inviting was an organization member within the last three months, select whether
> to **restore their privileges** or **start fresh**" — then click **Invite and reinstate** or **Invite
> and start fresh**.

([GitHub, Inviting users](https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization))

**Restored** ([Reinstating a former member](https://docs.github.com/enterprise-cloud@latest/organizations/managing-membership-in-your-organization/reinstating-a-former-member-of-your-organization)): the user's role in the organization; private forks of organization-owned repositories; team membership; previous repository access and permissions; stars on organization repositories; issue assignments; repository subscriptions. The window is **3 months**, opened only by specific causes: manual removal, SCIM removal, removal because 2FA became required, SAML-enforcement removal, or member→collaborator conversion.

**The restoration path depends on the removal cause**, and the UI must branch on it:

| Removal cause | Path |
|---|---|
| SCIM | "re-invite the user via SCIM by re-assigning them to the application"; membership reinstated after sign-in and acceptance |
| SAML without SCIM | the user authenticates via SAML; "membership will be reinstated after they successfully authenticate" |
| 2FA requirement | "you can send an invitation to reinstate a user's privileges… **before they have enabled two-factor authentication**, but they must enable 2FA before they can accept" |
| otherwise | invite on GitHub with the reinstate / start-fresh choice |

Same at enforcement: "If a user rejoins the organization **within three months**, the user's access
privileges and settings will be restored"
([Enforcing SAML SSO](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/enforcing-saml-single-sign-on-for-your-organization)).
Slack's reinvite is explicitly *not* a reinstatement: "Should you re-invite them to Slack in the
future, they'll be treated as a **new invited member**"
([Slack, Invited members](https://slack.com/help/articles/360024686174-Invited-members-in-Slack)).

**Rule:** "Reinvite" is ambiguous in the domain. Name the branch in the button and show the diff —
*restore 6 privileges / start fresh and choose a role* — before send.

## Revocation is a sixth state

Slack: "If you revoke an invited member's invitation, their Slack account will be **deactivated** and
they'll stop receiving email notifications." GitHub deletes an invitation to "prevent an invited
member from accepting it". Revoke is not delete — if revocation deactivates an account, the
confirmation must say so.

## Paths that bypass invitation

An invite composer that claims to be the only way in is wrong
([Manage how people join](https://slack.com/help/articles/115004856503-Manage-how-people-join-your-workspace),
[About SAML SSO](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-identity-and-access-management-with-saml-single-sign-on),
[About SCIM](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-scim-for-organizations)):

- **Approved email domains:** "Anyone with an approved email address can join by clicking your
  workspace's sign-up link"; and "If a member of your workspace requests an invitation for someone with
  an approved email address, the request will be **approved automatically**". Slack also warns
  "Enabling single sign-on (SSO) will override your workspace signup preferences."
- **SAML self-service signup:** `https://github.com/orgs/ORGANIZATION/sso/sign_up` — "To provision new
  users **without an invitation**", and "only supported when SAML SSO is configured at the
  **organization** level, not when SAML SSO is configured at the enterprise account level."
- **SCIM:** "GitHub can automatically invite members… when you grant access on your IdP. If you remove
  a member's access… on your SAML IdP, the member will be automatically removed from the GitHub
  organization."
- **Managed users:** provisioned via SCIM, "not invited".

The composer should name these — including the data-integrity warning GitHub documents: "If a user is
invited to an organization manually instead of by an existing SCIM integration, their user account may
not get properly linked to their SCIM identity. This can prevent the user account from being
deprovisioned via SCIM in the future. If a user is removed manually… a stale linked identity will
remain."

## Checkable rules

1. Every row shows state, age and expiry countdown; expiry is never implicit.
2. Extend precedes resend; retry is offered only for genuinely failed sends.
3. Preconditions (licence, quota, 2FA, email match, flagged account) are inline states, not toasts.
4. *Requested* and *pending* are separate queues with separate owners and routing.
5. Denials capture a reason delivered to the requester.
6. Reinstate vs start fresh is a named branch with a visible privilege diff; 3-month windows stated.
7. Revoke is labelled as revocation and states its account-level consequences.
8. Auto-join paths are named where an invite would be sent, with the SCIM data-integrity warning.

## Sources

- https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/enterprise-cloud@latest/organizations/managing-membership-in-your-organization/reinstating-a-former-member-of-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-identity-and-access-management-with-saml-single-sign-on — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/enforcing-saml-single-sign-on-for-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-scim-for-organizations — GitHub — accessed 2026-10-05
- https://slack.com/help/articles/360060363633-Manage-pending-invitations-and-invite-links-for-your-workspace — Slack — accessed 2026-10-05
- https://slack.com/help/articles/360024686174-Invited-members-in-Slack — Slack — accessed 2026-10-05
- https://slack.com/help/articles/360018112273-Types-of-roles-in-Slack — Slack — accessed 2026-10-05
- https://slack.com/help/articles/115004854783-Require-admin-approval-for-invitations-to-Slack — Slack — accessed 2026-10-05
- https://slack.com/help/articles/115004856503-Manage-how-people-join-your-workspace — Slack — accessed 2026-10-05
- https://docs.stripe.com/get-started/account/teams — Stripe — accessed 2026-10-05