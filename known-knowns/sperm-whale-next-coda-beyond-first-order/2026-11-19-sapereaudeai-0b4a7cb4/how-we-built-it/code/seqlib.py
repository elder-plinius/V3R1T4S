"""Next-coda token model for the dialogues target: a log-linear tilt over the 50 tokens,
    P(x | history) = softmax_x( sum_k theta_k * F_k(x, history) ),
fit by L2-penalised maximum likelihood (L-BFGS). Probabilities are strictly positive and sum to 1 by
construction. Feature groups:
  TWIN  - previous coda only (token, click class, duration bin, exact duration/tempo of coda t-1) plus
          training-fold unigram; this is the "same model retrained with its input cut to the single previous coda"
  REP   - repetition persistence (run length of the previous token, stream-local repeat rate); TWIN+REP is the
          repetition-aware comparator named in the bank's pitfall
  HIGH  - everything else from earlier codas: stream cache, skip-bigram, coda t-2 identities, EWMA tempo,
          last same-click-class duration, whale-switch-aware echoes
feats(H, tables) reads only the History view H (rows [:t]) and training-fold count tables.
"""
import os
import sys

import numpy as np
from scipy.optimize import minimize
from scipy.special import log_softmax
from scipy.stats import norm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "evaluator", "code"))
import swlib  # noqa: E402

V, NB = swlib.V, swlib.NB
CX = np.arange(V) // NB + 1          # click class of each token
BX = np.arange(V) % NB               # duration bin of each token
TWIN = ["bigram", "uni", "samec1", "sameb1", "db1", "tempo1_s10", "tempo1_s25"]
REP = ["rep_run", "rep_rate"]
HIGH = ["cache", "cache_c", "skip", "same2", "samec2", "sameb2", "tempo_ewma", "samec_dur",
        "rep_if_same_whale", "echo2_if_switch"]
ALL = TWIN + REP + HIGH
LOCAL = TWIN + REP + ["cache", "cache_c"]   # diagnostic: previous coda + order-free bag of the stream so far
SETS = {"twin": TWIN, "rep": TWIN + REP, "local": LOCAL, "full": ALL}
LOGFLOOR = np.log(1e-12)
BG_ALPHA = 0.3


class Tables:
    """Count tables from a set of training streams (token sequences)."""

    def __init__(self, tok_seqs):
        uni = np.zeros(V)
        bg = np.zeros((V, V))
        sk = np.zeros((V, V))
        for x in tok_seqs:
            np.add.at(uni, x, 1)
            if len(x) >= 2:
                np.add.at(bg, (x[:-1], x[1:]), 1)
            if len(x) >= 3:
                np.add.at(sk, (x[:-2], x[2:]), 1)
        self.log_uni = np.log((uni + 0.5) / (uni.sum() + 0.5 * V))
        self.p_uni = np.exp(self.log_uni)
        pc = np.array([self.p_uni[CX == c].sum() for c in range(1, swlib.NC + 1)])
        self.p_uni_c = pc / pc.sum()
        self.log_bg = np.log((bg + BG_ALPHA) / (bg.sum(1, keepdims=True) + BG_ALPHA * V))
        self.log_sk = np.log((sk + BG_ALPHA) / (sk.sum(1, keepdims=True) + BG_ALPHA * V))


def _bin_logp(dpred, sigma, edges):
    """log P(duration bin | lognormal(log dpred, sigma)) for each token (by its click class), floored."""
    out = np.zeros(V)
    for c in range(2, swlib.NC + 1):
        m = np.log(dpred[c])
        cdf = norm.cdf((np.log(edges) - m) / sigma)
        p = np.diff(np.concatenate([[0.0], cdf, [1.0]]))
        out[CX == c] = np.maximum(np.log(np.maximum(p, 1e-300)), LOGFLOOR)
    return out


