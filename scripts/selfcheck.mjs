#!/usr/bin/env node
/**
 * selfcheck.mjs — structural self-check for premium-web-design.
 *
 * Usage:
 *   node scripts/selfcheck.mjs            # from the skill root
 *   node scripts/selfcheck.mjs --md       # emit a Markdown report
 *
 * This is the mechanical gate for the SKILL. It cannot judge taste. It catches the
 * failure modes that are expensive to discover by hand:
 *   - a command table pointing at a reference file that does not exist
 *   - a reference file with no Sources section (i.e. unsourced claims)
 *   - a reference file far outside the intended length band
 *   - a reference file listed in the knowledge library but absent on disk
 *   - duplicate or contradictory density declarations across files
 *
 * Exit 0 = clean. Exit 1 = at least one ERROR. Warnings do not fail the check.
 */
import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, dirname, resolve, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const SKILL_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const REFS = join(SKILL_ROOT, 'references');
const asMD = process.argv.includes('--md');

const MIN_LINES = 40;
// The agent-skills spec binds SKILL.md (<500 lines), not references/. Reference files
// are loaded on demand, and compressing them means deleting per-claim citations —
// which is the one thing this library exists to provide. Band is a smell test only.
const MAX_LINES = 500;

const errors = [];
const warnings = [];

function rel(p) {
  return p.slice(SKILL_ROOT.length + 1).replace(/\\/g, '/');
}

/* ---- 1. frontmatter ---- */
const skillPath = join(SKILL_ROOT, 'SKILL.md');
if (!existsSync(skillPath)) {
  errors.push('SKILL.md missing');
} else {
  const skill = readFileSync(skillPath, 'utf8');
  if (!/^---\r?\n/.test(skill)) errors.push('SKILL.md: missing YAML frontmatter');
  for (const key of ['name:', 'description:', 'version:']) {
    if (!new RegExp('^' + key, 'm').test(skill)) errors.push(`SKILL.md: frontmatter missing ${key}`);
  }
  const lineCount = skill.split(/\r?\n/).length;
  if (lineCount > 500) {
    errors.push(`SKILL.md is ${lineCount} lines — the agent-skills spec recommends under 500`);
  }
}

