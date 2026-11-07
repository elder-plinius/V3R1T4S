#!/usr/bin/env python3
"""
verify_solution.py — Self-contained standalone verifier for
bilateral-trade-best-offer-vs-second-best.

Validates:
1. Object SHA-256 integrity check.
2. BDK 2x2 calibration (1 under favourable ties, 3/4 under adversarial ties).
3. AlphaEvolve calibration (FB ~ 1.2322, SO ~ 0.3312, BO ~ 0.8565).
4. Exact rational verification of the certified 4x4 instance:
   - GFT_SO = 7133/1250 = 5.7064
   - GFT_BO = 1431/250 = 5.7240
   - max(SO, BO) = 1431/250 = 5.7240
   - GFT_M = 80301/10000 = 8.0301 (posted price p = 8)
   - Certified ratio: 19080/26767 approx 0.71281802 < 3/4 = 0.75000000
"""

from fractions import Fraction
import hashlib
import json
import math
import os
import sys

EXPECTED_OBJ_SHA = "0d1caf92a375e063c1e718a8431824747960f8f0d038726bde1c706e03e76ffb"

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

def run_alphaevolve_calibration():
    # AlphaEvolve Calibration (arXiv:2603.08679, H = 20000)
    import numpy as np
    H = 20000
    a1_base = 0.15
    a2 = 4.0
    w = 0.20
    a1_amp = 0.05
    a1_freq = 2.0

    cdf_s = np.zeros(H + 1)
    norm_factor = H + 1.0
    prev_cdf = 0.0

    for m in range(H + 1):
        base = max(0.0, min(1.0, (m + 1.0) / norm_factor))
        a1_eff = a1_base + a1_amp * math.sin(a1_freq * math.pi * base)
        a1_eff = max(1e-9, a1_eff)
        cdf1_val = base ** a1_eff
        cdf2_val = base ** a2
        current_cdf = w * cdf1_val + (1.0 - w) * cdf2_val
        current_cdf = max(0.0, min(current_cdf, 1.0))
        current_cdf = max(current_cdf, prev_cdf)
        cdf_s[m] = current_cdf
        prev_cdf = current_cdf

    sf_b = np.zeros(H + 1)
    sf_b[0] = 1.0
    for m in range(1, H + 1):
        sf_b[m] = 1.0 / m

    pmf_s = np.zeros(H + 1)
    pmf_s[0] = cdf_s[0]
    pmf_s[1:] = np.maximum(0.0, np.diff(cdf_s))

    pmf_b = np.zeros(H + 1)
    pmf_b[:-1] = np.maximum(0.0, sf_b[:-1] - sf_b[1:])
    pmf_b[H] = sf_b[H]

    # First Best
    suff_prob = np.zeros(H + 2)
    suff_val = np.zeros(H + 2)
    for b in range(H, -1, -1):
        suff_prob[b] = suff_prob[b+1] + pmf_b[b]
        suff_val[b] = suff_val[b+1] + pmf_b[b] * b

    fb = 0.0
    for s in range(H + 1):
        fb += pmf_s[s] * (suff_val[s] - s * suff_prob[s])

    so = 0.0
    for s in range(H + 1):
        if pmf_s[s] <= 0: continue
        p_opt = H
        so += pmf_s[s] * (suff_val[p_opt] - s * suff_prob[p_opt])

    pref_s_prob = np.cumsum(pmf_s)
    pref_s_val = np.cumsum(pmf_s * np.arange(H + 1))

    bo = 0.0
    for b in range(H + 1):
        if pmf_b[b] <= 0: continue
        p_arr = np.arange(b + 1)
        profs = cdf_s[:b+1] * (b - p_arr)
        max_idx = np.argmax(profs)
        bo += pmf_b[b] * (b * pref_s_prob[max_idx] - pref_s_val[max_idx])

    ro = 0.5 * (so + bo)
    print(f"Calibration 2 (AlphaEvolve H=20000): FB={fb:.4f} (target ~1.2322), SO={so:.4f} (target ~0.3312), BO={bo:.4f} (target ~0.8565) -> PASS")
    assert abs(fb - 1.2322) < 0.001, f"FB mismatch: {fb}"
    assert abs(so - 0.3312) < 0.001, f"SO mismatch: {so}"
    assert abs(bo - 0.8565) < 0.001, f"BO mismatch: {bo}"

def verify_instance(inst_path):
    with open(inst_path, "rb") as f:
        raw_b = f.read()

    actual_sha = hashlib.sha256(raw_b).hexdigest()
    assert actual_sha == EXPECTED_OBJ_SHA, f"Object SHA256 mismatch: got {actual_sha}, expected {EXPECTED_OBJ_SHA}"

    data = json.loads(raw_b.decode('utf-8'))

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
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    inst_path = os.path.join(pkg_dir, "object", "instance.json")
    if not os.path.exists(inst_path):
        inst_path = sys.argv[1] if len(sys.argv) > 1 else "instance.json"

    run_bdk_calibration()
    run_alphaevolve_calibration()
    verify_instance(inst_path)
