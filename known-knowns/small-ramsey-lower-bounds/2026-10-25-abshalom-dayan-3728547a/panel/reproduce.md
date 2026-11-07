context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/ .

# REPRODUCE verdict

Scope: I checked that the saved object is a valid 3-colouring of K_251 with no K_3 in colour 1, no K_5 in colour 2 and no K_7 in colour 3. I did not re-check the DS1 value 241 or the literature (the NOVELTY skeptic's job). I only read table_record.md, which quotes 241 for R(3,5,7).

Definition used (from CLAIM.md): vertices 0..250, edge {i,j} gets the colour of the distance (j-i) mod 251, with d and 251-d the same distance. Colour c must contain no clique K_k with k = 3, 5, 7 for c = 1, 2, 3. A colouring of K_N with these properties proves R(3,5,7) >= N+1 = 252.

## Object
`shasum -a 256 object/R_3_5_7.txt` gave 3728547aec5e9b0b5779c21b5bf06cee6dfb90a01230c42389b821fcfa351976, which matches the claim.

## My own checker (written before opening verify_circ.py): work/chk.py, work/sat.py
- Parsing and partition: the three distance sets have sizes 26, 42 and 57 and together are exactly 1..125. That is 251 vertices, every edge coloured exactly once, symmetric. Output line: `N 251 sizes {1: 26, 2: 42, 3: 57} partition ok`.
- Method 1, exhaustive clique search on all 251 vertices with no symmetry assumed (branch and bound over neighbour sets, built from the full adjacency, not only the neighbours of 0):
  - `colour 1 K3 present: (False, 6604)` and `K2 present: True`
  - `colour 2 K5 present: (False, 210199)` and `K4 present: True`
  - `colour 3 K7 present: (False, 2681085)` and `K6 present: True`
  - The True results for the smaller cliques are controls showing the search does find cliques.
- Method 2, SAT (CaDiCaL via python-sat): variable per vertex, a clause forbidding each pair that is not an edge of the colour, a sequential-counter "at least k true" constraint, and vertex 0 forced true (valid because the circulant is vertex-transitive):
  - `colour 1 K3 SAT: False`, control `K2 SAT: True`
  - `colour 2 K5 SAT: False`, control `K4 SAT: True`
  - `colour 3 K7 SAT: False`, control `K6 SAT: True`
  - UNSAT for each forbidden clique, SAT for each one-smaller control.
- Determinism: two further runs of chk.py gave identical output (sha256 of output both 4d0f0aaa4628108354a6b1d0a9a18dd59dc234b9048f93691e1934d650a9e818). Object hash was unchanged.

## Second opinion (run after my verdict): verify_circ.py
```
colour 1: degree 52, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 2: degree 84, no K_5 (no K_4 among the neighbours of 0, exhaustive)
colour 3: degree 114, no K_7 (no K_6 among the neighbours of 0, exhaustive)
N 251 colours 3 forbidden 3,5,7
proves R(3,5,7) >= 252
PASS
```
It agrees with my results.

## Result
Every property reproduced by two independent exact methods, plus the author's checker. No mismatch, no missing object, no non-determinism. The off-by-one is right: N = 251 gives R(3,5,7) >= 252. Against the quoted DS1 value 241 (table_record.md), 252 is higher, but that comparison and the "newer arXiv paper" clause are not part of what I verified.

pass: true
