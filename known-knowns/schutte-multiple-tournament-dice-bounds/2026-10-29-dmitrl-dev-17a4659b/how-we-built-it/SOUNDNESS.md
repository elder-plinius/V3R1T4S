# Soundness note: the CNF for "two tournaments on 13 vertices with every 5-subset dominated"

Contributor text. The CNF is produced by `encode_schutte.py 2 5 13 --sb global3`
(header `p cnf 42644 148931`, sha256 247ca74489c8144e2eca1fa1b7bfdd6c2f7f826e7deac2c46e4b3748c7069626). This note argues (1) the base formula F says exactly what Definition 2.2
asks, and (2) every added clause is sound: if some S_5 set of two tournaments on 13 vertices existed, a relabelled
copy of it would satisfy F and all added clauses. Hence UNSAT of the CNF proves that no such pair exists.

## Definition (arXiv:2604.08790, Definitions 2.1 and 2.2)
A set of m labelled tournaments on one vertex set V has property S_k if for every k-set U of V there are a tournament
T_i and a vertex u with u -> U in T_i (u beats every vertex of U, so u is outside U). f(m,k) is the minimum |V| for
which such a set of m tournaments exists.

## 1. The base formula F(m,k,n)
- Edge variables e(t,i,j), t = 0..m-1, 0 <= i < j <= n-1, numbered 1, 2, ... in the order t, i, j (t slowest);
  e(t,i,j) true means i -> j in T_t, false means j -> i. Assignments of the edge variables and tuples of m tournaments
  on {0..n-1} correspond one to one. lit(t,v,u) is e(t,v,u) if v < u and -e(t,u,v) if v > u ("v beats u in T_t").
- For every k-subset U and every (t, v) with v not in U, a variable d(t,v,U) with the k clauses (-d(t,v,U), lit(t,v,u))
  for u in U; and for every U the clause OR of d(t,v,U) over all t and all v not in U.
- F is satisfiable exactly when an S_k set of m tournaments on n vertices exists: from such a tuple set d(t,v,U) true
  iff v -> U in T_t; conversely a model gives, for each U, a true d(t,v,U), whose binary clauses force v -> U in T_t.
- verify-it-yourself/cnf_audit.py re-derives this from the clauses alone (stdlib): each domination clause has the
  m(n-k) candidates of one k-set, each candidate variable has exactly the k defining clauses and occurs nowhere else,
  and the k-sets are all C(n,k) subsets once each.

## 2. Added clauses (symmetry breaking), with d = out-degree of vertex 0 in T_0
(a) (-lit(0,0,u+1), lit(0,0,u)) for u = 1..n-2: the out-neighbourhood of 0 in T_0 is {1..d}.
(c) the units lit(0,0,u), u = 1..k: d >= k.
(b) for D = k..n-2, every t and every v: a Sinz sequential counter "at most D of the n-1 literals lit(t,v,u), u != v",
    whose overflow clauses carry the extra literals -lit(0,0,D) and lit(0,0,D+1). Under (a) both extra literals are
    false exactly when d = D, so (b) says: when d < n-1, every vertex of every tournament has out-degree <= d.
    The other counter clauses only force register bits upwards ("at least j+1 of the first i+1 literals"), so they
    are satisfied by the exact counts and never restrict the edge variables.
