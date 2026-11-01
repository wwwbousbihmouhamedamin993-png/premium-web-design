# Elevation layers

A logged-in B2B product is mostly flat. There is no hero floating over a photograph; the content is
dense and the page is a work surface. In that environment elevation is not decoration — it is the
mechanism that tells the user *what can be interacted with, what is on top of what, and what
dismisses what*. Most "the modal renders behind the header" and "the popover is invisible" bugs are
elevation bugs that were solved with a bigger `z-index` number.

This file is about **visual** elevation. For stacking order and the top layer, see
`z-index-layers.md`.

## Three tools, three jobs

| Tool | Answers | Works on dark ground? | In forced-colors? | Use it for |
|---|---|---|---|---|
| **Surface step** | "How far off the page is this?" | Yes — the primary dark cue | Yes | Every layered element |
| **Shadow** | "How far above, and from which light?" | Barely | **No — forced to `none`** | Light mode; transient states |
| **Border** | "Where does this end and that begin?" | Yes | Yes | Separators, control boundaries |

Material's framing is the one to adopt verbatim: "Elevation can be depicted using shadows **or other
visual cues, such as surface fills with a tone difference**" (Material Design 3, *Elevation*, accessed
2026-10-05). It also states two constraints most systems violate: elevation **tokens have no shadows
or colour** — each platform decides the actual values — and "stick to using a small amount of
elevation levels" (Material Design 3, *Elevation*, accessed 2026-10-05).

So the token is a *number*, not a shadow:

```css
--elevation-0: 0;   /* in-page content        */
--elevation-1: 10;  /* raised: hover, sticky  */
--elevation-2: 20;  /* overlay: popover, menu */
--elevation-3: 30;  /* modal: dialog, drawer  */
```

**Not found:** no primary source specifies numeric elevation levels or a maximum number of levels.
The four above are a house convention. What would settle them: a `DESIGN.md` decision, plus the
constraint that every level must be distinguishable in **both** modes and under `forced-colors`.

## The surface ramp

In light mode surface steps are nearly invisible, which is why they get ignored. They are the
load-bearing mechanism in dark mode and under high contrast:

| Step | Meaning | Light | Dark |
|---|---|---|---|
| `--surface-0` | The page itself | Ground | Ground (dark grey, not black) |
| `--surface-1` | Cards, panels, table containers | Ground + hairline | One step lighter |
| `--surface-2` | Menus, popovers, dropdowns | White + shadow | Two steps lighter |
| `--surface-3` | Dialogs, drawers, command palette | White + stronger shadow | Three steps lighter |

- **Monotonic in lightness.** Higher elevation is always lighter in dark mode (Material, *Dark
  theme*, accessed 2026-10-05) and always *at least equal* in light mode.
- **A surface step is a token swap, never an overlay.** The component does not paint translucent white
  on top of `--surface-1`.
- **One step per architectural boundary.** Two surfaces needing the same step are siblings, not parent
  and child.

## Shadows: three mechanics that change how you write them

`box-shadow` takes offset-x, offset-y, blur, spread, colour, plus optional `inset` (MDN, *`box-shadow`*,
accessed 2026-10-05). Three spec facts worth knowing:

1. **Negative blur is invalid.** `box-shadow-blur` is `<length [0,∞]>`; MDN: "Negative values are not
   allowed." To tighten a shadow, use negative **spread**.
2. **Zero offset plus zero blur is a ring, not a shadow.** When x-offset, y-offset, and blur are all
   zero, "the box shadow will be a solid-colored outline of equal-size on all sides" (MDN,
   *`box-shadow`*, accessed 2026-10-05). That is how to build a focus ring that follows
   `border-radius` — so a focus ring should be a zero-blur shadow or a real border, never an outline.
3. **Mismatched shadow lists do not animate.** If "in any pair of shadows, one has `inset` set and the
   other does not, the entire shadow list is uninterpolated; the shadows will change to the new values
   without an animating effect" (MDN, *`box-shadow`*, accessed 2026-10-05). Every elevation token must
   have the **same number of shadows and the same inset pattern**, or hover transitions snap.

The multi-shadow idiom for a believable stack — a tight contact shadow plus a wide ambient one:

```css
--shadow-1: 0 1px 2px rgb(0 0 0 / 0.06), 0 1px 3px rgb(0 0 0 / 0.10);
--shadow-2: 0 4px 8px rgb(0 0 0 / 0.08), 0 2px 4px rgb(0 0 0 / 0.06);
--shadow-3: 0 12px 24px rgb(0 0 0 / 0.12), 0 4px 8px rgb(0 0 0 / 0.08);
```

House rule: **higher elevation is softer and larger; lower elevation is crisper and smaller.**
Material states the same: "The shadow grows softer and larger as the object's elevation increases and
grows crisper and smaller as the elevation decreases" (Material Design, *Elevation & shadows*,
accessed 2026-10-05). Two shadows at the same softness imply two surfaces at the same height — the
ambiguity Material's own "Don't" example warns about.

## Borders are not a fallback for shadows

Borders get demoted to "the thing we use when shadows aren't available," and then fail in two places:

