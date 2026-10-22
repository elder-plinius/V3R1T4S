#!/usr/bin/env python3
"""Standalone stdlib-only verifier for fmm-ternary-integer-ring-upgrade (object/6x12x14_m654_ZT.json)."""
import csv
import hashlib
import json
import os
import random
import sys


def verify_file(pkg_root):
    idx_path = os.path.join(pkg_root, "INDEX.csv")
    with open(idx_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        print("FAIL: expected 1 data row in INDEX.csv")
        return False
    row = rows[0]
    obj_rel = row["file"].strip()
    obj_path = os.path.join(pkg_root, obj_rel)
    if not os.path.isfile(obj_path):
        print(f"FAIL: missing {obj_rel}")
        return False
    raw = open(obj_path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != row["sha256"].strip():
        print(f"FAIL: sha256 mismatch ({sha} != {row['sha256'].strip()})")
        return False

    try:
        d = json.loads(raw.decode("utf-8"))
    except Exception as e:
        print(f"FAIL: invalid JSON ({e})")
        return False

    n1, n2, n3 = d.get("n", [0, 0, 0])
    m = int(d.get("m", 0))
    U, V, W = d.get("u", []), d.get("v", []), d.get("w", [])
    if [n1, n2, n3] != [6, 12, 14] or m != 654 or int(row["value"]) != 654:
        print(f"FAIL: header mismatch n={[n1,n2,n3]} m={m}")
        return False
    if len(U) != m or len(V) != m or len(W) != m:
        print("FAIL: factor row count mismatch")
        return False
    dU, dV, dW = n1 * n2, n2 * n3, n3 * n1

    u_nz, v_nz, w_nz = [], [], []
    for r in range(m):
        ur, vr, wr = U[r], V[r], W[r]
        if len(ur) != dU or len(vr) != dV or len(wr) != dW:
            print(f"FAIL: dimension mismatch at product {r}")
            return False
        unz_r, vnz_r, wnz_r = [], [], []
        for idx, val in enumerate(ur):
            if type(val) is not int or val not in (-1, 0, 1):
                print(f"FAIL: non-ternary U[{r}][{idx}]={val}")
                return False
            if val:
                unz_r.append((idx, val))
        for idx, val in enumerate(vr):
            if type(val) is not int or val not in (-1, 0, 1):
                print(f"FAIL: non-ternary V[{r}][{idx}]={val}")
                return False
            if val:
                vnz_r.append((idx, val))
        for idx, val in enumerate(wr):
            if type(val) is not int or val not in (-1, 0, 1):
                print(f"FAIL: non-ternary W[{r}][{idx}]={val}")
                return False
            if val:
                wnz_r.append((idx, val))
        u_nz.append(unz_r)
        v_nz.append(vnz_r)
        w_nz.append(wnz_r)

    # Accumulate all 1,016,064 Brent equations over Z via sparse outer products
    accum = {}
    for r in range(m):
        for a, ua in u_nz[r]:
            for b, vb in v_nz[r]:
                uavb = ua * vb
                ab = a * dV + b
                for c, wc in w_nz[r]:
                    key = ab * dW + c
                    accum[key] = accum.get(key, 0) + uavb * wc

    expected = set()
    for i in range(n1):
        for k in range(n2):
            a = i * n2 + k
            for j in range(n3):
                b = k * n3 + j
                c = j * n1 + i
                expected.add((a * dV + b) * dW + c)

    brent_errors = 0
    for key in expected:
        if accum.get(key, 0) != 1:
            brent_errors += 1
    for key, val in accum.items():
        if key not in expected and val != 0:
            brent_errors += 1

    if brent_errors != 0:
        print(f"FAIL: {brent_errors} Brent equation errors over Z")
        return False

    # Also verify 10 random integer matrix products A * B = C
    rng = random.Random(20261017)
    for trial in range(10):
        A = [rng.randint(-9, 9) for _ in range(dU)]
        B = [rng.randint(-9, 9) for _ in range(dV)]
        C_alg = [0] * dW
        for r in range(m):
            sa = sum(A[idx] * val for idx, val in u_nz[r])
            sb = sum(B[idx] * val for idx, val in v_nz[r])
            prod = sa * sb
            if prod:
                for idx, val in w_nz[r]:
                    C_alg[idx] += prod * val
        for i in range(n1):
            for j in range(n3):
                ref = sum(A[i * n2 + k] * B[k * n3 + j] for k in range(n2))
                if C_alg[j * n1 + i] != ref:
                    print(f"FAIL: matrix product mismatch on trial {trial}")
                    return False

    print(
        f"VERIFIED: 6x12x14 rank={m} ring=ZT max_abs=(1,1,1) "
        f"brent_equations={dU*dV*dW} brent_errors=0 random_trials=10/10"
    )
    print("PASS")
    return True


if __name__ == "__main__":
    pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not verify_file(pkg_root):
        print("FAIL")
        sys.exit(1)
