#!/usr/bin/env python3
"""
Generate high-precision LP solution and integer-quantized Bell functional for
the asymmetric planar (m_A, m_B, m_C) = (18, 24, 72) GHZ_3 configuration, where:
  alpha_i = i * pi / 18   (i = 0..17)
  beta_j  = j * pi / 24   (j = 0..23)
  gamma_k = k * pi / 72   (k = 0..71)
and M_{ijk} = F((4*i + 3*j + k) mod 144), with F(s + 72) = -F(s), F(144 - s) = F(s), F(36) = 0.
Thus M is parameterized by 36 integers w[0..35] = F(0..35).
"""

import json
import math
import warnings
import numpy as np
from scipy.optimize import linprog

warnings.filterwarnings("ignore")


def strong_sep(M, n_restarts=1000, seed=1):
    mA, mB, mC = M.shape
    rng = np.random.default_rng(seed)
    seeds = []
    for sh in range(mA):
        a = np.ones(mA)
        a[:sh] = -1.0
        seeds.append(a)
    for i in range(0, mA, 2):
        for j in range(i + 1, mA):
            for k in range(j + 1, mA, 2):
                a = np.ones(mA)
                a[i:j] = -1.0
                a[k:] = -1.0
                seeds.append(a)
    for _ in range(n_restarts):
        seeds.append(rng.choice([-1.0, 1.0], mA))

    A = np.array(seeds, dtype=np.float64)
    B = rng.choice([-1.0, 1.0], (len(seeds), mB))
    for idx_s in range(min(mB, len(seeds))):
        b = np.ones(mB)
        b[:idx_s] = -1.0
        B[idx_s] = b

    for _ in range(22):
        Wab = np.einsum("si,ijk->sjk", A, M, optimize=True)
        sc = np.einsum("sj,sjk->sk", B, Wab, optimize=True)
        C = np.where(sc >= 0.0, 1.0, -1.0)
        Wac = np.einsum("sk,ijk->sij", C, M, optimize=True)
        sb = np.einsum("si,sij->sj", A, Wac, optimize=True)
        B = np.where(sb >= 0.0, 1.0, -1.0)
        sa = np.einsum("sij,sj->si", Wac, B, optimize=True)
        A = np.where(sa >= 0.0, 1.0, -1.0)

    Wab = np.einsum("si,ijk->sjk", A, M, optimize=True)
    sc = np.einsum("sj,sjk->sk", B, Wab, optimize=True)
    vals = np.sum(np.abs(sc), axis=1)
    C = np.where(sc >= 0.0, 1.0, -1.0)
    order = np.argsort(-vals)
    best_v = float(vals[order[0]])
    uniq, seen = [], set()
    for r in order:
        key = (A[r].tobytes(), B[r].tobytes())
        if key not in seen:
            seen.add(key)
            uniq.append((A[r], B[r], C[r]))
        if len(uniq) >= 60:
            break
    return best_v, uniq


def build_18_24_72_candidate(scale=200000):
    mA, mB, mC = 18, 24, 72
    stA, stB = 4, 3
    N2 = 144
    no = 36  # s in 0..35; s=36 has F(36) = -F(36) = 0

    idx = (stA * np.arange(mA)[:, None, None] + stB * np.arange(mB)[None, :, None] + np.arange(mC)[None, None, :]) % N2
    b_idx = np.full(N2, -1, dtype=np.int32)
    b_sgn = np.zeros(N2, dtype=np.float64)
    for s in range(N2):
        s1 = s if s <= mC else N2 - s
        if s1 < 36:
            b_idx[s] = s1
            b_sgn[s] = 1.0
        elif s1 > 36:
            b_idx[s] = 72 - s1
            b_sgn[s] = -1.0

    gid = b_idx[idx]
    gsgn = b_sgn[idx]
    qt = np.cos(math.pi * idx / mC)
    qred = np.array([np.sum(gsgn[gid == r] * qt[gid == r]) for r in range(no)])

    def proj(a, b, c):
        t = (a[:, None, None] * b[None, :, None] * c[None, None, :]).ravel()
        mask = gid.ravel() >= 0
        return np.bincount(gid.ravel()[mask], weights=gsgn.ravel()[mask] * t[mask], minlength=no)

    def lift(w):
        M = np.zeros((mA, mB, mC), dtype=np.float64)
        mask = gid >= 0
        M[mask] = gsgn[mask] * w[gid[mask]]
        return M

    cols = []
    rng = np.random.default_rng(17)
    for _ in range(80):
        d = proj(rng.choice([-1.0, 1.0], mA), rng.choice([-1.0, 1.0], mB), rng.choice([-1.0, 1.0], mC))
        cols += [d, -d]

    w = np.zeros(no)
    mu = 0.0
    for it in range(400):
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
        M = lift(w)
        Lh, strats = strong_sep(M, n_restarts=1000, seed=1000 + it)
        if abs(Lh - mu) < 1e-11:
            Lh2, strats2 = strong_sep(M, n_restarts=4000, seed=90000 + it)
            if abs(Lh2 - mu) < 1e-11:
                print(f"Converged at iter {it}: mu = {mu:.10f}")
                break
            strats = strats2
        for a, b, c in strats:
            d = proj(a, b, c)
            cols += [d, -d]

    w_int = [int(round(x / np.max(np.abs(w)) * scale)) for x in w]
    M_int = lift(np.array(w_int, dtype=np.float64))
    Lh_int, _ = strong_sep(M_int, n_restarts=4000, seed=4242)
    Q_int = float(np.dot(qred, w_int))
    print(f"Quantized (scale={scale}): L_heur = {int(Lh_int)}, Q = {Q_int:.6f}, v_heur = {Lh_int / Q_int:.10f}")

    out = {
        "mA": mA,
        "mB": mB,
        "mC": mC,
        "stepA": stA,
        "stepB": stB,
        "w_int": w_int,
        "L_heur": int(Lh_int),
        "Q_float": Q_int,
        "v_heur": Lh_int / Q_int,
    }
    with open("candidate_18x24x72.json", "w") as f:
        json.dump(out, f, indent=2)
    print("Wrote candidate_18x24x72.json")


if __name__ == "__main__":
    build_18_24_72_candidate(scale=200000)
