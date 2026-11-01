# Production launch checklist

Applies to: any logged-in product surface going to real users. This is a **verifiable gate**, not
advice. Every item states the artefact that proves it. An item with no artefact is not passed —
it is unverified, and unverified ships as a bug report.

Three classes of item, marked throughout:

- **[N]** Normative — traceable to a specification. Cite the clause in review.
- **[P]** Primary-source practice — traceable to a design system or engineering guide.
- **[H]** **House judgement.** Not sourced. Deliberate, reviewable, and overridable by the host
  project. Disagreement with an [H] item is a conversation, not a conformance failure.

## 0. Prerequisites

- [ ] **[H]** Density class declared and written into the tokens file: Focused, Standard, or Dense (`craft-floor.md`, `information-density.md`). Named, not implied by the CSS.
- [ ] **[H]** The surface is registered against `signature-moves.md` — at least one move that is not generic.
- [ ] **[P]** Loading, empty, error and permission states exist as designed variants. The test is Polaris': "A page that removes the skeleton but has no failure state isn't complete" (`loading-skeletons.md`).

## 1. States — every one present, every one reachable

- [ ] **[H]** Every data region has a defined terminal: loaded, empty, error. No spinner without a timeout you ship yourself — Polaris' spinner "continues spinning indefinitely … doesn't automatically stop after a timeout or show error states".
- [ ] **[H]** Empty states carry a next action, not an apology (`empty-states.md`).
- [ ] **[H]** Error states say what failed, what to do, and whether retry is safe (`error-states.md`).
- [ ] **[H]** Permission-denied is a designed state with a route back, not a blank pane or a 404 (`roles-permissions-matrix.md`).
- [ ] **[N]** Limit states exist: quota exceeded, trial expiry, plan downgrade, read-only mode.
- [ ] **[H]** Operations over 10s show percent-done **and** a cancel control (NN/g's 10s limit).
- [ ] **Artifact:** screenshot set — loaded / empty / error / permission / limit — per surface.

## 2. Density class consistency

- [ ] **[H]** One class per surface. No screen mixes 12px table text with 16px prose without a stated reason.
- [ ] **[H]** Row heights come from one scale; no hand-tuned `padding` outside it.
- [ ] **[H]** Numeric columns use `font-variant-numeric: tabular-nums` and are right-aligned; never centred.
- [ ] **[H]** Every table column maps to a scanning decision (identify, compare, sort). A column nobody reads or sorts by is removed, not narrowed.
- [ ] **Artifact:** density token resolved in devtools per surface; diff showing no ad-hoc `font-size`/`line-height`/`padding`.

## 3. Keyboard traversal

Tab order only, then the extras. Every route, unauthenticated state excluded.

- [ ] **[N]** Every pointer-reachable action is keyboard-reachable, no timing requirement — **SC 2.1.1, Level A**.
- [ ] **[N]** Focus order preserves meaning and operability — **SC 2.4.3, Level A**.
- [ ] **[N]** Skip link is the **first** focusable element and moves focus into the main region — **SC 2.4.1, Level A**. W3C's evidence: without it a keyboard user "needs to tab through approximately 40 links".
- [ ] **[N]** Nothing traps focus — **SC 2.1.2, Level A**.
- [ ] **[N]** No positive `tabindex` anywhere; APG calls values above 0 "strongly discouraged".
- [ ] **[H]** Every composite (menu, tablist, combobox, grid, tree) implements its full APG keyboard contract, or uses the native element.
- [ ] **[H]** Virtualised and re-sorted tables use roving tabindex; focus does not reset to the top on sort, re-fetch, or page change.
- [ ] **[H]** Focus is restored to the trigger when a dialog, drawer or menu closes — restored, not moved to `document.body`.
- [ ] **[H]** On route change, focus moves to the new `<h1>` (or a skip target) and the document title updates.
- [ ] **Artifact:** a recorded tab-through per route, or a transcript of every tab stop in order.

## 4. Focus visibility

- [ ] **[N]** Every keyboard-focusable element has a visible indicator that does not disappear over time — **SC 2.4.7, Level AA**.
- [ ] **[N]** The focused element is not entirely hidden by author-created content — **SC 2.4.11, Level AA**. Sticky headers, sticky footers, non-modal dialogs and cookie banners are the named offenders; W3C prescribes scroll padding.
- [ ] **[H]** Focus ring meets **SC 2.4.13 Focus Appearance (Level AAA)**: area ≥ a 2 CSS px thick perimeter of the unfocused component, and **3:1 between the same pixels focused and unfocused**. [H] for adopting it; [N] for the 2px/3:1 figures. Passing 2.4.7 is not the bar.
- [ ] **[H]** Two-colour indicator (technique **C40**) where the surface varies, so the ring holds on light, dark, and striped rows.
- [ ] **[N]** `outline` is never set to `none` without a replacement — technique **F78** (outlines styled to be invisible) fails 1.4.11, 2.4.7 and 2.4.13.
- [ ] **Artifact:** a focus-state screenshot of every distinct control variant on every surface colour it appears on.

## 5. Contrast verified in BOTH modes

- [ ] **[N]** Text 4.5:1; large text (≥24px, or ≥18.66px bold) 3:1 — **SC 1.4.3, Level AA**.
- [ ] **[N]** Components, state indicators and meaningful graphics 3:1 against adjacent colours — **SC 1.4.11, Level AA**.
- [ ] **[N]** **Ratios are not rounded.** W3C: computed values "should not be rounded (e.g. 2.999:1 would not meet the 3:1 threshold)". 4.499:1 fails.
- [ ] **[N]** Disabled components are exempt (1.4.11 excepts inactive controls). Do not use that to justify an unreadable disabled state.
- [ ] **[H]** Measured on rendered pixels from tokens, not off a screenshot, and run **twice** — light and dark, with `prefers-color-scheme` forced. Both passes recorded.
- [ ] **[H]** Chart series, status dots and badge fills are in scope: a green "healthy" dot at 2.8:1 on white fails whether or not it is "text".
- [ ] **[H]** Charts pass under `forced-colors: active` or degrade to non-colour encodings.
- [ ] **Artifact:** a contrast report listing every token pair in use, in both modes, with computed ratio and verdict. Not a spot check.

## 6. Reduced-motion variant

- [ ] **[H]** `prefers-reduced-motion: reduce` is a distinct stylesheet state, not a shorter duration. MDN: the user "prefers an interface that removes, reduces, **or replaces** motion-based animations".
- [ ] **[H]** Under `reduce`: no parallax, no translation across the viewport, no scale/zoom transitions, no auto-advancing carousel, no autoplaying video with motion. Fades are acceptable substitutes.
- [ ] **[H]** The variant is screenshotted and diffed against the default. A transition silently set to `0.01ms` is a regression with a plausible diff, not a variant.
- [ ] **[H]** Verified via the real OS setting on at least one OS, not only devtools emulation.
- [ ] **Artifact:** two screenshots per surface — default and reduced motion.

## 7. The criterion set, with levels

Covered item-by-item in §3–§5, §8 and §11. Levels, because levels are the trap:

| SC | Name | Level |
|---|---|---|
| 2.1.1 / 2.1.2 | Keyboard / No Keyboard Trap | **A** |
| 2.4.1 / 2.4.3 | Bypass Blocks / Focus Order | **A** |
| 4.1.2 / 3.3.1 | Name, Role, Value / Error Identification | **A** |
| 2.4.7 / 2.4.11 | Focus Visible / Focus Not Obscured (Min) | **AA** |
| 4.1.3 | Status Messages | **AA** |
| 1.4.3 / 1.4.11 | Contrast (Minimum) / Non-text Contrast | **AA** |
| 2.5.8 | Target Size (Minimum) — 24×24 CSS px | **AA** |
| 1.4.10 / 1.3.4 | Reflow — 320px/256px / Orientation | **AA** |
| 1.4.4 / 1.4.12 | Resize Text — 200% / Text Spacing | **AA** |

**2.5.5 Target Size (Enhanced) at 44×44 and 2.4.13 Focus Appearance are AAA, not AA** — an AA
audit never flags them, so a "passes AA" sign-off is not evidence either way. Criterion text and
techniques: `accessibility-web.md`.

## 8. Errors, status, and validation

- [ ] **[N]** Every auto-detected input error is identified **in text** and names the item — **SC 3.3.1, Level A**. A red border alone fails.
- [ ] **[N]** Where a correction is known, offer it — **SC 3.3.3, Level AA**.
- [ ] **[N]** A silently clamped value is still described. W3C: if the page "automatically changes that value to fall within the allowed range, the user's error would still need to be described to them".
- [ ] **[N]** Status messages that do not take focus are programmatically determinable so AT can present them **without receiving focus** — **SC 4.1.3, Level AA**: "Searching…", "18 results returned", "No results returned", busy indicators, "5 errors on page".
- [ ] **[N]** Every custom control has a programmatically determinable name, role and user-settable state — **SC 4.1.2, Level A**. Native elements used to specification satisfy this automatically.
- [ ] **[H]** The live-region container exists in the DOM **empty** before the message is written in; [N] 4.1.3 requires only programmatic determinability.
- [ ] **[H]** `aria-busy="true"` on a region being replaced, cleared when real content lands.
- [ ] **[H]** Fields carry the correct `autocomplete` token and a `name`; [N] user agents "might require" `name`/`id`, a `<form>` ancestor and a submit button. No `autocomplete="off"` on account or billing.
- [ ] **Artifact:** a screen-reader pass (VoiceOver or NVDA) over each surface's submit, validation, async and error paths.

## 9. Performance budgets met

Field numbers, not lab numbers.

- [ ] **[N]** **LCP ≤ 2.5 s · INP ≤ 200 ms · CLS ≤ 0.1**, judged at p75 segmented mobile/desktop; a page passes only if all three hold.
- [ ] **[H]** Measured on the five heaviest routes from field data (RUM or CrUX). Lab-only numbers do not close this item. [N] INP is field-measurable; TBT "may be a reasonable proxy … but it's not a substitute for INP in and of itself".
- [ ] **[N]** CLS: every async region reserves its final size in advance — "using a placeholder or skeleton UI" — and dynamic growth happens "within a fixed size container".
- [ ] **[N]** Every `<img>`/`<video>` has `width`/`height` or a reserving `aspect-ratio`.
- [ ] **[N]** `font-display` set deliberately; fallbacks carry `size-adjust`. [N] Chromium and Firefox block text rendering **up to 3 seconds**, Safari indefinitely.
- [ ] **[N]** No transition or animation on `top`, `left`: "Changing the top and left properties also cause layout shifts, even when the element being moved is on its own layer." Stick to `transform` and `opacity`.
- [ ] **[N]** Route-level code splitting: only the initial route's code ships in the initial bundle.
- [ ] **[H]** Every click produces a synchronous visual acknowledgement before any await; [N] INP measures latency to the next paint.
- [ ] **[H]** Every virtualised container declares an explicit height.
- [ ] **Artifact:** a dated field p75 report per route with the device split; plus a CI lab budget (TBT, throttled LCP) as the regression tripwire.

## 10. No console errors

- [ ] **[H]** Zero errors and zero unhandled rejections on every route, in every state, at every breakpoint in §11 — on load, navigation, mutation and unload.
- [ ] **[H]** Zero React key warnings, zero controlled/uncontrolled warnings, zero `act()` warnings. These are development-mode diagnostics of real defects.
- [ ] **[H]** No 404s or 5xx on any asset or API call during a full navigation walk.
- [ ] **[H]** No layout-shift source remains unaccounted for in §9.
- [ ] **Artifact:** a console recording per state and route, or an e2e assertion that fails the build on any console error.

## 11. Deep links resolve

- [ ] **[N]** Every route is addressable by URL and renders correctly on a cold load with no prior session state.
- [ ] **[N]** **SC 1.4.10 Reflow (AA)**: no two-dimensional page scrolling at **320 CSS px width** or **256 CSS px height** (equivalent to 1280px at 400% zoom). Tables may scroll horizontally; **each cell may not**.
- [ ] **[N]** **SC 1.3.4 Orientation (AA)**: no portrait/landscape lock.
- [ ] **[N]** **SC 1.4.4 Resize Text (AA)**: text resizable to 200% with no loss of content or functionality.
- [ ] **[N]** **SC 1.4.12 Text Spacing (AA)**: nothing clipped or lost with line-height 1.5×, paragraph spacing 2×, letter spacing 0.12×, word spacing 0.16×.
- [ ] **[H]** Back always works and means something; browser back, in-app back and breadcrumb agree.
- [ ] **[H]** A filtered, sorted, paginated URL reproduces that state on direct navigation — no state that exists only in memory.
- [ ] **[H]** An expired session on a deep link lands on login **with a return path** and returns the user to the original URL.
- [ ] **Artifact:** a deep-link matrix — five most-shared routes × {cold load, reload, pasted URL, expired session} — with the rendered result for each.

## 12. Tokens only, no raw hex

- [ ] **[H]** No raw hex, `rgb()` or `hsl()` literal in component or feature code; every colour is a token reference, enforced by a CI lint rule.
- [ ] **[H]** No hard-coded spacing, radius, shadow or type size in feature code. Density comes from the declared class.
- [ ] **[H]** Tokens are semantic, not literal: `surface-raised` / `text-muted` / `border-subtle`, never `grey-100`. Semantic tokens are what make the dark-mode and density passes mechanical.
- [ ] **[N]** Tokens that must survive forced-colors carry a `<system-color>` fallback — "authors should use colors from the `<system-color>` type for all properties that are not in the set of properties whose colors are overridden".
- [ ] **[N]** `color-scheme` is set **and** `prefers-color-scheme` is handled. MDN separates them: `color-scheme` handles UA chrome, and "Component authors must use the `prefers-color-scheme` media feature" for the rest.
- [ ] **[H]** Every token resolves in light, dark **and** forced-colors mode. A token that resolves in one only is a bug.
- [ ] **Artifact:** a passing lint run with the raw-colour rule enabled; plus the token diff showing no additions for this feature.

## 13. Internationalisation (only if the surface ships more than one locale)

- [ ] **[N]** `dir` set alongside `lang`; omitting `dir` does **not** enable automatic detection, and the default is left-to-right.
- [ ] **[N]** Every user-supplied name cell uses `dir="auto"` or `<bdi>` for unknown-directionality data.
- [ ] **[N]** No `left`/`right` CSS outside a `[dir=…]`-scoped override; logical properties throughout.
- [ ] **[N]** Every count uses `Intl.PluralRules`, not a ternary; all six CLDR category keys present in the catalogue.
- [ ] **[N]** Every user-visible sort goes through `Intl.Collator` for the active locale.
- [ ] **[N]** Buttons and column headers sized for the longest supported string: IBM's table in W3C's *Text size in translation* gives **200–300% expansion for source strings of 10 characters or fewer**.
- [ ] **Artifact:** a screenshot set in the longest supported locale, plus a pseudo-localisation run at ≥2× on every fixed-width element.

## 14. Sign-off

- [ ] **[H]** Every [H] item passed, or has a written, dated exception with a named owner. Undocumented exceptions are failures.
- [ ] **[H]** The density class on file matches the built result.
- [ ] **[H]** The screenshot set (states, focus, contrast, motion, long-locale) is attached to the release record.

## Not found

- **A single normative "definition of done" for accessibility.** WCAG 2.2 Level AA is the floor and
  no specification names a gate above it. This file's combination of AA clauses, the two AAA items
  adopted as house targets, and the artefact requirements is a house construction.
- **Any sourced requirement that a surface ship a density class, a token-only codebase, or a
  reduced-motion screenshot set.** These are [H] items by construction; no standard requires them.
  They are here because they are the failures that reach users most often on B2B consoles.
- **A numeric perf budget for bundle size or third-party script weight on a B2B console.** web.dev
  publishes the CWV thresholds and the code-splitting rule [N]; it publishes no byte budget.

## Sources

All pages **accessed 2026-10-05**. WCAG levels are as stated in §7 and taken from the W3C WAI
Understanding documents for each criterion; the URLs are listed individually in
`accessibility-web.md` § Sources (SC 1.3.4, 1.4.3, 1.4.4, 1.4.10, 1.4.11, 1.4.12, 2.1.1, 2.1.2,
2.4.1, 2.4.3, 2.4.7, 2.4.11, 2.5.5, 2.5.8, 3.3.1, 3.3.3, 4.1.2, 4.1.3), plus the standards and
engineering references cited inline above:

- **[N]** https://www.w3.org/WAI/WCAG22/Understanding/ — W3C WAI, *How to Meet WCAG*, index of all WCAG 2.2 Understanding documents.
- **[N]** https://web.dev/articles/vitals — web.dev (Google), *Web Vitals*. [CWV thresholds; p75 segmented mobile/desktop; pass requires all three]
- **[N]** https://web.dev/articles/inp — web.dev (Google), *INP*. [field-only measurement; 98th percentile; TBT caveat]
- **[N]** https://web.dev/articles/optimize-cls — web.dev (Google), *Optimize CLS*. [reserve space with placeholder or skeleton; fixed-size container; `width`/`height` or `aspect-ratio`; `top`/`left` cause shifts]
- **[N]** https://web.dev/articles/font-best-practices — web.dev (Google), *Best practices for fonts*. [3 s Chromium/Firefox block, Safari indefinite; `font-display` values; `size-adjust`]
- **[N]** https://web.dev/articles/reduce-javascript-payloads-with-code-splitting — web.dev (Google). [split to the initial route; dynamic `import()`]
- **[N]** https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ — W3C WAI, ARIA APG, *Dialog (Modal) Pattern*. [positive `tabindex` strongly discouraged]
- **[N]** https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/dir — MDN, *dir*. [inheritance; `auto` resolution; left-to-right default]
- **[N]** https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/bdi — MDN, *bdi*, Baseline since Jan 2020.
- **[N]** https://developer.mozilla.org/en-US/docs/Web/CSS/system-color — MDN, *system-color*. [forced-colors fallbacks]
- **[N]** https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme — MDN, *color-scheme*, Baseline since Jan 2022. [chrome recolouring vs `prefers-color-scheme` authorship]
- **[N]** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/PluralRules and .../Intl/Collator — MDN. [six CLDR tags; locale-dependent sort order]
- **[N]** https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/autocomplete — MDN, *autocomplete*. [user-agent preconditions]
- **[N]** https://www.w3.org/International/articles/article-text-size.en.html — W3C International, *Text size in translation*. [IBM expansion table, 200–300% at ≤10 characters]
- **[P]** https://shopify.dev/docs/apps/build/app-home/migrate-from-polaris-react/skeleton-page — Shopify. ["A page that removes the skeleton but has no failure state isn't complete"]
- **[P]** https://shopify.dev/docs/api/app-home/latest/web-components/feedback-and-status-indicators/spinner — Shopify Polaris. [spinner has no timeout or error state by default]