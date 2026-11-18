"""PREREG.v2 OOF sweep for CHEMBL244_Ki (train-only, 5-fold seed 20261118).

Pool: SVR configs (incl. the repo baseline C=10 gamma=0.01, FORCED member), RF + replica RF,
LGBM, KNN, SVR_SHRINK, MMP_LITE. NCD excluded BEFORE any OOF result (O(n^2) compression cost on
2476 rows; declared in NOTES).
Selection: greedy forward on OOF CLIFF-MSE with constraint OOF non-cliff MSE <= the baseline
member's OOF non-cliff MSE; combiner frozen to non-negative ridge (inner-CV alpha).
Saves all member OOF vectors to sweep244_members.npz.
"""
import json
import os
import sys
import time

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mace_common import ecfp_count, featurize, load_dataset  # noqa: E402

t0 = time.time()
ds = load_dataset("CHEMBL244_Ki")
tr_idx = np.where(ds["train"])[0]
mols_tr = [ds["mols"][i] for i in tr_idx]
y_tr = ds["y"][tr_idx]
c_tr = ds["cliff"][tr_idx] == 1

FEATS = ["ECFP4", "ECFP6", "FCFP4", "MACCS", "RDKIT2D"]
Xs = {f: featurize(mols_tr, f) for f in FEATS}
Xs["ECFP4CNT"] = ecfp_count(mols_tr, 2, 2048)
Xs["ECFP6CNT"] = ecfp_count(mols_tr, 3, 2048)
print("feats %.0fs" % (time.time() - t0), flush=True)

folds = list(KFold(n_splits=5, shuffle=True, random_state=20261118).split(Xs["ECFP4"], y_tr))


def oof(fn):
    o = np.zeros_like(y_tr, dtype=float)
    for tr, va in folds:
        o[va] = fn(tr, va)
    return o


members = {}


def reg(name, fn):
    o = oof(fn)
    members[name] = o
    print("%-26s OOF all %.4f cliff %.4f noncliff %.4f (%.0fs)" % (
        name, mean_squared_error(y_tr, o), mean_squared_error(y_tr[c_tr], o[c_tr]),
        mean_squared_error(y_tr[~c_tr], o[~c_tr]), time.time() - t0), flush=True)


# forced baseline member (repo config SVM/ECFP)
reg("B_SVR_ECFP4", lambda tr, va: SVR(C=10, epsilon=0.1, gamma=0.01)
    .fit(Xs["ECFP4"][tr], y_tr[tr]).predict(Xs["ECFP4"][va]))

for f in ["ECFP4", "ECFP6", "FCFP4", "ECFP4CNT", "ECFP6CNT"]:
    for C, g in [(30, 0.01), (100, 0.01), (10, 0.003), (30, 0.003)]:
        reg(f"SVR_{f}_C{C}_g{g}", lambda tr, va, f=f, C=C, g=g: SVR(C=C, epsilon=0.1, gamma=g)
            .fit(Xs[f][tr], y_tr[tr]).predict(Xs[f][va]))
reg("SVR_MACCS_C10", lambda tr, va: SVR(C=10, epsilon=0.1, gamma=0.01)
    .fit(Xs["MACCS"][tr], y_tr[tr]).predict(Xs["MACCS"][va]))


def svr_rdkit(tr, va):
    sc = StandardScaler().fit(Xs["RDKIT2D"][tr])
    m = SVR(C=10, epsilon=0.1, gamma=0.01)
    m.fit(sc.transform(Xs["RDKIT2D"][tr]), y_tr[tr])
    return m.predict(sc.transform(Xs["RDKIT2D"][va]))


reg("SVR_RDKIT2D", svr_rdkit)

# RF single + replica
for f in ["ECFP4", "ECFP6", "FCFP4", "ECFP4CNT", "MACCS", "RDKIT2D"]:
    reg(f"RF_{f}", lambda tr, va, f=f: RandomForestRegressor(n_estimators=250, random_state=0, n_jobs=-1)
        .fit(Xs[f][tr], y_tr[tr]).predict(Xs[f][va]))


def rfa(f):
    def fn(tr, va):
        ps = []
        for s in range(5):
            m = RandomForestRegressor(n_estimators=250, random_state=s, n_jobs=-1)
            m.fit(Xs[f][tr], y_tr[tr])
            ps.append(m.predict(Xs[f][va]))
        return np.mean(ps, axis=0)
    return fn


for f in ["ECFP4", "ECFP6", "FCFP4", "ECFP4CNT", "RDKIT2D"]:
    reg(f"RFA_{f}", rfa(f))


def lgbm1(f):
    def fn(tr, va):
        import lightgbm as lgb
        m = lgb.LGBMRegressor(n_estimators=3000, learning_rate=0.03, num_leaves=31,
                              subsample=0.8, colsample_bytree=0.8, random_state=0, verbose=-1)
        m.fit(Xs[f][tr], y_tr[tr])
        return m.predict(Xs[f][va])
    return fn


