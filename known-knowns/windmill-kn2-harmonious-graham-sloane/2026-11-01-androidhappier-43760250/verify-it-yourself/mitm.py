#!/usr/bin/env python3
"""mitm.py - independent second program (P2) for harmonious labelings of the windmill K_n^(2).

Definition: K_n^(2) = two copies of K_n sharing one vertex c; q = n(n-1) edges.  A harmonious labeling is an
injective f: V -> Z_q with the q edge sums f(u)+f(v) mod q pairwise distinct.

Algorithm (different from P1's nested backtracking): 
 1. Translation f -> f - f(c) (edge sums shift by -2 f(c), a bijection of Z_q; labels stay distinct), so f(c) = 0.
 2. Breadth-first, level by level, build EVERY n-subset S of Z_q with 0 in S whose C(n,2) pair sums are pairwise
    distinct mod q; record its sum set as a q-bit integer mask.
 3. A labeling is exactly a pair (S1, S2) of such sets with S1 & S2 = {0} and mask(S1) XOR mask(S2) = all ones with
    mask(S1) & mask(S2) = 0 (sums partition Z_q).  Since |mask| = C(n,2) = q/2 each, this is mask(S2) = ~mask(S1).
    Join through a dictionary keyed by mask.
No other symmetry is used.  Prints the number of sets, and the number of ordered pairs (S1,S2) that are labelings.
"""
import sys
from collections import defaultdict

def sets_with_distinct_sums(n, q):
    # level 1: {0}; elements are kept as tuples in increasing order, plus sum mask
    level = [((0,), 0)]
    for size in range(2, n + 1):
        nxt = []
        for elems, mask in level:
            for x in range(elems[-1] + 1, q):
                m = mask
                ok = True
                for e in elems:
                    s = (x + e) % q
                    bit = 1 << s
                    if m & bit:
                        ok = False
                        break
                    m |= bit
                if ok:
                    nxt.append((elems + (x,), m))
        level = nxt
    return level

def main():
    n = int(sys.argv[1]); q = n * (n - 1)
    full = (1 << q) - 1
    sets = sets_with_distinct_sums(n, q)
    bymask = defaultdict(list)
    for elems, mask in sets:
        bymask[mask].append(elems)
    sols = []
    for elems, mask in sets:
        comp = full ^ mask
        for other in bymask.get(comp, ()):
            if set(elems) & set(other) == {0}:
                sols.append((elems, other))
    print(f"n={n} q={q} sum_distinct_sets_containing_0={len(sets)} distinct_masks={len(bymask)} "
          f"solutions_ordered_pairs={len(sols)}")
    for a, b in sols[:20]:
        print("SOLUTION A=", a, "B=", b)
    print(f"VERDICT n={n}: {'HARMONIOUS' if sols else 'NOT HARMONIOUS'}")

if __name__ == "__main__":
    main()
