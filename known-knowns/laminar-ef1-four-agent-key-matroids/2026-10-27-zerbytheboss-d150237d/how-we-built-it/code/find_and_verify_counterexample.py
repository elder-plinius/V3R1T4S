#!/usr/bin/env python3
"""
Lens 1: Exact SMT search and independent rational verification of Cookson-Shah
four-agent key matroid counterexample on 8 goods.
"""

import sys
import json
import itertools
from fractions import Fraction
from pathlib import Path

def main():
    print("=== Lens 1: Exact SMT Counterexample Search and Verification ===")

    # Group constraints for size-8 key matroid
    goods = list(range(1, 9))
    G1 = {1, 2, 3}
    G2 = {4, 5, 6}
    G3 = {7, 8}

    # 1. Enumerate all valid bundles: size 2, at most 1 good per group
    valid_bundles = []
    for a, b in itertools.combinations(goods, 2):
        c1 = (a in G1) + (b in G1)
        c2 = (a in G2) + (b in G2)
        c3 = (a in G3) + (b in G3)
        if c1 <= 1 and c2 <= 1 and c3 <= 1:
            valid_bundles.append((a, b))
    print(f"Generated {len(valid_bundles)} valid candidate bundles of size 2.")

    # 2. Enumerate all 864 complete feasible labeled allocations (A1, A2, A3, A4)
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
    print(f"Generated {len(allocations)} complete feasible labeled allocations.")
    assert len(allocations) == 864, f"Expected 864 allocations, got {len(allocations)}"

    # 3. Discovered exact counterexample valuation matrix (integer representation, scale 100)
    # Rows correspond to agents 1, 2, 3, 4; columns to goods 1..8
    V_int = [
        [1, 15, 25, 7, 0, 12, 19, 21],
        [7, 23, 20, 17, 0, 8, 13, 12],
        [0, 12, 62, 0, 7, 14, 1, 4],
        [0, 78, 6, 10, 3, 0, 1, 2]
    ]

    # Verify each row sums to 100
    for i, row in enumerate(V_int):
        assert sum(row) == 100, f"Agent {i+1} row does not sum to 100"
    print("Verified integer valuation matrix (each agent sum = 100):")
    for i, row in enumerate(V_int):
        print(f"  Agent {i+1}: {row}")

    # Exact rational normalized valuations: v_i(g) in Q, sum = 1
    V_rat = [[Fraction(x, 100) for x in row] for row in V_int]

    # Helper evaluation functions using exact Fraction arithmetic
    def val(agent_idx, bundle):
        return sum(V_rat[agent_idx][g - 1] for g in bundle)

    def min_val(agent_idx, bundle):
        return min(V_rat[agent_idx][g - 1] for g in bundle)

    # 4. Check all 864 allocations for ordered no-envy and EF1
    obstruction_records = []
    oe_count = 0
    ef1_count = 0

    for idx, A in enumerate(allocations):
        # A is a tuple of 4 bundles: A[0] is Agent 1, A[1] Agent 2, A[2] Agent 3, A[3] Agent 4
        # Ordered no-envy: for all i < j: val(i, A[i]) >= val(i, A[j])
        violation = None
        for i in range(4):
            for j in range(i + 1, 4):
                if val(i, A[i]) < val(i, A[j]):
                    margin = val(i, A[j]) - val(i, A[i])
                    violation = {
                        "type": "ORDERED_ENVY",
                        "agent_i": i + 1,
                        "agent_j": j + 1,
                        "val_i_Ai": str(val(i, A[i])),
                        "val_i_Aj": str(val(i, A[j])),
                        "violation_margin": str(margin),
                        "explanation": f"Agent {i+1} envies later Agent {j+1}: v_{i+1}(A_{i+1})={val(i, A[i])} < v_{i+1}(A_{j+1})={val(i, A[j])}"
                    }
                    oe_count += 1
                    break
            if violation:
                break

        # EF1 condition: for all i > j: val(i, A[i]) >= min_{g in A_j} v_i(g)
        if not violation:
            for i in range(4):
                for j in range(i):
                    min_g = min_val(i, A[j])
                    if val(i, A[i]) < min_g:
                        margin = min_g - val(i, A[i])
                        violation = {
                            "type": "EF1_VIOLATION",
                            "agent_i": i + 1,
                            "agent_j": j + 1,
                            "val_i_Ai": str(val(i, A[i])),
                            "min_item_Aj": str(min_g),
                            "violation_margin": str(margin),
                            "explanation": f"Agent {i+1} violates EF1 toward earlier Agent {j+1}: v_{i+1}(A_{i+1})={val(i, A[i])} < min_g in A_{j+1} ={min_g}"
                        }
                        ef1_count += 1
                        break
                if violation:
                    break

        assert violation is not None, f"Allocation {idx} unexpectedly valid: {A}"
        obstruction_records.append({
            "allocation_index": idx,
            "allocation": [list(b) for b in A],
            "primary_violation": violation
        })

    print(f"\n--- Obstruction Certificate Summary ---")
    print(f"Total allocations evaluated: {len(obstruction_records)}")
    print(f"Total valid allocations: 0")
    print(f"Allocations failing ordered no-envy: {oe_count}")
    print(f"Allocations failing EF1: {ef1_count}")
    min_margin = min(Fraction(rec["primary_violation"]["violation_margin"]) for rec in obstruction_records)
    print(f"Minimum violation margin across all 864 allocations: {min_margin} = {float(min_margin)}")

    # 5. Export results
    result_dir = Path(__file__).resolve().parent.parent / "result"
    result_dir.mkdir(exist_ok=True, parents=True)

    val_matrix_file = result_dir / "valuation_matrix.json"
    with open(val_matrix_file, "w") as f:
        json.dump({
            "order": [1, 2, 3, 4],
            "num_agents": 4,
            "num_goods": 8,
            "groups": {"G1": [1, 2, 3], "G2": [4, 5, 6], "G3": [7, 8]},
            "scale": 100,
            "valuation_matrix_integer": V_int,
            "valuation_matrix_rational": [[str(x) for x in row] for row in V_rat]
        }, f, indent=2)
    print(f"Exported valuation matrix to {val_matrix_file}")

    cert_file = result_dir / "obstruction_certificate.json"
    with open(cert_file, "w") as f:
        json.dump({
            "target_id": "laminar-ef1-four-agent-key-matroids",
            "matroid": "size_8_key_matroid",
            "order": [1, 2, 3, 4],
            "total_allocations": len(obstruction_records),
            "valid_allocations": 0,
            "ordered_envy_failures": oe_count,
            "ef1_failures": ef1_count,
            "min_violation_margin": str(min_margin),
            "records": obstruction_records
        }, f, indent=2)
    print(f"Exported complete obstruction certificate to {cert_file}")
    print("=== Verification Finished Successfully (CHECK_PASSED) ===")

if __name__ == "__main__":
    main()
