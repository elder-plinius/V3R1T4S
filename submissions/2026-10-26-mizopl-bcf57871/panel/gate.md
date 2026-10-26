# Panel Gate — `conway-99-graph` (`2026-10-26-0516`)

status: CONFIRMED_PARTIAL_WIN
target_id: conway-99-graph
tracks: p2 + p1
reproduce: pass
novelty: pass
criterion: pass
confirmed_scope: Dual-encoded pure-RUP LRAT (0 RAT lemmas) machine-checked UNSAT certificates across two independent SAT cardinality encodings (Encoding A = Sinz 2005 Sequential Counter, Encoding B = Bailleux & Boufkhad 2003 Binary Tree Totalizer) for (1) all 5 forced-structure reduction propositions (p2_1 through p2_5) of Thakkar & Severini (arXiv:2608.11211), including positive SAT non-vacuity on srg(9, 4, 1, 2) = K_3 box K_3 (Track p2), and (2) 22 prime-order and subgroup automorphism exclusions on srg(99, 14, 1, 2) fixing a root vertex x—resolving the last open prime order p=7 with 1 fixed vertex and 14 7-cycles (p7_fix1) from Cesarz & Woldar (arXiv:2308.02978, 2023) and Thakkar & Severini (arXiv:2608.11211, 2026), together with prime order p=5 with 9 fixed vertices and 18 5-cycles (p5_t1_fix9), prime order p=3 with 33 fixed vertices and 22 3-cycles (p3_t1_fix33), the order-21 Frobenius group Frob(21) = Z_7 x| Z_3 (frob21_z7_z3), and 18 of the 19 prime-order p=2 involution profiles across (0,1,6), (0,2,5), (0,3,4), (0,4,3), (0,5,2), (0,6,1), (1,0,5), (1,1,4), (1,2,3), (1,3,2), (1,4,1), (1,5,0), (2,0,3), (2,1,2), (2,2,1), (2,3,0), (3,0,1), and (3,1,0) (Track p1)—totalling 27 theorems and 54 proofs (92,259 RUP steps, 0 RAT lemmas) verified from freshly generated CNF clauses in ~18 seconds by a standalone pure-Python LRAT RUP proof checker.
