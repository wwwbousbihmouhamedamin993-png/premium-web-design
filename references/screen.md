# Screen — design + build a new screen or flow

The build playbook. Run it end to end; do not skip to code.

## 1. Load what is true

Run the context script output (PRODUCT.md / DESIGN.md / project constitution), read the project's tokens and shared components, and load 1–3 knowledge files for the domains this screen touches. Note the surface's **mode** (Operate / Read / Decide / Support). An extension of an existing surface inherits that surface's world — do not turn a local addition into an identity exercise.

## 2. Name the usage scene

One sentence: who, where, on what hardware, how often, what competes for attention. A triage queue worked by a support agent on a 1280×720 laptop with two monitors and a Slack window behind the browser — that sentence rules out generous whitespace, big targets, and single-column layouts before any pixel exists. If the scene is genuinely unclear, ask one round of 2–3 questions (task, frequency, viewport/hardware, what "fast" means here). Skip settled facts.

## 3. Declare the density class

Web product surfaces span a density range that mobile never faces. **Declare the class before applying any type or spacing rule** — the boundaries are a design judgement (see `craft-floor.md`), and the rest of the build inherits them.

| Class | Surfaces | Base body | Row height | Measure |
|---|---|---|---|---|
| **Focused** | Auth, onboarding, checkout, single-form flows, settings detail | 16px | — | 60–70ch, centered |
| **Standard** | Project home, card+list feeds, record detail | 14–15px | 40–44px | 65–80ch |
| **Dense** | Data tables, admin consoles, observability, logs, trading, IDE-like | 12–13px | 28–32px | full-width |

One class per surface. A screen that mixes 13px table text with 16px prose side by side without a reason is two surfaces pretending to be one. If the screen has a Focused entry point (a form) and a Dense work area (a table of its results), that is legitimate — but they are two regions with two declared classes, not one drifting scale.

## 4. Write the brief (5–15 lines, show it to the user)

- **Goal:** what problem this screen solves, one sentence.
- **Mode:** Operate / Read / Decide / Support.
- **Density class:** Focused / Standard / Dense, with the boundary that put it there.
- **Emotion:** calm, confident, in-control — what the user should feel.
- **Hierarchy:** what dominates, what supports, what recedes — 3 items max.
- **Full states:** loading / empty / error / offline *for this screen*.
- **Icon:** family + stroke weight.
- **Microcopy:** what the buttons actually say.
- **Accent budget:** where the ≤2 accent uses land.

Get one confirmation. A wrong brief poisons everything downstream; a right one makes the build mechanical.

## 5. Commit a hierarchy

For an extension: inherit the world, decide only the new composition. Done when the new element's typography, spacing, and color inherit from the incumbent screen — verify by visual diff.

For a genuinely new whole screen: derive **5–7 materially different structures** from the usage scene (list-first, table-first, master-detail, panel-over-list, wizard, workspace-with-rail, command-bar-centric…), pick the one that serves the scene best, and explicitly name the category-default arrangement as the one you are refusing. Never split the difference between two structures — a screen that hedges reads as generic. Check `signature-moves.md`: what would the 1–2 posture-fit apps do differently from your first instinct?

## 6. Pick the boundary: route, panel, or modal

Decide this before building, and write the reason into the brief. It is a design judgement, not a sourced rule.

