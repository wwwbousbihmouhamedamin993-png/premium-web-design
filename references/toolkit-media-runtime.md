# Toolkit — Media runtime in product surfaces (Lottie, video embeds)

Product UI plays media; it does not produce it. This file owns the **runtime** side — playing
designer-authored Lottie animations and embedding video inside a logged-in surface — under the same
adopt/refuse discipline as the other toolkits. Production of the assets (videos, voiceovers, 3D)
belongs to `premium-marketing-design`'s asset pipeline (`toolkit-asset-pipeline.md`); when the ask is
"make a product tour video", hand it off, then embed the result by the rules here.

---

## 1. Lottie — the AE-authored micro-animation path

Lottie plays After Effects animations exported as JSON (Bodymovin). It is the legitimate path for
**designer-supplied** micro-animations — empty-state illustrations, onboarding moments, success
ticks — when the motion is too organic to hand-code. It is never a substitute for code animation: if
CSS/Motion can express it, a Lottie file is dead weight.

**The runtime decision (as-of 2026-11):**

| Runtime | State | Verdict |
|---|---|---|
| `lottie-web` (airbnb) | MIT, v5.13.0 — **last release 2024-11; repo effectively dormant** (~298 KB raw / 75 KB gz) | Existing installs only; do not start new work here |
| `@lottiefiles/dotlottie-web` (+ `dotlottie-react`) | MIT, v0.82.x — actively developed; plays `.lottie` (compressed) and JSON; **~30 KB gz** (WASM core) | **Default for new work** — ~2.5× smaller gzipped |

```js
import { DotLottie } from '@lottiefiles/dotlottie-web';
const dot = new DotLottie({ canvas, src: '/anim.lottie', autoplay: false, loop: false });
```

**The mandates (all five, every install):**

1. **Decorative by default.** `aria-hidden="true"`, no tabindex, no role. If the animation carries
   information, the information must also exist as text — the Lottie is the garnish.
2. **Reduced motion pauses it.** The player does nothing about `prefers-reduced-motion` itself — gate
   autoplay behind the media query and render the final frame (`dot.setFrame(...)` + freeze, or a
   static poster). A spinning Lottie under reduced motion is a defect.
3. **Canvas renderer for anything heavy.** The SVG renderer explodes on complex comps (thousands of
   nodes); canvas for anything nontrivial, SVG only for tiny icon-scale loops.
4. **Compressed and lazy.** Ship `.lottie` (compressed), gzip on the wire, load below the fold or on
   interaction — never in the critical path of an Operate surface.
5. **The floor still applies.** One authored moment per journey (`radius-motion-tokens.md`
   session-gated rule: play on first view per session, rest state on repeat); no Lottie next to a
   Dense table; and it earns its bytes — a Lottie that animates what a token-styled SVG icon could
   is refused.

**Where it is allowed:** onboarding, empty states, success/celebration moments (`Decide`
confirmations of completed work). **Where it is refused:** Operate/Read working surfaces, inside
tables and forms, navigation chrome.

## 2. Video embeds in product surfaces

Video in a logged-in product is rare and specific: onboarding walkthroughs, "how this works" help
moments, release-note demos. The embed rules:

- **Never the LCP.** A poster image paints first (`craft-floor.md` performance floor); the player
  hydrates after. Poster `srcset`, explicit `width`/`height`, `aspect-ratio` reserved — zero CLS.
- **Below the fold: `loading="lazy"`** on the iframe, or a click-to-play facade (poster + play
  button that swaps in the iframe on demand) — the facade is the better default, it costs nothing
  until clicked.
- **Captions required.** `<track kind="captions">` or burned-in from the pipeline's WhisperX word
  timings — an uncaptioned product video is an a11y defect (`accessibility-web.md`).
- **Autoplay rules:** muted + `playsinline` or don't; and off entirely under
  `prefers-reduced-motion` (swap the poster). SC 2.2.2 applies — anything auto-playing past 5
  seconds needs a pause control that is not hover-only.
- **Self-host or gated third party.** A public YouTube/Vimeo embed in a product surface leaks the
  workspace's existence to third parties; prefer self-hosted MP4/WebM from the asset pipeline.

## 3. What does NOT belong in product surfaces

- **anime.js** — rarely; prefer CSS transitions and Motion (`toolkit-motion.md`). Its v4 timeline
  earns a slot only in non-React surfaces with genuinely sequential choreography needs, which an
  Operate/Read surface almost never has.
- **Three.js / WebGL / WebGPU / any shader runtime** — refused in product surfaces
  (`atmosphere.md`); the expressive stack lives in `premium-marketing-design`.
- **Remotion in the page** — Remotion is a *renderer* that outputs MP4; nothing Remotion ships in a
  web bundle. If a task says "Remotion" inside a product UI, the deliverable is a video file to
  embed by §2, produced via the marketing asset pipeline.

## Sources

| Source | Publisher | URL | Accessed |
|---|---|---|---|
| lottie-web repo (license, release history, renderer notes) | Airbnb | https://github.com/airbnb/lottie-web | 2026-11-01 |
| dotLottie-web (npm, bundle size, WASM core) | LottieFiles | https://github.com/LottieFiles/dl-x | 2026-11-01 |
| anime.js v4 docs (verdict basis: scope of API) | Julian Garnier | https://animejs.com/ | 2026-11-01 |

`**Not found:**` a first-party reduced-motion mode in either Lottie runtime — the gating is always
the host page's job.
