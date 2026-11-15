#!/usr/bin/env python3
"""Standalone high-precision complex line packing checker.
Evaluates pairwise Hermitian inner products in 40-digit mpmath after normalization.
"""

import sys
import os
import mpmath

def check():
    mpmath.mp.dps = 40
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obj_path = os.path.join(pkg_dir, "object", "5x49_v3r1t4s.txt")
    
    d, n = 5, 49
    table_best = mpmath.mpf("0.54164128")
    lower_bound = mpmath.mpf("0.50751922")
    min_margin = mpmath.mpf("1e-8")
    
    if not os.path.isfile(obj_path):
        print(f"FAIL: Object file not found: {obj_path}")
        return False
        
    with open(obj_path, 'r') as f:
        vals = [mpmath.mpf(line.strip()) for line in f if line.strip()]
        
    if len(vals) != 2 * d * n:
        print(f"FAIL: Expected {2*d*n} values, got {len(vals)}")
        return False
        
    reals = vals[:d*n]
    imags = vals[d*n:]
    
    vecs = []
    for j in range(n):
        v = [mpmath.mpc(reals[j*d + m], imags[j*d + m]) for m in range(d)]
        norm = mpmath.sqrt(sum(c.real**2 + c.imag**2 for c in v))
        if norm <= mpmath.mpf("1e-20"):
            print(f"FAIL: Vector {j} has degenerate norm {norm}")
            return False
        vecs.append([c / norm for c in v])
        
    max_c = mpmath.mpf(0)
    for j in range(n):
        for k in range(j+1, n):
            ip = sum(vecs[j][m].conjugate() * vecs[k][m] for m in range(d))
            overlap = mpmath.sqrt(ip.real**2 + ip.imag**2)
            if overlap > max_c:
                max_c = overlap
                
    drop = table_best - max_c
    print("Object: object/5x49_v3r1t4s.txt")
    print(f"Dimension d={d}, Lines n={n}")
    print(f"Computed Coherence mu (40 digits): {max_c}")
    print(f"Leaderboard Record Coherence    : {table_best}")
    print(f"Theoretical Lower Bound         : {lower_bound}")
    print(f"Strict Lowering Margin          : {drop}")
    
    if max_c < lower_bound:
        print("FAIL: Coherence is strictly below lower bound")
        return False
    if drop < min_margin:
        print("FAIL: Lowering margin is strictly less than 1e-8")
        return False
        
    print(f"VERIFIED: mu = {max_c} strictly beats {table_best} by {drop} >= 1e-8")
    return True

if __name__ == "__main__":
    ok = check()
    if ok:
        sys.exit(0)
    else:
        sys.exit(1)
