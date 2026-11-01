# Views, Filters, Sorts — One Data Set, Many Named Views

Framing: a view is a **named, shareable configuration of a data surface**, not a saved filter string. Notion, Airtable, Linear, and Weights & Biases each ship the same idea independently, and they agree on the parts: a view owns its layout, its property visibility, its filter, its sort, and (usually) its grouping — and those settings do not leak between views.

The rule that makes it a view rather than a bookmark: **Notion states it flatly** — "Each database view has its own settings. Settings applied to one database view won't be applied across all other database views automatically."

## The per-view setting set

Notion's View settings menu is the most complete published list: **Layout, Property visibility, Filter, Sort, Group, Sub-group, Copy link to view**, plus an "Open pages in" choice of **Side peek / Center peek / Full page** (with defaults — "Table, Board, List & Timeline layouts will open pages in side peek by default. Gallery & Calendar layouts will open pages in center peek by default").

Compare the others:

| Surface | Published per-view settings | Source |
| --- | --- | --- |
| Notion | Layout, Property visibility, Filter, Sort, Group, Sub-group, Open pages in, copy link | Notion Help Center |
| W&B Weave saved views | Filters, Sort order, **Page size**, Column visibility, **Column pinning** | W&B docs |
| Linear (Display options) | Layout (list/board/timeline), Grouping, Sub-grouping, Ordering, Sub-issues, Show empty groups, Display properties, Zoom, Completed projects | Linear docs |
| Airtable | Field visibility, field order, row height, filters, groups, sorts, record colouring | Airtable docs |

Note that page size and column pinning count as view state at W&B, and display properties count at Linear — "Show or hide issue properties such as ID, status, assignee, priority, SLA, project, due date, milestone, cycle, release, estimate, labels, links, customers, customer revenue, time in status, created date, updated date, pull requests and commits, and Sentry issues" (Linear). If your grid has page size and pinned columns, they belong in the view config.

Linear also draws the distinction the others imply: **display properties are not filters.** "This is different from filters; filters will refine the list to only issues with certain properties while display options show all issues in the list but hide or show data on the issue item or board card."

## Personal vs shared configuration

Two independent axes, and products resolve them differently:

**Notion — per-setting, opt-in shared.** For filters: "You can choose to `Save for everyone` if you want the filter to be applied for everyone in the database view. If you want the filter to apply only for you, don't select this option." Same for sorts. But some view chrome is explicitly personal: choosing whether tabs show "Icon only, Text only, or both" — "Only you will see this change. It won't affect other people's views."

**Linear — personal until you publish a default.** "To update your view only, simply modify the display options (do *not* Set as default)." "Press Set as default to save the current display options as the default for other members in your workspace. It will apply the configuration to every other user in your workspace." Critically, Linear's default is a starting point, not a lock: "It will be the view they see when they first open it, but **they can always apply their own preferences on top of it**." And "Click Reset to default to revert back to the default (Saved) display options."

**W&B — two workspace kinds.** "Personal workspaces: A customizable workspace… Only the owner of the workspace can edit and save changes. Teammates can view a personal workspace but teammates can not make changes to someone else's personal workspace." "Saved views: Saved views are collaborative snapshots of a workspace. Anyone on your team can view, edit, and save changes to saved workspace views."

**Airtable — collaborative, personal, or locked.** Three collaboration types: "Collaborative views allow all base collaborators to see and edit the view's configuration, such as sorting, grouping, and filtering"; "Personal views are views that only you can configure and edit"; "Locked views prevent all collaborators from changing a view's configuration—like filters, field order, or visibility—until it's unlocked by someone with Creator or Owner permissions." Personal and locked views "are only available to users on paid workspace plans."

## Per-workspace locking

Locking is for configurations that must not drift — a shared triage queue, a finance export, anything someone else will silently re-sort.

Airtable's model is the reference implementation:

- **Lock the view, not the workspace.** "If you're a paid plan user with creator permissions and you want to ensure that your preferred row height configuration on a view won't get accidentally changed, you can lock the view, which will prevent all collaborators from altering a view's configuration until it's been unlocked by someone with creator permissions."
- **Permissions gate the unlock.** "Locked views prevent all collaborators from changing a view's configuration… until it's unlocked by someone with Creator or Owner permissions." Airtable's permissions table: owners/creators "Can create, delete, modify, lock/unlock, and print views"; editors "Can create, delete, modify, and print views"; commenters "Can create, delete, and modify their own personal views."
- **A table must always have one shared view.** "You cannot make the only view in a table into a personal view. For every table, there must always be at least one collaborative grid view accessible to everyone in the workspace." Guard this in the UI: block converting the last collaborative view.
- **Plan-aware degradation is acceptable; silent failure is not.** "Personal views are a premium feature… So regardless of your base's size, if your workspace is not on a current paid plan, you will not have access to premium or locked views unless your workspace plan is upgraded."

