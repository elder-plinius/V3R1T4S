# RUN_IT_YOURSELF.md

Exact commands, run from this package folder in a fresh shell. Needs only Python 3
(standard library).

## The one-command check
sh verify-it-yourself/run_checks.sh
# expected last line: PASS  (a few minutes on a laptop)

## What it does
1. `python3 verify-it-yourself/verify.py object/candidate_n4315.txt`
   - Parses the 4315 centers as exact decimals (no binary float), computes
     r* = min(min_{i<j}|c_i−c_j|/2, 1−max_i|c_i|) at 50 decimal digits.
   - Expected: r* = 0.01432454777069287128759443799585792968662…, table = 0.014323541476018172725671907488,
     margin = 1.006294675e-06 (need ≥ 1e-11) → PASS.
2. Builds a corrupted copy (one center duplicated onto another → zero pair distance) and checks the
   verifier rejects it (→ FAIL). Guards against a checker that passes everything.

## Rebuilding the object (how-we-built-it/)
The discovery code is in how-we-built-it/ (numpy/scipy needed). In brief:
1. Generate hexagonal truncations of ~4315 points (orientation θ, spacing s, offset):
   see wide_search.py (parameter search, 96,525 evaluations on the raw-truncation
   objective F = min(s/2, 1 − max|p|); best raw truncation θ=0 deg, s=0.02861557,
   offset (0.011446, 0), raw margin −1.576e-05).
2. Regenerate the two rotated basins with make_basins.py (θ=15 and θ=25 at the
   grid-best spacing and offsets; raw −5.721e-04 and −8.508e-04 — at this row
   orientation carries signal, unlike neighbouring rows).
3. Deep-polish the best four diverse truncations with smooth_max_polish (polish.py:
   L-BFGS-B on logsumexp(α·overlaps)/α, ratcheting r → feasible r each round).
   The best (the grid best, theta 0 deg basin) polishes from a raw −1.576e-05
   deficit to a certified +1.006294675e-06 surplus over the table; the random
   best (theta 8.52 deg) also clears the bar at +9.735e-07.
The exact command history is in how-we-built-it/COMMANDS.txt.

## Re-fetching the record we beat
curl -sS -A "V3R1T4S-recheck" https://packomania.com/cci/txt/radius.txt | awk '$1==4315'
# compare against INDEX.csv / the-record-we-beat/snapshot.txt
