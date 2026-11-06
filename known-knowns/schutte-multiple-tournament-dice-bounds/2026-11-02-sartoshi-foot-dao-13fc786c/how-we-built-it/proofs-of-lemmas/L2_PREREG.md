# PREREG (run 2026-10-27-0844), written before any cube code
Criterion: see target.md (verbatim). Claim rule unchanged from run 0745: a witness is m adjacency matrices passing attempts/*/code/checker.py
(checker validated in run 0745 on Paley-7 positive / transitive-7 negative; re-validated here). UNSAT is uncertified and never a claim.
null_test: required
Null design: 400 random tuples per cell through the checker, all must be rejected (undominated>0); also the solver pipeline must say UNSAT/not-SAT on 0 of the
known-SAT calibration instances (below). Written to null_test.md.

## Cube cover for (3,6,12) (sound argument)
Let T_1,T_2,T_3 be any S_6 triple on V={0..11}. Among all 36 (tournament, vertex) pairs choose one with maximum out-degree d (d>=6 as the mean is 5.5).
Permute tournament indices so it lies in T_1, relabel vertices so it is vertex 0 and its out-neighbours are 1..d (applying one vertex permutation to all
three tournaments keeps S_6, as does permuting tournaments). Now every vertex has out-degree <= d in every tournament, and 0 beats exactly 1..d in T_1.
Blocks A={1..d}, B={d+1..11}. Any relabelling inside A and inside B keeps vertex 0's T_1 row. In T_2 vertex 0 beats a vertices of A and b of B; relabel within
the blocks so these are 1..a and d+1..d+b. Constraint a+b<=d (max-degree). So the cubes are (d,a,b), 6<=d<=11, 0<=a<=d, 0<=b<=11-d, a+b<=d, and each cube's CNF is:
base encoding + out-degree(T_1,0)=d, T_2 row of vertex 0 as stated, out-degree<=d for all vertices in all tournaments. Every S_6 triple satisfies some cube, so
all cubes UNSAT => no S_6 triple on 12 vertices (f(3,6)>=13), uncertified. Calibration of the cube machinery: d=11 as a whole is UNSAT from run 0745 (CaDiCaL 1171 s), so all d=11 cubes must be UNSAT.
Level 2 (only for a cube that times out at the cap; never rerun at a bigger cap): in T_3, within each of the four blocks {1..a},{a+1..d},{d+1..d+b},{d+b+1..11},
vertex 0's out-neighbours form a prefix (relabelling inside blocks fixes all earlier constraints); sub-cubes (c1..c4), c_i from 0 to block size, with c1+..+c4<=d.
## Execution
One subprocess per cube, nice 15, hard cap 1200 s by perl alarm, 8 workers, CaDiCaL 1.5.3 (pysat). Ledger attempts/solver/ledger_m3k6n12.tsv (cube id, solver, cap, start UTC,
PID, result SAT|UNSAT|TIMEOUT|KILLED, seconds). A run starts from the ledger. Order: d=11, 10, 9, 8, 7, 6, within d by a+b. Nothing launched after 11:08 UTC (80% of 3 h from 08:44);
running workers are then killed by recorded PID and marked KILLED. SAT cube: write matrices, run checker, repeat PR search, panel if time.
Proof logging: not done in cubes (no checker allowed under rule 10; pysat keeps proofs in memory, unbounded). Stated plainly in the report.
## Calibration, before the cubes count
(1,2,7) SAT and (1,2,6) UNSAT; (2,4,10) SAT, (2,4,9) UNSAT; known-SAT (2,5,14) and (3,6,13) with checker acceptance (capped 10 min each, a TIMEOUT is reported as such, not as failure of the encoder);
cube machinery on a small cell: all cubes of (2,4,9) (d=4..8 analogue) must be UNSAT and of (2,4,10) at least one SAT.
