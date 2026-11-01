# Iconography

Icons in a B2B product are a **vocabulary, not a garnish**. A dense admin surface communicates
through them — row actions, resource types, status, sort direction, disclosure. The failure mode is
not ugly icons; it is a product where `⋯` means "more actions" in one place and "open detail" in
another, or where stroke weights drift so the set reads as assembled from five sources.

## One family, one stroke weight, one grid

**One family.** Pick a single set and use it exhaustively. Material states the reason as a hard rule:
"**Consistency aids user comprehension of icons.** Use the existing system icons whenever possible and
across different applications" (Material Design, *Icons*, accessed 2026-10-05).

**One stroke weight, everywhere.** "Consistent stroke weights are key to unifying the overall system icon
family. **Maintain a 2dp width for all stroke instances**, including curves, angles, and both interior and
exterior strokes" — and the anti-pattern by name: "Don't use inconsistent stroke weights or rounded stroke
terminals" (Material Design, *Icons*, accessed 2026-10-05). Note what "for all stroke instances" excludes:
Material's stroke-terminal diagram distinguishes stroke terminals from counter strokes and specifies
**squared** terminals, so rounding them is an all-or-nothing decision across the set, never per-icon.

**One corner treatment.** "**A 2dp corner radius is used on the silhouette form of the icon. Do not round
the corners of strokes** (shapes 2dp wide or less)" (Material Design, *Icons*, accessed 2026-10-05). The
distinction is exact: corners belong to *shapes*, not to *strokes*. A set with rounded stroke ends and
square shape corners is already inconsistent.

## The grid and keyline alignment

Material's system icons display at **24dp**, "when creating icons, it's important to design at 100%
scale for pixel-perfect accuracy," with "**20dp**" for dense layouts where "the mouse and keyboard are
the primary input methods" (Material Design, *Icons*, accessed 2026-10-05).

The alignment rule is the one that actually surfaces in web CSS:

> "**Do** position icons 'on pixel' – meaning the X and Y coordinates are integers and do not contain
> decimals. Icons should have equal width and height (e.g. 24x24) to avoid distorting the icon."
>
> "**Don't** place the icon on a coordinate that is not 'on pixel'. Don't distort the icon by having
> unequal width and height values." (Material Design, *Icons*, accessed 2026-10-05)

For the web: **equal width and height on every icon**, integer SVG coordinates, no non-uniform scaling.
An icon stretched to fill a flex row is a defect, not a responsive fix — use `flex-shrink: 0` so a long
label cannot squash it. **Keylines** are construction guides, not output: Material's system-icon keyline
shapes are 18dp square, 20dp circle, 20×16dp vertical rectangle, and 16×20dp horizontal rectangle
(Material Design, *Icons*); a keyline is how you keep optical balance consistent across glyphs.

**House scale for this skill:** 16px for icons inside text-adjacent UI and list rows, 20px for Dense
toolbars and table row actions, 24px for standalone feature icons in Focused surfaces. All square, one
family, one stroke weight.

**Not found:** no primary source specifies a web-appropriate icon px size for B2B product UI or a
stroke width in CSS pixels. Material's 24dp/20dp and 2dp stroke come from a mobile design system and
translate to 24px/20px and 2px in CSS, but the 16/20/24 choice above is a house convention. What would
settle it: optical comparison against adjacent text at each size.

## Optical sizing — keeping a scaled icon from going heavy

Scaling a 24px outline icon up does not scale gracefully: the stroke grows with it, so a large icon
reads as **fatter** than the surrounding type rather than larger. Material describes exactly this — a
"large scaled icon [that is] too heavy compared to the original" — and its answer is the **optical size**
axis: "To make the image look the same at different sizes, the stroke weight (thickness) changes as the
icon size scales. Optical size offers a way to **automatically adjust the stroke weight** when you
increase or decrease the symbol size. Optical sizes range from 20dp to 48dp" (Material Design, *Icons*,
accessed 2026-10-05).

