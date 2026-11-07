# Craft floor

Load this before editing UI, and build without announcing the checklist. The host project's
constitution overrides anything here. The floor holds the mechanics; it never picks the direction —
that is `screen.md` and `signature-moves.md`.

This floor is **density-aware**. Web product surfaces span a wide density range, and a single set of
defaults is what makes generic web advice — and generic detectors — wrong on real product work.
**Declare the surface's density class before applying any typographic or spacing rule.** Rules that
differ by class are tagged **[F] Focused · [S] Standard · [D] Dense**.

A 13px tabular numeral in a Dense surface is correct, not a violation.

## Density classes

| Class | Surfaces | Base body | Row height | Measure |
|---|---|---|---|---|
| **Focused** | Auth, onboarding, checkout, single-form flows, settings detail | 16px | — | 60–70ch, centered |
| **Standard** | Project home, card+list feeds, record detail | 14–15px | 40–44px | 65–80ch |
| **Dense** | Data tables, admin consoles, observability, logs, trading, IDE-like | 12–13px | 28–32px | full-width |

Whitespace budget by class: **Focused 55–70% · Standard 40–55% · Dense 25–40%.** Below the class
floor reads as cramped; above it reads as empty and wastes a viewport. Full mechanics:
`information-density.md`.

## Verify

Each of these is a check on the built result, not an intention.

### Density & scanability

- **One class per surface, applied consistently.** A screen does not mix 12px table text with 16px
  prose beside it without a reason. Row heights, gutters, and type size come from one scale.
- **Tabular numerals for anything comparable.** Any column of numbers, currency, timestamps, or
  deltas uses `font-variant-numeric: tabular-nums` so digits align vertically. Proportional figures
  in a numeric column is a defect.
- **Right-align numbers, left-align text.** Numbers align on the decimal; labels on the left. Never
  center a numeric column.
- **Every column earns its width.** Each table column maps to a scanning decision — identify,
  compare, sort. A column nobody reads or sorts by gets removed, not narrowed.
- **Density comes from row height, column pruning, and tight leading** — never from type small
  enough that a first-time user must zoom.
- **Alignment does the grouping.** Related values share a left edge; whitespace separates groups.
  Nested boxes are the last resort.

### Structure & IA

- **One screen, one job.** A route doing >2 major jobs gets split. Nested cards 2–3 deep mean the
  split is overdue.
- **Nav is scannable in under 2 seconds.** Group and label; **never cap the item count.** An
  over-short menu is its own failure — it forces abstract choices. Grouping, labelling, search, and
  recency beat arbitrary limits.
- **Every route reachable in ≤ 3 clicks** from the nav root. Otherwise it belongs elsewhere or needs
  search.
- **Back always works and always means something.** Browser back, in-app back, and breadcrumb agree.
  A deep link lands on the content, never the app home.
- **List and detail share a vocabulary.** A row and its detail page name things identically — same
  words, same order, same casing.
- **Destructive is never the primary accent,** and never wears the same weight as a safe action.
- **Unbounded content never enters shell navigation.** User-generated collections belong inside the
  content area, not the sidebar.

### Layout & responsive

- **Spacing on the 4px base scale** (8px comfortable [F/S], 4px [D]). No `17.0`, no `23.0`. Section
  rhythm: more space above a heading than below it.
- **Content has a max measure** [F/S]: 65–80ch for prose. Unconstrained for grids and tables [D].
- **Container queries for anything inside a resizable layout** (sidebars, panels, split views).
  Viewport media queries only for page-level reflow.
- **The page never scrolls sideways.** Overflow belongs in a named scroll region with
  `min-width: 0`, never on `body`.
- **Nothing important depends on hover.** Hover may reveal; focus and touch must reach the same
  content. Every hover-only affordance has a keyboard and touch path.
- **Narrow widths drop columns, not type size.** Hide low-priority columns and keep text legible.
- **`cq*` units have a fallback.** With no eligible container they silently resolve to small-viewport
  units — never use them where that would be wrong.

### Controls

