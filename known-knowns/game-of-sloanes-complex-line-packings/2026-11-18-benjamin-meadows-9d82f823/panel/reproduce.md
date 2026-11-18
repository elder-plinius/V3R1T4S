# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (6, 48)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 1128 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.462465554696522291085122901885, attained by vectors 27 and 38 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.462465554696522291085122901885, pair 27-38; difference from the exact method 1.34e-51.
- float64 sanity value 0.4624655546965225, pair 27-38. Largest minus second-largest overlap (exact): 2.7849E-13; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.46253866 from CLAIM.md: 7.310530E-05 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed 9d82f82313b33a98fe016af32807739bbf2f3f54efc4a1f1c977acf1fbd0f87a)
- exactly 2dn = 576 finite numbers: PASS (576 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 17; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.4624655546)
- the two exact-precision methods agree: PASS (difference 1.34e-51, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.46246555469652, difference 2.291E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.46253866 minus mu = 7.310530E-05)
- all three methods name the same attaining pair: PASS (27-38)

## Decision
The object for (6, 48) reproduces: exact and 50-digit computations give mu = 0.4624655546965222 on pair 27-38. That matches the claimed 0.46246555469652 and sits 7.310530E-05 below the leaderboard value 0.46253866, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
