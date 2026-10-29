# REPRODUCE skeptic: claim p2 (erdos757-sidon-in-45-sets)

context: subagent (fresh context, given only claim/)

Verdict: everything I am asked to reproduce holds. H in claim/H.json is 3-uniform, linear, F7-free and has
pairwise distinct middles in label order, with no middle at 0 or 100 (so m = 99 <= n - 2 = 99). alpha(H) = 56
exactly. The ratio 56/101 is strictly below 5/9 and 4/7 (exact fractions). I found no mismatch, no missing
object and no non-determinism.

## Order of work and inputs

1. I read claim/CLAIM.md, claim/REPRODUCE.md, claim/scout_record.md, claim/H.json (the data) and the paper
   (claim/paper/arxiv_2602.23282_v2.txt; I checked the F7 definition against the alttext in
   claim/paper/arxiv_2602.23282_v2.html).
2. I wrote my own checker from the paper's definitions and ran it to completion, twice.
3. Only then did I read claim/code/check_p2.py, claim/code/chain_build.py and claim/construction.json, and run
   them.

SHA-256 of the inputs as I read them:
- claim/H.json `6034e6cf9e482a4c15f1370cff8104c2f38282a6ffa5b38ce22a7303b8079b46`
- claim/construction.json `eacd7ef6d507e597199553c5034884b0b4b0e86ec7870d069f2596976f12531d`
- claim/code/check_p2.py `a55098176fc4ae61727691574e83f890d3971573ac375e52a56349e5db4c8189`
- claim/code/chain_build.py `bb390da856d69cde73933f605608f5b1c2e49587c588bed182caf0a09a55dfea`
- claim/paper/arxiv_2602.23282_v2.html `6b668ce63b00c5b81999adc934439b7feb2bc38daf0399f1777e37d451ac4608`
  (this matches the hash recorded in claim/scout_record.md)

My scripts and outputs are in the run folder under panel_work/reproduce/: my_check.py (the main checker),
solvers.py (library solvers, first probe), block_table.py (the transfer table), compare_build.py (rebuild
comparison), and run1.json and run2.json (the two checker runs, byte-identical, sha256
`64084310bd9f17f103fa44207b3f474a524a0675c54e154e72e607483c7be483`). Python is the run's .venv757 with `-I`.

## Definitions used (quoted from claim/paper/)

- A.P.-hypergraph (Definition 1.7): "The A.P.-hypergraph of $A$ is the $3$-uniform hypergraph $H(A)=(V,E)$ on
  vertex set $A$ whose edges are precisely the triples $\{a_{i},a_{j},a_{k}\}$ for which $a_{i},a_{j},a_{k}$ form
  a $3$-term arithmetic progression, where $1\leq i<j<k\leq n$."
- Linear (Section 2.2): "We say that a hypergraph is linear if any two distinct edges intersect in at most one
  vertex." Lemma 2.5: "If $A$ is a $(4,5)$-set, then its A.P.-hypergraph $H(A)$ is linear."
- Middles (Lemma 2.4): "For each edge $e=\{x-d,x,x+d\}\in E(H)$ with $d>0$, define its midpoint by
  $\mu(e):=x$. Then the map $\mu:E(H)\to A$ is injective. In particular, $m_{H}\leq n_{H}-2$." The proof adds:
  "$\mu(e)\notin\{a_{1},a_{n}\}$ for every $e\in E(H)$". Section 1.3 says the middles are distinct "(with
  respect to the natural order on $\mathbb{R}$)". For an abstract H, I take the label order as the order, so
  mu(e) is the median label of e, as the claim states.
- F7 (Section 1.3): "$F_{7}$ denotes the $3$-uniform hypergraph on vertex set $\{0,1,2,3,4,5,6\}$ with
  $E(F_{7})=\bigl\{\{0,1,2\},\{0,3,4\},\{0,5,6\},\{1,3,5\},\{2,4,6\}\bigr\}$". Lemma 5.2: "If $A$ is a
  $(4,5)$-set, then $H(A)$ contains no subhypergraph isomorphic to $F_{7}$." I tested non-induced containment,
  meaning any injective map of the 7 vertices that sends all 5 edges to edges of H counts. That is the stricter
  test, and it implies induced-freeness too.
- Independence number: alpha(H) is the largest vertex set that contains no edge. The paper uses
  "$\alpha(H)+\tau(H)=n_{H}$" (tau is the transversal number, the smallest vertex set meeting every edge).

