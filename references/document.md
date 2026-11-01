# Document — generate DESIGN.md from an existing codebase

Reverse-engineer the incumbent design system into `DESIGN.md` so future sessions inherit decisions
instead of re-deriving them. The output records **rules that survive**, not a catalogue of one-offs.

House process: this is `premium-mobile-design`'s `document` command adapted to web. The mobile skill's
shape — inventory tokens, inventory components, record rules, note drift honestly, keep it durable —
is preserved. Everything web-specific below (token *sources*, incumbent palette detection, density
identification, handling an inconsistent incumbent) is added for this skill. The CSS and WCAG facts are
sourced; the procedure is house process.

As-of: 2026-10-05.

**Do not run this on a codebase with no established system.** That is `init`, not `document`. The
difference: `document` records what is *already true*; `init` decides what *should* be true.

---

## 1. Find the token sources first

Everything downstream reads from these. Search in this order and stop at the first hit per category.

| Look for | Where | What it tells you |
|---|---|---|
| Tailwind v3 | `tailwind.config.*` (`theme.extend`) | scale + palette in JS |
| Tailwind v4 | `@theme` / `@theme inline` in CSS | scale as CSS custom properties |
| Plain CSS custom properties | `tokens.css`, `theme.css`, `:root` blocks | scale as CSS variables |
| Design-token files | `tokens.json`, `*.tokens.json` (DTCG format) | typed, layered, possibly generated |
| CSS-in-JS theme | `theme.ts`, `createTheme`, `styled-components` theme, `ThemeProvider` | typed object, maybe per-mode |
| Component-library theme | MUI `createTheme`, Chakra, Mantine, Polaris `theme` | the incumbent is *the library's* system |
| Storybook | `.storybook/preview.js` globals | the values designers actually use |
| Figma export | `theme.less`, `variables.json` | design source of truth, if code lags |

**Read in this order:** the token source → the global stylesheet → one dense surface (a real table
route) → one Focused surface (auth or a form) → the shared component directory. Reading the marketing
site tells you about the brand; reading a table route tells you about the product.

**Record which source is canonical.** If Figma and CSS disagree, say so in the file — that
disagreement is itself the finding.

## 2. Extract the incumbent palette

- **Collect** every colour literal in the token source, grouped by family. Count occurrences — a hex
  used once is a one-off, not a token.
- **Infer roles from usage, not from names.** A value used as `background` on 40 surfaces is
  `surface.canvas` even if it is called `--grey-50`. Map it into the Layer 2 role vocabulary from
  `tokens.md`, and keep a `legacy name → role` column so the rename is mechanical later.
- **Detect the accent budget in practice.** Grep for the accent hex; count instances per file. If one
  route has five filled accents, the incumbent budget is five — record that as **known drift**, not as
  the rule.
- **Find the status system.** Look for success/warning/danger/info tokens and check each one actually
  ships with a non-colour cue in the components. A `danger` red used alone in a toast is drift.
- **Check dark mode honestly.** Is there a second ramp, or is dark a filter? Is `color-scheme` set? Is
  `<meta name="color-scheme">` present in the head *before* the stylesheet (MDN, `color-scheme`)?
  Border strength in dark is the tell — a 1px hairline that reads as delicate on white usually reads
  as invisible on near-black, so if dark borders are the same value as light, dark was filtered.

## 3. Extract the type ramp

- **List every distinct `font-size` / `line-height` / `font-weight` triple in use**, with occurrence
  counts. That histogram *is* the ramp, warts included.
- **Identify the density class from the code, not from a declaration.** Measure the table row height,
  the base body size, and the measure on a real route, then read the class off the table:

  | Class | Surfaces | Base body | Row height | Measure |
  |---|---|---|---|---|
  | **Focused** | Auth, onboarding, checkout, single-form flows, settings detail | 16px | — | 60–70ch, centered |
  | **Standard** | Project home, card+list feeds, record detail | 14–15px | 40–44px | 65–80ch |
  | **Dense** | Data tables, admin consoles, observability, logs, trading, IDE-like | 12–13px | 28–32px | full-width |

  A codebase with a 14px base and 40px rows is Standard even if nobody wrote the word "Standard".
- **Check chrome heights against row height.** Carbon requires the column header, toolbar, batch bar
  and pagination to match the table's row height (Carbon, *Data table*). If the incumbent has a 40px
  toolbar over 32px rows, that is drift with a file reference — not the rhythm to standardise on.
- **Verify numerals.** Grep for `font-variant-numeric`. `tabular-nums` activates figures "all of the
  same size, allowing them to be easily aligned like in tables" (MDN, `font-variant-numeric`). Missing
  on a numeric column is drift, and it is the single most common drift.
- **Check the measure.** WCAG 2.2 SC 1.4.8 caps a text block at 80 characters (AAA); the incumbent
  should sit at 65–80ch for prose and be unconstrained for grids.

## 4. Inventory components and their states

For each shared component, record: default size, variants, **which states exist**, keyboard behaviour,
and the rules it already encodes (one primary CTA per view, toolbar action caps, matching row
heights).

Then check the states a component is *missing*. The common gaps, in order of frequency:

- `disabled` present but with **no explanation** mechanism anywhere in the codebase.
- `loading` implemented as a centred spinner on the page rather than a skeleton matching content.
- `error` with no recovery path — a toast, no retry.
- `offline` / `stale` absent entirely.
- `focus-visible` styled to near-invisibility, or `outline: none` with no replacement (violates
  SC 2.4.7; an author-supplied focus indicator must meet 3:1 against adjacent colours, SC 1.4.11).

## 5. Record the rules, not the values