- **One primary (filled) CTA per view** [F/S]. Dense toolbars may run a primary plus icon actions.
- **Pointer targets meet WCAG 2.2 SC 2.5.8: at least 24×24 CSS px, or the spacing exception** — a 24px
  circle centred on each target's bounding box must not intersect another target's. SC 2.5.5 at
  44×44 is **AAA, not AA**; treat 44px as the design target for primary controls [F/S] and the 24px
  floor as the hard minimum. Dense rows may use 24px with adequate spacing.
- **Labels name the action** — "Create project", not "OK", not "Submit". A button never changes
  width between idle and loading; reserve the space.
- **Every control has hover, focus-visible, active, and disabled states.** `:focus-visible` is visible
  and never removed. A disabled control says why on focus or hover, rather than being silently dead.
- **Toggles for instant binary state; checkboxes for batched multi-select.** Never mixed in one group.
- **No control is a `<div>` with a click handler.** If it behaves like a control it is a `<button>`,
  `<a>`, `<input>`, or carries the right roles, tabindex, and key handlers.

### Color

- **Semantic tokens only** — no raw hex in component code. Tokens resolve through the cascade, so
  light/dark and density are each one switch.
- **Three token layers, always:** primitive → semantic → component. A component consumes a semantic
  token; a semantic token resolves to a primitive. Nothing skips a layer.
- **No component-named primitive tokens.** `--card-bg`, `--tooltip` — these are the classic trap;
  one value serves several roles, so name the role, not the component.
- **Dark canvas is not pure black.** `#0E0E10`–`#141416` for app chrome. Depth comes from surface
  steps and 1px strokes, **never shadows on dark**.
- **Light mode is the default.** Dark mode is not a filter — it gets its own surface ramp, border
  strength, and shadow treatment (`dark-mode.md`).
- **Accent appears ≤ 2× per viewport** [F/S]. Dense surfaces may carry one status accent for
  selection or an active filter — still one accent hue.
- **Status is never colour alone.** Every state pairs colour with an icon, label, or shape. Green /
  amber / red always ship with text.
- **Contrast:** body ≥ 4.5:1, large text and UI boundaries ≥ 3:1 (WCAG 2.2 SC 1.4.3 and 1.4.11).
  **Do not round** — W3C states that 4.499:1 does not meet the 4.5:1 threshold. Large text is ≥ 24px,
  or ≥ 18.5px bold.

### Typography [F/S/D]

- **[F]** 16px base. Never below 14px for anything a first-time user must read.
- **[S]** 14–15px base; 13px for secondary metadata only.
- **[D]** 12–13px base permitted **for data surfaces only** — tables, logs, metrics, code. Prose
  inside a dense screen still steps up to 14px+. Dense is not a licence to make help text
  unreadable.
- **Line height:** 1.5 body · 1.2–1.3 headings · 1.4–1.5 dense rows. Never justify body text.
- **One family is the default.** A second only when it earns the contrast — a display face for
  marketing surfaces, a monospace for code, identifiers, and figures. Monospace is not a
  "technical" costume.
- **Fluid type is a marketing technique, not a product one.** Product UI uses fixed, stepped sizes;
  `clamp()` on a dashboard is a bug.
- **Tracking:** negative on large display, slightly positive on small uppercase labels, default on
  body.

### Motion

- **Entrances decelerate** (~200–300ms [F/S], ~120–180ms [D]); **exits accelerate** (~120–180ms).
  Symmetric ease-in-out on both directions is a defect.
- **Only `transform` and `opacity` animate** in product UI. Animating width, height, top, or left is
  a jank source.
- **Reduced motion is a real variant**, not `animation: none` everywhere: replace movement with a
  crossfade or an instant cut, keep opacity under ~150ms. Target vestibular triggers specifically —
  scaling and panning large objects.
- **Irreversible moments get no bounce.** Playful physics belong to marketing and empty moments,
  never to a confirm dialog.

### States

