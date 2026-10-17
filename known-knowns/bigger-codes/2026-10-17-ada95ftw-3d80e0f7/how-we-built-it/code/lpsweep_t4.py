"""Lens obstruction: LP upper bounds for A(n,d,w) (Johnson scheme), written from the definitions (independent of the repo's cwlp.py).
Constraints on inner distribution a_x (x = Johnson distance, a_0 = 1, a_x = 0 for 0<x<delta):
 (D_k)  sum_x a_x Q_k(x) >= 0, Q_k(x) = m_k E_x(k)/v_x (Eberlein form, Delsarte 1973)
 (M_ts) sum_x C(w-x,s)C(n-w-x,t-s) a_x <= U(n-t,d,w-s) C(w,s)C(n-w,t-s)   (t<=2; shortening second moment)
 (X_x)  a_x <= U(n,d,2x)   [c XOR (codewords at distance 2x from c) is an (n,d,2x) constant-weight code]
 (R_x)  a_x <= C(w,x) U(n-w,d,x),  a_x <= C(n-w,x) U(w,d,x)  [fix the removed / added part]
U(.) = numeric upper bound from the live table (mirror-aware) or exact elementary bounds (trivial cells, Johnson recursion).
Float HiGHS locates the optimum; the bound is then CERTIFIED by an exact rational dual vector (Fractions)."""
import sys, json, time
from fractions import Fraction as F
from math import comb, floor
from functools import lru_cache
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else 'tools')
from cells import parse
CELLS = parse(sys.argv[2] if len(sys.argv) > 2 else 'data/Andw.html')
USE_TABLE_SUB = True
TS = (1, 2, 3, 4)

@lru_cache(None)
def U(n, d, w):
    """Valid upper bound on A(n,d,w) (d even)."""
    if w < 0 or w > n: return 0
    if w > n - w: w = n - w
    delta = d // 2
    if w < delta: return 1
    if w == delta: return n // delta  # disjoint supports
    best = None
    if USE_TABLE_SUB and (n, d, w) in CELLS and CELLS[(n, d, w)][1] is not None:
        best = CELLS[(n, d, w)][1]
    j = (n * U(n - 1, d, w - 1)) // w  # Johnson
    best = j if best is None else min(best, j)
    return best

def E(n, w, x, k):
    return sum((-1) ** j * comb(k, j) * comb(w - k, x - j) * comb(n - w - k, x - j) for j in range(x + 1))

def Q(n, w, k, x):
    m = comb(n, k) - (comb(n, k - 1) if k else 0)
    return F(m * E(n, w, x, k), comb(w, x) * comb(n - w, x))

def build(n, d, w, moments=True, xb=True):
    delta = d // 2; X = list(range(delta, w + 1))
    rows = []; rhs = []; tags = []
    for k in range(1, w + 1):  # -sum a_x Q_k(x) <= Q_k(0)
        rows.append([-Q(n, w, k, x) for x in X]); rhs.append(Q(n, w, k, 0)); tags.append(f'D{k}')
    if moments:
        for t in TS:
            for s in range(t + 1):
                if s > w or t - s > n - w: continue
                N = comb(w, s) * comb(n - w, t - s); u = U(n - t, d, w - s)
                rows.append([F(comb(w - x, s) * comb(n - w - x, t - s)) for x in X]); rhs.append(F(u * N - N)); tags.append(f'M{t}{s}')
    if xb:
        for i, x in enumerate(X):
            b = min(U(n, d, 2 * x) if 2 * x <= n else 0, comb(w, x) * U(n - w, d, x), comb(n - w, x) * U(w, d, x))
            r = [F(0)] * len(X); r[i] = F(1); rows.append(r); rhs.append(F(b)); tags.append(f'X{x}')
    return X, rows, rhs, tags

def certify(n, d, w, **kw):
    X, rows, rhs, tags = build(n, d, w, **kw)
    sc = [max(max(abs(v) for v in r), abs(b), F(1)) for r, b in zip(rows, rhs)]
    A = np.array([[float(v / s) for v in r] for r, s in zip(rows, sc)]); b = np.array([float(bb / s) for bb, s in zip(rhs, sc)])
    res = linprog(-np.ones(len(X)), A_ub=A, b_ub=b, bounds=[(0, None)] * len(X), method='highs')
    if res.status != 0: return None
    ys = -res.ineqlin.marginals  # duals >= 0 for scaled rows
    best = None
    for den in (10**6, 10**9, 10**12):
        y = [max(F(v).limit_denominator(den), F(0)) / s for v, s in zip(ys, sc)]
        col = [sum(y[r] * rows[r][i] for r in range(len(rows))) for i in range(len(X))]
        mn = min(col)
        if mn <= 0: continue
        y = [v / mn for v in y] if mn < 1 else y
        col = [sum(y[r] * rows[r][i] for r in range(len(rows))) for i in range(len(X))]
        assert all(c >= 1 for c in col) and all(v >= 0 for v in y)
        val = 1 + sum(y[r] * rhs[r] for r in range(len(rows)))
        if best is None or val < best[0]: best = (val, y)
    if best is None: return None
    return dict(float_opt=1 - res.fun, cert=best[0], bound=floor(best[0]), y=best[1], tags=tags)

if __name__ == '__main__':
    t0 = time.time(); out = []
    for (n, d, w), (lo, hi, raw) in sorted(CELLS.items()):
        if 2 * w > n: continue
        r = certify(n, d, w)
        if r is None: print('FAIL', n, d, w, flush=True); continue
        rd = certify(n, d, w, moments=False, xb=False)
        line = dict(n=n, d=d, w=w, lo=lo, hi=hi, delsarte=rd and rd['bound'], strong=r['bound'], cert=str(r['cert']))
        out.append(line)
        flag = 'BELOW_TABLE' if hi is not None and r['bound'] < hi else ''
        if flag or (hi is not None and rd and rd['bound'] < hi): print(n, d, w, 'table', raw, 'delsarte', rd and rd['bound'], 'strong', r['bound'], flag, flush=True)
    json.dump(out, open(sys.argv[3] if len(sys.argv) > 3 else 'sweep.json', 'w'), indent=0)
    print('cells', len(out), 'below_table', sum(1 for o in out if o['hi'] is not None and o['strong'] < o['hi']), 'secs', round(time.time() - t0, 1))