for f in ["ECFP4", "ECFP4CNT", "FCFP4"]:
    reg(f"LGBM_{f}", lgbm1(f))

# KNN
for k in [5, 10, 20]:
    reg(f"KNN{k}_ECFP4", lambda tr, va, k=k: KNeighborsRegressor(n_neighbors=k, metric="rogerstanimoto",
                                                                weights="distance")
        .fit(Xs["ECFP4"][tr], y_tr[tr]).predict(Xs["ECFP4"][va]))

# SVR_SHRINK: SVR/ECFP6 + kNN-spread shrink (train-fold cosine on ECFP4)
def svr_shrink(tr, va, k=5):
    m = SVR(C=10, epsilon=0.1, gamma=0.01)
    m.fit(Xs["ECFP6"][tr], y_tr[tr])
    base = m.predict(Xs["ECFP6"][va])
    S = cosine_similarity(Xs["ECFP4"][va], Xs["ECFP4"][tr])
    preds = []
    for i in range(len(va)):
        order = np.argsort(-S[i])[:k]
        knn_mean = np.mean(y_tr[tr][order])
        spread = np.std(y_tr[tr][order])
        w = spread / (spread + 0.6)
        preds.append((1 - w) * base[i] + w * ((base[i] + knn_mean) / 2))
    return np.array(preds)


reg("SM_SVR_shrink", svr_shrink)


# MMP_LITE
def mmp(tr, va, k=3, lam=0.5):
    S = cosine_similarity(Xs["ECFP4"][va], Xs["ECFP4"][tr])
    preds = []
    for i in range(len(va)):
        order = np.argsort(-S[i])[:k]
        base = y_tr[tr][order[0]]
        delta = np.mean([y_tr[tr][order[t]] - y_tr[tr][order[t - 1]] for t in range(1, k)]) if k > 1 else 0.0
        preds.append((1 - lam) * base + lam * (base + delta * 0.3))
    return np.array(preds)


reg("SM_MMP_lite", mmp)

np.savez(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output",
                      "sweep244_members.npz"),
         M=np.column_stack([members[k] for k in members]), y=y_tr, cliff=c_tr,
         keys=np.array(list(members.keys())))
print("saved members npz %.0fs" % (time.time() - t0), flush=True)

# ---- selection: greedy forward on OOF cliff-MSE, constrained non-cliff ----
B_non = mean_squared_error(y_tr[~c_tr], members["B_SVR_ECFP4"][~c_tr])
B_cliff = mean_squared_error(y_tr[c_tr], members["B_SVR_ECFP4"][c_tr])
print("B OOF: cliff %.4f noncliff %.4f" % (B_cliff, B_non))


def stats(pred):
    return (mean_squared_error(y_tr[c_tr], pred[c_tr]), mean_squared_error(y_tr[~c_tr], pred[~c_tr]))


cur = ["B_SVR_ECFP4"]
cur_pred = members["B_SVR_ECFP4"].copy()
cur_cliff, cur_non = stats(cur_pred)
improved = True
while improved:
    improved = False
    best_add = None
    for k in members:
        if k in cur:
            continue
        # non-negative ridge blend of current set + candidate, alpha=1 (frozen combiner family)
        P = np.column_stack([members[j] for j in cur] + [members[k]])
        w = Ridge(alpha=1.0, positive=True).fit(P, y_tr)
        p = w.predict(P)
        cl, no = stats(p)
        if cl < cur_cliff - 1e-5 and no <= B_non + 1e-9:
            if best_add is None or cl < best_add[1]:
                best_add = (k, cl, no)
    if best_add:
        k, cl, no = best_add
        P = np.column_stack([members[j] for j in cur] + [members[k]])
        w = Ridge(alpha=1.0, positive=True).fit(P, y_tr)
        cur_pred = w.predict(P)
        cur_cliff, cur_non = stats(cur_pred)
        cur = cur + [k]
        improved = True
        print("ADD %-26s -> OOF cliff %.4f noncliff %.4f  (%d members)" % (k, cur_cliff, cur_non, len(cur)), flush=True)

print("FROZEN CANDIDATE M1 members:", cur)
print("M1 OOF: cliff %.4f (B %.4f) noncliff %.4f (B %.4f) all %.4f" % (
    cur_cliff, B_cliff, cur_non, B_non, mean_squared_error(y_tr, cur_pred)))
json.dump({"members": cur, "oof_cliff": float(cur_cliff), "oof_noncliff": float(cur_non),
           "oof_all": float(mean_squared_error(y_tr, cur_pred)),
           "B_oof_cliff": float(B_cliff), "B_oof_noncliff": float(B_non)},
          open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output",
                            "M1_selection.json"), "w"), indent=1)
np.save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output",
                     "M1_oof_pred.npy"), cur_pred)
print("DONE %.0fs" % (time.time() - t0))
