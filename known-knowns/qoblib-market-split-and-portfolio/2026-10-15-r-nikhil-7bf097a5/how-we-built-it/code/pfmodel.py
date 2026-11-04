"""Fast integer-table model of QOBLIB 06-portfolio (bqp_u3_c10), for search only.

The judge is checker/pf_eval.py (exact rationals). This module precomputes every rounded coefficient once
(float with an exact Fraction fallback near rounding ties) and evaluates portfolios in net-position space:
w[t, i] = long units - short units in {-3..3}. Canonical counts u+ = max(w, 0), u- = max(-w, 0) are optimal for a
given w (holding both directions only adds budget, short and trading cost), so the search works on w.

Objective per period t (t_end = last period), all coefficients exact integers:
  risk     w_t' Q_t w_t,  Q_t[i,j] = round(lambda * cov[i,j,t] * p[i,t] * p[j,t])
  cash     -100 + 10 * sum(w_t)              (-round(nu*unit*2^k) on the binary expansion of 10 - net)
  short    s_t . max(-w_t, 0),  s = round(rho * p)
  return   -r_t . w_t for t < t_end,  r = round(p[t+1] - p[t])
  trading  d_0 . |w_0| at t_beg; d_t . |w_t - w_{t-1}| for t_beg < t < t_end; d_end . |w_end| at t_end (liquidation)
Constraints per t: -5 <= sum(w_t) <= 10, sum |w_t| <= B, |w| <= 3.
"""
import gzip
import math
import os
from fractions import Fraction as F

import numpy as np

CASH, UNIT = F(1000000), F(100000)
DELTA, NU, RHO = F("0.001"), F("0.0001"), F("0.000025")
UB = 3


def zround(q):
    a = abs(q)
    n = math.floor(a + F(1, 2))
    return n if q >= 0 else -n


def _open(path):
    if os.path.exists(path):
        return open(path, "r", encoding="utf-8")
    return gzip.open(path + ".gz", "rt", encoding="utf-8")


def _rows(path):
    with _open(path) as f:
        for line in f:
            line = line.split("#", 1)[0].strip()
            if line:
                yield line.split()


class Model:
    def __init__(self, inst_dir, B, lam, need_cov=True):
        self.B = int(B)
        self.lam = F(lam)
        raw, order, days = {}, [], set()
        for t, s, v in _rows(os.path.join(inst_dir, "stock_prices.txt")):
            t = int(t)
            days.add(t)
            if s not in raw:
                raw[s] = {}
                order.append(s)
            raw[s][t] = F(v)
        T = sorted(days)
        assert T == list(range(T[0], T[-1] + 1))
        self.days = T
        self.t0 = T[0]
        self.order = order
        self.idx = {s: i for i, s in enumerate(order)}
        n, nT = len(order), len(T)
        self.n, self.nT = n, nT
        p = [[raw[s][t] * (UNIT / raw[s][T[0]]) for t in T] for s in order]  # p[i][k]
        self.r = np.zeros((nT, n), dtype=np.int64)
        self.d = np.zeros((nT, n), dtype=np.int64)
        self.s = np.zeros((nT, n), dtype=np.int64)
        for i in range(n):
            for k in range(nT):
                if k < nT - 1:
                    self.r[k, i] = zround(p[i][k + 1] - p[i][k])
                self.d[k, i] = zround(DELTA * p[i][k])
                self.s[k, i] = zround(RHO * p[i][k])
        self.Q = np.zeros((nT, n, n), dtype=np.int64)
        self.n_exact_fallback = 0
        if self.lam != 0 and need_cov:
            pf = np.array([[float(x) for x in row] for row in p])  # (n, nT)
            tt, ii, jj, vals = [], [], [], []
            for t, s1, s2, v in _rows(os.path.join(inst_dir, "covariance_matrices.txt")):
                tt.append(int(t) - T[0])
                ii.append(self.idx[s1])
                jj.append(self.idx[s2])
                vals.append(v)
            tt, ii, jj = np.array(tt), np.array(ii), np.array(jj)
            vf = np.array([float(v) for v in vals])
            x = float(self.lam) * vf * pf[ii, tt] * pf[jj, tt]
            ax = np.abs(x)
            q = np.sign(x) * np.floor(ax + 0.5)
            near = np.abs(ax - np.floor(ax) - 0.5) < 1e-6
            for k in np.nonzero(near)[0]:
                q[k] = zround(self.lam * F(vals[k]) * p[ii[k]][tt[k]] * p[jj[k]][tt[k]])
            self.n_exact_fallback = int(near.sum())
            self.Q[tt, ii, jj] = q.astype(np.int64)
            assert len(tt) == nT * n * n, "covariance is not complete"
        self.Qs = self.Q + np.transpose(self.Q, (0, 2, 1))
        self.diag = np.array([np.diag(self.Q[k]) for k in range(nT)])
        self.lin = 10 - self.r  # r[t_end] = 0 already, so lin[t_end] = 10

    def feasible(self, W):
        if np.abs(W).max() > UB:
            return False
        net = W.sum(axis=1)
        tot = np.abs(W).sum(axis=1)
        return bool(np.all(net >= -5) and np.all(net <= 10) and np.all(tot <= self.B))

    def objective(self, W):
        W = np.asarray(W, dtype=np.int64)
        L = self.nT - 1
        obj = 0
        for k in range(self.nT):
            w = W[k]
            obj += int(w @ self.Q[k] @ w)
            obj += -100 + 10 * int(w.sum())
            obj += int(self.s[k] @ np.maximum(-w, 0))
            if k < L:
                obj -= int(self.r[k] @ w)
            if k == 0 or k == L:
                obj += int(self.d[k] @ np.abs(w))
            else:
                obj += int(self.d[k] @ np.abs(w - W[k - 1]))
        return obj

    def read_solution(self, path):
        W = np.zeros((self.nT, self.n), dtype=np.int64)
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                tok = line.split()
                if len(tok) == 4:
                    W[int(tok[0]) - self.t0, self.idx[tok[1]]] += int(tok[2]) - int(tok[3])
        return W

    def write_solution(self, path, W, instance_name, lam_text, note):
        obj = self.objective(W)
        with open(path, "w", encoding="utf-8") as f:
            f.write("# %s\n" % note)
            f.write("instance %s\nbudget %d\nlambda %s\nobjective %d\n" % (instance_name, self.B, lam_text, obj))
            f.write("# period symbol long short\n")
            for k in range(self.nT):
                for i in range(self.n):
                    w = int(W[k, i])
                    if w:
                        f.write("%d %s %d %d\n" % (k + self.t0, self.order[i], max(w, 0), max(-w, 0)))
        return obj
