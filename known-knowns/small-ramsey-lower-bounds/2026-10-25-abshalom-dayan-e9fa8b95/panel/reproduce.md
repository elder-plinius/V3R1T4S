context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/ 
# REPRODUCE verdict

Checked 2026-10-25 (date -u: 09:29-09:30 UTC). Object: object/R_3_4_7.txt, `shasum -a 256` = e9fa8b95605e0f8e8d7b020855f7905ff9c02269c9d49a48abd725e7858d6a40 (matches CLAIM.md).

## Definition used
Circulant on Z_153, edge {i,j} has the colour of min((j-i) mod N, N-(j-i) mod N). Claim: colour 1 has no K_3, colour 2 no K_4, colour 3 no K_7. Then the 153-vertex colouring shows R(3,4,7) >= 154.

## Own checkers (written before reading verify_circ.py), work/mycheck.py and work/sat.py
- Format/partition: the three distance sets (18+21+37 = 76) partition 1..76 exactly, no duplicate or missing distance, matrix symmetric, zero diagonal (asserts passed).
- Method A, exhaustive bitset branch-and-bound clique number over all 153 vertices (no symmetry assumed):
  `colour 1 clique number 2 forbidden K 3 ok True`
  `colour 2 clique number 3 forbidden K 4 ok True`
  `colour 3 clique number 6 forbidden K 7 ok True`
  `N 153 => R(3,4,7) >= 154`
- Method B, independent SAT encoding (CaDiCaL, "at least k vertices pairwise adjacent in colour c", all 153 vertices free):
  `colour 1 K3 UNSAT`, `colour 2 K4 UNSAT`, `colour 3 K7 UNSAT`.
  Controls one size down are SAT with witnesses that I re-checked pair by pair: K2 [1, 2]; K3 [1, 3, 5]; K6 [1, 7, 13, 24, 35, 74] (all `witness valid True`). So the encoding is not vacuous and the cliques of size 2/3/6 are tight.
- Negative control: moving distance 6 from colour 3 to colour 1 (work/mut.txt) gave `colour 1 clique number 3 ... ok False` and `NOT PROVEN`, so the checker does detect violations.
- Determinism: two repeat runs of each checker gave identical output (md5 cc955d8a... for A, b30383c2... for B, both runs).

## Second opinion (run only after the above)
`python3 verify_circ.py object/R_3_4_7.txt 3 4 7` printed: colour 1 degree 36 no K_3, colour 2 degree 42 no K_4, colour 3 degree 74 no K_7, `proves R(3,4,7) >= 154`, `PASS`. Agrees.

## Scope and caveats
- Exhaustive and exact; no sampling. Two independent exact methods agree; all properties hold, no mismatch, no missing object.
- N+1 = 154 > 152 relies on the DS1 Table XIb value 152 as recorded in table_record.md. I did not re-fetch the survey or search arXiv (the web was not part of my task); that clause belongs to the NOVELTY skeptic.

pass: true
