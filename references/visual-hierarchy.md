# Visual hierarchy

Hierarchy is how the eye is told what to read first. In app surfaces it is built from four levers:
**weight, size, position, and space** — plus, deliberately, not from colour alone.

## The definition and the levers

Nielsen Norman Group's definition (Kelley Gordon, *Visual Hierarchy in UX: Definition*, 2021-01-17,
accessed 2026-10-05): visual hierarchy "refers to the organization of the design elements on the
page so that the eye is guided to consume each design element in the order of intended importance."

Colour is a lever, but NN/g demotes it: "**It's not the actual color of an element that creates the
hierarchy, but rather the contrast in value and saturation between the element and the context in
which it appears** (including background and other nearby elements)." And a hard rule: "**Do not
rely only on color to communicate visual hierarchy.** People with color blindness may not be able
to perceive differences between certain color combinations."

## Levers, in order of durability

| Lever | NN/g guidance | App example |
|---|---|---|
| **Weight** | "Typefaces with heavy weight, like bold, stand out against light-weighted or regular typefaces." Carbon: "A bold weight will always have more emphasis than a lighter weight font of the same size. However, a lighter weight font can rank hierarchically higher than a bold font if the lighter weight type size is significantly larger." | Section heading at 600 over body at 400, same 14px |
| **Size** | "**Use no more than 3 sizes** — small, medium, and large… sizes could range from 14px to 16px for the body copy, 18px to 22px for the subheader, and up to 32px for the header." Carbon's productive set supplies exactly three heading tiers at 14/20/28px (`heading-compact-01`, `heading-03`, `heading-04`). | Page title > section heading > body |
| **Position** | NN/g: users "expect to find specific menus in specific areas of the screen." Carbon: "Moving to the right along the header, the functions become more global." | Primary action last in the header's right cluster; primary column before secondary |
| **Space** | "Let it breathe. An element that has more space around it will be perceived as one group and thus will receive more attention." | Larger gap above a record's identity block than between its fields |

NN/g caps colour-based hierarchy hard, and the caps are worth quoting because they are easy to
breach in dashboards:

- "**Don't use too many colors.** While some complex color schemes are beautiful to look at, they
  can feel overwhelming… In common, uncomplicated designs, **limit your color use to 2 primary and
  2 secondary colors**."
- "**Don't use too many contrast variations. Use no more than 3 contrast variations** for complex
  designs. **If everything is contrasted, then nothing stands out.** Effective designs often use
  different treatments for header, subheader, and body text."
- "Reserve warm bright colors, like red, for warnings or errors."

## The one-dominant-element rule

Two sources converge, and it is worth stating as a hard check rather than a preference.

- **NN/g on scale:** "Make the most important element biggest… **Limit how many elements are big to
  a maximum of 2** so that they do stand out and reinforce the hierarchy."
- **NN/g on complex applications** (Kate Kaplan, *8 Design Guidelines for Complex Applications*,
  2020-11-08, accessed 2026-10-05): "The sheer amount of competing information and elements within
  complex application can hinder these tasks," and the guideline is to "**make critical elements
  visually salient** (i.e., making them stand out from surrounding elements)."

Kaplan adds the corrective that most consoles need: "**making important information stand out does
not always mean adding emphasis to that information** (e.g., a bright color or a heavier font
weight). **Removing nonessential elements can be equally or even more effective** at making
important information visually salient." Her example: dashboard numbers rendered large and clear
alone, versus the same numbers beside decorative money icons — the icons made the numbers *harder*
to find.

**One dominant element per view.** On an index page that is the filter/sort/search cluster plus the
table, and nothing else competing. On a details page it is the record's identity. On a homepage it
is whatever the user came to check. If two elements both claim the top slot, neither is read.

## Reading order must match DOM order

This is where hierarchy stops being aesthetic and becomes a conformance question.

- **WCAG 2.2 SC 2.4.3 Focus Order** (Level A): "If a web page can be navigated sequentially and the
  navigation sequences affect meaning or operation, focusable components receive focus in an order
  that preserves meaning and operability" (W3C, accessed 2026-10-05).
