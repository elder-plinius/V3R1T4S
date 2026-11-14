# REPRODUCE verdict: cohn-grassmannian-packings-table, cell 11-1-62

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-08T02:32:37Z

## Value computed here
- Method A (mpmath, 50 digits, modified Gram-Schmidt on each block, all 1891 pairs): 0.8891705545504745639782620838840554149827
- Method B (exact rational arithmetic, each decimal coordinate converted exactly to a fraction, projectors P_i = A_i^T (A_i A_i^T)^{-1} A_i, value n - tr(P_i P_j), all 1891 pairs): 0.8891705545504745639782620838840554149827 (exact fraction printed to 40 digits)
- Difference A - B: -8.5e-52, which is at the 50-digit working precision of method A.
- Attaining pair: subspaces 12 and 37 (1-indexed; indices 11 and 36 counted from zero). Both methods pick the same pair.
- The claimant's comment line in object/11-1-62.txt states 0.889170554550474563978262083884, and that matches both methods to all 30 printed digits.
- Table value 0.8891152435, taken from CLAIM.md (not fetched here; checking the live table is the other skeptics' job).
- Margin over the table value: 5.5311050474564e-5.
- Bound 0.9239940388. CLAIM.md does not state a bound, so this figure comes only from the claimant's comment line in the object file and is unverified here. The value sits 0.0348234842 below it.

## Clauses checked
- object/11-1-62.txt sha256 matches CLAIM.md (c9da55b9...bba3bb9d2): PASS
- Layout: 1 comment line and 62 data rows = N*n = 62*1, each row with exactly m = 11 comma-separated reals, every one parsed as a decimal: PASS
- Precision: the shortest coordinate has 28 significant digits, at least the 20 required: PASS
- The two independent methods agree to 8.5e-52 and pick the same minimal pair: PASS
- The computed value is greater than the table value 0.8891152435 by 5.53e-5, at least the 1e-9 required: PASS
- The computed value does not exceed the bound 0.9239940388 (taken from the object's comment, not from CLAIM.md or the live table) by more than 1e-10: PASS on that figure, which another skeptic must confirm against the live row.

## Decision
The object parses cleanly into 62 unit-normalisable lines in R^11 with at least 28 significant digits per coordinate. Floating-point (50-digit mpmath) and exact rational computation over all pairs give the same minimum squared chordal distance, 0.88917055455047456398, and it beats the table value from CLAIM.md by 5.53e-5. Nothing in the claim folder tried to steer the conclusion. The live table value, the star/note status, the bound and the arXiv clause were not checked here.

pass: true
