# Proof that B >= sqrt(3)/4 + 0.0155 = 0.44851270189...

B is Bloch's constant. Numbers below are checked by the programs named in REPRODUCE.md. Steps marked KNOWN are cited. The rest is proved here.

Notation. r0 = 1/sqrt3. T' = sqrt3/4 + 0.0155. D_r = {|z|<r}. Class 𝓑 = {f holomorphic on D: f(0)=1, (1-|z|^2)|f(z)| <= 1 on D}. Reference [W]: F. Wikstrom, An improved lower bound for Bloch's constant, arXiv 2608.17660v1.

## Reductions

**Step 1 (KNOWN, Landau 1929; [W] sec. 2).** It suffices to show beta(F) >= T' for every F with F(0)=0, F'(0)=1, sup_D (1-|z|^2)|F'(z)| <= 1. Put f=F', so f is in 𝓑.

**Step 2 (KNOWN, [W] Lemma 2.1; each line is elementary).** f = 1 + a2 z^2 + a3 z^3 + ..., with a1=0, |a2|<=1, and |ak| <= Bk := ((k+2)/k)^(k/2) (k+2)/2 <= (e/2)(k+2) for k>=1.

**Step 3 (KNOWN, M. Bonk, On Bloch's constant, Proc. AMS 110 (1990), 889-894; [W] Theorem 2.2).** Re f(z) > 0 on |z|<r0.

**Step 4 (Symmetrisation, [W] Lemma 2.4).** f_theta(z) = (f(z e^{i theta}) + conj f(conj(z) e^{i theta}))/2 is in 𝓑, has real coefficients b_k(theta) = Re(a_k e^{ik theta}), and f_theta(t) = Re f(t e^{i theta}) for real t. Hence R_r(theta) := int_0^r Re f(t e^{i theta}) dt = int_0^r f_theta(t) dt.

**Step 5 (Linear certificates, [W] Lemma 3.1 and Theorem 3.2, its proof applied with general objective weights as in [W] sec. 7).** Let g in 𝓑 have real coefficients g_k, rows r_k(rho,psi,gamma) = (1-rho^2) rho^k cos(k psi - gamma), multipliers lambda_j >= 0, and objective weights w_k >= 0 (w_k = r^(k+1)/(k+1) for the integral to r; w_k = x^k for the value g(x)). Then sum_k g_k r_k <= 1 for each row. With d_k = w_k + sum_j lambda_j r_k(rho_j,psi_j,gamma_j):
objective(g) >= d_0 - sum_j lambda_j - sum_{k=4}^K B_k |d_k| - T - T0 + d_2 g_2 + d_3 g_3,
where T = (e/2) sum_j lambda_j (1-rho_j^2) sum_{k>K} (k+2) rho_j^k, and T0 bounds (e/2) sum_{k>K} (k+2) w_k: T0 = (e/2) ((K+3)/(K+2)) r^(K+2)/(1-r) for the integral, [W] (19) for point values.
Consequence used below. Each stored cut (e,p,q) satisfies, for all theta and all f in 𝓑 with |a2|<=1, |a3|<=C:
R_r(theta) >= e + p b2(theta) + q b3(theta), b2 = Re(a2 e^{2i theta}), b3 = Re(a3 e^{3i theta}).
The stored doubles p,q differ from the exact d_2,d_3 by at most what e was lowered for ([W] sec. 7), so this holds on |b2|<=1, |b3|<=C with C=3.2888.

**Step 6 (|a3| <= C; [W] Theorem 3.5, Theorem 1.3).** |a3| <= 3.2888 for every f in 𝓑. Rebuilt in Arb from Wikstrom's stored multipliers (lam_a3, gam_a3).

**Step 7 (Necessary condition, [W] (20)).** Let 0<s<1, tau real. f_tau(s) <= |f_tau(s)| <= 1/(1-s^2), and f_tau(s) >= 1 + b2(tau) s^2 + b3(tau) s^3 - sum_{k>=4} B_k s^k. Dividing by s^2:
b2(tau) + s b3(tau) <= 1/(1-s^2) + sum_{k>=4} B_k s^(k-2) =: E(s).

**Step 8 (Lemma 2.3 of [W], read directly).** Suppose Re f>0 on D_r and c is a complex number with |c| < min_theta R_r(theta). Then F is univalent on D_r (Noshiro-Warschawski, by convexity of D_r) and beta(F) >= min_theta [R_r(theta) - Re(c e^{-i theta})].

**Step 9 (Normalisation).** G(z) = e^{-i tau} F(e^{i tau} z) and G(z) = conj F(conj z) satisfy the hypotheses of Step 1 and beta(G)=beta(F). The first sends (a2,a3) to (a2 e^{2i tau}, a3 e^{3i tau}); the second conjugates both. Choosing tau makes a2 = -A with A=|a2| in [0,1]. tau+pi keeps a2 and negates a3. So we may assume a2 = -A, a3 = rho e^{i phi}, rho=|a3|, phi in [0,pi/2] (take arg a3 into (-pi/2,pi/2] by negation, then into [0,pi/2] by conjugation, which fixes a2 = -A). Write phi = (pi/2) u, u in [0,1]. Then b2(theta) = -A cos 2theta, b3(theta) = rho cos(3 theta + phi).

## Seven pieces

Let (e1,e2,r) run over this table; r0 in the last line is exact 1/sqrt3 and its stored cuts use that value.

| piece | rho range | radius r | positivity on D_r from | T used |
|---|---|---|---|---|
| 1 | [0, 0.2] | 0.58732 | pts_eta0.2 | 0.0155 |
| 2 | [0.2, 0.3] | 0.58610 | pts_eta0.3 | 0.0155 |
| 3 | [0.3, 0.4] | 0.58498 | pts_eta0.4 | 0.0155 |
| 4 | [0.4, 0.5] | 0.58393 | pts_eta0.5 | 0.0155 |
| 5 | [0.5, 0.6] | 0.58297 | pts_eta0.6 | 0.0155 |
| 6 | [0.6, 0.7] | 0.58208 | pts_eta0.7 | 0.0155 |
| 7 | [0.7, 3.2888] | r0 | Step 3 | 0.0156 |

(Bounds are the double values stored in the files.)

**Step 10 (Positivity, computer-assisted, Prop. 7.1(i) of [W] with new multipliers).** For each eta in {0.2,...,0.7} with its r: for every real-coefficient g in 𝓑 with |g_2|<=1, |g_3|<=eta and every x in [r0, r], g(x) > 0. The certificate stores multiplier vectors at radial nodes; each vector is valid for all x. The checker subdivides [r0,r] itself (starting one double below r0) and on each subinterval [lo,hi] takes the better of the two vectors at the adjacent nodes; Step 5 with w_k = x^k, enclosed for all x in [lo,hi], with tail (19) at hi, gives g(x) >= 1 + q0 - sum lambda - sum B_k |x^k+q_k| - T - tail - |x^2+q_2| - eta |x^3+q_3| > 0.
Apply this to g=f_theta: |b2(theta)|<=|a2|<=1, |b3(theta)|<=|a3|<=eta. With Step 3, Re f>0 on D_r whenever |a3|<=eta.

**Step 11 (Cover, computer-assisted).** For each piece, the file pair c_*.leaves, c_*.wits is a list of exact dyadic boxes in (A, rho, u), whose union is [0,1] x [rho0, rho0+4] x [0,1] with rho0 = floor(e1 2^20)/2^20 <= e1, and each box Q has one of three kinds, valid on all of Q:
- kind 0: an affine centre c(A,rho,u) = c0 + J (x - x0), with |c| < 0.22 on Q, such that for all theta,
  max_j [e_j + p_j (-A cos 2 theta) + q_j rho cos(3 theta + phi)] - Re(c e^{-i theta}) > sqrt3/4 + T.
- kind 1: at a stored (tau, s) from the exclusion table: -A cos 2 tau + s rho cos(3 tau + phi) > E(s) on all of Q (upper bound of E(s) from Arb), so by Step 7 no f in 𝓑 has these coefficients.
- kind 2: rho > e2 on all of Q (for piece 7, rho > C).
Programs: check.c, check_arb.py; both bound the inequality by a Taylor form in (A,rho,phi,theta) with explicit second-order terms, adaptively in theta. cover_check.py merges the boxes up to the root in exact integers.

**Step 12 (Conclusion).** Let F be as normalised in Step 9. By Step 6, rho<=C, so rho lies in some piece: take the piece with e1 <= rho <= e2. Its radius r satisfies Re f>0 on D_r (Step 10, or Step 3 for piece 7). The point (A,rho,u) is in some box Q, which is not kind 1 (by Step 7, f exists) and not kind 2. So Q has kind 0, and with c=c(A,rho,u), Step 5 at radius r gives, for all theta,
R_r(theta) - Re(c e^{-i theta}) >= max_j[...] - Re(c e^{-i theta}) > T'' := sqrt3/4 + T >= T'.
Also R_r(theta) > T'' + Re(c e^{-i theta}) >= T'' - |c| > 0.448 - 0.22 = 0.228 > 0.22 > |c| (T'' >= sqrt3/4 + 0.0155 > 0.448). So Step 8 gives beta(F) >= T'. Take the infimum. QED.

Remarks. Pieces use no Sion duality and no moment bound, unlike [W]. The rows of piece 7 are Wikstrom's stored cuts. Those of pieces 1 to 6 and the positivity certificates are new.
