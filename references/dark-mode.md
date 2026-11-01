# Dark mode

Dark mode is not an inversion filter applied to a light theme. It is a **second theme with its own surface
ramp, its own border weight, its own shadow behaviour, and its own accent budget**. The most common defect
— light colours fed through `filter: invert()` or a lightness flip — produces text that is technically
inverted and perceptually wrong, because dark mode's problems are not hue problems.

Everything here is a **semantic token remap**: the semantic layer is declared twice, and only the second
declaration differs. No component CSS changes between modes.

## Why the light ramp cannot be inverted

Material states the failure mode in one line: "**Shadows are less effective in an app using a dark
theme, because they will have less contrast with the dark background colors and will appear to be less
visible**" (Material Components for Android, *Dark theme*, accessed 2026-10-05). A shadow is a dark region
cast on a lighter ground; darken the ground and the shadow disappears — every depth cue built from shadow
vanishes silently. Material's baseline dark background and surface colours "**are dark grey instead of
black, which increases visibility for shadows and also reduces eye strain for light text**" (Material
Components for Android, *Dark theme*) — both halves matter, since pure black ground also hardens contrast
against light text.

| Property | Light | Dark | Why |
|---|---|---|---|
| Ground | White / near-white | Dark grey, **not pure black** | Shadow visibility and eye strain |
| Surface ramp | Shadow + subtle tint | **Lighter surface** per step | M3 "represents elevation mainly using tonal color overlays… increasing tonal elevation uses a more prominent tone" (Android Developers, *Material Design 3 in Compose*) |
| Borders | Very subtle, near-invisible | **Stronger** than intuition suggests | Borders become the primary separator once shadows are gone |
| Accent | Saturated brand hue | Desaturated / lightened | Saturated hues glow on dark ground and shift perceived hue |
| Scrims | Black at low alpha | Black at **higher** alpha | Less light to darken |
| Charts | Series separated by hue | Need lightness separation too | Two series often land at the same apparent lightness |
| Images and media | Default | Reduced brightness or slight desaturation | Stops glaring against a dark ground |
| Focus ring | Accent outline | 3:1 against the surface; accent-on-accent buttons need an inner light ring | SC 1.4.11 |

**In dark mode, elevation is encoded as lightness.** Material encodes it as a semi-transparent
primary-coloured overlay whose alpha rises with elevation, so higher surfaces get lighter (Material
Components for Android, *Dark theme*). Any web implementation achieves the same with a three- or
four-step surface ramp; what matters is that the ramp is **monotonic in lightness** — step 4 is always
lighter than step 3.

**Borders must get stronger, not weaker.** Because shadows have stopped separating things, the hairline is
now load-bearing: a `--border-subtle` barely-there in light mode becomes an invisible grid in dark mode.
WCAG SC 1.4.11 requires 3:1 for "visual information provided that is necessary for a user to identify that a
control is present" (W3C WAI, *Understanding SC 1.4.11*, accessed 2026-10-05), and a hairline below that
fails in either mode. Charts are the most-missed item: validate every series against its actual dark
background, not the light one.

## The mode dimension, and where it cannot live

The token architecture from `color-token-system.md` does the work: primitives declared once, semantics
declared **twice**, components referencing semantics only. **Tailwind v4 constraint that shapes this:**
`@theme` variables "must be top-level" and cannot nest under selectors or media queries (Tailwind CSS,
*Theme variables*, accessed 2026-10-05). The mode dimension therefore **cannot live in `@theme`** — it must
live in `:root` / `.dark`, with `@theme inline` bridging references. A theme block attempting to express
"and when dark" is invalid.

```css
@layer reset, tokens, primitives, semantic, components;

@layer semantic {
  :root {
    --color-surface:        #ffffff;
    --color-surface-raised: #ffffff;
    --color-on-surface:     #16181d;
    --color-border-subtle:  rgb(0 0 0 / 0.08);
    --color-accent:         oklch(0.52 0.19 258);
  }
  .dark {
    /* Ground is dark grey, not black. Ramp rises in lightness. */
    --color-surface:        oklch(0.20 0.01 258);
    --color-surface-raised: oklch(0.24 0.012 258);
    --color-on-surface:     oklch(0.96 0.005 258);
    /* Border is STRONGER than the light value, not weaker. */
    --color-border-subtle:  oklch(0.38 0.012 258);
    /* Accent is lightened and desaturated. */
    --color-accent:         oklch(0.72 0.13 255);
  }
}
```

