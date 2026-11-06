# Soundness note: encoding and cube cover (to be checked by a skeptic against Definition 2.2)
Definition 2.2 (Jeffries, arXiv:2604.08790): tournaments T_1..T_m on a vertex set V are an S_k set if for every k-subset U of V there are t in 1..m and v in V\U
with v->u in T_t for every u in U. f(m,k) is the least |V| (with |V| >= k+1) admitting one.

1. Encoding (attempts/solver/code/cube.py `build`). Variable x[t,i,j] (i<j) is true iff i->j in T_t; "v beats u in t" is x[t,v,u] if v<u else not x[t,u,v]. One
   boolean per unordered pair per tournament makes each T_t a loop-free tournament (exactly one arc per pair) by construction. For each U, t, v not in U there is an auxiliary
   d(U,t,v) with clauses (not d or "v beats u in t") for all u in U, and one clause per U: OR of all d(U,t,v). A model gives a dominating (t,v) for every U; conversely
   a S_k set sets d(U,t,v) true for a dominating pair. So satisfiable iff an S_k set exists (one direction of d <-> conjunction suffices). The pitfall (t and v chosen
   per element instead of per subset) cannot occur because d is indexed by (U,t,v) and implies all of U.
2. Symmetries used. (i) A permutation of the vertex set applied to all m tournaments preserves S_k (U maps to a k-subset, dominating v maps to the image vertex). (ii) A permutation of the
   tournament indices preserves S_k (the quantifier over t is symmetric).
3. Cover. Let (T_1..T_m) be S_k on n vertices. Choose (t,v) maximising out-degree d over all m*n pairs; d >= ceil((n-1)/2) (mean degree of a tournament). By (ii) move t to index 1; by (i) relabel
   v as 0 and its T_1-out-neighbours as 1..d. Every out-degree in every tournament is now <= d. Let A={1..d}, B={d+1..n-1}; a relabelling that permutes A and B internally fixes
   all that was established (0's T_1 row is {1..d} as a set, degrees are unchanged). Using it, order T_2's out-neighbours of 0: a of them in A become 1..a, b of them in B become d+1..d+b.
   Hence (T_1,T_2,..) satisfies the cube (d,a,b) CNF: T_1 row of 0 = exactly 1..d, T_2 row of 0 = exactly 1..a and d+1..d+b, out-degree <= d everywhere (seqcounter at-most constraints), plus the base encoding.
   Cubes range over d from ceil((n-1)/2) to n-1, a in 0..d, b in 0..n-1-d, a+b <= d. (a, b are also bounded by the block sizes d and n-1-d.) Therefore the cubes cover all S_k sets, and "all cubes UNSAT" implies no S_k set on n vertices.
   This uses m >= 2 (cube fixes T_2); for m = 1 there is no T_2.
4. Empirical checks (not proofs): cover_check.out (516 distinct S_k sets of four small cells, each relabelled by the procedure above, passes the independent checker and satisfies
   its cube CNF as a model); witness_in_cube.out and knownsat_*: the composition witnesses at (2,5,14) and (3,6,13) land in cubes (10,0,0) and (11,7,0), and cube.py returns SAT on exactly those cubes with checker undominated 0;
   calibration: all 75 cubes of (2,4,9) UNSAT, 4 cubes of (2,4,10) SAT.
5. Not shown here: a proof certificate for any UNSAT cube. "UNSAT" below means one CaDiCaL 1.5.3 run said so; an encoder bug would be invisible to repeated solver runs. Only a DRAT/LRAT proof and a verified checker (rule 10: not installable here) would give p1.
