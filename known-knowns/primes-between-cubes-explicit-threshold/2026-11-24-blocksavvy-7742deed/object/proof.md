# Primes between consecutive cubes for n >= exp(exp(29.735))

**Theorem.** For every integer n >= exp(exp(29.735)) there is a prime p with n^3 + 1/2 < p <= n^3 + 3n^2 + 1/2;
in particular (n^3, (n+1)^3) contains a prime.

Credit: the idea of inserting Bellotti's near-unity density into Cully-Hugill's argument was first stated, as a non-rigorous
one-parameter model giving about 30.07 ("model, not a theorem"; Bellotti Thm 1.3 and Ford's c), by u/span_of_dilates, rStation
paper 130 §2.3 (v2, 08 Nov 2026), https://rstation.ai/problems/riemann_hypothesis/papers/130. This proof makes it rigorous.
Previous values: 32.892 (Cully-Hugill, J. Number Theory 247 (2023)); 32.76 (Mossinghoff, Trudgian & Yang, Res. Number Theory 10
(2024), https://doi.org/10.1007/s40993-023-00498-y); 32.537 (Cully-Hugill PhD thesis, Thm 4.3; see CLAIM.md for a caution about
the zero-free constant it appears to use).

Inputs I1-I7 below are used exactly as stated. I3 (Yang) is a UNSW PhD thesis (2025) and I4 (Bellotti) is an arXiv
preprint (v1, 2023, not refereed as far as we found); the variants in section 5 show what each one buys.

## 1. Inputs (exact statements, with the source text in data/)

- **I1 (Cully-Hugill, J. Number Theory 247 (2023) 100-117 = arXiv:2107.14468v3, Theorem 2 and Table 2).** Write
  psi(x) = x - sum_{|gamma|<T} x^rho/rho + E(x,T), the sum over non-trivial zeros rho = beta + i gamma of zeta (eq. (6)).
  "Theorem 2. For 50 < T < x and half odd integers x >= x_K we have psi(x) = x - sum_{|gamma|<T} x^rho/rho
  + O*(K x log x log log x / T)", with (Table 2) K = 2.4798 for log x_K = 10^6. (O* means a constant of absolute
  value at most 1.)
- **I2 (Hasanalizade-Shen-Wong, J. Number Theory 235 (2022), Cor. 1.2, as quoted in I1 eq. (3) and in I4 Thm 2.2).**
  For T >= e, |N(T) - (T/2pi) log(T/(2 pi e)) - 7/8| <= 0.1038 log T + 0.2573 log log T + 9.3675, where N(T) counts
  zeros with 0 < gamma <= T. We use only the consequence N(T) <= T log T for T >= 100.
- **I3 (A. Yang, "Explicit zero-free regions for the Riemann zeta-function", PhD thesis, UNSW Canberra, 2025,
  doi:10.26190/unsworks/31825, Theorem 1.3).** "One has zeta(sigma + it) != 0 if t >= 3 and
  sigma > 1 - 1/(51.34 (log t)^{2/3} (log log t)^{1/3})."
- **I4 (C. Bellotti, "Explicit zero density estimate near unity", arXiv:2311.05136v1, Theorem 1.1).** "For every
  sigma in [0.98, 1] and T >= 3, the following zero-density estimate holds uniformly:
  N(sigma,T) <= (C1 T^{57.8875(1-sigma)^{3/2}} (log T)^{19703/1800} + C2 T^{33.08(1-sigma)^{3/2}} (log T)^{503/45}
  + 0.27 (log T)^{14/10}) log log T, where C2 = 7.65*10^10 and C1 = ... 9.77*10^21 if T > e^{481958}."
  Here N(sigma,T) = #{rho : 0 < gamma < T, sigma < beta < 1} (her Section 1).
