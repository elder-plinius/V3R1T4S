# Errata (corrections the panel asked for; the panelled files are left exactly as panelled)

None of these changes the result or the certificate.

1. the-record-we-beat and the claim's literature record describe arXiv:2405.07345 as "a bound for the truncated
   square lattice". It is T. Koehler-Schindler and M. Sulser, "Critical probabilities for positively associated,
   finite-range dependent percolation models". It uses a lower bound for site percolation on the truncated square
   lattice as an input. It is not a bound for Z^2 and does not compete (NOVELTY).
2. object/PROOF.md, Section 0: the total order should be of type omega, for example an enumeration of Z^2 starting at
   O, so that "the least vertex with ..." always exists. Any such enumeration works (REPRODUCE).
3. object/PROOF.md, Lemma 2: the displayed density omits the factor 1[eps(O) open]. That factor is implied at every
   step after the first, because O then has a tree edge with eta = 1 (REPRODUCE).
4. The root step is checked by how-we-built-it/code/validate.py, which prints its margin (1.470119e-2) but does not
   assert it is positive, and it is not recorded in object/bound.json. verify-it-yourself/check_bound.py now
   recomputes it from the definition and asserts it. Two skeptics confirmed it independently (CRITERION).
5. The claim's phrase "enlarged to the whole exploration-tree history" should read "exact to depth 3, with universal
   outer cones covering the rest of the history" (CRITERION).
