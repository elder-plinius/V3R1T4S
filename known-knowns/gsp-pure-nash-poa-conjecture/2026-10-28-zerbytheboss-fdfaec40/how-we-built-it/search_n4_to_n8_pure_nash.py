#!/usr/bin/env python3
"""
search_n4_to_n8_pure_nash.py

Searches for pure Nash equilibria in Generalized Second Price (GSP) auctions
with n in {4, 5, 6, 7, 8} bidders to test the Lucier-Paes Leme conjecture
that the Price of Anarchy for pure Nash equilibria is bounded by 1.259134.

Examines:
1. Canonical cyclic shift permutations: pi = (1, 2, ..., n-1, 0)
2. Ding et al. generalized permutations: pi = (1, n-1, 0, 2, ...)
3. Reversing and block-shift permutations
4. Random derangements with multi-start local optimization (SLSQP / trust-constr)
   enforcing exact pure Nash deviation conditions and no-overbidding (0 <= b_i <= v_i).
"""

import sys
import json
import itertools
import numpy as np
from pathlib import Path
from scipy.optimize import minimize

def solve_pure_nash_for_permutation(pi, n_restarts=15, rng_seed=42):
    """
    Given a permutation pi where bidder pi[j] is assigned to slot j (bids sorted descending: b_{pi[0]} >= ... >= b_{pi[n-1]}),
    solves for values v, CTRs alpha, and bids b to maximize OPT(v) / SW(b, v)
    subject to:
      1. alpha_0 = 1 >= alpha_1 >= ... >= alpha_{n-1} >= 0
      2. v_0 >= v_1 >= ... >= v_{n-1} >= 0, v_0 = 1 (normalization)
      3. Pointwise no-overbidding: 0 <= b_i <= v_i for all i
      4. Bid ordering: b_{pi[0]} >= b_{pi[1]} >= ... >= b_{pi[n-1]} >= 0
      5. Pure Nash equilibrium constraints:
         For each bidder i = pi[j] currently in slot j paying b_{pi[j+1]}:
           Utility u_i = alpha_j * (v_i - b_{pi[j+1]})
         Upward deviation: cannot strictly gain by bidding above b_{pi[k]} for k < j:
           alpha_k * (v_i - b_{pi[k]}) <= u_i  for all k < j
         Downward deviation: cannot strictly gain by bidding between b_{pi[k+1]} and b_{pi[k]} for k > j:
           alpha_k * (v_i - b_{pi[k+1]}) <= u_i  for all k > j (with b_{pi[n]} = 0)
    """
    n = len(pi)
    pos_of = {bidder: j for j, bidder in enumerate(pi)}
    
    # Variables:
    # alpha: n variables [alpha_0, ..., alpha_{n-1}], with alpha_0 = 1 fixed
    # v: n variables [v_0, ..., v_{n-1}], with v_0 = 1 fixed
    # b: n variables [b_0, ..., b_{n-1}]
    # Total free variables: (n-1) + (n-1) + n = 3n - 2.
    # Parameterize as x in [0, 1]^(3n-2):
    # x[0:n-1] -> alpha_1 ... alpha_{n-1}
    # x[n-1:2n-2] -> v_1 ... v_{n-1}
    # x[2n-2:3n-2] -> b_0 ... b_{n-1}
    
    def decode(x):
        alpha = np.zeros(n)
        alpha[0] = 1.0
        alpha[1:] = x[0:n-1]
        
        v = np.zeros(n)
        v[0] = 1.0
        v[1:] = x[n-1:2*n-2]
        
        b = x[2*n-2:3*n-2]
        return alpha, v, b

    def objective(x):
        alpha, v, b = decode(x)
        opt = np.dot(alpha, v)
        sw = sum(alpha[j] * v[pi[j]] for j in range(n))
        if sw < 1e-9:
            return 0.0
        return - (opt / sw)

    # Constraints:
    constraints = []
    
    # 1. alpha monotonic: alpha_{k} - alpha_{k+1} >= 0
    for k in range(n - 1):
        def make_alpha_mono(k=k):
            def c(x):
                alpha, _, _ = decode(x)
                return alpha[k] - alpha[k+1]
            return c
        constraints.append({'type': 'ineq', 'fun': make_alpha_mono(k)})

    # 2. v monotonic: v_{k} - v_{k+1} >= 0
    for k in range(n - 1):
        def make_v_mono(k=k):
            def c(x):
                _, v, _ = decode(x)
                return v[k] - v[k+1]
            return c
        constraints.append({'type': 'ineq', 'fun': make_v_mono(k)})

    # 3. No overbidding: v_i - b_i >= 0
    for i in range(n):
        def make_no_overbid(i=i):
            def c(x):
                _, v, b = decode(x)
                return v[i] - b[i]
            return c
        constraints.append({'type': 'ineq', 'fun': make_no_overbid(i)})

    # 4. Bid order matching pi: b_{pi[j]} - b_{pi[j+1]} >= 0
    for j in range(n - 1):
        def make_bid_order(j=j):
            def c(x):
                _, _, b = decode(x)
                return b[pi[j]] - b[pi[j+1]]
            return c
        constraints.append({'type': 'ineq', 'fun': make_bid_order(j)})

    # 5. Pure Nash equilibrium constraints:
    for j in range(n):
        i = pi[j]
        # Upward deviations k < j:
        for k in range(j):
            def make_up_dev(j=j, i=i, k=k):
                def c(x):
                    alpha, v, b = decode(x)
                    p_curr = b[pi[j+1]] if j + 1 < n else 0.0
                    u_curr = alpha[j] * (v[i] - p_curr)
                    # Dev to slot k: pays b_{pi[k]}
                    u_dev = alpha[k] * (v[i] - b[pi[k]])
                    return u_curr - u_dev
                return c
            constraints.append({'type': 'ineq', 'fun': make_up_dev(j, i, k)})
            
        # Downward deviations k > j:
        for k in range(j + 1, n):
            def make_down_dev(j=j, i=i, k=k):
                def c(x):
                    alpha, v, b = decode(x)
                    p_curr = b[pi[j+1]] if j + 1 < n else 0.0
                    u_curr = alpha[j] * (v[i] - p_curr)
                    # Dev to slot k: pays b_{pi[k+1]} if k+1 < n else 0
                    p_dev = b[pi[k+1]] if k + 1 < n else 0.0
                    u_dev = alpha[k] * (v[i] - p_dev)
                    return u_curr - u_dev
                return c
            constraints.append({'type': 'ineq', 'fun': make_down_dev(j, i, k)})

    bounds = [(0.0, 1.0)] * (3 * n - 2)
    
    best_ratio = 1.0
    best_solution = None
    
    rng = np.random.default_rng(rng_seed)
    
    for r in range(n_restarts):
        # Sample plausible monotonic alpha and v
        raw_alpha = np.sort(rng.uniform(0.01, 0.99, size=n-1))[::-1]
        raw_v = np.sort(rng.uniform(0.01, 0.99, size=n-1))[::-1]
        
        # Sample bids matching order of pi and no-overbidding
        # Start with small bids b_{pi[j]}
        raw_b_ordered = np.sort(rng.uniform(0.005, 0.5, size=n))[::-1]
        raw_b = np.zeros(n)
        for j in range(n):
            raw_b[pi[j]] = min(raw_b_ordered[j], 1.0 if pi[j] == 0 else raw_v[pi[j]-1])
            
        x0 = np.concatenate([raw_alpha, raw_v, raw_b])
        
        res = minimize(
            objective,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': 500, 'ftol': 1e-7, 'disp': False}
        )
        
        if res.success or res.fun < -1.0:
            ratio = -res.fun
            # Check feasibility rigorously
            feasible = True
            for c in constraints:
                if c['fun'](res.x) < -1e-4:
                    feasible = False
                    break
            if feasible and ratio > best_ratio:
                best_ratio = ratio
                alpha_sol, v_sol, b_sol = decode(res.x)
                best_solution = {
                    'ratio': float(ratio),
                    'alpha': [float(round(a, 6)) for a in alpha_sol],
                    'v': [float(round(val, 6)) for val in v_sol],
                    'b': [float(round(bid, 6)) for bid in b_sol],
                }

    return best_ratio, best_solution

