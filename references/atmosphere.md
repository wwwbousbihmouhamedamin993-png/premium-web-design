# Atmosphere — declared field, gradient, and grain surfaces

Product UI's default atmosphere is **none**. Depth comes from surface steps and 1px hairlines
(`craft-floor.md`), and the Refuse list bans radial glow backgrounds, glassmorphism, and glowing
accents — because ambient decoration inside a work surface is slop with a GPU bill. This file governs
the single exception: a surface that **earns** an atmosphere moment, declares it in `DESIGN.md`, and
ships its static fallback.

A shader that exists because the screen looked flat is a decoration, not a design. The policy layer
here is adapted from `premium-mobile-design` `references/shaders-dithering.md`; the techniques are
rewritten web-native (CSS, SVG, canvas — never WebGL in product surfaces).

**Load this reference when:** an atmosphere moment, mesh gradient, aurora, grain overlay, or gradient
banding is considered for a product surface; a declared atmosphere block exists in `DESIGN.md`; or a
wide or dark gradient visibly bands.

**Done when:** every declared surface has a justification naming its job, an intensity token, a
trigger posture, a static fallback rendered in both appearances and under `prefers-reduced-motion`,
and every wide or dark gradient states its dither declaration — `none` is a valid declaration; a
missing one is a gap.

---

## 1. When atmosphere is earned — the governed exception

The craft-floor Refuse list stands. Atmosphere is earned by **exactly one** of two declarations, made
in `DESIGN.md` before the surface is built:

1. **A §1 signature move.** The field demonstrates the product's authored move — the gradient is the
   brand, the field is the identity. Named in `DESIGN.md` §1 (see `direction.md`) and carried here
   by the same name.
2. **Functional information.** The field *is* data — a `dataField` whose color and motion derive from
   the actual dataset, so the atmosphere carries information a static surface cannot. Name the job,
   not the look.

Everything else is refused. And the *where* is restricted before the *why* is even argued:

- **Allowed surfaces only:** onboarding, empty states, 404/error interstitials, first-load moments,
  upgrade/persuade surfaces (a `Decide` surface that sells), changelog/release notes. These are the
  product's stage moments — the places a person arrives, not the places they work.
- **Never behind work.** No atmosphere behind tables, forms, logs, charts' data area, or any
  Operate/Read working surface. Legibility and GPU cost on the interaction path both lose.
- **One moment per journey.** Stricter than one per surface: onboarding gets its one field; the
  upgrade page gets its own — a single session does not walk through three of them. The second
  atmosphere moment in a journey is the tell.

Five checks pass before a declaration is built:

- **One moment per journey** (above).
- **Never behind body copy, dense lists, or charts.**
- **Text gets a plate.** Any title, label, or control over a field sits on a scrim or static plate,
  and its contrast is measured against the **lightest and darkest frame** — in both appearances.
- **The static fallback exists before the field is built.** Render the paused frame first. If it is
  not a designed frame, the field is not ready.
- **The Swap Test.** Replace the product's colors and copy with another product's. If the field still
  reads as valid, it is generic atmosphere — rewrite or remove it.

The declared default is **none**. A family is opt-in, never inherited from a template or a component
library's decorative default.

### Relationship to the detector

`craft-floor.md`'s override table treats `radial-gradient-background-halo` as **advisory, not fail**,
on a surface carrying a declared atmosphere block (justification + intensity + fallback in
`DESIGN.md`) — on every other surface it still fails. Undeclared glow is slop wherever it appears.

---

## 2. The family table

Walk the decision tree in order; stop at the first answer that fits.

1. **Can a static surface do the job?** Then declare none. Atmosphere is not a finish pass.
2. **Is the job functional or expressive?** Functional means the surface carries information;
   expressive means brand presence on a stage surface.
3. **Functional → `dataField`.** Stop.
4. **Expressive →** an owned, dithered gradient: `staticGradient` (still) or `meshCSS` (structured
   multi-stop color). In product UI these do not idle-animate.
5. **Is it only texture?** That is `grainPlate`, not a field. Declare it under §4 and stop.
6. **Set intensity, trigger posture, and the static fallback.** A declaration with no fallback fails.

