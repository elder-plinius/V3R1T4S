# REPRODUCE verdict: sph-31-64

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:06Z

## Value computed here
- c* = 0.030319733375043224554 (max pairwise inner product after normalisation; attained by vectors 15 and 29, 0-indexed)
- minimal angle = 88.262540968584349 degrees
- table (31,64) = 0.030322662292 (row `31,64,0.030322662292` in https://spherical-codes.org/plain (fetched 2026-11-01T14:32Z, sha256 b7c6a76fe07eab18f4da729f1162a65d1e5042678d7568013b1d49737df254c1), the only 31,64 row)
- table - c* = 2.9289169567754461104e-6 (>= 1e-10)
- 1451 pairs lie within 1e-12 of the max (a highly balanced code, as expected of an optimised configuration).

## Clauses checked
- Parsing: 2 comment lines skipped (their stated values ignored), exactly 64 rows of 31 numbers, 64 distinct rows, no NaN/Inf, no zero tokens. Object sha256 38ad0da4...f421a matches SHA256SUMS. PASS.
- Digit requirement (>= 20 significant digits per coordinate): every one of the 1984 coordinates has exactly 21 significant digits. PASS.
- c* via method 1 (mpmath, 50 digits, normalise then fsum dot products): 0.03031973337504322455388961.
- c* via method 2 (exact Fractions for dot products and squared norms, Decimal at 60 digits for division and sqrt): 0.0303197333750432245538896. Both pick pair (15,29); |difference| = 3.8e-52. Agree. PASS.
- Margin: table - c* = 2.93e-6 >= 1e-10. PASS.
- Table source: https://spherical-codes.org/plain (fetched 2026-11-01T14:32Z, sha256 b7c6a76fe07eab18f4da729f1162a65d1e5042678d7568013b1d49737df254c1); this skeptic was given the fetched copy without its hash and did not re-verify the fetch sha256. The remaining success-criterion clauses (no '&ast;' mark, no 'needs more optimization', arXiv supersession) belong to other roles. The kissing-number exclusion does not apply (d = 31 is outside 9..23).

## Decision
Two independent high-precision computations agree that the posted 64 vectors in R^31, with 21-digit coordinates, have maximum normalised inner product c* = 0.030319733375043224554, which is below the table cosine 0.030322662292 by 2.93e-6, far more than the required 1e-10. All REPRODUCE clauses pass.

pass: true
