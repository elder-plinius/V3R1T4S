"""brute-scale lens optimizer library (numpy + scipy only; all-pairs, meant for N <= ~400).

- lse_polish: L-BFGS on the LogSumExp surrogate of max_{i<j} <y_i, y_j>, y = x/|x|, with an annealed beta schedule.
- slp_polish: sequential linear programming (HiGHS) on the near-active pairs, trust region per coordinate, tangent
  constraints; converges the max cosine to float precision.
- perturbations for basin hopping: gaussian on all points, gaussian on a random cap, re-seed k points into holes.
"""
import numpy as np
from scipy.optimize import minimize, linprog
from scipy import sparse


def normalize(X):
    return X / np.linalg.norm(X, axis=1)[:, None]


def cmax(X):
    Y = normalize(X)
    G = Y @ Y.T
    np.fill_diagonal(G, -3.0)
    return float(G.max())


def lse_fg(x, N, d, beta):
    Z = x.reshape(N, d)
    n = np.linalg.norm(Z, axis=1)
    Y = Z / n[:, None]
    G = Y @ Y.T
    np.fill_diagonal(G, -3.0)
    m = G.max()
    E = np.exp(beta * (G - m))
    np.fill_diagonal(E, 0.0)
    S = 0.5 * E.sum()
    val = m + np.log(S) / beta
    dY = (E @ Y) / S
    dZ = (dY - np.sum(dY * Y, axis=1)[:, None] * Y) / n[:, None]
    return val, dZ.ravel()


def lse_value(X, beta):
    N, d = X.shape
    return lse_fg(normalize(X).ravel(), N, d, beta)[0]


def lse_polish(X, betas, maxiter=400, gtol=1e-12):
    N, d = X.shape
    x = normalize(X).ravel()
    for b in betas:
        r = minimize(lse_fg, x, args=(N, d, b), jac=True, method="L-BFGS-B",
                     options={"maxiter": maxiter, "gtol": gtol, "ftol": 1e-15, "maxcor": 20})
        x = normalize(r.x.reshape(N, d)).ravel()
    return x.reshape(N, d)


def slp_polish(X, iters=80, r0=2e-4, rmin=1e-14, verbose=False, time_cap=None):
    import time
    t0 = time.time()
    Y = normalize(X)
    N, d = Y.shape
    G = Y @ Y.T
    np.fill_diagonal(G, -3.0)
    c = G.max()
    r = r0
    nv = N * d + 1
    for it in range(iters):
        if time_cap is not None and time.time() - t0 > time_cap:
            break
        act = c - (4.0 * r * np.sqrt(d) + 4.0 * r * r * d + 1e-13)
        I, J = np.nonzero(np.triu(G >= act, 1))
        P = len(I)
        # rows: pair constraints  y_j . dy_i + y_i . dy_j - t <= -g_ij
        rows = np.repeat(np.arange(P), 2 * d + 1)
        cols = np.empty((P, 2 * d + 1), dtype=np.int64)
        vals = np.empty((P, 2 * d + 1))
        ar = np.arange(d)
        cols[:, :d] = I[:, None] * d + ar[None, :]
        vals[:, :d] = Y[J]
        cols[:, d:2 * d] = J[:, None] * d + ar[None, :]
        vals[:, d:2 * d] = Y[I]
        cols[:, 2 * d] = nv - 1
        vals[:, 2 * d] = -1.0
        A = sparse.csr_matrix((vals.ravel(), (rows, cols.ravel())), shape=(P, nv))
        b = -G[I, J]
        # equality: y_i . dy_i = 0
        erows = np.repeat(np.arange(N), d)
        ecols = np.arange(N * d)
        Aeq = sparse.csr_matrix((Y.ravel(), (erows, ecols)), shape=(N, nv))
        beq = np.zeros(N)
        cobj = np.zeros(nv); cobj[-1] = 1.0
        bounds = [(-r, r)] * (N * d) + [(None, None)]
        res = linprog(cobj, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, bounds=bounds, method="highs")
        if res.status != 0:
            r *= 0.5
            if r < rmin:
                break
            continue
        dY = res.x[:-1].reshape(N, d)
        Yn = normalize(Y + dY)
        Gn = Yn @ Yn.T
        np.fill_diagonal(Gn, -3.0)
        cn = Gn.max()
        if verbose:
            print(it, "r", r, "P", P, "lp_t", res.x[-1], "c", c, "cn", cn, flush=True)
        if cn < c:
            pred = c - res.x[-1]
            actual = c - cn
            Y, G, c = Yn, Gn, cn
            if actual > 0.5 * pred:
                r = min(r * 2.0, 1e-2)
        else:
            r *= 0.25
            if r < rmin:
                break
    return Y, float(c)


