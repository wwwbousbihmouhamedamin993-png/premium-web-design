#!/usr/bin/env python3
"""unslop_grep — mechanical first pass for the unslop remediation audit.

Greps page source for the mechanically greppable signs from references/unslop/signs.md.
Every hit is a lead, not a verdict; the judgment signs (spacing rhythm, hierarchy,
template look) stay with the catalog walk. Zero dependencies, Python 3.8+.
Part of the unslop kit adapted from heydamir/unslop (CC BY 4.0).

Usage:
  python unslop_grep.py <paths...>            # walk files, print findings
  python unslop_grep.py <paths...> --json     # machine-readable findings
  python unslop_grep.py --list                # print the sign table

Exit codes: 0 = clean, 1 = findings, 2 = usage / IO error.
"""

import argparse
import json
import os
import re
import sys

# Each sign: id, group, regex, human sign, fix pointer (signs.md group).
SIGNS = [
    ("motion-loop", "Motion", r"animate-(pulse|ping|bounce)", "purposeless looping animation", "make it static (signs.md §Motion)"),
    ("motion-transition-all", "Motion", r"transition-all\b", "catch-all transition", "name the properties (signs.md §Motion)"),
    ("motion-hover-scale", "Motion", r"hover:scale-", "hover scale on cards/buttons", "color or surface step on hover (signs.md §Motion)"),
    ("motion-parallax", "Motion", r"\bparallax\b|data-speed=|rellax", "parallax / floating on scroll", "static layout (signs.md §Motion)"),
    ("motion-symmetric-ease", "Motion", r"ease-in-out", "symmetric easing on both directions", "decelerate in, accelerate out (signs.md §Motion)"),
    ("surface-gradient-text", "Surfaces and color", r"bg-clip-text|text-transparent\b", "gradient text", "solid primary text color (signs.md §Surfaces)"),
    ("surface-purple-gradient", "Surfaces and color", r"(from|via|to)-(purple|violet|pink|fuchsia)-\d{3}", "purple/violet/pink gradient family", "one neutral surface (signs.md §Surfaces)"),
    ("surface-glow", "Surfaces and color", r"shadow-\[0_0_|text-shadow-\[|drop-shadow-\[(?:0_0_)?\d*px.*rgba", "colored glow / glow shadow", "surface steps and hairlines (signs.md §Surfaces)"),
    ("surface-blob", "Surfaces and color", r"blur-(2xl|3xl)\b", "blurred blob / color wash behind content", "remove (signs.md §Surfaces)"),
    ("type-heavy-heading", "Type", r"font-(extrabold|black)\b", "heading weight 800-900", "400-500 with size for hierarchy (signs.md §Type)"),
    ("type-tracked-uppercase", "Type", r"uppercase\s+tracking-(wider|widest)|tracking-(wider|widest)\s+uppercase", "uppercase tracked label", "sentence case (signs.md §Type)"),
    ("components-pill-radius", "Components", r"9999px|rounded-\[9999px\]", "pill radius everywhere", "radius by size, nested math (signs.md §Components)"),
    ("copy-exclamation", "Copy", r"!!|\w!", "exclamation marks in interface copy", "plain statement (signs.md §Copy)"),
    ("copy-hype", "Copy", r"(?i)\b(supercharge\w*|revolutioni[sz]\w*|game-chan\w*|unleash\w*|elevate your|transform your|next-gen|next generation|effortless(ly)?|magic\w*|blazing(ly)? fast)\b", "hype word", "what the thing actually does (signs.md §Copy)"),
    ("copy-unlock", "Copy", r"(?i)\bunlock\w*\b", "unlock (hype)", "what the thing actually does (signs.md §Copy)"),
    ("copy-greeting", "Copy", r"(?i)welcome back", "greeting headline", "the page or period as the title (signs.md §Copy)"),
    ("copy-wordy-placeholder", "Copy", r"(?i)search (anything|for anything|everything)", "wordy placeholder", "short label: Search (signs.md §Copy)"),
    ("copy-unverified-claim", "Copy", r"(?i)(trusted by|loved by|used by|joined by)\s|\b\d{1,3},000\+", "unverified social-proof claim", "verify, then quiet and specific, or remove (signs.md §Landing)"),
    ("copy-ai-powered", "Copy", r"(?i)\bAI-powered\b|(?i)powered by AI", "AI-powered on everything", "what the AI actually produces (signs.md §Visuals)"),
    ("copy-fake-data", "Copy", r"\[X\]|(?i)lorem ipsum|\b123,456\b|\bJohn Doe\b|\bACME\b", "placeholder / fake looking data", "plausible numbers and names (signs.md §Copy)"),
]