Two consequences. **Prefer a set with an optical-size axis** — Material Symbols exposes four adjustable
axes (weight, fill, grade, optical size), with weight ranging "between thin (100) and bold (700)"
(Material Design, *Icons*). **If your set has no optical-size axis, do not scale**: ship at the designed
size only and add a second size variant if needed. Scaled-up plain SVGs are where stroke-weight
inconsistency enters an otherwise disciplined system. Material also gives a floor worth honouring:
"Don't use the lightest weight for standard-size (24dp) icons. **The minimum weight for this size should
be 200**", plus the pairing rule "Use the same optical weight for your symbol and text" (Material
Design, *Icons*).

## Fill vs outline: a state channel, not a style preference

Use the two weights as a **selection channel**, consistently:

| Use | Treatment | Example |
|---|---|---|
| Default / available | Outline | Row actions, unselected nav, inactive filter chips |
| **Selected / active** | Fill | Active nav item, selected sidebar entry, on-state toggle |
| Alert / severity | Fill **plus** colour | Destructive action, error field state |

The rule that makes it legible: **fill must mean selected, everywhere.** If fill means one thing in the nav
and another in a table row, the channel carries no information. Selected state must not be signalled by
fill alone — WCAG SC 1.4.1 Use of Color and SC 1.4.11 Non-text Contrast both apply, so pair it with
`aria-current`/`aria-selected` and a non-colour cue. Fill also has a size floor: a filled glyph at 16px in a
Dense table often closes its counters and becomes a blob, so at 16px prefer outline and signal selection
with weight or background.

## Icon-only controls require a name

**WCAG SC 1.1.1 Non-text Content (Level A)** covers it: "If non-text content is a control or accepts user
input, then it **has a name that describes its purpose**" (W3C WAI, *Understanding SC 1.1.1*, accessed
2026-10-05). Situation C lists the techniques, including ARIA6 — "Using `aria-label` to provide labels for
objects" — and it applies to inline SVG exactly as to `<img>`: the W3C test rules include "SVG element with
explicit role has non-empty accessible name" and "Image button has non-empty accessible name."

**Hide the icon when text carries the name.** Polaris: "If the icon appears without text, then use the
`accessibilityLabel` prop to give the icon a text alternative" (Shopify Polaris, *Icon*, accessed
2026-10-05). Concretely:

```html
<button type="button">
  <svg aria-hidden="true" focusable="false"><!-- 16px glyph --></svg>
  Duplicate record
</button>
```

**When icon-only, name the action, not the shape.** Polaris: "For interactive icons, don't describe the
image ('magnifying glass'). Instead, describe the action ('search')" (Shopify Polaris, *Alternative
text*), and use `accessibilityLabel` when "the button has no text and relies on an icon alone to convey its
purpose" (Shopify Polaris, *Button*). Polaris also flags a trap: "make sure that the aria-label text
includes any button text that's visible. **Mismatches between visible and programmatic labeling can cause
confusion, and might prevent voice recognition commands from working**" (Shopify Polaris, *Button*).

**Icon-only is also a target-size obligation.** A 16px glyph in a 24px hit area passes; the same glyph in
a 20px hit area beside adjacent 20px controls fails. WCAG 2.2 SC 2.5.8 (AA) requires targets "at least 24 by
24 CSS pixels," with the **Spacing** exception allowing undersized targets only if "if a 24 CSS pixel
diameter circle is centered on the bounding box of each, the circles do not intersect another target" (W3C
WAI, *Understanding SC 2.5.8*, accessed 2026-10-05). Material's numbers: "Symbols of 24dp should have a
target size of 48dp by default," and "A 20dp size symbol can use a target size of 40dp" (Material Design,
*Icons*, accessed 2026-10-05).

**And the glyph is the only indicator, so it must meet non-text contrast.** SC 1.4.11 requires 3:1 for
information "necessary for a user to identify that a control is present," and W3C's worked example measures
a down-arrow icon at 4.7:1 against its button background (W3C WAI, *Understanding SC 1.4.11*). For a
borderless icon-only button, **the glyph itself** must clear 3:1 against the page background. **When to
drop the icon-only pattern:** if a control is the primary or destructive action on a surface it gets a text
label. Icon-only is for tertiary row actions, toolbar overflow, and disclosure — Polaris: "Use a tertiary
icon button for items and rows in a list or table" (Shopify Polaris, *Common actions*).

## SVG mechanics

**Theme with `currentColor`, not hardcoded hex.** `fill="currentColor"` means one icon file works in every
mode and state. This requires **inline** SVG; an `<img src="…svg">` cannot inherit.

