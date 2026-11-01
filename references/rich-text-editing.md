# Rich text editing

Framing: a product surface with a text editor is not a document tool. The user is editing one record,
and what the editor does to their hands, clipboard, and trust matters more than rendering fidelity.
Three decisions come first: engine, formatting set, and what happens to pasted content.

## Engine: `contenteditable` vs a framework editor

| | Raw `contenteditable` | Framework editor |
|---|---|---|
| You own | Selection reconciliation, IME, undo stack, schema, paste handling | All of the above |
| `beforeinput` reliability | You handle what it misses yourself | Handled |
| Choose it when | Plain text, or single-style notes | Block types, comments, collaboration |

If you go raw, the platform constrains you. `contenteditable` is an **enumerated** attribute with three
values — `true`/empty string, `false`, and `plaintext-only` — not a boolean; if missing or invalid, the
value is **inherited from the parent**, so an unclosed editable ancestor silently makes everything below
editable (MDN). "If content is pasted into an element with `contenteditable="true"`, all formatting is
retained. If content is pasted into an element with `contenteditable="plaintext-only"`, all formatting
is removed" — so `plaintext-only` is the cheapest correct paste policy. Nested editables are **not** in
the tab sequence by default; MDN's remedy is an explicit `tabindex="0"` on the nested editable.

`beforeinput` fires on `contenteditable` and `designMode` elements, and its target is the **editing
host** — "the nearest ancestor element whose parent isn't editable" (MDN). But "not every user
modification results in `beforeinput` firing… by autocomplete, by accepting a correction from a spell
checker, by password manager autofill, by IME," and "the event may fire but be non-cancelable."
Overriding edit behaviour everywhere requires handling `input` too and reverting what `beforeinput`
missed.

`document.execCommand()` is deprecated and non-standard: "not implemented consistently or fully by user
agents, and it is not expected that this will change in the foreseeable future" (MDN). Its one
legitimate reason to survive: "unlike direct DOM manipulation, modifications performed by
`execCommand()` **preserve the undo buffer**" — exactly what a raw editable field needs. Guard with
`document.queryCommandSupported()`.

## Toolbar: one pattern, two halves

APG's Toolbar Pattern: make the toolbar **one tab stop** with arrows moving among controls ("In
horizontal toolbars, Left Arrow and Right Arrow navigate among controls"), via roving tabindex, and
**"Use `toolbar` as a grouping element only if the group contains 3 or more controls."** Label with
`aria-labelledby` from the visible label, else `aria-label`.

The split most editors get wrong is **inline formatting** (bold, italic, code, link, comment), which is a
toolbar with one tab stop and arrows within, versus **block type** (paragraph, H1–H3, lists, quote, code
block), which should be a **menu button opening a listbox**, not a row of toolbar buttons. APG writes the
editor case out: "In applications where quick access to a toolbar is important, such as accessing an
editor's toolbar from its text area, **a documented shortcut key** for moving focus from the relevant
context to its corresponding toolbar is recommended."

## The formatting set a product UI needs

- **Inline:** bold, italic, inline code, link.
- **Block:** paragraph, heading (cap at H3 — the record title is the H1), bulleted and numbered list,
  blockquote, code block.
- **Structural, as dialogs or side panels, never toolbar buttons:** attachment, mention, table,
  comment.
- Cut entirely: `fontName`, `foreColor`, `backColor`, `fontSize`, `justify*`. All exist in
  `execCommand()`'s command list — the platform exposing them is not a reason to expose them.

## Link insertion and unfurling safety

Insert through a dialog, not an inline prompt: the user must see and edit the URL, choose display text,
and cancel. `execCommand("createLink")` "creates a hyperlink from the selection, **but only if there is
a selection**" (MDN) — it is a formatting command, not a link workflow. Validate the scheme before it
reaches an `href`: allow `http:`, `https:`, `mailto:`, internal relative paths; reject everything else.
External links carry `rel="noopener noreferrer"`: MDN defines `noopener` as creating "a top-level
browsing context that is not an auxiliary browsing context" for a hyperlink with an appropriate
`target`, and `noreferrer` as "No `Referer` header will be included. Additionally, has the same effect as
`noopener`" — so with a `target` present, `rel="noreferrer"` implies both.

**Unfurling is a server-side fetch of an attacker-supplied URL.** OWASP's SSRF page is the threat model:
"The attacker modifies the calls to this functionality by supplying a completely different URL," and
by choosing targets an attacker "may be able to read data from services that are not directly exposed on
the internet" — cloud metadata endpoints, internal REST interfaces, database HTTP interfaces, `file://`
URIs. Requirements: resolve DNS and reject private/loopback/link-local ranges **after** resolution,
allowlist schemes, cap response size and redirect count, fetch with no ambient credentials, and render
text and metadata only — never fetched HTML. The preview card is inert: host, path, favicon.

## Paste sanitisation

