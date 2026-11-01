# Accessibility: WCAG 2.2 AA as the shipping floor

Applies to: every logged-in product surface. WCAG 2.2 Level AA is the floor, not the goal. The
danger on a B2B console is not that nobody knows the rules — it is that an AA audit passes, the
work ships, and the failures that survive are the ones the audit never measured.

**Why "AA" is the right floor.** WCAG conformance has four levels: A, AA, AAA. Not all
success criteria are AA. A criterion that is AAA is *not* an AA gate, and an AA audit will never
flag it. Two criteria bite hardest on SaaS surfaces for exactly this reason: **SC 2.5.5 Target
Size (Enhanced), 44×44 CSS px, is Level AAA** — while **SC 2.5.8 Target Size (Minimum), 24×24
CSS px, is Level AA** [S1]. **SC 2.4.13 Focus Appearance is Level AAA** [S2] — while
**SC 2.4.7 Focus Visible, which only requires *a* visible indicator, is Level AA** [S3]. A
sub-threshold focus ring — 1px, or 2px at 1.4:1 — passes 2.4.7 and 2.4.11 and still fails 2.4.13.
Treat 2.4.13 as the house target anyway, because it is the cheapest way to be visibly right for
low-vision users.

## The criteria that bite hardest on a data-dense app

| SC | Name | Level | What it demands, verbatim in substance |
|---|---|---|---|
| 2.1.1 | Keyboard | **A** | "All functionality of the content is operable through a keyboard interface without requiring specific timings for individual keystrokes" [S4] |
| 2.4.1 | Bypass Blocks | **A** | "A mechanism is available to bypass blocks of content that are repeated on multiple web pages" [S5] |
| 2.4.3 | Focus Order | **A** | Focusable components "receive focus in an order that preserves meaning and operability" [S6] |
| 2.4.7 | Focus Visible | **AA** | Any keyboard-operable UI "has a mode of operation where the keyboard focus indicator is visible" [S3] |
| 2.4.11 | Focus Not Obscured (Minimum) | **AA** | "When a user interface component receives keyboard focus, the component is not entirely hidden due to author-created content" [S7] |
| 2.4.13 | Focus Appearance | **AAA** | Indicator area at least that of "a 2 CSS pixel thick perimeter of the unfocused component", **and** "a contrast ratio of at least 3:1 between the same pixels in the focused and unfocused states" [S2] |
| 1.4.11 | Non-text Contrast | **AA** | UI components, and visual information required to identify components and states, at "at least 3:1 against adjacent color(s)" [S8] |
| 3.3.1 | Error Identification | **A** | "If an input error is automatically detected, the item that is in error is identified and the error is described to the user in text" [S9] |
| 4.1.2 | Name, Role, Value | **A** | Name and role "can be programmatically determined"; user-settable states, properties and values "can be programmatically set"; and changes are notified to user agents [S10] |
| 4.1.3 | Status Messages | **AA** | Status messages "can be programmatically determined through role or properties such that they can be presented to the user by assistive technologies **without receiving focus**" [S11] |
| 2.5.8 | Target Size (Minimum) | **AA** | ≥ **24×24 CSS px**, or undersized targets spaced so 24px-diameter circles centred on them do not intersect [S1] |
| 1.4.10 | Reflow | **AA** | No two-dimensional scrolling at "a width equivalent to **320 CSS pixels**" (vertical) or "a height equivalent to **256 CSS pixels**" (horizontal); **data tables (not individual cells)** are excepted as two-dimensional content [S12] |
| 1.3.4 | Orientation | **AA** | "Content does not restrict its view and operation to a single display orientation … unless a specific display orientation is essential" [S13] |
| 1.4.4 | Resize Text | **AA** | Text resizable "up to 200 percent without loss of content or functionality" [S14] |
| 1.4.12 | Text Spacing | **AA** | No loss of content/functionality when line-height ≥1.5×, paragraph spacing ≥2×, letter spacing ≥0.12×, word spacing ≥0.16× font size are all applied [S15] |

## The five failures that ship anyway

### 1. Target size in dense tables and toolbars

24×24 CSS px is the AA gate [S1]. The 24px *spacing-circle* exception is real: undersized targets
pass if a 24 CSS px diameter circle centred on each target's bounding box does not intersect
another target or another such circle. The other exceptions are **Equivalent** (same function
available via another AA-compliant control on the page), **Inline** (inside a sentence, constrained
by line-height), **User Agent Control** (size not modified by the author), and **Essential** [S1].
A 16px icon button that is not in a sentence is excused by nothing except spacing, and a row of
16px buttons at 20px pitch fails the circle test.

