#!/usr/bin/env python3
"""Verdict for run_checks.sh: compares what the checkers computed with the claim in the object JSON.
Needs, in the results file: the gf3prep.py line (n, s, c, k from S), the check_eaqecc.py prepare JSON line (GF(9)
description consistent with S), the gf9info.py prep lines (span(S)^perp closed under w, so it is phi(C) for a
GF(9)-linear code C of dimension kappa = dim/2, and symplectic weight there is Hamming weight on C), the infoset
lines for m = n - d + 1 (every m-subset of coordinates holds an information set of C, in all parts, the parts
together covering all C(n, m) subsets: no nonzero word of C vanishes on m coordinates, so d >= claimed d on all of
span(S)^perp), and the witness.py line (a vector of span(S)^perp outside span(S) with symplectic weight equal to the
claimed d, so d <= claimed d).
Usage: verdict.py object.json results.txt   (exit 0 only if every computed value equals the claimed one)"""
import json, re, sys
from math import comb
obj = json.load(open(sys.argv[1])); txt = open(sys.argv[2]).read()
n, k, c, d = obj["n"], obj["k"], obj["c"], obj["d"]
m = re.search(r"n=(\d+) s=(\d+) c=(\d+) k=(\d+) dim_isotropic=(\d+) dim_dual=(\d+)", txt)
g = re.search(r'"D9_herm_orthogonal_to_G9": (true|false), "rowspace_S_equals_phi_D9": (true|false)', txt)
p9 = re.search(r"n=(\d+) s=(\d+) c=(\d+) k=(\d+) dim_N=(\d+) dim_I=(\d+) N_closed_under_w=(True|False)", txt)
ka = re.search(r"kappa=(\d+) \(2\*kappa == dim_N: (True|False)\)", txt)
parts = re.findall(r"kappa=(\d+) n=(\d+) m=(\d+) part=(\d+)/(\d+) subsets=(\d+) deficient=(\d+)", txt)
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
need(p9 is not None and p9.group(7) == "True" and ka is not None and ka.group(2) == "True",
     "span(S)^perp is closed under w (GF(9)-linear, dimension 2 kappa)")
if p9 and m:
    need(tuple(map(int, p9.groups()[:4])) == tuple(map(int, m.groups()[:4])), "the two parameter computations agree")
M = n - d + 1
sel = [p for p in parts if int(p[2]) == M and int(p[1]) == n]
need(len(sel) > 0 and {int(p[3]) for p in sel} == set(range(int(sel[0][4]))) if sel else False, "all parts of the m=%d information-set test present" % M)
if sel:
    tot = sum(int(p[5]) for p in sel); bad = sum(int(p[6]) for p in sel)
    need(ka is not None and all(int(p[0]) == int(ka.group(1)) for p in sel), "test run on the code recovered from S (kappa=%s)" % (ka.group(1) if ka else "?"))
    need(tot == comb(n, M), "examined %d of C(%d,%d) = %d coordinate subsets" % (tot, n, M, comb(n, M)))
    need(bad == 0, "every %d coordinates hold an information set (deficient subsets: %d), so d >= %d" % (M, bad, d))
need(w is not None and w.group(2) == "True" and int(w.group(1)) == d, "witness of symplectic weight %s outside span(S), claimed d=%d" % (w.group(1) if w else "?", d))
print("computed d=%s; claimed d=%d" % (d if ok else "?", d))
sys.exit(0 if ok else 1)
