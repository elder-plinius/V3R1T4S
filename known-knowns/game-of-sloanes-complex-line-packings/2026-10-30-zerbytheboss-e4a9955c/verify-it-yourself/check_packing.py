#!/usr/bin/env python3
"""Standalone high-precision complex line packing checker.
Evaluates pairwise Hermitian inner products in 40-digit mpmath after normalization.
"""

import sys
import os
import hashlib
import mpmath

EXPECTED_SHA = "e4a9955cacd99a53c63ab4c8df9b4c20fe63a0876ea1766437eadf49476e9346"

def check():
    mpmath.mp.dps = 40
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obj_path = os.path.join(pkg_dir, "object", "5x47_v3r1t4s.txt")

    d, n = 5, 47
    table_best = mpmath.mpf("0.53660699")
    lower_bound = mpmath.mpf("0.50395263")
    min_margin = mpmath.mpf("1e-8")

    if not os.path.isfile(obj_path):
        print(f"FAIL: Object file not found: {obj_path}")
        return False

    with open(obj_path, "rb") as f:
        data_bytes = f.read()

    actual_sha = hashlib.sha256(data_bytes).hexdigest()
    if actual_sha != EXPECTED_SHA:
        print(f"FAIL: SHA256 mismatch: expected {EXPECTED_SHA}, got {actual_sha}")
        return False

    try:
        text = data_bytes.decode("utf-8")
        vals = [mpmath.mpf(line.strip()) for line in text.splitlines() if line.strip()]
    except Exception as e:
        print(f"FAIL: Could not parse floating point values: {e}")
        return False

    if len(vals) != 2 * d * n:
        print(f"FAIL: Expected {2*d*n} values, got {len(vals)}")
        return False

    reals = vals[:d*n]
    imags = vals[d*n:]

    vecs = []
    for j in range(n):
        v = [mpmath.mpc(reals[j*d + m], imags[j*d + m]) for m in range(d)]
        norm = mpmath.sqrt(sum(c.real**2 + c.imag**2 for c in v))
        if norm <= mpmath.mpf("1e-20"):
            print(f"FAIL: Vector {j} has degenerate norm {norm}")
            return False
        vecs.append([c / norm for c in v])

    max_c = mpmath.mpf(0)
    for j in range(n):
        for k in range(j+1, n):
            ip = sum(vecs[j][m].conjugate() * vecs[k][m] for m in range(d))
            overlap = mpmath.sqrt(ip.real**2 + ip.imag**2)
            if overlap > max_c:
                max_c = overlap

    drop = table_best - max_c
    print("Object: object/5x47_v3r1t4s.txt")
    print(f"Dimension d={d}, Lines n={n}")
    print(f"Computed Coherence mu (40 digits): {max_c}")
    print(f"Leaderboard Record Coherence    : {table_best}")
    print(f"Theoretical Lower Bound         : {lower_bound}")
    print(f"Strict Lowering Margin          : {drop}")

    if max_c < lower_bound:
        print("FAIL: Coherence is strictly below lower bound")
        return False
    if drop < min_margin:
        print("FAIL: Lowering margin is strictly less than 1e-8")
        return False

    print(f"VERIFIED: mu = {max_c} strictly beats {table_best} by {drop} >= 1e-8")
    print("PASS")
    return True

if __name__ == "__main__":
    if check():
        sys.exit(0)
    else:
        sys.exit(1)
