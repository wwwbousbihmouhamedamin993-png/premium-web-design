# Whitespace & hierarchy

Whitespace is a structural instrument, not decoration. It creates relationships, it creates
hierarchy, and — this is the part with a research trail — it measurably affects reading
comprehension. Carbon's spacing foundation is the primary mechanism reference; the comprehension
claim comes from a controlled study, not from a blog post.

## The spacing scale

Carbon's spacing scale "complements the 2x Grid and typography scale by using multiples of two,
four, and eight," with a token per level (Carbon, *Spacing*, accessed 2026-10-05):

| Token | rem | px | Token | rem | px |
|---|---|---|---|---|---|
| `$spacing-01` | 0.125 | 2 | `$spacing-08` | 2.5 | 40 |
| `$spacing-02` | 0.25 | 4 | `$spacing-09` | 3 | 48 |
| `$spacing-03` | 0.5 | 8 | `$spacing-10` | 4 | 64 |
| `$spacing-04` | 0.75 | 12 | `$spacing-11` | 5 | 80 |
| `$spacing-05` | 1 | 16 | `$spacing-12` | 6 | 96 |
| `$spacing-06` | 1.5 | 24 | `$spacing-13` | 10 | 160 |
| `$spacing-07` | 2 | 32 | | | |

Three Carbon mechanics worth keeping:

- **Stacking, not ad-hoc margins.** Carbon's Stack component "uses the Carbon spacing scale to
  determine how much space there should be between items," which "allows components not to use
  margin and instead delegate the responsibility of positioning and layout to parent components."
  Parent-owned spacing is what makes density swappable at one breakpoint.
- **Spacing is not responsive; jumping a step is.** Carbon's FAQ: "the tokens themselves do not
  change values based on the screen size. However, it is acceptable at page breakpoints to jump a
  step(s) on the spacing scale" — Carbon's own example goes from `$spacing-05` at 1440px to
  `$spacing-03` at 768px.
- **Percentages are for dividing a page, not for rhythm.** Carbon: "Percentages like 50% (1/2) or
  33% (1/3) are acceptable ways to divide a page. Percentages can all be used to control max and
  min widths."

## What space does

Carbon states the three jobs plainly (*Spacing*, "Designing with space"):

- **Relationship.** "Elements in a design that are near each other are seen as being meaningfully
  related. As more space is added between elements, their perceived relationship weakens." Same
  pattern ⇒ equal weight, seen as related pieces.
- **Hierarchy.** "Elements that have more spacing around them tend to be perceived as higher in
  importance than elements that have less space around them." Carbon's caution is the operative
  part: "Elements that are set close to each other can be easily overlooked. Users may see the
  grouping but not process each individual item."
- **Grouping without a box.** "Space can also be used to denote groups of associated information.
  This creates content sections on a page without having to use lines or other graphical elements
  as a divider."

## Section rhythm

- **Carbon's rule for the vertical: a fixed sizing scale, applied as margin.** The 2x Grid
  document says to "use the fixed sizing scale to set vertical spacing between sections, by adding
  it to the top or bottom margin of a box," with the documented values 8, 16, 24, 32, 48, 64,
  80px (1×–10× the 8px mini unit).
- **Two levels only, in practice.** Within a section, space is one step; between sections, two or
  more steps. If every gap is distinct, no gap reads as structural.
- **NN/g's independent statement of the same mechanism:** whitespace works "to achieve a balanced
  design, making it easier for your users to scan and read," and depends on "a consistent spacing
  system and the proximity principle" (NN/g, *What is Whitespace?*, Kelley Gordon, 2024-04-08,
  accessed 2026-10-05).

## When whitespace replaces a container

Use space instead of a border or background when the content is genuinely one group and the
reading order is already obvious. Do not use it when:

- the group is visually adjacent to another group with the same weight (space alone won't
  disambiguate) — add a rule or a surface;
- the content is interactive and the boundary is the hit target;
- the surface is Dense and rows are already at their minimum height — a card per row costs a row.

Carbon's anti-pattern is spacing *plus* a border *plus* a background for the same grouping.
Nielsen Norman Group's version: "If varying whitespace alone is not enough of a visual cue to
create hierarchy, add extra elements like borders or backgrounds. These additional elements can
create visual clutter, so use them sparingly."

## Optical alignment

- **Type sits against the padding, never inside it.** Carbon: "Always place type to the edge of box
  padding," with an explicit don't: "Never place type on the padding." Carbon also notes that some
  design tools add text-box padding by default — check and remove it.
