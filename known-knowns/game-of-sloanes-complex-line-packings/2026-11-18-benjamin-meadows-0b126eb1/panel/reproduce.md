# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (4, 28)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 378 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.577117059925903874523452603022, attained by vectors 2 and 17 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.577117059925903874523452603022, pair 2-17; difference from the exact method 1.34e-51.
- float64 sanity value 0.5771170599259039, pair 2-17. Largest minus second-largest overlap (exact): 3.8421E-15; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.57711826 from CLAIM.md: 1.200074E-06 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed 0b126eb16a321d7691a921464458ceed7b9113cc00660376208dfee443df7c72)
- exactly 2dn = 224 finite numbers: PASS (224 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 17; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.5771170599)
- the two exact-precision methods agree: PASS (difference 1.34e-51, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.57711705992590, difference 3.875E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.57711826 minus mu = 1.200074E-06)
- all three methods name the same attaining pair: PASS (2-17)

## Decision
The object for (4, 28) reproduces: exact and 50-digit computations give mu = 0.5771170599259038 on pair 2-17. That matches the claimed 0.57711705992590 and sits 1.200074E-06 below the leaderboard value 0.57711826, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