**House rule (judgement, not sourced):** size the *hit area* with padding or a pseudo-element to
24×24 minimum rather than relying on the spacing exception. The spacing exception passes an audit
and fails real hands. Hold 44×44 as the design target for primary touch actions on coarse pointers
— that is AAA [S1], and it is the number that survives user testing on a phone.

Targets that select values by *position* — sliders, gradient colour pickers, cursor-positioned
editing areas — count as **one** target, not many [S1]. A dropdown trigger with a caret icon is
one target.

### 2. Focus rings that fail AAA while passing AA

SC 2.4.7 requires only that an indicator be visible and that it "must not be time limited" [S3].
SC 2.4.13 sets the measurable bar: indicator area ≥ a 2 CSS px thick perimeter of the *unfocused*
component, and ≥3:1 contrast between the same pixels focused vs unfocused [S2]. Focus indicators
are generally non-text content, so they are also subject to SC 1.4.11 at 3:1 [S3][S8].

- **Perimeter, not outline.** 2.4.13 measures an *area*, and "does not require that the focus
  indicator literally be a 2 CSS pixel thick outline, only that the indicator be at least that
  large" [S2]. For non-rectangular components the perimeter may enclose the shape or its minimum
  bounding box [S2].
- **Measure against the unfocused pixels, not the ring's own background.** 3:1 is between the same
  pixels focused and unfocused [S2]. A ring 3:1 against white but 1.1:1 against the row it sits on
  fails.
- **Two-colour indicators are the documented technique.** Technique **C40** builds a two-colour
  indicator to ensure sufficient contrast with all components; **C45** uses `:focus-visible` [S3].
  In practice: a ring with a contrasting inner and outer band survives both light and dark.

### 3. Sticky layers hiding the thing you are tabbing to

SC 2.4.11 is new in WCAG 2.2 and is **Level AA** [S7]. W3C names the culprits: "sticky footers,
sticky headers, and non-modal dialogs", and specifically "A notification implemented as sticky
content, such as a cookie banner, will fail this success criterion if it entirely obscures a
component receiving focus" [S7]. AA permits *partial* obscuration; the AAA sibling 2.4.12 requires
none [S7].

Passing ways named by W3C: make the banner modal so the user must dismiss it, or "use scroll
padding so the banner does not overlap other content"; a notification needing no user action "could
also meet this criterion by closing on loss of focus" [S7]. For a console this is the **sticky
header plus sticky first column plus sticky action column** problem — a row scrolled under the
header is still obscured.

**House rule (judgement, not sourced):** on every scrollable region, `scroll-padding-block-start`
equal to the sticky header height, so focus scroll-into-view never lands underneath it.

### 4. Status messages that never reach the screen reader

4.1.3 applies to messages that **do not take focus**. Two conditions define a status message: it
gives "information to the user on the success or results of an action, on the waiting state of an
application, on the progress of a process, or on the existence of errors", and it "is not delivered
via a change in context" [S11].

Named examples that are verbatim console states: "Searching...", "18 results returned", "No results
returned", a busy icon announced as "application busy", "Saved in 'Wedding' album", "5 errors on
page" [S11]. The exclusion that catches teams out: **the list of search results itself is not a
status update** — only the brief message *about* it is [S11]. An error message inside a dialog that
takes focus is out of scope, because the change of context already gets announced [S11].

| Situation | Documented technique [S11] |
|---|---|
| Success/results, application state | **ARIA22** — `role="status"`, with G199 |
| Error, warning, suggestion | **ARIA19** — `role="alert"` / live regions, with G83/G84/G85/G177 |
| Progress of a process | **ARIA23** (`role="log"`), **ARIA25** (live region), **ARIA27** (`ariaNotify`) |

**House rules (judgement, not sourced):** the live-region container must exist in the DOM *empty*
before the message is written into it, or many screen readers will not announce it; every async
region also needs `aria-busy="true"` while its content is replaced, cleared when real content
lands, so partial DOM churn is not read out. Neither is in 4.1.3's text — it requires only
programmatic determinability [S11].

### 5. Name, Role, Value on anything you built

4.1.2 is Level **A** and covers "all user interface components (including but not limited to: form
elements, links and components generated by scripts)" [S10]. The intent text is the design brief:
"standard HTML controls already meet this success criterion when used according to specification" —
"If custom controls are created … then additional measures need to be taken" [S10]. Named states
that must be exposed include checked state of a checkbox or radio, and expanded/collapsed state of
an accordion or tree view [S10].

## Keyboard operability, and error identification

- **Everything pointer-reachable is keyboard-reachable**, with no timing requirement: "a user would
  be required to repeat or execute multiple keystrokes within a short period of time or where a key
  must be held down for an extended period" is a failure [S4].
