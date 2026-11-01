# SSO, MFA and sessions

Identity surfaces of a settings tree. Vendor states, durations and side effects cited.

## SAML: exactly three states

GitHub's docs state the model: "For an organization, SAML SSO can be **disabled**, **enabled but not
enforced**, or **enabled and enforced**. After you enable SAML SSO… and your organization's members
successfully authenticate with your IdP, you can enforce the SAML SSO configuration."
([About SAML SSO](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-identity-and-access-management-with-saml-single-sign-on))

Enforcement is a **gated transition**, not a third checkbox: "Enable and test SAML SSO for your
organization, then authenticate with your IdP **at least once**"
([Preparing to enforce](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/preparing-to-enforce-saml-single-sign-on-in-your-organization)).
The toggle is named **"Require SAML SSO authentication for all members of the `ORGANIZATION`
organization"**, with the tip "you can test your implementation without affecting your organization
members by leaving [it] unchecked"
([Enforcing SAML SSO](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/enforcing-saml-single-sign-on-for-your-organization)).
Slack's equivalents are separate rows, each with its own Edit: **Require SSO authentication**, **Sync
user profiles**, **Email address changes**, **Display name changes**, (Business+ only) **SSO name and
sign-in button**; at org level **SSO member exclusions** and **SSO guest exclusions**
([Slack, Manage SSO settings](https://slack.com/help/articles/220403548-Manage-single-sign-on-settings)).

## The org-vs-enterprise enforcement divergence

The most consequential documented asymmetry in this set. Blurring it causes member removal.

| Level | Effect on members who never authenticated via the IdP |
|---|---|
| **Organization** | **Removes them.** "Enforcement removes any members and administrators who have not authenticated via your IdP from the organization. GitHub sends an email notification to each removed user." Confirm button: **"Remove members and require SAML single sign-on"** |
| **Enterprise** | Does not remove; forces re-authentication across every organization in the enterprise |

([Enforcing SAML SSO](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/enforcing-saml-single-sign-on-for-your-organization),
[About SAML SSO](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-identity-and-access-management-with-saml-single-sign-on))

The org screen previews the damage: "If any organization members have not authenticated via your
IdP, GitHub displays the members… GitHub will remove the members from the organization." It reaches
machine principals too: "Bots and service accounts that do not have external identities set up in
your organization's IdP will also be removed when you enforce SAML SSO." And enterprise config wins:
"requiring SAML for the enterprise account will override your organization-level SAML configuration and
enforce SAML SSO for every organization in the enterprise."

**Rules.** Enforcement is a separate destructive-gated step; the screen lists affected principals by
name, humans and bots separately, before the confirm; the button names the removal; on an
enterprise-owned org the org screen states that the enterprise setting wins and links to it. Close
the flow with the recovery artefact GitHub documents: **"Single sign-on recovery codes — review your
recovery codes. Store the recovery codes in a safe location like a password manager."** Removed users
can return — "If a user rejoins the organization **within three months**, the user's access privileges
and settings will be restored."

## What SSO does not cover

Documented carve-outs, because admins assume the opposite
([About SAML SSO](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-identity-and-access-management-with-saml-single-sign-on)):

- **SSO is not login.** "Unless you use Enterprise Managed Users, members will continue to sign into
  their personal accounts on GitHub.com, and each personal account will be linked to an external
  identity in your IdP."
- **Public-repo read paths exempt.** No IdP authentication for the repository overview page and file
  contents, forking, or "read operations via Git, such as cloning". Issues, pull requests, projects
  and releases *do* require authentication.
- **Outside collaborators exempt.** "SSO authentication is not required for outside collaborators."
- **API and Git need credentials, not sessions** — "members must authorize and authenticate with a
  personal access token or SSH key".
- **OAuth apps need a live session**, and GitHub "does not recommend opting out".
- **No SAML Single Logout.** "To terminate an active SAML session, users should log out directly on
  their SAML IdP."
- **Visibility flips under SSO:** "If members are signed in with a SAML SSO session when they create a
  new repository, the default visibility of that repository is **private**."
- Internally tested IdPs: Microsoft ADFS, Microsoft Entra ID, Okta, OneLogin, PingOne, Shibboleth.

## SCIM is a path distinct from invitation

The absence of SCIM has a stated failure mode, which is the whole argument for a "SCIM not configured"
state worded as risk:

> "If you use SAML SSO without implementing SCIM, you **won't have automatic deprovisioning**… **Authorized
> tokens grant access to the organization even after their sessions expire.**"

([About SCIM for organizations](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-scim-for-organizations))

Further documented constraints: "You cannot use this implementation of SCIM with an enterprise account
or with an organization with managed users"; compatible IdPs are Entra ID, Okta, OneLogin; SCIM "must
use a third-party-owned OAuth app… acts on behalf of, a specific GitHub user. **If the user who last
authorized this OAuth app leaves or is removed from the organization, SCIM will stop working.**" —
GitHub recommends a dedicated account, which "must be an organization owner and will consume a
license"; "The SAML IdP and the SCIM client must use matching `NameID` and `userName` values";
authorizing requires an active SAML session. Manual edits corrupt the link: manual invite → "may not
get properly linked to their SCIM identity… can prevent the user account from being deprovisioned";
manual removal → "a stale linked identity will remain". Managed users are the SCIM-only path —
"Managed user accounts are provisioned using SCIM, not invited"
([Inviting users](https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization)).

Slack splits provisioning into two visible modes: "**pre-provisioned** invited members will be visible
in Slack as soon as they're added via your identity provider… **Users provisioned with just-in-time
provisioning will not be visible in Slack until they log in**"
([Slack, Invited members](https://slack.com/help/articles/360024686174-Invited-members-in-Slack)).

## MFA enrolment states

**Slack, mandatory 2FA** ([Mandatory workspace 2FA](https://slack.com/help/articles/212221668-Mandatory-workspace-two-factor-authentication)):
one row — `Two-factor authentication for email sign-in` → `Edit` → **Require members to have 2FA set
up**, plus **Authenticator apps only**. Defaults: "people can choose between SMS text message and
authentication app 2FA methods"; "Owners and admins on paid plans are required to use 2FA… even if
they haven't enabled mandatory 2FA". Grace then lockout: "People who don't set up 2FA within **24
hours** will be signed out of Slack… New members will be required to set up 2FA before creating an
account". Visibility is a filter: members → `Filter` → **Authentication** → **Two-factor (2FA)**, and
"you can only see who has 2FA enabled at the workspace level at this time". Recovery is hierarchical:
admins can **Disable 2FA** for a locked-out member (re-prompted on next sign-in), but "Only the
**Workspace Primary Owner** can turn off 2FA for Workspace Owners. Only Workspace Owners can turn off
2FA for Workspace Admins." And SSO supersedes it: "2FA in Slack will be turned off when a member
connects, or binds, their SSO account."

**GitHub** ([Configuring 2FA](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication)):
after configuring, the account "will enter a **28-day check up period**… Otherwise, you will be
prompted to perform 2FA in an existing GitHub session on the 28th day." Methods: TOTP, SMS, passkey,
security key, GitHub Mobile; TOTP strongly recommended over SMS.

GitHub's org requirement splits consequences by principal
([Requiring 2FA](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-two-factor-authentication-for-your-organization/requiring-two-factor-authentication-in-your-organization)):

| Principal | Documented consequence |
|---|---|
| members, billing managers | "will not be able to access your organization's resources until they enable 2FA… They will **retain membership** even without 2FA, **including consuming seats**" |
| outside collaborators | "will be **removed**… lose access to its repositories… and their forks"; privileges restorable "within three months" if they enable 2FA; disabling 2FA afterwards removes them automatically |
| sole org owner | "you won't be able to disable 2FA for your personal account without disabling required 2FA for the organization" |

Prerequisite: "you must enable 2FA for your account" before requiring it. Under a requirement,
invitees "must enable two-factor authentication before accepting the invitation"
([Inviting users](https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization)).

**Rules.** Compliance is a filterable column — enrolled / SMS-only / not enrolled / checkup-pending /
locked-out. Enforcement screens state the grace window (24 hours) and the lockout. The remediation
(Disable 2FA) shows its own scope limit. The consequence table differs by principal type because the
same enforcement has two outcomes; show the seat cost of non-compliance.

## Sessions and duration

**Slack session duration** ([Manage session duration](https://slack.com/help/articles/115005223763-Manage-session-duration)):
separate rows **Desktop** and **Mobile**; two modes — on app close, or after a period. Warning cadence:
"Members will be warned **two hours before** session expiration, and receive a final reminder **15
minutes** before they're signed out." No mass logout on change: "Changes… take effect the day you make
them and will end member sessions **randomly over the timeframe you've selected**… if you set a
session duration for seven days, session expirations will begin that day and continue gradually over
the next seven days." And a per-user override exists on Enterprise: "you can use the session duration
API to customize the session duration for a subset of members to be shorter or longer than your
org-level session duration" — so the members table needs a duration column that can differ from the
default.

**GitHub** ties the clock to the IdP: "The duration of this login period is specified by your IdP and
is generally **24 hours**" ([About SAML SSO](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-identity-and-access-management-with-saml-single-sign-on)).

**Session inventory.** GitHub puts three object lists on one subject page — linked identity, active
sessions, authorized credentials. Stripe puts "your active sessions" under Personal details
([Dashboard basics](https://docs.stripe.com/dashboard/basics)). Slack's access logs show "The time and
date of each new sign in, The IP address of each device… A list of devices", refreshed "every 5-10
minutes", generated on sign-in, app/web open, unique-IP sign-in, or "Perform actions through an app or
bot that acts on their behalf" — with a documented gap: "On Enterprise plans, **not all** mobile
sessions, web client visits, or third-party app actions are displayed in workspace-level access logs.
For more complete access logs… use the access logs API." Slack's remedy is member-side: "ask the
affected member(s) to sign out of all sessions from their personal access logs"
([Slack, View access logs](https://slack.com/help/articles/360002084807-View-access-logs-for-your-workspace)).

## Revoking a linked identity: three revokes, three consequences

| Revoke target | Documented side effect |
|---|---|
| Linked identity | Confirm text **"Revoke external identity"**. Wrong identity linked → revoking "allow[s] the member to try again". **SCIM warning:** "Revoking a linked user identity on GitHub will also remove the SAML and SCIM metadata. As a result, the identity provider will **not be able to synchronize or deprovision**… An admin must revoke a linked identity through the identity provider." **Team-sync warning:** revoking "will remove that person from **any teams mapped to IdP groups**" |
| Active SAML session | Session revoked. Note "GitHub does not support SAML Single Logout" |
| Authorized credential | "**revoking a credential only removes the SAML authorization. It does not delete the underlying token or SSH key.**" Confirm text **"I understand, revoke access for this token"**. Only "the last several characters of each token or key are visible" |

([GitHub, Viewing and managing a member's SAML access](https://docs.github.com/enterprise-cloud@latest/organizations/granting-access-to-your-organization-with-saml-single-sign-on/viewing-and-managing-a-members-saml-access-to-your-organization))

Three consequences: never one "Revoke access" button, because the side effects differ in kind;
credential revoke is not credential deletion and the dialog must say so — anyone reading only the
confirm button will believe the token is dead; and once SCIM is on, identity revoke is a *provisioning*
operation whose correct path is documented as being in the IdP — "an admin can remove and re-assign the
user to the GitHub Enterprise Cloud application."

Incident actions come in three granularities from the same page — per member; per credential type
("such as only personal access tokens (classic), across your entire organization or for a specific
individual member"); and bulk "across all members and all/a specific supported credential type" — and
the inventory to show first: "In the 'Authentication security' section of your organization settings,
you can **review counts** for user tokens and keys that are authorized for single sign-on (SSO)."

## Not found

- **Not found:** a vendor-documented session lifecycle (active → revoked → expired) or per-device
  revoke, beyond GitHub's active-session list and Slack's sign-out actions. What would settle it: a
  vendor device-management admin page enumerating session states.
- **Not found:** a documented MFA **recovery-code** lifecycle (count, regeneration, invalidation)
  beyond GitHub's "review your recovery codes… store the recovery codes in a safe location" and Slack's
  owner backup-password note. What would settle it: a vendor recovery-codes page; the GitHub
  enterprise sidebar lists *Manage recovery codes* and *Download recovery codes*, not fetched here.

## Sources

- https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-identity-and-access-management-with-saml-single-sign-on — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/enforcing-saml-single-sign-on-for-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/preparing-to-enforce-saml-single-sign-on-in-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-scim-for-organizations — GitHub — accessed 2026-10-05
- https://docs.github.com/enterprise-cloud@latest/organizations/granting-access-to-your-organization-with-saml-single-sign-on/viewing-and-managing-a-members-saml-access-to-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-two-factor-authentication-for-your-organization/requiring-two-factor-authentication-in-your-organization — GitHub — accessed 2026-10-05
- https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication — GitHub — accessed 2026-10-05
- https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization — GitHub — accessed 2026-10-05
- https://slack.com/help/articles/212221668-Mandatory-workspace-two-factor-authentication — Slack — accessed 2026-10-05
- https://slack.com/help/articles/115005223763-Manage-session-duration — Slack — accessed 2026-10-05
- https://slack.com/help/articles/220403548-Manage-single-sign-on-settings — Slack — accessed 2026-10-05
- https://slack.com/help/articles/360002084807-View-access-logs-for-your-workspace — Slack — accessed 2026-10-05
- https://slack.com/help/articles/360024686174-Invited-members-in-Slack — Slack — accessed 2026-10-05
- https://docs.stripe.com/dashboard/basics — Stripe — accessed 2026-10-05