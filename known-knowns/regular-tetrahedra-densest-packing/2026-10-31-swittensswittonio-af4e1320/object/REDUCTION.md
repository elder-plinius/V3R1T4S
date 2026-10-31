# REDUCTION: a certified upper bound  density <= 1 - 1.0215e-15  for packings of regular tetrahedra

Lens `formalist-3`, repair round on partial win p2.  Everything below corresponds, step by step, to the files
`code/rig_dp.py` (sections 3), `code/scheme.py` (section 4), `code/verify_final.py` (re-check), run with the Arb ball-arithmetic
library (python-flint 0.9.0, 160-bit precision) – NOT with the earlier `mpmath.iv` + custom acos/asin + `sq0` clamp kit.

Labels:  **KNOWN** = taken from Gravel-Elser-Kallus (GEK, arXiv:1008.2830) or textbook geometry, not re-proved here;
**PROVED-HERE** = proof is given in this file (short, elementary) and the numbers are evaluated by the code;
**CERT** = a numerical inequality verified with outward-rounded Arb balls (re-runnable, `code/verify_final.py`);
**NUMERICAL** = floating/Monte-Carlo evidence that is *not* used in the proof (sanity only).

Notation: theta = arccos(1/3) (tetrahedron dihedral angle), alpha = theta/(2 pi) = 0.195913..., kappa = sqrt(2)/3,
B = unit ball centred at c, vol(B)=4pi/3, v_t = sqrt(2)/12 (unit-edge tetrahedron).

---------------------------------------------------------------------------------------------------------------------------
## 0. Statement

**Theorem.** Every packing of regular tetrahedra (any edge length, any packing, density defined as limsup over cubes of
vol(packing ∩ cube)/vol(cube); for periodic packings the density of the cell) has density <= 1/(1+b) <= 1 - b/(1+b) with
b >= 1.0215562e-15 (`code/verify_final.out`, last lines).  Hence density <= 1 - 1.0215e-15, i.e. the density *deficit* is >= 1.02e-15,
which is 3.9e9 times the published deficit 2.6e-25 (GEK) and 9.5e7 times the earlier formalist certificate 1.07e-23.

The theorem is conditional on the KNOWN inputs K1-K5 of section 1 (published lemmas of GEK, with one repaired gap, see 2.1) and on
Arb being correct.  It is NOT machine-checked in a proof assistant.

---------------------------------------------------------------------------------------------------------------------------
## 1. Setting and KNOWN inputs

**Objects.**  A *B-wedge* is B ∩ H1 ∩ H2 (two half-spaces whose boundary planes meet at dihedral angle theta); a *B-cap* is B ∩ H
(half-space).  A wedge is *centred* if its edge is a diameter of B.  K(c,w) denotes the set of configurations of pairwise
interior-disjoint objects in B consisting of one centred wedge W0 plus at most (w-1) further wedges and at most c caps (all positions
allowed).  (GEK write K(c,w,infinity).)  The missing fraction of a configuration K is M(K) = 1 - vol(∪K)/vol(B), and
rho(c,w) := inf over K(c,w) of M(K).  Partial order: (c,w) <= (c',w') iff w <= w' and c+w <= c'+w'; then K(c,w) ⊂ K(c',w') and
rho(c,w) >= rho(c',w').  Every non-central object O satisfies c ∉ int O (because c ∈ closure(W0)); hence O lies in a half-space H
with c ∉ int H and vol(O)/vol(B) <= 1/2.

Let a(r) denote the surface-area fraction (on ∂B) of the wedge W*(r) whose bisecting plane contains c, whose interior does not
contain c and whose edge is at distance r from c.  Closed form (Gauss-Bonnet): with h = r/sqrt3,
phi = arccos((1/3+h²)/(1-h²)), psi = 2 arcsin(sqrt(1-r²)/sqrt(1-h²)):   a(r) = (2 phi - 2 h psi)/(4 pi)   (`rig_dp.a_lo`, `a_f`).

