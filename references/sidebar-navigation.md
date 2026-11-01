# Sidebar navigation IA

The sidebar answers one question: *where am I, and what else is here?* Everything below serves that.
Grouping, labelling, and search do the work. **Item-count caps do not** — and the sources below
say so explicitly, which is why arbitrary caps are called out as an anti-pattern.

## Rules

- **Group, then label.** Carbon's organisational-scheme guidance is explicit about both:
  "Create logical groups that align to your user's goals and improves access to the content," and
  alphabetisation "is only successful if the user knows what they are looking for and how the item
  is labeled. **Alphabetical navigation decreases discoverability** in cases where the user is
  looking for a synonym of an item (e.g. 'pop-up, modal, lightbox, dialogue')."
- **Nouns, not verbs, and short.** Polaris: "Make navigation items short and scannable. **Use nouns
  instead of verbs** to keep the navigation menu concise" (shopify.dev, *Navigation*, accessed
  2026-10-05).
- **Fewest categories that still cover the product.** Polaris: "**Use the fewest possible categories
  to define what your app does**" — that is a grouping instruction, not a cap on items.
- **Depth stops at two tiers in the panel.** Carbon: "The left panel does not support three tiers of
  navigation. If you have additional content to display beneath a sub-menu, use tabs within the
  page." Polaris makes the same point about tabs: use them "sparingly for secondary navigation…
  Clicking a tab should only change the content below it, not above it. **Tabs should never wrap
  onto multiple lines.** Navigating between tabs shouldn't cause the tabs to change position or
  move."
- **Where the sidebar lives.** NN/g's expected-location table places "Primary navigation menu —
  Websites: Header; **Applications: Left side of the screen**," and local navigation "along the
  left-hand side on desktop websites" (*Menu-Design Checklist*, Page Laubheimer, 2024-06-07,
  accessed 2026-10-05).
- **Show it on large screens.** NN/g: "the hamburger menu (or any form of hiding the navigation
  categories under a single menu) is **not appropriate for desktop** websites and apps. Out of sight
  means out of mind." And navigation "helps users to understand the scope of your resources or
  content."
- **Always mark the current location.** NN/g: "Users rely on visual cues from menus (and other
  navigation elements such as breadcrumbs) to answer this critical question. **Failing to indicate
  the current location is probably the single most common mistake we see on website menus.**"
  Polaris's app nav icon is "gray when it's inactive and green when it's active."
- **Mark it visually, not only structurally.** Carbon's tree view: "If the branch node of a
  selected child node is collapsed, the parent node should inherit the selected state so the user
  does not lose the context of what is selected, even if it is out of view."
- **Left-justify and front-load.** NN/g: "You can reduce the amount of time users need to spend
  reading menus by left-justifying vertical menus and by front-loading key terms."
- **Signify expandable items.** NN/g: "Clearly signify submenus with a caret or arrow icon… Users
  may not even realize that there is a submenu if the category name doesn't look clickable."
- **Click-activated, not hover-activated.** NN/g: "Hover is not universally available… **It's better
  to have a consistent, reliable interaction pattern** across devices and input modalities."
- **Do not replicate the sidebar inside the page.** Polaris: "Avoid replicating the app nav
  content in the app body, as it results in unnecessary repetition."
- **Do not put nav in the page header.** Polaris: "Avoid placing the main navigation in the page
  header. This can mislead merchants. The page header is reserved for in-page actions."

## Why arbitrary item caps are wrong

The instinct to cap the sidebar at "5–7 items" produces a specific, predictable failure: the
capped items get abstract names, because a short list has to name a *category* rather than a
resource. Users then cannot tell which bucket their task belongs in, and the routes that were
hidden become unreachable except by guessing. The evidence:

- **Carbon sets a threshold, not a ceiling, and it is a component-constraint.** "Use the left
  panel if there are more than five secondary navigation items, or if you expect a user to switch
  between secondary items frequently." That is guidance on *when to add a panel*, not permission to
  hide or merge items below five.
- **The one real cap in the sources is a rendering budget, not an IA rule — and it is explicitly
  attributed to the vendor.** Polaris: "When you use more than seven items in the `App nav` web
  component, item seven and above are truncated into a `View more` button." This is a documented
  behaviour of one component in one host platform (the Shopify admin sidebar). It is not a
  universal design rule, and treating it as one is exactly the generalisation this skill forbids.
