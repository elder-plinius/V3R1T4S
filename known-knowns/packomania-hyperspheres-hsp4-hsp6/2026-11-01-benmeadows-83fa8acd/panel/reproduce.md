# REPRODUCE verdict: hsp4-N217

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:06Z

## Value computed here
r* = 0.20344247849929273721 (container term binds: 1 - max|c_i|)
half min distance = 0.20344247849929279774 (pair 14,189, 0-based), about 6e-17 above the container term
table (claim/hsp4_radius_live.txt, row 217) = 0.203438871092
r* - table = 3.6074072927e-6

Script: work/check.py (mine). The comment lines in the object file state values; I ignored them and computed my own, which match.
Table value comes from claim/hsp4_radius_live.txt. This cell has no evidence/ folder, so I did not check a live-fetch sha256 here.

## Clauses checked
- Parse: object sha256 matches CLAIM.md (83fa8acd...0bc). There are 217 non-comment rows of 4 numbers each, with no duplicate rows and no NaN or Inf. PASS
- Coordinate precision: 17 to 20 significant digits per number. Reported for information; the hsp4 cells have no digit threshold.
- r* in mpmath at 50 digits with no tolerance: 0.20344247849929273721302. PASS
- Second method: exact Fractions for the squared distances and norms, then Decimal square roots at 60 digits. It gives r* = 0.2034424784992927372130200..., which differs from mpmath by 6.7e-52. They agree. PASS
- r* - table >= 1e-10: 3.607e-6 >= 1e-10. PASS

## Decision
I recomputed r* from the submitted coordinates with two independent methods, and they agree to about 50 digits. r* beats the 12-decimal table value for N = 217 by 3.6e-6, which is far above the 1e-10 threshold. The ball-boundary constraint binds, and the closest pair sits only 6e-17 above it, so the packing is tight. This verdict covers only the REPRODUCE clause. The non-isometry, polish, queue and history clauses belong to other roles.

pass: true