- **I5 (Kadiri-Lumley-Ng zero density, J. Math. Anal. Appl. 465 (2018), as stated and used in I1, eq. (4) and
  Section 4, constants recomputed there).** For T >= H_0 and k in [10^9/H, 1] (H < H_0):
  N(sigma,T) <= C1(sigma) (log kT)^{2 sigma} (log T)^{5-4 sigma} T^{8(1-sigma)/3} + C2(sigma) log^2 T, with C1(sigma)
  increasing, C2(sigma) decreasing, and "we can take C1 = 17.418 ... and C2 = 5.272" (C1 = C1(1), C2 = C2(0.6)), i.e.
  for sigma in [0.6, 1). Here N(sigma,T) counts 0 < gamma <= T, sigma < beta < 1. (Used only for sigma <= 1 - 10^-6,
  where it contributes less than exp(-10^6); see Remark 2.)
- **I6 (elementary; Erdos).** prod_{p <= m} p < 4^m for every integer m >= 1, hence theta(t) < t log 4 for t >= 1.
- **I7 (Riemann zeros, classical).** Zeros are symmetric under rho -> conj(rho); no zero has 0 <= gamma < 14.
  The function nu(t) := 1/(51.34 (log t)^{2/3} (log log t)^{1/3}) is decreasing on t >= 3 (log 3 > 1, so both factors
  of the denominator are positive and increasing).

## 2. Notation
alpha = 1/3 + 10^-9, delta = 10^-9, sigma1 = 3/5, u2 = 10^-6. For an integer n >= 2 put x = n^3 + 1/2,
h = 3n^2, y = x + h = n^3 + 3n^2 + 1/2 (x and y are half odd integers), X = log x, T = x^alpha, L = log T = alpha X,
nu = nu(T), a8 = 1 - 8 alpha/3 (> 0). Since y < (n+1)^3, theta(y) - theta(x) > 0 gives the Theorem.
Facts used: y <= 2x, log y <= X + 1, log log y <= log(X+1), h = 3(x - 1/2)^{2/3} >= 2.99 x^{2/3}.

## 3. Lemmas

**Lemma 1 (prime powers).** theta(y) - theta(x) >= psi(y) - psi(x) - log 4 (y^{1/2} + y^{1/3} log y / log 2).
*Proof.* psi - theta = sum_{k>=2} theta(t^{1/k}) is >= 0, so theta(y)-theta(x) >= psi(y)-psi(x) - (psi-theta)(y), and
(psi-theta)(y) <= theta(y^{1/2}) + sum_{3<=k<=log y/log 2} theta(y^{1/3}) (terms with y^{1/k} < 2 vanish); apply I6. QED

**Lemma 2 (explicit formula).** If X >= 10^6 then psi(y) - psi(x) >= h (1 - S) - K (x X log X + y log y log log y)/T,
where S = sum_{|gamma|<T} x^{beta-1} and K = 2.4798.
*Proof.* I1 at x and at y (both half odd, 50 < T < x < y, x >= x_K) gives
psi(y) - psi(x) = h - sum_{|gamma|<T} (y^rho - x^rho)/rho + E(y,T) - E(x,T). For each zero,
|(y^rho - x^rho)/rho| = |int_x^y u^{rho-1} du| <= int_x^y u^{beta-1} du <= h x^{beta-1} (beta < 1). QED

**Lemma 3 (zero-free).** Every zero with 0 < gamma < T has beta <= 1 - nu(T).
*Proof.* By I7, gamma >= 14 > 3, and by I3, beta <= 1 - nu(gamma) <= 1 - nu(T) because nu is decreasing. QED

**Lemma 4 (sum over zeros).** Let M(sigma) = #{0 < gamma < T : beta > sigma}, N*(T) = #{0 < gamma < T}. Then
S = 2 [ N*(T) x^{-1} + int_0^1 X x^{sigma-1} M(sigma) d sigma ] and, if T >= 3*10^12, nu < u2, X >= 10^6,
S <= 2 (A0 + A1 + A2) with
  A0 = alpha X exp(-(2/5 - alpha) X),
  A1 = (2/5) X [17.418 L^{3.8} exp(-u2 a8 X) + 5.272 L^2 exp(-u2 X)],
  A2 = log L * sum_{i=1..3} C_i L^{e_i} exp(-X g_i) / m_i,