- **The real constraint is about unbounded content, and it is about *kind*, not *count*.** Carbon:
  "**Avoid placing unbounded content in the shell side navigation. Usability drops when the number
  of items within the shell get too high. For this reason, do not place content that has no upper
  limit (such as content created by users) within the shell's side navigation. Instead, make use of
  drill down patterns**" (*Global header pattern*). The problem is the ceiling being *infinite*, not
  the number being large.
- **Drill-down is the sanctioned alternative.** Carbon: "A drill down can be triggered from any
  interactive element in an application, and will generally open a new page focused purely on the
  object that was selected. This new page will then include a breadcrumb of the path back to the
  root level above the title." Polaris ships the same pattern as the *interstitial nav* composition:
  "As your app grows, merchants need clear paths to deeper pages without cluttering your main
  navigation."

So: user-created collections, saved views, and per-resource rows stay **inside** the surface —
searchable, filterable, paginated. The sidebar carries only the fixed set a user could enumerate.

## Secondary navigation within a section

Once the panel has its two tiers, the third level of navigation belongs in the page. Options, in
order of fit:

| Pattern | Use when | Source |
|---|---|---|
| Tabs | Sibling views of the same record that fit one line | Carbon ("use tabs within the page"); Polaris ("sparingly… should only change the content below it") |
| Breadcrumb | Depth exists and the user needs to move up | Carbon: breadcrumbs are for hierarchies "of more than two levels" |
| Interstitial nav | A section is a hub linking to deeper pages | Polaris *interstitial nav* composition |
| Drill-down page | A user-selected object needs a focused page | Carbon *Global header pattern* |

## Grouping and labelling checklist

1. Every item is a noun naming a resource or task — not a verb, not a category abstraction forced by
   a length limit.
2. Groups are labelled, and the label is a heading in the a11y tree, not just visual bold text
   (Carbon on headings: "the visual representation of a heading should match the underlying
   ranking of the header tag").
3. Current location is visible on the item **and** its ancestor group when collapsed.
4. Group order follows frequency of use or the product's task model — Carbon's options are most
   recent, customized, audience, alphabetical, and company organization, and it warns that
   alphabetical "decreases discoverability," company organization should "reflect an appropriate
   domain model rather than an org chart," and most-recent ordering "loses any logical grouping and
   may be suited as an alternative way to organize rather than the primary way."
5. Expanded/collapsed group state is per-session and does not lose the active item — the Carbon
   selection-inheritance rule above.
6. Unbounded user content is absent; it is reachable by search, filter, or a drill-down route.

## Sources

- Global header pattern (organizational schemes; **unbound content must not go in shell side nav**; drill-down + breadcrumbs; local nav; C27) — Carbon Design System (IBM). https://carbondesignsystem.com/patterns/global-header/ — accessed 2026-10-05
- UI shell left panel (secondary navigation; more-than-five threshold; three tiers unsupported) — Carbon Design System (IBM). https://carbondesignsystem.com/components/ui-shell-left-panel/usage/ — accessed 2026-10-05
- Tree view (selection inheritance on collapsed parents; node labels; keyboard controls) — Carbon Design System (IBM). https://carbondesignsystem.com/components/tree-view/usage/ — accessed 2026-10-05
- Breadcrumb (more-than-two-levels threshold; never replaces primary nav) — Carbon Design System (IBM). https://carbondesignsystem.com/components/breadcrumb/usage/ — accessed 2026-10-05
- Navigation (IA; nouns over verbs; fewest categories; seven-item `View more` truncation; tabs sparingly; don't replicate nav in body or page header; current-location icon) — Shopify App Design Guidelines. https://shopify.dev/docs/apps/design/navigation — accessed 2026-10-05
- App structure (app nav / app header / page header / overflow menu / app body regions) — Shopify App Design Guidelines. https://shopify.dev/docs/apps/design/app-structure — accessed 2026-10-05
- Interstitial nav (composition) — Shopify Polaris (App Home), shopify.dev. https://shopify.dev/docs/api/app-home/patterns/compositions/interstitial-nav — accessed 2026-10-05
- Menu-Design Checklist: 17 UX Guidelines (expected menu locations; no hamburger on desktop; indicate current location; local nav for related content; clear labels; left-justify and front-load; caret to signify submenus; click not hover) — Nielsen Norman Group, Page Laubheimer, 2024-06-07. https://www.nngroup.com/articles/menu-design/ — accessed 2026-10-05
