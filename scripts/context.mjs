#!/usr/bin/env node
/**
 * context.mjs — load the host project's design context for premium-web-design.
 *
 * Usage (from the project root, keep cwd at the user's project):
 *   node <skill-base-dir>/scripts/context.mjs [--target <path>]
 *
 * Prints the project's product/design docs, detects the stack so `init` knows which
 * DESIGN-[framework].md adapter to generate, and prints the directives that govern a
 * design session. Exits 0 always; a missing doc is a note, not an error.
 */
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';

const args = process.argv.slice(2);
const targetIdx = args.indexOf('--target');
const target = targetIdx !== -1 ? args[targetIdx + 1] : null;

const CANDIDATES = [
  'PRODUCT.md',
  'DESIGN.md',
  'DESIGN-tailwind.md',
  'DESIGN-css-modules.md',
  'DESIGN-vue.md',
  'DESIGN-svelte.md',
  'DESIGN-nextjs.md',
  'docs/DESIGN.md',
  'docs/design.md',
  'docs/PRODUCT.md',
  'AGENTS.md',
  'CLAUDE.md',
  '.agents/skills/design-review/SKILL.md',
  'docs/ui-polish-workflow.md',
];

const MAX_LINES = 140;

function printDoc(relPath) {
  const abs = resolve(process.cwd(), relPath);
  if (!existsSync(abs)) return false;
  const lines = readFileSync(abs, 'utf8').split(/\r?\n/);
  const truncated = lines.length > MAX_LINES;
  console.log(`\n=== ${relPath}${truncated ? ` (first ${MAX_LINES} of ${lines.length} lines)` : ''} ===`);
  console.log(lines.slice(0, MAX_LINES).join('\n'));
  if (truncated) console.log(`… read ${relPath} directly for the rest`);
  return true;
}

/* ---- stack detection: decides which DESIGN-[framework].md adapter `init` writes ---- */

const STACK_SIGNALS = [
  { id: 'nextjs', label: 'Next.js', deps: ['next'], files: ['next.config.js', 'next.config.mjs', 'next.config.ts'] },
  { id: 'react', label: 'React', deps: ['react'], files: [] },
  { id: 'vue', label: 'Vue', deps: ['vue'], files: [] },
  { id: 'svelte', label: 'Svelte / SvelteKit', deps: ['svelte', '@sveltejs/kit'], files: [] },
  { id: 'angular', label: 'Angular', deps: ['@angular/core'], files: [] },
  { id: 'astro', label: 'Astro', deps: ['astro'], files: [] },
  { id: 'remix', label: 'Remix / React Router', deps: ['@remix-run/react', 'react-router-dom'], files: [] },
  { id: 'tanstack', label: 'TanStack Start', deps: ['@tanstack/react-start'], files: [] },
];

const STYLING_SIGNALS = [
  { id: 'tailwind', label: 'Tailwind CSS', deps: ['tailwindcss'], files: [] },
  { id: 'css-modules', label: 'CSS Modules / plain CSS', deps: [], files: [] },
  { id: 'styled-components', label: 'styled-components', deps: ['styled-components'], files: [] },
  { id: 'emotion', label: 'Emotion', deps: ['@emotion/react', '@emotion/styled'], files: [] },
  { id: 'vanilla-extract', label: 'vanilla-extract', deps: ['vanilla-extract'], files: [] },
  { id: 'unocss', label: 'UnoCSS', deps: ['unocss'], files: [] },
];

