"""Lens linear-ti (partial win p2): small linear temperature-index-style models for winter balance, at most 20 fitted
parameters. A monthly linear model f = sum_k b_k phi_k summed over the season's months is a linear regression of the
point balance on the per-point sums of phi_k. Candidate sets are compared by glacier-grouped 6-fold CV on the 18
training glaciers only (PREREG.md). Reads only the training CSV.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
import numpy as np
import mbdata, feats

F = feats.F


def phis(d):
    X = d["X"]
    dz = X[:, F["altitude_diff"]]
    t = X[:, F["t2m"]] - 273.15 + 0.0065 * dz
    tp = X[:, F["tp"]] * 1000.0
    solid = tp * (t < 1.0)
    pdd = np.maximum(t, 0.0)
    sw = X[:, F["ssrd"]] * (1 - X[:, F["fal"]]) / 1e6
    P = {"one": np.ones(len(X)), "tp": tp, "tp_dz": tp * dz / 1000, "solid": solid, "solid_dz": solid * dz / 1000,
         "pdd": pdd, "pdd_dz": pdd * dz / 1000, "t": t, "sw": sw, "fal": X[:, F["fal"]],
         "slhf": X[:, F["slhf"]] / 1e6, "sshf": X[:, F["sshf"]] / 1e6, "str": X[:, F["str"]] / 1e6,
         "svf_tp": X[:, F["skyview_factor"]] * tp, "slope_tp": X[:, F["slope"]] * tp}
    return P


SETS = {
    "S1": ["one", "tp"],
    "S2": ["one", "tp", "tp_dz"],
    "S3": ["one", "solid", "solid_dz", "pdd"],
    "S4": ["one", "tp", "tp_dz", "solid", "pdd", "t"],
    "S5": ["one", "tp", "tp_dz", "solid", "solid_dz", "pdd", "pdd_dz", "t", "sw"],
    "S6": ["one", "tp", "tp_dz", "solid", "solid_dz", "pdd", "pdd_dz", "t", "sw", "fal", "slhf", "sshf", "str"],
    "S7": ["one", "tp", "tp_dz", "solid", "solid_dz", "pdd", "t", "svf_tp", "slope_tp"],
}


def design(d, names, season=7):
    P = phis(d)
    rows = d["n_months"] == season
    uid, inv = np.unique(d["gid"][rows], return_inverse=True)
    A = np.column_stack([np.bincount(inv, weights=P[n][rows]) for n in names])
    y = np.bincount(inv, weights=d["balance"][rows]) / np.bincount(inv)
    rgi = np.empty(len(uid), dtype=object); rgi[inv] = d["rgi"][rows]
    return A, y, rgi.astype(str)


def fit(A, y, ridge=0.0):
    k = A.shape[1]
    return np.linalg.solve(A.T @ A + ridge * np.eye(k), A.T @ y)


if __name__ == "__main__":
    tr = mbdata.load("train")
    _, fold_of = mbdata.glacier_folds(tr, 6)
    out = []
    for name, cols in SETS.items():
        assert len(cols) <= 20
        A, y, rgi = design(tr, cols)
        fo = np.array([fold_of[r] for r in rgi]); pred = np.zeros(len(y))
        for k in range(6):
            te = fo == k
            pred[te] = A[te] @ fit(A[~te], y[~te])
        r = float(np.sqrt(np.mean((pred - y) ** 2)))
        out.append({"set": name, "n_params": len(cols), "cv_Bw": r})
        print(json.dumps(out[-1]))
    best = min(out, key=lambda o: o["cv_Bw"])
    print("primary by CV:", json.dumps(best))