- **Follow platform conventions.** "As a best practice, content should follow the platform/user
  agent conventions. However, deviating from these conventions does not fail the normative
  requirement" [S4]. A custom button binding only `Enter` still passes 2.1.1 — a usability defect,
  not a conformance one.
- **`tabindex` > 0 is strongly discouraged** and creates 2.4.3 failures the moment the DOM is
  reordered: focus order "does not necessarily need to follow the visual layout … as long as the
  order in which elements receive focus is logical" [S6].
- **Virtualised and re-sorted rows** are the classic 2.4.3 hazard. On sort, focus must stay on the
  activated header or move deliberately — roving tabindex, not Tab-per-cell.
- **Bypass block.** 2.4.1 is Level A and W3C's example is quantitative: without a skip link "a
  keyboard user needs to tab through approximately 40 links to reach the story" and "the screen
  reader user has to listen 200 words" [S5]. A persistent 30-link sidebar is that case. You still
  need the mechanism — 2.4.1 "is not the intent… to require authors to provide methods that are
  redundant to functionality provided by the user agent" [S5].
- **No traps.** SC 2.1.2 is Level A and pairs with every drawer, popover and virtualised list.

**Errors: text, in the field, named.** 3.3.1 is Level **A** and requires the error be "described to
the user in **text**", including the identity of the item in error [S9]. A red border plus a red icon
fails — colour is not text. W3C's "input error" examples include a bad state abbreviation, an invalid
postal code, "a birth date 2 years in the future", letters in a numeric-only phone field, and "a
bid that is below the previous bid or the minimum bid increment" [S9] — the last is the B2B case, and
it is still an input error.

- **SC 3.3.3 Error Suggestion (AA)** is the sibling. One sentence can satisfy both — "Email is not
  valid" passes 3.3.1; "Please provide a valid email address in the format name@domain.com" also
  passes 3.3.3 [S9].
- **A silent auto-correct is still an error.** If the page "automatically changes that value to fall
  within the allowed range, the user's error would still need to be described to them" [S9].
  Clamping a quantity field silently fails 3.3.1.
- **Native validation is a floor.** User agents prevent submission and "display generic error
  messages", but "the message may not be permanent, or fail to scroll with the page" [S9].
- Wire errors with `aria-describedby` to the message element and `aria-invalid="true"` on the
  control. 3.3.1 does not require this — it requires text — but its intent note says programmatic
  identification "may be covered by other criteria such as 4.1.2" [S9]. **House judgement:** assert
  it in review; it is the difference between an announced error and a drawn one.

## Non-text contrast, and the reflow exception

SC 1.4.11 requires 3:1 for "User Interface Components" and for "Visual information required to
identify user interface components and states", excepting inactive components and
user-agent-determined appearance [S8]. The rule is explicit: **computed contrast ratios must not be
rounded — "e.g. 2.999:1 would not meet the 3:1 threshold"** [S8]. Note the exemption's wording:
appearance "determined by the user agent and **not modified by the author**" [S8]. Setting
`appearance: none` on a checkbox and restyling it puts you **back in scope** — every control you
skin is a 1.4.11 obligation. And anti-aliasing makes on-screen thin lines look fainter than their
computed contrast, so evaluate from the underlying CSS, not the screenshot, and avoid "particularly
thin lines and shapes" [S8]. On a console, 1px table borders and 1px focus rings are both suspect.

| Purpose | Ratio | Level | Source |
|---|---|---|---|
| Body text | 4.5:1 | AA | [S16] |
| Large text — ≥24px, or ≥18.66px bold | 3:1 | AA | [S16] |
| UI components, states, meaningful graphics | 3:1 | AA | [S8] |
| Focus indicator, focused vs unfocused pixels | 3:1 | **AAA** | [S2] |
| Enhanced contrast (text, non-text) | 7:1 | AAA | [S16] |

**Reflow, for tables.** SC 1.4.10 (AA) requires no two-dimensional scrolling at **320 CSS px width**
or **256 CSS px height**; 320 CSS px "is equivalent to a starting viewport width of 1280 CSS pixels
wide at 400% zoom" [S12]. A table *may* scroll horizontally — two-dimensional layout is acceptable
for "data tables (not individual cells)" among others [S12] — but the carve-back is narrow: "each
cell within a table … would still need to meet this success criterion" [S12]. **Consequence:** the
table as a whole may scroll sideways at 320px; the *cells* may not. A cell reachable only by
horizontal scroll fails; a cell that truncates with a title/tooltip and expands vertically passes.

## Not found

