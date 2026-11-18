# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (4, 29)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 406 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.577329820586956761543589370375, attained by vectors 12 and 17 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.577329820586956761543589370375, pair 12-17; difference from the exact method 1.34e-51.
- float64 sanity value 0.5773298205869569, pair 12-17. Largest minus second-largest overlap (exact): 6.0105E-13; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.57733882 from CLAIM.md: 8.999413E-06 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed c4aa38eb11e27923235073314ff87c88ac79524317ff5b9a7fee611869361a6e)
- exactly 2dn = 232 finite numbers: PASS (232 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 17; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.5773298205)
- the two exact-precision methods agree: PASS (difference 1.34e-51, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.57732982058695, difference 6.762E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.57733882 minus mu = 8.999413E-06)
- all three methods name the same attaining pair: PASS (12-17)

## Decision
The object for (4, 29) reproduces: exact and 50-digit computations give mu = 0.5773298205869567 on pair 12-17. That matches the claimed 0.57732982058695 and sits 8.999413E-06 below the leaderboard value 0.57733882, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
