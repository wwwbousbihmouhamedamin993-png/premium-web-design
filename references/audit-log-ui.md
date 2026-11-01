# Audit log as a designed surface

The audit log is a **Dense** data surface (see `craft-floor.md`) with a filter-first, query-second
interaction model. Vendor states, windows and limits cited.

## Naming: `category.operation`

> "The name for each audit log entry is composed of a **category of events, followed by an operation
> type**. For example, the `repo.create` entry refers to the `create` operation on the `repo` category."
> ([Audit log for an enterprise](https://docs.github.com/en/enterprise-cloud@latest/admin/concepts/security-and-compliance/audit-log-for-an-enterprise))

Seven operation types are enumerated: **create, access, modify, remove, authentication, transfer,
restore**. Two filter tiers sit over one vocabulary — `operation:create` filters by verb across
categories; `action:team`, `action:team.create`, `-action:hook` filter by category or category+verb
([Searching the audit log](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/searching-the-audit-log-for-your-enterprise)).

**Rule:** the entry name is the row's identity — selectable, copyable, filterable as one token — and
renders `category` and `operation` in distinct styles inside one cell so the verb is scannable
without parsing.

## The fixed entry fields

GitHub enumerates them: the enterprise or organization the action was performed in; the **actor**; the
**user affected**; which repository; the action performed; which **country**; date and time; the
**SAML SSO and SCIM identity** of the actor; for actions outside the web UI, **how the actor
authenticated**; and optionally the **source IP address**
([Audit log for an enterprise](https://docs.github.com/en/enterprise-cloud@latest/admin/concepts/security-and-compliance/audit-log-for-an-enterprise)).

The optionality is a UI instruction: source IP is a disclosure setting, so the column may be absent.
GitHub's incident-response advice is to enable streaming, API-request streaming and source-IP
disclosure *before* an incident — "Without all three features enabled, responders will have critical
visibility gaps"
([Accessing the audit log](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/accessing-the-audit-log-for-your-enterprise)).

Slack adds an agent value: "If Slackbot has taken action on behalf of a user… you'll see
`acting_agent: Slackbot` in the detailed audit log entry or the Audit Logs API output"
([Audit logs in Slack](https://slack.com/help/articles/360000394286-Audit-logs-in-Slack)) — *agent* is
a distinct actor column value, not a footnote on the human actor. Stripe's equivalent is **Security
history**, which "logs the account activity of team members during the past **180 days**"
([Start a team](https://docs.stripe.com/get-started/account/teams)); its event list is narrow —
approval rule created/updated/activated/deactivated/deleted, approval request created/approved/denied
([Approvals](https://docs.stripe.com/account/approvals)).

## Retention boundary vs default window

Three numbers; conflating them is the classic bug. GitHub's
([Accessing the audit log](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/accessing-the-audit-log-for-your-enterprise)):

| Number | Value | Meaning |
|---|---|---|
| Retention boundary | **180 days** audit events, **7 days** Git events | Hard horizon — past it the data is gone |
| Default displayed window | **3 months** | "By default, only events from the past three months are displayed" |
| To see older | "specify a date range with the `created` parameter" | Query-language only |

Slack's numbers differ and must not be copied: "As of **April 30, 2026**, audit logs are retained for a
maximum of **two years** for all Enterprise customers… Search query log exports will only contain
results from the last **90 days**"
([Audit logs](https://slack.com/help/articles/360000394286-Audit-logs-in-Slack)).

**Rules:** label the window control's outer stops with numbers ("Last 7 days · Last 3 months · Last
180 days (max)"), not relative dates alone; when the default window is narrower than the boundary say
so ("showing last 3 months of 180 days retained"); never imply that narrowing deletes anything; a
stream with a shorter retention (GitHub's 7-day Git events) must explain its own horizon.

## Filter facets

GitHub is filter-first and explicitly not free-text: "You can search… using the **Filters** dropdown,
or by typing a search query. **You cannot search for entries using text.** You can, however, construct
search queries using a variety of filters. Many operators used when querying the log, such as `-`,
`>`, or `<`, match the same format as searching across GitHub." Eight `key:value` pairs are documented
(`action`, `actor`, `created`, `ip`, `operation`, `repository`, `user`), with constraints: "you can only
use a GitHub **username**, not an individual's real name"; "you must include the account name within the
`repo` qualifier"; "**Git events are not included in search results**"; values combine
(`actor:octocat actor:Copilot`) and negate (`-actor:Copilot`). Seven named dropdown filters ship
alongside: **Yesterday's activity, Enterprise account management, Organization membership, Team
management, Repository management, Billing updates, Hook activity, Security management**
([Searching the audit log](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/searching-the-audit-log-for-your-enterprise)).

Slack's four facets: **Date range, Acting user, Affects (either user, workspace, or organization),
Events** ([Audit logs](https://slack.com/help/articles/360000394286-Audit-logs-in-Slack)). Note
*Affects* is a **scope** facet — the thing acted upon — separate from *Acting user*.

**Rules:** facets first, query input second; separate *acting user* from *affects* as two facets
(conflating them is the most common defect); every active filter renders as a removable chip and the
query bar mirrors the chips; a filtered-out or unavailable stream states why.

## Export: scope, limits, and failure states

GitHub's export surface is the most completely specified
([Exporting audit log activity](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/exporting-audit-log-activity-for-your-enterprise)):

- **JSON or CSV** for audit data; Git events are **JSON only**, "a compressed, newline-delimited JSON
  file", by date range, and "you cannot query for specific Git events to filter and export".
- **Silent gap:** "events that were initiated via the web browser or the REST or GraphQL APIs are not
  included. For example, when a user merges a pull request in the web browser, changes are pushed to
  the base branch, but the Git event for that push is not included."
- **Hard limits — export fails at either:** "**100 MB compressed file**, or **10 minutes export
  processing time**, or both." Remedies given: filter smaller, or stream.
- Path: `Settings` → `Audit log` → **Export** → format; **Export Git Events** → date range →
  **Download Results**.

Slack: `Export` → **Export CSV** or **Export JSON**; **Export search queries** requires a custom role
with both *Access search query logs* and *Read audit logs*, limited to 90 days
([Audit logs](https://slack.com/help/articles/360000394286-Audit-logs-in-Slack)).

The one vendor-documented export-adjacent lifecycle in this set is Stripe's approval-request stream —
a genuine queued model worth copying: `created`, `approved`, `rejected`, `canceled`, `expired` ("the
request expired after 14 days"), `succeeded` ("the approved action completed successfully"), `failed`
("the approved action failed to execute") ([Approvals](https://docs.stripe.com/account/approvals)).

**Rules:** export is **queued** whenever the payload can hit a documented limit — model at minimum
queued → processing → ready → failed and surface *which* limit failed (size vs time); state the limits
in the dialog before the click ("up to 100 MB compressed or 10 minutes"); put the remedy next to the
failure ("narrow your filters", "stream instead"); warn about content missing from exports before the
user discovers the gap in a SIEM; **expired is a terminal state, not an error**.

## Access methods expose different subsets

GitHub publishes a matrix worth copying into the UI (so the admin knows which path is complete
([Accessing the audit log](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/accessing-the-audit-log-for-your-enterprise))):

| Data | Web UI | JSON/CSV export | REST API | Streaming |
|---|---|---|---|---|
| Web events | 180 days | 180 days | 180 days | per external retention |
| API request events | — | — | — | only if streaming of API requests enabled |
| Git events | 7 days | 7 days, JSON only | 7 days | 7 days |
| SSO responses, workflow runs, started jobs, runners | yes | yes | yes | yes |

Plus: "Audit log streaming only includes activity from the time you enable it. Enabling it during an
incident will not recover earlier activity."

## Row-level action

A log you cannot act on is a report. Slack: on an anomaly entry, "click the three dots icon next to an
anomaly audit log entry and select **Sign Out Of Slack**", with a configurable automatic anomaly-event
response and a separate **Security Detections** tab ([Audit logs](https://slack.com/help/articles/360000394286-Audit-logs-in-Slack)).
GitHub: per-entry revoke of a linked SAML identity, an active session, or an authorized credential —
credential confirm text **"I understand, revoke access for this token"** ([SAML access](https://docs.github.com/enterprise-cloud@latest/organizations/granting-access-to-your-organization-with-saml-single-sign-on/viewing-and-managing-a-members-saml-access-to-your-organization);
side effects in `sso-mfa-sessions.md`).

**Rule:** every row identifying an actor offers exactly one safe next action (open the member, filter
to that actor, revoke session). Revoke-level actions sit behind a per-row overflow with named
confirmation text, never as a bulk default.

## Not found

- **Not found:** any vendor-documented statement about audit-log pagination (cursor vs page), row
  virtualisation, or default rows-per-page. What would settle it: a vendor docs page on audit-log API
  pagination parameters, or a design-system spec. The fetched pages document search and export, not
  list rendering.
- **Not found:** a vendor-documented cap on the number of filter facets or saved views (GitHub states
  7 `key:value` pairs and 7 dropdown filters; no cap).

## Sources

- https://docs.github.com/en/enterprise-cloud@latest/admin/concepts/security-and-compliance/audit-log-for-an-enterprise — GitHub — accessed 2026-10-05
- https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/searching-the-audit-log-for-your-enterprise — GitHub — accessed 2026-10-05
- https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/accessing-the-audit-log-for-your-enterprise — GitHub — accessed 2026-10-05
- https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/exporting-audit-log-activity-for-your-enterprise — GitHub — accessed 2026-10-05
- https://docs.github.com/enterprise-cloud@latest/organizations/granting-access-to-your-organization-with-saml-single-sign-on/viewing-and-managing-a-members-saml-access-to-your-organization — GitHub — accessed 2026-10-05
- https://slack.com/help/articles/360000394286-Audit-logs-in-Slack — Slack — accessed 2026-10-05
- https://docs.stripe.com/account/approvals — Stripe — accessed 2026-10-05
- https://docs.stripe.com/get-started/account/teams — Stripe — accessed 2026-10-05