def run_pure_nash_search():
    results = {}
    print("=" * 70)
    print("Searching Pure Nash Equilibrium PoA for n = 4, 5, 6, 7, 8")
    print("=" * 70)

    for n in range(4, 9):
        print(f"\n--- Testing n = {n} ---")
        candidate_perms = []
        
        # 1. Cyclic shift: (1, 2, ..., n-1, 0)
        perm_cyclic = list(range(1, n)) + [0]
        candidate_perms.append(("cyclic_shift", perm_cyclic))
        
        # 2. Ding et al. generalized: (1, n-1, 0, 2, ...)
        perm_ding = [1, n-1, 0] + [i for i in range(2, n-1)]
        candidate_perms.append(("ding_generalized", perm_ding))
        
        # 3. Two-block shift: [1, 0, 3, 2, ...]
        perm_block = []
        for b in range(0, n - 1, 2):
            perm_block.extend([b+1, b])
        if len(perm_block) < n:
            perm_block.append(n-1)
        candidate_perms.append(("two_block_shift", perm_block))
        
        # 4. Derangements / additional permutations
        # Reverse order: (n-1, n-2, ..., 0)
        candidate_perms.append(("reverse", list(range(n-1, -1, -1))))
        
        # Random derangements
        rng = np.random.default_rng(100 + n)
        for d in range(8):
            p = list(range(n))
            while True:
                rng.shuffle(p)
                if all(p[k] != k for k in range(n)):
                    break
            candidate_perms.append((f"derangement_{d}", p))
            
        n_results = []
        max_ratio_for_n = 1.0
        best_perm_info = None
        
        for name, p in candidate_perms:
            ratio, sol = solve_pure_nash_for_permutation(p, n_restarts=10, rng_seed=42 + n)
            n_results.append({
                'permutation_name': name,
                'permutation': p,
                'max_pure_nash_ratio': ratio,
                'exceeds_lucier_paes_leme': bool(ratio > 1.259134),
                'solution': sol
            })
            if ratio > max_ratio_for_n:
                max_ratio_for_n = ratio
                best_perm_info = (name, p, ratio)
                
            print(f"  Permutation {p} ({name}): max pure NE ratio = {ratio:.6f}")
            
        results[f"n={n}"] = {
            'n': n,
            'max_pure_nash_ratio': max_ratio_for_n,
            'best_permutation': best_perm_info[1] if best_perm_info else None,
            'best_permutation_name': best_perm_info[0] if best_perm_info else None,
            'exceeds_lucier_paes_leme_conjecture': bool(max_ratio_for_n > 1.259134),
            'tested_permutations': n_results
        }
        print(f"--> Summary for n={n}: max ratio = {max_ratio_for_n:.6f} (exceeds 1.259134: {max_ratio_for_n > 1.259134})")

    out_file = Path("runs/2026-10-28-1950/attempts/lens1_gsp_poa_cce_nash/output/n4_to_n8_pure_nash_search.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nAll search results saved to {out_file}")

if __name__ == "__main__":
    run_pure_nash_search()
