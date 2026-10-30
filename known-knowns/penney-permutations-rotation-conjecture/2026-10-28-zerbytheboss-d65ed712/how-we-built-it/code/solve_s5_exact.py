#!/usr/bin/env python3
"""Exact consecutive-pattern dynamic programming engine for S_5 Penney's game.
Computes exact integer counts A(H), B(H), R(H) and two-sided rational intervals
for all 120 permutations of S_5 up to horizon H=16 across 60 complement-symmetry classes.
"""

import itertools
import json
import math
import os
import sys
import time
from collections import defaultdict
from multiprocessing import Pool, cpu_count

def to_pattern(seq):
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

def solve_one_class(args):
    s, max_h = args
    tau = right_rotation(s)
    k = len(s)
    counts = { (1,): 1 }
    for m in range(2, k):
        new_counts = defaultdict(int)
        for state, cnt in counts.items():
            for v in range(1, m + 1):
                new_state = tuple((x if x < v else x + 1) for x in state) + (v,)
                new_counts[new_state] += cnt
        counts = new_counts

    av_s = {}
    av_t = {}
    for m in range(k, max_h + 1):
        new_counts = defaultdict(int)
        A_m = 0
        B_m = 0
        for state, cnt in counts.items():
            for v in range(1, m + 1):
                shifted = tuple((x if x < v else x + 1) for x in state)
                window = shifted + (v,)
                pat = to_pattern(window)
                if pat == s: A_m += cnt
                elif pat == tau: B_m += cnt
                else:
                    new_state = shifted[1:] + (v,)
                    new_counts[new_state] += cnt
        counts = new_counts
        av_s[m] = A_m
        av_t[m] = B_m

    fact_H = math.factorial(max_h)
    A = sum(av_s[j] * (fact_H // math.factorial(j)) for j in range(k, max_h + 1))
    B = sum(av_t[j] * (fact_H // math.factorial(j)) for j in range(k, max_h + 1))
    R = sum(counts.values())
    assert A + B + R == fact_H
    return s, tau, max_h, A, B, R, fact_H

def main():
    max_h = 16
    all_s5 = list(itertools.permutations(range(1, 6)))
    classes = []
    seen = set()
    for s in all_s5:
        if s not in seen:
            sc = complement(s)
            seen.add(s)
            seen.add(sc)
            classes.append((s, max_h))

    print(f"Solving {len(classes)} symmetry classes to H={max_h} using {cpu_count()} cores...")
    t0 = time.time()
    with Pool() as pool:
        class_results = pool.map(solve_one_class, classes)
    dt = time.time() - t0
    print(f"Computed all {len(class_results)} classes in {dt:.2f}s!")

    class_dict = {}
    for s, tau, h, A, B, R, fact_H in class_results:
        class_dict[s] = (A, B, R, fact_H)
        sc = complement(s)
        class_dict[sc] = (A, B, R, fact_H)

    intervals = []
    min_b_ratio = 1.0
    max_b_ratio = 0.0
    min_sigma = None
    all_favor_bob = True

    for s in all_s5:
        tau = right_rotation(s)
        A, B, R, fact_H = class_dict[s]
        assert A + B + R == fact_H
        b_ratio = B / (A + B)
        if b_ratio < min_b_ratio:
            min_b_ratio = b_ratio
            min_sigma = s
        if b_ratio > max_b_ratio:
            max_b_ratio = b_ratio
        if B <= A:
            all_favor_bob = False

        intervals.append({
            "sigma": list(s),
            "tau": list(tau),
            "complement_symmetric_to": list(complement(s)),
            "horizon": max_h,
            "A": str(A),
            "B": str(B),
            "R": str(R),
            "H_fact": str(fact_H),
            "A_over_fact": round(A / fact_H, 8),
            "B_over_fact": round(B / fact_H, 8),
            "R_over_fact": round(R / fact_H, 8),
            "A_plus_R_over_fact": round((A + R) / fact_H, 8),
            "rational_interval_alice": [f"{A}/{fact_H}", f"{A + R}/{fact_H}"],
            "rational_interval_bob": [f"{B}/{fact_H}", f"{B + R}/{fact_H}"],
            "bob_win_ratio_conditional": round(b_ratio, 6),
            "favors_bob": bool(B > A)
        })

    out_data = {
        "target_id": "penney-permutations-rotation-conjecture",
        "claim": "p2",
        "symmetric_group": "S_5",
        "horizon": max_h,
        "total_permutations": len(intervals),
        "symmetry_classes": len(classes),
        "min_bob_win_ratio": round(min_b_ratio, 6),
        "max_bob_win_ratio": round(max_b_ratio, 6),
        "min_bob_sigma": list(min_sigma),
        "all_favor_bob": all_favor_bob,
        "intervals": intervals
    }

    out_path = os.path.join(os.path.dirname(__file__), "..", "..", "object", "s5_rational_intervals.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=2)

    print(f"Wrote {len(intervals)} S_5 intervals to {out_path}!")

if __name__ == "__main__":
    main()
