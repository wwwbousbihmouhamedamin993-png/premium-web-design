# Z-index and layers

Ad-hoc `z-index: 9999` is the single most common cause of "the modal renders behind the header" and
"the popover disappears inside a scroll container". The cause is not the number; it is that nobody
decided what the numbers mean. Two mechanisms fix it: a **named stacking scale** for app chrome,
and the **top layer** for anything that must escape all context.

## The stacking scale

Declare these once as tokens. Every overlay in the product takes a token, never a literal.

| Token | Layer | Typical members | Rationale |
|---|---|---|---|
| `--z-base` | `0` | Page content, cards, in-flow elements | Document flow |
| `--z-raised` | `10` | Hover elevation, lifted rows, dragged items | Above content, still in flow context |
| `--z-sticky` | `100` | Sticky headers, sticky table headers, sticky column, sticky sub-nav | Must survive scroll and sit over raised |
| `--z-dropdown` | `200` | Select menus, combobox popups, date pickers | Above sticky chrome; anchored to a field |
| `--z-popover` | `300` | Hover cards, rich popovers, preview panels | Above dropdowns |
| `--z-drawer` | `400` | Side panels, inspector panels, command surfaces | Above everything non-modal |
| `--z-modal` | `500` | Modal dialogs and their scrim (`::backdrop`) | Only above a drawer |
| `--z-toast` | `600` | Toast region | Above modals, never interactive-blocking |

Spacing rule: one step in the scale = one architectural boundary. Never skip a step, never
duplicate a value. If two components both claim `--z-dropdown`, one of them is really a popover.

**Backdrops belong to their surface's token, not their own.** A modal scrim sits at the same band as
its dialog (or exactly one below), never at a global "scrim" layer that drawers can also reach.

**Not found:** no normative source specifies numeric z-index values or spacing between them. Any
specific numbers above are a house convention; what matters is that they are tokens, ordered, and
enforced. Record the final values in `DESIGN.md`.

## Why ad-hoc values fail

Stacking is not global. MDN: "Elements within a stacking context are stacked independently from
elements outside of that stacking context"; each stacking context is "a single unit in the stacking
order of its parent stacking context", and "the `z-index` values of its child stacking contexts
only have meaning within its parent's stacking context" (MDN, Stacking context).

So `z-index: 9999` inside a `transform`ed card cannot beat `z-index: 1` on a sibling of that card.
MDN lists the property set that silently creates a stacking context — enough to make any hand-tuned
value wrong:

- root `<html>`
- `position: absolute | relative` **with** `z-index` other than `auto`
- `position: fixed | sticky`
- `container-type: size | inline-size`
- flex or grid item with `z-index` other than `auto`
- `opacity` less than `1`
- `mix-blend-mode` other than `normal`
- `transform`, `scale`, `rotate`, `translate`, `filter`, `backdrop-filter`, `perspective`,
  `clip-path`, `mask`/`mask-image`/`mask-border` — any value other than `none`
- `isolation: isolate`
- `will-change` naming such a property
- `contain: layout | paint` (and composites such as `contain: strict | content`)
- element in the **top layer** and its `::backdrop`
- `@keyframes`-animated stacking-context properties with `animation-fill-mode: forwards`

MDN's worked example shows the trap directly: a section with `z-index: 6` inside an article with
`z-index: 4` renders *under* an outside article with `z-index: 5`, because 6 only competes within
its parent's context (MDN, Stacking context).

`z-index` itself also has a hard precondition: it "sets the z-order of a positioned element and its
descendants or flex and grid items" (MDN, `z-index`), and an `<integer>` value "establishes a local
stacking context … the `z-index`es of descendants are not compared to the `z-index`es of elements
outside this element" (MDN, `z-index`). `z-index: auto` does not create one and sits at stack
level `0`.

Two product rules fall out:

1. **A component that needs a fixed or sticky position must not sit inside a `transform`, `filter`,
   `opacity < 1`, or `contain: paint` ancestor.** That ancestor is the bug, not the z-index.
