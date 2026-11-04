# REPRODUCE verdict: hsp4-N213

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:06Z

## Value computed here
Own code: work/check.py (mpmath at 50 digits, plus exact Fractions with 60-digit Decimal square roots).
- r* = 0.20405661952173254774 (boundary term binds)
- half min distance = 0.204056619521732566095527 (pair indices 74,160, 0-based data rows)
- 1 - max|c_i| = 0.2040566195217325477356727
- table row 213 (claim/hsp4_radius_live.txt) = 0.204053178162
- r* - table = 3.44135973254774e-6
- the two methods agree to 6.7e-52
- coordinate precision: 17 to 20 significant digits per number (16 to 19 decimals), in scientific notation

## Clauses checked
- Object integrity: the sha256 of hsp4_N213.txt matches CLAIM.md (1dd27691...39e8c). PASS
- Parse: 213 non-comment rows, each with 4 numbers. No NaN or Inf, no duplicate rows. The `#` header lines were skipped and not trusted. They state the same value that I computed independently. PASS
- r* computed with no tolerance, in mpmath at 50 digits and with exact rationals: 0.20405661952173254774. The boundary term binds. The distance term is larger by about 1.8e-17. PASS
- r* - table >= 1e-10: 3.44136e-6 >= 1e-10. PASS
- Two independent computations agree (difference 6.7e-52). PASS

Note: my folder has no evidence/ directory and no FETCHED.md. As REPRODUCE.md directs, I used the table file provided at claim/hsp4_radius_live.txt (sha256 f3ddaa94...569f) as the live table. Its row 213 matches the value quoted in CLAIM.md. I did not check freshness, the comparison against the posted packing, the queue rule or history entries; those are outside the REPRODUCE role.
injection_suspected: none (the header comments only state values)

## Decision
The configuration is well formed. Its feasible radius, recomputed two independent ways, is 0.20405661952173254774. That is above the table value 0.204053178162 by 3.44e-6, far above the 1e-10 margin. Every REPRODUCE clause passes.

pass: true
