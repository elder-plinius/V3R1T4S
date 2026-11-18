# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (3, 46)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 1035 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.794283670417108555043698378821, attained by vectors 12 and 26 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.794283670417108555043698378821, pair 12-26; difference from the exact method 1.34e-51.
- float64 sanity value 0.7942836704171089, pair 12-26. Largest minus second-largest overlap (exact): 1.4841E-14; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.79435710 from CLAIM.md: 7.342958E-05 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed a7bb774c95dff1a9b33b464e8d898037621da74deaff699814f20fe77b350902)
- exactly 2dn = 276 finite numbers: PASS (276 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 18; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.7942836704)
- the two exact-precision methods agree: PASS (difference 1.34e-51, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.79428367041710, difference 8.555E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.79435710 minus mu = 7.342958E-05)
- all three methods name the same attaining pair: PASS (12-26)

## Decision
The object for (3, 46) reproduces: exact and 50-digit computations give mu = 0.7942836704171085 on pair 12-26. That matches the claimed 0.79428367041710 and sits 7.342958E-05 below the leaderboard value 0.79435710, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
