# Media, images, and avatars

Framing: images are the most-requested asset type on the web and the most common cause of layout
shift. web.dev, citing the HTTP Archive, reports images "are the most-requested asset type for most
websites, and they usually take up more bandwidth than any other resource. At the 90th percentile,
sites send over 5 MB of images on desktop and mobile." Everything below is about reserving space
before bytes arrive and keeping it reserved.

## The zero-CLS rule

MDN's usage note is operative: **"Use both `width` and `height` to set the intrinsic size of the
image, allowing it to take up space before it loads, to mitigate content layout shifts."** The
`height` attribute's entry explains why: "Including `height` and `width` enables the aspect ratio of
the image to be calculated by the browser prior to the image being loaded. This aspect ratio is used
to reserve the space needed to display the image, **reducing or even preventing a layout shift** when
the image is downloaded and painted to the screen." web.dev ranks the cause first: "The most common
causes of a poor CLS are: images without dimensions…"

Target: "sites should strive to have a CLS score of **0.1 or less**" — good is ≤0.1, poor is >0.25,
measured at the **75th percentile of page loads**, segmented across mobile and desktop (web.dev, CLS).
Shifts "within 500 milliseconds" of a qualifying interaction are excluded as expected (web.dev,
Optimize CLS) — chase first-load pop, not interaction reflow.

## Fixed aspect-ratio boxes, defined before load

Three layers, in order. **1.** `width` + `height` attributes on every `<img>` — gives the browser the
ratio before load. **2.** `aspect-ratio` on the wrapper: "At least one of the box's sizes needs to be
automatic in order for `aspect-ratio` to have any effect" (MDN); for a replaced element with
`aspect-ratio: auto 16/9`, "the given ratio is used until the content is loaded. After the content is
loaded, the auto value is applied" — so use the bare `16/9` (no `auto`) when the box must hold the
crop regardless of source. **3.** `object-fit` on the image: it "adjust[s] the sizing of the image
within the box (for example, whether the image should fit the box or fill it even if clipping is
required)," with `object-position` placing it in that box.

Avatars are the case where the ratio is fixed, not intrinsic: a 1:1 box, `object-fit: cover`,
`border-radius: 50%` from a token.

## `loading="lazy"`, and when not to

MDN: `lazy` "defers loading the image until it reaches a calculated distance from the viewport, as
defined by the browser. Lazy loading avoids the network and storage bandwidth required to handle the
image until it's reasonably certain that it will be needed." `eager` is the default.

`width`/`height` matter *more* for lazy images — MDN: "Lazy-loaded images will never be loaded if they do
not intersect a visible part of an element… because **unloaded images have a width and height of 0**. It
creates an even more disruptive user experience when the content visible in the viewport reflows in the
middle of reading it." Two more behaviours: "Lazy-loaded images located in the visual viewport may not yet
be visible when the `Window` load event is fired," because that event is based on eager-loaded images — so
don't gate first-screen measurement on `load` if any image there is lazy. And "Loading is only deferred
when JavaScript is enabled. This is an anti-tracking measure."

web.dev's caution: **"Don't lazy-load images that are likely to be in-viewport when the page loads,
especially LCP images."** Chromium's thresholds were reduced in July 2020 — "on fast connections (4G), we
reduced Chrome's distance-from-viewport thresholds from 3000px to **1250px** and on slower connections
(3G or lower), changed the threshold from 4000px to **2500px**" — with Chrome Android experiments finding
"on 4G, **97.5%** of lazy-loaded images were fully loaded within 10ms of becoming visible. Even on slow 2G
networks, **92.6%**." The threshold "varies depending on… the type of image resource being fetched" and
"the effective connection type." Attribute these to Chromium; they are not cross-browser guarantees.

Rule: **first screenful eager, below the fold lazy.** In a console, table-row avatars are lazy; the
workspace logo and record header image are not. For the one image that matters most use `fetchpriority`
— MDN allows `high`, `low`, `auto`; web.dev: "If you want to increase the fetch priority of an important
image (for example, the LCP image), use Fetch Priority with `fetchpriority="high"`." Never stack both:
"An image with `loading="lazy"` and `fetchpriority="high"` is still delayed while it's off-screen."

## `srcset` and `sizes`

web.dev's fallback rule: "Make the resource you specify in `src` large enough to work well on all device
sizes." MDN: `src` "is ignored in user agents that support `srcset` when `w` descriptors are included," and
with only `x` descriptors "the image referenced in the `src` attribute is counted as a 1x candidate." On
`sizes`, web.dev: it "tells the browser how wide the image will be when it's displayed, **though it doesn't
affect the image's display size, so you still need CSS for that**." MDN adds that a browser not recognising
`sizes` falls back to `src`, and that "(`sizes` and `srcset` were introduced at the same time, so every
browser supports either both attributes or neither.)"

```html
<img src="chart-1200.png"
     srcset="chart-400.png 400w, chart-800.png 800w, chart-1200.png 1200w"
     sizes="(width <= 640px) 100vw, (width <= 1024px) 50vw, 640px"
     width="1200" height="800" loading="lazy" alt="Revenue by quarter, Q1 to Q4 2026" />
```

