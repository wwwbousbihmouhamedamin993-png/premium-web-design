# Information density

Density is a declared property of a surface, not a taste. A 13px tabular numeral in a Dense
console is correct; the same numeral in a Focused auth form is a defect. This file gives the three
classes, the mechanics per class, and the accessibility floor that no class may cross.

## The three classes

Class definitions come from this skill's own floor (`craft-floor.md`). Vendor rows below are the
evidence for what each class is made of.

| Class | Surfaces | Base body | Row height | Measure |
|---|---|---|---|---|
| **Focused** | Auth, onboarding, checkout, single-form flows, settings detail | 16px | — | 60–70ch, centered |
| **Standard** | Project home, card+list feeds, record detail | 14–15px | 40–44px | 65–80ch |
| **Dense** | Data tables, admin consoles, observability, logs, trading, IDE-like | 12–13px | 28–32px | full-width |

## Carbon's productive type set is the Standard class, precisely

Carbon splits its type system into two sets, and the split is a density decision made explicit:
the **productive** set uses "a base type size of 14px, while the **expressive** set uses a base
type size of 16px" (Carbon, *Type sets*). Carbon's own words on why: the productive set is "primarily
used within product spaces, where users benefit from a more condensed treatment of content to
maintain focus on tasks," while expressive styles "would be distracting if used in product"
(Carbon, *Typography overview*).

Productive tokens — the Standard/Dense working set:

| Token | Size | Line height | Weight | Use |
|---|---|---|---|---|
| `label-01` | 12px | 16px | 400 | field labels, error messages, captions; "should not be used for body copy" |
| `helper-text-01` | 12px | 16px | 400 | explanatory helper text below a field title |
| `code-01` | 12px | 20px→16px (IBM Plex Mono) | 400 | inline code and small code elements |
| `body-compact-01` | 14px | 18px | 400 | "short paragraphs with no more than four lines… commonly used in components" |
| `body-01` | 14px | 20px | 400 | long paragraphs, four lines or more; always left-aligned |
| `heading-compact-01` | 14px | 18px | 600 | component and layout headings; pairs with `body-compact-01` |
| `heading-01` | 14px | 20px | 600 | smaller layout headings |

Expressive tokens are the Focused class: `label-02` 14px/18px, `body-compact-02` 16px/22px,
`body-02` 16px/24px, `heading-compact-02` 16px/22px semibold, `heading-02` 16px/24px semibold.

Carbon's own pairing rule is the one to internalise: **a compact heading pairs with compact body,
never across sets.** `heading-compact-01` (14px semibold) with `body-01` (14px/20px) keeps the
weight contrast; pairing it with 16px body destroys the hierarchy.

## Row height is the real density lever

Carbon's data table offers five heights and names the intent of each (Carbon, *Data table*):

| Size | Height | Carbon's stated use |
|---|---|---|
| xs | 24px / 1.5rem | "highly dense layouts where maximizing information within limited space is a priority" |
| sm | 32px / 2rem | "compact interfaces that require reduced component height while maintaining comfortable readability and interaction" |
| md | 40px / 2.5rem | "the default and most commonly used size… when no specific density or spacing requirements exist" |
| lg | 48px / 3rem | "spacious layouts where increased emphasis and easier interaction are important" |
| xl | 64px / 4rem | rows containing multiple lines of information |

So: **Dense → xs/sm. Standard → md. Focused → no rows.** Two coupled rules Carbon states:

- **Header row height must match the body rows.** "The column header row… should always match the
  row size of the table." Mixing is a defect.
- **Chrome height matches rows too.** Toolbar height, batch action bar height, and pagination
  height "should always match the row height of the data table," with one documented exception per
  component for xl. An index page is a vertical rhythm, and a 40px toolbar over 24px rows breaks it.

Carbon's tree view repeats the pairing at a different scale: small nodes 32px (default, "similar
geometries as the UI shell left navigation panel") and extra small 24px for "more condensed view"
(Carbon, *Tree view*). A sidebar whose rows are 24px tall against a 32px main list is a
misalignment, not a hierarchy.

## Density is not accessibility — the floor that applies to all three

- **Minimum target size: 24×24 CSS pixels.** WCAG 2.2 SC 2.5.8 Target Size (Minimum), Level AA:
  "The size of the target for pointer inputs is at least 24 by 24 CSS pixels," with five exceptions
  — Spacing, Equivalent, Inline, User agent Control, and Essential (W3C, accessed 2026-10-05).
