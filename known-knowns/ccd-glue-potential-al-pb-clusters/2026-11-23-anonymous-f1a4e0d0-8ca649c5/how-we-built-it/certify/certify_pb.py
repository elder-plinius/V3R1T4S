"""Certify a Pb glue minimum: float64 L-BFGS polish (gtol 1e-12) then Newton steps with the FD Hessian, gradient
re-evaluated in mpmath (30 digits) with the same piecewise formulas as lead.py; double-precision Hessian (central
differences of the analytic gradient, h = 1e-5 A); compare with the polished posted structure.
Usage: certify_pb.py coords.xyz N table_energy posted out.xyz"""
import sys, json, numpy as np, mpmath as mp, lead
from scipy.optimize import minimize
mp.mp.dps = 30
L = lead
def poly(x, cs):
    s = mp.mpf(0); ds = mp.mpf(0)
    for k, c in reversed(list(enumerate(cs))):
        s = s * x + mp.mpf(c)
    for k, c in reversed(list(enumerate(cs))):
        if k: ds = ds * x + k * mp.mpf(c)
    return s, ds
def deriv(x, cs):
    return sum(k * mp.mpf(c) * x**(k-1) for k, c in enumerate(cs) if k)
def P(x, cs): return sum(mp.mpf(c) * x**k for k, c in enumerate(cs)), deriv(x, cs)
def rh(r):
    if r >= L.RRC: return mp.mpf(0), mp.mpf(0)
    if r >= L.RRB: return P(r - L.RRC, [0, 0, L.R2III, L.R3III])
    if r >= L.RRD: return P(r - L.RRD, [L.RHOD, L.R1II, L.R2II, L.R3II])
    return P(r - L.RRD, [L.RHOD, L.R1I, L.R2I, L.R3I])
def uu(n):
    if n > L.DB: return P(n - L.DB, [L.UB, 0, L.B2III, L.B3III])
    if n > L.DSW: return P(n - L.DB, [L.UB, 0, L.B2II, L.B3II, L.B4II])
    return P(n - L.DSW, [L.B0I, L.B1I, L.B2I, L.B3I, L.B4I])
def v2(r):
    if r >= L.RC: return mp.mpf(0), mp.mpf(0)
    if r >= L.D: return P(r - L.D, [L.A0II, L.A1II, L.A2II, L.A3II, L.A4II, L.A5II, L.A6II])
    return P(r - L.D, [L.A0I, L.A1I, L.A2I, L.A3I, L.A4I])
def eg_mp(X):
    n = len(X); X = [[mp.mpf(float(v)) for v in row] for row in X]; rho = [mp.mpf(0)] * n; E = mp.mpf(0); pr = []
    for i in range(n):
        for j in range(i + 1, n):
            dv = [X[i][k] - X[j][k] for k in range(3)]; r = mp.sqrt(sum(t * t for t in dv))
            if r >= L.RRC: continue
            p, dp = v2(r); q, dq = rh(r); E += p; rho[i] += q; rho[j] += q; pr.append((i, j, dv, r, dp, dq))
    du = []
    for i in range(n): u, d = uu(rho[i]); E += u; du.append(d)
    g = [[mp.mpf(0)] * 3 for _ in range(n)]
    for i, j, dv, r, dp, dq in pr:
        w = (dp + (du[i] + du[j]) * dq) / r
        for k in range(3): g[i][k] += dv[k] * w; g[j][k] -= dv[k] * w
    return E, mp.sqrt(sum(t * t for row in g for t in row))
def hess(x, h=1e-5):
    n = len(x); H = np.zeros((n, n))
    for k in range(n):
        e = np.zeros(n); e[k] = h; H[:, k] = (L.eg(x + e)[1] - L.eg(x - e)[1]) / (2 * h)
    return (H + H.T) / 2
def polish(X):
    r = minimize(L.eg, np.asarray(X, float).ravel(), jac=True, method='L-BFGS-B', options={'gtol': 1e-12, 'ftol': 1e-16, 'maxiter': 50000})
    x = r.x
    for _ in range(3):
        g = L.eg(x)[1]
        if np.linalg.norm(g) < 1e-12: break
        H = hess(x); w, V = np.linalg.eigh(H); keep = np.abs(w) > 1e-6
        x = x - V[:, keep] @ ((V[:, keep].T @ g) / w[keep])
    return x
if __name__ == '__main__':
    f, N, Et, post, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]
    X = np.loadtxt(f); assert len(X) == N
    x = polish(X); Emp, gmp = eg_mp(x.reshape(-1, 3)); w = np.linalg.eigvalsh(hess(x))
    zero = int((np.abs(w) < 1e-6).sum()); neg = int((w < -1e-6).sum())
    import glue; Ep = L.eg(polish(glue.load(post)))[0]
    np.savetxt(out, x.reshape(-1, 3), fmt='%.15f')
    print(json.dumps({'N': N, 'E_mp': mp.nstr(Emp, 20), 'grad_norm_mp': mp.nstr(gmp, 5), 'grad_ok': bool(gmp < 1e-10),
        'zero_modes': zero, 'negative_modes': neg, 'lowest_nonzero': float(np.sort(np.abs(w))[6]), 'E_table': Et,
        'margin_vs_table': float(Emp) - Et, 'E_posted_polished': float(Ep), 'margin_vs_posted': float(Emp) - float(Ep),
        'certified': bool(gmp < 1e-10 and zero == 6 and neg == 0 and float(Emp) <= Et - 1e-4 and float(Emp) <= Ep - 1e-4)}))
