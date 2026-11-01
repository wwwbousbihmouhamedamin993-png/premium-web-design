# Radius and motion tokens

Two token families always audited together, because both are pure appearance — and both are where
"it looked off but I can't say why" defects come from. Radius has a checkable geometric rule (nested
corners must be concentric). Motion has a hard principle (animate compositor properties only) and a
hard accessibility requirement (`prefers-reduced-motion`).

## Radius: one base, derived multipliers

There is **no standardized density or scale mode selector** in CSS. The only shipped pattern is a single
base token with `calc()` multipliers. shadcn/ui's is the reference: `--radius` is the base and each step
is `calc(var(--radius) * n)` — `-sm: * 0.6`, `-md: * 0.8`, `-lg: * 1.2`, `-xl: * 1.6`, `-2xl: * 2`,
`-4xl: * 2.6` (shadcn/ui, *Theming*, accessed 2026-10-05). That is deliberately not a spec: the Design
Tokens Format Module states token groups "are arbitrary" and tools "SHOULD NOT" use them to infer type or
purpose (W3C Design Tokens Community Group, *Design Tokens Format Module*). **House rule.**

```css
:root {
  --radius: 0.375rem;             /* the only authored value */
  --radius-xs:  calc(var(--radius) * 0.4);
  --radius-sm:  calc(var(--radius) * 0.6);
  --radius-md:  calc(var(--radius) * 0.8);   /* default container */
  --radius-lg:  calc(var(--radius) * 1.2);
  --radius-xl:  calc(var(--radius) * 1.6);
  --radius-full: 9999px;          /* pills; the one exception */
}
```


**Radius encodes size, in reverse** — that is what makes the scale mean something: `xs`/`sm` for checkboxes,
tags, small badges; `md` for inputs, selects, buttons; `lg`/`xl` for cards, panels, dialogs; `full` for
pills, avatars, status dots. The failure mode is a uniform radius everywhere: when a 28px checkbox and a
600px dialog share one, one looks wrong. Material treats radius as a continuum on the type-scale model:
4/8/12/16/24dp (Android Developers, *Material Design 3 in Compose*, accessed 2026-10-05).

## The nested-radius rule

**If one rounded box sits inside another, their radii must not be equal.** Equal radii make the gap between
edges visibly wider at the corner than along the straight edges, and the result reads as a mistake. The
correction is geometric: **inner radius = outer radius − padding**. Material states this as "optical
roundness": "Outer radius - padding = inner radius. For example: **48dp - 14dp = 34dp**", with the
instruction "**Do use different corner radii values for nested components so they have optical
roundness**" (Material Design 3, *Shape*, accessed 2026-10-05). Why: for concentric corners the arc centres
must lie on the same axis, and the distance between arc centres equals the gap between the edges.

```css
.card     { --r: var(--radius-lg); padding: 0.75rem; border-radius: var(--r); }
.card > * { border-radius: max(0px, calc(var(--r) - 0.75rem)); }
```

`max()` is load-bearing: a card with 4px radius and 16px padding would otherwise compute `-12px`, which is
invalid. Include the border width in the inset — the gap is edge-to-edge. **Exception: pills**, which stay
fully rounded based on their own size. **When to stop deriving:** if the inset varies around the component,
the inner element does not reach the corner, or the surfaces deliberately use different corner characters,
set the radius by eye.

**Not found:** no W3C, MDN, or vendor primary source publishes the concentric-radius formula as a general
rule; Material's *Shape* page is closest and gives one worked example. The `max(0px, …)` guard, the
size-encoding table, and the 0.375rem base are house rules.

## Motion tokens and asymmetric durations

Two axes, tokenised separately: **duration** (how long) and **easing** (how the rate changes). **Both sets
of values below are house values.**

```css
:root {
  --duration-instant: 80ms;   --ease-decelerate: cubic-bezier(0, 0, 0, 1);
  --duration-fast:    140ms;  --ease-accelerate: cubic-bezier(0.3, 0, 1, 1);
  --duration-base:    200ms;  --ease-linear: linear;
  --duration-slow:    280ms;
}
```

