#!/usr/bin/env python3
"""Standalone checker (Python 3 standard library only) for a Packomania scu data-integrity finding.

Definition (bank target packomania-scu-spheres-in-cube): for centres c_i in the cube [-1/2,1/2]^3,
  r* = min( min_{i<j} |c_i - c_j| / 2 , 1/2 - max_i max(|x_i|,|y_i|,|z_i|) ).
Partial win p3: the posted coordinates scu<N>.txt do NOT achieve the posted radius.txt value.
Reads CLAIM.json next to this script. Exact Decimal arithmetic at 60 digits (square root only at the end).
"""
import hashlib, itertools, json, os, sys
from decimal import Decimal as D, getcontext
getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE)
C = json.load(open(os.path.join(HERE, "CLAIM.json")))
N = int(C["N"]); cell = D(C["table_value"]); margin = D(C["margin"])
ok = True
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def centres(path, idx):
    out = []
    for line in open(path):
        p = line.split()
        if not p or p[0].startswith("#"): continue
        if idx and len(p) >= 4: out.append([D(x) for x in p[1:4]])
        elif not idx and len(p) == 3: out.append([D(x) for x in p])
    return out
def rstar(P):
    w = min(D("0.5") - max(abs(x) for x in c) for c in P)
    d2 = min(sum((a - b) ** 2 for a, b in zip(P[i], P[j])) for i, j in itertools.combinations(range(len(P)), 2))
    return min(d2.sqrt() / 2, w), w, d2.sqrt() / 2
posted = os.path.join(PKG, C["posted_copy"])
s = sha(posted); print("posted copy sha256", s)
if s != C["posted_sha256"]: print("posted copy sha256 differs from the live fetch"); ok = False
P = centres(posted, True)
print("N", N, "centre rows in posted file", len(P))
if C["kind"] == "row_count":
    if len(P) != N - int(C["missing_rows"]): print("row count differs from claim"); ok = False
    else: print("posted file holds %d centres for N = %d: it cannot certify the posted radius for N = %d" % (len(P), N, N))
    r, w, h = rstar(P)
    print("r* of the %d posted centres %s (cell %s)" % (len(P), r, cell))
else:
    if len(P) != N: print("posted file row count is not N"); ok = False
    r, w, h = rstar(P)
    print("posted r* %s (wall %s, half min distance %s)" % (r, w, h))
    print("table cell %s" % cell); gap = r - cell; print("posted r* - cell %s" % gap)
    if not gap < -margin: print("posted file is not short of the cell by more than %s" % margin); ok = False
    if C.get("object"):
        ob = os.path.join(PKG, C["object"]); so = sha(ob); print("object sha256", so)
        if so != C["object_sha256"]: print("object sha256 differs"); ok = False
        Q = centres(ob, False)
        if len(Q) != N: print("object row count is not N"); ok = False
        ro = rstar(Q)[0]; print("object (refined from posted) r* %s; minus cell %s" % (ro, ro - cell))
        if not str(ro).startswith(C["object_rstar_prefix"]):
            print("object r* differs from claim"); ok = False
        if not ro - cell < -margin: print("object reaches the cell"); ok = False
sys.exit(0 if ok else 1)
