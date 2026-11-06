#!/usr/bin/env python3
"""Thomson-problem judge, written from the bank definition (thomson-problem-live-tables):

  E(X) = sum_{i<j} 1/|x_i - x_j| for N points on the unit sphere, computed in mpmath at mp.dps = 30
  from the normalised coordinates; certified strict local minimum = tangent-space Newton in mpmath to
  tangent-gradient norm < 1e-20 and all 2N-3 non-rotational tangent-Hessian eigenvalues > 0.

Polish routine (identical for every input):
  1. float64 L-BFGS on y -> y/|y| (scipy), tight tolerances;
  2. float64 Riemannian Newton steps until |g_T| < 1e-9 (at most 8);
  3. mpmath (dps 30) Newton: gradient in mpmath, step from the float64 reduced tangent Hessian, retraction by
     renormalisation in mpmath; until |g_T| < 1e-20 (at most 8 steps).
Hessian test at the final point: float64 Riemannian Hessian in an orthonormal tangent basis, the 3 rotation
generators projected out, smallest of the 2N-3 eigenvalues compared with delta = 10*(2N)*2.22e-16*||H||_F.

Usage:
  certify.py polish <points-file> <out-json> [<out-coords>]   # full polish + Hessian, writes JSON (+ 30-digit coords)
  certify.py check  <points-file> <out-json>                  # NO polish: energy, gradient, Hessian at the file's point
Points file: lines of 3 numbers (x y z); a leading line with a single integer (xyz count) or non-numeric
lines are skipped. Only the python standard library, numpy, scipy and mpmath are used.
"""
import sys, json, time, hashlib
import numpy as np
import mpmath as mp
from scipy.optimize import minimize

mp.mp.dps = 30


def read_points(path):
    rows = []
    with open(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) < 3:
                continue
            try:
                [float(p) for p in parts[-3:]]
            except ValueError:
                continue
            rows.append(parts[-3:])
    return rows


def to_mp_normalised(rows):
    X = []
    for r in rows:
        v = [mp.mpf(s) for s in r]
        n = mp.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
        X.append([v[0] / n, v[1] / n, v[2] / n])
    return X


def mp_energy_grad(X):
    """Energy and Euclidean gradient in mpmath (current mp.dps)."""
    N = len(X)
    E = mp.mpf(0)
    G = [[mp.mpf(0), mp.mpf(0), mp.mpf(0)] for _ in range(N)]
    for i in range(N):
        xi, yi, zi = X[i]
        gi = G[i]
        for j in range(i + 1, N):
            xj = X[j]
            dx = xi - xj[0]; dy = yi - xj[1]; dz = zi - xj[2]
            r2 = dx * dx + dy * dy + dz * dz
            r = mp.sqrt(r2)
            ir = 1 / r
            E += ir
            ir3 = ir / r2
            fx = dx * ir3; fy = dy * ir3; fz = dz * ir3
            gi[0] -= fx; gi[1] -= fy; gi[2] -= fz
            gj = G[j]
            gj[0] += fx; gj[1] += fy; gj[2] += fz
    return E, G


def mp_tangent(X, G):
    """Tangent gradient g_i - (x_i.g_i) x_i, its 2-norm, and the multipliers x_i.g_i (mpmath)."""
    T = []
    lam = []
    s = mp.mpf(0)
    for x, g in zip(X, G):
        l = x[0] * g[0] + x[1] * g[1] + x[2] * g[2]
        t = [g[0] - l * x[0], g[1] - l * x[1], g[2] - l * x[2]]
        T.append(t)
        lam.append(l)
        s += t[0] ** 2 + t[1] ** 2 + t[2] ** 2
    return T, mp.sqrt(s), lam


# ---------------- float64 pieces ----------------

def f64_energy_grad(x):
    d = x[:, None, :] - x[None, :, :]
    r2 = np.einsum('ijk,ijk->ij', d, d)
    np.fill_diagonal(r2, 1.0)
    ir = 1.0 / np.sqrt(r2)
    np.fill_diagonal(ir, 0.0)
    E = 0.5 * ir.sum()
    ir3 = ir ** 3
    g = -np.einsum('ij,ijk->ik', ir3, d)
    return E, g


def f64_tangent_norm(x, g):
    lam = np.einsum('ik,ik->i', x, g)
    gt = g - lam[:, None] * x
    return np.sqrt((gt ** 2).sum()), gt, lam


def tangent_basis(x):
    N = len(x)
    B = np.zeros((N, 3, 2))
    for i in range(N):
        a = np.array([1.0, 0.0, 0.0]) if abs(x[i, 0]) < 0.9 else np.array([0.0, 1.0, 0.0])
        u = a - x[i].dot(a) * x[i]; u /= np.linalg.norm(u)
        v = np.cross(x[i], u); v /= np.linalg.norm(v)
        B[i, :, 0] = u; B[i, :, 1] = v
    return B


