# Page composition

Every logged-in B2B SaaS screen reduces to four templates: **Homepage, Index (list), Details
(record), Settings**. Shopify Polaris names index and settings as first-class templates with their
own route conventions; Carbon names the anatomy of the pieces. Both are vendor positions —
attribute them.

## Polaris's own route-file names for two of these

| Template | Polaris route file | Polaris doc says |
|---|---|---|
| Index | `app.[resources].jsx` | "should use a plural noun for the resource type. For example, `app.products.jsx`" |
| Settings | `app.settings.jsx` | "All apps have settings merchants need to configure" |

(Shopify, *Index* and *Settings* templates, shopify.dev, accessed 2026-10-05.)

## The four templates

| Template | Job | Body | Density | Page-header actions |
|---|---|---|---|---|
| **Homepage** | Orient, then route. One glance: what needs me now? | Summary metrics + a small set of live items | Standard | Usually none, or one "create" |
| **Index** | Manage a collection. Bulk actions live here. | Search/filter/sort toolbar + table or resource list | Dense | One create + up to three secondary |
| **Details** | One record. Read, then act on it. | Identity block, key fields, then history/related | Standard | One primary + up to three secondary |
| **Settings** | Configure the app. Grouped, explanatory, save-guarded. | Named sections + contextual help aside | Focused | Save/discard, guarded |

**Density per template is a derived decision, not a preference.** An index of 40+ rows is Dense;
the same route showing 6 rows for one workspace is Standard. Declare the class, then apply the
class's row heights and type sizes — see `information-density.md`.

## Page-header anatomy

Carbon and Polaris agree on the parts; only the slot names differ.

| Part | Source | Rule |
|---|---|---|
| Breadcrumb / back | Carbon breadcrumb; Polaris `breadcrumb-actions` slot | "Only accepts link components" (Polaris) |
| Title | Polaris `heading`; Carbon breadcrumb is placed "underneath the header and navigation, but above the page title" | "Always provide a title that describes the current page" (Polaris) |
| Description | Polaris `s-section` heading | Optional; one line of context |
| Primary action | Polaris `primary-action` slot | "Only accepts a single button component with a `variant` of `primary`" |
| Secondary actions | Polaris `secondary-actions` slot | "Only accepts button group and button components" |
| Supplemental content | Polaris `supplemental-start` slot | Page-wide banner, "renders between the page header and the sections" |

Polaris states the action budget as a best practice: **"Include no more than one primary action
and 3 secondary actions per page"** and **"Don't include any actions at the bottom of the page"**
(*Page* web component, shopify.dev, accessed 2026-10-05). Attribute this to Polaris; it is not a
W3C rule.

## Action placement rules

- **Page-header actions act on the whole page; row actions act on a row.** Carbon's data table
  puts "global data table actions such as table settings, complex filters, exporting, or editing
  table data" in the toolbar, and row-scoped actions behind a per-row overflow menu.
- **Table chrome caps at five toolbar actions.** Carbon: "Include up to five actions within the
  table toolbar. More actions can be made available through an overflow menu."
- **Row actions stay inline when there are few.** Carbon: "When the overflow menu contains fewer
  than three options, keep the actions inline as icon buttons instead."
- **Page width is a template decision.** Polaris's `page` component takes `inlineSize` of
  `small`, `base` (default), or `large`, where `large` is "full width with whitespace" — and its
  own layout guidance says for resource index pages "use a full-width page," which "is helpful
  when merchants are dealing with lists of data that have many columns."
- **Settings is a two-column layout on purpose.** Polaris: the settings layout "lets merchants
  quickly scan and find groups of settings that are related to each other," with "a thinner column
  on the left with a title and description, and a wider column on the right with form elements."
  Polaris's `aside` slot renders **only** at `inlineSize: base` — the aside is not a free extra.
- **Don't put navigation in the page header.** Polaris: "Avoid placing the main navigation in the
  page header. This can mislead merchants. The page header is reserved for in-page actions."
- **Don't use primary-styled buttons inside tables.** Polaris: "Actions in tables should use
  secondary action styling, such as a text button, minor icon, or dropdown menu."

## Empty, loading, and settings-specific states

- **An index page's first-run state is a real screen, not a blank table.** Polaris's Index
  template ships a full empty state with `graphic`, `subheading`, `secondary-actions`, and
  `primary-action` slots, and repeats the same create action from the page header so the entry
  point is in both places.
- **Settings pages guard unsaved work.** The Polaris Settings template "leverages the Save Bar API
  to protect unsaved changes from being lost," triggered by `data-save-bar` on the form, with
  save/discard controls appearing when the form is dirty.
- **Destructive actions get a confirm and a critical tone.** Polaris's Settings example confirms
  "Reset all settings" with a Modal carrying `tone="critical"` and an explicit "This action cannot
  be undone."
- **Destructive actions never sit at the bottom of a page** (Polaris, quoted above).

**Not found:** a primary source giving a per-template action-count budget for surfaces other than
Polaris's own (Carbon states five for the data-table toolbar; no equivalent table exists for
homepage or details). Settled by: cross-system audit of Carbon's button/action guidelines plus a
major vendor set's page-header spec.

## Sources

- Index (template) — Shopify Polaris (App Home), shopify.dev. https://shopify.dev/docs/api/app-home/patterns/templates/resource-index — accessed 2026-10-05
- Settings (template) — Shopify Polaris (App Home), shopify.dev. https://shopify.dev/docs/api/app-home/patterns/templates/settings — accessed 2026-10-05
- Page (web component: heading, slots, `inlineSize`, best practices) — Shopify Polaris (App Home), shopify.dev. https://shopify.dev/docs/api/app-home/web-components/layout-and-structure/page — accessed 2026-10-05
- Layout (single-column, two-column, settings layout, spacing, containers, tables) — Shopify App Design Guidelines. https://shopify.dev/docs/apps/design/layout — accessed 2026-10-05
- Navigation (page header reserved for in-page actions; action labels) — Shopify App Design Guidelines. https://shopify.dev/docs/apps/design/navigation — accessed 2026-10-05
- Breadcrumb (placement, variants, truncation) — Carbon Design System (IBM). https://carbondesignsystem.com/components/breadcrumb/usage/ — accessed 2026-10-05
- Data table (toolbar actions, row actions, row heights, empty/loading states) — Carbon Design System (IBM). https://carbondesignsystem.com/components/data-table/usage/ — accessed 2026-10-05