(n) only when d = n-1 (every nested clause carries the literal -lit(0,0,n-1)), on V' = {1..n-1} and T_1..T_(m-1):
    (-lit(1,1,u+1), lit(1,1,u)) for u = 2..n-2 (the out-neighbourhood of 1 in T_1 inside V' is {2..d'+1});
    units lit(1,1,u) for u = 2..k (d' >= k-1); and for D' = k-1..n-3, every t >= 1 and v in V', an "at most D'"
    counter over lit(t,v,u), u in V' - {v}, whose overflow clauses also carry -lit(1,1,D'+1) and lit(1,1,D'+2).
(l) only when d = D < n-1 (clauses carry -lit(0,0,D) and lit(0,0,D+1)), with w = D+1:
    (-lit(0,w,u+1), lit(0,w,u)) for u = 1..D-1 and for u = D+2..n-2: the out-neighbourhood of w in T_0 is an initial
    segment of {1..D} and an initial segment of {D+2..n-1}.
(s) only for m >= 3 (absent here, m = 2): (lit(1,0,1), -lit(2,0,1), lit(0,0,n-1)).

## 2a. Where each family sits in the CNF (clause indices)
Clause i is the i-th clause after the `p cnf 42644 148931` line of the CNF (sha256
247ca74489c8144e2eca1fa1b7bfdd6c2f7f826e7deac2c46e4b3748c7069626), counting from 1; these are also the LRAT ids of the
input clauses. The families follow each other in this order and cover clauses 1..148931 without gaps; "new
variables" are the auxiliary variables a family introduces (counter registers). Each counter is the Sinz sequential
counter of verify-it-yourself/encode_schutte.py (function at_most) over its literals in increasing order of u; only
its overflow clauses carry the extra literals, and its other clauses only push register bits upward. The ranges come
from replaying the encoder's construction order, which reproduces the encoder's clause list exactly. The first and
last clause of every non-counter family, the overflow clauses of every counter group and the layout of the base
clauses were also checked against the CNF file itself.

| family | clauses | count | new variables | clauses in the range |
|---|---|---|---|---|
| base F(2,5,13) | 1..104247 | 104247 | 1..20748 | for each of the 1287 5-subsets U in lexicographic order, 81 consecutive clauses: for each of the 16 candidates (t = 0, 1; v not in U, ascending) its 5 defining clauses (-d(t,v,U), lit(t,v,u)), u in U ascending; then the domination clause, the OR of the 16 d(t,v,U). Edge variables 1..78 (T_0) and 79..156 (T_1); d variables 157..20748 |
| (a) | 104248..104258 | 11 | - | (-lit(0,0,u+1), lit(0,0,u)) for u = 1..11 |
| (c) | 104259..104263 | 5 | - | units lit(0,0,u) for u = 1..5 |
| (b) D = 5 | 104264..107279 | 3016 | 20749..22178 | 26 counters "at most 5 of lit(t,v,u), u != v", for (t, v) = (0,0), (0,1), .., (1,12) in that order, 116 clauses each; the 11 overflow clauses of each carry -lit(0,0,5) and lit(0,0,6) |
| (b) D = 6 | 107280..110841 | 3562 | 22179..23894 | 26 counters "at most 6 of lit(t,v,u), u != v", for (t, v) = (0,0), (0,1), .., (1,12) in that order, 137 clauses each; the 11 overflow clauses of each carry -lit(0,0,6) and lit(0,0,7) |
| (b) D = 7 | 110842..114949 | 4108 | 23895..25896 | 26 counters "at most 7 of lit(t,v,u), u != v", for (t, v) = (0,0), (0,1), .., (1,12) in that order, 158 clauses each; the 11 overflow clauses of each carry -lit(0,0,7) and lit(0,0,8) |
| (b) D = 8 | 114950..119603 | 4654 | 25897..28184 | 26 counters "at most 8 of lit(t,v,u), u != v", for (t, v) = (0,0), (0,1), .., (1,12) in that order, 179 clauses each; the 11 overflow clauses of each carry -lit(0,0,8) and lit(0,0,9) |
| (b) D = 9 | 119604..124803 | 5200 | 28185..30758 | 26 counters "at most 9 of lit(t,v,u), u != v", for (t, v) = (0,0), (0,1), .., (1,12) in that order, 200 clauses each; the 11 overflow clauses of each carry -lit(0,0,9) and lit(0,0,10) |
| (b) D = 10 | 124804..130549 | 5746 | 30759..33618 | 26 counters "at most 10 of lit(t,v,u), u != v", for (t, v) = (0,0), (0,1), .., (1,12) in that order, 221 clauses each; the 11 overflow clauses of each carry -lit(0,0,10) and lit(0,0,11) |
| (b) D = 11 | 130550..136841 | 6292 | 33619..36764 | 26 counters "at most 11 of lit(t,v,u), u != v", for (t, v) = (0,0), (0,1), .., (1,12) in that order, 242 clauses each; the 11 overflow clauses of each carry -lit(0,0,11) and lit(0,0,12) |
| (n) initial segment | 136842..136851 | 10 | - | (-lit(1,1,u+1), lit(1,1,u), -lit(0,0,12)) for u = 2..11 |
| (n) units | 136852..136855 | 4 | - | (lit(1,1,u), -lit(0,0,12)) for u = 2..5 |
| (n) counters D' = 4 | 136856..137887 | 1032 | 36765..37244 | 12 counters "at most 4 of lit(1,v,u), u in {1..12} - {v}", for v = 1..12 in that order, 86 clauses each; the 10 overflow clauses of each carry -lit(0,0,12), -lit(1,1,5) and lit(1,1,6) |
| (n) counters D' = 5 | 137888..139147 | 1260 | 37245..37844 | 12 counters "at most 5 of lit(1,v,u), u in {1..12} - {v}", for v = 1..12 in that order, 105 clauses each; the 10 overflow clauses of each carry -lit(0,0,12), -lit(1,1,6) and lit(1,1,7) |
| (n) counters D' = 6 | 139148..140635 | 1488 | 37845..38564 | 12 counters "at most 6 of lit(1,v,u), u in {1..12} - {v}", for v = 1..12 in that order, 124 clauses each; the 10 overflow clauses of each carry -lit(0,0,12), -lit(1,1,7) and lit(1,1,8) |
| (n) counters D' = 7 | 140636..142351 | 1716 | 38565..39404 | 12 counters "at most 7 of lit(1,v,u), u in {1..12} - {v}", for v = 1..12 in that order, 143 clauses each; the 10 overflow clauses of each carry -lit(0,0,12), -lit(1,1,8) and lit(1,1,9) |
| (n) counters D' = 8 | 142352..144295 | 1944 | 39405..40364 | 12 counters "at most 8 of lit(1,v,u), u in {1..12} - {v}", for v = 1..12 in that order, 162 clauses each; the 10 overflow clauses of each carry -lit(0,0,12), -lit(1,1,9) and lit(1,1,10) |
| (n) counters D' = 9 | 144296..146467 | 2172 | 40365..41444 | 12 counters "at most 9 of lit(1,v,u), u in {1..12} - {v}", for v = 1..12 in that order, 181 clauses each; the 10 overflow clauses of each carry -lit(0,0,12), -lit(1,1,10) and lit(1,1,11) |
| (n) counters D' = 10 | 146468..148867 | 2400 | 41445..42644 | 12 counters "at most 10 of lit(1,v,u), u in {1..12} - {v}", for v = 1..12 in that order, 200 clauses each; the 10 overflow clauses of each carry -lit(0,0,12), -lit(1,1,11) and lit(1,1,12) |
| (l) D = 5 | 148868..148876 | 9 | - | (-lit(0,6,u+1), lit(0,6,u), -lit(0,0,5), lit(0,0,6)) for u = 1..4 (block {1..5}) and u = 7..11 (block {7..12}) |
| (l) D = 6 | 148877..148885 | 9 | - | (-lit(0,7,u+1), lit(0,7,u), -lit(0,0,6), lit(0,0,7)) for u = 1..5 (block {1..6}) and u = 8..11 (block {8..12}) |
| (l) D = 7 | 148886..148894 | 9 | - | (-lit(0,8,u+1), lit(0,8,u), -lit(0,0,7), lit(0,0,8)) for u = 1..6 (block {1..7}) and u = 9..11 (block {9..12}) |
| (l) D = 8 | 148895..148903 | 9 | - | (-lit(0,9,u+1), lit(0,9,u), -lit(0,0,8), lit(0,0,9)) for u = 1..7 (block {1..8}) and u = 10..11 (block {10..12}) |
| (l) D = 9 | 148904..148912 | 9 | - | (-lit(0,10,u+1), lit(0,10,u), -lit(0,0,9), lit(0,0,10)) for u = 1..8 (block {1..9}) and u = 11..11 (block {11..12}) |
| (l) D = 10 | 148913..148921 | 9 | - | (-lit(0,11,u+1), lit(0,11,u), -lit(0,0,10), lit(0,0,11)) for u = 1..9 (block {1..10}; the block {12} has no pair) |
| (l) D = 11 | 148922..148931 | 10 | - | (-lit(0,12,u+1), lit(0,12,u), -lit(0,0,11), lit(0,0,12)) for u = 1..10 (block {1..11}; the second block is empty) |
| (s) | - | 0 | - | absent (m = 2) |

## 3. Why the added clauses are sound
Take any S_k set of m tournaments on n vertices (n >= k+1). Relabelling vertices and reordering tournaments keep
property S_k and all out-degrees.
1. Pick (t*, v*) of largest out-degree D* over all tournaments and vertices. Some vertex dominates some k-set, so
   D* >= k. Move t* to position 0; relabel v* as 0, its out-neighbours in T_0 as 1..D*, its in-neighbours as
   D*+1..n-1 (orders chosen below). Then (a) and (c) hold, d = D*, and (b) holds because D* is the maximum.
2. If D* < n-1: let w be any in-neighbour of 0 and give it label D*+1. Order {1..D*} and the remaining in-neighbours
   (labels D*+2..n-1) so that the out-neighbours of w in T_0 come first inside each block. These choices fix vertex
   0, the set {1..D*} and w, so steps 1 and (a), (b), (c) are unaffected, and (l) holds. (n) is void (d < n-1). For
   m >= 3, if lit(2,0,1) holds and lit(1,0,1) does not, swap T_1 and T_2; no other added clause distinguishes them
   when d < n-1, so (s) holds.
3. If D* = n-1: vertex 0 beats everyone in T_0, so every k-set {0} + W (W a (k-1)-subset of V') is dominated by some
   v that beats 0, hence in some T_t with t >= 1, and v -> W there: some (t >= 1, v in V') has out-degree >= k-1
   inside V'. Pick a maximiser (t', v') of the out-degree inside V' over t >= 1, value D' >= k-1; move t' to
   position 1 (among T_1..T_(m-1)) and relabel inside V' so that v' = 1 and its out-neighbours inside V' are 2..D'+1.
   This fixes 0 and keeps "0 beats everyone in T_0", so (a), (c) still hold and (b), (l), (s) are void; (n) holds.
how-we-built-it/sb_audit.py implements this procedure as a randomised test on random tuples.

## 4. Monotonicity: order 13 settles f(2,5) >= 14
If an S_k set of m tournaments on n >= k+1 vertices exists, one on n+1 vertices exists: add a vertex w that loses to
everyone in every tournament. A k-set without w keeps its dominator. For a k-set U containing w, extend U - {w} by
an old vertex x outside it to a k-set of old vertices; its dominator v is an old vertex outside that set, so v is
outside U, beats U - {w} and beats w. So no S_5 pair on 13 vertices means none on 6..12 vertices either, and
f(2,5) >= 14. Figure 7 of arXiv:2604.08790 (Proposition 2.3 applied to two order-7 Paley tournaments; object
upper_bound_m2k5n14.json) gives f(2,5) <= 14.
