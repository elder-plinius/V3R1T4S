# How we found it (contributor text, unverified)

Brief: the 2026-10-25 V3R1T4S weekend runs on small-ramsey-lower-bounds (one laptop, CPU only). The target asks for
a two-colour Ramsey lower bound above DS1; a multicolour cell above DS1 is partial win p1.

- The idea: Exoo and Tatarevic (arXiv:1504.02403) built three-colour bounds R(3,k,m) by taking a two-colour colouring
  with no K_s in one colour and no K_m in the other, and splitting the K_s-free colour into a triangle-free colour and
  a K_k-free colour; this can only work when s <= R(3,k) (14 for k = 5). Kuznetsov's circulants (arXiv:1505.07186,
  posted after the Exoo-Tatarevic preprint) include a (6,9) graph on 182 vertices.
- What worked: Kuznetsov's (6,9) circulant on Z_182. Its K9-free colour (54 distance classes) splits into a
  triangle-free circulant colour and a K5-free circulant colour (SAT over the distance classes, with complete
  triangle clauses and lazily added K5 clauses, exact final check). Colour 3 is the source's K6-free colour,
  unchanged. 182 + 1 = 183 > 181.
- What failed: one-vertex extension of the object (SAT; stopped undecided at its 1600 s alarm); K3 + K5 circulant
  splits of the (6,10) graph on 203 and the (6,12) graph on 293 (solver UNSAT, no certificate saved).
- Checks: two exact checkers in the run (bitset branch and bound, and a CaDiCaL UNSAT answer, no certificate saved) agree for every colour;
  the standard-library checker in verify-it-yourself/ agrees; the reports of three fresh-context skeptics (REPRODUCE, NOVELTY,
  CRITERION) are in panel/.
