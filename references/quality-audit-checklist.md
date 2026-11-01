# Quality audit — the mechanical pass

Evaluate command. `audit` runs the checks that can be *run* rather than judged, and separates them
honestly from the ones that need a human eye. It does not score (that is `critique.md`) and it does
not fix (that is `polish.md`, `harden.md`, `clarify.md`).

**Divide every check into one of three kinds before reporting it:**

- **[M] Mechanical** — a tool or a grep answers it. Pass/fail, reproducible.
- **[J] Judgement** — a human (or a rendered pixel) answers it. No tool decides it; report the
  evidence and let a person rule.
- **[G] Gated on environment** — needs a browser, a deployed URL, a screen reader, or field data.
  Unrunnable in this environment is a *result*, not a silence.

## 1. Deterministic gates first

Run these before anything that takes a human:

| Check | How | Kind |
|---|---|---|
| Type/analyzer/lint/tests | Project's own scripts | [M] |
| Raw hex / `rgb(` / `hsl(` outside the primitive token file | grep | [M] |
| `clamp(` / `vw` / `vh` inside a `font-size` | grep | [M] |
| `outline: none` with no `:focus-visible` in the same file | grep | [M] |
| `transition` on `width`, `height`, `top`, `left`, `margin` | grep | [M] |
| `border-radius` literal outside the token file | grep | [M] |
| `.dark` or `[data-theme]` selectors inside a component stylesheet | grep | [M] |
| `alert(` / `confirm(` / `prompt(` | grep | [M] |
| User-visible copy as string literals or concatenation | grep | [M] |
| `<div`/`<span` with `onClick` and no `role`/`tabIndex`/key handler | grep + read | [M] |
| `<img>` with no `width`/`height` and no `aspect-ratio` | grep | [M] |
| `ease-in-out` on both entrance and exit | grep | [M] |
| `font-variant-numeric` missing on a numeric column | read the column, check the class | [M] |
| Contrast of every token pair in both modes | measured ratio, not eyeballed | [M] once measured |
| `aria-rowcount` / `aria-rowindex` present on a virtualised grid | read | [M] |

The grep list is `critique.md`'s; each hit is a **lead, not a verdict** — confirm it before
reporting.

## 2. The full check table

Marked by kind. **[M]** items are pass/fail; **[J]** items need a rendered pixel and a ruling;
**[G]** items need an environment.

