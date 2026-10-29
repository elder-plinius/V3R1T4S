# How we found it (contributor text, unverified)

This cell is one of twelve from the same batch run. The earlier 19^3 claims (PR #708 for <18,19,19> at 3424 and PR #714 for <18,18,19> at 3225) read Khoruzhii, Serafin, Gelss and Pokutta's LITA square schemes as data and found that one non-coordinate slice of LITA N^3 (direction e* = (1,...,1, -(N-5)/2, 1,...,1) on one side of a shared index, a unit vector on the other) kills (N^2 - 1)/2 + (3N - 1)/2 terms, and that one exact 2-reduction then removes one more term. The batch applied the same code, unchanged, to LITA 31^3 (rank 13433).

The first slice (direction e* = (1,...,1, -13, 1,...,1) with -13 at index 15 on the A side of the shared row index, a unit vector on the C side) kills 526 terms (480 + 46) and one exact 2-reduction gives <30,31,31> at 12906. Applying a second slice of the same kind to the <30,31,31> scheme of rank 12906, on the other shared index, kills 510 more terms (31 on the A side, 479 on the B side), and one more 2-reduction gives <30,30,31> at 12395, against 12789 in fmm_sota.json and the Lille index.

Term accounting: 526 + 1 + 510 + 1 = 1038 = 13433 - 12395.

What did not work: plain coordinate projections. Deleting a row and a column of LITA 31^3 gives at best 13309 (124 terms vanish), and the best single-coordinate deletion of the <30,31,31> scheme gives 12845; both are above the 12789 in the tables. Checks and the pitfalls list for the batch are in how-we-built-it/PREREG.md.

Checks done for this package: the rebuild from LITA's public file was done once; a second rebuild was not run, so its determinism is not confirmed. A standard-library exact checker over all Brent equations, a separately written numpy exact checker, exact random evaluations, negative controls that both checkers reject, and an exact count of the terms each step removes.
