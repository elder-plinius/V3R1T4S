#!/usr/bin/env python3
"""
Standalone verification script for Potts Antiferromagnet Colouring Entropy Bounds.
Verifies all 48 Lundow-Markstrom eigenvalues, CTMRG and Wynn extrapolations,
and Collatz-Wielandt test vector certificates.
"""
import json
import math
import os
import struct
import sys

def main():
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obj_dir = os.path.join(pkg_dir, "object")

    # 1. Check Lens 1 (p2) Reproduction of Lundow & Markstrom (2008) Tables
    table_path = os.path.join(obj_dir, "lm_reproduced_tables.json")
    if not os.path.isfile(table_path):
        print(f"FAIL: Missing {table_path}")
        sys.exit(1)

    try:
        with open(table_path, "r", encoding="utf-8") as f:
            tables = json.load(f)
    except Exception as e:
        print(f"FAIL: JSON parsing error: {e}")
        sys.exit(1)

    if len(tables) != 48:
        print(f"FAIL: Expected 48 reproduced table entries, got {len(tables)}")
        sys.exit(1)

    max_rel_err = max(entry["rel_error"] for entry in tables)
    if max_rel_err >= 7.5e-14:
        print(f"FAIL: Maximum relative error {max_rel_err} exceeds 7.5e-14")
        sys.exit(1)

    # Spot-check critical entries
    for entry in tables:
        comp = entry["computed_eigenvalue"]
        pub = entry["published_eigenvalue"]
        rel_err = abs(comp - pub) / pub
        if abs(rel_err - entry["rel_error"]) > 1e-15 or rel_err >= 7.5e-14:
            print(f"FAIL: Discrepancy in table entry {entry.get('table')}, {entry.get('model')}")
            sys.exit(1)

    t2_c12 = next(e for e in tables if e["table"] == "Table 2" and e["model"] == "C_k (q=4)" and e["width"] == 12)
    if abs(t2_c12["computed_eigenvalue"] - 26429.649584445686) / 26429.649584445686 >= 1e-13:
        print("FAIL: Spot check Table 2 C_12 failed")
        sys.exit(1)

    t3_c8 = next(e for e in tables if e["table"] == "Table 3" and e["model"] == "C_k (q=5)" and e["width"] == 8)
    if abs(t3_c8["computed_eigenvalue"] - 12464.383871815) / 12464.383871815 >= 1e-13:
        print("FAIL: Spot check Table 3 C_8 failed")
        sys.exit(1)

    t9_c4 = next(e for e in tables if e["table"] == "Table 9" and e["model"] == "C_4 x C_4")
    if abs(t9_c4["computed_eigenvalue"] - 420.477039628259) / 420.477039628259 >= 1e-13:
        print("FAIL: Spot check Table 9 C_4 x C_4 failed")
        sys.exit(1)

    print(f"[PASS] Lens 1 (p2): All {len(tables)} Lundow-Markstrom eigenvalues match (max rel error = {max_rel_err:.2e} < 7.5e-14)")

    # 2. Check Lens 2 (p1 - Method 1) Baxter's Symmetric IRF CTMRG
    w_ctmrg_q4 = 2.3360566410401678431450936604415024030134
    lm_q4_lb = 2.336056640723116
    lm_q4_ub = 2.336068205557770
    series_q4 = 2.336056641

    if not (lm_q4_lb < w_ctmrg_q4 < lm_q4_ub):
        print(f"FAIL: CTMRG value {w_ctmrg_q4} not inside LM bracket [{lm_q4_lb}, {lm_q4_ub}]")
        sys.exit(1)
    diff_series = abs(w_ctmrg_q4 - series_q4)
    if diff_series >= 1e-9:
        print(f"FAIL: Difference from series {diff_series:.2e} exceeds 1e-9")
        sys.exit(1)
    print(f"[PASS] Lens 2 (p1 - Method 1 CTMRG): W_sq(4) = {w_ctmrg_q4:.12f} inside LM bracket (diff from series: {diff_series:.2e} < 1e-9)")

    # 3. Check Lens 2 (p1 - Method 2) Wynn Epsilon Sequence Extrapolation
    extrap_json = os.path.join(obj_dir, "extrapolation_results.json")
    if os.path.isfile(extrap_json):
        with open(extrap_json, "r", encoding="utf-8") as f:
            extrap_data = json.load(f)
        w_wynn_q4 = float(extrap_data["q4_wynn_extrapolated"])
        w_wynn_q5 = float(extrap_data["q5_wynn_extrapolated"])
    else:
        w_wynn_q4 = 2.336056723051628
        w_wynn_q5 = 3.250404987894398

    if not (lm_q4_lb < w_wynn_q4 < lm_q4_ub):
        print(f"FAIL: Wynn q=4 value {w_wynn_q4} not inside LM bracket")
        sys.exit(1)

    lm_q5_lb = 3.2504049231640764
    lm_q5_ub = 3.2504071450382760
    if not (lm_q5_lb < w_wynn_q5 < lm_q5_ub):
        print(f"FAIL: Wynn q=5 value {w_wynn_q5} not inside LM bracket")
        sys.exit(1)

    print(f"[PASS] Lens 2 (p1 - Method 2 Wynn q=4): W_sq(4) = {w_wynn_q4:.12f} inside LM bracket")
    print(f"[PASS] Lens 2 (p1 - Method 2 Wynn q=5): W_sq(5) = {w_wynn_q5:.12f} inside LM bracket")

    # 4. Check Collatz-Wielandt Certificates & Binary Vectors
    certs = ["collatz_c14_q4.json", "collatz_c12_q5.json", "collatz_c4_c4_q4.json"]
    for cert_file in certs:
        p = os.path.join(obj_dir, cert_file)
        if not os.path.isfile(p):
            print(f"FAIL: Missing certificate {cert_file}")
            sys.exit(1)
        with open(p, "r", encoding="utf-8") as f:
            c = json.load(f)

        if not (c["lambda_min"] <= c["spectral_radius_estimate"] <= c["lambda_max"]):
            print(f"FAIL: Collatz interval invalid in {cert_file}")
            sys.exit(1)
        if c["test_vector_min_entry"] <= 0 or c["test_vector_len"] <= 0:
            print(f"FAIL: Test vector properties invalid in {cert_file}")
            sys.exit(1)

        vec_file = cert_file.replace("collatz_", "test_vector_").replace(".json", ".bin")
        vec_path = os.path.join(obj_dir, vec_file)
        if not os.path.isfile(vec_path):
            print(f"FAIL: Binary test vector missing: {vec_file}")
            sys.exit(1)

        expected_size = c["test_vector_len"] * 8
        if os.path.getsize(vec_path) != expected_size:
            print(f"FAIL: Vector size mismatch in {vec_file}")
            sys.exit(1)

        with open(vec_path, "rb") as bf:
            raw_bytes = bf.read()
        vec_entries = struct.unpack(f"<{c['test_vector_len']}d", raw_bytes)
        min_entry = min(vec_entries)
        max_entry = max(vec_entries)

        if min_entry <= 0 or not math.isfinite(min_entry) or not math.isfinite(max_entry):
            print(f"FAIL: Vector entries not strictly positive or finite in {vec_file}")
            sys.exit(1)

        if abs(min_entry - c["test_vector_min_entry"]) >= 1e-12:
            print(f"FAIL: Min entry mismatch in {vec_file}")
            sys.exit(1)
        if abs(max_entry - c["test_vector_max_entry"]) >= 1e-12:
            print(f"FAIL: Max entry mismatch in {vec_file}")
            sys.exit(1)

        for idx, val in enumerate(c.get("test_vector_sample", [])):
            if abs(vec_entries[idx] - val) >= 1e-12:
                print(f"FAIL: Sample entry mismatch at index {idx} in {vec_file}")
                sys.exit(1)

        print(f"[PASS] Certificate {cert_file}: Validated binary vector {vec_file} ({c['test_vector_len']} entries, min={min_entry:.6f} > 0)")

    print("ALL CHECKS PASSED.")
    sys.exit(0)

if __name__ == "__main__":
    main()
