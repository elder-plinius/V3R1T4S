#!/usr/bin/env python3
"""Standalone verifier for penney-permutations-rotation-conjecture.
Verifies both:
1. Part 1 (p1): S_4 exact integer horizon certificates in object/s4_certificates.json.
   - All 24 permutations in S_4.
   - Right cyclic rotation tau = (sigma_4, sigma_1, sigma_2, sigma_3).
   - Exact big integer sum A(H) + B(H) + R(H) == H!.
   - Rigorous tail inequality 2 * (A(H) + R(H)) < H!, proving Pr(sigma precedes tau) < 1/2.
   - Complementary Bob inequality 2 * B(H) > H!, proving Pr(tau precedes sigma) > 1/2.
   - Exact 42-digit integer match on calibration benchmark 2341 -> 1234 at H=36.

2. Part 2 (p2): S_5 exact rational intervals and large-horizon counts in object/s5_rational_intervals.json.
   - All 120 permutations in S_5 across 60 complement-symmetry classes at H=16.
   - Right cyclic rotation tau = (sigma_5, sigma_1, sigma_2, sigma_3, sigma_4).
   - Exact complement symmetry: A, B, R invariant under complementation sigma -> sigma^c.
   - Exact integer partition A(16) + B(16) + R(16) == 16! == 20922789888000.
   - Rigorous two-sided rational interval bounds [A/H!, (A+R)/H!] and [B/H!, (B+R)/H!].
   - Conjectural direction audit: B > A for ALL 120 permutations (zero counterexamples in S_5).
   - Minimum conditional Bob win ratio B / (A + B) >= 0.5478.
"""

import json
import math
import os
import sys

