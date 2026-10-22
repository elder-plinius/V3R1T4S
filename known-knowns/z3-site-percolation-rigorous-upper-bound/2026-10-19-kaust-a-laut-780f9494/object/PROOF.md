# p_c^site(Z^3) <= 0.4427: a block growth-process coupling with exact certificates

2026-10-18. The coupling lemma and the tree-information lemma follow J. van den Berg and A. Ermakov, "A new lower
bound for the critical probability of site percolation on the square lattice", Random Structures Algorithms 8
(1996) 199-212 (growth process and Strassen coupling), written out here for blocks of Z^3. Strassen's theorem: a
law P on a finite poset stochastically dominates Q (a coupling with X >= Y exists) iff P(A) >= Q(A) for every
up-set A (V. Strassen, Ann. Math. Statist. 36 (1965) 423-439).

## 0. Setting

Site percolation on Z^3 with parameter p; P_p, theta(p) = P_p(|C(0)| = infinity). Block B = {0,1,2}^3 (27 sites);
B_v = B + 3v for v in Z^3. The blocks are disjoint and cover Z^3; coarse neighbours v ~ w iff |v - w|_1 = 1, and
then B_v, B_w share a 3 x 3 face: x in B_v and y in B_w are Z^3-adjacent iff x lies on that face of B_v and
y = x + (w - v) (each face site has exactly one partner, its mirror image across the face). Sites of blocks that are
not coarse neighbours are never Z^3-adjacent.

eps(v) in {0,1}^B is the configuration of B_v translated to B. G(eps) is the largest open component of eps
(connectivity inside B); ties are broken by the larger sum over the six faces of the number of the component's sites
on that face, then by the first component found in site order; and G = empty set if that component has fewer than
s = 6 sites (or eps has no open site). Any deterministic rule giving a connected set or the empty set would do.

For coarse neighbours v, w: eta(v, w) = 1 iff some site of G(eps(v)) + 3v is Z^3-adjacent to some site of
G(eps(w)) + 3w. Writing T_F(eps) for the trace of G(eps) on face F, eta(v, w) = 1 iff T_F(eps(v)) and the mirror of
T_{F'}(eps(w)) meet, where F, F' are the faces of B_v, B_w on their common boundary. eta is a function of
(eps(v), eps(w)).

## 1. The growth process

R is the event that eps(0) is all open (P_p(R) = p^27 > 0). Under P_p( . | R): xi(0) = 1. Fix a total order on Z^3
with least element 0. At each step select the least v with xi(v) = 1 that has a coarse neighbour without a
xi-value; those neighbours are v's children; each child u gets xi(u) = eta(v, u).

Claim. If xi(u) = 1 then every site of G(eps(u)) + 3u is in the open cluster of 0. (Induction along the parent chain:
G(eps(u)) is connected and contains a site adjacent to a site of G(eps(parent)), which is in the cluster; B_0 is all
open and connected and contains 0.)

## 2. Coupling lemma (Lemma 1 of the square-site proof, for blocks)

Lemma 1. Suppose, under P_p( . | R), at every step and for every history, the conditional law of the children's
xi-values stochastically dominates Bernoulli(q)^children. Then theta_{Z^3}(q) <= P_p(survival | R) <= theta(p)/p^27.

Proof. Build zeta alongside xi, under P_p( . | R). At the root, zeta(0) ~ Bernoulli(q) independently, so
zeta(0) <= xi(0) = 1. At each step, given the history of both processes, use Strassen's theorem to choose zeta on the
children with law Bernoulli(q)^children, independent of the history, and zeta <= xi on the children; coarse vertices
never assigned a xi-value get fresh independent Bernoulli(q) values.

zeta is i.i.d. Bernoulli(q). The zeta values on a step's children are drawn from a Strassen coupling Q_h( . | xi on
the children), using fresh auxiliary uniforms, where Q_h may depend on the history h. Earlier zeta values are
functions of earlier xi-values and auxiliary uniforms, which are independent of the block states. So the law of the
new xi-values given (h, earlier zeta) is their law given h, and the new batch of zeta is exactly
Bernoulli(q)^children given everything before it; the number of children is a function of h. For the whole field,
pre-sample independent Bernoulli(q) coins Y(v), and after n steps form the hybrid field: zeta on the vertices
assigned so far, Y elsewhere. Each hybrid field is i.i.d. Bernoulli(q) by induction on n, and the hybrid fields
converge pointwise to zeta, so every finite-dimensional law of zeta is the product law.