def deep_holes(Y, k, rng, M=20000):
    N, d = Y.shape
    S = normalize(rng.normal(size=(M, d)))
    mc = (S @ Y.T).max(axis=1)
    idx = np.argsort(mc)[:k * 20]
    # pick k well separated among the best candidates
    chosen = []
    for i in idx:
        if all(S[i] @ S[j] < 0.9 for j in chosen):
            chosen.append(i)
        if len(chosen) == k:
            break
    return S[chosen]


def perturb(Y, kind, scale, rng):
    N, d = Y.shape
    Z = Y.copy()
    if kind == "gauss":
        Z = Z + scale * rng.normal(size=Z.shape)
    elif kind == "cap":
        u = normalize(rng.normal(size=(1, d)))[0]
        h = Z @ u
        sel = h > np.quantile(h, 1.0 - min(0.9, max(0.05, scale * 10)))
        Z[sel] = Z[sel] + 0.3 * rng.normal(size=(sel.sum(), d)) / np.sqrt(d)
    elif kind == "reseed":
        k = max(1, int(round(scale)))
        G = Z @ Z.T
        np.fill_diagonal(G, -3.0)
        # remove the k points with the most near-max contacts (ties broken randomly)
        c = G.max()
        cnt = (G > c - 1e-3).sum(axis=1) + rng.random(N) * 0.5
        rem = np.argsort(-cnt)[:k] if rng.random() < 0.5 else rng.choice(N, k, replace=False)
        keep = np.setdiff1d(np.arange(N), rem)
        H = deep_holes(Z[keep], k, rng)
        if len(H) < k:
            H = np.vstack([H, normalize(rng.normal(size=(k - len(H), d)))])
        Z = np.vstack([Z[keep], H])
        Z = Z + 1e-3 * rng.normal(size=Z.shape)
    return normalize(Z)


# ---------------- C-backed versions ----------------
import ctypes, os
_lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), "liblse3.so"))
_dp = ctypes.POINTER(ctypes.c_double)
for _f in (_lib.lse_fg, _lib.pen_fg):
    _f.restype = ctypes.c_double
    _f.argtypes = [ctypes.c_int, ctypes.c_int, _dp, ctypes.c_double, _dp, _dp]
_lib.cmax.restype = ctypes.c_double
_lib.cmax.argtypes = [ctypes.c_int, ctypes.c_int, _dp, _dp]


class CObj:
    def __init__(self, N, d):
        self.N, self.d = N, d
        self.work = np.zeros(N * d + N + N * N + 8)
        self.grad = np.zeros(N * d)
        self.wp = self.work.ctypes.data_as(_dp)
        self.gp = self.grad.ctypes.data_as(_dp)
        self.nfev = 0

    def lse(self, x, beta):
        x = np.ascontiguousarray(x, dtype=np.float64)
        v = _lib.lse_fg(self.N, self.d, x.ctypes.data_as(_dp), beta, self.gp, self.wp)
        self.nfev += 1
        return v, self.grad.copy()

    def pen(self, x, t):
        x = np.ascontiguousarray(x, dtype=np.float64)
        v = _lib.pen_fg(self.N, self.d, x.ctypes.data_as(_dp), t, self.gp, self.wp)
        self.nfev += 1
        return v, self.grad.copy()

    def cmax(self, X):
        x = np.ascontiguousarray(X, dtype=np.float64).ravel()
        return _lib.cmax(self.N, self.d, x.ctypes.data_as(_dp), self.wp)


