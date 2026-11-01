# AI chat and assistant UI

Framing: an assistant inside a B2B product is not a chat app. The user arrived to do a task in a record;
the assistant is a means to that end. Two consequences: the transcript is **secondary content that must
never displace the work surface**, and every model action must be **inspectable** because the user remains
accountable for what it did to their data.

## The state list, idle to error

Design all twelve. Missing states are where these surfaces fail.

| State | Surface | Semantics |
|---|---|---|
| Idle, empty | Prompt suggestions as clickable chips; never an empty void | — |
| Idle, has history | Composer ready | — |
| Composing | Auto-growing composer, `Enter` to send, `Shift`+`Enter` newline | — |
| Submitting | Send becomes Stop, same position | `role="status"` on the status line |
| Streaming | Text appends; **input stays enabled** | `role="status"`, polite |
| Tool running | Named step row: what is running, on what object | `role="status"` |
| Stopped by user | Partial answer kept, labelled partial, Regenerate offered | — |
| Complete | Normal message | — |
| Complete, cited | Source list attached to the message | — |
| Error, retryable | Inline in the transcript, Retry as a primary action | `role="status"`, not a toast |
| Error, not retryable | Explains the cause and next step; prompt stays visible | — |
| Rate limited | States the limit and when it resets | — |

Two rules carry most of the weight. **Streaming must never block**: the composer stays focusable and
typable throughout, send becomes stop, the page scrolls independently. And **never announce tokens** — a
live region updating per chunk is unusable; announce the *completion*, not the progress. `role="status"`
has implicit `aria-live="polite"` and implicit `aria-atomic="true"`, and authors "SHOULD ensure an
element with `role="status"` does not receive focus as a result of change in status" (WAI-ARIA 1.3) — so
render the message, then update a single persistent status element's text.

## The message/thread model

