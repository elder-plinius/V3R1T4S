#!/usr/bin/env python3
"""
reproduce_gsp_calibrations.py

Exact rational verification of standard GSP auction Price of Anarchy baselines:
1. 2-slot instance: v = (1, 1/2), alpha = (1, 1/2), b = (0, 1/2), ratio = 5/4 = 1.25.
2. 3-slot instance: Caragiannis et al. (JET 2015 / arXiv:1201.6429 Theorem 4.2 / App B.1)
   v = (1, 5296/10000, 14583/100000), alpha = (1, 55071/100000, 4704/10000),
   b = (0, 5296/10000, 14583/100000), ratio >= 1.259133.

All arithmetic is performed with Python's fractions.Fraction (exact rational).
"""

from fractions import Fraction
import json
import os
import sys

def check_gsp_pne(v, alpha, b):
    n = len(v)
    # Standard deterministic tie-breaking: higher bid wins, ties broken by smaller index i
    sorted_bidders = sorted(range(n), key=lambda i: (-b[i], i))
    slot_of = {bidder: slot for slot, bidder in enumerate(sorted_bidders)}
    
    # Payments in GSP: p_s = b_{\pi(s+1)} for s < n-1, p_{n-1} = 0
    p = [Fraction(0)] * n
    for slot in range(n - 1):
        p[slot] = b[sorted_bidders[slot + 1]]
    p[n - 1] = Fraction(0)
    
    # Equilibrium utilities
    u = [Fraction(0)] * n
    for slot, bidder in enumerate(sorted_bidders):
        u[bidder] = alpha[slot] * (v[bidder] - p[slot])
    
    # Check all possible unilateral deviations for every bidder
    deviations = []
    is_pne = True
    for i in range(n):
        s_i = slot_of[i]
        for target_slot in range(n):
            if target_slot == s_i:
                continue
            # Moving up (target_slot < s_i):
            if target_slot < s_i:
                threshold = b[sorted_bidders[target_slot]]
                # Can bidder i land in target_slot with b'_i in [0, v_i]?
                can_reach = (v[i] > threshold) or (v[i] == threshold and i < sorted_bidders[target_slot])
                if can_reach:
                    price = threshold
                    dev_u = alpha[target_slot] * (v[i] - price)
                    if dev_u > u[i]:
                        is_pne = False
                        deviations.append({
                            "bidder": i, "target_slot": target_slot, "type": "UP",
                            "current_u": str(u[i]), "dev_u": str(dev_u), "gain": str(dev_u - u[i])
                        })
            else:
                # Moving down (target_slot > s_i): always reachable by bidding below sorted_bidders[target_slot]
                price = b[sorted_bidders[target_slot + 1]] if target_slot < n - 1 else Fraction(0)
                dev_u = alpha[target_slot] * (v[i] - price)
                if dev_u > u[i]:
                    is_pne = False
                    deviations.append({
                        "bidder": i, "target_slot": target_slot, "type": "DOWN",
                        "current_u": str(u[i]), "dev_u": str(dev_u), "gain": str(dev_u - u[i])
                    })
                    
    sw = sum(alpha[slot] * v[sorted_bidders[slot]] for slot in range(n))
    opt = sum(alpha[slot] * sorted(v, reverse=True)[slot] for slot in range(n))
    ratio = opt / sw
    
    return {
        "n": n,
        "is_pne": is_pne,
        "sorted_bidders": sorted_bidders,
        "payments": [str(x) for x in p],
        "utilities": [str(x) for x in u],
        "deviations": deviations,
        "sw_exact": str(sw),
        "sw_float": float(sw),
        "opt_exact": str(opt),
        "opt_float": float(opt),
        "ratio_exact": str(ratio),
        "ratio_float": float(ratio)
    }

def main():
    # 2-slot calibration
    v2 = [Fraction(1), Fraction(1, 2)]
    a2 = [Fraction(1), Fraction(1, 2)]
    b2 = [Fraction(0), Fraction(1, 2)]
    res2 = check_gsp_pne(v2, a2, b2)
    assert res2["is_pne"] is True
    assert res2["ratio_exact"] == "5/4"
    print("2-Slot Calibration:")
    print(f"  PNE: {res2['is_pne']}, SW: {res2['sw_exact']}, OPT: {res2['opt_exact']}, Ratio: {res2['ratio_exact']} ({res2['ratio_float']:.4f})")

    # 3-slot calibration (JET 2015)
    v3 = [Fraction(1), Fraction(5296, 10000), Fraction(14583, 100000)]
    a3 = [Fraction(1), Fraction(55071, 100000), Fraction(4704, 10000)]
    b3 = [Fraction(0), Fraction(5296, 10000), Fraction(14583, 100000)]
    res3 = check_gsp_pne(v3, a3, b3)
    assert res3["is_pne"] is True
    assert res3["ratio_float"] >= 1.259133
    print("\n3-Slot Calibration:")
    print(f"  PNE: {res3['is_pne']}, SW: {res3['sw_float']:.7f}, OPT: {res3['opt_float']:.7f}, Ratio: {res3['ratio_exact']} ({res3['ratio_float']:.7f})")
    print(f"  Ratio >= 1.259133: {res3['ratio_float'] >= 1.259133}")

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "gsp_calibrations_output.json"), "w") as f:
        json.dump({"2_slot": res2, "3_slot": res3}, f, indent=2)
    print("\nCalibrations verified and saved to output/gsp_calibrations_output.json")

if __name__ == "__main__":
    main()
