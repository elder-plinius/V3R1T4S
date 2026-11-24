role: REPRODUCE
context: fresh subagent (new context, no prior conversation; saw only kit/RULES.md, PANEL_BRIEFS.md common header + REPRODUCE section, and a copy of claim/ in sandbox/panel-0729-reproduce/claim; did not open attempts/, notes/, runs/2026-11-24-0527/ or any other panel file)
claim: under GRH (Dirichlet L-functions / Dedekind zeta of Q(zeta_q)) and RH, Brun's constant B < 2.1257395 (partial win p1); runs/2026-11-24-0729/claim/
date_utc: Tue Nov 24 08:44:03 UTC 2026

## Method
My own checker was written and run before I opened any author code (code/, verify/*.py, verify/*.c). Before that I read only CLAIM.md, REPRODUCE.md,
PROOF_DELTA.md, PROOF.md, data/klyve2007.txt, data/dunn_arxiv2504.15658v2.txt and the certificate data verify/cert_rho_p128.json (z_i and stated terms).
Scratch code (sandbox, relative to claim/: ../mine/): lam.py (weights), rho.c (per-modulus accumulator), exact.py (Fractions), vw.c (V/W sieve),
consts.py (C2, S(sigma)), evalB.py (all 9906 terms), my_tamper.py. Cores: <= 3 (taskset 0-2 / 3 processes), nice 10.

## (1) R1-R2 re-derived from Klyve (PROVED-HERE, elementary; checked against data/klyve2007.txt)
Definition quoted (Klyve Thm 5.4, (5.13)): "Define R_d by the equation A_d = X/f(d) + R_d for each d|P_z."
Klyve's proof (p.117, display before (5.16)): S(A,P) <= sum_{a in A} (sum_{d|P_z, a in A_d} lambda_d)^2 = sum_{d1,d2<=z, d_i|P_z} lambda_d1 lambda_d2 A_[d1,d2]
(an identity after (5.15); lambda_1 = 1, lambda_d = 0 for d > z). Since [d1,d2] | P_z, (5.13) applies to it, giving the EQUALITY
sum lambda_d1 lambda_d2 A_[d1,d2] = X sum lambda_d1 lambda_d2/f([d1,d2]) + sum lambda_d1 lambda_d2 R_[d1,d2]; the printed (5.16) with |.| on the
second sum and "=" is indeed an "=" for "<=" slip. Grouping the finite second sum by q = [d1,d2] is a rearrangement: sum_q rho_q R_q, rho_q =
sum_{[d1,d2]=q} lambda_d1 lambda_d2, and |sum_q rho_q R_q| <= (sum_q |rho_q|) max_q |R_q| <= Lambda^2 max_q |R_q|.
Uniformity: every such q is odd squarefree, q <= d1 d2 <= z^2, (q, -2) = 1. The GRH bound used (Grenie-Molteni Cor 1.2 as quoted in PROOF.md B,
L = Q(zeta_q), log Delta_L <= phi(q) log q) is |E(x;q)| <= sqrt(x) log x K(x, lambda) with lambda = log q/log x <= 2 log z_i/log m_i for every
x in [m_i, m_{i+1}] and every q <= z_i^2; I re-did the algebra (lambda = 1/2 gives Dunn's c_pi exactly) and K is decreasing in x. It is one
number for all q, so it may multiply ANY upper bound for sum_q |rho_q|. The main term X/V(z) and the pi_2(z) correction are untouched; the
weights are fixed per interval so Dunn's partial summation (Lemma 3.1, re-read in data/dunn...txt) goes through with r(z)^2 -> Sigma(z).
lambda_d depends on z only via floor(z): confirmed (d <= z and primes p <= z). R1-R2: CORRECT.
Not re-opened by me: the Grenie-Molteni paper itself, Platt-Trudgian B(4e18) <= 1.840518, pi_2(4e18) (all inherited KNOWN inputs of the base
e6b84d42 proof, cited by exact statement in PROOF.md; not in data/).

## (2) R3 rounding bound re-derived (PROVED-HERE)
Write 2^K lambda_d = L_d + e_d, |e_d| <= 1. Then 2^(2K) lambda_a lambda_b = L_a L_b + L_a e_b + e_a L_b + e_a e_b, so
2^(2K)|rho_q| <= |P_q| + sum_{[a,b]=q} (|L_a| + |L_b| + 1). Each ordered pair lies in exactly one q, hence
2^(2K) Sigma <= S + 2 N sum|L| + N^2 (N = #odd squarefree d <= n; these all divide P_n). With K = 40 this is the claim's formula. CORRECT.
I also verified, for all 22 rho_levels rows of verify/cert_rho_p128.json, that the stated reduced fraction equals (S + 2N sum|L| + N^2)/2^80
exactly (Python Fractions): 22/22 equal.

## (3) Own Sigma(n) and own evaluation of all 9906 terms (NUMERICAL, interval arithmetic + exact integers)
Levels: floor(z_i) of the 22 'rho' entries, derived from the z hex myself: 20 distinct n = 3363 3957 4415 4899 5403 6015 6699 7457 8267 9187
10209 11315 12605 14009 15595 17356 19263 19993 19997 19999 (matches the cert's rho_levels order).
Weights: Klyve (5.26) and p.125, V(n) lambda_d = mu(d) prod_{p|d}(p-1)/(p-2) sum_{t<=n/d,(t,d)=1,t|P_n} 1/f1(t), f1(p) = p-2, in arb at 256 bits
(lam.py); lambda_1 = 1 certified (ball within 2^-236 of 1) at every level; scale K = 48 (author: 40), L_d = floor(mid(2^48 lambda_d)),
|2^48 lambda_d - L_d| <= 1 certified from the ball for every d. Accumulator: my own bucketed dense exact __int128 sum (rho.c, author: sort-based),
identity sum_q P_q = (sum L)^2 OK at every level. Bound Sigma(n) <= (S + 2N sum|L| + N^2)/2^96.
Cross-check of my pipeline vs exact-rational Sigma(n) by brute force (exact.py, Fractions) at n = 51, 99, 151, 299: bound >= exact, excess
3.0e-14..3.5e-14 relative. Result vs the cert: for all 22 rho entries the cert's Sigma_up >= my Sigma_up, relative difference 1.07e-11..1.28e-11
(= the author's coarser 2^40 rounding slack). Sigma/Lambda^2 ~ 0.645 (e.g. n = 19999: Sigma_up 2066747.87359, Lambda = 1790.11248...).
V, W for the 140 intervals with z_i <= 1e10 and V(1e10): my own segmented sieve over all odd n <= 1e10 (vw.c), V-terms floor(2^90/prod(p-2)),
W-terms ceil(2^60 n/prod(p-2)), exact u128; checked vs Fractions at 8 points <= 2001 and V(19999) vs lam.py (8.462698114825246, agree).
V(1e10) >= 18.401710861705048 (claim: V_lo(1e10) = 18.4017108616).
Lemmas re-derived (PROVED-HERE): V lemma (section C: h = u*f, O(t), |eps| <= 4/t, Rankin, max at u = 1, A <= (kappa+12) L^-s S(s)) and W lemma
(S3b: u*f' = g, Rankin, W <= z/(2C2) + z^s S'(s), S'(s) = S(1-s)). Own constants (consts.py, arb 256, exact product over odd p <= 1e7, tail via
pi(x) <= 1.25506 x/log x): C2 in [0.660161809434, 0.660161819716]; S(0.44) <= 21.2718848066822 (= claim), S(0.40) <= 12.5695122276934 (= claim
S'(0.60)), all 9 claim S' values reproduced to all printed digits.
Own evaluation (evalB.py; c1 = [loglog t - li(t)/t] with arb li, c2 = [-2(log t+2)/sqrt t], c_pi(m_i; lambda_i = 2 log z_i/log m_i), admissibility
z_i < m_i^(1/4) asserted for all 9906, term 2(c1/V + c_pi c2 E) + 2 z_i/m_i, head 1.840518 - 2 pi_2(4e18)/4e18, tail 32 C2/log m_k + 8/sqrt m_k):
 - with the claim's constants (A = 0.0107001, C2 0.6601619/0.6601618, the claim's 9-point s grid): B <= 2.125739397303683734773 (prec 256)
   (author's checker: 2.1257393973040676877; difference 3.8e-13 = my tighter Sigma).
 - with my own constants (best sigma = 0.45, A <= 0.01047564668; C2 from my product; 35-point s grid): B <= 2.125738734833951112012 (prec 256 and
   512 identical).
 - every one of the 9906 stated cert terms is >= my recomputed upper bound (max (mine - stated)/stated = -1.7e-14; rho terms <= -2.1e-13).
Both totals < 2.1257395. Margin of the claim's rounding: ~1.03e-7 (checker value) / 6.9e-8 (author program value 2.1257394310040893870).

## (4) Author's checks and corruptions
sh verify/run_checks.sh (python-flint 0.9.0 venv, taskset 3 cores, nice 10): 128 bits PASS and 256 bits PASS, "B <= 2.1257393973040676877",
check 3 "A(1e10) <= 0.01070009059 <= 0.0107001", last line PASS.
python3 verify/tamper_tests.py: all 5 corruptions rejected, "tamper tests: PASS".
My own corruptions (my_tamper.py, check_rho.py at 128): rho interval 17 z -> 20001.5 with flag kept: FAIL ("rho flag on interval 17 with z > 20000");
interval 5000 t -> log(m_i)/4 + 1e-3: FAIL ("z_5000 not admissible"); last interval deleted: FAIL ("expected 9906 intervals");
z of rho intervals 0 and 21 swapped: FAIL ("interval 0: recomputed 0.01503... exceeds stated 0.00644..."). 4/4 rejected.
Determinism: author program code/rho_bound.py --prec 128 rerun from my copy (tables from sandbox/brun-work read-only, rhofx rebuilt):
B_upper 2.1257394310040893870, work/cert.json byte-identical to verify/cert_rho_p128.json (sha256 ece6008a7d8615fe294374f58927b8b45aedbf478c39e5a88f346a90d4f8261c).
My own evaluator gave identical output at 256 and 512 bits.

## Notes (no effect on the verdict)
- check_rho.py's wvcount uses up to 8 threads by default (I constrained it with taskset); worth a note in REPRODUCE.md for shared boxes.
- The "K1 control" value 2.12698720 uses re-optimised z_i; with the claim's own z_i and Lambda^2 instead of Sigma my evaluator gives 2.12726669 (expected, not a mismatch).
- My constants are stored as 30-digit decimal strings of arb upper/lower bounds; the slack of every such bound (>= 1e-9) dwarfs the 1e-30 print rounding.

## Verdict
No mismatch, missing object or non-determinism found. R1-R2 and the R3 rounding bound are correct; my independently computed Sigma(n) at all 20
levels lies below the certificate's values; my own arb evaluation of all 9906 interval terms gives B <= 2.12573940 with the claim's constants and
B <= 2.12573874 with my own; both < 2.1257395. Scope of this pass: reproduction of the stated bound from the stated (cited) inputs, conditional on GRH.
pass: true
