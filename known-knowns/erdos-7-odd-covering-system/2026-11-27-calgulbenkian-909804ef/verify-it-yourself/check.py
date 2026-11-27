#!/usr/bin/env python3
"""
Standalone exact-rational verifier for the global odd-covering lower bound:

    L >= 6,557,114,959,770,375 = 3^5 * 5^3 * 7^2 * 11^2 * 13^2 * 17 * 19 * 23 * 29

Uses only the Python 3 standard library. Performs zero floating-point arithmetic
for mathematical verification and uses no `assert` statements for checks (safe
under `python3 -O`).

Last line of stdout is always `PASS` (exit code 0) or `FAIL` (exit code 1).
"""

import argparse
import hashlib
import json
import math
import os
import sys
import time
from fractions import Fraction
from multiprocessing import Pool


# =============================================================================
# Hard-coded theorem constants (verified internally where applicable)
# =============================================================================

L_TARGET = 6557114959770375  # 3^5 * 5^3 * 7^2 * 11^2 * 13^2 * 17 * 19 * 23 * 29
FIRST_ODD_PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)
MAX_FILE_BYTES = 1_000_000

EXPECTED_VECTOR_COUNTS = {
    9: 5028,
    10: 1484,
    11: 248,
    12: 21,
    13: 1,
}

EXPECTED_SCALAR_COUNT = 738
EXPECTED_ANCHORED_GROUPS = {
    "A8": (1, 28057),
    "F9": (23, 736),
    "G01_G13": (13, 692),
}

VALID_PHASES = frozenset({
    "basic",
    "basic75",
    "mixed",
    "coarse",
    "spatial",
    "pure3",
    "fixed165",
})


class CheckError(Exception):
    """Raised on any verification failure."""


def check(condition, message):
    if not condition:
        raise CheckError(message)


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def verify_first_odd_primes():
    check(FIRST_ODD_PRIMES[0] == 3, "First odd prime must be 3")
    for idx, p in enumerate(FIRST_ODD_PRIMES):
        check(p % 2 == 1 and is_prime(p), f"Not an odd prime: {p}")
        if idx > 0:
            prev = FIRST_ODD_PRIMES[idx - 1]
            check(p > prev, "Prime list not strictly increasing")
            for cand in range(prev + 2, p, 2):
                check(not is_prime(cand), f"Missed odd prime {cand} between {prev} and {p}")
    prod14 = 1
    for p in FIRST_ODD_PRIMES:
        prod14 *= p
    check(prod14 > L_TARGET, f"Product of first 14 odd primes {prod14} <= {L_TARGET}")
    return prod14


def parse_fraction(s, label="fraction"):
    s = s.strip()
    check(len(s) > 0, f"Empty {label}")
    if "/" in s:
        parts = s.split("/")
        check(len(parts) == 2, f"Malformed {label}: {s!r}")
        num_s, den_s = parts
        check(
            (num_s.isdigit() or (num_s.startswith("-") and num_s[1:].isdigit()))
            and den_s.isdigit(),
            f"Non-integer rational components in {label}: {s!r}",
        )
        den = int(den_s)
        check(den > 0, f"Non-positive denominator in {label}: {s!r}")
        return Fraction(int(num_s), den)
    check(
        s.isdigit() or (s.startswith("-") and s[1:].isdigit()),
        f"Non-integer {label}: {s!r}",
    )
    return Fraction(int(s), 1)


def parse_int(s, label="int"):
    s = s.strip()
    check(
        len(s) > 0 and (s.isdigit() or (s.startswith("-") and s[1:].isdigit())),
        f"Malformed {label}: {s!r}",
    )
    return int(s)


def sha256_and_size(path):
    h = hashlib.sha256()
    size = 0
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            size += len(chunk)
            h.update(chunk)
    return h.hexdigest(), size


# =============================================================================
# Part 1: Lemma U (scalar distortion) verifier
# =============================================================================

def eval_lemma_u(primes, exps, k0, Cs):
    r = len(primes)
    check(r >= 2, f"Lemma U requires r >= 2, got {r}")
    check(primes == FIRST_ODD_PRIMES[:r], f"Lemma U primes {primes} != first {r} odd primes")
    check(len(exps) == r, f"Lemma U len(exps) != {r}")
    check(1 <= k0 < r, f"Lemma U invalid k0={k0} for r={r}")
    check(len(Cs) == r - k0, f"Lemma U len(Cs)={len(Cs)} != {r - k0}")

    for e in exps:
        check(isinstance(e, int) and e >= 1, f"Lemma U invalid exponent {e}")

    prod_th = Fraction(1)
    sum_th = Fraction(0)
    for m in range(k0):
        p = primes[m]
        e = exps[m]
        pe = p ** e
        th = Fraction(pe - 1, (p - 2) * pe + 1)
        prod_th *= (1 + th)
        sum_th += th
    B = prod_th - 1 - sum_th

    max_K = max(primes[k0:]) + 2
    dist = {1: Fraction(1)}
    mean = Fraction(1)

    for m in range(r):
        p = primes[m]
        e = exps[m]
        if m >= k0:
            C = Cs[m - k0]
            check(C > 1 and C <= p, f"Lemma U cap out of range: C={C} at p={p}")
            pe = p ** e
            rho = Fraction(pe - 1, (p - 1) * pe)
            delta = 1 - Fraction(1, C)
            check(delta >= rho, f"Lemma U side condition failed: delta={delta} < rho={rho} at p={p}")
            ex = rho * mean - delta
            for k, pk in dist.items():
                if rho * k < delta:
                    ex += pk * (delta - rho * k)
            B += C * ex
        if m == r - 1:
            break
        if m < k0:
            pe = p ** e
            denom = (p - 2) * pe + 1
            p_ge = [Fraction((p - 1) * (p ** (e - t)), denom) for t in range(1, e + 1)]
            steps = [(0, 1 - p_ge[0])]
            for t in range(1, e):
                steps.append((t, p_ge[t - 1] - p_ge[t]))
            steps.append((e, p_ge[e - 1]))
            mean *= (1 + sum(p_ge))
        else:
            C = Cs[m - k0]
            steps = [(0, 1 - C / p)]
            for t in range(1, e):
                steps.append((t, C * Fraction(p - 1, p ** (t + 1))))
            steps.append((e, C / (p ** e)))
            mean *= (1 + C * Fraction(p ** e - 1, (p - 1) * (p ** e)))
        nd = {}
        for k, pk in dist.items():
            for t, pt in steps:
                nk = k * (t + 1)
                if nk >= max_K:
                    break
                nd[nk] = nd.get(nk, Fraction(0)) + pk * pt
        dist = nd

    return B


