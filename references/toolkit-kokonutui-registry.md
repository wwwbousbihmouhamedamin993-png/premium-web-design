# Toolkit — Kokonut UI (kokonutui.com)

Load for mechanical scaffolding under time pressure. **Read `toolkit-selection.md` first** — this
library's default components include patterns `craft-floor.md` refuses.

## What it is

Kokonut UI is 100+ free and open-source components built with React, Tailwind CSS, Motion and
shadcn/ui. It ships a **machine-readable shadcn registry** under the `@kokonutui` namespace, an
`llms.txt`, and its own MCP server. 2k+ GitHub stars, a Vercel OSS 2025 program participant, with a
separate paid Pro tier of templates and components.

Its own positioning — "Components humans browse. Agents ship." — is the useful idea: a human gets a
live preview and copy-paste source; an agent gets a registry it can install from.

## The install protocol — the part worth adopting regardless of library

```bash
# register the MCP server so your agent can read the registry
npx shadcn@latest mcp init --client claude

# add a component
npx shadcn@latest add @kokonutui/<name>
```

Two properties make this better than any other sourcing route available in this skill:

1. **You get source, not a picture.** The component lands in your repo and you own it — no black box,
   no vendor runtime, freely editable. That is the same rule `component-consistency.md` sets.
2. **The registry is machine-readable**, so an agent can discover and install without a human
   copying from a gallery page. This is strictly better than browsing a screenshot gallery.

Kokonut's docs give the three steps as Browse → Install → Customize, with the explicit promise
"Tailwind + React — own your code, no black boxes."

Named components include `particle-button`, `liquid-glass-card`, `shimmer-text`, and `ai-prompt`.

## ⚠️ Those names are the problem

Read them again: **`liquid-glass-card`**, **`shimmer-text`**, **`particle-button`**.

`craft-floor.md` refuses, inside product surfaces:

- **Marketing aesthetics inside the product** — glassmorphism across content cards, gradient text.
- **Bouncy physics on routine interactions** — a particle button is a Persuade-mode move.

These are legitimate *marketing* components and they are legitimate *product* components in the
right surface. The failure mode is installing them as a default and inheriting their aesthetics into
an Operate or Dense screen. So:

**Adopt the mechanics, refuse the decoration.** Kokonut is a fine source for a combobox, a date
picker, a data table, an empty state, or a command menu. It is not a source of visual identity. When
you install a component, run the Refuse list against it before it reaches a committed screen — and
restyle through tokens (`color-token-system.md`) rather than leaving defaults.

Also note the stack coupling: React + Tailwind + Motion + shadcn. A Vue, Svelte, or plain-CSS project
gets nothing from this library, and the skill is framework-neutral — so treat this as an optional
adapter, never a core dependency.

## When to reach for it

| Situation | Use Kokonut? |
|---|---|
| Need a date picker, combobox, or table and the deadline is today | Yes — you own the source immediately |
| Building a hero section, animated CTA, or scroll effect | No — that's `premium-marketing-design` |
| The surface is Operate or Dense and the component is decorative | No — write the plain version |
| Vue / Svelte / vanilla-CSS project | No — incompatible stack |
| You need the component to *be* the design | Never — that's an identity exercise, not a scaffold |

## Not found

- **No per-component accessibility conformance statement** and no published WCAG level on the pages
  read. Audit anything you install against `accessibility-web.md`.
- **No published bundle sizes** or performance budgets for components.
- **No component-level token contract.** Whether components accept your `DESIGN.md` tokens or hard-code
  values was not stated on the pages read — inspect a component's source after installing, and restyle
  through tokens if it does not.
- **No stated policy on component deprecation or stability** — the registry is described as 100+
  components with no versioning policy on the pages read.
- **The Pro tier's contents** were not enumerated; only that premium components, advanced templates,
  and a complete package exist.

## Sources

| Source | Publisher | URL | Accessed |
|---|---|---|---|
| Kokonut UI homepage, registry commands, component examples | Kokonut UI | https://kokonutui.com/ | 2026-10-05 |

Install commands, the MCP init command, component names, star count, and the stack coupling are
quoted from that page.