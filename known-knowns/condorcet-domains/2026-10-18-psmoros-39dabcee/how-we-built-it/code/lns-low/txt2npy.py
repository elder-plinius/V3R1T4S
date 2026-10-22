"""Convert an assignment text file (lines 'a b c iNj', 1-based) to the colex uint8 .npy encoding (3*(i-1)+(j-1))."""
import sys
from math import comb
import numpy as np
txt, n, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
cond = np.full(comb(n, 3), 255, dtype=np.uint8)
for ln in open(txt):
    a, b, c, r = ln.split(); a, b, c = int(a) - 1, int(b) - 1, int(c) - 1
    assert a < b < c
    i, j = int(r[0]), int(r[2]); cond[comb(c, 3) + comb(b, 2) + a] = 3 * (i - 1) + (j - 1)
assert (cond < 9).all(); np.save(out, cond); print('wrote', out, 'triples', len(cond))
