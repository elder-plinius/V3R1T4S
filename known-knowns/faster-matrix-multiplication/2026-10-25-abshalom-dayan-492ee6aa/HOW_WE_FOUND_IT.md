# How we found it (contributor text, unverified)

This cell is one of twelve from the same batch run. The earlier 19^3 claims (PR #708 for <18,19,19> at 3424 and PR #714 for <18,18,19> at 3225) read Khoruzhii, Serafin, Gelss and Pokutta's LITA square schemes as data and found that one non-coordinate slice of LITA N^3 (direction e* = (1,...,1, -(N-5)/2, 1,...,1) on one side of a shared index, a unit vector on the other) kills (N^2 - 1)/2 + (3N - 1)/2 terms, and that one exact 2-reduction then removes one more term. The batch applied the same code, unchanged, to LITA 23^3 (rank 6009).

The first slice (direction e* = (1,...,1, -9, 1,...,1) with -9 at index 11 on the A side of the shared row index, a unit vector on the C side) kills 298 terms (264 + 34) and one exact 2-reduction gives <22,23,23> at 5710. Applying a second slice of the same kind to the <22,23,23> scheme of rank 5710, on the other shared index, kills 286 more terms (23 on the A side, 263 on the B side), and one more 2-reduction gives <22,22,23> at 5423, against 5625 in fmm_sota.json and the Lille index.

Term accounting: 298 + 1 + 286 + 1 = 586 = 6009 - 5423.

What did not work: plain coordinate projections. Deleting a row and a column of LITA 23^3 gives at best 5917 (92 terms vanish), and the best single-coordinate deletion of the <22,23,23> scheme gives 5665; both are above the 5625 in the tables. Checks and the pitfalls list for the batch are in how-we-built-it/PREREG.md.

Checks done for this package: the rebuild from LITA's public file was done twice with byte-identical step files and text exports. A standard-library exact checker over all Brent equations, a separately written numpy exact checker, exact random evaluations, negative controls that both checkers reject, and an exact count of the terms each step removes.
