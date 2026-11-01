# Signature moves

Which production web apps to look at, and what to actually take from each.

This file covers **logged-in B2B SaaS product surfaces** — dashboards, data tables, settings,
admin, billing, builders. Marketing and landing pages are out of scope, as are mobile apps.

Every move below is an observable design decision with a source behind it. **Steal the decision,
not the layout.** A Linear list view transplanted into a settings page is a costume; the decision
behind it — "don't compete for attention you haven't earned" — is transferable.

Do not generalise any single vendor's choices into a universal rule. Two of the fourteen products
here ship dark-first, four ship light-first, and one ships a warm tan. None of that is a law.

---

## Posture A — Restrained instrument

**References:** Linear · Stripe · Grafana · Datadog · GitHub (Primer) · Vercel · Okta

**Feel:** the chrome is a frame, not a statement. The user arrived to read or change something; the
interface's job is to make that one thing easy and then get out of the way.

### Moves

1. **Visual weight is rationed, and the rationing is explicit.** Linear's rule is that not every
   element carries equal weight — parts central to the task stay in focus, parts that support
   orientation recede. Their 2026 refresh moved the sidebar "a few notches dimmer" so the content
   area takes precedence, dimmed inactive text, reduced vertical padding, and shrank icons.
   *(Linear, "A calmer interface for a product in motion")*
2. **Theme from three inputs, not a hundred hand-tuned ones.** Linear generates light and dark
   themes from base colour, accent colour, and a contrast variable — three, replacing "98 specific
   variables for each theme" — using the LCH colour space so equal lightness reads equally light
   across hues. A contrast slider then produces super-high-contrast themes for accessibility.
   *(Linear, "How we redesigned the Linear UI (part Ⅱ)")*
3. **Colour contrast is a property of the scale, not of each pairing.** Stripe rebuilt its palette
   in CIELAB so that every hue follows one contrast curve, then wrote the guarantee into the system:
   any two colours at least five levels apart have sufficient contrast for small text, at least
   four levels apart for icons and large text. Their Badge fix was to shift background *and* text up
   one level rather than retune each colour combination. *(Stripe, "Designing accessible color systems")*
4. **Friction is scaled to blast radius, by rule.** Grafana's "Tasteful Friction": saving a team
   name is low-risk and needs no ceremony; a save that overwrites a dashboard others depend on
   needs explicit, consequence-aware confirmation. Their other principles: anchor on the user's
   primary task ("Task-at-Hand"), let the system absorb complexity so the user's solution stays
   simple, and reuse rather than diverge. *(Grafana Labs, Saga Design Principles)*
5. **Nav is ordered by usage, with the top and bottom reserved for the extremes.** Datadog puts
   search and recently-accessed items at the very top, direct links to high-traffic features
   (Watchdog, Service Management) alongside, product-area groups in the middle, the "core features"
   that collect the platform's data (metrics, logs) at the bottom, then collaboration and support
   resources, then admin and help last. Inside a sub-menu, the left column lists the highlights and
   the right column carries configuration detail. *(Datadog, "A closer look at our navigation redesign")*
6. **Every component is one click from its source.** Datadog's DRUIDS ships a "Loupe" — a keyboard
   shortcut on any page reveals every design-system component in use, hovering through to source,
   design tool, and docs — plus auto-generated API tables pulled from the component's source code,
   because a design system is "worthless without designers and developers actually using it."
   Their stated platform tenet: minimise dead ends, keep additional context close at hand.
   *(Datadog, "DRUIDS, the design system that powers Datadog")*
7. **Semantic tokens by function, many themes per mode.** Primer runs light and dark modes, each with
   a default, dimmed, high-contrast, and colour-vision-deficiency themes; tokens are named by role
   (`fgColor-*`, `bgColor-*`, `borderColor-*`) rather than hue; and contrast changes were made once in
   Primer Primitives after the team identified over 100 text-on-background colour pairs and
   automated the checking. Primer keeps **Product UI** and **Brand UI** as separate systems.
   *(GitHub, "Unlocking inclusive design: how Primer's color system is making GitHub.com more inclusive")*
