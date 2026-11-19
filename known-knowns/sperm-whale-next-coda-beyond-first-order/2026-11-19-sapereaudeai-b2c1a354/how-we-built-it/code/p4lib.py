"""p4 turn-taking model: P(whale[t] == whale[t-1] | earlier codas of the stream).

feats(H) reads only the History view H (rows [:t]); it never sees row t or later.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "evaluator", "code"))
import swlib  # noqa: E402

FEATURE_SETS = {
    # name -> list of feature keys
    "state": ["s1"],
    "pattern": ["s1", "s2", "s2_missing", "aba"],
    "adaptive": ["s1", "s2", "s2_missing", "aba", "loc_rate", "log_ntrans", "log_nd", "log_run", "share_prev",
                 "prev_is_mode", "s1_x_loc_rate"],
    "full": ["s1", "s2", "s2_missing", "aba", "loc_rate", "log_ntrans", "log_nd", "log_run", "share_prev",
             "prev_is_mode", "s1_x_loc_rate", "log_gap1", "overlap1", "end_gap1", "s1_x_log_gap1",
             "log_since_other", "since_other_missing", "prev_c", "prev_dur", "log_gap2", "overlap2"],
}


def _logit(p):
    return np.log(p / (1 - p))


def feats(H):
    t = H.t
    w = H.a["Whale"]
    ts = H.a["TsTo"]
    d = H.a["Duration"]
    nc = H.a["nClicks"]
    assert t >= 2 and len(w) == t
    f = {}
    f["s1"] = float(w[t - 1] == w[t - 2])
    if t >= 3:
        f["s2"] = float(w[t - 2] == w[t - 3])
        f["s2_missing"] = 0.0
        f["aba"] = float(w[t - 1] == w[t - 3])
    else:
        f["s2"], f["s2_missing"], f["aba"] = 0.0, 1.0, 0.0
    y = (w[1:] == w[:-1]).astype(float)          # transitions among earlier codas, length t-1
    k, n = y.sum(), len(y)
    f["loc_rate"] = _logit((k + 1.0) / (n + 2.0))
    f["log_ntrans"] = np.log(n + 1.0)
    f["log_nd"] = np.log(len(np.unique(w)))
    r = 1
    while r < t and w[t - 1 - r] == w[t - 1]:
        r += 1
    f["log_run"] = np.log(r)
    f["share_prev"] = float((w == w[t - 1]).mean())
    vals, cnts = np.unique(w, return_counts=True)
    f["prev_is_mode"] = float(w[t - 1] == vals[np.argmax(cnts)])
    f["s1_x_loc_rate"] = f["s1"] * f["loc_rate"]
    g1 = ts[t - 1] - ts[t - 2]
    f["log_gap1"] = np.log(max(g1, 1e-3))
    f["overlap1"] = float(ts[t - 1] < ts[t - 2] + d[t - 2])
    f["end_gap1"] = float(np.clip(ts[t - 1] - (ts[t - 2] + d[t - 2]), -2.0, 10.0))
    f["s1_x_log_gap1"] = f["s1"] * f["log_gap1"]
    other = np.nonzero(w != w[t - 1])[0]
    if len(other):
        f["log_since_other"] = np.log(max(ts[t - 1] - ts[other[-1]], 1e-3))
        f["since_other_missing"] = 0.0
    else:
        f["log_since_other"], f["since_other_missing"] = 0.0, 1.0
    f["prev_c"] = min(nc[t - 1], 10) / 10.0
    f["prev_dur"] = float(d[t - 1])
    if t >= 3:
        g2 = ts[t - 2] - ts[t - 3]
        f["log_gap2"] = np.log(max(g2, 1e-3))
        f["overlap2"] = float(ts[t - 2] < ts[t - 3] + d[t - 3])
    else:
        f["log_gap2"], f["overlap2"] = 0.0, 0.0
    return f


def target(stream, t):
    return int(stream.a["Whale"][t] == stream.a["Whale"][t - 1])


def design(streams, folds, keys, positions="scored"):
    """Rows for all positions t >= 2 of streams in `folds`. Returns X, y, rec ids, (rec, t) list."""
    X, y, rid, where = [], [], [], []
    for r, s in streams.items():
        if s.fold not in folds:
            continue
        for t in range(2, s.n):
            f = feats(_hist(s, t))
            X.append([f[k] for k in keys])
            y.append(target(s, t))
            rid.append(r)
            where.append((r, t))
    return np.array(X, dtype=float), np.array(y, dtype=int), np.array(rid), where


class _H:
    __slots__ = ("t", "a")


def _hist(s, t):
    """History view without tokens (p4 needs no duration bins)."""
    h = _H()
    h.t = t
    h.a = {k: v[:t].copy() for k, v in s.a.items()}
    return h


CS = (0.01, 0.1, 1.0, 10.0)


def _lr(C):
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    return make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=5000))


def _bits(y, p):
    return -(y * np.log2(p) + (1 - y) * np.log2(1 - p))


def fit_fold(streams, train_folds, test_folds, keys, Cs=CS):
    """Frozen p4 pipeline for one outer fold: reference (first-order same/switch chain, alpha by inner CV) and
    logistic regression on `keys` (C by inner leave-one-training-fold-out CV, total log-loss)."""
    train_folds, test_folds = list(train_folds), list(test_folds)
    Xtr, ytr, rtr, wtr = design(streams, train_folds, keys)
    gtr = np.array([streams[r].fold for r in rtr])
    losses = []
    for C in Cs:
        tot = 0.0
        for g in train_folds:
            m = _lr(C).fit(Xtr[gtr != g], ytr[gtr != g])
            tot += _bits(ytr[gtr == g], m.predict_proba(Xtr[gtr == g])[:, 1]).sum()
        losses.append(tot)
    C = Cs[int(np.argmin(losses))]
    model = _lr(C).fit(Xtr, ytr)
    Xte, yte, rte, wte = design(streams, test_folds, keys)
    P, alpha, ref_losses = swlib.switch_ref_fit(streams, train_folds)
    s1 = np.array([int(streams[r].a["Whale"][t - 1] == streams[r].a["Whale"][t - 2]) for r, t in wte])
    return {"model": model, "keys": keys, "C": C, "C_losses": losses, "P_ref": P, "ref_alpha": alpha,
            "ref_losses": ref_losses, "where": wte, "y": yte, "rec": rte,
            "p": model.predict_proba(Xte)[:, 1], "p_ref": P[s1, 1]}


def predict_one(fit, stream, t):
    """Recompute P(same) at position t from scratch; used by the leakage self-test."""
    f = feats(_hist(stream, t))
    p = fit["model"].predict_proba(np.array([[f[k] for k in fit["keys"]]], dtype=float))[0, 1]
    w = stream.a["Whale"][:t]
    p_ref = fit["P_ref"][int(w[t - 1] == w[t - 2]), 1]
    return p, p_ref
