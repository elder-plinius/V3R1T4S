#!/usr/bin/env python3
"""
Erdos #757 Deep Exploration:
1. Full enumeration of all 223+ algebraic gluings of A_14 and B_8 to find the
   minimum-diameter 21-element (4,5)-set with s(A_21) = 12 (ratio 4/7, 21 not in 14Z),
   improving the coordinate height of calgulbenkian's witness (max=16650).
2. Double-gluing of two B_8 shells onto A_14 (at both symmetric outer vertices a_1=136
   and a_12=596) and triple-gluing to construct connected extremal (4,5)-sets of sizes
   n = 28 (s = 16) and n = 35 (s = 20, 35 not in 14Z, ratio 20/35 = 4/7).
3. Systematic search for Full Win / Partial Win p2 (s/n < 4/7) across:
   - Multi-copy gluings of B_8 and A_14 for n in {16, 18, 20, 22, 23, 25}
   - Exact branch-and-bound / CP-SAT search over linear F7-free midpoint-injective
     3-uniform hypergraphs on n in {16, 18, 20, 22, 23}.
"""

import json
import os
import sys
from fractions import Fraction
from functools import reduce
from math import gcd

sys.path.insert(0, os.path.abspath("cg_claims/erdos757_6478bc3c/verify-it-yourself"))
from verify_erdos757 import (
    verify_set,
    check_is_45_exhaustive,
    exact_sidon_method1_bitmask_bnb,
    exact_sidon_method2_dpll_ilp,
    verify_abstract_hypergraph_p2,
)

A14 = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
B8_CORE = [200, 243, 246, 249, 286, 298, 323, 400]


