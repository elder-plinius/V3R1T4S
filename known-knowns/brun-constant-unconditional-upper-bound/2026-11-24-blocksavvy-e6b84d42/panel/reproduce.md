role: reproduce
context: fresh subagent (new context; saw only repo/kit/RULES.md, PANEL_BRIEFS.md header + REPRODUCE section, and a copy of claim/ in sandbox/panel-0527-reproduce/claim; did not open attempts/, notes/ or any other panel file)
claim: Assuming GRH for Dirichlet L-functions (and RH), Brun's constant satisfies B < 2.126988 (claim/CLAIM.md, partial win p1)
date_utc: 2026-11-24T06:10:09Z

## Definitions used (quoted from the package, before reading any author code)
- Klyve thesis (data/klyve2007.txt) Thm 5.4 proof: (5.16) "sum lambda_d1 lambda_d2 A_[d1,d2] = X sum lambda_d1 lambda_d2 / f([d1,d2]) + sum |lambda_d1||lambda_d2||R_[d1,d2]|"
  (the "=" is really "<="); (5.24) "u_delta = mu(delta)/(f1(delta) V(z))"; (5.25) "lambda_delta = f(delta) sum_{d|P_z, delta|d} mu(d/delta) u_d";
  (5.26) "V(z) lambda_delta = f(delta) sum_{d|P_z, delta|d} mu(d/delta) V(z) u_d". Dunn setting (data/dunn_arxiv2504.15658v2.txt Sec. 2.1):
  P = odd primes, P_z = prod_{p<=z, p odd}, A_d = pi(x; d, -2), f = phi, f1(p) = p - 2, V(z) = sum_{d<=z, d|P_z} prod_{p|d} 1/(p-2).
- Dunn Theorem 3.1 / Lemma 3.2 (tail 32 pi_2/log m_k + 8/sqrt(m_k), pi_2 = twin prime constant) and PROOF.md A-D, S.

## S2 re-derived (PROVED-HERE, agrees with PROOF.md S2)
For squarefree d = delta t, mu(d/delta) mu(d) = mu(delta), so (5.26) gives V lambda_delta = mu(delta) f(delta)/f1(delta) sum_{t<=z/delta,(t,delta)=1, t|P_z} 1/f1(t).
Summing |.| over delta and setting n = delta t (n <= z odd squarefree, so n | P_z since P_z contains every odd prime <= z):
V(z) sum|lambda_delta| = sum_n (1/f1(n)) sum_{delta|n} f(delta) = sum_n prod_{p|n} (1 + f(p))/f1(p) = sum_n prod_{p|n} p/(p-2) = W(z).
Then sum_{d1,d2}|lambda_d1||lambda_d2||E(x;[d1,d2])| <= (W/V)^2 max_{q<=z^2} |E(x;q)|. Correct.
Own exact-rational check (sandbox mine/klyve_identity.py, independent of code/check_lambda.py): lambda from (5.24)-(5.25) directly, for every
z = 1..199 and z in {257, 500, 1000, 1500, 2000, 3000}: lambda_1 = 1, |lambda| <= 1, sum|lambda| = W/V exactly, closed form of S1 exact,
and the quadratic form sum lambda_d1 lambda_d2/f([d1,d2]) = 1/V(z) exactly at z in {10, 50, 99, 150, 199, 257}: PASS.
(Lambda(100) = 17.137504, Lambda(1000) = 121.866404, as in out/check_lambda.txt.)