- **Route** — the user has an address for it, can deep-link to it, browser-back means something, and it is durable state. Anything a user will return to tomorrow belongs here.
- **Panel** — a drawer, a side inspector, a split view: context stays visible, the user keeps working beside it, dismissal is cheap. Reflow beats overlap where the layout allows it (see WCAG's focus-not-obscured discussion of a side panel that pushes content rather than covering it) [S9].
- **Modal** — short, focused, interruptive, with a clear exit. A properly constructed modal takes focus on appearance and constrains interaction until dismissed [S9], so it is the *only* boundary that can be trusted to fully interrupt. One modal layer at a time; a modal inside a modal is a failure, not a composition.

Test: if the work is more than ~a few fields, or the user needs to see the underlying rows while working, it is a route or a panel. A modal that a user must dismiss to read what changed is a route wearing a costume. Every overlay must have an Escape path and a visible close affordance, or it is a keyboard trap by another name.

## 7. Design for keyboard reach as a requirement

On a B2B surface this is not an accessibility afterthought; it is a primary input model. Price the keyboard path before drawing.

- **Everything operable by keyboard.** WCAG 2.2 SC 2.1.1 (Level A) requires all functionality to be operable through a keyboard interface without requiring specific timings for individual keystrokes [S4].
- **Focus always visible.** SC 2.4.7 (AA) requires a mode of operation where the keyboard focus indicator is visible, and it must not be time-limited [S6]. Never `outline: none` without a stronger `:focus-visible` replacement.
- **The focused item stays visible.** SC 2.4.11 (AA) requires the focused component not be *entirely* hidden by author-created content [S9]. Sticky headers, sticky footers, and persistent non-modal overlays are the usual offenders. `scroll-padding` is the cited technique for un-obscureing content [S9].
- **Targets meet SC 2.5.8:** at least **24×24 CSS px**, or the spacing exception — a 24px-diameter circle centred on each target's bounding box must not intersect another target or another undersized target's circle [S1]. SC 2.5.5 at **44×44 CSS px** is **AAA**, not AA [S2]; treat 44px as the design target for primary controls in Focused/Standard surfaces and 24px as the hard floor, with Dense icon columns at 24px plus adequate spacing.
- **Focus rings are non-text contrast.** An author-styled focus indicator must meet **3:1** against adjacent colours [S3] — and it must still meet it when a dim overlay sits on top [S9].
- **Plan the tab order and the roving tabindex** for toolbars, menus, grids, and trees. A dense table with 20 focusable cells per row needs one stop per row, not 20. Escape closes the transient layer; arrows move within it.
- **Write the shortcut set** into the brief for Operate surfaces: the two or three actions that must be one keystroke (save, next row, search).

Hover may *reveal*; focus and touch must reach the same content. WCAG is explicit that hover styling is optional and not required to identify the hover state [S3], and the `hover` media feature exists precisely because the primary input may have no hover capability at all (`hover: none`) [S11].

## 8. Build fully committed

- **Greenfield projects without `DESIGN.md`, `DESIGN-[framework].md`, or `PRODUCT.md`:** Stop and run `init` first (`references/init.md`). It captures durable product truth and derives a production-grade `DESIGN.md` and companion `DESIGN-[framework].md` from the reference web design systems before any screen is built. Resume `screen` immediately once all documents exist.
- **`DESIGN.md` & `DESIGN-[framework].md` exist:** Inherit the tokens directly from both documents. Do not invent raw values or deviate from the established palette, type ramp, or component rules.
- **Existing codebases:** Inherit the existing design tokens and shared wrappers. If no `DESIGN.md` exists yet, run `document` to record the incumbent system.

- Tokens only; use the project's shared wrappers/components; restyle stock defaults through the token system — a stock default component inside a committed screen is a lapse.
- **Numbers get numerals.** Any column of figures, currency, timestamps, or deltas sets `font-variant-numeric: tabular-nums` so digits align vertically [S7]; right-align numerics, left-align text. Proportional figures in a numeric column is a defect, not a style choice.
- **States built, not deferred:** skeleton shaped like the real content, empty state with a CTA, error with recovery, offline/stale behaviour.
- **Async status is announced, not just painted.** Status messages that don't move focus — "18 results returned", "Saved", "5 errors on page" — need a role or property so assistive technology presents them without stealing focus (SC 4.1.3, AA) [S8].
- **Dark mode is a real variant,** not an inverted filter: its own surface ramp and border strength, driven by `prefers-color-scheme` [S10] and the `color-scheme` property so native controls and scrollbars follow [S10].
- **Motion asymmetric** (decelerate in, accelerate out); `transform`/`opacity` only; `prefers-reduced-motion: reduce` honoured as a crossfade or instant cut, targeting vestibular triggers specifically — MDN names scaling and panning large objects as the triggers [S12].
- Real-feeling demo data at real lengths (long customer names, two-line titles, decimals, +35% expansion strings, 40-row tables) — author it, don't ship `Lorem`.

## 9. Write the responsive and container-query contract as a brief item

The adaptation behaviour is part of the design, decided here, not discovered during implementation. Container queries let a component respond to *its container* rather than the viewport, so the same component works in a sidebar, a split view, and a full-width page without knowing where it sits [S13]. Declare containment with `container-type: size | inline-size | normal` and query with `@container` [S13].

The brief carries these lines, filled in before build:

- **Containers:** which elements are query containers, and are they named (`container-name`) when more than one exists [S13].
- **Breakpoints:** what changes at each container width — columns dropped, actions moved into an overflow menu, labels truncated, filters collapsed into a popover. Narrow widths drop columns, not type size.
- **Viewport vs. container:** viewport media queries only for page-level reflow; container queries for anything inside a resizable layout (sidebar open/closed, inspector expanded, split drag) [S13].
- **Reflow floor:** content presents without two-dimensional scrolling at **320 CSS px** width (vertical content) or **256 CSS px** height (horizontal content), except for parts that genuinely require 2D layout — data tables, maps, video, presentations, and interfaces that must keep toolbars in view while being manipulated (SC 1.4.10, AA) [S14]. A table gets its own scroll container; the heading, filter bar, and pagination around it still reflow [S14].
- **`cq*` unit fallback:** with no eligible container, container query length units resolve to the small viewport unit for that axis [S13]. Never use them where that substitution would be wrong; give the component a plain fallback first.
- **No sideways page scroll:** overflow lives in a named scroll region with `min-width: 0`, never on `body`.
- **Hover capability:** any hover-revealed affordance has its focus/touch equivalent, and hover styling is gated on `@media (hover: hover)` where it drives layout [S11].

## 10. Render and look

Run `render-loop.md` now — this step is not optional. Minimum passes: default state, one populated state, dark mode, narrow container width, 200% zoom. Critique against `craft-floor.md` (Verify + Refuse) and the brief; fix at the cause; re-render. Two passes minimum, more until a fresh pass finds no floor violation.

On performance, hold the design to the Core Web Vitals thresholds at the 75th percentile, segmented across mobile and desktop: **LCP ≤ 2.5s**, **INP ≤ 200ms**, **CLS ≤ 0.1** [S15]. INP is field-only; use TBT as the lab proxy [S15]. The design-side levers this screen owns: reserve space for every async region so nothing shifts when data lands (a skeleton with the real content's dimensions), explicit `width`/`height` on images and avatars, self-hosted preloaded fonts, and route-level code splitting [S16].

## 11. Finish

- Keyboard walk: complete the screen's primary task without touching the mouse, with the focus ring visible the whole way and never hidden by a sticky layer.
- 320px reflow check on the non-excepted regions [S14].
- Record any durable system decisions in the project's DESIGN.md (rules from `document.md`) — a new density tier or navigation pattern that survived the build becomes a token or component note, not tribal memory.
- Run the mechanical grep list from `critique.md` over the changed files; fix real hits.
- Run the project's analyzer/lint/tests.

**Exit criteria:** brief satisfied, density class declared and applied, boundary chosen and justified, keyboard path complete, floor green in light + dark, states real, render loop converged, project checks clean.

## Not found

- **A normative threshold for "when must this be a route rather than a modal."** WCAG and Core Web Vitals say nothing about route-vs-modal; the boundary ladder in step 6 is design judgement. Settling it with authority would need a dated usability study on overlay abandonment rates versus route depth (Nielsen Norman Group's own overlay research, or a comparable peer-reviewed source) — none was consulted here.
- **A normative minimum text size for Dense product surfaces.** WCAG sets contrast (SC 1.4.3) and resize/reflow (SC 1.4.10, SC 1.4.4) but no floor font size; the 12–13px Dense range is this skill's design judgement, and the project's `DESIGN.md` overrides it.

## Sources

- **[S1]** https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — W3C WAI, WCAG 2.2 Understanding docs (SC 2.5.8 Target Size (Minimum)). Accessed 2026-10-05.
- **[S2]** https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html — W3C WAI, WCAG 2.2 Understanding docs (SC 2.5.5 Target Size (Enhanced), AAA). Accessed 2026-10-05.
- **[S3]** https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — W3C WAI, WCAG 2.2 Understanding docs (SC 1.4.11 Non-text Contrast, includes hover-state and focus-indicator guidance). Accessed 2026-10-05.
- **[S4]** https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html — W3C WAI, WCAG 2.2 Understanding docs (SC 2.1.1 Keyboard, Level A). Accessed 2026-10-05.
- **[S6]** https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html — W3C WAI, WCAG 2.2 Understanding docs (SC 2.4.7 Focus Visible). Accessed 2026-10-05.
- **[S7]** https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric — Mozilla Developer Network (CSS Fonts Module Level 4 reference). Accessed 2026-10-05.
- **[S8]** https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html — W3C WAI, WCAG 2.2 Understanding docs (SC 4.1.3 Status Messages). Accessed 2026-10-05.
- **[S9]** https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html — W3C WAI, WCAG 2.2 Understanding docs (SC 2.4.11 Focus Not Obscured (Minimum); panel/dialog/focus-trap discussion). Accessed 2026-10-05.
- **[S10]** https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme — Mozilla Developer Network (`prefers-color-scheme` media feature, `color-scheme` interaction). Accessed 2026-10-05.
- **[S11]** https://developer.mozilla.org/en-US/docs/Web/CSS/@media/hover — Mozilla Developer Network (`hover` media feature). Accessed 2026-10-05.
- **[S12]** https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion — Mozilla Developer Network (`prefers-reduced-motion` media feature). Accessed 2026-10-05.
- **[S13]** https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries — Mozilla Developer Network (CSS container queries: `container-type`, `@container`, named contexts, `cq*` units and fallback behaviour). Accessed 2026-10-05.
- **[S14]** https://www.w3.org/WAI/WCAG22/Understanding/reflow.html — W3C WAI, WCAG 2.2 Understanding docs (SC 1.4.10 Reflow: 320/256 CSS px, 2D-layout exceptions, scrollable table pattern). Accessed 2026-10-05.
- **[S15]** https://web.dev/articles/vitals — Google / web.dev (Web Vitals: LCP 2.5s, INP 200ms, CLS 0.1, 75th percentile, TBT as lab proxy). Accessed 2026-10-05.
- **[S16]** https://web.dev/articles/css-web-vitals — Google / web.dev (CSS for Web Vitals: reserving image space, font swap shifts, non-composited animations, critical CSS). Accessed 2026-10-05.