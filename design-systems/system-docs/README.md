# System docs — public design-system documentation sites

Reverse-engineered specs from seven public design-system documentation sites: Microsoft Fluent 2,
Adobe Spectrum, Uber Base, Pinterest Gestalt, Salesforce Lightning (SLDS), Vercel Geist, and
Wise. Geist and Wise live here as *system* references even though the same brands have product
posture specs in `devtools/` and `fintech/` — different questions, different answers.

These are a different species from every other category here. The app specs are *visual
direction* — load them to pick a posture and steal moves. System docs are *standards* — load
them when the work is building or repairing the system itself:

- **Token architecture** — how each system layers primitives, semantic aliases, and component
  tokens, and how it versions and deprecates them (Lightning and Spectrum are the strongest
  references for versioning discipline).
- **Component state matrices** — the full enumeration of hover / focus-visible / active /
  selected / disabled / read-only per component. This is the industry's strongest public
  material for non-negotiable #4 (states are designed, not afterthoughts).
- **Density** — Lightning and Fluent are the canonical references for the Dense class (28–32px
  rows, 12–13px body): how compact variants are tokenized rather than hard-coded.
- **Focus & a11y conventions** — Spectrum and Gestalt document focus-visible treatment and
  screen-reader behavior per component; steal the pattern of shipping it per component.

**Do not use these as posture-fit visual direction.** They are deliberately neutral — their job
is to be invisible scaffolding for other people's products. A landing page or a committed-brand
surface derived from one of these will read corporate-gray. Pick posture-fit apps from
`references/signature-moves.md` as usual; reach here only when the task names tokens, states,
density, or a11y mechanics.

| System | Path | Steal it for |
|---|---|---|
| Fluent 2 (Microsoft) | `fluent-2/` | State-layer model, type ramp, focus ring treatment |
| Spectrum (Adobe) | `spectrum/` | T-shirt size scaling, per-component a11y docs, color slots |
| Base (Uber) | `base-uber/` | Style-extension API, compact enterprise density |
| Gestalt (Pinterest) | `gestalt/` | Dark-first tokens, per-component localization sections |
| Lightning (Salesforce) | `lightning-slds/` | Enterprise density, token versioning & deprecation policy |
| Geist (Vercel) | `geist-vercel/` | Monochrome discipline, class-packaged type ramp, P3 tokens, gray-step interactions |
| Wise | `wise/` | Money-surface state transparency, two-color accent scarcity, illustration binding |

## Same-problem comparison

The reading protocol that makes seven systems worth more than seven separate specs: systems
think best in **disagreement**. When building or repairing a component, run this once —
usually inside `tokens`, `component-consistency`, or a `screen` build:

1. **Pick the problem, not the system.** Name the component you're actually building (a toast,
   a data-table row, a focus ring).
2. **Read that component across the specs** — its state list in Spectrum, its state-layer
   recipe in Fluent, its density handling in Lightning/Base, its token consumption in Geist/
   Gestalt, its transparency treatment in Wise (for money components).
3. **Name the disagreement** in one sentence: "Spectrum treats selected and focus as
   coexisting states; Fluent collapses them into overlays; Geist resolves both as gray
   steps." The disagreement is the lesson — each answer encodes a constraint the others
   don't have.
4. **Commit, then record.** Choose the answer that fits this project's density class and
   posture, and write the choice into the project's `DESIGN.md` component section so the
   next session doesn't re-derive it.

Run the comparison before the build, not during — it earns its keep by pre-answering the
state and token questions the build would otherwise improvise.

Provenance: transcribed from the public documentation sites. Geist, Fluent's motion page, and
Spectrum's color fundamentals were verified against the live docs; Wise combines live positioning
with stable public brand values. Structural rules (token layering, state names, density
mechanics) are stable and safe to trust; specific hex values were recorded at transcription time
and every spec says which ones to re-verify at the source before a build depends on them.
**Access notes (as of transcription):** Gestalt's foundations pages sit behind Okta sign-in —
its spec reflects the last public state; lightningdesignsystem.com blocks automated fetching —
verify Lightning values manually in a browser. Like every spec here, all rules are fully
expressible in text.
