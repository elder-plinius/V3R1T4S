#!/usr/bin/env python3
"""
Standalone rigorous interval-arithmetic verifier for the 4-to-1 qubit QRAC
with shared randomness optimality certificate (p(4) <= 0.741481 + 10^-6).

Uses ONLY Python standard library + mpmath.iv (directed outward rounding at
40 decimal digits / >130 bits of precision). No C++ solver code is trusted.

Verification steps:
  1. Calibration checks:
     - n = 2 orthogonal Bloch vectors -> 1/2 + 1/(2*sqrt(2)) = 0.85355339...
     - n = 3 orthogonal Bloch vectors -> 1/2 + 1/(2*sqrt(3)) = 0.78867513...
     - n = 4 Ambainis configuration z* = (0, 0, 1, 0, 1) ->
       1/2 + (1 + sqrt(3)) / (8 * sqrt(2)) = 0.741481456572267...
     - Rank-4 elliptope negative check: G = I_4 gives 0.75 > 0.741482.
     - Constructive O(3) x (S_4 x| Z_2^4) symmetry-reduction check on
       deterministic test configurations in (S^2)^4.
  2. Exact dyadic partition check:
     - Traverses the preorder binary split tree from the exact root box
       [-1, 1] x [-1, 1] x [0, 1] x [-1, 1] x [0, 1] using exact rational
       (fractions.Fraction) endpoints, ensuring zero gaps and exact match
       against all header metadata counts.
  3. Outward-rounded mpmath.iv certification on every leaf:
     - 'S4'..'S9': strict interval exclusion from the canonical symmetry
       domain F.
     - 'A': singularity-free AM-GM rational quadratic Taylor upper bound
       <= 0.741482.
     - 'Q': smooth 2nd-order Taylor / concave-quadratic tangent upper bound
       (with interval LDL^T verification of -H_mid > 0) <= 0.741482.
     - 'H': strict interval LDL^T verification of -H(B) > 0 around z*.
"""

from fractions import Fraction
from functools import lru_cache
import json
import math
import os
import sys

from mpmath import iv, mp

mp.dps = 40
iv.dps = 40

SIGNS = (
    (1, -1, -1, -1),
    (1, -1, -1, 1),
    (1, -1, 1, -1),
    (1, -1, 1, 1),
    (1, 1, -1, -1),
    (1, 1, -1, 1),
    (1, 1, 1, -1),
    (1, 1, 1, 1),
)

IV_ZERO = iv.mpf(0)
IV_ONE = iv.mpf(1)
IV_TWO = iv.mpf(2)
IV_FOUR = iv.mpf(4)
IV_HALF = iv.mpf("0.5")
IV_INV64 = IV_ONE / iv.mpf(64)
IV_INV128 = IV_ONE / iv.mpf(128)
V1_IV = (IV_ZERO, IV_ZERO, IV_ONE)


def lo_mpf(x):
    """Exact lower endpoint of an iv.mpf interval as a scalar mp.mpf."""
    return mp.mpf(x.a)


def hi_mpf(x):
    """Exact upper endpoint of an iv.mpf interval as a scalar mp.mpf."""
    return mp.mpf(x.b)


@lru_cache(maxsize=None)
def frac_to_iv(q: Fraction):
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)


@lru_cache(maxsize=None)
def box1d_iv(lo_q: Fraction, hi_q: Fraction):
    return iv.mpf([lo_mpf(frac_to_iv(lo_q)), hi_mpf(frac_to_iv(hi_q))])


def iv_sqr(x):
    """Rigorous outward-rounded square with non-negativity on intervals straddling 0."""
    sq = x * x
    xa = lo_mpf(x)
    xb = hi_mpf(x)
    sq_a = lo_mpf(sq)
    sq_b = hi_mpf(sq)
    if xa <= 0 <= xb or sq_a < 0:
        return iv.mpf([0, sq_b])
    return iv.mpf([sq_a, sq_b])


def iv_mag_mpf(x):
    xa = abs(lo_mpf(x))
    xb = abs(hi_mpf(x))
    return xa if xa >= xb else xb


def iv_clamp_unit(x):
    xa = lo_mpf(x)
    xb = hi_mpf(x)
    lo = xa if xa > mp.mpf(-1) else mp.mpf(-1)
    hi = xb if xb < mp.mpf(1) else mp.mpf(1)
    if lo > hi:
        raise ValueError("Empty unit-clamped interval")
    return iv.mpf([lo, hi])


def clamp_unit3(v):
    return (iv_clamp_unit(v[0]), iv_clamp_unit(v[1]), iv_clamp_unit(v[2]))


