"""CV-only analysis of OOF predictions (training glaciers): per-season RMSE of linear, plain GBM and hybrid at each stage,
blend weights w (GBM share, 0..1 step 0.05) per season minimising pooled OOF RMSE, and per-glacier RMSE.
Usage: python3 -I -B analyze.py <oof.npz> [optional choice .json output path]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np, mbdata, score

z = np.load(sys.argv[1]); tr = mbdata.load("train")
R = lambda p: score.rmse_by_season(tr["gid"], p, tr["balance"], tr["n_months"])
fmt = lambda r: "Ba %.4f Bw %.4f Bs %.4f mean %.4f" % (r["Ba"], r["Bw"], r["Bs"], (r["Ba"] + r["Bw"] + r["Bs"]) / 3)
print("cfg", str(z["cfg"]))
print("linear      ", fmt(R(z["lin"])))
out = {"linear": R(z["lin"])}
for name in ("plain", "hyb"):
    for s in range(z[name].shape[0]):
        print("%-5s n=%3d  " % (name, (s + 1) * 50), fmt(R(z[name][s])))
# best plain stage by mean, then blend weights per season
best = {}
for name in ("plain", "hyb"):
    sc = [np.mean([R(z[name][s])[k] for k in ("Ba", "Bw", "Bs")]) for s in range(z[name].shape[0])]
    best[name] = int(np.argmin(sc)); print("best stage", name, (best[name] + 1) * 50, "%.4f" % min(sc))
g = z["plain"][best["plain"]]; l = z["lin"]
ws = np.round(np.arange(0, 1.0001, 0.05), 2); wbest = {}
for s in ("Ba", "Bw", "Bs"):
    sc = [R(w * g + (1 - w) * l)[s] for w in ws]
    wbest[s] = float(ws[int(np.argmin(sc))]); print("blend", s, "w_gbm", wbest[s], "cv %.4f" % min(sc), "(w=0 %.4f, w=1 %.4f)" % (sc[0], sc[-1]))
choice = {"best_plain_n": (best["plain"] + 1) * 50, "best_hyb_n": (best["hyb"] + 1) * 50, "w_gbm": wbest}
print("choice", json.dumps(choice))
if len(sys.argv) > 2:
    json.dump(choice, open(sys.argv[2], "w"), indent=1)
# per-glacier pooled-season RMSE (linear vs plain best)
uid, inv = np.unique(tr["gid"], return_inverse=True); obs = np.zeros(len(uid)); obs[inv] = tr["balance"]
rgi = np.empty(len(uid), dtype=object); rgi[inv] = tr["rgi"]
for nm, p in (("lin", l), ("gbm", g)):
    S = np.bincount(inv, weights=p)
    print(nm, " ".join("%s:%.2f(n%d)" % (r[-5:], np.sqrt(np.mean((S[rgi == r] - obs[rgi == r]) ** 2)), (rgi == r).sum()) for r in sorted(set(rgi))))
