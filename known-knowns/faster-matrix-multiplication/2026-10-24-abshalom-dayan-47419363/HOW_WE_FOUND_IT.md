# How we found it (contributor text, unverified)

The run started from Khoruzhii, Serafin, Gelss and Pokutta's LITA schemes for odd N x N x N (13, 15, 17) and an
exact engine for one-slice restrictions: pair a vector e on one side of a shared index with a vector f on the other
(e . f != 0), restrict, drop the terms that vanish, then remove linearly dependent terms exactly (2-reductions).
Reading the LITA schemes as data showed that the best single slice always kills (N^2 - 1)/2 + (3N - 1)/2 terms on any
axis, with e = (1,...,1, -(N-5)/2, 1,...,1) and f a unit vector, followed by one 2-reduction.

The run's main targets (formats with max dimension at most 16, for example <12,13,13> at 1274) stayed one to four
above the record: flip walks, an exhaustive exact single-flip screen and branching over removal choices found
nothing more. Its first p1 candidate, <16,16,17> at 2392 from LITA 17^3, went to the panel and failed NOVELTY: a
closed pull request of this repository (#44, 2026-10-14) had already published 2392. That pull request and its
siblings (#41-#51) cover the p1 formats with max dimension 17 and 18.

No pull request covers max dimension 19 and above, where the Lille catalogue still lists coordinate projections of
LITA's squares (<18,19,19>: 3633) and block sums. The closed form predicted <18,19,19> at 3633 - 209 = 3424 before the
build; one slice of LITA 19^3 gave 3425 and one 2-reduction 3424, exactly as predicted (about 2 minutes). The same
closed form predicts far larger gaps next to LITA 21^3 ... 31^3; those cells were not built in this run (one cell per
claim).
