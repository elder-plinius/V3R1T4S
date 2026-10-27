"""Crossing estimator p_L from nzwrap histograms: the root of R_2D(p) - R_0D(p) = 0 on one torus size.

R_0D(n) = P(n < n1) (no cluster with a non-contractible cycle after n elements), R_2D(n) = P(n >= n2).
Canonical curves: R(p) = sum_n Binom(M, n, p) R(n). Error bar: jackknife over the independent blocks.

usage: python analyze_mc.py <hist files ...>   (all files must share mode, L1, L2, M)
"""
import sys
import math
import glob
import numpy as np
from scipy.special import gammaln


def read_hist(path):
    with open(path) as f:
        head = f.readline().split()
        meta = dict(zip(head[0::2], head[1::2]))
        rows = np.loadtxt(f, dtype=np.int64, ndmin=2)
    return meta, rows


def load(paths):
    metas, hs = [], []
    M = None
    for p in paths:
        meta, rows = read_hist(p)
        if M is None:
            M = int(meta["M"])
        assert int(meta["M"]) == M
        h1 = np.zeros(M + 1, np.int64)
        h2 = np.zeros(M + 1, np.int64)
        if rows.size:
            h1[rows[:, 0]] += rows[:, 1]
            h2[rows[:, 0]] += rows[:, 2]
        metas.append(meta)
        hs.append((h1, h2))
    return metas, hs, M


def curves(h1, h2):
    S = h1.sum()
    # R0(n) = P(n1 > n): fraction of samples whose first winding came after n elements
    c1 = np.cumsum(h1)          # number with n1 <= n
    R0 = 1.0 - c1 / S
    c2 = np.cumsum(h2)          # number with n2 <= n
    R2 = c2 / S
    return R0, R2


class Canon:
    def __init__(self, M):
        self.M = M
        self.n = np.arange(M + 1)
        self.lg = gammaln(M + 1) - gammaln(self.n + 1) - gammaln(M - self.n + 1)

    def weights(self, p):
        mu = self.M * p
        sd = math.sqrt(self.M * p * (1 - p))
        lo = max(0, int(mu - 14 * sd) - 2)
        hi = min(self.M, int(mu + 14 * sd) + 2)
        nn = self.n[lo:hi + 1]
        lw = self.lg[lo:hi + 1] + nn * math.log(p) + (self.M - nn) * math.log1p(-p)
        w = np.exp(lw - lw.max())
        w /= w.sum()
        return lo, hi, w

    def value(self, R, p):
        lo, hi, w = self.weights(p)
        return float(w @ R[lo:hi + 1])


def root(can, R0, R2, a=0.05, b=0.95, tol=1e-12):
    f = lambda p: can.value(R2, p) - can.value(R0, p)
    fa, fb = f(a), f(b)
    if not (fa < 0 < fb):
        raise ValueError("not bracketed")
    for _ in range(200):
        m = 0.5 * (a + b)
        fm = f(m)
        if fm < 0:
            a, fa = m, fm
        else:
            b, fb = m, fm
        if b - a < tol:
            break
    return 0.5 * (a + b), (can.value(R2, 0.5 * (a + b)) + can.value(R0, 0.5 * (a + b))) / 2


def analyze(paths, quiet=False):
    metas, hs, M = load(paths)
    can = Canon(M)
    H1 = sum(h[0] for h in hs)
    H2 = sum(h[1] for h in hs)
    S = int(H1.sum())
    R0, R2 = curves(H1, H2)
    p_all, rc = root(can, R0, R2)
    nb = len(hs)
    jk = []
    for k in range(nb):
        R0k, R2k = curves(H1 - hs[k][0], H2 - hs[k][1])
        jk.append(root(can, R0k, R2k, a=p_all - 0.05, b=p_all + 0.05)[0])
    jk = np.array(jk)
    err = math.sqrt((nb - 1) / nb * np.sum((jk - jk.mean()) ** 2)) if nb > 1 else float("nan")
    m = metas[0]
    if not quiet:
        print("mode %s L1 %s L2 %s M %d blocks %d samples %d  p_L %.9f +- %.9f  R0=R2 at crossing %.4f" % (
            m["mode"], m["L1"], m["L2"], M, nb, S, p_all, err, rc))
    return {"L1": int(m["L1"]), "L2": int(m["L2"]), "M": M, "blocks": nb, "samples": S, "p": p_all, "err": err,
            "Rc": rc}


if __name__ == "__main__":
    paths = []
    for a in sys.argv[1:]:
        paths += sorted(glob.glob(a))
    analyze(paths)
