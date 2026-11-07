# Design System — Turso

<!-- premium-web-design:design-system 2 -->
<!-- As-of: 2026-11-01 -->
<!-- Reference inspirations: Turso Cloud dashboard app.turso.tech (colour + shell, pixel-sampled from official screenshots), Turso marketing site turso.tech (posture/type — sibling spec premium-marketing-design/design-systems/devtools/turso/DESIGN.md supplied rung-1 raw materials) -->
<!-- Surface classes: 7 routes classified; density classes S (org overview, group databases, database detail, settings, billing), F (auth, dialogs); D reserved for query-results/log surfaces -->

## 1. Design Posture & Atmosphere

Turso is a SQLite-compatible edge database platform, and its dashboard app.turso.tech feels like the terminal it grew out of: a near-black canvas with a faint green undertone, one vivid mint accent that behaves like a power LED, and everything else in a disciplined blue-gray ink ramp. After eight hours in this surface the eyes are never assaulted — the loudest thing on screen is a 4px mint progress bar or a 2px active-tab underline — and status is always a quiet pill ("Healthy", "Enterprise") rather than a shout. The 2024 "brand new web app" relaunch traded an earlier sidebar-heavy layout for a shallow, crumb-driven shell: logo → organization switcher → group switcher → tab bar, so every route is one or two hops deep and the content owns the width.

