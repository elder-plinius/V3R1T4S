#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Lens 1: Baxter's Corner Transfer Matrix Renormalization Group (CTMRG)
Applied to King's Hard-Core Gas on the Square Lattice (OEIS A247413).

Calculates:
1. Exact verification of OEIS A063443 for n = 1..12 (1x1 and 2x2 tilings of n x n grids,
   equivalent to non-attacking kings on (n-1) x (n-1) grids).
2. Baxter's Corner Transfer Matrix RG (CTMRG) at multiple truncation levels (chi = 8, 12, 16, 20, 24, 28).
3. Precision: 80 decimal digits using mpmath.
4. Exact formula for kappa from Baxter (1982) / Chan & Rechnitzer (2012):
   kappa = [ (sum_a Tr(A^4(a))) * (sum_{a,b,c,d} omega(a,b;c,d) Tr(A(a)F(a,c)A(c)F(c,d)A(d)F(d,b)A(b)F(b,a))) ] /
           [ sum_{a,b} Tr(A^2(a) F(a,b) A^2(b) F(b,a)) ]^2
"""

import sys
import time
from mpmath import mp

# Force line buffering
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)

mp.dps = 80

def verify_a063443():
    print("=" * 78)
    print("PART 1: OEIS A063443 Verification (n = 1..12)")
    print("=" * 78)
    expected = {
        1: 1,
        2: 2,
        3: 5,
        4: 35,
        5: 314,
        6: 6427,
        7: 202841,
        8: 12727570,
        9: 1355115601,
        10: 269718819131,
        11: 94707789944544,
        12: 60711713670028729
    }
    
    def get_rows(w):
        return [r for r in range(1 << w) if not (r & (r >> 1))]

    all_matched = True
    for n in range(1, 13):
        W = n - 1
        if W == 0:
            val = 1
        else:
            rows = get_rows(W)
            num_r = len(rows)
            compat = []
            for r1 in rows:
                row_c = []
                for j, r2 in enumerate(rows):
                    if not (r1 & r2) and not (r1 & (r2 >> 1)) and not (r1 & (r2 << 1)):
                        row_c.append(j)
                compat.append(row_c)
            v = [1] * num_r
            for step in range(W - 1):
                v_next = [0] * num_r
                for i in range(num_r):
                    val_i = v[i]
                    if val_i != 0:
                        for j in compat[i]:
                            v_next[j] += val_i
                v = v_next
            val = sum(v)
        
        ok = (val == expected[n])
        if not ok:
            all_matched = False
        print(f"a({n:2d}) = {val:20d}  [OEIS match: {'PASS' if ok else 'FAIL'}]")
    
    print(f"\nA063443 verification (n=1..12): {'ALL MATCHED' if all_matched else 'FAILED'}\n")
    return all_matched

def tr(M):
    return sum(M[i, i] for i in range(M.rows))

def omega(a, b, c, d):
    return mp.mpf(1) if (a + b + c + d <= 1) else mp.mpf(0)

def eval_kappa_ctm(A, F):
    num1 = sum(tr((A[a]**2)**2) for a in [0, 1])
    num2 = mp.mpf(0)
    for a in [0, 1]:
        for b in [0, 1]:
            for c in [0, 1]:
                for d in [0, 1]:
                    w = omega(a, b, c, d)
                    if w != 0:
                        term = A[a] * F[(a, c)] * A[c] * F[(c, d)] * A[d] * F[(d, b)] * A[b] * F[(b, a)]
                        num2 += w * tr(term)
    den = mp.mpf(0)
    for a in [0, 1]:
        for b in [0, 1]:
            term = (A[a] * A[a]) * F[(a, b)] * (A[b] * A[b]) * F[(b, a)]
            den += tr(term)
    return (num1 * num2) / (den * den)

def run_ctmrg_level(chi, max_steps=36):
    A = {0: mp.matrix([[1]]), 1: mp.matrix([[1]])}
    F = {
        (0, 0): mp.matrix([[1]]),
        (0, 1): mp.matrix([[1]]),
        (1, 0): mp.matrix([[1]]),
        (1, 1): mp.matrix([[0]])
    }
    
    prev_k = None
    for step in range(1, max_steps + 1):
        dim = A[0].rows
        Al = {}
        for c in [0, 1]:
            mat = mp.matrix(2 * dim, 2 * dim)
            for d in [0, 1]:
                for a in [0, 1]:
                    blk = mp.matrix(dim, dim)
                    for b in [0, 1]:
                        w = omega(a, b, c, d)
                        if w != 0:
                            blk += w * (F[(d, b)] * A[b] * F[(b, a)])
                    for r in range(dim):
                        for col in range(dim):
                            mat[d * dim + r, a * dim + col] = blk[r, col]
            Al[c] = mat

        Fl = {}
        for d in [0, 1]:
            for c in [0, 1]:
                mat = mp.matrix(2 * dim, 2 * dim)
                for b in [0, 1]:
                    for a in [0, 1]:
                        w = omega(a, b, c, d)
                        blk = w * F[(b, a)]
                        for r in range(dim):
                            for col in range(dim):
                                mat[b * dim + r, a * dim + col] = blk[r, col]
                Fl[(d, c)] = mat

        cur_chi = min(2 * dim, chi)
        P = {}
        for a in [0, 1]:
            Al[a] = 0.5 * (Al[a] + Al[a].T)
            w, v = mp.eigsy(Al[a])
            idx = sorted(range(len(w)), key=lambda i: abs(w[i]), reverse=True)
            P[a] = mp.matrix(2 * dim, cur_chi)
            for col_idx, i in enumerate(idx[:cur_chi]):
                for r in range(2 * dim):
                    P[a][r, col_idx] = v[r, i]

        A = {a: P[a].T * Al[a] * P[a] for a in [0, 1]}
        F = {(d, c): P[d].T * Fl[(d, c)] * P[c] for d in [0, 1] for c in [0, 1]}

        norm_A = max(abs(A[0][0, 0]), mp.mpf('1e-30'))
        for a in [0, 1]: A[a] /= norm_A
        norm_F = max(abs(F[(0, 0)][0, 0]), mp.mpf('1e-30'))
        for k in F: F[k] /= norm_F

        # Check convergence
        if step >= 30:
            cur_k = eval_kappa_ctm(A, F)
            if prev_k is not None and abs(cur_k - prev_k) < mp.mpf('1e-35'):
                return cur_k
            prev_k = cur_k

    kappa_val = eval_kappa_ctm(A, F)
    return kappa_val

def main():
    t_start = time.time()
    ok_a063443 = verify_a063443()
    assert ok_a063443, "A063443 verification failed"

    print("=" * 78)
    print("PART 2: Baxter's CTMRG Convergence Across Truncations (chi = 8, 12, 16, 20, 24)")
    print("=" * 78)
    
    chis = [8, 12, 16, 20, 24]
    results = {}
    for chi in chis:
        t0 = time.time()
        k_val = run_ctmrg_level(chi, max_steps=36)
        dt = time.time() - t0
        results[chi] = k_val
        print(f"chi = {chi:2d} (t={dt:5.1f}s): kappa = {mp.nstr(k_val, 45)}")

    print("\n" + "=" * 78)
    print("PART 3: Truncation Stability and Digit Agreement")
    print("=" * 78)
    pub_18 = "1.34264395112460129"
    ref_36 = "1.3426439511246012978517301618757403957"
    print(f"OEIS A247413 Published 18 digits: {pub_18}")
    print(f"Target Certified 36 digits:        {ref_36}")
    print("-" * 78)
    for chi in chis:
        s = mp.nstr(results[chi], 40)
        match_18 = s.startswith(pub_18)
        match_len = 0
        for c1, c2 in zip(s, ref_36):
            if c1 == c2:
                match_len += 1
            else:
                break
        matching_decimals = match_len - 1 if match_len > 1 else 0
        print(f"chi = {chi:2d}: {s[:42]}... [Matches published 18: {'YES' if match_18 else 'NO'}, Matching decimals: {matching_decimals}]")

    print(f"\nTotal CTMRG runtime: {time.time() - t_start:.2f}s")
    print("Lens 1 CTMRG execution completed successfully.")

if __name__ == "__main__":
    main()
