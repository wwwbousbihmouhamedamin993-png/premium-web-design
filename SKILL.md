---
name: premium-web-design
description: Use when the user invokes /premium-web-design by name.
version: 1.6.0
---

# Premium Web Design

Design for the part of the product people log into to work.

This skill has two layers. **Process** (this file + the playbooks it routes to): how to work like a
design director — commit to a direction, build it fully, then render it and *look* at it until it
passes. **Knowledge** (`references/`, ~81 files; `design-systems/`, ~130 apps): the enforceable
standards — load 1–3 per task, on demand.

A design you never looked at is a guess. The loop is non-negotiable: brief → build committed →
render → critique against the floor → fix → re-render.

## Scope boundary

| Surface | Owner |
|---|---|
| Public marketing, landing, hero, pricing, conversion | **`premium-marketing-design`** — do not handle it here |
| Mobile app UI | **`premium-mobile-design`** |
| **Logged-in SaaS web product UI** | **This skill** |

This skill owns the application after authentication. If a request is a public page, hand it off
rather than improvising — the floors differ, and marketing density rules actively harm product
surfaces.

## Setup (every session — a precondition, not a suggestion)

**Do not Edit or Write any UI file until steps 1 and 3 are done this session.** If you are about to
edit a UI file and skipped a step, stop and do it now — skipped setup is the failure mode this
skill exists to prevent.

1. Run `node <skill-base-dir>/scripts/context.mjs` once (optionally `--target <path/to/file>`). It
   prints the host project's product and design docs. Follow its directives — see Precedence.
2. Load the one playbook that owns the request: the command table's reference for an explicit or
   clearly implied command; `references/screen.md` for a new surface or replacement;
   `references/critique.md` when the ask is a review. Ask once if two fit.
3. Load `references/craft-floor.md` immediately before editing UI — the verify/refuse floor every
   build is held to, including the density-class table. Planning-only work may skip it.

## Modes

The mode names what the user's success looks like on this surface. Choose from the surface, not the
product — a billing tool's upgrade screen is still *Decide*.

- **Operate** — the user completes a task: data entry, editing records, configuring settings, bulk
  actions, admin work. Speed, density, and keyboard reach outrank expression.
- **Read** — the user understands state: dashboards, reports, logs, audit trails, analytics.
  Structure for comprehension first, then make it worth staying in.
- **Decide** — the user commits to something that costs money or can't be undone: plan changes, seat
  counts, permission grants, feature enablement, data export. The screen must make the consequence
  legible *before* the click, not after.
- **Support** — the user is inside someone else's work: agent consoles, review queues, approval
  workflows, collaborative editors. Your work is context, so chrome recedes.

`Decide` and `Support` are the modes with no mobile analogue. In-product `Decide` screens face a
committed user with existing data at risk — the opposite of a visitor being persuaded.

## Density classes

Web product surfaces span a wide density range, and one set of defaults cannot serve all of them.
**Declare the class before applying any typographic or spacing rule.** Boundaries are a design
decision, tuned against real observation.

| Class | Surfaces | Base body | Row height | Measure |
|---|---|---|---|---|
| **Focused** | Auth, onboarding, checkout, single-form flows, settings detail | 16px | — | 60–70ch, centered |
| **Standard** | Project home, card+list feeds, record detail | 14–15px | 40–44px | 65–80ch |
| **Dense** | Data tables, admin consoles, observability, logs, trading, IDE-like | 12–13px | 28–32px | full-width |

This is the mechanism that lets one skill serve a Stripe-style console and a Stripe-style checkout.
Full rules and the detector-override table: `references/craft-floor.md`.

## Commands

