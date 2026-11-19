"""M1 candidate test read for p2 on CHEMBL244_Ki (PREREG.v2 §5).

Trains the FROZEN M1 recipe (members + non-negative ridge weights, alpha=1, fit on ALL train
OOF predictions as in the greedy step — weights recomputed at full-train member level) and
reads the test set ONCE. Verdict per PREREG.v2 thresholds 1-2 vs the saved baseline B bars.
"""
import json
import os
import sys
import time

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mace_common import featurize, load_dataset  # noqa: E402

# member reconstruction map: name -> (kind, feat, params)  (must mirror sweep_244.py exactly)
import importlib.util as _ilu

t0 = time.time()
ds = load_dataset("CHEMBL244_Ki")
tr_idx = np.where(ds["train"])[0]
te_idx = np.where(ds["test"])[0]
mols_tr = [ds["mols"][i] for i in tr_idx]
mols_te = [ds["mols"][i] for i in te_idx]
y_tr, y_te = ds["y"][tr_idx], ds["y"][te_idx]
c_te = ds["cliff"][te_idx] == 1

sel = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                  "output", "M1_selection.json")))
member_names = sel["members"]

FEATS = ["ECFP4", "ECFP6", "FCFP4", "MACCS", "RDKIT2D"]
Xs = {f: featurize(mols_tr, f) for f in FEATS}
from mace_common import ecfp_count
Xs["ECFP4CNT"] = ecfp_count(mols_tr, 2, 2048)
Xs["ECFP6CNT"] = ecfp_count(mols_tr, 3, 2048)
Xs_te = {f: featurize(mols_te, f) for f in FEATS}
Xs_te["ECFP4CNT"] = ecfp_count(mols_te, 2, 2048)
Xs_te["ECFP6CNT"] = ecfp_count(mols_te, 3, 2048)
print("feats %.0fs" % (time.time() - t0), flush=True)


def fit_member(name):
    """Fit member on ALL 2476 train rows; return test predictions."""
    from sklearn.svm import SVR
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics.pairwise import cosine_similarity
    if name == "B_SVR_ECFP4":
        m = SVR(C=10, epsilon=0.1, gamma=0.01).fit(Xs["ECFP4"], y_tr)
        return m.predict(Xs_te["ECFP4"])
    if name.startswith("SVR_"):
        rest = name[4:]
        f, cfg = rest.rsplit("_C", 1)
        C, g = cfg.split("_g")
        C, g = int(C), float(g)
        m = SVR(C=C, epsilon=0.1, gamma=g).fit(Xs[f], y_tr)
        return m.predict(Xs_te[f])
    if name == "SVR_MACCS_C10":
        m = SVR(C=10, epsilon=0.1, gamma=0.01).fit(Xs["MACCS"], y_tr)
        return m.predict(Xs_te["MACCS"])
    if name == "SVR_RDKIT2D":
        sc = StandardScaler().fit(Xs["RDKIT2D"])
        m = SVR(C=10, epsilon=0.1, gamma=0.01).fit(sc.transform(Xs["RDKIT2D"]), y_tr)
        return m.predict(sc.transform(Xs_te["RDKIT2D"]))
    if name.startswith("RF_"):
        f = name[3:]
        m = RandomForestRegressor(n_estimators=250, random_state=0, n_jobs=-1).fit(Xs[f], y_tr)
        return m.predict(Xs_te[f])
    if name.startswith("RFA_"):
        f = name[4:]
        ps = []
        for s in range(5):
            m = RandomForestRegressor(n_estimators=250, random_state=s, n_jobs=-1).fit(Xs[f], y_tr)
            ps.append(m.predict(Xs_te[f]))
        return np.mean(ps, axis=0)
    if name.startswith("LGBM_"):
        import lightgbm as lgb
        f = name[5:]
        m = lgb.LGBMRegressor(n_estimators=3000, learning_rate=0.03, num_leaves=31,
                              subsample=0.8, colsample_bytree=0.8, random_state=0, verbose=-1)
        m.fit(Xs[f], y_tr)
        return m.predict(Xs_te[f])
    if name.startswith("KNN"):
        k = int(name[3:].split("_")[0])
        m = KNeighborsRegressor(n_neighbors=k, metric="rogerstanimoto", weights="distance").fit(Xs["ECFP4"], y_tr)
        return m.predict(Xs_te["ECFP4"])
    if name == "SM_SVR_shrink":
        from sklearn.svm import SVR as SVR2
        m = SVR2(C=10, epsilon=0.1, gamma=0.01).fit(Xs["ECFP6"], y_tr)
        base = m.predict(Xs_te["ECFP6"])
        S = cosine_similarity(Xs_te["ECFP4"], Xs["ECFP4"])
        preds = []
        for i in range(len(base)):
            order = np.argsort(-S[i])[:5]
            knn_mean = np.mean(y_tr[order])
            spread = np.std(y_tr[order])
            w = spread / (spread + 0.6)
            preds.append((1 - w) * base[i] + w * ((base[i] + knn_mean) / 2))
        return np.array(preds)
    if name == "SM_MMP_lite":
        S = cosine_similarity(Xs_te["ECFP4"], Xs["ECFP4"])
        preds = []
        for i in range(len(y_te)):
            order = np.argsort(-S[i])[:3]
            b = y_tr[order[0]]
            delta = np.mean([y_tr[order[t]] - y_tr[order[t - 1]] for t in range(1, 3)])
            preds.append(0.5 * b + 0.5 * (b + delta * 0.3))
        return np.array(preds)
    raise ValueError(name)


P = {}
for n in member_names:
    P[n] = fit_member(n)
    print("member %s fit (%.0fs)" % (n, time.time() - t0), flush=True)

# combiner: non-negative ridge alpha=1.0 on the TRAIN-member matrix (train labels only).
# We need each member's predictions on TRAIN rows to fit the combiner: use each member's
# OOF vector from the sweep (train-only predictions of the same recipe family).
z = np.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output",
                         "sweep244_members.npz"))
oof = {str(k): z["M"][:, i] for i, k in enumerate(z["keys"])}
Ptr = np.column_stack([oof[n] for n in member_names])
w = Ridge(alpha=1.0, positive=True).fit(Ptr, y_tr)
Pte = np.column_stack([P[n] for n in member_names])
y_hat = w.predict(Pte)

mse_all = mean_squared_error(y_te, y_hat)
mse_cliff = mean_squared_error(y_te[c_te], y_hat[c_te])
mse_non = mean_squared_error(y_te[~c_te], y_hat[~c_te])
B = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                                "baseline", "baseline_B_chembl244.json")))
verdict = {
    "mse_all": float(mse_all), "mse_cliff": float(mse_cliff), "mse_noncliff": float(mse_non),
    "B_mse_all": B["mse"], "B_mse_cliff": B["mse_cliff"], "B_mse_noncliff": B["mse_noncliff"],
    "cliff_strictly_lower": bool(mse_cliff < B["mse_cliff"]),
    "noncliff_not_worse": bool(mse_non <= B["mse_noncliff"]),
    "members": member_names,
    "weights": {n: float(c) for n, c in zip(member_names, w.coef_)},
    "seconds": time.time() - t0,
}
verdict["P2_THRESHOLDS_MET"] = bool(verdict["cliff_strictly_lower"] and verdict["noncliff_not_worse"])
print(json.dumps(verdict, indent=1))
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
json.dump(verdict, open(os.path.join(OUT, "M1_read_result.json"), "w"), indent=1)
np.save(os.path.join(OUT, "M1_test_predictions.npy"), y_hat)
print("WROTE output/M1_read_result.json")
