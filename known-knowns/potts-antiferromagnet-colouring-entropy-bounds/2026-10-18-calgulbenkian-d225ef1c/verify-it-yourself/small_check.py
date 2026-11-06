"""Independent small-width check: dominant eigenvalue theta_1 of the row-to-row transfer matrix for proper q-colourings of the
square grid, strip of width m with free ends (path P_m) or periodic (cycle C_m), computed matrix-free and compared with the table in
THETA_TABLE_qQ.txt. Uses numpy when available (widths up to q^m <= 2.5 million); otherwise a pure-python fallback (q^m <= 20000).
usage: small_check.py Q TABLE.txt MAXM"""
import sys, itertools
q, table, maxm = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
try:
    import numpy as np
    LIMIT = 2_500_000
except ImportError:
    np = None
    LIMIT = 20000
    print('NOTE: numpy not installed; pure-python fallback, widths with q^m <= %d only' % LIMIT)
ref = {}
for line in open(table):
    if line.startswith('#') or not line.strip(): continue
    a, kind, m, val = line.split(); ref[(kind, int(m))] = val
def theta_np(kind, m):
    shape = (q,) * m
    idx = np.indices(shape)
    ok = np.ones(shape, dtype=bool)
    for i in range(m - 1): ok &= idx[i] != idx[i + 1]
    if kind == 'cycle' and m >= 3: ok &= idx[m - 1] != idx[0]
    maskf = ok.astype(np.float64)
    if q ** m <= 1100:   # small: dense symmetric eigenproblem on the proper colourings
        K = np.ones((1, 1))
        for _ in range(m): K = np.kron(K, np.ones((q, q)) - np.eye(q))
        sel = np.flatnonzero(ok.reshape(-1))
        return float(np.linalg.eigvalsh(K[np.ix_(sel, sel)])[-1])
    x = maskf.copy(); x /= np.linalg.norm(x)
    def T(x):
        y = x
        for ax in range(m): y = y.sum(axis=ax, keepdims=True) - y  # apply (J - I) along each axis
        return y * maskf
    lam = 0.0
    for it in range(4000):
        y = T(x)
        new = float(np.vdot(x, y))
        y = y + 0.5 * new * x   # shift so that negative eigenvalues cannot compete
        y /= np.linalg.norm(y)
        if it > 5 and abs(new - lam) < 1e-13 * abs(new): lam = new; break
        lam = new; x = y
    return lam
def theta_py(kind, m):
    n = q ** m
    cols = list(itertools.product(range(q), repeat=m))
    mask = [1.0 if all(c[i] != c[i + 1] for i in range(m - 1)) and (kind != 'cycle' or m < 3 or c[m - 1] != c[0]) else 0.0 for c in cols]
    x = [v / sum(mask) for v in mask]
    strides = [q ** (m - 1 - i) for i in range(m)]
    def T(x):
        y = x
        for st in strides:
            z = [0.0] * n
            for base in range(n):
                if (base // st) % q != 0: continue
                tot = sum(y[base + j * st] for j in range(q))
                for j in range(q): z[base + j * st] = tot - y[base + j * st]
            y = z
        return [a * b for a, b in zip(y, mask)]
    lam = 0.0
    for it in range(600):
        y = T(x)
        new = sum(a * b for a, b in zip(x, y)) / sum(a * a for a in x)
        y = [a + 0.5 * new * b for a, b in zip(y, x)]
        nr = sum(a * a for a in y) ** 0.5
        x = [a / nr for a in y]
        if it > 5 and abs(new - lam) < 1e-13 * abs(new): lam = new; break
        lam = new
    return lam
bad = 0; done = 0
for kind in ('path', 'cycle'):
    for m in range(3 if kind == 'cycle' else 2, maxm + 1):
        if (kind, m) not in ref or q ** m > LIMIT: continue
        t = (theta_np if np is not None else theta_py)(kind, m); r = float(ref[(kind, m)])
        rel = abs(t - r) / r
        good = rel < 1e-10
        bad += not good; done += 1
        print('%s q=%d %s m=%d: computed %.12f, table %.12f, relative diff %.2e' % ('PASS' if good else 'FAIL', q, kind, m, t, r, rel))
bad += done == 0
print('SMALL-WIDTH CHECK OK (%d comparisons)' % done if bad == 0 else 'SMALL-WIDTH CHECK FAILED')
sys.exit(1 if bad else 0)
