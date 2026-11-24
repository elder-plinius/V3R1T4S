# Proof of B < 2.156967 under GRH (changes to Dunn's proof only; everything else is Dunn, Bull. Aust. Math. Soc. 113(2) (2026) 293-303, arXiv:2504.15658v2; theorem numbers below are arXiv v2's)

## A. Framework (Dunn arXiv:2504.15658v2 Theorem 3.1, plus one inherited correction)
B <= 1.840518 + 2 sum_{i=1}^{k-1} [ c1(m_i, m_{i+1}) / V(z_i) + c_pi(m_i) r(z_i)^2 c2(m_i, m_{i+1}) ] + 32 pi_2 / log m_k + 8/sqrt(m_k)
     - 2 pi_2(4e18)/4e18,
with m_1 = 4e18, m_{i+1} = 10^(19 + (i-1)/5) (i = 1..9906; m_k = 10^2000), z_i < m_i^(1/4), pi_2(4e18) = 3023463123235320,
B(4e18) <= 1.840518 (Platt-Trudgian Lemmas 5-6), c1 = upper bound for int_{m_i}^{m_{i+1}} li(t)/t^2 dt, c2 = int t^(-3/2) log t dt,
r(z) = M(z) = #{odd squarefree d <= z} (exact for z < 1e7; Dunn Lemma 2.2 above). The GRH input is in Dunn Theorem 2.2:
sum_{d1,d2 <= z, d_i | P_z} |E(x; [d1,d2])| <= r(z)^2 * max_q |E(x;q)|, where E(x;q) = pi(x; q, -2) - li(x)/phi(q) and
q = [d1,d2] <= z^2 is odd squarefree. (Dunn's printed Lemma 3.2 has 16 pi_2/log m_k; his proof and code use 32; we use 32.)
Correction (inherited from Dunn Theorem 2.1): pi_2(x) <= S(A,P,z) omits twin pairs (p, p+2) with p+2 <= z, which the sieve removes;
the correct inequality is pi_2(x) <= S(A,P,z) + pi_2(z) with pi_2(z) <= z. Carried through the partial summation of Lemma 3.1
(the integrand gains <= 2 z_i/t^2 on [m_i, m_{i+1}]) it adds at most 2 sum_i z_i/m_i <= 1.03e-15 (arb, verify/check.py) to the bound,
which is included in the stated total 2.15696693552995885 < 2.156967.

## B. Change (B): modulus-dependent GRH constant
Grenie-Molteni, "An explicit Chebotarev density theorem under GRH", J. Number Theory (2019), arXiv:1709.07609v3, Cor. 1.2
(second line, pi_C = number of non-ramified primes with Artin symbol C): for x >= 2,
| (|G|/|C|) pi_C(x) - int_2^x du/log u | <= sqrt(x) [ (1/(2 pi) + 3/log x) log Delta_L + (log x/(8 pi) + 1/(4 pi) + 6/log x) n_L ].
Take K = Q, L = Q(zeta_q), G = (Z/q)^*, C = {a}, (a,q) = 1 (for q = 1, 2: L = Q, n_L = 1, Delta_L = 1). Then pi_C(x) = pi(x;q,a),
|G|/|C| = n_L = phi(q), and log Delta_L <= phi(q) log q. Dividing by phi(q) and adding li(2)/phi(q) <= li(2) to pass from
int_2^x to li(x):
|pi(x;q,a) - li(x)/phi(q)| <= sqrt(x) log x * [ 1/(8 pi) + (1/(2 pi) + 3/log x) * lambda + 1/(4 pi log x) + 6/log^2 x
                                                + li(2)/(sqrt(x) log x) ],      lambda = log q / log x.
Check: lambda = 1/2 gives 3/(8 pi) + (6 + 1/pi)/(4 log x) + 6/log^2 x + li2/(sqrt x log x), exactly JS Lemma 5.1 / Dunn's c_pi.
For x in [m_i, m_{i+1}] and q <= z_i^2: lambda <= 2 log z_i / log m_i (<= 1/2 since z_i <= m_i^(1/4)); the code uses
lambda_i = min(1/2, 2 log z_i / log m_i), and
every term is decreasing in x, so c_pi(m_i; z_i) bounds the interval. Hypothesis: GRH for zeta_{Q(zeta_q)} = product of
Dirichlet L-functions (Grenie-Molteni assume GRH for the Dedekind zeta of L).

## C. Change (V): lower bound for V(z), z > L = 1e10 (replaces Dunn Lemma 2.1 / Klyve's c3)
V(y) = sum_{n <= y, n odd squarefree} prod_{p|n} 1/(p-2). Let u(m) = 1/m for odd m (0 for even), and f multiplicative on odd d with
f(p) = 2/(p(p-2)), f(p^2) = -1/(p(p-2)), f(p^k) = 0 (k >= 3). Then h = u * f: at p: 1/p + 2/(p(p-2)) = 1/(p-2); at p^k, k >= 2:
p^-k [1 + 2/(p-2) - p/(p-2)] = 0 (with f(p^2) term only for k >= 2). Hence V(y) = sum_{d <= y} f(d) O(y/d), O(t) = sum_{m <= t odd} 1/m.
O(t) = H(t) - H(t/2)/2 = (1/2) log t + kappa + eps(t), kappa = (gamma + log 2)/2, and |eps(t)| <= 4/t for t >= 1: write
H(t) = log t + gamma + delta(t); for t in [n, n+1), delta in (-1/n, 1/(2n)) so |delta| < 1/n <= 2/t; for t >= 2,
eps = delta(t) - delta(t/2)/2, |eps| <= 2/t + 2/t; for 1 <= t < 2, O = 1 and eps in (0.018, 0.366) <= 4/t.
Sum_d f(d) = prod_p (1 + 2/(p(p-2)) - 1/(p(p-2))) = prod_{p>2} (p-1)^2/(p(p-2)) = 1/C_2. For z > L >= 1:
V(z) - V(L) - log(z/L)/(2 C_2) = sum_{d<=L} f(d)[eps(z/d) - eps(L/d)] + sum_{L<d<=z} f(d)[-(1/2)log(d/L) + kappa + eps(z/d)]
                                  - sum_{d>z} f(d) (1/2) log(z/L),
so |.| <= (8/L) sum_{d<=L} |f(d)| d + sum_{d>L} |f(d)| ((1/2) log(d/L) + kappa + 4). With Rankin (0 < s < 1/2):
sum_{d<=L} |f(d)| d <= L^(1-s) S(s), sum_{d>L} |f(d)| g(d/L) <= L^-s S(s) max_{u>=1} g(u) u^-s = L^-s S(s) (kappa + 4)
(the max is at u = 1 because kappa + 4 >= 1/(2s)), S(s) = sum_d |f(d)| d^s = prod_{p>2} (1 + (2 p^s + p^(2s))/(p(p-2))).
So A(L) <= (kappa + 12) L^-s S(s). S(s) is bounded in arb: exact product over odd p <= 1e7, tail via log(1+a) <= a,
p/(p-2) <= (P+1)/(P-1) and sum_{p>P} p^-b <= 1.25506 b P^(1-b)/((b-1) log P) (partial summation with pi(x) <= 1.25506 x/log x,
x > 1; Rosser-Schoenfeld 1962 (3.6), also Dusart 2018 (5.2)). At s = 0.44: S <= 21.271885, A(1e10) <= 0.010700091
(out/vlemma.txt). We use V(z) >= V_lo(1e10) + (log z - log 1e10)/(2 * 0.6601619) - 0.0107001 (0.6601619 > C_2).

## D. Change (L): c1 with li computed directly
c1 = [log log e - li(e)/e] - [log log s - li(s)/s] = int_s^e li(t)/t^2 dt exactly (d/dt of the bracket is li(t)/t^2), evaluated
in arb (li via arb_hypgeom_li). Since li(t) >= li(t) - li(2), this bounds the integrand in either convention. Removes Dusart's
Theorem 5.1 (7.32) and Schoenfeld's bound from the proof (both were verified anyway: Dusart, Ramanujan J. 45 (2018) Thm 5.1, whose
theta input is re-proved in Broadbent-Kadiri-Lumley-Ng-Wilk, Math. Comp. 90 (2021) Cor. 11.2).

