# How we found it (contributor text, unverified)

Brief: the 2026-10-25 V3R1T4S weekend runs on small-ramsey-lower-bounds (one laptop, CPU only). The target asks for
a two-colour Ramsey lower bound above DS1; a multicolour cell above DS1 is partial win p1.

- The idea: Exoo and Tatarevic (arXiv:1504.02403) built three-colour bounds R(3,k,m) by taking a two-colour colouring
  with no K_s in one colour and no K_m in the other, and splitting the K_s-free colour into a triangle-free colour and
  a K_k-free colour; this can only work when s <= R(3,k) (9 for k = 4). Kuznetsov's circulants (arXiv:1505.07186,
  posted after the Exoo-Tatarevic preprint) include a (7,7) graph on 153 vertices.
- What worked: Kuznetsov's (7,7) circulant on Z_153. One of its two K7-free colours (39 distance classes) splits
  into a triangle-free circulant colour and a K4-free circulant colour (SAT over the distance classes, with complete
  triangle clauses and lazily added K4 clauses, exact final check). Colour 3 is the source's other K7-free colour,
  unchanged. 153 + 1 = 154 > 152.
- What failed: one-vertex extension of the object (SAT; solver UNSAT, no certificate saved); K3 + K4 circulant splits of both colours of
  a (7,7) circulant on 202 vertices from Kuznetsov's table and of the (7,9) graph on 251 (solver UNSAT, no certificate saved).
- Checks: two exact checkers in the run (bitset branch and bound, and a CaDiCaL UNSAT answer, no certificate saved) agree for every colour;
  the standard-library checker in verify-it-yourself/ agrees; the reports of three fresh-context skeptics (REPRODUCE, NOVELTY,
  CRITERION) are in panel/.
