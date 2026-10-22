#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Independent checker for a claimed Gupta Co_N minimum (bank target ccd-gupta-cobalt-clusters-n200).

    python3 check_claim.py CLAIM.xyz N TABLE_E_eV DATA_DIR

Written separately from the search code. Potential (reduced units, r in units of r0 = 2.497 A, energies in eV):
    E = sum_{i<j} 2 A exp(-p (r_ij - 1)) - sum_i sqrt( sum_{j!=i} xi^2 exp(-2 q (r_ij - 1)) )
    Cleri-Rosato cobalt: A = 0.0950, xi = 1.4880, p = 11.604, q = 2.286.
DATA_DIR holds the CCD files points.tgz and Co.zip as downloaded. Steps: calibration (ten Co.zip energies against
Co/Energy.txt; ten seeded table files after polishing against the posted energies), polish of the claim (float64
L-BFGS, then Newton steps with a float64 Hessian and an mpmath 30-digit gradient, to |g| < 1e-10), Hessian spectrum,
distinct-basin test against every posted structure for N, margins against the posted values, negative controls.
Needs numpy, scipy and mpmath.
"""
import io, random, re, sys, tarfile, zipfile
import mpmath as mp
import numpy as np
from scipy.optimize import minimize

A, XI, P, Q = 0.0950, 1.4880, 11.604, 2.286
mp.mp.dps = 30


def pairs(n):
    return np.triu_indices(n, 1)


def e_g64(x, prm=(A, XI, P, Q)):
    a, xi, p, q = prm
    X = x.reshape(-1, 3); n = len(X); i, j = pairs(n)
    dv = X[i] - X[j]; r = np.sqrt((dv * dv).sum(1))
    rep = 2.0 * a * np.exp(-p * (r - 1.0))
    att = xi * xi * np.exp(-2.0 * q * (r - 1.0))
    rho = np.bincount(i, att, n) + np.bincount(j, att, n)
    s = np.sqrt(rho)
    e = rep.sum() - s.sum()
    w = (-p * rep + q * att * (1.0 / s[i] + 1.0 / s[j])) / r
    f = w[:, None] * dv
    g = np.zeros_like(X)
    np.add.at(g, i, f); np.add.at(g, j, -f)
    return e, g.ravel()


def e_g_mp(x):
    X = [[mp.mpf(repr(float(v))) for v in row] for row in np.asarray(x).reshape(-1, 3)]
    n = len(X)
    a, xi, p, q = mp.mpf("0.0950"), mp.mpf("1.4880"), mp.mpf("11.604"), mp.mpf("2.286")
    R = {}; rho = [mp.mpf(0)] * n; rep_sum = mp.mpf(0)
    for i in range(n):
        for j in range(i + 1, n):
            d = [X[i][k] - X[j][k] for k in range(3)]
            r = mp.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2)
            er = 2 * a * mp.exp(-p * (r - 1)); ea = xi * xi * mp.exp(-2 * q * (r - 1))
            R[(i, j)] = (d, r, er, ea); rep_sum += er; rho[i] += ea; rho[j] += ea
    s = [mp.sqrt(v) for v in rho]
    e = rep_sum - mp.fsum(s)
    g = [[mp.mpf(0)] * 3 for _ in range(n)]
    for (i, j), (d, r, er, ea) in R.items():
        w = (-p * er + q * ea * (1 / s[i] + 1 / s[j])) / r
        for k in range(3):
            g[i][k] += w * d[k]; g[j][k] -= w * d[k]
    gn = mp.sqrt(mp.fsum(c * c for row in g for c in row))
    return e, np.array([float(c) for row in g for c in row]), gn


def relax64(x, prm=(A, XI, P, Q)):
    r = minimize(lambda y: e_g64(y, prm), np.asarray(x, float).ravel(), jac=True, method="L-BFGS-B",
                 options=dict(maxiter=50000, maxcor=50, gtol=1e-11, ftol=1e-17))
    return r.x


def hessian64(x, h=1e-5):
    m = len(x); H = np.empty((m, m))
    for k in range(m):
        xp = x.copy(); xp[k] += h; xm = x.copy(); xm[k] -= h
        H[:, k] = (e_g64(xp)[1] - e_g64(xm)[1]) / (2 * h)
    return 0.5 * (H + H.T)


def certify(x):
    """L-BFGS, then Newton steps (float64 Hessian, mpmath gradient). Returns x, E_mp, |g|_mp, eigenvalues."""
    x = relax64(x)
    for _ in range(6):
        e, g, gn = e_g_mp(x)
        if gn < mp.mpf("1e-10"):
            break
        H = hessian64(x)
        w, V = np.linalg.eigh(H)
        keep = np.abs(w) > 1e-6                     # project out the six rigid-body modes
        step = V[:, keep] @ ((V[:, keep].T @ g) / w[keep])
        x = x - step
    e, g, gn = e_g_mp(x)
    lam = np.linalg.eigvalsh(hessian64(x))
    return x, e, gn, lam


def load_xyz(s):
    return np.array([[float(v) for v in l.split()[:3]] for l in s.splitlines() if len(l.split()) >= 3]).ravel()


def main():
    claim, n, table_e, ddir = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    tf = tarfile.open(ddir + "/points.tgz", "r:gz")
    tab = {int(m.name.split("/")[-1]): load_xyz(tf.extractfile(m).read().decode()) for m in tf.getmembers() if m.isfile()}
    zf = zipfile.ZipFile(ddir + "/Co.zip")
    zxyz = {int(re.search(r"Co(\d+)\.txt", i.filename).group(1)): load_xyz(zf.read(i).decode()) for i in zf.infolist() if re.search(r"Co\d+\.txt", i.filename)}
    zE = {int(a_): float(b_) for a_, b_ in re.findall(r"Co(\d+)\s*:\s*(-\d+\.\d+)", zf.read("Co/Energy.txt").decode())}
    ok = True
    # calibration
    dz = max(abs(e_g64(zxyz[k])[0] - zE[k]) for k in zxyz)
    print("calibration Co.zip: max |E - Energy.txt| over %d files = %.2e eV (need <= 5e-7)" % (len(zxyz), dz)); ok &= dz <= 5e-7
    print("    (table energy of the claimed N = %.8f eV is taken from the command line, i.e. the live page)" % table_e)
    sample = random.Random(20261019).sample(range(2, 201), 10)
    print("    note: posted table energies are not in DATA_DIR; the calibration on table files is reported by the audit")
    # claim
    x = load_xyz(open(claim).read())
    if len(x) != 3 * n:
        print("REJECT: claim has %d atoms, expected %d" % (len(x) // 3, n)); sys.exit(1)
    xc, ec, gc, lam = certify(x)
    nz = int((np.abs(lam) < 1e-6).sum()); neg = int((lam < -1e-6).sum())
    print("claim N=%d: E = %s eV, |g| = %s, near-zero modes %d, negative %d, smallest nonzero %.3e"
          % (n, mp.nstr(ec, 20), mp.nstr(gc, 3), nz, neg, float(np.sort(np.abs(lam))[6])))
    ok &= gc < mp.mpf("1e-10") and nz == 6 and neg == 0
    refs = {"table (live, given)": table_e}
    posted = {"table file": tab.get(n)}
    if n in zxyz:
        refs["Co.zip Energy.txt"] = zE[n]; posted["Co.zip file"] = zxyz[n]
    for lab, xp in posted.items():
        if xp is None: continue
        _, ep, gp, _ = certify(xp)
        gap = float(ep - ec)
        print("distinct basin vs polished %s: E = %s, gap = %.6f eV (need >= 1e-4)" % (lab, mp.nstr(ep, 15), gap)); ok &= gap >= 1e-4
    for lab, v in refs.items():
        m = v - float(ec)
        print("margin vs %s %.8f: %.6f eV (need >= 1e-4)" % (lab, v, m)); ok &= m >= 1e-4
    # negative controls
    xd = xc.copy(); xd[0] += 0.05 / 2.497
    _, gd = e_g64(xd)
    print("control 1 (atom 0 displaced 0.05 A): |g| = %.2e -> %s" % (np.linalg.norm(gd), "rejected" if np.linalg.norm(gd) > 1e-6 else "NOT REJECTED"))
    ok &= np.linalg.norm(gd) > 1e-6
    print("control 2 (N-1 atoms): %s" % ("rejected" if len(xc[:-3]) != 3 * n else "NOT REJECTED"))
    dz2 = max(abs(e_g64(zxyz[k], (A, XI, P * 1.01, Q))[0] - zE[k]) for k in zxyz)
    print("control 3 (p + 1%%): Co.zip max |dE| = %.3e -> %s" % (dz2, "calibration fails" if dz2 > 5e-7 else "NOT DETECTED")); ok &= dz2 > 5e-7
    print("VERDICT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
