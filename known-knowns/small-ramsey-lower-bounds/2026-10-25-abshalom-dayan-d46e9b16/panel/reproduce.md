context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/ 

# REPRODUCE verdict: R(3,3,14) >= 267 circulant colouring (claim p1)

Verdict: the object reproduces. Colours 1 and 2 are triangle-free and colour 3 has clique number exactly 13, so it has no K_14. Two independent exact methods agree. The author's checker was run only after mine had produced its verdict.

## Object
- `shasum -a 256 object/R_3_3_14.txt` printed `d46e9b167a93492eb02cabc1d2d9f81c975ea68698cb55944a4afac2463034ba`. This matches CLAIM.md and was unchanged on a second check at the end.
- Definition used (CLAIM.md): "edge {i,j} has the colour of the distance (j-i) mod N, and d and N-d name the same distance."
- My checker is `work/mycheck.py`. It first checks that the listed distances exactly partition 1..133 for N=266, with no gaps, repeats or out-of-range values. The assert passed. Colour sizes are {1: 22, 2: 25, 3: 86}. Degrees are 43, 50 and 172, which sum to 265 = N-1.

## Method A: own exhaustive checks (`work/mycheck.py`, `work/tri.py`)
- Colours 1 and 2 are K_3-free. The circulant test is that no a, b in the symmetric distance set has a+b mod 266 in the set. It printed `col1 K3-free True` and `col2 K3-free True`.
- I also built the full 266x266 matrix and counted monochromatic triangles directly. It printed `colour 1 edges 5719 monochromatic triangles (explicit matrix): 0` and `colour 2 edges 6650 monochromatic triangles (explicit matrix): 0`.
- Colour 3 is checked with my own branch and bound (greedy-colouring bound) over the 172 colour-3 neighbours of vertex 0. A circulant is vertex-transitive, so a maximum clique can be taken to contain vertex 0. The run explored 1943452 nodes and printed `omega(colour3) = 13 nodes 1943452 deg 172` and `K14-free: True`. A second run printed the same node count, so it is deterministic.

## Method B: SAT (`work/sat2.py`, CaDiCaL via python-sat, totalizer cardinality encoding)
The encoding is a clique among the 172 colour-3 neighbours of vertex 0. It printed:
```
need 12 more vertices beside 0 (clique size 13 ): SAT
need 13 more vertices beside 0 (clique size 14 ): UNSAT
```
This confirms omega(colour 3) = 13. The SAT result for size 13 shows the encoding can find cliques, so the UNSAT at 14 is not a vacuous encoding. The run took 1:57.

Two other attempts did not finish and are not evidence. A full-graph SAT encoding (`work/sat.py`) hit the 10-minute cap, was killed, and printed nothing. An OR-Tools CP-SAT maximisation (`work/cpsat.py`) was still running when I killed it. Neither result is used.

## Second opinion: author's checker (run after the above)
`python3 verify_circ.py object/R_3_3_14.txt 3 3 14` printed:
```
colour 1: degree 43, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 2: degree 50, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 3: degree 172, no K_14 (no K_13 among the neighbours of 0, exhaustive)
N 266 colours 3 forbidden 3,3,14
proves R(3,3,14) >= 267
PASS
```
The degrees match mine.

## Off-by-one and the table
- A colouring of K_266 without the forbidden cliques proves R(3,3,14) >= 267. That is consistent with the claim.
- The DS1 entry of 242 for the R(3,3,14) cell is taken from `table_record.md` (Table XIb, 242 in the m=14 column of the k=3 row). I did not re-fetch DS1 or search newer papers, because this skeptic covers reproduction only. 267 > 242 holds against that record, but whether anything newer exists is for the NOVELTY skeptic.

## Caveats
- The reduction to vertex 0 relies on circulant vertex-transitivity, which is exact.
- Triangle-freeness was checked both by the circulant criterion and on the explicit matrix.

pass: true