* **K1 (GEK Lemma 3.3, KNOWN).** A B-wedge meeting B_r has surface fraction >= a(r) on ∂B; a B-cap at distance delta from c has
  surface fraction exactly (1-delta)/2.  [GEK prove the planar minimisation in their appendix; a(r) is the exact area of the minimiser.]
  NUMERICAL check of the closed form against the Monte-Carlo area of W*(r): `code/a_check.out` (r = .1,.3,.6,.8,.9, agree to 2e-4).
* **K2 (GEK Cor. 3.4, KNOWN + K1).** gamma_q := the root of alpha + q a(gamma) = 1.  If alpha + q a(gamma) > 1 then, in any
  configuration with a centred wedge, at most q objects (counting the centred one) meet B_gamma.  (Proof: the surface fractions of
  the objects meeting B_gamma add up, by K1, to more than 1 otherwise.)  `scheme.gamma_lo` certifies alpha + q a(r) > 1 for the
  r it uses (CERT).
* **K3 (GEK Lemma 4.2 construction, KNOWN).** For K ∈ K(c,w), 0 < s <= 1 there is K'_s, a configuration in B_s, such that
  M(K) >= s³ M(K'_s / s), where K'_s consists of W0 ∩ B_s, the wedges O ∩ B_s of those objects whose edge meets the open ball
  int B_s (these stay wedges), and caps (one for each remaining object O that meets B_s; an object that does not meet B_s is
  absent; some objects may be deleted).  Consequently (after rescaling by 1/s):
  K'_s/s ∈ K( #caps, 1 + #{wedges with edge distance < s} ) ⊂ K(c', w') for every (c',w') >= that type.
* **K4 (GEK Lemma 3.5, KNOWN).** If a unit-edge regular tetrahedron T has c ∉ int T and all its vertices at distance > 3 rho/sqrt2
  from c, then T ∩ B(c,rho) is a B-wedge (possibly empty).  [Proof in GEK appendix; the constant 3/sqrt2 was checked NUMERICALLY
  by the earlier lens (`formalist/code/lemma35_sup.out`); this lens does not re-prove it.]
* **K5 (elementary).** If P is a point of an edge of T at distance >= d from both end vertices, the ball B(P, sqrt(2/3) d) does not
  meet the planes of the two faces not containing that edge (the distance from P to the plane of a face containing only the nearer
  vertex is t·sqrt(2/3) for t = distance to that vertex), so T ∩ B(P, sqrt(2/3) d) = H1 ∩ H2 ∩ B(P,..) is a wedge.

---------------------------------------------------------------------------------------------------------------------------
## 2. New lemmas (PROVED-HERE)

### 2.1 Lemma V (wedge volume), repairs GEK Lemma 3.1 / formalist "exact V(d)"
**Statement.** Let W be a B-wedge with c ∉ int W whose edge line is at distance e (0 <= e <= 1) from c.  Then
vol(W)/vol(B) <= alpha + E(e), E(e) := min( (3/(4pi)) ∫_0^e A(x) dx , 1/2 - alpha ),
A(x) = R²( pi - arccos y + y sqrt(1-y²) ),  R² = 1-x²,  y = x cot(theta)/R,  cot(theta) = 1/(2 sqrt2)  (valid for x <= 0.9).
**Proof.** Put c = 0.  Write W = {n1·x <= s1} ∩ {n2·x <= s2} ∩ B with unit outward normals, n1·n2 = -cos(theta).  Since c ∉ int W, one of
the half-spaces, say the first, has 0 ∉ its interior, i.e. s1 <= 0.  Then W ⊂ W' = {n1·x <= 0} ∩ {n2·x <= s2} ∩ B.  The plane
{n2·x = s2} contains the edge, so |s2| <= e.  If s2 <= 0, W' lies in the centred wedge {n1·x<=0, n2·x<=0}, of volume fraction alpha.
If s2 > 0, W' = W_c ⊔ J with W_c = {n1·x<=0,n2·x<=0}∩B (centred, fraction alpha) and J = {n1·x<=0, 0 < n2·x <= s2}∩B.
Slice J by the planes n2·x = x0 (0<x0<=s2): the slice of B is a disc of radius R = sqrt(1-x0²) centred x0 n2; on it the condition
n1·x <= 0 reads n1∥·u <= x0 cos(theta) with |n1∥| = sin(theta), i.e. a half-plane at distance x0 cot(theta) from the centre which
contains the centre; its area is R²(pi - arccos y + y sqrt(1-y²)) = A(x0) (disc minus circular segment).  So vol(J) = ∫_0^{s2} A <= ∫_0^e A.
Finally vol(W) <= vol(H)/... <= 1/2 for every object, which gives the cap in E.  ∎
**Why this replaces earlier values.**  (i) GEK translate the face through c and assert that the edge distance does not grow; it can
(by the law of sines up to 1/sin(theta)); the slab thickness is however always <= e (|s2| <= e), which is the version above.
(ii) The formalist's "exact V(d)" (flush wedge with edge distance d) is *not* an upper bound for non-flush wedges:
`code/e_sup_check.out` finds wedges with edge distance 0.3 (0.6) and volume fraction 0.306035 (0.410380) > V_flush = 0.305799 (0.410070)
(NUMERICAL).  Lemma V is above all those values (E_f(0.3)=0.11654 vs max found 0.11012; GEK's printed alpha+0.3536e+0.0786e² also is).
**Code:** `rig_dp.A_ball`, `rig_dp.E_up` (160-cell Riemann upper sum with ball enclosures per cell; capped by 1/2 - alpha) – CERT.

### 2.2 Lemma A (several caps), new
**Statement.** In a configuration with centred wedge W0, let C_1..C_n (n >= 2) be pairwise disjoint caps (each disjoint from W0).
Then sum_i vol(C_i)/vol(B) <= F := 1/2 + s(pi/2 - theta/2) = 1 - alpha - sqrt2/(3 pi) = 0.654034.  In particular rho(c,1) >= sqrt2/(3pi) = 0.150052 for c >= 2
(GEK have rho(2,1) >= 2.2e-3).
**Proof.** Slice by planes z = h orthogonal to the axis of W0.  The slice of B is a disc D of radius R = sqrt(1-h²) centred O on the axis;
W0 ∩ D is the open sector S of angle theta with apex O.  A cap slices to D ∩ P (P a half-plane); if O were in int P, P ∩ D would
overlap S near O, so O ∉ int P: the chord is at distance d >= 0 from O and D ∩ P is a circular segment with footprint arc of
half-angle rho = arccos(d/R) ∈ [0, pi/2] and area fraction s(rho) = (rho - sin rho cos rho)/pi of the disc.  The footprints of the
segments and of S are pairwise interior-disjoint open arcs of ∂D (if two footprints overlapped, the corresponding regions would
overlap near ∂D), so 2 sum rho_i + theta <= 2 pi.  s is convex on [0,pi/2] (s'' = 2 sin 2rho/pi >= 0), so sum s(rho_i) is maximal on the polytope
{0<=rho_i<=pi/2, sum rho_i <= pi - theta/2} at a vertex, i.e. rho = (pi/2, pi/2-theta/2, 0,..): s(pi/2)+s(pi/2-theta/2) = 1/2 + (pi/2 - theta/2 - sin(theta)/2)/pi.
Since sin(theta)/2 = sqrt2/3 and theta/(2pi)=alpha, this equals 1 - alpha - sqrt2/(3pi).  Integrate over h (the bound is a fixed fraction of the disc
area in every slice).  ∎  (NUMERICAL: a differential-evolution search found two caps of total volume 0.63 <= 0.654.)
**Code:** `FCAP`, base values `rho[(c,1)]`, and the cap test `caps.lower() > FCAP.upper()` in `cert_gt1`.

### 2.3 Lemma R (profile recursion), new — replaces GEK's single-radius dynamic programme
For a state (c,w) let the non-central objects be c caps Q_i and (w-1) wedges O_j.  For a wedge O_j put  e_j = distance from c to its edge
line (infinity if the edge misses B) and delta_j = dist(c,O_j) <= e_j; for a cap put delta_i = distance to its plane.

**(R1, wedge-count states with t := w alpha + c/2 < 1).**  Sort the wedge edge distances e_(1) <= ... <= e_(w-1).  For K ∈ K(c,w) with this profile:
 (a) for k = 0..w-2:  M(K) >= min(e_(k+1),1)³ · rho(c+w-1-k, 1+k).     [K3 at s = min(e_(k+1),1): at most k wedges have edge inside int B_s,
     all other present objects become caps, and K(c+w-1-k',1+k') ⊂ K(c+w-1-k,1+k) for k' <= k.]
 (b) M(K) >= VOL := 1 - w alpha - capvol(c) - sum_j Etilde(e_j),   Etilde = E for e<1, 1/2-alpha for e>=1 (Lemma V), capvol(c)=c/2 for c<=1 and F for c>=2 (Lemma A).
Let rho_k := rho(c+w-1-k,1+k) (non-increasing in k).  Define T* as the root of  T = 1 - w alpha - capvol(c) - sum_k Etilde( (T/rho_k)^{1/3} ).
The right side minus T is strictly decreasing, so T* is unique, and if all terms in (a) are < T then e_(k+1) < (T/rho_k)^{1/3} for all k, so VOL >= (RHS at T) .
Hence  **M(K) >= T*** for every K ∈ K(c,w): rho(c,w) >= T*.
*Certified form (cert_lt1):* a number T_lo is accepted iff  (1 - w alpha - capvol_up(c) - sum_k E_up( upper((T_lo/rho_k)^{1/3}) ) - T_lo).lower() >= 0,
with rho_k the already certified lower bounds.  Then T* >= T_lo.

**(R2, states with t > 1).**  Order the non-central objects by delta; let sigma be the resulting sequence of types (cap/wedge).  Because objects are pairwise
disjoint and disjoint from W0 (area alpha on ∂B), K1 gives  sum_j A_j(delta_j) <= 1 - alpha with A = (1-delta)/2 for caps, a(delta) for wedges
(0 for delta >= 1); Lemma A gives sum of cap volumes (1-delta)²(2+delta)/4 <= F if at least two caps meet B.  K3 at s = delta_(i) (just below):
only the first i-1 objects are present, and in the worst case (wedge objects have e_j = delta_j) they form the type
(#caps, 1+#wedges) of the first i-1 objects:  M(K) >= min(delta_(i),1)³ · rho(type_{i-1}(sigma)).  Let rho_{i-1}^sigma be these (non-increasing in i).
If some profile had all terms < T then delta_(i) < u_i(T) := (T/rho_{i-1}^sigma)^{1/3}, so by monotonicity of A the coverage constraint would
be violated as soon as  sum_i A_{sigma_i}(u_i(T)) > 1-alpha  (or the cap-volume constraint if the caps' volumes at u_i exceed F).
Hence rho(c,w) >= T_lo as soon as T_lo is *infeasible for every ordering sigma* (min over the finitely many sigma).
*Certified form (cert_gt1):* for every sigma, with  u_i := upper((T_lo/rho_{i-1}^sigma)^{1/3}) (skipping u_i >= 1),
 sum_i A_lower(u_i) > upper(1-alpha)   or   (>= 2 caps and sum of cap-volume lower bounds > upper(F)).

**(R3, monotone closure and large states.)**  rho(k) is replaced by max(rho(k), rho(k2)) for k <= k2 in the partial order (inclusion of classes).
For pure-wedge states (0,w), w >= 6, the single ordering is all-wedge; the recursion shows rho(0,w) = rho(0,6) = 3.636896e-12 for w = 6..151 (CERT):
a sixth wedge cannot be present near c (the five already present cover 98% of ∂B), so it is forced to distance > 0.7 and costs only a factor 0.42.

**Table of certified lower bounds (`code/rig_dp.out`, re-checked in `code/verify_final.out`; GEK's published value of rho(0,5) is 8.5e-19,
the formalist's certificate 1.43e-18):**

| state | t | CERT lower bound | state | t | CERT lower bound |
|---|---|---|---|---|---|
| (c,1), c>=2 | | 0.150052 (Lemma A) | (0,4) | .784 | 7.637494e-07 |
| (1,2) | .892 | 2.979110e-03 | (3,2) | 1.892 | 6.508480e-04 |
| (0,3) | .588 | 2.979110e-03 | (2,3) | 1.588 | 9.056212e-06 |
| (2,2) | 1.392 | 6.508480e-04 | (1,4) | 1.284 | 1.205094e-07 |
| (1,3) | 1.088 | 9.056212e-06 | **(0,5)** | .980 | **8.619948e-12** |
| | | | (0,6..151) | >1 | 3.636896e-12 |

(An independent float implementation `code/profile_dp.py` with the printed GEK E(r) gave 1.1e-11 for (0,5); the certified chain uses the larger, sound Lemma V.)

---------------------------------------------------------------------------------------------------------------------------
## 3. How the code implements section 2
`rig_dp.py`: constants (Arb 160 bit); `a_lo` = closed form of a(r) evaluated at an exact point, rounded down; `A_ball`, `E_up` = Lemma V;
`orderings(c,w)` = all type sequences sigma; `cert_lt1`, `cert_gt1` = certified forms of R1, R2; the *searching* helpers `search_lt1`, `search_gt1`
(plain floats) only propose T_lo, they are not part of the proof; `solve_state` multiplies the proposal by (1-1e-6) and re-certifies.
`verify_final.py` re-certifies every stored value of `rho_cert.json` from scratch (155 states) and the scheme of section 4.

---------------------------------------------------------------------------------------------------------------------------
## 4. From rho(0,Q) to a density bound (counting scheme)  — `scheme.cert`
Parameters (certified optimum found): Q = 40, k = 38 pearl centres per edge, u = 0.0084 (deficit-ball radius), spacing sigma = 2u,
end offset d = (1-(k-1)sigma)/2 = 0.1892, gamma_Q = gamma_40 = 0.788335 (CERT: alpha + 40 a(gamma_Q) > 1), R0 := u/gamma_Q, r_v := R0/kappa = 0.022603.
Edges per tetrahedron e = 6, vertices g = 4.

* **Pearls.** On each edge of every tetrahedron T of the packing put k points ("centres") at distance d + j sigma from one vertex, j = 0..k-1
  (the last is at distance d from the other vertex).  A centre c is *good* if no vertex of any tetrahedron lies in the closed ball B(c,r_v).
* **Claim 1 (deficit of a good centre).** For good c on T and every tetrahedron T' ≠ T: c ∉ int T' (c ∈ ∂T), and all vertices of T' are at
  distance > r_v = 3 R0/sqrt2 · (something): precisely 3 R0/sqrt2 = 3 kappa r_v/sqrt2 = r_v, so K4 with rho = R0 shows T' ∩ B(c,R0) is a wedge (or empty).
  T ∩ B(c,R0) is a centred wedge (K4 with c on an edge, vertices at distance >= d > r_v).  By K2 (Q = 40, gamma_Q R0 = u) at most Q
  tetrahedra meet B(c,u), so (restricting to B(c,u)) the packing in B(c,u) is a configuration of K(0,Q) and
  vol(B(c,u) \ packing) >= rho(0,Q) vol(B(c,u)).   [CERT for rho(0,40) >= 3.636896e-12.]
* **Claim 2 (conflict graph).** Two good centres c ∈ T, c' ∈ T' have intersecting deficit balls only if |c-c'| < delta := 2u.  Centres of the same tetrahedron are
  >= min(sigma, d, 1/sqrt2) >= 2u apart (same edge: sigma = 2u; adjacent edges: >= d; opposite: 1/sqrt2), so they never conflict.  Let c be a centre of T.  Every
  tetrahedron T'' ≠ T with a centre c'' within delta of c is, by K5 applied at c'' (distance >= d from the vertices of T''), a wedge in B(c,R1),
  R1 = sqrt(2/3) d - delta (B(c,R1) ⊂ B(c'', sqrt(2/3) d)), with c ∉ int T''; T itself is a centred wedge in B(c,R1) (K5).  All these meet B(c,delta).  If
  gamma_q R1 > delta (CERT, q = 5 here) then by K2 at most q of them meet B(c,delta), so at most q-1 tetrahedra T'' conflict with T-centres at c.
  Two centres of one T'' lie within delta of c only if on the same edge (different edges: >= d >= 2 delta apart; checked d >= 4u), and at most m = 2
  (an open interval of length 2 delta = 2 sigma contains <= 2 progression points).  So each centre conflicts with <= Delta = m(q-1) = 8 others.
* **Claim 3 (vertices).** A centre c of T is bad iff some vertex w ∈ B(c,r_v); w is not a vertex of T because d > r_v.  For a fixed vertex w let c_0 be one centre within r_v of w;
  every other tetrahedron with a centre within r_v of w has it within 2 r_v of c_0, so as in Claim 2 (with delta' = 2 r_v, R1' = sqrt(2/3)d - delta') at most q_v of them
  (including the tetrahedron of c_0) meet B(c_0,delta') provided gamma_{q_v} R1' > delta' (CERT, q_v = 9).  Centres of one tetrahedron within r_v of w lie on one edge
  (d > 2 r_v, CERT) and are at most m_v = floor(2 r_v/sigma)+1 = 3.  Hence each vertex w produces at most q_v m_v = 27 bad centres, so the number of bad centres is
  at most g q_v m_v N = 108 N and the number of good centres at least (e k - g q_v m_v) N = 120 N.
* **Independent set.** The conflict graph on good centres has maximum degree <= Delta = 8, so it has an independent set of size >= 120 N/(Delta+1); the corresponding
  balls B(c,u) are pairwise disjoint, each is at least a fraction rho(0,Q) uncovered (Claim 1).  With V = volume of the region,
  V >= N v_t + (120 N/9)·rho(0,Q)·(4pi/3) u³, i.e. density = N v_t/V <= 1/(1+b),  b = (120/9)(4pi/3)/v_t · u³ · rho(0,Q) >= 1.0215562e-15  (CERT).
  Code: `scheme.cert` checks d > 2 r_v, d >= 4u, R1 > 0, finds q, q_v (smallest with gamma_q R > delta using certified gamma lower bounds), m, m_v, and computes b with
  rounding downward; `verify_final.py` prints the final line.
* **Boundary / general packings (written here, earlier lenses had no argument).** Let P be any packing, C_L a cube of side L.  Let T_L^- = tetrahedra contained in C_{L-1} and T_L = tetrahedra
  meeting C_L; |T_L| - |T_L^-| <= vol(boundary layer of thickness 3)/v_t = O(L²) because tetrahedra are disjoint with diameter 1.  The counting above is local: the
  conflict degree bound and the vertex bound hold in the infinite packing, so choose the independent set among the good centres of tetrahedra of T_L^-; their balls lie in C_L.  The bad
  centres on T_L^- come from vertices of tetrahedra meeting C_{L}, at most |T_L| of them.  So vol(C_L) >= vol(P ∩ C_L) + (120/9)(4pi/3)u³ rho (|T_L^-| - O(L²)) and vol(P ∩ C_L) <= v_t|T_L|, giving
  vol(P∩C_L)/vol(C_L) <= 1/(1+b) + O(1/L).  For a periodic packing the same argument is done in the quotient torus (a lattice translate cannot conflict with itself since two translates by a vector of length < 2u overlap).

---------------------------------------------------------------------------------------------------------------------------
## 5. What is and is not proved
PROVED-HERE: Lemma V, Lemma A, Lemma R (R1-R3 logic), the counting Claims 1-3 modulo K1-K5, the boundary argument, base values rho(0,1)=1-alpha, rho(1,1)=rho(0,2)=1/2-alpha
(a second object lies in a half-space not containing c, so has volume <= 1/2; equality for a hemisphere).
CERT (Arb): all numbers (E_up, a_lo, gamma_q, every inequality of cert_lt1/cert_gt1/scheme.cert).
KNOWN, not re-proved: K1 (minimality of W*(r) for the wedge area; a(r) closed form is the area of W*, checked numerically), K3 (GEK's construction), K4 (the constant 3/sqrt2).
Not machine-checked in Lean/Isabelle; Arb is trusted.
Possible weak points a skeptic should attack first: K3 (the non-overlap of K'_s after enlarging wedges to caps), K4, and the claim in R2 that in the worst case wedge objects
have e_j = delta_j (monotonicity of rho under the partial order).
