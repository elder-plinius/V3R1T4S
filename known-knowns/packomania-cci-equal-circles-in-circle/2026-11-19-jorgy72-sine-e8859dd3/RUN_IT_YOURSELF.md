# RUN_IT_YOURSELF.md

Exact commands, run from this package folder in a fresh shell. Needs only Python 3
(standard library).

## The one-command check
sh verify-it-yourself/run_checks.sh
# expected last line: PASS  (a few minutes on a laptop)

## What it does
1. `python3 verify-it-yourself/verify.py object/candidate_n4345.txt`
   - Parses the 4345 centers as exact decimals (no binary float), computes
     r* = min(min_{i<j}|c_i−c_j|/2, 1−max_i|c_i|) at 50 decimal digits.
   - Expected: r* = 0.01427701232602575290682290312897756077321…, table = 0.014273228279866076598567467525,
     margin = 3.784e-06 (need ≥ 1e-11) → PASS.
2. Builds a corrupted copy (one center duplicated onto another → zero pair distance) and checks the
   verifier rejects it (→ FAIL). Guards against a checker that passes everything.

## Rebuilding the object (how-we-built-it/)
The discovery code is in how-we-built-it/ (numpy/scipy needed). In brief:
1. Generate hexagonal truncations of ~4345 points (orientation θ, spacing s, offset):
   see wide_search.py (parameter search, 96,525 evaluations on the raw-truncation
   objective F = min(s/2, 1 − max|p|); grid best θ=11.50 deg, s=0.02851791,
   offset (0.011407, 0.011407), raw margin −1.427e-05; refine best θ=10.63 deg,
   raw margin −1.347e-05; random phase best θ=18.65 deg, raw margin −1.437e-05).
2. Regenerate the two rotated basins with make_basins.py (θ=15 and θ=25 at the
   grid-best spacing and offsets; raw −3.382e-04 and −5.662e-04 — at this row
   orientation carries little signal in the raw evaluator: the top-20 ties
   span θ 11.5–18.5 deg).
3. Deep-polish the best four diverse truncations with smooth_max_polish (polish.py:
   L-BFGS-B on logsumexp(α·overlaps)/α, ratcheting r → feasible r each round).
   The theta-25 basin polishes from a raw −5.662e-04 deficit to a certified
   +3.78404615968e-06 surplus over the table; the refine best also clears the
   bar at +1.71342783757e-06.
The exact command history is in how-we-built-it/COMMANDS.txt.

## Re-fetching the record we beat
curl -sS -A "V3R1T4S-recheck" https://packomania.com/cci/txt/radius.txt | awk '$1==4345'
# compare against INDEX.csv / the-record-we-beat/snapshot.txt
