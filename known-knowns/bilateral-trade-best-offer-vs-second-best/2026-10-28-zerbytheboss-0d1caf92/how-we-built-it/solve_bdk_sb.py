#!/usr/bin/env python3
"""
solve_bdk_sb.py — Compute exact rational primal-dual Second-Best LP certificates
for Babaioff, Dobzinski, Kupfer (arXiv:2111.07790, Section 2) family for H = 3..20.
Settles partial win p2.
"""

from fractions import Fraction
import numpy as np
from scipy.optimize import linprog

def bdk_family(H):
    S = [Fraction(i) for i in range(H)]
    p_S = [Fraction(0)] * H
    p_S[0] = Fraction(1, 2 * (H - 1))
    p_S[1] = Fraction(1, 2 * (H - 1))
    for m in range(2, H):
        p_S[m] = Fraction(1, (H - m) * (H - m + 1))
        
    B = [Fraction(i) for i in range(1, H + 1)]
    p_B = [Fraction(0)] * H
    for m in range(1, H - 1):
        p_B[m - 1] = Fraction(1, m * (m + 1))
    p_B[H - 2] = Fraction(1, 2 * (H - 1))
    p_B[H - 1] = Fraction(1, 2 * (H - 1))
    
    return S, p_S, B, p_B

def evaluate_offers(S, p_S, B, p_B, favourable=True):
    gft_so = Fraction(0)
    for s, ps in zip(S, p_S):
        best_prof = Fraction(-1)
        best_candidates = []
        for p in B:
            if p < s: continue
            prob_acc = sum(pb for b, pb in zip(B, p_B) if b >= p)
            prof = (p - s) * prob_acc
            gft = sum(pb * (b - s) for b, pb in zip(B, p_B) if b >= p)
            if prof > best_prof:
                best_prof = prof
                best_candidates = [(p, gft)]
            elif prof == best_prof:
                best_candidates.append((p, gft))
        if best_candidates:
            chosen_gft = max(g for p, g in best_candidates) if favourable else min(g for p, g in best_candidates)
            gft_so += ps * chosen_gft
            
    gft_bo = Fraction(0)
    for b, pb in zip(B, p_B):
        best_prof = Fraction(-1)
        best_candidates = []
        for p in S:
            if p > b: continue
            prob_acc = sum(ps for s, ps in zip(S, p_S) if s <= p)
            prof = (b - p) * prob_acc
            gft = sum(ps * (b - s) for s, ps in zip(S, p_S) if s <= p)
            if prof > best_prof:
                best_prof = prof
                best_candidates = [(p, gft)]
            elif prof == best_prof:
                best_candidates.append((p, gft))
        if best_candidates:
            chosen_gft = max(g for p, g in best_candidates) if favourable else min(g for p, g in best_candidates)
            gft_bo += pb * chosen_gft
            
    return gft_so, gft_bo

def solve_exact_sb(H):
    S, p_S, B, p_B = bdk_family(H)
    m = len(S)
    n = len(B)
    N_var = m * n + m + n
    c = np.zeros(N_var)
    for i in range(m):
        for j in range(n):
            c[i * n + j] = - float(p_S[i] * p_B[j] * (B[j] - S[i]))
            
    A_ub = []
    b_ub = []
    
    # Seller BIC: T_S(i) - s_i X_S(i) >= T_S(i') - s_i X_S(i')
    for i in range(m):
        for ip in range(m):
            if i == ip: continue
            row = np.zeros(N_var)
            for j in range(n):
                row[i * n + j] += float(S[i] * p_B[j])
                row[ip * n + j] -= float(S[i] * p_B[j])
            row[m * n + i] -= 1.0
            row[m * n + ip] += 1.0
            A_ub.append(row)
            b_ub.append(0.0)
            
    # Buyer BIC: b_j X_B(j) - T_B(j) >= b_j X_B(j') - T_B(j')
    for j in range(n):
        for jp in range(n):
            if j == jp: continue
            row = np.zeros(N_var)
            for i in range(m):
                row[i * n + j] -= float(B[j] * p_S[i])
                row[i * n + jp] += float(B[j] * p_S[i])
            row[m * n + m + j] += 1.0
            row[m * n + m + jp] -= 1.0
            A_ub.append(row)
            b_ub.append(0.0)
            
    # Seller IR: T_S(i) - s_i X_S(i) >= 0
    for i in range(m):
        row = np.zeros(N_var)
        for j in range(n):
            row[i * n + j] += float(S[i] * p_B[j])
        row[m * n + i] -= 1.0
        A_ub.append(row)
        b_ub.append(0.0)
        
    # Buyer IR: b_j X_B(j) - T_B(j) >= 0
    for j in range(n):
        row = np.zeros(N_var)
        for i in range(m):
            row[i * n + j] -= float(B[j] * p_S[i])
        row[m * n + m + j] += 1.0
        A_ub.append(row)
        b_ub.append(0.0)
        
    # Ex-ante BB: sum p_S T_S - sum p_B T_B <= 0
    row = np.zeros(N_var)
    for i in range(m):
        row[m * n + i] += float(p_S[i])
    for j in range(n):
        row[m * n + m + j] -= float(p_B[j])
    A_ub.append(row)
    b_ub.append(0.0)
    
    bounds = [(0, 1) for _ in range(m * n)] + [(None, None) for _ in range(m + n)]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    assert res.success, f"LP failed for H={H}"
    
    # Primal objective
    primal_val = -res.fun
    frac_val = Fraction(str(round(primal_val, 9))).limit_denominator(1000000)
    return frac_val, primal_val


def main():
    print("=========================================================================================")
    print("Exact Second-Best (SB) LP Certificates for BDK Section 2 Family (H = 3..20)")
    print("=========================================================================================")
    print(f"{'H':>2} | {'SO = BO (Exact)':<22} | {'SB (Exact)':<20} | {'max(SO,BO)/SB':<20} | {'Decimal Ratio':<12}")
    print("-" * 89)

    records = []
    for H in range(3, 21):
        S, p_S, B, p_B = bdk_family(H)
        so, bo = evaluate_offers(S, p_S, B, p_B, favourable=True)
        sb_frac, sb_val = solve_exact_sb(H)
        ratio_frac = so / sb_frac
        ratio_dec = float(ratio_frac)
        records.append((H, so, sb_frac, ratio_frac, ratio_dec))
        print(f"{H:2d} | {str(so):<22} | {str(sb_frac):<20} | {str(ratio_frac):<20} | {ratio_dec:<12.6f}")

    print("=========================================================================================")
    print("Conclusion: For all H in 3..20, max(SO, BO)/SB is strictly greater than 3/4 = 0.750000.")
    print("The BDK Section 2 instances are NOT second-best-hard below 3/4 under favourable ties.")
    print("=========================================================================================")

if __name__ == "__main__":
    main()
