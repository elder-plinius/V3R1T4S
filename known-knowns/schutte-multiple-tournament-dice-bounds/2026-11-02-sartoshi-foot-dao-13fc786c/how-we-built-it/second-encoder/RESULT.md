# Second, independent encoder: result (2026-11-03)

**Result: AGREE. No disagreement anywhere.** Our encoder (ours/, byte-identical to the certificate's certify/encoder/) and a second encoder
written from the paper alone (enc2/) give the same answer on every case tried, and both match a direct check of the definition.

## What was done
- enc2/enc2.py was written by a fresh Claude Opus 5.5 subagent that was told not to open any of our files and worked only from
  arXiv:2604.08790v1 (Definitions 2.1 and 2.2, quoted in enc2/NOTES.md). It writes its own at-most counters (no pysat.card) and uses its
  own auxiliary variables; only the arc-variable numbering was fixed in advance so the two can be compared. Its own self-test
  (enc2/selftest.out) ends PASS: least n is 3 for (1,1), 7 for (1,2) (the classical values), 4 for (2,2), 6 for (2,3), and
  (2,4,9) UNSAT, (2,4,10) SAT, i.e. f(2,4) = 10 with no normal form at all.
- compare.py (written by the thread session, which sees both) ran on ser5 in Docker (python:3.12-slim, python-sat 1.9.dev17,
  CaDiCaL 1.9.5, 8 GB, 1 CPU each, two containers): out_A.txt (phase A, 90 s) and out_BC.txt (phases B and C, 191 s). About
  0.1 CPU-hour of the 2 CPU-hour cap.

## Checks and outcomes
- **Small cells, every level-1 cube** (13 cells: (1,1,3) (1,2,6) (1,2,7) (2,2,4) (2,2,5) (2,3,6..8) (2,4,9) (2,4,10) (3,2,4) (3,3,6)
  (3,3,7); 379 cubes, 92 SAT): the same SAT/UNSAT on every cube. Each cell's answer (some cube of ours SAT) equals enc2's plain
  formula with no normal form, so on these cells the normal form also loses nothing. (2,4,9): all cubes UNSAT on both sides and enc2
  plain UNSAT; (2,4,10): SAT on both, so f(2,4) = 10 by both encoders.
- **Same set of solutions, not just the same answer**: 12,813 full arc assignments (each side's models, their 1-3 arc flips, random
  ones) were fed to both formulas as unit clauses. Every time, both formulas and the direct check (checker.py: property S_k and the
  cube's constraints read off the matrices) gave the same answer.
- **Real cells, seeded samples** (seed 20261103): 30 level-1 cubes of (2,5,13) and 20 quick level-1 leaves of (3,6,12), the cell of
  the claim. All 50 UNSAT on both encoders.
- **Upper-bound witnesses**: the (2,5,14) and (3,6,13) witnesses satisfy both formulas, and each of their 182 and 234 single-arc
  flips gets the same answer from both formulas and the direct check (37 and 97 of the flips still satisfy them).

## What this does and does not show
It is strong evidence that our formula says exactly what Definitions 2.1/2.2 plus the cube's constraints say, at the real sizes as
well as small ones. It does not re-check the full (3,6,12) certificate with the second encoder (about 27 CPU-hours), nor the
normal-form arguments beyond the small cells. enc2's notes flag one reading point: for n <= k the literal definition is vacuous;
it follows the paper's proof of Proposition 2.2 (n <= k is not S_k). No cell used here has n <= k.

To rerun: put a copy of certify/encoder/ in ours/, then `python -I compare.py` (needs python-sat 1.9.dev17). Last line AGREE.