## Naming, organising, sharing

- **Views are addressable.** Notion: "Copy link to view: Get a direct link to the particular database view you're in." Linear: "Copy view URL… Sharing a link does not automatically give anyone access to a view, it must be shared first."
- **Favourites and grouping are navigation aids.** Airtable's sidebar sections are "My personal views," "More personal views," "My favorites," "Custom view sections," and "More collaborative views." Notion: "You can reorder your views by dragging them. If you have a lot of views, you can select `{#} more...`."
- **Ownership is explicit.** Linear: "Every view has an owner property visible in that View's dedicated sidebar… This field defaults to the creator of the view but can be changed to other users as desired. Before deleting a view, we advise checking in with its owner."
- **Scope by audience.** Linear: "If a shared view is created at the workspace level, then the view will appear under Workspace views… and is available to full members. If you select a specific team, project, or initiative when creating the view, the shared view is available within that team, project, or initiative scope."
- **Copy before you convert.** Airtable's warning: "If you choose to switch a non-personal view to a personal view, then… the 'original' view will not remain after converting to a personal view. As a best practice tip, duplicate any views you wish to keep before converting them."
- **Config transfer is a first-class feature.** Airtable lets you "copy another view's configuration," picking which elements to copy, but "the different view configuration options that can be copied **vary depending on the view type**" and "You can only copy view configurations from views within the same table."

## Filter and sort mechanics worth copying

- **Filter groups nest.** Notion: "combine `AND` and `OR` logic by using filter groups. These can be nested up to three layers deep!" Three levels is a sensible depth cap for a UI.
- **Sort order per enum is author-controlled.** Notion: "For `Select` and `Multi-select` properties, you get to define what sorting order means. Click on the property, then drag options up or down to set the sort order." Alphabetical ordering of a status column is almost never what anyone wants.
- **Multi-sort order is explicit.** Notion lets the user "Change the order that multiple sorts are applied by dragging them up or down using `⋮⋮`." (Note the ARIA ceiling: `aria-sort` cannot express sort level — see `table-columns-sorting.md`.)
- **Sorting is property-type dependent.** Notion: "Text properties such as `Name` and `Text` sort alphabetically. Number properties sort numerically."
- **Keep filter state in the URL so views are shareable by link.** Shopify's index-table migration puts `query`, `status`, `sort`, `cursor`, `direction` in URL search params, which makes any state of the table copy-pasteable — the same outcome Notion and Linear get from view URLs.
- **Subscriptions are a view-level concern.** Linear: "Configure personal or Slack channel notifications when an issue meets specific parameters defined by a view, or when an issue in a view is closed."

## Checklist for shipping a view system

1. Every view owns: layout, column visibility + order + widths, filters, sorts, grouping, page size, pinned columns.
2. Changing a view's config does not change any other view's config. Enforce with a test.
3. Every view has a URL. Back/Forward restores it exactly.
4. Personal edits never write to a shared view until published; "Set as default" is explicit and reversible ("Reset to default").
5. Locking is per view, gated on a role, and never allowed to remove the last shared view.
6. Enum sort order is configurable by an author, not derived alphabetically.
7. Renaming, duplicating, and deleting are separate actions; duplicating before converting is the documented safe path.

**Not found:** Weights & Biases documentation for **per-workspace locking** of a saved view, and any documented limit on how many views a surface may have. Airtable states a related but different rule: "In any table containing more than 20 views, new or duplicated views are automatically created as personal views rather than collaborative." What would settle it: W&B's workspace/saved-view API reference (`docs.coreweave.com`, which redirected to an access-restricted page when I fetched it) and a W&B article on saved-view permissions.

## Sources

- Notion Help Center, "Views, filters, sorts & groups" — https://www.notion.com/help/views-filters-and-sorts — Notion — accessed 2026-10-05
- Airtable, "Getting started with Airtable views" — https://support.airtable.com/docs/getting-started-with-airtable-views — Airtable — accessed 2026-10-05
- Linear, "Custom Views" — https://linear.app/docs/custom-views — Linear — accessed 2026-10-05
- Linear, "Display options" — https://linear.app/docs/display-options — Linear — accessed 2026-10-05
- Linear, "Filters" — https://linear.app/docs/filters — Linear — accessed 2026-10-05
- Weights & Biases, "Create and manage saved views" — https://docs.wandb.ai/weave/guides/tools/saved-views — Weights & Biases — accessed 2026-10-05
- Shopify, "Migrate IndexTable from Polaris React" — https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/index-table — Shopify — accessed 2026-10-05
- Shopify, "Migrate DataTable from Polaris React" — https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/data-table — Shopify — accessed 2026-10-05
- W3C ARIA Authoring Practices, "Grid and Table Properties" — https://www.w3.org/WAI/ARIA/apg/practices/grid-and-table-properties/ — W3C — accessed 2026-10-05