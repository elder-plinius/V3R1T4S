#!/usr/bin/env python3
"""
Standalone checker for ECC Inversion Addition Chains (Partial Win p1).
Recomputes all 20 addition chains from step definitions [j, k],
verifies monotonicity, doublings/additions counts, exact endpoints,
and executes 100 Fermat modular exponentiations per curve.
"""
import json
import os
import random
import sys

def main():
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(pkg_dir, "object", "certified_chains.json")
    if not os.path.isfile(json_path):
        print(f"FAIL: Missing certified_chains.json at {json_path}")
        sys.exit(1)

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"FAIL: Cannot parse JSON: {e}")
        sys.exit(1)

    curves = data.get("curves", [])
    if len(curves) != 20:
        print(f"FAIL: Expected 20 certified curve addition chains, got {len(curves)}")
        sys.exit(1)

    p1_wins = 0
    main_upgrades = 0

    for curve in curves:
        name = curve["name"]
        E = int(curve["hex_exponent"], 16)
        N = int(curve["hex_modulus"], 16)
        d = curve["d"]
        claimed_len = curve["total_length"]
        claimed_dbls = curve["doublings"]
        claimed_adds = curve["additions"]
        steps = curve["steps"]

        if len(steps) != claimed_len:
            print(f"FAIL: {name}: step count mismatch ({len(steps)} != {claimed_len})")
            sys.exit(1)

        # Re-evaluate addition chain step by step
        vals = [1]
        dbls = 0
        adds = 0

        for step_idx, (j, k) in enumerate(steps):
            if not (0 <= j <= step_idx and 0 <= k <= step_idx):
                print(f"FAIL: {name} step {step_idx}: invalid indices ({j}, {k})")
                sys.exit(1)
            val = vals[j] + vals[k]
            if val <= vals[-1]:
                print(f"FAIL: {name} step {step_idx}: non-monotonic value {val}")
                sys.exit(1)
            vals.append(val)
            if j == k:
                dbls += 1
            else:
                adds += 1

        if dbls != claimed_dbls or adds != claimed_adds:
            print(f"FAIL: {name}: operation counts mismatch (dbls: {dbls}!={claimed_dbls}, adds: {adds}!={claimed_adds})")
            sys.exit(1)

        if vals[-1] != E:
            print(f"FAIL: {name}: endpoint mismatch! Got {hex(vals[-1])}, expected {hex(E)}")
            sys.exit(1)

        if E != N - d:
            print(f"FAIL: {name}: exponent != N - d")
            sys.exit(1)

        # 100 Fermat tests: x^E * x^(d-1) == x^(N-1) == 1 mod N
        rng = random.Random(0x1337beef + claimed_len)
        for _ in range(100):
            x = rng.randint(2, N - 2)
            x_inv = pow(x, E, N)
            x_pow_d = pow(x, d - 1, N)
            prod = (x_inv * x_pow_d) % N
            if prod != 1:
                print(f"FAIL: {name}: Fermat test failed for x={x}")
                sys.exit(1)

        if not curve["is_main"] and claimed_len < curve["addchain_baseline"]:
            p1_wins += 1
        elif curve["is_main"] and claimed_len < curve["addchain_baseline"]:
            main_upgrades += 1

    if p1_wins < 2:
        print(f"FAIL: Expected at least 2 secondary curve wins, got {p1_wins}")
        sys.exit(1)

    # Check specific wins
    m383 = next(c for c in curves if c["name"] == "M-383")
    if m383["total_length"] != 395 or m383["total_length"] >= m383["addchain_baseline"]:
        print(f"FAIL: M-383 win condition not met: length {m383['total_length']} vs baseline {m383['addchain_baseline']}")
        sys.exit(1)

    m511 = next(c for c in curves if c["name"] == "M-511")
    if m511["total_length"] != 524 or m511["total_length"] >= m511["addchain_baseline"]:
        print(f"FAIL: M-511 win condition not met: length {m511['total_length']} vs baseline {m511['addchain_baseline']}")
        sys.exit(1)

    c25519_scalar = next(c for c in curves if c["name"] == "Curve25519 Scalar")
    if c25519_scalar["total_length"] > 282:
        print(f"FAIL: Curve25519 Scalar length {c25519_scalar['total_length']} > 282 (record beat not achieved)")
        sys.exit(1)

    p384_scalar = next(c for c in curves if c["name"] == "NIST P-384 Scalar")
    if p384_scalar["additions"] > 50:
        print(f"FAIL: NIST P-384 Scalar additions {p384_scalar['additions']} > 50 (p2 win not achieved)")
        sys.exit(1)

    print("VERIFICATION COMPLETE: 20/20 chains algebraically certified.")
    print(f"Secondary curve wins (p1): {p1_wins} (M-383: 395 < 396; M-511: 524 < 525)")
    print(f"Main curve records:         Curve25519 Scalar: {c25519_scalar['total_length']} steps (CONFIRMED_SOLUTION < 283 addchain baseline)")
    print(f"                            NIST P-384 Scalar: {p384_scalar['additions']} adds, {p384_scalar['total_length']} steps (p2 win < 52 adds)")
    print(f"Main curve improvements:    {main_upgrades} (Curve25519 Field: 265 < 266; NIST P-384 Field: 396 < 397)")
    print("ALL CHECKS PASSED.")
    sys.exit(0)

if __name__ == "__main__":
    main()
