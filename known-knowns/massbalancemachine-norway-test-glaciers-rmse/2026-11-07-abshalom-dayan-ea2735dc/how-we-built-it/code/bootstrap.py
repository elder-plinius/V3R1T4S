"""Supplementary spread (not gating): glacier-block bootstrap over the 14 test glaciers of RMSE(model) - RMSE(MBM) per
season. Resamples whole glaciers with replacement (numpy default_rng(seed 0), 2000 resamples); a resampled glacier
contributes all its points of that season. Inputs: two test monthly prediction arrays (.npy, row order of the test CSV).
Usage: python3 -I -B bootstrap.py <model_pred.npy> <mbm_pred.npy> [seasons, default Ba,Bw,Bs]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, mbdata

SEAS = {"Ba": 12, "Bw": 7, "Bs": 5}
te = mbdata.load("test")
pm, pb = np.load(sys.argv[1]), np.load(sys.argv[2])
seasons = sys.argv[3].split(",") if len(sys.argv) > 3 else ["Ba", "Bw", "Bs"]
uid, inv = np.unique(te["gid"], return_inverse=True)
obs = np.zeros(len(uid)); obs[inv] = te["balance"]; nm = np.zeros(len(uid), int); nm[inv] = te["n_months"]
rgi = np.empty(len(uid), dtype=object); rgi[inv] = te["rgi"]
Sm, Sb = np.bincount(inv, weights=pm), np.bincount(inv, weights=pb)
gl = sorted(set(rgi)); rng = np.random.default_rng(0); B = 2000
draws = [rng.integers(0, len(gl), len(gl)) for _ in range(B)]
for s in seasons:
    k = nm == SEAS[s]
    em, eb = (Sm[k] - obs[k]) ** 2, (Sb[k] - obs[k]) ** 2
    g = np.array([gl.index(r) for r in rgi[k]])
    sm = np.bincount(g, weights=em, minlength=len(gl)); sb = np.bincount(g, weights=eb, minlength=len(gl)); n = np.bincount(g, minlength=len(gl))
    d0 = np.sqrt(em.mean()) - np.sqrt(eb.mean())
    d = np.array([np.sqrt(sm[i].sum() / n[i].sum()) - np.sqrt(sb[i].sum() / n[i].sum()) for i in draws])
    lo, hi = np.percentile(d, [2.5, 97.5])
    print("%s n=%d model %.4f MBM %.4f diff %+.4f  95%% [%+.4f, %+.4f]  share of resamples with diff<0: %.3f" % (
        s, k.sum(), np.sqrt(em.mean()), np.sqrt(eb.mean()), d0, lo, hi, (d < 0).mean()))