- **Every surface that fetches has all four:** loading (skeleton shaped like the real content — never
  a centred spinner on a blank page), empty (actionable: what's missing plus the CTA that fixes it),
  error (what happened plus how to recover), and offline/stale (what's known vs. what's cached).
- **Empty is a designed state with a job.** It teaches the shape of the thing and offers the first
  action. "Nothing here yet" is a defect.
- **Optimistic UI must be reversible.** If it can't be undone, it waits for confirmation and says so.
- **Long lists are virtualised past ~200 rows.** Beyond that, pagination or infinite scroll with a
  real end state — never an unbounded scroll with no floor.
- **Images and avatars sit in a fixed aspect-ratio box defined before load.** Zero layout shift. Set
  `width`/`height` attributes and `aspect-ratio`.
- **Copy says what happened and what to do next.** No bare "Submit"/"OK"/"Error", no raw server
  strings, no string concatenation. +35% expansion budget, locale formatters, ICU plurals. Keep
  paragraphs to ~150 words, never over 250.

### Performance floor

- **No layout shift on load.** Reserve space for every async region; skeletons match final
  dimensions.
- **Response-time budget [F/S]:** 0.1s feels instantaneous · 1.0s keeps flow of thought intact ·
  10s holds attention. Beyond ~10s a percent-done indicator is **required**, not optional.
- **Images:** explicit dimensions, `loading="lazy"` below the fold, modern formats, responsive
  `srcset`.
- **Table sort and filter stay interactive at 1k+ rows** — virtualise, debounce input, never block
  the main thread on sort.
- **Route-level code splitting.** A settings bundle must not load on first paint of the dashboard.
- **Fonts self-hosted and preloaded**, `font-display: swap` or `optional`, subset to the ranges used.
  Third-party font CDNs are a render-blocking risk.
- **Targets:** LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1, measured at the 75th percentile. INP is field-only
  — use TBT as the lab proxy.

## Refuse

These are the web's defaults, not bans: the brief's own words can earn any of them. Reaching for one
on a free axis means you were not deciding.

- **Marketing aesthetics inside the product.** Gradient text, radial glow backgrounds, glassmorphism
  across content cards, purple/cyan AI palettes, glowing dark-mode accents, hero-metric templates.
  Public marketing pages belong to `premium-marketing-design`; inside the app, depth comes from
  surface steps and hairlines. The one exception is a **declared** atmosphere moment under
  `atmosphere.md` — governed, rare, stage surfaces only, always carrying its static fallback.
  Undeclared glow is slop wherever it appears.
- **Affective mascot wrappers masking AI latency or failure.** Cute 3D avatars, blinking anthropomorphic
  eyes, or apologetic personality wrappers ("Oops! My brain got tangled") deflecting from model
  latency, uncertainty, or tool errors. Surface mechanical state instead — which step is running,
  elapsed time, what failed, rollback status, and a direct Retry / Undo control (`ai-chat-ui.md`).
- **Card inflation.** Card → card → card; five layers of boxes around one paragraph; an icon in a
  rounded tile above every heading; a coloured stripe on every card. Cards are for repeated peer
  items and containment, not for every group of three lines. Group with whitespace, dividers, and
  weight.
- **Stat-card dashboard.** Four identical KPI tiles in a row, carrying the same weight as everything
  else. One dominant metric per view; the rest support it. When every number shouts, nothing
  communicates.
- **Modals as connective tissue.** A modal for a three-field edit, a settings dialog holding 40
  controls, a modal inside a modal. Modals are for short, focused, interruptive tasks with a clear
  exit. Everything else is a route or a panel.
- **Two primary buttons side by side.** One primary per view; secondary and tertiary step down.
- **A toolbar of twelve unlabelled icon buttons.** Icons need labels or tooltips; past ~5 groups,
  overflow goes into a menu. Separate destructive from safe with a divider.
- **Hidden affordances.** Icon-only buttons with no tooltip, drag handles with no grip, scroll
  regions with no affordance, hover-only submenus with no keyboard path.
- **Placeholder-as-label.** A field that empties on focus and forgets its name.
- **A whole-page spinner; layout that jumps when data lands; optimistic UI with no undo.**
- **Browser `alert()`/`confirm()`;** a toast for an error that needs a decision; a centred modal for
  a two-field confirmation when an inline confirm or undo-toast suffices.
- **Tiny type as a density strategy.**
- **A disabled primary button as the only affordance** where an explanation exists. Say why, and
  offer the fix.
- **Unlabelled numeric badges** where colour alone carries the meaning.

## Density overrides for generic web detectors

`npx impeccable detect` encodes marketing-page defaults. At the class noted, treat these as
**advisory**, not failures:

| Detector finding | [F] Focused | [S] Standard | [D] Dense |
|---|---|---|---|
| `tiny-interface-text` | **fail** | **fail** (< 14px body) | **advisory** — 12–13px data type is legal |
| `identical-card-grids` | advisory | **advisory** — legal in a settings or feature index | fail |
| `modal-abuse` | fail | advisory — legal for scoped config | advisory |
| `monotonous-spacing` | **fail** | **fail** | advisory — even rhythm is correct in tables |
| `line-length-too-long` | **fail** | **fail** | advisory — full-width is correct in tables |
| `cramped-padding` | **fail** | **fail** | advisory — tight row padding is correct |
| `nested-cards` | **fail** | **fail** | **fail** |
| `gradient-text` | **fail** | **fail** | **fail** |
| `radial-gradient-background-halo` | **fail** | **fail** | **fail** |
| `low-contrast-text` | **fail** | **fail** | **fail** |
| `oversized-hero-headline` | n/a — not a marketing surface | n/a | n/a |

**The declared-atmosphere row.** `radial-gradient-background-halo` (and `gradient-text`) reads
**advisory, not fail**, on a surface carrying a declared atmosphere block — a `DESIGN.md` §1 entry
naming the family, intensity, trigger, fallback, and dither mode per `atmosphere.md`. On every other
surface it still fails. The detector cannot read `DESIGN.md`; the agent resolves the finding: declared
→ record advisory with the §1 reference; undeclared → fail, no discretion.

Record intentional exceptions rather than silencing a rule globally. A rule silenced everywhere is a
rule nobody reads. Mechanics: `detector-integration.md`.

---

The floor holds the mechanics; it never picks the direction. With every check green, spend the screen
on the committed direction — and when torn between refined and committed, commit. Worked
before/after pairs: `examples.md`. The reasoning behind the numbers: `ux-laws.md`.

## Sources

Numeric thresholds in this floor are traceable to the pages below. Where a rule is house judgement
rather than a sourced fact, the text says so at the point of use — the density class boundaries,
the whitespace budget per class, and the accent-use limits are all this skill's own decisions, not
standards.

| Source | Publisher | Used for | URL | Accessed |
|---|---|---|---|---|
| Understanding SC 2.5.8 Target Size (Minimum) (Level AA) | W3C WAI | 24×24 CSS px minimum; 24 px spacing-circle exception | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html | 2026-10-05 |
| Understanding SC 2.5.5 Target Size (Enhanced) (Level AAA) | W3C WAI | 44×44 is AAA, not AA | https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html | 2026-10-05 |
| Understanding SC 1.4.3 Contrast (Minimum) (Level AA) | W3C WAI | 4.5:1 text; 3:1 large text; large-text size; unrounded thresholds | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html | 2026-10-05 |
| Understanding SC 1.4.11 Non-text Contrast (Level AA) | W3C WAI | 3:1 for UI boundaries and chart marks | https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html | 2026-10-05 |
| Response Times: The 3 Important Limits | Nielsen Norman Group | 0.1 s / 1.0 s / 10 s; percent-done indicator beyond ~10 s | https://www.nngroup.com/articles/response-times-3-important-limits | 2026-10-05 |
| Web Vitals | Google / web.dev | LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 at p75; INP field-only, TBT lab proxy | https://web.dev/articles/vitals | 2026-10-05 |
| `prefers-reduced-motion` | MDN | two values; vestibular triggers | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion | 2026-10-05 |
| Container queries (incl. `cq*` units) | MDN | content-box measurement; `sv*` fallback when no container | https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries | 2026-10-05 |
| Short-Term Memory and Web Usability | Nielsen Norman Group | why "cap menus at 7 items" is a misreading | https://www.nngroup.com/articles/short-term-memory-and-web-usability/ | 2026-10-05 |
| Clear and short (plain language) | U.S. GSA / Digital.gov | 150-word paragraphs; 250-word hard ceiling | https://digital.gov/guides/plain-language/writing/clear-short | 2026-10-05 |
| Slop catalog | Impeccable | the rules this floor overrides per density class | https://impeccable.style/slop | 2026-10-05 |