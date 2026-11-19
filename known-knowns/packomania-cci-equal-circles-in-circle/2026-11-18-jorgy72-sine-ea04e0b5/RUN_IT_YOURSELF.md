# RUN_IT_YOURSELF.md

Exact commands, run from this package folder in a fresh shell. Needs only Python 3
(standard library).

## The one-command check
sh verify-it-yourself/run_checks.sh
# expected last line: PASS  (a few minutes on a laptop)

## What it does
1. `python3 verify-it-yourself/verify.py object/candidate_n4339.txt`
   - Parses the 4339 centers as exact decimals (no binary float), computes
     r* = min(min_{i<j}|c_i−c_j|/2, 1−max_i|c_i|) at 50 decimal digits.
   - Expected: r* = 0.01428914037842894912706195794112189732227…, table = 0.014278996448020329132467169733,
     margin = 1.014e-05 (need ≥ 1e-11) → PASS.
2. Builds a corrupted copy (one center duplicated onto another → zero pair distance) and checks the
   verifier rejects it (→ FAIL). Guards against a checker that passes everything.

## Rebuilding the object (how-we-built-it/)
The discovery code is in how-we-built-it/ (numpy/scipy needed). In brief:
1. Generate hexagonal truncations of ~4339 points (orientation θ, spacing s, offset):
   see wide_search.py (parameter search, 96,525 evaluations on the raw-truncation
   objective F = min(s/2, 1 − max|p|); best raw truncation θ=29.25 deg, s=0.02853229,
   offset (0.011413, 0), raw margin −1.285e-05; random phase best θ=0.24 deg,
   raw margin −1.209e-05 — the best raw floor of any rotation night).
2. Regenerate the two rotated basins with make_basins.py (θ=15 and θ=25 at the
   grid-best spacing and offsets; raw −1.002e-03 and −3.570e-04 — at this row
   orientation carries little signal in the raw evaluator: the top-20 ties
   span θ 0–29.25 deg).
3. Deep-polish the best four diverse truncations with smooth_max_polish (polish.py:
   L-BFGS-B on logsumexp(α·overlaps)/α, ratcheting r → feasible r each round).
   The best (the grid best, theta 29.25 deg basin) polishes from a raw −1.285e-05
   deficit to a certified +1.014393041e-05 surplus over the table; the theta-25
   basin also clears the bar at +8.345155687e-06.
The exact command history is in how-we-built-it/COMMANDS.txt.

## Re-fetching the record we beat
curl -sS -A "V3R1T4S-recheck" https://packomania.com/cci/txt/radius.txt | awk '$1==4339'
# compare against INDEX.csv / the-record-we-beat/snapshot.txt
