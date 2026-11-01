# Toolkit selection — five external toolkits, and the floor that governs them

Load when a task touches animation, charts, component sourcing, visual inspiration, or media
runtime (Lottie, video embeds). These sites are **tools with a floor**, not sources of truth. Adopt
their *mechanics*; refuse their *decorative defaults*.

| Toolkit | What it is | Adopt | Refuse |
|---|---|---|---|
| [motion.dev](https://motion.dev/) | Animation library (ex-Framer Motion), React/Vue/JS | Spring physics, reduced-motion plumbing, MotionScore audit | Playful/bouncy physics in product surfaces |
| [bklit.com](https://bklit.com/) | Data-visualisation components on a shadcn registry | Chart token architecture, composition pattern, 16 chart types | Decorative chart styling; charts where a number suffices |
| [godly.design](https://godly.design/) | Curated gallery of web/app/UI work | Direction-setting reference, esp. `/screenshots` | Copying composition wholesale into a product surface |
| [kokonutui.com](https://kokonutui.com/) | 100+ OSS components, shadcn registry + MCP | Registry/MCP install protocol, own-your-code model | Its default components — several are on the Refuse list |
| [toolkit-media-runtime.md](toolkit-media-runtime.md) | Lottie/dotLottie playback + video embed rules | The runtime mandates (a11y, reduced-motion, poster-first) | Lottie as a substitute for code animation; uncaptioned or LCP video |

**The boundary line.** The 3D/WebGL stack (three.js, postprocessing, pathtracing, physics, Paper
Shaders) and the video/asset production pipeline (Remotion, FFmpeg, ComfyUI, Blender MCP, voice and
caption tooling) do **not** belong to this skill — product surfaces refuse WebGL entirely
(`atmosphere.md`), and assets are produced, not rendered in the page. They live in
`premium-marketing-design` (`toolkit-three.md`, `toolkit-asset-pipeline.md`); this skill embeds
their *outputs* under `toolkit-media-runtime.md`.

## The conflict you must resolve every time

**Two of these four ship defaults that this skill's floor refuses.** That is not a reason to skip
them — it is the reason the floor exists.

Kokonut's own component names include `liquid-glass-card`, `shimmer-text`, and `particle-button`.
Those are glassmorphism and gradient treatments, which `craft-floor.md` refuses inside product
surfaces. Motion UI ships "animated sections" led by `hero-editorial-stagger` and
`scroll-word-reveal` — marketing-page motion, wrong for an Operate or Dense surface.

So the rule is mechanical, not aesthetic:

1. **Never let a component library choose the direction.** The library supplies mechanics —
   a spring solver, a chart primitive, a registry entry. `screen.md` supplies the composition.
2. **Adopting a component is adopting its *behaviour*, and you still owe it the floor.** Install a
   component, then run the Refuse list against it. If it fails, restyle through tokens or don't use it.
3. **A stock component inside a committed surface is a lapse** — the same rule
   `component-consistency.md` sets for any other default.
4. **Marketing-only components are out of scope here entirely.** If it is a hero, a word-reveal, or a
   scroll-driven section, it belongs to `premium-marketing-design`.

## When each is the right answer

**Motion** — when motion is load-bearing: layout transitions, presence/exit, gesture response, shared-element routing. Not for product surfaces that should feel instant. Reach for `radius-motion-tokens.md` first; reach for a library when you need spring physics or `AnimatePresence`-class exit handling that CSS cannot express.

**Bklit** — when the surface genuinely needs a chart (see `charts-data-viz.md` for whether it does). Before installing, check whether a stat tile in `metrics-stat-tiles.md` answers the question instead — most dashboard needs are not charting needs.

**Godly** — at direction-setting time only, and specifically `/screenshots` for logged-in app UI rather than `/websites`, which is marketing work this skill does not own. Use it to answer "what would the best version of this look like", then close the tab and build from the brief.

**Kokonut** — for mechanical scaffolding under time pressure: a date picker, a combobox, a data table. Never as the visual identity of a surface.

## Licensing and posture

- **Motion** is MIT-licensed and open source. Its paid tier (Motion+, Motion Studio) is optional; the mechanics this skill needs are in the free library.
- **Bklit** is open source and a Vercel OSS Program participant.
- **Kokonut** is 100% free and open source with a separate paid Pro tier of templates/components.
- **Godly** is a gallery. Its *images* are other people's work; see `design-systems/LICENSE-NOTES.md` for the same provenance discipline this skill applies to its own screenshots.

**Prefer the registry over the gallery.** Kokonut and Bklit both ship a machine-readable shadcn
registry and an MCP server, which means an agent can install source it can read and modify. That is
strictly better than copying a snippet from a gallery page — you get the code, not the picture.

## Sources

| Source | Publisher | URL | Accessed |
|---|---|---|---|
| Motion homepage and changelog | Motion | https://motion.dev/ | 2026-10-05 |
| Create accessible animations in React | Motion | https://motion.dev/docs/react-accessibility | 2026-10-05 |
| Bklit UI homepage | Bklit | https://bklit.com/ | 2026-10-05 |
| Skills | Bklit UI | https://bklit.com/docs/skills | 2026-10-05 |
| Godly Design Inspiration homepage | Godly | https://godly.design/ | 2026-10-05 |
| Kokonut UI homepage | Kokonut UI | https://kokonutui.com/ | 2026-10-05 |

Component and API names in the companion files are quoted from these pages. Anything beyond them is
marked `**Not found:**` there.