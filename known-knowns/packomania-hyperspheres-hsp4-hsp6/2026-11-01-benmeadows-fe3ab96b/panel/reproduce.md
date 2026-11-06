# REPRODUCE verdict: hsp4-N160

context: subagent (fresh context started by the packaging session's Agent tool; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-01T21:06Z

## Value computed here
r* = 0.21857935352324099278 (mpmath 50 digits; agrees to >45 digits with exact Fractions + 60-digit Decimal sqrt).
Binding term: containment, 1 - max|c_i| = 0.2185793535232409927806705 (half min distance = 0.2185793536151558885367938, pair (6,102), 0-based).
Table row 160 (claim/hsp4_radius_live.txt): 0.218358476129. r* - table = 2.2087739424099278e-4.

## Clauses checked
- Parse: object sha256 fe3ab96b...e394 matches CLAIM.md; 160 non-comment rows, 4 numbers each, all finite, no duplicate rows: pass. Header comment ignored (its numbers happen to agree with mine).
- Coordinate precision: 13-17 significant digits per number (float64 round-trip repr); no digit requirement for hsp4 cells.
- r* - table >= 1e-10: 2.2088e-4; also verified exactly in rational arithmetic that min-dist^2 > (2(table+1e-10))^2 and max-norm^2 < (1-(table+1e-10))^2: pass.
- Two independent computations (mpmath vs Fractions+Decimal) agree: pass.
- Note: no evidence/ folder was present in this cell; the table value was read from claim/hsp4_radius_live.txt as REPRODUCE.md directs. Other criterion clauses (isometry/polish/queue/history) are outside this role.

## Decision
The configuration is valid and its feasible radius, computed directly from the coordinates with no tolerance, exceeds the N=160 table value by 2.2e-4, far above 1e-10. Containment binds. Both computations agree.

pass: true
