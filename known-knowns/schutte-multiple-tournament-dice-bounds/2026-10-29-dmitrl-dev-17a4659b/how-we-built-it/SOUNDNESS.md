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
