# REDUCTION2: density <= 1 - 4.5011e-15 for packings of regular tetrahedra (improves 1 - 1.0215562e-15)

This file CHANGES three places of the previous reduction (`REDUCTION_prev.md`, whose sections 1, 2.2, 2.3 and 3 stay valid verbatim: inputs K1-K5, Lemma A, Lemma R,
chain code `code/rig_dp.py`) and keeps the rest.  Notation, labels (KNOWN / PROVED-HERE / CERT / NUMERICAL / HEURISTIC) as there.
theta = arccos(1/3), kappa = cos(theta) = 1/3, sin(theta) = 2 sqrt2/3, alpha = theta/(2 pi), B unit ball, v_t = sqrt2/12.

Conditional status is unchanged: the result depends on the SAME three GEK inputs (Lemma 3.3 = K1 [wedge-area minimiser a(r)],
Lemma 3.5 = K4 [constant 3/sqrt2], Lemma 4.2 construction = K3) plus K2/K5 which follow from them / elementary geometry, and on Arb being correct.
NOT machine-checked in a proof assistant.

## 0. Statement
Every packing of regular tetrahedra has density <= 1/(1+b) <= 1 - b/(1+b), b >= 4.5011410e-15 (`code/verify_final2.out`, last lines), i.e.
deficit >= 4.5011e-15 = 4.41 x (previous 1.0215562e-15) = 1.7e10 x (GEK 2.6e-25).
Break-down (`code/ablation.out`, Q=40, best certified deficits): previous 1.0216e-15 -> multiplicity count only 1.8388e-15 -> + area vertex count
3.0642e-15 -> + Lemma V2 (chain) 4.5011e-15; (chain V2 with old vertex count: 2.7011e-15).

