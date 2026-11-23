# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (6, 46)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 1035 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.455410437265652888193858789017, attained by vectors 42 and 45 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.455410437265652888193858789017, pair 42-45; difference from the exact method 1.34e-51.
- float64 sanity value 0.455410437265653, pair 42-45. Largest minus second-largest overlap (exact): 1.0014E-14; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.45560317 from CLAIM.md: 1.927327E-04 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed a35b0cc597adb04c4b61fae188a9e30d0e9ada055da97508cc91c0971e4d2715)
- exactly 2dn = 552 finite numbers: PASS (552 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 17; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.4554104372)
- the two exact-precision methods agree: PASS (difference 1.34e-51, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.45541043726565, difference 2.888E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.45560317 minus mu = 1.927327E-04)
- all three methods name the same attaining pair: PASS (42-45)

## Decision
The object for (6, 46) reproduces: exact and 50-digit computations give mu = 0.4554104372656528 on pair 42-45. That matches the claimed 0.45541043726565 and sits 1.927327E-04 below the leaderboard value 0.45560317, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
