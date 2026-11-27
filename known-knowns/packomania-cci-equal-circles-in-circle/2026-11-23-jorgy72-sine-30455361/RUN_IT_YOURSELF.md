# RUN_IT_YOURSELF.md

Exact commands, run from this package folder in a fresh shell. Needs only Python 3
(standard library).

## The one-command check
sh verify-it-yourself/run_checks.sh
# expected last line: PASS  (a few minutes on a laptop)

## What it does
1. `python3 verify-it-yourself/verify.py object/candidate_n4405.txt`
   - Parses the 4405 centers as exact decimals (no binary float), computes
     r* = min(min_{i<j}|c_i−c_j|/2, 1−max_i|c_i|) at 50 decimal digits.
   - Expected: r* = 0.014193819376049377319011472067507150119907818321175…, table = 0.014190212251,
     margin = 3.607e-06 (need ≥ 1e-11) → PASS.
2. Builds a corrupted copy (one center duplicated onto another → zero pair distance) and checks the
   verifier rejects it (→ FAIL). Guards against a checker that passes everything.

## Rebuilding the object (how-we-built-it/)
The discovery code is in how-we-built-it/ (numpy/scipy needed). In brief:
1. Generate hexagonal truncations of ~4405 points (orientation θ, spacing s, offset):
   see wide_search.py (parameter search, 96,525 evaluations on the raw-truncation
   objective F = min(s/2, 1 − max|p|); grid best θ=0.00 deg, s=0.02835204,
   offset (0.000000, 0.000000), raw margin −1.419e-05; refine best identical to
   the grid best (refine gained 0); random phase best θ=13.09 deg, raw margin −1.554e-05).
2. Regenerate the two rotated basins with make_basins.py (θ=15 and θ=25 at the
   grid-best spacing and offsets; raw −1.419e-05 each — at this row
   orientation carries no signal in the raw evaluator: the top-20 ties
   span θ 0.00–4.75 deg and F = s/2 for every orientation).
3. Deep-polish the best four diverse truncations with smooth_max_polish (polish.py:
   L-BFGS-B on logsumexp(α·overlaps)/α, ratcheting r → feasible r each round).
   The random-phase basin polishes from a raw −1.554e-05 deficit to a certified
   +3.607125049e-06 surplus over the table; the refine best polishes to
   −2.221e-06, below the bar; the theta-25 basin polishes to +2.038e-06,
   a second above-bar file (banked, not bundled).
The exact command history is in how-we-built-it/COMMANDS.txt.

## Re-fetching the record we beat
curl -sS -A "V3R1T4S-recheck" https://packomania.com/cci/txt/radius.txt | awk '$1==4405'
# compare against INDEX.csv / the-record-we-beat/snapshot.txt