If the process dies out (finitely many steps), no vertex with xi = 1 has a neighbour without a xi-value, so every
coarse neighbour u of a xi = 1 vertex received its xi-value at some step, with zeta(u) <= xi(u). By induction along
any zeta-open path from 0 (zeta(0) <= xi(0)), every vertex of the path has xi = 1, so the zeta-open cluster of 0 lies
in the finite set {xi = 1}. If the process survives, it has infinitely many steps, each selecting a distinct block
with xi = 1; by the Claim, the open cluster of 0 meets all of them, so it is infinite. Hence
theta_{Z^3}(q) <= P_p(survival | R) <= P_p(|C(0)| = infinity | R) <= theta(p)/P_p(R). []

(The die-out/survival split is needed: for a general order, a vertex with xi = 1 need not ever be selected when the
process survives.)

## 3. Tree information (Lemma 2 of the square-site proof)

The history is R together with the event that eta(e) = x_e on the edges of the exploration tree. Children are
blocks without a xi-value, so their eps are independent of the history. Hence the children's xi law given the
history is sum_beta w(beta) nu_beta, where w is the posterior law of eps(b2) (b2 the selected block, c its parent)
and nu_beta = prod over children i of Bernoulli(r_i(T_i(beta))), with r_i(T) = P_p(T meets the mirror of the trace
of G(eps') on the facing face) for independent eps'. By message passing on the tree,
w(beta) ∝ pi(beta) sum_gamma 1[eta(gamma, beta) = 1] mu_c(gamma), mu_c a probability law on the states of c (the
point mass at the all-open state when c = 0). Grouping gamma by U = mirror of T_F(gamma):
w = sum_U lambda_U w_U, with w_U(beta) ∝ pi(beta) 1[T_in(beta) meets U], over nonempty U in the entry face.

## 4. Reduction to finitely many checks

The set of laws on {0,1}^k that dominate Bernoulli(q)^k is convex, and domination survives projection to a subset of
coordinates. So Lemma 1's hypothesis holds if:
(i) at the root step (eps(0) all open, U = the full face for each child): r_f(full face) >= q for each face f;
(ii) for each entry face F_in and each nonempty U contained in F_in, the law of the 5 children's eta under w_U
dominates Bernoulli(q)^5. By Strassen's theorem this is: for every up-set A of {0,1}^5, law_U(A) >= q-measure of A.
Both are finite computations over the 2^27 block states, done in interval arithmetic with outward rounding.

## 5. The chain

Each link j is a run of the checks of section 4 at a rational pair (p_j, q_j); if they pass, Lemma 1 gives
theta(p_j) >= p_j^27 theta(q_j), so theta(q_j) > 0 implies theta(p_j) > 0 and p_c <= p_j.

Base: theta(q_1) > 0 for q_1 = 501/1000, because p_c^site(Z^3) <= 1/2 (Campanino and Russo 1985, the comparison
with the triangular lattice; their strict inequality is not needed). Links (all checks passed in exact arithmetic;
outputs/chainB_summary.txt and outputs/chainA_summary.txt):

| link | p_j | q_j | worst up-set margin |
|---|---|---|---|
| 1 | 2317/5000 = 0.4634 | 501/1000 | 1.94e-4 |
| 2 | 9/20 = 0.45 | 2317/5000 | 1.12e-4 |
| 3 | 1781/4000 = 0.44525 | 9/20 | 1.14e-4 |
| 4 | 1109/2500 = 0.4436 | 1781/4000 | 2.04e-4 |
| 5 | 443/1000 = 0.443 | 1109/2500 | 1.66e-4 |
| 6 | 1107/2500 = 0.4428 | 443/1000 | 1.99e-4 |
| 7 | 4427/10000 = 0.4427 | 1107/2500 | 1.23e-4 |

(An alternative start, q_1 = 1/2 with p_1 = 463/1000 and p_2 = 4499/10000, also passes; it needs Campanino-Russo's
strict inequality.) Every link also checks the root condition r_f(full face) >= q_j exactly (outputs/*_log.txt, "root:" lines).

Theorem. p_c^site(Z^3) <= 4427/10000 = 0.4427.
