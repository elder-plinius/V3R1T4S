#!/usr/bin/env python3
"""Rebuild a one-slice child of a LITA cube scheme (here 15x15x15 rank 1977 -> 14x15x15): one exact one-slice restriction of the row
index i of A and C (axis 0) with the direction pair (e, f), then flat (consensus) absorption with a fixed seed.
Needs engine.py and flat.py from this folder (numpy, python-flint 0.9.0).
Usage: rebuild_slice.py lita.json out.json e f seed [restarts] [mode] [start]
  e, f: N comma-separated integers;  e.g. the claimed object is rebuilt with the arguments in ../REPRODUCE.md"""
import sys, os, random
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import load_json, save_json, restrict
from flat import flat_all

src, dst = sys.argv[1], sys.argv[2]
e = tuple(Fraction(x) for x in sys.argv[3].split(","))
f = tuple(Fraction(x) for x in sys.argv[4].split(","))
seed = int(sys.argv[5])
restarts = int(sys.argv[6]) if len(sys.argv) > 6 else 6
mode = sys.argv[7] if len(sys.argv) > 7 else "rflat"
start = int(sys.argv[8]) if len(sys.argv) > 8 else 0
S0 = load_json(src)
print("parent <%d,%d,%d> rank %d" % (S0[0], S0[1], S0[2], len(S0[3])), flush=True)
S1 = restrict(S0, 0, e, f)
print("slice axis 0 with e=%s f=%s -> (%d, %d, %d) rank %d" % (",".join(map(str, e)), ",".join(map(str, f)),
                                                               S1[0], S1[1], S1[2], len(S1[3])), flush=True)
S2, ab = flat_all(S1, rng=random.Random(seed), restarts=restarts, mode=mode, start=start)
print("flat absorption removed %d -> rank %d" % (ab, len(S2[3])), flush=True)
save_json(S2, dst, note="rebuild_slice e=%s f=%s seed %d restarts %d mode %s start %d"
          % (",".join(map(str, e)), ",".join(map(str, f)), seed, restarts, mode, start))
