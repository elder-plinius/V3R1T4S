#!/usr/bin/env python3
"""
verify_solution.py — Self-contained exact rational verification checker
for bilateral-trade-best-offer-vs-second-best.
Strictly under 200 lines, uses fractions.Fraction exclusively for exact arithmetic.
"""

from fractions import Fraction
import json
import os
import sys

def run_bdk_calibration():
    # 2x2 Calibration from BDK 2021 (arXiv:2111.07790 Section 3)
    S = [Fraction(0), Fraction(1)]
    p_S = [Fraction(1, 2), Fraction(1, 2)]
    B = [Fraction(1), Fraction(2)]
    p_B = [Fraction(1, 2), Fraction(1, 2)]

    def calc(favourable):
        so = Fraction(0)
        for s, ps in zip(S, p_S):
            cands = []
            max_prof = Fraction(-1)
            for p in B:
                if p < s: continue
                acc = sum(pb for b, pb in zip(B, p_B) if b >= p)
                prof = (p - s) * acc
                gft = sum(pb * (b - s) for b, pb in zip(B, p_B) if b >= p)
                if prof > max_prof:
                    max_prof = prof
                    cands = [gft]
                elif prof == max_prof:
                    cands.append(gft)
            so += ps * (max(cands) if favourable else min(cands))
        bo = Fraction(0)
        for b, pb in zip(B, p_B):
            cands = []
            max_prof = Fraction(-1)
            for p in S:
                if p > b: continue
                acc = sum(ps for s, ps in zip(S, p_S) if s <= p)
                prof = (b - p) * acc
                gft = sum(ps * (b - s) for s, ps in zip(S, p_S) if s <= p)
                if prof > max_prof:
                    max_prof = prof
                    cands = [gft]
                elif prof == max_prof:
                    cands.append(gft)
            bo += pb * (max(cands) if favourable else min(cands))
        return so, bo

    so_fav, bo_fav = calc(favourable=True)
    so_adv, bo_adv = calc(favourable=False)
    pp_1 = sum(ps * pb * (b - s) for s, ps in zip(S, p_S) if s <= 1 for b, pb in zip(B, p_B) if b >= 1)

    r_fav = max(so_fav, bo_fav) / pp_1
    r_adv = max(so_adv, bo_adv) / pp_1
    assert r_fav == Fraction(1, 1), f"BDK favourable mismatch: {r_fav}"
    assert r_adv == Fraction(3, 4), f"BDK adversarial mismatch: {r_adv}"
    print(f"Calibration 1 (BDK 2x2): Favourable ratio = {r_fav}, Adversarial ratio = {r_adv} -> PASS")


def verify_instance(inst_path):
    if not os.path.exists(inst_path) and not os.path.isabs(inst_path):
        cand = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "result", "instance.json")
        if os.path.exists(cand):
            inst_path = cand
        else:
            cand2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), inst_path)
            if os.path.exists(cand2):
                inst_path = cand2
    with open(inst_path, "r") as f:
        data = json.load(f)

    S = [Fraction(x) for x in data["seller_support"]]
    p_S = [Fraction(p) for p in data["seller_probabilities"]]
    B = [Fraction(x) for x in data["buyer_support"]]
    p_B = [Fraction(p) for p in data["buyer_probabilities"]]
    p_posted = Fraction(data["posted_price"])

    # 1. Validate distributions
    assert len(S) == len(p_S) and len(B) == len(p_B)
    assert all(p > 0 for p in p_S) and sum(p_S) == Fraction(1, 1), "Invalid seller distribution"
    assert all(p > 0 for p in p_B) and sum(p_B) == Fraction(1, 1), "Invalid buyer distribution"
    assert S == sorted(S) and B == sorted(B), "Supports must be sorted"

    # 2. Seller Offering (GFT-favourable tie-breaking)
    gft_so = Fraction(0)
    for s, ps in zip(S, p_S):
        max_prof = Fraction(-1)
        best_gfts = []
        best_offers = []
        for p in B:
            if p < s: continue
            prob_acc = sum(pb for b, pb in zip(B, p_B) if b >= p)
            prof = (p - s) * prob_acc
            gft = sum(pb * (b - s) for b, pb in zip(B, p_B) if b >= p)
            if prof > max_prof:
                max_prof = prof
                best_gfts = [gft]
                best_offers = [p]
            elif prof == max_prof:
                best_gfts.append(gft)
                best_offers.append(p)
        chosen_gft = max(best_gfts)
        gft_so += ps * chosen_gft
        is_unique = (len(best_offers) == 1)
        print(f"  Seller s={str(s):>2}: optimal offer(s)={best_offers}, profit={float(max_prof):.4f}, unique={is_unique}")

    # 3. Buyer Offering (GFT-favourable tie-breaking)
    gft_bo = Fraction(0)
    for b, pb in zip(B, p_B):
        max_prof = Fraction(-1)
        best_gfts = []
        best_offers = []
        for p in S:
            if p > b: continue
            prob_acc = sum(ps for s, ps in zip(S, p_S) if s <= p)
            prof = (b - p) * prob_acc
            gft = sum(ps * (b - s) for s, ps in zip(S, p_S) if s <= p)
            if prof > max_prof:
                max_prof = prof
                best_gfts = [gft]
                best_offers = [p]
            elif prof == max_prof:
                best_gfts.append(gft)
                best_offers.append(p)
        chosen_gft = max(best_gfts)
        gft_bo += pb * chosen_gft
        is_unique = (len(best_offers) == 1)
        print(f"  Buyer  b={str(b):>2}: optimal offer(s)={best_offers}, profit={float(max_prof):.4f}, unique={is_unique}")

    # 4. Mechanism M: Posted Price p_posted
    # By construction, posted price p is dominant-strategy incentive compatible,
    # individually rational, and ex-ante budget balanced (with equality E[payment]=E[receipt]).
    gft_m = sum(ps * pb * (b - s) for s, ps in zip(S, p_S) if s <= p_posted for b, pb in zip(B, p_B) if b >= p_posted)
    assert gft_m > 0, "GFT_M must be strictly positive"

    best_offer = max(gft_so, gft_bo)
    ratio = best_offer / gft_m
    bar = Fraction(3, 4)

    print("\n=== EXACT RATIONAL VERIFICATION SUMMARY ===")
    print(f"Seller distribution: S = {S}, p_S = {p_S}")
    print(f"Buyer distribution:  B = {B}, p_B = {p_B}")
    print(f"Mechanism M: Posted Price p = {p_posted}")
    print(f"GFT_SO (exact): {gft_so} = {float(gft_so):.8f}")
    print(f"GFT_BO (exact): {gft_bo} = {float(gft_bo):.8f}")
    print(f"max(GFT_SO, GFT_BO): {best_offer} = {float(best_offer):.8f}")
    print(f"GFT_M (exact):  {gft_m} = {float(gft_m):.8f}")
    print(f"Certified Ratio max(SO, BO) / GFT_M: {ratio} = {float(ratio):.8f}")
    print(f"Target Bar: 3/4 = {bar} = {float(bar):.8f}")
    print(f"Strict Margin below 3/4: {bar - ratio} = {float(bar - ratio):.8f}")

    assert ratio < bar, f"FAILED: ratio {ratio} not strictly less than 3/4!"
    print("\nSUCCESS: max(GFT_SO, GFT_BO) < (3/4) * GFT_M CONFIRMED UNDER FAVOURABLE TIES!")
    return True

if __name__ == "__main__":
    run_bdk_calibration()
    inst = sys.argv[1] if len(sys.argv) > 1 else "instance.json"
    verify_instance(inst)
