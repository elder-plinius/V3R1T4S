#!/usr/bin/env python3
"""Extract and check a witness: a vector v of span(S)^perp supported inside the given position
set T and not in the isotropic part span(S) ∩ span(S)^perp. Checks, from S directly: <r, v> = 0 for every row r of
S; v is not in span(S) (so not in the isotropic part); its symplectic weight.
Usage: witness.py object.json "t1,t2,..."   prints v as (x|z) and the checks."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf3prep import analyze, nullspace, rank, symp, vecmat

obj = json.load(open(sys.argv[1])); n, S = obj["n"], obj["S"]
T = sorted(int(t) for t in sys.argv[2].split(","))
info, B = analyze(S, n)
out = [i for i in range(n) if i not in T]
cols = out + [n + i for i in out]
# a with (a B)|out = 0  <=>  B_out^T a = 0
Bt = [[B[r][c] for r in range(len(B))] for c in cols]
A = nullspace(Bt, len(B))
s = rank(S, 2 * n)
for a in A:
    v = vecmat(a, B)
    if rank(S + [v], 2 * n) > s:
        w = sum(1 for i in range(n) if v[i] or v[n + i])
        ok_dual = all(symp(r, v, n) == 0 for r in S)
        print("T=%s" % T)
        print("v_x=%s" % " ".join(map(str, v[:n])))
        print("v_z=%s" % " ".join(map(str, v[n:])))
        print("symplectic_weight=%d orthogonal_to_all_rows_of_S=%s in_span_S=False support=%s" %
              (w, ok_dual, [i for i in range(n) if v[i] or v[n + i]]))
        break
else:
    print("no vector of N outside span(S) supported in T")