8. **Same tab everywhere, and the same page at two scopes is a filter, not a second route.** Vercel's
   February 2026 dashboard redesign moved horizontal tabs into a resizable, hideable sidebar, made
   tabs consistent across team and project levels, ordered items by the most common developer
   workflows, and turned projects into filters so switching between the team and project version of
   the same page is one click. *(Vercel, "New dashboard redesign is now the default")*
9. **Restyle incrementally, behind a flag you can toggle against the old version in one click.**
   Linear shipped its redesign behind an internal dev-toolbar feature-flag toggle so "when something
   didn't look right, it took us just one click to compare it with the previous version," rolling
   out by percentage of workspaces per day rather than all at once. Okta calls the same discipline
   "think big while acting small": unify the suite's vision, prioritise features by known customer
   feedback, ship continuously. *(Linear, redesign part Ⅱ; Okta, "Unifying the look and feel of Okta's products")*

### Per app — steal / don't copy

**Linear**
- *Steal:* the earned-attention rule as a review question. For every element on the screen, ask
  whether it is competing for attention the user hasn't granted it. Dim the chrome, keep the work
  area lit. Also steal the 3-variable theme generation if you support light *and* dark with a
  contrast control.
- *Don't copy:* the dimmed chrome only works because Linear's content area carries the weight and
  its users are dense, keyboard-driven, single-purpose. On a Focused surface (onboarding, checkout,
  a settings detail) a nearly-invisible sidebar and 12px labels read as unfinished. Their tab-bar
  compaction also assumes a desktop Electron client with many open tabs — a plain web app with one
  route has nothing to compact.

**Stripe**
- *Steal:* the level-based contrast guarantee, stated as a rule your palette can be checked against.
  It converts a per-combination audit into a single invariant. Also steal the "shift both levels
  together" fix for badge/chip families rather than tuning each one.
- *Don't copy:* their conclusion that vibrancy and accessibility are compatible only because they
  built a perceptual tool. Without a contrast guarantee enforced in tokens, a vibrant brand palette
  on small text simply fails. And do not copy the reduced customisation policy wholesale — Stripe
  caps third-party app styling because it controls the host surface; a product that owns its own
  extensibility model needs the opposite.

**Grafana**
- *Steal:* "Tasteful Friction" as a written rule, applied to destructive and overwriting actions
  specifically. Their reasoning is the transferable part: match friction to the severity and blast
  radius of the action, not to the action's label.
- *Don't copy:* Grafana's density and its alert-vs-panel mental model assume an on-call operator
  reading live state. Copying the density into a Standard or Focused surface produces the cramped
  reading this skill's craft floor already forbids. Also: Saga's repo is archived and its docs now
  live in Storybook — do not cite Saga as current tooling.

**Datadog**
- *Steal:* the sidebar ordering logic (used → areas → core data → resources → admin) and the
  two-column sub-menu split between "what this is" and "how to configure it." Both are cheap and
  survive transplant.
- *Don't copy:* the "core features at the bottom" logic assumes a funnel where users arrive with a
  question and leave through data. On a workspace or settings surface there is no such funnel, and
  burying the object list at the bottom strands it. Their 20+ products and 1,000+ integrations also
  make hover-to-jump menus necessary; with fewer destinations, a hover flyout is wasted motion.

**GitHub (Primer)**
- *Steal:* functional token naming and one-contrast-change-in-primitives. Also the Product UI /
  Brand UI split — if your marketing and product surfaces share tokens today, separate them.
- *Don't copy:* Primer's scale of variants. Primer exposes many themes and hundreds of components
  because it serves four audiences with different abilities and different surfaces. A single-product
  app that ships all of it ships a design system nobody can hold in their head, and Primer's own
  contribution guide treats this as a problem.

**Vercel**
- *Steal:* projects-as-filters, and the resizable/hideable sidebar. Both remove a class of
  navigation bug rather than a class of visual problem.
