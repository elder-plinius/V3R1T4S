#!/opt/homebrew/bin/python3
"""
Standalone exhaustive exact-integer Brent-equation verifier for the 7 fast matrix
multiplication schemes in object/ (6 ZT = {-1, 0, 1} upgrades + 1 Z record upgrade)
and object/CERTIFICATE.json (submission 2026-10-22-mizopl-5ab48b6b).
"""
import sys
import os
import json
import hashlib
import numpy as np

EXPECTED_CERT_SHA256 = "4050811589871e8e0b91e766d8587a39fe00649cce86b6e1fb974e755aae0bcf"


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

    nnz_u = int(np.count_nonzero(U))
    nnz_v = int(np.count_nonzero(V))
    nnz_w = int(np.count_nonzero(W))
    complexity = nnz_u + nnz_v + nnz_w - 2 * m - (n3 * n1)

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
        "n": [n1, n2, n3],
        "m": m,
        "max_abs": max_abs,
        "zero_terms": zero_terms,
        "nnz_u": nnz_u,
        "nnz_v": nnz_v,
        "nnz_w": nnz_w,
        "total_nnz": nnz_u + nnz_v + nnz_w,
        "complexity": complexity,
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
    cert_path = os.path.join(pkg_root, "object", "CERTIFICATE.json")
    if not os.path.exists(cert_path):
        cert_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "claim", "CERTIFICATE.json")
        pkg_root = os.path.dirname(os.path.abspath(__file__))

    with open(cert_path, "rb") as f:
        cert_raw = f.read()
    cert_sha = hashlib.sha256(cert_raw).hexdigest()
    if cert_sha != EXPECTED_CERT_SHA256:
        fail(f"CERTIFICATE.json sha256 mismatch: {cert_sha} != {EXPECTED_CERT_SHA256}")
    cert = json.loads(cert_raw.decode("utf-8"))
    print(f"certificate_sha256={cert_sha} (PASS)")

    total_eqs_all = 0
    for entry in cert["schemes"]:
        rel_file = entry["file"]
        obj_path = os.path.join(pkg_root, rel_file)
        if not os.path.exists(obj_path):
            obj_path = os.path.join(pkg_root, "claim", os.path.basename(rel_file))
        with open(obj_path, "rb") as f:
            raw = f.read()
        sha = hashlib.sha256(raw).hexdigest()
        if sha != entry["sha256"]:
            fail(f"{rel_file} sha256 mismatch: {sha} != {entry['sha256']}")
        if len(raw) != entry["bytes"]:
            fail(f"{rel_file} byte size mismatch: {len(raw)} != {entry['bytes']}")

        d = json.loads(raw.decode("utf-8"))
        req_zt = (entry["ring"] == "ZT")
        ok, info = verify_scheme_dict(d, require_zt=req_zt)
        if not ok:
            fail(f"{rel_file} verification failed: {info}")

        if info["n"] != entry["dimensions"] or info["m"] != entry["rank"]:
            fail(f"{rel_file} dimension/rank mismatch: {info} vs {entry}")
        if info["max_abs"] != entry["max_abs"]:
            fail(f"{rel_file} max_abs mismatch: {info['max_abs']} != {entry['max_abs']}")
        if info["complexity"] != entry["complexity"]:
            fail(f"{rel_file} complexity mismatch: {info['complexity']} != {entry['complexity']}")
        if info["nnz_u"] != entry["nnz_u"] or info["nnz_v"] != entry["nnz_v"] or info["nnz_w"] != entry["nnz_w"]:
            fail(f"{rel_file} nnz mismatch: {info} vs {entry}")

        total_eqs_all += info["total_eqs"]
        print(
            f"verified {entry['format']:8s} [{entry['ring']:2s}] rank={info['m']:4d} "
            f"(prev_ZT={entry['previous_zt_rank']}, prev_Z={entry['previous_z_rank']}, Q={entry['overall_q_rank']}) "
            f"max_abs={info['max_abs']} complexity={info['complexity']:5d} "
            f"eqs={info['total_eqs']:7d} mismatches=0 sha256={sha[:16]}..."
        )

    if total_eqs_all != cert["totals"]["total_exact_int64_brent_equations_verified"]:
        fail(f"total equations mismatch: {total_eqs_all}")

    print(f"VERIFIED: {len(cert['schemes'])}/{len(cert['schemes'])} schemes (6 ZT + 1 Z), {total_eqs_all}/{total_eqs_all} exact integer Brent equations PASS")
    print("PASS")


if __name__ == "__main__":
    main()
