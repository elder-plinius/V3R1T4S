"""Fast numpy evaluator for LJ clusters with harmonic zero-point energy (V3R1T4S run 2026-10-31-1915).

E_LJ = 4 sum_{i<j} (r^-12 - r^-6); analytic gradient and Hessian (unit masses);
E_sp = E_LJ + (q/2) sum sqrt(lambda) over the 3N-6 nonzero Hessian eigenvalues, q = 0.01 Xe, 0.03 Ar, 0.095 Ne.
Used only to search and rank. The judge is checker/check_lj_zpe.py (50-digit decimal E and gradient).
"""
import re
import numpy as np

Q = {"Xe": 0.01, "Ar": 0.03, "Ne": 0.095}


def read_xyz(path):
    pts = []
    for line in open(path, encoding="latin-1"):
        t = line.split()
        if len(t) >= 3:
            t = t[-3:]
            try:
                pts.append([float(re.sub(r"[dD]", "e", s)) for s in t])
            except ValueError:
                pass
    return np.array(pts)


def write_xyz(path, x, comment=""):
    x = np.asarray(x).reshape(-1, 3)
    with open(path, "w") as f:
        f.write("%d\n%s\n" % (len(x), comment))
        for p in x:
            f.write("LJ %.17e %.17e %.17e\n" % tuple(p))


def _pair(x):
    d = x[:, None, :] - x[None, :, :]
    r2 = (d * d).sum(-1)
    np.fill_diagonal(r2, np.inf)
    ir2 = 1.0 / r2
    return d, ir2


def energy(x):
    x = x.reshape(-1, 3)
    _, ir2 = _pair(x)
    ir6 = ir2 ** 3
    return 2.0 * float((ir6 * ir6 - ir6).sum())


def eg(x):
    x = x.reshape(-1, 3)
    d, ir2 = _pair(x)
    ir6 = ir2 ** 3
    e = 2.0 * float((ir6 * ir6 - ir6).sum())
    f = (-24.0 * ir6 * ir6 + 12.0 * ir6) * ir2          # dV/d(r^2)
    g = 2.0 * (f[:, :, None] * d).sum(1)
    return e, g.ravel()


def hessian(x):
    x = x.reshape(-1, 3)
    n = len(x)
    d, ir2 = _pair(x)
    ir6 = ir2 ** 3
    f = (-24.0 * ir6 * ir6 + 12.0 * ir6) * ir2           # dV/dr2
    fp = (168.0 * ir6 * ir6 - 48.0 * ir6) * ir2 * ir2     # d2V/dr2^2
    B = 2.0 * f[:, :, None, None] * np.eye(3)[None, None] + 4.0 * fp[:, :, None, None] * d[:, :, :, None] * d[:, :, None, :]
    H = -B.transpose(0, 2, 1, 3).reshape(3 * n, 3 * n)
    diag = B.sum(1)
    for i in range(n):
        H[3 * i:3 * i + 3, 3 * i:3 * i + 3] = diag[i]
    return H


def modes(x):
    lam, V = np.linalg.eigh(hessian(x))
    return lam, V


def zpe_terms(lam):
    """Return (nonzero eigenvalues, zero-mode eigenvalues) by dropping the 6 smallest |lambda|."""
    idx = np.argsort(np.abs(lam))
    return lam[idx[6:]], lam[idx[:6]]


def esp_all(x, lam=None):
    """dict with E_LJ, E_Xe, E_Ar, E_Ne, min nonzero eigenvalue, max |zero mode|."""
    x = x.reshape(-1, 3)
    if lam is None:
        lam = np.linalg.eigvalsh(hessian(x))
    nz, z = zpe_terms(lam)
    e = energy(x)
    s = float(np.sqrt(np.clip(nz, 0, None)).sum())
    out = {"E_LJ": e, "minnz": float(nz.min()), "maxzero": float(np.abs(z).max())}
    for sp, q in Q.items():
        out["E_" + sp] = e + 0.5 * q * s
    return out


def lbfgs(x, gtol=1e-6, maxit=5000, m=10, maxstep=0.3):
    """Minimise E_LJ on the classical surface. gtol is on the rms gradient."""
    x = np.array(x, dtype=float).ravel()
    e, g = eg(x)
    S, Y = [], []
    n = len(x)
    for it in range(maxit):
        if np.sqrt(g @ g / n) < gtol:
            break
        q = g.copy()
        al = []
        for s, y in zip(reversed(S), reversed(Y)):
            rho = 1.0 / (y @ s)
            a = rho * (s @ q)
            q -= a * y
            al.append((rho, a, s, y))
        gamma = (S[-1] @ Y[-1]) / (Y[-1] @ Y[-1]) if S else 1e-3
        r = gamma * q
        for rho, a, s, y in reversed(al):
            b = rho * (y @ r)
            r += s * (a - b)
        p = -r
        if p @ g > 0:
            S.clear(); Y.clear()
            p = -1e-3 * g
        pn = np.sqrt(p @ p)
        if pn > maxstep:
            p *= maxstep / pn
        for _ in range(30):
            xn = x + p
            en, gn = eg(xn)
            if en <= e + 1e-12 * abs(e):
                break
            p *= 0.5
        s = xn - x
        y = gn - g
        if y @ s > 1e-14:
            S.append(s); Y.append(y)
            if len(S) > m:
                S.pop(0); Y.pop(0)
        x, e, g = xn, en, gn
    return x, e, float(np.sqrt(g @ g / n)), it


def newton_polish(x, steps=30, tol=1e-13):
    """Newton steps on the classical surface in the space of nonzero modes. Only for points near a minimum."""
    x = np.array(x, dtype=float).ravel()
    for k in range(steps):
        e, g = eg(x)
        if np.sqrt(g @ g) < tol:
            break
        lam, V = np.linalg.eigh(hessian(x))
        idx = np.argsort(np.abs(lam))[6:]
        c = V[:, idx].T @ g
        x = x - V[:, idx] @ (c / lam[idx])
    e, g = eg(x)
    return x, e, float(np.sqrt(g @ g))


def connected(x, rcut=1.7):
    x = x.reshape(-1, 3)
    d = np.sqrt(((x[:, None] - x[None]) ** 2).sum(-1))
    adj = d < rcut
    seen = {0}
    stack = [0]
    while stack:
        i = stack.pop()
        for j in np.nonzero(adj[i])[0]:
            if j not in seen:
                seen.add(int(j)); stack.append(int(j))
    return len(seen) == len(x)


def quench_check(x, gtol=1e-6):
    """Quench, then classify: returns (x, props) where props has E_* and 'ok' (a minimum, connected)."""
    x, e, grms, it = lbfgs(x, gtol=gtol)
    lam = np.linalg.eigvalsh(hessian(x))
    p = esp_all(x, lam)
    p["grms"] = grms
    p["ok"] = (p["minnz"] > 1e-5) and connected(x)
    return x, p
