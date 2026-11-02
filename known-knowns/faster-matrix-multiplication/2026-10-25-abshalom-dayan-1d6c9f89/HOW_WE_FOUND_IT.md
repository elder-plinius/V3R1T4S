# How we found it (contributor text, unverified)

This cell is one of twelve from the same batch run. The earlier 19^3 claims (PR #708 for <18,19,19> at 3424 and PR #714 for <18,18,19> at 3225) read Khoruzhii, Serafin, Gelss and Pokutta's LITA square schemes as data and found that one non-coordinate slice of LITA N^3 (direction e* = (1,...,1, -(N-5)/2, 1,...,1) on one side of a shared index, a unit vector on the other) kills (N^2 - 1)/2 + (3N - 1)/2 terms, and that one exact 2-reduction then removes one more term. The batch applied the same code, unchanged, to LITA 27^3 (rank 9233).

The first slice (direction e* = (1,...,1, -11, 1,...,1) with -11 at index 13 on the A side of the shared row index, a unit vector on the C side) kills 404 terms (364 + 40) and one exact 2-reduction gives <26,27,27> at 8828. Applying a second slice of the same kind to the <26,27,27> scheme of rank 8828, on the other shared index, kills 390 more terms (27 on the A side, 363 on the B side), and one more 2-reduction gives <26,26,27> at 8437, against 8727 in fmm_sota.json and the Lille index.

Term accounting: 404 + 1 + 390 + 1 = 796 = 9233 - 8437.

What did not work: plain coordinate projections. Deleting a row and a column of LITA 27^3 gives at best 9125 (108 terms vanish), and the best single-coordinate deletion of the <26,27,27> scheme gives 8775; both are above the 8727 in the tables. Checks and the pitfalls list for the batch are in how-we-built-it/PREREG.md.

Checks done for this package: the rebuild from LITA's public file was done once; a second rebuild was not run, so its determinism is not confirmed. A standard-library exact checker over all Brent equations, a separately written numpy exact checker, exact random evaluations, negative controls that both checkers reject, and an exact count of the terms each step removes.
