# How we found it (contributor text, unverified)

This cell is one of twelve from the same batch run. The earlier 19^3 claims (PR #708 for <18,19,19> at 3424 and PR #714 for <18,18,19> at 3225) read Khoruzhii, Serafin, Gelss and Pokutta's LITA square schemes as data and found that one non-coordinate slice of LITA N^3 (direction e* = (1,...,1, -(N-5)/2, 1,...,1) on one side of a shared index, a unit vector on the other) kills (N^2 - 1)/2 + (3N - 1)/2 terms, and that one exact 2-reduction then removes one more term. The batch applied the same code, unchanged, to LITA 27^3 (rank 9233).

The slice (direction e* = (1,...,1, -11, 1,...,1) with -11 at index 13 on the A side of the shared row index, a unit vector on the C side) kills 404 terms (364 + 40) and one exact 2-reduction gives <26,27,27> at 8828, against 9233 in fmm_sota.json and the Lille index.

Term accounting: 404 + 1 = 405 = 9233 - 8828.

What did not work: plain coordinate projections. Deleting the best single index of LITA 27^3 gives 9179 (54 terms vanish), below the 9233 in fmm_sota.json and the Lille index, but already listed by matmulcatalog, so not new. Checks and the pitfalls list for the batch are in how-we-built-it/PREREG.md.

Checks done for this package: the rebuild from LITA's public file was done once; a second rebuild was not run, so its determinism is not confirmed. A standard-library exact checker over all Brent equations, a separately written numpy exact checker, exact random evaluations, negative controls that both checkers reject, and an exact count of the terms each step removes.