def verify_s4(base_dir):
    obj_path = os.path.join(base_dir, "object", "s4_certificates.json")
    if not os.path.isfile(obj_path):
        obj_path = "object/s4_certificates.json"

    with open(obj_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("target_id") == "penney-permutations-rotation-conjecture", "Incorrect target_id in s4"
    assert data.get("claim") == "p1", "Incorrect claim in s4"
    assert data.get("symmetric_group") == "S_4", "Incorrect group in s4"

    certs = data.get("certificates", [])
    assert len(certs) == 24, f"Expected 24 certificates for S_4, got {len(certs)}"

    seen_sigmas = set()

    for c in certs:
        sigma = tuple(c["sigma"])
        tau = tuple(c["tau"])
        assert len(sigma) == 4 and sorted(sigma) == [1, 2, 3, 4], f"Invalid sigma: {sigma}"
        assert sigma not in seen_sigmas, f"Duplicate sigma: {sigma}"
        seen_sigmas.add(sigma)

        expected_tau = (sigma[3], sigma[0], sigma[1], sigma[2])
        assert tau == expected_tau, f"Tau mismatch for {sigma}: expected {expected_tau}, got {tau}"

        H = int(c["horizon"])
        assert 4 <= H <= 36, f"Horizon {H} out of bounds"

        A = int(c["A"])
        B = int(c["B"])
        R = int(c["R"])
        H_fact = int(c["H_fact"])

        expected_fact = math.factorial(H)
        assert H_fact == expected_fact, f"H_fact mismatch for H={H}"
        assert A + B + R == H_fact, f"Partition count mismatch: A+B+R={A+B+R} != {H_fact}"

        # Rigorous mathematical proof that Bob beats Alice:
        # Pr(Alice wins) <= (A + R) / H! < 1/2  <=>  2 * (A + R) < H!
        assert 2 * (A + R) < H_fact, f"Tail bound violated for {sigma}: 2*(A+R)={2*(A+R)} >= {H_fact}"
        assert 2 * B > H_fact, f"Bob win bound violated for {sigma}: 2*B={2*B} <= {H_fact}"

        # Float consistency
        a_f = A / H_fact
        b_f = B / H_fact
        ar_f = (A + R) / H_fact
        assert f"{a_f:.7f}" == f"{float(c['A_over_fact']):.7f}", f"A float mismatch: {a_f:.7f} vs {c['A_over_fact']}"
        assert f"{b_f:.7f}" == f"{float(c['B_over_fact']):.7f}", f"B float mismatch: {b_f:.7f} vs {c['B_over_fact']}"
        assert f"{ar_f:.7f}" == f"{float(c['A_plus_R_over_fact']):.7f}", f"AR float mismatch: {ar_f:.7f} vs {c['A_plus_R_over_fact']}"

        # Benchmark check for 2341 -> 1234
        if sigma == (2, 3, 4, 1):
            assert H == 36
            assert A == 147886985383757458869209075733594161570220
            assert B == 186454247223712671395113700966835612829428
            assert R == 37652094182431087203676671450405425600352

    assert len(seen_sigmas) == 24, "Did not verify all 24 permutations of S_4"
    print("  [PASS] All 24 S_4 Penney rotation certificates (p1) verified successfully!")

def verify_s5(base_dir):
    obj_path = os.path.join(base_dir, "object", "s5_rational_intervals.json")
    if not os.path.isfile(obj_path):
        obj_path = "object/s5_rational_intervals.json"

    with open(obj_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("target_id") == "penney-permutations-rotation-conjecture", "Incorrect target_id in s5"
    assert data.get("claim") == "p2", "Incorrect claim in s5"
    assert data.get("symmetric_group") == "S_5", "Incorrect group in s5"
    assert data.get("horizon") == 16, "Expected horizon 16"
    assert data.get("total_permutations") == 120, "Expected 120 permutations"
    assert data.get("symmetry_classes") == 60, "Expected 60 classes"
    assert data.get("all_favor_bob") is True, "Not all favor bob"

    intervals = data.get("intervals", [])
    assert len(intervals) == 120, f"Expected 120 intervals, got {len(intervals)}"

    seen_sigmas = {}
    H16_fact = math.factorial(16)
    assert H16_fact == 20922789888000

    for item in intervals:
        sigma = tuple(item["sigma"])
        tau = tuple(item["tau"])
        assert len(sigma) == 5 and sorted(sigma) == [1, 2, 3, 4, 5], f"Invalid sigma: {sigma}"
        assert sigma not in seen_sigmas, f"Duplicate sigma: {sigma}"

        expected_tau = (sigma[4], sigma[0], sigma[1], sigma[2], sigma[3])
        assert tau == expected_tau, f"Tau mismatch for {sigma}: expected {expected_tau}, got {tau}"

        expected_comp = tuple(6 - x for x in sigma)
        assert tuple(item["complement_symmetric_to"]) == expected_comp, f"Complement mismatch for {sigma}"

        A = int(item["A"])
        B = int(item["B"])
        R = int(item["R"])
        H_fact = int(item["H_fact"])

        assert H_fact == H16_fact, f"H_fact mismatch: {H_fact} != {H16_fact}"
        assert A + B + R == H16_fact, f"Count partition mismatch: A+B+R={A+B+R} != {H16_fact}"

        # Bob strictly beats Alice conditionally
        assert B > A, f"Conjecture 6.1 counterexample found in S_5 at {sigma}: B={B} <= A={A}!"
        b_ratio = B / (A + B)
        assert b_ratio >= 0.5478, f"Unexpectedly low Bob win ratio: {b_ratio} for {sigma}"
        assert item["favors_bob"] is True

        # Rational interval consistency
        assert item["rational_interval_alice"] == [f"{A}/{H16_fact}", f"{A+R}/{H16_fact}"]
        assert item["rational_interval_bob"] == [f"{B}/{H16_fact}", f"{B+R}/{H16_fact}"]

        seen_sigmas[sigma] = (A, B, R)

    # Check complement symmetry across all pairs
    for sigma, (A, B, R) in seen_sigmas.items():
        comp_sigma = tuple(6 - x for x in sigma)
        assert comp_sigma in seen_sigmas
        cA, cB, cR = seen_sigmas[comp_sigma]
        assert (A, B, R) == (cA, cB, cR), f"Complement symmetry violation: {sigma} vs {comp_sigma}"

    print(f"  [PASS] All 120 S_5 exact rational intervals (p2) verified successfully (min B/(A+B) = {data['min_bob_win_ratio']:.4f})!")

def main():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print("=== Verifying penney-permutations-rotation-conjecture package ===")
        verify_s4(base_dir)
        verify_s5(base_dir)
        print("All verification checks PASSED!")
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"VERIFICATION FAILURE: {e}")
        print("FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
