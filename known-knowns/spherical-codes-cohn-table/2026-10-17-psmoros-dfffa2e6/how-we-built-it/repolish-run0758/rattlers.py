#!/usr/bin/env python3
"""repolish lens, H7 (jamming / rattlers, imported from granular-matter physics): for codes whose near-max contact
count k(eps) is below the Maxwell count M, strip rattlers (points with < d contacts within eps of the max, iterated,
as in jammed-packing analysis), then compare the backbone's contacts with the backbone's Maxwell count
M_b = n_b (d-1) - d(d-1)/2 + 1. If contacts >= M_b, the backbone can be rigid and the code is plausibly a strict
local optimum despite k < M (HEURISTIC: counting only, no stress computation).
usage: rattlers.py EPS file:d:N ... > out/rattlers.tsv"""
import sys
import numpy as np

eps = float(sys.argv[1])
print("d\tN\tfile\tM\tk_eps\trattlers\tn_backbone\tcontacts_backbone\tM_backbone\tbackbone_over_maxwell")
for spec in sys.argv[2:]:
    f, d, N = spec.rsplit(":", 2)
    d, N = int(d), int(N)
    X = np.array([[float(t) for t in l.replace(",", " ").split()] for l in open(f) if l.strip()])
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    G = X @ X.T
    np.fill_diagonal(G, -3)
    c = G.max()
    A = G >= c - eps
    k = int(np.triu(A, 1).sum())
    alive = np.ones(N, bool)
    while True:
        deg = (A & alive[None, :] & alive[:, None]).sum(1)
        drop = alive & (deg < d)
        if not drop.any():
            break
        alive &= ~drop
    nb = int(alive.sum())
    kb = int(np.triu(A & alive[None, :] & alive[:, None], 1).sum())
    M = N * (d - 1) - d * (d - 1) // 2 + 1
    Mb = nb * (d - 1) - d * (d - 1) // 2 + 1 if nb else 0
    print("%d\t%d\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%.3f" % (d, N, f.split("/")[-1], M, k, N - nb, nb, kb, Mb,
                                                       kb / Mb if Mb > 0 else float("nan")))
    sys.stdout.flush()