Three layers, in order. **1.** Prefer `plaintext-only` when the field does not need formatting. **2.**
Intercept `paste` and read `event.clipboardData` (`ClipboardEvent` — "events providing information
related to modification of the clipboard, that is cut, copy, and paste events," MDN). Async clipboard
reads need a **secure context**, and browsers diverge: Chromium requests the `clipboard-read` permission;
Firefox and Safari instead show an ephemeral menu with a single "Paste" option enabled after 1 second, and
neither supports those permissions. So read from `clipboardData` during the event rather than
`navigator.clipboard.read()`. **3.** Sanitise on every render. `new Sanitizer()` defaults to an **allow**
configuration that "omits XSS-unsafe elements and attributes, along with other elements and attributes
that can potentially be used in other attacks, such as clickjacking and spoofing" (MDN) — but Sanitizer
is **"Limited availability… not Baseline because it does not work in some of the most widely-used
browsers"**, so it is defence in depth, never the only defence. Restrict to the format set
(`new Sanitizer({ elements: ["p","a","strong","em","code","ul","ol","li","blockquote","h1","h2","h3"] })`
plus `allowAttribute("href")`) and feed it to `Element.setHTML()`, which MDN positions as "a drop in
replacement for `Element.innerHTML`". The `*Unsafe` variants should be used only with Trusted Types.
Sanitise again on save: client sanitisation defends the client; it is not a data boundary.

## Comments and suggestions

A comment is not an inline format. It is an anchored range plus a thread — `{anchor, threadId,
authorId, body, resolvedAt}`, never a node in the document tree. Suggestion mode is a **diff over the
same document model** with per-suggestion accept/reject and the original text preserved until resolved;
do not implement it as undo. Announce new comments without stealing focus: `role="status"` has implicit
`aria-live="polite"` and implicit `aria-atomic="true"`, and authors "SHOULD ensure an element with
`role="status"` does not receive focus as a result of change in status" (WAI-ARIA 1.3) — the mechanism
satisfying WCAG 2.2 SC 4.1.3 Status Messages (Level AA).

**Not found:** no primary source consulted specifies comment anchor granularity, suggestion-merge
behaviour, a same-range conflict policy, or thread nesting limits. Settle them in `DESIGN.md` as
product decisions; do not present them as standards.

## Keyboard shortcuts

Undo is `Control`+`Z` and redo `Control`+`Shift`+`Z`, or the `Command` variants on macOS — a platform
convention APG records as one authors assign (Developing a Keyboard Interface). Bold `Control`+`B` and
italic `Control`+`I` are de-facto conventions: **Not found** in any primary source consulted, so treat
them as house rules. `Control`+`K` for insert link is **Not found** on the same basis.

Every author-assigned shortcut must be discoverable in-product (APG: "Assigning and revealing keyboard
shortcuts, including guidance on how to avoid problematic conflicts with keyboard commands of assistive
technologies, browsers, and operating systems"). Record them in a `?` overlay.

## Saving and conflict states

| State | Surface |
|---|---|
| Idle / saved | Nothing, or a persistent "Saved" with timestamp |
| Unsaved | `role="status"`, polite, non-focus-stealing |
| Saving | Same region, text swapped — not a second live region |
| Save failed | Inline message in the editor footer with Retry; **never** auto-dismiss |
| Conflict | Dialog naming both versions: keep mine / take theirs / view diff |

Two constraints make this correct rather than decorative: **one live region for the whole save
lifecycle** (a fresh `role="status"` element per change defeats the announcement), and **never lose the
draft** — persist locally on failure and never clear a dirty buffer on a rejected write.

**Not found:** no primary source specifies an autosave debounce, a conflict-detection window, or a
reconnect policy for a failed write. Decide once, in `DESIGN.md`, for every editor in the product.

## Sources

- [`contenteditable` HTML global attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/contenteditable) — MDN, accessed 2026-10-05
- [`Element: beforeinput event`](https://developer.mozilla.org/en-US/docs/Web/API/Element/beforeinput_event) — MDN, accessed 2026-10-05
- [`Document.execCommand()` method](https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand) — MDN, accessed 2026-10-05
- [Clipboard API](https://developer.mozilla.org/en-US/docs/Web/API/Clipboard_API) — MDN, accessed 2026-10-05
- [`Sanitizer()` constructor](https://developer.mozilla.org/en-US/docs/Web/API/Sanitizer/Sanitizer) — MDN, accessed 2026-10-05
- [Using the HTML Sanitizer API](https://developer.mozilla.org/en-US/docs/Web/API/HTML_Sanitizer_API/Using_the_HTML_Sanitizer_API) — MDN, accessed 2026-10-05
- [`rel` HTML attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel) — MDN, accessed 2026-10-05
- [Toolbar Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/toolbar/) — W3C WAI-ARIA Authoring Practices Guide, accessed 2026-10-05
- [Developing a Keyboard Interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/) — W3C WAI ARIA APG, accessed 2026-10-05
- [WAI-ARIA 1.3 — `status` role](https://www.w3.org/TR/wai-aria-1.3/#status) — W3C Working Draft, accessed 2026-10-05
- [Server Side Request Forgery](https://owasp.org/www-community/attacks/Server_Side_Request_Forgery) — OWASP, accessed 2026-10-05