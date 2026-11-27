"""Lens ensemble: glacier-grouped 6-fold OOF predictions on the 18 training glaciers for
 (a) the season-wise linear model (sets of attempts/linear-ti/code/combined.py, route direct),
 (b) a GBM (plain), and (c) a residual hybrid GBM started from the linear prediction (init offset), with staged
 OOF every 50 trees. Reads only the training CSV. Writes only <out.npz>.
Usage: python3 -I -B oof.py <out.npz> '<gbm config json>'"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np, mbdata, gbm, feats
import combined as C

STEP = 50


def gbm_from(c):
    return gbm.GBM(n_trees=c["n_max"], lr=c["lr"], depth=c["depth"], lam=c["lam"], min_child=c["min_child"],
                   subsample=c["subsample"], colsample=c.get("colsample", 1), seed=c["seed"], monotone=c.get("monotone"))


def staged(m, X, init):
    B = gbm.apply_bins(X, m.edges); acc = m.base + init.copy(); out = []
    for t, tree in enumerate(m.trees):
        acc += m._predict_tree(tree, B)
        if (t + 1) % STEP == 0:
            out.append(acc.copy())
    return np.array(out)


if __name__ == "__main__":
    out, c = sys.argv[1], json.loads(sys.argv[2])
    tr = mbdata.load("train"); fold, fold_of = mbdata.glacier_folds(tr, 6)
    X, _ = feats.build(tr, c["fs"]); edges = gbm.make_bins(X)
    n = len(X); ns = c["n_max"] // STEP
    lin = np.zeros(n); plain = np.zeros((ns, n)); hyb = np.zeros((ns, n))
    for k in range(6):
        te = fold == k
        coefs = C.fit_all(tr, keep=lambda rgi: np.array([fold_of[r] != k for r in rgi])); coefs["route"] = "direct"
        lm = C.monthly(tr, coefs)
        lin[te] = lm[te]
        sub = lambda a: a[~te]
        m1 = gbm_from(c).fit(X[~te], tr["gid"][~te], tr["balance"][~te], edges=edges)
        plain[:, te] = staged(m1, X[te], np.zeros(te.sum()))
        m2 = gbm_from(c).fit(X[~te], tr["gid"][~te], tr["balance"][~te], edges=edges, init=lm[~te])
        hyb[:, te] = staged(m2, X[te], lm[te])
        print("fold", k, "done", flush=True)
    np.savez_compressed(out, lin=lin, plain=plain, hyb=hyb, cfg=json.dumps(c))