/* ---- 2. every relative link in SKILL.md resolves ---- */
if (existsSync(skillPath)) {
  const skill = readFileSync(skillPath, 'utf8');
  const links = [...skill.matchAll(/\]\((?!https?:|#)([^)]+)\)/g)].map((m) => m[1]);
  const seen = new Set();
  for (const link of links) {
    if (seen.has(link)) continue;
    seen.add(link);
    const target = resolve(SKILL_ROOT, link);
    if (!existsSync(target)) errors.push(`SKILL.md: link target missing — ${link}`);
  }
}

/* ---- 3. reference files: sources + length band ---- */
let refCount = 0;
const noSources = [];
const outOfBand = [];
if (existsSync(REFS)) {
  const files = readdirSync(REFS).filter((f) => f.endsWith('.md'));
  refCount = files.length;
  for (const f of files) {
    const abs = join(REFS, f);
    const body = readFileSync(abs, 'utf8');
    const lines = body.split(/\r?\n/).length;

    if (!/^##\s+Sources/im.test(body)) noSources.push(f);
    if (lines < MIN_LINES) outOfBand.push(`${f} (${lines} lines, min ${MIN_LINES})`);
    else if (lines > MAX_LINES) outOfBand.push(`${f} (${lines} lines, max ${MAX_LINES})`);

    // unsourced numeric threshold: a bare px/ms/% figure with no http anywhere in file
    if (!/https?:\/\//.test(body) && !/^##\s+Sources/im.test(body)) {
      warnings.push(`${f}: no URLs at all — cannot be traceable`);
    }
  }
}
for (const f of noSources) errors.push(`references/${f}: no "## Sources" section`);
for (const f of outOfBand) warnings.push(`references/${f}: length out of band`);

/* ---- 4. density declarations agree across files ----
 * A density class must resolve to exactly ONE base value across every file that
 * states it. Identical text in several files is correct and expected (the floor is
 * repeated deliberately); two DIFFERENT values for one class is a real defect.
 */
if (existsSync(REFS)) {
  const files = readdirSync(REFS).filter((f) => f.endsWith('.md'));
  const classes = new Map(); // class -> Map<baseString, Set<file>>
  for (const f of files) {
    const body = readFileSync(join(REFS, f), 'utf8');
    for (const m of body.matchAll(/\|\s*\*\*(Focused|Standard|Dense)\*\*\s*\|([^|]*)\|([^|]*)\|/g)) {
      const cls = m[1];
      const base = m[2].trim();
      if (!classes.has(cls)) classes.set(cls, new Map());
      const byValue = classes.get(cls);
      if (!byValue.has(base)) byValue.set(base, new Set());
      byValue.get(base).add(f);
    }
  }
  for (const [cls, byValue] of classes) {
    if (byValue.size > 1) {
      const detail = [...byValue.entries()]
        .map(([v, fs]) => `"${v}" in ${[...fs].join(', ')}`)
        .join('   |   ');
      errors.push(`density class "${cls}" has ${byValue.size} conflicting base values: ${detail}`);
    }
  }
}

/* ---- 5. the floor must exist and carry the density table ---- */
const floor = join(REFS, 'craft-floor.md');
if (!existsSync(floor)) {
  errors.push('references/craft-floor.md missing — it is the load-bearing file');
} else {
  const body = readFileSync(floor, 'utf8');
  for (const required of ['## Verify', '## Refuse', 'Focused', 'Standard', 'Dense']) {
    if (!body.includes(required)) errors.push(`craft-floor.md: missing "${required}"`);
  }
}

/* ---- 6. design-systems folder shape ---- */
const ds = join(SKILL_ROOT, 'design-systems');
let appCount = 0;
let catCount = 0;
if (existsSync(ds)) {
  const cats = readdirSync(ds).filter((d) => statSync(join(ds, d)).isDirectory());
  catCount = cats.length;
  for (const c of cats) {
    const apps = readdirSync(join(ds, c)).filter((d) => statSync(join(ds, c, d)).isDirectory());
    appCount += apps.length;
  }
}

/* ---- 7. every reference file is mentioned in SKILL.md, and every `file.md`
 * backtick reference inside a reference file resolves.
 *
 * Two bugs escaped an earlier version of this checker; both are now permanent checks:
 *   - SKILL.md's knowledge library lists most files as BARE TEXT, not markdown links,
 *     so the link-target check in step 2 could not see them. ux-laws.md was listed
 *     there but had never actually been written.
 *   - reference files cross-reference each other in backticks (`empty-states.md`),
 *     which no check inspected. render-loop.md pointed at animate.md after that file
 *     was renamed to toolkit-motion.md.
 */
if (existsSync(skillPath) && existsSync(REFS)) {
  const skill = readFileSync(skillPath, 'utf8');
  const refFiles = readdirSync(REFS).filter((f) => f.endsWith('.md'));
  const onDisk = new Set(refFiles);

  for (const f of refFiles) {
    if (!skill.includes(f)) {
      errors.push(`references/${f}: exists but is NOT mentioned in SKILL.md — unreachable`);
    }
  }

  const BACKTICK_MD = /`([a-z0-9][a-z0-9-]*\.md)`/g;
  for (const f of refFiles) {
    const body = readFileSync(join(REFS, f), 'utf8');
    for (const m of body.matchAll(BACKTICK_MD)) {
      if (!onDisk.has(m[1])) {
        errors.push(`references/${f}: cross-reference to missing file — ${m[1]}`);
      }
    }
  }

  for (const m of skill.matchAll(BACKTICK_MD)) {
    if (!onDisk.has(m[1])) {
      errors.push(`SKILL.md: names a missing reference in backticks — ${m[1]}`);
    }
  }
}

/* ---- report ---- */
const lines = [];
lines.push(`premium-web-design self-check`);
lines.push(`root: ${SKILL_ROOT}`);
lines.push('');
lines.push(`SKILL.md            ${existsSync(skillPath) ? 'present' : 'MISSING'}`);
lines.push(`references/         ${refCount} files`);
lines.push(`design-systems/     ${appCount} app folders across ${catCount} categories`);
lines.push('');
lines.push(`ERRORS   ${errors.length}`);
for (const e of errors) lines.push(`  ✗ ${e}`);
lines.push(`WARNINGS ${warnings.length}`);
for (const w of warnings) lines.push(`  ! ${w}`);
lines.push('');
lines.push(errors.length ? 'RESULT: FAIL' : 'RESULT: PASS');

const out = lines.join('\n');
console.log(out);
process.exit(errors.length ? 1 : 0);