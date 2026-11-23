# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (3, 41)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 820 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.778477832643142136069829949549, attained by vectors 22 and 29 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.778477832643142136069829949549, pair 22-29; difference from the exact method 0.0.
- float64 sanity value 0.7784778326431422, pair 22-29. Largest minus second-largest overlap (exact): 2.3935E-15; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.77848806 from CLAIM.md: 1.022736E-05 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed 07b61665a7df72affdb89b3bc1770541c6ad1e57b0fd95aadb476f8cf215bbfd)
- exactly 2dn = 246 finite numbers: PASS (246 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 21; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.7784778326)
- the two exact-precision methods agree: PASS (difference 0.0, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.77847783264314, difference 2.136E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.77848806 minus mu = 1.022736E-05)
- all three methods name the same attaining pair: PASS (22-29)

## Decision
The object for (3, 41) reproduces: exact and 50-digit computations give mu = 0.7784778326431421 on pair 22-29. That matches the claimed 0.77847783264314 and sits 1.022736E-05 below the leaderboard value 0.77848806, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
