# How we found it (contributor text, unverified)

This cell came out of the same run as PR #708 (<18,19,19> rank 3424). That run read Khoruzhii, Serafin, Gelss and
Pokutta's LITA square schemes as data and found that one non-coordinate slice of LITA N^3 (direction
e* = (1,...,1, -(N-5)/2, 1,...,1) on one side of a shared index, a unit vector on the other) kills
(N^2 - 1)/2 + (3N - 1)/2 terms, and that one exact 2-reduction then removes one more term. For N = 19 that gave
<18,19,19> at 3424 (PR #708).

Applying a second slice of the same kind to the 3424 scheme, on a different shared index, kills 198 more terms, and
one more 2-reduction gives <18,18,19> at 3225, against 3355 in fmm_sota.json and the Lille index. The code that does
both slices (code/rebuild_lita_slices.py) was already published in #708's how-we-built-it/, and #708's text
mentioned the value 3225; this package files the scheme itself, with its own checks.

What did not work: plain coordinate projections. Deleting a row and a column of LITA 19^3 gives at best 3557, and
deleting one column of the 3424 scheme gives 3395; both are above the 3355 block sum in the tables. Earlier in that
run, one candidate (<16,16,17> 2392) failed novelty because closed PR #44 had already published it; #41-#51 cover the
p1 formats with max dimension 17 and 18, which is why the run moved to max dimension 19.

Checks done for this package: a byte-identical rebuild from LITA's public file, a new standard-library checker over
all 37,896,336 Brent equations, exact random evaluations, negative controls that both checkers reject, and an exact
count of the terms each step removes (208 + 1 + 198 + 1 = 408 = 3633 - 3225).
