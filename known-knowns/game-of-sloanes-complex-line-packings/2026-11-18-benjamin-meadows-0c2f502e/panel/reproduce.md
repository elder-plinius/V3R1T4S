# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (5, 32)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 496 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.486814719985448945730525054244, attained by vectors 9 and 17 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.486814719985448945730525054244, pair 9-17; difference from the exact method 6.68e-52.
- float64 sanity value 0.48681471998544895, pair 9-17. Largest minus second-largest overlap (exact): 6.1129E-16; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.48688165 from CLAIM.md: 6.693001E-05 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed 0c2f502eea61853ec7affdb883fb3f628b7c64c22703cb725116b15f37784914)
- exactly 2dn = 320 finite numbers: PASS (320 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 18; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.4868147199)
- the two exact-precision methods agree: PASS (difference 6.68e-52, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.48681471998544, difference 8.946E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.48688165 minus mu = 6.693001E-05)
- all three methods name the same attaining pair: PASS (9-17)

## Decision
The object for (5, 32) reproduces: exact and 50-digit computations give mu = 0.4868147199854489 on pair 9-17. That matches the claimed 0.48681471998544 and sits 6.693001E-05 below the leaderboard value 0.48688165, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
