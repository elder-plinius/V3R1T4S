# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (6, 24)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 276 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.369605367639093155993976166451, attained by vectors 6 and 21 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.369605367639093155993976166451, pair 6-21; difference from the exact method 6.68e-52.
- float64 sanity value 0.36960536763909324, pair 6-21. Largest minus second-largest overlap (exact): 3.3952E-14; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.36998252 from CLAIM.md: 3.771524E-04 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed 8456e23556911891ea6d3ccc7c3095bda2bd3d96b3f7ddd4bfd6fec8636f67ee)
- exactly 2dn = 288 finite numbers: PASS (288 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 18; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.3696053676)
- the two exact-precision methods agree: PASS (difference 6.68e-52, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.36960536763909, difference 3.156E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.36998252 minus mu = 3.771524E-04)
- all three methods name the same attaining pair: PASS (6-21)

## Decision
The object for (6, 24) reproduces: exact and 50-digit computations give mu = 0.3696053676390931 on pair 6-21. That matches the claimed 0.36960536763909 and sits 3.771524E-04 below the leaderboard value 0.36998252, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