- **`forced-colors: active`** — `box-shadow` is forced to `none` (MDN, *`forced-colors`*, accessed
  2026-10-05). Every shadow-only component becomes invisible. MDN's fix is a border: `border: 2px
  ButtonText solid`.
- **WCAG SC 1.4.11** — non-text contrast. A boundary identifying a control requires 3:1 against
  adjacent colours; W3C's test procedure is to identify "the visual (non-text) indicators of the
  component required to identify that a control exists" and check contrast in each state (W3C WAI,
  *Understanding SC 1.4.11*, accessed 2026-10-05).

A subtlety in SC 1.4.11 that rewards reading carefully: the criterion does **not** require a visual
boundary if the control is identifiable another way — "If a control has visible content (such as text
or a sufficiently contrasting icon) which helps users identify the presence of the control, then a
border… is not required" (W3C WAI, *Understanding SC 1.4.11*, accessed 2026-10-05). So a text button
with no border can legitimately pass. A borderless **icon-only** button cannot: the glyph is the only
indicator, so its own contrast carries the requirement and there is no boundary to fall back on.

## The top layer is a different concept

The **top layer** "spans the entire width and height of the viewport and sits on top of all other
layers displayed in a web document" (MDN, *Top layer*, accessed 2026-10-05). The browser creates it for
fullscreen elements, `<dialog>` via `showModal()`, elements via `showPopover()`, and the drop-down
picker of a customizable `<select>` once opened. Elements in it generate a new stacking context, as do
their `::backdrop` pseudo-elements (MDN, *Top layer*, accessed 2026-10-05).

Two consequences: top-layer surfaces still need **visual** elevation — escaping the stacking hierarchy
says nothing about whether a dialog reads as above a menu — and the layer "is an internal browser
concept and cannot be directly manipulated from code" (MDN, *Top layer*, accessed 2026-10-05).

## `@layer` and stacking contexts are separate axes

**Cascade order** — `@layer` decides which *declaration* wins. MDN: "styles that are not defined in a
layer always override styles declared in named and anonymous layers," and "once the layer order has
been established, specificity and order of appearance are ignored" (MDN, *`@layer`*, accessed
2026-10-05). Layer order beats selector specificity entirely.

**Stack order** — stacking contexts decide what *paints* on top. "Elements within a stacking context
are stacked independently from elements outside of that stacking context," and child `z-index` values
"only have meaning within its parent's stacking context" (MDN, *Stacking context*, accessed 2026-10-05).

They interact: `@layer` sets cascade precedence, so a component in a higher layer wins its colour fight
without `!important` — and then `z-index` places it. Getting a colour override right by bumping
`z-index` is a category error; `z-index` has no effect on `background-color`. Declare the layer list
once, in one file, one order (`@layer reset, tokens, primitives, semantic, components, overlays;`);
first declared is lowest priority, `!important` reverses it, and re-declaring a name later appends rules
without changing the order (both MDN, *`@layer`*).

**Stacking contexts are created silently by many properties.** MDN's list includes `position: fixed |
sticky`, `container-type: size | inline-size`, flex/grid items with `z-index` other than `auto`,
`opacity < 1`, `mix-blend-mode` other than `normal`, any `transform`/`filter`/`backdrop-filter`/
`clip-path`/`mask` other than `none`, `isolation: isolate`, `contain: layout | paint`, and `will-change`
naming such a property (MDN, *Stacking context*, accessed 2026-10-05). So a card with
`transform: translateZ(0)` — a GPU-promotion trick — becomes a stacking context and breaks a sticky
header inside it. The ancestor is the bug; the `z-index` is not the fix.

**Not found:** no primary source specifies a maximum number of surface steps, a required lightness
delta between adjacent steps, or a required minimum blur ratio relative to offset. The four steps, the
two-shadow idiom, and the softening direction are house conventions grounded in Material's qualitative
rule. What would settle the numbers: measured contrast between adjacent surfaces, and screenshots at
each level in both modes.

## Verify

- Render every elevation level in light **and** dark. Each must be distinguishable without a shadow in
  dark mode.
- Toggle `forced-colors: active`. Every elevated surface must still read as elevated — this is the
  test that catches shadow-only components.
- Confirm each elevation token has the same shadow count and inset pattern as its neighbours.
- Grep for `outline:` used as a focus ring. Replace with a zero-blur shadow or border so it follows
  `border-radius`.
- Confirm no component sets `z-index` to affect colour precedence.
- Check every `transform`/`filter`/`opacity < 1` ancestor of a sticky or fixed element.
- Click through card → menu → popover → dialog. Each must read one step further forward.

## Sources

- Elevation (tokens have no shadows or colour; use a small number of levels; elevation may be depicted with surface fills/tone difference) — Material Design 3. https://m3.material.io/styles/elevation — accessed 2026-10-05
- Elevation & shadows (shadow grows softer and larger with elevation, crisper and smaller as it decreases) — Material Design. https://m1.material.io/material-design/elevation-shadows.html — accessed 2026-10-05
- Dark theme (shadows less effective on dark; elevation overlays lighten surfaces with elevation; dark grey not black) — Material Components for Android. https://github.com/material-components/material-components-android/blob/master/docs/theming/Dark.md — accessed 2026-10-05
- `box-shadow` (negative blur invalid; zero offset + zero blur is an equal-size outline; mismatched inset shadow lists are uninterpolated) · `forced-colors` (`box-shadow` forced to `none`; use a border instead) · `@layer` (unlayered normal outranks layered normal; re-declaring a name appends rules) — MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/box-shadow · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/forced-colors · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer — accessed 2026-10-05
- Top layer (spans the viewport; creates a stacking context; cannot be directly manipulated) · Stacking context (elements stack independently; properties that create one) — MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/Glossary/Top_layer · https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_context — accessed 2026-10-05
- Understanding SC 1.4.11 Non-text Contrast (boundaries not required when text or a sufficiently contrasting icon identifies the control; 3:1 for state indicators) — W3C Web Accessibility Initiative. https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — accessed 2026-10-05
