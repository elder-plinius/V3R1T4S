# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (6, 38)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 703 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.416750437383911316847865823800, attained by vectors 11 and 12 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.416750437383911316847865823800, pair 11-12; difference from the exact method 6.68e-52.
- float64 sanity value 0.4167504373839115, pair 11-12. Largest minus second-largest overlap (exact): 3.1914E-12; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.41682055 from CLAIM.md: 7.011262E-05 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed c74eab6fe1a84859d0f3ff0027bddbc084891b8fe4a6c5689e3065e9017a169e)
- exactly 2dn = 456 finite numbers: PASS (456 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 17; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.4167504373)
- the two exact-precision methods agree: PASS (difference 6.68e-52, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.41675043738391, difference 1.317E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.41682055 minus mu = 7.011262E-05)
- all three methods name the same attaining pair: PASS (11-12)

## Decision
The object for (6, 38) reproduces: exact and 50-digit computations give mu = 0.4167504373839113 on pair 11-12. That matches the claimed 0.41675043738391 and sits 7.011262E-05 below the leaderboard value 0.41682055, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
