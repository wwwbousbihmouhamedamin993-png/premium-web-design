# Toolkit — Godly (godly.design)

Load at **direction-setting time only**, before writing the brief in `screen.md`. This is a gallery,
not a source of truth, and the images in it are other people's work.

## What it is

Godly is a curated gallery of web, app, UI and visual design work published on the internet. It is
sponsored by Framer and accepts submissions.

## Sections — and which one you actually want

| Section | Contains | Use in this skill? |
|---|---|---|
| `/screenshots` (Apps) | Logged-in **application** UI screenshots | **Yes — this is the relevant one** |
| `/websites` | Marketing and landing sites | No — belongs to `premium-marketing-design` |
| `/hero`, `/cta`, `/footer` | Individual marketing sections | No |
| `/og-images`, `/logos`, `/app-icons` | Brand and social assets | No |
| `/templates`, `/tools`, `/resources`, `/posts` | Cross-category | Rarely — check before using |
| `/trending`, `/categories` | Discovery indexes | Only to find a direction to research properly |

**The `/websites` vs `/screenshots` distinction is the whole point.** A gallery that mixes marketing
and product UI will drift a product surface toward marketing aesthetics if you browse it without that
filter — which is exactly the Refuse-list failure `craft-floor.md` guards against. Use `/screenshots`.

Interface affordances: `⌘K` search, `⌘J` to open a result in a preview pane, arrow keys to navigate,
`Esc` to dismiss.

## How to use it without copying

The gallery's value is **calibration**, not templates. It answers "what does the best version of this
screen look like", which is a question about standards, not about layout.

1. **Browse `/screenshots` for the surface class, not the product.** Looking for a project-management
   board? Look at project-management app UIs, not at Linear specifically — you want the class, not
   one house's answer.
2. **Name the move, then close the tab.** "Records are grouped in a two-pane split with the detail
   on the right" is a decision you can implement. A screenshot is not a spec.
3. **Then go to the primary source.** For real token values, component states, or interaction
   behaviour, use `signature-moves.md` and `design-systems/<app>/` — those are documented and cited.
   A gallery image has no states, no dark mode, no keyboard path, and no empty state.
4. **Never let a gallery image set the density class.** The whole failure mode of inspiration-driven
   design is drifting Standard surfaces into Dense or vice versa. Density comes from
   `information-density.md`.

## Provenance

Godly's images are other designers' and companies' work, curated by a third party. That is a
different posture from the `design-systems/` library, where this skill reverse-engineers *token values*
from public documentation and records an as-of date and source per app. **A gallery screenshot
cannot be reverse-engineered into tokens — it has no tokens.** So the discipline differs:

- From `design-systems/`: extract documented values, cite the source, pin an as-of date.
- From Godly: extract *direction only*. Never copy an asset, and never treat a screenshot as evidence
  for a rule.

If a screenshot genuinely needs to be captured into this skill's own repository, follow
`design-systems/LICENSE-NOTES.md`.

## Not found

- **No stated licensing or reuse terms** for gallery content on the pages read — no licence, no
  attribution policy, no submission agreement was visible. Treat reuse as not granted.
- **No published curation criteria**, so "curated" carries no verifiable standard. Do not treat
  presence in the gallery as validation.
- **No API or programmatic access** documented; the sections are browsed, not queryable.
- **No accessibility, performance, or state information** accompanies any entry — by construction.

## Sources

| Source | Publisher | URL | Accessed |
|---|---|---|---|
| Godly Design Inspiration homepage and section index | Godly | https://godly.design/ | 2026-10-05 |

Section names and keyboard affordances above are quoted from that page. Absence of licensing terms
is recorded as an observation of that page, not as a claim that none exists anywhere.