- **Undersized targets may pass on spacing instead of size.** The exception: targets under 24×24
  pass if "if a 24 CSS pixel diameter circle is centered on the bounding box of each, the circles do
  not intersect another target or the circle for another undersized target." W3C's own worked
  example: a row of 20×20 targets with 4px gaps passes; the same 20×20 targets with no gaps fail.
  This is the mechanism that lets a 24px Dense row survive: the *row* must provide the clearance,
  so row hover and the interactive target have to be the full row, not the 12px glyph.
- **Zoom does not excuse it.** W3C: "The requirement is independent of the zoom factor of the page;
  when users zoom in, the CSS pixel size of elements does not change. This means that authors
  cannot meet it by claiming that the target will have enough spacing or sufficient size if the
  user zooms into the page."
- **Density is user-controllable, and that's endorsed.** W3C's note on SC 2.5.8: "Another option
  is to provide a mechanism to control the density of layout and thereby change target size or
  spacing, or both. This can be beneficial for a wide range of users. For example, users with
  visual field loss may prefer a more condensed layout with smaller sized controls while users
  with other forms of low vision may prefer large controls." Treat a density switch as an
  accessibility affordance, not a preference toggle.
- **Measure: 80 characters is the AAA ceiling for blocks of text.** WCAG 2.2 SC 1.4.8 Visual
  Presentation requires a mechanism for "Width is no more than 80 characters or glyphs (40 if
  CJK)," plus non-justified text, "Line spacing (leading) is at least space-and-a-half within
  paragraphs, and paragraph spacing is at least 1.5 times larger than the line spacing," and
  resizing to 200% "without… scroll[ing] horizontally to read a line of text" (W3C, accessed
  2026-10-05). Carbon concurs on direction: `body-01` "is always left-aligned."
- **Contrast floor applies at every class.** WCAG 2.2 SC 1.4.11 Non-text Contrast governs focus
  indicators and control boundaries; a Dense 12px `label-01` has *less* tolerance for low contrast
  than a Focused 16px body, not more.

## Switching class

- **Declare once per surface, then apply mechanically.** Type size, row height, gutter, and padding
  all come from one class. A screen that mixes 12px table text with 16px prose side by side without
  a reason is a class violation, not a nuance.
- **Do not switch mid-page.** Polaris is explicit: "Use looser spacing for low-density layouts. Use
  tighter spacing for high-density layouts… **Avoid changing information density within a single
  page**, otherwise your app can feel disjointed" (shopify.dev, *Layout*, accessed 2026-10-05).
- **Do switch across routes that belong to different jobs.** An index route that lists 200 rows is
  Dense; the settings route for the same object is Focused. That transition is legitimate; it
  should feel like entering a different room.
- **Prefer row height over type size for compression.** Carbon's xs row is 24px with 12px
  `label-01` and 16px line height — the glyph shrinks but the leading stays legible. Shrinking the
  type without shrinking the row buys nothing.
- **Density control, if offered, is a theme-level token swap.** Carbon's spacing FAQ notes the
  tokens themselves "do not change values based on the screen size," so density must be a separate
  token axis rather than a media query.

**Not found:** a primary-source measurement of what fraction of viewport area should be whitespace
per density class. The classes above carry a whitespace budget from `craft-floor.md`
(Focused 55–70% · Standard 40–55% · Dense 25–40%), which is this skill's own heuristic, not a
vendor or standards figure. Settled by: none available; treat as a starting point and validate by
screenshot.

## Sources

- Typography: type sets (productive base 14px / expressive base 16px; fixed vs fluid headings) — Carbon Design System (IBM). https://carbondesignsystem.com/elements/typography/type-sets/ — accessed 2026-10-05
- Typography overview (productive vs expressive intent; weights; type colour) — Carbon Design System (IBM). https://carbondesignsystem.com/elements/typography/overview/ — accessed 2026-10-05
- Data table (five row heights and their stated uses; header/toolbar/pagination height matching; toolbar action cap) — Carbon Design System (IBM). https://carbondesignsystem.com/components/data-table/usage/ — accessed 2026-10-05
- Tree view (node sizes small 32px / extra small 24px) — Carbon Design System (IBM). https://carbondesignsystem.com/components/tree-view/usage/ — accessed 2026-10-05
- Understanding SC 2.5.8 Target Size (Minimum) — W3C Web Accessibility Initiative. https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — accessed 2026-10-05
- Understanding SC 1.4.8 Visual Presentation — W3C Web Accessibility Initiative. https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html — accessed 2026-10-05
- Layout (information density: looser for low, tighter for high; avoid changing within a page) — Shopify App Design Guidelines. https://shopify.dev/docs/apps/design/layout — accessed 2026-10-05
- Craft floor (density-class definitions and whitespace budget) — this skill, `references/craft-floor.md` — accessed 2026-10-05
