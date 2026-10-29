# How we found it (contributor text, unverified)

Brief: the 2026-10-25 V3R1T4S weekend runs on small-ramsey-lower-bounds (one laptop, CPU only). The target asks for
a two-colour Ramsey lower bound above DS1; a multicolour cell above DS1 is partial win p1.

- The idea: once an earlier run of the same weekend had a 3-colouring of K_266 with no triangle in colours 1 and 2 and no K_14 in colour 3
  (R(3,3,14) >= 267, its own claim), the elementary colour-3 join gives the next cell for free: add five vertices
  coloured as a pentagon (colour 1) and a pentagram (colour 2), and give every edge from them to the old vertices
  colour 3. A colour-3 clique can use at most one of the five, so the largest colour-3 clique grows from 13 to 14.
- What worked: the join gives a 3-colouring of K_271 with no K_3, K_3, K_15, so R(3,3,15) >= 272, above DS1's 269
  (Exoo and Tatarevic). The construction is folklore; the new value comes from the new R(3,3,14) colouring, which
  splits Kuznetsov's (5,14) circulant on Z_266 by the Exoo-Tatarevic method.
- What failed: the same join from the weekend's other colourings stays below DS1 in every other cell; the K_271
  colouring has no one-vertex extension (it would extend the K_266 colouring, and a SAT search on the run's
  machine returned UNSAT for that; the search is not shipped here).
- Checks: a structural checker (circulant part by exhaustive branch and bound, block checked) and a second exact
  checker that uses only the rotation symmetry of the old part (branch and bound and a CaDiCaL UNSAT verdict through
  vertex 0, no proof certificate saved); the reports of three fresh-context skeptics (REPRODUCE, NOVELTY, CRITERION) are in panel/.