`instant` is for opacity and colour, `fast` for hover and focus, `base` for popovers and dropdowns, `slow`
for dialogs and drawers. The cited part is the shipped keyword curves: MDN gives the exact cubic Bézier each
equals — `linear` = `cubic-bezier(0.0, 0.0, 1.0, 1.0)`; `ease` = `cubic-bezier(0.25, 0.1, 0.25, 1.0)` (the
default); `ease-in` = `cubic-bezier(0.42, 0, 1, 1)`; `ease-out` = `cubic-bezier(0, 0, 0.58, 1)`;
`ease-in-out` = `cubic-bezier(0.42, 0, 0.58, 1)` (MDN, *`<easing-function>`*, accessed 2026-10-05). Two hard
validity facts from MDN's `cubic-bezier()` page: **P1x and P2x must be in `[0, 1]`** — "valid when the
x-axis coordinates of P1 and P2 are both in the `[0, 1]` range" — while P1y/P2y may sit outside it, at the
cost of a "bouncing" overshoot; and **an invalid curve is silently dropped**, since "if the cubic Bézier
curve is invalid, CSS ignores the whole property." **`linear()` is now Baseline *Widely available*** — good
for progress bars and multi-stop motion, where `linear(0, 0.25, 1)` "has linear stops of `0`, `0.25`, and
`1`" with each segment taking 50% of the duration (MDN, *`linear()`*); gate it behind `@supports` because
Safari support lagged (MDN blog, *Creating custom easing effects with `linear()`*).

**An element entering and the same element leaving must not share a duration.** Elements should
**decelerate in** (fast start, gentle settle — they arrive and stop) and **accelerate out** (gentle start,
quick exit — they leave and are gone). `ease-out` is `cubic-bezier(0, 0, 0.58, 1)` and MDN notes it "slows
down towards the end"; `ease-in` is `cubic-bezier(0.42, 0, 1, 1)`, which "starts slowly, then progressively
speeds up until the end, at which point it stops abruptly" (MDN, *`<easing-function>`*). Also shorten the
exit — the user has already decided to dismiss it — and roughly 70–80% of entry is the working ratio. The
principle: easing that changes rate "give[s] the element a sense of weight as it appears to gather
momentum" (MDN, *CSS easing functions*, accessed 2026-10-05).

| Transition | Duration | Curve |
|---|---|---|
| Popover / dropdown enter → exit | `base` → `fast` | decelerate → accelerate |
| Dialog / drawer enter → exit | `slow` → `base` | decelerate → accelerate |
| Hover / focus / toggle | `fast` | decelerate |
| Skeleton shimmer, spinner | `slow` loop | `linear` |

**What may animate.** `transform` and `opacity` stay on the compositor; `width`, `height`, `top`, `left`,
`margin`, and `box-shadow` force layout or paint every frame. One exception: **a zero-blur shadow is the one
animatable shadow** — when x-offset, y-offset, and blur are all zero, `box-shadow` renders as "a
solid-colored outline of equal-size on all sides" (MDN, *`box-shadow`*, accessed 2026-10-05), a ring that
follows `border-radius`, so animated focus rings should use it. One trap: **`will-change` and transforms
create stacking contexts** (MDN, *Stacking context*, accessed 2026-10-05), so promoting a card with
`will-change: transform` silently breaks a sticky header inside it.

**Not found:** no primary source specifies a numeric entry:exit ratio or the control points above. The
70–80% ratio and the 80/140/200/280ms ladder are house conventions.

## Session-gated counters

When a number displays on page load — a stat tile's total, a usage counter, a billing balance — roll
it **once per session on first view**, then render instantly on every repeat visit and tab switch in
that same session. Replaying the roll every time the dashboard mounts is animation fatigue: engaging
on day one becomes friction by day ten, and on a surface visited twenty times a day the roll is the
defect, not the polish.

