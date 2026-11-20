"""Vectorised re-implementation of seqlib.feats for the null controls only. It performs the same elementwise
floating-point operations as the frozen seqlib.feats (log, ndtr, diff, maximum per element), so its output must be
bit-identical; nulls.py checks np.array_equal against the frozen feats on every real scored position before use."""
import numpy as np
from scipy.special import ndtr

import seqlib
import swlib

V, NC = seqlib.V, swlib.NC
CX, BX = seqlib.CX, seqlib.BX
ALL = seqlib.ALL
COL = {k: i for i, k in enumerate(ALL)}
LOGFLOOR = seqlib.LOGFLOOR
CS = np.arange(2, NC + 1)
TOKC = CX - 2                      # row index into the per-click-class (c=2..10) table; -1 for c=1


def _rows(m, sigma, logedges):
    """per click class row: log bin probabilities for log-means m (shape (9,)) -> (9, 5)."""
    cdf = ndtr((logedges[None, :] - m[:, None]) / sigma)
    p = np.diff(np.concatenate([np.zeros((len(m), 1)), cdf, np.ones((len(m), 1))], axis=1), axis=1)
    return np.maximum(np.log(np.maximum(p, 1e-300)), LOGFLOOR)


def _spread(rows):
    out = np.zeros(V)
    ok = TOKC >= 0
    out[ok] = rows[TOKC[ok], BX[ok]]
    return out


def bin_logp_vec(dpred_by_c, sigma, edges):
    m = np.log(np.array([dpred_by_c[c] for c in CS]))
    return _spread(_rows(m, sigma, np.log(edges)))


def feats(H, tb):
    t = H.t
    a = H.a
    tok = H.tok
    edges = H.edges
    nc = np.minimum(a["nClicks"], NC)
    dur = a["Duration"]
    w = a["Whale"]
    F = np.zeros((V, len(ALL)))
    x1 = tok[t - 1]
    c1, b1 = CX[x1], BX[x1]
    F[:, COL["bigram"]] = tb.log_bg[x1]
    F[:, COL["uni"]] = tb.log_uni
    F[:, COL["samec1"]] = (CX == c1)
    F[:, COL["sameb1"]] = (BX == b1)
    F[:, COL["db1"]] = np.abs(BX - b1)
    n1, d1 = a["nClicks"][t - 1], dur[t - 1]
    if n1 >= 2 and d1 > 0:
        ici = d1 / (n1 - 1)
        dpred = {c: ici * (c - 1) for c in range(2, NC + 1)}
        F[:, COL["tempo1_s10"]] = bin_logp_vec(dpred, 0.10, edges)
        F[:, COL["tempo1_s25"]] = bin_logp_vec(dpred, 0.25, edges)
    r = 1
    while r < t and tok[t - 1 - r] == x1:
        r += 1
    rep = (np.arange(V) == x1).astype(float)
    F[:, COL["rep_run"]] = rep * np.log(r)
    if t >= 2:
        nrep = float((tok[1:t] == tok[:t - 1]).sum())
        F[:, COL["rep_rate"]] = rep * np.log((nrep + 1.0) / (t - 1 - nrep + 1.0))
    cnt = np.bincount(tok, minlength=V).astype(float)
    F[:, COL["cache"]] = np.log((cnt + tb.p_uni) / (t + 1.0))
    cntc = np.bincount(nc, minlength=NC + 1)[1:].astype(float)
    F[:, COL["cache_c"]] = np.log((cntc[CX - 1] + tb.p_uni_c[CX - 1]) / (t + 1.0))
    if t >= 2:
        x2 = tok[t - 2]
        F[:, COL["skip"]] = tb.log_sk[x2]
        F[:, COL["same2"]] = (np.arange(V) == x2)
        F[:, COL["samec2"]] = (CX == CX[x2])
        F[:, COL["sameb2"]] = (BX == BX[x2])
        s1 = float(w[t - 1] == w[t - 2])
        F[:, COL["rep_if_same_whale"]] = rep * s1
        F[:, COL["echo2_if_switch"]] = (np.arange(V) == x2) * (1.0 - s1)
    ok = (a["nClicks"] >= 2) & (dur > 0)
    if ok.any():
        k = np.nonzero(ok)[0]
        wts = 0.6 ** (t - 1 - k)
        ici = np.sum(wts * dur[k] / (a["nClicks"][k] - 1)) / wts.sum()
        F[:, COL["tempo_ewma"]] = bin_logp_vec({c: ici * (c - 1) for c in range(2, NC + 1)}, 0.15, edges)
    # samec_dur: for class c, the frozen code evaluates the bin row at dpred = duration of the last earlier coda of
    # class c (the same value for every cc), then keeps the row of class c. Each row depends only on that duration.
    sd = np.zeros(V)
    logedges = np.log(edges)
    for c in range(2, NC + 1):
        kk = np.nonzero((nc == c) & (dur > 0))[0]
        if len(kk):
            row = _rows(np.array([np.log(dur[kk[-1]])]), 0.10, logedges)[0]
            sel = CX == c
            sd[sel] = row[BX[sel]]
    F[:, COL["samec_dur"]] = sd
    return F
