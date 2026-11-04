# REPRODUCE verdict: hsp4-N215

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:06Z

## Value computed here
r* = 0.20376854965104970107 (binding term: wall, 1 - max|c_i|)
- half min pair distance = 0.20376854965104974669 (pair indices 111, 171, 0-based), only ~4.6e-17 above the wall term
- table row 215 (claim/hsp4_radius_live.txt) = 0.203682998566
- r* - table = 8.5551085049701071154e-5

Code: work/rep.py (my own). The table file is the live re-fetch the panel supplied in claim/. My folder has no evidence/ directory; I did no web access.

## Clauses checked
- Parse: 215 non-comment rows, each with exactly 4 numbers. No NaN or inf. All 215 rows are distinct, compared as exact Fractions. Comment lines were ignored; they state the same value I computed, and I did not use them. PASS
- Coordinate precision: every number is in scientific notation with up to 20 significant digits (mantissa d.ddddddddddddddddddd). The minimum is 17 significant digits after trailing zeros are dropped. Fractional-part lengths are 19–22 characters. Recorded only; not a pass criterion for hsp4.
- Computation 1, mpmath at 50 digits: r* = 0.203768549651049701071154. PASS
- Computation 2, exact Fractions with Decimal square roots at 60 digits: r* = 0.2037685496510497010711540416… The two methods differ by 3.3e-52, so they agree. PASS
- r* - table >= 1e-10: 8.555e-5 >= 1e-10. PASS
- sha256 of hsp4_N215.txt = 08d402ae2020be2bab2b33b7f3dd9846efc5ff6e7fe71f8715d4071c74238687, which matches CLAIM.md.

## Decision
Two independent high-precision computations from the submitted coordinates agree. Both give r* = 0.20376854965104970107. That is 8.56e-5 above the table value of 0.203682998566 for N = 215, far more than the required 1e-10. The wall term binds, and the minimum pair distance is almost exactly equal to it, which fits a polished packing. No injection was suspected. Novelty, isometry and queue clauses are not part of the REPRODUCE role.

pass: true