- **Roll on load, once per session.** A `sessionStorage` flag (or the framework's equivalent) gates
  the entrance interpolation; afterwards the value renders at rest.
- **Roll on direct action, always.** A value the user just changed with a control updates by
  interpolation on every action — that is state-change feedback, not decoration.
- **Roll the value, not the glyphs.** Interpolate the number (~`--duration-base`), never cross-fade
  two strings — reflowing glyph strings jitters layout. Keep `tabular-nums` on through the roll.
- **Session-gated applies to entrance cascades too.** On high-frequency surfaces, hero-number and
  stagger entrances run on first appearance per session; back-navigations render at rest.

House rule, adapted from `premium-mobile-design` `motion-physics.md` — the mobile skill retains the
original. No vendor source prescribes it; the rule is this skill's judgement that replay cost scales
with visit frequency, and dashboards are the highest-frequency surfaces in the product.

## Reduced motion

`prefers-reduced-motion` is Baseline **Widely available**, has **exactly two** values (`no-preference` /
`reduce`), and targets **vestibular** triggers specifically — scaling and panning large objects, parallax,
similar large-area movement (MDN, *`prefers-reduced-motion`*, accessed 2026-10-05). It is not a blanket
"turn off animation" switch, so the implementation is **substitution, not deletion**: replace slide-ins and
scale-ins with cross-fades; replace the skeleton shimmer with a static block or a slow opacity pulse; set
`animation: none` on parallax and scroll-linked transforms. **Keep** spinner rotation (small, continuous,
non-vestibular) and hover/focus colour transitions (no motion at all). But do not zero out `--duration-*`
blindly — that turns transitions into instant flips, removing the state-change signal the animation provided:
```css
@media (prefers-reduced-motion: reduce) {
  :root { --duration-fast: 1ms; --duration-base: 1ms; --duration-slow: 1ms; }
  .drawer { translate: none; }   /* replace movement with a fade */
  .toast  { opacity: 1; }        /* keep opacity and colour */
}
```

**WCAG requirements CSS cannot satisfy.** **SC 2.2.2 Pause, Stop, Hide (A)**: anything that "(1) starts
automatically, (2) lasts more than five seconds, and (3) is presented in parallel with other content" needs
"a mechanism for the user to pause, stop, or hide it unless the movement, blinking, or scrolling is part of
an activity where it is essential" (W3C WAI, *Understanding SC 2.2.2*, accessed 2026-10-05). Live-tailing
log viewers, auto-advancing carousels, and pulsing "syncing" indicators fall under this. W3C adds two
constraints that catch teams: the mechanism "must provide the user with a means to pause that does not tie
up the user or the focus" (so a hover-only pause fails), and authors should provide "a single mechanism"
governing all such motion "rather than one per element" (both W3C WAI, *Understanding SC 2.2.2*). **SC 2.3.3
Animation from Interactions (AAA)**: motion triggered by interaction must be disableable "unless the
animation is essential to the functionality or the information being conveyed" (W3C, *WCAG 2.2*) —
`prefers-reduced-motion` satisfies it.

## Entry and exit: the platform mechanism

Entering and leaving is where hand-rolled motion breaks. Both `@starting-style` and `transition-behavior:
allow-discrete` are Baseline **Newly available** as of 2024-08-06 (Chrome 117, Edge 117, Firefox 129,
Safari 17.4) (GoogleChrome/modern-web-guidance, *animate-to-from-top-layer*, accessed 2026-10-05). Three
mandatory pieces for top-layer surfaces. **`@starting-style`** — "CSS transitions are by default not
triggered on an element's initial style update, or when its `display` type changes from `none`… To enable
first-style transitions, `@starting-style` rules are needed" (MDN, *`@starting-style`*, accessed
2026-10-05). **`transition-behavior: allow-discrete`** — "Transitions will be started on the element for
discrete animated properties," and `display` must be in the transition list "to ensure the animated element
is visible… throughout both the entry and exit animations" (MDN, *`transition-behavior`*). And
**`overlay` in the transition list** to defer removal from the top layer until the animation ends (MDN,
*`overlay`*) — **limited availability, Chrome 117 and Edge 117 only**, and "can only be set by the browser —
author styles cannot change the `overlay` value."

**Shorthand ordering trap.** "**DO NOT** use `allow-discrete` in the `transition` shorthand — it will make
older browsers ignore the entire `transition` declaration. Except in use cases where that is desirable, use
a separate `transition-behavior: allow-discrete` declaration" (GoogleChrome/modern-web-guidance,
*animate-element-entry-exit*, accessed 2026-10-05) — and it must come **after** the `transition` shorthand,
or the shorthand resets it:

