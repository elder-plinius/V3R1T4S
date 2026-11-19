# How we found it (contributor text, unverified)

Brief: the 2026-10-25 V3R1T4S weekend runs on small-ramsey-lower-bounds (one laptop, CPU only). The target asks for
a two-colour Ramsey lower bound above DS1; a multicolour cell above DS1 is partial win p1.

- The idea: Exoo and Tatarevic (arXiv:1504.02403) built many three-colour bounds R(3,k,m) by taking a two-colour
  colouring with no K_s in one colour (s <= 5) and no K_m in the other, and splitting the K_s-free colour into two
  triangle-free colours. Kuznetsov's circulants (arXiv:1505.07186, posted after the Exoo-Tatarevic preprint) include
  larger (5,m) graphs than the ones behind several DS1 Table XIb entries. Nobody had published the split of those.
- What worked: Kuznetsov's (5,14) circulant on Z_266. Its K5-free colour (47 distance classes) splits into two
  triangle-free circulant colours; a SAT solver over the distance classes found the split in well under a second.
  Colour 3 is the source's K14-free colour, unchanged. 266 + 1 = 267 > 242.
- What failed: one-vertex extension of the object (SAT, exact UNSAT); circulant and edge-level splits of the other
  sources tried for R(3,3,m) (each either exact UNSAT or, for the (5,11), (5,12) and (5,14) circulants, a successful
  split that is a separate claim); lazy edge-level K4/K5 splits
  of non-circulant graphs gave no answer within their time caps.
- Checks: two exact checkers in the run (bitset branch and bound, and CaDiCaL via pysat returning UNSAT; no DRAT/LRAT certificate) agree that colour 3 has
  no K14 (its clique number is 13); the standard-library checker in verify-it-yourself/ agrees; the reports of three fresh-context
  skeptics (REPRODUCE, NOVELTY, CRITERION) are in panel/.
