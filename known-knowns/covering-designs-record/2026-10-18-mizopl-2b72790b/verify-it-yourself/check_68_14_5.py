#!/usr/bin/env python3
"""Standalone exhaustive verifier for C(68, 14, 5) <= 15,675.

Checks:
1. Positive control: Fano plane C(7, 3, 2) = 7 passes (uncovered = 0).
2. Negative control: Fano plane minus 1 block fails (uncovered = 3 > 0).
3. Object check on object/design_68_14_5.txt:
   - Exact line count = 15,675
   - Every block has 14 distinct integers in {1, ..., 68}
   - All 15,675 blocks are distinct
   - Schonheim lower bound L(68, 14, 5) = 5,785 <= 15,675
   - Every one of the C(68, 5) = 10,424,128 5-subsets of {1, ..., 68} is covered (uncovered = 0)
   - Strictly beats the Covering Repository record (16,004) and La Jolla Covering Repository record (16,004) by 329 blocks.

Prints PASS on the final line if and only if every check succeeds; otherwise prints FAIL and exits 1.
"""
import hashlib
import os
import sys
from itertools import combinations
from math import ceil
import numpy as np


def schonheim(v, k, t):
    b = 1
    for i in range(t - 1, -1, -1):
        b = ceil(b * (v - i) / (k - i))
    return b


def check_design(v, k, t, blocks):
    C = np.zeros((v + 1, t + 1), dtype=np.int64)
    for n in range(v + 1):
        C[n, 0] = 1
        for r in range(1, min(n, t) + 1):
            C[n, r] = C[n - 1, r - 1] + C[n - 1, r]
    total = int(C[v, t])
    covered = np.zeros(total, dtype=np.uint8)
    idx = np.array(list(combinations(range(k), t)), dtype=np.int64)
    weights = [C[np.arange(v), r + 1] for r in range(t)]
    for b in blocks:
        pts = np.array(b, dtype=np.int64)
        sub = pts[idx]
        ranks = sum(weights[r][sub[:, r]] for r in range(t))
        covered[ranks] = 1
    uncovered = int(total - int(covered.sum()))
    return total, uncovered


def fail(msg):
    print("ERROR: " + msg)
    print("FAIL")
    sys.exit(1)


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obj_path = os.path.join(root, "object", "design_68_14_5.txt")
    if not os.path.isfile(obj_path):
        fail("Missing object/design_68_14_5.txt")

    # 1. Positive + negative controls on Fano plane C(7, 3, 2) = 7
    fano = [
        [0, 1, 3], [1, 2, 4], [2, 3, 5], [3, 4, 6],
        [0, 4, 5], [1, 5, 6], [0, 2, 6],
    ]
    tot7, unc7_pos = check_design(7, 3, 2, fano)
    _, unc7_neg = check_design(7, 3, 2, fano[:-1])
    if tot7 != 21 or unc7_pos != 0 or unc7_neg != 3:
        fail(f"Control check failed: tot7={tot7} unc7_pos={unc7_pos} unc7_neg={unc7_neg}")
    print("control_positive_fano_7_3_2: PASS (21/21 covered, uncovered=0)")
    print("control_negative_fano_minus_1: PASS (rejected with uncovered=3)")

    # 2. Load and validate object/design_68_14_5.txt
    raw = open(obj_path, "rb").read()
    sha256 = hashlib.sha256(raw).hexdigest()
    expected_sha256 = "2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07"
    lines = [l.strip() for l in raw.decode("utf-8", "replace").splitlines() if l.strip()]
    v, k, t = 68, 14, 5
    expected_b = 15675
    cr_record = 16004
    ljcr_record = 16004

    if len(lines) != expected_b:
        fail(f"Expected {expected_b} blocks, found {len(lines)}")

    blocks = []
    seen = set()
    for lineno, line in enumerate(lines, 1):
        parts = line.split()
        if len(parts) != k:
            fail(f"Line {lineno}: expected {k} integers, got {len(parts)}")
        try:
            pts = [int(x) for x in parts]
        except ValueError:
            fail(f"Line {lineno}: non-integer token")
        if any(x < 1 or x > v for x in pts):
            fail(f"Line {lineno}: point outside 1..{v}")
        if len(set(pts)) != k or pts != sorted(pts):
            fail(f"Line {lineno}: duplicate or unsorted points in block")
        zb = tuple(x - 1 for x in pts)
        seen.add(zb)
        blocks.append(list(zb))

    if len(seen) != expected_b:
        fail(f"Duplicate blocks found: distinct={len(seen)} vs total={expected_b}")

    lb = schonheim(v, k, t)
    if lb != 5785 or len(blocks) < lb:
        fail(f"Schonheim bound violation: b={len(blocks)} < L={lb}")

    if not (len(blocks) < cr_record and len(blocks) < ljcr_record):
        fail(f"Does not strictly beat record: b={len(blocks)} vs CR={cr_record}, LJCR={ljcr_record}")

    total_subsets, uncovered = check_design(v, k, t, blocks)
    print(f"sha256={sha256}")
    print(f"v={v} k={k} t={t} blocks={len(blocks)} distinct={len(seen)}")
    print(f"schonheim_lower_bound={lb}")
    print(f"previous_cr_record={cr_record} previous_ljcr_record={ljcr_record} delta={len(blocks) - cr_record}")
    print(f"total_5_subsets={total_subsets} uncovered={uncovered}")

    if total_subsets != 10424128 or uncovered != 0:
        fail(f"Coverage failed: uncovered={uncovered} out of {total_subsets}")

    print("PASS")


if __name__ == "__main__":
    main()
