#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Lens 1: Symmetric Corner Transfer Matrix Renormalization Group (CTMRG)
Applied to the Monomer-Dimer Model on the Square Lattice (OEIS A028420).

Calculates:
1. Exact verification of OEIS A028420 for n = 1..14 via frontier transfer DP.
2. Symmetric CTMRG on the 4-state monomer-dimer vertex tensor:
   T_{s_N, s_E, s_S, s_W} = 1 if s_N + s_E + s_S + s_W <= 1 else 0.
3. 80-digit precision arithmetic using mpmath.
4. Evaluation across bond dimensions chi in {8, 12, 16, 20, 24, 28, 32}.
5. Extraction of partition function per site kappa and monomer-dimer entropy h_2 = ln(kappa).
6. Verification against Kong's 2006 bracket [0.662798972831, 0.662798972845].
7. Certification of >= 24 stable matching decimal digits.
"""

import os
import sys
import time
import mpmath as mp

# Force unbuffered output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)

mp.mp.dps = 80

def verify_a028420():
    print("=" * 80)
    print("PART 1: OEIS A028420 Verification (n = 1..14)")
    print("=" * 80)
    
    expected = {
        1: 1,
        2: 7,
        3: 131,
        4: 10012,
        5: 2810694,
        6: 2989126727,
        7: 11945257052321,
        8: 179788343101980135,
        9: 10185111919160666118608,
        10: 2172138783673094193937750015,
        11: 1743829823240164494694386437970640,
        12: 5270137993816086266962874395450234534887,
        13: 59956919824257750508655631107474672284499736089,
        14: 2567773069787030667011494675812637832667677810219203068
    }
    
    all_matched = True
    for n in range(1, 15):
        t0 = time.time()
        dp = {0: 1}
        for r in range(n):
            for c in range(n):
                new_dp = {}
                for state, cnt in dp.items():
                    mask_v = state >> 1
                    l = state & 1
                    u = (mask_v >> c) & 1
                    if u and l:
                        continue
                    elif u or l:
                        new_mask_v = mask_v & ~(1 << c)
                        new_state = new_mask_v << 1
                        new_dp[new_state] = new_dp.get(new_state, 0) + cnt
                    else:
                        # 1. Monomer
                        new_state = mask_v << 1
                        new_dp[new_state] = new_dp.get(new_state, 0) + cnt
                        # 2. Vertical dimer down
                        if r < n - 1:
                            new_state = (mask_v | (1 << c)) << 1
                            new_dp[new_state] = new_dp.get(new_state, 0) + cnt
                        # 3. Horizontal dimer right
                        if c < n - 1:
                            new_state = (mask_v << 1) | 1
                            new_dp[new_state] = new_dp.get(new_state, 0) + cnt
                dp = new_dp
        val = dp.get(0, 0)
        dt = time.time() - t0
        ok = (val == expected[n])
        if not ok:
            all_matched = False
        print(f"a({n:2d}) = {val:55d}  [OEIS match: {'PASS' if ok else 'FAIL'}] ({dt:.3f}s)")
        
    print(f"\nA028420 verification (n=1..14): {'ALL MATCHED' if all_matched else 'FAILED'}\n")
    return all_matched

def run_ctmrg_solver():
    print("=" * 80)
    print("PART 2: Symmetric CTMRG on Monomer-Dimer Vertex Tensor (80 Digits)")
    print("=" * 80)
    
    # Vertex tensor W: W[(n, e, s, w)] = 1 if n + e + s + w <= 1 else 0
    W = {}
    for n in range(2):
        for e in range(2):
            for s in range(2):
                for w in range(2):
                    W[(n, e, s, w)] = mp.mpf(1) if n + e + s + w <= 1 else mp.mpf(0)
                    
    results = {}
    chis = [8, 12, 16, 20, 24, 28, 32]
    
    for chi in chis:
        t0 = time.time()
        # Initialize C: 2x2
        C = mp.matrix(2, 2)
        for e in range(2):
            for s in range(2):
                C[e, s] = W[(0, e, s, 0)]
                
        # Initialize T: list of two 2x2 matrices T[s]
        T = [mp.matrix(2, 2) for _ in range(2)]
        for s in range(2):
            for w in range(2):
                for e in range(2):
                    T[s][w, e] = W[(0, e, s, w)]
                    
        dc = 2
        prev_h2 = None
        converged_step = 0
        norm_t = mp.mpf(1)
        
        for step in range(1, 35):
            # Precompute M[n, w] = T[n].T * C * T[w]
            M = {}
            for n in range(2):
                for w in range(2):
                    M[(n, w)] = T[n].T * C * T[w]
                    
            # Build C_tilde of size (2*dc) x (2*dc)
            C_tilde = mp.matrix(2 * dc, 2 * dc)
            for e in range(2):
                for s in range(2):
                    blk = mp.matrix(dc, dc)
                    for n in range(2):
                        for w in range(2):
                            wt = W[(n, e, s, w)]
                            if wt != 0:
                                blk += wt * M[(n, w)]
                    for i in range(dc):
                        for j in range(dc):
                            C_tilde[i * 2 + e, j * 2 + s] = blk[i, j]
                            
            C_tilde = 0.5 * (C_tilde + C_tilde.T)
            
            # Build T_tilde: for each s in range(2), shape (2*dc) x (2*dc)
            T_tilde = [mp.matrix(2 * dc, 2 * dc) for _ in range(2)]
            for s in range(2):
                for w in range(2):
                    for e in range(2):
                        blk = mp.matrix(dc, dc)
                        for n in range(2):
                            wt = W[(n, e, s, w)]
                            if wt != 0:
                                blk += wt * T[n]
                        for i in range(dc):
                            for j in range(dc):
                                T_tilde[s][i * 2 + w, j * 2 + e] = blk[i, j]
                                
            # Eigendecomposition of symmetric C_tilde
            vals, vecs = mp.eigsy(C_tilde)
            idx = sorted(range(len(vals)), key=lambda i: abs(vals[i]), reverse=True)
            new_chi = min(2 * dc, chi)
            
            P = mp.matrix(2 * dc, new_chi)
            for j in range(new_chi):
                col = idx[j]
                for i in range(2 * dc):
                    P[i, j] = vecs[i, col]
                    
            # Project C and T
            C = P.T * C_tilde * P
            norm_c = max(abs(C[i, j]) for i in range(new_chi) for j in range(new_chi))
            C /= norm_c
            
            T_next = [P.T * T_tilde[s] * P for s in range(2)]
            norm_t = max(abs(T_next[s][i, j]) for s in range(2) for i in range(new_chi) for j in range(new_chi))
            T = [T_next[s] / norm_t for s in range(2)]
            dc = new_chi
            
            cur_h2 = mp.log(norm_t)
            if prev_h2 is not None and abs(cur_h2 - prev_h2) < mp.mpf('1e-50'):
                converged_step = step
                break
            prev_h2 = cur_h2
            converged_step = step
            
        dt = time.time() - t0
        kappa_val = norm_t
        h2_val = mp.log(norm_t)
        results[chi] = (kappa_val, h2_val)
        
        print(f"chi = {chi:2d} (converged at step {converged_step:2d}, {dt:.2f}s):")
        print(f"  kappa = {mp.nstr(kappa_val, 40)}")
        print(f"  h2    = {mp.nstr(h2_val, 40)}")
        
    print("\n" + "=" * 80)
    print("PART 3: Truncation Stability & Kong Bracket Verification")
    print("=" * 80)
    
    kong_low = mp.mpf('0.662798972831')
    kong_high = mp.mpf('0.662798972845')
    kong_est = mp.mpf('0.662798972834')
    
    h2_last = results[chis[-1]][1]
    in_bracket = (kong_low <= h2_last <= kong_high)
    print(f"Kong bracket: [{mp.nstr(kong_low, 15)}, {mp.nstr(kong_high, 15)}]")
    print(f"Final h2 (chi={chis[-1]}): {mp.nstr(h2_last, 40)}")
    print(f"Inside Kong bracket: {'YES (PASS)' if in_bracket else 'NO (FAIL)'}")
    print(f"Matches Kong 0.662798972834 to 12 decimals: {'YES (PASS)' if str(h2_last)[:14] == str(kong_est)[:14] else 'NO'}")
    
    print("\nConsecutive Digit Differences across Truncations:")
    for i in range(len(chis) - 1):
        c1, c2 = chis[i], chis[i+1]
        diff = abs(results[c2][1] - results[c1][1])
        print(f"  |h2(chi={c2:2d}) - h2(chi={c1:2d})| = {mp.nstr(diff, 10)}")
        
    # Match count across last 3 truncations (chi=24, 28, 32)
    s24 = mp.nstr(results[24][1], 50)
    s28 = mp.nstr(results[28][1], 50)
    s32 = mp.nstr(results[32][1], 50)
    
    match_len = 0
    while match_len < len(s24) and match_len < len(s28) and match_len < len(s32) and s24[match_len] == s28[match_len] == s32[match_len]:
        match_len += 1
    # subtract 2 for '0.'
    matching_decimals = match_len - 2
    print(f"\nStable matching decimals across chi in {{24, 28, 32}}: {matching_decimals}")
    print(f"Certified digits (h2): {s32[:match_len]}")
    
    return results, in_bracket, matching_decimals

def main():
    t_start = time.time()
    ok_a028420 = verify_a028420()
    assert ok_a028420, "OEIS A028420 verification failed!"
    
    results, in_bracket, matching_decimals = run_ctmrg_solver()
    assert in_bracket, "h2 is not inside Kong's bracket!"
    assert matching_decimals >= 24, f"Fewer than 24 matching decimals: {matching_decimals}"
    
    total_dt = time.time() - t_start
    print(f"\nTotal execution time: {total_dt:.2f}s")
    print("Lens 1: SUCCESSFUL SOLUTION CLAIM.")

if __name__ == '__main__':
    main()