- **Visual order and focus order need not be identical, but both must make sense.** W3C: "The focus
  order may not be identical to the programmatically determined reading order… as long as the user
  can still understand and operate the web page." And the best practice: "make sure the focus order
  reinforces the reading order implied by the visual layout."
- **Two user groups, two orders.** W3C: "a screen reader user interacts with the programmatically
  determined reading order, while a sighted keyboard user interacts with the visual presentation…
  Care should be taken so that the focus order makes sense to both of these sets of users and does
  not appear to either of them to jump around randomly."
- **Sufficient technique: match DOM to visual order.** W3C lists C27, "Making the DOM order match
  the visual order." Carbon adopts it for the shell: matching "the visual order of your UI objects
  with the order they appear in the Document Object Model… ensures the designed hierarchy of
  information is communicated the same visually as it is by assistive technologies" (Carbon,
  *Global header pattern*).
- **Carbon's carve-out is instructive.** Styling a different visual order than DOM order "may be
  beneficial. For example, on narrow or mobile screen widths you may choose to move your navigation
  from the top of the screen to another area." The relocation is legitimate because the *reading
  order* is preserved — the same content in a different position, not a different content order.
- **Headings must match the heading tag.** Carbon, citing the WCAG page-structure tutorials: "To
  ensure all users interpret the structure of your content in the same way, the visual
  representation of a heading should match the underlying ranking of the header tag."
- **A visual hierarchy that relies on `tabindex` is a red flag.** W3C failure F44 covers "using
  `tabindex` to create a tab order that does not preserve meaning and operability."

## Tests

- **The squint test.** NN/g: "we are taught to squint or apply a slight blur to the design to get an
  idea of the conveyed groupings and hierarchy." Blur at radius 5–10px to check grouping; a 20px
  blur reveals unintended hierarchy — in NN/g's Spotify example, "one of the recently played items
  [becomes] the most prominent element of the page due to its strong color," an effect present in
  the original too.
- **Test the content, not just the template.** NN/g: "it's not enough to design the template — you
  must also consider the content that will fill it."
- **Keyboard pass.** Tab from the top: does focus walk the visual order? Does anything get trapped?
  Does a sticky header or an open panel swallow it (WCAG 2.2 SC 2.4.11 Focus Not Obscured
  (Minimum))?
- **Greyscale pass.** Turn colour off. If the hierarchy collapses, it was colour doing the work
  that weight, size, position, or space should have done.

## Sources

- Visual Hierarchy in UX: Definition (definition; colour/contrast/scale caps of 3 sizes, 2 big elements, 3 contrast variations; grouping; squint test) — Nielsen Norman Group, Kelley Gordon, 2021-01-17. https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ — accessed 2026-10-05
- 8 Design Guidelines for Complex Applications (guideline 8: make important information visually salient; removal as an alternative to emphasis) — Nielsen Norman Group, Kate Kaplan, 2020-11-08. https://www.nngroup.com/articles/complex-application-design/ — accessed 2026-10-05
- Signal–to–Noise Ratio (signal definition; visual hierarchy reflects relative importance; use hierarchy techniques sparingly) — Nielsen Norman Group, Xinyi Chen, 2018-09-09. https://www.nngroup.com/articles/signal-noise-ratio — accessed 2026-10-05
- Understanding SC 2.4.3 Focus Order — W3C Web Accessibility Initiative. https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html — accessed 2026-10-05
- Understanding SC 2.4.11 Focus Not Obscured (Minimum) — W3C Web Accessibility Initiative. https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html — accessed 2026-10-05
- Typography: type sets (productive heading sizes 14/20/28px) — Carbon Design System (IBM). https://carbondesignsystem.com/elements/typography/type-sets/ — accessed 2026-10-05
- Typography overview (weight vs size hierarchy; semibold for section headers, not long text; type colour) — Carbon Design System (IBM). https://carbondesignsystem.com/elements/typography/overview/ — accessed 2026-10-05
- Global header pattern (C27 DOM/visual order; heading tags match visual representation) — Carbon Design System (IBM). https://carbondesignsystem.com/patterns/global-header/ — accessed 2026-10-05
