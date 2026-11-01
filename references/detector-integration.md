# Detector integration — `npx impeccable detect`

`impeccable detect` is a **dependency, not a fork**. It is invoked from `audit` and `loop`; it is
never vendored, re-implemented, or "fixed" in this skill. Its rules encode marketing-page defaults
that are wrong on product surfaces, which is exactly why this file exists: to say which findings flip
by density class, and to make sure exceptions are recorded narrowly.

## 1. Invoke it

From the project folder:

```
npx impeccable detect src/
npx impeccable detect src/components/Card.tsx
npx impeccable detect http://localhost:3000
npx impeccable detect --json src/
```

**Source scans** inspect UI code and styles — HTML files get static HTML/CSS analysis (which follows
linked CSS), other files get pattern matching, so CSS, JSX, and TSX are covered. **URL scans** open
the page in a browser (headless rendering) so checks can use the *rendered* layout; `http://`,
`https://`, and `file://` URLs are all accepted, and accessible linked CSS is included.

Choose the target that matches the question: a source scan answers "is this pattern in the code," a
URL scan answers "does it look right when rendered." Layout, contrast, and line-length findings
generally only exist in a URL scan; pattern findings generally only exist in a source scan.

## 2. Exit codes

Verified from the CLI's own usage text:

| Code | Meaning | What to do |
|---|---|---|
| `0` | Scan completed with no **primary** findings. **Advisories may still be listed.** | Clean. Read the advisory section anyway. |
| `2` | Scan completed with primary findings. | Fix, or record a narrow exception. |
| `1` | At least one requested target could not be scanned. | **A scan failure, not a pass.** |

Two consequences that matter in a script: primary findings alone determine the count and the exit
code, so advisories never block automation; and on a partial multi-target scan **operational failure
takes precedence** — treat `1` as a failure even if other targets returned findings.

Human-readable findings go to **stderr**, so stdout stays clean for structured output. Use `--json`
for JSON on stdout, or `2> findings.txt` to keep the text. `--quiet` prints only the final count.
`--no-advisory` suppresses advisory findings entirely. Other flags from the usage text:
`--scope <type|layout>`, `--viewport <WxH>` (default 1280x800), `--no-config`,
`--no-inline-ignores`, `--no-design-system`.

**A clean scan is not a good design.** The docs are explicit: "A clean scan means these checks found
no reportable problem; `critique` can assess the wider design." A product surface can be exit-0 and
still have no hierarchy, no states, and a density class nobody declared.

## 3. DESIGN.md-aware drift checks

When a local `DESIGN.md` exists, the detector checks documented fonts, colors, corner radii, and
type sizes against the code; `.impeccable/design.json` supplies the same data structurally. Four
rules come from this: font, colour, radius, and font size outside `DESIGN.md`.

Keep the record current with `impeccable document`, or run one scan without the check with
`--no-design-system`.

This is why a `DESIGN.md` is worth having before a screen is built rather than after: these four
rules only exist once the documented system exists. Drift findings are the mechanical argument for
`init.md` and `document.md`.

## 4. Exceptions: scoped, valued, and reasoned

**The rule that keeps this skill honest: record intentional exceptions with a value-level ignore, not
a global one.**

```
npx impeccable ignores add-value <rule> <value> --reason "<why>"
```

Because "that keeps the rule active for other fonts." A rule silenced everywhere is a rule nobody
reads — `add-rule` turns a check off for the whole repository and returns nothing ever again. Value
ignores buy specificity:

```
# Brand font — the rule stays live for every other font
npx impeccable ignores add-value overused-font Inter --reason "Brand font"

# One file may hold any colour; colours elsewhere are still checked
npx impeccable ignores add-value design-system-color "*" --file "src/demo.css" --reason "Palette comparison demo"
```

A wildcard value `"*"` **requires a file scope.** Manage and review with
`impeccable ignores list` and `impeccable ignores remove-value <rule> <value>`. Shared by default
(written to `.impeccable/config.json`, committed for team decisions); `--local` writes
`.impeccable/config.local.json` and is excluded from git. Manual scans and hooks read the same
ignores.

Where an exception must travel with a file outside the repository, use an inline comment:
`<!-- impeccable-disable overused-font: exported brand document -->`, or the `-line` /
`-next-line` forms. Static HTML findings have no line number, so they need the whole-file form.
Run `/impeccable doctor` afterwards — it checks for unknown keys, **outdated rule IDs**, and
project-root patterns that match nothing, which is how a stale ignore silently rots.

**Workflow:** fix the real problem → re-scan → if the choice is genuinely intentional, record the
value ignore with a reason → never suppress to make a scan go green.

## 5. The density-class advisory table

`craft-floor.md` carries this table and is authoritative; reproduced here because the detector is
where it is needed. **At the class noted, the finding is advisory — not a failure.**

