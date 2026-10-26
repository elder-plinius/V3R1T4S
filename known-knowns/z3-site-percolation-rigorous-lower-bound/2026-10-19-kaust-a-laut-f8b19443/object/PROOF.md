# Proof that p_c^site(Z^3) >= 263376/10^6

## 0. Setting
Site percolation on Z^3 (nearest-neighbour graph) with parameter p: under P_p the sites are open independently
with probability p. C(0) is the open cluster of 0 (empty if 0 is closed), theta(p) = P_p(|C(0)| = infinity), and
p_c = sup{p : theta(p) = 0}. theta is nondecreasing in p (standard monotone coupling). For x in C(0), d(x) is the
graph distance from 0 inside the subgraph of Z^3 induced by the open sites (finite, since C(0) is connected).
Directions e_0, ..., e_5 = +x, -x, +y, -y, +z, -z; dirindex(e_i) = i. For neighbours a ~ b, dirindex(b - a) is
"the direction index of b seen from a". A neighbour-avoiding walk (NAW) is a walk v_0, ..., v_N with v_i ~ v_j only
for |i - j| = 1 (in particular it is self-avoiding).

## 1. The parent tree and tree paths
For x in C(0) \ {0} with d(x) = k >= 1, the set P(x) = {w ~ x : w in C(0), d(w) = k - 1} is nonempty (the
second-to-last vertex of a shortest path). parent(x) is the element of P(x) with the smallest direction index seen
from x; it is unique because distinct neighbours of x lie in distinct directions. Following parents decreases d by
one, so the parent pointers form a tree T on C(0) rooted at 0, in which every vertex has at most 6 children. A tree
path of length N is a sequence v_0 = 0, v_1, ..., v_N with parent(v_{k+1}) = v_k for 0 <= k < N.

For any N-step NAW gamma = (v_0, ..., v_N) from 0 define the set F(gamma) = S(gamma) u C(gamma), where
- S(gamma) = { w not in gamma : w ~ v_i and w ~ v_j for some i, j with j - i >= 3 } (shortcut sites);
- C(gamma) = { u_k : 1 <= k <= N - 1, v_{k+1} - v_k != v_k - v_{k-1} (a turn), and
  dirindex(u_k - v_{k+1}) < dirindex(v_k - v_{k+1}) }, where u_k = v_{k-1} + v_{k+1} - v_k (turn corners);
and E(gamma) = { y ~ v_N : y not in gamma, y adjacent to no v_i with i < N, y not in F(gamma) }.

Lemma 0. For every NAW gamma, F(gamma) and gamma are disjoint.
Proof. S(gamma) excludes gamma by definition. At a turn, v_{k+1} - v_k is a unit vector different from
+-(v_k - v_{k-1}) (not equal: a turn; not opposite: v_{k+1} != v_{k-1}), so u_k - v_{k-1} = v_{k+1} - v_k and
u_k - v_{k+1} = v_{k-1} - v_k are unit vectors: u_k ~ v_{k-1} and u_k ~ v_{k+1}. If u_k = v_m, the NAW property gives
|m - (k-1)| <= 1 and |m - (k+1)| <= 1, so m = k, but u_k != v_k. []

Lemma 1. Let gamma = (v_0, ..., v_N) be a tree path. Then (a) every v_k is open and d(v_k) = k; (b) gamma is a NAW;
(c) every site of F(gamma) is closed.
Proof. (a) Induction along the path: v_{k+1} is in C(0) and d(v_{k+1}) = d(parent(v_{k+1})) + 1.
(b) If v_i ~ v_j with j >= i + 2, both are open, so d(v_j) <= d(v_i) + 1 = i + 1 < j, contradicting (a).
(c) Shortcut sites: if w in S(gamma) were open, then w in C(0) (it neighbours v_i), d(w) <= i + 1, and
d(v_j) <= i + 2 < i + 3 <= j, contradicting (a). Turn corners: let u = u_k in C(gamma); u ~ v_{k-1} and
u ~ v_{k+1} (proof of Lemma 0). If u were open, then u in C(0), d(u) <= d(v_{k-1}) + 1 = k, and
k + 1 = d(v_{k+1}) <= d(u) + 1, so d(u) = k and u in P(v_{k+1}). Also v_k in P(v_{k+1}). Since u has the smaller
direction index seen from v_{k+1}, parent(v_{k+1}) != v_k, contradicting the tree path. []

## 2. The finite criterion
For a NAW gamma and y in E(gamma), let A_gamma = {every site of gamma is open} n {every site of F(gamma) is closed},
and B_{gamma,y} = {y is open, and some infinite self-avoiding path of open sites starts at y and stays in
Z^3 \ (gamma u F(gamma))}.

