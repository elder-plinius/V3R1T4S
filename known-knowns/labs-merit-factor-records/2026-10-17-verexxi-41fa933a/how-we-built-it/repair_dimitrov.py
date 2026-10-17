#!/usr/bin/env python3
"""Try to repair arXiv:2206.12070 rows whose printed hex does not reproduce the printed F: insert one hex digit at
every position (or delete one), decode left-padded to L, keep candidates whose exact energy reproduces the printed F
at its printed precision. Output: L, printed F, number of matching repairs, energy, repaired sequence (0 -> +1)."""
import csv, sys, re
import numpy as np
from fractions import Fraction
rows = [r for r in csv.DictReader(open(sys.argv[1]), delimiter="\t") if r["src"] == "2206.12070" and r["kind"].endswith("?")]
src = re.sub(r"\\allowbreak|\{|\}|\$", "", open(sys.argv[2]).read())
def E(bits):
    s = np.array([1 if c == "0" else -1 for c in bits], dtype=np.int64)
    return int((np.correlate(s, s, "full")[len(s):] ** 2).sum())
for r in rows:
    L = int(r["L"]); F = r["pF"]; dec = len(F.split(".")[1])
    m = re.search(rf"^\s*{L}\s*&[^&]*&\s*([0-9A-Fa-f ]+?)\s*&", src, re.M); h = m.group(1).replace(" ", "")
    tries = {h[:i] + d + h[i:] for i in range(len(h) + 1) for d in "0123456789abcdef"} | {h[:i] + h[i + 1:] for i in range(len(h))}
    hits = set()
    for t in tries:
        v = bin(int(t, 16))[2:]
        if len(v) > L: continue
        b = v.zfill(L); e = E(b)
        if abs(Fraction(L * L, 2 * e) - Fraction(F)) <= Fraction(1, 2 * 10 ** dec): hits.add((e, b))
    print(L, F, len(hits), *(sorted(hits)[0] if hits else ("-", "-")))
