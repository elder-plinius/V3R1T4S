# How we found it

contributor text, unverified

The brief: attack the densest-packing question for regular tetrahedra from the upper-bound side, where a partial win (a certified bound beating the published 1 - 2.6e-25 of Gravel, Elser and Kallus) is reachable by exact computation. No new packing was sought.

Lens trail (several lenses ran on the same run):
- formalist (first version): produced a certificate of 1 - 1.0748e-23. Withdrawn: its exact wedge volume bound was found unsound.
- formalist-2: tier A, 1 - 5.714e-24, derived only from GEK's printed statements; separately panelled with three passes. Its folder is in the run but not in this package.
- formalist-3 (this claim): new Lemmas A, R and V together with GEK Lemmas 3.3, 3.5 and the Lemma 4.2 construction, evaluated with Arb: a dynamic-programming chain of certified rho_hat(c,w) lower bounds (`rig_dp.py`) and a scheme scan for Q=40 (`scheme.py`) giving b >= 1.0215562e-15.

What failed: the first lens's wedge-volume bound; some numerical optimisation checks (`numopt.py`, `capsph.py`) were only sanity tools. What worked: the Arb-certified chain plus a small parameter scan. The panel (three skeptics, honesty gate) is in `panel/`.
