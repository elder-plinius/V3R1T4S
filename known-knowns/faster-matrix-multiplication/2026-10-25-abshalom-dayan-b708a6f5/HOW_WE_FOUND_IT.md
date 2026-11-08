# How we found it (contributor text, unverified)

This cell is one of twelve from the same batch run. The earlier 19^3 claims (PR #708 for <18,19,19> at 3424 and PR #714 for <18,18,19> at 3225) read Khoruzhii, Serafin, Gelss and Pokutta's LITA square schemes as data and found that one non-coordinate slice of LITA N^3 (direction e* = (1,...,1, -(N-5)/2, 1,...,1) on one side of a shared index, a unit vector on the other) kills (N^2 - 1)/2 + (3N - 1)/2 terms, and that one exact 2-reduction then removes one more term. The batch applied the same code, unchanged, to LITA 29^3 (rank 11203).

The first slice (direction e* = (1,...,1, -12, 1,...,1) with -12 at index 14 on the A side of the shared row index, a unit vector on the C side) kills 463 terms (420 + 43) and one exact 2-reduction gives <28,29,29> at 10739. Applying a second slice of the same kind to the <28,29,29> scheme of rank 10739, on the other shared index, kills 448 more terms (29 on the A side, 419 on the B side), and one more 2-reduction gives <28,28,29> at 10290, against 10630 in fmm_sota.json and the Lille index.

Term accounting: 463 + 1 + 448 + 1 = 913 = 11203 - 10290.

What did not work: plain coordinate projections. Deleting a row and a column of LITA 29^3 gives at best 11087 (116 terms vanish), and the best single-coordinate deletion of the <28,29,29> scheme gives 10682; both are above the 10630 in the tables. Checks and the pitfalls list for the batch are in how-we-built-it/PREREG.md.

Checks done for this package: the rebuild from LITA's public file was done once; a second rebuild was not run, so its determinism is not confirmed. A standard-library exact checker over all Brent equations, a separately written numpy exact checker, exact random evaluations, negative controls that both checkers reject, and an exact count of the terms each step removes.
