# Unslop remediation — rescue AI-looking UI in nine ordered passes

A playbook for the screen that never met a designer: the vibecoded page where every surface glows, every label carries an emoji, spacing is whatever the model typed that day, and the copy shouts. Adapted from [unslop](https://github.com/heydamir/unslop) by Damir Sokolovsky (@heydamir), CC BY 4.0 — keep this credit in copies and adaptations.

Division of ownership: this playbook owns the **sequence**; `signs.md` owns the audit catalog; `tokens.md` owns the starting values; `craft-floor.md` owns the floor the result must land on; `signature-moves.md` owns posture. Where a rule already lives in one of those, this file points instead of restating.

Remediation fixes the craft and keeps the product — features, content, and section order stay; every size, color, word, and image becomes deliberate. Removing slop is half the job: a clean screen that could belong to any product is the next template (the **template look**), so every run ends with a screen only this product could have.

The difference between slop and craft is where the richness goes. Slop spreads color and effects across the chrome — backgrounds, buttons, borders, labels. Craft keeps the chrome quiet and spends the richness on one or two **moments** of content people remember: a rendered object, a chart whose colors each mean a series, an image from the product's world.

Work like a designer doing a **redline** review: one layer at a time, across the whole screen.

## When

- The user names the AI look: "this looks AI-generated", "vibecoded", "unslop this", "too many gradients/emoji".
- `critique.md`'s slop detector fired and the user wants the fixes applied, not just scored.
- Distinct from `polish.md` (final pass on an already-designed screen) and `distill.md` (complexity removal).

## Run it

1. **Look at the screen in a browser — the mandate.** Find the files that render it, open the page in a real browser (local file or dev server), and step through it: top, scrolled, dark mode, narrow width. Reading code supports the browser; it never replaces it. Capture before screenshots — the audit and the final check both compare against them (`render-loop.md`, "Get pixels").
2. **Audit.** Run the mechanical sweep first — `python <skill-base-dir>/scripts/unslop_grep.py <source paths>` — then walk every group in `signs.md` and list each sign found with where it lives, one line each. Grep hits are leads; the catalog walk plus the browser look is the audit.
3. **Triage** the audit honestly before planning anything:
   - **Heavy slop** — many signs across color, type, icons, and copy: run the full process below.
   - **Light slop** — a mostly designed screen with a few signs left: fix only what the audit found, take the direction from the existing brand instead of inventing one, and keep palette, type, layout, and visual. Bigger ideas — a missing moment, a scene — go into the report as suggestions.
   - **No slop** — say so plainly and offer two or three refinements at most, with exact values; apply only if the user agrees. Never change a good screen to make it different.
4. **Set the direction and stop.** Write the five lines below, show the audit and the direction, and wait for the user's answer before editing — changing the direction later means redoing everything. Skip the wait only when the user already said to just do it.
5. **Fix in nine passes, in order.** Finish a pass across the whole screen before starting the next. When nearly every line changes, plan the passes, then write the new screen in one go — as long as every pass lands. Spacing comes first because everything else reads differently once the rhythm is right; copy comes before type and layout because headline length decides size and placement; visuals and motion come last because they must fit a screen that already works without them.
6. **Check.** Render again, run the checklist below against the audit list, and fix anything still on it — then run the comparison bar (below).
7. **Report** the direction, a few lines per pass on what changed, and any image prompt written.

A light-slop pass keeps the run quick: at most three render checks. A heavy rescue iterates render → compare → fix until the checklist passes — the budget is attention per cycle, not a cap on care. **Done when:** the checklist passes on a fresh render, every sign from the audit is resolved or explicitly waived by the user, and the comparison bar (below) has been run with its side-by-side in front of the user.

## Direction

Before touching anything, write five short lines, derived from what the page says the product does and who it is for — never from what is trending. Map the result onto a `signature-moves.md` posture; the direction tailors the posture to this product.

- **Product.** What it does and for whom, one plain sentence.
- **Character.** Two or three concrete words, like "calm, exact, a little warm" or "fast, technical, playful". Clean, modern, sleek, minimal, and premium are banned — they describe every template.
- **World.** The place or material the product naturally belongs to. A note app lives near paper and ink; a monitoring tool near instruments and night shifts; a travel app near maps and window light. The world sets the tint of the neutrals, the accent, and the visual (`tokens.md`).
- **Moments.** One or two places where the screen gets rich color, material, and detail, chosen from what the product shows. A rendered card or device inside the preview, a chart whose colors each mean a series, an object from the world placed next to the content. Write what they are.
- **Signature.** One small detail only this product would have, used consistently — a live status dot for a monitoring tool, keycaps for a developer tool, a route line for a delivery app. One detail, not five.

If the product has a real brand — a logo file, a color, a typeface that is not slop — keep it and build the direction around it. A violet-to-blue gradient, sparkles, and glow are slop even when they sit in the logo, so they do not count as brand unless the user says they do.

## 1. Spacing

- Everything sits on the 4px scale (`craft-floor.md`); one-off values that break the rhythm (`mt-[13px]`, `py-[11px]`) become steps from the scale.
- Same thing, same size: all rows in a list share one height and one gap; all sibling cards share one padding.
- Space shows grouping: space inside a group is smaller than space between groups, so a list reads as one block and sections as separate ones.
- Things line up: icons sit in one column, labels start on one line, numbers align right in one column. Nothing is nudged off the line with a stray translate or odd margin.
- Padding follows density: compact panels and sidebars around 16, cards 20 to 24, page edges 24 to 32.
- Navigation is the densest part of an app: sidebar rows 32 to 36 tall with 2 to 4 between them, icons in one column, labels on one line; a section label sits closer to its own items than to the section above it (24 above, 8 below). Measure the sidebar after the pass — it is where spacing breaks most often.

## 2. Color

- Build from one neutral ramp tinted toward the world from the direction — graphite, warm, or ink from `tokens.md`, or tint your own the same way. Background, raised surfaces, borders, and text all come from that ramp.
- In product surfaces the chrome stays neutral: people look at it for hours, so the content carries the color. The world shows in the accent, the charts, and the moments, not in the surfaces. (Landing pages may tint their surfaces further — that is `premium-marketing-design`'s domain.)
- Three text roles: primary, secondary, muted. Ten slightly different lavenders is the failure.
- One accent in the chrome, used rarely: it marks the primary action, the selection, or the one number that matters (`craft-floor.md`: accent ≤ 2× per viewport).
- The moments are the exception: inside them color can be rich — several hues in a chart, a rendered object with real materials — as long as it stays inside the world and each color means something.
- A real brand color becomes the accent and leaves the surfaces; with no brand color, take the accent from the world (`tokens.md`).
- Text on the accent reaches 4.5:1; darken the accent or put dark text on it when it does not.
- On dark themes the primary button can be an off-white from the ramp with dark text, and the accent can live in a smaller place — the selection or a key figure. This often reads more deliberate than a colored button.
- Semantic colors only carry meaning, toned down to sit inside the palette.
- Depth comes from surface steps and hairlines (`dark-mode.md`, `elevation-layers.md`); borders are the ramp's primary text at 6 to 10% opacity.
- A gradient earns its place only as a small tone shift inside one neutral, like an active row going #2b2b2b → #1f1f1f. Never from one hue to another.

## 3. Icons

- Every emoji used as an icon or label decoration becomes a line icon from one set — the project's set when it has one, else lucide.
- One size and one stroke everywhere (16 or 18px, 1.5 stroke); icons take the color of their text role, usually secondary or muted, and never get their own colors.
- The icon box has the same width in every row and a fixed 8 to 10 gap to the label, so labels align.
- Drop icons that add nothing — an emoji in every card title or before every section label. Categories that need color get a small status dot. (`iconography.md` owns stroke and optical rules.)

## 4. Copy

- Headlines say what the product does for whom, in plain words, so they could not fit another product. Use the facts already on the page; invent none.
- Interface text carries no exclamation marks, and never `!!`.
- No greeting headlines ("Welcome back, Alex! 👋") — the title names the context, the page or the period ("October 2026").
- Short labels: "Search", not "Search anything...".
- A change says what it compares to: "+12% vs last month", "3 fewer vs last month".
- Headlines, subheads, labels, buttons, and captions end without a period; only paragraphs of several sentences keep theirs.
- Hype words — supercharge, seamless, unlock, magic, revolutionize, game-changing — and "AI-powered" on everything give way to what the thing actually does (`clarify.md`, `examples.md`).
- Claims that cannot be checked ("Loved by 10,000+ teams", "10× faster") become quiet and specific if the user confirms they are real, and are removed otherwise. Ask, and list them in the report.
- Mock data looks real: plausible numbers and names, never `[X]` or `123,456`.
- Badges — `PRO`, `New ✨`, `Beta 🚀` — go away unless the product really needs them, and then they are quiet text.

## 5. Type

- Choose type for the character from the family table in `tokens.md`; keep the project's font when it is part of a real brand. A default nobody chose may be swapped when another family fits the character better. One interface family, plus at most one partner from any row — a mono for figures and meta, or a display face for large headlines (`typography-web.md`).
- A few sizes from a scale and two weights, 400 and 500, with 600 at most for rare emphasis. Hierarchy comes from size and color, not from weight.
- Sentence case everywhere: uppercase tracked labels (`NAVIGATION`, `PAID THIS MONTH`) become `Navigation`, `Paid this month`.
- Small text never gets negative letter-spacing; readability on small text means bigger, slightly bolder, or slightly looser. Tight tracking belongs to large display text only.
- Numbers use `tabular-nums` and one format across the screen — if one figure is `$48,210`, the next is not `$124,860.40` (`craft-floor.md`).
- No italic for emphasis; color or weight carries it instead.

## 6. Layout

- Keep the sections and their order; alignment and proportions inside a section may change when that makes the screen clearer.
- Product surfaces keep real app proportions: the shell fills the viewport, a sidebar of 240 to 280 with fluid content capped around 1440 to 1600, and the page as long as its content. Never shrink an app into a narrow centered column; if the original was drawn as a small window on a backdrop, keep it visibly a window with desktop proportions inside.
- One primary action and at most one secondary next to it; anything else moves out of the view.
- Navigation stays quiet: logo, the existing links, one button. Log in is a quiet text link, not a second button.
- Compose the first screen as a whole: the viewport holds a complete composition with no dead empty band, and content below invites the scroll.
- The declared density class still rules every spacing and type value (`craft-floor.md`).

## 7. Details

- Nested radius: inner = outer − padding, never below 4. Controls 8 to 10, cards 12 to 16, panels 14 to 20. Not everything is a pill (`radius-motion-tokens.md`).
- Counts and meta become quiet text, often mono and muted, instead of glowing pills; keyboard shortcuts become small keycaps.
- Charts sit on a muted grid with muted mono labels, no rainbow bars inside one series and no glowing bars. One main chart is clearly the biggest thing on the screen, drawn with care; anything else that shows data is smaller and different in kind — a ranked list with thin bars or a short table, never a second chart of the same size (`charts-data-viz.md`, `dashboard-composition.md`).
- One accent per chart: the thing that matters — the current month, the tracked line, the plan that grew — gets it, and everything else sits in neutral steps of the ramp. Several hues only when the chart must tell series apart, and even then one leads and the rest stay quiet.
- Stat cards are numbers: a label, a big figure, and a change with what it compares to. A card holds a real object only when it is the very thing its number counts — a paid receipt next to paid revenue. Vary the sizes: three or four compact stats in a row above one wide chart, or a wide chart next to a narrow list.
- The chart type serves the data: a trend is a line, a comparison is bars, a share is one stacked bar or a list with bars, a single goal is a progress bar.
- The active state is a small surface step with a hairline highlight, not a gradient with a glow.
- Hover and focus states exist and stay inside the palette, with a visible focus ring for keyboard users (`craft-floor.md`).
- The logo is the product name in the main family plus a simple mark when there is one — no gradient wordmark, no sparkle tile.
- The signature detail appears where it belongs and nowhere else.

## 8. Visuals

- Decorative filler goes: glossy blobs, orbs, nebulas, floating cubes, glowing grids, holographic brains and robots say nothing about the product.
- Product surfaces almost never need generated images. Their moments come from the product itself: a chart drawn with care, figures set beautifully, real content. A physical thing the product deals with — a payment card in a finance tool — is usually better built in code with real materials.
- Generate images only for empty states, onboarding, and marketing moments, or when the user asks. The decision, the styles, the prompt recipe, and the placement live in `visuals.md`; code treatments in `effects.md`; finished screens to calibrate against in `refs.md`.

## 9. Motion

- Motion that loops for no reason goes: `animate-pulse` and `animate-ping` on things that are not live, breathing glows, floating elements, parallax, `transition-all`, and `hover:scale` on cards.
- Motion that explains something stays: a hover is a quick color or surface change, a press is a tiny scale down (0.97 to 0.98), a menu fades and rises a few pixels from where it opens, a changed number tweens (`toolkit-motion.md`, `radius-motion-tokens.md`).
- Transition color, background, border, opacity, and transform — named (`transition-colors`, `transition-[transform,opacity]`), never a catch-all. Width, height, top, and left stay unanimated; they stutter on weak devices.
- One easing curve and a few durations across the screen, from `tokens.md`: short for feedback, longer for entrances.
- At most one entrance on load: a short fade-and-rise for the main content with a small stagger, not every card flying in from a different side.

## Live sites & the story video

Both scripts live in `scripts/` next to this file. They need `node` with Playwright (`npm i playwright && npx playwright install chromium`); the story video also needs `ffmpeg`.

- **Rescue from a live URL only** — no code access? Save it first: `node scripts/snapshot.mjs <url> unslop/original.html` (add `--dark` or `--light` to match the theme the user sees). It also saves `original.live.png`; render the saved copy and compare the two before starting, then work on the copy and say in the report that the deliverable is redesigned code to hand back.
- **Story video (optional, when the user wants something to share)** — a square ~10s video of the screen unslopping itself: one story file (`unslop-story/story.html`, a standalone copy of the ORIGINAL screen with its styles inline), three to five steps written as cumulative CSS classes (`.s1`, `.s2`, …) that change values only — nothing is swapped, everything morphs in a wave from the top left down; changing copy rolls in letter by letter (at most eight swaps); red redlines (`data-gap`, `data-radius`) measure the slop and turn white as the passes fix it; the frame shows only the screen, cropped close on the most visible change. Render with `node scripts/story.mjs unslop-story/story.html unslop-story.mp4` (`--wide` for 16:9, `--play` to loop live in a browser). Pull a few frames with ffmpeg and check them before handing over — checking the story file and the video does not count against the run's three-render budget. Every video carries a small `unslop by @heydamir` credit, as the license asks. The clean result still ships as normal code without `.s` classes or story attributes.

## Do not

- Do not rename the product, even when the name has AI in it, and do not replace a real logo. When the logo itself is slop — an emoji or a sparkle in a gradient tile — redraw it flat: the wordmark alone in the new type, or a simple glyph from the product's idea in one solid color. Never a glossy ball, a glow, or a gradient tile; those read as AI at first sight.
- Do not change what the product is: features, content, and the order of sections stay unless the user asks for more. Placeholder content that means nothing may be replaced with content that does.
- Do not replace removed decoration with new decoration, and do not swap one trend for another — glass, grain, noise, neon, bento grids.
- Do not invent features, claims, or data.
- Do not fall back to the same look for every product: the direction decides the palette tint, the type, and the visual, not habit.

## The comparison bar

The finished screen is judged against real work, never against itself.

1. **The kit's refs.** Screenshot the result and put it side-by-side with `refs.md`'s four images. Name what each ref has that the render does not — composition, the moment's material quality, restraint — fix the top gaps, and repeat until nothing a client would notice remains.
2. **Production work from `design-systems/`.** Pick the 2–3 packs nearest the product's category and posture (`design-systems/README.md` is the index). Where a pack carries screenshots or images, put same-surface frames next to the render and compare. Where a pack is text-only, compare against its written values — type ramp, spacing scale, radius scale, color roles — value by value. Image coverage in `design-systems/` grows over time; use whatever is there. The step itself is never skipped.

The comparison output — the side-by-side and the gap list — goes in front of the user. Their eye is the final bar; a builder's own "same level" verdict over-claims (observed in the first full run, 2026-11-01), so label it self-graded until the user confirms.

## Checklist

- [ ] The direction is written and every pass follows it
- [ ] Every spacing value is on the 4px scale and equal things have equal sizes
- [ ] Icons, labels, and numbers each sit in one aligned column
- [ ] One tinted neutral ramp, three text roles, one accent with enough contrast
- [ ] No hue gradients, gradient text, glows, colored shadows, or color blobs
- [ ] No emoji left in the interface
- [ ] One icon set at one size and stroke
- [ ] Type chosen for the character, weights 400 to 600, sentence case, no italic, no negative tracking on small text
- [ ] No exclamation marks, no trailing periods on short strings, no greeting headline, no unverified claims
- [ ] Numbers in one format with tabular figures
- [ ] Nested radii add up
- [ ] No looping or bouncy motion, one easing curve, no animated layout properties
- [ ] Template look: swap this product's name for another product's — if the screen still fits, push the direction harder in the copy, the visual, and the signature detail

Refs: `signs.md`, `tokens.md`, `visuals.md`, `effects.md`, `refs.md`, `craft-floor.md`, `critique.md`, `signature-moves.md`, `polish.md`, `examples.md`.