def dot3(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def scale3(s, v):
    return (s * v[0], s * v[1], s * v[2])


def stereo_pos(a, b):
    a2 = iv_sqr(a)
    b2 = iv_sqr(b)
    d = IV_ONE + a2 + b2
    inv_d = IV_ONE / d
    return (IV_TWO * a * inv_d, IV_TWO * b * inv_d, (IV_ONE - a2 - b2) * inv_d)


def stereo_jet1(a, b):
    a2 = iv_sqr(a)
    b2 = iv_sqr(b)
    d = IV_ONE + a2 + b2
    inv_d = IV_ONE / d
    inv_d2 = iv_sqr(inv_d)
    v = (IV_TWO * a * inv_d, IV_TWO * b * inv_d, (IV_ONE - a2 - b2) * inv_d)
    c_va = iv.mpf(-4) * a * inv_d2
    va = (IV_TWO * inv_d + c_va * a, c_va * b, c_va)
    c_vb = iv.mpf(-4) * b * inv_d2
    vb = (c_vb * a, IV_TWO * inv_d + c_vb * b, c_vb)
    return v, va, vb


def stereo_jet2(a, b):
    a2 = iv_sqr(a)
    b2 = iv_sqr(b)
    d = IV_ONE + a2 + b2
    inv_d = IV_ONE / d
    inv_d2 = iv_sqr(inv_d)
    inv_d3 = inv_d2 * inv_d
    v = (IV_TWO * a * inv_d, IV_TWO * b * inv_d, (IV_ONE - a2 - b2) * inv_d)
    c_va = iv.mpf(-4) * a * inv_d2
    va = (IV_TWO * inv_d + c_va * a, c_va * b, c_va)
    c_vb = iv.mpf(-4) * b * inv_d2
    vb = (c_vb * a, IV_TWO * inv_d + c_vb * b, c_vb)

    k_aa = iv.mpf(16) * a2 * inv_d3 - IV_FOUR * inv_d2
    vaa = (iv.mpf(-8) * a * inv_d2 + k_aa * a, k_aa * b, k_aa)
    k_bb = iv.mpf(16) * b2 * inv_d3 - IV_FOUR * inv_d2
    vbb = (k_bb * a, iv.mpf(-8) * b * inv_d2 + k_bb * b, k_bb)
    k_ab = iv.mpf(16) * a * b * inv_d3
    vab = (iv.mpf(-4) * b * inv_d2 + k_ab * a, iv.mpf(-4) * a * inv_d2 + k_ab * b, k_ab)
    return v, va, vb, vaa, vbb, vab


def quad1d_ub_iv(g_iv, h_iv, r_iv):
    """
    Rigorous interval upper bound on max_{y in [-r, r]} (g * y + 0.5 * h * y^2)
    for any g in g_iv and h in h_iv, where r = r_iv >= 0.
    """
    g_mag = iv_mag_mpf(g_iv)
    g_abs = iv.mpf(g_mag)
    h_hi = hi_mpf(h_iv)
    if h_hi >= 0:
        return g_abs * r_iv + IV_HALF * iv.mpf(h_hi) * iv_sqr(r_iv)
    neg_h = iv.mpf(-h_hi)
    prod = neg_h * r_iv
    if g_mag >= hi_mpf(prod):
        return g_abs * r_iv - IV_HALF * neg_h * iv_sqr(r_iv)
    if g_mag <= lo_mpf(prod):
        return iv_sqr(g_abs) / (IV_TWO * neg_h)
    cand1 = g_abs * r_iv - IV_HALF * neg_h * iv_sqr(r_iv)
    cand2 = iv_sqr(g_abs) / (IV_TWO * neg_h)
    return iv.mpf([min(lo_mpf(cand1), lo_mpf(cand2)), max(hi_mpf(cand1), hi_mpf(cand2))])


def is_spd_ldlt_iv(M):
    """
    Rigorous interval LDL^T verification that symmetric 5x5 interval matrix M
    contains only strictly positive definite matrices (every pivot D[j] > 0).
    """
    L = [[IV_ZERO] * 5 for _ in range(5)]
    D = [IV_ZERO] * 5
    for j in range(5):
        s = M[j][j]
        for k in range(j):
            s = s - iv_sqr(L[j][k]) * D[k]
        if not (lo_mpf(s) > 0):
            return False
        D[j] = s
        for i in range(j + 1, 5):
            sij = M[i][j]
            for k in range(j):
                sij = sij - L[i][k] * L[j][k] * D[k]
            L[i][j] = sij / D[j]
    return True


def eval_qrac_n(vectors):
    """Evaluate n-to-1 QRAC success probability in mpmath.iv for given 3D interval vectors."""
    n = len(vectors)
    total = IV_ZERO
    half_count = 1 << (n - 1)
    for mask in range(half_count):
        wx, wy, wz = vectors[0]
        for k in range(1, n):
            sgn = 1 if ((mask >> (k - 1)) & 1) else -1
            vk = vectors[k]
            if sgn == 1:
                wx = wx + vk[0]
                wy = wy + vk[1]
                wz = wz + vk[2]
            else:
                wx = wx - vk[0]
                wy = wy - vk[1]
                wz = wz - vk[2]
        q = iv_sqr(wx) + iv_sqr(wy) + iv_sqr(wz)
        total = total + iv.sqrt(q)
    denom = iv.mpf(n * (1 << n))
    return IV_HALF + total / denom


def run_calibration_checks():
    tol = mp.mpf("1e-34")
    e1 = (IV_ONE, IV_ZERO, IV_ZERO)
    e2 = (IV_ZERO, IV_ONE, IV_ZERO)
    e3 = (IV_ZERO, IV_ZERO, IV_ONE)

    # 1. n = 2 calibration: 1/2 + 1/(2*sqrt(2)) = 0.85355339059327376...
    p2_iv = eval_qrac_n([e3, e1])
    p2_exact = IV_HALF + IV_ONE / (IV_TWO * iv.sqrt(IV_TWO))
    if not (lo_mpf(p2_iv) <= hi_mpf(p2_exact) and lo_mpf(p2_exact) <= hi_mpf(p2_iv)):
        raise AssertionError("n=2 calibration interval mismatch")
    if (hi_mpf(p2_iv) - lo_mpf(p2_iv)) > tol:
        raise AssertionError("n=2 calibration interval too wide")

    # 2. n = 3 calibration: 1/2 + 1/(2*sqrt(3)) = 0.78867513459481288...
    p3_iv = eval_qrac_n([e3, e1, e2])
    p3_exact = IV_HALF + IV_ONE / (IV_TWO * iv.sqrt(iv.mpf(3)))
    if not (lo_mpf(p3_iv) <= hi_mpf(p3_exact) and lo_mpf(p3_exact) <= hi_mpf(p3_iv)):
        raise AssertionError("n=3 calibration interval mismatch")
    if (hi_mpf(p3_iv) - lo_mpf(p3_iv)) > tol:
        raise AssertionError("n=3 calibration interval too wide")

    # 3. n = 4 Ambainis construction at z* = (0, 0, 1, 0, 1):
    v2_star = stereo_pos(IV_ZERO, IV_ZERO)
    v3_star = stereo_pos(IV_ONE, IV_ZERO)
    v4_star = stereo_pos(IV_ZERO, IV_ONE)
    p4_iv = eval_qrac_n([e3, v2_star, v3_star, v4_star])
    p4_exact = IV_HALF + (IV_ONE + iv.sqrt(iv.mpf(3))) / (iv.mpf(8) * iv.sqrt(IV_TWO))
    if not (lo_mpf(p4_iv) <= hi_mpf(p4_exact) and lo_mpf(p4_exact) <= hi_mpf(p4_iv)):
        raise AssertionError("n=4 Ambainis calibration interval mismatch")
    if (hi_mpf(p4_iv) - lo_mpf(p4_iv)) > tol:
        raise AssertionError("n=4 Ambainis calibration interval too wide")

    # 4. Negative check: Rank-4 correlation matrix G = I_4 in E_4 gives 0.75 > 0.741482:
    p4_rank4 = IV_HALF + iv.mpf(8) * iv.sqrt(IV_FOUR) * IV_INV64
    if not (lo_mpf(p4_rank4) > mp.mpf("0.749999")):
        raise AssertionError("Rank-4 negative calibration check failed")

    # 5. Constructive symmetry-reduction sanity check on 25 deterministic configurations in (S^2)^4:
    for seed in range(1, 26):
        raw_vecs = []
        for k in range(4):
            t1 = mp.mpf(((seed * 7 + k * 13) % 23) - 11) / mp.mpf(9)
            t2 = mp.mpf(((seed * 11 + k * 5) % 19) - 9) / mp.mpf(8)
            denom = 1 + t1 * t1 + t2 * t2
            vx = 2 * t1 / denom
            vy = 2 * t2 / denom
            vz = (1 - t1 * t1 - t2 * t2) / denom
            if (seed + k) % 2 == 1:
                vx, vy, vz = -vx, -vy, -vz
            raw_vecs.append([vx, vy, vz])

        p_orig = eval_qrac_n([(iv.mpf(v[0]), iv.mpf(v[1]), iv.mpf(v[2])) for v in raw_vecs])

        best_abs = mp.mpf(-1)
        best_pair = (0, 1)
        for i in range(4):
            for j in range(i + 1, 4):
                d_ij = abs(
                    raw_vecs[i][0] * raw_vecs[j][0]
                    + raw_vecs[i][1] * raw_vecs[j][1]
                    + raw_vecs[i][2] * raw_vecs[j][2]
                )
                if d_ij > best_abs:
                    best_abs = d_ij
                    best_pair = (i, j)
        rem = [k for k in range(4) if k not in best_pair]
        order = [best_pair[0], best_pair[1], rem[0], rem[1]]
        vecs = [list(raw_vecs[k]) for k in order]

        for k in (1, 2, 3):
            if vecs[0][0] * vecs[k][0] + vecs[0][1] * vecs[k][1] + vecs[0][2] * vecs[k][2] < 0:
                vecs[k] = [-vecs[k][0], -vecs[k][1], -vecs[k][2]]
        d02 = vecs[0][0] * vecs[2][0] + vecs[0][1] * vecs[2][1] + vecs[0][2] * vecs[2][2]
        d03 = vecs[0][0] * vecs[3][0] + vecs[0][1] * vecs[3][1] + vecs[0][2] * vecs[3][2]
        if d03 > d02:
            vecs[2], vecs[3] = vecs[3], vecs[2]

        f3 = vecs[0]
        proj = vecs[2][0] * f3[0] + vecs[2][1] * f3[1] + vecs[2][2] * f3[2]
        ux = vecs[2][0] - proj * f3[0]
        uy = vecs[2][1] - proj * f3[1]
        uz = vecs[2][2] - proj * f3[2]
        unorm = mp.sqrt(ux * ux + uy * uy + uz * uz)
        f1 = [ux / unorm, uy / unorm, uz / unorm]
        f2 = [
            f3[1] * f1[2] - f3[2] * f1[1],
            f3[2] * f1[0] - f3[0] * f1[2],
            f3[0] * f1[1] - f3[1] * f1[0],
        ]
        if vecs[3][0] * f2[0] + vecs[3][1] * f2[1] + vecs[3][2] * f2[2] < 0:
            f2 = [-f2[0], -f2[1], -f2[2]]

        def to_frame(v):
            return [
                v[0] * f1[0] + v[1] * f1[1] + v[2] * f1[2],
                v[0] * f2[0] + v[1] * f2[1] + v[2] * f2[2],
                v[0] * f3[0] + v[1] * f3[1] + v[2] * f3[2],
            ]

        w2 = to_frame(vecs[1])
        w3 = to_frame(vecs[2])
        w4 = to_frame(vecs[3])
        a2 = w2[0] / (1 + w2[2])
        b2 = w2[1] / (1 + w2[2])
        c = w3[0] / (1 + w3[2])
        a4 = w4[0] / (1 + w4[2])
        b4 = w4[1] / (1 + w4[2])

        if not (-1 <= a2 <= 1 and -1 <= b2 <= 1 and 0 <= c <= 1 and -1 <= a4 <= 1 and 0 <= b4 <= 1):
            raise AssertionError("Symmetry reduction left root box D")
        if not (a2 * a2 + b2 * b2 <= c * c + mp.mpf("1e-35") <= a4 * a4 + b4 * b4 + mp.mpf("2e-35") <= 1 + mp.mpf("3e-35")):
            raise AssertionError("Symmetry reduction violated radial ordering")
        p_red = eval_qrac_n([
            V1_IV,
            stereo_pos(iv.mpf(a2), iv.mpf(b2)),
            stereo_pos(iv.mpf(c), IV_ZERO),
            stereo_pos(iv.mpf(a4), iv.mpf(b4)),
        ])
        if abs(lo_mpf(p_orig) - lo_mpf(p_red)) > mp.mpf("1e-32"):
            raise AssertionError("Symmetry reduction failed invariance check")

    return hi_mpf(p2_iv), hi_mpf(p3_iv), hi_mpf(p4_iv)


def verify_sym_leaf(code: int, lo_f, hi_f):
    a2 = box1d_iv(lo_f[0], hi_f[0])
    b2 = box1d_iv(lo_f[1], hi_f[1])
    c = box1d_iv(lo_f[2], hi_f[2])
    a4 = box1d_iv(lo_f[3], hi_f[3])
    b4 = box1d_iv(lo_f[4], hi_f[4])

    if code == 4:
        r4_sq = iv_sqr(a4) + iv_sqr(b4)
        return lo_mpf(r4_sq) > mp.mpf(1)
    if code == 5:
        r2_sq = iv_sqr(a2) + iv_sqr(b2)
        c_sq = iv_sqr(c)
        return lo_mpf(r2_sq) > hi_mpf(c_sq)
    if code == 6:
        r4_sq = iv_sqr(a4) + iv_sqr(b4)
        c_sq = iv_sqr(c)
        return hi_mpf(r4_sq) < lo_mpf(c_sq)

    v2 = stereo_pos(a2, b2)
    g12_hi = hi_mpf(v2[2])
    if code == 7:
        v3 = stereo_pos(c, IV_ZERO)
        return lo_mpf(abs(dot3(v2, v3))) > g12_hi
    if code == 8:
        v4 = stereo_pos(a4, b4)
        return lo_mpf(abs(dot3(v2, v4))) > g12_hi
    if code == 9:
        v3 = stereo_pos(c, IV_ZERO)
        v4 = stereo_pos(a4, b4)
        return lo_mpf(abs(dot3(v3, v4))) > g12_hi
    return False


def verify_amgm_leaf(lo_f, hi_f):
    m_f = [(lo_f[i] + hi_f[i]) / 2 for i in range(5)]
    r_f = [(hi_f[i] - lo_f[i]) / 2 for i in range(5)]

    m_iv = [frac_to_iv(q) for q in m_f]
    r_iv = [frac_to_iv(q) for q in r_f]
    box_iv = [box1d_iv(lo_f[i], hi_f[i]) for i in range(5)]

    # Fast float midpoint strictly for choosing positive AM-GM weights rho_s > 0
    m_flt = [float(q) for q in m_f]
    d2f = 1.0 + m_flt[0] * m_flt[0] + m_flt[1] * m_flt[1]
    v2f = (2.0 * m_flt[0] / d2f, 2.0 * m_flt[1] / d2f, (1.0 - m_flt[0] * m_flt[0] - m_flt[1] * m_flt[1]) / d2f)
    d3f = 1.0 + m_flt[2] * m_flt[2]
    v3f = (2.0 * m_flt[2] / d3f, 0.0, (1.0 - m_flt[2] * m_flt[2]) / d3f)
    d4f = 1.0 + m_flt[3] * m_flt[3] + m_flt[4] * m_flt[4]
    v4f = (2.0 * m_flt[3] / d4f, 2.0 * m_flt[4] / d4f, (1.0 - m_flt[3] * m_flt[3] - m_flt[4] * m_flt[4]) / d4f)

    C0 = IV_HALF
    alpha12 = IV_ZERO
    alpha13 = IV_ZERO
    alpha14 = IV_ZERO
    alpha23 = IV_ZERO
    alpha24 = IV_ZERO
    alpha34 = IV_ZERO

    for _, s2i, s3i, s4i in SIGNS:
        wx = s2i * v2f[0] + s3i * v3f[0] + s4i * v4f[0]
        wy = s2i * v2f[1] + s3i * v3f[1] + s4i * v4f[1]
        wz = 1.0 + s2i * v2f[2] + s3i * v3f[2] + s4i * v4f[2]
        rho_flt = max(math.sqrt(wx * wx + wy * wy + wz * wz), 0.02)
        if not (rho_flt > 0.0 and math.isfinite(rho_flt)):
            raise ValueError("Invalid rho_flt")
        rho = iv.mpf(rho_flt)
        if not (lo_mpf(rho) > 0):
            raise ValueError("Non-positive rho interval")
        inv_rho = IV_ONE / rho
        C0 = C0 + (rho + IV_FOUR * inv_rho) * IV_INV128
        w_s = inv_rho * IV_INV64
        alpha12 = alpha12 + (w_s if s2i == 1 else -w_s)
        alpha13 = alpha13 + (w_s if s3i == 1 else -w_s)
        alpha14 = alpha14 + (w_s if s4i == 1 else -w_s)
        alpha23 = alpha23 + (w_s if (s2i * s3i) == 1 else -w_s)
        alpha24 = alpha24 + (w_s if (s2i * s4i) == 1 else -w_s)
        alpha34 = alpha34 + (w_s if (s3i * s4i) == 1 else -w_s)

    M2_v, M2_va, M2_vb = stereo_jet1(m_iv[0], m_iv[1])
    M3_v, M3_va, _ = stereo_jet1(m_iv[2], IV_ZERO)
    M4_v, M4_va, M4_vb = stereo_jet1(m_iv[3], m_iv[4])

    Lm = (
        C0
        + alpha12 * M2_v[2]
        + alpha13 * M3_v[2]
        + alpha14 * M4_v[2]
        + alpha23 * dot3(M2_v, M3_v)
        + alpha24 * dot3(M2_v, M4_v)
        + alpha34 * dot3(M3_v, M4_v)
    )

    u2m = (
        alpha23 * M3_v[0] + alpha24 * M4_v[0],
        alpha23 * M3_v[1] + alpha24 * M4_v[1],
        alpha12 + alpha23 * M3_v[2] + alpha24 * M4_v[2],
    )
    u3m = (
        alpha23 * M2_v[0] + alpha34 * M4_v[0],
        alpha23 * M2_v[1] + alpha34 * M4_v[1],
        alpha13 + alpha23 * M2_v[2] + alpha34 * M4_v[2],
    )
    u4m = (
        alpha24 * M2_v[0] + alpha34 * M3_v[0],
        alpha24 * M2_v[1] + alpha34 * M3_v[1],
        alpha14 + alpha24 * M2_v[2] + alpha34 * M3_v[2],
    )
    gL = (
        dot3(u2m, M2_va),
        dot3(u2m, M2_vb),
        dot3(u3m, M3_va),
        dot3(u4m, M4_va),
        dot3(u4m, M4_vb),
    )

    J2_v, J2_va, J2_vb, J2_vaa, J2_vbb, J2_vab = stereo_jet2(box_iv[0], box_iv[1])
    J3_v, J3_va, _, J3_vaa, _, _ = stereo_jet2(box_iv[2], IV_ZERO)
    J4_v, J4_va, J4_vb, J4_vaa, J4_vbb, J4_vab = stereo_jet2(box_iv[3], box_iv[4])

    U2 = (
        alpha23 * J3_v[0] + alpha24 * J4_v[0],
        alpha23 * J3_v[1] + alpha24 * J4_v[1],
        alpha12 + alpha23 * J3_v[2] + alpha24 * J4_v[2],
    )
    U3 = (
        alpha23 * J2_v[0] + alpha34 * J4_v[0],
        alpha23 * J2_v[1] + alpha34 * J4_v[1],
        alpha13 + alpha23 * J2_v[2] + alpha34 * J4_v[2],
    )
    U4 = (
        alpha24 * J2_v[0] + alpha34 * J3_v[0],
        alpha24 * J2_v[1] + alpha34 * J3_v[1],
        alpha14 + alpha24 * J2_v[2] + alpha34 * J3_v[2],
    )

    HL_diag = (
        dot3(U2, J2_vaa),
        dot3(U2, J2_vbb),
        dot3(U3, J3_vaa),
        dot3(U4, J4_vaa),
        dot3(U4, J4_vbb),
    )

    ub = Lm
    for i in range(5):
        ub = ub + quad1d_ub_iv(gL[i], HL_diag[i], r_iv[i])

    off_terms = (
        (dot3(U2, J2_vab), r_iv[0] * r_iv[1]),
        (dot3(U4, J4_vab), r_iv[3] * r_iv[4]),
        (alpha23 * dot3(J2_va, J3_va), r_iv[0] * r_iv[2]),
        (alpha23 * dot3(J2_vb, J3_va), r_iv[1] * r_iv[2]),
        (alpha24 * dot3(J2_va, J4_va), r_iv[0] * r_iv[3]),
        (alpha24 * dot3(J2_va, J4_vb), r_iv[0] * r_iv[4]),
        (alpha24 * dot3(J2_vb, J4_va), r_iv[1] * r_iv[3]),
        (alpha24 * dot3(J2_vb, J4_vb), r_iv[1] * r_iv[4]),
        (alpha34 * dot3(J3_va, J4_va), r_iv[2] * r_iv[3]),
        (alpha34 * dot3(J3_va, J4_vb), r_iv[2] * r_iv[4]),
    )
    for coeff_iv, rr in off_terms:
        ub = ub + iv.mpf(iv_mag_mpf(coeff_iv)) * rr

    return hi_mpf(ub)


def verify_quad_or_star_leaf(kind: str, lo_f, hi_f, threshold_mpf):
    m_f = [(lo_f[i] + hi_f[i]) / 2 for i in range(5)]
    r_f = [(hi_f[i] - lo_f[i]) / 2 for i in range(5)]

    m_iv = [frac_to_iv(q) for q in m_f]
    r_iv = [frac_to_iv(q) for q in r_f]
    box_iv = [box1d_iv(lo_f[i], hi_f[i]) for i in range(5)]

    J2_v, J2_va, J2_vb, J2_vaa, J2_vbb, J2_vab = stereo_jet2(box_iv[0], box_iv[1])
    J3_v, J3_va, _, J3_vaa, _, _ = stereo_jet2(box_iv[2], IV_ZERO)
    J4_v, J4_va, J4_vb, J4_vaa, J4_vbb, J4_vab = stereo_jet2(box_iv[3], box_iv[4])

    M2_v, M2_va, M2_vb = stereo_jet1(m_iv[0], m_iv[1])
    M3_v, M3_va, _ = stereo_jet1(m_iv[2], IV_ZERO)
    M4_v, M4_va, M4_vb = stereo_jet1(m_iv[3], m_iv[4])

    best_ub = mp.mpf("inf")

    if kind == "Q":
        naive_sum = IV_ZERO
        p0_smooth = IV_HALF
        p0_nonsmooth_hi = IV_ZERO
        G1 = [IV_ZERO] * 5
        all_smooth = True

        for _, s2i, s3i, s4i in SIGNS:
            s2 = iv.mpf(s2i)
            s3 = iv.mpf(s3i)
            s4 = iv.mpf(s4i)
            w = (
                s2 * J2_v[0] + s3 * J3_v[0] + s4 * J4_v[0],
                s2 * J2_v[1] + s3 * J3_v[1] + s4 * J4_v[1],
                IV_ONE + s2 * J2_v[2] + s3 * J3_v[2] + s4 * J4_v[2],
            )
            q = dot3(w, w)
            q_b = hi_mpf(q)
            q_hi = q_b if q_b > 0 else mp.mpf(0)
            q_hi_sqrt = iv.sqrt(iv.mpf([0, q_hi]))
            naive_sum = naive_sum + q_hi_sqrt
            if lo_mpf(q) > 0:
                r = iv.sqrt(q)
                wh = clamp_unit3(scale3(IV_ONE / r, w))
                G1[0] = G1[0] + s2 * dot3(wh, J2_va) * IV_INV64
                G1[1] = G1[1] + s2 * dot3(wh, J2_vb) * IV_INV64
                G1[2] = G1[2] + s3 * dot3(wh, J3_va) * IV_INV64
                G1[3] = G1[3] + s4 * dot3(wh, J4_va) * IV_INV64
                G1[4] = G1[4] + s4 * dot3(wh, J4_vb) * IV_INV64

                wm = (
                    s2 * M2_v[0] + s3 * M3_v[0] + s4 * M4_v[0],
                    s2 * M2_v[1] + s3 * M3_v[1] + s4 * M4_v[1],
                    IV_ONE + s2 * M2_v[2] + s3 * M3_v[2] + s4 * M4_v[2],
                )
                p0_smooth = p0_smooth + iv.sqrt(dot3(wm, wm)) * IV_INV64
            else:
                all_smooth = False
                p0_nonsmooth_hi = p0_nonsmooth_hi + q_hi_sqrt * IV_INV64

        ub_naive = hi_mpf(IV_HALF + naive_sum * IV_INV64)
        ub_mv1_iv = p0_smooth + p0_nonsmooth_hi
        for i in range(5):
            ub_mv1_iv = ub_mv1_iv + iv.mpf(iv_mag_mpf(G1[i])) * r_iv[i]
        ub_mv1 = hi_mpf(ub_mv1_iv)
        best_ub = ub_naive if ub_naive <= ub_mv1 else ub_mv1
        if best_ub <= threshold_mpf or not all_smooth:
            return best_ub

    # Full 5x5 interval Hessian H(B): requires strict smoothness q.a > 0 for all 8 signs
    H = [[IV_ZERO] * 5 for _ in range(5)]
    for _, s2i, s3i, s4i in SIGNS:
        s2 = iv.mpf(s2i)
        s3 = iv.mpf(s3i)
        s4 = iv.mpf(s4i)
        w = (
            s2 * J2_v[0] + s3 * J3_v[0] + s4 * J4_v[0],
            s2 * J2_v[1] + s3 * J3_v[1] + s4 * J4_v[1],
            IV_ONE + s2 * J2_v[2] + s3 * J3_v[2] + s4 * J4_v[2],
        )
        q = dot3(w, w)
        if not (lo_mpf(q) > 0):
            raise ValueError("Non-smooth box encountered in 2nd-order Hessian check")
        r = iv.sqrt(q)
        inv_r = IV_ONE / r
        wh = clamp_unit3(scale3(inv_r, w))
        dw = (
            scale3(s2, J2_va),
            scale3(s2, J2_vb),
            scale3(s3, J3_va),
            scale3(s4, J4_va),
            scale3(s4, J4_vb),
        )
        proj = [dot3(wh, dw[i]) for i in range(5)]
        for i in range(5):
            for j in range(i, 5):
                num = dot3(dw[i], dw[j]) - proj[i] * proj[j]
                if i == j and lo_mpf(num) < 0:
                    nb = hi_mpf(num)
                    if nb < 0:
                        raise ValueError("Invalid Cauchy-Schwarz diagonal interval")
                    num = iv.mpf([0, nb])
                term = num * inv_r
                if i == 0 and j == 0:
                    term = term + dot3(wh, scale3(s2, J2_vaa))
                elif i == 0 and j == 1:
                    term = term + dot3(wh, scale3(s2, J2_vab))
                elif i == 1 and j == 1:
                    term = term + dot3(wh, scale3(s2, J2_vbb))
                elif i == 2 and j == 2:
                    term = term + dot3(wh, scale3(s3, J3_vaa))
                elif i == 3 and j == 3:
                    term = term + dot3(wh, scale3(s4, J4_vaa))
                elif i == 3 and j == 4:
                    term = term + dot3(wh, scale3(s4, J4_vab))
                elif i == 4 and j == 4:
                    term = term + dot3(wh, scale3(s4, J4_vbb))
                H[i][j] = H[i][j] + term * IV_INV64
    for i in range(5):
        for j in range(i):
            H[i][j] = H[j][i]

    if kind == "H":
        z_star_f = (Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(1))
        for i in range(5):
            if not (lo_f[i] <= z_star_f[i] <= hi_f[i]):
                raise ValueError("H leaf does not contain z*")
        M_neg = [[IV_ZERO] * 5 for _ in range(5)]
        for i in range(5):
            rad_sum = IV_ZERO
            for j in range(5):
                ha = lo_mpf(H[i][j])
                hb = hi_mpf(H[i][j])
                mid_ij = (ha + hb) / 2
                rad_ij = iv.mpf([0, max(hb - mid_ij, mid_ij - ha)])
                rad_sum = rad_sum + rad_ij
                M_neg[i][j] = iv.mpf(-mid_ij)
            M_neg[i][i] = M_neg[i][i] - rad_sum
        if not is_spd_ldlt_iv(M_neg):
            raise ValueError("H leaf failed strict SPD check on -H(B)")
        p_star = IV_HALF + (IV_ONE + iv.sqrt(iv.mpf(3))) / (iv.mpf(8) * iv.sqrt(IV_TWO))
        return hi_mpf(p_star)

    p0 = IV_HALF
    g0 = [IV_ZERO] * 5
    for _, s2i, s3i, s4i in SIGNS:
        s2 = iv.mpf(s2i)
        s3 = iv.mpf(s3i)
        s4 = iv.mpf(s4i)
        wm = (
            s2 * M2_v[0] + s3 * M3_v[0] + s4 * M4_v[0],
            s2 * M2_v[1] + s3 * M3_v[1] + s4 * M4_v[1],
            IV_ONE + s2 * M2_v[2] + s3 * M3_v[2] + s4 * M4_v[2],
        )
        qm = dot3(wm, wm)
        rm = iv.sqrt(qm)
        p0 = p0 + rm * IV_INV64
        whm = scale3(IV_INV64 / rm, wm)
        g0[0] = g0[0] + s2 * dot3(whm, M2_va)
        g0[1] = g0[1] + s2 * dot3(whm, M2_vb)
        g0[2] = g0[2] + s3 * dot3(whm, M3_va)
        g0[3] = g0[3] + s4 * dot3(whm, M4_va)
        g0[4] = g0[4] + s4 * dot3(whm, M4_vb)

    ub_diag_iv = p0
    for i in range(5):
        ub_diag_iv = ub_diag_iv + quad1d_ub_iv(g0[i], H[i][i], r_iv[i])
        for j in range(i + 1, 5):
            ub_diag_iv = ub_diag_iv + iv.mpf(iv_mag_mpf(H[i][j])) * r_iv[i] * r_iv[j]
    ub_diag = hi_mpf(ub_diag_iv)
    if ub_diag < best_ub:
        best_ub = ub_diag
    if best_ub <= threshold_mpf:
        return best_ub

    H_mid = [[mp.mpf(0)] * 5 for _ in range(5)]
    H_rad = [[IV_ZERO] * 5 for _ in range(5)]
    neg_H_mid = [[IV_ZERO] * 5 for _ in range(5)]
    for i in range(5):
        for j in range(i, 5):
            ha = lo_mpf(H[i][j])
            hb = hi_mpf(H[i][j])
            mid_ij = (ha + hb) / 2
            H_mid[i][j] = mid_ij
            H_mid[j][i] = mid_ij
            rad_ij = max(hb - mid_ij, mid_ij - ha)
            H_rad[i][j] = iv.mpf(rad_ij)
            H_rad[j][i] = H_rad[i][j]
            neg_H_mid[i][j] = iv.mpf(-mid_ij)
            neg_H_mid[j][i] = neg_H_mid[i][j]

    if is_spd_ldlt_iv(neg_H_mid):
        u_mp = [mp.mpf(0)] * 5
        g_mp = [(lo_mpf(g0[i]) + hi_mpf(g0[i])) / 2 for i in range(5)]
        r_mp = [hi_mpf(r_iv[i]) for i in range(5)]
        for _ in range(20):
            for i in range(5):
                lin = g_mp[i]
                for j in range(5):
                    if j != i:
                        lin += H_mid[i][j] * u_mp[j]
                u_star = -lin / H_mid[i][i]
                if u_star < -r_mp[i]:
                    u_mp[i] = -r_mp[i]
                elif u_star > r_mp[i]:
                    u_mp[i] = r_mp[i]
                else:
                    u_mp[i] = u_star

        u_iv = [iv.mpf(u_mp[i]) for i in range(5)]
        q_u = p0
        eta = [IV_ZERO] * 5
        for i in range(5):
            eta_i = g0[i]
            for j in range(5):
                hij = iv.mpf(H_mid[i][j])
                eta_i = eta_i + hij * u_iv[j]
                q_u = q_u + IV_HALF * hij * u_iv[i] * u_iv[j]
            eta[i] = eta_i
            q_u = q_u + g0[i] * u_iv[i]

        dual_gap = IV_ZERO
        for i in range(5):
            dual_gap = dual_gap + abs(eta[i]) * r_iv[i] - eta[i] * u_iv[i]

        cubic_rem = IV_ZERO
        for i in range(5):
            for j in range(5):
                cubic_rem = cubic_rem + IV_HALF * H_rad[i][j] * r_iv[i] * r_iv[j]

        ub_cubic = hi_mpf(q_u + dual_gap + cubic_rem)
        if ub_cubic < best_ub:
            best_ub = ub_cubic

    return best_ub


def verify_certificate(cert_path: str):
    with open(cert_path, "r", encoding="utf-8") as f:
        cert = json.load(f)

    if cert.get("n") != 4:
        raise ValueError("Certificate 'n' must equal 4")
    if cert.get("problem") != "4-to-1 qubit QRAC with shared randomness":
        raise ValueError("Unexpected 'problem' field")
    if cert.get("root_box_weierstrass") != [[-1, 1], [-1, 1], [0, 1], [-1, 1], [0, 1]]:
        raise ValueError("Unexpected 'root_box_weierstrass'")
    if cert.get("claimed_upper_bound") != "0.741482":
        raise ValueError("Unexpected 'claimed_upper_bound'")
    if cert.get("tight_certified_bound") != "0.7414818":
        raise ValueError("Unexpected 'tight_certified_bound'")

    threshold = mp.mpf(cert["claimed_upper_bound"])
    tight_threshold = mp.mpf(cert["tight_certified_bound"])
    if threshold > mp.mpf("0.741482") or tight_threshold > threshold:
        raise ValueError("Invalid threshold configuration")

    p2_cal, p3_cal, p4_cal = run_calibration_checks()

    tree = cert.get("preorder_tree", "")
    if not isinstance(tree, str) or not tree:
        raise ValueError("Empty or invalid preorder_tree")

    sys.setrecursionlimit(max(10000, len(tree) + 100))

    idx = 0
    n_chars = len(tree)
    counts = {
        "A": 0,
        "Q": 0,
        "H": 0,
        "S": 0,
        "splits": [0, 0, 0, 0, 0],
    }
    max_certified_ub = mp.mpf(0)

    def walk(lo_f, hi_f):
        nonlocal idx, max_certified_ub
        if idx >= n_chars:
            raise ValueError("Unexpected end of preorder_tree")
        ch = tree[idx]
        idx += 1

        if ch == "S":
            if idx >= n_chars:
                raise ValueError("Truncated symmetry code in preorder_tree")
            code_ch = tree[idx]
            idx += 1
            if code_ch not in ("4", "5", "6", "7", "8", "9"):
                raise ValueError(f"Invalid symmetry code S{code_ch}")
            if not verify_sym_leaf(int(code_ch), lo_f, hi_f):
                raise ValueError(f"Symmetry exclusion S{code_ch} failed on box")
            counts["S"] += 1
            return

        if ch == "A":
            ub = verify_amgm_leaf(lo_f, hi_f)
            if not (ub <= tight_threshold):
                raise ValueError(f"AM-GM leaf exceeded tight bound: {ub}")
            if ub > max_certified_ub:
                max_certified_ub = ub
            counts["A"] += 1
            return

        if ch in ("Q", "H"):
            ub = verify_quad_or_star_leaf(ch, lo_f, hi_f, tight_threshold)
            if not (ub <= tight_threshold):
                raise ValueError(f"{ch} leaf exceeded tight bound: {ub}")
            if ub > max_certified_ub:
                max_certified_ub = ub
            counts[ch] += 1
            return

        if ch in ("0", "1", "2", "3", "4"):
            d = int(ch)
            counts["splits"][d] += 1
            mid = (lo_f[d] + hi_f[d]) / 2
            hi_left = list(hi_f)
            hi_left[d] = mid
            lo_right = list(lo_f)
            lo_right[d] = mid
            walk(lo_f, hi_left)
            walk(lo_right, hi_f)
            return

        raise ValueError(f"Unexpected token '{ch}' in preorder_tree")

    root_lo = [Fraction(-1), Fraction(-1), Fraction(0), Fraction(-1), Fraction(0)]
    root_hi = [Fraction(1), Fraction(1), Fraction(1), Fraction(1), Fraction(1)]
    walk(root_lo, root_hi)

    if idx != n_chars:
        raise ValueError(f"Unconsumed trailing tokens in preorder_tree ({n_chars - idx} chars)")

    total_leaves = counts["A"] + counts["Q"] + counts["H"] + counts["S"]
    if total_leaves != cert.get("total_leaves"):
        raise ValueError("total_leaves mismatch against header")
    if counts["A"] != cert.get("amgm_leaves"):
        raise ValueError("amgm_leaves mismatch against header")
    if counts["Q"] != cert.get("quad_leaves"):
        raise ValueError("quad_leaves mismatch against header")
    if counts["H"] != cert.get("hessian_star_leaves"):
        raise ValueError("hessian_star_leaves mismatch against header")
    if counts["S"] != cert.get("symmetry_leaves"):
        raise ValueError("symmetry_leaves mismatch against header")
    if counts["splits"] != cert.get("split_counts"):
        raise ValueError("split_counts mismatch against header")
    if not (max_certified_ub <= threshold):
        raise ValueError("Global upper bound exceeded target threshold")

    print("Calibration checks (mpmath.iv, 40 dps):")
    print(f"  p(2) orthogonal = {mp.nstr(p2_cal, 18)}")
    print(f"  p(3) orthogonal = {mp.nstr(p3_cal, 18)}")
    print(f"  p(4) Ambainis   = {mp.nstr(p4_cal, 18)}")
    print("Exact dyadic partition & interval verification:")
    print(f"  Total leaves verified : {total_leaves}")
    print(f"    AM-GM leaves (A)    : {counts['A']}")
    print(f"    Quadratic leaves (Q): {counts['Q']}")
    print(f"    Star leaves (H)     : {counts['H']}")
    print(f"    Symmetry leaves (S) : {counts['S']}")
    print(f"  Split counts          : {counts['splits']}")
    print(f"  Max certified UB      : {mp.nstr(max_certified_ub, 18)}")
    print(f"  Target threshold      : {mp.nstr(threshold, 10)} (0.741481 + 1e-6)")
    print("PASS")


def main():
    default_cert = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "object",
        "certificate_qrac4.json",
    )
    cert_path = sys.argv[1] if len(sys.argv) > 1 else default_cert
    try:
        verify_certificate(cert_path)
    except Exception as exc:
        sys.stderr.write(f"Verification error ({exc.__class__.__name__}): {exc}\n")
        print("FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
