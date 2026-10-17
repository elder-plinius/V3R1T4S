#!/usr/bin/env python3
"""Standalone check written from the definition: s_i in {+1,-1}, C_k = sum_{i=0}^{L-1-k} s_i s_{i+k},
E = sum_{k=1}^{L-1} C_k^2 (exact integers), F = L^2/(2E). In object/sequence.txt, 0 means +1 and 1 means -1
(a global sign flip does not change E). Exit code 0 only if the length, the alphabet and the claimed energy all
match and the energy is strictly below the best published value."""
import sys
L, E_CLAIM, E_BEST = 391, 10471, 10675
s = open("object/sequence.txt").read().strip()
if len(s) != L or not set(s) <= {"0", "1"}:
    print("wrong length or alphabet: length %d" % len(s))
    sys.exit(1)
x = [1 if ch == "0" else -1 for ch in s]
E = sum(sum(x[i] * x[i + k] for i in range(L - k)) ** 2 for k in range(1, L))
print("length %d, energy %d (F = %.4f); claimed %d; best published %d" % (L, E, L * L / (2 * E), E_CLAIM, E_BEST))
sys.exit(0 if E == E_CLAIM and E < E_BEST else 1)
