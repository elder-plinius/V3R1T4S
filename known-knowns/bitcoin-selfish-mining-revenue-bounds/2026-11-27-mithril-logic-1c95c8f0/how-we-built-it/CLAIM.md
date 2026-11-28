# Claim (single-context, unpanelled; label PROMISING at most until a fresh three-skeptic panel)

Target id: bitcoin-selfish-mining-revenue-bounds (bank criterion: repo/bank/targets.json; a verbatim copy is in
the run's target.md, outside claim/). Status source: https://arxiv.org/abs/1507.06183 (paper PDF: 1507.06183.pdf here).
Scope: alpha = 9/20 = 0.45, gamma = 0 only. (alpha = 0.475 is NOT claimed.)

## Claim sentence
For SSZ's gamma = 0 Bitcoin selfish-mining model (arXiv 1507.06183, Sec. 2-4) at alpha = 9/20, an exact-rational
average-reward dual certificate (bias h, gain g = -29177/5497558138880 ~ -5.31e-9 < 0) exists for the over-paying
MDP N_rho^T at T = 2000, rho = 67005787/10^8 = 0.67005787, and it is valid BOTH for N_rho^T with the truncation
compensation exactly as printed (eq. (7) and the display after it = eq. (28)) AND for the corrected compensation
derived below. Using SSZ Proposition 3 with the corrected compensation (the only version we show to be an
over-payer), the optimal untruncated relative revenue satisfies max REV < 0.67005787 (bank bar: <= 0.70099).

Erratum findings stated inside this claim (both checked numerically, code/verify_compensation.py):
  E1. Lemma 13 / eq. (22) (hence eq. (26), (27) and eq. (7)): the expected number of returns of the gap walk to
      the origin is 2 alpha/(1-2alpha), not alpha/(1-2alpha). Corrected: E[last(a,h)] = 2K + ((a-h)/(1-2alpha)+a+h)/2,
      K = alpha(1-alpha)/(1-2alpha)^2. The printed value is K too small.
  E2. Proof of Prop. 3 / eq. (28): E[a0 | return occurs] = h + alpha(h-a)/(1-2alpha), not (h-a)/(1-2alpha)
      (the printed value is the expected excursion DURATION, not the position a0 >= h).
  Both errors make the printed N_rho^T UNDER-compensate, so Prop. 3 is not proven for N as printed.

Supporting results (same checker):
  - Lower side: an explicit stationary policy (adopt at its boundary T = 1500) has exactly certified gain
    g_lo = 837/1374389534720 > 0 in the under-paying M_rho^T at rho = 67005786/10^8 (rewards identical to the
    untruncated model for this policy), so REV(policy) > 0.67005786 and max REV > 0.67005786.
    Hence 0.67005786 < max REV < 0.67005787 (enclosure width 1e-8; SSZ Table 2 gives [0.66891, 0.70109]).
  - Extra upper certificates: T = 1000, rho = 0.67006 (g ~ -1.232e-6); T = 250, rho = 0.67078 (g ~ -3.761e-6,
    275 KB file, the smallest).
  - The 2026-11-26 claim point (T = 250, rho = 0.67045) does NOT survive the full correction: an exactly
    certified policy has gain +1.93e-4 > 0 in the corrected N at T = 250, rho = 0.67045 (negative control 3).
    The corrected T = 250 float root is 0.6707737; correcting only E2 (as the 2026-11-26 REPRODUCE skeptic did)
    leaves it at ~0.670445, so E1 is what moves it.

## Model (SSZ Table 1, gamma = 0) as implemented by code/check_cert.py
State (a, h, f), 0 <= a, h <= T, f in {irrelevant, relevant, active}; reward pair (x,y) -> (1-rho)x - rho y.
adopt: -> (1,0,irr) alpha / (0,1,irr) 1-alpha, reward (0,h). override (a > h): -> (a-h,0,irr) alpha /
(a-h-1,1,rel) 1-alpha, reward (h+1,0). wait (f irr/rel): -> (a+1,h,irr) alpha / (a,h+1,rel) 1-alpha.
wait from active, and match (f = relevant, a >= h): -> (a+1,h,active) alpha / (a-h,1,rel) gamma(1-alpha) = 0 /
(a,h+1,rel) (1-gamma)(1-alpha); expected reward 0 at gamma = 0. Truncating states max(a,h) = T: adopt only, with the
adopt reward replaced by the compensation (eq. (7) if T = a >= h, eq. (28) if T = h > a; (T,T) uses eq. (7)).
The certificate's bias is label-invariant, h(a,h,f) = H[a][h]/2^40; the checker still enumerates every
(state, action) pair with all labels (501253 pairs at T = 250, 32010003 at T = 2000).
Dual certificate: if r(s,a) + sum P h - h(s) <= g for all pairs, every policy of N has long-run gain <= g.

## Derivation of the corrected compensation
Notation: alpha < 1/2, q = alpha/(1-alpha), K = alpha(1-alpha)/(1-2alpha)^2, the attacker only waits in the
oracle argument, so each block moves the gap D = a - h by +1 (prob alpha) or -1 (prob 1-alpha).

E1 (case T = a >= h, Lemma 13). SSZ: psi = last time the walk is in Low-Triangle {D >= 0}; it is on the
diagonal there and last(a,h) = a + (psi - d)/2 with d = a - h (paper, correct). E[psi] = E[psi_1] + E[#returns] *
E[excursion length | return], E[psi_1] = d/(1-2alpha) (paper, correct). From the origin an excursion returns iff it
steps to +1 (prob alpha; it then returns a.s. because the drift is toward -infinity) or steps to -1 and returns
(prob (1-alpha) q = alpha). So P(return) = 2 alpha and #returns is geometric with mean 2alpha/(1-2alpha). The paper
uses success probability 1 - alpha/(1-alpha) (it omits the +1 side) and gets alpha/(1-2alpha). Given a return, the
length is 1 + 1/(1-2alpha) on either side (paper, correct). So
  E[psi] = d/(1-2alpha) + 4 alpha(1-alpha)/(1-2alpha)^2,   E[last(a,h)] = 2K + (d/(1-2alpha) + a + h)/2.
Check (alpha = .45): a deterministic series for E[psi] gives 99.000000 at (0,0), 149.000000 at (5,0); the corrected
E[last] 49.5/77.0 matches, the printed 24.75/52.25 does not (Monte Carlo agrees: 49.352 at (0,0)).
Corrected (7):  (1-rho) * ( 2K + ((a-h)/(1-2alpha) + a + h)/2 ),  T = a >= h.

E2 (case T = h > a, proof of Prop. 3). Let d = h - a > 0. The gap returns to 0 with prob q^d (paper, correct).
At the return the state is (a0, a0) with a0 = h + U, U = honest blocks during the excursion (h never decreases
before an adopt, so a0 >= h). Conditioned on return the walk is the Doob transform with steps -1 w.p. 1-alpha, +1
w.p. alpha; its duration N has E[N | return] = d/(1-2alpha) (this is the value printed for E[a0|return]), and
U = (N - d)/2, so E[U | return] = alpha d/(1-2alpha). Exact check: G(d) = q^d alpha d/(1-2alpha) satisfies
G(d) = alpha G(d-1) + (1-alpha)(G(d+1) + q^(d+1)), G(0) = 0, G -> 0 (verified in Fractions for d <= 60), which is
the recursion for E[U ; return]. Monte Carlo at (249,250): E[a0|ret] 254.553 vs corrected 254.500 (printed: 10).
The paper then bounds the post-return reward by (1-rho) E[last(a0,a0)] = (1-rho)(K + a0) "by (22)"; with E1 this
is (1-rho)(2K + a0), linear in a0. Non-return branch: adopt at once, reward -rho h (paper, correct).
Corrected (28): (1 - q^d)(-rho h) + q^d (1-rho) ( 2K + h + alpha (h-a)/(1-2alpha) ),  T = h > a.
Consistency: at a = h = T both corrected formulas give (1-rho)(2K + T) (the printed ones disagree: K+T vs K).

What the claim relies on (stated, not re-proved here): the rest of SSZ's Prop. 3 argument, i.e. Part I's oracle
bound (the expected reward from a truncating state up to tau_1 is at most the conditional expectations above) and
Part II's ratio argument (with v* >= 0, replacing the continuation by the compensation and adopting cannot lower
the average value). With corrected (7)/(28) the over-paying N'_rho^T satisfies u'^T >= v* whenever v* >= 0.
Contrapositive: a dual certificate with g < 0 gives u'^T <= g < 0, so v*_rho < 0, so every policy has REV < rho.
The certificate also passes with the printed compensation; that check only shows the literal bank format is met,
it is NOT evidence of soundness because the printed N is not shown to over-pay.

## Negative controls (all in run_checks.sh; every one behaves as required)
1. certs/NEG_dual_a45_T2000_rho67005785 (built the same way at rho = 0.67005785, below the float root
   0.6700578610 at T = 2000): CERT_FAIL, max residual +6.82e-9, both variants.
2. certs/NEG_pol_a45_T2000_rho67005785: exact policy lower certificate in the corrected N^2000 at rho = 0.67005785:
   g_lo = 36019/5497558138880 > 0, so no g < 0 certificate exists there at T = 2000.
3. certs/NEG_pol_a45_T250_rho67045: corrected N^250 at the old claim's rho = 0.67045: g_lo ~ +1.931e-4 > 0.
4. certs/NEG_dual_a45_T95_rho66 (bank sanity point rho = 0.66): CERT_FAIL, +1.364e-2.
5. certs/NEG_tampered_a45_T250_rho67078 (one H entry lowered by 2^-10): CERT_FAIL at (10,10).
6. The lower certificate itself: since max REV > 0.67005786, no rho <= 0.67005786 can be certified at any T.

## Calibration (own builder; under-paying roots: attempts/certifier-v2/out_calib_roots.txt; over-paying gains at rho .66: out_sanity_v2.txt)
Under-paying root T = 95: alpha .425 in [0.5680878, 0.5680885] (SSZ 0.56808); alpha .45 in [0.6689129, 0.6689135]
(SSZ 0.66891). Over-paying optimal gain at alpha .45, T = 95, rho = .66: printed +1.000611546e-02, corrected
+1.336925514e-02 (positive, as the bank requires).
Float roots of the optimal gain (alpha .45; both errata fixed; attempts/certifier-v2/out_roots_v2_small.txt, out_roots_v2_large.txt, out_roots_under.txt, out_roots_precise.txt): corrected/max N: T=95 0.6808712, T=250 0.6707737, T=500 0.6700818,
T=1000 0.6700579226, T=1500 0.6700578612, T=2000 0.6700578610-0.6700578611; under-paying M: T=400 0.6700504,
T=1000 0.6700578558, T=1500 0.6700578610-0.6700578611.

## Not claimed
- alpha = 0.475 (a separate attempt, outside this claim).
- That SSZ's Prop. 3 holds for N as printed; that SSZ's Table 2 numbers are wrong (their upper bound 0.70109 used
  the printed N; we did not re-run their Algorithm 1).
- The bank's p1 (exact rational REV of a policy from its Markov chain): our lower result is an exact inequality
  certificate (REV > 0.67005786), not an exact REV value.
- Novelty of the two errata beyond the 2026-11-26 panel's search (NOVELTY must re-check; arXiv 2607.24415 and open
  PR #814 at ~0.70099 are the known nearby items).
