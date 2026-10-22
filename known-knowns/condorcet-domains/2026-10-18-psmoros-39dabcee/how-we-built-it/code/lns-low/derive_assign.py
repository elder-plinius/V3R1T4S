"""Derive a never-condition assignment from an explicit domain (one order per line, 1-based, best first).
For each triple a<b<c pick a condition (code 3*s+p) that no order violates; preference: unique, else peak-pit
order given by PREF.  Prints per-triple ambiguity stats and the DP count of the full domain.
Usage: python derive_assign.py DOMAIN(.txt|.gz) OUT.npy"""
import gzip, sys, os
from itertools import combinations
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdlib

path, out = sys.argv[1], sys.argv[2]
op = gzip.open if path.endswith('.gz') else open
with op(path, 'rt') as f:
    D = np.array([[int(x) for x in l.split()] for l in f if l.strip()], dtype=np.int16) - 1
m, n = D.shape
pos = np.empty_like(D); rows = np.arange(m)[:, None]
pos[rows, D] = np.arange(n)[None, :]
cond = np.zeros(cdlib.ntrip(n), dtype=np.uint8)
PREF = [2, 6, 3, 5, 0, 8, 1, 4, 7]
amb = {}
for a, b, c in combinations(range(n), 3):
    P = np.stack([pos[:, a], pos[:, b], pos[:, c]], 1)
    rk = np.argsort(np.argsort(P, 1), 1)  # rank within triple: 0 top
    ok = []
    for s in range(3):
        seen = set(np.unique(rk[:, s]).tolist())
        for p in range(3):
            if p not in seen:
                ok.append(3 * s + p)
    if not ok:
        print('triple', a, b, c, 'no never condition: not a CD'); sys.exit(1)
    amb[len(ok)] = amb.get(len(ok), 0) + 1
    cond[cdlib.tidx(a, b, c)] = sorted(ok, key=PREF.index)[0]
np.save(out, cond)
print('n', n, 'orders', m, 'distinct', len(np.unique(D, axis=0)), 'ambiguity', amb, 'codes', np.bincount(cond, minlength=9).tolist(),
      'fulldomain', cdlib.count(n, cond))
