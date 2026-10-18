#!/opt/homebrew/bin/python3
"""
Standalone exhaustive exact-integer Brent-equation verifier for
object/14x15x15_m1894_ZT.json (format 14x15x15, rank 1894, ring ZT = {-1, 0, 1}).
"""
import sys
import os
import json
import hashlib
import numpy as np

EXPECTED_SHA256 = "bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb"


def fail(msg):
    print(f"ERROR: {msg}")
    print("FAIL")
    sys.exit(1)


def load_uvw(d):
    n1, n2, n3 = d["n"]
    m = int(d["m"])
    if "u" in d and "v" in d and "w" in d:
        U = np.array(d["u"], dtype=np.int64)
        V = np.array(d["v"], dtype=np.int64)
        W = np.array(d["w"], dtype=np.int64)
    elif "u_sparse" in d and "v_sparse" in d and "w_sparse" in d:
        U = np.zeros((m, n1 * n2), dtype=np.int64)
        V = np.zeros((m, n2 * n3), dtype=np.int64)
        W = np.zeros((m, n3 * n1), dtype=np.int64)
        for q, row in enumerate(d["u_sparse"]):
            for idx, val in row:
                U[q, int(idx)] = int(val)
        for q, row in enumerate(d["v_sparse"]):
            for idx, val in row:
                V[q, int(idx)] = int(val)
        for q, row in enumerate(d["w_sparse"]):
            for idx, val in row:
                W[q, int(idx)] = int(val)
    else:
        raise ValueError("Missing u/v/w or u_sparse/v_sparse/w_sparse")
    return n1, n2, n3, m, U, V, W


def verify_scheme_dict(d, require_zt=True):
    n1, n2, n3, m, U, V, W = load_uvw(d)

    if U.shape != (m, n1 * n2) or V.shape != (m, n2 * n3) or W.shape != (m, n3 * n1):
        return False, "shape mismatch"

    max_abs = int(max(np.max(np.abs(U)), np.max(np.abs(V)), np.max(np.abs(W))))
    if require_zt and max_abs > 1:
        return False, f"max_abs={max_abs} > 1"

    zero_terms = int(
        np.count_nonzero(
            (np.max(np.abs(U), axis=1) == 0)
            | (np.max(np.abs(V), axis=1) == 0)
            | (np.max(np.abs(W), axis=1) == 0)
        )
    )
    if zero_terms != 0:
        return False, f"zero_terms={zero_terms}"

    total_eqs = (n1 * n2) * (n2 * n3) * (n3 * n1)
    mismatches = 0
    for i1 in range(n1):
        for i2 in range(n2):
            a = i1 * n2 + i2
            u_col = U[:, a]
            nz = np.nonzero(u_col)[0]
            if len(nz) == 0:
                T_a = np.zeros((n2 * n3, n3 * n1), dtype=np.int64)
            else:
                UV_a = V[nz] * u_col[nz, None]
                T_a = UV_a.T @ W[nz]

            expected = np.zeros((n2 * n3, n3 * n1), dtype=np.int64)
            for i3 in range(n3):
                expected[i2 * n3 + i3, i3 * n1 + i1] = 1

            diff = int(np.count_nonzero(T_a != expected))
            if diff > 0:
                mismatches += diff

    if mismatches != 0:
        return False, f"mismatches={mismatches}/{total_eqs}"

    return True, {
        "n": (n1, n2, n3),
        "m": m,
        "max_abs": max_abs,
        "zero_terms": zero_terms,
        "total_eqs": total_eqs,
        "mismatches": mismatches,
    }


def self_test():
    strassen = {
        "n": [2, 2, 2],
        "m": 7,
        "u": [[1,0,0,1],[0,0,1,1],[1,0,0,0],[0,0,0,1],[1,1,0,0],[-1,0,1,0],[0,1,0,-1]],
        "v": [[1,0,0,1],[1,0,0,0],[0,1,0,-1],[-1,0,1,0],[0,0,0,1],[1,1,0,0],[0,0,1,1]],
        "w": [[1,0,0,1],[0,1,0,-1],[0,0,1,1],[1,1,0,0],[-1,0,1,0],[0,0,0,1],[1,0,0,0]],
    }
    ok_pos, info = verify_scheme_dict(strassen, require_zt=True)
    if not ok_pos:
        fail(f"positive control Strassen 2x2x2 failed: {info}")
    print("control_positive_strassen_2_2_2: PASS (64/64 equations, mismatches=0)")

    bad_brent = json.loads(json.dumps(strassen))
    bad_brent["w"][0][0] = 0
    ok_neg1, _ = verify_scheme_dict(bad_brent, require_zt=True)
    if ok_neg1:
        fail("negative control 1 (corrupted W) unexpectedly passed")
    print("control_negative_corrupted_brent: PASS (rejected)")

    bad_zt = json.loads(json.dumps(strassen))
    bad_zt["u"][0][0] = 2
    ok_neg2, _ = verify_scheme_dict(bad_zt, require_zt=True)
    if ok_neg2:
        fail("negative control 2 (non-ZT entry 2) unexpectedly passed")
    print("control_negative_non_zt_coeff: PASS (rejected)")


def main():
    self_test()
    pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obj_path = os.path.join(pkg_root, "object", "14x15x15_m1894_ZT.json")
    try:
        with open(obj_path, "rb") as f:
            raw = f.read()
        sha = hashlib.sha256(raw).hexdigest()
        d = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        fail(f"failed to load object: {exc}")

    ok, info = verify_scheme_dict(d, require_zt=True)
    if not ok:
        fail(f"object verification failed: {info}")

    if info["n"] != (14, 15, 15) or info["m"] != 1894:
        fail(f"unexpected format/rank: {info}")

    if sha != EXPECTED_SHA256:
        fail(f"sha256 mismatch: {sha} != {EXPECTED_SHA256}")

    print(f"sha256={sha}")
    print("format=14x15x15 rank=1894 ring=ZT max_abs=1 zero_terms=0")
    print("previous_zt_record=1905 previous_z_record=1895 overall_q_record=1848 delta_zt=-11 delta_z=-1")
    print(f"total_brent_equations={info['total_eqs']} mismatches={info['mismatches']}")
    print("PASS")


if __name__ == "__main__":
    main()
