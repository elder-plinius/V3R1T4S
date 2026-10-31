# REDUCTION_FULL: an upper bound  density <= 1 - 4.5011e-15  for packings of congruent regular tetrahedra, from first principles

Everything needed is in this folder (`REDUCTION_FULL.md`, `REPRODUCE.md`, `code/`).  The argument follows the strategy of
Gravel, Elser and Kallus (arXiv:1008.2830, "Upper bound on the packing density of regular tetrahedra and octahedra", Discrete Comput. Geom. 46 (2011) 799)
and re-proves, instead of quoting, each lemma that they use (their Lemmas 3.3, 3.5 and the construction of 4.2 are proved below; their Lemma 3.1
is replaced by an independently proved Lemma V2, see section 5 and the retraction note in section 11).  The final computation (sections 5, 6, 8)
is a re-runnable interval-arithmetic computation (Arb balls via python-flint), the tetrahedron lemma (section 7) is an exact integer
branch-and-bound.  Section 10 lists exactly what is still taken on faith.

Labels: **PROVED-HERE** = a complete written proof is given in this file; **CERT** = inequality certified by the Arb program named, whose
output is quoted; **NUMERICAL** = floating/Monte-Carlo evidence that is NOT used by the proof; **STANDARD** = elementary geometry or calculus
used without proof (listed in section 10).  The argument is NOT machine-checked in a proof assistant.

## 0. Statement

**Theorem.** Let P be any packing of regular tetrahedra of one edge length (closed tetrahedra with pairwise disjoint interiors in R^3, any positions).
Its upper density  limsup_{L->inf} sup_x vol(P cap (x+[0,L]^3))/L^3  is at most 1/(1+b) <= 1 - b/(1+b), where  b >= 4.501166e-15  (certified, section 9).
Hence density <= 1 - 4.5011e-15.  (The published value is 1 - 2.6e-25.)

Scale: edge length 1, tetrahedron volume v_t = sqrt2/12, theta = arccos(1/3) (dihedral angle), alpha = theta/(2 pi) = 0.1959132760...,
B = closed unit ball centred at c, B_r = closed ball of radius r about the same centre, vol(B)/v_t = VBT.

---------------------------------------------------------------------------------------------------------------------------------
## 1. Objects

* A **B-wedge** is W = B cap H1 cap H2, H_i = {x : n_i.x <= s_i}, with unit normals satisfying n1.n2 = -1/3 (dihedral angle theta) and arbitrary
  real offsets s_i.  If some s_i >= 1 the half-space is redundant; W is then a **B-cap** (one plane) or B itself (both redundant); W may be empty.
  The **edge line** is {n1.x = s1, n2.x = s2}; e(W) = its distance from c (infinity if some s_i is redundant, i.e. for caps).
  W is **centred** if c lies on the edge line (s1 = s2 = 0); a centred wedge has surface fraction alpha on dB and volume fraction alpha.
  The same names are used for a ball B(c', r) in place of B (a "B(c',r)-wedge").  Intersecting a B_R-wedge with B_r (r <= R) gives a B_r-wedge.
* Fraction of a set S in B: vol(S)/vol(B); surface fraction: area(S cap dB)/area(dB).
* **E1 (traces).**  Let O be a B-wedge with non-empty interior and p a point of the relative interior (inside the sphere dB) of O cap dB.  Then p lies in int H1 and int H2 (a point of dB on a bounding plane is a boundary point of
  the trace relative to dB because the plane cuts the sphere transversally or is tangent), so a neighbourhood of p in B is contained in O.  Two interior-disjoint objects therefore have traces on dB with disjoint relative interiors,
  and the boundary of a trace is a finite union of circle arcs (measure zero): **surface fractions of interior-disjoint objects add up to <= 1** (STANDARD).
* If O is an object in B with c not in int O, then c is on one side of a plane: O lies in a half-space H with c not in int H, so vol(O)/vol(B) <= 1/2 (E2, STANDARD).
  If W0 is a centred wedge and O is interior-disjoint from W0, then c is not in int O (c is in the closure of int W0).
* **Classes.** K(c,w) = all families of pairwise interior-disjoint objects in B: one centred wedge W0, at most c caps ("cap slots"), at most w-1 further wedges
  ("wedge slots"; a cap or the empty set may occupy a wedge slot).  Empty objects are allowed (they have e = delta = infinity).
  M(K) = 1 - vol(union K)/vol(B);  rho(c,w) = inf_{K in K(c,w)} M(K).
  Partial order (c,w) <= (c',w') :<=> w <= w' and c+w <= c'+w'.  Then K(c,w) subset K(c',w') (surplus caps go to the extra wedge slots), so rho(c,w) >= rho(c',w').
* delta(O) = dist(c,O) (<= e(O)).

---------------------------------------------------------------------------------------------------------------------------------
## 2. Base values and Lemma A

