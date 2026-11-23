# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (7, 30)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 435 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.345227045418659395074694864104, attained by vectors 3 and 15 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.345227045418659395074694864104, pair 3-15; difference from the exact method 1.34e-51.
- float64 sanity value 0.3452270454186595, pair 3-15. Largest minus second-largest overlap (exact): 1.8940E-14; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.34639121 from CLAIM.md: 1.164165E-03 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed c3a325a490a3c4a7ae4c26f80bfbe524b4f909dba875780b44f0591085da686e)
- exactly 2dn = 420 finite numbers: PASS (420 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 17; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.3452270454)
- the two exact-precision methods agree: PASS (difference 1.34e-51, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.34522704541865, difference 9.395E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.34639121 minus mu = 1.164165E-03)
- all three methods name the same attaining pair: PASS (3-15)

## Decision
The object for (7, 30) reproduces: exact and 50-digit computations give mu = 0.3452270454186593 on pair 3-15. That matches the claimed 0.34522704541865 and sits 1.164165E-03 below the leaderboard value 0.34639121, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
