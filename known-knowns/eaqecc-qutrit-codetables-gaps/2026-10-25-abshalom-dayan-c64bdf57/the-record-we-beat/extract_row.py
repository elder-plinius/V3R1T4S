#!/usr/bin/env python3
"""Print every table cell of row (n, k) of a saved qutrit.php verbatim, then a summary c: d_lower-d_upper.
Usage: extract_row.py qutrit.php n k"""
import re, sys
t = open(sys.argv[1], encoding="utf-8", errors="replace").read(); n, k = int(sys.argv[2]), int(sys.argv[3])
cells = re.findall(r'<TD[^>]*>\[\[%d,%d,[^\]]*\]\]<sub>3</sub></TD>' % (n, k), t)
summ = []
for c in cells:
    print(c)
    m = re.search(r'\[\[%d,%d,(\d+)(?:-(\d+))?;(\d+)\]\]' % (n, k), c)
    lo, hi, cc = m.group(1), m.group(2) or m.group(1), m.group(3)
    tele = "teleportation" in c
    summ.append((int(cc), "%s: %s-%s%s" % (cc, lo, hi, " (using teleportation)" if tele else "")))
print("row (%d,%d), %d cells; c: d_lower-d_upper: %s" % (n, k, len(cells), "; ".join(s for _, s in sorted(summ))))
