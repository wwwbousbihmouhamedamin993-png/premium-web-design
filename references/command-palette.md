# Command palette & global search

Applies to: the ⌘K / Ctrl+K layer in logged-in product surfaces — jump to any route, run a named action,
search entities without leaving the current screen.

## When to build one

Build a palette when at least two of these are true:

- The product has **many routes** and navigation is the bottleneck, not the feature set. This is the
single strongest justification: a palette is a search index over your own IA.
- There are **named actions** users repeat (create record, invite member, toggle a mode) with no
natural home in any toolbar.
- The app has **keyboard power users** who will find and expect ⌘K. Once a user learns one palette,
they look for it everywhere.

Do not build one for a product with a small, flat route set and a visible nav: the palette becomes an
undiscoverable second navigation system, and it competes for the same ⌘K chord the browser and OS use for
address-bar focus.

**The strong argument against is conflict**, not effort. APG treats shortcut conflicts as a first-class
hazard: it covers "Assigning and revealing keyboard shortcuts, including guidance on how to avoid
problematic conflicts with keyboard commands of assistive technologies, browsers, and operating systems"
(https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/). Bind to ⌘K / Ctrl+K — not ⌘P, ⌘N, ⌘F, ⌘O,
⌘T — and suppress it while focus is in a text field.

**Not found:** no primary source states a numeric threshold for "enough routes" or "enough commands"
to justify a palette. Settled by instrumentation — measure how often users fail to find a route via nav
before committing.

## The command list model

A palette is a flat, typed list of independently executable commands. Model it as data: `id`, `label`
(verb-first), `group`, `keywords[]`, `icon?`, `shortcut?`, `when?` (role, entity existence, feature flag),
`run()`.

Two properties are sourced rather than assumed:

