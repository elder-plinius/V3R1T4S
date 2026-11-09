#!/usr/bin/env python3
"""Rebuild the <13,14,15> rank-1644 scheme (stored as format 14x15x13) from LITA's 15x15x15 rank-1977 scheme by three
exact one-slice restrictions, each followed by flat (consensus) absorption with a fixed seed, exactly as the run
of 2026-10-25 built it (rebuild_slice.py for step 1, scanD.py cuts for steps 2 and 3, both not shipped: restrict, then
flat_all(rng=Random(seed), restarts=6), mode rflat, start 0). Needs engine.py and flat.py from this folder
(numpy, python-flint 0.9.0).
Usage: rebuild_chain.py lita_15.json out.json"""
import sys, os, random
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import load_json, save_json, restrict
from flat import flat_all

def vec(n, entries):
    v = [Fraction(0)] * n
    for i, c in entries.items():
        v[i] = Fraction(c)
    return tuple(v)

ones15_m5 = vec(15, {**{i: 1 for i in range(15)}, 7: -5})
STEPS = [  # (axis, e, f, seed)
    (0, ones15_m5, vec(15, {**{i: 1 for i in range(15)}, 0: -1}), 5001),   # -> 14x15x15 1836
    (2, vec(15, {0: 1}), ones15_m5, 1000),                                    # -> 14x15x14 1709 (cut 0 of D1836_ax2)
    (2, vec(14, {2: 1, 7: -1}), vec(14, {2: 1, 10: 1}), 1008),                # -> 14x15x13 1644 (cut 8 of D1709_ax2)
]
S = load_json(sys.argv[1])
print("parent <%d,%d,%d> rank %d" % (S[0], S[1], S[2], len(S[3])), flush=True)
for axis, e, f, seed in STEPS:
    S1 = restrict(S, axis, e, f)
    S, ab = flat_all(S1, rng=random.Random(seed), restarts=6)
    print("axis %d e=%s f=%s: slice -> (%d, %d, %d) rank %d; flat absorption seed %d removed %d -> rank %d"
          % (axis, ",".join(map(str, e)), ",".join(map(str, f)), S1[0], S1[1], S1[2], len(S1[3]), seed, ab, len(S[3])), flush=True)
save_json(S, sys.argv[2], note="rebuild_chain.py from LITA 15x15x15 r1977")