The complete list of structural properties the paper proves for H(A) of a (4,5)-set: 3-uniform (Def 1.7),
distinct middles with none at the ends and m <= n-2 (Lemma 2.4), linear (Lemma 2.5), F7-free (Lemma 5.2).
Section 1.3 lists the same three restrictions. I grepped every Lemma, Theorem, Proposition and Definition in the
text extraction and found no other listed condition.

## Properties: result and method

| Property | Result | Method (all exhaustive) |
|---|---|---|
| Format | OK | n = 101, m = 99. Every edge has 3 distinct ints in 0..100. No repeated edge. No isolated vertex (degree histogram 1:3, 2:18, 3:62, 4:18). |
| 3-uniform | true | Follows from the format check. |
| Linear | true | (a) All C(99,2) = 4851 edge pairs intersect in at most 1 vertex. (b) Every vertex pair lies in at most 1 edge. 0 violations in both. |
| Distinct middles (label order) | true | 99 medians, all distinct. |
| No middle at 0 or 100 | true | No median equals 0 or 100. |
| m <= n - 2 | true (99 <= 99) | Re-derived: mu is injective into {1..99}, which has 99 elements, so m <= 99. The middles in fact fill all of {1..99}: every interior label is a middle exactly once. |
| F7-free | true | (A) My backtracking search over every injective map {0..6} -> V with all 5 F7 edges mapped onto edges of H: 0 maps. (B) networkx VF2 typed subgraph monomorphism of the F7 incidence graph into the H incidence graph: none. |

Controls, all passing:
- F7 relabelled into 20 vertices plus a noise edge: 12 maps (= |Aut(F7)| = 12, also computed directly), VF2 True.
- F7 with one edge removed: 0 maps, VF2 False.
- On 200 random small hypergraphs the two F7 methods agreed every time (16 positives).
- A non-linear pair is detected by both linearity tests.

## Exact alpha = 56

Witness (from my DP, checked by direct test that no edge lies inside it; size 56):
`[0,1,2,3,5,6,7,8,9,11,12,13,14,15,17,18,19,20,21,23,24,25,26,27,29,30,31,32,33,35,36,37,38,39,41,42,43,44,45,47,48,49,50,51,53,54,55,60,65,70,75,80,85,90,95,100]`
The CP-SAT, SCIP, RC2 and SAT witnesses (size 56) were also each checked independent.

Proof that 57 is impossible, by two independent exact methods of my own and four library solvers:

1. **My exact DP over a vertex order.** I wrote it without using the block structure. The state is the set of
   chosen vertices among decided vertices that still sit in an undecided edge. It is exact for any order. It
   gives alpha = 56 with a greedy min-frontier order (at most 112 states) and also with the reversed order (at
   most 128 states). It matched brute force on 300 random hypergraphs with n <= 14, including random orders.
2. **My block transfer method (own code, different algorithm).** The 99 edges split into 9 groups of 11
   consecutive edges. My code checks that each group's vertex set has 13 vertices, that non-adjacent groups are
   disjoint, that consecutive groups share exactly the pairs [6,96], [12,91], [18,86], [24,81], [30,76],
   [36,71], [42,66], [48,61], and that all 101 vertices are covered. It then brute-forces every block over all
   2^13 subsets for each interface assignment and combines the blocks by a max-plus product. Result: alpha = 56.
   As a hand-checkable proof (block_table.py, from claim/construction.json), let T[s][t] be the most chosen
   vertices among the block's non-anchor vertices 1..11, given the anchor state s = (x0, x12) and the out-pair
   state t = (x6, x8). Rows and columns are in the order 00, 01, 10, 11:
   `T[00] = [6,7,7,7]`, `T[01] = T[10] = T[11] = [5,6,6,6]`.
   Let f_c(t) be the best total over copies 0..c with copy c's out-pair in state t. Then f_0 = (7, 8, 8, 8), and
   f_{c+1}(00) = max(f_c(00)+6, a_c+5) = a_c+5 and f_{c+1}(t != 00) = max(f_c(00)+7, a_c+6) = a_c+6, where
   a_c = max f_c. So the pattern (a-1, a, a, a) persists and a_{c+1} = a_c + 6. Hence alpha(H_K) = 8 + 6K, and
   for K = 8 alpha = 56.
3. **CP-SAT** (8 workers): OPTIMAL, objective 56 = bound 56. Feasibility of sum >= 57: INFEASIBLE.
4. **SAT** (python-sat, CaDiCaL 1.5.3, totalizer encoding): ">= 56" is SAT with a checked witness; ">= 57" is
   UNSAT.
