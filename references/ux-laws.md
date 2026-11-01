# UX laws — only the enforceable ones

Load when a rule needs a number behind it. This file exists to stop the most common failure in
design guidance: citing a named law as though it settles a question, when it carries no threshold.

Most named UX laws have **no measurable threshold**. They are useful as vocabulary and dangerous as
gates. This file splits them into three tiers and says plainly which is which.

---

## Tier 1 — enforceable: these become rules

Each has a number, printed by the primary source. These are the only laws permitted to gate a pass.

### Response-time limits — Nielsen, citing Miller 1968 and Card/Robertson/Newell 1991

| Limit | What the user experiences | Required behaviour |
|---|---|---|
| **0.1 s** | Feels like direct manipulation | Nothing to show |
| **1.0 s** | Flow of thought stays uninterrupted | Keep the user informed at the edge |
| **10 s** | Attention stays on the task | **Percent-done indicator required**, plus a signposted way to interrupt |

Nielsen adds a nuance that most restatements drop: for operations between roughly 2 and 10 seconds a
true percent-done bar may be *overkill* and a true progress bar violates "display inertia" — less
conspicuous feedback is correct in that band.

**`craft-floor.md` applies this.** Do not quote a single "400 ms" figure: see Tier 3.

### Target size — WCAG 2.2

| Criterion | Level | Size | Note |
|---|---|---|---|
| SC 2.5.8 Target Size (Minimum) | **AA** | **24×24 CSS px** | With a spacing exception: a 24 px circle centred on each target's bounding box must not intersect another target's. Meeting only the spacing exception still passes. |
| SC 2.5.5 Target Size (Enhanced) | **AAA** | 44×44 CSS px | **Not AA.** Most secondary pages present 44 px as the AA requirement; that is wrong. |

The spacing exception is what makes Dense rows legal: 24 px targets are acceptable *with* adequate
spacing, and 2.5.8 defines "a minimum size and, if that can't be met, a minimum spacing."

### Contrast — WCAG 2.2

| Criterion | Level | Ratio |
|---|---|---|
| SC 1.4.3 Contrast (Minimum) | AA | 4.5:1 text; **3:1** large text |
| SC 1.4.3 | AAA | 7:1 |
| SC 1.4.11 Non-text Contrast | AA | 3:1 for UI boundaries and meaningful graphics |

**Do not round.** W3C is explicit: 4.499:1 does not meet 4.5:1, and 2.999:1 does not meet 3:1.

Large text is defined as 24 px, or 18.5 px bold (14 pt / 18 pt at 1pt = 1.333px).

The figures are derived, not arbitrary: 3:1 is the ANSI-HFES-100-1988 minimum for normal observers,
and 20/40 visual acuity carries roughly a 1.5× contrast-sensitivity loss, giving 3 × 1.5 = 4.5.

### Core Web Vitals — Google

| Metric | Good | Measured at |
|---|---|---|
| LCP | ≤ 2.5 s | 75th percentile |
| INP | ≤ 200 ms | 75th percentile |
| CLS | ≤ 0.1 | 75th percentile |

Segmented by mobile and desktop. **INP cannot be measured in a lab** — it requires real user input —
so use **TBT** as the lab proxy. Thresholds are stable-by-policy but allowed to change annually.

### Plain language — U.S. GSA / Digital.gov

- Paragraphs **no more than 150 words**, in three to eight sentences.
- **Never longer than 250 words.**
- One idea per sentence. One topic per paragraph or section, with a topic sentence.
- Present tense, active voice.

Readability formulas (Flesch–Kincaid) exist and are computable, but carry a documented weakness: they
were built for school books, ignore between-reader differences, and neglect content, layout and
retrieval aids. If you enforce a grade ceiling, state that limitation alongside it.

---

## Tier 2 — formulas only: no static rule can be derived

Each needs an empirically fitted constant, so none yields a number you can put in a checklist.

### Hick's law — `T = b · log₂(n + 1)`

Two reasons it cannot become "cap the menu":

1. `b` is fitted from measured data, not fixed.
2. It has a documented **exception that breaks the rule reading**: searching a randomly ordered list
   takes linear time, so the law "does not apply" there. An alphabetical list where the user knows
   the name permits a logarithmic strategy.

Also exempted: verbal response to familiar stimuli, and saccade responses.

### Fitts's law — Shannon form `MT = a + b · log₂(D/W + 1)`

Included in ISO 9241 as a recommended pointing-evaluation method. But because the index of difficulty
depends only on the *ratio* of distance to width, the model implies a distance/width pair can be
rescaled arbitrarily without affecting movement time — which is impossible in reality.

**So Fitts's law cannot justify a pixel minimum.** Do not cite it as the origin of 24 px or 44 px;
those come from WCAG.

It does yield two genuinely useful layout rules with no numeric minimum: the **rule of the infinite
edges** (targets on screen edges have effectively unbounded width in one dimension) and **magic
corners** (two colliding edges form a theoretically unbounded target).

### Miller 1956 (7±2) and Cowan 2001 (4±1)

Both are real and citable, but they describe **chunks held in memory**, not menu length or column
count. Miller himself said the number seven was rhetorical and the limit was in chunks, not bits.
Cowan proposes about four chunks; Gobet and Clarkson found over half of recall conditions yielded
only about two.

Reconciling them: seven applies when chunking is unrestricted, four applies when neither rehearsal nor
long-term memory can build chunks.

---

## Tier 3 — vocabulary only: never a pass/fail gate

