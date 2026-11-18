# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (3, 49)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 1176 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.801400292907831448549195159200, attained by vectors 12 and 29 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.801400292907831448549195159200, pair 12-29; difference from the exact method 2.67e-51.
- float64 sanity value 0.8014002929078317, pair 12-29. Largest minus second-largest overlap (exact): 2.1716E-14; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.80155093 from CLAIM.md: 1.506371E-04 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed 4c41c7c0e9e16eed48aef8079a6c5026221bbc3864fe2bf0c4e988b60efca4a6)
- exactly 2dn = 294 finite numbers: PASS (294 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 16; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.8014002929)
- the two exact-precision methods agree: PASS (difference 2.67e-51, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.80140029290783, difference 1.449E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.80155093 minus mu = 1.506371E-04)
- all three methods name the same attaining pair: PASS (12-29)

## Decision
The object for (3, 49) reproduces: exact and 50-digit computations give mu = 0.8014002929078314 on pair 12-29. That matches the claimed 0.80140029290783 and sits 1.506371E-04 below the leaderboard value 0.80155093, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
