# Critique — scored design review

Evaluate a rendered screen or flow. The score is diagnostic; the fixes are the deliverable. Never review from code alone — get pixels first (`render-loop.md`, "Get pixels").

## Procedure

1. **Establish scope.** Target screen/flow, its mode (Operate / Read / Decide / Support), its declared **density class** (Focused / Standard / Dense), the brief and DESIGN.md if they exist, and the knowledge files for its domains.
2. **Walk the real path.** Render and step through it as the user would: default state, populated, dark, narrow container width, 200% zoom. Do the primary task with the keyboard only. Use `critique` passes from `render-loop.md`.
3. **Score the pillars** (0–10 each, weighted to 100):

> The weights below are a design judgement about what breaks B2B product UI most often. They are not sourced; the numeric thresholds they reference are.

| Pillar | Weight | What 10 looks like |
|---|---|---|
| Hierarchy & focus | 12 | Eye lands on the right thing first; one dominant job per view; the primary action obvious in a glance |
| Density & scanability | 14 | One declared class applied consistently; row heights, gutters, and type from a single scale; density from row height and column pruning, never from shrinking type |
| Typography & numerals | 12 | Clear roles and ramp; `tabular-nums` on every comparable figure column; numerics right-aligned, text left; measure and line-height right at the class |
| Layout & container adaptation | 12 | Components respond to their container via `@container`/`container-type`, not only the viewport; 320px reflow on non-excepted regions; no sideways page scroll; `cq*` fallbacks defined |
| States coverage | 12 | Skeleton/empty/error/offline designed; loading/pressed on every control; async status announced via role, not only painted; no dead ends |
| Component consistency | 8 | One radius per family; coherent icon system; shared components reused, no drift; one primary CTA per view |
| Keyboard & focus | 12 | Full task operable by keyboard; visible focus indicator at ≥3:1; focused item never hidden by sticky chrome; roving tabindex in grids and toolbars |
| Color, dark mode & contrast | 8 | Semantic tokens only; body text ≥4.5:1, large text and UI boundaries ≥3:1, no rounding; dark mode a real variant, not an inverted filter |
| Motion & reduced-motion | 4 | Asymmetric easing; one authored moment; `transform`/`opacity` only; `prefers-reduced-motion` honoured as a real variant |
| Copy voice | 3 | Specific, actionable, product's own voice; labels name the action; no filler, no cheerleading, no raw server strings |
| Performance signals | 3 | Reserved space for async regions; explicit image dimensions; route-level code splitting; Core Web Vitals-shaped budgets in place |

4. **Run the slop checklist** below. **3+ checked boxes = rework risk regardless of score.** The full AI-look sign catalog (sign → fix, including the tells this checklist compresses: greeting headlines, `New ✨` badges, gradient logos, fake mock data, pill-everything) lives in `unslop/signs.md`, and the ordered remediation sequence in `unslop/remediation.md`.
5. **Deliver:** score, band, and the **top 5 material fixes** ordered by impact, each tied to the brief or a pillar. Vague findings ("improve spacing") are not findings — name the element, the value, and the fix.

**Bands:** ≥ 85 ship-ready · 70–84 one polish pass · < 70 rework.

## Slop detector checklist

Flag any that are true:

**Density & numerals**
- [ ] Two density classes mixed on one surface with no declared boundary (12px table text beside 16px prose)
- [ ] Body type below 14px [F]/[S] with no data justification, or help text shrunk as a density strategy
- [ ] Proportional figures (`proportional-nums` or no `font-variant-numeric`) in a numeric column — digits fail to align vertically [S1]
- [ ] Centred numeric column, or currency/timestamps left-aligned ragged
- [ ] Row heights drifting (28 / 32 / 40px in one table) instead of one scale
- [ ] Column that nobody reads or sorts by, kept and narrowed instead of removed
- [ ] Density achieved by shrinking type rather than by row height, column pruning, and tight leading