def euclid_hessian(x):
    N = len(x)
    d = x[:, None, :] - x[None, :, :]
    r2 = np.einsum('ijk,ijk->ij', d, d)
    np.fill_diagonal(r2, 1.0)
    ir = 1.0 / np.sqrt(r2)
    np.fill_diagonal(ir, 0.0)
    ir3 = ir ** 3
    ir5 = ir3 * ir * ir
    # off-diagonal blocks: I/r^3 - 3 d d^T / r^5
    H = np.einsum('ij,ab->iajb', ir3, np.eye(3)) - 3.0 * np.einsum('ij,ija,ijb->iajb', ir5, d, d)
    for i in range(N):
        H[i, :, i, :] = -H[i, :, :, :].sum(axis=1)  # blocks j != i only (diagonal block zero before this)
    return H.reshape(3 * N, 3 * N)


def reduced_tangent_hessian(x, g):
    """Riemannian Hessian in the tangent basis, rotations projected out. Returns (Hred, Q, B, Ht, rot)."""
    N = len(x)
    B = tangent_basis(x)
    He = euclid_hessian(x)
    lam = np.einsum('ik,ik->i', x, g)
    Bm = np.zeros((3 * N, 2 * N))
    for i in range(N):
        Bm[3 * i:3 * i + 3, 2 * i:2 * i + 2] = B[i]
    Ht = Bm.T @ He @ Bm
    Ht -= np.diag(np.repeat(lam, 2))
    Ht = 0.5 * (Ht + Ht.T)
    rot = np.zeros((2 * N, 3))
    for k in range(3):
        e = np.zeros(3); e[k] = 1.0
        v = np.cross(e, x)  # tangent field of rotation about axis k
        rot[:, k] = np.einsum('ika,ia->ik', B.transpose(0, 2, 1), v).reshape(-1)
    Qfull, _ = np.linalg.qr(np.hstack([rot, np.eye(2 * N)[:, :0]]), mode='complete')
    Qperp = Qfull[:, 3:]
    Hred = Qperp.T @ Ht @ Qperp
    Hred = 0.5 * (Hred + Hred.T)
    return Hred, Qperp, B, Ht, rot


def newton_step_f64(x, g):
    """Tangent Newton step (float64) with rotations projected out; returns per-point 3-vectors."""
    N = len(x)
    _, gt, _ = f64_tangent_norm(x, g)
    Hred, Q, B, _, _ = reduced_tangent_hessian(x, g)
    gT = np.einsum('iak,ia->ik', B, gt).reshape(-1)
    xi = Q @ np.linalg.solve(Hred, -(Q.T @ gT))
    return np.einsum('iak,ik->ia', B, xi.reshape(N, 2))


def lbfgs_polish(x0):
    N = len(x0)

    def fun(yflat):
        y = yflat.reshape(N, 3)
        n = np.linalg.norm(y, axis=1)
        x = y / n[:, None]
        E, g = f64_energy_grad(x)
        lam = np.einsum('ik,ik->i', x, g)
        gy = (g - lam[:, None] * x) / n[:, None]
        return E, gy.reshape(-1)

    res = minimize(fun, x0.reshape(-1), jac=True, method='L-BFGS-B',
                   options={'maxiter': 20000, 'maxcor': 30, 'ftol': 1e-16, 'gtol': 1e-11})
    y = res.x.reshape(N, 3)
    return y / np.linalg.norm(y, axis=1)[:, None], int(res.nit)


def hessian_report(xf, gf):
    Hred, _, _, Ht, rot = reduced_tangent_hessian(xf, gf)
    ev = np.linalg.eigvalsh(Hred)
    fro = float(np.linalg.norm(Ht))
    delta = 10 * Ht.shape[0] * 2.22e-16 * fro
    rq = []
    for k in range(3):
        v = rot[:, k] / np.linalg.norm(rot[:, k])
        rq.append(float(v @ Ht @ v))
    nneg = int((ev <= 0).sum())
    return {
        'n_eigs': int(len(ev)), 'expected_n_eigs': int(2 * len(xf) - 3),
        'min_eig': float(ev[0]), 'second_eig': float(ev[1]), 'max_eig': float(ev[-1]),
        'n_nonpositive': nneg, 'frobenius_norm_Ht': fro, 'delta_bound': delta,
        'rotation_rayleigh_quotients': rq,
        'hessian_pass': bool(len(ev) == 2 * len(xf) - 3 and ev[0] > delta and max(abs(q) for q in rq) < 1e-6),
    }


def fmt(v, n=25):
    return mp.nstr(v, n)