| Command | Category | What it does | Reference |
|---|---|---|---|
| `init` | Build | Capture product truth (`PRODUCT.md`) & derive a framework-agnostic `DESIGN.md` + optional `DESIGN-[framework].md` adapters | [init.md](references/init.md) |
| `screen [feature]` | Build | Design + build a new screen or flow, end to end | [screen.md](references/screen.md) |
| `shell [target]` | Build | App shell, sidebar, routing model, page composition, breadcrumbs | [app-shell-navigation.md](references/app-shell-navigation.md) |
| `table [target]` | Build | Data grid: columns, sorting, selection, bulk actions, virtualization | [data-tables.md](references/data-tables.md) |
| `form [target]` | Build | Form architecture, validation timing, error placement, recovery | [forms-validation.md](references/forms-validation.md) |
| `billing [target]` | Build | Plans, seats, upgrade/downgrade, proration preview, invoices, usage limits | [billing-subscriptions.md](references/billing-subscriptions.md) |
| `admin [target]` | Build | Settings IA, roles & permissions, members, invitations, audit log | [settings-information-architecture.md](references/settings-information-architecture.md) |
| `tokens [target]` | Build | Establish or repair the token system (primitive → semantic → component) | [tokens.md](references/tokens.md) |
| `document [target]` | Build | Generate `DESIGN.md` from existing code | [document.md](references/document.md) |
| `direction [target]` | Build | Mood archetype, signature move, two-tier category refusal, 3–5 machine-enforced brand invariants → `DESIGN.md` §1 | [direction.md](references/direction.md) |
| `specimen [target]` | Build | Render the whole design language as one token-faithful page; stop-and-ask confirmation before any screen scope | [specimen.md](references/specimen.md) |
| `atmosphere [target]` | Build | Declare an earned atmosphere moment (family, intensity, trigger, fallback, dither) or audit an existing one | [atmosphere.md](references/atmosphere.md) |
| `critique [target]` | Evaluate | Scored design review (0–100) + slop detector | [critique.md](references/critique.md) |
| `audit [target]` | Evaluate | Mechanical checks: a11y, states, perf, plus `impeccable detect` | [quality-audit-checklist.md](references/quality-audit-checklist.md) |
| `a11y [target]` | Evaluate | WCAG 2.2 conformance against the real DOM | [accessibility-web.md](references/accessibility-web.md) |
| `density [target]` | Enhance | Re-tier a surface between Focused / Standard / Dense | [information-density.md](references/information-density.md) |
| `layout [target]` | Enhance | Grid, rhythm, hierarchy, alignment | [layout.md](references/layout.md) |
| `typeset [target]` | Enhance | Type ramp, measure, leading, numerals | [typeset.md](references/typeset.md) |
| `colorize [target]` | Enhance | Semantic color, accent scarcity, surface steps | [colorize.md](references/colorize.md) |
| `animate [target]` | Enhance | Purposeful motion, reduced-motion variants | [toolkit-motion.md](references/toolkit-motion.md) + [radius-motion-tokens.md](references/radius-motion-tokens.md) |
| `polish [target]` | Refine | Final quality pass before shipping | [polish.md](references/polish.md) |
| `unslop [target]` | Refine | Rescue AI-looking ("vibecoded") UI: audit → triage → direction → nine ordered passes | [remediation.md](references/unslop/remediation.md) |
| `distill [target]` | Refine | Strip to essence, remove complexity | [distill.md](references/distill.md) |
| `onboard [target]` | Refine | First-run flows, empty states, activation | [onboard.md](references/onboard.md) |
| `harden [target]` | Fix | Errors, edge cases, permissions, offline, long lists | [harden.md](references/harden.md) |
| `clarify [target]` | Fix | UX copy, labels, error messages, destructive confirms | [clarify.md](references/clarify.md) |
| `adapt [target]` | Fix | Viewport, container, and density adaptation | [responsive-edges.md](references/responsive-edges.md) |
| `optimize [target]` | Fix | Core Web Vitals, render cost, large lists | [web-vitals-performance.md](references/web-vitals-performance.md) |
| `loop [target]` | Iterate | Render → critique → fix cycle on real pixels | [render-loop.md](references/render-loop.md) |

