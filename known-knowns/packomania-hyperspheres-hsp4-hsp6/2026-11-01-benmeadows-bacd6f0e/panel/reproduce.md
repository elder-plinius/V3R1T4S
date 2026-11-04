# REPRODUCE verdict: hsp4-N216

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:06Z

## Value computed here
Own code: work/check.py (run with python3 -I, OMP/OPENBLAS threads = 1).

- r* = 0.20362333097990599275 (mpmath, 50 digits)
- binding term: container boundary, 1 - max|c_i| = 0.2036233309799059927522058
- pair term: min|c_i - c_j|/2 = 0.2036233309799060304522135 (pair 53, 74, 0-based), larger by about 3.8e-17
- table row 216 (claim/hsp4_radius_live.txt): 0.203582040585
- r* - table = 4.1290394905992752206e-5
- coordinate precision: 16 to 20 significant digits per number
- 666 pairs and 188 boundary contacts lie within 1e-9 of r*, which is what a polished packing looks like

## Clauses checked
- Object integrity: sha256 of hsp4_N216.txt is bacd6f0e…5e968, the same as in CLAIM.md. Skipping the `#` lines leaves 216 rows, each with exactly 4 numbers. There are no NaN or inf values and all 216 rows are distinct. PASS.
- Recomputing r* in mpmath at 50 digits with no tolerance gives 0.2036233309799059927522058, and the boundary term is the one that binds. PASS.
- Independent second computation: I used exact Fractions for the squared distances and squared norms, then 60-digit Decimal square roots. Half the minimum distance came out as 0.2036233309799060304522134…, the boundary term as 0.2036233309799059927522057…, and r* - table as 4.12903949059927522057…e-5. This agrees with mpmath to every digit printed; the only gap is in the 25th digit, because Decimal truncated where mpmath rounded. PASS.
- Margin over the table: r* - table = 4.129e-5, which is at least 1e-10. PASS.
- The comment header in the object states r* = 0.2036233309799059927522058. My value matches it, but I computed mine on my own and did not rely on the header. No injection suspected.
- Table source: the table value comes from claim/hsp4_radius_live.txt. The panel's instructions describe that file as the owner's live re-fetch from 2026-11-01. This folder has no evidence/FETCHED.md, so I could not check a sha256 for the table file. The re-fetch and history checks belong to other roles.

## Decision
Two independent high-precision computations of r*, starting from the submitted coordinates, agree on 0.20362333097990599275. The container boundary is the binding term. That value beats the table entry 0.203582040585 by 4.13e-5, far more than the required 1e-10. The object is well formed: 216 distinct 4-vectors with 16 to 20 significant digits. Every clause assigned to REPRODUCE passes.

pass: true