def polish(path):
    t0 = time.time()
    rows = read_points(path)
    N = len(rows)
    X0 = to_mp_normalised(rows)
    E0, G0 = mp_energy_grad(X0)
    _, gn0, _ = mp_tangent(X0, G0)
    log = {'input': path.split('/')[-1], 'input_sha256': hashlib.sha256(open(path, 'rb').read()).hexdigest(),
           'N': N, 'E_input_mp30': fmt(E0), 'gT_input_mp30': fmt(gn0, 6)}
    x = np.array([[float(c) for c in p] for p in X0])
    x, nit = lbfgs_polish(x)
    E, g = f64_energy_grad(x)
    gn, _, _ = f64_tangent_norm(x, g)
    log['lbfgs_iters'] = nit
    log['after_lbfgs_E_f64'] = repr(E); log['after_lbfgs_gT_f64'] = float(gn)
    k = 0
    while gn > 1e-9 and k < 8:
        dx = newton_step_f64(x, g)
        x = x + dx
        x /= np.linalg.norm(x, axis=1)[:, None]
        E, g = f64_energy_grad(x)
        gn, _, _ = f64_tangent_norm(x, g)
        k += 1
    log['f64_newton_steps'] = k; log['after_f64_newton_E'] = repr(E); log['after_f64_newton_gT'] = float(gn)
    # mpmath stage
    X = [[mp.mpf(float(c)) for c in p] for p in x]
    X = [[c / mp.sqrt(p[0] ** 2 + p[1] ** 2 + p[2] ** 2) for c in p] for p in X]
    Em, Gm = mp_energy_grad(X)
    _, gm, _ = mp_tangent(X, Gm)
    E_mp_start = Em
    steps = []
    k = 0
    while gm >= mp.mpf('1e-20') and k < 8:
        xf = np.array([[float(c) for c in p] for p in X])
        gf = np.array([[float(c) for c in gg] for gg in Gm])
        # float64 Newton step driven by the mpmath gradient
        Tm, _, _ = mp_tangent(X, Gm)
        gtf = np.array([[float(c) for c in t] for t in Tm])
        Hred, Q, B, _, _ = reduced_tangent_hessian(xf, gf)
        gT = np.einsum('iak,ia->ik', B, gtf).reshape(-1)
        xi = Q @ np.linalg.solve(Hred, -(Q.T @ gT))
        d3 = np.einsum('iak,ik->ia', B, xi.reshape(N, 2))
        X = [[p[a] + mp.mpf(float(d3[i, a])) for a in range(3)] for i, p in enumerate(X)]
        X = [[c / mp.sqrt(p[0] ** 2 + p[1] ** 2 + p[2] ** 2) for c in p] for p in X]
        Em, Gm = mp_energy_grad(X)
        _, gm, _ = mp_tangent(X, Gm)
        k += 1
        steps.append({'step': k, 'E_mp30': fmt(Em), 'gT_mp30': fmt(gm, 6)})
    log['mp_newton_steps'] = steps
    log['E_star_mp30'] = fmt(Em)
    log['gT_final_mp30'] = fmt(gm, 6)
    log['gT_below_1e-20'] = bool(gm < mp.mpf('1e-20'))
    log['E_change_in_mp_stage'] = fmt(abs(Em - E_mp_start), 6)
    log['E_change_input_to_final'] = fmt(Em - E0, 12)
    xf = np.array([[float(c) for c in p] for p in X])
    gf = np.array([[float(c) for c in gg] for gg in Gm])
    log['hessian'] = hessian_report(xf, gf)
    log['seconds'] = round(time.time() - t0, 1)
    return log, X


def check(path):
    t0 = time.time()
    rows = read_points(path)
    X = to_mp_normalised(rows)
    E, G = mp_energy_grad(X)
    _, gn, _ = mp_tangent(X, G)
    xf = np.array([[float(c) for c in p] for p in X])
    gf = np.array([[float(c) for c in gg] for gg in G])
    return {'input': path.split('/')[-1], 'N': len(rows), 'E_mp30': fmt(E), 'gT_mp30': fmt(gn, 6),
            'min_digits_in_file': min(len(s.lstrip('-+').replace('.', '').split('e')[0].split('E')[0]) for r in rows for s in r),
            'hessian_at_file_point': hessian_report(xf, gf), 'seconds': round(time.time() - t0, 1)}


if __name__ == '__main__':
    mode, path, out = sys.argv[1], sys.argv[2], sys.argv[3]
    if mode == 'polish':
        log, X = polish(path)
        if len(sys.argv) > 4:
            with open(sys.argv[4], 'w') as f:
                for p in X:
                    f.write(' '.join(mp.nstr(c, 30, strip_zeros=False) for c in p) + '\n')
            log['coords_out'] = sys.argv[4].split('/')[-1]
    else:
        log = check(path)
    json.dump(log, open(out, 'w'), indent=1)
    print(json.dumps(log, indent=1))