| Family | Job | Where allowed | Intensity token | Trigger posture | Static fallback |
|---|---|---|---|---|---|
| **Owned gradient** (`staticGradient`) | A brand-colored field on a stage surface; dithered per §3 | Onboarding hero, empty state, upgrade page | `atmosphere.gradient.intensity` 0.10–0.25 | Static — never idles | It is the fallback |
| **CSS mesh** (`meshCSS`) | Structured multi-stop color field, richer than one gradient | Same surfaces as `staticGradient`; one per journey | `atmosphere.mesh.intensity` 0.15–0.30 | Static; entrance may crossfade two baked fields (opacity only) | First frame, frozen |
| **Data field** (`dataField`) | Atmosphere derived from the real dataset — the field is information | Empty/briefing moments where the data has shape (activity summary, project overview) | `atmosphere.dataField.intensity` 0.20–0.40 | **Redraw on data change only, never per frame**; pause via `IntersectionObserver` when scrolled away | The current dataset rendered as a still |
| **Grain plate** (`grainPlate`) | Texture that kills the flat digital fill | Same stage surfaces; §4 scope rules | `grain.opacity` 0.03–0.08 | Static; no frame loop | It is already the fallback |

Implementation seams, in honesty:

- `staticGradient` and `meshCSS` are **CSS gradients** — `radial-gradient` / `conic-gradient` layers,
  baked stops (§3). A CSS gradient cannot be a real fragment shader and does not need to be; if a
  direction demands true fluid simulation, that is a marketing surface, not a product one.
- Motion on a mesh is **opacity-only crossfade between two pre-baked fields** (compositor-safe). Never
  animate gradient stop positions — that repaints every frame.
- `dataField` is a small **canvas 2D** render owned by the project: sample the dataset (bins, heat,
  activity), paint once per data change, respect DPR ≤ 2, pause off-screen. If it needs WebGL to look
  right, it does not belong in this skill's surfaces.
- **Bloom is refused** (craft-floor: glowing dark-mode accents), and there is no glass family —
  glassmorphism across content is already on the Refuse list.

`intensity` values above are house calibration; a product may re-tune them, but the token and the
fallback are not optional. An intensity of `0` is written `n/a — reason`, never as a zero-opacity
layer left in the tree.

---

## 3. Banding and dithering — including charts

Banding is posterization: the renderer rounds a gradient to the nearest available code value, and a
long, shallow ramp in dark tones exposes the steps. Eight bits per channel gives 256 levels; near
black, the first code steps are the largest luminance jumps. Dithering adds roughly **one 8-bit step —
1/255, about 0.39%** — of noise in quantization space immediately before rounding. It is a rendering
control, not a mood layer.

**When to dither — all three must be true:**

1. The gradient is product-owned and rendered (a token gradient, a canvas field) — not a photograph,
   illustration, or video.
2. It spans a long, shallow ramp (roughly a third of the viewport or more) or a wide dark field where
   banding is visible.
3. The output is 8-bit and the platform does not already dither the surface.

A short accent gradient on a known surface does not need it. A dark, full-bleed stage field does —
`craft-floor.md`'s near-black canvas (`#0E0E10`–`#141416`) with a subtle luminance ramp is exactly the
banding-prone case.

**The chart clause (product-specific, and the reason this file exists).** Gradient *scales* are data
surfaces: heatmap color ramps, area-chart fills, sparkline gradients, usage-arc gradients. On dark
canvases these band, and the banding reads as fake data contours. Dither the **field**, not the
content — mask data marks, text, and controls out of the dither pass. Noise over a glyph reduces
legibility; noise over a data mark corrupts the read.

**Techniques (web-native):**

| Technique | Use when | Avoid when |
|---|---|---|
| **SVG `feTurbulence`** (fractalNoise, tiled) as an overlay at ~0.4–1% effective opacity | Default for CSS gradient fields; no build step | The tile visibly repeats at the target scale |
| **Blue-noise tile** (pre-baked 128–160px data-URI, point-sampled) | Gradients and `dataField` outputs; isotropic, reads as fine grain | None in practice — bake it once |
| **Ordered / Bayer 4×4** baked at build time | Cheap static gradients in canvas output | Large flat fields — the crosshatch shows |
| **Error-diffusion (Floyd–Steinberg)** | Offline/baked assets only | Runtime; serial, not GPU-friendly |
| **Per-frame `getImageData` dithering** | Never | It is the effects.md perf rule — treatments bake once at load |

Four rules keep it honest:

- **Do not double-dither.** The browser compositing path may already apply dithering on some surfaces;
  audit the stack before adding a pass. One dither per final quantization.
- **Dither is not grain.** A calibrated dither is ~0.39% in quantization space; a grain plate is a
  3–8% alpha composite — an order of magnitude apart, doing different jobs. Never use grain to "fix"
  banding; never use dither to add texture.
- **Dither the field, not the content.** Charts and text are masked out (the chart clause above).
- **Match the output depth.** On wide-gamut/HDR pipelines the 1/255 amplitude is invisible and only
  costs fill — scale it or skip.

**Token contract** — the atmosphere block in `DESIGN.md` carries one row per treated gradient:

```
dither.mode        none | blueNoise | bayer4
dither.amplitude   1 step (0.39% in quantization)
dither.scope       <gradient token ids or surface ids>
dither.exclude     text, controls, chart marks
```