## S3(b) re-derived (PROVED-HERE, agrees)
u = 1_{odd}, f'(p) = 2/(p-2), f'(p^2) = -p/(p-2), f'(p^k)=0 (k>=3), on odd d: (u*f')(p) = p/(p-2), (u*f')(p^k) = 1 + 2/(p-2) - p/(p-2) = 0 (k>=2),
0 on even n. W(z) = sum_{d<=z} f'(d) O1(z/d), O1(t) = floor((t+1)/2) = t/2 + e, e in (-1/2, 1/2]. sum f'(d)/d = prod(1+1/(p(p-2))) = 1/C2.
Rankin: for d > z, 1/d <= z^(s-1) d^(-s); for d <= z, 1 <= (z/d)^s. Hence W(z) <= z/(2 C2) + (z/2) z^(s-1) S'(s) + (1/2) z^s S'(s), 1/2 < s < 1. Correct.
Also re-derived PROOF.md C (V lemma: h = u*f, O(t) = (1/2)log t + kappa + eps, |eps| <= 4/t, Rankin max at u = 1, A(L) <= (kappa+12) L^-s S(s)),
the pi_2(z) correction in A (pi_2(x) <= S(A,P,z) + pi_2(z), adds <= 2 z_i/m_i per interval), c1 = [log log t - li(t)/t] (derivative li(t)/t^2),
c2 = [-2 t^(-1/2)(log t + 2)], and PROOF.md B against the primary source: Grenie-Molteni arXiv:1709.07609v3 Cor. 1.2 (fetched 2026-11-24T06:08:06Z,
HTTP 200, sha256 5b04d675a9ea5874b6813a6074b5f786ece6ad7880e8337abf17e704c4372dbd): the quoted inequality matches verbatim; with K = Q,
L = Q(zeta_q), n_L = phi(q), log Delta_L <= phi(q) log q the stated c_pi(m_i; z_i) follows, decreasing in x, lambda_i <= 2 log z_i/log m_i <= 1/2.
Not re-derived here (inherited, cited): Platt-Trudgian Lemmas 3, 5, 6 (B(4e18) <= 1.840518, pi_2(4e18), tail), Dunn's partial summation, pi(x) <= 1.25506 x/log x.

## Independent numerics (written before opening any author code)
- Own sieve (mine/vw.c, segmented, 7 threads, long double block sums + __float128 combine, rigorous relative padding 1e-12 applied):
  V, W, M at floor(z_i) for the 140 intervals with z_i <= 1e10 and at 1e10. V(1e10) = 18.401710861705..., W(1e10) = 7573900191.97797...,
  M(1e10) = 4052847232, W(1e7) = 7573985.94267 (all consistent with PROOF.md F/REPRODUCE.md). Rerun with 3 threads: byte-identical.
- Own arb constants (mine/consts.py, 128 bits, primes to 1e8 / 1e7): C2 in [0.66016181528, 0.66016181619] (so 0.6601618 <= C2 <= 0.6601619);
  S'(s) for s in {0.52..0.75} identical to out/sprime.json to 15 digits; own A(1e10) <= 0.01070009059 <= 0.0107001.
- Own evaluation of all 9906 interval terms (mine/check_B.py, arb, 256 and 128 bits, identical output on reruns): z_i read from
  verify/cert_selberg_p128.json (sha256 e6b84d427b0fc63661a4011cd7bc2b4f1f35e60f75f3ac3411e8829b7d4ac92c, 9906 entries: 181 exact doubles,
  9725 as exp(t)); every z_i satisfies 3 < z_i < m_i^(1/4) and every exp(t) z_i > 1e10. T_i = 2(c1/V_lo + c_pi Lambda_up^2 c2) + 2 z_i/m_i.
  Sum T_i = 0.2833936237944095 (incl. pi_2(z) correction 3.5092e-15); head 1.840518 + 32*0.6601619/log 10^2000 + 8/10^1000 - 2*3023463123235320/4e18
  = 1.8435935431637066. Result: B <= 2.126987166958116126708 < 2.126988. TRUE (NUMERICAL, rigorous ball arithmetic).
- Comparison with the certificate: without my 1e-12 padding every own term is <= the stated term; with it, the worst excess is 1.1e-12 relative
  (interval 12), i.e. exactly my safety padding, not a discrepancy. Sum of stated terms 0.28339365690049897 >= own 0.28339362379.
- Author's standalone checker (run after my checker): sh verify/run_checks.sh twice, identical output, PASS, B <= 2.1269871669853558245
  (agrees with mine to 2.7e-11; mine is lower because I used A = 0.01070009059 instead of 0.0107001).

## Defects found (non-blocking for the claim B < 2.126988; should be fixed before packaging)
1. PROOF.md S4 and F say the program value B <= 2.1269872000642055706 (code/selberg_bound.py, out/selberg_free_p*.json) includes the
   pi_2(z) correction "inside each interval term". It does not: the certificate key is "B_upper_without_pi2z", its note says the terms are
   "2*(c1/V + c_pi c2 r^2)", and the stated terms sum exactly to sum_upper 0.28339365690049896914 with no 2 z_i/m_i term. Missing amount: 3.5092e-15.
   The statement stays true only because the checker/own value (which do include it) is 3.3e-8 lower.
2. PROOF.md A says the correction is <= 1.03e-15; that is for the earlier submission's z_i. For this certificate it is 3.5092e-15.
Neither changes the value in CLAIM.md (2.1269871669853558245, from the checker, which includes the correction) or the rounded claim 2.126988.

## Verdict
Every proof step I was asked to re-derive (S1, S2, S3(b), plus C, D, B's use of Grenie-Molteni and the pi_2(z) correction) checks out. My own sieve,
own constants and own arb evaluation of all 9906 interval terms give B <= 2.1269871669581 < 2.126988 under GRH. No missing object, no
non-determinism (sieve and evaluation reruns identical; author checker reruns identical). The only mismatches are the two labels above (3.5e-15 level).
Scratch files: sandbox/panel-0527-reproduce/mine/ (vw.c, vw_out.txt, consts.py, consts_128.json, check_B.py, check_B_128.txt, check_B_256.txt, klyve_identity.py).
pass: true