Lemma 2. If |C(0)| = infinity, then for every N there are a tree path gamma of length N and y in E(gamma) such
that A_gamma and B_{gamma,y} both hold.
Proof. T is infinite and locally finite, so by Konig's lemma it has an infinite ray 0 = v_0, v_1, v_2, ... with
parent(v_{m+1}) = v_m. Put gamma = (v_0, ..., v_N), y = v_{N+1}. gamma is a tree path, so A_gamma holds (Lemma 1).
(v_0, ..., v_{N+1}) is also a tree path, hence a NAW: y is not in gamma and is adjacent to no v_i with i < N; y is
open, so y is not in F(gamma) (closed by Lemma 1(c)); thus y in E(gamma). The sites v_m, m >= N + 1, are open and
distinct, have d(v_m) = m > N (so they are not in gamma) and are open (so not in F(gamma)); they form an infinite
self-avoiding open path from y inside Z^3 \ (gamma u F(gamma)). So B_{gamma,y} holds. []

Lemma 3. For every N >= 1 and p in [0, 1],
    theta(p) <= K_N(p) theta(p),   K_N(p) = sum over N-step NAWs gamma from 0 of |E(gamma)| p^(N+1) (1-p)^|F(gamma)|.
Proof. By Lemma 2 (and Lemma 1(b): tree paths are NAWs), {|C(0)| = infinity} is contained in the union over NAWs
gamma and y in E(gamma) of A_gamma n B_{gamma,y}. A_gamma depends only on the sites of gamma u F(gamma), which are
N + 1 + |F(gamma)| distinct sites (Lemma 0), so P_p(A_gamma) = p^(N+1) (1-p)^|F(gamma)|. B_{gamma,y} depends only
on sites outside gamma u F(gamma) (y is outside), so it is independent of A_gamma, and B_{gamma,y} is contained in
{|C(y)| = infinity}, so P_p(B_{gamma,y}) <= theta(p) by translation invariance. Sum over (gamma, y). []

Corollary. If K_N(p) < 1 then theta(p) = 0, hence theta(p') = 0 for all p' <= p and p_c^site(Z^3) >= p.

## 3. The computation
Write c_f = sum of |E(gamma)| over N-step NAWs gamma from 0 with |F(gamma)| = f, so K_N(p) = sum_f c_f p^(N+1)(1-p)^f.

Lemma 4 (sign flips). Let G = (Z_2)^3 act on Z^3 by flipping coordinate signs. For g in G and a NAW gamma from 0,
g(gamma) is a NAW from 0, F(g gamma) = g F(gamma) and E(g gamma) = g E(gamma); in particular |F| and |E| are
G-invariant.
Proof. g is a graph automorphism fixing 0, which gives everything except the corner rule. At a turn, u_k - v_{k+1}
lies on the axis of step k - 1 and v_k - v_{k+1} on the axis of step k, two different axes. Every direction index of
axis a (2a and 2a + 1) is smaller than every index of axis b > a, so the comparison depends only on the two axes,
which g preserves. []
Let A(gamma) be the set of axes used by the steps of gamma. The stabilizer of gamma in G is the set of flips of
unused axes, so the orbit of gamma has 2^|A(gamma)| elements, and each orbit has exactly one member whose first
step along every used axis is positive. Hence c_f = sum over such canonical walks with |F| = f of
2^|A(gamma)| |E(gamma)|.

Program code/par/main.go enumerates the canonical N-step NAWs by depth-first search (a step along an unused axis is
only taken in the positive direction), keeps F(gamma) as a set of flagged sites built incrementally (when v_j is
added: each off-path neighbour z of v_j that already has a path neighbour of index <= j - 3 joins S, using the
smallest index of a path neighbour of z; at a turn at v_{j-1}, the corner joins C if the rank condition holds),
counts E at the leaf (neighbours y of v_N off the path, with exactly one path neighbour, not flagged), and adds
2^|A| |E| to c_|F|. A site flagged in F can never later become a path vertex (it already has two path neighbours,
or a path neighbour at index distance >= 2), so the incremental F equals F(gamma) of the final walk.

## 4. Certificate and theorem
outputs/p20.txt holds c_f for N = 20 (EXT line) and the walk total a_20 = 3516072837894. In exact rational
arithmetic (code/verify_cert.py), K_20(263376/10^6) = 0.99997152... < 1. Also K_20(5/19) = 0.98475899... < 1.
(Each term p^21 (1-p)^f increases on [0, 21/(21+f)], and f <= 23, so K_20 increases on [0, 21/44]; the grid value
263377/10^6 gives K_20 > 1, so 263376/10^6 is the largest passing value on the 10^-6 grid. This is not needed for
validity.)

Theorem. p_c^site(Z^3) >= 263376/10^6 = 0.263376.