where (C_i, B_i, e_i) = (9.77e21, 57.8875, 19703/1800), (7.65e10, 33.08, 503/45), (0.27, 0, 14/10),
g_i = nu - B_i alpha nu^{3/2}, m_i = 1 - (3/2) B_i alpha u2^{1/2}, provided L > 481958 and every m_i > 0.
*Proof.* By I7, S = 2 sum_{0<gamma<T} x^{beta-1}, and x^{beta-1} = x^{-1} + int_0^beta X x^{sigma-1} d sigma; summing
(a finite sum) gives the identity. Split [0,1] at sigma1, 1 - u2, 1 - nu.
(a) On [0, sigma1]: M <= N*(T) <= T log T (I2, T >= 100), and N*/x + int_0^{sigma1} X x^{sigma-1} N* = N* x^{sigma1-1}
    <= T log T x^{-2/5} = A0.
(b) On [sigma1, 1-u2]: M(sigma) <= N_KLN(sigma,T) (it counts a superset). By I5 with k <= 1 (so 0 < log kT <= L) and
    sigma >= 0.6: N <= 17.418 L^{5-2 sigma} T^{8(1-sigma)/3} + 5.272 L^2 <= 17.418 L^{3.8} T^{8u/3} + 5.272 L^2,
    u = 1 - sigma >= u2. Since x^{-u} T^{8u/3} = exp(-u a8 X) <= exp(-u2 a8 X) and x^{-u} <= exp(-u2 X), and the interval
    has length <= 2/5, the integral is <= A1.
(c) On [1-u2, 1-nu]: 1 - u2 >= 0.98, so I4 applies (T > e^{481958}): with u = 1 - sigma and T^{B u^{3/2}} = exp(B alpha
    u^{3/2} X), the integral is <= log L sum_i C_i L^{e_i} int_nu^{u2} X exp(-X (u - B_i alpha u^{3/2})) du. The function
    g(u) = u - B_i alpha u^{3/2} has g'(u) = 1 - (3/2) B_i alpha sqrt(u) >= m_i > 0 on [0, u2], so
    g(u) >= g(nu) + m_i (u - nu) and the inner integral is <= exp(-X g(nu)) / m_i. This gives A2.
(d) On [1-nu, 1]: M = 0 by Lemma 3. QED

**Lemma 5 (assembly).** For n as above with X >= 10^6, T >= 3*10^12, L > 481958, nu < u2, all m_i > 0:
theta(y) - theta(x) >= h (1 - Phi(X)), where Phi = 2 (A0 + A1 + A2) + R_E + R_T,
  R_E = (3K/2.99) (X+1) log(X+1) exp(-delta X),
  R_T = (log 4 / 2.99) (sqrt 2 exp(-X/6) + 2^{1/3} (X+1) exp(-X/3) / log 2).
*Proof.* Lemmas 1, 2, 4. For the error term: K(x X log X + y log y log log y)/T <= 3K x (X+1) log(X+1)/T and
x/(T h) <= x^{-delta}/2.99. For Lemma 1's term divide by h >= 2.99 x^{2/3} and use y <= 2x, log y <= X + 1. QED

**Lemma 6 (monotonicity).** Let X0 > 0 satisfy
 (M1) (2/5 - alpha) X0 >= 1; (M2) u2 a8 X0 >= 4.8 and u2 X0 >= 3; (M4) delta X0 >= 2;
 (M3) for i = 1, 2, 3: B_i alpha sqrt(nu0) < 1, m_i > 0 and Q_i(X0) := (1 - B_i alpha sqrt(nu0)) X0 nu0 (1 - 1/log L0)/3
      >= e_i + 1/log L0, where L0 = alpha X0, nu0 = nu(e^{L0});
 (V) X0 >= 10^6, L0 > 481958, log L0 > 1, nu0 < u2.
Then each of A0, A1, A2, R_E, R_T is non-increasing in X on [X0, infinity), and (V) holds for every X >= X0.
*Proof.* As functions of X (with L = alpha X, nu = nu(e^L)):
- d/dX log A0 = 1/X - (2/5 - alpha) <= 0 by (M1). The two terms of A1 have log-derivatives 4.8/X - u2 a8 and 3/X - u2,
  <= 0 by (M2). d/dX log[(X+1) log(X+1) e^{-delta X}] <= 2/X - delta <= 0 by (M4). R_T is decreasing for X > 2.
