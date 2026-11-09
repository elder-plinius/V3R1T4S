# PROOF: a certified enclosure of lambda_2 of the Gauss-Kuzmin-Wirsing operator with radius < 10^-842

Every lemma is labelled PROVED-HERE (a complete argument here) or KNOWN (a cited standard theorem). Every numerical
constant is produced by `code/gkw_cert.py` in Arb ball arithmetic (python-flint 0.9.0); the function that computes it is
named next to it, and its value is copied from `result/cert_L1.json` (precision 3900 bits, J = 11200) and
`result/cert_L2.json` (4300 bits, J = 12320). Floating midpoints are used only in `gkw_cert.py eigvec` to find the
approximate eigenvector v and to propose the centre mu; v and mu are then fixed inputs (`inputs/v_N2800.txt`, N = 2800
exact dyadic coefficients, and the decimal string `inputs/mu_N2800.txt`), and nothing below depends on how they were found
(Remark 0).

The argument is the same as for the certificates of runs 2026-11-08-2057 (N = 1000, 300 decimals) and 2026-11-09-0627
(N = 2000, 601 decimals; this file's N = 2800 vector was warm-started from an N = 2400 vector of the same route, itself certified to 721 decimals in this run but not claimed here); only N, J, the working precision and the source of the centre change. The certify part of
`gkw_cert.py` is unchanged from the N = 2000 version. The eigvec part (non-rigorous) now applies the factor P of the
section by exact integer polynomial composition instead of a stored matrix, and writes the Rayleigh quotient of its
final vector as a proposed centre.

## Remark 0 (the centre: where it comes from does not matter) PROVED-HERE

mu is the number arb(s).mid() for the first token s of `inputs/mu_N2800.txt`, rounded to the working precision of the
run (3900 bits in L1, 4300 bits in L2), so L1 and L2 use two dyadic numbers that differ from the decimal s by less than
2^-3900 |s| and 2^-4300 |s| (about 1e-1174 and 1e-1294). Each run proves its statement for its own exact dyadic mu.
The decimal s is the Rayleigh quotient <v, Mv>/<v, v> of the final eigvec vector for the N = 2800 section M, computed in
midpoint arithmetic at 3900 bits; that is only how a candidate was found. Lemma 11 holds for every complex mu and
every nonzero v: mu enters the certificate only through (i) the residual eta of Lemma 7, computed with that mu, (ii) the
circle Gamma_2 centred at mu in Lemmas 8-10, and (iii) the eigenvalue counts for that circle, and all three are
computed for the given mu in ball arithmetic. A poor centre can only make eta and the radius larger, or make the
isolation fail (then certify stops); it cannot make a false enclosure pass. The negative control `result/cert_NEG_L.*`
(mu shifted by +10^-800) shows this: its radius is 1.64561e-800, not below 10^-842. Because mu does not come from the
earlier 649-decimal computation, the agreement with those 649 decimals (Theorem) is an independent consistency check.

## Setting

- c = 3/5, R = 4/5, D = {z : |z - c| < R} (so D contains [0,1]; its closure is the disc [-1/5, 7/5] on the real line).
- w = (z - c)/R. H = H^2(D) = {f = sum_{k>=0} a_k w^k holomorphic on D : ||f||^2 = sum |a_k|^2 < infinity}. The e_k = w^k
  form an orthonormal basis. P_K = orthogonal projection onto span(e_0, ..., e_{K-1}). For g bounded and holomorphic
  on D, ||g|| <= sup_D |g| (the H^2 norm is the sup over r < 1 of the L^2 mean over the circle of radius rR).
- h_n(z) = 1/(z+n), n >= 1, and (Lf)(z) = sum_{n>=1} h_n(z)^2 f(h_n(z)) (the GKW operator; on [0,1] this is the
  transfer operator of the Gauss map).
- A_K = (<L e_k, e_j>)_{j,k<K}, L_K = P_K L P_K = A_K (+) 0.

## Lemma 1 (geometry of the branches) PROVED-HERE

For n >= 1, h_n maps the closed disc cl(D) onto the closed disc with centre m_n = (n+c)/((n+c)^2 - R^2) and radius
r_n = R/((n+c)^2 - R^2). Put rho_n = (|m_n - c| + r_n)/R = max over cl(D) of |w(h_n(z))|. Then rho_1 = 13/16 and
rho_n = (c - 1/(n+c+R))/R < 3/4 for n >= 2. On cl(D), |z + n| >= n - 1/5.

Proof. z + n ranges over the closed disc with centre n + c and radius R, contained in Re > n - 1/5 > 0. Inversion maps
it to the closed disc symmetric about the real axis with diameter [1/(n+c+R), 1/(n+c-R)]; this gives m_n and r_n.
n = 1: m_1 = 5/6, r_1 = 5/12, |m_1 - c| + r_1 = 13/20, rho_1 = 13/16. n >= 2: m_n is decreasing in n and
m_2 = 65/153 < 3/5, so |m_n - c| + r_n = c - m_n + r_n = c - (n+c-R)/((n+c)^2-R^2) = c - 1/(n+c+R). The last claim:
|z + n| >= (n + c) - R. QED

## Lemma 2 (L is bounded and compact on H; known eigenvalue 1) PROVED-HERE

For f in H and |w(zeta)| <= rho < 1, Cauchy-Schwarz gives |f(zeta)| <= ||f|| (1 - rho^2)^(-1/2). By Lemma 1 the series
defining Lf converges uniformly on cl(D), with sup_D |Lf| <= ||f|| sum_n (n - 1/5)^(-2) (1 - rho_n^2)^(-1/2) < infinity,
so L is bounded on H. Lemma 4 gives ||L(I - P_K)|| -> 0, hence L is a norm limit of finite-rank operators and is
compact; its nonzero spectrum consists of isolated eigenvalues of finite algebraic multiplicity. g(z) = 1/(1+z) is in H
(its only singularity, -1, is outside cl(D)) and Lg = sum_n 1/((z+n)(z+n+1)) = 1/(z+1) (telescoping), so 1 is an
eigenvalue. QED

## Lemma 3 (exact Taylor coefficients of L applied to a polynomial) PROVED-HERE

Let v = sum_{k<N} v_k e_k and write v(u) = sum_{m<N} p_m u^m (`w_to_monomial`: Taylor shift by -3/4 and scaling by 5/4,
since w = (5/4)u - 3/4). Then for z in D, (Lv)(z) = sum_{m<N} p_m zeta(m+2, z+1), and the coefficient of w^j of Lv is

  (Lv)_j = (-1)^j R^j sum_{m<N} p_m binom(m+1+j, j) zeta(m+2+j, 1+c)
         = (-1)^j (R^j / j!) sum_{m<N} [p_m/(m+1)!] h_{m+j},   h_s = (s+1)! zeta(s+2, 8/5)

(`Lcoeffs_from_monomial`, Hurwitz zeta from Arb, `zeta_list`, `hankel_h`).

Proof. sum_n (z+n)^(-m-2) = zeta(m+2, z+1), absolutely convergent since m + 2 >= 2. zeta(s, z+1) is holomorphic in z off
(-infinity, -1]; the j-th derivative is (-1)^j s(s+1)...(s+j-1) zeta(s+j, z+1), so the Taylor series about c has
radius 1 + c = 8/5 > R and the stated coefficients; (z - c)^j = R^j w^j. QED

Check (NUMERICAL, not used in the proof): `code/crosscheck.py` evaluates Lv at four points of D by the explicit sum over
n <= 40 with v evaluated by Horner in w, plus the Hurwitz tail, and compares with sum_j (Lv)_j w^j: agreement to within the ball radii (1.09e-879 to 2.21e-1171),
`result/crosscheck_N2800.txt`.

## Lemma 4 (truncation, first part) PROVED-HERE

||L(I - P_K)|| <= eps_a(K) = (25/16)(13/16)^K (1 - (13/16)^2)^(-1/2) + (10/13)(3/4)^K (1 - (3/4)^2)^(-1/2).

Proof. Let f = sum_{k>=K} a_k w^k with ||f|| = 1. For |w(zeta)| <= rho < 1, |f(zeta)| <= (sum_{k>=K} rho^(2k))^(1/2) =
rho^K (1 - rho^2)^(-1/2), increasing in rho. For z in D, by Lemma 1, |(Lf)(z)| <= sum_n |z+n|^(-2) rho_n^K (1-rho_n^2)^(-1/2)
<= (4/5)^(-2) (13/16)^K (...) + sum_{n>=2} (n - 1/5)^(-2) (3/4)^K (1 - 9/16)^(-1/2), and since x -> (x - 1/5)^(-2) is
convex, sum_{n>=2} (n - 1/5)^(-2) <= integral_{3/2}^{infinity} (x - 1/5)^(-2) dx = 10/13. Finally ||Lf|| <= sup_D |Lf|.
QED  (`cmd_certify`, variable epsa; K = 80: eps_a = 1.6382e-7.)

## Lemma 5 (tail bounds) PROVED-HERE

(a) For sigma > 1 and a = 8/5: zeta(sigma, a) <= a^(-sigma) kappa(sigma), kappa(sigma) = 1 + (a/(1+a))^sigma (1 + (1+a)/(sigma-1)),
and kappa is decreasing in sigma (`zeta_tail_kappa`).
(b) For 0 <= m < J: T_m(J) := sum_{j>=J} binom(m+1+j, j) R^j zeta(m+j+2, a)
    <= kappa(J+2) a^(-(m+2)) binom(m+1+J, J) 2^(-J) / (1 - q),  q = (m+2+J)/(2(J+1)) < 1   (`tail_l1_factor`).

Proof. (a) zeta(sigma, a) = a^(-sigma) + sum_{n>=1} (n+a)^(-sigma) <= a^(-sigma) + (1+a)^(-sigma) + integral_1^inf (x+a)^(-sigma) dx
= a^(-sigma) + (1+a)^(-sigma) (1 + (1+a)/(sigma-1)); both factors of the correction decrease in sigma. (b) With (a),
m + j + 2 >= J + 2 and R/a = 1/2, the j-th term is at most kappa(J+2) a^(-(m+2)) t_j with t_j = binom(m+1+j, j) 2^(-j);
t_{j+1}/t_j = (m+2+j)/(2(j+1)) is decreasing in j, hence <= q for j >= J, and q < 1 iff m < J. Geometric series. QED

## Lemma 6 (truncation, second part) PROVED-HERE

||(I - P_K) L P_K|| <= eps_b = ||(A_jk)_{K<=j<J0, k<K}||_F + (sum_{k<K} tau_k^2)^(1/2), tau_k = sum_{m<=k} |P_mk| T_m(J0),
where P_mk = binom(k, m)(-c)^(k-m) R^(-k) are the monomial coefficients of e_k (`P_matrix`, exact rationals) and A_jk,
j < J0, are computed in balls by Lemma 3 (BK * PK in `cmd_certify`).

Proof. Operator norm <= Frobenius norm; split the rows j >= K into K <= j < J0 and j >= J0; for the latter, the l^2
norm of each column is at most its l^1 norm, which by Lemma 3 and the triangle inequality is at most tau_k. QED
(K = 80, J0 = 480: rows part 0.00014729, tail part 4.3376e-51.)

Hence eps = eps_a + eps_b >= ||L - L_K|| since L - P_K L P_K = L(I - P_K) + (I - P_K) L P_K. Value: eps = 0.00014747.

## Lemma 7 (residual of the true operator) PROVED-HERE

For the fixed exact v (N = 2800 coefficients) and the run's exact dyadic mu:
||(L - mu) v|| <= r_head + r_tail, with r_head = (sum_{j<J} |(Lv)_j - mu v_j|^2)^(1/2) (v_j = 0 for j >= N; Lemma 3 in
balls) and r_tail = sum_{m<N} |p_m| T_m(J) (Lemma 5(b), since |(Lv)_j| <= sum_m |p_m| binom(m+1+j,j) R^j zeta(m+2+j, a)
and the l^2 norm of the tail j >= J is at most its l^1 norm). eta = (r_head + r_tail)/||v||_lower.

Values (J = 11200, prec 3900): r_head = 1.4041e-842, r_tail = 2.3711e-1271, ||v|| >= 5.079176271, eta <= 2.7645e-843.
At prec 4300, J = 12320: r_tail = 6.7482e-1518, eta <= 2.7645e-843.

## Lemma 8 (resolvent of the section on a circle) PROVED-HERE

For z != 0 not an eigenvalue of A_K, ||(L_K - z)^(-1)|| = max(||(A_K - z)^(-1)||_2, 1/|z|) <= max(||(A_K - z)^(-1)||_F, 1/|z|).
Let Gamma be the circle with centre z_c and radius r, z_i = z_c + r e^(2 pi i i/Q). If m_i bounds the left side at z_i
and delta = 2 r sin(pi/(2Q)), then every z on Gamma is within delta of some z_i. Write T = L_K. Since
T - z = (T - z_i) - (z - z_i) I = (I - (z - z_i)(T - z_i)^(-1)) (T - z_i), and the Neumann series converges when
|z - z_i| m_i <= delta m_i < 1, we get (T - z)^(-1) = (T - z_i)^(-1) (I - (z - z_i)(T - z_i)^(-1))^(-1) (the two factors
commute, both being functions of T), hence ||(L_K - z)^(-1)|| <= m_i/(1 - delta m_i).
The inverses (A_K - z_i)^(-1) are rigorous ball enclosures (acb_mat.inv; the ball for z_i contains the exact point), so
M_K = max_i m_i/(1 - delta m_i) bounds sup_Gamma ||(L_K - z)^(-1)|| (`resolvent_circle`). QED

Values: Gamma_2 = {|z - mu| = 1/100}, Q = 64: M_K <= 160.663 (prec-4300 run, Q = 96: 156.549).
Gamma_rho = {|z| = 1/5}, Q = 256: M_K <= 55.6975.

## Lemma 9 (small gain and counting) PROVED-HERE using KNOWN facts

Let L_t = L_K + t(L - L_K), t in [0,1]. On a circle Gamma with eps M_K < 1: L_t - z = (L_K - z)(I + t (L_K - z)^(-1)(L - L_K))
is invertible for all t and z in Gamma, with ||(L_t - z)^(-1)|| <= M_K/(1 - eps M_K) =: M. The Riesz projector
Pi_t = (2 pi i)^(-1) integral_Gamma (z - L_t)^(-1) dz depends continuously on t in norm, so its rank (the number of
eigenvalues of L_t inside Gamma, with algebraic multiplicity) is constant in t (KNOWN: Kato, Perturbation Theory for Linear
Operators, I.4.6 and IV.3.4-3.5: projections close in norm have equal rank). All L_t are compact.
For the exterior of |z| = rho use the annulus rho < |z| < R_big with R_big > ||A_K||_F + eps >= sup_t ||L_t||; no L_t has
spectrum on or outside |z| = R_big, so the number of eigenvalues of L in |z| > rho equals the number of eigenvalues of A_K
in |z| > rho. Values (L1): eps M_K = 0.02370 on Gamma_2 and 0.008214 on Gamma_rho (both < 1); M = 164.562 on Gamma_2,
56.1588 on Gamma_rho. ||A_K||_F <= 1.3479954. QED

## Lemma 10 (eigenvalues of A_K) Arb-verified, independently cross-checked

`acb_mat.eig()` with python-flint 0.9.0's defaults (multiple=False, algorithm=None) calls Arb's simple-eigenvalue
routine with python-flint's default algorithm, which in 0.9.0 is the van der Hoeven-Mourrain method
("vdhoeven_mourrain", as the acb_mat.eig docstring states). It either proves that the matrix has K simple eigenvalues and
returns K pairwise disjoint isolating balls, each containing exactly one eigenvalue, or raises an error; certify also
stops unless exactly K balls come back (`n_eig_total` in the JSON). On the ball matrix A_K (K = 80) it returns 80 balls.
Exactly one ball lies inside Gamma_2 (prec-3900 run: [-0.3036630028987326585974481219015562291726 +/- 1.51e-41]); exactly two balls lie in |z| > 1/5 (1 and the same
lambda_2 approximation); no ball meets either circle. Independent check without the eig isolation guarantee
(`code/gershgorin_count.py`, `result/gershgorin_K80_p3900.txt`): with an approximate eigenvector matrix X (exact
midpoints), B = X^(-1) A_K X in balls has 80 pairwise disjoint Gershgorin discs (max disc radius [9.42e-1003 +/- 2.02e-1006] at 3900 bits), so each holds exactly one
eigenvalue (Gershgorin's theorem with disjoint discs, KNOWN); counts 1 inside Gamma_2 and 2 in |z| > 1/5:
GERSHGORIN_COUNT PASS.

## Lemma 11 (eigenvalue enclosure from a residual) PROVED-HERE

Let T be a bounded operator on a Hilbert space, Gamma = {|z - mu| = r0}, M >= sup_Gamma ||(T - z)^(-1)||, and suppose T has
exactly one eigenvalue lambda inside Gamma, of algebraic multiplicity 1, and no other spectrum in the closed disc. If v != 0
and ||(T - mu)v|| <= eta ||v|| with s eta < 1, s = M(1 + r0 M), then |lambda - mu| <= r0 M eta / (1 - s eta).

Proof. The Riesz projector Pi = (2 pi i)^(-1) integral_Gamma (z - T)^(-1) dz has ||Pi|| <= r0 M and rank 1, and T Pi = lambda Pi.
For z inside Gamma, z != lambda: (T - z)^(-1) = Pi/(lambda - z) + S(z), S(z) = (T - z)^(-1)(I - Pi). S extends holomorphically
to the open disc (the spectrum of T on the range of I - Pi lies outside the closed disc) and continuously to Gamma, where
||S(z)|| <= M ||I - Pi|| <= M(1 + r0 M) = s; the norm of a holomorphic operator-valued function is subharmonic, so ||S|| <= s
on the disc. If mu = lambda there is nothing to prove. Otherwise v = (T - mu)^(-1)(T - mu)v gives
||v|| <= (||Pi||/|lambda - mu| + s) eta ||v||, i.e. (1 - s eta)|lambda - mu| <= r0 M eta. QED

## Lemma 12 (identification of lambda_2; reality and sign) PROVED-HERE

By Lemmas 9-10 applied to Gamma_2 and to |z| = 1/5: L has exactly one eigenvalue lambda (simple) inside Gamma_2 and exactly
two eigenvalues, counted with algebraic multiplicity, in |z| > 1/5. Since |mu| - r0 = 0.2937 > 1/5, the disc of Gamma_2 lies
in |z| > 1/5, so lambda is one of the two; the other is the eigenvalue 1 of Lemma 2 (1 is not in the closed Gamma_2 disc).
All remaining eigenvalues have modulus <= 1/5 < |lambda|. So lambda is the eigenvalue of second largest modulus, lambda_2,
and it is simple. L commutes with f -> f*(z) = conj(f(conj z)) (D, c, R are symmetric under conjugation), so conj(lambda)
is an eigenvalue in the same Gamma_2 disc (mu is real); by uniqueness lambda is real, and lambda < 0 because mu + r0 < 0.

## Lemma 13 (the spectrum does not depend on the function space) PROVED-HERE

Let D' = {|z - 1| < 3/2} (Mayer's disc). (i) h_n(cl D) lies in a compact subset of D' (by Lemma 1: |m_1 - 1| + r_1 = 7/12 < 3/2,
and for n >= 2 the image is the disc with diameter [1/(n+7/5), 1/(n-1/5)], inside {Re z > 0, |z| <= 5/9}, where
|z - 1|^2 = |z|^2 - 2 Re z + 1 < 1.31). (ii) For z in cl D', Re(z + n) >= n - 1/2 > 0, so h_n(cl D') lies in the
closed right half-plane; then Re(h_n(z) + m) >= m >= 1, so h_m(h_n(cl D')) lies in the disc |z - 1/2| <= 1/2, which is a
compact subset of D (|z - 3/5| <= 3/5 there). Hence for a nonzero eigenvalue the generalized eigenspaces of L on H^2(D) and
on the bounded holomorphic functions of D' correspond: on the finite-dimensional generalized eigenspace E, L is invertible,
so every g in E equals L^2 g' with g' in E, and L^2 (resp. L) maps functions holomorphic and bounded on a compact
subset of D (resp. D') to functions holomorphic on a neighbourhood of cl D' (resp. cl D), with the series converging
uniformly. So the nonzero eigenvalues and their algebraic multiplicities coincide; lambda_2 here is the classical lambda_2.

## Theorem (PROVED-HERE, given the Arb/python-flint ball arithmetic and the cited KNOWN facts)

Let s be the decimal string in `inputs/mu_N2800.txt` (1154 significant digits, beginning
-0.3036630028987326585974481219015562331108773522536578951882454814672269952942469...). In L1, mu = arb(s).mid() at 3900 bits; Lemma 11 with T = L, r0 = 1/100, M = 164.562,
eta <= 2.7645e-843 gives |lambda_2 - mu| <= 4.5491e-843. In L2, mu = arb(s).mid() at 4300 bits, M = 160.248, eta <= 2.7645e-843,
gives |lambda_2 - mu| <= 4.4298e-843. Both dyadic centres are within 1e-1000 of s, so

  C_83 = -lambda_2 in [-s - 4.55e-843, -s + 4.55e-843],  radius < 10^-842,

i.e. D = 842 certified decimals (the minimum over L1 and L2). Outward-rounded decimal endpoints of the hull of both runs
are in `result/enclosure_C83.txt`; the endpoints agree on the first 842 decimals. The centre agrees with Nisoli's
175-digit centre (difference 4.10e-176, within 10^-175 + radius; `result/compare_L1.txt`, `result/compare_L2.txt`) and
with all 382 decimals of the OEIS A038517 b-file. It also agrees, within radius + 10^-649, with the 649 non-certified
decimals of the earlier two-method computation (`inputs/C83_649_noncertified.txt`). That check is not circular: mu
comes from the N = 2800 Rayleigh quotient (Remark 0), not from those 649 decimals.

## Constants and where they come from

| constant | value (L1: prec 3900, J 11200) | computed by |
|---|---|---|
| rho_1, rho_inf | 13/16, 3/4 | Lemma 1 (exact) |
| eps_a (K = 80) | 1.6382e-7 | cmd_certify (epsa), Lemma 4 |
| eps_b rows (K <= j < 480) | 0.00014729 | frob_upper(AJ0, K, J0, 0, K), Lemma 6 |
| eps_b tail (j >= 480) | 4.3376e-51 | tail_l1_factor, Lemma 5-6 |
| eps | 0.00014747 | sum |
| M_K on Gamma_2 / Gamma_rho | 160.663 / 55.6975 | resolvent_circle (Q = 64 / 256, 320-bit inverses) |
| eps M_K | 0.02370 / 0.008214 | Lemma 9 |
| M on Gamma_2 / Gamma_rho | 164.562 / 56.1588 | Lemma 9 |
| ||A_K||_F | 1.3479954 | frob_upper(AK) |
| r_head, r_tail | 1.4041e-842, 2.3711e-1271 | Lcoeffs_from_monomial, tail_l1_factor (J = 11200) |
| ||v|| lower | 5.079176271 | cmd_certify |
| eta | 2.7645e-843 | Lemma 7 |
| radius | 4.5491e-843 | Lemma 11 |
