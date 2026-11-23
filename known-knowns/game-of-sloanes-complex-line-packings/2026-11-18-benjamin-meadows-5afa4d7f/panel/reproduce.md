# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (7, 25)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 300 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.332068328253993509593155877876, attained by vectors 13 and 19 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.332068328253993509593155877876, pair 13-19; difference from the exact method 0.0.
- float64 sanity value 0.33206832825399357, pair 13-19. Largest minus second-largest overlap (exact): 4.3160E-12; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.33247138 from CLAIM.md: 4.030517E-04 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed 5afa4d7ffef566ee89999ca24b1c10dcb1450cbc032c34c8b3b316e8255ddbf9)
- exactly 2dn = 350 finite numbers: PASS (350 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 18; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.3320683282)
- the two exact-precision methods agree: PASS (difference 0.0, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.33206832825399, difference 3.510E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.33247138 minus mu = 4.030517E-04)
- all three methods name the same attaining pair: PASS (13-19)

## Decision
The object for (7, 25) reproduces: exact and 50-digit computations give mu = 0.3320683282539935 on pair 13-19. That matches the claimed 0.33206832825399 and sits 4.030517E-04 below the leaderboard value 0.33247138, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
