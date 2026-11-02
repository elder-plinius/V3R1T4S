# REPRODUCE verdict: hsp4-N156

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:06Z

## Value computed here
r* = 0.22031376415231824839 (mpmath, 50 digits; my own code at work/check.py)
- half min pairwise distance = 0.2203137811634562339267044 (pair indices 80, 90, 0-based)
- 1 - max |c_i|             = 0.220313764152318248389127  -> BINDING term is the container boundary
- table row 156 (claim/hsp4_radius_live.txt) = 0.220308265077
- r* - table = 5.49907531824839e-6 (>= 1e-10)

Note: no `evidence/` folder was provided in my cell; the table value was read from claim/hsp4_radius_live.txt as instructed by REPRODUCE.md. The object's `#` header line states values; it was ignored and all numbers above were computed independently (they happen to agree with it).

## Clauses checked
- Object integrity: sha256 of hsp4-156.txt = a7ced3321fa76c13cb6372501334593f81d9a0385864873726b3b9fb87483f3b, matches CLAIM.md. PASS
- Parse: 156 non-comment rows, 4 numbers each, no NaN/inf, no duplicate rows (as strings and as exact rationals). PASS
- Coordinate precision: 14 to 17 significant digits per number (median 16), i.e. IEEE double output. Recorded; the hsp4 criterion has no digit requirement.
- Computation 1 (mpmath, 50 dps, no tolerance): r* = 0.22031376415231824839, boundary term binds. PASS
- Computation 2 (exact Fractions for all squared distances/norms, 60-digit Decimal square roots): r* = 0.2203137641523182483891270108; differs from mpmath by -6.7e-52. Agreement confirmed.
- Margin: r* - table = 5.499075318e-6 >= 1e-10. PASS

## Decision
Both independent computations reproduce r* = 0.22031376415231824839 from the submitted coordinates, binding at the container boundary, exceeding the live table value 0.220308265077 for N = 156 by 5.50e-6, far above the 1e-10 threshold. All REPRODUCE clauses pass. (Clauses about posted-file isometry/polish, history entries and the pending queue are outside this role.)

pass: true
