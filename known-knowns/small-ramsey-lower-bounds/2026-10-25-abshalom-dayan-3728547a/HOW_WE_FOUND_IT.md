# How we found it (contributor text, unverified)

Brief: the 2026-10-25 V3R1T4S weekend runs on small-ramsey-lower-bounds (one laptop, CPU only). The target asks for
a two-colour Ramsey lower bound above DS1; a multicolour cell above DS1 is partial win p1.

- The idea: Exoo and Tatarevic (arXiv:1504.02403) built three-colour bounds R(3,k,m) by taking a two-colour colouring
  with no K_s in one colour and no K_m in the other, and splitting the K_s-free colour into a triangle-free colour and
  a K_k-free colour; this can only work when s <= R(3,k) (14 for k = 5). Kuznetsov's circulants (arXiv:1505.07186,
  posted after the Exoo-Tatarevic preprint) include a (7,9) graph on 251 vertices.
- What worked: Kuznetsov's (7,9) circulant on Z_251. Its K9-free colour (68 distance classes) splits into a
  triangle-free circulant colour and a K5-free circulant colour (SAT over the distance classes, with complete
  triangle clauses and lazily added K5 clauses, exact final check). Colour 3 is the source's K7-free colour,
  unchanged. 251 + 1 = 252 > 241 (DS1's R(3,5,7) entry comes from a general construction, item 6.2.g).
- What failed: one-vertex extension of the object (SAT; stopped undecided after 27 minutes); K3 + K5 circulant splits
  of the (7,10) graph on 291 and of a 404-vertex (7,11) circulant that an earlier run found on 2026-10-24 (it
  only ties the published R(7,11) >= 405) (each returned UNSAT from CaDiCaL via pysat).
- Checks: two exact checkers in the run (bitset branch and bound, and CaDiCaL via pysat returning UNSAT; no DRAT/LRAT certificate) agree for every colour;
  the standard-library checker in verify-it-yourself/ agrees; the reports of three fresh-context skeptics (REPRODUCE, NOVELTY,
  CRITERION) are in panel/.
