#!/usr/bin/env python3
"""Brute force over ALL injective labelings of K_4^(2) (7 vertices, Z_12), no reduction at all.
Validates the translation reduction: expected labelings = (ordered pairs with f(c)=0) * q translations * ((n-1)!)^2."""
import itertools
n, q = 4, 12
cnt = 0
for lab in itertools.permutations(range(q), 2 * n - 1):
    c, a, b = lab[0], lab[1:n], lab[n:]
    A = (c,) + a; B = (c,) + b
    sums = [(x + y) % q for x, y in itertools.combinations(A, 2)] + [(x + y) % q for x, y in itertools.combinations(B, 2)]
    if len(set(sums)) == q:
        cnt += 1
print("brute_force_labelings", cnt, "expected", 48 * q * 6 * 6)
