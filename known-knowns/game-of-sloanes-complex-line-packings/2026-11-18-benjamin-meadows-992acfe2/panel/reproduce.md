# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (7, 19)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 171 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.308836400201367998528749847692, attained by vectors 4 and 10 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.308836400201367998528749847692, pair 4-10; difference from the exact method 0.0.
- float64 sanity value 0.3088364002013681, pair 4-10. Largest minus second-largest overlap (exact): 1.6312E-13; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.30884718 from CLAIM.md: 1.077980E-05 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed 992acfe275d9130797743c01024fb7741a1317458a47a32d45a6918de64e7a87)
- exactly 2dn = 266 finite numbers: PASS (266 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 17; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.3088364002)
- the two exact-precision methods agree: PASS (difference 0.0, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.30883640020136, difference 7.999E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.30884718 minus mu = 1.077980E-05)
- all three methods name the same attaining pair: PASS (4-10)

## Decision
The object for (7, 19) reproduces: exact and 50-digit computations give mu = 0.3088364002013679 on pair 4-10. That matches the claimed 0.30883640020136 and sits 1.077980E-05 below the leaderboard value 0.30884718, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
