#!/usr/bin/env python3
"""Standalone stdlib-only verifier for fmm-additive-complexity-records (4x5x5_m76_cr280_ZT_reduced.json)."""
import csv
import hashlib
import json
import os
import random
import sys


def expand_factor(n_inputs, fresh_list, out_list):
    vecs = []

    def vec_of(form, limit):
        if not isinstance(form, list) or len(form) == 0:
            raise ValueError("Empty form")
        out = {}
        for t in form:
            i = int(t["index"])
            c = int(t["value"])
            if c not in (-1, 1):
                raise ValueError(f"Non-unit SLP coefficient {c}")
            if not (0 <= i < limit):
                raise ValueError(f"Index {i} out of straight-line order (limit {limit})")
            src = {i: 1} if i < n_inputs else vecs[i - n_inputs]
            for k, v in src.items():
                out[k] = out.get(k, 0) + c * v
        return {k: v for k, v in out.items() if v != 0}

    for f in fresh_list:
        if len(f) < 2:
            raise ValueError("Fresh form must have length >= 2")
        vecs.append(vec_of(f, n_inputs + len(vecs)))

    dense = []
    for f in out_list:
        comb = vec_of(f, n_inputs + len(vecs))
        row = [comb.get(i, 0) for i in range(n_inputs)]
        for c in row:
            if c not in (-1, 0, 1):
                raise ValueError(f"Expanded coefficient {c} not in {{-1,0,1}}")
        dense.append(row)

    adds = sum(len(f) - 1 for f in fresh_list) + sum(len(f) - 1 for f in out_list)
    return dense, adds


def run_slp(fresh_list, out_list, inputs):
    vals = list(inputs)
    for f in fresh_list:
        vals.append(sum(int(t["value"]) * vals[int(t["index"])] for t in f))
    return [sum(int(t["value"]) * vals[int(t["index"])] for t in f) for f in out_list]


def verify_pkg(pkg_root):
    idx_path = os.path.join(pkg_root, "INDEX.csv")
    with open(idx_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        print("FAIL: expected 1 row in INDEX.csv")
        return False
    row = rows[0]
    obj_rel = row["file"].strip()
    obj_path = os.path.join(pkg_root, obj_rel)
    raw = open(obj_path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != row["sha256"].strip():
        print(f"FAIL: sha256 mismatch ({sha} != {row['sha256'].strip()})")
        return False

    try:
        d = json.loads(raw.decode("utf-8"))
        n1, n2, n3 = d["n"]
        m = int(d["m"])
        if [n1, n2, n3] != [4, 5, 5] or m != 76:
            print("FAIL: unexpected n or m")
            return False
        U, adds_u = expand_factor(n1 * n2, d["u_fresh"], d["u"])
        V, adds_v = expand_factor(n2 * n3, d["v_fresh"], d["v"])
        W_out, adds_w = expand_factor(m, d["w_fresh"], d["w"])
    except Exception as e:
        print(f"FAIL: expansion error ({e})")
        return False

    if len(U) != m or len(V) != m or len(W_out) != n3 * n1:
        print("FAIL: factor dimensions mismatch")
        return False

    W = [[W_out[c][r] for c in range(n3 * n1)] for r in range(m)]
    total_adds = adds_u + adds_v + adds_w
    if total_adds != 280 or int(row["value"]) != 280:
        print(f"FAIL: addition count mismatch ({total_adds})")
        return False

    # Check all 10,000 Brent equations over Z (C^T indexing: c = j2 * n1 + i2)
    dU, dV, dW = n1 * n2, n2 * n3, n3 * n1
    brent_errors = 0
    for i in range(n1):
        for k in range(n2):
            a = i * n2 + k
            for k2 in range(n2):
                for j in range(n3):
                    b = k2 * n3 + j
                    for j2 in range(n3):
                        for i2 in range(n1):
                            c = j2 * n1 + i2
                            s = sum(U[r][a] * V[r][b] * W[r][c] for r in range(m))
                            target = 1 if (i == i2 and k == k2 and j == j2) else 0
                            if s != target:
                                brent_errors += 1
    if brent_errors != 0:
        print(f"FAIL: {brent_errors} Brent equation errors")
        return False

    # Check 20 random integer matrix products directly via SLP execution
    rng = random.Random(20261017)
    for _ in range(20):
        A = [rng.randint(-50, 50) for _ in range(dU)]
        B = [rng.randint(-50, 50) for _ in range(dV)]
        pu = run_slp(d["u_fresh"], d["u"], A)
        pv = run_slp(d["v_fresh"], d["v"], B)
        prods = [x * y for x, y in zip(pu, pv)]
        C_slp = run_slp(d["w_fresh"], d["w"], prods)
        for i in range(n1):
            for j in range(n3):
                ref = sum(A[i * n2 + k] * B[k * n3 + j] for k in range(n2))
                if C_slp[j * n1 + i] != ref:
                    print("FAIL: matrix multiplication mismatch")
                    return False

    print(
        f"VERIFIED: 4x5x5 rank={m} adds_U={adds_u} adds_V={adds_v} adds_W={adds_w} "
        f"cr={total_adds} brent_equations=10000 brent_errors=0"
    )
    print("PASS")
    return True


if __name__ == "__main__":
    pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not verify_pkg(pkg_root):
        print("FAIL")
        sys.exit(1)
