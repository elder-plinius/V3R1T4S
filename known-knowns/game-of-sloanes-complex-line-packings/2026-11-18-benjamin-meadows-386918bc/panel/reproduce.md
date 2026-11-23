# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (5, 38)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 703 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.499980998839978899992989845882, attained by vectors 2 and 7 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.499980998839978899992989845882, pair 2-7; difference from the exact method 6.68e-52.
- float64 sanity value 0.4999809988399789, pair 2-7. Largest minus second-largest overlap (exact): 3.9011E-11; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.49998890 from CLAIM.md: 7.901160E-06 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed 386918bcc87c79220d9738c9244850bae315e9f8f5b1bcc547f274870bbc9642)
- exactly 2dn = 380 finite numbers: PASS (380 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 17; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.4999809988)
- the two exact-precision methods agree: PASS (difference 6.68e-52, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.49998099883997, difference 8.900E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.49998890 minus mu = 7.901160E-06)
- all three methods name the same attaining pair: PASS (2-7)

## Decision
The object for (5, 38) reproduces: exact and 50-digit computations give mu = 0.4999809988399788 on pair 2-7. That matches the claimed 0.49998099883997 and sits 7.901160E-06 below the leaderboard value 0.49998890, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
