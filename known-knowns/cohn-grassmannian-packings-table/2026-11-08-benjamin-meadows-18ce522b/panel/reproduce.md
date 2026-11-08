# REPRODUCE verdict: cohn-grassmannian-packings-table, cell 11-4-66

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-08T02:32:54Z

## Value computed here
- Method A (mpmath, 50 digits, modified Gram-Schmidt with reorthogonalisation on each 4x11 block, all 2145 pairs): 2.577769552477307143413419651715461698922. Running mpmath's own QR on the attaining pair gives the same 40 digits.
- Method B (exact rationals: decimal strings read as Fractions, P_i = A_i^T (A_i A_i^T)^{-1} A_i, value n - tr(P_i P_j), all 2145 pairs): 2.577769552477307143413419651715461698922 (exact Fraction, printed to 40 digits).
- Difference A - B at the minimum: -5.3e-51. Largest |A - B| over all 2145 pairs: 1.6e-50. A numpy float64 QR check gives 2.577769552477307.
- Attaining pair: subspaces 32 and 43 (1-indexed; 0-indexed (31, 42)), the same pair in both methods. It is the only pair within 1e-12 of the minimum. The next smallest pair value is 2.57776961937462908267228, about 6.7e-8 higher.
- Table value: 2.5777278197, taken from CLAIM.md (I did not fetch the live table). Margin: value - table = 4.17327773069e-5.
- Bound: CLAIM.md gives no bound. The comment line in object/11-4-66.txt gives 2.5846153847. That matches the simplex (Rankin) bound n(m-n)/m * N/(N-1) = 168/65 = 2.5846153846153846154, which I computed myself. The value is 0.00684583222269 below 2.5846153847. Whether the live row lists this bound is for the other skeptics to check.

## Clauses checked
- File hash: sha256 of object/11-4-66.txt is 18ce522b9988706b958025d21a9c807f3b487f5e10610d86d4f25406fa058532, which matches CLAIM.md. PASS
- Layout: 1 '#' comment line plus 264 data rows = 66 subspaces x 4 rows. Every row has exactly 11 comma-separated reals. PASS
- Precision: every one of the 2904 coordinates has between 27 and 30 significant digits, and none has fewer than 20. PASS
- Orthonormalisation: the largest |U U^T - I| entry after Gram-Schmidt is 5.3e-51, and every block has full rank 4 (the exact 4x4 Gram inverses exist). PASS
- Two independent methods agree: they differ by 1.6e-50 at most over all pairs and pick the same attaining pair. PASS
- Value matches the claim: the computed 2.577769552477307143413419651715 agrees with the claimed "about 2.57776955247730" and with all 31 digits in the object's comment line. PASS
- Strictly beats the table by at least 1e-9: 2.5777695525 - 2.5777278197 = 4.173e-5, which is at least 1e-9. PASS
- Does not exceed the bound by more than 1e-10: the value is 0.0068 below 2.5846153847 (= 168/65), so it is not above the bound at all. PASS
- Steering check: no file in the claim folder tries to steer the verdict. The object's comment line states the value, the table value, the bound and the margin; I treated it as data and recomputed each figure.

## Decision
Two independent computations (mpmath 50-digit Gram-Schmidt and exact rational projectors) over all 2145 pairs both give a minimum squared chordal distance of 2.5777695524773071434134196517..., attained only by subspaces 32 and 43. This beats the table value 2.5777278197 from CLAIM.md by 4.17e-5 and stays below the simplex bound 168/65. The object file is well formed and precise enough, so the claimed value reproduces. The live table, star/note, bound and arXiv clauses are for the other skeptics.

pass: true
