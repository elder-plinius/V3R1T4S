# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (6, 47)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 1081 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.459047847717500093477702391468, attained by vectors 18 and 24 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.459047847717500093477702391468, pair 18-24; difference from the exact method 6.68e-52.
- float64 sanity value 0.4590478477175001, pair 18-24. Largest minus second-largest overlap (exact): 2.4732E-15; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.45924802 from CLAIM.md: 2.001723E-04 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed c8fa32286e01682d603e52dd8146c7f8ed6b01be7f3e1a171344c74a643ff8eb)
- exactly 2dn = 564 finite numbers: PASS (564 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 17; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.4590478477)
- the two exact-precision methods agree: PASS (difference 6.68e-52, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.45904784771750, difference 9.348E-17 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.45924802 minus mu = 2.001723E-04)
- all three methods name the same attaining pair: PASS (18-24)

## Decision
The object for (6, 47) reproduces: exact and 50-digit computations give mu = 0.4590478477175000 on pair 18-24. That matches the claimed 0.45904784771750 and sits 2.001723E-04 below the leaderboard value 0.45924802, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
