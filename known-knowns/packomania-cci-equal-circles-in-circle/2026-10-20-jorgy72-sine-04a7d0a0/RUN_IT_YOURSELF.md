# RUN_IT_YOURSELF.md

Exact commands, run from this package folder in a fresh shell. Needs only Python 3
(standard library).

## The one-command check
sh verify-it-yourself/run_checks.sh
# expected last line: PASS  (under a minute on a laptop)

## What it does
1. `python3 verify-it-yourself/verify.py object/candidate_n3949.txt`
   - Parses the 3949 centers as exact decimals (no binary float), computes
     r* = min(min_{i<j}|c_i−c_j|/2, 1−max_i|c_i|) at 50 decimal digits.
   - Expected: r* = 0.01496783530958494442…, table = 0.014965462848801963307763269064,
     margin = 2.372e-06 (need ≥ 1e-11) → PASS.
2. Builds a corrupted copy (one center duplicated → zero pair distance) and checks the
   verifier rejects it (→ FAIL). Guards against a checker that passes everything.

## Rebuilding the object (how-we-built-it/)
The discovery code is in how-we-built-it/ (numpy/scipy needed). In brief, from the
lens's REPRODUCE notes:
1. Generate hexagonal truncations of ~3949 points (orientation θ, spacing s, offset):
   see how-we-built-it/gen.py / how-we-built-it/a2search.py (parameter search, 20k evaluations on the raw-truncation
   objective F = min(s/2, 1 − max|p|); best raw truncation θ=12.863°, s=0.02987721).
2. Jam each truncation with the overlap-relaxation in how-we-built-it/jam.py.
3. Deep-polish the best with smooth_max_polish (how-we-built-it/polish.py: L-BFGS-B on
   logsumexp(α·overlaps)/α, ratcheting r → feasible r each round), then aggressive
   re-polish (how-we-built-it/batch_polish.py, how-we-built-it/squeeze.py) → +2.372e-06.
The exact command history is in how-we-built-it/COMMANDS.txt.

## Re-fetching the record we beat
curl -sS -A "V3R1T4S-recheck" https://packomania.com/cci/txt/radius.txt | awk '$1==3949'
# compare against INDEX.csv / the-record-we-beat/snapshot.txt