The file is rules. A value belongs in `DESIGN.md` because it is a *system rule*, not because it
appears twice. Write each rule so a reviewer could check a diff against it:

> Row height is 40px in Standard and 32px in Dense. Toolbar, header and pagination heights always
> match the row height of the table they sit above.

Not:

> The table uses `padding: 0 16px`.

## 6. When the incumbent system is inconsistent

This is the normal case, and how you handle it decides whether the file is useful.

**Never document a violation as the rule.** If one route uses a 13px radius and the rest use 8px, the
rule is 8px and the 13px is a defect with a file path.

Sort what you find into four buckets:

1. **Rule + conformance.** The majority behaviour, confirmed. Becomes the rule.
2. **Rule + known drift.** The majority behaviour, with N exceptions. The rule plus a
   `known drift` line naming each file. Never silently bless an exception by omitting it, and never
   document the violation as the rule.
3. **No rule — an undecided axis.** The incumbent offers no dominant choice (two equally-used
   accent hues, no consistent radius family). Mark it **unresolved** with the two candidates and a
   one-line recommendation, and flag it to the user as a decision they must make. Do not invent a
   house rule to fill the hole.
4. **Out of scope for `document`.** A value that appears once and has no sibling. Leave it out
   until a later `tokens` pass promotes it.

**Never silently normalise.** Writing `DESIGN.md` that disagrees with the shipped UI is worse than
writing none — every future session trusts the file.

## 7. Rules for the file itself

- Short enough to read in one sitting. Rules, not essays.
- Every rule phrased so a reviewer could check a diff against it.
- Platform grammar (CSS layers, Tailwind, library theming) recorded once, with the project's
  exceptions called out explicitly.
- The **three-layer consumption rule** stated even if the code violates it — record it as the target
  and list the violations as drift. The architecture in `tokens.md` is a house rule, not a standard:
  the W3C DTCG format module calls token groups "arbitrary" and says tools "SHOULD NOT" infer type
  or purpose from them, while *requiring* a determinable `$type`, case-sensitive names free of `$`,
  `{`, `}`, `.`, and error detection on circular references.
- Update it when a build *settles* a previously provisional value.

## 8. Verify before handing it over

1. Render one representative **Dense** surface and one **Focused** surface from the codebase.
2. Check the documented rules against what actually ships: type sizes, row heights, radii, colours,
   states. Every mismatch is either a rule correction or a new drift line.
3. Run the drift sweeps from `tokens.md` § *Drift detection* and paste the counts into the file — a
   reviewer can then see the size of the job without running it.
4. Report to the user: rules confirmed, drift found (with file paths), and the axes marked
   unresolved.

## Not found

- **A tooling convention for exporting DESIGN.md from Figma or a token pipeline.** Multiple tools
  exist; none is a standard, and each emits a different shape. Settled by: none — this file's schema
  is the contract.
- **A source for how a codebase should be ranked when incumbent behaviours are near-tied.** "Majority
  wins" is this skill's heuristic; near-ties are marked unresolved for a human decision. Settled by:
  none.
- **A standardised reverse-engineering checklist.** The mobile skill's `document` procedure is the
  ancestor of this one; the token-source, palette, and density-extraction steps above are additions
  made for web.

## Sources

All accessed 2026-10-05. Parenthetical = what the citation carries in this procedure.

- **Design Tokens Format Module 2025.10** — W3C Design Tokens Community Group. (Groups arbitrary; tools SHOULD NOT infer type/purpose; `$type` determinable or invalid; names case-sensitive excluding `$`/`{`/`}`/`.`; circular refs MUST error.) https://www.designtokens.org/TR/2025.10/format/
- **Registering custom properties in CSS** — MDN, Mozilla. (`@property` needs `syntax` AND `inherits`; `initial-value` cannot use `%`/`em`; registered interpolates, unregistered animates discretely.) https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Properties_and_values_API/Registering_properties
- **`color-scheme`** — MDN, Mozilla. (Repaints UA chrome only; does not theme the document; `<meta name="color-scheme">` before CSS to avoid a flash.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme
- **`@layer`** — MDN, Mozilla. (Order beats specificity entirely; unlayered normal declarations outrank layered ones.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer
- **`font-variant-numeric`** — MDN, Mozilla. (`tabular-nums` activates figures "all of the same size, allowing them to be easily aligned like in tables"; Baseline widely available since January 2020.) https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variant-numeric
- **WCAG 2.2** — W3C / W3C WAI. (SC 2.4.7 Focus Visible; SC 1.4.11 Non-text Contrast — an author-supplied focus indicator must meet 3:1 against adjacent colours; SC 1.4.8 — 80-character measure ceiling.) https://www.w3.org/TR/WCAG22/ · https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- **Data table** — Carbon Design System, IBM. (Row sizes xs 24 / sm 32 / md 40 / lg 48 / xl 64; header, toolbar and pagination heights match the row size.) https://carbondesignsystem.com/components/data-table/usage/
- **Theme variables** — Tailwind CSS v4, Tailwind Labs. (`@theme` for tokens that map to utilities; `:root` for plain CSS variables; `@theme` top-level; `@theme inline` when a theme variable references another.) https://tailwindcss.com/docs/theme
- **Theming** — shadcn/ui. (One base `--radius` with derived `calc()` multipliers; one base `--spacing` value; spacing tokens do not change on screen size.) https://ui.shadcn.com/docs/theming
- Density class definitions — house rule: `references/craft-floor.md`.
- Procedure shape (inventory tokens, inventory components, record rules, note drift honestly, keep it durable) — `premium-mobile-design` `references/document.md`.
