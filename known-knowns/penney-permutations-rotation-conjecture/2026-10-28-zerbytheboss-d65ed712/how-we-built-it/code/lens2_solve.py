#!/usr/bin/env python3
# Lens 2: Pure Python Brute Force Enumeration & Independent Exact Integer DP Engine
# Cross-validation against Lens 1 and Elizalde-Lin (arXiv:2404.06585)

import itertools
import math
import sys
import time
from collections import defaultdict

# Ensure immediate unbuffered output
sys.stdout.reconfigure(line_buffering=True)

def to_pattern(seq):
    """Standardize sequence to relative order permutation (1-indexed)."""
    order = sorted(range(len(seq)), key=lambda i: seq[i])
    rank = [0] * len(seq)
    for r, idx in enumerate(order):
        rank[idx] = r + 1
    return tuple(rank)

def right_rotation(sigma):
    return (sigma[-1],) + sigma[:-1]

def complement(sigma):
    k = len(sigma)
    return tuple(k + 1 - x for x in sigma)

def brute_force_counts(sigma, tau, H):
    """Exhaustive enumeration over all H! permutations."""
    k = len(sigma)
    A = 0
    B = 0
    R = 0
    for p in itertools.permutations(range(H)):
        for i in range(H - k + 1):
            pat = to_pattern(p[i:i+k])
            if pat == sigma:
                A += 1
                break
            elif pat == tau:
                B += 1
                break
        else:
            R += 1
    factH = math.factorial(H)
    assert A + B + R == factH
    return A, B, R, factH

