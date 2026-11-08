"""Exhaustive subset search by glacier-grouped CV (training glaciers only): 'one' plus up to K other phis, for one season.
Usage: python3 -I subset_search_season.py <n_months> <K>"""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, mbdata
import cv_linear as L
season, K = int(sys.argv[1]), int(sys.argv[2])
tr = mbdata.load("train"); _, fold_of = mbdata.glacier_folds(tr, 6)
names = [n for n in L.phis(tr) if n != "one"]
A_all, y, rgi = L.design(tr, ["one"] + names, season=season)
fo = np.array([fold_of[r] for r in rgi])
res = []
for k in range(0, K + 1):
    for sub in itertools.combinations(range(len(names)), k):
        idx = [0] + [i + 1 for i in sub]; A = A_all[:, idx]; pred = np.zeros(len(y))
        for f in range(6):
            te = fo == f; pred[te] = A[te] @ L.fit(A[~te], y[~te])
        res.append((float(np.sqrt(np.mean((pred - y) ** 2))), ["one"] + [names[i] for i in sub]))
res.sort()
print("season", season, "points", len(y), "subsets searched:", len(res))
for r in res[:12]: print("%.4f" % r[0], r[1])