| Detector finding | [F] Focused | [S] Standard | [D] Dense |
|---|---|---|---|
| `tiny-interface-text` | **fail** | **fail** (< 14px body) | **advisory** — 12–13px data type is legal |
| `identical-card-grids` | advisory | **advisory** — legal in a settings or feature index | fail |
| `modal-abuse` | fail | advisory — legal for scoped config | advisory |
| `monotonous-spacing` | **fail** | **fail** | advisory — even rhythm is correct in tables |
| `line-length-too-long` | **fail** | **fail** | advisory — full-width is correct in tables |
| `cramped-padding` | **fail** | **fail** | advisory — tight row padding is correct |
| `nested-cards` | **fail** | **fail** | **fail** |
| `gradient-text` | **fail** | **fail** | **fail** |
| `radial-gradient-background-halo` | **fail** | **fail** | **fail** |
| `low-contrast-text` | **fail** | **fail** | **fail** |
| `oversized-hero-headline` | n/a — not a marketing surface | n/a | n/a |

**The class is a declaration, not an inference.** `audit` reads it from the tokens file or the
brief; if nobody declared one, the scan cannot be adjudicated and the finding stands as a failure.

**Rule-ID caveat.** The names above are the slop catalog's slugs as published on the Impeccable site.
The CLI reports a rule id in each finding's bracket, and the ids are not always identical to the
catalog slugs — the registry this pass read exposes, for example, `undersized-ui-text` and
`tiny-text` for the text-size family, `line-length`, `radial-halo`, `low-contrast`, and `oversized-h1`.
**Take the id from the finding's own bracket before writing an ignore**, and run
`impeccable doctor` to catch an id that no longer resolves. Two slugs in the table above —
`identical-card-grids` and `modal-abuse` — were not present in the registry read on 2026-10-05; the
"Modal abuse" example page is published on the slop site, so treat those two as unverified rather than
renaming them by guess.

**Advisory ≠ ignore.** Impeccable's own advisory mechanism (severity `advisory`, or `--no-advisory`)
is separate from this table. A density-flip finding is *already* in the advisory section if the
rule declares it; where the table promotes a finding to advisory at a class, record it in the audit
report as a class-relative ruling rather than suppressing the rule.

## Not found

- **A normative list of which rules "should" be advisory at which class.** The table is house
  judgement applied to Impeccable's marketing-page defaults. It would be settled by the tool
  publishing per-rule density metadata, or by an upstream change to the rule texts.
- **A published, current mapping from every catalog slug to its CLI rule id.** The registry read for
  this file (2026-10-05) did not contain every slug in the advisory table. Settled by: a slug-to-id
  table in the Impeccable docs, or a versioned rule-pack manifest.
- **Any advice on how long an ignore should live.** Nothing consulted addresses ignore decay;
  `/impeccable doctor`'s outdated-rule-ID check is the only staleness mechanism found.

## Sources

Primary reference for the CLI, exit codes, and ignore mechanics — Impeccable documentation, accessed
2026-10-05:

- Run a detector scan. https://impeccable.style/docs/detector — `npx impeccable detect src/`; one
  file or a URL as a target; source scans vs URL scans (static HTML/CSS analysis for HTML files,
  pattern matching for other files, headless browser rendering for `http(s)://` and `file://`
  URLs including accessible linked CSS); `--json`; the exit-code table (0 no primary findings with
  advisories possible, 2 primary findings, 1 at least one target could not be scanned); DESIGN.md
  and `.impeccable/design.json` drift checks and `--no-design-system`; `npx impeccable ignores
  add-value <rule> <value> --reason "<why>"` and the statement that a value ignore keeps the rule
  active for other values; "A clean scan means these checks found no reportable problem; `critique`
  can assess the wider design."
- Configuration & ignores. https://impeccable.style/docs/config — shared `.impeccable/config.json`
  vs `--local` `config.local.json`; `ignores list` / `remove-value`; `--file` scoping and the rule
  that a wildcard value requires a file scope; inline `impeccable-disable` / `-line` /
  `-next-line` markers with the note that static HTML findings have no line number;
  `projectRoots`; `/impeccable doctor` checking for unknown keys, **outdated rule IDs**, and
  project-root patterns that match nothing; `detector.ignoreRules` / `ignoreFiles` / `ignoreValues` /
  `designSystem.enabled` config keys.
- Slop catalog. https://impeccable.style/slop — the finding slugs, their categories, the four
  DESIGN.md drift rules, and the terminal-invocation examples.
- CLI usage text as published in the tool's own source (`crates/detect/src/cli.rs`) and ignore
  command usage (`crates/detect/src/ignores.rs`), read 2026-10-05 — for `--quiet`, `--scope`,
  `--viewport` (default 1280x800), `--no-config`, `--no-inline-ignores`, `--no-design-system`,
  `--no-advisory`, the stderr/stdout split, the advisory-vs-primary partition, "Operational failure
  takes precedence when a multi-target scan is partial," the `severity: "advisory"` rule field, and
  the rule registry whose ids are quoted in section 5's caveat.

Internal reference files: `craft-floor.md` (the authoritative density-override table and the
refuse list), `quality-audit-checklist.md` (where `audit` runs the scan), `render-loop.md`,
`information-density.md`, `color-token-system.md`.

**House process, not sourced fact:** the density-class advisory table's per-class rulings (with the
underlying Impeccable rule texts cited), the "fix → re-scan → record → never suppress to go green"
workflow, the rule-id caveat, and the integration of the detector into `audit` and `loop` as a
dependency rather than a fork. Exit codes, flags, ignore mechanics, and rule ids are quoted from the
tool's own documentation and source.