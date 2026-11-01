# MEMORY — premium-web-design build state

Resumable handoff. Read this first in a new session.

## What this is

A third sibling skill for **logged-in B2B SaaS web product surfaces** — the layer none of the
existing skills covered. Sits alongside `premium-mobile-design` (200 mobile systems) and
`premium-marketing-design` (74 marketing systems).

Root: `C:\Users\nigatron\.gemini\config\skills\premium-web-design\`

## Status: reference library COMPLETE, design systems NOT STARTED

```
node scripts/selfcheck.mjs     → ERRORS 0, WARNINGS 0, PASS
91 reference files · 131 design-system folders · 12 categories
```

## Decisions locked (do not relitigate)

| Decision | Choice |
|---|---|
| Approach | **New sibling skill, not a fork.** Impeccable stays an external detector dependency, invoked from `audit`/`loop`. Never vendored or re-maintained. |
| Scope | **Product surfaces only.** Marketing pages → `premium-marketing-design`. Mobile → `premium-mobile-design`. |
| Stack | **Framework-neutral.** Tokens as CSS custom properties; `DESIGN-[framework].md` adapters optional and generated only if a stack is detected. |
| Images | **Text + screenshots.** `DESIGN.md` is load-bearing; one downscaled `screenshot.png` per app is supporting evidence only, lazily referenced. |
| Screens | **~130 apps**, one canonical category each, no duplicates. |

## The core invention: density classes

Focused (16px base, forms/auth) · Standard (14–15px, app screens) · Dense (12–13px, tables/consoles).
Every type and spacing rule is tagged to a class. This is what lets one skill serve a Stripe-style
console and a Stripe-style checkout, and it is what overrides Impeccable's marketing-page defaults —
`tiny-interface-text` is an **advisory** in Dense and a **failure** in Focused.

The 5-column table lives in `craft-floor.md`. A machine check compares it across all files, so
reproduce it verbatim or route to `craft-floor.md` instead of duplicating.

## Corrections research forced (do not reintroduce)

1. **Target sizes** — WCAG 2.2 SC 2.5.8 is **24×24 px at AA**; 44×44 (SC 2.5.5) is **AAA, not AA**.
   An earlier draft's "32×32" matched nothing.
2. **Nav caps** — "max 7 menu items" is a **misreading NN/g explicitly rejects**. Group and label;
   never cap. Carbon's real sidebar constraint is about *kind* (no unbounded user content), not count.
3. **Latency** — the 400 ms Doherty figure is **not in the primary 1982 paper**, which concludes for
   sub-second. Use Nielsen's 0.1 / 1.0 / 10 s, with a percent-done indicator required beyond ~10 s.
4. **Whitespace "20% comprehension"** — **no traceable primary source.** Chaparro et al. 2004 reports
   margins affect speed and comprehension with no percentage, and leading did not. Marked not-found.
5. **Token layering** — the primitive → semantic → component taxonomy is a **house rule**, not a
   standard. DTCG 2025.10 says token groups "are arbitrary" and tools "SHOULD NOT" infer purpose.
6. **`light-dark()`** — Baseline 2024 **Newly available** while everything else is "Widely available".
   Do NOT make it the primary theming primitive; shadcn and Tailwind both chose selector remap.
7. **Playwright MCP** — `@playwright/mcp` and `chrome-devtools-mcp` are real and verified. My earlier
   claim that none exists was wrong; what is true is that neither is wired to a given session's
   tool list, so `render-loop.md` treats them as "use if present" with CLI fallbacks.

## Sourcing contract (why this build differs from a training-data build)

Every reference file carries inline citations per numeric threshold plus a `## Sources` section with
URL, publisher, and accessed date. Unsubstantiated claims appear as `**Not found:**` with what would
settle them. **Line-length targets were deliberately not enforced** — compressing a file means
deleting citations, which defeats the purpose. `selfcheck.mjs` enforces a 500-line smell ceiling only.

## Scripts

- `scripts/context.mjs` — loads PRODUCT.md/DESIGN.md, detects framework + styling from `package.json`,
  emits density hints. Strips UTF-8 BOM before `JSON.parse` (Windows-authored `package.json` files
  carry one and `JSON.parse` rejects it).
- `scripts/selfcheck.mjs` — link targets, sources sections, line band, density-table consistency,
  design-system shape. Exit 1 on error.

## Design systems — NOT STARTED

131 empty app folders exist under `design-systems/<category>/<app>/`. Each needs its own research
pass to extract real token values into `DESIGN.md` + `README.md` + `screenshot.png`.

Template per app: identity & posture · colour tokens (primitives + semantics, light and dark) ·
type ramp · spacing + density defaults · radius · elevation · component inventory with states ·
density-class defaults · signature moves · what *not* to copy · sources + **as-of date**.

The as-of date is not optional — Figma reorganised its chrome, W&B moved to CoreWeave's docs host,
and Okta's Admin Dashboard page carries a "Classic Engine publication" banner.

Also needed: `design-systems/README.md` (index) and `design-systems/LICENSE-NOTES.md` (screenshot
provenance).

## Known weak spots (flagged, not hidden)

- **Vendor URLs are rotting.** Several moved or 404'd mid-2026: Carbon's
  `/components/switcher/` and `/patterns/onboarding-pattern/` return 404; `polaris.shopify.com`
  now redirects to a surfaces page. Substitutes used in the library: Carbon's UI shell header
  guidelines for the switcher pattern, `shopify.dev` web-components badge docs for Polaris.
  **Expect this during the design-systems phase** — re-fetch rather than trusting a URL from an
  older session, and pin an as-of date per app.
- **Cloud admin consoles and CRM/sales** returned zero substantiated apps in research — ~18 of the
  131 entries are provisional pending a gap-pass round.
- **Shopify admin** is Claimed-only (HTTP 403); re-fetch before writing its spec.
- **`command-palette.md`, `bulk-selection-actions.md`, in-app billing UI, audit-log UI** have no
  design-system precedent; built from ARIA/vendor docs, so visual guidance is weaker.
- **No date-time picker sourcing on timezones** — that file's DST rules are judgement, not fact.
- **Chromium-specific numbers are labelled as such** (1250px/2500px lazy thresholds, 97.5%/92.6%
  load-in-10ms) — do not generalise them to other browsers. Same for Anthropic's context windows
  and Stripe features marked "Public preview" on the page checked.
- Research workspace (plan, 6 findings, ledger L1–L52, report, citation check) is in
  `%LOCALAPPDATA%\Temp\opencode\deep-research\` — outside the skill, and will not survive cleanup.
  Copy it somewhere durable if it matters.