- *Don't copy:* assuming two scopes (team and project) for every route. Where a resource is genuinely
  scoped differently, two scopes per route doubles your nav, your breadcrumbs, and your empty
  states. Also, Geist's materials are documented as presets for radii, fills, strokes, and shadows —
  take the *structure*, and get the actual values from `design-systems/devtools/`, not from prose.

**Okta**
- *Steal:* the "think big while acting small" sequencing, and their diagnosis that fragmented UX
  across a suite causes "steep learning curves and cognitive overload" — the argument for spending
  redesign budget on the shared nav before any single surface.
- *Don't copy:* their admin-console bridge strategy of stylesheets that mimic a newer design system
  so a later cutover blends in. Sentry's SVP of Design made the opposite call about coexisting
  generations — "we can't have a Franken app… that to me just ruins trust" — and that reading is
  better supported. Do not ship a frankenstein console.

---

## Posture B — Committed brand

**References:** Sentry · Slack · Figma · PostHog

**Feel:** the product *is* the brand, so the interface carries personality — but every expressive
move is measured against a stated cost to the user's work.

### Moves

1. **Personality is admitted as a product requirement, then bounded.** Sentry shipped S.C.R.A.P.S.
   — Standardized Collection of Reusable Assets & Patterns for Sentry — after "our product looked
   like boring enterprise software, while our brand screamed bold and irreverent." The brief was
   explicitly *not* a sleeker UI: it was "something that felt like us again," balanced against
   "the tension between the art and the system." The stated test: "more vibrant, more tactile…
   still gets out of your way when you're working." Cost: a year and a half across design, a
   newly-spun-up design engineering team, front-end, and brand, rebuilding hundreds of components.
   *(Sentry, "Sentry has a bold new look")*
2. **Expressiveness lands in physicality, not ornament.** S.C.R.A.P.S. drops elements *into* the
   page when they expect text input, makes buttons stand taller than other elements and recess to
   the page surface when pressed, lifts buttons slightly on hover "to greet your cursor" — which
   they note real buttons don't do — and has switches convey state through their tactile style. They
   keep Flat UI's uniformity and add ornament only to communicate what input an element expects.
   *(Sentry, as above)*
3. **Personality must not cost density.** Slack's 2023 refresh explicitly committed to "keeping all
   of the information density intact," on the argument that a communication tool's original design
   "handled displaying varied information in a structured and consistent manner very well." The
   changes that shipped were approachability ones: gradients and transparent surfaces to feel
   lighter, more rounded buttons and avatars, less stark borders, added elevation to delineate
   regions. *(Slack Design, "A new visual language for Slack")*
4. **Expressiveness comes from acknowledging the user's taste, not from winning the argument about
   it.** Slack's designers explicitly rejected "our taste is the best taste" reasoning, because
   "what we as designers determine to be aesthetically pleasing may not align with other people's
   tastes," and used a desk metaphor: people love their desk because it's theirs. They cut theming
   from nine inputs to four and replaced hex entry with twenty predetermined palettes, plus a
   "Surprise Me" button — Slack's own research found "less than 85% of users changed the default
   theming preset." *(Slack Design, as above)*
5. **Ambient signals replace notification badges.** Slack's *Bloops* put the sender's avatar
   temporarily over the Direct Messages icon as a real-time signal, with a convention that names
   both the *type* of activity and *where* in the nav it will appear — so the user can decide
   whether to switch context without leaving. *Peeks* make hovering a nav tab preview that tab's
   contents, including jumping straight to a specific message. *(Slack Design, as above)*
