# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (3, 38)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 703 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.771884153294935269055505910059, attained by vectors 9 and 12 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.771884153294935269055505910059, pair 9-12; difference from the exact method 1.34e-51.
- float64 sanity value 0.7718841532949353, pair 9-12. Largest minus second-largest overlap (exact): 4.9103E-15; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.77189089 from CLAIM.md: 6.736705E-06 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed a92052bf04a83b879bb98e662333aa98651f5a87c1b154b63d7241d107625f8f)
- exactly 2dn = 228 finite numbers: PASS (228 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 18; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.7718841532)
- the two exact-precision methods agree: PASS (difference 1.34e-51, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.77188415329493, difference 5.269E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.77189089 minus mu = 6.736705E-06)
- all three methods name the same attaining pair: PASS (9-12)

## Decision
The object for (3, 38) reproduces: exact and 50-digit computations give mu = 0.7718841532949352 on pair 9-12. That matches the claimed 0.77188415329493 and sits 6.736705E-06 below the leaderboard value 0.77189089, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