### Nielsen's ten usability heuristics

Nielsen's own words disqualify them as rules: they are called "heuristics" because they are **"broad
rules of thumb and not specific usability guidelines."** No number attaches to any of the ten.

Use them as review vocabulary. Never as a gate.

### The "7 menu items" rule is a misreading

This is the single most misapplied claim in web design, and NN/g rejects it in writing:

> "It's a common misconception that limited short-term memory implies that menus should be similarly
> limited to 7 items. It's fine to have longer menus (if needed), because users don't have to
> memorize the full list of menu items […] if you make a menu too short, the choices become overly
> abstract and obscure."

The correct rule is **group and label, never cap.** The real constraint on navigation is about *kind*,
not count: unbounded user-created content must not enter shell navigation, because usability drops as
items grow — with drill-down as the sanctioned alternative. See `sidebar-navigation.md`.

### Also vocabulary, no threshold found

Recognition over recall (mechanism is cue count; no number), von Restorff / isolation effect, the
Zeigarnik effect, the peak-end rule, cognitive load theory (NN/g gives "slots in working memory" with
no count), and the Gestalt principles of proximity and common region.

### The 400 ms figure

The famous Doherty threshold number is **not in the primary source**. The 1982 IBM paper concludes for
*sub-second* response — "rapid system response time, ultimately reaching sub-second values […] offers
the promise of substantial improvements in user productivity" — and its worked data uses
3.0 / 2.0 / 1.0 / 0.6 / 0.3 seconds. The text contains no occurrence of "400".

Widely repeated later by Laws of UX as the requirement Doherty & Thadani set, replacing the previous
two-second standard. Treat 400 ms as a later restatement, not the paper's finding.

**Use Nielsen's 0.1 / 1.0 / 10 s instead** — those are attributable and they are what Tier 1 needs.

---

## How to use this file

- Cite **Tier 1** when a rule needs defending. It will survive scrutiny.
- Reach for **Tier 2** when reasoning about why a design is faster or slower — not to produce a number.
- Use **Tier 3** to structure a critique, never to fail a build.
- If you catch yourself writing "because of Miller's law," stop. Ask which tier you are in.

**Not found:** any primary source publishing a target option count, a maximum nav depth, or a
per-screen component limit as a numeric standard. W3C endorses *a user-facing density control* as an
accessibility affordance (SC 1.4.4 Resize Text / related), but no source converts that into a count.
The density classes in `craft-floor.md` are this skill's own heuristic.

## Sources

| Source | Publisher | URL | Accessed |
|---|---|---|---|
| Response Times: The 3 Important Limits | Nielsen Norman Group | https://www.nngroup.com/articles/response-times-3-important-limits | 2026-10-05 |
| Short-Term Memory and Web Usability | Nielsen Norman Group | https://www.nngroup.com/articles/short-term-memory-and-web-usability/ | 2026-10-05 |
| 10 Usability Heuristics for User Interface Design | Nielsen Norman Group | https://www.nngroup.com/articles/ten-usability-heuristics/ | 2026-10-05 |
| Memory Recognition and Recall in User Interfaces | Nielsen Norman Group | https://www.nngroup.com/articles/recognition-and-recall/ | 2026-10-05 |
| Minimize Cognitive Load to Maximize Usability | Nielsen Norman Group | https://www.nngroup.com/articles/minimize-cognitive-load/ | 2026-10-05 |
| Understanding SC 2.5.8 Target Size (Minimum) (AA) | W3C WAI | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html | 2026-10-05 |
| Understanding SC 2.5.5 Target Size (Enhanced) (AAA) | W3C WAI | https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html | 2026-10-05 |
| Understanding SC 1.4.3 Contrast (Minimum) (AA) | W3C WAI | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html | 2026-10-05 |
| Understanding SC 1.4.11 Non-text Contrast (AA) | W3C WAI | https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html | 2026-10-05 |
| Web Vitals | Google / web.dev | https://web.dev/articles/vitals | 2026-10-05 |
| Plain language guide — Clear and short | U.S. GSA / Digital.gov | https://digital.gov/guides/plain-language/writing/clear-short | 2026-10-05 |
| Plain language guide — Writing for understanding | U.S. GSA / Digital.gov | https://digital.gov/guides/plain-language/writing | 2026-10-05 |
| The Economic Value of Rapid Response Time (1982, republished) | Doherty & Thadani / IBM | https://jlelliotton.blogspot.com/p/the-economic-value-of-rapid-response.html | 2026-10-05 |
| Doherty Threshold (the 400 ms restatement) | Laws of UX | https://lawsofux.com/doherty-threshold/ | 2026-10-05 |
| Hick's law | Wikipedia (secondary — lacks inline citations) | https://en.wikipedia.org/wiki/Hick%27s_law | 2026-10-05 |
| Fitts's law | Wikipedia (secondary — lacks inline citations) | https://en.wikipedia.org/wiki/Fitts%27s_law | 2026-10-05 |
| The Magical Number Seven, Plus or Minus Two | Wikipedia (secondary) | https://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two | 2026-10-05 |
| Flesch–Kincaid readability tests | Wikipedia (secondary) | https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests | 2026-10-05 |

Tier 2 sources are secondary and are used for reasoning, never as gates. The Doherty 400 ms figure is
recorded as a **conflict**: the primary paper's sub-second conclusion (Verified) versus the widely
repeated 400 ms restatement (Claimed). For design purposes this skill weighs the primary paper.