5. **SCIP MILP** (through OR-Tools): OPTIMAL, objective 56 = best bound 56.
6. **RC2 MaxSAT**: the minimum number of unselected vertices is 45, so alpha = 101 - 45 = 56.

A note on method: CP-SAT with a single worker did not close the gap in 120 s (FEASIBLE 56, bound 101). That is a
solver limit, not a disagreement. With 8 workers it proves optimality in under a second.

Calibration: the paper's A_base = {0,136,200,243,246,249,272,286,298,323,400,528,596,1056}.
- It is a (4,5)-set (all 1001 4-subsets checked).
- Its A.P.-hypergraph has m = 12 = n - 2 and is linear, F7-free, with distinct middles.
- alpha = 8 by my DP, CP-SAT (OPTIMAL 8/8), SCIP (8/8), RC2 (8) and SAT (>= 8 SAT, >= 9 UNSAT).
- h(A_base) = 8 by brute force over all 2^14 subsets with the Sidon definition (all x+y with x <= y distinct).
- The paper's subset {0,136,200,243,246,298,323,528} is Sidon.

## Ratio (fractions.Fraction)

- alpha/n = 56/101, already in lowest terms.
- 56/101 < 5/9: 56*9 = 504 < 505 = 5*101. True.
- 56/101 < 4/7: 392 < 404. True. Also 5/9 < 4/7, since 35 < 36.
- Consistency with the paper's lower bound: 56/101 >= 9/17, since 952 >= 909.
- Henning-Yeo (Theorem 5.3): 17*tau = 17*45 = 765 <= 5n + 3m = 802.
- Chvatal-McDiarmid (Theorem 4.6): 4*tau = 180 <= n + m = 200.
- The family has n_K = 13 + 11K and alpha_K = 8 + 6K. K = 7 gives exactly 5/9 (50/90). K = 8 is the first member
  strictly below 5/9. The family's limit is 6/11.

The live-best values (4/7 on the three named sources; 5/9 as the community record) come from
claim/scout_record.md. I could not re-fetch them, because this sandbox has no web access. The comparison above is
against those recorded values.

## Author's code (read and run after my checker)

- `chain_build.py '[block_edges as JSON]' 13 6 8 8`, run in my work folder, prints n = 13 + 11K, m = n - 2 and
  alpha_dp = 8 + 6K for K = 0..8; for K = 8 that is n 101, m 99, alpha 56, ratio 56/101.
  - Its out/chain_K8.json equals claim/H.json: same n, same edges, same order.
  - Two runs gave byte-identical output.
- My own structural check of claim/construction.json against claim/H.json:
  - Each 11-edge group is an image of block_edges under an order-preserving map.
  - Copy c+1's local vertices 0 and 12 equal copy c's p = 6 and q = 8, as the description says.
- `check_p2.py claim/H.json` prints "P2_CHECK: PASS". Every field matches mine: linear, middles, m <= n-2, F7-free
  by both methods, CP-SAT OPTIMAL 56/56, pysat UNSAT at 57, ratio 56/101. Two runs were identical apart from
  timings.
- Its F7 star search and generic backtracking search are both correct for the paper's F7.
- Minor notes, none of them a mismatch:
  - It also prints "I11_11tau<=3n+2m", which is not in the paper. It holds (495 <= 501) and is not part of the
    PASS condition.
  - It has no A_base calibration step; mine does, and it passes.
  - `int(ObjectiveValue())` could truncate a float. Not an issue here, since the bound equals 56.

## Does the paper already exhibit or exclude such an H?

From the saved paper, no.
- The only hypergraphs it exhibits are:
  - F7 (forbidden).
  - H(A_base): n = 14, alpha = 8, ratio 4/7, not below 4/7.
  - H(A_{2n+1}) for the weak Sidon sets of Section 4. These are not linear: Lemma 4.4's edges
    {X_i, X_{i+1}, Y_i} and {X_i, Y_i, Y_{i+1}} share two vertices. I confirmed this computationally for A_7.
- The only exclusion is Theorem 5.3 with Lemma 2.4, which gives alpha >= 9n/17 (directly, tau <= (5n+3m)/17).
  For n = 101 and m = 99 that forces alpha >= 54. H has 56, so it is not excluded.

Scope: H is an abstract target. The claim does not say H is the A.P.-hypergraph of a (4,5)-set, and so H by
itself gives no upper bound on c*. That matches the p2 wording.

## Mismatches

None.

pass: true
