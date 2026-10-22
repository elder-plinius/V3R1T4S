"""Write a colex .npy never-condition assignment as text: one line per triple 'a b c iNj' (a<b<c, 1-based;
the i-th smallest alternative of the triple is never at position j, j = 1 top, 2 middle, 3 bottom).
Usage: python assign_txt.py N in.npy out.txt"""
import sys
from itertools import combinations
from math import comb
import numpy as np
n = int(sys.argv[1]); c = np.load(sys.argv[2])
assert len(c) == comb(n, 3)
with open(sys.argv[3], 'w') as f:
    for a, b, d in combinations(range(n), 3):
        code = int(c[comb(d, 3) + comb(b, 2) + a]); assert code < 9
        f.write(f'{a+1} {b+1} {d+1} {code//3+1}N{code%3+1}\n')
print('wrote', sys.argv[3], comb(n, 3), 'lines')
