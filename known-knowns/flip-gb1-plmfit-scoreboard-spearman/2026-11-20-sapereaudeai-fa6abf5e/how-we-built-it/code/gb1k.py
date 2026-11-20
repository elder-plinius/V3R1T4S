"""Mutation-kernel machinery for the FLIP GB1 three_vs_rest attempt (run 2026-11-20-0215).

Everything is built from the 20-letter amino-acid alphabet and the four known varying
sites (1-indexed 39, 40, 41, 54 of the 265-residue 5LDE chain A construct; Wu et al.,
eLife 2016;5:e16965, sites V39 D40 G41 V54).  No statistic computed over test rows
enters any feature, transform, penalty or selection.

The one-hot interaction expansion of a four-site sequence to order <= 3, with block
scales (1, s2, s3), has the closed-form Gram matrix

    K(i,j) = m + s2^2 * C(m,2) + s3^2 * C(m,3)

where m is the number of the four sites at which i and j carry the same residue.
(Established and checked against sklearn Ridge in run 2026-11-19-2355; re-checked here
by selftest.py.)  Two consequences used in this run's pre-registration:

  * C(m,4) = [m == 4] is the identity matrix on a set of distinct genotypes, so an
    order-4 block is exactly a shift of the ridge penalty: extending the family to
    fourth order IS extending the alpha grid downwards, nothing more.
  * {1, m, C(m,2), C(m,3), C(m,4)} spans every function of m, and a constant added to
    a Gram matrix is annihilated by the centring that implements the intercept.  So
    (s2, s3, alpha) already parameterise the complete family of mutation kernels on
    four sites - the whole Gaussian-process/variance-component family - up to scale.
"""
import csv
import hashlib

import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.special import expit
from scipy.stats import norm, spearmanr

SITES = (38, 39, 40, 53)          # 0-indexed; 1-indexed 39, 40, 41, 54
AA = "ACDEFGHIKLMNPQRSTVWY"       # the 20-letter alphabet, fixed a priori
AAIDX = {a: i for i, a in enumerate(AA)}


def load(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))
    return hashlib.sha256(raw).hexdigest(), rows


def codes(rows):
    return np.array([[AAIDX[r["aa_seq"][p]] for p in SITES] for r in rows], dtype=np.int8)


def scores(rows):
    return np.array([float(r["score"]) for r in rows], dtype=np.float64)


def nmut(rows):
    return np.array([int(r["no_mut"]) for r in rows], dtype=np.int64)


def match_counts(A, B):
    m = np.zeros((A.shape[0], B.shape[0]), dtype=np.int16)
    for p in range(4):
        m += (A[:, p][:, None] == B[None, :, p])
    return m


def kernel(m, s2=0.0, s3=0.0):
    mf = m.astype(np.float64)
    K = mf.copy()
    if s2:
        K += (s2 ** 2) * mf * (mf - 1.0) / 2.0
    if s3:
        K += (s3 ** 2) * mf * (mf - 1.0) * (mf - 2.0) / 6.0
    return K


def centre(K):
    rm = K.mean(axis=0, keepdims=True)
    cm = K.mean(axis=1, keepdims=True)
    gm = K.mean()
    return K - rm - cm + gm, rm, gm


def centre_cross(K_ev_tr, rm, gm):
    return K_ev_tr - K_ev_tr.mean(axis=1, keepdims=True) - rm + gm


# ---------------------------------------------------------------- target transforms
LOG_CS = (0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0)
TRANSFORMS = (["raw"] + ["log%g" % c for c in LOG_CS] + ["vdw", "lrank", "ace"])


def midranks(y):
    n = len(y)
    order = np.argsort(y, kind="mergesort")
    ranks = np.empty(n)
    ranks[order] = np.arange(1, n + 1, dtype=np.float64)
    uniq, inv, cnt = np.unique(y, return_inverse=True, return_counts=True)
    sums = np.zeros(len(uniq))
    np.add.at(sums, inv, ranks)
    return (sums / cnt)[inv]


def standardise(v):
    s = v.std()
    return (v - v.mean()) / (s if s > 0 else 1.0)


def transform(y_tr, kind):
    """Target transform computed from the FITTING rows only ('ace' is handled
    separately because it also depends on the kernel and the penalty)."""
    if kind == "raw":
        return y_tr.copy()
    if kind.startswith("log"):
        return np.log(y_tr + float(kind[3:]))
    if kind == "vdw":
        n = len(y_tr)
        return norm.ppf((midranks(y_tr) - 0.5) / n)
    if kind == "lrank":
        return standardise(midranks(y_tr))
    raise ValueError(kind)


