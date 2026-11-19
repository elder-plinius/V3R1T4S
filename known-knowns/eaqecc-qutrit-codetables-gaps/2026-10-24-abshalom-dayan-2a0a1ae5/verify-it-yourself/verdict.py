#!/usr/bin/env python3
"""Verdict for run_checks.sh: compares what the checkers computed with the claim in the object JSON.
Needs, in the results file: the gf3prep.py line (n, s, c, k), the check_eaqecc.py prepare JSON line (GF(9) checks),
the four subset_ea W = d - 1 lines (every (d-1)-subset of positions examined, none holding a vector of span(S)^perp
outside the isotropic part, so d >= claimed d), and the witness.py line (a vector of span(S)^perp outside span(S)
with symplectic weight equal to the claimed d, so d <= claimed d).
Usage: verdict.py object.json results.txt   (exit 0 only if every computed value equals the claimed one)"""
import json, re, sys
from math import comb
obj = json.load(open(sys.argv[1])); txt = open(sys.argv[2]).read()
n, k, c, d = obj["n"], obj["k"], obj["c"], obj["d"]
m = re.search(r"n=(\d+) s=(\d+) c=(\d+) k=(\d+) dim_isotropic=(\d+) dim_dual=(\d+)", txt)
g = re.search(r'"D9_herm_orthogonal_to_G9": (true|false), "rowspace_S_equals_phi_D9": (true|false)', txt)
parts = re.findall(r"W=(\d+) part=(\d+)/(\d+) total_subsets=(\d+) examined=(\d+) with_vector_outside_isotropic=(\d+)", txt)
w = re.search(r"symplectic_weight=(\d+) orthogonal_to_all_rows_of_S=(True|False) in_span_S=False", txt)
ok = True
def need(cond, msg):
    global ok
    print(("ok:   " if cond else "FAIL: ") + msg); ok = ok and cond
need(m is not None, "parameters computed from S")
if m:
    cn, cs, cc, ck = map(int, m.groups()[:4])
    need((cn, ck, cc) == (n, k, c) and cc >= 1, "computed n=%d s=%d c=%d k=%d; claimed n=%d k=%d c=%d" % (cn, cs, cc, ck, n, k, c))
need(g is not None and g.group(1) == "true" and g.group(2) == "true", "GF(9) description consistent with S")
W = d - 1
sel = [p for p in parts if int(p[0]) == W]
need(len(sel) > 0 and {int(p[1]) for p in sel} == set(range(int(sel[0][2]))) if sel else False, "all parts of the W=%d subset test present" % W)
if sel:
    ex = sum(int(p[4]) for p in sel); bad = sum(int(p[5]) for p in sel)
    need(ex == comb(n, W) and all(int(p[3]) == comb(n, W) for p in sel), "examined %d of C(%d,%d) = %d subsets" % (ex, n, W, comb(n, W)))
    need(bad == 0, "no vector of span(S)^perp outside the isotropic part on <= %d positions (found %d)" % (W, bad))
need(w is not None and w.group(2) == "True" and int(w.group(1)) == d, "witness of symplectic weight %s outside span(S), claimed d=%d" % (w.group(1) if w else "?", d))
print("computed d=%s; claimed d=%d" % (d if ok else "?", d))
sys.exit(0 if ok else 1)
