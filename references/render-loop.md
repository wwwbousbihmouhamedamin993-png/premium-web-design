# Render loop — you cannot design what you cannot see

Rules produce competent output; looking produces good output. Every screen gets rendered and critiqued on
real pixels before it is called done. **Minimum two critique–fix passes**; continue until a fresh pass finds
no floor violation. Never declare a screen finished from code alone.

Web has a better toolset than mobile here: a headless browser produces true CSS-pixel screenshots with no
display, no emulator, and no device. There is never a good excuse for shipping an unrendered screen.

---

## Get pixels (per stack)

**Playwright MCP is optional.** If the agent has a browser MCP server connected, use it — it is the lowest
friction path. If it does not, use the CLI. Do not install one mid-task and do not assume one exists.

| Tool | Verified? | Screenshot call |
|---|---|---|
| **Playwright MCP** (`@playwright/mcp`) | ✅ exists | [`browser_take_screenshot`](https://playwright.dev/mcp/tools/screenshots) |
| **Chrome DevTools MCP** (`chrome-devtools-mcp`) | ✅ exists | [`take_screenshot`](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md) |
| **Playwright CLI** (`@playwright/cli`) | ✅ exists | [`playwright-cli screenshot`](https://playwright.dev/agent-cli/commands/screenshots-pdf) |
| **Playwright library** | ✅ exists | [`page.screenshot()`](https://playwright.dev/docs/api/class-page#page-screenshot) |
| **Puppeteer** | ✅ exists | [`page.screenshot()`](https://pptr.dev/api/puppeteer.page.screenshot) |

### Serve the page first. Always.

**Next.js** — `next dev` starts the dev server with HMR on `http://localhost:3000` by default
([Next.js CLI docs](https://nextjs.org/docs/app/api-reference/cli/next)); override with `next dev -p 4000`.
Critique against a **production** build when the layout depends on real font loading or bundle splitting:
`next build && next start`.

**Any other framework** — run that project's own dev or preview server (the one in `package.json`).

**Plain static / HTML / a lone `.tsx` file** — no dev server needed:

```bash
python -m http.server 9000
```

([Python `http.server` CLI](https://docs.python.org/3/library/http.server.html#command-line-interface);
listens on 8000 by default, `--directory <dir>` and `--bind 127.0.0.1` available.) **Not found:** a
first-party `playwright-cli serve` / built-in static server command — none appears in the Playwright CLI or
library docs. What would settle it: a Playwright docs page or CLI reference listing a serve command. The
Python one-liner above is the fallback and needs no install on most machines.

Playwright's test runner can boot the server itself via `webServer` in `playwright.config.ts`
([Playwright web server docs](https://playwright.dev/docs/test-webserver)) — worth wiring up **once** in the
host project so every later pass is one command, but it requires a test-runner dependency and is not
required to run a render pass.

### Playwright MCP (when present)

Registered as `"playwright"` running `npx @playwright/mcp@latest`
([Playwright MCP introduction](https://playwright.dev/mcp/introduction)). Defaults to **headed**; add
`--headless` for a machine with no display ([MCP configuration](https://playwright.dev/mcp/configuration/options)).

- `browser_navigate` → `browser_take_screenshot { fullPage: true, filename: "dark.png" }`
- `browser_resize` for viewport changes; `browser_wait_for { text: "…" }` to await async regions
- `browser_console_messages { level: "error" }` for the error gate
- `--viewport-size=1280x720`, `--browser=chrome|firefox|webkit|msedge`, `--device="iPhone 15"`

With no `filename`, the image is returned inline so the agent can see it. `--image-responses=omit` keeps
images out of the response — do not use that while critiquing.

### Playwright CLI (no MCP configured)

```bash
npm install -g @playwright/cli@latest   # requires Node.js 20+
playwright-cli install                   # creates .playwright/, downloads the browser
playwright-cli open http://localhost:3000
playwright-cli resize 1440 900
playwright-cli screenshot --filename=pass1-default.png
playwright-cli screenshot --full-page --filename=pass1-full.png
playwright-cli screenshot --hires --filename=pass1-2x.png
playwright-cli console error
playwright-cli eval "() => document.title"
playwright-cli run-code "async (page) => { await page.emulateMedia({colorScheme:'dark'}); }"
```

All commands and flags above are from the [Playwright CLI command reference](https://playwright.dev/agent-cli/introduction)
and [Screenshots & PDF](https://playwright.dev/agent-cli/commands/screenshots-pdf) / [Console & Eval](https://playwright.dev/agent-cli/commands/console-eval) pages.
The CLI is **headless by default** ([CLI configuration](https://playwright.dev/agent-cli/configuration)) and
returns an accessibility snapshot with element refs after every command, so it doubles as an a11y check.
If Playwright is already a project dependency, `npx playwright cli <command>` works with no global install.

### Playwright library (script you own — the repeatable path)

```js
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();            // headless by default
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2,                             // dpr; defaults to 1
    colorScheme: 'dark',
  });
  const page = await context.newPage();

  const errors = [];
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', (e) => errors.push(String(e)));

  await page.goto('http://localhost:3000/billing');
  await page.evaluate(() => document.fonts.ready);   // see "Wait properly" below
  await page.screenshot({ path: 'shots/dark-2x.png', animations: 'disabled' });
  console.log(errors);
  await browser.close();
})();
```

Every option above is documented: `viewport` / `deviceScaleFactor` / `colorScheme` on `browser.newContext`
([Playwright API](https://playwright.dev/docs/api/class-page#page-screenshot), defaults noted on each
option), `page.on('console')` and `page.on('pageerror')`
([Playwright Page events](https://playwright.dev/docs/api/class-page)), `page.screenshot({ animations })`
where `'disabled'` fast-forwards finite animations and cancels infinite ones to their initial state
([screenshot options](https://playwright.dev/docs/api/class-page#page-screenshot)).

Useful `page.screenshot()` options, all from the same page:

| Option | Effect |
|---|---|
| `fullPage: true` | whole scrollable page, "as if you had a very tall screen" ([Screenshots guide](https://playwright.dev/docs/screenshots)) |
| `scale: 'css'` | one image pixel per CSS pixel (small file); default is `'device'` |
| `scale: 'device'` | one pixel per device pixel — 2× DPR captures are twice as large |
| `animations: 'disabled'` | kill animations so captures are deterministic |
| `caret: 'hide'` | hide the text caret (this is the default) |
| `mask: [locator]` | overlay a `#FF00FF` box — cover avatars and timestamps |
| `omitBackground: true` | transparent PNG (not for `jpeg`) |
| `type: 'png' \| 'jpeg' \| 'webp'` | `webp` at `quality: 100` is lossless |

Element-level: `await page.locator('.billing-table').screenshot({ path: '…' })` ([Screenshots guide](https://playwright.dev/docs/screenshots)).

### Puppeteer (when the project already uses it)

```js
const puppeteer = require('puppeteer');
const browser = await puppeteer.launch();                  // headless: true by default
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
const errors = [];
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
page.on('pageerror', (e) => errors.push(e.message));       // uncaught exception in page
await page.goto('https://example.com', { waitUntil: 'networkidle2' });
await page.screenshot({ path: 'shot.png', fullPage: false });
```

`setViewport` and `screenshot` from the [Puppeteer API](https://pptr.dev/api/puppeteer.page.setviewport);
`Viewport` fields `width` / `height` / `deviceScaleFactor` (default `1`) / `hasTouch` / `isMobile`
([Viewport interface](https://pptr.dev/api/puppeteer.viewport)); `console` / `pageerror` events from
[PageEvent](https://pptr.dev/api/puppeteer.pageevent). Puppeteer launches the **new headless mode** by
default; `headless: 'shell'` selects the older `chrome-headless-shell` binary and `headless: false` goes
headful ([Puppeteer headless modes](https://pptr.dev/guides/headless-modes)).

### Chrome DevTools MCP (when present)

`npx -y chrome-devtools-mcp@latest` ([Chrome for developers: agents](https://developer.chrome.com/docs/devtools/agents)).
Beyond screenshots it exposes `emulate` (`colorScheme`, `cpuThrottlingRate`, `networkConditions`,
`viewport: '<w>x<h>x<dpr>[,mobile][,touch][,landscape]'`), `performance_start_trace`,
`lighthouse_audit`, and `list_console_messages` — all from the
[tool reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md).
`--slim --headless` gives a minimal tool set on a machine with no display. It officially supports Google
Chrome and Chrome for Testing only.

### One-shot Chrome (last resort, no library)

```bash
chrome --headless --screenshot --window-size=1440,900 --timeout=10000 https://example.com
```

Flags from the [Chrome Headless command-line reference](https://developer.chrome.com/docs/automation-and-testing/headless-cli):
`--screenshot` writes `screenshot.png` into the working directory, `--window-size` sets the viewport,
`--timeout` is the max wait in ms, and `--virtual-time-budget` fast-forwards timers.

### No display required

Chrome's unified headless mode **creates but does not display** platform windows and has all features of
the headed browser ([Chrome Headless mode](https://developer.chrome.com/docs/chromium/headless)). Since
Chrome 112. So a headless render pass works on a headless CI box, a container, or a locked-down laptop —
this is not the degraded path, it is the normal path.

---

## Wait properly, or the screenshot lies

An early screenshot shows a skeleton. That is a false critique, and re-fixing it wastes a pass.

- **Playwright explicitly discourages `networkidle`.** `page.waitForLoadState('networkidle')` is marked
  **DISCOURAGED** — "Don't use this method for testing, rely on web assertions to assess readiness
  instead" ([Playwright API](https://playwright.dev/docs/api/class-page#page-screenshot); the same
  warning appears on every `waitUntil` option).
- **Wait on a web assertion, not a clock.** `await expect(page.getByRole('table')).toBeVisible()` or
  `await page.getByText('Invoice total').waitFor()` retries until true ([auto-waiting](https://playwright.dev/docs/actionability)).
- **Playwright auto-waits before every action anyway** — it checks Visible, Stable, Receives Events, and
  Enabled, and "operates as a very fast user" ([Navigations](https://playwright.dev/docs/navigations),
  [Auto-waiting](https://playwright.dev/docs/actionability)). A screenshot is *not* an action, so it gets
  none of that protection — you must wait explicitly.
- **Fonts:** `await page.evaluate(() => document.fonts.ready)` — resolves "once the document has
  completed loading fonts, layout operations are completed, and no further font loads are needed"
  ([MDN `FontFaceSet.ready`](https://developer.mozilla.org/en-US/docs/Web/API/FontFaceSet/ready)). Skip
  this and every critique is against a fallback font.
- **One re-shot is the tell.** If a screenshot differs from the one 300ms earlier, you caught a transition.
  Re-shoot before critiquing.
- **Puppeteer:** `waitUntil: 'networkidle2'` (≤2 connections for 500ms) or `'networkidle0'` (0 connections)
  are the available values, alongside `'load'` and `'domcontentloaded'`
  ([PuppeteerLifeCycleEvent](https://pptr.dev/api/puppeteer.puppeteerlifecycleevent)). If the app polls or
  holds an SSE connection, use `'load'` plus an explicit selector wait instead.

---

## The passes (each pass = render + look + name what's wrong)

Run all nine per screen. Each is one re-render; batch the captures, then look at the images.

1. **Default state, light, 1440×900** — hierarchy: does the eye land on the right thing first? Is the
   primary action obvious in one glance? Is the density class right for the surface?
2. **Populated with realistic long data** — the pass that finds real defects. Long org names, a 90-character
   email, a plan title that wraps to two lines, `€1,284,930.55`, a zero row, a 1,247-item count, a
   relative timestamp. Fixed widths and one-line truncations collapse here.
3. **Dark mode** — `colorScheme: 'dark'`. No shadows on dark surfaces, canvas not pure black, accent and
   contrast survive, status colours still readable.
4. **Narrow viewport** — 320 CSS px wide. This is the automated form of WCAG SC 1.4.10 Reflow, whose
   requirement is "a width equivalent to 320 CSS pixels" for vertical content (and "256 CSS pixels" for
   horizontal), with 320 CSS px being "equivalent to a starting viewport width of 1280 CSS pixels wide at
   400% zoom" ([W3C, Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)). Nothing important
   may require two-dimensional scrolling; data tables may legitimately scroll in their own container.
5. **200% text zoom** — SC 1.4.4 requires text resizable "up to 200 percent without loss of content or
   functionality" ([W3C, Resize Text](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html)).
   **Not found:** a documented Playwright or Puppeteer API that sets the browser's *page zoom level* — the
   published `page.screenshot` / `page.setViewport` / `browser.newContext` options cover viewport and DPR
   only, not zoom. What would settle it: a Puppeteer or Playwright page documenting a zoom/zoom-factor
   option, or a Chrome launch-flag reference listing one (`--force-device-scale-factor` appears in
   community threads but is **not** on the official
   [Headless command-line reference](https://developer.chrome.com/docs/automation-and-testing/headless-cli),
   so do not rely on it). Honest degraded approximation for this pass: use pass 4's 320px capture, plus a
   text-only scale check by overriding the root font size in the page and re-shooting — and say in the
   report that page-level zoom was not exercised.
6. **Keyboard-only traversal** — Tab from the top of the document. Every interactive control is reachable,
   `:focus-visible` is visible and never removed, order follows the DOM, focus never lands on nothing, and
   a dialog or drawer traps focus and returns it on close. Playwright: `page.keyboard.press('Tab')` in a
   loop, or the CLI's `press Tab`; assert with `expect(locator).toBeFocused()`
   ([Auto-waiting assertions](https://playwright.dev/docs/actionability)). Also check that focused content
   is never fully obscured by sticky chrome — the failure WCAG's Reflow doc calls out directly
   ([Reflow, Focus Not Obscured](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html#focus-not-obscured-minimum)).
7. **Empty + error + loading** — for every surface that fetches, all four states exist and are designed.
   Empty is actionable (what's missing + the CTA that fixes it), error names the problem and the recovery,
   loading is a skeleton shaped like the real content. Screenshot the real routes, not Storybook states.
8. **No layout shift** — see below. A screen that renders correctly and *jumps* when data lands has failed.
9. **Axe-core accessibility scan** — the mechanical half of the a11y review, after the keyboard
   traversal pass found the experiential half. Run `@axe-core/playwright` against the real DOM per
   route:

   ```js
   const { AxeBuilder } = require('@axe-core/playwright');
   const results = await new AxeBuilder({ page })
     .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
     .analyze();
   console.log(results.violations.map(v => `${v.id} (${v.impact}): ${v.nodes.length} nodes`));
   ```

   (`AxeBuilder` is the documented axe-core/Playwright integration — [axe-core-npm,
   packages/playwright](https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright);
   `withTags` filters the ruleset to WCAG 2.x A/AA/2.2 AA). **Critical and serious violations are a
   failed pass**, not notes; moderate violations are recorded as advisory with the node count. Axe
   catches what eyes miss (missing labels, name/role/value breaks, contrast pairs the screenshots
   rendered too small to judge) and eyes catch what axe cannot (focus order sanity, focus-visible
   rendering). Run both; neither substitutes for the other. Not installed? One dev dependency:
   `npm i -D @axe-core/playwright`.

**Motion degrades.** A still screenshot cannot show easing. Verify transition code against
`radius-motion-tokens.md` and `toolkit-motion.md` manually, and note in the report that motion was
not visually reviewed.

## The atmosphere & dither pass (only when declared)

Runs as a tenth capture set **only** on surfaces carrying a declared atmosphere family
(`atmosphere.md`) — a static field needs no pass. Four checks:

1. **Both frames rendered.** The active frame *and* the static fallback are captured; the fallback
   must be a designed frame, not a blank fill. Capture with `animations: 'disabled'` and again with
   animations allowed — the animation-trap comparison proves the fallback is what reduced-motion and
   paused users actually get.
2. **Contrast at both extremes.** Text plated over the field is measured against the **lightest and
   darkest frame**, in both appearances. Over a static gradient, that means the two composition
   extremes of the field itself. Unrounded, per `craft-floor.md`.
3. **Banding at 100% zoom.** Screenshot at `scale: 'css'` (1:1 CSS pixels), view at 100%, and look at
   the ramp: visible banding on a gradient whose `dither.mode` is not `none` is a defect; visible
   banding with `dither.mode: none` declared is a *decision to revisit*, not a pass note.
4. **Chart clause.** If the dither scope includes chart gradients (heatmap ramps, area fills), confirm
   data marks and labels are masked out of the pass — noise over a data mark corrupts the read.

## Peer check — the critic who never saw the build

The agent that built a screen is the worst judge of it. After the stop condition holds and before
reporting done, run one **peer check** per flow (or standalone screen): a critic subagent that never
saw the build ranks the candidate's finish level against real production screens. Adapted from
`premium-mobile-design` `render-loop.md`; the evidence source differs — this skill's
`design-systems/<category>/<app>/screenshot.png` files and the user's own references.

1. **Ask how to compare.** One question to the user before dispatching: *"How do you want to compare
   this `<surface>`?"* Resolution order: screenshots the user sends → apps the user names → the
   project's `Reference inspirations` from `DESIGN.md`. Resolve named apps against
   `design-systems/`; an app with no pack gets one ask for a screenshot; unresolved apps are dropped
   and named in the report.
2. **Pick key frames.** Two to four captures that carry the surface's job — the entry, the decision,
   the payoff. One for a standalone screen.
3. **Match peer frames.** Per peer app, the `screenshot.png` showing the same surface class at the
   same density class. (Honest limitation: one frame per app, unlike mobile's multi-screen packs —
   the comparison is finish level, not flow.)
4. **Level the lineup.** Scale all images to one width, strip browser chrome, re-encode uniformly.
   Label every image A, B, C… **in a fresh random order, and keep the label map — the brief sent to
   the critic names no candidate.**
5. **Dispatch the critic** — a strong model, no conversation history, no candidate identity, no
   design rationale. Brief: *"You are a design critic. Each group below holds screens of the same
   surface, labeled A, B, C… Judge finish: how premium, clean, and production-ready each screen
   looks."* Required output per group: `RANK <A > C > B>` (ties allowed; resemblance to the
   candidate's own claims is irrelevant), then per step `STEP <X> over <Y>: <axis>: <element and what
   you see>` with axis ∈ {hierarchy, type, spacing, color and accent, depth and corners, density,
   content realism}, plus `TELLS <label>: <tells> | none` — mock tells = placeholder copy, stock
   names, round demo numbers, empty grey boxes, mixed icon weights.
6. **Act on the verdict.** Fix each gap at its cause, inside the project's tokens, through the axis
   the critic names. **A gap that needs a token, palette, or direction change goes to the user —
   `DESIGN.md` outranks the critic.** Re-run the floor passes on every changed frame, then re-dispatch
   the critic once more on the fixed lineup.
7. **Report.** Per key frame: the lineup, the candidate's final rank, the gaps named, what was fixed,
   what was handed to the user. A frame still ranked below every peer is reported as below tier with
   its deciding gaps — pushing further is the user's call.

---

## Fail a pass on a JS error, and on the animation trap

**The error gate.** Collect `console` messages of type `error` and `pageerror` events for every capture;
a pass with an uncaught error is a failed pass, not a pass with a note. Playwright exposes
`page.on('console')` / `page.on('pageerror')` and the pull-style `page.consoleMessages()` /
`page.pageErrors()`; Puppeteer exposes `page.on('console')` / `page.on('pageerror')`, where `pageerror`
fires on "an uncaught exception happens within the page". Puppeteer's `console` event is also emitted when
the page throws an error or a warning ([PageEvent](https://pptr.dev/api/puppeteer.pageevent)). In the CLI
and MCP, `console error` / `browser_console_messages { level: "error" }` do the same in one call.

**The animation trap — content hidden waiting for an animation that never ran.** This is the web failure
mode that produces a blank-looking screenshot and a wrong critique. The mechanism is verified: with
`animations: 'disabled'`, Playwright **cancels infinite animations to their initial state** and only plays
them over *after* the screenshot ([screenshot options](https://playwright.dev/docs/api/class-page#page-screenshot)).
So a component revealed by an infinite animation, a `transition` that never completes because hydration
never attached, or a JS-driven reveal will capture as invisible or invisible-by-design. The same class of
bug is what Playwright's own guide calls **poor hydration**: the static page is sent first, the dynamic part
arrives later, and — because Playwright "operates as a very fast user" — it will interact with a control
whose listeners are not attached yet, so "the button clicks will be ignored and the entered text will be
reset" ([Navigations → Hydration](https://playwright.dev/docs/navigations)).

Detect it, don't guess at it:

- If a capture shows a container whose children are missing entirely, re-shoot with
  `animations: 'allow'` (the Playwright default) and compare. Visible with animations on, blank with them
  off → the reveal depends on an animation.
- Assert the presence of real content, not just a container: `expect(page.getByRole('table')).toHaveCount(1)`.
- Read the console for the hydration error class of messages. Playwright's own diagnosis path is Chrome
  DevTools with Slow 3G throttling and a reload, watching clicks get ignored
  ([Navigations → Hydration](https://playwright.dev/docs/navigations)); the `emulate` tool in Chrome
  DevTools MCP exposes `networkConditions: "Slow 3G"` for the same purpose
  ([tool reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md)).
- Also check Playwright's **Stable** check, which defines stable as "maintained the same bounding box for
  at least two consecutive animation frames" ([Auto-waiting](https://playwright.dev/docs/actionability)) — a
  component that never settles will fail every actionability check, which is the loudest possible signal.

**Not found:** the literal string "content hidden waiting for an animation that never ran" as an error
message emitted by Playwright, Puppeteer, or Chrome. What would settle it: the Playwright or Puppeteer error
message catalogue listing it. Treat it as the *name of this failure mode*, not a string to grep for.

---

## The no-layout-shift check

Load, then interact, and measure. `layout shift score = impact fraction × distance fraction`, and CLS is the
**largest burst** of shift scores — a session window is shifts less than 1 second apart, max 5 seconds total
([web.dev, CLS](https://web.dev/articles/cls)).

In-page probe:

```js
new PerformanceObserver((list) => {
  for (const e of list.getEntries()) {
    if (!e.hadRecentInput) console.log('shift', e.value, e.sources);
  }
}).observe({ type: 'layout-shift', buffered: true });
```

([web.dev, CLS](https://web.dev/articles/cls)). Note what does *not* count: "if a new element is added to
the DOM or an existing element changes size, it doesn't count as a layout shift — as long as the change
doesn't cause other visible elements to change their start position". A growing skeleton that pushes the
page down *does* count, because the content below moves.

**Targets, measured at the 75th percentile of page loads, segmented across mobile and desktop**
([web.dev, Web Vitals](https://web.dev/articles/vitals)):

| Metric | Good | Source |
|---|---|---|
| **LCP** | ≤ **2.5 s** | [web.dev Web Vitals](https://web.dev/articles/vitals) |
| **INP** | ≤ **200 ms** | [web.dev Web Vitals](https://web.dev/articles/vitals) |
| **CLS** | ≤ **0.1** | [web.dev Web Vitals](https://web.dev/articles/vitals); [web.dev CLS](https://web.dev/articles/cls) |

The `web-vitals` library exports the same cut-points as code — `CLSThresholds` `[0.1, 0.25]`,
`INPThresholds` `[200, 500]`, `LCPThresholds` `[2500, 4000]`
([GoogleChrome/web-vitals README](https://github.com/GoogleChrome/web-vitals#rating-thresholds)). Use
`onCLS(console.log, { reportAllChanges: true })` inside the render pass to watch shifts as they happen.

**INP cannot be measured in a lab.** "Tools like Lighthouse that load pages in a simulated environment
without a user cannot measure INP, as there is no user input" ([web.dev, Web Vitals](https://web.dev/articles/vitals)).
The proxy is **Total Blocking Time (TBT)**: TBT "may be a reasonable proxy metric for INP for the lab but
it's not a substitute for INP in and of itself", and it is lab-measurable
([web.dev, TBT](https://web.dev/articles/tbt)). A good TBT is **under 200 ms on average mobile hardware**
([web.dev, TBT](https://web.dev/articles/tbt)); Lighthouse's own mobile bands are 0–200 green, 200–600
orange, over 600 red, and desktop 0–150 / 150–350 / over 350
([Chrome for Developers, TBT](https://developer.chrome.com/docs/lighthouse/performance/lighthouse-total-blocking-time)).
The main thread counts as "blocked" by any task over **50 ms**, and the blocking portion is the excess over
50 ms ([web.dev, TBT](https://web.dev/articles/tbt)).

Lab run in the loop:

```bash
npm install -g lighthouse
lighthouse http://localhost:3000 --only-categories=performance --output json --output-path ./lh.json
```

`lighthouse <url>` and `--output json --output-path <path>` are from the
[Lighthouse intro](https://developer.chrome.com/docs/lighthouse/overview); `onlyCategories` is the config
setting ([Lighthouse configuration](https://github.com/GoogleChrome/lighthouse/blob/main/docs/configuration.md)).
**State in the report that INP was not measured** — no lab can. It needs field data via CrUX or RUM
([web.dev, Web Vitals](https://web.dev/articles/vitals)).

---

## Visual regression (only if the project already has it)

Do not add a visual-regression service to satisfy this loop. Look at the pixels.

**Playwright's built-in comparison** is the zero-new-dependency option: `await expect(page).toHaveScreenshot()`
generates a reference on first run and compares on later runs, using **pixelmatch**
([Playwright, Visual comparisons](https://playwright.dev/docs/test-snapshots)). Notable mechanics, all from
that page:

- Snapshots are named per browser and platform (`landing-chromium-darwin.png`) — **rendering varies by host
  OS, browser version, hardware, power source, and headless mode**, so baselines must be generated in the
  same environment they are compared in.
- On the first run it "took a bunch of screenshots until two consecutive screenshots matched" — i.e. it
  already handles the settle problem, which is why it is worth using if a test harness exists.
- Update baselines with `npx playwright test --update-snapshots`.
- Tolerances: `maxDiffPixels` (shared via `expect.toHaveScreenshot` in config), and `stylePath` to inject a
  stylesheet that hides volatile elements (e.g. `iframe { visibility: hidden; }`).
- Non-image snapshots also work: `expect(value).toMatchSnapshot('hero.txt')`.

**BackstopJS** (MIT, `npm install -g backstopjs`) wraps Playwright or Puppeteer with an in-browser diff
report, `backstop init` / `test` / `approve`, `misMatchThreshold` (default 0.1% differing pixels),
`requireSameDimensions` (default true), `hideSelectors`, `readySelector` / `readyEvent` / `delay`, and
`--docker` for cross-platform-stable rendering — its docs explicitly note that different environments
render text differently ([BackstopJS README](https://github.com/garris/BackstopJS)). Use it when the team
already has it. **The repo currently states it "needs a new maintainer/owner"** — treat as unmaintained.

**Commercial services.** Percy requires a BrowserStack account and renders across real devices; its free
plan includes 5,000 screenshots/month with unlimited team members, and paid plans are sold through
BrowserStack rather than as a published fixed monthly price
([Chromatic's Percy comparison](https://www.chromatic.com/compare/percy) — a competitor's page, treat the
numbers as indicative, not as Percy's own pricing). **Not found:** Percy's own pricing table — the
`percy.io/pricing` page returned no readable content on 2026-10-05. What would settle it: a Percy or
BrowserStack pricing page that renders server-side. Chromatic publishes exact tiers — Free $0/month with
5,000 billed snapshots, Starter $179/month with 35,000, Pro $399/month with 85,000, Enterprise custom
([Chromatic pricing](https://www.chromatic.com/pricing)).

---

## Critique honestly

Judge each pass against three things: the **brief** (does the screen satisfy what was promised?),
`craft-floor.md` **Verify** (mechanics), and **Refuse** (would this pass the slop detector?). Name each
problem in one line, fix at the cause — token, component, or layout, never a one-off patch — and re-render.
Do not rationalize a violation because the fix is awkward.

## Stop condition

A fresh pass finds zero Verify violations and zero Refuse hits, zero console errors, and CLS within target
→ done. Report what was rendered, at which viewport and scale, which states were reviewed, which tool
produced the pixels, and any passes skipped. The user should know exactly what was and wasn't seen.

Minimum two passes. The first pass is nearly always wrong about something.

---

## When there is no browser automation at all

Say so plainly. Then run the honest approximation — never a fake one:

1. **Static markup and CSS reasoning.** Walk the DOM: does the flex child have `min-width: 0`? Does the
   grid track have a `minmax` floor? Is every async region height-reserved? Is `prefers-color-scheme` or
   `.dark` actually wired? This catches a real class of defects and is not a substitute.
2. **Run the project's own tests** — `npx impeccable detect` (see `detector-integration.md`), unit tests,
   and any snapshot tests already in the repo. Mechanical findings only.
3. **Ask the user for pixels.** One request: "start the app and screenshot `<route>` at 1440px, or tell me
   to install Playwright." Most environments can install it; the cost is one `npx playwright install`.
4. Mark the screen **"unreviewed — needs render pass."** An unreviewed screen is not a finished screen.

Never describe a screenshot you did not take. Never claim a dark-mode or narrow-viewport pass you ran only
in your head. The report is the deliverable's honesty record.

---

## Sources

- Playwright — Screenshots guide. https://playwright.dev/docs/screenshots — Microsoft — accessed 2026-10-05
- Playwright — Page API (`page.screenshot`, `browser.newContext` options, events). https://playwright.dev/docs/api/class-page — Microsoft — accessed 2026-10-05
- Playwright — Visual comparisons (`toHaveScreenshot`, pixelmatch, `maxDiffPixels`, `stylePath`, `--update-snapshots`). https://playwright.dev/docs/test-snapshots — Microsoft — accessed 2026-10-05
- Playwright — Auto-waiting (actionability, Stable/Visible definitions, assertions). https://playwright.dev/docs/actionability — Microsoft — accessed 2026-10-05
- Playwright — Navigations (hydration, "very fast user"). https://playwright.dev/docs/navigations — Microsoft — accessed 2026-10-05
- Playwright — Emulation (viewport, `isMobile`, `colorScheme`, locale, timezone, offline). https://playwright.dev/docs/emulation — Microsoft — accessed 2026-10-05
- Playwright — Browsers (install, headless shell, channels). https://playwright.dev/docs/browsers — Microsoft — accessed 2026-10-05
- Playwright — Web server (`webServer` config). https://playwright.dev/docs/test-webserver — Microsoft — accessed 2026-10-05
- Playwright MCP — Introduction (tool list, `@playwright/mcp`). https://playwright.dev/mcp/introduction — Microsoft — accessed 2026-10-05
- Playwright MCP — Screenshots (`browser_take_screenshot`). https://playwright.dev/mcp/tools/screenshots — Microsoft — accessed 2026-10-05
- Playwright MCP — Waiting (`browser_wait_for`). https://playwright.dev/mcp/tools/waiting — Microsoft — accessed 2026-10-05
- Playwright MCP — Console (`browser_console_messages`). https://playwright.dev/mcp/tools/console — Microsoft — accessed 2026-10-05
- Playwright MCP — Configuration & CLI options. https://playwright.dev/mcp/configuration/options — Microsoft — accessed 2026-10-05
- Playwright CLI — Introduction (all commands). https://playwright.dev/agent-cli/introduction — Microsoft — accessed 2026-10-05
- Playwright CLI — Installation. https://playwright.dev/agent-cli/installation — Microsoft — accessed 2026-10-05
- Playwright CLI — Screenshots & PDF. https://playwright.dev/agent-cli/commands/screenshots-pdf — Microsoft — accessed 2026-10-05
- Playwright CLI — Console & Eval. https://playwright.dev/agent-cli/commands/console-eval — Microsoft — accessed 2026-10-05
- Playwright CLI — Configuration. https://playwright.dev/agent-cli/configuration — Microsoft — accessed 2026-10-05
- Puppeteer — `Page.screenshot()`. https://pptr.dev/api/puppeteer.page.screenshot — Google — accessed 2026-10-05
- Puppeteer — `ScreenshotOptions` interface. https://pptr.dev/api/puppeteer.screenshotoptions — Google — accessed 2026-10-05
- Puppeteer — `Page.setViewport()`. https://pptr.dev/api/puppeteer.page.setviewport — Google — accessed 2026-10-05
- Puppeteer — `Viewport` interface. https://pptr.dev/api/puppeteer.viewport — Google — accessed 2026-10-05
- Puppeteer — `Page.emulateMediaFeatures()`. https://pptr.dev/api/puppeteer.page.emulatemediafeatures — Google — accessed 2026-10-05
- Puppeteer — `PageEvent` enum / page events. https://pptr.dev/api/puppeteer.pageevent — Google — accessed 2026-10-05
- Puppeteer — `PuppeteerLifeCycleEvent`. https://pptr.dev/api/puppeteer.puppeteerlifecycleevent — Google — accessed 2026-10-05
- Puppeteer — `Page.waitForNetworkIdle()`. https://pptr.dev/api/puppeteer.page.waitfornetworkidle — Google — accessed 2026-10-05
- Puppeteer — Screenshots guide. https://pptr.dev/guides/screenshots — Google — accessed 2026-10-05
- Puppeteer — Headless modes. https://pptr.dev/guides/headless-modes — Google — accessed 2026-10-05
- Chrome DevTools for agents — overview. https://developer.chrome.com/docs/devtools/agents — Google — accessed 2026-10-05
- chrome-devtools-mcp — tool reference (`take_screenshot`, `emulate`, `resize_page`, `performance_start_trace`, `lighthouse_audit`, `list_console_messages`). https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md — Google (ChromeDevTools) — accessed 2026-10-05
- chrome-devtools-mcp — README (config, `--slim`, `--headless`, Chrome-only support). https://github.com/ChromeDevTools/chrome-devtools-mcp — Google (ChromeDevTools) — accessed 2026-10-05
- Chrome Headless mode (headless without a display; unified headless since Chrome 112). https://developer.chrome.com/docs/chromium/headless — Google — accessed 2026-10-05
- Chrome Headless command-line reference (`--screenshot`, `--window-size`, `--timeout`, `--virtual-time-budget`). https://developer.chrome.com/docs/automation-and-testing/headless-cli — Google — accessed 2026-10-05
- Lighthouse — Introduction (CLI usage, `--output json`, `--output-path`). https://developer.chrome.com/docs/lighthouse/overview — Google — accessed 2026-10-05
- Lighthouse — Total Blocking Time (score bands, 50 ms long-task definition). https://developer.chrome.com/docs/lighthouse/performance/lighthouse-total-blocking-time — Google — accessed 2026-10-05
- Lighthouse — Configuration (`onlyCategories`, `onlyAudits`, `skipAudits`). https://github.com/GoogleChrome/lighthouse/blob/main/docs/configuration.md — Google — accessed 2026-10-05
- web.dev — Web Vitals (LCP/INP/CLS thresholds, 75th percentile, INP not lab-measurable, TBT as proxy). https://web.dev/articles/vitals — Google — accessed 2026-10-05
- web.dev — Cumulative Layout Shift (session window, score formula, `layout-shift` observer). https://web.dev/articles/cls — Google — accessed 2026-10-05
- web.dev — Total Blocking Time (lab proxy for INP, 200 ms target). https://web.dev/articles/tbt — Google — accessed 2026-10-05
- GoogleChrome/web-vitals — README (rating thresholds, `onCLS`/`onINP`/`onLCP`). https://github.com/GoogleChrome/web-vitals — Google — accessed 2026-10-05
- W3C — Understanding SC 1.4.10 Reflow (320 CSS px / 256 CSS px, 400% zoom equivalence, sticky-obscuring-focus failure). https://www.w3.org/WAI/WCAG22/Understanding/reflow.html — W3C — accessed 2026-10-05
- W3C — Understanding SC 1.4.4 Resize Text (200 percent). https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html — W3C — accessed 2026-10-05
- MDN — `FontFaceSet.ready` / `document.fonts.ready`. https://developer.mozilla.org/en-US/docs/Web/API/FontFaceSet/ready — Mozilla — accessed 2026-10-05
- Next.js — next CLI (`next dev`, `next build`, `next start`, `-p`). https://nextjs.org/docs/app/api-reference/cli/next — Vercel — accessed 2026-10-05
- Python — `http.server` command-line interface. https://docs.python.org/3/library/http.server.html#command-line-interface — Python Software Foundation — accessed 2026-10-05
- BackstopJS — README (MIT, `backstop init|test|approve`, `misMatchThreshold`, `requireSameDimensions`, `--docker`, maintainer notice). https://github.com/garris/BackstopJS — GitHub / open source — accessed 2026-10-05
- Chromatic — Pricing (Free $0/5,000 snapshots; Starter $179/35,000; Pro $399/85,000). https://www.chromatic.com/pricing — Chroma Software Inc. — accessed 2026-10-05
- Chromatic — Percy comparison (Percy free plan 5,000 screenshots/mo; pricing via BrowserStack). https://www.chromatic.com/compare/percy — Chroma Software Inc. (competitor-authored) — accessed 2026-10-05
