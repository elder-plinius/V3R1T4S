context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/ 

# REPRODUCE verdict: R(3,3,15) >= 272 colouring (object/R_3_3_15.txt)

Scope: I re-checked the object (no K_3 in colour 1, no K_3 in colour 2, no K_15 in colour 3, N = 271). Whether 272 beats the literature (DS1 269, newer papers) is the NOVELTY skeptic's job; I did not search the web.

## Object
`shasum -a 256 object/R_3_3_15.txt` -> `4e457e7ee1232a6b4c5ea299b7616c6e4329f04ba11531cadacd4a0d715e9ca7` (matches CLAIM.md). Header `matrix 271 3`, 271 rows of 271 digits.

## My checker (written before opening verify_join.py): work/chk2.py
Definition used: colour classes are the graphs G_c on {i,j} with M[i][j]=c; need omega(G_1)<3, omega(G_2)<3, omega(G_3)<15.
Output:
```
valid matrix                         (square, symmetric, diagonal 0, off-diagonal in {1,2,3})
colour 1 triangles: 0 edges 5724
colour 2 triangles: 0 edges 6655
old part circulant mod 266: True
block has colour-3 edge: False
block-old edges all colour 3: True
colour3 degree of 0 in old: 172
max colour-3 clique in old part containing vertex 0: 13 nodes 1130444 sec 5.1
```
Triangles in colours 1 and 2 were enumerated over all triples (every edge), not sampled.
Colour 3 argument, each step checked from the file: vertices 0..265 are circulant (checked for all pairs), so the graph is vertex-transitive and every clique can be rotated to contain 0; exhaustive branch and bound (greedy-colouring bound) over cliques through 0 gives clique number 13 there. The block 266..270 has no colour-3 edge, so a colour-3 clique holds at most 1 block vertex. Hence omega(G_3) <= 13 + 1 = 14 < 15.

## Second exact method: SAT (work/sat.py, python-sat CaDiCaL)
Encoding: x_v for v in 0..265, conflict clause for every pair not coloured 3, x_0 forced (justified by the circulant check), at-least-14 sequential counter.
```
old size>= 14 UNSAT sec 281.2
```
So no colour-3 K_14 in 0..265 through vertex 0, hence none at all, agreeing with the branch and bound (13). Combined with the block argument: no colour-3 K_15.

## Author's checker as second opinion (run after my verdict)
`python3 -I verify_join.py object/R_3_3_15.txt 266`, run twice, identical output both times (determinism OK), ending:
```
colour 1: 5724 edges, no triangle (every edge checked)
colour 2: 6655 edges, no triangle (every edge checked)
colour 3 on vertices 0..265 (circulant, verified): clique number 13 (exhaustive through vertex 0)
colour 3 clique number = 14; witness of size 14: [0, 264, 261, 246, 242, 249, 189, 186, 83, 86, 33, 30, 2, 266]
N 271: no K_3 in colour 1, no K_3 in colour 2, no K_15 in colour 3
proves R(3,3,15) >= 272
PASS
```
Edge counts agree with mine (5724, 6655).

## Caveats
- I did not run a structure-blind branch and bound on the whole 271-vertex colour-3 graph; my first attempt was too slow and I killed it (it was started several times by mistake, all copies killed; no result from it is used). The full-graph conclusion rests on the checked structure (circulant part, block without colour-3 edges) plus the exhaustive and SAT results above.
- Off-by-one: a valid colouring of K_271 gives R(3,3,15) >= 272, as claimed.

Verdict: every property and the claimed value reproduce by two independent exact methods; no mismatch, no missing object, no non-determinism seen.

pass: true