| # | Check | Kind | Threshold / source |
|---|---|---|---|
| 1 | Density class declared and applied consistently | [J] | Class table in `craft-floor.md`; mixed classes are a defect |
| 2 | `tabular-nums` on every comparable figure column | [M] | `critique.md`; MDN `font-variant-numeric` |
| 3 | Numerics right-aligned, text left-aligned, no centred numeric column | [J] | `craft-floor.md` |
| 4 | Row heights from one scale; header/toolbar/pagination match row height | [J] | `information-density.md` (Carbon data table) |
| 5 | No viewport-derived font size anywhere | [M] | grep for `clamp(`/`vw` in `font-size` |
| 6 | Every `font-size` paired with a `line-height` token | [M] | grep |
| 7 | Distinct font weights ≤ 3 | [M] | `typography-web.md` (house: 400 + 600) |
| 8 | Measure ≤ 80ch on prose; none on table cells | [M] measure the widest breakpoint | WCAG 2.2 SC 1.4.8 (AAA), W3C |
| 9 | No `text-align: justify` | [M] | SC 1.4.8; Carbon `body-01` left-aligned |
| 10 | Body text ≥ 4.5:1, large text and UI boundaries ≥ 3:1, **unrounded** | [M] once measured | WCAG 2.2 SC 1.4.3, 1.4.11; W3C: values "should not be rounded" |
| 11 | Contrast measured in **both** modes, chart series individually | [M] × 2 | `production-launch-checklist.md` §5 |
| 12 | Dark canvas not pure black; depth from surface steps and hairlines, never shadows | [J] | `dark-mode.md`, `elevation-layers.md` |
| 13 | Dark surface ramp monotonic in lightness (step 4 > step 3) | [M] screenshot compare | Material dark-theme tonal elevation |
| 14 | No component stylesheet branches on the mode | [M] grep | `dark-mode.md` |
| 15 | Semantic tokens only, three layers, every `*-bg` has an `on-bg` | [M] grep | `color-token-system.md` (house rule) |
| 16 | Accent uses ≤ 2 per viewport (Dense: one status accent) | [J] count on screen | `color-token-system.md` (house) |
| 17 | Status never carried by colour alone | [J] greyscale pass | WCAG SC 1.4.1 |
| 18 | All functionality keyboard-operable | [G] recorded tab-through | WCAG 2.2 SC 2.1.1 (Level A) |
| 19 | Focus order preserves meaning; skip link first; nothing traps focus | [G] | SC 2.4.3, 2.4.1, 2.1.2 (Level A) |
| 20 | Focus indicator visible and ≥ 3:1, including under a dim overlay | [M] measured + [G] keyboard | SC 2.4.7 (AA), 2.4.13 (AAA), 1.4.11 |
| 21 | Focused item never fully hidden by sticky chrome | [G] keyboard walk | SC 2.4.11 (AA); `scroll-padding` is the cited fix |
| 22 | Targets ≥ 24×24 CSS px, or the 24px spacing-circle exception holds | [M] measure + spacing test | SC 2.5.8 (AA); 44×44 is AAA (SC 2.5.5), not AA |
| 23 | Reflow: no 2D scroll at 320 CSS px / 256 CSS px outside excepted regions | [G] viewport | SC 1.4.10 (AA); tables/maps/video/toolbar-bound editors excepted |
| 24 | Text resizable to 200% without loss | [G] | SC 1.4.4 (AA) |
| 25 | Name, Role, Value determinable; states settable and announced | [G] | SC 4.1.2 (Level A) |
| 26 | Async status announced without stealing focus | [G] screen reader / DOM | SC 4.1.3 (AA) |
| 27 | Loading / empty / error / offline present **and reachable** for every fetching region | [J] + [G] | `production-launch-checklist.md` §1 |
| 28 | No centred spinner on a blank region; skeleton matches final dimensions | [J] | `loading-skeletons.md` |
| 29 | `prefers-reduced-motion` is a real variant, not `animation: none` everywhere | [G] emulate | MDN: "removes, reduces, **or replaces**" |
| 30 | Core Web Vitals: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 at p75 | [G] field; [M] lab proxy (TBT for INP) | `web-vitals-performance.md`; web.dev |
| 31 | No console errors on load | [G] | `production-launch-checklist.md` §10 |
| 32 | Every async region reserves its final size; images have dimensions | [J] + [M] | web.dev CSS for Web Vitals |
| 33 | Tokens only, no raw hex; no `!important` colour precedence | [M] grep | `craft-floor.md` |
| 34 | `z-index` never used to fix colour precedence; layer order used instead | [J] | `elevation-layers.md`; MDN `@layer` |
| 35 | Deep links resolve to the content, not app home; back agrees with breadcrumb | [G] | `critique.md` |
| 36 | Overlays: `Escape` path, visible close, focus returns to the trigger, no modal-in-modal | [G] keyboard | `modals-dialogs-drawers.md`; APG |
| 37 | Copy: no bare "Submit"/"OK"/"Error", no raw server strings, no concatenation | [M] grep | `clarify.md`; GSA 150/250 words |
| 38 | Strings survive +35% expansion and RTL | [G] locale + expansion | `i18n-rtl.md` |
| 39 | `npx impeccable detect` reconciled | [M] | `detector-integration.md` |
| 40 | The whole surface looks like one committed direction, not a template fill | [J] | `signature-moves.md`, `critique.md` |

Rows 40 and 1, 16, 40 are the ones an audit cannot mechanise; if the audit reports only mechanical
passes, the surface has not been reviewed.

## 3. Run the detector

```
npx impeccable detect src/
npx impeccable detect --json src/          # for CI or a scripted read
npx impeccable detect http://localhost:3000 # a URL scan needs a browser
```

**Exit codes** (verified from the CLI usage text): `0` scan completed with no primary findings,
advisories may still be listed · `1` at least one requested target could not be scanned ·
`2` scan completed with primary findings. On a partial multi-target scan the operational failure
takes precedence — treat `1` as a scan failure even if other targets produced findings.

