# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (7, 20)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 190 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.313076140781610781371986787441, attained by vectors 7 and 12 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.313076140781610781371986787441, pair 7-12; difference from the exact method 0.0.
- float64 sanity value 0.3130761407816107, pair 7-12. Largest minus second-largest overlap (exact): 6.5677E-15; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.31334596 from CLAIM.md: 2.698192E-04 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed bfca650c9a2fa6b2df28ba36c2ff0607705e5b28f8287beb04f3d209b9d51c6d)
- exactly 2dn = 280 finite numbers: PASS (280 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 18; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.3130761407)
- the two exact-precision methods agree: PASS (difference 0.0, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.31307614078161, difference 7.814E-16 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.31334596 minus mu = 2.698192E-04)
- all three methods name the same attaining pair: PASS (7-12)

## Decision
The object for (7, 20) reproduces: exact and 50-digit computations give mu = 0.3130761407816107 on pair 7-12. That matches the claimed 0.31307614078161 and sits 2.698192E-04 below the leaderboard value 0.31334596, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