```css
dialog[open], [popover]:popover-open {
  opacity: 1; translate: 0 0;
  @starting-style { opacity: 0; translate: 0 12px; }
}
dialog, [popover] {
  opacity: 0; translate: 0 12px;
  transition-property: opacity, translate, display, overlay;
  transition-duration: 200ms;
  transition-behavior: allow-discrete;   /* AFTER the shorthand */
}
```

Treat it all as **progressive enhancement**: where unsupported, the element toggles `display: none`
instantly and everything still works (web.dev, *Now in Baseline: animating entry effects*).

## Verify

- Grep for `border-radius` literals outside the token file. Any hit is a defect.
- Screenshot every nested rounded pair — the corner gap must match the straight-edge gap.
- Force padding above the outer radius; confirm `max()` prevents a negative value.
- Grep for `transition` on `width`, `height`, `top`, `left`, or `margin`.
- Grep for `allow-discrete` inside a `transition` shorthand; verify each standalone `transition-behavior`
  declaration follows its shorthand.
- Emulate `prefers-reduced-motion: reduce`. Every large-area movement must be gone; fades remain.
- Confirm any auto-starting motion over five seconds has a pause control independent of hover or focus.
- Open a surface that rolled a load-time counter, navigate away, navigate back: the value renders at
  rest on the repeat visit. A re-rolled counter is a defect.

## Sources

- Theming (`--radius` base with `calc()` multipliers: sm 0.6, md 0.8, lg 1.2, xl 1.6, 2xl 2, 4xl 2.6) — shadcn/ui. https://ui.shadcn.com/docs/theming — accessed 2026-10-05
- Shape — corner radius scale (optical roundness: outer radius − padding = inner radius; 48 − 14 = 34dp) — Material Design 3. https://m3.material.io/styles/shape/corner-radius-scale — accessed 2026-10-05
- Material Design 3 in Compose (shape scale 4/8/12/16/24dp) — Android Developers. https://developer.android.com/develop/ui/compose/designsystems/material3 — accessed 2026-10-05
- The Math Behind Nesting Rounded Corners (`r_outer = r_inner + inset`) — Cloud Four. https://cloudfour.com/thinks/the-math-behind-nesting-rounded-corners/ — accessed 2026-10-05
- Design Tokens Format Module (groups arbitrary; tools SHOULD NOT infer type/purpose — the radius scale is a house rule) — W3C DTCG. https://www.designtokens.org/TR/2025.10/format/ — accessed 2026-10-05
- MDN Web Docs — `easing-function` (exact cubic Bézier per keyword), `cubic-bezier()` (P1x/P2x in `[0,1]`; invalid curve ignored), `linear()` (Baseline Widely available), `prefers-reduced-motion` (two values; vestibular targets), `box-shadow` (zero offset + blur = outline), Stacking context (`transform`/`filter`/`will-change`), `@starting-style`, `transition-behavior`, `overlay`, *Creating custom easing effects with `linear()`* (Safari caveat), *CSS easing functions* ("a sense of weight"). https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/easing-function · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/easing-function/cubic-bezier · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/easing-function/linear · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/box-shadow · https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_context · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@starting-style · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/transition-behavior · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/overlay · https://developer.mozilla.org/en-US/blog/custom-easing-in-css-with-linear/ · https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Easing_functions — all accessed 2026-10-05
- GoogleChrome/modern-web-guidance — Animate to/from top layer (Baseline Newly available 2024-08-06; `overlay` limited availability, Chrome/Edge 117); Animate element entry/exit (`allow-discrete` in the shorthand makes older browsers ignore the whole declaration). https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/user-experience/animate-to-from-top-layer.md · https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/animate-element-entry-exit.md — accessed 2026-10-05
- Now in Baseline: animating entry effects (Newly available with Firefox 129; progressive enhancement) — web.dev. https://web.dev/blog/baseline-entry-animations — accessed 2026-10-05
- Understanding SC 2.2.2 Pause, Stop, Hide; WCAG 2.2 SC 2.3.3 Animation from Interactions (AAA) — W3C. https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html · https://www.w3.org/TR/WCAG22/ — accessed 2026-10-05