- **Groups, not a flat list.** cmdk's `Command.Group` "groups items together with the given
`heading`", and its docs show a `<Command.Group heading="Recent">` block — recents are a *group*, not a
special control (https://dip-cmdk.mintlify.app/components/group).
- **Groups hide, they don't unmount.** "Groups will not unmount from the DOM, rather the `hidden`
attribute is applied to hide it from view" — and `forceMount` keeps a group permanently visible, which is
the mechanism for a pinned Recent section.

**Dynamic filtering.** cmdk's `shouldFilter={false}` disables built-in filtering "for server-side filtering
or virtualized lists", and `filter` takes a ranking function returning "a number between `0` and `1`, where
`1` is the best match and `0` hides the item entirely. Defaults to the built-in `command-score` algorithm"
(https://dip-cmdk.mintlify.app/components/command). That 0–1 range is the portable contract: rank, and treat
0 as exclusion.

## Fuzzy matching

**Not found:** no primary source specifies a fuzzy-matching algorithm, edit-distance threshold, or
subsequence rule for command palettes. What would settle it: a fuzzy-matching library's scoring
specification, so the behaviour is at least explicit. Until then:

- **Subsequence + ranking** is the behaviour users expect: `opst` finds "Open settings". Score by
match quality — contiguous > word-boundary > scattered.
- **Always render matched characters highlighted**, or the matching is invisible and unlearnable.
- **Never fuzzy-match the command's effect.** Match on label and keywords only, and do not reorder so
aggressively that the first keystroke surfaces an unrelated command. Pinned recents staying above fuzzy
results is the intended behaviour — which is exactly why `forceMount` exists.
- **Empty query shows recents and top commands**, not an alphabetical dump.

## Keyboard-only operation

A palette that cannot be driven from the keyboard is broken, because its discoverability mechanism is the
shortcut.

**Combobox semantics** (https://www.w3.org/WAI/ARIA/apg/patterns/combobox/) — the input carries
`role="combobox"`, `aria-controls` referencing the popup, `aria-expanded` `false`/`true`, and
`aria-autocomplete`. APG is explicit that `aria-controls` replaces ARIA 1.0's `aria-owns`: "it is strongly
recommended that authors use `aria-controls`." Elements with `role="combobox"` have an implicit
`aria-haspopup` of `listbox`; set `aria-haspopup` explicitly only for `grid`, `tree`, or `dialog` popups.

`aria-autocomplete` maps to one of three behaviours (APG):
- `none` — suggestions do not change with input
- `list` — suggestions complete or correspond to the typed characters
- `both` — as `list`, plus an inline completion string after the cursor

**Focus management is the non-obvious part.** For a listbox popup, "DOM focus remains on the combobox and
the assistive technology focus is moved within the listbox using `aria-activedescendant`". The combobox
carries `aria-activedescendant` referencing the active option. Also: "the popup indicator icon or button (if
present), the popup, and the popup descendants are **excluded** from the page `Tab` sequence" — so `Tab` out
of the input leaves the palette, it does not walk the results.

**Keyboard contract** (APG combobox, with cmdk's key map for the concrete bindings):

| Key | Action |
|---|---|
| `Down Arrow` | move focus into the popup / select next item |
| `Up Arrow` | select previous item (optional per APG) |
| `Alt+Down Arrow` | open the popup **without moving focus** (optional per APG) |
| `Alt+Up Arrow` | from inside the popup, return focus to the combobox and close |
| `Escape` | "Dismisses the popup if it is visible. Optionally, if the popup is hidden before `Escape` is pressed, clears the combobox." |
| `Enter` | accept the selected suggestion |
| `Home` / `End` | first / last option |
| printable chars | type into the input; focus stays in the input |
| `Tab` / `Shift+Tab` | leave the composite entirely |

*(https://www.w3.org/WAI/ARIA/apg/patterns/combobox/; https://dip-cmdk.mintlify.app/components/command for
`Alt+ArrowDown` group jumps, `Meta+ArrowDown`/`Home`/`End`, `Ctrl+N`/`Ctrl+J`/`Ctrl+P`/`Ctrl+K` Vim
bindings, and `loop` for wraparound)*

APG's warning about editing keys is a real bug source: "**Ensure JavaScript does not interfere with
browser-provided text editing functions by capturing key events for the keys used to perform them.**" A
palette that captures printable characters or arrow keys for navigation breaks typing and caret movement.
Also do not preventDefault on `/`-type "type to search" shortcuts without re-dispatching.

**The dialog layer.** If the palette renders as an overlay modal, it composes the modal dialog pattern
(https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/): role `dialog`, `aria-modal="true"`,
`aria-labelledby` to a visible title, `Tab`/`Shift+Tab` cycling within, `Escape` closing, focus returning to
the invoking element. And the condition on `aria-modal` is strict: mark it modal "**only** when both:
application code prevents all users from interacting in any way with content outside of it; **and** visual
styling obscures the content outside of it." A palette that traps focus but leaves a dimmed page clickable
is marked modal falsely — APG calls the result "severe negative ramifications" for users of some assistive
technologies.

cmdk's dialog mode "composes an accessible Radix UI Dialog" (https://dip-cmdk.mintlify.app/introduction),
which is the pattern: the dialog owns focus containment, the combobox owns list navigation.

**Recent commands**

**Not found:** no primary source specifies a recent-commands cap, ordering rule, decay policy, or
storage model. cmdk demonstrates a `Recent` group with `forceMount` but does not specify how recents are
populated or ordered. Settled by your own product decision.

- **Recents is a group with `forceMount`**, so it stays visible while the user types. If recents
vanish as soon as you type a character, the palette's fastest path disappears.
- **Recents must not outrank a deliberate match.** Pinned above, filtered below.
- **Search history is a different feature from command recents.** If the palette also searches
entities, recent *searches* need their own group so the two histories do not interleave.

## Accessibility wiring, assembled

```html
<button id="cmd-trigger" aria-haspopup="dialog" aria-expanded="false">Search</button>

<div role="dialog" aria-modal="true" aria-labelledby="cmd-title">
  <h2 id="cmd-title">Command menu</h2>
  <input role="combobox" aria-controls="cmd-list" aria-expanded="true"
         aria-autocomplete="list" aria-label="Command menu"
         placeholder="Type a command or search…" autocomplete="off">
  <ul id="cmd-list" role="listbox" aria-label="Suggestions">
    <li role="option" id="cmd-opt-1" aria-selected="true">Create project</li>
    <li role="option" id="cmd-opt-2" aria-selected="false">Go to Billing</li>
  </ul>
</div>
```

Every role and attribute above is named in https://www.w3.org/WAI/ARIA/apg/patterns/combobox/ (roles
`combobox`, `listbox`, `option`; `aria-controls`, `aria-expanded`, `aria-autocomplete`,
`aria-activedescendant`, `aria-selected`; label via `aria-label`/`aria-labelledby`) or
https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ (role `dialog`; `aria-modal`, `aria-labelledby`). Per
cmdk's group docs, group headings render `aria-hidden` "so it doesn't interfere with listbox accessibility
semantics" — accessible grouping comes from `aria-label` and the option set, not visual headings.

## APG's composite-widget frame

One APG principle underwrites the whole palette
(https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/): "`Tab` and `Shift+Tab` move focus from one
UI component to another while other keys, primarily the arrow keys, move focus inside of components that
include multiple focusable elements."

The palette is one composite. Its results are **not** 40 tab stops. If yours are, it is not a palette — it
is a list with a filter box, and it traps keyboard users inside a long options list.

## Review checklist

- [ ] Justified by route count and/or named repeated actions; not a second undiscoverable nav.
- [ ] Bound to ⌘K / Ctrl+K, conflicting chords avoided, suppressible in text fields.
- [ ] `role="combobox"` + `aria-controls` (not `aria-owns`) + `aria-expanded` + `aria-autocomplete`.
- [ ] `aria-activedescendant` moves AT focus; DOM focus stays on the input.
- [ ] Popup and its descendants excluded from the page tab sequence.
- [ ] `Escape` dismisses, then clears; focus returns to the trigger on close.
- [ ] Modal only if focus is truly blocked **and** content is visually obscured.
- [ ] No `keydown` preventDefault on text-editing keys.
- [ ] Commands grouped with headings; groups hidden via `hidden`, not unmounted.
- [ ] Recents pinned above matched results, still visible while typing.
- [ ] Matched characters highlighted.
- [ ] Every command has a visible name; icon-only commands get `aria-label`.

## Sources

- Combobox Pattern — WAI-ARIA Authoring Practices Guide (W3C) — https://www.w3.org/WAI/ARIA/apg/patterns/combobox/ — accessed 2026-10-05
- Dialog (Modal) Pattern — WAI-ARIA Authoring Practices Guide (W3C) — https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ — accessed 2026-10-05
- Developing a Keyboard Interface — WAI-ARIA Authoring Practices Guide (W3C) — https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/ — accessed 2026-10-05
- Command — cmdk documentation (dip/cmdk) — https://dip-cmdk.mintlify.app/components/command — accessed 2026-10-05
- Group — cmdk documentation (dip/cmdk) — https://dip-cmdk.mintlify.app/components/group — accessed 2026-10-05
- Introduction — cmdk documentation (dip/cmdk) — https://dip-cmdk.mintlify.app/introduction — accessed 2026-10-05