### Routing

- **No argument:** present the command table; never auto-run a command.
- **Explicit or clearly implied command:** load its reference and follow it.
- **Otherwise:** general design work — a new surface → `references/screen.md`; refinement of
  existing UI → `references/polish.md`; a review → `references/critique.md`.
- **A request with no `PRODUCT.md` or `DESIGN.md`:** route through `references/init.md` first. A
  narrow refinement of existing code proceeds without blocking on it, offering init afterward.
- **AI-slop rescue** ("this looks AI-generated", "vibecoded", "unslop this screen", "too many
  gradients/emoji") → `references/unslop/remediation.md`.
- **Shader surfaces, atmosphere & banding** ("aurora", "mesh gradient", "grain", "noise overlay",
  "gradient banding", "the empty state looks flat") → `references/atmosphere.md` — governed exception;
  the default is none.
- **Visual direction & mood** ("define direction", "mood archetype", "signature move", "category
  refusal", "brand invariants", "it looks like every other console") → `references/direction.md`.
- **Design-language review** ("specimen", "review the whole design language", "design system page")
  → `references/specimen.md`.
- **Media runtime** ("add a Lottie", "embed the product tour video", "the empty state animation") →
  `references/toolkit-media-runtime.md`.
- **Produce media assets** ("make a product video", "voiceover", "3D hero asset", "demo reel") →
  hand to `premium-marketing-design` (`toolkit-asset-pipeline.md` owns production; this skill only
  embeds the outputs).
- **A public marketing page:** hand off to `premium-marketing-design`.

## Precedence

Conflicts resolve in this order:

1. **Host project constitution** — `DESIGN.md`, `PRODUCT.md`, `DESIGN-[framework].md`, `AGENTS.md`,
   established wrapper components, brand tokens, copy voice. Project rules win; if the project
   demands 32px targets in a console, that beats this skill's 24px floor.
2. **This skill's floor** — `craft-floor.md` and the playbooks.
3. **Reference web design systems** — `design-systems/`.
4. **Generic web advice, including Impeccable's detector defaults.** See below.

Never relitigate a project's committed dials; fill gaps instead.

### The Impeccable bridge

`npx impeccable detect` is a **dependency, not a fork** — invoked from `audit` and `loop`, never
vendored or re-maintained. Its rules encode marketing-page defaults that are wrong on product
surfaces: `tiny-interface-text` reads "increase the size so people can read without zooming," which
is correct in a Focused surface and wrong in a Dense one. `craft-floor.md` carries a per-density
override table; treat those findings as advisory at the class noted, not as failures. Usage,
exit codes, and exception discipline: `references/detector-integration.md`.

## Knowledge library

Load only what's relevant — 1–3 files per task.

### Layout, shell & hierarchy
`app-shell-navigation.md` · `routing-navigation-model.md` · `page-composition.md` ·
`layout-grid.md` · `responsive-container-queries.md` · `information-density.md` ·
`whitespace-hierarchy.md` · `visual-hierarchy.md` · `sidebar-navigation.md`

### Data, tables & views
`data-tables.md` · `table-columns-sorting.md` · `bulk-selection-actions.md` ·
`pagination-infinite-scroll.md` · `virtualization-lists.md` · `views-filters-sorts.md`

### Forms & input
`forms-validation.md` · `text-inputs.md` · `selection-controls.md` · `date-time-pickers.md` ·
`file-upload.md` · `search-filter-sort-ui.md` · `command-palette.md`

### Overlays & feedback
`modals-dialogs-drawers.md` · `popovers-tooltips.md` · `toasts-notifications.md` ·
`z-index-layers.md` · `focus-management.md`

### States
`loading-skeletons.md` · `empty-states.md` · `error-states.md` · `offline-stale-sync.md`

### Dashboards & data viz
`dashboard-composition.md` · `charts-data-viz.md` · `metrics-stat-tiles.md`

### Settings, admin & identity
`settings-information-architecture.md` · `admin-console.md` · `roles-permissions-matrix.md` ·
`member-invitations.md` · `audit-log-ui.md` · `sso-mfa-sessions.md` · `api-keys-webhooks.md`

### Commerce & entitlement
`billing-subscriptions.md` · `plan-upgrade-downgrade.md` · `usage-limits-quotas.md` ·
`invoices-payments.md` · `entitlements-feature-gating.md`

### Content, media & AI
`rich-text-editing.md` · `media-images-avatars.md` · `notifications-activity-feed.md` ·
`ai-chat-ui.md`

### Theme & tokens
`color-token-system.md` · `dark-mode.md` · `elevation-layers.md` · `typography-web.md` ·
`iconography.md` · `radius-motion-tokens.md`

### Direction & atmosphere
`direction.md` — mood archetypes, signature-move authoring, two-tier category refusal, machine-enforced
invariants · `atmosphere.md` — the governed earned-atmosphere contract: families, banding & dither
(including chart gradients), grain policy · `specimen.md` — the design language on one confirmed page

### Toolkits
`toolkit-selection.md` · `toolkit-motion.md` · `toolkit-bklit-dataviz.md` ·
`toolkit-godly-inspiration.md` · `toolkit-kokonutui-registry.md` · `toolkit-media-runtime.md`

External tools this skill expects you may reach for — animation, charts, component registries, and
inspiration galleries. **Read `toolkit-selection.md` first.** Two of these ship defaults that
`craft-floor.md` refuses, so adopt their *mechanics* and refuse their *decorative defaults*: a
component library supplies the how, never the direction.

### Quality & operations
`accessibility-web.md` · `web-vitals-performance.md` · `i18n-rtl.md` · `responsive-edges.md` ·
`browser-native-affordances.md` · `production-launch-checklist.md` · `detector-integration.md`

### Slop rescue (unslop)
Adapted from [heydamir/unslop](https://github.com/heydamir/unslop) (CC BY 4.0); the whole kit lives in `references/unslop/`. `remediation.md` is the rescue playbook — browser look (mandated) → mechanical sweep → audit → triage → direction → nine ordered passes. Its companions: `signs.md` (the signs-of-slop audit catalog, sign → fix) · `tokens.md` (starting values: world-tinted ramps, type families by character, motion bands) · `visuals.md` (when a surface earns imagery; styles that work, prompt recipe, placement) · `effects.md` (glyph, halftone, dither, and duotone image treatments) · `refs.md` (finished screens to calibrate against, in `references/unslop/refs/`). Mechanical sweep: `scripts/unslop_grep.py`; live-site snapshot and story-video renderers bundled in `references/unslop/scripts/` (need node + Playwright, video needs ffmpeg).

### Process & system
`craft-floor.md` · `signature-moves.md` · `screen.md` · `critique.md` · `render-loop.md` ·
`ux-laws.md` · `init.md` · `document.md` · `tokens.md` · `init-design-template.md` ·
`document-template.md` · `examples.md` · `component-consistency.md`

### Domain playbooks
`saas-onboarding-playbooks.md` · `multi-tenant-workspaces.md`

### UX law
`ux-laws.md` — only the **enforceable** subset ships as rules, in three tiers: measurable
thresholds, formula-only laws with no static rule, and vocabulary that must never gate a pass.

## Design systems (~130 apps)

`design-systems/` contains reverse-engineered `DESIGN.md` specs from ~130 production web apps —
exact hex palettes, type ramps, spacing, radius scales, component states, motion curves. Each app
also carries a single downscaled `screenshot.png` as **supporting evidence only**: every rule is
fully expressible in text, because no documentation guarantees an agent reads a bundled image.

Load 1–2 when deriving visual direction or inspecting a component pattern. Never more than 2–3 at
once. See `design-systems/README.md` for the index.

**`system-docs/` is the exception to posture-fit.** Those five are public design-system
documentation sites — standards, not visual direction. Reach for them only when the work names
tokens, state matrices, density mechanics, or per-component a11y docs; never to pick a mood.
See `design-systems/system-docs/README.md`.

| Category | Path | Notable |
|---|---|---|
| Developer tools & CI | `design-systems/devtools/` | Vercel, Linear, GitHub, Retool, Sourcegraph, Sentry |
| Observability | `design-systems/observability/` | Grafana, Datadog, Honeycomb, Prometheus, Kibana |
| Data & BI | `design-systems/data-bi/` | Databricks, Snowflake, Tableau, Metabase, Hex |
| Databases & backend | `design-systems/backend/` | Supabase, MongoDB Atlas, PlanetScale, Neon, Cloudflare |
| CRM & sales | `design-systems/crm/` | HubSpot, Pipedrive, Attio, Close |
| Support | `design-systems/support/` | Zendesk, Intercom, Front, Freshdesk |
| Project & knowledge | `design-systems/workspace/` | Notion, Airtable, Asana, Monday, ClickUp, Coda |
| Design & creative | `design-systems/creative/` | Figma, Canva, Framer, Webflow, Excalidraw |
| Admin & identity | `design-systems/identity/` | Okta, Auth0, Clerk, Keycloak, JumpCloud |
| Fintech & billing | `design-systems/fintech/` | Stripe, Wise, Revolut, Plaid, Brex, Ramp, Mercury |
| Commerce admin | `design-systems/commerce/` | Shopify, BigCommerce, Squarespace, Wix |
| Infrastructure & cloud | `design-systems/cloud/` | AWS, GCP, Azure, Cloudflare, Netlify, Fly |
| Design-system standards | `design-systems/system-docs/` | Fluent 2, Spectrum, Uber Base, Gestalt, Lightning (SLDS), Geist, Wise |

**Pick posture-fit apps before building**, not after: `references/signature-moves.md`. Two postures
cover nearly everything — *restrained instrument* (Linear, Stripe, Grafana, Vercel) and *committed
brand* (Figma, Retool, Slack, Stripe's marketing-adjacent product surfaces). Steal moves, not
layouts.

## Non-negotiables

1. **Render before done.** Run `references/render-loop.md` — minimum two critique–fix passes on real
   pixels. Never declare a screen finished from code alone.
2. **Floor before build.** `references/craft-floor.md` loaded before editing UI and applied during.
3. **Declare the density class** before applying any type or spacing rule.
4. **States are designed, not afterthoughts.** Loading (skeleton, not spinner), empty (actionable),
   error (recoverable), and offline/stale — for every surface that fetches. This is where the
   industry is weakest: Carbon's own docs list Error states and Onboarding as *"(future)"*.
5. **Tokens only.** No raw hex, no magic spacing. Three layers — primitive → semantic → component —
   because no standard mandates it and this skill does.
6. **Consequence before click.** In `Decide` surfaces, the cost, the effective date, and what breaks
   are visible before the user commits.
7. **One direction, committed.** If a screen could pass the slop detector (`critique.md`), the
   self-check failed. When the detector fires on an existing screen, remediate through
   `references/unslop/remediation.md` rather than ad-hoc fixes.
8. **The specimen gates scope.** On an `init` project, no build command runs until
   `design-system.html` is confirmed (`references/specimen.md`) — a correction during review is a
   token edit plus regeneration, never a hand-tweak of the page.
9. **Atmosphere is declared or absent.** A gradient field, grain overlay, or any shader look exists
   only as a `DESIGN.md` §1 declaration with intensity, trigger, static fallback, and dither mode
   (`references/atmosphere.md`) — stage surfaces only, one moment per journey, `prefers-reduced-motion`
   served the designed frame. Everywhere else the Refuse list stands.