web.dev's own recommendation on version count: "there is no single 'correct' answer… but it is common
to serve **3-5 different sizes** of an image." Its tooling: the `sharp` npm package, ImageMagick CLI, and
the hosted services Thumbor and Cloudinary.

## Modern formats, with fallbacks

From MDN's format guide, in its own comparative language: **AVIF** (`image/avif`) offers "much better
compression than PNG or JPEG," and "when using AVIF, you should include fallbacks to formats with better
browser support (i.e., using the `<picture>` element)." **WebP** (`image/webp`) is comparable, except
"AVIF offers slightly better compression, but is not quite as well-supported and **does not support
progressive rendering**." **JPEG XL** (`image/jxl`) has the same fallback requirement because "browser
support is not yet universal." **JPEG, PNG and GIF** keep broad historical support but show "poor
performance compared to newer formats." **SVG** (`image/svg+xml`) is "ideal for user interface elements,
icons, diagrams, etc., that must be drawn accurately at different sizes."

Two consequences for a product shell: **icons and empty states should be SVG** — MDN notes "SVG images
have no intrinsic dimensions if their root `<svg>` element doesn't have a width or height set on it," so
set them. And **serve `<picture>` with AVIF/WebP plus a JPEG or PNG fallback**, since MDN's own
compatibility notes are the justification, not preference.

## Blur-up placeholders

A blurred preview decorates a **reserved box**; it never substitutes for `width`/`height`. The wrapper
carries `aspect-ratio` and the placeholder as `background-image`, so the box exists in first paint; a tiny
placeholder (a few-hundred-byte low-res copy, or a dominant-colour fill computed server-side) paints
blurred via `filter: blur()`; the `<img>` loads with dimensions and `loading` set and fades in on its `load`
event, dropping the blur. There is no `onload` attribute in the HTML spec — attach a listener, and never
gate placeholder removal on anything but the image's own `load`.

**Not found:** no primary source specifies a placeholder byte budget, blur radius, or cross-fade duration.
Those are `DESIGN.md` decisions.

## Avatars

An ordered fallback chain, each rung a design surface. **1.** The uploaded image in a 1:1
`object-fit: cover` box, `alt` naming the person — MDN: for images that trigger an action, describe
**the action** (`alt="next page"` rather than `alt="arrow right"`), which in an avatar list means the
person, not the avatar. **2.** The identity provider's avatar image, if your product resolves one —
attribute to that provider's own behaviour and terms; do not assume it exists. **3.** Initials on a neutral
surface, uppercase, from a single normalised word, two letters not a full name: normalisation is
locale-sensitive — MDN notes `toUpperCase("ß")` is `"SS"` — so treat a name with no letters as its own
fallback. **4.** A neutral glyph if initials cannot be produced. Never fall back to the raw URL: MDN,
"When an `alt` attribute is not present on an image, some screen readers may announce the image's file
name instead."

## Broken-image handling

MDN enumerates when `error` fires — use it as the switch: "`src` or `srcset` attributes are empty (`""`)
or null; the `src` URL is the same as the URL of the page the user is currently on; the image is corrupted
in some way that prevents it from being loaded; the image's metadata is corrupted in such a way that it's
impossible to retrieve its dimensions, and no dimensions were specified in the `<img>` element's
attributes; the image is in a format not supported by the user agent."

- **Reserve the box still.** On error, swap in the initials or glyph inside the same `aspect-ratio`
  wrapper. The layout must not move.
- **`alt` is the last resort, not the design.** MDN: "Alt text is also displayed on the page if the image
  can't be loaded for some reason: for example, network errors, content blocking, or link rot." `alt=""`
  is meaningful: it "indicates that this image is not a key part of the content (it's decoration or a
  tracking pixel)," exposes the implicit role `presentation` instead of `img`, and "Visual browsers will
  also hide the broken image icon if the alt attribute is empty and the image failed to display."
- **Retry visibly, once** with backoff for a transient 5xx; then hold the fallback. Never loop. The
  fallback carries the same `alt`, so nothing is lost when the image never arrives.
- **Privacy:** cross-origin images default to a non-CORS request, so set `crossorigin` when the image
  must be readable from `<canvas>` and use `referrerpolicy` to control the `Referer` header (MDN). For
  third-party avatars this is a real lever.

## Sources

- [`<img>` HTML image embed element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img) — MDN, accessed 2026-10-05
- [`aspect-ratio` CSS property](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/aspect-ratio) — MDN, accessed 2026-10-05
- [Image file type and format guide](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types) — MDN, accessed 2026-10-05
- [`String.prototype`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String) — MDN, accessed 2026-10-05
- [Browser-level image lazy loading for the web](https://web.dev/articles/lazy-loading) — web.dev (Google), accessed 2026-10-05
- [Cumulative Layout Shift (CLS)](https://web.dev/articles/cls) — web.dev (Google), accessed 2026-10-05
- [Optimize Cumulative Layout Shift](https://web.dev/articles/optimize-cls) — web.dev (Google), accessed 2026-10-05
- [Serve responsive images](https://web.dev/articles/serve-responsive-images) — web.dev (Google), accessed 2026-10-05