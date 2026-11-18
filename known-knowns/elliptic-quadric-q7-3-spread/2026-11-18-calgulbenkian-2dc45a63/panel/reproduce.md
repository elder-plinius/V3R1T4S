context: Claude Code subagent, fresh context [Sonnet 5.5]

# REPRODUCE report, partial win p1 (no spread of Q^-(7,3) has an automorphism of order 3)

No downloads or fetches were made.

## 1. Own model, written before reading the package code
Quadric Q(x) = x1x2 + x3x4 + x5x6 + x7^2 + x8^2 over GF(3), enumerated from scratch (pure Python, own B and Q).
- 1066 singular projective points: confirmed.
- 22960 totally singular planes (built as 4-cliques of lines through each point, 13 points each): confirmed; every point lies on exactly 280 planes; 1066/13 = 82 planes per spread.
- |O^-(8,3)| = 2*3^12*82*8*80*728 = 40,607,874,478,080, equal to the stated |PGO^-(8,3)| (order-3 elements of PGO lie in O^-: a similitude of multiplier -1 would give multiplier -1 for its cube, but a cube equal to +-I has multiplier 1; and a lift with A^3 = I is unique up to sign).

## 2. Classes of order-3 elements (derived myself)
Order 3 in char 3 means unipotent with (A-1)^3 = 0, so Jordan blocks have size <= 3. Orthogonal groups need even blocks in pairs. Partitions of 8: 2^2 1^4, 2^4, 3 1^5, 3 2^2 1, 3^2 1^2. Even-block pairs give hyperbolic summands, so 2^4 (all hyperbolic) cannot be elliptic. Wall's invariants (forms on the multiplicity spaces of the odd blocks) with the elliptic constraint give 7 classes in O^-(8,3): 1 for 2^2 1^4, 2 for 3 1^5, 2 for 3 2^2 1, 2 for 3^2 1^2.
I sampled 4000 random elements of O^-(8,3) (products of reflections), took their 3-parts, and computed Jordan type, both Wall discriminants and the number of fixed points. Exactly those 7 classes appeared and no other (fixed points 94, 121 twice, 13 twice, 22, 4), matching the package's labels C3_94, C3_121, C3_13, C3_4, C3_22. Classes 121 and 13 each occur as an O-class pair; I verified with an explicit similitude (multiplier 2) that conjugation swaps the two members of each pair and fixes the invariants of 94, 22 and 4, so the full group has 5 classes. I searched every O-class representative except the second 13 representative, which is the image of the first under that similitude (so a spread invariant under one maps to a spread invariant under the other).
Limit: I did not independently re-count the 430,408,160 elements; completeness rests on Wall's classification plus the sampling agreement and the match with the package's five classes.

## 3. Own exact-cover search (own Python geometry plus own Knuth DLX in C, no code shared with the package)
For each representative g: rows are g-orbits of planes, valid only if the planes of the orbit are pairwise disjoint (fixed plane = 13 points, 3-orbit = 39 points); exact cover of the 1066 points. DLX was sanity-tested on Knuth's small example and on a positive control: for Q^-(5,3) (112 points, 280 lines) the same pipeline finds many g-invariant 28-line spreads for order-3 g (882 and 6480 solutions in two classes) and 0 in another.
Results on Q^-(7,3):
- fixed points 121 (both O-classes): 280 valid rows (all fixed planes), 0 solutions, refuted at the root.
- 94: 1090 rows, 0 solutions, 11 nodes.
- 22: 5842 rows, 0 solutions, 2 nodes.
- 4: 5896 rows, 0 solutions, 11 nodes.
- 13: plain DLX is infeasible (random-dive estimate about 2.6e12 nodes), so I used symmetry breaking with my own group: 40 random elements of C_O(g) built by Cayley transform from the Lie-algebra centralizer (each verified to commute with g and preserve the form). That group is transitive on all 6561 plane 3-orbits (with 37 fixed planes only, 37*13 < 1066 so a spread must contain a 3-orbit), so WLOG orbit O0 is in the spread; then Schreier stabilizers, orbit representatives of the candidates of a chosen uncovered point-orbit column at three successive levels (exhaustive over candidates up to group action). Result: 2064 tasks, all unsatisfiable, 1,767,150,367 nodes, 0 solutions, all tasks consistent (no overlap among forced rows). Runtime about 1 hour on 4 threads.
Conclusion of my own run: all 5 classes (7 O-classes) have no invariant spread: 0 solutions.

## 4. Package rerun (copy of this package in my work area)
- `sh verify-it-yourself/run_checks.sh`: all checks printed PASS, last line `PASS` (57 s). Engine 2 C3_13: EXACT UNSAT, 143 tasks, 8,776,899 branches.
- `how-we-built-it/solve_ord3_staged_swar.c`, built as in `how-we-built-it/BUILD_COMMANDS.md`: `STAGED SWAR COMPLETE: sat=0, total_tasks=144, total_nodes=8796560` (15.5 s), identical to the expected line.
No mismatch, no non-determinism, no missing object. Node counts of the two package engines match their documented values; my independent search reaches the same conclusion by different symmetry breaking.

## Verdict
The claim that no spread of Q^-(7,3) is invariant under an element of order 3 is reproduced by an independent implementation covering every conjugacy class I derived, and by both package engines. p1's "(or of order 3)" clause is met; I did not examine the order-2 part. Not claimed here: existence or nonexistence of a spread, and spreads with automorphism group of order 1 or 2.

pass: true
