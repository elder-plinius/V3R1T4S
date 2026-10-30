context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/ 

# REPRODUCE verdict: R(3,3,12) >= 203 via circulant 3-colouring of K_202

## Object
`shasum -a 256 object/R_3_3_12.txt` -> `eeb47c398be7c450cadf8d9b5939d4996761911a1ddba276e6d820b87fd0db1b` (matches CLAIM.md; re-run after the checks gave the same hash).

## Definition used (CLAIM.md)
Vertices 0..201, edge {i,j} gets the colour of distance (j-i) mod 202; d and 202-d are the same distance. The claim: no K_3 in colour 1, no K_3 in colour 2, no K_12 in colour 3. A graph on N vertices with this property proves R(3,3,12) >= N+1 = 203.

## My own checker (work/mycheck.py, written before opening verify_circ.py; standard-library B&B max clique with greedy-colouring bound, run in the venv python)
Checks: (a) the three distance sets, normalised to 1..101, partition {1..101} exactly (every edge has exactly one colour, no duplicates, no 0); (b) the clique number of each colour graph. The graph is vertex-transitive, so omega = 1 + max clique in the neighbourhood of vertex 0.
Output (work/mycheck.out):
```
N 202 sizes {1: 18, 2: 20, 3: 63} partition ok
colour 1 omega = 2
colour 2 omega = 2
colour 3 omega = 11
```
Exhaustive B&B, so omega(colour 3) = 11 < 12, omega(colours 1, 2) = 2 < 3. A second run gave an identical output (`diff` empty, "deterministic").

## Second exact method: SAT (work/sat.py, CaDiCaL via python-sat, sequential-counter cardinality, clique through vertex 0)
Output (work/sat.out):
```
colour 1 triangles via distances: 0
colour 2 triangles via distances: 0
colour 3 K12 containing vertex 0 SAT? False
colour 3 K11 containing vertex 0 SAT? True [3, 6, 11, 14, 17, 43, 61, 64, 67, 75]
 witness verified size 11
colour 1 K3 containing vertex 0 SAT? False
colour 2 K3 containing vertex 0 SAT? False
```
- UNSAT for K_12 in colour 3 and K_3 in colours 1 and 2.
- The encoding is not vacuous: K_11 in colour 3 is SAT, and its witness checks by hand-coded pair test (so colour 3 is tight at 11).
- Colours 1 and 2 also have no K_3 by the direct sum-free test over all distance pairs (a+b or a-b in the same set): 0 violations each.

## Author's checker as a second opinion (python3 verify_circ.py object/R_3_3_12.txt 3 3 12), run after mine
```
colour 1: degree 35, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 2: degree 40, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 3: degree 126, no K_12 (no K_11 among the neighbours of 0, exhaustive)
N 202 colours 3 forbidden 3,3,12
proves R(3,3,12) >= 203
PASS
```
Degrees agree with my sizes (distance 101 is its own inverse: 2*18-1 = 35, 2*20 = 40, 2*63 = 126; total 201 = N-1).

## Scope and caveats
- Mathematical content of the claim (the colouring is a valid 3-colouring of K_202 with the stated forbidden cliques, hence R(3,3,12) >= 203) reproduced by two independent exact methods plus the author's code; no mismatch, nothing missing, deterministic.
- I did not re-fetch DS1 or search for newer papers (outside this skeptic's scope; the NOVELTY skeptic covers it). The comparison to 194 rests on the author's table_record.md, which I only read; 203 > 194 is arithmetic on that quoted figure.
- The "exhaustive" requirement is met: both clique searches are complete (B&B and UNSAT), not samples.

pass: true
