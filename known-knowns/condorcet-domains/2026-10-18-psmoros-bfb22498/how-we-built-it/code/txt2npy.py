"""Convert an assignment text (`a b c iNj`, 1-based) to the .npy used by lsx (uint8, colex C(c,3)+C(b,2)+a, code 3*(i-1)+(j-1)).
Usage: python txt2npy.py IN.txt N OUT.npy"""
import sys
from math import comb
import numpy as np
n = int(sys.argv[2]); a = np.full(comb(n, 3), 255, dtype=np.uint8)
for ln in open(sys.argv[1]):
    x, y, z, c = ln.split(); x, y, z = int(x) - 1, int(y) - 1, int(z) - 1; i, j = int(c[0]), int(c[2])
    assert 0 <= x < y < z < n and c[1] == "N"; a[comb(z, 3) + comb(y, 2) + x] = 3 * (i - 1) + (j - 1)
assert (a < 9).all(); np.save(sys.argv[3], a)
