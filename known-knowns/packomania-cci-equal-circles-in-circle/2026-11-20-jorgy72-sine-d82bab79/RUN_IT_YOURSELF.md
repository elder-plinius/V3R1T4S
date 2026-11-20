# RUN_IT_YOURSELF.md

Exact commands, run from this package folder in a fresh shell. Needs only Python 3
(standard library).

## The one-command check
sh verify-it-yourself/run_checks.sh
# expected last line: PASS  (a few minutes on a laptop)

## What it does
1. `python3 verify-it-yourself/verify.py object/candidate_n4357.txt`
   - Parses the 4357 centers as exact decimals (no binary float), computes
     r* = min(min_{i<j}|c_i−c_j|/2, 1−max_i|c_i|) at 50 decimal digits.
   - Expected: r* = 0.01426010900644796452099252854563731797493935762124…, table = 0.014255170553446144330034824715,
     margin = 4.938e-06 (need ≥ 1e-11) → PASS.
2. Builds a corrupted copy (one center duplicated onto another → zero pair distance) and checks the
   verifier rejects it (→ FAIL). Guards against a checker that passes everything.

## Rebuilding the object (how-we-built-it/)
The discovery code is in how-we-built-it/ (numpy/scipy needed). In brief:
1. Generate hexagonal truncations of ~4357 points (orientation θ, spacing s, offset):
   see wide_search.py (parameter search, 96,525 evaluations on the raw-truncation
   objective F = min(s/2, 1 − max|p|); grid best θ=7.75 deg, s=0.02847898,
   offset (0.000000, 0.017087), raw margin −1.568e-05; refine best identical to
   the grid best (refine gained 0); random phase best θ=1.09 deg, raw margin −1.609e-05).
2. Regenerate the two rotated basins with make_basins.py (θ=15 and θ=25 at the
   grid-best spacing and offsets; raw −8.256e-04 and −1.114e-03 — at this row
   orientation carries little signal in the raw evaluator: the top-20 ties
   span θ 7.75–22.25 deg).
3. Deep-polish the best four diverse truncations with smooth_max_polish (polish.py:
   L-BFGS-B on logsumexp(α·overlaps)/α, ratcheting r → feasible r each round).
   The random-phase basin polishes from a raw −1.609e-05 deficit to a certified
   +4.93845300182e-06 surplus over the table; the refine best polishes to
   −2.348e-07, just below the bar; the theta-15 basin recovers +8.19e-04
   to −6.908e-06.
The exact command history is in how-we-built-it/COMMANDS.txt.

## Re-fetching the record we beat
curl -sS -A "V3R1T4S-recheck" https://packomania.com/cci/txt/radius.txt | awk '$1==4357'
# compare against INDEX.csv / the-record-we-beat/snapshot.txt
