# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (7, 26)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:27:19Z

## Value computed here
- Exact rational arithmetic on the decimal strings (all 325 pairs, squared overlap as an exact fraction, square root at 60 digits): mu = 0.333071874375315829479595221429, attained by vectors 15 and 21 (0-based).
- mpmath at 50 digits (each vector normalised first, complex inner products): mu = 0.333071874375315829479595221429, pair 15-21; difference from the exact method 0.0.
- float64 sanity value 0.3330718743753159, pair 15-21. Largest minus second-largest overlap (exact): 2.0470E-10; the largest value is attained by 1 pair exactly.
- Margin vs the leaderboard value 0.33315439 from CLAIM.md: 8.251562E-05 below it.

## Clauses checked
- sha256 of the object matches CLAIM.md: PASS (computed c546acd73014a01099f3b54379f86edd3ee81eb54a002df6398f0a8d4332fcb6)
- exactly 2dn = 364 finite numbers: PASS (364 tokens, 0 not plain finite decimals)
- every coordinate written with >= 16 significant digits: PASS (fewest significant digits as written: 18; exact zeros: 0)
- no zero vector: PASS (smallest squared norm 1)
- no repeated line (mu < 1): PASS (mu = 0.3330718743)
- the two exact-precision methods agree: PASS (difference 0.0, same pair)
- computed mu agrees with the claimed value: PASS (claimed 0.33307187437531, difference 5.829E-15 (claimed value is mu cut to 14 decimals))
- mu at least 1e-8 below the leaderboard value: PASS (leaderboard 0.33315439 minus mu = 8.251562E-05)
- all three methods name the same attaining pair: PASS (15-21)

## Decision
The object for (7, 26) reproduces: exact and 50-digit computations give mu = 0.3330718743753158 on pair 15-21. That matches the claimed 0.33307187437531 and sits 8.251562E-05 below the leaderboard value 0.33315439, well past the 1e-8 bar. The file format, digit count and hash all check out. The live leaderboard re-fetch is left to another reviewer.

pass: true
