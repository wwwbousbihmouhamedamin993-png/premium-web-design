# App shell & navigation

Logged-in B2B SaaS surfaces are built from a persistent frame that never reloads. IBM Carbon's
UI shell is the primary reference here because it names each region and states its job. Treat
Carbon's specifics as Carbon's; the region model generalises, the pixel rules do not.

## The three shell components

Carbon defines the UI shell as three components — **header**, **left panel**, **right panel** —
each usable independently but "designed to work together" (Carbon, *UI shell header*, accessed
2026-10-05). The same page repeats Carbon's table:

| Component | Job (Carbon's wording) |
|---|---|
| Header | "The highest level of navigation." Identifies the product; globally persistent. |
| Left panel | "An optional panel that is used for a product's navigation." Secondary navigation. |
| Right panel | "An optional panel that shows additional system-level actions." |

## Rules

- **The header spans the full width of the viewport and is the topmost element, persistent
  throughout the product experience** (Carbon, *UI shell header*).
- **Scope reads left-to-right as product-to-global.** Middle = system-level controls; far right
  (switcher) = the most global scope, spanning products (Carbon, *UI shell header*).
- **Utility icons open a panel; they do not navigate directly.** Carbon: "Utility icons should not
  be used to directly navigate to an area. Instead, they should open a panel that provides access
  to other places in the product" (*Global header pattern*).
- **Icon order is fixed, not decorative.** Carbon's placement table: search is the furthest-left
  icon (so its expanding field doesn't shift others); help is 4th from the right; notifications
  3rd from the right; account 2nd from the right; switcher always furthest right. Header icons are
  right-aligned **with no gaps between them**.
- **Submenu labels only open the submenu.** "Sub-menu labels serve only to open the dropdown; they
  cannot link to another page in the product." The chevron points up when open (Carbon).
- **Right panels float, anchor, and never select.** "Right panels always float over page content,
  and always remain anchored to their associated icon." Only one expanded at a time. "There is no
  selected state for right panel items" (Carbon, *UI shell right panel*).
- **Left panel is for depth, and it stops at two tiers.** Carbon: use it "if there are more than
  five secondary navigation items, or if you expect a user to switch between secondary items
  frequently," and "The left panel does not support three tiers of navigation. If you have
  additional content to display beneath a sub-menu, use tabs within the page."
- **Skip link first.** A "Skip to main content" link is the first focusable element, required by
  WCAG 2.2 SC 2.4.1 Bypass Blocks (W3C). Carbon's own site does this. Carbon also warns: starting
  focus in the main nav "could block them from the main content if there is a large number of
  navigation items to tab through first."
- **Landmark regions are labelled.** Carbon names navigation, main, form, banner, and search, and
  says: "If there are multiple navigation landmark regions give each a unique label" (*Global
  header pattern*).
- **DOM order must match visual order.** Carbon adopts WCAG technique C27 for this, and calls it
  "necessary when the organization of your navigation menu is used to convey the meaning of
  stepped concepts like provisioning or other wizard-style patterns."

## The dominant console frame: three regions

The console frame that B2B products converge on is **navigation rail → list/queue → detail pane**,
each region scrolling independently. Carbon's 2x Grid records the same hybrid sizing logic that
makes it work, and the table is directly reusable:

| Component | Width | Height | (Carbon, *2x Grid*, hybrid boxes) |
|---|---|---|
| Header | Fluid (grid) | Fixed (mini unit) | — |
| Toolbar | Fluid (grid) | Fixed (mini unit) | — |
| Side panel | Fixed | Fluid (grid) | — |
| Menu | Fixed | Fluid (content) | — |
| Content | Fixed | Fluid (content) | — |
| Data table | Fluid (grid) | Fluid (content) | — |

Two Carbon facts make the console frame legal: **"All vertical panels expand to fill the full
height of the browser window"** (*2x Grid*, panel behaviour), and Carbon's screen-region list
names **header, global sidenav, local sidenav, dropdown menu, content, footer, dialog** as the
regions users expect in fixed places.

## Shell state belongs in the URL

Carbon states the technique and the caveat plainly: "One technique to maintain this state is to
use the shell's menu items to track the essential state elements in the URL and return the user
to that URL automatically when they return. **This capability is not part of the UI Shell component
and must be added during implementation**" (*Global header pattern*). Selection, filter, and
expanded-group state are your job, not the framework's.

**Not found:** a vendor-authored, opinionated spec for resizable splitter positions persisted in
the URL or a `ResizeObserver`-based standard. Settled by: reading a production pattern's source or
a CSS spec proposal; no primary source located in this pass.

## Sources

- UI shell header — Carbon Design System (IBM). https://carbondesignsystem.com/components/ui-shell-header/usage/ — accessed 2026-10-05
- UI shell left panel — Carbon Design System (IBM). https://carbondesignsystem.com/components/ui-shell-left-panel/usage/ — accessed 2026-10-05
- UI shell right panel — Carbon Design System (IBM). https://carbondesignsystem.com/components/ui-shell-right-panel/usage/ — accessed 2026-10-05
- Global header (pattern) — Carbon Design System (IBM). https://carbondesignsystem.com/patterns/global-header/ — accessed 2026-10-05
- 2x Grid — Carbon Design System (IBM). https://carbondesignsystem.com/elements/2x-grid/overview/ — accessed 2026-10-05
- Understanding SC 2.4.1 Bypass Blocks — W3C Web Accessibility Initiative. https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html — accessed 2026-10-05