- **Carbon's caution about optical spacing vs the unit:** "The mini unit is the guide when needed.
  Spacer snaps to the text box and does not necessarily need to snap to the mini unit." Optical
  adjustments are permitted where the unit cannot hold; structural spacing still uses the scale.
- **Alignment beats balance.** Carbon: "Horizontal and vertical alignment are equally critical.
  When present, the eye can follow content more easily, increasing the perception of visual
  harmony."
- **Height is content-driven.** Carbon's vertical-rhythm guidance: "Always use 'Auto' in alignment
  to ensure the text box fits with the content."

## The whitespace / comprehension claim — and its source

The widely-repeated figure that "good use of white space between paragraphs and in the left and
right margins increases comprehension by almost 20%" circulates through design commentary without
a citation. The underlying controlled study is:

> Chaparro, B., Baker, J. R., Shaikh, A. D., Hull, S., & Brady, L. (Wichita State University).
> *Reading Online Text: A Comparison of Four White Space Layouts.* **Usability News, vol. 6,
> published July 2004.**
> Abstract, as recorded in the Embry-Riddle Aeronautical University research portfolio
> (https://portfolio.erau.edu/en/publications/reading-online-text-a-comparison-of-four-white-space-layouts,
> accessed 2026-10-05): "In this study, reading performance with four white space layouts was
> compared. Margins surrounding the text and leading (space between lines) were manipulated to
> generate four white space conditions. **Results show that the use of margins affected both
> reading speed and comprehension more than the No Margin text.** Participants were also generally
> more satisfied with the text with margins. **Leading was not shown to impact reading performance
> but did influence overall user preference.**"

What the study does and does not establish:

| Claim | Support |
|---|---|
| Side margins affect reading speed and comprehension | **Yes** — the study's stated finding |
| Line-height (leading) improves comprehension | **No** — "Leading was not shown to impact reading performance" |
| More whitespace is preferred | **Yes** — preference and satisfaction moved with margins |
| A specific percentage improvement | **Not established** by this abstract |

Two cautions. First, the study is 2004, twenty college students, and continuous prose passages —
**not** a table, console, or dashboard. It supports margins and grouping in reading surfaces, and
does not transfer to Dense data views, where the applicable floor is WCAG 2.2 SC 2.5.8's 24×24 CSS
pixel minimum target (W3C, accessed 2026-10-05). Second, Carbon's own framing is the more usable
one for product: "White space helps with information processing; too much dense information can be
disorienting or overwhelming for a user. **Sections of a UI are allowed to be dense, but the whole
page should not be crowded; there should be white space to let the user's eye rest**"
(Carbon, *Spacing*).

**Not found:** the primary source for the "increases comprehension by almost 20%" figure. It is
repeated in design commentary attributed only to "a study"; the Chaparro et al. paper above is
the study usually cited and does not state a percentage in its abstract. Settled by: the full
article text (Usability News vol. 6, 2004) or a different paper with the figure stated explicitly.

## Sources

- Spacing (scale table, stacking, relationship/hierarchy/grouping, white space, FAQ on breakpoints) — Carbon Design System (IBM). https://carbondesignsystem.com/elements/spacing/overview/ — accessed 2026-10-05
- 2x Grid (fixed sizing scale, vertical rhythm, padding, type against padding edge, key lines) — Carbon Design System (IBM). https://carbondesignsystem.com/elements/2x-grid/overview/ — accessed 2026-10-05
- What is Whitespace? (video) — Nielsen Norman Group, Kelley Gordon, 2024-04-08. https://www.nngroup.com/videos/whitespace — accessed 2026-10-05
- Visual Hierarchy in UX: Definition (grouping via proximity and common region; when to add a container; "use them sparingly") — Nielsen Norman Group, Kelley Gordon, 2021-01-17. https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ — accessed 2026-10-05
- Chaparro, Baker, Shaikh, Hull & Brady, *Reading Online Text: A Comparison of Four White Space Layouts*, Usability News vol. 6, July 2004 — abstract via Embry-Riddle Aeronautical University research portfolio. https://portfolio.erau.edu/en/publications/reading-online-text-a-comparison-of-four-white-space-layouts — accessed 2026-10-05
- Understanding SC 2.5.8 Target Size (Minimum) — W3C Web Accessibility Initiative. https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — accessed 2026-10-05