Two structural rules make this maintainable. **The remap is a whole block, not a diff:** every semantic
token that changes gets a line in `.dark`; a token absent from `.dark` inherits the light value, correct
only if that value genuinely works in both modes — there is no third state. And **never branch component
CSS on the mode:** no `.dark .button { … }`. If a component needs mode-specific styling, it needs a
semantic token that is remapped, not a selector. **Do not use `light-dark()` as the primary mechanism** —
it is Baseline 2024 *Newly available*, materially less mature than `prefers-color-scheme`, `color-scheme`,
`@property`, or `@layer` (MDN, *`light-dark()`*, accessed 2026-10-05). Use it only as progressive
enhancement behind `@supports`.

## `color-scheme`, the meta tag, and the FOUC-free toggle

**`color-scheme` is inherited and only repaints user-agent chrome.** When set, the user agent adjusts
"form controls, scrollbars, and the used values of CSS system colors" (MDN, *`color-scheme` property*,
accessed 2026-10-05). It does **not** theme the document — MDN is explicit that "Component authors must use
the `prefers-color-scheme` media feature to support the color schemes on the rest of the elements." Apply
it to `html` / `:root`, not `body`: browsers "look to the root element to determine the theme for the
entire viewport — including the root scrollbars and the initial 'canvas' background"; applied only to
`body`, those surfaces stay light (GoogleChrome/modern-web-guidance, *dark-mode*, accessed 2026-10-05).

**The `<meta>` tag must precede all CSS.** MDN: include `<meta name="color-scheme">` in `<head>` "before any
CSS style information, to inform user agents about the preferred color scheme, helping prevent unwanted
screen flashes during the page load" (MDN, *`color-scheme`*, accessed 2026-10-05) — i.e.
`<meta name="color-scheme" content="light dark">` as the first element in `<head>`, ahead of every
stylesheet link. Note Google's own caveat, the honest version of "prevents FOUC": the tag "may not
completely eliminate flashes in all browsers or loading conditions" (GoogleChrome/modern-web-guidance,
*dark-mode*). It sets the initial canvas early; it guarantees nothing.

The flash proper happens when a stored preference is applied by JavaScript *after* first paint. The fix is
an **inline, synchronous script in `<head>` that sets the mode before any stylesheet applies**, plus a class
on the root so CSS can branch. Three specifics from Google's guidance, all load-bearing: the script **must
not be `type=module` and must not be `defer`**, because both postpone execution past first paint; it
**must update the `<meta>` tag's `content`**, not only a class; and **CSS must default to the system
preference**, with overrides for the user's pinned choice, so the site still honours the OS setting if
JavaScript fails.

```html
<script>
  // Synchronous, inline, in <head>, before any stylesheet.
  {
    const stored = localStorage.getItem("color-scheme");
    if (stored) {
      document.documentElement.classList.add(stored);
      document.querySelector('meta[name="color-scheme"]').content = stored;
    }
  }
</script>
```

```css
:root { color-scheme: light dark; }

@media (prefers-color-scheme: dark) { :root { /* dark semantics */ } }
:root.dark  { /* dark semantics  — class overrides the media query */ }
:root.light { /* light semantics — class overrides the media query */ }
```

Because a class selector and a `:root` media-query rule differ in specificity, the class wins when present
and the media query governs when it is not. **Do not** set `color-scheme: light` or `dark` on the root by
default — Google's guidance says the default MUST be the system preference, which `color-scheme: light dark`
already produces.

