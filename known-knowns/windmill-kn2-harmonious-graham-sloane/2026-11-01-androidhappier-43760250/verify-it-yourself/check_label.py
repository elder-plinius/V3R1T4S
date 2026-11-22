#!/usr/bin/env python3
"""check_label.py n "c a1 .. a_{n-1}" "b1 .. b_{n-1}"
Checks a labeling of the windmill K_n^(2) straight from the definition (Graham-Sloane 1980): q = n(n-1) edges;
vertices c (shared), a_1..a_{n-1} (clique 1), b_1..b_{n-1} (clique 2); labels must be 2n-1 DISTINCT residues mod q and
the q edge sums (each clique is complete, c in both) pairwise distinct mod q. Prints VALID or INVALID: <reason>."""
import sys, itertools
n = int(sys.argv[1]); q = n * (n - 1)
first = [int(t) % q for t in sys.argv[2].split()]
second = [int(t) % q for t in sys.argv[3].split()]
c, a = first[0], first[1:]
b = second
if len(a) != n - 1 or len(b) != n - 1:
    print("INVALID: wrong vertex count"); sys.exit(1)
labels = [c] + a + b
if len(set(labels)) != 2 * n - 1:
    print("INVALID: labels not distinct"); sys.exit(1)
edges = list(itertools.combinations([c] + a, 2)) + list(itertools.combinations([c] + b, 2))
assert len(edges) == q
sums = [(u + v) % q for u, v in edges]
if len(set(sums)) != q:
    print("INVALID: edge sums repeat"); sys.exit(1)
print("VALID"); sys.exit(0)