**Never scale strokes with the box.** `vector-effect: non-scaling-stroke` makes "the element's drawn
stroke width… physically equal in size to its defined stroke width, even if the element has been scaled
up or down in size due to transforms of either itself or its coordinate system" (MDN, *`vector-effect`*,
accessed 2026-10-05). **Not found:** no primary source sets a stroke width in CSS pixels, nor prescribes
the `non-scaling-stroke` default across icon libraries; major sets (Lucide, Feather, Heroicons,
Phosphor) ship 24×24 or 22×22 viewBoxes with 2px strokes as a house convention, not a standard. What
would settle it: optical comparison against the adjacent label at each shipped size. Caution:
`vector-effect` behaves inconsistently inside **nested** `<svg>` elements in some engines — a documented
Firefox regression around v127 concerned exactly that (Mozilla Bugzilla bug 1903546, accessed 2026-10-05)
— so treat it as a progressive enhancement; the baseline is a correctly-sized, unscaled glyph.

**Set stroke-linecap and stroke-linejoin globally, once,** on the icon sprite or `.icon` class.
Per-icon overrides are how a set drifts.

## Verify

- Dump every icon path and count distinct sources. More than one family is a finding.
- Overlay two icons of the same family at different rendered sizes. Stroke must look the same weight.
  If not, the set needs optical sizing or fixed sizes only.
- Check every icon box is square (`width === height`) with integer SVG coordinates.
- Grep for `aria-hidden` on icons and `aria-label` on icon-only buttons. Any icon-only control without
  an accessible name is a finding.
- Read every `aria-label` on an icon-only control. If it names the shape ("trash can") instead of the
  action ("Delete record"), it is a finding.
- Measure every icon-only hit area against SC 2.5.8's 24px rule and its neighbours' clearance circles.
- Toggle dark mode and confirm no icon hardcodes a hex colour.
- Confirm `fill` appears only on selected/active state across the whole product.

## Sources

- Icons (24dp display; 20dp for dense keyboard-first layouts; keyline shapes 18/20/20×16/16×20dp; 2dp stroke for all stroke instances; 2dp silhouette corner radius, do not round stroke corners; squared stroke terminals; on-pixel integer coordinates and equal width/height; "don't use inconsistent stroke weights"; optical size 20–48dp; minimum weight 200 at 24dp; 24dp symbol → 48dp target, 20dp symbol → 40dp target) — Material Design. https://m1.material.io/style/icons.html — accessed 2026-10-05
- Icons — applying icons (outlined vs sharp styles; Material Symbols axes: weight 100–700, fill, grade, optical size; match optical weight to text) — Material Design 3. https://m3.material.io/styles/icons/applying-icons — accessed 2026-10-05
- `vector-effect` (`non-scaling-stroke` keeps stroke width constant under transforms and resizing) ·
  `vector-effect` SVG attribute (nested-SVG behaviour change in Firefox 127, restored in 134 per Bugzilla
  1903546) — MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/vector-effect ·
  https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/vector-effect — accessed 2026-10-05
- Understanding SC 1.1.1 Non-text Content (controls need a name describing purpose; ARIA6 `aria-label`;
  SVG-with-role and image-button test rules) · Understanding SC 1.4.11 Non-text Contrast (3:1 to identify
  a control; down-arrow at 4.7:1; no boundary required when visible content identifies the control) ·
  Understanding SC 2.5.8 Target Size (Minimum) (24×24 CSS px; 24px-diameter-circle Spacing exception) —
  W3C Web Accessibility Initiative. https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html ·
  https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html ·
  https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — accessed 2026-10-05
- Alternative text ("For interactive icons, don't describe the image — describe the action") · Button
  (`accessibilityLabel` for icon-only buttons; include visible text in the label to keep voice commands
  working) · Icon (`accessibilityLabel` when the icon appears without text) · Common actions ("Use a
  tertiary icon button for items and rows in a list or table") — Shopify Polaris.
  https://polaris-react.shopify.com/content/alternative-text ·
  https://polaris-react.shopify.com/components/actions/button ·
  https://polaris-react.shopify.com/components/images-and-icons/icon ·
  https://polaris-react.shopify.com/patterns/common-actions/best-practices — accessed 2026-10-05