`dither.mode: none` is a valid, explicit declaration. A gradient with no declaration is a gap.

---

## 4. Grain policy

Grain is an aesthetic surface treatment: monochrome, static, and scoped. It is **not** a banding fix,
and it does not inherit the dither amplitude.

- **Static, full stop, in product UI.** A fixed tile is the shipped pattern — a 160×160 (or 128×128)
  monochrome tile at low opacity, repeated. Animated grain is refused here; the stage surfaces this
  file governs have no need for it.
- **One tile, not one bitmap.** Tile a small noise texture (`background-repeat`) or a tiled SVG
  `feTurbulence`; never ship a full-screen grain image. A 160×160 tile is acceptable; a 2880×1800 PNG
  is not.
- **Monochrome only.** Color noise introduces hues outside the token system.
- **Scope is part of the spec.** Stage surfaces only — onboarding hero, empty state, 404. Never over
  tables, forms, logs, or charts. A product with no grain declares `grain.scope: n/a — reason`; a
  grain declaration with no scope is rejected.
- **Near-black canvas lifts.** `craft-floor.md`'s dark canvas is not pure black, but grain still lifts
  a dark field toward gray. Scope grain to fields with a visible luminance ramp, or accept the lift
  deliberately and re-check the elevation story.

```
grain.opacity   0.03–0.08
grain.scale     160 or 128 (tile edge, px)
grain.scope     onboarding | emptyState | error404
```

**Hand-off:** image treatments — glyph, halftone, dither, duotone applied to *raster images* — live in
`unslop/effects.md` and stay there. This file owns rendered surfaces and gradients the product draws
itself.

---

## 5. Guardrails

**No idle loops in product UI.** An atmosphere surface is static, entrance-only (a one-shot opacity
crossfade at `--duration-slow`), or event/data-driven (`dataField` redraws). There is no 30fps ambient
loop here — product surfaces spend their frame budget on interaction, and an idle canvas loop on a
dashboard is the fastest route off this floor. If a direction genuinely needs continuous motion, it
belongs to a marketing surface.

**Pause when off-screen.** Any canvas or animated field observes `IntersectionObserver` and stops when
scrolled away — offscreen is the cheapest field. This is also the render-loop animation trap in
reverse: a field paused by `animations: 'disabled'` during capture must still be critiqued via its
static fallback, which is why the fallback exists.

**Reduced motion is a real variant.** `prefers-reduced-motion: reduce` renders the static frame — for
`meshCSS` the frozen first field, for `dataField` the current still. Contrast for plated text is
measured at the lightest and darkest frame in both appearances *before* the field ships, not after a
failure.

**Performance floor holds.** No atmosphere canvas may be the LCP element — paint the static fallback
first, hydrate the field after. Fixed aspect boxes (zero CLS). DPR capped at 2 for canvas fields.
`craft-floor.md`'s targets (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1) apply unchanged to any surface carrying
atmosphere. Bundle honesty: CSS/SVG fields cost ~0 kB; a `dataField` is project-owned canvas code; if
a proposal needs a WebGL runtime, it is a marketing surface — hand it to `premium-marketing-design`.

**Verify it in the render loop.** The active frame and the paused frame are both rendered; both
appearances are checked; `prefers-reduced-motion` is exercised; text contrast is measured over the
lightest and darkest frame; banding is checked at 100% zoom. The pass lives in `render-loop.md`
§"Atmosphere & dither pass".

---

## 6. Sources

| Claim | Source | Label |
|---|---|---|
| Earned-only shader doctrine, family/intensity/fallback contract, dither-vs-grain split, Swap Test, 0.39% amplitude, blue-noise default, grain 3–8% static 160px tile | `premium-mobile-design` `references/shaders-dithering.md` (policy origin, adapted — mobile skill retains the original) | Verified (its sources) |
| Banding worsens on longer/shallower ramps; 8-bit near-black steps | Colour banding (Wikipedia); Blender manual — via the mobile skill's sourced table | Claimed |
| `feTurbulence` fractalNoise / tiling | MDN SVG filter primitives | Verified |
| `prefers-reduced-motion` two values; vestibular targets | MDN (also cited in `radius-motion-tokens.md`) | Verified |
| IntersectionObserver pause; DPR ≤ 2 canvas cap | House rules, consistent with `render-loop.md` tooling and `unslop/effects.md` perf rules | House |
| Near-black canvas `#0E0E10`–`#141416`; no shadows on dark | `craft-floor.md` Color section | House |
| No idle rAF in product surfaces; WebGL refused in product | House rule — this skill's stance, stricter than the mobile policy it adapts | House |

A claim that cannot carry one of these labels does not enter this file.
