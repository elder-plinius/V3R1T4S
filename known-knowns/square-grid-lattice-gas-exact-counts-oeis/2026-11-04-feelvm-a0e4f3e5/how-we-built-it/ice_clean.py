"""Clean transfer matrix for the ice model on the n×n torus (A054759).

The ice rule at each vertex: 2-IN, 2-OUT among 4 edges.
From the vertex equation (1-s[j]) + s'[j] + (1-h[j-1]) + h[j] = 2:
  h[j] = h[j-1] + s[j] - s'[j]
The h-values must be 0 or 1. The h-sequence wraps around (h[n] = h[0]).

The transfer matrix element T[s][s']:
1. The flip set D = {j: s[j] ≠ s'[j]} must have EVEN cardinality (cycle closure).
2. The s[j]-values at D positions must ALTERNATE between 0 and 1 in cyclic order
   (otherwise the h-sequence has values outside {0,1}).
3. T[s][s'] = 2 if D = ∅ (two possible h-values), 1 if D ≠ ∅ and conditions hold.
"""
import numpy as np


def transfer_element(s, s_prime, n):
    flip_s_vals = []
    for j in range(n):
        sj = (s >> j) & 1
        spj = (s_prime >> j) & 1
        if sj != spj:
            flip_s_vals.append(sj)
    k = len(flip_s_vals)
    if k % 2 != 0:
        return 0
    if k == 0:
        return 2
    for i in range(k):
        if flip_s_vals[i] == flip_s_vals[(i + 1) % k]:
            return 0
    return 1


def build_transfer(n):
    size = 1 << n
    T = np.zeros((size, size), dtype=np.int64)
    for s in range(size):
        for sp in range(size):
            T[s][sp] = transfer_element(s, sp, n)
    return T


def trace_power(T, p):
    return int(np.trace(np.linalg.matrix_power(T, p)))
