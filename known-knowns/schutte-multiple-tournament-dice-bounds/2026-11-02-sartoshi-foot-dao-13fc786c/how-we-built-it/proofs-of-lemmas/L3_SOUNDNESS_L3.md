# Soundness of level 3 (written before the first level-3 job; to be checked by a skeptic against Definition 2.2)
Setting: (3,6,12), cube (d,a,b), level-2 sub-cube c=(c1..c4), PREREG.v2 order constraint, exactly as in run 0844's SOUNDNESS_NOTE.md. Claim: every S_6 triple that satisfies the sub-cube's
CNF, after one more relabelling, satisfies the CNF of exactly one level-3 cube (e,a',b') of the same parent; hence "all level-3 cubes UNSAT" implies the parent sub-cube is UNSAT.

1. Invariance. The parent CNF consists of: Definition 2.2 clauses (invariant under any vertex permutation applied to all three tournaments, symmetry (i) of the note); out-degree <= d for every vertex in every
   tournament (invariant under vertex permutations); vertex 0's rows in T_1, T_2, T_3 given as explicit sets (the four blocks of the cube, T_3 as prefixes of lengths c_i inside each block); the v2 degree bound on vertex 0's T_3 row.
   Let a *cell* be a maximal interval of vertices 1..11 on which all three of vertex 0's rows are constant (the four blocks, each cut after its c_i-th element; cells are intervals by construction).
   A permutation of vertices that fixes 0 and maps each cell to itself leaves all three rows of vertex 0 unchanged as sets, so it maps models of the parent CNF to models of the parent CNF.
2. Choice of cell. C = the largest cell, ties broken by smallest first vertex: a function of (d,a,b,c) only, so every model of the parent uses the same C. Let z=|C| >= 3 and s its first vertex.
3. Pivot. In T_1 restricted to C (a tournament on z vertices) let e be the maximum out-degree inside C and pick p in C attaining it. The mean out-degree in a tournament on z vertices is (z-1)/2, so e >= (z-1)/2, i.e. e >= ceil((z-1)/2) = z//2,
   and e <= z-1. Relabel within C so that p is vertex s and p's T_1 out-neighbours inside C are s+1..s+e (any permutation of C is allowed by (1); doing it in two steps - move p to s, then permute the remaining z-1 vertices
   keeping the out-set and in-set of p as sets - is a permutation of C).
4. Second split. A' = {s+1..s+e}, B' = {s+e+1..s+z-1}. In T_2, p beats a' vertices of A' and b' of B' (0<=a'<=e, 0<=b'<=z-1-e). A permutation inside A' and inside B' fixes p's T_1 row inside C (as sets), vertex 0's rows (it stays inside the cell)
   and p itself, so we can relabel so that p's T_2 out-neighbours are s+1..s+a' and s+e+1..s+e+b'. (T_3 for p is left free.)
5. Result. The relabelled triple satisfies: the parent CNF (by 1); T_1 row of p within C exactly s+1..s+e; T_2 row of p within C exactly the two prefixes; for every u in C, T_1 out-degree inside C <= e (p was a maximiser).
   That is the CNF of cube3.build3 / add_l3 for (e,a',b'). The (e,a',b') range over e in [z//2, z-1], a' in [0,e], b' in [0,z-1-e], which is what cube3.l3_params enumerates. The cubes therefore cover.
6. Not used: no constraint on p's T_3 row, no constraint tying p to the global degree bound beyond the existing out-degree <= d clauses.
Empirical check (not proof): cover_check_l3.py relabels sampled S_k sets of small cells through levels 1-3 and asserts the level-3 CNF accepts them.