## 1. Lemma V2 (sharper single-wedge excess), PROVED-HERE, code `code/estab.py`, chain `code/rig2.py`
Replaces Lemma V (E(e) ~ 0.375 e) by E2(e) ~ 0.3537 e = sqrt2/4 e (= the flush-wedge value; 5.7% smaller; tight: at e=0.3 it gives 0.11012 = the
numerically found sup of a Monte-Carlo scan of the previous reduction (not included here; the claim does not rely on it).
**Statement.** W B-wedge (dihedral theta), c not interior, edge LINE at distance <= e from c.  Then vol(W)/vol(B) <= alpha + E2(e), where
E2(e) = (3/(4 pi)) sup_{0<=t<=e} [ Vslab(t, s2max(t,e)) - Loss(t) ],  s2max = kappa t + sqrt((1-kappa^2)(e^2-t^2)),
Vslab(t,s2) = int_0^{s2} A(x; -t) dx,  A(x;s1) = R^2 (pi - arccos y + y sqrt(1-y^2)), R^2 = 1-x^2, y = (s1 + kappa x)/(R sin theta),
Loss(t) = int_0^t Bl(x) dx, Bl(x) = R^2 (pi - arccos y + y sqrt(1-y^2)), R^2 = 1-x^2, y = -kappa x/(R sin theta).
**Proof.** c = 0.  W = {n1.x <= s1} & {n2.x <= s2} & B, outward unit normals, n1.n2 = -kappa.  c not interior => some s <= 0; call that face 1, t := -s1 >= 0.
If s2 <= 0, W lies in the centred wedge C = {n1.x<=0, n2.x<=0}&B, vol <= alpha.  Let s2 > 0.  Then
 W \ C = {n1.x <= -t, 0 < n2.x <= s2}&B   and   C \ W = {-t < n1.x <= 0, n2.x <= 0}&B  (exact), so vol(W) = alpha + vol(W\C) - vol(C\W).
(i) vol(W\C): slice by planes n2.x = x (0<x<=s2): disc of radius R = sqrt(1-x^2) centred x n2; with n1 = n1_par - kappa n2, |n1_par| = sin(theta), the condition becomes
n1_par.u <= kappa x - t, a half-plane at signed distance (kappa x - t)/sin(theta) from the centre; its area is R^2(pi - arccos y + y sqrt(1-y^2)) with y = (kappa x - t)/(R sin theta) (valid for |y|<=1).
This is A(x;-t).  (ii) vol(C\W): slice by n1.x = -x (0<=x<t): disc radius sqrt(1-x^2) centred -x n1; n2.x = n2_par.u + kappa x <= 0 is a half-plane at distance -kappa x/sin(theta): area Bl(x).
(iii) edge line L = {n1.x = -t, n2.x = s2}: its point closest to c is a n1 + b n2 with a = (kappa s2 - t)/(1-kappa^2), b = (s2 - kappa t)/(1-kappa^2) and
|.|^2 = (s2^2 + t^2 - 2 kappa t s2)/(1-kappa^2) <= e^2  <=>  s2 <= s2max(t,e) (and t <= e); computed by expanding the quadratic form (done in the notes of this lens).
(iv) A(x;-t) is non-increasing in t, Vslab non-decreasing in s2, Loss non-decreasing in t, hence on a t-cell [t0,t1] the excess is at most
Vslab(t0, sup_{cell} s2max) - Loss(t0), with sup_{cell} s2max <= min(e, kappa t1 + sqrt((1-kappa^2)(e^2 - t0^2))) (Cauchy-Schwarz: s2max <= e).  Bl is decreasing, so Loss(t0) >= right-endpoint Riemann sum.  QED.
**Code.** `estab.E2_up_exact(e)`: 36 t-cells (t_i = e (i/36)^2), 48 x-cells per integral, A and Bl evaluated on Arb balls (NaN enclosures raise); `estab.E_up_combined` = min(old Lemma V bound, E2 table);
the table is built on the geometric grid e_k = 1e-5 * 1.012^k up to EMAX = 0.9 and E_up(u) is the table value at the next grid point >= u (E2 is non-decreasing in e, a running max enforces this in the table).
`rig2.py` runs the unchanged chain of `rig_dp.py` (Lemma R, searching helpers plus certified forms `cert_lt1`, `cert_gt1`) with `rig_dp.E_up`, `rig_dp.E_f` replaced.  Result `code/rig2.out`, `code/rho_cert2.json`:
rho(0,5) >= 1.273839e-11 (was 8.619948e-12), rho(0,Q>=6) >= 5.342361e-12 (was 3.636896e-12).  `verify_final2.py` re-certifies all 155 states from scratch.

## 2. Counting scheme v2 (replaces previous section 4; code `code/scheme2.py`), PROVED-HERE modulo K1-K5
Parameters: Q, k pearl centres per edge, deficit-ball radius u, spacing sigma = 2u, d = (1-(k-1)sigma)/2 (distance of the end centres from the vertices), gamma_Q (K2 radius, alpha + Q a(gamma_Q) > 1),
R0 = u/gamma_Q, r_v = 3R0/sqrt2 = u/(gamma_Q kappa'), kappa' = sqrt2/3.  Pearls are placed as before on the 6 edges of each tetrahedron; a centre is GOOD if no vertex of any tetrahedron lies in the closed ball B(c, r_v).
* **Claim 1 (unchanged).**  Around a good centre c on T, T cap B(c,R0) is a centred wedge (K4/K5) and every other tetrahedron meeting B(c,R0) gives a wedge (K4); by K2 at most Q tetrahedra meet B(c,u); hence vol(B(c,u) \ packing) >= rho(0,Q) vol(B(c,u)) (rho(0,Q) from the certified chain).
* **Claim 2' (multiplicity; replaces conflict graph + independent set).**  Let q be minimal with gamma_q R1 > 2u, R1 = sqrt(2/3) d - 2u.  Then every point x lies in at most q of the open balls B(c,u), c good.  
  Proof.  Centres c, c' of the same tetrahedron with |c-c'| < 2u: same edge impossible (spacing sigma = 2u), different edges are >= d >= 2u apart (adjacent edges: distances s,t >= d to the common vertex give |c-c'|^2 = s^2+t^2-st >= d^2; opposite edges >= 1/sqrt2), checked by `chk["d>=2u"]`.  So the good centres in B(x,u) belong to pairwise different tetrahedra T_1..T_n; fix c_1 in T_1, |c_1 - c_i| < 2u.
  K5 at c_i (distance >= d from the vertices of T_i) makes T_i cap B(c_i, sqrt(2/3) d) a wedge, B(c_1,R1) subset B(c_i, sqrt(2/3) d), c_1 not in int T_i (c_1 in T_1), T_1 cap B(c_1,R1) is a centred wedge (c_1 on an edge); all T_i meet B(c_1,2u).  K2 with gamma_q R1 > 2u: n <= q.  QED.
  Therefore sum over good centres of vol(B(c,u) \ P) <= q * vol(U \ P) where U is the union of the balls: the uncovered volume is >= (#good centres) rho(0,Q) vol(B_u)/q.  (previous: independent set, factor 1/(Delta+1) = 1/9; now 1/q, q = 6 at the optimum.)
* **Claim 3' (bad centres by surface area; replaces q_v from K2).**  Fix a vertex w of a tetrahedron T_w.  Let S = set of tetrahedra T' != T_w with a centre c' in B(w,r_v) (closed).  R'' := sqrt(2/3) d - r_v.  K5 at c' makes T' cap B(c',sqrt(2/3)d) a wedge and B(w,R'') subset B(c',sqrt(2/3)d), so T' cap B(w,R'') is a B(w,R'')-wedge that meets B(w,r_v); w not in int T'.
  T_w cap B(w,R'') is the vertex cone (R'' < sqrt(2/3) = distance from w to the opposite face; `chk["0<R''<sqrt(2/3)"]`) whose surface fraction is (3 theta - pi)/(4 pi) = 0.0439 (solid angle of a regular tetrahedron vertex).  All these objects are interior-disjoint, so the surface fractions add up to <= 1; K1 gives each T' >= a(r_v/R'').
  Hence |S| <= floor((1 - (3 theta - pi)/(4 pi))/a(r_v/R'')) (`scheme2.vertex_count`; `qv_area`).  Centres of one T' within r_v of w lie on one edge (d > 2 r_v, `chk["d>2*r_v"]`) and there are <= floor(2 r_v/sigma)+1 = m_v of them.  So <= g |S| m_v bad centres per tetrahedron (g = 4 vertices).  (previous: q_v = 9 from K2, here q_v = 7 [the code also computes the old K2 count `qv_old` and takes the min].)
* **Conclusion.**  good >= e k - g q_v m_v per tetrahedron (e = 6 edges), and uncovered volume >= good N rho(0,Q) (4 pi/3) u^3 / q.  With V the volume of the region,
  V >= N v_t (1 + b), b = (good/q) (4 pi/3)/v_t u^3 rho(0,Q); density <= 1/(1+b).  Boundary / periodic-torus handling exactly as previous section 4 (the counting is local; multiplicity and bad-centre counts hold in the infinite packing).
* **Certified optimum** (`scheme2.cert`, `code/scheme2.out`, `verify_final2.out`): Q = 40, k = 30, u = 0.01140, gamma_Q = 0.788335, r_v = 0.030676, d = 0.16940, q = 6, q_v = 7, m_v = 3, good/tet = 180 - 84 = 96, rho(0,40) >= 5.342361e-12 => b >= 4.501141e-15.
  Variant Q = 150 (gamma = 0.913, a(r) needed up to r = 0.913): 5.0685e-15 (`scheme2.out`), not the headline for the same reason as in the previous run.

## 3. Where the remaining 9-10 orders of magnitude sit, and what the stability lemma would be worth  (new analysis of this lens)
### 3.1 Lemma G (exact reduction of the volume step to five centred wedges), PROVED-HERE, not used in the certificate
In a configuration with centred wedge W0 = C_0 and wedges W_1..W_m (m = w-1), disjoint from each other, write (proof of Lemma V/V2) W_j subset C_j u J_j with C_j a centred wedge (same dihedral angle, edge line through c, parallel to the edge of W_j) and J_j = {n1_j.x <= 0, 0 < n2_j.x <= s_j} the outward slab (0 <= s_j <= e_j).
Then the uncovered set contains G \ (J_1 u ... u J_m), where G = B \ (C_0 u ... u C_m) is a CONE with apex c.  Hence M(K) >= vol(G \ u J_j)/vol(B) >= (1 - w alpha) + overlaps - sum_j vol(J_j \ U)/vol(B), U = u C_j: only the part of the slab that lies in the GAP of the centred wedges is lost.  (Disjointness of the W_j is dropped: this is a relaxation.)
Consequences: (a) the linear Lemma V/V2 bound 1 - w alpha - sum E is the relaxation with every slab entirely inside the gap; (b) as G is a cone bounded by half-planes through c, each gap piece is a lune-like cone whose width at distance rho from c is delta rho, and a slab of thickness s only swallows the part within distance s of its face: this is the "gap-swallowing" mechanism of NOTES C7.
### 3.2 Leverage (`code/sens.out`, `code/sens2.out`, NUMERICAL float recursion)
If the wedge excess function E is replaced by lambda E in the recursion, the float rho(0,6) (= plateau used by the counting) becomes:
lambda=1: 3.65e-12;  0.943: 7.69e-12;  0.8: 4.2e-11;  0.6: 4.1e-10;  0.5: 1.4e-9;  0.25: 2.8e-7;  0.1: 7.1e-6;  0.02: 1.65e-4.  (E ~ e^2 instead of e: 5.5e-9.)
So a provable constant-factor reduction of the first-order wedge excess is worth orders of magnitude; Lemma V2 is the lambda = 0.943 point (it is the exact single-wedge optimum, so lambda < 0.943 needs interaction between wedges).
### 3.3 What the relaxed problem of Lemma G looks like numerically (`code/num_relaxed.out`, NUMERICAL, differential evolution, 1e5 sample points)
Minimal uncovered fraction of five wedges {n1.x<=0}&{n2.x<=s_j}, s_j<=e (no disjointness): e=0.01: 0.0079 (linear bound 0.0063), e=0.02: 0.0016 (linear: closed), e=0.03: 0.0 .
All optima found have parallel axes (theta_d = 0 or pi): the worst case of the relaxed problem is the planar fan of five lunes with the gap spread over four seams, and its closing threshold is e* ~ 0.02-0.03, against 0.0144 for the linear bound (lambda_eff ~ 0.5-0.7 on the threshold).
Sketch of the exact fan value: a seam of angle delta between two half-planes through c has volume 2 delta/3 while a slab of thickness delta (the minimum that swallows it) has volume (pi/2) delta: ratio 4/(3 pi) = 0.42.
### 3.4 What is NOT proved (the honest gap)
The inequality "for ANY five centred wedges (arbitrary axes) and slabs of thickness <= e_j, vol(B \ (U u slabs)) >= F_fan(e)" (the fan is the worst case) is NOT proved here.  The sphere-level version needs a taper argument for gap polygons bounded by great semicircles whose axes differ;
I could only prove the first-order statement (Steiner/bathtub: covered gap <= eps * length of slab arcs, which reproduces the linear bound: no gain) and the exact fan value.  A numerical attempt to see the DISJOINT problem (`code/num_excess.out`) did not converge (differential evolution did not even find the 5-lune fan tiling at 6e4 points): inconclusive, no claim.
Next test and checkpoint: prove or refute "fan is optimal" for the relaxed problem by an interval branch-and-bound over the 12-dimensional arrangement (axis directions mod rotation) using the Arb machinery of `code/estab.py`; checkpoint = `code/num_relaxed.py` optimum per e (`code/num_relaxed.out`).

## 4. Function-by-function correspondence
| Section | Code | Output |
|---|---|---|
| Lemma V2 | `estab.E2_up_exact`, `estab.E2_table`, `estab.E_up_combined`, `estab.E_f_table` | `estab_test.out` |
| Lemma R chain with V2 | `rig2.main` -> `rig_dp.solve_state`, `rig_dp.cert_lt1`, `rig_dp.cert_gt1` (unchanged) | `rig2.out`, `rho_cert2.json` |
| Claims 1, 2', 3', conclusion | `scheme2.cert`, `scheme2.qmin`, `scheme2.vertex_count`, `scheme2.gamma_lo` | `scheme2.out`, `scheme2_best_40.json` |
| Re-certification | `verify_final2.py` (all 155 states + `scheme2.cert` at the stored (Q,k,u)) | `verify_final2.out` |
| Ablation | `ablation.py` | `ablation.out` |