- A2: write P = X nu. From nu = L^{-2/3} (log L)^{-1/3}/51.34, d log P/dX = (1/(3X))(1 - 1/log L) > 0, so
  dP/dX = nu (1 - 1/log L)/3. Since d nu/dX < 0, d(X nu^{3/2})/dX = nu^{1/2} dP/dX + (P/2) nu^{-1/2} d nu/dX
  <= nu^{1/2} dP/dX, hence d(X g_i)/dX >= (1 - B_i alpha sqrt(nu)) dP/dX = Q_i(X)/X. Therefore
  d/dX log(C_i L^{e_i} log L e^{-X g_i}/m_i) = e_i/X + 1/(X log L) - d(X g_i)/dX <= (e_i + 1/log L - Q_i(X))/X.
  Each factor of Q_i is positive and non-decreasing in X (nu decreases, P increases, log L increases), so
  Q_i(X) >= Q_i(X0) >= e_i + 1/log L0 >= e_i + 1/log L, and the derivative is <= 0.
- (V) is monotone in the right direction (X, L increase; nu decreases). QED

## 4. Proof of the Theorem
Let Y = 29.735 and X0 = 3 e^Y. The certificate (code/cert_arb.py, arb ball arithmetic with outward rounding, at 128
and 256 bits; and independently code/standalone_check.py, mpmath interval arithmetic at 300 bits) proves
(M1)-(M4), (V) and Phi(X0) < 0.93426 < 1 (out/). For an integer n >= exp(exp(Y)), X = log(n^3 + 1/2) > 3 log n >= X0,
so by Lemma 6, Phi(X) <= Phi(X0) < 1, and T = x^alpha >= 3*10^12; Lemma 5 gives theta(y) - theta(x) > 0. QED

Remark 1 (sharpness of the certificate). Phi(3 e^{29.734}) > 1.04, so 29.735 is the best value on the 10^-3 grid for
this exact chain of inequalities.
Remark 2 (robustness). A0, A1, R_E, R_T are below exp(-10^4) at X0, so I1, I2, I5, I6 could be replaced by much weaker
statements (any error term O(x log^2 x / T) with constant < e^{1000}; any density bound N(sigma,T) <= C T^{A(1-sigma)}
(log T)^D on [3/5, 1 - 10^-6] with A <= 3 - 10^-3, C <= e^{1000}, D <= 100) without changing the result. The threshold is driven only by I3 and I4:
X0 nu0 = 380.33 against the log of the I4 constants.

## 5. Variants (same proof, same code; out/scan_out.txt)
| zero-free region | density near 1 | certified Y (n >= exp(exp(Y))) |
|---|---|---|
| I3 Yang thesis c = 51.34 | I4 Bellotti Thm 1.1 | **29.735** (this theorem) |
| Bellotti c = 54.004 (arXiv:2306.10680v1 Thm 1.2, in data/; journal JMAA 536 (2024)) | I4 Bellotti Thm 1.1 | 29.907 |
| (c = 53.989, the journal value as quoted in Yang's thesis Table 4.1; journal text not in data/) | I4 Bellotti Thm 1.1 | 29.906 |
| Ford 2002 c = 57.54 (journal) | I4 Bellotti Thm 1.1 | 30.123 |
| I3 c = 51.34 | Bellotti Thm 1.3 (T >= exp(6.7e12); proof only sketched in source) | 29.671 |
| I3 c = 51.34 | none (I5 up to 1 - nu, as in Cully-Hugill) | 32.505 |
| Bellotti c = 54.004 (arXiv v1 / JMAA 2024) | none (I5) | 32.677 (no thesis or preprint input) |
| Ford c = 57.54 | none (I5) | 32.892 (= Cully-Hugill JNT 2023, reproduced) |
For the I5-only rows, A1 is replaced by C1 L^3 X e^{-nu(a8 X - 2 log L)}/(a8 X - 2 log L) + C2 L^2 e^{-nu X}
(integrating L^{3+2u} e^{-u a8 X} over u >= nu) and A2 = 0; monotonicity needs a8 X0 nu0 (1 - 1/log L0)/3 >= 4.