The category default for database consoles is either a dense operator cockpit (rows of grids, toolbars of icons) or a bland SaaS admin. Turso deliberately sits between: generous Standard-density lists with 44px rows and roomy stat tiles, typographic hierarchy carried by weight and the blue-gray ramp instead of boxes and dividers, and depth expressed as surface luminance steps plus 1px hairlines — never drop shadows. Buttons are quiet dark raised fills until the single mint filled action appears; destructive actions are the only red on screen. The marketing site (dark canvas #0d1318, 72px Inter 800 mint headlines, 9999px pill buttons) sets the emotional register; the product keeps the register but speaks at a lower volume.

The single visual metaphor: **a rack of dark steel with one mint LED per unit** — each card is a unit on the rack, each mint signal (progress fill, active tab, plan badge, primary button) is its status light. If a screen needs more than a handful of lit LEDs, the design is wrong.

**Key Characteristics**
- Dark-only product. Canvas `#0d1317`, cards `#141a1e`, ghost fills `#1b242a` — a three-step luminance ramp plus hairlines, zero drop shadows in-app.
- One accent hue: mint. Bright signal `#4ff7d1` (progress bars), text-grade mint `#14e0b9` (links, CTA text), pill-grade mint `#1ed8a4` (badges), filled-control mint `#3ab59a` (primary button), dark washes `#012f24`/`#09352c`/`#11362e` (pill backgrounds).
- Red exists exactly once: the destructive confirm button (`#d93840` fill, white label; `#e5484d` glyph tone on a near-black red wash).
- Primary ink is not pure white: `#e9eff3`; secondary `#a2b7c6`; tertiary `#90a2af`; disabled `#647f93` — a blue-gray ramp, never gray-on-gray flat.
- UI typeface Inter (400/500/600/700); every identifier, currency amount and hex ID sets in IBM Plex Mono.
- Tabular numerals on every comparable value; stat values 28px/700 with `/ ∞` limit suffixes in secondary ink.
- Standard density: 44px list rows, 12px cell padding, 24px gutters; no dense tables in the shipped dashboard.
- Radius families: 10px controls, 12px stat tiles, 16px cards/dialogs, 9999px badges/avatars/progress tracks. No other values.
- Active tab = text turns primary + 2px mint underline; inactive tabs sit in secondary ink with no fill.
- Status pills pair mint text on a dark green wash — never a saturated fill; colour always ships with a word ("Healthy").
- Section cards open with a 20px/600 header row that carries its own actions (ghost buttons) on the right, separated from the body by a hairline.
- Row actions hide behind a vertical-kebab; no icon-toolbars, no inline action floods.
- Marketing-only expressiveness: 3D bull mascot, mint headline type, sage-green gradient backdrops — these never enter the product token layers.
- Empty states are text + one mint CTA; no illustration system exists inside the app.
- Focus is always visible: a 1.5px mint ring at `border.focus`, measuring 6.90:1 against raised surfaces — never an removed outline.
- Prose measure is capped at 65–80 characters; dialog leads and empty-state body never run full card width.
- Depth reads top-down: sticky chrome on `surface.canvas`, content on `surface.raised`, interactive wells sinking to `surface.inset` — light never accumulates downward.
- The four fixed hairline strengths (subtle, strong, focus, and the #212a31 progress track) are the only 1px values; ad-hoc border grays are banned.

## 2. Token Architecture   ← normative

**Three layers.** A component consumes **semantic** tokens only; a semantic token resolves to a **primitive**; nothing skips a layer.

- **L1 Primitive** — literal values named by value: `ink.1000` (darkest) … `ink.100` (lightest) for the blue-gray ramp, `mint.950` … `mint.200` for the accent ramp, `red.950/500/600`, `amber.950/400`, `blue.950/400`; `font.inter`, `font.plex-mono`; `size.100` (12px) … `size.900` (48px); `space.0` … `space.20`; `radius.sm/md/lg/full`; `dur.fast/base/slow` + easing curves (decelerate 0.2/0/0/1, accelerate 0.4/0/1/1). Referenced only by L2. Banned: component-named primitives (`--card-bg`, `--upgrade-pill`) — one value, many roles.
- **L2 Semantic** — role names: `surface.canvas`, `surface.raised`, `surface.overlay`, `surface.inset`, `surface.hover`; `border.subtle`, `border.strong`, `border.focus`; `accent.action`, `accent.onAction`, `accent.text`, `accent.wash`, `accent.onWash`, `accent.subtle`; `text.primary/secondary/tertiary/disabled`; `status.success/error/warning/info` each with `-wash`, plus `status.error.strong` and `status.onError`. The only layer a component may consume.
- **L3 Component** — only for deliberate deviation: `btn-primary.fill → accent.action`, `btn-ghost.fill → surface.overlay`, `btn-ghost.label → text.secondary`, `btn-destructive.fill → status.error.strong`, `btn-destructive.label → status.onError`, `tab.active-indicator → accent.action`, `badge.plan.fg → status.success`, `badge.plan.bg → accent.subtle`, `stat.value-font → font.inter` with tabular numerals, `mono.data → font.plex-mono`. Each points at L2, never at a raw hex, never at a sibling component.

**Rules.** Every token has a determinable type (color / dimension / fontFamily / duration); names are case-sensitive and free of `$`, `{`, `}`, `.`; circular references are errors. Turso ships dark only, so every semantic role carries exactly one value and that value is the dark value — when light mode ships (on the public roadmap), any role left valueless in light resolves to its dark value and will fail contrast there; audit before shipping. Animatable tokens (progress-fill width is *not* one — animate transform scale instead) must be registered with both `syntax` and `inherits`, and `initial-value` must be computationally independent, so percentage units are illegal in them.

**Layer order (low → high)** `reset → primitives → semantic → components → utilities`. Un-layered declarations would outrank this entire stack, so any value a consumer must override without `!important` lives in the top layer; a stray un-layered rule inside a component file is a defect.

## 3. Colour Roles

| Role | Dark (shipped) | Notes |
|---|---|---|
| `surface.canvas` | `#0d1317` | Page canvas — near-black with green undertone, never pure black |
| `surface.raised` | `#141a1e` | Cards, section containers, dialog surfaces |
| `surface.overlay` | `#1b242a` | Ghost buttons, hover fills, raised controls |
| `surface.inset` | `#0b0e10` | Inputs, selects, scroll wells — darker than the card it sits in |
| `surface.hover` | `#1b242a` | Row/list hover fill (one luminance step up) |
| `surface.selected` | `#0b0e10` + `border.focus` ring | Selected segmented option; inset fill plus 1px mint ring |
| `border.subtle` | `#25323c` | 1px decorative hairlines: card edges, row dividers, card-header rules |
| `border.strong` | `#566f85` | Structural keylines that must independently read: sticky-header rule, hovered card edge |
| `border.focus` | `#3ab59a` | Focus ring and selected-control ring, 1.5px |
| `accent.action` | `#3ab59a` | The one filled primary control per view |
| `accent.onAction` | `#0d1317` | Label on the filled control |
| `accent.text` | `#14e0b9` | Mint as text: links, CTA labels on washes |
| `accent.wash` | `#012f24` | Dark mint pill background (Upgrade) |
| `accent.onWash` | `#14e0b9` | Mint text on the wash |
| `accent.subtle` | `#11362e` | Badge wash (Enterprise, Healthy) |
| `text.primary` | `#e9eff3` | Headings, row names, values |
| `text.secondary` | `#a2b7c6` | Labels, inactive tabs, ghost-button labels, descriptions |
| `text.tertiary` | `#90a2af` | Metadata, role names ("owner"), helper text |
| `text.disabled` | `#647f93` | Inactive controls only — not gated, floor 3:1 |
| `status.success` / `-wash` | `#1ed8a4` / `#11362e` | "Healthy" pill; ships the word as its glyph |
| `status.error` / `-wash` | `#e5484d` / `#23100f` | Error text/glyph on near-black red wash |
| `status.error.strong` / `status.onError` | `#d93840` / `#ffffff` | Destructive confirm fill + label |
| `status.warning` / `-wash` | `#f5a623` / `#2b1d07` | Reserved: degraded replication warnings |
| `status.info` / `-wash` | `#6cb8ff` / `#0f2337` | Reserved: informational banners |

Dark canvas is **not** pure black: the canvas-to-card ramp spans `#0b0e10` → `#1b242a` (roughly 4–11% luminance), all with the same green-gray cast. Depth comes from surface steps and 1px strokes, never shadows.

**Contrast gate — computed with the WCAG relative-luminance formula, unrounded to two decimals; 4.499:1 fails.** Body ≥4.5:1; UI boundaries and focus ≥3:1.

| Foreground | Hex | Background | Hex | Ratio | Required | Verdict |
|---|---|---|---|---|---|---|
| `text.primary` | `#e9eff3` | `surface.canvas` | `#0d1317` | 16.13:1 | 4.5 | PASS |
| `text.secondary` | `#a2b7c6` | `surface.canvas` | `#0d1317` | 9.02:1 | 4.5 | PASS |
| `text.tertiary` | `#90a2af` | `surface.canvas` | `#0d1317` | 7.10:1 | 4.5 | PASS |
| `accent.onAction` | `#0d1317` | `accent.action` | `#3ab59a` | 7.35:1 | 4.5 | PASS |
| `accent.text` | `#14e0b9` | `surface.canvas` | `#0d1317` | 11.04:1 | 4.5 | PASS |
| `accent.onWash` | `#14e0b9` | `accent.wash` | `#012f24` | 8.65:1 | 4.5 | PASS |
| `border.strong` | `#566f85` | `surface.raised` | `#141a1e` | 3.35:1 | 3.0 | PASS |
| `border.focus` | `#3ab59a` | `surface.raised` | `#141a1e` | 6.90:1 | 3.0 | PASS |
| `status.success` | `#1ed8a4` | success wash | `#11362e` | 7.17:1 | 4.5 | PASS |
| `status.error` | `#e5484d` | error wash | `#23100f` | 4.66:1 | 4.5 | PASS |
| `status.onError` | `#ffffff` | `status.error.strong` | `#d93840` | 4.57:1 | 4.5 | PASS |
| `status.warning` | `#f5a623` | warning wash | `#2b1d07` | 8.08:1 | 4.5 | PASS |
| `status.info` | `#6cb8ff` | info wash | `#0f2337` | 7.55:1 | 4.5 | PASS |

Recorded, not gated: `text.disabled` `#647f93` on canvas = 4.45:1 and on `surface.raised` = 4.18:1 — inactive controls are exempt (WCAG SC 1.4.3 inactive-component note), house floor 3:1 satisfied. The shipped white-on-`#e5484d` destructive button measures 3.91:1 and is therefore **corrected** in this spec to `#d93840` under `status.error.strong`; do not copy the observed pair. For reference the marketing-site canvas `#0d1318` and this product's `#0d1317` differ by one step in the blue channel only; either passes identically, and this spec standardizes on the pixel-sampled product value.

## 4. Typography

**Families.** UI: **Inter**, self-hosted, preloaded, weights 400/500/600/700, fallback chain `Inter Fallback → ui-sans-serif → system-ui` (confirmed from app.turso.tech compiled styles). Numeric/code: **IBM Plex Mono**, self-hosted, weights 400/500/600, fallback `ui-monospace → SFMono-Regular → Menlo → Consolas` (loaded explicitly as the dashboard's mono voice). The marketing site additionally ships Geist Mono for code styling; the product standardizes on IBM Plex Mono. *Monospace is for identifiers, connection URLs, token hashes, database hex IDs, currency amounts and CLI output — never a costume for UI copy.*

**One ramp table per class, not one blended table.**

| Role | Size | Weight | Line height | Tracking | Numerals | Use |
|---|---|---|---|---|---|---|
| **[F] Focused — 16px base (dialogs, auth, forms)** |
| Dialog title | 24px | 600 | 1.33 | −0.4px | — | "Create Database Token" |
| Dialog body | 16px | 400 | 1.5 | −0.2px | — | Explanatory lead |
| Field label | 14px | 500 | 1.5 | −0.1px | — | "Expires", "Access" |
| Field value | 16px | 400 | 1.5 | −0.2px | — | Select/segment labels |
| Dialog meta | 12px | 400 | 1.5 | 0 | tabular | Auxiliary detail |
| **[S] Standard — 15px base (all dashboard routes)** |
| Page title | 28px | 700 | 1.2 | −0.6px | — | Group name, org name |
| Section title | 20px | 600 | 1.3 | −0.3px | — | Card headers: "Remote Replicas", "Team" |
| Body | 15px | 400 | 1.5 | −0.2px | — | Descriptions, empty-state copy |
| Row primary | 15px | 500 | 1.4 | −0.2px | — | Database names, member names |
| Row secondary | 14px | 400 | 1.4 | −0.1px | — | Roles, billing rows |
| Stat value | 28px | 700 | 1.2 | −0.6px | tabular | "6,606", "v0.24.18", "2.99 MB" |
| Stat label | 14px | 400 | 1.4 | 0 | — | "Rows Read", "Storage" |
| Tab | 15px | 500 | 1.4 | −0.2px | — | Overview / Databases / Analytics / Settings |
| Button label | 14px | 500 | 1.2 | −0.1px | — | All button variants |
| Badge | 12px | 500 | 1.2 | +0.2px | — | "Enterprise", "Healthy" |
| Meta | 12px | 400 | 1.5 | 0 | — | Timestamps, counts in kebab menus |
| **[D] Dense — 12–13px base (reserved: query results, logs, metrics grids)** |
| Grid header | 12px | 500 | 1.4 | +0.3px | — | Uppercase column labels |
| Grid cell numeric | 13px | 400 | 1.4 | 0 | mono, tabular | Counts, durations, sizes |
| Grid cell text | 13px | 400 | 1.4 | 0 | — | Identifiers, states |
| Log line | 13px | 400 | 1.5 | 0 | mono | Query/CLI output |
| Inline help | 12px | 400 | 1.5 | 0 | — | Row-level hints |

**Invariants.** Tabular numerals on every comparable value — row counts, storage sizes, invoices, version strings, hex IDs. Right-align numerics, left-align text, never centre a numeric column; currency amounts and identifiers set in IBM Plex Mono (the `$29.00` invoice row is the canonical example). Fixed stepped sizes only; no fluid interpolation. Measure ≤80 characters (65–80ch in [F/S] prose, unconstrained in [D] logs).

## 5. Spacing Scale & Density Scales   ← two axes, never one

**Spacing base: 4px grid; 8px rhythm in [S], 4px in [D].** `space.0` 0 · `1` 4px icon-to-label gap · `2` 8px control padding [D], badge padding · `3` 12px cell padding [S], list-row vertical padding · `4` 16px control padding, button padding, card internal gaps · `6` 24px card padding, page gutter, card-to-card gap [S] · `8` 32px stat-tile padding · `12` 48px section separation · `16` 64px rarely (dialog breathing room). *No 17px, no 23px. If a layout needs an off-scale value, the layout is wrong.*

**Density mode — the rescaling axis.**

| Mode | Row height | Base body | Cell pad | Gutter | Surfaces |
|---|---|---|---|---|---|
| `focused` | — | 16px | 16px | 24px | Auth, dialogs, token creation |
| `standard` | 44px (56px with descriptions) | 15px | 12px | 24px | Org overview, group databases, database detail, settings, billing |
| `dense` | 28–32px | 12–13px | 8px | 16px | Reserved: query results, logs, metrics |

- Density comes from row height, column pruning and leading — never from type too small to read. All shipped dashboard routes are Standard; the databases list runs 44px rows, settings rows 56px because each carries a description line.
- **Never switch density mid-page.** A card header, its rows and its footer share one rhythm; switching across routes is fine and should feel like a different room.
- **Chrome follows rows.** The tab bar, card headers and pagination (when it ships) match the row height of the content they govern — a 44px tab bar over 44px list rows is the observed harmony.
- Whitespace budget: Standard 40–55%, Focused 55–70%, Dense 25–40% (house heuristic — validate against `screens/dashboard.webp`: the group page sits near the top of the Standard band).
- Dialog rhythm: 24px padding all round, 16px between field groups, 8px between a label and its control, 24px above the footer action row.

## 6. Radius Scale

`none` 0 · `sm` 8px inputs, selects, icon tiles, progress tracks · `md` 10px buttons, segmented options, checkboxes · `lg` 16px cards, section containers, dialogs · `xl` 12px stat tiles (the one intentional exception, between md and lg) · `full` 9999px badges, avatars, progress fill caps. **One radius per component family**: buttons never mix 10px and 9999px inside the product (the marketing site's 9999px pill buttons are a separate, marketing-only family). Nested radii obey `radius_inner = radius_outer − padding`: a 10px button inside a 16px card with 24px padding may keep 10px (inner ≤ outer − padding is satisfied since 16 − 24 clamps to 0 → inner is unconstrained upward to `lg`); a 12px tile inside a 16px card uses ≥4px padding. The 40px list icon tiles and the 48px dialog medallion both use `md` — circular only when the shape is an avatar or a badge, never for an icon tile.

## 7. Elevation

**Strategy: surface-luminance steps + 1px keylines, zero drop shadows** — a shadow is invisible on a near-black canvas and the marketing system already banned them. Levels, low → high: **0** `surface.canvas` (no shadow, no border) · **1** card/panel: one step up to `surface.raised` + `border.subtle` hairline · **2** sticky top bar/tab bar: `surface.canvas` fill + `border.subtle` bottom rule (never a shadow when the list scrolls beneath) · **3** dialog: `surface.raised` fill + `border.subtle` + a 60% black scrim over the page; the dialog is the only overlay and it is modal. There is no level 4. The mint `border.focus` ring is not elevation — it is state.

## 8. Motion

`instant` 0ms · `fast` 120ms ease-out (exits, hover/press feedback, [D] exits) · `base` 180ms decelerate (entrances, tab switches, [D] entrances) · `slow` 240ms decelerate (dialog in/out, drawer reveals).
- Entrances decelerate, exits accelerate; symmetric ease-in-out on both directions is a defect.
- Animate `transform` and `opacity` only — progress bars fill via scaleX of the fill, never width.
- Skeletons pulse opacity 0.4→1.0 at `base` duration on a 1.2s loop; toggles flip their knob transform at `fast`; hover fills fade at `fast`; dialog scrim fades at `slow` while the panel scales 0.98→1.0 with deceleration.
- No bounce on irreversible moments: the Revoke confirm and plan changes get a plain fade, no overshoot.
- **Reduced motion is a real variant:** movement above ~150ms (dialog scale/fade, tab underline slide) collapses to a ≤150ms crossfade; scaling/panning of large objects is fully neutralised. Per-component variants are listed in §10.

## 9. Imagery & Art Direction   ← the one licensed saturation moment

- **Brand moment:** the 3D bull mascot and mint-on-navy headline lockups (og image, launch covers) plus the sage-green gradient backdrops used to frame marketing shots. This palette — gradient sage `#4a977e`, marketing navy `#10131c`, headline mint `#3ce6b0` — **never leaks into the UI token layers**; inside the app the mascot appears nowhere.
- **Iconography:** custom line icon set, 1.5px strokes on a 24px grid, geometric, matched to Inter's tone (bull mark, globe, database stack, document/schema, key, copy, chevrons, kebab, close). Filled variants only where a 1.5px stroke cannot carry 16px. Icon-only controls always carry a label or tooltip (§10).
- **Photography:** none anywhere.
- **Illustration / 3D:** marketing-only (mascot renders, launch covers). No motion-heavy illustration inside the product.
- **Third-party marks:** client-language logos (TypeScript, Rust, Go, Python, PHP) render monochrome white inside committed dark cells of the Connect card — never in their brand colours.
- **Empty / error art:** no illustration system exists in-app; an empty state is a text headline, one line of body, and the mint CTA that fixes it. An unspecified gap must not be filled with ad-hoc mascot cameos.

## 10. Surface & Component Inventory

| Component | Density | Variants | States | Keyboard | Primary microcopy |
|---|---|---|---|---|---|
| Top bar | S | org-level, group-level | default, sticky | logo→Home, switchers via Enter/arrow popover | org name + plan badge; "Upgrade", "Support" |
| Org/group switcher | S | single- vs two-segment crumb | closed, open, item-hover | Enter opens, arrows move, Esc closes | crumb trail "logo / org / group" |
| Tab bar | S | 2–4 tabs | active (primary text + 2px mint underline), inactive | arrows move, Enter select; home/end | "Overview", "Databases", "Analytics", "Settings" |
| Section card | S | with/without header description | default, loading, error | header actions reachable in tab order | header 20px/600 + ghost actions |
| Stat tile | S | value-only, value+limit, value+progress | default, loading | value announced as one label | label 14px gray; value 28px/700 tabular; "/ ∞" suffix |
| Progress bar | S | usage fraction | animating (scaleX), full | aria-valuenow on the host | track `#212a31`, fill `accent.action` |
| List row | S | database row, replica row, member row, invoice row | default, hover `surface.hover`, focused | row focusable; Enter opens; kebab via Enter | icon tile + name; kebab for actions |
| Row action menu (kebab) | S | single menu | open (focus-trap), item-hover | Enter, arrows, Esc | "Delete", "Rename", "Copy URL" |
| Ghost button | S/F | default, with icon | hover `surface.overlay`→brighter, disabled + reason | Enter/Space | "Create Database", "Add Location", "Copy URL" |
| Primary button | F | filled mint | hover brightens to mint.400, loading (label kept, width reserved), disabled + reason | Enter/Space | "Create Token", "Save" |
| Destructive button | F | dialog-final | hover darkens, loading reserved-width | Enter/Space | "Revoke" on `status.error.strong` |
| Text-on-wash button | S | pill | hover brightens text one step | Enter/Space | "Change Plan", "Upgrade" |
| Badge | S | plan, status | static | — | "Enterprise", "Healthy" — word is the glyph |
| Select | F | with chevron | closed, open, focused ring, disabled | Enter, arrows, type-ahead | "No Expiration" |
| Segmented control | F | 2 options | unselected, selected (inset fill + mint ring) | arrows, Space | "Read & Write" / "Read Only" |
| Checkbox list | F | scrollable, counter | unchecked, checked, focus ring | Space toggles, arrows move | "Read ATTACH Permissions" |
| Toggle row | S | with description | on, off, disabled + reason, loading | Space flips | "Block Writes — Block all write operations on your database." |
| Text input | F | single-line | default inset, focused ring, error (red ring + text below), disabled | standard text nav | "john@example.com" placeholder, never label |
| Dialog | F | confirm, create | open (focus-trap, scrim), closing | Esc closes; focus returns to invoker | title 24px/600; Cancel ghost + final action |
| Avatar | S | initials, image | default | — | 2-letter initials on mint wash |
| Member row | S | with role | hover, kebab | as list row | name 15px/500 + role 14px tertiary |
| Invoice row | S | with amount | hover, download action | as list row | month 15px/500 + amount in mono tertiary |
| Plan control | S | Overages toggle + Change Plan | toggle on/off/loading; change disabled + reason | Space flips toggle | plan name in badge; toggle labelled "Overages" |
| Tooltip | S/F | dark tip on hover/focus | hidden, visible, delayed 300ms | focus shows it; Esc hides | names the icon action ("Copy URL") |
| Skeleton | S/F | tile, row, table shapes | pulsing (opacity 0.4→1) | aria-busy on the region | no text; geometry matches final |
| Empty state | S/F | first-run, no-results | static | CTA reachable | headline + one body line + mint CTA |

**Every fetching surface also designs:** loading = skeleton matching final geometry (tile/row shapes pulse via opacity, never a centred spinner on a blank page); empty = what is missing + the mint CTA that creates it; error = what happened in one sentence + retry as ghost button; offline/stale = cached values shown with a "last updated" meta line and a retry affordance.

**Contracts this table encodes:** one primary filled CTA per view [F/S]; every icon-only control (kebab, close, copy) carries a tooltip; a disabled control states why on focus or hover ("Overages unavailable on the Free plan"); a button never changes width between idle and loading — the space is reserved.

## 11. Light / Dark Strategy

- **Posture: B dark-only.** The product was designed dark-first (the relaunch roadmap publicly lists light mode as future work); a single-mode system ships fewer, better-calibrated roles.
- **Mechanism:** semantic roles are authored once, in dark values. No role is absent; when light mode ships, each must gain a light value and re-pass the §3 gate — a role silently inheriting its dark value would fail contrast on white.
- **`color-scheme: dark`** is set at the root so UA chrome, form controls and scrollbars render dark; it repaints UA-provided parts of the canvas only, not the document theme.
- **The color-scheme declaration is mirrored in a document-head meta tag before the stylesheet** to prevent a flash of the wrong scheme on first paint.
- **Dark is authored, not inverted:** its own green-cast ramp, its own border strength (hairlines are lighter than the card by design — a "delicate" dark hairline is invisible), no filtered negative. Any future light theme is a new authored ramp, not an inversion.
- Org-tinting: not offered. If an enterprise theming need appears, colour tokens swap and geometry (radii, type sizes, spacing) freezes.
- Form controls: native controls are only acceptable once recoloured to the ramp — an unthemed white UA select or scrollbar inside a committed surface is a lapse; `color-scheme: dark` is the baseline, the token-mapped styling is the standard.

## 12. Density-Mode Strategy

- **Default mode per surface class:** Standard on every shipped dashboard route (the boundary: rows are primary content and never exceed a few dozen per view); Focused on dialogs and auth; Dense is specified (§4/§5) for the query-results/log class but ships nothing today.
- **Mechanism:** a density marker at the app root rescales row height, cell padding, gutter and body size **together** as a token axis — spacing tokens do not change value based on screen size, only the density axis moves them.
- **Container queries for reflow:** components reflow to their container, not the viewport, via container queries on the content box; where no eligible container exists, size queries fail closed to small-viewport units, so container units are never used where that fallback would be wrong (e.g., no `cq*` units on the stat-tile grid's limit suffix).
- **Style queries** comparing a density marker compare computed values, so the marker must be a registered custom property.
- **The switch is an accessibility affordance,** not a preference: a Dense toggle is offered per data surface for users with visual field loss, per W3C's note on target-size/spacing guidance endorsing density-control mechanisms.
- Dense chrome: grid headers stay 32px (matching the upper dense row height), and a sticky dense header keeps `border.subtle` as its scroll keyline so column alignment survives vertical scroll.

## 13. Accessibility Commitments

- **Target:** WCAG 2.2 AA minimum; AAA on the §3 headline pairings (16.13:1 primary ink; body pairs all ≥4.5:1).
- **Target size:** ≥24×24 CSS px hard minimum for every control (kebab, close, checkbox), with 44×44 the design target for primary controls in [F/S]; the spacing exception (24px circle non-intersection) is honoured in the dense list rows; zoom does not excuse it.
- **Keyboard:** every function operable without a pointer; switchers, tab bar, kebab menus and dialogs follow the §10 keyboard columns; the focused item is never entirely hidden behind the sticky top bar (scroll-margin on anchor targets).
- **Focus indicator:** `border.focus` mint ring at 1.5px, always visible, never removed without an equally strong replacement; ring contrast on `surface.raised` = 6.90:1 (≥3:1 required).
- **Contrast:** the full §3 gate; colour independence — every status pairs colour with a word ("Healthy") or a glyph; usage deltas would carry a sign, not just a colour.
- **Motion:** the §8 reduced-motion variant per component (dialog, tab underline, progress fill, skeletons).
- **Text:** ≤80-character measure, 1.5 leading on body, 200% resize without horizontal scroll.
- **Semantics:** real button/link/input elements; tab bar exposes tab semantics with selected state; dialogs trap focus and return it; loading regions announce busy state; usage counters announce as one label ("2 of unlimited locations").
- **Contrast preference:** `prefers-contrast: more` raises `border.subtle` to `border.strong` and `text.tertiary` to `text.secondary` (recognised values: `no-preference`, `more`, `less`, `custom`).

## 14. Anti-Patterns

**Do**
1. Keep the canvas at `#0d1317` with green undertone — the cast is the brand; a neutral `#0a0a0a` reads as someone else's product.
2. Express depth with the 3-step luminance ramp + hairlines; the darkest inset wells (`#0b0e10`) sit *inside* cards, the lightest fills (`#1b242a`) sit *on* them.
3. Reserve the mint filled control for the one action that creates or confirms — one per view.
4. Pair every mint wash with mint text at the computed gate values (`#14e0b9` on `#012f24` = 8.65:1).
5. Set every identifier, URL, hex ID and currency amount in IBM Plex Mono with tabular figures.
6. Give card headers their own action row (ghost buttons right-aligned) and separate it from the body with `border.subtle`.
7. Use 44px rows in lists, 56px when the row carries a description — chrome heights follow.
8. Correct the destructive fill to `#d93840`; the observed `#e5484d`-with-white-label pair fails AA at 3.91:1.
9. Render third-party client logos monochrome inside the Connect card's committed cells.
10. Write empty states as headline + one sentence + the mint CTA that fixes the emptiness.
11. Keep inactive tabs in `text.secondary` with zero fill; the mint underline is the only active signal.
12. Show skeletons that match final geometry — tile for tile, row for row.

**Don't**
1. No drop shadows or glow elevation anywhere in the product — surface steps only (marketing ban, honoured in-app).
2. No magenta/plum accents in-app: `#d946ef`/`#a21caf` belong to the marketing beta framing and stay there; the product's chromatic budget is mint + one red.
3. No pure `#000000` canvas or `#ffffff` text — the authored ramp is `#0d1317`/`#e9eff3`.
4. No second filled-chromatic control beside the primary; a view with "Upgrade" *and* "Create Token" filled is a defect.
5. No status communicated by colour alone — "Healthy" is a word, red is a labelled confirm button.
6. No hover-only affordances: the kebab menu, row actions and copy buttons all work from keyboard and are visible on focus.
7. No placeholder-as-label — the input in the billing settings shows a placeholder and a persistent visible label.
8. No whole-page spinners; skeletons match final geometry or the surface doesn't ship.
9. No `alert()`/`confirm()` — destructive intent gets the authored dialog with an explicit, action-named button ("Revoke", not "OK").
10. No tiny type as a density strategy — 12px is the floor and only in [D]/meta roles; a 13px tabular numeral belongs in a dense table, not a focused form.
11. No mascot, gradient backdrop or marketing headline style inside app chrome — the brand moment never leaks into tokens (§9).
12. No radius zoo: 10px buttons never meet 12px buttons; stat tiles are the single intentional 12px family.
13. No disabled primary sitting silently dead — it states the blocker ("Overages unavailable on the Free plan").
14. No mid-page density switches — a card's header, rows and footer share one rhythm.

## 15. Quick Reference & Verification Gate

**Colour (dark-only, role → hex)**
`surface.canvas` #0d1317 · `surface.raised` #141a1e · `surface.overlay`/`surface.hover` #1b242a · `surface.inset` #0b0e10 · `border.subtle` #25323c · `border.strong` #566f85 · `border.focus` #3ab59a · `accent.action` #3ab59a · `accent.onAction` #0d1317 · `accent.text`/`accent.onWash` #14e0b9 · `accent.wash` #012f24 · `accent.subtle` #11362e · `text.primary` #e9eff3 · `text.secondary` #a2b7c6 · `text.tertiary` #90a2af · `text.disabled` #647f93 · `status.success` #1ed8a4 / wash #11362e · `status.error` #e5484d / wash #23100f · `status.error.strong` #d93840 / `status.onError` #ffffff · `status.warning` #f5a623 / wash #2b1d07 · `status.info` #6cb8ff / wash #0f2337

**Type ramp** — Inter 400/500/600/700; IBM Plex Mono 400/500/600.
[F] 24/600 title · 16/400 body · 14/500 label · 12/400 meta.
[S] 28/700 page · 20/600 section · 15/400 body · 15/500 row · 14/400 secondary · 28/700 stat (tabular) · 14/400 stat label · 15/500 tab · 14/500 button · 12/500 badge · 12/400 meta.
[D] 12/500 header (+0.3px) · 13 mono numeric · 13 text · 13 mono log · 12 help.

**Spacing + radius** — 4px grid: 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64. Rows 44/56px [S], 28–32px [D]. Gutter 24px [S], 16px [D]. Radii: 8 inputs/tiles-inset · 10 buttons/segments · 12 stat tiles · 16 cards/dialogs · 9999 badges/avatars/tracks.

**Component → token map**
Top bar: `surface.canvas` + `border.subtle`; Tab bar: `text.secondary`/`text.primary` + `accent.action` underline; Card: `surface.raised` + `border.subtle`, header rule `border.subtle`; Stat tile: `surface.raised`, label `text.secondary`, value `text.primary`, bar track #212a31, fill `accent.action`; List row: name `text.primary`, secondary `text.secondary`/`text.tertiary`, hover `surface.hover`; Ghost button: `surface.overlay` fill + `text.secondary` label; Primary button: `accent.action` + `accent.onAction`; Destructive: `status.error.strong` + `status.onError`; Text-on-wash button: `accent.wash` + `accent.onWash`; Badge: `accent.subtle` + `status.success`; Select/Input: `surface.inset` + `border.subtle`, focus `border.focus`; Segmented selected: `surface.selected` + `border.focus`; Dialog: `surface.raised` + `border.subtle` + 60% black scrim; Progress: track #212a31, fill `accent.action`; Mono data: `font.plex-mono`, tint `text.secondary`/`text.tertiary`.

**Agent prompt block (verbatim-consumable).** Turso dashboard spec: dark-only. Canvas #0d1317; cards #141a1e; wells #0b0e10; ghost fills #1b242a; hairlines #25323c; keylines #566f85; ink #e9eff3 → #a2b7c6 → #90a2af; mint accent: filled #3ab59a (label #0d1317), text/links #14e0b9, washes #012f24/#11362e, bright signal #4ff7d1; destructive #d93840 + white; success #1ed8a4 on #11362e. Inter for UI (400–700), IBM Plex Mono for IDs/URLs/currency, tabular numerals everywhere numeric. Type: page 28/700, section 20/600, body 15/400, rows 15/500, stat 28/700, button 14/500, badge 12/500. Spacing 4px grid; rows 44px (56 with description), gutter and card padding 24px, cell padding 12px, control padding 8/16px. Radii: 8/10/12/16/9999 only. Motion 120/180/240ms; transform+opacity only; reduced-motion = ≤150ms crossfade. Focus ring #3ab59a 1.5px. One filled mint control per view; destructive red appears once, behind a confirm dialog; every status is colour + word; icons 1.5px line, 24px grid; third-party logos monochrome.

**Example component prompts**
1. *Group databases page* — `surface.canvas` background; top bar on `surface.canvas` with `border.subtle` bottom rule; crumb "bull mark / org [badge: `accent.subtle` bg, `status.success` label] / group"; tab bar with active tab in `text.primary` plus 2px `accent.action` underline, inactive tabs `text.secondary`. Header block: 48px icon tile (`surface.overlay`, radius 10) + "Group" label in `text.secondary` 14px + group name 28px/700 `text.primary`; right-aligned ghost buttons ("Create Database", "Create Group Token") — `surface.overlay` fill, `text.secondary` label, radius 10, 8×16px padding. Four stat tiles: `surface.raised`, `border.subtle`, radius 12, 24px padding; label 14px `text.secondary`; value 28px/700 `text.primary` tabular; status tile shows a badge (`status.success` on `accent.subtle`, radius 9999). Section cards below: header row (20px/600 `text.primary` + ghost action right) separated by `border.subtle`; rows 44px, icon tile 40px `surface.overlay` radius 10, name 15px/500, kebab 24px target with tooltip; row hover `surface.hover`. No shadows above level 0.
2. *Data row* — Standard 44px height; label left in 15px/500 `text.primary`; every numeric cell in IBM Plex Mono with tabular figures, right-aligned; hover fill `surface.hover`; focus ring `border.focus` 1.5px; kebab menu opens a focus-trapped list (Enter, arrows, Esc); header, toolbar and pagination (when present) heights equal to 44px.
3. *Create-database-token dialog* — scrim 60% black; dialog `surface.raised`, `border.subtle`, radius 16, 24px padding, title 24px/600 `text.primary`, lead 16px/400 `text.secondary`; labels 14px/500; select on `surface.inset` radius 8 with `border.subtle`, focus ring `border.focus`; segmented control with selected option on `surface.selected` + `border.focus` ring; checkbox list on `surface.inset` radius 8, 12px labels, IDs in mono; footer right-aligned: Cancel ghost + Create Token filled (`accent.action`/`accent.onAction`, width reserved for loading). Esc closes; focus returns to invoker; reduced-motion collapses entry to a 150ms crossfade.

**Pre-ship checklist.**
1. Zero raw hex outside L1. 2. No token resolves to a component name. 3. Every §3 contrast pairing computed, passing, unrounded. 4. Every semantic role has a value in the shipped (dark) mode — and a light value before light mode ships. 5. Every fetching surface has loading/empty/error/offline specified. 6. Every component row lists disabled and loading states. 7. Row, header, toolbar and pagination heights agree. 8. Reduced-motion variant written for every authored motion. 9. Every control keyboard-reachable with a visible `border.focus` indicator. 10. Dark authored, not filtered, with border strength exceeding any future light theme's. 11. No unoverridden stock-library default inside a committed surface. 12. Nothing came from a marketing page — mascot, gradients and magenta stay out of the token layers. 13. The §9 brand-moment palette appears nowhere in L1–L3.