def pav(y, w):
    """Pool-adjacent-violators: weighted isotonic (non-decreasing) least-squares fit
    of y with weights w.  Explicit and simple; y has at most n_bins entries here."""
    val = np.asarray(y, dtype=np.float64)
    wt = np.asarray(w, dtype=np.float64)
    lvl, lw, lsz = [], [], []
    for i in range(len(val)):
        lvl.append(val[i]); lw.append(wt[i]); lsz.append(1)
        while len(lvl) > 1 and lvl[-2] > lvl[-1]:
            v = (lvl[-2] * lw[-2] + lvl[-1] * lw[-1]) / (lw[-2] + lw[-1])
            w2 = lw[-2] + lw[-1]
            s2 = lsz[-2] + lsz[-1]
            lvl.pop(); lw.pop(); lsz.pop()
            lvl[-1] = v; lw[-1] = w2; lsz[-1] = s2
    out = np.empty(len(val))
    k = 0
    for v, s in zip(lvl, lsz):
        out[k:k + s] = v
        k += s
    return out


def ace_target(y_tr, d, V, alpha, n_bins=100, n_iter=5):
    """Alternating monotone transform (ACE, Breiman and Friedman 1985), computed from
    the FITTING rows only.  Starts from van der Waerden normal scores; each iteration
    takes the in-sample ridge fit f of the current transformed target, replaces the
    transform by the weighted isotonic regression of f on y (binned into n_bins
    quantile bins of the fitting targets), standardises it, and repeats."""
    n = len(y_tr)
    # quantile bins over the fitting targets; a tied value falls in a single bin
    edges = np.unique(np.quantile(y_tr, np.linspace(0, 1, n_bins + 1)))
    bin_of = np.clip(np.searchsorted(edges, y_tr, side="right") - 1, 0, len(edges) - 2)
    # bins must be monotone in y: they are, since they come from thresholds on y
    nb = bin_of.max() + 1
    cnt = np.bincount(bin_of, minlength=nb).astype(np.float64)
    keep = cnt > 0
    g = transform(y_tr, "vdw")
    g = standardise(g)
    for _ in range(n_iter):
        gc = g - g.mean()
        Vt = V.T @ gc
        f = V @ (Vt * (d / (d + alpha)))          # in-sample ridge fit, centred
        fb = np.bincount(bin_of, weights=f, minlength=nb)[keep] / cnt[keep]
        iso = pav(fb, cnt[keep])
        full = np.zeros(nb)
        full[keep] = iso
        gnew = full[bin_of]
        if gnew.std() == 0:
            break
        gnew = standardise(gnew)
        if np.max(np.abs(gnew - g)) < 1e-10:
            g = gnew
            break
        g = gnew
    return g


# ---------------------------------------------------------------- pairwise ranking
def ranknet_fit(Kc, y, alpha, a0, maxiter=40):
    """Minimise  (n/npairs) * sum_{i<j, y_i != y_j} log(1 + exp(-s_ij (f_i - f_j)))
    + (alpha/2) a' Kc a,  with f = Kc a, by L-BFGS-B.  The loss is invariant to adding
    a constant to f, so no intercept is needed.  Fitting rows only."""
    from scipy.optimize import minimize
    n = len(y)
    S = np.sign(y[:, None] - y[None, :]).astype(np.float32)
    live = (S != 0)
    npairs = float(np.count_nonzero(S)) / 2.0
    scale = n / max(npairs, 1.0)

    def fg(a):
        f64 = Kc @ a
        f = f64.astype(np.float32)
        Z = (-S) * (f[:, None] - f[None, :])
        L = 0.5 * float(np.logaddexp(np.float32(0.0), Z, where=live,
                                     out=np.zeros_like(Z)).sum(dtype=np.float64))
        gf = -(S * expit(Z)).sum(axis=1, dtype=np.float64)
        obj = scale * L + 0.5 * alpha * float(a @ f64)
        grad = Kc @ (scale * gf + alpha * a)
        return obj, grad

    res = minimize(fg, a0, jac=True, method="L-BFGS-B",
                   options={"maxiter": maxiter, "maxcor": 10})
    del S, live
    return res.x, res


# ---------------------------------------------------------------- solvers / utils
def ridge_dual(Kc, yc, alpha):
    c = cho_factor(Kc + alpha * np.eye(Kc.shape[0]), lower=True, check_finite=False)
    return cho_solve(c, yc, check_finite=False)


def spear(a, b):
    return float(spearmanr(a, b).statistic)


def boot_ci(y, p, n_boot=10000, seed=0):
    rng = np.random.default_rng(seed)
    n = len(y)
    out = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        out[b] = spearmanr(y[idx], p[idx]).statistic
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))
