# Proof of B < 2.126988 under GRH (Dirichlet L-functions). Base: the submitted proof of B < 2.156967 (sections A-F below, unchanged except where marked) plus Change (S), exact Selberg weights. Everything else is Dunn, Bull. Aust. Math. Soc. 113(2) (2026) 293-303, arXiv:2504.15658v2; theorem numbers are arXiv v2's

## A. Framework (Dunn arXiv:2504.15658v2 Theorem 3.1, plus one inherited correction)
B <= 1.840518 + 2 sum_{i=1}^{k-1} [ c1(m_i, m_{i+1}) / V(z_i) + c_pi(m_i) r(z_i)^2 c2(m_i, m_{i+1}) ] + 32 pi_2 / log m_k + 8/sqrt(m_k)
     - 2 pi_2(4e18)/4e18,
with m_1 = 4e18, m_{i+1} = 10^(19 + (i-1)/5) (i = 1..9906; m_k = 10^2000), z_i < m_i^(1/4), pi_2(4e18) = 3023463123235320,
B(4e18) <= 1.840518 (Platt-Trudgian Lemmas 5-6), c1 = upper bound for int_{m_i}^{m_{i+1}} li(t)/t^2 dt, c2 = int t^(-3/2) log t dt,
r(z) = M(z) = #{odd squarefree d <= z} (exact for z < 1e7; Dunn Lemma 2.2 above) [Dunn's original step; in this claim r(z) is replaced by Lambda(z) of section S, so M(z) and Dunn Lemma 2.2 enter only the weights-off control]. The GRH input is in Dunn Theorem 2.2:
sum_{d1,d2 <= z, d_i | P_z} |E(x; [d1,d2])| <= r(z)^2 * max_q |E(x;q)|, where E(x;q) = pi(x; q, -2) - li(x)/phi(q) and
q = [d1,d2] <= z^2 is odd squarefree. (Dunn's printed Lemma 3.2 has 16 pi_2/log m_k; his proof and code use 32; we use 32.)
Correction (inherited from Dunn Theorem 2.1): pi_2(x) <= S(A,P,z) omits twin pairs (p, p+2) with p+2 <= z, which the sieve removes;
the correct inequality is pi_2(x) <= S(A,P,z) + pi_2(z) with pi_2(z) <= z. Carried through the partial summation of Lemma 3.1
(the integrand gains <= 2 z_i/t^2 on [m_i, m_{i+1}]) it adds at most 2 sum_i z_i/m_i to the bound; for this claim's certificate that is <= 3.5093e-15 (arb sup 3.509248783e-15, out/pi2z_correction.txt; verify/check_selberg.py adds 2 z_i/m_i to every interval term),
which is included in every total stated in this claim.

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

## S. Change (S): exact Selberg weights in the error term (NEW in this claim; replaces r(z) = M(z) in A by Lambda(z))
In A, the GRH step bounds sum_{d1,d2} |E(x;[d1,d2])| <= r(z)^2 max_q |E(x;q)|, which uses |lambda_d| <= 1. We use the weights themselves:

## S1. Weighted error term (KNOWN; Klyve thesis 2007, Theorem 5.4 proof, (5.16), (5.24)-(5.26), pp.117-125)
For any real lambda_d (lambda_1 = 1, lambda_d = 0 for d > z, d | P_z) Klyve's (5.16) gives
S(A,P,z) <= X sum lambda_d1 lambda_d2 / f([d1,d2]) + sum_{d1,d2} |lambda_d1| |lambda_d2| |R_[d1,d2]|.
With his choice (5.24) the first term is X/V(z) and, by (5.26) and the equalities on p.125 up to the change of variables,
V(z) lambda_delta = mu(delta) (f(delta)/f1(delta)) sum_{t <= z/delta, (t,delta)=1, t | P_z} 1/f1(t).
(Klyve's last line on p.125, "|lambda_delta| = 1", is an equality slip for "<= 1"; we use only the exact formula above.)
Dunn's setting (his Section 2, following Klyve Section 5.5): P = odd primes, f(p) = p - 1, f1(p) = p - 2, X = li(x).

## S2. Lambda(z) := sum_{delta<=z} |lambda_delta| = W(z)/V(z) (PROVED-HERE)
W(z) := sum_{n <= z, n odd squarefree} prod_{p|n} p/(p-2). Sum S1 over delta, put n = delta t (coprime, n <= z odd squarefree,
so n | P_z): V(z) Lambda(z) = sum_n sum_{delta|n} f(delta)/(f1(delta) f1(n/delta)) = sum_n (1/f1(n)) sum_{delta|n} f(delta)
= sum_n prod_{p|n} (1 + f(p))/f1(p) = sum_n prod p/(p-2).  Checked in exact rationals against the weights computed directly
from (5.26) for 126 values of z <= 2e4 (code/check_lambda.py, out/check_lambda.txt: PASS; a halved Lambda is flagged).
Hence Dunn's Theorem 2.2 step becomes sum |lambda_d1||lambda_d2||E(x;[d1,d2])| <= Lambda(z)^2 max_{q<=z^2} |E(x;q)|,
i.e. r(z) = M(z) is replaced by Lambda(z) <= W_up(z)/V_low(z). Nothing else in the proof changes.

## S3. Upper bounds for W (PROVED-HERE + NUMERICAL tables)
(a) z <= 1e10: exact fixed point, each term replaced by ceil(2^40 n / prod(p-2)) (code/wsieve_fx.c; dense double table
    rounded up for z <= 1e7, exact u128 cumulative sums at multiples of 1e4 up to 1e10, W(z) <= W(ceil(z/1e4) 1e4)).
    Independent float re-computation (code/indep_W.py): max rel diff 3.7e-13, no violation.
(b) z > 1e10: for 1/2 < s < 1, W(z) <= z/(2 C2) + z^s S'(s), S'(s) = prod_{p>2} (1 + (2/(p-2)) p^-s + (p/(p-2)) p^-2s).
    Proof: let u = indicator of odd m, f' multiplicative on odd d with f'(p) = 2/(p-2), f'(p^2) = -p/(p-2), f'(p^k) = 0 (k>=3).
    Then u * f' = g (g(p) = p/(p-2), g(p^k) = 0 for k >= 2, g(even) = 0): at p: 1 + 2/(p-2) = p/(p-2); at p^k, k >= 2:
    1 + 2/(p-2) - p/(p-2) = 0. So W(z) = sum_{d<=z} f'(d) O1(z/d), O1(t) = #{odd m <= t} = t/2 + e(t), |e| <= 1/2.
    sum_d f'(d)/d = prod (1 + 1/(p(p-2))) = 1/C2, so W(z) = z/(2C2) - (z/2) sum_{d>z} f'(d)/d + sum_{d<=z} f'(d) e(z/d)
    <= z/(2C2) + (z/2) z^(s-1) S'(s) + (1/2) z^s S'(s).  S'(s) bounded in arb (code/sprime.py: exact product p <= 1e7, tail via
    pi(x) <= 1.25506 x/log x; e.g. S'(0.60) <= 12.5695, S'(0.70) <= 6.5529). C2 >= 0.6601618 used.

## S4. Result (NUMERICAL, arb at 128 and 256 bits, outward rounding; z_i chosen by a float optimiser, any choice is valid)
Same intervals, head, remainder, c1 (direct li), q-dependent GRH constant and own V lemma as the submitted package, plus the
pi_2(z) correction 2 sum z_i/m_i inside the sum. Free bracket (grid + Brent per interval):
  B <= 2.1269872000642055706 (prec 128 and 256 agree to all 20 printed digits; float model agrees to 8e-14). [Post-panel note (d): this program value INCLUDES the pi_2(z) correction (code/selberg_bound.py adds 2 z/m_i to each term; removing it lowers sum_upper by exactly 3.50925e-15, out/pi2z_included_test.txt). The certificate key 'B_upper_without_pi2z' and its 'note' text are labels inherited from the earlier replay code and are wrong for this certificate: its stated terms include 2 z_i/m_i. The checker ignores both fields and sums its own recomputed terms.]
Ablations (out/*.json): Lambda := M with Dunn's bracket -> 2.1569669355299588530 (= submitted U0, control C1 PASS);
  Lambda := M with free bracket -> 2.1569674; Selberg + Dunn bracket -> 2.1271534;
  Selberg weights on Dunn's ORIGINAL inputs (JS c_pi, Dusart/Schoenfeld c1, Klyve c3) -> 2.1282623.
So the gain (~0.030) comes from the weights, not from the bracket or the earlier input changes.


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
- Dunn Lemma 2.2 / Proposition 2.1 (r(z) above 1e7): used ONLY by the weights-off control (r = M); the claimed bound does not use it.

## F. Numerics (all rigorous)
V(z) for z <= 1e10: exact fixed point (code/vsieve_fx.c): each term replaced by floor(2^64/prod(p-2)) (exact u64 product), summed in
u128, so S_lo/2^64 <= V(z); for z <= 1e8 per integer z (stored as doubles rounded down), for 1e8 < z <= 1e10 at multiples of 1e4
(V(z) >= V(floor(z/1e4) 1e4)). V_lo(1e10) = 18.4017108616. M(z) exact counts for z < 1e7, Dunn Lemma 2.2 above (control only).
Everything else in arb ball arithmetic (128 and 256 bits); z_i are chosen by a float optimiser (any z_i < m_i^(1/4) is valid,
asserted in code), and the reported value is the sup of the final ball.

Change (S) numerics: W(z) for z <= 1e10 exact fixed point (code/wsieve_fx.c, each term ceil(2^40 n / prod(p-2)), so the table is an
upper bound); z > 1e10: W(z) <= z/(2*0.6601618) + z^s S'(s) (S above; S'(s) in out/sprime.json from code/sprime.py). Lambda(z) <=
W_up(z)/V_lo(z). The per-interval z_i come from a float optimiser (free bracket: 400-point grid on [max(log 3, t_{i-1} - log 10), log m_i/4)
then Brent); any z_i in [1, m_i^(1/4)) gives a valid bound (asserted). The pi_2(z) correction 2 z_i/m_i is added inside each interval term.
Result: B <= 2.1269872000642055706 (code/selberg_bound.py, 128 and 256 bits, out/selberg_free_p*.json; includes the correction, see S4 note); the standalone checker
verify/check_selberg.py recomputes every interval term from definitions (own sieve verify/wvcount.c for V, M, W at floor(z_i)) and gets
B <= 2.1269871669853558245 < 2.126988 at both 128 and 256 bits (out/check_selberg.txt, out/check_selberg_p256.txt).