- **A numeric minimum touch-target size for coarse pointers in any primary source.** 44×44 CSS px is
  the AAA figure in SC 2.5.5 [S1]; platform HIGs publish larger figures (44pt / 48dp) but neither is
  a WCAG source. Settling a house number would need the specific platform guideline you intend to
  cite.
- **Any WCAG criterion mandating a focus-ring thickness, colour, or offset at Level AA.** 2.4.7 AA
  requires only visibility [S3]; the 2px/3:1 quantification is AAA 2.4.13 [S2]. "WCAG requires a
  3px blue outline" is wrong at both levels.
- **An authoritative "live region container must pre-exist in the DOM" rule.** 4.1.3 requires only
  programmatic determinability through role or properties [S11]. The pre-existing-empty-container
  pattern comes from MDN's `aria-live` guidance, so this file labels it house judgement.
- **A WCAG criterion for announcement politeness.** `aria-live="polite"` vs `"assertive"` is MDN
  guidance, not a WCAG requirement; 4.1.3 only requires the message be exposed [S11].

## Sources

All W3C WAI pages below are *Understanding [SC]* documents from the WCAG 2.2 series, pages current as of their stated update dates, **accessed 2026-10-05**. The annotated claim each one supports is given in brackets.

- **[S1]** https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — W3C WAI, *SC 2.5.8 Target Size (Minimum), Level AA*. [24×24 CSS px; five exceptions; spatial targets count as one; AAA pointer]
- **[S2]** https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html — W3C WAI, *SC 2.4.13 Focus Appearance, Level AAA*. [2 CSS px perimeter area; 3:1 focused-vs-unfocused; bounding-box equivalence; two UA exceptions]
- **[S3]** https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html — W3C WAI, *SC 2.4.7 Focus Visible, Level AA*. [visible indicator; not time-limited; links to 2.4.13 and 1.4.11; techniques C15/C40/C45/G149/G165/G195; failures F55/F78]
- **[S4]** https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html — W3C WAI, *SC 2.1.1 Keyboard, Level A*. [no specific timings; path-dependent exception; platform conventions best-practice not normative]
- **[S5]** https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html — W3C WAI, *SC 2.4.1 Bypass Blocks, Level A*. [mechanism required; not duplicating UA function; the "40 links / 200 words" example]
- **[S6]** https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html — W3C WAI, *SC 2.4.3 Focus Order, Level A*. [order preserves meaning; need not match visual layout but must be logical; composite arrow-nav out of scope]
- **[S7]** https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html — W3C WAI, *SC 2.4.11 Focus Not Obscured (Minimum), Level AA*. [sticky headers/footers, non-modal dialogs, cookie banners; partial obscuration allowed at AA; scroll padding as a pass]
- **[S8]** https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — W3C WAI, *SC 1.4.11 Non-text Contrast, Level AA*. [3:1; inactive and UA-determined exceptions; "do not round, 2.999:1 would not meet the 3:1 threshold"; anti-aliasing guidance]
- **[S9]** https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html — W3C WAI, *SC 3.3.1 Error Identification, Level A*. [error in text naming the item; 3.3.1-vs-3.3.3 worked examples; auto-clamped values still need describing; native-validation disadvantages]
- **[S10]** https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html — W3C WAI, *SC 4.1.2 Name, Role, Value, Level A*. [scope incl. script-generated components; standard HTML meets it when used to spec; checked and expanded/collapsed as named states]
- **[S11]** https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html — W3C WAI, *SC 4.1.3 Status Messages, Level AA*. [two-condition definition; announced without focus; "Searching…"/"18 results returned"/"application busy" examples; results list itself excluded; ARIA19/22/23/25/27; failure F103]
- **[S12]** https://www.w3.org/WAI/WCAG22/Understanding/reflow.html — W3C WAI, *SC 1.4.10 Reflow, Level AA*. [320/256 CSS px; 1280px-at-400%-zoom equivalence; "data tables (not individual cells)" exception and the per-cell carve-back]
- **[S13]** https://www.w3.org/WAI/WCAG22/Understanding/orientation.html — W3C WAI, *SC 1.3.4 Orientation, Level AA*. [no orientation lock unless essential; fixed-orientation mounting rationale]
- **[S14]** https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html — W3C WAI, *SC 1.4.4 Resize Text, Level AA*. [200% without loss of content or functionality; author must not obstruct UA scaling]
- **[S15]** https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html — W3C WAI, *SC 1.4.12 Text Spacing, Level AA*. [the four overridable values: 1.5× line-height, 2× paragraph spacing, 0.12× letter spacing, 0.16× word spacing]
- **[S16]** https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — W3C WAI, *SC 1.4.3 Contrast (Minimum)*. [4.5:1 normal text, 3:1 large text at 24px/18.66px bold, 7:1 at AAA; the no-rounding rule]