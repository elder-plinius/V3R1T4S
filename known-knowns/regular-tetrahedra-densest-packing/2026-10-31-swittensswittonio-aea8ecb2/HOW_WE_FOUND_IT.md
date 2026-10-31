# How we found it

contributor text, unverified

The brief: attack the densest-packing question for regular tetrahedra from the upper-bound side, where a partial win (a certified bound beating the published 1 - 2.6e-25 of Gravel, Elser and Kallus) is reachable by exact computation. No packing was sought in this claim (several packing searches ran in the same run and found nothing above 4000/4671).

Lens trail: an earlier run certified 1 - 1.0215562e-15 (draft PR #863), then this run's `stability` lens 1 - 4.501141e-15 (draft PR #864), both conditional on three published GEK lemmas. Two further lenses then removed the conditions: `lemma-check` proved K1 analytically, K4 by exact integer branch-and-bound with slack, and wrote a K3 argument, and found that a step in GEK's Lemma 3.1 proof is false as printed; `fullproof` assembled one self-contained written reduction (`object/REDUCTION_FULL.md`) and a rewritten Arb chain with K4's constant (3/sqrt2)(1+1/1000), giving b >= 4.501166e-15.

What failed: a first-order stability lemma for five near-cone wedges, which numerics suggest could gain orders of magnitude, was not obtained. The panel (three fresh skeptics, honesty gate) is in `panel/`.
