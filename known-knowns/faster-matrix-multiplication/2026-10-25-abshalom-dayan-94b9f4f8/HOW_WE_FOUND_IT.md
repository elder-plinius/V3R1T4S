# How we found it (contributor text, unverified)

This cell is one of twelve from the same batch run. The earlier 19^3 claims (PR #708 for <18,19,19> at 3424 and PR #714 for <18,18,19> at 3225) read Khoruzhii, Serafin, Gelss and Pokutta's LITA square schemes as data and found that one non-coordinate slice of LITA N^3 (direction e* = (1,...,1, -(N-5)/2, 1,...,1) on one side of a shared index, a unit vector on the other) kills (N^2 - 1)/2 + (3N - 1)/2 terms, and that one exact 2-reduction then removes one more term. The batch applied the same code, unchanged, to LITA 29^3 (rank 11203).

The slice (direction e* = (1,...,1, -12, 1,...,1) with -12 at index 14 on the A side of the shared row index, a unit vector on the C side) kills 463 terms (420 + 43) and one exact 2-reduction gives <28,29,29> at 10739, against 11203 in fmm_sota.json and the Lille index.

Term accounting: 463 + 1 = 464 = 11203 - 10739.

What did not work: plain coordinate projections. Deleting the best single index of LITA 29^3 gives 11145 (58 terms vanish), below the 11203 in fmm_sota.json and the Lille index, but already listed by matmulcatalog, so not new. Checks and the pitfalls list for the batch are in how-we-built-it/PREREG.md.

Checks done for this package: the rebuild from LITA's public file was done once; a second rebuild was not run, so its determinism is not confirmed. A standard-library exact checker over all Brent equations, a separately written numpy exact checker, exact random evaluations, negative controls that both checkers reject, and an exact count of the terms each step removes.
