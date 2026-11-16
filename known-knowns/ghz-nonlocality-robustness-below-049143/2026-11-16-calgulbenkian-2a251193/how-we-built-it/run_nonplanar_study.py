#!/usr/bin/env python3
"""
Lens 1 (Non-Planar 3D Bloch Sphere & Phase-Shifted Polygon Study):
Tests exact critical white-noise visibility v* on |GHZ_3> for:
  0. Calibration: Mermin m=2 (0.5), planar m=6 (50/101), m=8 (0.49316885), m=10 (0.49206349).
  1. Phase-shifted planar polygons (confirming v* = 0.49309520 < 0.49316885 at m=8).
  2. Non-planar 3D Bloch configurations: Z-pole + equatorial polygon (with 2-body ZZ marginals)
     and 3D latitude rings / antiprisms at polar angle theta in (0, pi/2).
"""

import math
import warnings
import numpy as np
from scipy.optimize import linprog

warnings.filterwarnings("ignore")


def ghz3_q(A, B, C, include_marginals=True):
    A = np.asarray(A, dtype=np.float64)
    B = np.asarray(B, dtype=np.float64)
    C = np.asarray(C, dtype=np.float64)
    uA = A[:, 0] + 1j * A[:, 1]
    uB = B[:, 0] + 1j * B[:, 1]
    uC = C[:, 0] + 1j * C[:, 1]
    q3 = np.real(uA[:, None, None] * uB[None, :, None] * uC[None, None, :])
    if not include_marginals:
        return None, None, None, q3
    qAB = A[:, 2][:, None] * B[:, 2][None, :]
    qAC = A[:, 2][:, None] * C[:, 2][None, :]
    qBC = B[:, 2][:, None] * C[:, 2][None, :]
    return qAB, qAC, qBC, q3


def exact_sep_small(JAB, JAC, JBC, M, top_k=24):
    mA, mB, mC = M.shape
    marg = JAB is not None
    if not marg:
        nA = 1 << (mA - 1)
        A_all = np.concatenate([np.ones((nA, 1)), (((np.arange(nA)[:, None] >> np.arange(mA - 1)[None, :]) & 1) * 2.0 - 1.0)], axis=1)
        nB = 1 << (mB - 1)
        B_all = np.concatenate([np.ones((nB, 1)), (((np.arange(nB)[:, None] >> np.arange(mB - 1)[None, :]) & 1) * 2.0 - 1.0)], axis=1)
    else:
        nA = 1 << mA
        A_all = ((np.arange(nA)[:, None] >> np.arange(mA)[None, :]) & 1) * 2.0 - 1.0
        nB = 1 << mB
        B_all = ((np.arange(nB)[:, None] >> np.arange(mB)[None, :]) & 1) * 2.0 - 1.0

    W = (A_all @ M.reshape(mA, mB * mC)).reshape(nA, mB, mC)
    SC = np.einsum("aij,bi->abj", W, B_all, optimize=True)
    if marg:
        SC = SC + (A_all @ JAC)[:, None, :] + (B_all @ JBC)[None, :, :]
        vals = (A_all @ JAB) @ B_all.T + np.sum(np.abs(SC), axis=2)
    else:
        vals = np.sum(np.abs(SC), axis=2)

    best_L = float(np.max(vals))
    k_take = min(top_k, vals.size)
    flat_idx = np.argpartition(vals.ravel(), -k_take)[-k_take:]
    out = []
    for idx in flat_idx:
        ai, bi = divmod(int(idx), nB)
        c = np.where(SC[ai, bi] >= 0.0, 1.0, -1.0)
        out.append((float(vals[ai, bi]), A_all[ai], B_all[bi], c))
    out.sort(key=lambda x: -x[0])
    return best_L, [(a, b, c) for _, a, b, c in out]


