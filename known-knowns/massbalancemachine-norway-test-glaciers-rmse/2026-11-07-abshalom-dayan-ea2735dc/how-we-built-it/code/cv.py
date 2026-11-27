"""Glacier-grouped 6-fold CV on the 18 training glaciers for GBM configs (PREREG.md). Reads only the training CSV.

Usage: python3 -I -B cv.py <out.jsonl> <config-json-list>
Each config: {"fs": "F0|F1|F2|F3", "depth":..,"lr":..,"lam":..,"min_child":..,"subsample":..,"colsample":..,"n_max":..,"seed":..}
Writes one JSON line per config with the CV score (mean of 3 seasonal pooled OOF RMSEs) at every 50 trees.
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import mbdata, score, gbm, feats

tr = mbdata.load("train")
fold, fold_of = mbdata.glacier_folds(tr, 6)
STEP = 50


def cv_one(c):
    X, _ = feats.build(tr, c["fs"])
    edges = gbm.make_bins(X)
    nstage = c["n_max"] // STEP
    oof = np.zeros((nstage, len(X)))
    for k in range(6):
        te = fold == k
        m = gbm.GBM(n_trees=c["n_max"], lr=c["lr"], depth=c["depth"], lam=c["lam"], min_child=c["min_child"],
                    subsample=c["subsample"], colsample=c["colsample"], seed=c["seed"],
                    monotone=c.get("monotone")).fit(X[~te], tr["gid"][~te], tr["balance"][~te], edges=edges)
        B = gbm.apply_bins(X[te], edges); acc = np.full(te.sum(), m.base)
        for t, tree in enumerate(m.trees):
            acc += m._predict_tree(tree, B)
            if (t + 1) % STEP == 0:
                oof[(t + 1) // STEP - 1, te] = acc
    res = []
    for s in range(nstage):
        r = score.rmse_by_season(tr["gid"], oof[s], tr["balance"], tr["n_months"])
        res.append({"n_trees": (s + 1) * STEP, "Ba": r["Ba"], "Bw": r["Bw"], "Bs": r["Bs"],
                    "cv": (r["Ba"] + r["Bw"] + r["Bs"]) / 3})
    return res


if __name__ == "__main__":
    out = sys.argv[1]; cfgs = json.loads(open(sys.argv[2]).read()) if os.path.exists(sys.argv[2]) else json.loads(sys.argv[2])
    for c in cfgs:
        t0 = time.time(); res = cv_one(c)
        best = min(res, key=lambda r: r["cv"])
        with open(out, "a") as f:
            f.write(json.dumps({"cfg": c, "best": best, "curve": res, "sec": round(time.time() - t0, 1)}) + "\n")
        print(json.dumps({"cfg": c, "best": best, "sec": round(time.time() - t0, 1)}), flush=True)