HINTS = [
    ("hint-pill", "Components", r"rounded-full\b", "pill radius (fine for avatars/dots — check it is not every element)", "radius by size (signs.md §Components)"),
    ("hint-gradient", "Surfaces and color", r"bg-gradient-to-", "gradient in use — check it is a tone shift inside one neutral, never hue to hue", "signs.md §Surfaces"),
]

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u2B50]"
)
EXTENSIONS = {".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".jsx",
              ".ts", ".tsx", ".vue", ".svelte", ".astro", ".php", ".erb", ".hbs",
              ".handlebars", ".ejs"}
SKIP_DIRS = {".git", "node_modules", "dist", "build", "out", ".next", ".nuxt",
             "coverage", ".venv", "venv", "__pycache__"}


def iter_files(paths):
    for path in paths:
        if os.path.isfile(path):
            yield path
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for name in files:
                    if os.path.splitext(name)[1].lower() in EXTENSIONS:
                        yield os.path.join(root, name)
        else:
            print(f"unslop_grep: path not found: {path}", file=sys.stderr)


def compile_signs(signs):
    """Compile patterns; an inline (?i) becomes a compile-time flag (3.11+ strictness)."""
    out = []
    for sign_id, group, pattern, sign, fix in signs:
        flags = re.IGNORECASE if "(?i)" in pattern else 0
        out.append((sign_id, group, re.compile(pattern.replace("(?i)", ""), flags), sign, fix))
    return out


def scan(lines):
    """Yield (lineno, kind, sign_id, group, sign, fix, match_text) for one file."""
    for lineno, line in enumerate(lines, 1):
        for sign_id, group, regex, sign, fix in COMPILED_SIGNS:
            m = regex.search(line)
            if m:
                yield lineno, "sign", sign_id, group, sign, fix, m.group(0)
        for sign_id, group, regex, sign, fix in COMPILED_HINTS:
            m = regex.search(line)
            if m:
                yield lineno, "hint", sign_id, group, sign, fix, m.group(0)
        if EMOJI_RE.search(line):
            sample = EMOJI_RE.search(line).group(0)
            yield lineno, "sign", "emoji-decoration", "Icons", \
                f"emoji in UI source ({sample})", \
                "one line icon set or nothing (signs.md §Icons)", sample


COMPILED_SIGNS = compile_signs(SIGNS)
COMPILED_HINTS = compile_signs(HINTS)


def main():
    ap = argparse.ArgumentParser(description="Mechanical slop sweep (unslop kit)")
    ap.add_argument("paths", nargs="*", help="files or directories to scan")
    ap.add_argument("--json", action="store_true", help="emit findings as JSON")
    ap.add_argument("--list", action="store_true", help="print the sign table and exit")
    args = ap.parse_args()

    if args.list:
        print(f"{'id':<26}{'group':<22}sign")
        for sign_id, group, _, sign, _ in SIGNS:
            print(f"{sign_id:<26}{group:<22}{sign}")
        for sign_id, group, _, sign, _ in HINTS:
            print(f"{sign_id:<26}{group:<22}{sign}  [hint]")
        return 0

    if not args.paths:
        ap.error("provide at least one file or directory (or --list)")

    findings = []
    for path in iter_files(args.paths):
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                for hit in scan(fh.read().splitlines()):
                    findings.append((path,) + hit)
        except OSError as exc:
            print(f"unslop_grep: cannot read {path}: {exc}", file=sys.stderr)

    if args.json:
        print(json.dumps([
            {"file": f, "line": ln, "kind": kind, "id": sid, "group": g,
             "sign": s, "fix": fx, "match": mt}
            for (f, ln, kind, sid, g, s, fx, mt) in findings
        ], indent=2))
    else:
        for f, ln, kind, sid, g, s, fx, mt in findings:
            tag = "hint" if kind == "hint" else "sign"
            print(f"{f}:{ln}  [{tag}] {g} · {sid}: {s}  → {fx}")
        if findings:
            signs = sum(1 for x in findings if x[2] == "sign")
            hints = len(findings) - signs
            print(f"\n{signs} sign(s), {hints} hint(s). "
                  "Hits are leads, not verdicts — walk references/unslop/signs.md "
                  "for the full audit and the browser look.")

    return 1 if any(x[2] == "sign" for x in findings) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
