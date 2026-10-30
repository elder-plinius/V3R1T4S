#!/usr/bin/env python3
"""
calibrate.py — Exact calibration reproducing:
1. BDK (arXiv:2111.07790) 2x2 instance:
   - ratio 1 under GFT-favourable tie-breaking
   - ratio 3/4 under BDK adversarial tie-breaking
2. AlphaEvolve (arXiv:2603.08679) instance:
   - FB ~ 1.2322, SO ~ 0.3312, BO ~ 0.8565 under paper's own tie rule.
"""

from fractions import Fraction
import math
import numpy as np

def calibrate_bdk_2x2():
    print("=== 1. BDK (arXiv:2111.07790) 2x2 Calibration ===")
    S = [Fraction(0), Fraction(1)]
    p_S = [Fraction(1, 2), Fraction(1, 2)]
    B = [Fraction(1), Fraction(2)]
    p_B = [Fraction(1, 2), Fraction(1, 2)]

    def eval_offers(favourable=True):
        gft_so = Fraction(0)
        for s, ps in zip(S, p_S):
            best_prof = Fraction(-1)
            best_cands = []
            for p in B:
                if p < s: continue
                prob_acc = sum(pb for b, pb in zip(B, p_B) if b >= p)
                prof = (p - s) * prob_acc
                gft = sum(pb * (b - s) for b, pb in zip(B, p_B) if b >= p)
                if prof > best_prof:
                    best_prof = prof
                    best_cands = [gft]
                elif prof == best_prof:
                    best_cands.append(gft)
            chosen = max(best_cands) if favourable else min(best_cands)
            gft_so += ps * chosen

        gft_bo = Fraction(0)
        for b, pb in zip(B, p_B):
            best_prof = Fraction(-1)
            best_cands = []
            for p in S:
                if p > b: continue
                prob_acc = sum(ps for s, ps in zip(S, p_S) if s <= p)
                prof = (b - p) * prob_acc
                gft = sum(ps * (b - s) for s, ps in zip(S, p_S) if s <= p)
                if prof > best_prof:
                    best_prof = prof
                    best_cands = [gft]
                elif prof == best_prof:
                    best_cands.append(gft)
            chosen = max(best_cands) if favourable else min(best_cands)
            gft_bo += pb * chosen

        return gft_so, gft_bo

    so_fav, bo_fav = eval_offers(favourable=True)
    so_adv, bo_adv = eval_offers(favourable=False)

    # Posted price p = 1: trades on (0, 1), (0, 2), (1, 1), (1, 2)
    p_mid = Fraction(1)
    gft_m = sum(ps * pb * (b - s) for s, ps in zip(S, p_S) if s <= p_mid for b, pb in zip(B, p_B) if b >= p_mid)

    ratio_fav = max(so_fav, bo_fav) / gft_m
    ratio_adv = max(so_adv, bo_adv) / gft_m

    print(f"Posted Price p=1 GFT: {gft_m}")
    print(f"Favourable Ties:   SO = {so_fav}, BO = {bo_fav}, max = {max(so_fav, bo_fav)}, ratio = {ratio_fav}")
    print(f"Adversarial Ties:  SO = {so_adv}, BO = {bo_adv}, max = {max(so_adv, bo_adv)}, ratio = {ratio_adv}")
    assert ratio_fav == Fraction(1, 1), f"Expected 1, got {ratio_fav}"
    assert ratio_adv == Fraction(3, 4), f"Expected 3/4, got {ratio_adv}"
    print("BDK 2x2 Calibration: PASS\n")


def calibrate_alphaevolve():
    print("=== 2. AlphaEvolve (arXiv:2603.08679) Calibration ===")
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

    # Seller Offering (using paper's >= tie-breaking rule)
    so = 0.0
    for s in range(H + 1):
        if pmf_s[s] <= 0: continue
        # Since 1 - s/p is non-decreasing for p >= 1, optimal price is H
        p_opt = H
        so += pmf_s[s] * (suff_val[p_opt] - s * suff_prob[p_opt])

    # Buyer Offering (using paper's > tie-breaking rule)
    pref_s_prob = np.cumsum(pmf_s)
    pref_s_val = np.cumsum(pmf_s * np.arange(H + 1))

    # To evaluate BO in under 1 second, vectorize in chunks of b
    bo = 0.0
    # Search over candidate grid: p <= b
    for b in range(H + 1):
        if pmf_b[b] <= 0: continue
        # profit for offer p <= b is cdf_s[p] * (b - p)
        # We can find argmax efficiently:
        # Since cdf_s is concave/modulated, argmax p is unimodal or near upper range
        p_arr = np.arange(b + 1)
        profs = cdf_s[:b+1] * (b - p_arr)
        # strictly greater keeps earliest index on tie
        max_idx = np.argmax(profs)
        bo += pmf_b[b] * (b * pref_s_prob[max_idx] - pref_s_val[max_idx])

    ro = 0.5 * (so + bo)
    print(f"FB: {fb:.6f} (target ~ 1.2322)")
    print(f"SO: {so:.6f} (target ~ 0.3312)")
    print(f"BO: {bo:.6f} (target ~ 0.8565)")
    print(f"RO: {ro:.6f}")
    print(f"FB / RO: {fb / ro:.4f} (target ~ 2.0749)")

    assert abs(fb - 1.2322) < 0.001, f"FB mismatch: {fb}"
    assert abs(so - 0.3312) < 0.001, f"SO mismatch: {so}"
    assert abs(bo - 0.8565) < 0.001, f"BO mismatch: {bo}"
    print("AlphaEvolve Calibration: PASS\n")


if __name__ == "__main__":
    calibrate_bdk_2x2()
    calibrate_alphaevolve()
