# Design System — Prisma

<!-- premium-web-design:design-system 2 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: sibling spec premium-marketing-design/design-systems/devtools/prisma/DESIGN.md (ladder rung 1 — palette and type raw materials; its single-accent teal #14b8a6 and Mona Sans readings describe the pre-2026 brand and are superseded here by the five-hue system and Sora verified live), Linear (density/type discipline), Vercel (colour restraint + hairline shell) -->
<!-- Surface classes: 7 routes classified; density classes F/S/D assigned -->
<!-- Evidence: prisma.io homepage/pricing/docs captures, console.prisma.io login + shipped console UI screenshots (Agents workspace, App usage, project setup), prisma.io site CSS tokens. Screens in ./screens/. -->

## 1. Design Posture & Atmosphere

Prisma's 2026 surface reads as an engineer's studio lit by one prism. The canvas is a warm, paper-textured white — barely off-pure, never clinical — carrying near-black ink set in Sora for display and Inter for everything that works for a living. Colour is rationed with unusual discipline for a brand that owns five hues: cyan is the only accent that ever signals interactive truth (focus rings, live dots, chart series, links on dark), while amber, orange, red and magenta exist almost exclusively inside one signature motif — a thin diagonal stripe at 85 degrees running cyan to pink, blurred into ambient glows or drawn as a hard ribbon across hero bands. After eight hours in the console, the eye is not tired: chrome recedes to hairlines, the texture stays sub-perceptual, and the loudest thing on screen is data.

The product spans two temperature zones. Marketing (prisma.io) and the console's default dashboard are light, airy, scrollytelling-paced — big Sora statements, black pill buttons, one filled action per view. The operational surfaces (usage analytics, project setup, the dark docs landing, the login screen) are authored dark: a #0a0a0a-to-#262626 charcoal ramp with #171717 cards, cyan chart lines and tabular numerals, feeling like a night-shift observatory of your own database. Both zones share the same geometry — 10px corner system, 4px spacing grid, hairline separation — so crossing the boundary feels like dimming the lights in the same room, not switching products.

The visual metaphor: a schematic on drafting paper with a prism stripe pinned across the corner. Code is first-class imagery (terminal panels, CLI pills, schema fragments replace stock photography), numbers are always tabular and right-aligned, and every status pairs a colour with a word. The legacy brand (dark navy + green CTA + concentric triangle) survives only in old social previews and one onboarding flow; new work follows this spec.

**Key Characteristics**
- One signal hue per mode: cyan 01d7e4 carries focus, live state, links-on-dark and data series; it is never body-size text on light (measured 1.773:1 on white — banned).
- Primary action is an ink-black pill (#151515 fill, white label, full corner radius); one per view, with the five-hue gradient allowed as a 1px ring on marketing only.
- Five-hue signature gradient at 85 degrees — 01d7e4 0%, f3c306 25%, f37a03 50%, f43531 74%, f00e5c 100% — appears as thin stripe, blurred ambient glow, or gradient ring; it never becomes a fill for cards, tables or chrome.
- Depth is 1px hairlines (#e5e5e5 light, white at 10% alpha dark) plus surface steps in dark; shadows are capped at a single 0 1px 2px rgba(0,0,0,0.04) in light and forbidden in dark.
- Corner system: 6px inputs, 8px buttons/rows, 12px cards, 16px overlay panels, full-radius pills and badges; nothing between 16 and full.
- Type: Sora (variable 100–800) for display/headings only; Inter (variable 100–900) for body and UI; a system mono stack for commands, identifiers, slugs and dense data headers.
- Eyebrow labels are 12–13px uppercase with 0.08–0.12em tracking, often mono-flavoured, always paired with a small icon or hue dot.
- Numbers are tabular everywhere they compare: usage tiles, invoices, chart legends, table cells; right-aligned, never centred.
- Status badges are tinted washes with dark same-hue text and a leading dot glyph — colour never carries the message alone.
- Marketing rhythm: 96px section bands, 1200–1280px content measure, alternating 2-column text/code layouts and full-bleed texture bands; console rhythm: 275px sidebar, 24px region gaps, 48–72px table rows.
- Dark mode is authored, not inverted: own charcoal ramp (0a0a0a canvas, 171717 cards, 1e1e1e/262626 raised), white-alpha borders, zero shadows.
- Imagery is product UI, code panels and soft-focus nature stills tinted with the stripe's light-leak; never stock photos of people.
- Scroll-driven pinned scenes exist on marketing; every one ships a static fallback under reduced-motion preference.
- The paper/noise texture (roughly 2–4% luminance variance) is a canvas treatment in both modes, never applied to cards or text containers.

## 2. Token Architecture

Three layers. A component consumes **semantic** tokens only; a semantic token resolves to a **primitive**; nothing skips a layer. (House rule: this taxonomy is the skill's, not a web standard; token names here are case-sensitive and contain no `$`, `{`, `}` or `.` characters — they are written with dots for readability.)

- **L1 Primitive** — literal values named by value: `palette.ink.900`, `palette.cyan.400`, `space.4`, `radius.lg`. Referenced only by L2. Banned: component-named primitives (no `card.background` at this layer — one value, many roles).
- **L2 Semantic** — role names: `surface.canvas`, `text.primary`, `accent.action`, `status.error.wash`. The only layer a component may consume. Every semantic role carries a value in **both** shipped modes; a role without a dark value would resolve to its light value and fail contrast, so none exist.
- **L3 Component** — only for deliberate deviation (e.g. `announcement.banner.fill`), pointing at L2 or L1, never at a raw value, never at a sibling component's token.

**Rules.** Every token has a determinable type (colour, dimension, number, font-family, duration) or it is invalid. No circular references; a cycle is a build error, not a runtime fallback. Animatable custom properties are registered with both a syntax descriptor and an inheritance flag — missing either invalidates the registration, and the initial value must be computationally independent (no percentage or font-relative units). Layer order, low to high: reset, primitives, semantic, components, utilities. Cascade layer order beats selector specificity entirely, and an unlayered normal declaration outranks every layered one — so anything a consumer must override without forcing importance sits in the top layer, and no stray unlayered rule may ship inside a component file.

**Primitive palette (L1, value-named):**

| Step | Value | Step | Value |
|---|---|---|---|
| ink.900 | #151515 | cyan.400 | #01d7e4 |
| ink.600 | #646567 | cyan.600 | #00bbcb |
| ink.500 | #767676 | amber.500 | #f3c306 |
| ink.400 | #a1a1a1 | amber.700 | #eaa700 |
| ink.300 | #b3b3b3 | orange.500 | #f37a03 |
| ink.200 | #8c8c8c | red.500 | #f43531 |
| paper.50 | #ffffff | magenta.500 | #f00e5c |
| paper.100 | #faf9f7 | magenta.600 | #d02344 |
| paper.200 | #f5f5f5 | magenta.400 | #ff6568 |
| paper.300 | #ededed | green.500 | #00c758 |
| paper.400 | #e5e5e5 | amber.600 | #f99c00 |
| night.950 | #0a0a0a | blue.600 | #1d4fd8 |
| night.900 | #171717 | blue.400 | #8ab4ff |
| night.850 | #1e1e1e | stone.500 | #f7f6f4 |
| night.800 | #262626 | steel.600 | #565656 |

## 3. Colour Roles

| Role | Light | Dark | Notes |
|---|---|---|---|
| `surface.canvas` / `raised` / `overlay` / `inset` | #ffffff / #ffffff / #ffffff / #f5f5f5 | #0a0a0a / #171717 / #1e1e1e / #262626 | canvas · cards · overlays · wells; light canvas carries the paper texture; marketing hero band reads #faf9f7 |
| `surface.hover` / `surface.selected` | #f5f5f5 / #ededed | #262626 / #1e1e1e | Interaction fills; selected console nav item is a raised pill |
| `border.subtle` / `strong` / `focus` | #e5e5e5 / #646567 / #151515 | white 10% / #8c8c8c / #01d7e4 | subtle is decorative (1.260:1 — never a sole boundary); strong carries the 3:1 duty; focus pairs cyan inner ring with ink outer ring on light |
| `accent.action` / `onAction` / `signal` / `subtle` | #151515 / #ffffff / #01d7e4 / #f5f5f5 | #01d7e4 / #151515 / #01d7e4 / #262626 | action = the one filled pill per view; signal = focus, live dots, chart series, links-on-dark; subtle = pressed track |
| `text.primary` / `secondary` / `tertiary` / `disabled` | #151515 / #646567 / #767676 / #b3b3b3 | #fafafa / #a1a1a1 / #a1a1a1 / #565656 | ink ramp; tertiary floors at 4.542:1 by house rule though WCAG exempts inactive UI |
| `status.success` / `warning` / `error` / `info` | #116b3f on #e7f6ee / #8a5a00 on #fdf2d9 / #b3223f on #fdeef0 / #1d4fd8 on #e8eefc | #00c758 on #0c2118 / #f99c00 on #241a09 / #ff6568 on #2a1214 / #8ab4ff on #0e1a2b | rendered as wash pill + leading dot + word; glyph colours: green.500 / amber.600 / magenta.500 / blue.600 |

Dark canvas is **not** pure black: the ramp runs #0a0a0a (canvas) → #171717 (card) → #1e1e1e (overlay) → #262626 (inset/hover). Depth in dark comes from these surface steps and 1px white-alpha strokes, never shadows.

**Contrast gate — computed, not asserted; ratios are exact to three decimals. Body ≥4.5:1; UI boundaries and focus ≥3:1.**

| Gate row | Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|---|
| text.primary on canvas (light) | text.primary | #151515 | surface.canvas | #ffffff | 18.261:1 | 4.5:1 | pass |
| text.secondary on canvas (light) | text.secondary | #646567 | surface.canvas | #ffffff | 5.835:1 | 4.5:1 | pass |
| text.tertiary on canvas (light) | text.tertiary | #767676 | surface.canvas | #ffffff | 4.542:1 | 4.5:1 | pass |
| onAction on ink pill (light) | accent.onAction | #ffffff | accent.action | #151515 | 18.261:1 | 4.5:1 | pass |
| onAction on cyan signal fill (light) | text.primary | #151515 | accent.signal | #01d7e4 | 10.297:1 | 4.5:1 | pass |
| onAction on amber signal fill (light) | text.primary | #151515 | palette amber.500 | #f3c306 | 10.974:1 | 4.5:1 | pass |
| border.strong on raised (light) | border.strong | #646567 | surface.raised | #ffffff | 5.835:1 | 3:1 | pass |
| status.success text on wash (light) | status.success | #116b3f | wash | #e7f6ee | 5.882:1 | 4.5:1 | pass |
| status.warning text on wash (light) | status.warning | #8a5a00 | wash | #fdf2d9 | 5.328:1 | 4.5:1 | pass |
| status.error text on wash (light) | status.error | #b3223f | wash | #fdeef0 | 5.801:1 | 4.5:1 | pass |
| status.info text on wash (light) | status.info | #1d4fd8 | wash | #e8eefc | 5.713:1 | 4.5:1 | pass |
| text.primary on canvas (dark) | text.primary | #fafafa | surface.canvas | #0a0a0a | 18.968:1 | 4.5:1 | pass |
| text.secondary on canvas (dark) | text.secondary | #a1a1a1 | surface.canvas | #0a0a0a | 7.663:1 | 4.5:1 | pass |
| text.secondary on card (dark) | text.secondary | #a1a1a1 | surface.raised | #171717 | 6.939:1 | 4.5:1 | pass |
| accent.signal as text (dark) | accent.signal | #01d7e4 | surface.canvas | #0a0a0a | 11.164:1 | 4.5:1 | pass |
| border.strong on raised (dark) | border.strong | #8c8c8c | surface.raised | #171717 | 5.331:1 | 3:1 | pass |
| status.success on wash (dark) | status.success | #00c758 | wash | #0c2118 | 7.470:1 | 4.5:1 | pass |
| status.warning on wash (dark) | status.warning | #f99c00 | wash | #241a09 | 7.975:1 | 4.5:1 | pass |
| status.error on wash (dark) | status.error | #ff6568 | wash | #2a1214 | 6.120:1 | 4.5:1 | pass |
| status.info on wash (dark) | status.info | #8ab4ff | wash | #0e1a2b | 8.368:1 | 4.5:1 | pass |

Documented failures by design: `accent.signal` cyan as text on light = 1.773:1 (banned — cyan is fill/ring/series only on light); `border.subtle` on canvas = 1.260:1 (decorative hairline; a real boundary always gets `border.strong`); disabled text #b3b3b3 on #f5f5f5 = 1.923:1 and #565656 on #171717 = 2.443:1 (WCAG exempts inactive components; a disabled control states its reason on focus or hover).

## 4. Typography

**Families.** UI and body: **Inter**, self-hosted variable (100–900), preloaded, falling back to the system sans stack. Display and headings: **Sora**, self-hosted variable (100–800), heading-role only, falling back to an Arial-metric-adjusted clone. Numeric and code: system mono stack (ui-monospace, SFMono-Regular, Menlo, Consolas) for identifiers, hashes, timestamps, CLI commands, project slugs and dense data headers. Monospace is for identifiers and code, never a costume — marketing eyebrows may track uppercase Inter instead.

**One ramp per density class, not a blended table.**

**[F] Focused — auth, onboarding, project setup — 16px base**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Display | 40px | Sora 600 | 1.15 | −0.01em | — | "Welcome back", "Set up your project" |
| Heading | 24px | Sora 600 | 1.25 | 0 | — | Card and step headings |
| Body | 16px | Inter 400 | 1.5 | 0 | — | Explanatory copy, ≤72ch |
| Label | 14px | Inter 500 | 1.4 | 0 | — | Field labels |
| Helper | 13px | Inter 400 | 1.45 | 0 | — | Constraint hints below fields |
| Value | 16px | Inter 400 | 1.4 | 0 | tabular | Form values, mono for slugs |

**[S] Standard — marketing pages, docs landing, console dashboard — 15–16px base**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Page title | 40px | Sora 600 | 1.15 | −0.01em | — | Console page headings, pricing headline (56–64px on marketing hero, same family) |
| Section title | 24px | Sora 600 | 1.25 | 0 | — | Card groups, table sections |
| Body | 16px | Inter 400 | 1.5 | 0 | — | Marketing paragraphs, docs lead, 65–80ch |
| Row primary | 14px | Inter 500 | 1.4 | 0 | — | Table first cell, list titles |
| Row secondary | 13px | Inter 400 | 1.4 | 0 | tabular | Host names, dates, sub-values |
| Stat value | 28px | Sora 600 | 1.1 | 0 | tabular | Usage tiles ("54") |
| Stat label | 12px | Inter 600 | 1.3 | 0.08em uppercase | — | REQUESTS, TOTAL REQUESTS |
| Meta | 12px | Inter 400 | 1.35 | 0 | tabular | Timestamps, "2 minutes ago" |

**[D] Dense — usage analytics, audit log, changelog, query insights — 13px base**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| Grid header | 12px | Inter 600 or mono 500 | 1.3 | 0.08em uppercase | — | AGENT, SPONSOR, ACCESS, STATUS, LAST ACTIVE |
| Grid cell numeric | 13px | Inter 400 | 1.35 | 0 | tabular | Requests, GiB-hours, MiB — right-aligned |
| Grid cell text | 13px | Inter 400 | 1.35 | 0 | — | Policy names, regions |
| Log line | 13px | mono 400 | 1.45 | 0 | tabular | POST paths, CLI commands |
| Inline help | 12px | Inter 400 | 1.4 | 0 | — | "Lowercase letters, numbers, and dashes" |

Prose inside a dense screen still steps up to the [S] body role. Invariants: tabular numerals on every comparable value (currency, timestamps, deltas, counts, IDs); right-align numerics, left-align text, never centre a numeric column; fixed stepped sizes, no fluid interpolation; measure ≤80 characters (65–80ch for F/S, unconstrained inside data grids).

## 5. Spacing Scale & Density Scales

**Spacing base: 4px grid; 8px comfortable in F/S, 4px in D.** `space.0` 0 · `1` 4px icon-to-label · `2` 8px control padding [D] · `3` 12px cell padding [S] · `4` 16px card padding [S] / page gutter (24px marketing) · `6` 24px card padding [F] + console region gap · `8` 32px section gap [S] · `12` 48px region separation · `16` 64px rarely · `24` 96px marketing section band. No 17px, no 23px; an off-scale value means the layout is wrong.

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 24px | 32px | Login, sign-up, onboarding, project setup |
| `standard` | 48px single-line / 72px two-line | 15–16px | 12–16px | 24px | Marketing, docs, console dashboard, billing |
| `dense` | 32px | 13px | 8px | 16px | Usage analytics, audit log, changelog, query insights |

- Density comes from row height, column pruning and leading — never from type too small to read. A 13px tabular numeral in a dense grid is correct; the same numeral in a focused form is a defect.
- Never switch density mid-page. Switching across routes with different jobs is legitimate and should feel like a different room.
- Chrome follows rows: header, toolbar, batch bar and pagination heights match the table's row height (48px toolbar over 48px rows).
- Whitespace budget: Focused 55–70% · Standard 40–55% · Dense 25–40% (house heuristic, validated against the captured screens).

## 6. Radius Scale

`none` 0 · `sm` 6px inputs, dense cells, code pills · `md` 8px buttons, rows, badges on tables, menu items · `lg` 12px cards, pricing plans, console panels · `xl` 16px overlay panels, auth card, large marketing media frames · `full` 9999px pills (primary CTA, announcement chip, avatars, status dots, search bar). One radius per component family, never mixed ad-hoc. Nested radii obey `radius_inner = radius_outer − padding` (a 12px card holding an 8px button keeps ≥4px padding between them).

## 7. Elevation

**One strategy per mode, never mixed.** Light: hairline border plus at most one soft ambient shadow. Dark: surface-luminance steps plus 1px keylines, zero shadows — a drop shadow is invisible on near-black.

- **Level 0 — canvas:** no shadow, both modes.
- **Level 1 — card/panel:** 1px `border.subtle` + optional rgba(0,0,0,0.04) 0 1px 2px (light only); dark: one surface step up + keyline.
- **Level 2 — sticky header/toolbar:** rgba(0,0,0,0.06) 0 1px 2px + `border.subtle` (light); dark: #1e1e1e + `border.strong`.
- **Level 3 — overlay (dropdown, command palette):** rgba(0,0,0,0.10) 0 4px 16px, `radius.lg` (light); dark: #1e1e1e + `border.strong`.
- **Level 4 — dialog:** rgba(0,0,0,0.14) 0 8px 32px + scrim rgba(0,0,0,0.4) (light); dark: #262626 + scrim rgba(0,0,0,0.6).

The 0 1px 2px at 4% black observed on the marketing nav is the ceiling for chrome; nothing ships heavier except overlays.

## 8. Motion

`instant` 0ms · `fast` 120ms ease-out (exits in D) · `base` 180ms decelerate (D entrances, hover fills, colour transitions) · `slow` 240–300ms decelerate (F/S entrances, dialogs, drawer).

- Entrances decelerate, exits accelerate; symmetric ease-in-out on both directions is a defect.
- Animate transform and opacity only — never width, height, top, left.
- No bounce on irreversible moments: not on the revoke-agent confirm, not on plan downgrades.
- Marketing pins and scrolls large textured scenes; under reduced-motion preference every pinned scene renders as its static end-state and blurs crossfade under ~150ms — scaling and panning of large objects are exactly what must be neutralised.
- Reduced motion is a real variant, not an animation kill-switch: movement becomes crossfade, spinners become indeterminate bars.

## 9. Imagery & Art Direction

Policy, not asset list.

- **Brand moment:** the diagonal five-hue stripe (cyan → amber → orange → red → magenta, 85 degrees) and its blurred ambient-glow derivative. It is the single expressive device: a hard ribbon across hero bands, a gradient ring on the primary pill, a glow bleeding behind dark panels. Its palette never leaks into UI tokens — it appears in the token layers only as the data-series ramp, where the same five hues are the chart's categorical order (cyan first = primary series, then amber, magenta).
- **Iconography:** 16–20px line icons, 1.5px strokes on a 24px grid, geometric with rounded terminals — matched to Inter's tone; filled variants only where a stroke cannot carry 16px. Icon-only controls always carry a tooltip label.
- **Photography:** soft-focus nature stills (foggy meadows, pine forests) tinted with the stripe's light-leak, used full-bleed behind marketing sections only. None inside the product. Third-party logos render full-colour on the neutral paper band of the homepage strip, never on coloured fills, and monochrome everywhere else.
- **Illustration / 3D:** one 3D family — glassy prismatic renders of database cylinders and stacked modules wrapped by the stripe — used on marketing cards; no 3D in the console.
- **Code as imagery:** terminal panels, CLI command pills with copy affordances, and schema fragments are first-class marketing imagery, framed in `radius.lg` panels with `surface.inset` fills.
- **Empty / error art:** none — empty states are typographic ("How would you like to start?" plus two path cards); recovery CTAs are never replaced by illustration.

## 10. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| App shell/sidebar | S | light, dark; workspace + project sections | current item as raised pill; collapsed labels; disabled items explain on hover | arrow navigation, tab order top-down | WORKSPACE / PROJECT section eyebrows |
| Data table (agents) | S/D | single- and two-line rows | hover fill, selected, loading skeleton rows, empty with CTA | arrow keys, enter opens, esc closes | AGENT · SPONSOR · ACCESS · STATUS · LAST ACTIVE |
| Filter/search bar | S | nav search pill, command palette trigger | focused ring, loading, no-results with suggestion | Cmd/Ctrl K opens, esc closes | "Search…" |
| Row action menu | S/D | inline overflow | focus-trapped, esc closes, disabled items state why | arrows + enter | "Review" |
| Stat tile | S/D | with/without sparkline | loading shimmer matching final geometry, stale-data note | tabbable, value announced | "Requests", "Provisioned memory" |
| Drawer/inspector | S | right sheet, full-height | open, scrim, esc, focus-trap | esc closes, focus returns | "Review" |
| Dialog | F/S | confirm, form | scrim, focus-trap, esc, submitting | esc cancels, enter submits | "Enroll agent" |
| Plan/seat control | S | pricing card, billing row | current plan, upgrading, downgrading blocked | radio semantics | "$10 /month", "Spend limits" |
| Member row | S | avatar + email + role | removing (confirm), role changing | row menu | role name is the value, not a placeholder |
| Audit entry | D | actor + action + target + time | expanded detail, filtered | enter expands | "wants to create a database" |
| Command palette | S | search + recent | loading, empty, no-results | Cmd/Ctrl K, arrows, enter | "Search…" |
| Onboarding path card | F | recommended, alternative | hover lift, selected, loading | enter selects | "Connect a GitHub repo", RECOMMENDED tag |
| CLI command snippet | S/D | one-line, multi-line | copied confirmation (width-stable), wrapped | tab to copy | "$ npx prisma deploy module.ts" |
| Status badge | S/D | active, paused, revoked, free, recommended | static (read-only by nature) | — | ACTIVE · PAUSED · REVOKED |
| Announcement banner | S | full-width gradient band | dismissible, link out | esc dismisses | "Read the docs →" |
| Doc link card | S | gradient panel tile | hover border lift, focus ring | enter follows | "docs →" |

**Every fetching surface also designs:** loading (skeleton matching final geometry — never a centred spinner on a blank page), empty (what is missing plus the CTA that fixes it — the get-started screen is the canonical empty state), error (what happened plus how to recover), offline/stale (what is known vs cached, with the stale timestamp in `text.tertiary`).

**Contracts this table encodes:** one primary filled CTA per view in F/S (dense toolbars may run a primary plus icon actions); every icon-only control carries a label or tooltip; a disabled control states why on focus or hover rather than sitting silently dead; a button never changes width between idle and loading — reserve the space.

## 11. Light / Dark Strategy

- **Posture: C dual-parity.** Marketing, docs articles and the console dashboard are light-first; usage analytics, project setup, the docs landing and auth are authored dark-first. Both modes ship for every role — no role exists in only one mode.
- **Mechanism:** semantic roles remapped per mode at the app root; nothing is inverted at render time. Dark is authored: its own charcoal ramp, its own border strengths (white 10% subtle, #8c8c8c strong — a delicate white hairline would vanish on charcoal), its own shadow policy (none).
- **Root scheme attribute** is set so UA chrome, form controls and scrollbars follow the active mode; the scheme meta tag ships in the head before any stylesheet to prevent a flash of the wrong scheme.
- Single-mode decorative treatments: the paper texture is a light-canvas property; dark uses a fine noise grain instead. Neither carries information.
- The five-hue stripe reads on both canvases; on light it stays thin and hard-edged, on dark it glows.
- No org-tinted variant ships; if one ever does, only colour tokens may change — radii, type sizes and layout freeze so a theme swap cannot move anything.

## 12. Density-Mode Strategy

- **Default per surface class:** F for auth/onboarding; S for marketing, docs and the console shell; D for usage, audit, changelog and query insights. The boundary is the job: reading/editing gets S, monitoring gets D.
- **Mechanism:** a density marker on the app root rescales row height, cell padding, gutter and base body size together as a token axis, not a media query; spacing tokens themselves keep their values.
- **Container queries** drive reflow so components respond to their container, not the viewport; size queries fail closed with no eligible container, and container-relative units silently fall back to small-viewport units there — they are never used where that fallback would be wrong.
- Style queries compare computed values, so the density marker must be a registered custom property.
- **The switch is offered as an accessibility affordance**, not a preference: a density control honours users with visual field loss, per WCAG's note on target size.

## 13. Accessibility Commitments

- **Target: WCAG 2.2 AA** minimum; AAA for contrast on body text in reading surfaces (docs articles).
- **Target size:** ≥24×24 CSS px minimum, 44×44 design target for primary controls in F/S; zoom does not excuse it.
- **Keyboard:** every function operable; focus indicator always visible — on light a 2px ink ring with a cyan inner accent, on dark a 2px cyan ring (11.164:1); the focused item is never fully hidden behind a sticky header or persistent overlay.
- **Contrast:** text ≥4.5:1 (gate in §3); UI boundaries ≥3:1 via `border.strong`; every status pairs colour with a dot glyph and a word; chart deltas carry sign or direction.
- **Motion:** the §8 reduced-motion variant per component, including static fallbacks for pinned marketing scenes.
- **Text:** ≤80-character measure, 1.5 leading on body, 200% resize without horizontal scroll.
- **Semantics:** real buttons, links and inputs; correct roles; headings matching visual rank; polite live regions for usage refreshes and deploy progress; busy state on loading regions.
- **Contrast preference:** if the user asks for more contrast, borders step from `border.subtle` to `border.strong` globally and `text.tertiary` promotes to `text.secondary`.

## 14. Anti-Patterns

**Do**
- Use the ink-black pill as the only filled CTA on a light surface; it is the system's strongest signal and the gradient ring is its one ornament.
- Confine cyan to focus rings, live dots, links-on-dark and the first chart series — it earns attention precisely because it is rare.
- Keep the five-hue gradient thin (≤8px ribbon or blurred glow); its power is linear, not areal.
- Set stat labels 12px uppercase with 0.08em tracking above tabular values — the pairing is the data-surface signature.
- Separate regions with 1px hairlines and surface steps; reach for shadow only on overlays.
- Pair every status colour with a dot and a word; the badge must survive a greyscale screenshot.
- Render code as imagery — CLI pills, terminal panels, schema fragments — on marketing as in docs.
- Give every pinned marketing scene a static reduced-motion end-state, authored, not auto-generated.
- Keep marketing and console geometry identical (10px corner system, 4px grid) so the dark surfaces feel like the same product at night.
- Reserve the paper texture for canvases; cards stay flat clean fills.
- Use the mono stack for identifiers, commands and dense headers — and Inter for everything a human reads as prose.
- Right-align every numeric column and let header heights match row heights.

**Don't**
- Don't set cyan text on light backgrounds — 1.773:1; it fails everywhere it can be measured.
- Don't reuse the legacy single-accent teal #14b8a6 or the navy-and-green palette in new surfaces; they describe the pre-2026 brand and survive only in legacy flows and old previews.
- Don't fill cards, tables, toolbars or chrome with the signature gradient; it is a stripe, a ring, or a glow — never a surface fill.
- Don't ship a second chromatic accent beyond the five-hue system; purple and teal-adjacent greens break the prism's order.
- Don't centre numeric columns or use proportional figures in comparable data; tabular or nothing.
- Don't use placeholder text as a label; the console's helper lines sit below labelled fields, never instead of them.
- Don't drop shadows in dark mode; a shadow on #0a0a0a is decoration pretending to be depth.
- Don't exceed one filled CTA per view; "Get started" and "Contact us" competing on one screen is a defect.
- Don't paste stock photography of people into product surfaces; the only humans in the system are 32px avatars with initials fallbacks.
- Don't use whole-page spinners; skeletons match final geometry or they lie.
- Don't shrink type below 12px to fit density; prune columns instead.
- Don't let a disabled primary button sit mute; it states its reason or it is a bug.

## 15. Quick Reference & Verification Gate

**Colour (role → light / dark):** surface.canvas #ffffff / #0a0a0a · surface.raised #ffffff / #171717 · surface.overlay #ffffff / #1e1e1e · surface.inset #f5f5f5 / #262626 · surface.hover #f5f5f5 / #262626 · surface.selected #ededed / #1e1e1e · border.subtle #e5e5e5 / white 10% · border.strong #646567 / #8c8c8c · border.focus #151515 / #01d7e4 · accent.action #151515 / #01d7e4 · accent.onAction #ffffff / #151515 · accent.signal #01d7e4 / #01d7e4 · text.primary #151515 / #fafafa · text.secondary #646567 / #a1a1a1 · text.tertiary #767676 / #a1a1a1 · text.disabled #b3b3b3 / #565656 · status.success #116b3f on #e7f6ee / #00c758 on #0c2118 · status.warning #8a5a00 on #fdf2d9 / #f99c00 on #241a09 · status.error #b3223f on #fdeef0 / #ff6568 on #2a1214 · status.info #1d4fd8 on #e8eefc / #8ab4ff on #0e1a2b.

**Type ramp (flat):** 64/40/32/24 display+headings Sora 600 · 28 stat value Sora 600 tabular · 16 body Inter 400/1.5 · 15 [S] base · 14 row primary Inter 500 · 13 row secondary, dense cell, helper · 12 stat label uppercase 0.08em, grid header, meta · mono for commands/IDs.

**Spacing + radius (flat):** 4 base · 8/12/16/24/32/48/64/96 steps · radius 6 inputs / 8 buttons / 12 cards / 16 overlays / full pills.

**Component → token map:** primary pill → accent.action + accent.onAction, radius full, space.2/3 padding · card → surface.raised + border.subtle, radius lg, space.4 padding · table row → surface.raised + surface.hover, radius md, height = density row · stat tile → surface.raised, text.primary value, text.secondary label at Stat-label role · status badge → status.*.wash + status.*.text, radius full, dot glyph · code pill → surface.inset + border.subtle, mono · focus ring → border.focus, 2px + 2px offset · command palette → surface.overlay + border.strong, radius lg, level 3.

**Agent prompt block (verbatim-consumable).** Role→hex: canvas #ffffff (dark #0a0a0a); card #ffffff (dark #171717); ink #151515; body-grey #646567; muted #767676; hairline #e5e5e5; strong border #646567; action fill #151515 with #ffffff label (dark: cyan #01d7e4 fill with #151515 label); signal cyan #01d7e4 — never text on light; success #116b3f on #e7f6ee; warning #8a5a00 on #fdf2d9; error #b3223f on #fdeef0; info #1d4fd8 on #e8eefc. Ramp: Sora 600 headings (64/40/24), Inter body 16/1.5, rows 14/13, stat labels 12 uppercase 0.08em, mono for code. Spacing 4-base (8/12/16/24/32/48/96); radius 6/8/12/16/full. Density: focused 16px, standard 48–72px rows, dense 32px rows 13px.

**Example component prompts.**
1. *Console dashboard page (Agents)* — surface.canvas background with paper texture; 275px sidebar in surface.raised, current item as surface.selected pill, section eyebrows in text.secondary at Stat-label role; page title in text.primary at Page title role; one accent.action pill "Enroll agent" top-right; table rows 72px two-line, Grid header role uppercase, STATUS as status badge (success/paused-neutral/error washes), Row secondary in mono for hosts; hover fill surface.hover; focus ring border.focus; no shadow above level 1.
2. *Usage analytics screen (dark, dense)* — surface.canvas #0a0a0a, stat tiles in surface.raised with Stat value tabular in text.primary and Stat label uppercase in text.secondary; line chart series in accent.signal cyan first, amber.500 second, magenta.500 third, 2px strokes, dotted baseline grid in border.subtle; legend dots match series order; zero shadows, all depth via surface steps; log lines in mono at Log-line role; loading = shimmer skeletons matching tile geometry.
3. *Marketing hero band (light)* — surface.canvas with paper texture; eyebrow at Stat-label role with signal-cyan dot; display headline in text.primary, Sora, 64px, −0.01em; body line in text.secondary 18px; one accent.action pill with the five-hue gradient ring (1px) and one ghost outline pill beside it; brand stripe ribbon ≤8px entering from the edge; trusted-line numbers tabular.

**Pre-ship checklist.** 1 Zero raw hex outside L1. 2 No token resolves to a component name. 3 Every contrast pairing computed, passing, unrounded. 4 Every semantic role has a value in both modes. 5 Every fetching surface has loading/empty/error/offline specified. 6 Every component row lists disabled and loading states. 7 Row, header, toolbar and pagination heights agree. 8 Reduced-motion variant written for every authored motion, including pinned marketing scenes. 9 Every control keyboard-reachable with a visible focus indicator. 10 Dark authored, not filtered, with border strength exceeding light's. 11 No unoverridden stock default inside a committed surface. 12 Nothing came from a marketing page into the console's token layers. 13 The §9 brand-moment palette appears nowhere in the UI token layers except the sanctioned data-series ramp.

## Sources

All accessed 2026-11-01. Values were extracted from production surfaces, not reconstructed from memory.

- **prisma.io homepage, pricing and docs** — live captures in `screens/overview.webp`, `screens/pricing.webp`, `screens/docs.webp`; site CSS chunks supplied the primitive palette (five-hue signature gradient, focus rings, cyan pressed variants), the shadcn-style docs token pairs (canvas/foreground/border/destructive), the 0.625rem base radius and the Inter/Sora font-family declarations with their variable weight ranges.
- **Prisma Console product UI** — shipped screenshots from the official docs repository (served from prisma.io changelog and product paths, archived in `screens/dashboard.webp`, `screens/features.webp`, `screens/product.webp`, `screens/onboarding.webp`): sidebar architecture, agents table, usage analytics tiles, onboarding path cards, status badge styling, mono table headers.
- **console.prisma.io login** — live capture in `screens/auth.webp`: dark textured canvas, Sora display, testimonial cards with hue-coded top borders, rainbow stripe.
- **Open Graph and GitHub social previews** — `screens/og.webp` (current five-hue brand), `screens/gh-preview.webp` (legacy navy/green brand, cited in §1 and §14 as superseded).
- **Sibling spec** — premium-marketing-design `devtools/prisma` DESIGN.md (ladder rung 1): supplied the hairline/hex raw-material vocabulary and the pre-2026 teal reading; superseded values are called out in §1, §3 and §14 rather than silently dropped.
