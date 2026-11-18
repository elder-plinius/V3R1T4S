# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (3, 24)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 276 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.719064770737380696322709458993, attained by vectors 0 and 10 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.719064770737380696322709458993, pair 0-10; difference from the exact method 1.34e-51.
- float64 sanity value 0.7190647707373807, pair 0-10. Largest minus second-largest overlap (exact): 2.1536E-15; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.71909565 from CLAIM.md: 3.087926E-05 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed 1c52b4afe1001f0b48df54d0650a323ac00bafbeb3d9643cf175895950d61c88)
- exactly 2dn = 144 finite numbers: PASS (144 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 18; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.7190647707)
- the two exact-precision methods agree: PASS (difference 1.34e-51, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.71906477073738, difference 6.963E-16 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.71909565 minus mu = 3.087926E-05)
- all three methods name the same attaining pair: PASS (0-10)

## Decision
The object for (3, 24) reproduces: exact and 50-digit computations give mu = 0.7190647707373806 on pair 0-10. That matches the claimed 0.71906477073738 and sits 3.087926E-05 below the leaderboard value 0.71909565, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
