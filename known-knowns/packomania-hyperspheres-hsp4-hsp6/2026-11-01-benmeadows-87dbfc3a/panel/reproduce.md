# REPRODUCE verdict: hsp4-N136

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:06Z

## Value computed here
- r* = 0.22622027641762341826 (mpmath, 50 digits), binding term: boundary (1 - max_i |c_i|).
- half min distance = 0.22622027769783905028 (pair indices 20, 118, 0-based), so the pair term is about 1.3e-9 larger.
- Table row 136 (claim/hsp4_radius_live.txt): 0.226201706521.
- r* - table = 1.85698966234e-5.
- Coordinate precision: 14 to 17 significant digits per number (ordinary double-precision decimal output).
- Live data: no `evidence/` folder was provided for this cell. The table row was read from `claim/hsp4_radius_live.txt`, as REPRODUCE.md says. The object's sha256 matches the value stated in CLAIM.md (87dbfc3a...a963).

## Clauses checked
- Parse: 136 non-comment rows, each with exactly 4 numbers, 136 distinct rows, no NaN or Inf. PASS.
- r* in mpmath at 50 digits with no tolerance: 0.2262202764176234182699781. PASS.
- Second computation (exact Fractions with 60-digit Decimal square roots) gives r* = 0.2262202764176234182699781. It agrees with mpmath to better than 1e-40. An exact rational check also passes: with t = table + 1e-10, both 4t^2 < min d^2 and (1-t)^2 > max |c|^2 hold. PASS.
- r* - table >= 1e-10: 1.857e-5. PASS.
- Comment line in the object states r* = 0.2262202764176234. I ignored it and computed my own value, which matches it. No injection suspected.

## Decision
Two independent computations, plus an exact rational inequality check, show that the 136 centres have a feasible radius of 0.22622027641762341827. This beats the table value 0.226201706521 by 1.857e-5, well above the 1e-10 margin. The boundary term binds, and the pair term is only about 1.3e-9 above it. The other clauses (non-isometry, polish, provenance, history and queue) belong to other roles and were not checked here.

pass: true