def parse_and_verify_scalar_file(path):
    header = {}
    certs_by_r = {}
    seen_ids = set()
    max_B = Fraction(0)
    row_count = 0

    with open(path, "r", encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.rstrip("\n")
            if not line:
                continue
            if line.startswith("# "):
                body = line[2:]
                if ":" in body:
                    k, v = body.split(":", 1)
                    header[k.strip()] = v.strip()
                continue
            check(not line.startswith("#"), f"Malformed comment at {path}:{lineno}")
            fields = line.split("\t")
            check(len(fields) == 7, f"Expected 7 tab fields at {path}:{lineno}, got {len(fields)}")
            cid, omega_s, primes_s, exps_s, k0_s, cs_s, b_s = fields
            check(cid not in seen_ids, f"Duplicate scalar id {cid} at {path}:{lineno}")
            seen_ids.add(cid)

            r = parse_int(omega_s, "omega")
            primes = tuple(parse_int(x, "prime") for x in primes_s.split(","))
            exps = tuple(parse_int(x, "exp") for x in exps_s.split(","))
            check(
                r == len(primes) and r == len(exps),
                f"Scalar rank mismatch on {cid}: omega={r}, len(primes)={len(primes)}, len(exps)={len(exps)}",
            )
            check(r in EXPECTED_VECTOR_COUNTS, f"Unexpected scalar omega={r} on {cid}")
            k0 = parse_int(k0_s, "k0")
            Cs = tuple(parse_fraction(x, "C") for x in cs_s.split(","))
            B_stored = parse_fraction(b_s, "B_exact")

            B_calc = eval_lemma_u(primes, exps, k0, Cs)
            check(B_calc == B_stored, f"Scalar B mismatch on {cid}: calc={B_calc} stored={B_stored}")
            check(B_calc < 1, f"Scalar B >= 1 on {cid}: {B_calc}")
            if B_calc > max_B:
                max_B = B_calc
            certs_by_r.setdefault(len(primes), []).append(exps)
            row_count += 1

    check(header.get("format") == "lemma_u_v1", f"Unexpected scalar format: {header.get('format')!r}")
    check(parse_int(header.get("L_target", ""), "L_target") == L_TARGET, "Scalar L_target header mismatch")
    check(row_count > 0, "Scalar certificate file has 0 rows")
    return row_count, certs_by_r, max_B


# =============================================================================
# Part 2: Exact mod-135 geometric maximum (pure Python, exact integer DP)
# =============================================================================

_CORE_CACHE = {}


def core_cells(a, b, r):
    key = (a, b, r)
    res = _CORE_CACHE.get(key)
    if res is None:
        res = tuple(
            x for x in range(135)
            if x % 3 != 0 and x % 9 != 1 and x % 27 != b
            and x % 5 != 0 and x % 15 != a
            and (r < 0 or x % 45 != r)
        )
        _CORE_CACHE[key] = res
    return res


def surviving_rows(b):
    return tuple(h for h in range(27) if h % 3 != 0 and h % 9 != 1 and h != b)


def r15_valid(a):
    return tuple(x for x in range(15) if x % 3 != 0 and x % 5 != 0 and x != a)


def xi_list(a):
    r15s = r15_valid(a)
    out = []
    for x3 in (1, 2):
        for x5 in (1, 2, 3, 4):
            for x9 in (2, 4, 5, 7, 8):
                for x15 in r15s:
                    out.append((x3, x5, x9, x15))
    return tuple(out)


def s_counts(xs, xi):
    x3, x5, x9, x15 = xi
    return tuple((x % 3 == x3) + (x % 5 == x5) + (x % 9 == x9) + (x % 15 == x15) for x in xs)


def build_slab_core(xs, aw, off):
    """
    Collapse each mod-9 row across its 2 or 3 children mod 27.

    Mathematical justification (exact): within a residue class r9 mod 9 and column
    c5 mod 5, every offset off[x] is constant across x mod 27, and there exists a
    single child v27* mod 27 whose cell weight simultaneously maximizes aw[x] in
    every column c5 (verified explicitly below). Because (.)_+ is increasing and
    convex and all category coefficients c_g >= 0, both the mod-27 and mod-135
    choices achieve their simultaneous optimum on child v27* whenever they fall in
    row r9.
    """
    r5_vals = tuple(sorted({x % 5 for x in xs}))
    r15_vals = tuple(sorted({x % 15 for x in xs}))
    r9_vals = tuple(sorted({x % 9 for x in xs}))
    slabs = {1: [], 2: []}
    o_set = set()
    uniq_cols = {}
    for r9 in r9_vals:
        r_idx = [i for i, x in enumerate(xs) if x % 9 == r9]
        r27s = sorted({xs[i] % 27 for i in r_idx})
        r5s_row = sorted({xs[i] % 5 for i in r_idx})
        cell = {(xs[i] % 27, xs[i] % 5): i for i in r_idx}
        check(len(cell) == len(r27s) * len(r5s_row), "Non-rectangular mod-9 row in core")
        v27_best = max(r27s, key=lambda v27: sum(aw[cell[(v27, c5)]] for c5 in r5s_row))
        cols = []
        for c5 in r5s_row:
            o0 = off[cell[(v27_best, c5)]]
            w_max = aw[cell[(v27_best, c5)]]
            w_sum = 0
            for v27 in r27s:
                idx = cell[(v27, c5)]
                check(off[idx] == o0, "Offset varies across mod-27 children inside a mod-9 row")
                check(aw[idx] <= w_max, "No dominant mod-27 child inside a mod-9 row")
                w_sum += aw[idx]
            cols.append((c5, o0, w_sum, w_max))
            o_set.add(o0)
        ct = tuple(cols)
        cid = uniq_cols.setdefault(ct, len(uniq_cols))
        slabs[r9 % 3].append((cid, ct))
    check(len(slabs[1]) > 0 and len(slabs[2]) > 0, "Empty mod-3 slab in core")
    c15_1 = tuple(sorted({r15 % 5 for r15 in r15_vals if r15 % 3 == 1}))
    c15_2 = tuple(sorted({r15 % 5 for r15 in r15_vals if r15 % 3 == 2}))
    return r5_vals, tuple(slabs[1]), tuple(slabs[2]), c15_1, c15_2, tuple(sorted(o_set))


def _merge16(a, b):
    a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15 = a
    b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15 = b
    return (
        a0 + b0,
        a0 + b1 if a0 + b1 > a1 + b0 else a1 + b0,
        a0 + b2 if a0 + b2 > a2 + b0 else a2 + b0,
        max(a0 + b3, a1 + b2, a2 + b1, a3 + b0),
        a0 + b4 if a0 + b4 > a4 + b0 else a4 + b0,
        max(a0 + b5, a1 + b4, a4 + b1, a5 + b0),
        max(a0 + b6, a2 + b4, a4 + b2, a6 + b0),
        max(a0 + b7, a1 + b6, a2 + b5, a3 + b4, a4 + b3, a5 + b2, a6 + b1, a7 + b0),
        a0 + b8 if a0 + b8 > a8 + b0 else a8 + b0,
        max(a0 + b9, a1 + b8, a8 + b1, a9 + b0),
        max(a0 + b10, a2 + b8, a8 + b2, a10 + b0),
        max(a0 + b11, a1 + b10, a2 + b9, a3 + b8, a8 + b3, a9 + b2, a10 + b1, a11 + b0),
        max(a0 + b12, a4 + b8, a8 + b4, a12 + b0),
        max(a0 + b13, a1 + b12, a4 + b9, a5 + b8, a8 + b5, a9 + b4, a12 + b1, a13 + b0),
        max(a0 + b14, a2 + b12, a4 + b10, a6 + b8, a8 + b6, a10 + b4, a12 + b2, a14 + b0),
        max(
            a0 + b15, a1 + b14, a2 + b13, a3 + b12, a4 + b11, a5 + b10, a6 + b9, a7 + b8,
            a8 + b7, a9 + b6, a10 + b5, a11 + b4, a12 + b3, a13 + b2, a14 + b1, a15 + b0,
        ),
    )


def geom135_exact(core_info, shift, c3, c9, c27, c5, c15, c45, c135):
    """
    Exact integer computation of:
      max_{r3,r9,r27,r5,r15,r45,r135} sum_{x in K} a_x * max(0, shift + off_x + sum_g c_g 1[x=r_g(g)])
    using 16-state subset DP across mod-9 rows, split by mod-3 slab with exact (r5, col15)
    symmetry memoization when c5 == c15.
    """
    r5_vals, slab1, slab2, c15_1, c15_2, o_vals = core_info
    c27_45 = c27 + c45
    c27_135 = c27 + c135
    c45_135 = c45 + c135
    c27_45_135 = c27_45 + c135
    sym515 = (c5 == c15)
    dys = (0, c5, c5 + c5) if sym515 else (0, c5, c15, c5 + c15)

    lut = {}
    for b3c in (0, c3):
        for b9c in (0, c9):
            b39 = shift + b3c + b9c
            for o0 in o_vals:
                bo = b39 + o0
                for dy in dys:
                    y = bo + dy
                    if y not in lut:
                        v0 = y if y > 0 else 0
                        t = y + c27
                        v27 = t if t > 0 else 0
                        t = y + c45
                        v45 = t if t > 0 else 0
                        t = y + c27_45
                        v2745 = t if t > 0 else 0
                        t = y + c135
                        vs0 = t if t > 0 else 0
                        t = y + c27_135
                        vs27 = t if t > 0 else 0
                        t = y + c45_135
                        vs45 = t if t > 0 else 0
                        t = y + c27_45_135
                        vs2745 = t if t > 0 else 0
                        lut[y] = (
                            v0,
                            v27 - v0,
                            v45 - v0,
                            v2745 - v27 - v45 + v0,
                            vs0 - v0,
                            vs27 - v27,
                            vs45 - v45,
                            vs2745 - v2745,
                        )

    row_cache = {}
    slab_cache = {}

    def row_dp(cid, cols, base_s, r5, col15):
        if sym515 and col15 and r5 > col15:
            rkey = (cid, base_s, col15, r5)
        else:
            rkey = (cid, base_s, r5, col15)
        cached = row_cache.get(rkey)
        if cached is not None:
            return cached
        rb = [0] * 16
        nc = len(cols)
        for b9, bs in ((0, base_s), (1, base_s + c9)):
            if nc == 4:
                c0, c1, c2, c3_ = cols
                y = bs + c0[1] + (c5 if c0[0] == r5 else 0) + (c15 if c0[0] == col15 else 0)
                v0, d27, d45, p27, g0, g27, g45, g2745 = lut[y]
                ws0, wm0 = c0[2], c0[3]
                base = ws0 * v0
                d27_sum = wm0 * d27
                m0 = wm0 * g0
                m27 = wm0 * g27
                d45_0 = ws0 * d45
                p_0 = wm0 * p27
                g45_0 = wm0 * g45
                g14_0 = wm0 * g2745

                y = bs + c1[1] + (c5 if c1[0] == r5 else 0) + (c15 if c1[0] == col15 else 0)
                v0, d27, d45, p27, g0, g27, g45, g2745 = lut[y]
                ws1, wm1 = c1[2], c1[3]
                base += ws1 * v0
                d27_sum += wm1 * d27
                t = wm1 * g0
                if t > m0:
                    m0 = t
                t = wm1 * g27
                if t > m27:
                    m27 = t
                d45_1 = ws1 * d45
                p_1 = wm1 * p27
                g45_1 = wm1 * g45
                g14_1 = wm1 * g2745

                y = bs + c2[1] + (c5 if c2[0] == r5 else 0) + (c15 if c2[0] == col15 else 0)
                v0, d27, d45, p27, g0, g27, g45, g2745 = lut[y]
                ws2, wm2 = c2[2], c2[3]
                base += ws2 * v0
                d27_sum += wm2 * d27
                t = wm2 * g0
                if t > m0:
                    m0 = t
                t = wm2 * g27
                if t > m27:
                    m27 = t
                d45_2 = ws2 * d45
                p_2 = wm2 * p27
                g45_2 = wm2 * g45
                g14_2 = wm2 * g2745

                y = bs + c3_[1] + (c5 if c3_[0] == r5 else 0) + (c15 if c3_[0] == col15 else 0)
                v0, d27, d45, p27, g0, g27, g45, g2745 = lut[y]
                ws3, wm3 = c3_[2], c3_[3]
                base += ws3 * v0
                d27_sum += wm3 * d27
                t = wm3 * g0
                if t > m0:
                    m0 = t
                t = wm3 * g27
                if t > m27:
                    m27 = t
                d45_3 = ws3 * d45
                p_3 = wm3 * p27
                g45_3 = wm3 * g45
                g14_3 = wm3 * g2745

                b2 = base + d27_sum
                rb[b9] = base
                rb[b9 | 8] = base + m0
                rb[b9 | 2] = b2
                rb[b9 | 10] = b2 + m27
                rb[b9 | 4] = base + max(d45_0, d45_1, d45_2, d45_3)
                rb[b9 | 12] = base + max(
                    d45_0 + (g45_0 if g45_0 > m0 else m0),
                    d45_1 + (g45_1 if g45_1 > m0 else m0),
                    d45_2 + (g45_2 if g45_2 > m0 else m0),
                    d45_3 + (g45_3 if g45_3 > m0 else m0),
                )
                q0 = d45_0 + p_0
                q1 = d45_1 + p_1
                q2 = d45_2 + p_2
                q3 = d45_3 + p_3
                rb[b9 | 6] = b2 + max(q0, q1, q2, q3)
                rb[b9 | 14] = b2 + max(
                    q0 + (g14_0 if g14_0 > m27 else m27),
                    q1 + (g14_1 if g14_1 > m27 else m27),
                    q2 + (g14_2 if g14_2 > m27 else m27),
                    q3 + (g14_3 if g14_3 > m27 else m27),
                )
            elif nc == 3:
                c0, c1, c2 = cols
                y = bs + c0[1] + (c5 if c0[0] == r5 else 0) + (c15 if c0[0] == col15 else 0)
                v0, d27, d45, p27, g0, g27, g45, g2745 = lut[y]
                ws0, wm0 = c0[2], c0[3]
                base = ws0 * v0
                d27_sum = wm0 * d27
                m0 = wm0 * g0
                m27 = wm0 * g27
                d45_0 = ws0 * d45
                p_0 = wm0 * p27
                g45_0 = wm0 * g45
                g14_0 = wm0 * g2745

                y = bs + c1[1] + (c5 if c1[0] == r5 else 0) + (c15 if c1[0] == col15 else 0)
                v0, d27, d45, p27, g0, g27, g45, g2745 = lut[y]
                ws1, wm1 = c1[2], c1[3]
                base += ws1 * v0
                d27_sum += wm1 * d27
                t = wm1 * g0
                if t > m0:
                    m0 = t
                t = wm1 * g27
                if t > m27:
                    m27 = t
                d45_1 = ws1 * d45
                p_1 = wm1 * p27
                g45_1 = wm1 * g45
                g14_1 = wm1 * g2745

                y = bs + c2[1] + (c5 if c2[0] == r5 else 0) + (c15 if c2[0] == col15 else 0)
                v0, d27, d45, p27, g0, g27, g45, g2745 = lut[y]
                ws2, wm2 = c2[2], c2[3]
                base += ws2 * v0
                d27_sum += wm2 * d27
                t = wm2 * g0
                if t > m0:
                    m0 = t
                t = wm2 * g27
                if t > m27:
                    m27 = t
                d45_2 = ws2 * d45
                p_2 = wm2 * p27
                g45_2 = wm2 * g45
                g14_2 = wm2 * g2745

                b2 = base + d27_sum
                rb[b9] = base
                rb[b9 | 8] = base + m0
                rb[b9 | 2] = b2
                rb[b9 | 10] = b2 + m27
                rb[b9 | 4] = base + max(d45_0, d45_1, d45_2)
                rb[b9 | 12] = base + max(
                    d45_0 + (g45_0 if g45_0 > m0 else m0),
                    d45_1 + (g45_1 if g45_1 > m0 else m0),
                    d45_2 + (g45_2 if g45_2 > m0 else m0),
                )
                q0 = d45_0 + p_0
                q1 = d45_1 + p_1
                q2 = d45_2 + p_2
                rb[b9 | 6] = b2 + max(q0, q1, q2)
                rb[b9 | 14] = b2 + max(
                    q0 + (g14_0 if g14_0 > m27 else m27),
                    q1 + (g14_1 if g14_1 > m27 else m27),
                    q2 + (g14_2 if g14_2 > m27 else m27),
                )
            else:
                base = 0
                d27_sum = 0
                max_gs0 = 0
                max_g27 = 0
                d45s = []
                p2745s = []
                gs45s = []
                gs2745s = []
                for c5_v, o0, w_sum, w_max in cols:
                    y = bs + o0
                    if c5_v == r5:
                        y += c5
                    if c5_v == col15:
                        y += c15
                    v0, d27, d45, p2745, gs0, gs27, gs45, gs2745 = lut[y]
                    base += w_sum * v0
                    d27_sum += w_max * d27
                    t = w_max * gs0
                    if t > max_gs0:
                        max_gs0 = t
                    t = w_max * gs27
                    if t > max_g27:
                        max_g27 = t
                    d45s.append(w_sum * d45)
                    p2745s.append(w_max * p2745)
                    gs45s.append(w_max * gs45)
                    gs2745s.append(w_max * gs2745)
                rb[b9] = base
                rb[b9 | 8] = base + max_gs0
                b2 = base + d27_sum
                rb[b9 | 2] = b2
                rb[b9 | 10] = b2 + max_g27
                b45 = 0
                b45s = 0
                b6 = 0
                b14 = 0
                for k in range(nc):
                    dk = d45s[k]
                    cur45 = base + dk
                    if cur45 > b45:
                        b45 = cur45
                    g = gs45s[k]
                    if max_gs0 > g:
                        g = max_gs0
                    if cur45 + g > b45s:
                        b45s = cur45 + g
                    cur6 = b2 + dk + p2745s[k]
                    if cur6 > b6:
                        b6 = cur6
                    g = gs2745s[k]
                    if max_g27 > g:
                        g = max_g27
                    if cur6 + g > b14:
                        b14 = cur6 + g
                rb[b9 | 4] = b45
                rb[b9 | 12] = b45s
                rb[b9 | 6] = b6
                rb[b9 | 14] = b14
        res = tuple(rb)
        row_cache[rkey] = res
        return res

    def eval_s(sid, srows, bs, r5, col15):
        if sym515 and col15 and r5 > col15:
            skey = (sid, bs, col15, r5)
        else:
            skey = (sid, bs, r5, col15)
        cached = slab_cache.get(skey)
        if cached is not None:
            return cached
        dp = row_dp(srows[0][0], srows[0][1], bs, r5, col15)
        for k in range(1, len(srows)):
            dp = _merge16(dp, row_dp(srows[k][0], srows[k][1], bs, r5, col15))
        slab_cache[skey] = dp
        return dp

    best = 0
    for r5 in r5_vals:
        s1_0 = (eval_s(1, slab1, shift, r5, 0), eval_s(1, slab1, shift + c3, r5, 0))
        s2_0 = (eval_s(2, slab2, shift, r5, 0), eval_s(2, slab2, shift + c3, r5, 0))
        for b3_1 in (0, 1):
            a = s2_0[1 - b3_1]
            a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15 = a
            bs1 = shift + c3 if b3_1 else shift
            for col15 in c15_1:
                b = eval_s(1, slab1, bs1, r5, col15)
                v = max(
                    a0 + b[15], a1 + b[14], a2 + b[13], a3 + b[12],
                    a4 + b[11], a5 + b[10], a6 + b[9], a7 + b[8],
                    a8 + b[7], a9 + b[6], a10 + b[5], a11 + b[4],
                    a12 + b[3], a13 + b[2], a14 + b[1], a15 + b[0],
                )
                if v > best:
                    best = v
            a = s1_0[b3_1]
            a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15 = a
            bs2 = shift if b3_1 else shift + c3
            for col15 in c15_2:
                b = eval_s(2, slab2, bs2, r5, col15)
                v = max(
                    a0 + b[15], a1 + b[14], a2 + b[13], a3 + b[12],
                    a4 + b[11], a5 + b[10], a6 + b[9], a7 + b[8],
                    a8 + b[7], a9 + b[6], a10 + b[5], a11 + b[4],
                    a12 + b[3], a13 + b[2], a14 + b[1], a15 + b[0],
                )
                if v > best:
                    best = v
    return best


# =============================================================================
# Part 3: Anchored model verifier (Lemmas A2 - A13)
# =============================================================================

def verify_completion_divisor_sums(primes, exps):
    """Explicitly check Lemma A2 proper-divisor sums < 1 on the completion set D."""
    # Check all mixed moduli in D: {15, 21, 35, 45, 63, 75, 105, 15*p_3}.
    # Pure prime powers p^e have sum_{1<=k<e} p^{-k} < 1/(p-1) <= 1/2 < 1.
    check(len(primes) >= 4, "Anchored completion requires at least 4 primes")
    mixed = [15, 21, 35, 45, 63, 75, 105, 15 * primes[3]]
    # Collect all pure prime powers in D dividing any m in mixed
    pure = set()
    for p, vp in zip(primes, exps):
        lim = 3 if vp is None else min(vp, 3)
        for e in range(1, lim + 1):
            pure.add(p ** e)
    D_fin = sorted(pure | set(mixed))
    for m in mixed:
        # Check m is supported on primes within exponent caps
        rem = m
        for p, vp in zip(primes, exps):
            cnt = 0
            while rem % p == 0:
                rem //= p
                cnt += 1
            if vp is not None:
                check(cnt <= vp, f"Completion modulus {m} exceeds cap v_{p}={vp}")
        check(rem == 1, f"Completion modulus {m} not supported on {primes}")
        s = sum(Fraction(1, d) for d in D_fin if d < m and m % d == 0)
        check(s < 1, f"Lemma A2 divisor sum >= 1 at m={m}: {s}")


class AnchoredModel:
    def __init__(self, primes, exps, C7, taus_later, U_cut, V_cut, phases_used):
        check(len(primes) >= 4, f"Need at least 4 primes, got {primes}")
        check(primes[:3] == (3, 5, 7), f"First three primes must be (3, 5, 7), got {primes[:3]}")
        for idx, p in enumerate(primes):
            check(p % 2 == 1 and is_prime(p), f"Invalid odd prime {p}")
            if idx > 0:
                check(p > primes[idx - 1], f"Primes not strictly increasing: {primes}")
        check(len(exps) == len(primes), "len(exps) != len(primes)")
        check(len(taus_later) == len(primes) - 3, "len(taus_later) != len(primes) - 3")

        v3, v5, v7 = exps[0], exps[1], exps[2]
        check(v3 is None or (isinstance(v3, int) and v3 >= 3), f"Invalid v3={v3}")
        check(v5 is None or (isinstance(v5, int) and v5 >= 2), f"Invalid v5={v5}")
        for vp in exps[2:]:
            check(vp is None or (isinstance(vp, int) and vp >= 1), f"Invalid exponent {vp}")

        check(isinstance(U_cut, int) and U_cut >= 1, f"Invalid U_cut={U_cut}")
        check(isinstance(V_cut, int) and V_cut >= 1, f"Invalid V_cut={V_cut}")
        if v3 is not None:
            check(U_cut > v3 - 3, f"Require U_cut ({U_cut}) > v3 - 3 ({v3 - 3}) for finite v3")
        if v5 is not None:
            check(V_cut > v5 - 1, f"Require V_cut ({V_cut}) > v5 - 1 ({v5 - 1}) for finite v5")

        uses_165 = "fixed165" in phases_used
        verify_completion_divisor_sums(primes, exps)

        self.primes = primes
        self.primes_later = primes[2:]
        self.exps = exps
        self.v3, self.v5, self.v7 = v3, v5, v7
        self.v_later = exps[2:]
        self.U_cut = U_cut
        self.V_cut = V_cut

        self.P3 = Fraction(1, 2) if v3 is None else Fraction(3 ** v3 - 1, 2 * (3 ** v3))
        self.P5 = Fraction(1, 4) if v5 is None else Fraction(5 ** v5 - 1, 4 * (5 ** v5))
        self.P7 = Fraction(1, 6) if v7 is None else Fraction(7 ** v7 - 1, 6 * (7 ** v7))
        self.R0 = 135 * (1 - self.P3 - self.P5)

        self.Z_budget = Fraction(1, 2) if v3 is None else Fraction(3 ** (v3 - 3) - 1, 2 * (3 ** (v3 - 3)))
        self.T_budget = Fraction(1, 20) if v5 is None else Fraction(5 ** (v5 - 2) - 1, 20 * (5 ** (v5 - 2)))

        if v3 is None:
            self.u_pos = tuple((u, Fraction(2, 3 ** (u + 1))) for u in range(1, U_cut))
            self.u_tail_p = Fraction(1, 3 ** U_cut)
            self.u_tail_m = self.u_tail_p * (U_cut + Fraction(1, 2))
            self.u_has_pos = True
        elif v3 == 3:
            self.u_pos = ()
            self.u_tail_p = Fraction(0)
            self.u_tail_m = Fraction(0)
            self.u_has_pos = False
        else:
            umax = v3 - 3
            self.u_pos = tuple((u, Fraction(2, 3 ** (u + 1))) for u in range(1, umax)) + ((umax, Fraction(1, 3 ** umax)),)
            self.u_tail_p = Fraction(0)
            self.u_tail_m = Fraction(0)
            self.u_has_pos = True

        if v5 is None:
            self.v_pos = tuple((v, Fraction(4, 5 ** (v + 1))) for v in range(1, V_cut))
            self.v_tail_p = Fraction(1, 5 ** V_cut)
            self.v_tail_m = self.v_tail_p * (V_cut + Fraction(1, 4))
        else:
            vmax = v5 - 1
            self.v_pos = tuple((v, Fraction(4, 5 ** (v + 1))) for v in range(1, vmax)) + ((vmax, Fraction(1, 5 ** vmax)),)
            self.v_tail_p = Fraction(0)
            self.v_tail_m = Fraction(0)

        # Stage 7 hypotheses
        self.C7 = C7
        self.N7 = 1 / self.P7
        check(self.C7 > 1 and self.C7 <= 7, f"Invalid C7={self.C7}")
        check(self.C7 * (1 - self.P7) >= 1, f"C7*(1-P7) < 1: C7={self.C7}, P7={self.P7}")
        self.TAU7 = self.N7 * (1 - 1 / self.C7)
        self.BETA7 = self.N7 - self.TAU7
        check(self.TAU7 >= 1 and self.TAU7 < self.N7 and self.BETA7 > 0, "Invalid stage-7 threshold")
        self.W7_ext = self.N7 / 7
        self.W7_rem = 1 - self.W7_ext
        check(self.W7_rem >= 0, f"W7_rem < 0: {self.W7_rem}")

        self.S_s = tuple(min(Fraction(1), self.C7 * Fraction(6 - s, 7)) for s in range(5))
        for s, Sv in enumerate(self.S_s):
            check(Sv >= self.C7 / 7 and Sv <= 1, f"Padded 7-fibre mass out of range at s={s}: {Sv}")
        check(
            self.TAU7 >= 1 + self.W7_ext,
            f"Side condition (SC) requires TAU7 ({self.TAU7}) >= 1 + n_7/7 ({1 + self.W7_ext})",
        )
        self.pi7_0_s = tuple(Sv - self.C7 / 7 for Sv in self.S_s)
        den_k = 1
        for x in self.pi7_0_s:
            den_k = math.lcm(den_k, x.denominator)
        self.kappa_den = den_k
        self.kappa_int = tuple(int(x * den_k) for x in self.pi7_0_s)

        # Later stages
        norms = [self.N7]
        for p, vp in zip(self.primes_later[1:], self.v_later[1:]):
            Pp = Fraction(1, p - 1) if vp is None else Fraction(p ** vp - 1, (p - 1) * (p ** vp))
            norms.append(1 / Pp)
        self.norms = tuple(norms)
        self.taus = (self.TAU7,) + tuple(taus_later)
        self.betas = tuple(n - t for n, t in zip(self.norms, self.taus))
        self.caps = tuple(n / b for n, b in zip(self.norms, self.betas))
        for p, t, n, b, C in zip(self.primes_later, self.taus, self.norms, self.betas, self.caps):
            check(t >= 1 and t < n and b > 0, f"Invalid tau={t} at p={p} (n={n})")
            check(C > 1 and C <= p, f"Invalid cap C={C} at p={p}")

        if uses_165:
            w165 = self.norms[1] / self.primes_later[1]
            check(0 < w165 <= 1, f"Invalid pinned weight w165={w165}")

        M_CUT = int(max(self.taus)) + 2
        self.M_CUT = M_CUT

        self.pi7_pos = []
        if v7 is None:
            for j in range(1, M_CUT + 2):
                self.pi7_pos.append((j, self.C7 * Fraction(6, 7 ** (j + 1))))
            self.mean_1pJ7 = Fraction(1) + self.C7 / 6
        else:
            for j in range(1, v7):
                self.pi7_pos.append((j, self.C7 * Fraction(6, 7 ** (j + 1))))
            self.pi7_pos.append((v7, self.C7 * Fraction(1, 7 ** v7)))
            self.mean_1pJ7 = Fraction(1) + self.C7 * self.P7
        self.pi7_pos = tuple(self.pi7_pos)

        def build_dist(include_7):
            out = []
            dist = {1: Fraction(1)}
            mean = Fraction(1)
            for p, vp, C, n_p in zip(self.primes_later, self.v_later, self.caps, self.norms):
                out.append((dict(dist), mean))
                if p == 7 and not include_7:
                    continue
                if vp is None:
                    steps = [(0, 1 - C / p)] + [(e, C * Fraction(p - 1, p ** (e + 1))) for e in range(1, M_CUT)]
                else:
                    steps = (
                        [(0, 1 - C / p)]
                        + [(e, C * Fraction(p - 1, p ** (e + 1))) for e in range(1, vp)]
                        + [(vp, C * Fraction(1, p ** vp))]
                    )
                mean = mean * (1 + C / n_p)
                nd = {}
                for m_val, pr_m in dist.items():
                    for e, pr_e in steps:
                        nm = m_val * (e + 1)
                        if nm >= M_CUT:
                            break
                        nd[nm] = nd.get(nm, Fraction(0)) + pr_m * pr_e
                dist = nd
            return out

        self.full = build_dist(True)
        self.post7 = build_dist(False)

        # Exact minimal sets of rational thresholds t = tau / m actually queried
        ts_full = set()
        for (dist, _), tau in zip(self.full, self.taus):
            for m, pr in dist.items():
                if pr > 0 and m < tau:
                    ts_full.add(tau / m)
        ts_post7 = set()
        for q in range(1, len(self.primes_later)):
            dist, _ = self.post7[q]
            tau = self.taus[q]
            for m, pr in dist.items():
                if pr > 0 and m < tau:
                    ts_post7.add(tau / m)
        self.ts_full = tuple(sorted(ts_full))
        self.ts_post7 = tuple(sorted(ts_post7))

        # Per-model pure memoization caches (zero approximation)
        self._ord_block_cache = {}
        self._pad7_block_cache = {}
        self._ord_env_cache = {}
        self._coarse_common_cache = {}
        self._jpos_cache = {}

    def exact_reserve(self, state):
        a, b, c, r, j, d, k, i_e, z = state
        zz = self.Z_budget if z >= 0 else Fraction(0)

        def D(h):
            return (Fraction(1, 5) if h == c else Fraction(0)) + (self.T_budget if h == j else Fraction(0))

        g15 = 3 * (a == 1) + (b % 3 == a % 3) + (zz if (z >= 0 and z % 3 == a % 3) else Fraction(0))
        R = self.R0 + g15 + (9 - g15) * D(a)
        if r >= 0:
            g45 = Fraction(1 if b % 9 == r % 9 else 0) + (zz if (z >= 0 and z % 9 == r % 9) else Fraction(0))
            R += g45 + (3 - g45) * D(r % 5)
        if d != 0:
            cs = core_cells(a, b, r)
            B_mass = sum(
                (1 - (zz if x % 27 == z else Fraction(0)))
                for x in cs if x % 3 == d and x % 5 == k
            )
            R += Fraction(9, 5) - B_mass * (Fraction(1, 5) - i_e * self.T_budget)
        return R

    def cell_weight_blocks(self, state):
        a, b, c, r, j, d, k, i_e, z = state
        xs = core_cells(a, b, r)
        w3_fr = [
            (Fraction(1) if not self.u_has_pos else Fraction(2, 3))
            - (self.Z_budget if (z >= 0 and x % 27 == z) else Fraction(0))
            for x in xs
        ]
        w5_fr = [
            Fraction(4, 5)
            - (Fraction(1, 5) if x % 5 == c else Fraction(0))
            - (self.T_budget if x % 5 == j else Fraction(0))
            - ((Fraction(1, 5) - i_e * self.T_budget) if (d != 0 and x % 3 == d and x % 5 == k) else Fraction(0))
            for x in xs
        ]
        for w in w3_fr:
            check(w > 0, f"Non-positive w3 cell weight {w} at {state}")
        for w in w5_fr:
            check(w > 0, f"Non-positive w5 cell weight {w} at {state}")
        d3 = 1
        for w in w3_fr:
            d3 = math.lcm(d3, w.denominator)
        d5 = 1
        for w in w5_fr:
            d5 = math.lcm(d5, w.denominator)
        w3_int = tuple(int(w * d3) for w in w3_fr)
        w5_int = tuple(int(w * d5) for w in w5_fr)
        blocks = {
            (False, False): (tuple(w3_int[i] * w5_int[i] for i in range(len(xs))), d3 * d5),
            (False, True): (w3_int, d3),
            (True, False): (w5_int, d5),
            (True, True): (tuple(1 for _ in xs), 1),
        }
        return xs, blocks

    def _eval_ord_block(self, core_key, xs, aw, den_tot, upos, vpos, ts_needed):
        ckey = (core_key, aw, den_tot, upos, vpos, ts_needed)
        cached = self._ord_block_cache.get(ckey)
        if cached is not None:
            return cached

        tot_w = sum(aw)
        mx_w = max(aw)
        h_g = []
        for g in (3, 9, 27, 5, 15, 45):
            acc = {}
            for x, w in zip(xs, aw):
                acc[x % g] = acc.get(x % g, 0) + w
            h_g.append(max(acc.values()))

        u_atoms = self.u_pos if upos else ((0, Fraction(1)),)
        v_atoms = self.v_pos if vpos else ((0, Fraction(1)),)
        M_blk = Fraction(0)
        W_blk = Fraction(0)
        F_blk = {t: Fraction(0) for t in ts_needed}

        core_info = build_slab_core(xs, aw, (0,) * len(xs))
        for u, pu in u_atoms:
            for v, pv in v_atoms:
                w_uv = pu * pv
                M_blk += w_uv * Fraction(tot_w, den_tot)
                lin_uv = (
                    tot_w
                    + h_g[0] + h_g[1] + (1 + u) * h_g[2]
                    + (1 + v) * (h_g[3] + h_g[4] + h_g[5])
                    + (1 + u) * (1 + v) * mx_w
                )
                W_blk += w_uv * Fraction(lin_uv, den_tot)
                for t in ts_needed:
                    qt, pt = t.denominator, t.numerator
                    val = geom135_exact(
                        core_info,
                        qt - pt,
                        qt, qt, qt * (1 + u),
                        qt * (1 + v), qt * (1 + v), qt * (1 + v),
                        qt * (1 + u) * (1 + v),
                    )
                    F_blk[t] += w_uv * Fraction(val, qt * den_tot)

        res = (M_blk, W_blk, F_blk, tot_w, mx_w, tuple(h_g), den_tot)
        self._ord_block_cache[ckey] = res
        return res

    def eval_ord_envelope(self, state, xi=None, use_kappa=False):
        ekey = (state, xi, use_kappa)
        cached = self._ord_env_cache.get(ekey)
        if cached is not None:
            return cached

        core_key = (state[0], state[1], state[3])
        xs, blocks = self.cell_weight_blocks(state)
        sc = s_counts(xs, xi) if use_kappa else None
        ts_needed = self.ts_post7 if use_kappa else self.ts_full
        u_modes = (False, True) if self.u_has_pos else (False,)

        M_tot = Fraction(0)
        W_tot = Fraction(0)
        F_vals = {t: Fraction(0) for t in ts_needed}
        blk_stats = {}

        for upos in u_modes:
            for vpos in (False, True):
                aw_base, den_blk = blocks[(upos, vpos)]
                if use_kappa:
                    aw = tuple(aw_base[i] * self.kappa_int[sc[i]] for i in range(len(xs)))
                    den_tot = den_blk * self.kappa_den
                else:
                    aw = aw_base
                    den_tot = den_blk
                M_b, W_b, F_b, tot_w, mx_w, h_g, d_t = self._eval_ord_block(
                    core_key, xs, aw, den_tot, upos, vpos, ts_needed
                )
                M_tot += M_b
                W_tot += W_b
                for t in ts_needed:
                    F_vals[t] += F_b[t]
                blk_stats[(upos, vpos)] = (d_t, tot_w, mx_w, h_g)

        def add_linear_tail(upos, vpos, p_u, m_u, p_v, m_v):
            nonlocal M_tot, W_tot
            if p_u == 0 or p_v == 0:
                return
            den_tot, tot_w, mx_w, h_g = blk_stats[(upos, vpos)]
            p_uv = p_u * p_v
            eu1 = p_u + m_u
            ev1 = p_v + m_v
            M_add = p_uv * Fraction(tot_w, den_tot)
            W_add = (
                p_uv * (tot_w + h_g[0] + h_g[1])
                + eu1 * p_v * h_g[2]
                + p_u * ev1 * (h_g[3] + h_g[4] + h_g[5])
                + eu1 * ev1 * mx_w
            ) / den_tot
            M_tot += M_add
            W_tot += W_add
            for t in ts_needed:
                F_vals[t] += W_add

        if self.u_tail_p > 0:
            add_linear_tail(True, False, self.u_tail_p, self.u_tail_m, Fraction(1), Fraction(0))
            vp_sum = sum(pv for _, pv in self.v_pos)
            vm_sum = sum(v * pv for v, pv in self.v_pos)
            add_linear_tail(True, True, self.u_tail_p, self.u_tail_m, vp_sum, vm_sum)
            if self.v_tail_p > 0:
                add_linear_tail(True, True, self.u_tail_p, self.u_tail_m, self.v_tail_p, self.v_tail_m)
        if self.v_tail_p > 0:
            add_linear_tail(False, True, Fraction(1), Fraction(0), self.v_tail_p, self.v_tail_m)
            if self.u_has_pos:
                up_sum = sum(pu for _, pu in self.u_pos)
                um_sum = sum(u * pu for u, pu in self.u_pos)
                add_linear_tail(True, True, up_sum, um_sum, self.v_tail_p, self.v_tail_m)

        res = (M_tot, W_tot, F_vals)
        if not use_kappa:
            self._ord_env_cache[ekey] = res
        return res

    def stage_expectation(self, env, dist, mean, tau, mult_scale=1):
        M_tot, W_tot, F_vals = env
        low_sum = Fraction(0)
        low_p = Fraction(0)
        low_m = Fraction(0)
        for m, pr in dist.items():
            mm = mult_scale * m
            if mm < tau:
                low_sum += pr * mm * F_vals[tau / mm]
                low_p += pr
                low_m += pr * mm
        rem_mean = mult_scale * mean - low_m
        rem_p = 1 - low_p
        return low_sum + rem_mean * W_tot - tau * rem_p * M_tot

    def eval_ord_stages(self, state):
        env = self.eval_ord_envelope(state, xi=None, use_kappa=False)
        return tuple(
            self.stage_expectation(env, dist, mean, t, mult_scale=1) / b
            for (dist, mean), t, b in zip(self.full, self.taus, self.betas)
        )

    def eval_stage7_coarse_common(self, state):
        cached = self._coarse_common_cache.get(state)
        if cached is not None:
            return cached

        xs, blocks = self.cell_weight_blocks(state)
        a, b, c, r, j, d, k, i_e, z = state
        check(z == -1, f"Coarse stage 7 requires z == -1, got {z}")
        delta7 = (self.TAU7 - 1) - self.W7_ext
        D = math.lcm(self.W7_rem.denominator, delta7.denominator)
        w_rem_i = int(self.W7_rem * D)
        sh_i = -int(delta7 * D)
        zeros = (0,) * len(xs)

        u_modes = (False, True) if self.u_has_pos else (False,)
        tot = Fraction(0)
        blk_stats = {}
        for upos in u_modes:
            u_atoms = self.u_pos if upos else ((0, Fraction(1)),)
            for vpos in (False, True):
                v_atoms = self.v_pos if vpos else ((0, Fraction(1)),)
                aw, den_blk = blocks[(upos, vpos)]
                core_info = build_slab_core(xs, aw, zeros)
                for u, pu in u_atoms:
                    for v, pv in v_atoms:
                        val = geom135_exact(
                            core_info,
                            sh_i,
                            w_rem_i, w_rem_i, D * (1 + u),
                            D * v + w_rem_i, D * v + w_rem_i, D * (1 + v),
                            D * (1 + u) * (1 + v),
                        )
                        tot += pu * pv * Fraction(val, D * den_blk)
                if self.u_tail_p > 0 or self.v_tail_p > 0:
                    mx_w = max(aw)
                    h_g = []
                    for g in (3, 9, 27, 5, 15, 45):
                        d_g = {}
                        for x, w in zip(xs, aw):
                            d_g[x % g] = d_g.get(x % g, 0) + w
                        h_g.append(max(d_g.values()))
                    blk_stats[(upos, vpos)] = (den_blk, mx_w, h_g)

        def add_c_tail(upos, vpos, p_u, m_u, p_v, m_v):
            nonlocal tot
            if p_u == 0 or p_v == 0:
                return
            den_blk, mx_w, h_g = blk_stats[(upos, vpos)]
            p_uv = p_u * p_v
            eu1 = p_u + m_u
            ev1 = p_v + m_v
            tot += (
                p_uv * self.W7_rem * (h_g[0] + h_g[1] + h_g[3] + h_g[4])
                + eu1 * p_v * h_g[2]
                + p_u * m_v * (h_g[3] + h_g[4])
                + p_u * ev1 * h_g[5]
                + eu1 * ev1 * mx_w
            ) / den_blk

        if self.u_tail_p > 0:
            add_c_tail(True, False, self.u_tail_p, self.u_tail_m, Fraction(1), Fraction(0))
            vp_sum = sum(pv for _, pv in self.v_pos)
            vm_sum = sum(v * pv for v, pv in self.v_pos)
            add_c_tail(True, True, self.u_tail_p, self.u_tail_m, vp_sum, vm_sum)
            if self.v_tail_p > 0:
                add_c_tail(True, True, self.u_tail_p, self.u_tail_m, self.v_tail_p, self.v_tail_m)
        if self.v_tail_p > 0:
            add_c_tail(False, True, Fraction(1), Fraction(0), self.v_tail_p, self.v_tail_m)
            if self.u_has_pos:
                up_sum = sum(pu for _, pu in self.u_pos)
                um_sum = sum(u * pu for u, pu in self.u_pos)
                add_c_tail(True, True, up_sum, um_sum, self.v_tail_p, self.v_tail_m)

        col_full = tuple(
            Fraction(1)
            - (Fraction(1, 5) if x % 5 == c else Fraction(0))
            - (self.T_budget if x % 5 == j else Fraction(0))
            - ((Fraction(1, 5) - i_e * self.T_budget) if (d != 0 and x % 3 == d and x % 5 == k) else Fraction(0))
            for x in xs
        )
        res = (tot / self.BETA7, xs, col_full)
        self._coarse_common_cache[state] = res
        return res

    def eval_stage7_padded(self, state, xi):
        core_key = (state[0], state[1], state[3])
        xs, blocks = self.cell_weight_blocks(state)
        sc = s_counts(xs, xi)
        D = math.lcm(self.W7_ext.denominator, self.W7_rem.denominator, (self.TAU7 - 1).denominator)
        w_ext_i = int(self.W7_ext * D)
        w_rem_i = int(self.W7_rem * D)
        sh_i = -int((self.TAU7 - 1) * D)
        off = tuple(w_ext_i * s for s in sc)

        u_modes = (False, True) if self.u_has_pos else (False,)
        tot = Fraction(0)
        blk_stats = {}
        for upos in u_modes:
            u_atoms = self.u_pos if upos else ((0, Fraction(1)),)
            for vpos in (False, True):
                v_atoms = self.v_pos if vpos else ((0, Fraction(1)),)
                aw, den_blk = blocks[(upos, vpos)]
                bkey = (core_key, aw, sc, den_blk, upos, vpos)
                cached = self._pad7_block_cache.get(bkey)
                if cached is not None:
                    b_tot, st_info = cached
                else:
                    core_info = build_slab_core(xs, aw, off)
                    b_tot = Fraction(0)
                    for u, pu in u_atoms:
                        for v, pv in v_atoms:
                            val = geom135_exact(
                                core_info,
                                sh_i,
                                w_rem_i, w_rem_i, D * (1 + u),
                                D * v + w_rem_i, D * v + w_rem_i, D * (1 + v),
                                D * (1 + u) * (1 + v),
                            )
                            b_tot += pu * pv * Fraction(val, D * den_blk)
                    st_info = None
                    if self.u_tail_p > 0 or self.v_tail_p > 0:
                        s_w = sum(aw[i] * sc[i] for i in range(len(xs)))
                        mx_w = max(aw)
                        h_g = []
                        for g in (3, 9, 27, 5, 15, 45):
                            acc = {}
                            for x, w in zip(xs, aw):
                                acc[x % g] = acc.get(x % g, 0) + w
                            h_g.append(max(acc.values()))
                        st_info = (den_blk, s_w, mx_w, tuple(h_g))
                    self._pad7_block_cache[bkey] = (b_tot, st_info)
                tot += b_tot
                if st_info is not None:
                    blk_stats[(upos, vpos)] = st_info

        def add_pad_tail(upos, vpos, p_u, m_u, p_v, m_v):
            nonlocal tot
            if p_u == 0 or p_v == 0:
                return
            den_blk, s_w, mx_w, h_g = blk_stats[(upos, vpos)]
            p_uv = p_u * p_v
            eu1 = p_u + m_u
            ev1 = p_v + m_v
            tot += (
                p_uv * (self.W7_ext * s_w + self.W7_rem * (h_g[0] + h_g[1] + h_g[3] + h_g[4]))
                + eu1 * p_v * h_g[2]
                + p_u * m_v * (h_g[3] + h_g[4])
                + p_u * ev1 * h_g[5]
                + eu1 * ev1 * mx_w
            ) / den_blk

        if self.u_tail_p > 0:
            add_pad_tail(True, False, self.u_tail_p, self.u_tail_m, Fraction(1), Fraction(0))
            vp_sum = sum(pv for _, pv in self.v_pos)
            vm_sum = sum(v * pv for v, pv in self.v_pos)
            add_pad_tail(True, True, self.u_tail_p, self.u_tail_m, vp_sum, vm_sum)
            if self.v_tail_p > 0:
                add_pad_tail(True, True, self.u_tail_p, self.u_tail_m, self.v_tail_p, self.v_tail_m)
        if self.v_tail_p > 0:
            add_pad_tail(False, True, Fraction(1), Fraction(0), self.v_tail_p, self.v_tail_m)
            if self.u_has_pos:
                up_sum = sum(pu for _, pu in self.u_pos)
                um_sum = sum(u * pu for u, pu in self.u_pos)
                add_pad_tail(True, True, up_sum, um_sum, self.v_tail_p, self.v_tail_m)

        return tot / self.BETA7

    def eval_jpos_later(self, state):
        cached = self._jpos_cache.get(state)
        if cached is not None:
            return cached
        env_unpad = self.eval_ord_envelope(state, xi=None, use_kappa=False)
        n_p = len(self.primes_later)
        L_jpos = [Fraction(0)]
        for q in range(1, n_p):
            dist_p7, mean_p7 = self.post7[q]
            t_q, b_q = self.taus[q], self.betas[q]
            jpos = Fraction(0)
            used_p = Fraction(0)
            used_m = Fraction(0)
            for j, pj in self.pi7_pos:
                mm = 1 + j
                if mm < t_q:
                    jpos += pj * self.stage_expectation(env_unpad, dist_p7, mean_p7, t_q, mult_scale=mm)
                    used_p += pj
                    used_m += mm * pj
            rem_p = self.C7 / 7 - used_p
            rem_m = (self.mean_1pJ7 - (1 - self.C7 / 7)) - used_m
            if rem_p > 0:
                M_tot, W_tot, _ = env_unpad
                jpos += rem_m * mean_p7 * W_tot - t_q * rem_p * M_tot
            L_jpos.append(jpos / b_q)
        res = tuple(L_jpos)
        self._jpos_cache[state] = res
        return res

    def eval_spatial_stages(self, state, xi):
        l7 = self.eval_stage7_padded(state, xi)
        env_kap = self.eval_ord_envelope(state, xi=xi, use_kappa=True)
        L_jpos = self.eval_jpos_later(state)
        n_p = len(self.primes_later)
        Ls = [l7]
        for q in range(1, n_p):
            dist_p7, mean_p7 = self.post7[q]
            j0 = self.stage_expectation(env_kap, dist_p7, mean_p7, self.taus[q], mult_scale=1) / self.betas[q]
            Ls.append(j0 + L_jpos[q])
        return tuple(Ls)

    def eval_fixed165_stage11(self, state, xi, eta):
        xs, blocks = self.cell_weight_blocks(state)
        sc = s_counts(xs, xi)
        tau11 = self.taus[1]
        beta11 = self.betas[1]
        w165 = self.norms[1] / self.primes_later[1]
        D = math.lcm(w165.denominator, tau11.denominator)
        w165_i = int(w165 * D)
        tau11_i = int(tau11 * D)
        off = tuple(w165_i if x % 15 == eta else 0 for x in xs)

        env_unpad = self.eval_ord_envelope(state, xi=None, use_kappa=False)
        M_tot, W_tot, _ = env_unpad

        u_modes = (False, True) if self.u_has_pos else (False,)
        tot = Fraction(0)

        used_pos_p = Fraction(0)
        used_pos_m = Fraction(0)
        m_list = [(1, True, Fraction(1))]
        for j, pj in self.pi7_pos:
            m = 1 + j
            if m < tau11:
                m_list.append((m, False, pj))
                used_pos_p += pj
                used_pos_m += m * pj

        for m, use_kap, m_wt in m_list:
            shift = D * m - tau11_i
            mD = D * m
            blk_stats = {}
            for upos in u_modes:
                u_atoms = self.u_pos if upos else ((0, Fraction(1)),)
                for vpos in (False, True):
                    v_atoms = self.v_pos if vpos else ((0, Fraction(1)),)
                    aw_base, den_blk = blocks[(upos, vpos)]
                    if use_kap:
                        aw = tuple(aw_base[i] * self.kappa_int[sc[i]] for i in range(len(xs)))
                        den_tot = den_blk * self.kappa_den
                    else:
                        aw = aw_base
                        den_tot = den_blk
                    core_info = build_slab_core(xs, aw, off)
                    for u, pu in u_atoms:
                        for v, pv in v_atoms:
                            c15 = mD * (1 + v) - w165_i
                            check(c15 >= 0, f"Negative residual c15={c15} in fixed165")
                            val = geom135_exact(
                                core_info,
                                shift,
                                mD, mD, mD * (1 + u),
                                mD * (1 + v), c15, mD * (1 + v),
                                mD * (1 + u) * (1 + v),
                            )
                            tot += m_wt * pu * pv * Fraction(val, D * den_tot)
                    if self.u_tail_p > 0 or self.v_tail_p > 0:
                        tot_w = sum(aw)
                        mx_w = max(aw)
                        h_g = []
                        for g in (3, 9, 27, 5, 15, 45):
                            acc = {}
                            for x, w in zip(xs, aw):
                                acc[x % g] = acc.get(x % g, 0) + w
                            h_g.append(max(acc.values()))
                        blk_stats[(upos, vpos)] = (den_tot, tot_w, mx_w, h_g)

            if self.u_tail_p > 0 or self.v_tail_p > 0:
                def add_165_tail(upos, vpos, p_u, m_u, p_v, m_v):
                    nonlocal tot
                    if p_u == 0 or p_v == 0:
                        return
                    den_tot, tot_w, mx_w, h_g = blk_stats[(upos, vpos)]
                    p_uv = p_u * p_v
                    eu1 = p_u + m_u
                    ev1 = p_v + m_v
                    W_add = (
                        p_uv * (tot_w + h_g[0] + h_g[1])
                        + eu1 * p_v * h_g[2]
                        + p_u * ev1 * (h_g[3] + h_g[4] + h_g[5])
                        + eu1 * ev1 * mx_w
                    ) / den_tot
                    tot += m_wt * m * W_add

                if self.u_tail_p > 0:
                    add_165_tail(True, False, self.u_tail_p, self.u_tail_m, Fraction(1), Fraction(0))
                    vp_sum = sum(pv for _, pv in self.v_pos)
                    vm_sum = sum(v * pv for v, pv in self.v_pos)
                    add_165_tail(True, True, self.u_tail_p, self.u_tail_m, vp_sum, vm_sum)
                    if self.v_tail_p > 0:
                        add_165_tail(True, True, self.u_tail_p, self.u_tail_m, self.v_tail_p, self.v_tail_m)
                if self.v_tail_p > 0:
                    add_165_tail(False, True, Fraction(1), Fraction(0), self.v_tail_p, self.v_tail_m)
                    if self.u_has_pos:
                        up_sum = sum(pu for _, pu in self.u_pos)
                        um_sum = sum(u * pu for u, pu in self.u_pos)
                        add_165_tail(True, True, up_sum, um_sum, self.v_tail_p, self.v_tail_m)

        rem_p = self.C7 / 7 - used_pos_p
        rem_m = (self.mean_1pJ7 - (1 - self.C7 / 7)) - used_pos_m
        if rem_p > 0:
            tot += rem_m * W_tot - tau11 * rem_p * M_tot
        return tot / beta11


# =============================================================================
# Part 4: Parsing anchored TSV files, hierarchy completeness, parallel dispatch
# =============================================================================

def parse_anchored_models(part_paths):
    """
    Parse one or more TSV files belonging to a logical anchored file group.
    Multi-part files (part k/N with N > 1) merge into a single model after
    verifying identical mathematical headers and consecutive part indices 1..N.
    Single-part files may contain one or more models separated by `# --- model ---`.
    """
    models = []
    if len(part_paths) > 1:
        merged_header = None
        merged_rows = []
        n_parts = len(part_paths)
        for idx, p in enumerate(part_paths, 1):
            hdr = {}
            in_rows = False
            with open(p, "r", encoding="utf-8") as f:
                for lineno, raw in enumerate(f, 1):
                    line = raw.rstrip("\n")
                    if not line:
                        continue
                    if line.startswith("# "):
                        check(not in_rows, f"Header line after data rows in {p}:{lineno}")
                        body = line[2:]
                        check(body != "--- model ---", f"Unexpected model separator in multi-part file {p}:{lineno}")
                        if ":" in body:
                            k, v = body.split(":", 1)
                            hdr[k.strip()] = v.strip()
                        continue
                    check(not line.startswith("#"), f"Malformed comment at {p}:{lineno}")
                    in_rows = True
                    merged_rows.append(_parse_anchored_row(line, p, lineno))
            check(hdr.get("format") == "anchored_cert_v1", f"Bad format in {p}: {hdr.get('format')!r}")
            check(hdr.get("part") == f"{idx}/{n_parts}", f"Bad part tag in {p}: {hdr.get('part')!r}")
            cmp_hdr = {k: v for k, v in hdr.items() if k != "part"}
            if merged_header is None:
                merged_header = cmp_hdr
            else:
                check(cmp_hdr == merged_header, f"Header mismatch across parts in {p}")
        models.append((merged_header, merged_rows))
        return models

    # Single file (may contain 1 or more models separated by `# --- model ---`)
    p = part_paths[0]
    cur_hdr = {}
    cur_rows = []
    in_rows = False
    with open(p, "r", encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.rstrip("\n")
            if not line:
                continue
            if line == "# --- model ---":
                if cur_hdr or cur_rows:
                    models.append((cur_hdr, cur_rows))
                cur_hdr = {}
                cur_rows = []
                in_rows = False
                continue
            if line.startswith("# "):
                check(not in_rows, f"Header line after data rows without separator at {p}:{lineno}")
                body = line[2:]
                if ":" in body:
                    k, v = body.split(":", 1)
                    cur_hdr[k.strip()] = v.strip()
                continue
            check(not line.startswith("#"), f"Malformed comment at {p}:{lineno}")
            in_rows = True
            cur_rows.append(_parse_anchored_row(line, p, lineno))
    if cur_hdr or cur_rows:
        models.append((cur_hdr, cur_rows))
    check(len(models) > 0, f"No models found in {p}")
    for hdr, rows in models:
        check(hdr.get("format") == "anchored_cert_v1", f"Bad format in {p}: {hdr.get('format')!r}")
        check(hdr.get("part", "1/1") == "1/1", f"Unexpected part tag in single file {p}")
        check(len(rows) > 0, f"Empty model {hdr.get('id')} in {p}")
    return models


def _parse_anchored_row(line, path, lineno):
    fields = line.split("\t")
    check(len(fields) == 4, f"Expected 4 tab fields at {path}:{lineno}, got {len(fields)}")
    phase, key_s, r_s, s_s = fields
    check(phase in VALID_PHASES, f"Unknown phase {phase!r} at {path}:{lineno}")
    key = tuple(parse_int(x, "key") for x in key_s.split(","))
    if phase in ("basic", "basic75", "mixed"):
        check(len(key) == 9, f"Phase {phase} requires key length 9 at {path}:{lineno}")
    elif phase in ("coarse", "spatial", "pure3"):
        check(len(key) == 13, f"Phase {phase} requires key length 13 at {path}:{lineno}")
    elif phase == "fixed165":
        check(len(key) == 14, f"Phase fixed165 requires key length 14 at {path}:{lineno}")
    R_val = parse_fraction(r_s, "R_exact")
    S_val = parse_fraction(s_s, "S_exact")
    return phase, key, R_val, S_val


def verify_hierarchy_completeness(rows, model_id):
    row_set = set()
    for phase, key, _, _ in rows:
        item = (phase, key)
        check(item not in row_set, f"Duplicate row {item} in {model_id}")
        row_set.add(item)

    used = set()
    uncovered = 0

    for a in (1, 2):
        r15s = r15_valid(a)
        xis = xi_list(a)
        for b in (2, 4):
            z_rows = surviving_rows(b)
            for c in (a, 3 - a):
                b_states = [(a, b, c, -1, j, 0, 0, 0, -1) for j in range(1, 5)]
                if all(("basic", st) in row_set for st in b_states):
                    for st in b_states:
                        used.add(("basic", st))
                    continue
                if b == 2 and all(("basic75", st) in row_set for st in b_states):
                    for st in b_states:
                        used.add(("basic75", st))
                    continue
                reps = {}
                for r in range(45):
                    if r % 3 and r % 9 != 1 and r % 5 and r % 15 != a:
                        reps.setdefault((r % 3, r % 9 == b % 9, r % 5 == a, r % 5 == c), r)
                for r in reps.values():
                    for d in (1, 2):
                        for k in range(1, 5):
                            if (d, k) == (a % 3, a % 5):
                                continue
                            for j, i_e in [(jj, 0) for jj in range(1, 5)] + [(k, 1)]:
                                st = (a, b, c, r, j, d, k, i_e, -1)
                                if ("mixed", st) in row_set:
                                    used.add(("mixed", st))
                                    continue
                                for xi in xis:
                                    key_xi = st + xi
                                    if ("coarse", key_xi) in row_set:
                                        used.add(("coarse", key_xi))
                                        continue
                                    if ("spatial", key_xi) in row_set:
                                        used.add(("spatial", key_xi))
                                        continue
                                    for z in z_rows:
                                        stz = st[:-1] + (z,)
                                        key_z = stz + xi
                                        if ("pure3", key_z) in row_set:
                                            used.add(("pure3", key_z))
                                            continue
                                        for eta in r15s:
                                            key_eta = key_z + (eta,)
                                            if ("fixed165", key_eta) in row_set:
                                                used.add(("fixed165", key_eta))
                                            else:
                                                uncovered += 1

    unused = len(row_set) - len(used)
    check(uncovered == 0, f"Hierarchy incomplete in {model_id}: {uncovered} uncovered leaves")
    check(unused == 0, f"Hierarchy has {unused} unused/unreachable rows in {model_id}")


def _verify_group_worker(args):
    """Worker for parallel verification of (a, b, r)-grouped rows of a large model."""
    model_cfg, row_group = args
    primes, exps, C7, taus_later, U_cut, V_cut, phases_used, model_id = model_cfg
    mod = AnchoredModel(primes, exps, C7, taus_later, U_cut, V_cut, phases_used)
    min_margin = None
    spatial_cache = {}
    for phase, key, R_stored, S_stored in row_group:
        st = key[:9]
        R_calc = mod.exact_reserve(st)
        if phase == "basic75":
            check(st[1] == 2 and st[3] == -1 and st[5] == 0 and st[6] == 0 and st[7] == 0 and st[8] == -1,
                  f"Invalid basic75 key {st} in {model_id}")
            R_calc += Fraction(1, 5)

        if phase in ("basic", "basic75", "mixed"):
            Ls = mod.eval_ord_stages(st)
            S_calc = sum(Ls)
        elif phase == "coarse":
            xi = key[9:13]
            L_ord = mod.eval_ord_stages(st)
            common, xs, col_full = mod.eval_stage7_coarse_common(st)
            sc = s_counts(xs, xi)
            s_pen = sum(col_full[i] * (sc[i] - 1) for i in range(len(xs)) if sc[i] > 1)
            S_calc = common + (mod.C7 / 7) * s_pen + sum(L_ord[1:])
        elif phase in ("spatial", "pure3"):
            xi = key[9:13]
            Ls = mod.eval_spatial_stages(st, xi)
            S_calc = sum(Ls)
        elif phase == "fixed165":
            xi = key[9:13]
            eta = key[13]
            check(eta in r15_valid(st[0]), f"Invalid eta={eta} for a={st[0]} in {model_id}")
            sp_key = (st, xi)
            Ls_base = spatial_cache.get(sp_key)
            if Ls_base is None:
                Ls_base = mod.eval_spatial_stages(st, xi)
                spatial_cache[sp_key] = Ls_base
            l11 = mod.eval_fixed165_stage11(st, xi, eta)
            S_calc = Ls_base[0] + l11 + sum(Ls_base[2:])
        else:
            raise CheckError(f"Unhandled phase {phase}")

        check(R_calc == R_stored, f"R mismatch in {model_id} {phase} {key}: calc={R_calc} stored={R_stored}")
        check(S_calc == S_stored, f"S mismatch in {model_id} {phase} {key}: calc={S_calc} stored={S_stored}")
        margin = R_calc - S_calc
        check(margin > 0, f"Non-positive margin in {model_id} {phase} {key}: {margin}")
        if min_margin is None or margin < min_margin:
            min_margin = margin
    return len(row_group), min_margin


def validate_anchored_header_and_tree(hdr, rows):
    model_id = hdr.get("id", "<missing>")
    check(len(model_id) > 0 and model_id != "<missing>", "Missing model id in header")
    primes = tuple(parse_int(x, "prime") for x in hdr["primes"].split(","))
    exps = tuple(None if x.strip() == "inf" else parse_int(x, "exp") for x in hdr["exps"].split(","))
    C7 = parse_fraction(hdr["C7"], "C7")
    taus_later = tuple(parse_fraction(x, "tau") for x in hdr["taus_later"].split(","))
    U_cut = parse_int(hdr["U_cut"], "U_cut")
    V_cut = parse_int(hdr["V_cut"], "V_cut")
    phases_used = frozenset(r[0] for r in rows)

    # Validate model hypotheses and complete hierarchy partition
    AnchoredModel(primes, exps, C7, taus_later, U_cut, V_cut, phases_used)
    verify_hierarchy_completeness(rows, model_id)
    model_cfg = (primes, exps, C7, taus_later, U_cut, V_cut, phases_used, model_id)
    return model_id, primes, exps, model_cfg


def verify_anchored_rows(model_cfg, rows, procs=1):
    model_id = model_cfg[7]

    # Group rows by (a, b, r) so memoization of (True, True) / (False, True) / (True, False) blocks is maximized!
    groups = {}
    for row in rows:
        key = row[1]
        gkey = (key[0], key[1], key[3])
        groups.setdefault(gkey, []).append(row)

    # For multi-core on a large model, further split large spatial/pure3/fixed165 groups by (a, b, r, xi) if needed
    work_items = []
    if procs > 1 and len(rows) > 1000:
        for gkey, grows in sorted(groups.items()):
            # Keep basic/basic75/mixed/coarse together (instant), split deep rows by xi!
            shallow = [r for r in grows if r[0] in ("basic", "basic75", "mixed", "coarse")]
            deep = [r for r in grows if r[0] not in ("basic", "basic75", "mixed", "coarse")]
            if shallow:
                work_items.append((model_cfg, shallow))
            if deep:
                by_xi = {}
                for r in deep:
                    by_xi.setdefault(r[1][9:13], []).append(r)
                # Batch xi into chunks to preserve (a,b,r) sharing while keeping cores busy
                xi_items = sorted(by_xi.items())
                chunk_sz = max(1, (len(xi_items) + procs * 2 - 1) // (procs * 2))
                for i in range(0, len(xi_items), chunk_sz):
                    chunk_rows = []
                    for _, rlist in xi_items[i:i + chunk_sz]:
                        chunk_rows.extend(rlist)
                    work_items.append((model_cfg, chunk_rows))
    else:
        for _, grows in sorted(groups.items()):
            work_items.append((model_cfg, grows))

    min_margin = None
    checked_rows = 0
    if procs > 1 and len(work_items) > 1:
        with Pool(min(procs, len(work_items))) as pool:
            for cnt, mm in pool.map(_verify_group_worker, work_items):
                checked_rows += cnt
                if mm is not None and (min_margin is None or mm < min_margin):
                    min_margin = mm
    else:
        for item in work_items:
            cnt, mm = _verify_group_worker(item)
            checked_rows += cnt
            if mm is not None and (min_margin is None or mm < min_margin):
                min_margin = mm

    check(checked_rows == len(rows), f"Row count mismatch in {model_id}")
    return checked_rows, min_margin


def verify_anchored_model(hdr, rows, procs=1):
    model_id, primes, exps, model_cfg = validate_anchored_header_and_tree(hdr, rows)
    checked_rows, min_margin = verify_anchored_rows(model_cfg, rows, procs=procs)
    return model_id, primes, exps, checked_rows, min_margin


# =============================================================================
# Part 5: Exhaustive exponent-vector enumeration and domination check
# =============================================================================

def enumerate_vectors_below(r, limit):
    ps = FIRST_ODD_PRIMES[:r]
    base = 1
    for p in ps:
        base *= p
    out = []

    def dfs(pos, cur, es):
        if pos == r:
            out.append(tuple(es))
            return
        e = 1
        v = cur
        while v < limit:
            dfs(pos + 1, v, es + [e])
            e += 1
            v *= ps[pos]

    if base < limit:
        dfs(0, base, [])
    return out


def dominates(cap, vec):
    check(len(cap) == len(vec), f"Dimension mismatch in dominates: len(cap)={len(cap)} != len(vec)={len(vec)}")
    return all(c is None or v <= c for c, v in zip(cap, vec))


# =============================================================================
# Main driver
# =============================================================================

def run_verification(pkg_dir, procs=1):
    t0 = time.time()
    pkg_dir = os.path.abspath(pkg_dir)
    pkg_prefix = pkg_dir if pkg_dir.endswith(os.sep) else pkg_dir + os.sep
    prod14 = verify_first_odd_primes()
    print(f"[OK] Consecutive odd primes verified; prod(first 14) = {prod14:,} > {L_TARGET:,}", flush=True)

    manifest_path = os.path.join(pkg_dir, "MANIFEST.json")
    check(os.path.isfile(manifest_path), f"Missing MANIFEST.json at {manifest_path}")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    check(manifest.get("format") == "erdos7_package_manifest_v1", "Unexpected manifest format")
    check(manifest.get("L_target") == L_TARGET, f"Manifest L_target mismatch: {manifest.get('L_target')}")

    files_meta = manifest.get("files")
    check(isinstance(files_meta, list) and len(files_meta) > 0, "Manifest files list empty")

    # Verify SHA-256, byte count, and <= 1,000,000 byte limit for every listed file
    file_index = {}
    total_bytes = 0
    for entry in files_meta:
        rel = entry["path"]
        check(rel not in file_index, f"Duplicate path in manifest: {rel}")
        abs_p = os.path.abspath(os.path.join(pkg_dir, rel))
        check(abs_p.startswith(pkg_prefix), f"Path escapes package dir: {rel}")
        check(os.path.isfile(abs_p), f"Missing certificate file: {rel}")
        digest, size = sha256_and_size(abs_p)
        check(size <= MAX_FILE_BYTES, f"File {rel} exceeds {MAX_FILE_BYTES} bytes ({size})")
        check(size == entry["bytes"], f"Byte size mismatch on {rel}: actual={size} manifest={entry['bytes']}")
        check(digest == entry["sha256"], f"SHA-256 mismatch on {rel}: actual={digest} manifest={entry['sha256']}")
        file_index[rel] = (abs_p, entry)
        total_bytes += size
    check(total_bytes <= 50_000_000, f"Total certificate bytes {total_bytes} exceeds 50 MB limit")
    if "total_files" in manifest:
        check(manifest["total_files"] == len(files_meta),
              f"Manifest total_files mismatch: {manifest['total_files']} != {len(files_meta)}")
    if "total_bytes" in manifest:
        check(manifest["total_bytes"] == total_bytes,
              f"Manifest total_bytes mismatch: {manifest['total_bytes']} != {total_bytes}")
    print(f"[OK] Manifest verified: {len(files_meta)} files, {total_bytes:,} bytes total (all <= 1,000,000 B, all SHA-256 exact)", flush=True)

    # Verify every logical certificate group listed in manifest
    certs_meta = manifest.get("certificates")
    check(isinstance(certs_meta, list) and len(certs_meta) > 0, "Manifest certificates list empty")

    # Validate certificate group set up front and run fast groups before A8
    expected_group_ids = {"U1_U738"} | set(EXPECTED_ANCHORED_GROUPS)
    seen_cert_ids = set()
    by_id = {}
    for c_entry in certs_meta:
        cid = c_entry["id"]
        check(cid not in seen_cert_ids, f"Duplicate certificate group id in manifest: {cid}")
        seen_cert_ids.add(cid)
        by_id[cid] = c_entry
    check(seen_cert_ids == expected_group_ids,
          f"Certificate group set mismatch: got {sorted(seen_cert_ids)}, expected {sorted(expected_group_ids)}")

    ordered_ids = ("U1_U738", "G01_G13", "F9", "A8")
    verified_caps_by_r = {r: [] for r in (8, 9, 10, 11, 12, 13)}
    seen_model_ids = set()
    thmA_header_ok = False
    total_scalar = 0
    anchored_plan = []

    # Pass 1: Verify scalar file completely, plus parse & validate all anchored headers,
    # side conditions, hierarchy completeness, statement bindings, and vector coverage.
    for cid in ordered_ids:
        c_entry = by_id[cid]
        kind = c_entry["kind"]
        parts = c_entry["parts"]
        check(isinstance(parts, list) and len(parts) >= 1, f"Empty parts for {cid}")
        abs_parts = []
        for rel in parts:
            check(rel in file_index, f"Certificate part not listed in manifest files: {rel}")
            abs_parts.append(file_index[rel][0])

        if kind == "lemma_u":
            check(cid == "U1_U738", f"Unexpected scalar group id: {cid}")
            check(len(abs_parts) == 1, "Scalar Lemma U group must be 1 file")
            t1 = time.time()
            n_sc, sc_by_r, max_B = parse_and_verify_scalar_file(abs_parts[0])
            check(n_sc == c_entry["count"], f"Scalar count mismatch: actual={n_sc} manifest={c_entry['count']}")
            check(n_sc == EXPECTED_SCALAR_COUNT, f"Scalar count {n_sc} != expected {EXPECTED_SCALAR_COUNT}")
            total_scalar += n_sc
            for r, cap_list in sc_by_r.items():
                check(r in verified_caps_by_r, f"Unexpected scalar omega={r}")
                for cap in cap_list:
                    check(len(cap) == r, f"Scalar cap length {len(cap)} != {r}")
                verified_caps_by_r[r].extend(cap_list)
            print(f"[OK] {cid}: {n_sc} Lemma U certs verified exact (max B = {float(max_B):.6f} < 1) [{time.time()-t1:.2f}s]", flush=True)

        elif kind == "anchored":
            check(cid in EXPECTED_ANCHORED_GROUPS, f"Unexpected anchored group id: {cid}")
            exp_models_hc, exp_rows_hc = EXPECTED_ANCHORED_GROUPS[cid]
            models = parse_anchored_models(abs_parts)
            expected_models = c_entry["model_count"]
            expected_rows = c_entry["total_rows"]
            check(len(models) == expected_models == exp_models_hc,
                  f"Model count mismatch in {cid}: actual={len(models)} manifest={expected_models} expected={exp_models_hc}")
            parsed_models = []
            group_rows = 0
            for hdr, rows in models:
                mid, primes, exps, model_cfg = validate_anchored_header_and_tree(hdr, rows)
                check(mid not in seen_model_ids, f"Duplicate anchored model id: {mid}")
                seen_model_ids.add(mid)
                r = len(primes)
                check(primes == FIRST_ODD_PRIMES[:r], f"Model {mid} primes {primes} != P_{r}")
                check(len(exps) == r, f"Model {mid} exps length {len(exps)} != {r}")
                if cid == "A8":
                    check(r == 8 and all(e is None for e in exps),
                          f"Theorem A model {mid} must have 8 primes with all unrestricted exponents")
                    thmA_header_ok = True
                elif cid == "F9":
                    check(r == 9, f"Nine-prime group F9 model {mid} must have 9 primes, got {r}")
                elif cid == "G01_G13":
                    check(r in (10, 11), f"Global anchored group G01_G13 model {mid} must have 10 or 11 primes, got {r}")
                if r in verified_caps_by_r:
                    verified_caps_by_r[r].append(exps)
                group_rows += len(rows)
                parsed_models.append((model_cfg, rows))
            check(group_rows == expected_rows == exp_rows_hc,
                  f"Row count mismatch in {cid}: actual={group_rows} manifest={expected_rows} expected={exp_rows_hc}")
            anchored_plan.append((cid, parsed_models, exp_rows_hc))
        else:
            raise CheckError(f"Unknown certificate kind {kind!r}")

    check(thmA_header_ok, "Theorem A (8 primes, all unrestricted exponents) header missing")

    # Exhaustive vector enumeration and cap domination check (all caps still must pass exact row verification below)
    total_vecs = 0
    for r in (9, 10, 11, 12, 13):
        vecs = enumerate_vectors_below(r, L_TARGET)
        check(
            len(vecs) == EXPECTED_VECTOR_COUNTS[r],
            f"Unexpected vector count at omega={r}: got {len(vecs)}, expected {EXPECTED_VECTOR_COUNTS[r]}",
        )
        caps = verified_caps_by_r[r]
        uncovered = 0
        for vec in vecs:
            if not any(dominates(cap, vec) for cap in caps):
                uncovered += 1
                if uncovered == 1:
                    first_miss = vec
        check(uncovered == 0, f"At omega={r}: {uncovered} uncovered vectors below {L_TARGET}, e.g. {first_miss if uncovered else None}")
        total_vecs += len(vecs)
        print(f"[OK] omega={r:2d}: all {len(vecs):4d}/{len(vecs):4d} exponent vectors < {L_TARGET:,} dominated by declared caps", flush=True)

    # Pass 2: Exact rational recomputation of R and S on every anchored row (G01_G13 -> F9 -> A8)
    total_anchored_models = 0
    total_anchored_rows = 0
    thmA_verified = False
    for cid, parsed_models, exp_rows_hc in anchored_plan:
        t1 = time.time()
        group_rows = 0
        group_min = None
        for model_cfg, rows in parsed_models:
            nrows, mm = verify_anchored_rows(model_cfg, rows, procs=procs)
            group_rows += nrows
            total_anchored_models += 1
            total_anchored_rows += nrows
            if mm is not None and (group_min is None or mm < group_min):
                group_min = mm
        check(group_rows == exp_rows_hc, f"Verified row count mismatch in {cid}: {group_rows} != {exp_rows_hc}")
        if cid == "A8":
            thmA_verified = True
        print(f"[OK] {cid}: {len(parsed_models)} anchored model(s), {group_rows:,} rows verified exact (min surplus = {float(group_min):.6f}) [{time.time()-t1:.2f}s]", flush=True)

    # Hard-coded final theorem assembly checks
    check(seen_cert_ids == expected_group_ids,
          f"Certificate group set mismatch: got {sorted(seen_cert_ids)}")
    check(total_scalar == EXPECTED_SCALAR_COUNT, f"Total scalar count {total_scalar} != {EXPECTED_SCALAR_COUNT}")
    check(total_anchored_models == sum(m for m, _ in EXPECTED_ANCHORED_GROUPS.values()),
          f"Total anchored model count mismatch: {total_anchored_models}")
    check(total_anchored_rows == sum(r for _, r in EXPECTED_ANCHORED_GROUPS.values()),
          f"Total anchored row count mismatch: {total_anchored_rows}")
    check(thmA_verified, "Theorem A (8 primes, all unrestricted exponents) was NOT verified")
    print("[OK] Theorem A (omega(L) >= 9) and all 6,782 exponent vectors verified unconditionally", flush=True)

    check(total_scalar > 0 and total_anchored_models > 0, "Missing required certificate classes")
    print(
        f"[SUMMARY] Verified Theorem A + {total_scalar} scalar certs + {total_anchored_models} anchored models "
        f"({total_anchored_rows:,} rows), covering all {total_vecs:,} exponent vectors for omega in 9..13 "
        f"in {time.time() - t0:.2f}s.",
        flush=True,
    )
    print("PASS", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Verify odd-covering lower bound certificate package.")
    parser.add_argument("--dir", default=os.path.dirname(os.path.abspath(__file__)),
                        help="Package directory containing MANIFEST.json and certs/ (default: directory of check.py)")
    parser.add_argument("--procs", type=int, default=1,
                        help="Number of worker processes for anchored row verification (default: 1)")
    args = parser.parse_args()
    try:
        check(args.procs >= 1, "--procs must be >= 1")
        run_verification(args.dir, procs=args.procs)
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", flush=True)
        print("FAIL", flush=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
