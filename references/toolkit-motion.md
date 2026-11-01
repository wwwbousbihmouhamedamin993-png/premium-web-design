# Toolkit — Motion (motion.dev)

Load when animation is load-bearing in a React/Vue/JS surface: layout transitions, presence/exit,
gesture response. Pair with `radius-motion-tokens.md` — that file owns the *tokens*, this one owns the
*library mechanics*.

## What it is

Motion (formerly Framer Motion) is a production animation library for React, JavaScript and Vue,
distributed under MIT and free to use. Its stated differentiators are a hybrid engine combining
JavaScript with hardware-accelerated browser APIs, independent transforms (`x`, `y`, `rotate`,
`scale` on one element without wrappers), native `hover`/`press`/`drag` gestures, single-prop layout
animation between any two layouts, real spring physics, `AnimatePresence` for exit animation,
variants/stagger/timelines, and `useMotionValue` for driving derived state. Its APIs are stated as up
to 90% smaller than a GSAP alternative, and it is trusted by Framer and Figma.

**Agent-facing:** the project ships `npx motion-ai` — an AI Kit (docs + examples vault + Motion UI)
— and an MCP server, and describes itself as "built for AI". **The import is `motion/react`, not
`framer-motion`**: the rename is complete, the old package still publishes but the docs say
"Framer Motion is now Motion. Import from motion/react instead of framer-motion." Stale training
data reaches for `framer-motion` — don't. If you install it, also install its skill so the agent
gets the current API rather than recalling a stale one.

## Reduced motion — the part that matters most

This is the library's strongest contribution to a product UI, and it maps directly onto the
`craft-floor.md` reduced-motion rule.

Two mechanisms:

**Site-wide, automatic.** Set `reducedMotion="user"` on `MotionConfig`. All `motion` components then
**automatically disable transform and layout animations while preserving animation of other values
such as `opacity` and `backgroundColor`**. You can also pass `"always"` or `"never"` to let a user
override it for their site.

```jsx
<MotionConfig reducedMotion="user">{children}</MotionConfig>
```

**Per-component, manual.** The `useReducedMotion()` hook returns a boolean. Motion's own guidance
names three concrete substitutions:

1. **Replace `transform` with `opacity`.** Because iOS still animates between states for users with
   Reduced Motion enabled, substitute a fade for scale and x/y animations.
2. **Disable auto-playing video.** The hook returns a plain boolean, usable for any purpose —
   `<video autoplay={!shouldReduceMotion} />`.
3. **Disable parallax.** Motion's docs call parallax "very unpleasant for people pre-disposed to
   motion sickness"; pass `0` in place of the derived `MotionValue`.

This aligns with `radius-motion-tokens.md`: reduced motion is a real variant, not `animation: none`
everywhere — opacity survives, movement does not.

## Performance auditing

**MotionScore** (`score.motion.dev`) is a free animation-performance audit. It grades a live site
S through F, breaks the score down finding by finding, runs desktop and mobile viewports, emits
copy-paste fixes intended for an AI agent, and is guard-gated for CI.

That last property is the useful one for this skill: MotionScore can join `render-loop.md` as a
mechanical gate on motion quality, the way `npx impeccable detect` gates static design problems.

## Version notes worth knowing

As-of 2026-11: current line is **14.9.0** (14.8.0 dated 2026-10-29 — very active). The bundle
numbers: full `motion` component feature set **~43 KB**; `m` + `LazyMotion` initial render **as low
as 5 KB** with `domAnimation`/`domMax` feature bundles loaded separately; the site claims
"start at 3.2 kB with the mini `animate` function". In app code, the LazyMotion pattern is the
default — agents reaching for the 43 KB import out of habit is the defect to grep for. `spring`
accepts a **negative `bounce` from 0 to −1 to define overdamped springs**; `scroll`/`useScroll`
use the native **ScrollTimeline** for hardware-accelerated scroll-linked effects where available.
The paid Motion Studio added a reduced-motion mode that can edit a reduced-motion variant
independently of the full-motion one.

**Overdamped springs are the product-UI case.** A spring with negative bounce settles without
overshoot — the right choice for a panel or a popover in a Dense surface. Bouncy springs are a
`Persuade`-mode choice and belong to marketing.

## The floor still applies

Motion is a mechanics library, not a direction. Before shipping any motion in a product surface:

- Entrances decelerate, exits accelerate — asymmetric. Symmetric ease-in-out is a defect.
- Only `transform` and `opacity` animate. Animating `width`, `height`, `top`, or `left` is a jank source.
- Irreversible moments get no bounce. A confirm dialog is not a playground.
- Reduced motion must be real, not `animation: none`.

Motion UI (the paid tier's section/component library) ships `hero-editorial-stagger`,
`scroll-word-reveal`, and `footer-reveal`. Those are marketing surfaces — hand them to
`premium-marketing-design`.

## Not found

- **No published MotionScore scoring rubric.** Grades are S–F with a per-finding breakdown, but the
  weightings behind each grade were not found on the pages read.
- **No documented guidance on animation counts per surface.** There is no Motion equivalent of a
  "max N animated moments per view" rule; that remains house judgement from `craft-floor.md`.

## Sources

| Source | Publisher | URL | Accessed |
|---|---|---|---|
| Motion homepage, feature list, bundle claims, AI Kit/MCP | Motion | https://motion.dev/ | 2026-11-01 |
| Create accessible animations in React | Motion | https://motion.dev/docs/react-accessibility | 2026-11-01 |
| Motion repo (MIT license, rename notice, 14.9.0, LazyMotion/m sizes, ScrollTimeline) | Motion Division | https://github.com/motiondivision/motion | 2026-11-01 |

All API names, the `reducedMotion` values, and the changelog entries above are quoted from those
pages; bundle sizes are the project's own published figures (as-of 2026-11), not independently
measured.