2. **One overlay per stacking context.** A popover rendered inline inside a table cell inherits that
   cell's context and is clipped. Move it to the overlay root with the Popover API.

## The top layer, and why it beats z-index entirely

The **top layer** "spans the entire width and height of the viewport and sits on top of all other
layers displayed in a web document" (MDN, Top layer). It is created by the browser for:

- fullscreen elements (`Element.requestFullscreen()`)
- `<dialog>` shown via `showModal()`
- elements shown via `showPopover()`
- the drop-down picker of a customizable `<select>` once opened

Elements in the top layer generate a new stacking context, as do their `::backdrop` pseudo-elements
(MDN, Top layer). Because `showModal()` and `showPopover()` promote to the top layer, they escape
ancestor `overflow`, `transform`, and `z-index` entirely — no token needed and no clipping possible.

Practical consequences:

- **Modal dialogs and popovers: use the platform.** `showModal()` / `showPopover()` and stop
  maintaining a z-index scale for them. `--z-modal` and `--z-popover` remain for hand-rolled
  surfaces that cannot use the platform (a framework drawer inside a shadow root, say).
- The top layer "is an internal browser concept and cannot be directly manipulated from code" — you
  can target elements *in* it, not the layer itself (MDN, Top layer).
- Chrome surfaces top-layer entries as a separate DOM tree entry in DevTools (MDN, Top layer) —
  which is why "I can't find my popover in the DOM tree" is expected, not evidence of a bug.

## CSS `@layer` — the cascade, not the z-order

`@layer` does **not** order z-index. It orders *declaration priority*, and it removes the need to
fight specificity. MDN: rules within a cascade layer "cascade together"; "styles that are not
defined in a layer always override styles declared in named and anonymous layers"; and "once the
layer order has been established, specificity and order of appearance are ignored" (MDN, `@layer`).
The first layer declared gets the lowest priority, the last the highest, and `!important` reverses
that order (MDN, `@layer`).

How that helps this file:

```css
@layer reset, tokens, components, overlays;   /* precedence, low → high */

@layer overlays {
  .toast-region { z-index: var(--z-toast); }
  .modal-scrim  { z-index: var(--z-modal); }
}
```

Layer order is declared **once**, up front, and a component's layer position is fixed by that
declaration rather than by how specific its selector happens to be. A design system's overlay CSS
can be appended to `overlays` later (re-declaring the name appends rules without changing layer
order) and still win by position rather than by `!important` (MDN, `@layer`).

Rules for the team:

- Declare the layer list once, in one file, in one order. Never declare a layer name for the first
  time inside a component.
- `!important` inside a layer beats unlayered author declarations (MDN, `@layer`) — treat any
  `!important` inside `overlays` as a bug report against the layer list, not as a solution.
- Anonymous layers (`@layer { … }`) can never be appended to later (MDN, `@layer`) — name every
  layer.
- `@layer` is Baseline widely available (MDN, `@layer`) — safe to rely on; `@scope`-era tooling is
  not part of this contract.

## Verify

- Grep the codebase for `z-index` literals. Any hit outside the token definition file is a defect.
- Force-render each token: sticky header, open menu, open popover, open drawer, open modal, toast.
  All six must stack in scale order, top to bottom.
- Check no overlay clips inside a scrolling table: open a row action menu near the table edge.
- Check no sticky header is trapped: `opacity`/`transform`/`filter` on any ancestor of a sticky
  element is a finding.
- Toggle `container-type`, `filter`, and `contain` on ancestors in DevTools if an overlay misbehaves
  — that is usually the cause.

## Sources

- [Stacking context](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_context) — MDN Web Docs (Mozilla), accessed 2026-10-05
- [`z-index` CSS property](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/z-index) — MDN Web Docs (Mozilla), accessed 2026-10-05
- [Top layer](https://developer.mozilla.org/en-US/docs/Glossary/Top_layer) — MDN Web Docs (Mozilla), accessed 2026-10-05
- [`@layer` CSS at-rule](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer) — MDN Web Docs (Mozilla), accessed 2026-10-05