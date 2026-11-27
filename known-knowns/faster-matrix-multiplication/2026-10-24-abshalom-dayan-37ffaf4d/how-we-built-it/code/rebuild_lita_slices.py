#!/usr/bin/env python3
"""General form of rebuild_16x16x17.py (not shipped) for any odd N: from LITA's N x N x N scheme, two exact one-slice steps.

Step 1 (axis 0, rows of A and C): e = star, f = e_0, then exact 2-reductions -> <N-1,N,N>.
Step 2 (axis 1, columns of A / rows of B): e = e_0, f = star, then exact 2-reductions -> <N-1,N-1,N>.
star = (1,...,1, -(N-5)/2 at index (N-1)/2, 1,...,1)   (N = 17 gives rebuild_16x16x17.py, not shipped, exactly).
Usage: rebuild_lita_slices.py lita_N.json out_step1.json out_step2.json
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import load_json, save_json, restrict, absorb_all
from fractions import Fraction as F

src, dst1, dst2 = sys.argv[1], sys.argv[2], sys.argv[3]
S = load_json(src)
N = S[0]
assert S[:3] == (N, N, N) and N % 2 == 1, "expected a cubic odd-N LITA scheme"
print("input", S[:3], "rank", len(S[3]))
t0 = time.time()
star = tuple(F(-(N - 5) // 2) if i == (N - 1) // 2 else F(1) for i in range(N))
unit = tuple(F(int(i == 0)) for i in range(N))
S1 = restrict(S, 0, star, unit)
print("step 1: slice axis 0 ->", S1[:3], "rank", len(S1[3]))
S1, ab = absorb_all(S1)
print("step 1: absorbed", ab, "-> rank", len(S1[3]), "(%.0fs)" % (time.time() - t0))
save_json(S1, dst1, note="rebuild_lita_slices.py step 1 from LITA %dx%dx%d r%d" % (N, N, N, len(S[3])))
S2 = restrict(S1, 1, unit, star)
print("step 2: slice axis 1 ->", S2[:3], "rank", len(S2[3]))
S2, ab = absorb_all(S2)
print("step 2: absorbed", ab, "-> rank", len(S2[3]), "(%.0fs)" % (time.time() - t0))
save_json(S2, dst2, note="rebuild_lita_slices.py step 2 from LITA %dx%dx%d r%d" % (N, N, N, len(S[3])))
print("wrote", dst1, dst2)