**If JavaScript reads the preference, it must also listen for change.** "If you are using JS to read
`matchMedia("(prefers-color-scheme: dark)")`, you MUST also use `addEventListener("change", fn)`… CSS
automatically adapts to changes" (GoogleChrome/modern-web-guidance, *dark-mode*). CSS-only theming has no
change-listener bug; JS-driven theming does. **Server-rendered alternative:** the `Sec-CH-Prefers-Color-
Scheme` client hint lets the server obtain the preference at request time and inline the correct CSS,
"therefore avoid[ing] a flash of incorrect color theme" (web.dev, *`prefers-color-scheme`: Hello darkness*,
accessed 2026-10-05).

**Not found:** no primary source specifies a maximum acceptable theme-switch flash duration, a canonical
storage key or precedence order for pinned-vs-system theme, or a required number of steps in a dark surface
ramp. The three-step ramp, the `.dark`/`.light` class precedence, and the storage key are house
conventions. What would settle them: a `DESIGN.md` decision plus Lighthouse measurement of first-paint
stability under a forced dark preference.

## Accessibility modes beyond light/dark

Dark mode is one axis of three. The others ship too, both Baseline *Widely available* (MDN, accessed
2026-10-05): **`prefers-contrast`** (values `no-preference`, `more`, `less`, `custom`; MDN,
*`prefers-contrast`* — bump border and text contrast under `more`) and **`forced-colors`** (`active` /
`none`). The critical warning for anyone relying on elevation cues: in forced-colors mode **`box-shadow` is
forced to `none`**, as are `text-shadow`, non-URL `background-image`, `color-scheme`, and
`scrollbar-color` (MDN, *`forced-colors`*, accessed 2026-10-05). Any component whose only depth cue is a
shadow becomes **completely flat** in Windows High Contrast — which is why borders must exist independently
of shadows in *both* modes. MDN advises authors **not** to build a separate design for forced-colors: "its
intended usage is to make small tweaks" (MDN, *`forced-colors`*). The smallest correct tweak is MDN's own
example: swap the shadow for a border.

## Verify

- Load with the OS in dark mode and no stored preference. The first paint must already be dark.
- Hard-reload with a stored `dark` preference while the OS is light. Any white flash is a FOUC bug.
- Confirm `color-scheme` is on `:root` and the `<meta>` precedes the first stylesheet link.
- Screenshot the surface ramp: step 4 must be lighter than step 3, always.
- Measure every dark-mode border against its surface. Under 3:1 fails.
- Enable high-contrast mode and confirm no component becomes invisible.
- Confirm no component stylesheet contains `.dark` or `[data-theme]`.

## Sources

- Dark theme (shadows less effective on dark; dark grey not black baseline; elevation overlays lighten with elevation) — Material Components for Android. https://github.com/material-components/material-components-android/blob/master/docs/theming/Dark.md — accessed 2026-10-05
- Material Design 3 in Compose (elevation mainly tonal overlays) · ElevationOverlay ("where shadows are not as visible") — Android Developers. https://developer.android.com/develop/ui/compose/designsystems/material3 · https://developer.android.com/reference/kotlin/androidx/compose/material/ElevationOverlay — accessed 2026-10-05
- MDN: `color-scheme` (UA chrome only; apply to `:root`; `<meta>` before CSS) · `prefers-color-scheme` · `light-dark()` (Baseline 2024 Newly available) · `forced-colors` (`box-shadow` forced to `none`) · `prefers-contrast`. https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/light-dark · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/forced-colors · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-contrast — accessed 2026-10-05
- dark-mode guide (MANDATORY root `color-scheme`; MANDATORY `<meta>`; inline non-module non-defer script; CSS defaults to system preference; MUST listen for OS change) — GoogleChrome/modern-web-guidance. https://github.com/GoogleChrome/modern-web-guidance-src/blob/main/guides/user-experience/dark-mode/guide.md — accessed 2026-10-05
- `prefers-color-scheme`: Hello darkness, my old friend (`Sec-CH-Prefers-Color-Scheme`) — web.dev. https://web.dev/articles/prefers-color-scheme — accessed 2026-10-05
- Theme variables (`@theme` must be top-level) — Tailwind CSS. https://tailwindcss.com/docs/theme — accessed 2026-10-05
- Understanding SC 1.4.11 Non-text Contrast (3:1) — W3C WAI. https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — accessed 2026-10-05