6. **Redesigns ship as reversible, flag-gated comparisons and get reverted when they cost speed.**
   Figma shipped UI3 with an opt-out during beta ("if you get UI3 on a Wednesday, but have a work
   deadline for Friday, you can still go back to the old version"), then reversed its headline idea:
   floating panels shipped, then came back as fixed-but-resizable after beta users reported the
   panels cramped the canvas, made designs "peek out from behind them," and moved rulers too far
   from the work. "The nail in the coffin was learning that they slowed people down." Figma also
   reverted two smaller controls: blend mode came out from behind an icon button (the tooltip delay
   slowed the workflow) and clip content came back from a dropdown to a checkbox (the extra click
   slowed the workflow). *(Figma, "Our approach to designing UI3")*
7. **Say the rule out loud and let it override the layout.** Figma's Minimize UI collapses the side
   panels for distraction-free work but keeps tools reachable, and its navigation panel now lists
   file, branch, and project name *linearly*, then pages, then layers — chosen because it leaves
   "a logical place for those to extend without hard tradeoffs." The team described its pre-UI3
   condition as "playing Tetris while fitting in new features." *(Figma, as above)*
8. **Accessibility is settled before minimalism, not after.** Figma's early UI3 labelling proposal
   showed only a minimal noun label with the direction in a tooltip; the team reversed it — "this
   was a deal breaker" — so visible labels now match the `aria-label`, giving full context in both.
   UI3 also ships 200 hand-drawn icons, backgrounds on inputs, and borders around dropdowns.
   *(Figma, as above)*
9. **Expressiveness costs nothing if the density is set deliberately.** PostHog published the
   trade as a table: whitespace → data density; large titles → smaller text; whole-page scroll →
   fixed panels and panes; large buttons and nav → keyboard-focused navigation; Web 2.0 →
   desktop-like layout. The goal was stated as "PostHog should feel less like a generic SaaS app
   and more like a dev tool," with "dev tool" defined to include any product built with power users
   in mind. *(PostHog, "What if PostHog looked like a dev tool?")*
10. **Brand colour and product colour get reconciled, deliberately.** PostHog had "a stark
    contrast between our website branding and the product" and made the product's buttons match the
    website as an explicit goal, calling the effort tricky because buttons serve different purposes
    on a site and in a product. Their light mode ships a deliberately warm "PostHog tan."
    *(PostHog, as above)*
11. **Personality shows up in navigation structure, not just pixels.** PostHog replaced a
    always-growing product list with nested folders, an "Unfiled" migration bucket so existing data
    had a home, user-pinned shortcuts for anything, and a searchable Products menu behind a gear —
    plus a draggable, double-click-collapsible sidebar divider for users who have internalised the
    icons. *(PostHog, "Breaking: Local engineers outraged as PostHog removes its beloved clutter")*

### Per app — steal / don't copy

**Sentry**
- *Steal:* the physicality rules as a checklist. Which elements expect text input and should sink?
  Which should stand proud? Which states can be read from shape rather than colour alone? That is a
  testable set, and it survives outside their illustration style.
- *Don't copy:* the ornament itself. S.C.R.A.P.S. took a year and a half, a dedicated design
  engineering team, and hundreds of rebuilt components, and it is explicitly justified by a brand
  whose illustrations are the reference. Transplant the *logic* — element type determines treatment
  — but you cannot transplant the payoff, and half-adopting the style on a Dense admin console reads
  as skeuomorphic noise.

**Slack**
- *Steal:* ambient activity signals with an explicit naming convention, and preview-on-hover for nav
  destinations. Both cut context switches, which is their stated goal ("reduce pogo-sticking").
  Also steal the theming lesson: reduce the number of customisation *controls* to make customisation
  more likely, rather than adding controls.
- *Don't copy:* hover previews are a pointer affordance and mean nothing on touch or keyboard-only
  use. Nor does the avatar-over-nav-icon signal survive a layout where the nav is text-labelled. And
  Slack's density commitment is scoped to a messaging surface with an established information
  hierarchy; on a settings surface, "keep all the density" is not a goal.

**Figma**
- *Steal:* the reversal discipline. Ship the bold idea behind a flag, measure, and be willing to
  take it back — twice, in Figma's case, at whole-interface and single-control scale. Also steal
  linear (not nested) navigation ordering chosen for future extensibility, and the rule that
  visible labels match `aria-label`.
- *Don't copy:* Figma's context. Its users are in the tool for hours a day, which is why chrome
  reduction and Minimize UI pay off and why floating panels felt like a loss. On a surface people
  visit for two minutes a day, Minimize UI is a feature nobody finds and a layout you now have to
  support twice. Its opt-out-during-beta model is also expensive; it needs a second implementation.

**PostHog**
- *Steal:* the fixed-panels-and-panes layout and the keyboard-first navigation, plus the honest
  admission that brand and product had drifted and were reconciled on purpose. Also steal the
  pin-your-shortcuts move — it hands the long-tail nav problem back to the user, which is how
  Datadog and Vercel both solve it structurally.
- *Don't copy:* the tan. It is a brand choice by a company whose brand *is* irreverent, and warm
  off-whites shift every contrast calculation you validated elsewhere. Nor the "Surprise Me"
  randomisation on a surface where a user needs to recognise a state at a glance.

---

## Posture C — Configurable workbench

**References:** Retool · Supabase · Notion

**Feel:** the surface is a machine the user configures or fills. Density is the product. The job is
to make a lot of variable content legible and to keep the machinery from leaking into the work.

### Moves

1. **Ship a component library shaped by the surface class, not by a general framework.** Retool
   rebuilt off Ant Design after "building increasingly brittle hacks and maintaining hundreds of
   manual overrides," producing 90+ components with 40+ input options carrying pre-configured
   validation and dynamic row height, and 20+ table column types with per-column border-visibility,
   dynamic row height, and conditional cell, column, and row colour. *(Retool, "Why Retool rebuilt
   our UI component library from scratch")*
2. **Tables lose their furniture to gain data.** Retool's own table guidance: remove the outside
   border, the vertical borders, and the box shadow, and use only very light, semi-transparent cell
   backgrounds. *(Retool Docs, Design best practices)*
3. **Pick the table complexity that matches the job — three, not one.** Supabase documents three
   tiers: `Table` for static, read-only, known-row-count display; `Data Table` (TanStack) for
   sorting, filtering, pagination, search, and row actions; and `Data Grid` (React Data Grid) when
   you need virtualization, column resizing, or spreadsheet-like cell editing. Their own rule:
   "Use Data Grid only when you need virtualization today, you need column resizing, or you need
   spreadsheet-like editing. Otherwise Data Table is simpler and more flexible." Their Data Grid
   reference configuration is `rowHeight` 44 with `headerRowHeight` 36. *(Supabase Design System,
   UI Patterns: Tables)*
4. **Controls carry their own formatting and validation, so the user stops doing work.** Retool
   ships presets preconfigured for URL, Email, and Currency with one-click switching between
   equivalent components; Supabase requires `FormItemLayout` rather than hand-composed form items
   and exposes a `size="tiny"` variant for filter and pagination controls in dense tables.
   *(Retool, component library post; Supabase Design System, Tables / Supabase Studio UI patterns)*
5. **Theme centrally, scope the escape hatch.** Retool exposes key values globally in organization
   settings that apply across apps, with per-app overrides, Light/Dark template themes "optimized for
   high-contrast use," and user tokens for colour, typography, and metrics including a default border
   radius — with custom CSS available globally or per app for what tokens can't reach. *(Retool Docs,
   Themes)*
6. **Layout is a small set of named page parts, composed per screen.** Supabase's Studio pages are
   built from `PageContainer`, optional `PageBreadcrumbs` / `PageNav`, `PageHeader`, and
   `PageSection`. *(Supabase Design System, UI Patterns: Layout)*
7. **Rhythm comes from a spacing scale plus neighbour-awareness, not from alignment.** Notion
   abandoned baseline alignment — blocks vary in height and are often user-controlled — in favour of
   standardised spacings, then made padding adjacency-aware: a block's neighbours above and below
   change its padding, and a list item whose neighbour is another list item gets reduced padding so
   lists chunk together while paragraphs keep breathing room. The rule covers checklists, bulleted,
   toggle, numbered, and page lists. *(Notion, "Updating the design of Notion pages")*
8. **Make the deliberate break in the scale visible and justified.** Notion found that with one
   uniform block padding, single-line list items looked badly over-padded; with one uniform gap,
   paragraphs felt too tight. The answer was two different mechanisms — paragraph spacing distinct
   from single-line spacing — so paragraphs read as scannable breaks. *(Notion, as above)*
9. **Keep the library small enough that it stays true.** Supabase deliberately adds only components
   used more than a few times, explicitly to avoid the system "spread[ing] into unique use-cases and
   suffer[ing] content bloat," and uses nested Figma components to collapse permutations.
   *(Supabase, "How design works at Supabase")*
10. **Token pipeline runs one way, from the design file into production.** Supabase exports Figma
    variables into CSS custom properties consumed by Tailwind, so `background.default` in Tailwind
    resolves to the same palette as the Figma file — a fully synced colour system, with spacing,
    sizes, and typography named as the next expansions. *(Supabase, as above)*
11. **Design work is a reference, not a spec.** Supabase's stated model: "Design work is treated as
    a reference more than a pixel-perfect outcome," with design engineers as co-owners of what ships.
    Their iteration trick is to screenshot production and overlay new Figma elements on top rather
    than rebuild stale components. *(Supabase, as above)*

### Per app — steal / don't copy

**Retool**
- *Steal:* the table-furniture rule (drop the outer border, the vertical rules, and the shadow;
   substitute a faint cell tint) and the "the control does the formatting" principle. Both are
   observable, cheap, and correct on dense tables generally.
- *Don't copy:* the 3,400-icon and 20-column-type breadth. That is a builder for people assembling
   arbitrary internal tools, where the author — not the app — is the designer. In a fixed product
   surface it produces a configurator where a screen should be.

**Supabase**
- *Steal:* the three-tier table decision, with its stated default toward the middle tier. Most
   product tables need sorting, filtering, pagination, and row actions — and almost none of them
   need virtualization or column resizing.
- *Don't copy:* Supabase's actual row geometry. `rowHeight` 44 and `headerRowHeight` 36 come from
   their Table Editor and Query Performance surfaces; a logs or transactions view needs tighter
   rows than that, and a record detail list can afford them. Take the tier logic from them, the
   numbers from `design-systems/`.

**Notion**
- *Steal:* adjacency-aware spacing, and the discipline of naming the two mechanisms separately
   (paragraph spacing vs. line spacing) so one change cannot silently break the other.
- *Don't copy:* the neighbour rule as a general-purpose primitive. It works because every Notion
   block is user-positioned in a vertical stack with variable height. A settings page with fixed
   rows has no ambiguous neighbours, and a spacing engine that infers grouping from siblings will
   behave unpredictably on a table or a form.

---

## Choosing references

Pick **one or two** apps, not a set. Load the matching `design-systems/` spec only after the posture
is chosen.

| Surface class | Density | Start with | Add, if the screen needs it |
|---|---|---|---|
| Operate / read (dashboards, queues, issue lists, monitors) | Dense | Linear, Grafana | Datadog for wide-catalogue nav; Stripe for tabular + money-shaped data |
| Admin console, settings, IAM, permissions | Dense | GitHub (Primer), Okta | Grafana for destructive-action friction rules |
| Internal tooling / no-code / app builder | Dense | Retool, Supabase | Linear for the earned-attention review |
| Billing, invoices, payments, subscriptions | Standard–Dense | Stripe | Linear for record-detail hierarchy |
| Workspace / database / document | Standard | Notion, Airtable | Slack for ambient signals if there is realtime activity |
| Canvas / editor / creative | Standard | Figma, PostHog | Supabase for token pipeline |
| Realtime collaboration, messaging, notifications | Standard | Slack, PostHog | Linear for density discipline |
| Observability, logs, traces, error monitoring | Dense | Datadog, Grafana, Sentry | GitHub for semantic-token discipline |
| Onboarding, auth, checkout, single-form flows | Focused | **Posture A only** | Okta for auth-specific friction. Never Posture B's physicality or PostHog's tan here. |

Rules for using this table:

- **Focused surfaces borrow from Posture A and nothing else.** A committed-brand surface in
  onboarding reads as a vendor interrupt; it competes with the one thing the user came to do.
- **Two apps is the working limit.** One for hierarchy, one for the specific pattern (table, nav,
  form). Three references produce mush, because their moves conflict on purpose — Linear's dimmed
  chrome and Slack's added elevation are opposite answers to the same question.
- **When two references disagree, decide by density class, not by taste.** Linear dims its chrome
  and Stripe holds consistent visual weight across hues; Slack adds elevation and Notion removes
  shadows. The correct answer for a Dense table is Stripe's; for a Standard workspace, Notion's.
- **Never copy a layout.** Copy the decision. If the reference's answer depends on a constraint you
  do not share, take the principle and rebuild the form — every "don't copy" line above is a
  constraint you probably do not share.

## Exact values live in `design-systems/`

Nothing in this file is a substitute for a number. Type ramps, hex palettes, spacing scales,
radius and motion curves, component states — all of it belongs in the per-app specs under
`design-systems/<category>/<app>/`, loaded for the one or two apps you picked:

- `design-systems/devtools/` — Vercel, Linear, GitHub, Retool, Sentry
- `design-systems/observability/` — Grafana, Datadog
- `design-systems/backend/` — Supabase
- `design-systems/workspace/` — Notion, Airtable
- `design-systems/creative/` — Figma
- `design-systems/fintech/` — Stripe
- `design-systems/identity/` — Okta
- `design-systems/crm/` — Attio, Close, HubSpot, Pipedrive

Read `design-systems/README.md` for the index. Take every hex, size, spacing step, radius, and
duration from those files or from the app's own live product — never from this file, and never from
memory. This file only tells you *which* app to open and *what to check* once you have it.

## Not found

- **Attio — product-UI design decisions.** No primary source. Attio's own engineering blog covers
  architecture ("Where's the technical challenge in CRM anyway?", which asserts a "no-compromise
  approach to design and usability" without naming a single decision); their docs cover the App SDK,
  not the product UI. Every specific claim available about Attio's visual language comes from
  third-party reverse-engineering sites, which are not evidence. *What would settle it:* an Attio
  engineering or design post on a CRM list/detail redesign, or an official Attio design system
  published under their own domain.
- **Airtable — product-UI design posture.** No primary source found. `blog.airtable.com` publishes
  Interface Designer announcements, which are feature marketing, not design-decision records, and the
  Airtable engineering blog on Medium does not cover UI. *What would settle it:* an Airtable
  engineering post on the grid or field-type UI, or official Airtable design-system documentation.
  Airtable is therefore absent from the posture tables above despite appearing in the brief's
  candidate list, and in the `design-systems/workspace/` list for values only.
- **Slack, exact type scale and hex values.** Not substantiated from the sources cited here. The
  2023 Slack Design post describes theming mechanics (four inputs, twenty palettes) without giving
  values. *What would settle it:* Slack's own published design system or theme specification.
- **Sentry S.C.R.A.P.S. token values.** The blog post describes the rules (which elements sink,
  which stand proud, how switches read state) but publishes no dimensions, colours, or durations.
  *What would settle it:* a published Sentry design system or the design.sentry.dev token source.

## Sources

All accessed 2026-10-05.

| Source | Publisher | URL |
|---|---|---|
| A design reset (part I) | Linear | https://linear.app/blog/a-design-reset |
| How we redesigned the Linear UI (part Ⅱ) | Linear | https://linear.app/blog/how-we-redesigned-the-linear-ui |
| A calmer interface for a product in motion | Linear | https://linear.app/now/behind-the-latest-design-refresh |
| Designing accessible color systems | Stripe | https://stripe.com/blog/accessible-color-systems |
| Design your app (Stripe Apps) | Stripe | https://docs.stripe.com/stripe-apps/design |
| New Dashboard features to save you time | Stripe | https://stripe.com/blog/dashboard-updates-oct-2020 |
| Saga Design System: shaping the future of user experiences at Grafana Labs | Grafana Labs | https://grafana.com/blog/saga-design-system-shaping-the-future-of-user-experiences-at-grafana-labs |
| Design Principles (Saga) | Grafana Labs | https://grafana.com/developers/saga/foundations/design-principles |
| About DRUIDS | Datadog | https://druids.datadoghq.com/principles/about-druids |
| DRUIDS, the design system that powers Datadog | Datadog | https://www.datadoghq.com/blog/engineering/druids-the-design-system-that-powers-datadog |
| A closer look at our navigation redesign | Datadog | https://www.datadoghq.com/blog/datadog-navigation-redesign |
| Unlocking inclusive design: how Primer's color system is making GitHub.com more inclusive | GitHub | https://github.blog/engineering/user-experience/unlocking-inclusive-design-how-primers-color-system-is-making-github-com-more-inclusive |
| Primer Primitives — Color | GitHub (Primer) | https://primer.style/primitives/color/ |
| Design — contribution guidelines | GitHub (Primer) | https://primer.style/contribute/design |
| New dashboard redesign is now the default | Vercel | https://vercel.com/changelog/dashboard-navigation-redesign-rollout |
| Geist Design System introduction | Vercel | https://vercel.com/geist/introduction |
| Unifying the look and feel of Okta's products | Okta | https://www.okta.com/blog/product-innovation/unifying-the-look-and-feel-of-oktas-products |
| Okta launches its new open-source design system with a focus on accessibility — *secondary; used only for the Odyssey launch, the admin-console bridge strategy, and the WCAG-compliance claim, none of which appear in an Okta primary source* | TechCrunch | https://techcrunch.com/2021/02/04/okta-launches-its-new-open-source-design-system-with-a-focus-on-accessibility |
| Sentry has a bold new look | Sentry | https://blog.sentry.io/sentry-has-a-bold-new-look |
| A new visual language for Slack | Slack Design | https://slack.design/articles/a-new-visual-language-for-slack |
| How our biggest redesign yet came to be | Slack Design | https://slack.design/articles/how-our-biggest-redesign-yet-came-to-be |
| Figma on Figma: Our approach to designing UI3 | Figma | https://www.figma.com/blog/our-approach-to-designing-ui3 |
| What if PostHog looked like a dev tool? | PostHog | https://posthog.com/blog/posthog-as-a-dev-tool |
| Breaking: Local engineers outraged as PostHog removes its beloved clutter | PostHog | https://posthog.com/blog/redesigned-nav-menu |
| Building UI at PostHog (`frontend/src/design.md`) — *primary, in-repo; cited for the flag-gated parallel redesign only* | PostHog (GitHub) | https://github.com/PostHog/posthog/blob/master/frontend/src/design.md |
| Why Retool rebuilt our UI component library from scratch | Retool | https://retool.com/blog/redesigned-ui-component-library |
| Design — best practices | Retool Docs | https://docs.retool.com/education/coe/well-architected/design |
| Design organization and classic app themes | Retool Docs | https://docs.retool.com/apps/guides/presentation-styling/themes |
| How design works at Supabase | Supabase | https://supabase.com/blog/how-design-works-at-supabase |
| UI Patterns: Tables | Supabase Design System | https://supabase.com/design-system/docs/ui-patterns/tables |
| UI Patterns: Layout | Supabase Design System | https://supabase.com/design-system/docs/ui-patterns/layout |
| Studio UI Patterns — *primary, in-repo; cited for `FormItemLayout` and table-tier guidance only* | Supabase (GitHub) | https://github.com/supabase/supabase/blob/master/.claude/skills/studio-ui-patterns/SKILL.md |
| Updating the design of Notion pages | Notion | https://www.notion.com/blog/updating-the-design-of-notion-pages |