**Advisory rule for this skill:** the detector encodes marketing-page defaults, and several of its
findings flip by density class. `craft-floor.md` carries the per-class override table; at the class
noted, those findings are **advisory, not failures**. `tiny-interface-text` reads "increase the size
so people can read without zooming" — correct in a Focused surface, wrong in a Dense console.
`nested-cards`, `gradient-text`, `radial-gradient-background-halo`, `low-contrast-text`, and
`justified-text` fail at every class. Mechanics, `--json`, DESIGN.md drift checks, scoped
value-level ignores, and the rule-ID caveat: `detector-integration.md`.

**Never silence a rule globally to make a scan pass.** Record the exception:

```
npx impeccable ignores add-value <rule> <value> --reason "<why>"
```

A rule silenced everywhere is a rule nobody reads.

## 4. Report

For each item: **[M]** pass/fail with the artefact (the grep output, the measured ratio, the exit
code). **[J]** the finding plus the screenshot region, and an explicit statement that it needs a
ruling. **[G]** either ran, or *not run and why* — an unrun check is an open item, not a pass.

Order the failures by user impact, not by file. Name the element, the value, and the fix: "improve
spacing" is not a finding.

**Not found:** no sourced set of audit *weights* or a mechanical pass-rate threshold exists — a
"90% audit score" would be invented. `critique.md`'s pillar weights are explicitly labelled
judgement, and `production-launch-checklist.md` is the artefact-bearing gate this audit points at.

## Sources

Sibling reference files: `production-launch-checklist.md` (the artefact-bearing launch gate; [N]/[P]/[H]
item classes), `accessibility-web.md` (the criterion table with levels), `web-vitals-performance.md`
(the three gates and what design owns), `detector-integration.md` (CLI, exit codes, ignores),
`critique.md` (slop detector and the mechanical grep list), `craft-floor.md` (per-density overrides),
`dark-mode.md`, `color-token-system.md`, `typography-web.md`, `information-density.md`,
`render-loop.md`, `i18n-rtl.md`, `modals-dialogs-drawers.md`, `loading-skeletons.md`.

External pages cited above, all previously opened by this skill:

- Run a detector scan (source vs URL scans; `--json`; exit codes 0/1/2; `--no-design-system`;
  `npx impeccable ignores add-value <rule> <value> --reason`) and Configuration & ignores (shared
  vs `--local` config; `--file` scoping; wildcard values need a file scope; inline
  `impeccable-disable` forms; `/impeccable doctor` checks for outdated rule IDs) — Impeccable docs.
  https://impeccable.style/docs/detector · https://impeccable.style/docs/config — accessed 2026-10-05.
- Slop catalog (rule names, categories, and which rules are advisory) — Impeccable.
  https://impeccable.style/slop — accessed 2026-10-05.
- Understanding SC 1.4.3 Contrast (Minimum) ("should not be rounded") · SC 1.4.11 Non-text Contrast ·
  SC 1.4.4 Resize Text · SC 1.4.10 Reflow · SC 2.1.1 Keyboard · SC 2.4.3 Focus Order ·
  SC 2.4.7 Focus Visible · SC 2.4.11 Focus Not Obscured · SC 2.4.13 Focus Appearance ·
  SC 2.5.5 Target Size (Enhanced) · SC 2.5.8 Target Size (Minimum) · SC 3.3.1 Error Identification ·
  SC 4.1.2 Name, Role, Value · SC 4.1.3 Status Messages — W3C WAI.
  https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — accessed 2026-10-05.
- Web Vitals (LCP 2.5 s / INP 200 ms / CLS 0.1 at p75; INP field-only, TBT lab proxy) and CSS for
  Web Vitals (reserve space for async regions) — Google / web.dev.
  https://web.dev/articles/vitals · https://web.dev/articles/css-web-vitals — accessed 2026-10-05.
- `prefers-reduced-motion` ("removes, reduces, **or replaces**") · `font-variant-numeric` ·
  `@layer` · `box-shadow` — MDN. https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
  — accessed 2026-10-05.
- Clear and short (plain language): 150/250-word paragraph rule — U.S. GSA / Digital.gov.
  https://digital.gov/guides/plain-language/writing/clear-short — accessed 2026-10-05.

**House process, not sourced fact:** the three-way [M]/[J]/[G] classification, the forty-row table's
ordering, the reporting format, and the "unrun is an open item" rule. The thresholds in the table are
cited; the exit codes were read from the Impeccable CLI usage text.