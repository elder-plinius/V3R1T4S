# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (5, 33)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 528 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.490903793686186209462173767370, attained by vectors 1 and 16 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.490903793686186209462173767370, pair 1-16; difference from the exact method 0.0.
- float64 sanity value 0.4909037936861862, pair 1-16. Largest minus second-largest overlap (exact): 1.1956E-14; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.49101569 from CLAIM.md: 1.118963E-04 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed b627ac48b13f07c546e1e28d888b27f759daf03d430999c6ac10fdfc6de78d05)
- exactly 2dn = 330 finite numbers: PASS (330 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 17; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.4909037936)
- the two exact-precision methods agree: PASS (difference 0.0, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.49090379368618, difference 6.209E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.49101569 minus mu = 1.118963E-04)
- all three methods name the same attaining pair: PASS (1-16)

## Decision
The object for (5, 33) reproduces: exact and 50-digit computations give mu = 0.4909037936861862 on pair 1-16. That matches the claimed 0.49090379368618 and sits 1.118963E-04 below the leaderboard value 0.49101569, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