def c_lse_polish(obj, X, betas, maxiter=400, gtol=1e-13, maxcor=20):
    N, d = obj.N, obj.d
    x = normalize(X).ravel()
    for b in betas:
        r = minimize(obj.lse, x, args=(b,), jac=True, method="L-BFGS-B",
                     options={"maxiter": maxiter, "gtol": gtol, "ftol": 1e-16, "maxcor": maxcor})
        x = normalize(r.x.reshape(N, d)).ravel()
    return x.reshape(N, d)


def c_pen_polish(obj, X, t, maxiter=2000):
    """minimise overlap penalty at target t; returns (Y, E)."""
    N, d = obj.N, obj.d
    x = normalize(X).ravel()
    r = minimize(obj.pen, x, args=(t,), jac=True, method="L-BFGS-B",
                 options={"maxiter": maxiter, "gtol": 1e-18, "ftol": 1e-22, "maxcor": 30})
    Y = normalize(r.x.reshape(N, d))
    return Y, r.fun


def c_pen_descend(obj, X, c_start, steps=12, shrink0=1e-5, time_cap=30.0):
    """Threshold-lowering polish: try targets t = c - delta; on success (energy ~ 0 -> cmax <= t + tiny) lower c.
    Returns best (Y, c)."""
    import time
    t0 = time.time()
    Y = normalize(X)
    c = obj.cmax(Y)
    delta = shrink0
    for _ in range(steps):
        if time.time() - t0 > time_cap:
            break
        t = c - delta
        Z, E = c_pen_polish(obj, Y, t)
        cz = obj.cmax(Z)
        if cz < c:
            Y, c = Z, cz
            delta *= 2.0
        else:
            delta *= 0.25
            if delta < 1e-15:
                break
    return Y, c


_lib.lbfgs_polish.restype = ctypes.c_double
_lib.lbfgs_polish.argtypes = [ctypes.c_int, ctypes.c_int, _dp, ctypes.c_int, _dp, ctypes.c_int, ctypes.c_int, _dp, _dp]
_MEM = 10


def cc_polish(obj, X, betas, maxiter=300):
    """L-BFGS polish fully in C. Returns (Y, cmax)."""
    N, d = obj.N, obj.d
    n = N * d
    if not hasattr(obj, "lw"):
        obj.lw = np.zeros((2 * _MEM + 4) * n + 2 * _MEM + 8)
    x = np.ascontiguousarray(normalize(X).ravel(), dtype=np.float64).copy()
    bt = np.ascontiguousarray(np.array(betas, dtype=np.float64))
    c = _lib.lbfgs_polish(N, d, x.ctypes.data_as(_dp), len(betas), bt.ctypes.data_as(_dp), int(maxiter), _MEM,
                          obj.wp, obj.lw.ctypes.data_as(_dp))
    return x.reshape(N, d), c


_OBJ_CACHE = {}


def evict(Y, k, rng, betas, maxiter=300):
    """H6 overfill-and-evict: add k points in deep holes, polish N+k points, delete the k points with the largest
    (max cosine, contact count) and return the N-point configuration (unpolished at N)."""
    N, d = Y.shape
    key = (N + k, d)
    if key not in _OBJ_CACHE:
        _OBJ_CACHE[key] = CObj(N + k, d)
    O2 = _OBJ_CACHE[key]
    H = deep_holes(Y, k, rng)
    if len(H) < k:
        H = np.vstack([H, normalize(rng.normal(size=(k - len(H), d)))])
    Z, c = cc_polish(O2, np.vstack([Y, H]), betas, maxiter=maxiter)
    G = Z @ Z.T
    np.fill_diagonal(G, -3.0)
    rem = []
    for _ in range(k):
        alive = np.setdiff1d(np.arange(N + k), rem)
        Gs = G[np.ix_(alive, alive)]
        cm = Gs.max()
        score = (Gs > cm - 1e-4).sum(axis=1) + Gs.max(axis=1) * 10 + rng.random(len(alive)) * 1e-3
        rem.append(alive[int(np.argmax(score))])
    keep = np.setdiff1d(np.arange(N + k), rem)
    return Z[keep]