def dp_solve_pair(sigma, tau, max_h=36):
    """Independent dynamic programming over boundary relative-order profiles."""
    k = len(sigma)
    counts = { (1,): 1 }
    for m in range(2, k):
        new_counts = defaultdict(int)
        for state, cnt in counts.items():
            for v in range(1, m + 1):
                new_state = tuple((x if x < v else x + 1) for x in state) + (v,)
                new_counts[new_state] += cnt
        counts = new_counts

    av_sigma = {}
    av_tau = {}
    av_R = {}

    history = []
    cert_h = None

    for m in range(k, max_h + 1):
        new_counts = defaultdict(int)
        A_m = 0
        B_m = 0
        for state, cnt in counts.items():
            for v in range(1, m + 1):
                shifted = tuple((x if x < v else x + 1) for x in state)
                window = shifted + (v,)
                pat = to_pattern(window)
                if pat == sigma:
                    A_m += cnt
                elif pat == tau:
                    B_m += cnt
                else:
                    new_state = shifted[1:] + (v,)
                    new_counts[new_state] += cnt
        counts = new_counts
        av_sigma[m] = A_m
        av_tau[m] = B_m
        R_m = sum(counts.values())
        av_R[m] = R_m

        # Compute cumulative (A, B, R) at current horizon m
        fact_m = math.factorial(m)
        A_m_cum = sum(av_sigma[j] * (fact_m // math.factorial(j)) for j in range(k, m + 1))
        B_m_cum = sum(av_tau[j] * (fact_m // math.factorial(j)) for j in range(k, m + 1))
        assert A_m_cum + B_m_cum + R_m == fact_m
        history.append((m, A_m_cum, B_m_cum, R_m, fact_m))

        if 2 * (A_m_cum + R_m) < fact_m:
            cert_h = m
            break

    return cert_h, history

def run_brute_force_cross_check():
    print("=== 1. Cross-Check: Exhaustive Permutation Enumeration vs DP (H <= 9) ===")
    test_pairs = [
        ((1, 3, 2), (2, 3, 1), 7),
        ((1, 2, 3), (3, 1, 2), 7),
        ((2, 3, 4, 1), (1, 2, 3, 4), 8),
        ((1, 4, 3, 2), (2, 1, 4, 3), 8),
    ]

    for sigma, tau, max_bf_h in test_pairs:
        print(f"\nTesting sigma={sigma} vs tau={tau} up to H={max_bf_h}:")
        _, dp_hist = dp_solve_pair(sigma, tau, max_bf_h)
        dp_dict = {h: (a, b, r, f) for h, a, b, r, f in dp_hist}

        for H in range(len(sigma), max_bf_h + 1):
            t_bf = time.time()
            bf_a, bf_b, bf_r, bf_f = brute_force_counts(sigma, tau, H)
            dt_bf = time.time() - t_bf

            dp_a, dp_b, dp_r, dp_f = dp_dict[H]

            print(f"  H={H:2} (BF {dt_bf:.3f}s): A={bf_a}, B={bf_b}, R={bf_r}, H!={bf_f}")
            assert (bf_a, bf_b, bf_r, bf_f) == (dp_a, dp_b, dp_r, dp_f), \
                f"MISMATCH at H={H}: BF={(bf_a, bf_b, bf_r)} vs DP={(dp_a, dp_b, dp_r)}"

        print(f"  [PASS] 100% exact match between Brute Force S_H enumeration and DP across all H <= {max_bf_h}!")

def run_2341_deep_verification():
    print("\n=== 2. Deep Verification of sigma = (2, 3, 4, 1) -> tau = (1, 2, 3, 4) ===")
    sigma = (2, 3, 4, 1)
    tau = (1, 2, 3, 4)
    t0 = time.time()
    cert_h, history = dp_solve_pair(sigma, tau, 36)
    dt = time.time() - t0
    h36 = [item for item in history if item[0] == 36][0]
    h, a, b, r, fact_h = h36

    print(f"  Solved to H=36 in {dt:.2f}s:")
    print(f"    A(36) = {a}")
    print(f"    B(36) = {b}")
    print(f"    R(36) = {r}")
    print(f"    36!   = {fact_h}")
    print(f"    A/36! = {a / fact_h:.8f}")
    print(f"    B/36! = {b / fact_h:.8f} (> 0.5)")
    print(f"    (A+R)/36! = {(a + r) / fact_h:.8f} (< 0.5)")
    assert 2 * (a + r) < fact_h
    assert 2 * b > fact_h
    assert cert_h == 36
    print("  [PASS] Independent Python verification of 2341 certificate passed!\n")

def run_s4_verification():
    print("=== 3. Independent Verification of S_4 Certificates (p1) ===")
    all_s4 = list(itertools.permutations(range(1, 5)))
    print(f"Total permutations in S_4: {len(all_s4)}")
    max_h_needed = 0

    print(f"  {'sigma':<14} -> {'tau':<14} | {'H':<4} | {'(A+R)/H!':<10} | {'B/H!':<10} | Status")
    print(f"  {'-'*65}")

    t_start = time.time()
    # Check all symmetry classes (or all 24 with early exit)
    for sigma in all_s4:
        tau = right_rotation(sigma)
        cert_h, history = dp_solve_pair(sigma, tau, 36)
        assert cert_h is not None, f"Failed to certify {sigma} by H=36!"
        max_h_needed = max(max_h_needed, cert_h)
        entry = [item for item in history if item[0] == cert_h][0]
        h, a, b, r, fact_h = entry
        ar_ratio = (a + r) / fact_h
        b_ratio = b / fact_h
        print(f"  {str(sigma):<14} -> {str(tau):<14} | H={h:<2} | {ar_ratio:.5f}    | {b_ratio:.5f}    | CERTIFIED (< 1/2)")

    print(f"  {'-'*65}")
    print(f"  All 24/24 permutations in S_4 certified in {time.time() - t_start:.2f}s! Max H needed: {max_h_needed}")
    print("  [CONFIRMED PARTIAL p1] Rigorous integer certificates established for all of S_4.\n")

def main():
    t0 = time.time()
    print("==========================================================================")
    print("V3R1T4S Lens 2: Pure Python Brute Force & Independent Exact DP Engine")
    print("Target: penney-permutations-rotation-conjecture")
    print("==========================================================================\n")

    run_brute_force_cross_check()
    run_2341_deep_verification()
    run_s4_verification()

    print("==========================================================================")
    print(f"Lens 2 execution complete in {time.time() - t0:.2f}s")
    print("==========================================================================")

if __name__ == "__main__":
    main()