function readJSON(path) {
  try {
    // Strip a UTF-8 BOM if present: JSON.parse rejects it, and real-world
    // package.json files (especially Windows-authored) sometimes carry one.
    const raw = readFileSync(resolve(process.cwd(), path), 'utf8').replace(/^﻿/, '');
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function detectStack() {
  const pkg = readJSON('package.json');
  const deps = pkg ? { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}) } : {};
  const has = (name) => Object.prototype.hasOwnProperty.call(deps, name);
  const fileExists = (name) => existsSync(resolve(process.cwd(), name));

  const frameworks = STACK_SIGNALS.filter((s) => s.deps.some(has) || s.files.some(fileExists));
  const styling = STYLING_SIGNALS.filter((s) => s.deps.some(has));
  if (styling.length === 0 && (frameworks.length > 0 || pkg)) styling.push({ id: 'css-modules', label: 'CSS Modules / plain CSS (assumed)' });

  const dens = Object.keys(deps).filter((d) => d.includes('tailwind') || d.includes('radix') || d.includes('headless') || d.includes('shadcn'));
  const scripts = pkg && pkg.scripts ? Object.keys(pkg.scripts) : [];

  return { frameworks, styling, dens, scripts, hasPkg: !!pkg };
}

/* ---- density hints: surfaces that suggest a tier before the mode is declared ---- */

function densityHints(stack) {
  const hints = [];
  const s = new Set([...stack.frameworks, ...stack.styling].map((x) => x.id));
  if (s.has('tailwind')) hints.push('Tailwind detected — its default `--spacing: 0.25rem` base is Standard-leaning; a Dense console needs an explicit density mode, not smaller default type.');
  hints.push('No density class is declared yet. Declare Focused / Standard / Dense before applying any type or spacing rule (craft-floor.md).');
  return hints;
}

/* ---- run ---- */

console.log('PREMIUM-WEB-DESIGN — project context');
console.log('cwd: ' + process.cwd());

let found = 0;
for (const c of CANDIDATES) {
  if (printDoc(c)) found++;
}

if (target) {
  if (!printDoc(target)) {
    console.log(`\n=== ${target} ===\n(not found — verify the path)`);
  }
}

const stack = detectStack();
console.log('\n=== DETECTED STACK ===');
if (!stack.hasPkg) {
  console.log('no package.json found — framework-neutral defaults apply.');
} else {
  console.log('framework:  ' + (stack.frameworks.map((f) => f.label).join(', ') || 'unknown'));
  console.log('styling:    ' + (stack.styling.map((f) => f.label).join(', ') || 'unknown'));
  if (stack.dens.length) console.log('ui libs:    ' + stack.dens.join(', '));
  if (stack.scripts.length) console.log('scripts:    ' + stack.scripts.slice(0, 12).join(', '));
}
console.log('\n=== DENSITY HINTS ===');
for (const h of densityHints(stack)) console.log('- ' + h);

if (found === 0 && !target) {
  console.log('\nNo project design docs found. This skill\'s defaults apply;');
  console.log('run the `init` command to capture product truth in PRODUCT.md');
  console.log('and derive a framework-agnostic DESIGN.md plus an optional');
  console.log('DESIGN-[framework].md adapter, or `document` to record an incumbent system.');
} else if (!existsSync(resolve(process.cwd(), 'PRODUCT.md'))) {
  console.log('\nPRODUCT.md not found — run the `init` command to capture');
  console.log('durable product truth and derive DESIGN.md before new-surface work.');
}

console.log('\n=== DIRECTIVES ===');
console.log('1. Precedence: host project docs above override this skill\'s defaults');
console.log('   (tokens, target-size minimums, copy voice, wrapper components).');
console.log('2. Follow the project\'s brief workflow if its docs define one.');
console.log('3. This skill owns logged-in product surfaces only. Public marketing');
console.log('   pages route to premium-marketing-design; mobile routes to');
console.log('   premium-mobile-design.');
console.log('4. Load references/craft-floor.md before editing UI, and declare the');
console.log('   surface\'s density class (Focused / Standard / Dense) first.');
console.log('5. Load references/render-loop.md before calling any screen done.');
console.log('6. `npx impeccable detect` is advisory at the density class noted in');
console.log('   craft-floor.md, not a hard gate. See references/detector-integration.md.');
console.log('7. Do not rerun context.mjs this session.');