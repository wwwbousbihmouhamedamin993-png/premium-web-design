# Specimen — the design language on one page

Before any screen scope is declared on an `init` project, render the whole design language as one
reviewable page: `<project>/design-system.html`, built from
[`templates/system-specimen.html`](templates/system-specimen.html) and the token values in
`DESIGN.md`. The mandate is **item-level**: every §1–§14 item of `DESIGN.md` owns a section on the
page. Only §15 (Quick Reference & Verification Gate) stays off the page — it *is* the gate this page
must pass.

A design language reviewed as prose is a design language nobody confirmed. The specimen is where the
user sees every committed value rendered — and stops the ones they disagree with *before* they are
spread across twenty screens.

**Done when:** the user confirms the specimen, every §1–§14 item owns a section or an explicit
`n/a — reason`, the greps below are clean, and the confirmation date is recorded (a
`Specimen confirmed:` line in `DESIGN.md` §15 carries it from here).

---

## The three rules

1. **Token-faithful.** Every rendered value on the page is a `var()` referencing the token block
   emitted from `DESIGN.md` — no hand-typed hex, no magic spacing anywhere in the page's CSS. The
   `:root` block in the template is the only place literal values appear.
2. **Derived.** A correction found during review is a `DESIGN.md` edit plus regeneration of the
   page — never a hand-tweak of the HTML. Record the change in the `DESIGN.md` as-of comment. The
   page is disposable; the spec is the artifact.
3. **Coverage-visible.** An item the medium cannot demo (e.g. localization expansion) renders as a
   table or checklist; an item that does not apply carries an explicit `n/a — reason`. Silence is a
   gap, not an omission.

---

## What the page must demo (beyond the mobile pattern)

The mobile skill's specimen demos haptics and Dynamic Type; a web product's specimen demos what web
owns. These are the sections that make this page a *system* specimen:

- **Density classes side by side (§5, §12).** The same content — a heading, a paragraph, a row of
  controls — rendered three times at Focused, Standard, and Dense. This is the skill's defining
  mechanism; the page is where the user *feels* the three classes before any route inherits one.
- **Keyboard & focus strip (§13).** The focus ring rendered on every context it will ever sit on:
  canvas, raised surface, accent fill, dark canvas. A tab-through order strip demonstrating the
  `:focus-visible` style and the skip link. A focus ring that only works on one background is a
  defect the page catches for free.
- **Component variant × state matrix (§10).** Every committed component rendered across its states —
  default / hover / focus-visible / active / selected / disabled / loading / error — not described,
  rendered. Each block led by its one-line character statement from `DESIGN.md` §10.
- **Both appearances (§11).** The whole page re-themes from the token block alone — light and dark
  rendered from the same `var()`s, switched by the page's own toggle. If a semantic token has no dark
  value, the page shows the light value leaking and the gap is visible.
- **Data furniture.** A real table row set (tabular figures, right-aligned numerals, one selected
  row), a sparkline, and the status color ramp with its non-color glyphs — the surfaces this skill
  exists for, on the page.
- **Declared atmosphere with its static fallback (§1).** When `atmosphere.md` declares a family for a
  stage surface, the specimen renders the **static fallback frame** beside its declaration row
  (family, intensity, trigger, fallback, dither mode). A declared atmosphere with no rendered
  fallback fails the page.
- **The signature move (§1).** Demonstrated live where the medium allows, with its reduced-motion
  substitute rendered beside it; otherwise described with its trigger, keyboard path, and fallback.
- **Anti-patterns as struck don'ts (§14).** The product's own bans from `DESIGN.md` §14, each shown
  struck-through with its one-line reason — the refusal is part of the language.

---

## The stop-and-ask

When the page is built and clean, **stop and ask**:

> "Here is the whole design language on one page — `design-system.html`. Look at every section. What
> should change before any screen is built?"

Do not proceed to `screen`, `table`, `form`, or any build command until the user confirms. On an
`init` project the gate is absolute: until confirmation, the only files written are `PRODUCT.md`,
`DESIGN.md`, the token source, and `design-system.html` itself. A narrow refinement of existing UI may
proceed without the specimen, offering init afterward — the gate guards new scope, not maintenance.

Record the confirmation: `Specimen confirmed: YYYY-MM-DD` in `DESIGN.md` §15.

---

## Verify

- Grep the page for raw hex outside the token block — any hit is a defect (`tokens.md` gate, applied
  to the page itself).
- Render both appearances from the same token block; confirm no `var()` falls back to a literal
  because a dark value is missing.
- Confirm every `DESIGN.md` §1–§14 item owns a section or an `n/a — reason` — walk the list, print
  the mapping.
- Contrast: computed per pairing on the page's swatch grid, unrounded (`craft-floor.md` rule).
- `prefers-reduced-motion`: the page's motion demos have their static substitutes rendered beside
  them.

## Sources

| Claim | Source | Label |
|---|---|---|
| Specimen gate, stop-and-ask, token-faithful/derived/coverage-visible rules | House process adapted from `premium-mobile-design` `references/init.md` Phase 3.5 (mobile retains the original) | House |
| "Every rendered value is a `var()`"; token greps as defects | `tokens.md` token rules and gates — this skill | House |
| Unrounded contrast; focus ≥ 3:1 | `craft-floor.md` Color section (WCAG 2.2 SC 1.4.3 / 1.4.11) | Verified |
| Density classes as the defining mechanism | `craft-floor.md` / `information-density.md` | House |
