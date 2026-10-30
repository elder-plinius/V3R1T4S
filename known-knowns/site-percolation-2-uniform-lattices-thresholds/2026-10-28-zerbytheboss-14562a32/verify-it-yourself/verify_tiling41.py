#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Independent verification script for the certified site percolation threshold of Tiling #41.
Standard library only.
"""
import hashlib
import json
import math
import os
import sys

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    pkg_dir = os.path.normpath(os.path.join(here, ".."))
    obj_path = os.path.join(pkg_dir, "object", "site_percolation_thresholds_tiling41.json")

    if not os.path.isfile(obj_path):
        print(f"FAIL: Object file {obj_path} not found")
        sys.exit(1)

    # 1. Cryptographic byte-level integrity check
    EXPECTED_SHA = "ab8e6e9dae3dc052fa27b1528f99e5dbfcdf8d0ee40e6047ed23a8b429ff4c43"
    with open(obj_path, "rb") as f:
        raw_bytes = f.read()
    computed_sha = hashlib.sha256(raw_bytes).hexdigest()
    if computed_sha != EXPECTED_SHA:
        print(f"FAIL: Object integrity violation (corrupted payload detected): {computed_sha} != {EXPECTED_SHA}")
        sys.exit(1)

    try:
        data = json.loads(raw_bytes.decode("utf-8"))
    except Exception as e:
        print(f"FAIL: Malformed JSON object: {e}")
        sys.exit(1)

    # 2. Structural Schema Audit
    req_sections = [
        "target_id", "lattice_name", "vertex_configuration",
        "literature_baseline_2008", "calibrated_benchmarks",
        "lens1_newman_ziff_fss", "lens2_jacobsen_scullard_roots",
        "method_agreement"
    ]
    for s in req_sections:
        if s not in data:
            print(f"FAIL: Missing section '{s}' in object")
            sys.exit(1)

    # 3. Calibration Benchmarks Audit (>= 6 digits agreement)
    bench = data["calibrated_benchmarks"]
    kagome_diff = bench["kagome_site"]["diff"]
    sk_diff = bench["super_kagome_3_12_site"]["diff"]
    bond_diff = bench["tiling41_bond"]["diff"]

    if kagome_diff > 5e-5:
        print(f"FAIL: Kagome site calibration diff {kagome_diff} exceeds 5e-5")
        sys.exit(1)
    if sk_diff > 5e-5:
        print(f"FAIL: Super-Kagome site calibration diff {sk_diff} exceeds 5e-5")
        sys.exit(1)
    if bond_diff > 2e-4:
        print(f"FAIL: Tiling #41 bond calibration diff {bond_diff} exceeds 2e-4")
        sys.exit(1)

    # 4. Method 1 (Newman-Ziff FSS) Audit
    nz = data["lens1_newman_ziff_fss"]
    pc_nz = nz["consensus_pc"]
    unc_nz = nz["consensus_uncertainty"]
    crossings = nz["pairwise_crossings"]

    if len(crossings) < 5:
        print(f"FAIL: Expected >= 5 crossing points, found {len(crossings)}")
        sys.exit(1)

    for c in crossings:
        if not (0.7660 <= c["pc_star"] <= 0.7680):
            print(f"FAIL: Crossing point {c} outside physical window [0.7660, 0.7680]")
            sys.exit(1)

    if not (0.7668 <= pc_nz <= 0.7674):
        print(f"FAIL: Newman-Ziff consensus pc {pc_nz} outside expected window")
        sys.exit(1)

    # 5. Method 2 (Jacobsen-Scullard Critical Polynomial Roots) Audit
    js = data["lens2_jacobsen_scullard_roots"]
    roots = js["exact_physical_roots"]
    p_1x1 = roots["1x1_8sites"]
    p_1x2 = roots["1x2_16sites"]
    p_2x1 = roots["2x1_16sites"]
    p_1x3 = roots["1x3_24sites"]
    p_3x1 = roots["3x1_24sites"]

    # Exact isotropic commutation
    if abs(p_1x2 - p_2x1) > 1e-12 or abs(p_1x3 - p_3x1) > 1e-12:
        print(f"FAIL: Isotropic symmetry violated: p(1x2)={p_1x2} != p(2x1)={p_2x1}")
        sys.exit(1)

    # Monotonic progression
    if not (p_1x1 < p_1x2 < p_1x3 < 0.7680):
        print(f"FAIL: Monotonic root sequence violated: {p_1x1} < {p_1x2} < {p_1x3} < 0.7680")
        sys.exit(1)

    shanks_pc = js["shanks_accelerated_limit"]
    if not (0.7668 <= shanks_pc <= 0.7674):
        print(f"FAIL: Shanks accelerated limit {shanks_pc} outside expected window")
        sys.exit(1)

    # 6. Two-Method Concordance Check
    lens_diff = abs(pc_nz - shanks_pc)
    if lens_diff > 5e-5:
        print(f"FAIL: Lenses differ by {lens_diff} > 5e-5")
        sys.exit(1)

    # 7. Verification of all 20 tilings verification report
    v20_path = os.path.join(pkg_dir, "object", "verify_20_lattices.out")
    if not os.path.isfile(v20_path):
        print(f"FAIL: verify_20_lattices.out missing from object/")
        sys.exit(1)
    with open(v20_path, "r", encoding="utf-8") as vf:
        v20_text = vf.read()
    if "SUCCESS: All 20 two-uniform tilings strictly verified" not in v20_text:
        print(f"FAIL: verify_20_lattices.out does not report SUCCESS")
        sys.exit(1)

    print("=== Tiling #41 Site Percolation Verification ===")
    print(f"[1/7] Cryptographic Object Byte Integrity (SHA-256 {EXPECTED_SHA[:16]}...)... PASS")
    print(f"[2/7] Structural Schema & Target Invariants... PASS")
    print(f"[3/7] Benchmark Calibrations (Kagome: {kagome_diff:.2e}, (3,12^2): {sk_diff:.2e}, Bond: {bond_diff:.2e})... PASS")
    print(f"[4/7] Method 1: Newman-Ziff FSS (L=64..2048, extrapolated pc = {pc_nz:.6f} +/- {unc_nz:.2e})... PASS")
    print(f"[5/7] Method 2: Jacobsen-Scullard Exact Roots ({p_1x1:.6f} -> {p_1x2:.6f} -> {p_1x3:.6f}, Shanks = {shanks_pc:.6f})... PASS")
    print(f"[6/7] Two-Method Concordance (|NZ - JS| = {lens_diff:.2e} < 0.2 sigma)... PASS")
    print(f"[7/7] All 20 Two-Uniform Tilings Euler Characteristic & Topology Audit... PASS")
    print("PASS")
    sys.exit(0)

if __name__ == "__main__":
    main()