Three layers, because they have different lifetimes. **1.** A **thread** is a named conversation, own
route, **editable title** (the model's default is often wrong), archive and delete. **2.** A **turn** is
one user message + one assistant message + zero or more tool steps — the retry unit: Retry re-sends the
same user message, Regenerate re-runs the assistant response for the same input. **3.** A **block** is a
piece of content inside an assistant message: prose, code block, table, citation list, tool-call step,
artifact preview.

Anthropic's streaming API is the wire reference for this shape: each message is "a series of content
blocks, each of which has a `content_block_start`, one or more `content_block_delta` events, and a
`content_block_stop` event. **Each content block has an index that corresponds to its index in the final
Message content array**" (Anthropic, Streaming messages). A `tool_use` block and a `text` block are
siblings in that array — which is exactly why the UI needs a block model, not a string per message.
Threads must survive reload, and an in-flight turn must be resumable or explicitly abandoned on reconnect.

## Input affordances

Auto-growing composer with a hard max height, and send disabled on empty input. `Enter` sends and
`Shift`+`Enter` inserts a newline — state it in a visible hint, not a tooltip. **Keep the draft**: switching
threads or navigating away must not lose the typed prompt. Attachments are removable chips above the
composer with type and size shown before send. Suggested prompts sit below an empty composer as chips —
shortcuts, not required reading. The composer is the single tab stop out of the transcript on every
navigation pass.

## Stop, retry, regenerate

| Control | Where | Behaviour |
|---|---|---|
| Stop | Replaces Send, top-right of composer | Aborts the request; partial text stays, labelled partial |
| Retry | On the failed turn, inline | Re-sends the identical request; no duplicate user message |
| Regenerate | On the completed message | Alternate response for the same input; the previous one is retained and switchable |
| Edit and resend | On the user message | Rewrites history forward, warning if later turns are discarded |

A stopped response is **not** an error state: no error styling, no retry banner — a partial answer with
a Regenerate pair. At the wire level a client must be able to end a turn at any block boundary: the
vocabulary runs `message_start`, the content-block triples, "one or more `message_delta` events,
indicating top-level changes to the final Message object," and "a final `message_stop` event" (Anthropic).

## Citations and source attribution

- **Attach citations to the specific claim**, as an inline numbered marker, not to a message footer.
- **Every source is openable and attributed**: title, host, and the specific fragment or page used. A
  source the user cannot open is a claim without provenance.
- **Say when there are no sources.** A retrieved-nothing answer must state that it answered from general
  knowledge rather than from your data.
- **Never render fetched content as trusted markup.** Retrieved passages are untrusted input; sanitise
  before display (see `rich-text-editing.md` for the Sanitizer API). Prompt injection inside a retrieved
  document is the failure mode, not a styling detail.
- Distinguish **model-generated text** from **quoted source text** visually and semantically.

Carbon's AI label is a working precedent for the transparency half: "The AI label identifies AI in the
UI, enabling transparency through visual recognition of the AI icon and triggering the **explainability
popover**," with anatomy "AI indicator / button… Text label… Explainability popover." Carbon is also firm
on separation of duties: "**Don't use the AI label as a trigger for AI actions**… That type of AI actions
will have their own UI icons" — so "regenerate" gets a regenerate icon.

## Tool and agent action transparency

One row per tool call, **named for a human** — "Read 3 rows from `invoices`", not "calling `query_db`".
Show the **actual arguments**, collapsible, visible without devtools. Distinguish **read from write**
visually, and give writes a confirm step. When the agent needs approval it **blocks on the user** with
explicit Approve / Reject, never a timeout. Render partial tool input as "preparing…" — never stream raw
JSON. On completion, summarise **what changed** in product terms with links to the objects. On failure,
name which step failed and whether prior steps were rolled back.

The wire model supports this precisely. Anthropic streams tool input as **partial JSON strings** — "The
deltas for `tool_use` content blocks correspond to updates for the `input` field of the block… the deltas
are partial JSON strings, whereas the final `tool_use.input` is always an object" — parsed once
`content_block_stop` arrives. Anthropic also warns that "when using tools, **there may be delays between
streaming events while the model is working**." A UI with no idle-feedback state for tool calls will look
frozen there; that is a design requirement, not an edge case.

## Context window and token-limit disclosure

Be honest at the boundary rather than letting the user hit it. **Show usage when it is actionable** — a
meter or "conversation is getting long" affordance *before* the limit, not an error after it. **Say what
counts**: Anthropic is explicit that "**Everything in the request counts toward the context window**: the
system prompt, every message in `messages` (including tool results, images, and documents), and your tool
definitions. The output Claude generates for the turn, including its extended thinking, counts too." A UI
showing "12k / 200k" while omitting attached files and tool definitions is lying.

**Attribute numbers to the vendor.** Anthropic documents a **1M-token** context window for Claude Fable 5.1,
Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5.5/5/4.8/4.7/4.6, Claude Sonnet 5.5/5, and
Claude Mythos Preview, and **200k** for other models including Claude Sonnet 4.5; a single request to a
1M-window model can generate up to **128k output tokens** (`max_tokens`). **Report what the API reports**:
"Every response reports what the request consumed in its `usage` field," and "The token counts shown in the
`usage` field of the `message_delta` event are **cumulative**." Surface the API's number; never estimate
client-side.

**Size limits are separate from token limits**: "A single request can include up to **600 images or PDF
pages** (100 for models with a 200k-token context window)… you might reach request size limits before the
token limit." The upload UI must enforce both. And **growth degrades quality — say so, and offer the
remedy**: "As token count grows, accuracy and recall degrade, a phenomenon known as **context rot**."
Anthropic's prescribed strategy is "server-side compaction"; the product-side equivalents are summarise,
start a new thread, and pin durable context.

## Error and degradation states

| Condition | Behaviour |
|---|---|
| Stream error mid-answer | Keep the partial text, mark it partial, offer Retry |
| Error event on the stream | Anthropic: "The API may occasionally send errors in the event stream. For example, during periods of high usage, you may receive an `overloaded_error`, which would normally correspond to an HTTP 529 in a non-streaming context" — surface as retryable |
| Unknown event type | Handle gracefully. Anthropic: "new event types may be added, and your code should handle unknown event types gracefully" |
| Tool failure | Name the step; say whether prior work stands |
| Guardrail refusal | A policy outcome, not a crash; keep the prompt |
| Offline mid-stream | Distinct from an error; keep the turn recoverable |

Errors go **inline in the transcript**, adjacent to the failed turn, with that turn's controls still
reachable. A toast cannot host a retry someone may need in thirty seconds, and `toasts-notifications.md`
routes errors to persistent surfaces.

**Not found:** no primary source consulted specifies a required first-token latency budget, a
streaming chunk-size minimum, or a maximum transcript length before compaction. Settle those in
`DESIGN.md`.

## Sources

- [Streaming messages](https://platform.claude.com/docs/en/build-with-claude/streaming) — Anthropic Claude Platform Docs, accessed 2026-10-05
- [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) — Anthropic Claude Platform Docs, accessed 2026-10-05
- [AI label](https://carbondesignsystem.com/components/ai-label/usage/) — Carbon Design System (IBM), accessed 2026-10-05
- [WAI-ARIA 1.3 — `status` role](https://www.w3.org/TR/wai-aria-1.3/#status) — W3C Working Draft, accessed 2026-10-05
- [Understanding SC 4.1.3 Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html) — W3C WCAG 2.2, accessed 2026-10-05
- [Using the HTML Sanitizer API](https://developer.mozilla.org/en-US/docs/Web/API/HTML_Sanitizer_API/Using_the_HTML_Sanitizer_API) — MDN, accessed 2026-10-05