## E. Inherited inputs and their sources (checked 2026-11-23)
- pi_2(4e18) = 3023463123235320: Bayless-Klyve-Oliveira e Silva, Integers 13 (2013) #A43 (fetched 17:31:59Z, HTTP 200; value computed
  by Oliveira e Silva) and Platt-Trudgian Lemma 5. Oliveira e Silva's own page returned HTTP 500 (one try).
- B(4e18) <= 1.840518: Platt-Trudgian, arXiv:1803.01925, Lemma 6 "B(4*10^18) in [1.840503, 1.840518]" (fetched 16:29:43Z).
- Klyve, PhD thesis (Dartmouth 2007) Theorem 5.7 (Selberg upper-bound sieve as used in Dunn Theorem 2.1): verified from the
  primary source (https://collections.dartmouth.edu/xcdas-derivative/dcdis/pdf/dcdis-klyve2007.pdf, fetched 2026-11-24T01:54:42Z,
  HTTP 200, sha256 5f3e0034...; p. 128). Unconditional (Theorem 5.4, Selberg's sieve), same A, P_z, V(z), E(x; d, -2) and li as
  Dunn. Klyve's (5.27) reads pi_2(x) - pi_2(z) <= S(A, P, z), confirming the pi_2(z) correction in A above.
- Dunn Lemma 2.2 / Proposition 2.1 (r(z) above 1e7): inherited from Dunn's refereed paper, not re-proved.

## F. Numerics (all rigorous)
V(z) for z <= 1e10: exact fixed point (code/vsieve_fx.c): each term replaced by floor(2^64/prod(p-2)) (exact u64 product), summed in
u128, so S_lo/2^64 <= V(z); for z <= 1e8 per integer z (stored as doubles rounded down), for 1e8 < z <= 1e10 at multiples of 1e4
(V(z) >= V(floor(z/1e4) 1e4)). V_lo(1e10) = 18.4017108616. M(z) exact counts for z < 1e7, Dunn Lemma 2.2 above.
Everything else in arb ball arithmetic (128 and 256 bits); z_i are chosen by a float optimiser (any z_i < m_i^(1/4) is valid,
asserted in code), and the reported value is the sup of the final ball.