def exact_v_small(A, B, C, marg=True, max_iters=180):
    mA, mB, mC = len(A), len(B), len(C)
    qAB, qAC, qBC, q3 = ghz3_q(A, B, C, marg)
    qv = q3.ravel() if not marg else np.concatenate([qAB.ravel(), qAC.ravel(), qBC.ravel(), q3.ravel()])

    vals = np.round(np.abs(qv), 10)
    uvals, inv = np.unique(vals, return_inverse=True)
    keep = uvals > 1e-11
    no = int(np.sum(keep))
    remap = np.full(len(uvals), -1, dtype=np.int32)
    remap[keep] = np.arange(no)
    gid = remap[inv]
    gsgn = np.where(qv >= 0.0, 1.0, -1.0)
    qred = np.array([np.sum(gsgn[gid == r] * qv[gid == r]) for r in range(no)])

    def svec(a, b, c):
        t3 = (a[:, None, None] * b[None, :, None] * c[None, None, :]).ravel()
        if not marg:
            return t3
        return np.concatenate([(a[:, None] * b[None, :]).ravel(), (a[:, None] * c[None, :]).ravel(), (b[:, None] * c[None, :]).ravel(), t3])

    def proj(a, b, c):
        sv = svec(a, b, c)
        mask = gid >= 0
        return np.bincount(gid[mask], weights=gsgn[mask] * sv[mask], minlength=no)

    def lift(w):
        y = np.zeros(len(qv))
        mask = gid >= 0
        y[mask] = gsgn[mask] * w[gid[mask]]
        if not marg:
            return None, None, None, y.reshape(mA, mB, mC)
        n1, n2, n3 = mA * mB, mA * (mB + mC), mA * (mB + mC) + mB * mC
        return y[:n1].reshape(mA, mB), y[n1:n2].reshape(mA, mC), y[n2:n3].reshape(mB, mC), y[n3:].reshape(mA, mB, mC)

    cols = []
    rng = np.random.default_rng(123)
    for _ in range(40):
        d = proj(rng.choice([-1.0, 1.0], mA), rng.choice([-1.0, 1.0], mB), rng.choice([-1.0, 1.0], mC))
        cols.append(d)
        if not marg:
            cols.append(-d)

    best_cert = 1.0
    mu = 0.0
    for _ in range(max_iters):
        D = np.array(cols)
        c_obj = np.zeros(no + 1)
        c_obj[-1] = 1.0
        res = linprog(
            c_obj,
            A_ub=np.hstack([D, -np.ones((len(cols), 1))]),
            b_ub=np.zeros(len(cols)),
            A_eq=np.append(qred, 0.0)[None, :],
            b_eq=[1.0],
            bounds=[(-20.0, 20.0)] * no + [(0.0, None)],
            method="highs",
        )
        w = res.x[:no]
        mu = float(res.x[-1])
        JAB, JAC, JBC, M = lift(w)
        L_ex, strats = exact_sep_small(JAB, JAC, JBC, M, top_k=24)
        if L_ex < best_cert:
            best_cert = L_ex
        if abs(L_ex - mu) < 1e-10:
            break
        for a, b, c in strats:
            d = proj(a, b, c)
            cols.append(d)
            if not marg:
                cols.append(-d)
    return best_cert, mu, no


def xy(m, sh=0.0):
    return [[math.cos(math.pi * k / m + sh), math.sin(math.pi * k / m + sh), 0.0] for k in range(m)]


def ring3d(m, theta, sh=0.0):
    st, ct = math.sin(theta), math.cos(theta)
    return [[st * math.cos(2.0 * math.pi * k / m + sh), st * math.sin(2.0 * math.pi * k / m + sh), ct] for k in range(m)]


if __name__ == "__main__":
    print("=== 0. Calibration ===")
    for m in [2, 6, 8, 10]:
        vc, mu, no = exact_v_small(xy(m), xy(m), xy(m), marg=False)
        print(f"Planar {m}x{m}x{m}: certified v* = {vc:.8f} (lb={mu:.8f}, orbs={no})")

    print("\n=== 1. Phase-Shifted Planar 8x8x8 ===")
    vc_sh, mu_sh, no_sh = exact_v_small(xy(8, 0.0), xy(8, 0.0), xy(8, math.pi / 24.0), marg=False)
    print(f"Shifted planar 8x8x8 (0, 0, pi/24): certified v* = {vc_sh:.8f} (beats unshifted 0.49316885)")

    print("\n=== 2. Non-Planar 3D Bloch: Z-Stabilizer + Equatorial Polygon (with ZZ marginals) ===")
    Z = [[0.0, 0.0, 1.0]]
    for m_eq in [4, 6, 8, 9]:
        V = Z + xy(m_eq)
        vc, mu, no = exact_v_small(V, V, V, marg=True)
        vc_pure, _, _ = exact_v_small(xy(m_eq + 1), xy(m_eq + 1), xy(m_eq + 1), marg=False)
        print(f"Z + XY({m_eq}) ({m_eq+1}^3): certified v* = {vc:.8f} vs pure planar {m_eq+1}^3 = {vc_pure:.8f}")

    print("\n=== 3. Non-Planar 3D Bloch: Tilted Latitude Rings & Antiprisms ===")
    for th_deg in [60.0, 75.0, 85.0, 89.0]:
        th = math.radians(th_deg)
        V_ring = ring3d(8, th)
        vc1, mu1, _ = exact_v_small(V_ring, V_ring, V_ring, marg=True)
        V_anti = ring3d(4, th, 0.0) + ring3d(4, math.pi - th, math.pi / 4.0)
        vc2, mu2, _ = exact_v_small(V_anti, V_anti, V_anti, marg=True)
        print(f"theta={th_deg:4.1f} deg: ring8 certified v* = {vc1:.8f} | antiprism(4+4) certified v* = {vc2:.8f}")