def feats(H, tb):
    """(V, len(ALL)) feature matrix for position H.t from history H only."""
    t = H.t
    a = H.a
    tok = H.tok
    edges = H.edges
    nc = np.minimum(a["nClicks"], swlib.NC)
    dur = a["Duration"]
    w = a["Whale"]
    F = np.zeros((V, len(ALL)))
    col = {k: i for i, k in enumerate(ALL)}
    x1 = tok[t - 1]
    c1, b1 = CX[x1], BX[x1]
    F[:, col["bigram"]] = tb.log_bg[x1]
    F[:, col["uni"]] = tb.log_uni
    F[:, col["samec1"]] = (CX == c1)
    F[:, col["sameb1"]] = (BX == b1)
    F[:, col["db1"]] = np.abs(BX - b1)
    n1, d1 = a["nClicks"][t - 1], dur[t - 1]
    if n1 >= 2 and d1 > 0:
        ici = d1 / (n1 - 1)
        dpred = {c: ici * (c - 1) for c in range(2, swlib.NC + 1)}
        F[:, col["tempo1_s10"]] = _bin_logp(dpred, 0.10, edges)
        F[:, col["tempo1_s25"]] = _bin_logp(dpred, 0.25, edges)
    # repetition persistence
    r = 1
    while r < t and tok[t - 1 - r] == x1:
        r += 1
    rep = (np.arange(V) == x1).astype(float)
    F[:, col["rep_run"]] = rep * np.log(r)
    if t >= 2:
        nrep = float((tok[1:t] == tok[:t - 1]).sum())
        F[:, col["rep_rate"]] = rep * np.log((nrep + 1.0) / (t - 1 - nrep + 1.0))
    # higher order
    cnt = np.bincount(tok, minlength=V).astype(float)
    F[:, col["cache"]] = np.log((cnt + tb.p_uni) / (t + 1.0))
    cntc = np.bincount(nc, minlength=swlib.NC + 1)[1:].astype(float)
    F[:, col["cache_c"]] = np.log((cntc[CX - 1] + tb.p_uni_c[CX - 1]) / (t + 1.0))
    if t >= 2:
        x2 = tok[t - 2]
        F[:, col["skip"]] = tb.log_sk[x2]
        F[:, col["same2"]] = (np.arange(V) == x2)
        F[:, col["samec2"]] = (CX == CX[x2])
        F[:, col["sameb2"]] = (BX == BX[x2])
        s1 = float(w[t - 1] == w[t - 2])
        F[:, col["rep_if_same_whale"]] = rep * s1
        F[:, col["echo2_if_switch"]] = (np.arange(V) == x2) * (1.0 - s1)
    ok = (a["nClicks"] >= 2) & (dur > 0)
    if ok.any():
        k = np.nonzero(ok)[0]
        wts = 0.6 ** (t - 1 - k)
        ici = np.sum(wts * dur[k] / (a["nClicks"][k] - 1)) / wts.sum()
        F[:, col["tempo_ewma"]] = _bin_logp({c: ici * (c - 1) for c in range(2, swlib.NC + 1)}, 0.15, edges)
    sd = np.zeros(V)
    for c in range(2, swlib.NC + 1):
        k = np.nonzero((nc == c) & (dur > 0))[0]
        if len(k):
            sd[CX == c] = _bin_logp({cc: dur[k[-1]] for cc in range(2, swlib.NC + 1)}, 0.10, edges)[CX == c]
    F[:, col["samec_dur"]] = sd
    return F


def nll_and_grad(theta, Fs, ys, lam):
    """Fs: (n, V, K), ys: (n,). Mean NLL in nats + lam*||theta||^2."""
    z = Fs @ theta                       # (n, V)
    lp = log_softmax(z, axis=1)
    n = len(ys)
    nll = -lp[np.arange(n), ys].mean() + lam * theta @ theta
    p = np.exp(lp)
    Ey = (p[:, :, None] * Fs).sum(1)     # (n, K)
    g = -(Fs[np.arange(n), ys] - Ey).mean(0) + 2 * lam * theta
    return nll, g


def fit(Fs, ys, lam):
    K = Fs.shape[2]
    th0 = np.zeros(K)
    th0[0] = 1.0                         # start at the bigram
    res = minimize(nll_and_grad, th0, args=(Fs, ys, lam), jac=True, method="L-BFGS-B",
                   options={"maxiter": 500})
    return res.x


def predict(theta, Fs):
    return np.exp(log_softmax(Fs @ theta, axis=1))
