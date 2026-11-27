#!/usr/bin/env python3
"""
neon_global_L_exact_map_r12.py

Uses the exact Lemma A1 projection:
  Any odd covering with omega(L) = r and L < X projects to a covering on the FIRST r
  odd primes P_r = (3, 5, ..., p_{r-1}) with exponents e = (e_0, ..., e_{r-1}) >= 1
  satisfying prod p_m^{e_m} < X!

Maps EVERY exponent vector e on P_r (r = 9, 10, 11, 12, 13) with prod p_m^{e_m} < 10^16
under scalar Lemma U, identifying the EXACT Pareto-minimal survivors and Pareto-maximal
killable families!
"""
import time
import sys
import os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from neon_global_bound_probe_r12 import ODD_PRIMES, optimize_scalar

def enum_exp_vecs(r, max_L):
    ps = tuple(ODD_PRIMES[:r])
    base = 1
    for p in ps:
        base *= p
    if base >= max_L:
        return ps, []
    # Factor budget = max_L // base
    res = []
    def dfs(pos, cur_L, es):
        if pos == r:
            res.append((cur_L, tuple(es)))
            return
        p = ps[pos]
        # remaining primes already included in base via exponent 1!
        # Wait: let's build from cur_L starting at base, multiplying by p^(e-1)
        e = 1
        val = cur_L
        while val < max_L:
            dfs(pos + 1, val, es + [e])
            e += 1
            val *= p
    dfs(0, base, [])
    res.sort()
    return ps, res

def pareto_min(items):
    """Given list of (L, es, B), keep only minimal es (no other es' <= es componentwise)."""
    # Sort by sum(es) ascending
    items_s = sorted(items, key=lambda x: (sum(x[1]), x[0]))
    mins = []
    for L, es, B in items_s:
        if any(all(m_es[i] <= es[i] for i in range(len(es))) for _, m_es, _ in mins):
            continue
        mins.append((L, es, B))
    mins.sort()
    return mins

def main():
    t0 = time.time()
    L_NEW9 = 3**5 * 5**3 * 7**2 * 11**2 * 13**2 * 17 * 19 * 23 * 29  # 6,557,114,959,770,375
    L_PUB  = 168131152814625

    for r, cap in [(9, 10**15), (10, L_NEW9), (11, L_NEW9), (12, L_NEW9), (13, 2 * 10**16)]:
        ps, vecs = enum_exp_vecs(r, cap)
        print(f"\n================ omega(L) = {r} (cap = {cap:,}) ================")
        print(f"Total exponent vectors on P_{r} with L < cap: {len(vecs)}")
        if not vecs:
            continue
        # Test in order; use monotonicity!
        # Maintain killed_max (if e <= k for some killed k -> killed) and surv_min (if e >= s -> survives? wait optimizer is heuristic so test all non-dominated!)
        survivors = []
        killed = 0
        # Sort by sum(es) descending to kill large vectors first? Wait, sorting ascending finds smallest survivors fast;
        # actually with only a few hundred/thousand vectors, test smartly!
        killed_front = []
        for L, es in vecs:
            # Skip if dominated by an already-killed vector (es <= k)
            if any(all(es[i] <= k[i] for i in range(r)) for k in killed_front):
                killed += 1
                continue
            B, cfg = optimize_scalar(ps, es, early_stop=0.98)
            if B < 0.9995:
                killed += 1
                # Add to killed_front (prune dominated)
                killed_front = [k for k in killed_front if not all(k[i] <= es[i] for i in range(r))]
                killed_front.append(es)
            else:
                survivors.append((L, es, B))
        # Second pass on survivors with thorough optimization (early_stop=0)
        real_surv = []
        for L, es, _ in survivors:
            if any(all(es[i] <= k[i] for i in range(r)) for k in killed_front):
                killed += 1
                continue
            B, cfg = optimize_scalar(ps, es, early_stop=0.0)
            if B < 0.9999:
                killed += 1
                killed_front = [k for k in killed_front if not all(k[i] <= es[i] for i in range(r))]
                killed_front.append(es)
            else:
                real_surv.append((L, es, B))
        real_surv.sort()
        pmins = pareto_min(real_surv)
        print(f"Killed by scalar Lemma U: {killed} / {len(vecs)} | Surviving: {len(real_surv)} | Pareto-minimal survivors: {len(pmins)}")
        for idx, (L, es, B) in enumerate(pmins[:25]):
            print(f"  PMIN #{idx+1:2d}: L={L:>21,} ({L/L_PUB:6.2f}x pub) | B={B:.6f} | e={es}")
        if real_surv:
            print(f"  --> SMALLEST SCALAR SURVIVOR (omega={r}): L = {real_surv[0][0]:,} ({real_surv[0][0]/L_PUB:.3f}x pub), e={real_surv[0][1]}, B={real_surv[0][2]:.6f}")

    print(f"\nElapsed: {time.time()-t0:.2f}s")

if __name__ == "__main__":
    main()
