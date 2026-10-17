#!/usr/bin/env python3
"""Propagation closure of live upper bounds U(n,k) for qubit codes, k >= 1 only (k = 0 uses a different
distance notion and is excluded).  Rules (each valid for stabilizer codes with k >= 1):
  R1 U(n,k) <= U(n,k-1)      for k >= 2      ([[n,k,d]] -> [[n,k-1,d]])
  R2 U(n,k) <= U(n+1,k)                      ([[n,k,d]] -> [[n+1,k,d]])
  R3 U(n,k) <= U(n-1,k+1)+1  for n >= 2      ([[n,k,d]] -> [[n-1,k+1,d-1]])
Usage: propagate.py parsed.json out.json [cell_overrides.json]
Writes closure, the list of live cells strictly above their closure (monotonicity audit), and a per-cell
'implied_by' witness."""
import json, sys
T = json.load(open(sys.argv[1]))
U = {(int(n), int(k)): v[1] for n, row in T.items() for k, v in row.items() if int(k) >= 1}
if len(sys.argv) > 3:
    for key, val in json.load(open(sys.argv[3])).items():
        n, k = map(int, key.split(','))
        U[(n, k)] = min(U[(n, k)], val)
C = dict(U)
why = {}
changed = True
while changed:
    changed = False
    for (n, k), u in sorted(C.items()):
        cands = []
        if k >= 2 and (n, k - 1) in C: cands.append((C[(n, k - 1)], 'R1 (%d,%d)' % (n, k - 1)))
        if (n + 1, k) in C: cands.append((C[(n + 1, k)], 'R2 (%d,%d)' % (n + 1, k)))
        if (n - 1, k + 1) in C: cands.append((C[(n - 1, k + 1)] + 1, 'R3 (%d,%d)+1' % (n - 1, k + 1)))
        for v, w in cands:
            if v < C[(n, k)]:
                C[(n, k)] = v; why[(n, k)] = w; changed = True
viol = sorted([(n, k, U[(n, k)], C[(n, k)], why[(n, k)]) for (n, k) in U if C[(n, k)] < U[(n, k)]])
out = {"closure": {"%d,%d" % nk: v for nk, v in C.items()},
       "violations": [{"n": n, "k": k, "live_upper": u, "implied_upper": c, "via": w} for n, k, u, c, w in viol]}
json.dump(out, open(sys.argv[2], 'w'))
big = [v for v in viol if v[0] > 100]
print("cells k>=1:", len(U), " live > implied:", len(viol), " of which n>100:", len(big),
      " n<=100:", len(viol) - len(big))
for v in viol[:5] + big[:10]: print("  ", v)
