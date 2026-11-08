"""Lead 1 (PREREG.md Part C, run 2026-11-07-1740): glacier-balanced blend weights from OOF predictions (training glaciers
only). For season s, balanced RMSE = sqrt(mean over training glaciers g with at least one point of season s of MSE_(g,s)).
Components fixed as BL1's: the plain GBM OOF stage of 200 trees and the season-wise linear OOF. Per season, w_gbm in
0, 0.05, ..., 1 minimising the balanced RMSE (ties: the smaller w, np.argmin order). Prints the table; writes nothing
unless an output path is given.
Usage: python3 -I -B analyze_balanced.py <oof.npz> [optional choice .json output path]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, mbdata

SEAS = {"Ba": 12, "Bw": 7, "Bs": 5}
STAGE = 200
z = np.load(sys.argv[1]); tr = mbdata.load("train")
uid, inv = np.unique(tr["gid"], return_inverse=True)
obs = np.zeros(len(uid)); obs[inv] = tr["balance"]; nm = np.zeros(len(uid), int); nm[inv] = tr["n_months"]
rgi = np.empty(len(uid), dtype=object); rgi[inv] = tr["rgi"]
g = z["plain"][STAGE // 50 - 1]; l = z["lin"]
Sg, Sl = np.bincount(inv, weights=g), np.bincount(inv, weights=l)


def bal(S, s):
    k = nm == SEAS[s]; e = (S[k] - obs[k]) ** 2; r = rgi[k]
    gl = sorted(set(r))
    return float(np.sqrt(np.mean([e[r == x].mean() for x in gl]))), len(gl)


def pooled(S, s):
    k = nm == SEAS[s]; return float(np.sqrt(np.mean((S[k] - obs[k]) ** 2)))


ws = np.round(np.arange(0, 1.0001, 0.05), 2); choice = {}
print("cfg", str(z["cfg"]), "stage", STAGE)
for s in SEAS:
    sc = [bal(w * Sg + (1 - w) * Sl, s)[0] for w in ws]
    i = int(np.argmin(sc)); choice[s] = float(ws[i])
    print("%s glaciers %d  balanced: lin %.4f gbm %.4f best w_gbm %.2f -> %.4f | pooled at that w %.4f | pooled-rule w (BL1) for reference" % (
        s, bal(Sl, s)[1], sc[0], sc[-1], ws[i], sc[i], pooled(ws[i] * Sg + (1 - ws[i]) * Sl, s)))
    print("   curve", " ".join("%.2f:%.4f" % (w, v) for w, v in zip(ws, sc)))
m = np.mean([bal(choice[s] * Sg + (1 - choice[s]) * Sl, s)[0] for s in SEAS])
print("choice", json.dumps({"w_gbm": choice, "stage": STAGE, "balanced_cv_mean": m}))
if len(sys.argv) > 2:
    json.dump({"w_gbm": choice, "stage": STAGE, "balanced_cv_mean": m}, open(sys.argv[2], "w"), indent=1)
