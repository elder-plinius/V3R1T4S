"""One outer fold of the frozen content pipeline: bin edges on training folds, R1, and the log-linear model
in its three input sets (twin, rep, full), each with lambda chosen by inner CV on the training folds."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "evaluator", "code"))
import seqlib  # noqa: E402
import swlib  # noqa: E402

LAMS = (1e-4, 1e-3, 1e-2, 1e-1)


def rows_tensor(streams, folds, edges, tables_for):
    Fs, ys, where = [], [], []
    for r, s in streams.items():
        if s.fold not in folds:
            continue
        tb = tables_for(s.fold)
        tok = swlib.tokens_from(s.a["nClicks"], s.a["Duration"], edges)
        for t in range(2, s.n):
            H = swlib.History.of(s, t, edges)
            Fs.append(seqlib.feats(H, tb))
            ys.append(tok[t])
            where.append((r, t))
    return np.array(Fs), np.array(ys, dtype=int), where


def run_fold(streams, train_folds, test_folds, sets=("twin", "rep", "full"), lams=LAMS, verbose=False):
    train_folds, test_folds = list(train_folds), list(test_folds)
    edges = swlib.bin_edges(np.concatenate([s.a["Duration"] for s in streams.values() if s.fold in train_folds]))
    tok = swlib.stream_tokens(streams, edges)
    # R1
    P1, alpha, r1_losses = swlib.r1_fit(streams, tok, train_folds)
    # count tables: cross-fitted for training rows, all training folds for test rows
    tb_all = seqlib.Tables([tok[r] for r, s in streams.items() if s.fold in train_folds])
    tb_cf = {g: seqlib.Tables([tok[r] for r, s in streams.items() if s.fold in train_folds and s.fold != g])
             for g in train_folds}
    Ftr, ytr, wtr = rows_tensor(streams, train_folds, edges, lambda f: tb_cf[f])
    Fte, yte, wte = rows_tensor(streams, test_folds, edges, lambda f: tb_all)
    gtr = np.array([streams[r].fold for r, _ in wtr])
    out = {"edges": edges, "r1_alpha": alpha, "r1_losses": r1_losses, "where": wte, "y": yte, "probs": {},
           "theta": {}, "lam": {}, "lam_losses": {}, "tb_all": tb_all, "P1": P1}
    out["probs"]["R1"] = np.array([P1[tok[r][t - 1]] for r, t in wte])
    for name in sets:
        idx = [seqlib.ALL.index(k) for k in seqlib.SETS[name]]
        A, B = Ftr[:, :, idx], Fte[:, :, idx]
        ll = []
        for lam in lams:
            tot = 0.0
            for g in train_folds:
                th = seqlib.fit(A[gtr != g], ytr[gtr != g], lam)
                p = seqlib.predict(th, A[gtr == g])
                tot -= np.log2(p[np.arange((gtr == g).sum()), ytr[gtr == g]]).sum()
            ll.append(tot)
        lam = lams[int(np.argmin(ll))]
        th = seqlib.fit(A, ytr, lam)
        out["probs"][name] = seqlib.predict(th, B)
        out["theta"][name], out["lam"][name], out["lam_losses"][name] = th, lam, ll
        if verbose:
            print("  set", name, "lambda", lam, "theta", np.round(th, 3))
    return out


def bits(probs, y):
    return -np.log2(probs[np.arange(len(y)), y])


def predict_one(out, name, stream, t):
    """Recompute the distribution at position t of `stream` from scratch (History slice -> features -> model).
    Used by the leakage self-test; must equal out['probs'][name] at that position."""
    H = swlib.History.of(stream, t, out["edges"])
    if name == "R1":
        return out["P1"][H.tok[t - 1]].copy()
    idx = [seqlib.ALL.index(k) for k in seqlib.SETS[name]]
    F = seqlib.feats(H, out["tb_all"])[None, :, idx]
    return seqlib.predict(out["theta"][name], F)[0]
