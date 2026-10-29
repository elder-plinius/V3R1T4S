context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/ 

# REPRODUCE verdict

Checked on 2026-10-25 (`date -u`: Sun Oct 25 11:16:34 UTC 2026).

## Object
`shasum -a 256 object/R_3_5_6.txt` -> `436b74cecb10c8263ed5c3413d66993ce1f9d34993718f7b5bb4b31890896826` (matches CLAIM.md).
Format: `circulant 182 3`; colours 1/2/3 have 20/34/37 distances. My parser confirms the distances of the three
colours partition 1..91 exactly once (every edge of K_182 is coloured exactly once, 91 = N/2 is self-inverse).

## Definition checked (from CLAIM.md)
"no monochromatic K_3 in colour 1, no K_5 in colour 2 and no K_6 in colour 3, so R(3,5,6) >= 183" (N = 182 vertices proves R >= N+1).

## My checkers (work/mycheck.py, work/sat.py, work/brute.py), written before opening verify_circ.py
1. Exhaustive branch-and-bound clique search from vertex 0 (valid by vertex-transitivity of a circulant):
   `colour 1 clique number 2 forbidden 3 ok True`, `colour 2 clique number 4 forbidden 5 ok True`,
   `colour 3 clique number 5 forbidden 6 ok True`, `RESULT PASS`.
2. SAT (CaDiCaL via python-sat), whole graph, no symmetry assumption: "at least k vertices pairwise adjacent in colour c" is UNSAT:
   `colour 1 K3 present: False`, `colour 2 K5 present: False`, `colour 3 K6 present: False`;
   tightness controls SAT: `control K2/K4/K5 present: True`.
3. Naive level-by-level enumeration of all cliques (no symmetry, no pruning): counts of cliques of size 1..k:
   colour 1 [182, 3549, 0]; colour 2 [182, 6188, 46592, 69524, 0]; colour 3 [182, 6734, 67704, 193466, 103012, 0].
   (Edge count check: colour 1 has degree 39 -> 182*39/2 = 3549 edges, matches.)
Three independent exact methods agree; reruns of mycheck.py give identical output (`RESULT PASS` twice more).

## Second opinion (author's verify_circ.py, run only after the above)
`colour 1: degree 39, no K_3 ...`, `colour 2: degree 68, no K_5 ...`, `colour 3: degree 74, no K_6 ...`,
`proves R(3,5,6) >= 183`, `PASS`. Agrees.

## Scope notes
- Reproduction covers the object, its three properties, and the inference R(3,5,6) >= 183. No mismatch, nothing missing, no non-determinism.
- That 181 is the best known lower bound (DS1 Table XIb) and the absence of newer papers is the NOVELTY skeptic's job; I did not re-fetch DS1.
  I only note that 183 > 181 arithmetically.

pass: true