**Keyboard & focus**
- [ ] Any action reachable only by pointer, or a `<div>`/`<span>` acting as a control without roles, tabindex, and key handlers
- [ ] `outline: none` with no `:focus-visible` replacement
- [ ] Focus indicator below 3:1 against adjacent colours, or dropping below it under a dim overlay [S2]
- [ ] Sticky header/footer or persistent overlay fully hiding the focused item [S3]
- [ ] No roving tabindex in a grid, toolbar, or tree — every cell a tab stop
- [ ] Overlay with no Escape path or no visible close affordance
- [ ] Hover-only disclosure, submenu, or action with no focus/touch equivalent
- [ ] `alert()`/`confirm()`, or a toast carrying an error that needs a decision

**Target size**
- [ ] Pointer target under 24×24 CSS px with no qualifying spacing (a 24px circle centred on each bounding box must not intersect another target or another undersized target's circle) [S4]
- [ ] Row of 20px-tall buttons stacked with a 1px gap — circles intersect [S4]
- [ ] Dropdown or menu items under 24px tall [S4]
- [ ] Primary action under 44×44 CSS px in a Focused/Standard surface — the AAA target, not the AA floor [S5]

**Layout & responsive**
- [ ] Component sized by viewport media queries while living inside a resizable sidebar, inspector, or split view [S6]
- [ ] No `container-type` on a container that actually needs to be queried [S6]
- [ ] `cq*` units used with no fallback, relying on the small-viewport substitution [S6]
- [ ] Horizontal page scroll instead of a named scroll region with `min-width: 0`
- [ ] Non-excepted content forcing two-dimensional scrolling at 320 CSS px width / 256 CSS px height — data tables, maps, video, and toolbar-bound editors are excepted; the heading, filters, and pagination around them are not [S7]
- [ ] Media or image without reserved dimensions or `aspect-ratio`, shifting layout on load [S8]
- [ ] Off-canvas value ~80 characters with no max measure [F/S]

**Color & dark mode**
- [ ] Raw hex or `rgb()` literal in component code (token bypass)
- [ ] Body text under 4.5:1, or large text / UI boundaries under 3:1 — computed ratios not rounded, so 4.499:1 fails [S9]
- [ ] Dark canvas at pure black, or depth carried by drop shadows on a dark surface
- [ ] Dark mode implemented as an inversion of light tokens — no separate surface ramp or border strength
- [ ] Drop shadow on a dark-mode surface; glow or blur used as elevation; ungrounded omnidirectional shadow (`0 0 24px rgba(...)` with `0` Y-offset) instead of dual-layer directional elevation
- [ ] More than 2 font families, icons mixing outline/filled with mismatched stroke weight, or hallucinated inline `<svg><path d="..."/></svg>` geometry instead of canonical icon-library imports
- [ ] Status carried by colour alone, with no icon, label, or shape

**States & data**
- [ ] Centred spinner on an otherwise blank region during fetch
- [ ] Empty state with no explanation of the shape and no CTA
- [ ] Raw error string or stack trace shown to the user
- [ ] Async status ("18 results returned", "Saved", "5 errors on page") painted but not exposed via a role or live region [S10]
- [ ] Button with no loading or pressed feedback; button that changes width between idle and loading
- [ ] Long list rendered whole past a few hundred rows without virtualisation, or an unbounded scroll with no floor
- [ ] Toggle without immediate visual state change; toggles and checkboxes mixed in one group

**Structure & navigation**
- [ ] Route doing more than 2 major jobs; cards nested 2–3 deep
- [ ] Modal used for what should be a route or a panel — more than a few fields, or the user needs the rows behind it
- [ ] Modal inside a modal; a settings dialog holding dozens of controls
- [ ] Two primary (filled) CTAs visible at once
- [ ] Icon-only buttons with no tooltip; a toolbar of a dozen unlabelled icons with no overflow menu
- [ ] Nav item count arbitrarily capped, or >3 clicks to reach a real route from the nav root
- [ ] Deep link landing on app home instead of the target content; breadcrumb disagreeing with browser back
- [ ] Unbounded user-generated collections sitting in shell navigation

**Marketing aesthetics inside the product**
- [ ] Gradient text, radial glow background, glassmorphism across content cards, purple/cyan AI palette
- [ ] Glowing accents or hero-metric treatment imported from a landing page
- [ ] Public marketing pattern (hero + 3-up feature cards + testimonial row) pasted into a product route
- [ ] Card → card → card nesting; five boxes around one paragraph; an icon in a rounded tile above every heading
- [ ] Four identical KPI tiles in a row carrying equal weight — one dominant metric per view, the rest support it
- [ ] Fluid `clamp()` type on a product surface

**Copy & misc**
- [ ] Placeholder-as-label (no persistent field label)
- [ ] Button copy that's a bare verb ("Submit", "OK", "Done") instead of naming the action
- [ ] String concatenation or hardcoded literals in UI code; no ICU plurals; raw dates/numbers instead of locale formatters
- [ ] Layout that clips at +35% string expansion; no overflow strategy on table cells
- [ ] A disabled primary button as the only affordance, with no explanation of why
- [ ] Symmetric easing on both enter and exit; spring/morph treatment on more than 2–3 moments per view
- [ ] `prefers-reduced-motion` handled as `animation: none` everywhere rather than a real variant [S11]

## Mechanical (grep) checks

Run against the changed code; each hit is a lead, not a verdict:

- **Slop sweep (unslop):** `python <skill-base-dir>/scripts/unslop_grep.py <changed paths>` — the mechanical first pass over the AI-look signs (`unslop/signs.md`): purposeless loops, gradient text, purple-family gradients, glows, ungrounded `0 0` shadows, hallucinated inline SVG paths, blobs, tracked-uppercase labels, heavy heading weights, pill radii, emoji decoration, hype words, greeting headlines, unverified claims, fake data. Exit 1 = findings.

- Raw hex / `rgb(` / `hsl(` literals in component files (token bypass)
- Ungrounded omnidirectional `box-shadow: 0 0` / `shadow-[0_0_` or ad-hoc inline `<path d="M..."` outside canonical icon components
- `outline: none` or `outline: 0` without a `:focus-visible` rule in the same file
- `@media` breakpoints inside a component that lives in a sidebar or split view (should be `@container`)
- `font-variant-numeric` missing on a numeric table/list column
- Fixed `width`/`height` in px on a table cell or grid item with no `min-width: 0` ancestor
- `<div` / `<span` with `onClick` and no `role` / `tabIndex` / key handler
- `transition` on `width`, `height`, `top`, or `left` (layout-animating)
- `ease-in-out` applied to both entrance and exit
- `<img>` with no `width`/`height` or `aspect-ratio`
- User-visible copy as string literals or concatenation (i18n leak)
- `alert(` / `confirm(` / `prompt(`

## Quantitative checks worth running

- Core Web Vitals thresholds at the 75th percentile, segmented mobile and desktop: **LCP ≤ 2.5s**, **INP ≤ 200ms**, **CLS ≤ 0.1**. INP cannot be measured in a lab (no user input); use **TBT** as the lab proxy — optimisations that improve TBT in the lab tend to improve INP in the field [S12].
- Contrast: body text ≥ 4.5:1; large-scale text (≥24px, or ≥18.5px bold — 18pt/14pt at 1pt = 1.333px) ≥ 3:1; UI component visual information and state indicators ≥ 3:1. Ratios are thresholds, not to be rounded [S9][S13].
- Target size: 24×24 CSS px minimum, or the spacing exception [S4]; 44×44 CSS px is the AAA enhanced target [S5].
- Reflow: content presented without two-dimensional scrolling at 320 CSS px width (equivalent to a 1280px viewport at 400% zoom) for vertical content, 256 CSS px height for horizontal content [S7].
- Layout shift audit: any element that moves after surrounding content loads, including late-loading cookie notices, ads, and embeds that Lighthouse's load-time analysis may not flag [S8].

## Not found

- **A sourced weighting for the pillar table.** Weights reflect design judgement about where B2B product UI fails most; no accessibility standard or performance guideline assigns weights to design quality dimensions. Settling them empirically would need task-success and time-on-task data from a usability study across the same surface set.
- **A normative minimum font size for Dense product UI.** WCAG constrains contrast and reflow, not type size. The 12–13px Dense range is this skill's judgement, overridable by the project's `DESIGN.md`.
- **A normative maximum modal depth or field count.** No standard caps modal scope; the route/panel/modal ladder is design judgement.

## Sources

- **[S1]** https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric — Mozilla Developer Network (`tabular-nums` activates figures "all of the same size, allowing them to be easily aligned like in tables"; CSS Fonts Module Level 4). Accessed 2026-10-05.
- **[S2]** https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — W3C WAI, WCAG 2.2 Understanding docs (SC 1.4.11 Non-text Contrast, 3:1; author-styled focus indicators must meet 3:1, including when overlays dim them). Accessed 2026-10-05.
- **[S3]** https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html — W3C WAI, WCAG 2.2 Understanding docs (SC 2.4.11 Focus Not Obscured (Minimum); sticky header/footer obscuring focused items; F110 failure). Accessed 2026-10-05.
- **[S4]** https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — W3C WAI, WCAG 2.2 Understanding docs (SC 2.5.8 Target Size (Minimum), 24×24 CSS px plus the spacing exception; 16px-tall stacked button-row failure; dropdown menu item height example). Accessed 2026-10-05.
- **[S5]** https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html — W3C WAI, WCAG 2.2 Understanding docs (SC 2.5.5 Target Size (Enhanced), Level AAA, 44×44 CSS px). Accessed 2026-10-05.
- **[S6]** https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries — Mozilla Developer Network (container queries as an alternative to viewport media queries; `container-type`, `@container`, `container-name`; `cq*` units default to small viewport units with no eligible container). Accessed 2026-10-05.
- **[S7]** https://www.w3.org/WAI/WCAG22/Understanding/reflow.html — W3C WAI, WCAG 2.2 Understanding docs (SC 1.4.10 Reflow: 320/256 CSS px, 400% zoom equivalence, two-dimensional layout exceptions, scrollable-container pattern for tables, non-excepted surrounding content). Accessed 2026-10-05.
- **[S8]** https://web.dev/articles/css-web-vitals — Google / web.dev (CSS for Web Vitals: reserving image space to prevent layout shift, Lighthouse's "Avoid large layout shifts" audit missing post-load widgets, non-composited animations, critical CSS). Accessed 2026-10-05.
- **[S9]** https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — W3C WAI, WCAG 2.2 Understanding docs (SC 1.4.3 Contrast (Minimum): 4.5:1 body, 3:1 large text, ratios are thresholds and must not be rounded; large-scale = 18pt or 14pt bold, ≈24px / ≈18.5px). Accessed 2026-10-05.
- **[S10]** https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html — W3C WAI, WCAG 2.2 Understanding docs (SC 4.1.3 Status Messages: status must be programmatically determinable via role or property and presented without receiving focus; "18 results returned", "5 errors on page" as named examples). Accessed 2026-10-05.
- **[S11]** https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion — Mozilla Developer Network (`prefers-reduced-motion: reduce`; scaling and panning large objects named as vestibular motion triggers; Baseline widely available). Accessed 2026-10-05.
- **[S12]** https://web.dev/articles/vitals — Google / web.dev (Web Vitals: LCP 2.5s, INP 200ms, CLS 0.1, 75th percentile segmented mobile/desktop; INP field-only with TBT as lab proxy). Accessed 2026-10-05.
- **[S13]** https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — as S2 (SC 1.4.11 covers UI component and state-indicator contrast at 3:1). Accessed 2026-10-05.