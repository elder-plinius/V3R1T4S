context: subagent
role: REPRODUCE skeptic A (claim folder `claim/`: bound density <= 1 - 1.0215562e-15)

## 1. Independent re-implementation (written from REDUCTION.md definitions only, before reading `code/*.py`)
Tools: python-flint 0.9.0 (Arb, 200-bit), mpmath, numpy, scipy in a private venv (not the author's).
Definitions implemented as quoted in REDUCTION.md:
- section 1 (K1-K5), Lemma V ("vol(W)/vol(B) <= alpha + E(e), E = min((3/4pi) int_0^e A, 1/2-alpha)"), Lemma A ("F = 1 - alpha - sqrt2/(3 pi)"),
  Lemma R1 ("T = 1 - w alpha - capvol(c) - sum_k Etilde((T/rho_k)^{1/3})"), Lemma R2 ("for every sigma ... sum_i A_lower(u_i) > upper(1-alpha)"), section 4 scheme.
- My E_up uses monotone cell bounds (R^2 decreasing, y increasing, g increasing) with min(y,1), valid on all of [0,1]; my a_lo evaluates the closed form at an exact point and rounds down; bisection to 1e-9 relative, then re-certified.
Results (my chain vs the author's `code/rig_dp.out`):
| state | mine | author |
|---|---|---|
| (1,2), (0,3) | 2.98218e-3 | 2.979110e-3 |
| (2,2), (3,2) | 6.51365e-4 | 6.508480e-4 |
| (1,3), (2,3) | 9.06393e-6 | 9.056212e-6 |
| (0,4) | 7.65911e-7 | 7.637494e-7 |
| (1,4) | 1.20839e-7 | 1.205094e-7 |
| (0,5) | 8.640905e-12 | 8.619948e-12 |
| (0,6..40) | 3.645779e-12 | 3.636896e-12 |
Mine are 0.1-0.3 % higher only because the author shaves 1e-6 and uses 160 cells; every author value is below mine, none above. (c,1), c>=2 = 0.150053 (Lemma A) agrees.
Scheme (my `myscheme.py`, own gamma_q by certified bisection): Q=40,k=38,u=0.0084 gives d=0.1892, gamma_40=0.78834, r_v=0.0226034, q=5, q_v=9, m=2, m_v=3, good=120, Delta=8, all side conditions (d>2r_v, d>=4u, R1>0, R1'>0) true; with rho(0,40)=3.6368e-12, b >= 1.02153e-15 (author 1.0215562e-15 with 3.636896e-12; rounding of the rho input only). Hand check: (120/9)(4pi/3)/v_t * u^3 = 2.809e-4, times 3.637e-12 = 1.0216e-15.

## 2. Author's code, run unmodified (private copy)
`rig_dp.py 150`, `scheme.py 40`, `verify_final.py` in a fresh venv: output identical to REPRODUCE.md's expected lines: "directly verified states: 155 closure-justified: 0", "scheme (Q=40, k=38, u=0.00840): gamma_Q=0.788335 r_v=0.022603 d=0.18920 q=5 q_v=9 m=2 m_v=3 good/tet=120 Delta=8", "rho_hat(0,Q) used = 3.636896e-12 ; b >= 1.021556e-15 ; CERTIFIED density <= 1 - 1.021556e-15". I read `rig_dp.py` (E_up, a_lo, cert_lt1, cert_gt1, solve_state) and `scheme.py` (cert): they implement exactly sections 2-4 (upper rounding of u, lower rounding of coverage, strict inequalities, closure only raises smaller states). E_up returns the cap 1/2-alpha for u>=0.9, which is a valid (trivial) bound.

## 3. GEK source (arxiv.org/pdf/1008.2830, fetched once) vs the KNOWN inputs
- K4 = GEK Lemma 3.5 (vertices at distance > 3r/sqrt2, c not interior): used exactly as printed. I also tested it numerically (1.12e6 random c near edges/vertices, ball radius 0.99999 m sqrt2/3: never more than 2 faces hit; at 1.03 m sqrt2/3 violations appear, so the test has power).
- K2 = GEK Cor. 3.4 (alpha + q a(gamma) > 1 => at most q objects). Author's exact-a gamma_5 = 0.12569 > 0.125, gamma_7 = 0.30529 > 0.304 (GEK, from a Taylor lower bound), consistent.
- K1 = GEK Lemma 3.3: author uses the exact area a(r) of the minimiser W* (an intermediate in GEK's proof, GEK then Taylor-bound it), not the printed polynomial. DEVIATION from the printed statement, but harmless: I verified the closed form equals an independent slice integral of area(W*(r)) (arcs 2 t0(z) dz) to 30 digits at r = 0,.05,.125,.3,.5,.788,.9,.99, and a 2-D scan (41 apex distances x 91 orientations) confirms the "bisector pointing away from centre" orientation minimises the cut arc, as GEK's proof asserts (GEK prove it only as "an exercise in planar geometry"). a(r) is decreasing on [0,1) (checked on a 200-point grid).
- K3 = GEK Lemma 4.2 construction: used for arbitrary s with several retained wedges (GEK only record the one-object-lost consequence). I re-derived the non-overlap of K'_s (edge-in-ball wedges and caps; the connectedness argument shows any other object lies wholly in one complementary cap and is removed) and agree that retained-wedge types (c+w-1-k, 1+k) and their inclusion in larger classes follow.
- GEK Lemma 3.1 is NOT used; replaced by Lemma V. GEK print alpha + 3r sin(theta)/8 + ...; the author's thickness |s2| <= e (instead of e sin theta) is weaker at first order (0.375e vs 0.3536e), so is sound.

## 4. Re-derivation of each new step
- **Lemma V**: valid. W subset W' = {n1x<=0} cap {n2x<=s2} cap B, |s2| <= e because the plane contains the edge; W' = W_c (centred, alpha) + J; slicing J by n2.x = x0 gives exactly A(x0) (disc radius R, half-plane at distance x0 cot theta containing the centre); thus vol(J) = int_0^{s2} A <= int_0^e A (A >= 0, not monotone: A rises first, and the code's ball-per-cell enclosure and my monotone-cell enclosure are both fine). Cap 1/2-alpha valid for every object. Monte-Carlo maximisation over (s1,s2) at e = .02,.05,.1,.3,.6 stays below alpha+E(e) (e.g. e=.3: 0.3051 vs 0.3125).
- **Lemma A**: valid. Slices orthogonal to the axis, O not in the interior of any cap half-plane, footprints disjoint so 2 sum rho_i + theta <= 2 pi, s convex on [0,pi/2] (s''=2 sin 2rho/pi), vertex maximum (pi/2, pi/2-theta/2): s sum = 1 - alpha - sin(theta)/(2 pi) = 1 - alpha - sqrt2/(3 pi). The bound is attained (hemisphere plus a segment of footprint pi - theta), so rho(c>=2,1) = 0.15005 is sharp, not optimistic.
- **Lemma R1**: valid. For any profile, s = min(e_(k+1),1) gives M >= s^3 rho(type); M(K) < T forces e_(k+1) < (T/rho_k)^{1/3} for all k and the monotone Etilde pairing gives M >= RHS(T) >= T, contradiction; the certified form checks RHS(T_lo) - T_lo >= 0. The root is a near-cancellation (1-5 alpha = 0.02043 vs sum E), so the exactness of Lemma V matters; it is exact (no Taylor).
- **Lemma R2**: valid. delta-ordering, K3 at s just below delta_(i), worst-case type with all earlier wedges retained (converting a wedge to a cap only moves into a larger class K(c1+1,w1-1) subset K(c1,w1)), area monotonicity of a and (1-delta)/2, infeasibility checked for every cap/wedge sequence. Pure-wedge states w>=6: only the first five terms matter (u_5 = 0.75, a(0.75) pushes coverage above 1), later terms are >=0 and skipped; rho(0,w) = rho(0,6) for all w<=151 reproduced independently up to w=40. Empty/absent objects are empty wedges at delta = infinity, last in the order.
- **Scheme**: Claim 1 (K4 with R0=u/gamma_Q, r_v=3R0/sqrt2 = R0/kappa; K2 gives <= Q wedges in B(c,u), class K(0,Q)), Claim 2 (K5 distance sqrt(2/3) d to the other faces, B(c,R1) inside B(c'',sqrt(2/3) d), q=5, m=2; adjacent-edge centre distance >= d since a^2+b^2-ab >= min^2), Claim 3 (2 r_v argument, q_v=9, m_v=3, 4*27 = 108 bad), degree <= 8, independent set >= 120N/9, boundary layer O(L^2): all re-derived and consistent with the numbers; margins: gamma_5 R1 = 0.01731 > delta = 0.0168; gamma_9 R1' > delta' certified.

## 5. Residual risks (not mismatches)
- Conditional on GEK's own lemmas (K3 construction, K4 proof, minimality in K1); not machine-checked in a proof assistant; Arb trusted. K1 minimality and K4 were checked only numerically by me.
- Final constant depends on rho(0,40) ~ 3.6e-12; the deficit is 3.9e9 times GEK's 2.6e-25 which is large, but the improvement is explained step by step (exact wedge volume instead of Taylor, profile recursion instead of single radius, sharp Lemma A, Q=40 with exact gamma, 120/9 counting vs GEK's chain) and every step reproduced.
I found no flaw, no mismatch between REDUCTION.md and code, and no misuse of a GEK input beyond the (justified) use of the exact a(r).

pass: true