* rho(0,1) = 1 - alpha;  rho(1,1) = rho(0,2) >= 1/2 - alpha (second object has fraction <= 1/2 by E2).
* **Lemma A (PROVED-HERE).** Let W0 be a centred wedge and C_1..C_n (n >= 2) caps, pairwise interior-disjoint and disjoint from W0.  Then
  sum vol(C_i)/vol(B) <= F := 1 - alpha - sqrt2/(3 pi) = 0.654034...  Hence rho(c,1) >= sqrt2/(3 pi) = 0.150052... for c >= 2.
  *Proof.* Slice by planes z = h orthogonal to the edge of W0 (|h|<1).  The slice of B is a disc D of radius R = sqrt(1-h^2) centred on the axis at O';
  W0 cap D is the open sector S of opening theta at O'.  A cap slices to D cap P, P a half-plane (if its boundary plane is parallel to the slice plane the slice is empty or all of D;
  all of D would contain S, impossible; so empty or half-plane).  If O' were in int P then P and S would overlap near O', so O' is not in int P: the chord of P is at distance
  d' >= 0 from O' and D cap P is a circular segment whose arc on dD has half-angle rho_i = arccos(d'/R) in [0, pi/2] and area fraction s(rho_i) = (rho_i - sin rho_i cos rho_i)/pi of D.
  The arcs of the segments and the arc of S on dD are pairwise interior-disjoint (overlapping arcs would give overlapping regions near dD), so 2 sum rho_i + theta <= 2 pi.
  s is convex on [0,pi/2] (s'' = 2 sin(2 rho)/pi >= 0), so sum s(rho_i) over the polytope {0 <= rho_i <= pi/2, sum rho_i <= pi - theta/2} is maximal at a vertex;
  since pi - theta/2 = pi/2 + (pi/2 - theta/2) with pi/2 - theta/2 < pi/2 and 2 (pi/2) > pi - theta/2, the vertices are: the origin, (pi/2, 0, ..., 0) (value 1/2), and the permutations of (pi/2, pi/2 - theta/2, 0, ..., 0) (the budget constraint active, exactly one coordinate strictly between its bounds); the largest value is at the last type; it is
  s(pi/2) + s(pi/2 - theta/2) = 1/2 + (pi/2 - theta/2 - sin(theta)/2)/pi = 1 - alpha - sin(theta)/(2 pi), and sin(theta) = 2 sqrt2/3.  Slices with fewer than two caps give <= 1/2 <= F.
  Integrating over h (the bound is a fixed fraction of the disc area in every slice) gives the claim.  Then M >= 1 - alpha - F.  QED.

---------------------------------------------------------------------------------------------------------------------------------
## 3. Lemma K1 (area of a wedge) and Corollary K2

Define  G(e,t) = sqrt(1-e^2) - e t arccos( e t / sqrt(1-e^2+e^2 t^2) )  (0 <= e < 1, |t| <= 1)  and
**a(e) := (1/(2 pi)) int_{-theta/2}^{theta/2} G(e, cos phi) dphi.**

### 3.1 Closed form (PROVED-HERE)
For 0 < e < 1 put k = sqrt(1-e^2) and z = e cos(phi).  Then (d/dz) arccos(z/sqrt(k^2+z^2)) = -k/(k^2+z^2) and k^2 + e^2 cos^2(phi) = 1 - e^2 sin^2(phi), so
(d/dphi) arccos(e cos(phi)/sqrt(1 - e^2 sin^2 phi)) = k e sin(phi)/(1 - e^2 sin^2 phi).  Let Phi = theta/2 < pi/2 and f = e cos(Phi)/sqrt(1 - e^2 sin^2 Phi).  Integration by parts gives
  int_0^Phi e cos(phi) arccos(.) dphi = e sin(Phi) arccos(f) - k e^2 int_0^Phi sin^2(phi)/(1 - e^2 sin^2 phi) dphi,
  int_0^Phi sin^2(phi)/(1 - e^2 sin^2 phi) dphi = (1/e^2) [ (1/k) arctan(k tan Phi) - Phi ]   (since int dphi/(1 - e^2 sin^2 phi) = (1/k) arctan(k tan phi)).
Hence, writing I := int_0^Phi sin^2 phi/(1 - e^2 sin^2 phi) dphi and using G = k - e cos(phi) arccos(.),
  int_0^Phi G dphi = k Phi - [ e sin(Phi) arccos f - k e^2 I ] = k Phi - e sin(Phi) arccos f + [ arctan(k tan Phi) - k Phi ] = arctan(k tan Phi) - e sin(Phi) arccos f.
Now sin(theta/2) = 1/sqrt3, cos(theta/2) = sqrt(2/3), tan(theta/2) = 1/sqrt2, 1 - e^2 sin^2(theta/2) = (3-e^2)/3, so f = e sqrt2/sqrt(3-e^2), and a(e) = (1/2 pi) 2 int_0^Phi G dphi gives:

  **a(e) = (1/pi) [ arctan( sqrt((1-e^2)/2) ) - (e/sqrt3) arccos( e sqrt2 / sqrt(3-e^2) ) ].**                    (3.1)

(a(0) = arctan(1/sqrt2)/pi = theta/(2 pi) = alpha.)  Check, not used: `code/k1_check.py` (output `code/k1_check.out`): Arb quadrature of the defining integral minus (3.1) is within 1e-35 of 0 at nine values of e in (0,1);
(3.1) agrees with the Gauss-Bonnet form used by earlier versions to 2e-16.  The program `a_lo` in `fullchain.py` evaluates exactly (3.1).

### 3.2 Lemma K1 (PROVED-HERE)
**Statement.** Let W be a B-wedge (definition of section 1, caps and B included) and 0 <= r < 1.  If W meets B_r then surface fraction of W >= a(r); a is non-increasing on [0,1).

*Proof.*  Step 1.  Let p in W cap B_r.  Put W' = {n_i.x <= n_i.p, i=1,2} cap B.  Since p in W, n_i.p <= s_i, hence W' subset W.  The edge line of W' passes through p, so e' := dist(c, edge(W')) <= |p| <= r < 1.
It suffices to show: for every wedge W' with outward normals n1.n2 = -1/3 and edge line at distance e < 1: surface fraction >= a(e), and a(e) >= a(r) (Step 6).

Step 2 (formula).  Choose coordinates with the edge along the z-axis, passing through P = (e, 0) of the xy-plane, c = origin.  W' is the cylinder over a planar wedge W2 of opening theta with apex P and boundary
rays in directions phi1 and phi1 + theta.  The sphere dB projects 2-to-1 onto the unit disc D, area element 2 du/sqrt(1-|u|^2) in the disc.  In polar coordinates about P, along direction phi:
|u|^2 = e^2 + 2 e t cos(phi) + t^2 and, with v = t + e cos(phi) and K^2 = 1 - e^2 + e^2 cos^2(phi),
 int_0^{T} t dt / sqrt(1 - e^2 - 2 e t cos phi - t^2) = int (v - e cos phi) dv / sqrt(K^2 - v^2) = sqrt(1-e^2) - e cos(phi) arccos(e cos(phi)/K) = G(e, cos phi)
(T = exit parameter; every ray from P in D exits since P is interior).  Hence surface fraction of W' =
 A(e,phi1) = (1/4 pi) int 2 du/sqrt(1-|u|^2) = (1/(2 pi)) int_{phi1}^{phi1+theta} G(e, cos phi) dphi.                                         (3.2)
(Checked by Monte Carlo, `code/k1_check.out`, NUMERICAL.)

Step 3 (G strictly decreasing in t).  For e > 0 put k = sqrt(1-e^2), z = e t, psi = arctan(z/k): dG/dz = -arccos(z/sqrt(k^2+z^2)) + z k/(k^2+z^2) = -(pi/2 - psi - sin psi cos psi) =: -q(psi);
q(pi/2) = 0 and q'(psi) = -2 cos^2 psi < 0, so q > 0 on (-pi/2, pi/2).  So G(e,.) is strictly decreasing.

Step 4 (critical points).  From (3.2), dA/dphi1 = (1/2 pi)(G(e,cos(phi1+theta)) - G(e,cos phi1)); by Step 3 it vanishes iff cos(phi1+theta) = cos(phi1), i.e. 2 phi1 + theta = 0 mod 2 pi: exactly two critical
points on the circle: "away" phi1 = -theta/2 (the wedge is symmetric about the positive x-axis, opening away from c) and "toward" phi1 = pi - theta/2.  A smooth function on the circle attains its minimum at a critical point.

Step 5 (the two values).  A_away(e) = (1/2 pi) int_{-theta/2}^{theta/2} G(e,cos phi) dphi = a(e) by definition.  A_toward = (1/2 pi) int_{-theta/2}^{theta/2} G(e, -cos psi) dpsi >= A_away because
-cos psi < cos psi for |psi| < pi/2 and G is decreasing.  So min over phi1 = a(e) (for e = 0 the function A is constant = alpha = a(0)).

Step 6 (monotone).  The "away" wedge with apex at distance e' > e on the same axis is contained in the one with apex at distance e (its apex lies in the larger wedge and both are translates of the same cone), so
the traces satisfy a(e') <= a(e) (the closed form (3.1) is used only for e' < 1, where it equals the area of the trace).  QED.  (NUMERICAL corroboration, not a proof input: `code/k1_random.out` -- 300 random wedges, smallest (Monte-Carlo fraction - a(dist)) = -0.00042, within the Monte-Carlo noise 0.0008; `code/k1_check.out`.)

### 3.3 Corollary K2 (PROVED-HERE)
Let K be a family of pairwise interior-disjoint objects in B, one of them centred (W0), and let q >= 1 be such that alpha + q a(gamma) > 1 (0 <= gamma < 1).  Then at most q objects (counting W0) meet B_gamma.
*Proof.* By E1 the traces add up to <= 1; W0 contributes alpha, every other object meeting B_gamma contributes >= a(gamma) (K1, a decreasing).  If n other objects meet B_gamma then alpha + n a(gamma) <= 1; since alpha + q a(gamma) > 1 this forces n <= q - 1.  QED.
Define gamma_q = the largest float certified (by Arb, `fullchain.gamma_lo`) with alpha + q a(gamma_q) > 1; by monotonicity K2 holds for every radius <= gamma_q.

---------------------------------------------------------------------------------------------------------------------------------
## 4. Lemma K3 (nested-ball replacement; the construction of GEK Lemma 4.2) -- PROVED-HERE

**Setting.** Objects O_0 = W0 (centred wedge), O_1..O_m: pairwise interior-disjoint objects in B (wedges, caps, B, or empty), none with c in its interior (E2 shows this follows from disjointness from W0).
Let 0 < s <= 1, G = int B_s.  c = 0.

**Lemma K3.** There is a finite family F' of pairwise interior-disjoint B_s-wedges (W0 cap B_s among them, as a centred wedge) such that
(i) vol(union F') >= vol(B_s cap union O_i);  (ii) every member is W0 cap B_s, or O_i cap B_s with O_i a wedge whose edge line meets G (that is e(O_i) < s), or a B_s-cap;
(iii) the number of members is at most 1 + #{i >= 1 : O_i cap G nonempty}.
Consequently M(K) >= s^3 M(F'/s) where F'/s is F' scaled by 1/s: (c, w) types are controlled as follows: if exactly k' non-central wedge slots of K have e < s, then F'/s is in K(c'', w'') for every
(c'', w'') with w'' >= 1 + k' and c'' + w'' >= 1 + #{objects of K meeting G}.

*Proof.* Objects with O cap G empty (up to the boundary of G) are discarded.  Objects with e(O) < s, caps, B, and W0 are **kept** as O cap B_s.  Let O = B cap H1 cap H2 be a wedge with edge line l missing G.
Let P_j = dH_j, D_j = P_j cap G.  The planes meet exactly in l, so D_1 cap D_2 = empty.
* *No plane cuts G.*  Then G lies in or outside each H_j; O cap G is empty or G; G subset O would put c in int O.  So empty.
* *One plane (P_j) cuts G.*  Then O cap G is empty or G cap H_j (the other half-space contains G or misses it); in the latter case c not in int H_j (else c in int O), and O cap B_s = B_s cap H_j is a B_s-cap: **kept**.
* *Both planes cut G.*  D_1 and D_2 are disjoint non-empty planar sections of the convex open set G.  P_1 splits G \ P_1 into two open convex sides; D_2 is connected and misses P_1, so it lies in one of them: call it G_1^m and the other G_1^a.
  Likewise P_2 gives sides G_2^m (containing D_1) and G_2^b.  **G_1^a cap G_2^b = empty:** if x were in it, take z in D_2; the segment [x,z] lies in G and crosses P_1 at a point w of D_1 (x and z are on different sides of P_1), w lying strictly between x and z;
  x and w are on different sides of P_2 (x in G_2^b, w in D_1 subset G_2^m), so the segment [x,w] would meet P_2, but the line xz meets P_2 only at z, which is not between x and w: contradiction.  Hence G minus (P_1 cup P_2) is the disjoint union of three open convex sets
  R_a := G_1^a (subset G_2^m), R_m := G_1^m cap G_2^m, R_b := G_2^b (subset G_1^m); D_1 subset cl R_m and D_2 subset cl R_m.  The open set int O cap G is one of R_a, R_b, R_m (or empty).
  If it is R_a (resp. R_b) it equals G cap int H_j for the half-space H_j whose open side is G_1^a (resp. G_2^b), so O cap B_s = cl(int O cap G) = B_s cap H_j is a B_s-cap: **kept**.
  If it is R_m ("middle type"): c is not in R_m (open and inside int O), so c lies in the closure of exactly one of R_a, R_b (the closures are disjoint: D_1 and D_2 are disjoint and R_m separates them); call the other one R^far,
  P_f the plane bounding the disc D_f between R_m and R^far, P_n the other plane, H_n the half-space of P_n containing R_m, H_f the half-space of P_f containing R_m.  Since c is in cl of the near region and not in cl R^far, R^far = G cap {n_f.x > s_f}
  with s_f > 0 (c is in H_f, s_f >= 0, and s_f = 0 would put c in the closure of R^far).  So R^far is an open convex "cap of G whose closure misses c".
  Replace O by the cap  C(O) := B_s cap H_n = cl(R_m cup D_f cup R^far); c is not in int H_n; vol(C(O)) >= vol(O cap B_s).

**Lemma Z.** If O is of middle type and O' is any other object with int O' cap R^far(O) nonempty, then int O' cap G subset R^far(O); hence O' cap B_s subset cl R^far(O).
*Proof.* U = int O' cap G is open convex and U cap R_m(O) = empty (R_m(O) subset int O, interiors disjoint).  Suppose U contains z in R^far and a point o outside R^far.  The segment [z,o] lies in U subset G; it leaves the half-space {n_f.x > s_f}
at a point q (q = o possible) of D_f.  Since q in U and U is open, U contains points of R_m(O) near q (D_f subset cl R_m(O), R_m(O) subset H_n on the near side of D_f): contradiction.  The closure statement: O' cap B_s = cl(U) if U is non-empty.  QED

**Radial structure.** For middle type O and any x in R^far(O), the segment [0,x] meets R_m(O): the point z_f at which it crosses P_f lies in D_f subset int H_n (D_f is disjoint from P_n and adjacent to R_m),
and points of the segment just before z_f are in H_f and in int H_n, i.e. in R_m(O).  Also for x in R^far and lambda >= 1 with lambda x in G: lambda x in R^far (s_f > 0).

**Lemma N.** Let O, O' be middle type with R^far(O) cap R^far(O') nonempty.  Then after renaming, O' cap B_s subset cl R^far(O) and R^far(O') subset R^far(O).
*Proof.* Take q in the intersection.  On the segment [0,q] the radial structure gives open intervals I = [0,q] cap R_m(O) and I' = [0,q] cap R_m(O'), each ending where the respective far plane is crossed; since R_m(O) subset int O and R_m(O') subset int O' they
are disjoint; rename so that I comes first: every point of I' lies strictly beyond the far plane P_f(O), i.e. in R^far(O).  Thus R_m(O') cap R^far(O) is non-empty, and Lemma Z (with the object O') gives int O' cap G subset R^far(O), so O' cap B_s subset cl R^far(O).
For x in R^far(O') the segment [0,x] meets R_m(O') at y = mu x, 0 < mu < 1; y in R^far(O) means n_f.y > s_f > 0, so n_f.x > n_f.y > s_f: x in R^far(O).  QED

**Assembly.** Order by the relation P < O :<=> O is of middle type, P != O and P cap B_s subset cl R^far(O).  The same argument as in Lemma N (y in R_m(P) subset int P cap G subset R^far(O) ... for P of middle type: R^far(P) subset R^far(O))
shows that if P < O then R^far(P) is a proper subset of R^far(O) for middle-type P (proper because R_m(P) subset R^far(O) is disjoint from R^far(P)), and that < is transitive on middle types; hence < is acyclic on a finite set.
**Delete** every object P with P < O for some O.  Replace every surviving middle-type O by C(O); keep the other survivors as O cap B_s; W0 survives (c in W0 cap B_s but c not in cl R^far(O) for any O).
* *Covering.*  A survivor is inside its member.  A deleted P has P cap B_s subset cl R^far(O*) subset C(O*) for a <-maximal O*, which is not deleted.  So (i).
* *Disjointness* (interiors, only int cap G matters, and open sets that are non-empty meet in a set of positive volume, so it suffices to compare the open regions).
  (a) two kept originals: disjoint by hypothesis.  (b) kept P' vs C(O): int P' cap R_m(O) subset int P' cap int O = empty; if int P' cap R^far(O) were non-empty, Lemma Z gives P' < O, so P' was deleted; for P' = W0 that would put c in cl R^far(O), impossible.
  (c) C(O), C(O') survivors of middle type: R^far(O) cap R^far(O') = empty (else Lemma N makes one deleted); R_m(O) cap R^far(O') = empty (else Lemma Z applied to the middle-type O' makes O < O', deleted); symmetric; R_m(O) cap R_m(O') = empty (interiors).
  The members are B_s-wedges or B_s-caps, so (ii).  (iii) holds because each member comes from a distinct object meeting G.
* *Scaling.*  M(K) = 1 - vol(union O_i)/vol(B) >= (vol(B_s) - vol(union F'))/vol(B) = s^3 M(F'/s).  Types: members that are wedges with centre c not on the edge are exactly the kept wedges with e < s (at most k'), and W0 cap B_s is the centred wedge;
  all other members are caps, at most (#objects meeting G) - k'; so F'/s is in K(#caps, 1+k') and thus in K(c'',w'') for the stated pairs by the partial order (surplus caps occupy wedge slots).  QED

(The case flagged by an earlier reviewer -- an edge line outside the ball with both faces cutting it -- is exactly the middle-type case; it is handled by the cap C(O) together with the deletions.
`code/k3_check.py` is a randomised sanity test of the construction (NUMERICAL, not a proof input): 150 families of exactly pairwise-disjoint objects (disjointness certified by a convex program) each containing a middle-type wedge, 72 nested deletions occurred, 0 violations of disjointness of the new family, 0 uncovered volume (`code/k3_check.out`).
(An earlier version of the test with sample-based disjointness reported 4 "overlaps" in 500 families; in each of them the original objects themselves overlapped in 2-3 sample points, and Lemma Z does not apply to overlapping originals; the exact-disjointness version removes that artefact.)

*Comparison with GEK's printed proof of their Lemma 4.2* (arXiv:1008.2830, section 4; read once for this file): they replace a wedge whose edge misses B_r by the cap formed with the component of B_r minus W not containing the centre, and say
that "as a final step we remove from K' any cap or wedge contained within these added disconnected components".  The statement of the construction is the same as above and was not found wrong.  The printed proof does not argue (1) that an object
meeting an added component is entirely contained in it (our Lemma Z: the only way an object can meet R^far(O) without overlapping O) nor (2) how two added components relate (our Lemma N: nested or disjoint); without (1) and (2) the new family could overlap.  Lemmas Z and N supply both.

---------------------------------------------------------------------------------------------------------------------------------
## 5. Lemma V2 (volume of one wedge) -- PROVED-HERE modulo the certified computation of section 5.2

**Statement.**  Let W be a B-wedge with c not in int W and edge line at distance <= e from c (e <= 0.9).  Then vol(W)/vol(B) <= alpha + E(e), E(e) := (3/(4 pi)) sup_{0<=t<=e} [ Vslab(t, s2max(t,e)) - Loss(t) ] where
(kappa = cos theta = 1/3, sin theta = 2 sqrt2/3, bracket(y) = pi - arccos y + y sqrt(1-y^2), R^2 = 1 - x^2)
 A(x; s1) = R^2 bracket( (s1 + kappa x)/(R sin theta) ),  Vslab(t,s2) = int_0^{s2} A(x;-t) dx,  Bl(x) = R^2 bracket( -kappa x/(R sin theta) ),  Loss(t) = int_0^t Bl(x) dx,
 s2max(t,e) = kappa t + sqrt((1-kappa^2)(e^2-t^2)).
For edge distance > 0.9 (or for caps) vol(W)/vol(B) <= 1/2 (E2); we use E(e) := 1/2 - alpha there.

**Proof.** c = 0, W = {n1.x <= s1} cap {n2.x <= s2} cap B.  c not in int W: some s_i <= 0; call that face 1, t := -s1 >= 0.  If s2 <= 0, W lies in the centred wedge C = {n1.x<=0,n2.x<=0} cap B, fraction alpha.  Let s2 > 0.  Exactly:
W \ C = {n1.x <= -t, 0 < n2.x <= s2} cap B and C \ W = {-t < n1.x <= 0, n2.x <= 0} cap B (as n1.x <= -t < 0 forces the n2 condition, and n2.x <= 0 <= s2), so vol(W) = vol(C) + vol(W\C) - vol(C\W).
(i) Slice W\C by planes n2.x = x (0 < x <= s2): a disc of radius R = sqrt(1-x^2) centred x n2.  Write n1 = n1par - kappa n2 with n1par orthogonal to n2, |n1par| = sin theta; for the point x n2 + u the condition n1.x <= -t reads
n1par.u <= kappa x - t, a half-plane at signed distance (kappa x - t)/sin theta from the centre; for |y| <= 1, y = (kappa x - t)/(R sin theta), its intersection with the disc has area R^2 (pi - arccos y + y sqrt(1-y^2)).  This is A(x;-t).
(ii) Slice C\W by planes n1.x = -x (0 <= x < t): disc of radius sqrt(1-x^2) centred -x n1; n2.(point) = n2par.u + kappa x <= 0 is a half-plane at signed distance -kappa x/sin theta: area Bl(x).
(iii) The point of the edge line {n1.x = -t, n2.x = s2} closest to 0 is a n1 + b n2 with a - kappa b = -t, b - kappa a = s2 (solve), and its squared norm is a(-t) + b s2 = (s2^2 + t^2 - 2 kappa t s2)/(1 - kappa^2).
It is <= e^2 iff s2 <= s2max(t,e) and t <= e.  (The edge line lies in the plane n1.x = -t, so dist >= t.)  By Cauchy-Schwarz s2max <= e.
So vol(W)/vol(B) <= alpha + (3/(4 pi)) [Vslab(t,s2) - Loss(t)] with 0 <= t <= e, 0 < s2 <= s2max(t,e).  QED.

### 5.2 Certified evaluation (CERT) -- `fullchain.E2_up_exact`, `fullchain.E_up`
All |y| < 1 needed above holds for x <= 0.9, t <= 0.9 (|y| <= 0.955, enforced by Arb: an arccos of a ball not inside [-1,1] gives NaN and the program raises).
For e (an exact float) split t in [0,e] into NT = 36 cells [t0,t1], t_i = e (i/36)^2.  For t in a cell: A(x;-t) is non-increasing in t (the half-plane threshold decreases), Bl >= 0, so
 Vslab(t,s2) <= int_0^{S} A(x;-t0) dx  with S = min(e, kappa t1 + sqrt((1-kappa^2)(e^2-t0^2))) >= s2max(t,e)  (s2max is increasing in kappa t and decreasing in the square root; Cauchy-Schwarz gives <= e),
 Loss(t) >= Loss(t0) >= right-endpoint sum of Bl (Bl is decreasing since R^2 and bracket(y) with y -> more negative both decrease).
The integral of A is bounded above by NX = 48 cell sums of (Arb enclosure of A over the cell).upper() times the cell width rounded up; Loss below by 48 right-endpoint terms with widths rounded down.  The cell values are maximised.
`E_up(u)` returns the value at the first element of the grid 1e-5 * 1.012^k (up to EMAX = 0.9) that is >= u (E is non-decreasing in e: the constraint set only grows), or 1/2 - alpha if u > 0.9.
Sanity (NUMERICAL, `code/v2_check.out`): slice formula vs Monte Carlo volumes (agree to 1e-4); for 5716 random wedges (excess volume) <= E_up(e) in all cases, largest ratio 0.9973.

---------------------------------------------------------------------------------------------------------------------------------
## 6. Lemma R (recursion for rho(c,w)) -- PROVED-HERE modulo K1, K3, V2, A and the certified computation

For K in K(c,w) let the non-central objects be listed; wedge slots have e_j = e(O_j) (infinity for caps/empty), all objects delta_j.  Let t* := w alpha + c/2.

**(R1) for t* < 1.**  Let e_(1) <= ... <= e_(w-1) be the sorted wedge-slot edge distances and rho_k := rho(c+w-1-k, 1+k) (certified lower bounds already known).
(a) For k = 0..w-2:  M(K) >= min(e_(k+1),1)^3 rho_k.  [K3 with s = min(e_(k+1),1): at most k wedge slots have e < s, so F'/s lies in K(c+w-1-k, 1+k) by K3's type statement.]
(b) M(K) >= VOL := 1 - w alpha - capvol(c) - sum_{j} Etilde(e_j), capvol(0)=0, capvol(1)=1/2, capvol(c>=2)=F (E2 and Lemma A),
    Etilde = E (Lemma V2) for e <= 0.9 and 1/2 - alpha otherwise (E2).  [W0 has fraction alpha, a wedge slot has fraction <= alpha + Etilde(e_j), caps <= capvol(c).]
*Certified form* `cert_lt1(c,w,T)`: T (float) is accepted iff  1 - w alpha - capvol_up(c) - sum_{k=0}^{w-2} E_up( upper((T/rho_k)^{1/3}) ) - T >= 0  as an Arb inequality (lower end of the ball >= 0).
Then M(K) >= T for every K in K(c,w): if M(K) < T, (a) gives min(e_(k+1),1) < (T/rho_k)^{1/3} =: u_k (for e_(k+1) >= 1 we get u_k > 1), hence Etilde(e_(k+1)) <= E_up(u_k) (E non-decreasing), so M(K) >= VOL >= RHS >= T, contradiction.

**(R2) for t* >= 1** (the code uses cert_gt1 whenever t* >= 1).  Sort the non-central objects by delta: delta_(1) <= ... <= delta_(m), m = c+w-1, with the type sequence sigma (cap slot / wedge slot).  Let
rho_{i-1}^sigma := rho(#cap slots, 1 + #wedge slots among the first i-1) (state of fewer objects, certified earlier; i = 1 gives rho(0,1)).
(a) M(K) >= min(delta_(i),1)^3 rho_{i-1}^sigma  for every i: apply K3 with s = min(delta_(i),1) (or s slightly smaller): the objects meeting G are among the first i-1; F'/s lies in K(type of the first i-1) by K3.
(b) coverage: alpha + sum_i A_{sigma_i}(delta_(i)) <= 1 where A(delta) >= a(delta) for wedge slots (K1: the object meets B_delta) and A(delta) = (1-delta)/2 for caps (exact trace of a cap at distance delta<1); 0 if delta >= 1 (E1).
(c) if at least two caps meet B: sum of cap volumes <= F (Lemma A); a cap at distance delta<1 has volume fraction (1-delta)^2 (2+delta)/4, decreasing in delta.
*Certified form* `cert_gt1(c,w,T)`: for every type sequence sigma with c cap slots, with u_i := upper((T/rho_{i-1}^sigma)^{1/3}) and skipping every i with u_i >= 1 (not certainly < 1),
 cov := sum over the remaining i of  (1-u_i)/2 (cap slot) or a_lo(u_i) (wedge slot)  satisfies  cov.lower > upper(1 - alpha),  or (at least two cap slots remaining and sum (1-u_i)^2(2+u_i)/4 .lower > upper(F)).
Then M(K) >= T: if M(K) < T, (a) gives delta_(i) < u_i for all i with u_i < 1 (for delta_(i) >= 1 (a) gives rho_{i-1}^sigma <= M < T, i.e. u_i > 1, skipped), and monotonicity of A, volume in delta gives cov <= sum A(delta_(i)) <= 1 - alpha,
resp. cap volume <= F, contradicting the certified alternative for the actual sigma.

**(R3) Monotone closure.**  After each state, rho(k) := max(rho(k), rho(k2)) for k <= k2 in the partial order (inclusion of classes).  The chain: base values (section 2); states (c,w), 2 <= w <= 5, c+w <= 5, in order of c+w;
then (0,w) for w = 6..41 by (R2) with rho(0,w) := min(certified T, rho(0,w-1)) (class inclusion).  Each T is found by bisection on the *certified* predicate (largest T for which cert_* returned True, so the stored value is certified by construction);
`verify_final.py` re-certifies every stored value from scratch, plus the base values.

**Result (CERT, `code/build_eps1000.out`, `code/verify_final.out`).**

| state | t* | certified lower bound of rho | state | t* | certified lower bound |
|---|---|---|---|---|---|
| (c>=2,1) | | 0.150052 (Lemma A) | (0,4) | .784 | 1.000423e-06 |
| (1,2), (0,3) | .892, .588 | 3.483101e-03 | (1,4) | 1.284 | 1.566597e-07 |
| (2,2), (3,2) | 1.392, 1.892 | 7.335398e-04 | **(0,5)** | .980 | **1.273845e-11** |
| (1,3), (2,3) | 1.088, 1.588 | 1.029911e-05 | (0,6..41) | >1 | 5.342391e-12 |

---------------------------------------------------------------------------------------------------------------------------------
## 7. Lemma K4 (the tetrahedron-ball lemma; GEK Lemma 3.5) -- PROVED-HERE with constant (3/sqrt2)(1+eps), eps = 1/1000

**Statement K4'.**  Let T be a regular tetrahedron of edge 1, O a point not in int T, r > 0, c' = (3/sqrt2)(1 + eps).  If every vertex of T is at distance > c' r from O, then T cap B(O,r) is a B(O,r)-wedge (possibly a cap, the ball or empty).

**Step N (necessity).**  If fewer than three of the closed face triangles F_i satisfy dist(O,F_i) < r, then T cap int B(O,r) is empty or equals int B cap (intersection of the half-spaces H_i of the faces with dist < r), at most two of them: a wedge of angle theta (two faces of a tetrahedron meet at theta), a cap, or the ball.
*Proof.* S = {i : dist(O,F_i) < r}, |S| <= 2, W = int B cap cap_{i in S} H_i contains T cap int B.  If z in T cap int B and x in W \ T: walk from z to x inside the convex set W; let q be the last point of the segment lying in T (T is closed).  Just beyond q
the segment is outside T, so some face constraint j' is violated immediately after q and active at q.  j' not in S because the points beyond q lie in W subset H_i for i in S.  But q in T cap plane(F_j') = F_j' and q in int B, so dist(O,F_j') < r, i.e. j' in S: contradiction.
If S is empty, int B misses the boundary of T, so int B is in int T (then O in int T, excluded) or int B cap T is empty.  Closing the ball gives the statement for B(O,r).  QED  (NUMERICAL check: `code/k4_necessity_check.out`, 4403 random cases, 0 counterexamples.)

**Step R (ratio lemma; computer proof).**  Let C = (9/2)(1+eps)^2 and D(O) = min over vertices |O-V|.  **Claim R(C):** for every O not in int T, at least two faces satisfy dist(O,F_i)^2 >= D(O)^2/C.
K4' follows from R: if D > c' r then D^2 > C r^2, so those two faces have dist > r, hence |S| <= 2, and Step N applies.
Scale invariance: T = conv{(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)} (edge sqrt8); faces F_k opposite V_k lie in the plane V_k.x = -1, outward normal -V_k (|V_k|^2 = 3), T = {V_k.x >= -1 for all k}.
*Box test.*  For a box X (integer dyadic corners, scaled by 2^30): (i) lower bound of dist^2(O,F_k): h^2 + (max_j out_j^+)^2, where h = |V_k.x+1|/sqrt3 is the distance to the face plane (lower end of the square of an interval) and out_j = m_j.(x-p_j)/sqrt24
are the signed outward distances to the three edge lines of the face inside the face plane (m_j in-plane outward normals of the edge, |m_j|^2 = 24); the distance to the triangle is >= sqrt(h^2 + out_j^2) for every j with out_j > 0 (the triangle lies on the inner side of each edge line).
(ii) upper bound of D^2 on X: min over vertices of max over X of |x-V|^2.  (iii) a box is **certified** if it lies in int T (all four V_k.x+1 > 0 on X), or two faces satisfy C dist_lb^2 >= D2_ub (compared as exact integers: Cn (8 h2 + out2) >= 24 Cd D2 for C = Cn/Cd), or it is outside the symmetry domain.
*Symmetry.*  T_d (24 elements: coordinate permutations and even sign changes) maps every point to the domain {x >= y >= |z|}; boxes disjoint from it are discarded.  The program covers [0,5] x [0,5] x [-5,5].
*Far field.*  For |O|_inf > 5 (so |O| > 5): every face distance is >= |O| - sqrt3 and D <= |O| + sqrt3, ratio (|O|+sqrt3)/(|O|-sqrt3) <= 2.07 < sqrt(C): any two faces work.
*Vertex neighbourhood.*  The only vertex in the domain is V0 = (1,1,1); the ratio is 0/0 there, so boxes inside the open cube Q0 = (0,2)^3 are not decided by the main test.  In Q0 the constraint of the opposite face V0.x >= -1 holds automatically (asserted by the code),
so T cap Q0 = cone(V0) cap Q0 with cone(V0) = {V_k.x >= -1, k=1,2,3}.  **Shell lemma:** every O in Q0 \ {V0} with O not in int T is scaled by 2^j (j >= 0) about V0 into the shell S = {1/2 <= |O-V0|_inf < 1}; cone distances and |O-V0| scale linearly;
the distance to the plane of the opposite face does not decrease relative to the scaled value: h_0(O) >= h_0(O_j)/2^j since h_0 = (4 + V0.u)/sqrt3 (u = O - V0): (4 + s) >= (4/lambda + s) for lambda = 2^j >= 1.  The box test on S uses for the three faces through V0 only the two edge lines through V0 (out_j) plus the plane distance, for the opposite face only the plane distance,
and D replaced by |O - V0| >= D.  A box of S inside the cone interior needs no cover (it would give O in int T).
Therefore a certificate of the box test on S gives R(C) for all O in Q0 \ {V0}.
*Result (exact integer arithmetic, `code/k4_bb.py`).*  eps = 1/1000, C = 9018009/2000000 = 4.5090045: main region 28959 boxes, shell 228811 boxes, unresolved 0, `RESULT: PROVED (all boxes certified)` (`code/k4_bb_eps_1_1000.out`).
Negative control: with C = (9/2)(1-1/100)^2 < 9/2 the same program fails (`code/k4_bb_negative_control_eps_-1_100.out`, ends `RESULT: NOT PROVED`), as it must since R(9/2) is tight:
NUMERICAL (`code/k4_num.out`, `code/k4_relax.out`): sup_O D/r_3(O) = 3/sqrt2 = 2.1213203436 on a curve of points in a face plane.  So GEK's constant is correct and cannot be proved by branch-and-bound with eps = 0; eps = 1/1000 is enough here (section 9).
**K4' is proved for eps = 1/1000.**

---------------------------------------------------------------------------------------------------------------------------------
## 8. The counting scheme (Claims 1-3, boundary) -- PROVED-HERE modulo the lemmas above

**K5 (elementary, STANDARD).**  If P is on an edge of T at distance >= d from both endpoints, the plane of each of the two faces not containing that edge is at distance >= d sqrt(2/3) from P (the edge makes angle with sin = sqrt(2/3) with the face plane through one endpoint, the distance is t sqrt(2/3) with t the distance to that endpoint),
so T cap B(P, rho) is the B(P,rho)-wedge H1 cap H2 cap B(P,rho) with centre on its edge (a centred wedge) for rho <= sqrt(2/3) d.

**Parameters.**  Q, k, u (radius of the "deficit balls"), eps = 1/1000, gamma_Q (K2: alpha + Q a(gamma_Q) > 1), R0 := u/gamma_Q, r_v := (3/sqrt2)(1+eps) R0, sigma := 2u, d := (1 - (k-1) sigma)/2, delta := 2u, R1 := sqrt(2/3) d - 2u.
Checked by Arb (`fullchain.scheme_cert`): d > 2 r_v, d >= 2u, 1/sqrt2 >= 2u, R0 <= sqrt(2/3) d, R1 > 0, 0 < R'' < sqrt(2/3) with R'' := sqrt(2/3) d - r_v, and r_v/R'' < 0.98.

**Pearls.**  On each of the 6 edges of every tetrahedron T of P put k points ("centres") at distances d, d+sigma, ..., d+(k-1)sigma from one endpoint (the last is at distance d from the other endpoint).
A centre c is **good** if no vertex of any tetrahedron of P lies in the closed ball B(c, r_v).

**Claim 1 (deficit of a good centre).**  For a good centre c on T: vol(B(c,u) \ P) >= rho(0,Q) vol(B(c,u)).
*Proof.* T cap B(c,R0) is a centred wedge (K5, R0 <= sqrt(2/3) d).  Every other tetrahedron T' has c not in int T' (c is on the boundary of T) and all its vertices at distance > r_v = c' R0 from c (c good), so by K4' (with r = R0) T' cap B(c,R0) is a B(c,R0)-wedge.
They are interior-disjoint; intersecting with B(c,u) gives B(c,u)-wedges, one centred.  By K2 (alpha + Q a(gamma_Q) > 1 and u = gamma_Q R0) at most Q of them meet B(c,u).  So after scaling, the traces in B(c,u) form a family of K(0,Q), and M >= rho(0,Q).  QED

**Claim 2 (multiplicity).**  Let q be the least integer >= 5 with gamma_q R1 > 2u (certified).  Then every point x lies in at most q of the open balls B(c,u), c good.
*Proof.* Let c_1, ..., c_n be good centres with |x - c_i| < u; then |c_i - c_j| < 2u.  Two centres of the same tetrahedron with distance < 2u: same edge is impossible (spacing sigma = 2u); different edges: adjacent edges with distances s,t >= d from the common vertex have
|c-c'|^2 = s^2 + t^2 - st >= d^2 (convex function, gradient (d,d) >= 0 at the corner (d,d) of the quadrant s,t >= d), and d >= 2u; opposite edges are 1/sqrt2 >= 2u apart.  So the centres belong to pairwise different tetrahedra T_1..T_n.  Fix c_1.
For i >= 2: K5 at c_i (distance >= d from the vertices of T_i, rho = sqrt(2/3) d) shows T_i cap B(c_i, sqrt(2/3) d) is a wedge; B(c_1,R1) is contained in B(c_i, sqrt(2/3) d) since |c_1-c_i| < 2u; thus T_i cap B(c_1,R1) is a B(c_1,R1)-wedge, c_1 not in int T_i (c_1 in T_1).
T_1 cap B(c_1,R1) is a centred wedge (K5, R1 <= sqrt(2/3) d).  All n objects meet B(c_1, 2u), which is inside B(c_1, gamma_q R1).  K2 gives n <= q.  QED
Consequence: sum over good centres of vol(B(c,u) \ P) <= q vol(U \ P), U the union of the balls; the uncovered volume in U is >= (#good) rho(0,Q) vol(B_u)/q.

**Claim 3 (bad centres).**  Fix a vertex w of a tetrahedron T_w and let S be the set of tetrahedra T' != T_w with a centre c' in the closed ball B(w,r_v).  Then |S| <= q_v := floor((1 - Omega)/a(r_v/R'')), Omega = (3 theta - pi)/(4 pi) (vertex solid angle fraction), and at most m_v := floor(2 r_v/sigma) + 1 centres of one T' lie in B(w,r_v).
*Proof.* K5 at c': T' cap B(c', sqrt(2/3) d) is a wedge; B(w,R'') is contained in B(c', sqrt(2/3) d) since |w - c'| <= r_v; so T' cap B(w,R'') is a B(w,R'')-wedge meeting B(w,r_v) (it contains c'), with w not in int T' (w in T_w).
T_w cap B(w,R'') is the vertex cone (R'' < sqrt(2/3) = distance from w to the opposite face), surface fraction Omega (solid angle of a regular tetrahedron vertex 3 theta - pi: STANDARD).  All objects are interior-disjoint, so by E1 and K1:
Omega + |S| a(r_v/R'') <= 1.  Centres of one T' in B(w,r_v) lie on one edge: centres on different edges are >= d > 2 r_v apart (shown in Claim 2), and a closed interval of length 2 r_v contains at most floor(2 r_v/sigma)+1 points of a progression of spacing sigma.  QED
So at most 4 q_v m_v bad centres arise from the 4 vertices of each tetrahedron (a centre of T is never within r_v of a vertex of T itself: d > r_v).

**Boundary / general packings.**  Let P be any packing, L >= 10, C the cube x + [0,L]^3, C' its concentric sub-cube of side L - 2.  N^- = number of tetrahedra contained in C', N_C = number meeting C.  N_C - N^- <= vol((L+2)^3 - (L-4)^3 region)/v_t = O(L^2) (disjoint tetrahedra of diameter 1 meeting the shell).
All good centres of tetrahedra in C' have deficit balls inside C (u < 1).  The number of bad centres among centres of tetrahedra in C' is at most 4 q_v m_v N_C (a vertex within r_v < 1 of such a centre belongs to a tetrahedron meeting C).
So  good >= (6k - 4 q_v m_v) N^- - O(L^2).  Claims 1, 2: vol(C \ P) >= good rho(0,Q) vol(B_u)/q.  With vol(P cap C) <= v_t N_C and N^- >= N_C - O(L^2) >= vol(P cap C)/v_t - O(L^2):
vol(C) >= vol(P cap C) + vol(C \ P) >= vol(P cap C) (1 + b) - O(L^2), where **b := ((6k - 4 q_v m_v)/q) rho(0,Q) (4 pi/3) u^3 / v_t**.
Hence vol(P cap C)/vol(C) <= 1/(1+b) + O(1/L) with a constant independent of P and of x.  This proves the Theorem with the b of section 9.  (For a periodic packing the same argument in the quotient torus, or simply the same estimate with L -> infinity.)

---------------------------------------------------------------------------------------------------------------------------------
## 9. Certified numbers (CERT)

`code/scheme_eps1000_Q40.out` / `code/verify_final.out`:  Q = 40, k = 30, u = 0.01140, gamma_Q = 0.788335, r_v = 0.030707, d = 0.1694, q = 6 (multiplicity), q_v = 7 (area count; the K2-count would be 44), m_v = 3, good per tetrahedron 6k - 4 q_v m_v = 180 - 84 = 96,
rho(0,40) >= 5.342391e-12, hence **b >= 4.501166e-15** and **density <= 1 - 4.501166e-15** with K4' constant (3/sqrt2)(1.001).  Compared with the conditional bound of the stability lens (4.501141e-15, same quantities with the K4 constant (3/sqrt2) exactly assumed) the difference is the finer bisection and the 0.1% K4 slack: the slack costs nothing in b because q, q_v, m_v and the integer good-centre count are unchanged.

---------------------------------------------------------------------------------------------------------------------------------
## 10. Residual trust (what is NOT proved here, or taken on faith)

1. **Software:** Arb/python-flint 0.9.0 (outward rounding of acos, atan, sqrt, pow, ball arithmetic, `union`, `lower`/`upper`), CPython big integers (exact box test of section 7), and the correctness of my two programs `fullchain.py` and `k4_bb.py` relative to the text of sections 5-8 (audited line by line; the K4 program has a negative control; the chain has an independent re-certification pass).
2. **Human-checked paper proofs, not machine-checked:** K1 (section 3), K3 (section 4, including the planar three-region fact), Lemma V2 identities (section 5), Lemma A (section 2), Lemma R logic (section 6), Step N and the box-test/shell/symmetry/far-field reductions (section 7), Claims 1-3 and the boundary count (section 8).  Randomised sanity tests exist for K1, K3, V2, K4 (NUMERICAL, not proof inputs).  No proof assistant was used.
3. **STANDARD facts used without proof:** surface element of the sphere and 2-to-1 projection onto the disc; area of a disc cut by a half-plane; volume/area of a spherical cap ((1-delta)^2(2+delta)/4 and (1-delta)/2); the surface fraction alpha of a centred wedge and the solid angle 3 theta - pi of a regular tetrahedron vertex; elementary distances in a regular tetrahedron (height sqrt(2/3), opposite-edge distance 1/sqrt2, face-edge sine sqrt(2/3)); that a convex function with non-negative gradient at the corner of a quadrant is minimised there; that the minimum of a smooth periodic function is at a critical point; the formula for the minimum of a convex function on a polytope at a vertex; Fubini/measure-theoretic trivialities (traces of interior-disjoint convex sets, finite unions).
4. **Float-to-Arb conversion:** the stored values (json) are python floats and are converted exactly; the rounding helpers `down`/`up` use `nextafter` after `float(...)`; no step relies on a float comparison for soundness (all inequalities are Arb comparisons that are True only when certified).
5. K4 is proved only with the slack eps = 1/1000 (the constant 3/sqrt2 itself is tight and not needed).
Nothing from the literature is used as an unproved input.  Items 2-3 mean that this document is a *written* proof that has not been refereed or formalised; it should not be described as machine-verified.

---------------------------------------------------------------------------------------------------------------------------------
## 11. Retractions and notes (rule 14)

* GEK's Lemma 3.1 proof step "translate the face through the centre; the edge distance does not increase" is false as printed (`code/edge_dist_counter.out`: offsets s1 = -0.3, s2 = 0.9 have edge distance 0.9, and translating plane 1 through c gives 0.9546; the ratio reaches 1/sin theta = 1.0607).  **This chain does not use that step or the statement of GEK Lemma 3.1**: it uses Lemma V2 (section 5), which is proved above directly and checked against Monte Carlo (`code/v2_check.out`).  Whether the printed constant 2.6e-25 of GEK is affected is not decided here.
* Earlier versions of this computation (written by other sessions of this project) used (a) `float(u.upper())` and float comparisons inside the certificates (sub-ulp unsound, no numerical effect), (b) the Gauss-Bonnet closed form for a(r) without a derivation, (c) unproved GEK K1/K3/K4 as inputs, and a minimum of two wedge-volume bounds whose weaker member needed an extra lemma; this file removes (a)-(c).  An earlier code comment said Lemma V2 was valid for e <= 0.5 while the code used EMAX = 0.9; here EMAX = 0.9 is enforced by the Arb domain check (NaN raises).

## 12. File map
| section | code | output |
|---|---|---|
| 3.1 a(e), 3.2 K1 | `fullchain.a_lo`, `k1_check.py`, `k1_random.py` | `k1_check.out`, `k1_random.out` |
| 4 K3 | (paper), `k3_check.py` | `k3_check.out` |
| 5 V2 | `fullchain.E2_up_exact`, `E_up`, `v2_check.py` | `v2_check.out` |
| 6 Lemma R, table | `fullchain.cert_lt1/cert_gt1/solve_state/build`, `verify_final.py` | `build_eps1000.out`, `verify_final.out` |
| 7 K4 | `k4_bb.py`, `k4_num.py`, `k4_relax.py`, `k4_necessity_check.py` | `k4_bb_eps_1_1000.out`, `k4_bb_negative_control_eps_-1_100.out`, `k4_*.out` |
| 8-9 scheme | `fullchain.scheme_cert/scan`, `verify_final.py` | `scheme_eps1000_Q40.out`, `verify_final.out` |
