#!/usr/bin/env python3
"""Parse eaqecc.codetables.de/qutrit.php into rows n,k,c,dlo,dhi,title (TSV)."""
import re, sys, html
h = open(sys.argv[1], encoding='utf-8', errors='replace').read()
rx = re.compile(r'<TD NOWRAP bgcolor="(#[0-9a-fA-F]+)" class="EAQECC" title="([^"]*)">\[\[(\d+),(\d+),(\d+)(?:-(\d+))?;(\d+)\]\]<sub>3</sub>')
rows = []
for m in rx.finditer(h):
    col, title, n, k, dlo, dhi, c = m.groups()
    dlo = int(dlo); dhi = int(dhi) if dhi else dlo
    rows.append((int(n), int(k), int(c), dlo, dhi, col, html.unescape(title)))
out = open(sys.argv[2], 'w')
out.write("n\tk\tc\tdlo\tdhi\tcolour\ttitle\n")
for r in rows:
    out.write("\t".join(map(str, r)) + "\n")
print("entries", len(rows), "gaps", sum(1 for r in rows if r[3] < r[4]),
      "gaps c>=1", sum(1 for r in rows if r[3] < r[4] and r[2] >= 1),
      "gaps c>=1 n<=15", sum(1 for r in rows if r[3] < r[4] and r[2] >= 1 and r[0] <= 15))
