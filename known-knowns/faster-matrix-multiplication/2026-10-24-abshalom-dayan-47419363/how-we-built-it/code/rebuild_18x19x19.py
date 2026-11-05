#!/usr/bin/env python3
"""Rebuild the <18,19,19> scheme from LITA's 19x19x19 rank-3633 scheme in one exact step.

Slice on axis 0 (rows of A and C): e = (1,1,1,1,1,1,1,1,1,-7,1,1,1,1,1,1,1,1,1), f = e_0; then exact 2-reductions.
(The same construction as step 1 of rebuild_16x16x17.py, with N = 19 instead of 17.)
Usage: rebuild_18x19x19.py lita_19_r3633.json out.json   (the JSON made by convert.py from LITA's npz)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import load_json, save_json, restrict, absorb_all
from fractions import Fraction as F

src, dst = sys.argv[1], sys.argv[2]
S = load_json(src)
assert S[:3] == (19, 19, 19) and len(S[3]) == 3633, "expected LITA 19x19x19 rank 3633"
star = tuple(F(-7) if i == 9 else F(1) for i in range(19))
unit = tuple(F(int(i == 0)) for i in range(19))
S1 = restrict(S, 0, star, unit)
print("slice axis 0 ->", S1[:3], "rank", len(S1[3]), flush=True)
S1, ab = absorb_all(S1)
print("absorbed", ab, "-> rank", len(S1[3]), flush=True)
save_json(S1, dst, note="rebuild_18x19x19.py from LITA 19x19x19 r3633")
print("wrote", dst)
