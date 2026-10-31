# How we found it

contributor text, unverified

The brief: attack the densest-packing question for regular tetrahedra from the upper-bound side, where a partial win (a certified bound beating the published 1 - 2.6e-25 of Gravel, Elser and Kallus) is reachable by exact computation. No new packing was sought here (several packing searches ran in the same run and found nothing above 4000/4671).

Lens trail: an earlier run certified 1 - 1.0215562e-15 (draft PR #863) with new Lemmas A, R and V on top of GEK's Lemmas 3.3, 3.5 and the Lemma 4.2 construction. This run's `stability` lens improved it in three places, each ablated in `how-we-built-it/ablation.out`: (1) a multiplicity count (every point lies in at most 6 deficit balls) instead of an independent-set bound, 1.0216e-15 -> 1.8388e-15; (2) counting bad centres at vertices by surface area instead of through Lemma 3.4, -> 3.0642e-15; (3) Lemma V2, a sharper single-wedge excess using both face offsets, -> 4.5011e-15.

What failed: a hoped-for first-order stability lemma for five near-cone wedges (numerics suggest a gain of orders of magnitude is possible, but no proof was found); the Q = 150 variant (5.0685e-15) needs the wedge-area function beyond r = 0.9 and is not the headline. The panel (three fresh skeptics, honesty gate) is in `panel/`.
