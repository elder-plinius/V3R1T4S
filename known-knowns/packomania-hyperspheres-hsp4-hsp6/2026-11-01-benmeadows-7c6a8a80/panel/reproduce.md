# REPRODUCE verdict: hsp4-N163

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:06Z

## Value computed here
r* = 0.21713800642461929883 (binding term: 1 - max_i |c_i|, attained at centre index 0)
half min distance = 0.21713800790564662267 (pair 133,142, 0-based), slack 1.48e-9 above the binding term
table (row 163 of claim/hsp4_radius_live.txt) = 0.217115168538
r* - table = 2.28378866192988e-5

## Clauses checked
- Parse: work/check.py skipped 1 comment line (the claimant's stated value, not trusted) and found exactly 163 rows of 4 numbers, no NaN, no duplicate rows. Object sha256 7c6a8a80...299c6 matches CLAIM.md. PASS
- Coordinate precision: 14 to 17 significant digits per number (float64 shortest repr). Reported; the hsp4 rule sets no minimum.
- r* two ways: (A) exact Fractions for all squared distances and norms, then 60-digit Decimal square roots; (B) mpmath at 50 dps. Both give r* = 0.2171380064246192988269432; |A - B| = 6.7e-52. They agree. PASS
- r* - table >= 1e-10: 2.2838e-5 >= 1e-10. PASS
- Table source: read from the provided claim/hsp4_radius_live.txt (sha256 f3ddaa94...569f). This folder had no evidence/ directory, so I verified no FETCHED.md hashes here. I treat that file as the live re-fetch the panel instructions describe.

## Decision
Both independent high-precision computations reproduce r* = 0.21713800642461929883. The boundary term binds, and the result beats the table value 0.217115168538 by 2.28e-5, far above the 1e-10 margin. This role does not cover the isometry, polish, relaxed-copy, history and queue clauses; the other skeptics check those.

pass: true