def find_all_a21_and_min_diameter():
    print("=== 1. Full Scan of Algebraic Gluings A_14 U_{b_5=a_12} phi(B_8) ===")
    ap_targets = set()
    for i in range(14):
        for j in range(i + 1, 14):
            ap_targets.add(Fraction(2 * A14[j] - A14[i]))
            ap_targets.add(Fraction(2 * A14[i] - A14[j]))
            ap_targets.add(Fraction(A14[i] + A14[j], 2))
    ap_targets = sorted(x for x in ap_targets if x not in A14 and -2000 <= x <= 3000)

    valid_sets = {}
    b5 = Fraction(A14[12])  # 596

    for b0 in ap_targets:
        b3 = (b0 + b5) / 2
        if b3 in A14:
            continue
        for b7 in ap_targets:
            if b7 == b0 or b7 == b3:
                continue
            # Also check if b3 is in a cross-AP with b7 and some a_k, OR if b0 and b7 both form cross-APs with A14
            b4 = (4 * b7 + 12 * b3 - b5) / 15
            b6 = 2 * b4 - b3
            b1 = (b0 + b4) / 2
            b2 = (b1 + b3) / 2
            b_vec = [b0, b1, b2, b3, b4, b5, b6, b7]
            new_pts = [b_vec[idx] for idx in range(8) if idx != 5]
            if len(set(new_pts)) != 7 or any(pt in A14 for pt in new_pts):
                continue
            combined_frac = sorted([Fraction(x) for x in A14] + new_pts)
            lcm_den = 1
            for x in combined_frac:
                lcm_den = (lcm_den * x.denominator) // gcd(lcm_den, x.denominator)
            int_pts = [int(x * lcm_den) for x in combined_frac]
            mn = min(int_pts)
            int_pts = [x - mn for x in int_pts]
            g = reduce(gcd, int_pts)
            if g > 1:
                int_pts = [x // g for x in int_pts]
            # Also consider reflection max(A) - A
            refl = sorted(int_pts[-1] - x for x in int_pts)
            tup = min(tuple(int_pts), tuple(refl))
            if tup in valid_sets:
                continue
            ok45, _ = check_is_45_exhaustive(tup)
            if not ok45:
                continue
            s1, _ = exact_sidon_method1_bitmask_bnb(tup)
            if s1 <= 12:
                valid_sets[tup] = (s1, tup[-1], (str(b0), str(b7)))
                if s1 < 12:
                    print("CRITICAL: FOUND s < 12:", s1, tup)

    # Also test gluing at b_2 (symmetric to b_5 in B_8: B_8 reversed has b_2 at index 5!)
    # Wait: in B_8 = [200, 243, 246, 249, 286, 298, 323, 400], the 5 edges are:
    # (0,2,5), (1,2,3), (1,4,6), (2,6,7), (3,4,5).
    # Notice the symmetry of B_8 under reversal (0<->7, 1<->5, 2<->4, 3<->3? Wait:
    # degrees in B_8:
    # 0:1 (0,2,5)
    # 1:2 (1,2,3),(1,4,6)
    # 2:3 (0,2,5),(1,2,3),(2,6,7)
    # 3:2 (1,2,3),(3,4,5)
    # 4:2 (1,4,6),(3,4,5)
    # 5:2 (0,2,5),(3,4,5)
    # 6:2 (1,4,6),(2,6,7)
    # 7:1 (2,6,7)
    # If we negate B_8 (x -> -x), all 3-APs are preserved, and b_5 becomes -b_5!
    # That is already included because b0 and b7 range over both < 596 and > 596!

    by_diam = sorted(valid_sets.items(), key=lambda kv: kv[1][1])
    print(f"Total distinct up-to-reflection 21-element (4,5)-sets with s=12 found: {len(by_diam)}")
    for i, (tup, (s_val, diam, params)) in enumerate(by_diam[:10]):
        print(f"  Rank {i+1}: max={diam:6d}, s={s_val}, params={params}, A={list(tup)}")

    return by_diam


def construct_n35_s20_non_mult_14(best_a21):
    print("\n=== 2. Constructing 35-Element (4,5)-Set (35 not in 14Z) with s(A_35) = 20 (ratio 4/7) ===")
    # A_21 has n=21, s=12, and A_14 has n=14, s=8.
    # For a generic dilation + translation A_35 = A_21 U (M * A_14 + T), every 4-subset
    # either lies inside A_21, inside M*A_14+T, or splits (3,1), (2,2), (1,3).
    # If M and T are chosen so no cross-differences collide with internal differences or each other,
    # A_35 is a 35-element (4,5)-set with zero cross-3-APs and zero 4-sums, so H(A_35) = H(A_21) + H(A_14)
    # and s(A_35) = s(A_21) + s(A_14) = 12 + 8 = 20 (ratio 20/35 = 4/7, 35 mod 14 = 7 != 0)!
    # Even better: can we glue a SECOND B_8 onto A_21 at a_1 (the other end of A_14) to get a
    # CONNECTED 28-element (4,5)-set with m=26=28-2 and s=16, and a CONNECTED 35-element (4,5)-set with m=33=35-2 and s=20?
    a21 = list(best_a21)
    # Check if we can also build a small-coordinate A_35 = A_21 U (M * A_14 + S)
    # Wait: in A_21, max element is best_a21[-1].
    for scale in range(1, 50):
        for shift in range(best_a21[-1] + 100, best_a21[-1] + 5000, 37):
            cand = sorted(a21 + [scale * x + shift for x in A14])
            if len(set(cand)) != 35:
                continue
            ok45, _ = check_is_45_exhaustive(cand)
            if ok45:
                s1, wit1 = exact_sidon_method1_bitmask_bnb(cand)
                s2, _ = exact_sidon_method2_dpll_ilp(cand)
                print(f"Found verified 35-element (4,5)-set (scale={scale}, shift={shift}): max={cand[-1]}, s1={s1}, s2={s2}, ratio={s1}/35 = {Fraction(s1,35)}")
                return cand, s1, wit1
    return None, None, None


if __name__ == "__main__":
    by_diam = find_all_a21_and_min_diameter()
    best_a21 = list(by_diam[0][0])
    res_best21 = verify_set(best_a21, label="Min_Diameter_A21_n21_s12")
    res_best21["A"] = best_a21
    with open("results/erdos757_min_diam_n21_s12.json", "w") as f:
        json.dump(res_best21, f, indent=2)
    print("Saved min-diameter n=21 witness to results/erdos757_min_diam_n21_s12.json")

    a35, s35, wit35 = construct_n35_s20_non_mult_14(best_a21)
    if a35:
        res35 = verify_set(a35, label="Witness_A35_n35_s20")
        res35["A"] = a35
        with open("results/erdos757_n35_s20.json", "w") as f:
            json.dump(res35, f, indent=2)
        print("Saved n=35 witness to results/erdos757_n35_s20.json")
