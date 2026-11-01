#!/usr/bin/env python3
"""
Builds the installable bookmarklet one-liner from mobbin_web_harvester.js.

Strips the header comment block and standalone // comment lines, joins the
code onto a single line (strings in this file never contain runs of spaces,
and every statement is semicolon-terminated), then percent-encodes it the
same way the mobile bookmarklet is encoded.

Output: mobbin_web_harvester_bookmarklet.txt  (paste into a bookmark URL)

Re-run this after any edit to mobbin_web_harvester.js.
"""

import os
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'mobbin_web_harvester.js')
OUT = os.path.join(HERE, 'mobbin_web_harvester_bookmarklet.txt')

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open(SRC, 'r', encoding='utf-8') as f:
    src = f.read()

# Keep only the code, drop the documentation header
start = src.index('javascript:(')
code = src[start:]

# Strip standalone // comment lines (never touches // inside strings,
# since those lines don't *start* with a comment)
lines = []
for line in code.splitlines():
    stripped = line.strip()
    if stripped.startswith('//'):
        continue
    lines.append(stripped)

# Join into one line; collapse whitespace runs (safe for this source)
one_line = ' '.join(l for l in lines if l)
while '  ' in one_line:
    one_line = one_line.replace('  ', ' ')

# sanity: balanced braces/parens
for open_c, close_c in (('{', '}'), ('(', ')'), ('[', ']')):
    if one_line.count(open_c) != one_line.count(close_c):
        sys.exit(f"❌ Unbalanced {open_c}{close_c} — refusing to build")

prefix = 'javascript:'
encoded = prefix + urllib.parse.quote(one_line[len(prefix):], safe='')

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(encoded)

print(f"✅ Bookmarklet built: {OUT}")
print(f"   {len(one_line)} chars of code -> {len(encoded)} chars encoded")
