"""Write a never-condition assignment (.npy, uint8, colex index C(c,3)+C(b,2)+a, code 3*s+p) as text lines
`a b c iNj` (1-based, a<b<c; the i-th smallest member is never at position j, 1 top, 2 middle, 3 bottom).
Usage: python write_assign_txt.py IN.npy N OUT.txt"""
import sys
from math import comb
import numpy as np
a = np.load(sys.argv[1]); n = int(sys.argv[2]); out = open(sys.argv[3], "w")
assert len(a) == comb(n, 3)
for c in range(2, n):
    for b in range(1, c):
        for x in range(b):
            v = int(a[comb(c, 3) + comb(b, 2) + x]); assert v < 9
            out.write("%d %d %d %dN%d\n" % (x + 1, b + 1, c + 1, v // 3 + 1, v % 3 + 1))
out.close()
