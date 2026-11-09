"""Combined season-wise linear model (all three seasons; LIN1 of run 2026-11-07-1434), chosen by glacier-grouped CV on
training glaciers only. Winter (7-month) points: winter set W. Summer (5-month) points: summer set S. Annual (12-month)
points: either route 'direct' (annual set A fitted on annual points) or route 'compose' (W applied to the oct-apr months
+ S applied to the may-sep months, both fitted on their own seasonal points). The route with the lower annual CV RMSE is
used ('direct' in that run). The sets W, S, A are the top lines of subset_search_season.py (CV only).
Usage: python3 -I -B combined.py cv   (prints the route CV; writes nothing)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np, mbdata, score
import cv_linear as L
W = ["one", "solid", "solid_dz"]
S = ["one", "tp_dz", "solid_dz", "pdd", "pdd_dz", "slhf"]
A = ["one", "tp_dz", "pdd", "t", "sw", "fal"]
WINTER_MONTHS = set(range(0, 7))  # oct..apr in mbdata.MONTHS order


def fit_set(d, cols, season, keep=None):
    Ad, y, rgi = L.design(d, cols, season)
    k = np.ones(len(y), bool) if keep is None else keep(rgi)
    return L.fit(Ad[k], y[k])


def monthly(d, coefs):
    P = L.phis(d); out = np.zeros(len(d["gid"]))
    nm = d["n_months"]; win = np.isin(d["month"], list(WINTER_MONTHS))
    lin = lambda cols, b: sum(c * P[n] for c, n in zip(b, cols))
    fw, fs = lin(W, coefs["W"]), lin(S, coefs["S"])
    out[nm == 7] = fw[nm == 7]; out[nm == 5] = fs[nm == 5]
    if coefs["route"] == "direct":
        fa = lin(A, coefs["A"]); out[nm == 12] = fa[nm == 12]
    else:
        a = nm == 12; out[a & win] = fw[a & win]; out[a & ~win] = fs[a & ~win]
    return out


def fit_all(d, keep=None):
    return {"W": fit_set(d, W, 7, keep), "S": fit_set(d, S, 5, keep), "A": fit_set(d, A, 12, keep)}


if __name__ == "__main__":
    assert sys.argv[1] == "cv"
    tr = mbdata.load("train"); fold, fold_of = mbdata.glacier_folds(tr, 6)
    res = {}
    for route in ("direct", "compose"):
        pred = np.zeros(len(tr["gid"]))
        for k in range(6):
            c = fit_all(tr, keep=lambda rgi: np.array([fold_of[r] != k for r in rgi])); c["route"] = route
            m = fold == k; pred[m] = monthly(tr, c)[m]
        res[route] = score.rmse_by_season(tr["gid"], pred, tr["balance"], tr["n_months"])
        print(route, json.dumps(res[route]))
    print("annual route by CV:", min(res, key=lambda r: res[r]["Ba"]))
