#!/usr/bin/env python3
"""
Standalone Exact Checker for laminar-ef1-four-agent-key-matroids.
Written from first principles using strictly Python standard library.
Checks:
1. Object integrity: Validates valuation_matrix.json, farkas_certificates.json,
   and obstruction_certificate.json with exact inner-product verification.
2. Search space generation: Regenerates all 864 complete feasible allocations
   from the size-8 key matroid group constraints directly.
3. Universal violation audit: Proves every allocation violates ordered no-envy
   or EF1 with positive rational margin.
"""

import sys
import json
import itertools
from fractions import Fraction
from pathlib import Path

def main():
    pkg_dir = Path(__file__).resolve().parent.parent
    obj_dir = pkg_dir / "object"
    matrix_path = obj_dir / "valuation_matrix.json"
    farkas_path = obj_dir / "farkas_certificates.json"
    obstruction_path = obj_dir / "obstruction_certificate.json"

    try:
        # 1. Validate all object files exist
        for p in [matrix_path, farkas_path, obstruction_path]:
            if not p.exists():
                print(f"ERROR: Missing object file at {p}")
                print("FAIL")
                sys.exit(1)

        # 2. Parse and validate valuation matrix
        with open(matrix_path, "r") as f:
            data = json.load(f)

        V_int = data.get("valuation_matrix_integer")
        if not V_int or len(V_int) != 4:
            print("ERROR: Invalid valuation matrix rows")
            print("FAIL")
            sys.exit(1)

        scale = data.get("scale", 100)
        for i, row in enumerate(V_int):
            if len(row) != 8:
                print(f"ERROR: Row {i} length != 8")
                print("FAIL")
                sys.exit(1)
            if any(x < 0 for x in row):
                print(f"ERROR: Row {i} has negative entries")
                print("FAIL")
                sys.exit(1)
            if sum(row) != scale:
                print(f"ERROR: Row {i} sum {sum(row)} != {scale}")
                print("FAIL")
                sys.exit(1)

        # Rational normalized valuations
        V_rat = [[Fraction(x, scale) for x in row] for row in V_int]

        # 3. Validate farkas_certificates.json integrity
        with open(farkas_path, "r") as f:
            farkas_data = json.load(f)
        if farkas_data.get("total_certificates") != 864:
            print("ERROR: farkas total_certificates != 864")
            print("FAIL")
            sys.exit(1)
        if farkas_data.get("ordered_envy_certificates") != 828:
            print("ERROR: farkas ordered_envy_certificates != 828")
            print("FAIL")
            sys.exit(1)
        if farkas_data.get("ef1_certificates") != 36:
            print("ERROR: farkas ef1_certificates != 36")
            print("FAIL")
            sys.exit(1)
        if Fraction(farkas_data.get("minimum_slack", "0")) != Fraction(1, 100):
            print("ERROR: farkas minimum_slack != 1/100")
            print("FAIL")
            sys.exit(1)
        if Fraction(farkas_data.get("stable_l_inf_radius", "0")) != Fraction(1, 400):
            print("ERROR: farkas stable_l_inf_radius != 1/400")
            print("FAIL")
            sys.exit(1)

        certs = farkas_data.get("certificates", [])
        if len(certs) < 20:
            print("ERROR: farkas certificates preview < 20")
            print("FAIL")
            sys.exit(1)
        for c in certs:
            row_idx = c["agent_row"] - 1
            inner = sum(c["normal_vector_row"][g] * V_rat[row_idx][g] for g in range(8))
            ev = Fraction(c["evaluated_value"])
            sm = Fraction(c["separating_margin"])
            if inner != ev:
                print(f"ERROR: Farkas certificate normal vector evaluation mismatch: {inner} != {ev}")
                print("FAIL")
                sys.exit(1)
            if sm != -ev:
                print(f"ERROR: Farkas certificate margin mismatch: {sm} != {-ev}")
                print("FAIL")
                sys.exit(1)

        # 4. Validate obstruction_certificate.json integrity
        with open(obstruction_path, "r") as f:
            obs_data = json.load(f)
        if obs_data.get("total_allocations") != 864 or obs_data.get("valid_allocations") != 0:
            print("ERROR: obstruction allocations count invalid")
            print("FAIL")
            sys.exit(1)
        if obs_data.get("ordered_envy_failures") != 828 or obs_data.get("ef1_failures") != 36:
            print("ERROR: obstruction failure counts invalid")
            print("FAIL")
            sys.exit(1)
        if Fraction(obs_data.get("min_violation_margin", "0")) != Fraction(1, 100):
            print("ERROR: obstruction min_violation_margin != 1/100")
            print("FAIL")
            sys.exit(1)
        records = obs_data.get("records", [])
        if len(records) != 864:
            print("ERROR: obstruction records count != 864")
            print("FAIL")
            sys.exit(1)

        # 5. Regenerate search space from group constraints
        goods = list(range(1, 9))
        G1 = {1, 2, 3}
        G2 = {4, 5, 6}
        G3 = {7, 8}

        valid_bundles = []
        for a, b in itertools.combinations(goods, 2):
            c1 = (a in G1) + (b in G1)
            c2 = (a in G2) + (b in G2)
            c3 = (a in G3) + (b in G3)
            if c1 <= 1 and c2 <= 1 and c3 <= 1:
                valid_bundles.append((a, b))

        allocations = []
        for b1 in valid_bundles:
            rem1 = set(goods) - set(b1)
            for b2 in valid_bundles:
                if not set(b2).issubset(rem1): continue
                rem2 = rem1 - set(b2)
                for b3 in valid_bundles:
                    if not set(b3).issubset(rem2): continue
                    b4 = tuple(sorted(rem2 - set(b3)))
                    if b4 in valid_bundles:
                        allocations.append((b1, b2, b3, b4))

        if len(allocations) != 864:
            print(f"ERROR: Expected 864 allocations, got {len(allocations)}")
            print("FAIL")
            sys.exit(1)

        def val(ag, b):
            return sum(V_rat[ag][g - 1] for g in b)

        def min_val(ag, b):
            return min(V_rat[ag][g - 1] for g in b)

        oe_fails = 0
        ef1_fails = 0
        valid_allocs = 0

        for A in allocations:
            bad = False
            # Ordered no-envy: i < j
            for i in range(4):
                for j in range(i + 1, 4):
                    if val(i, A[i]) < val(i, A[j]):
                        oe_fails += 1
                        bad = True
                        break
                if bad: break

            # EF1: i > j
            if not bad:
                for i in range(4):
                    for j in range(i):
                        if val(i, A[i]) < min_val(i, A[j]):
                            ef1_fails += 1
                            bad = True
                            break
                    if bad: break

            if not bad:
                valid_allocs += 1

        if valid_allocs > 0:
            print(f"ERROR: Found {valid_allocs} valid allocations; counterexample refuted!")
            print("FAIL")
            sys.exit(1)

        print(f"Evaluated all {len(allocations)} complete allocations.")
        print(f"Ordered no-envy violations: {oe_fails}")
        print(f"EF1 violations: {ef1_fails}")
        print("Universal obstruction confirmed: 0 valid allocations exist.")
        print("PASS")
        sys.exit(0)

    except Exception as e:
        print(f"EXCEPTION: {e}")
        print("FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
