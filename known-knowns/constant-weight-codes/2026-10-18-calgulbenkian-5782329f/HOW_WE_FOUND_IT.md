contributor text, unverified

Contributor: calgulbenkian. The search agent was Gemini ("Argon"), working on 2026-10-17 and 2026-10-18.

The brief was to attack Brouwer's table of bounds for constant-weight codes. Argon pre-registered three goals; this claim belongs to the first, an improved upper bound with an exact rational certificate. For cells with length n above 28 the live table prints no upper bound ("For n > 28 unmarked upper bounds are from the Johnson bound"), so Argon used only the Delsarte inequalities of the Johnson scheme (indices 1 to w) and solved the resulting linear program in exact fractions. For A(35,14,14) the optimum is 56100/67, and its integer part, 837, is the bound.

Argon's notes say that only 'D' constraints were active and no table values went in. The panel's reading of the target is that a bound already implied by other bounds through the Johnson rules is not a new record, so the claim is measured against the table-implied bound (1143), not against the empty cell.

What failed or was dropped along the way is not recorded in the snapshot. The LP-building code is not in the snapshot either (see how-we-built-it/README.md).
