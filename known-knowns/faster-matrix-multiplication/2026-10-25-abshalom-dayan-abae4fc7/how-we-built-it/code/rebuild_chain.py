#!/usr/bin/env python3
"""Rebuild a scheme from a published parent by a chain of exact one-slice restrictions, each followed by flat
(consensus) absorption with a fixed seed. Needs engine.py and flat.py from this folder (numpy, python-flint 0.9.0).
Usage: rebuild_chain.py parent.json out.json STEP [STEP ...]
  STEP = axis/e/f/seed/restarts   with e and f as comma-separated integers, for example
         0/1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1/-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1/5001/6
Axis 0 slices the row index i of A and C, axis 1 the index j shared by A and B, axis 2 the column index l of B and C.
For each step the program prints the rank after the slice and after absorption."""
import sys, os, random
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import load_json, save_json, restrict
from flat import flat_all

src, dst, steps = sys.argv[1], sys.argv[2], sys.argv[3:]
S = load_json(src)
print("parent <%d,%d,%d> rank %d" % (S[0], S[1], S[2], len(S[3])), flush=True)
notes = []
for k, st in enumerate(steps, 1):
    axis, es, fs, seed, restarts = st.split("/")
    axis, seed, restarts = int(axis), int(seed), int(restarts)
    e = tuple(Fraction(x) for x in es.split(","))
    f = tuple(Fraction(x) for x in fs.split(","))
    S1 = restrict(S, axis, e, f)
    print("step %d: slice axis %d with e=%s f=%s -> (%d, %d, %d) rank %d" % (k, axis, es, fs, S1[0], S1[1], S1[2], len(S1[3])), flush=True)
    S, ab = flat_all(S1, rng=random.Random(seed), restarts=restarts)
    print("step %d: flat absorption (seed %d, restarts %d) removed %d -> rank %d" % (k, seed, restarts, ab, len(S[3])), flush=True)
    notes.append(st)
save_json(S, dst, note="rebuild_chain steps " + " ".join(notes))
