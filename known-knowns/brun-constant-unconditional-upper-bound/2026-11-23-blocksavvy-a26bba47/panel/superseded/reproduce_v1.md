# REPRODUCE skeptic: Brun's constant under GRH, B < 2.156967 (claim/)
context: subagent (fresh knowledgeWork subagent context started by the run's main session; saw only claim/ plus the kit and the two cited papers)
role: REPRODUCE
time: 2026-11-23T17:30Z (date -u at the end of the work: Mon Nov 23 17:29:57 UTC 2026)
scratch: panel/scratch-reproduce/ (fresh copy of claim/, own venv with python-flint 0.9.0, numpy, scipy; gcc 14.2; 4 cores)

## Definition used for my own checker (written before reading claim/code)
Quoted from Dunn, arXiv:2504.15658v2, Theorem 3.1 (opened this session):
"B <= 1.840518 + 2 sum_{i=1}^{k-1} ( c1(m_i,m_{i+1})/V(z_i) + c_pi(m_i) r^2(z_i) c2(m_i,m_{i+1}) ) + 32 pi_2/log m_k + 8/sqrt(m_k) - 2 pi_2(m_1)/m_1",
with V(z) = sum_{d<=z, d|P_z} prod_{p|d} 1/(p-2), r(z) from Lemma 2.2, c_pi(x) = 3/(8 pi) + (6+1/pi)/(4 log x) + 6/log^2 x + li2/(sqrt(x) log x),
c2 = [(-2 log t - 4)/sqrt t]_{m_i}^{m_{i+1}}, c1 from li_up/li_low, Klyve's V lemma for z > 1e10, m_1 = 4e18, m_{i+1} = 10^(19+(i-1)/5), m_k = 10^2000.
Plus the claim's three changes as stated in claim/PROOF.md sections B, C, D.

## 1. Rebuild from scratch per claim/REPRODUCE.md: exact match (NUMERICAL)
- vsieve: M(1e7) = 4052875, ~0.6 s. vsieve_fx chunks (4 threads instead of 5): "S_lo(N)=3.3945165078224816e+20 count=4052847232
  Vlo=18.401710861595212 Vhi=18.401710861814917", 29 s. dense: "Vlo(N)=14.913800709097165", 3 s.
- code/replay.py, B_upper (sup of final ball), identical at 128 and 256 bits and identical to claim/out/*.json:
  R   = 2.1593210323778804655  (--prec 128 and 256)
  U'  = 2.1569562895056571339  (--cpi q, 128 and 256)
  U'' = 2.1569669355299578202  (--cpi q --c1 li --vlemma own, 128 and 256)  -> U'' < 2.156967 (margin 6.4e-8)
- code/vlemma.py: "s=0.44  S(s) <= 21.271885   A(1e10) <= 0.010700091", max t|eps(t)| for t <= 1e6 = 0.553 (<= 4). Same as claim/out/vlemma.txt.
- Determinism: results do not depend on thread count (integer fixed point) or on precision 128/256; reruns are bit-identical to claim/out.

## 2. Independent recomputation (own code: scratch mine/vmine.c, mine/mycheck.py, mine/myvlemma.py) (NUMERICAL)
- Own V(z) sieve (different method: long-double products, segmented, own threading). Versus the claim's exact fixed-point tables:
  dense z <= 1e8: 0 <= mine - theirs <= 1.10e-12 everywhere; 1e6 checkpoints k*1e4 <= 1e10: 0 <= mine - theirs <= 1.10e-10
  (consistent with their floor truncation, <= count*2^-64 = 2.2e-10); mine V(1e10) = 18.4017108617050 lies inside their [Vlo, Vhi].
  So the claim's tables are verified lower bounds to within my float error.
- M(z) exact counts: my sieve equals claim's M table byte-for-byte on 0..1e7; also checked by the Moebius formula
  M(x) = sum_{k odd} mu(k) #{odd m <= x/k^2} at x = 1, 2, 3, 1000, 123457, 2768896, 9999999, 1e7 (all equal).
- Own implementation of Thm 3.1 + changes in arb (own z optimiser, free search, rigorous margins 1e-9 / 1e-7 subtracted from my V tables,
  exact C2 enclosure in Klyve's lemma):
  Dunn replay: 2.1593043502;  change (B): 2.1569538766;  (B)+(L)+(V): 2.1569642936 (128 and 256 bits identical).
  All below the claimed R, U', U'' (my optimiser is not restricted to Dunn's bracket), and U'' < 2.156967 with margin 2.7e-6.
- Same check fed with the claim's own z_i (log10 z arrays from my rebuild): R 2.1593210265, U' 2.1569562836, U'' 2.1569669359;
  with my V margins set to 0 and C2 -> 0.6601619 in Klyve's lemma (as the claim does): R 2.1593210323651, U' 2.1569562894401,
  U'' 2.1569669354661, i.e. agreement with the claim to <= 1.3e-11 (the residual is my un-floored V and r(floor z)).
- Own S(0.44) bound (independent arb product over odd p <= 1e7 + the same Rosser-Schoenfeld tail): S <= 21.2718848067,
  A(1e10) <= 0.0107000906 <= 0.0107001 used.

## 3. Proof steps re-derived
- (B) Grenie-Molteni arXiv:1709.07609v3 Cor. 1.2 (opened): "|G|/|C| pi_C(x) - int_2^x du/log u| <= sqrt(x)[(1/(2pi) + 3/log x) log Delta_L
  + (log x/(8pi) + 1/(4pi) + 6/log x) n_L]" for x >= 2 under GRH, pi_C counting non-ramified primes. With L = Q(zeta_q), C = {a}:
  |G|/|C| = n_L = phi(q), log Delta_L <= phi(q) log q; dividing by phi(q) and factoring sqrt(x) log x gives exactly PROOF.md's bracket,
  and lambda = 1/2 reproduces Dunn's c_pi term by term (checked symbolically and in code: both formulas coincide). q = [d1,d2] <= d1 d2 <= z^2
  so lambda <= 2 log z_i / log m_i on [m_i, m_{i+1}]; every term decreases in x. Adding li(2)/phi(q) is only conservative (Dunn's li is
  truncated at 2, so GM bounds Dunn's E(x;q) directly). PROVED-HERE (re-derivation of the stated steps; GM and GRH for zeta_{Q(zeta_q)} KNOWN).
- (V) Checked h = u*f at p, p^2, p^k (all vanish as stated), V(y) = sum f(d) O(y/d), O = H(t) - H(t/2)/2, |eps(t)| <= 4/t (both ranges),
  the three-sum identity for V(z) - V(L) - log(z/L)/(2 C2) line by line, sum f = 1/C2, Rankin bounds, and max_{u>=1} g(u)u^-s at u = 1
  since kappa + 4 >= 1/(2s) = 1.136. PROVED-HERE (with Rosser-Schoenfeld pi(x) < 1.25506 x/log x KNOWN). Empirically, V(z) - log z/(2 C2)
  varies by < 3e-6 on [1e8, 1e10], far inside the 0.0107 allowance.
- (L) d/dt [log log t - li(t)/t] = li(t)/t^2 checked; arb li is the full li >= Dunn's truncated li, so c1 is an upper bound. PROVED-HERE.
- Framework (Dunn Thm 2.1/2.2/3.1, Lemma 2.2, Lemma 3.2) re-read: Lemma 2.2 constants follow from Prop. 2.1 at p = 2 (4/pi^2, 3.0377 -> 3.038,
  5.7436 -> 5.744); Lemma 3.2's proof gives 32 pi_2/log m_k (the printed 16 is a typo; claim uses 32). KNOWN (inherited).
- z_i < m_i^(1/4): asserted in code (mutation forcing z = 1.01 m^(1/4) trips the AssertionError); actual min gap log10(m_i^(1/4)/z_i) = 1.74.
  z_1 = 10^2.907 (807), z_last = 10^494.02, consistent with Dunn's Table 1 ranges.

## 4. Perturbation / mutation tests (code/replay.py copies in scratch)
- dense V table lowered by 1e-6: U'' -> 2.1569669945 (rises, as it must); A = 0.0207001: 2.1569940191; Klyve c3 doubled (U' path): 2.1569592316;
  pi_2(4e18) + 1e12: 2.1569664355; wrong lambda (log z/log m, factor 2 dropped): 2.1534717 (shows the factor 2 matters; claim's is correct).
- --vcap (no V lemma at all, V(z) >= V(1e10)): 2.4571576, so the (V) lemma (or Klyve's) is essential; the (V) proof was checked above.
- --bracket free: U' 2.1569570004, U'' 2.1569674324 (their free optimiser is slightly worse than Dunn's bracket; mine is better).
- --prec 64: 2.1569669272; --prec 53: 2.1569669653 (> 2.156967). Cause verified: the float optimiser is fed arb midpoints, so z_i change
  with precision (9783 of 9906 differ at 64 bits); my 128-bit checker on the 64-bit z_i gives 2.1569669271, matching. Not a rigour issue;
  the certified value is the 128/256-bit one. Note the rounding margin of U'' (6.4e-8) is thin vs z-choice noise; my free optimisation
  gives 2.7e-6 margin, so the headline 2.156967 is robust.

## 5. Not independently verified (inherited inputs, same as Dunn)
- pi_2(4e18) = 3023463123235320 (Oliveira e Silva table): one plain fetch of http://sweet.ua.pt/tos/primes.html returned HTTP 500 at
  2026-11-23 17:28:57Z; not retried (RULES 5). B(4e18) <= 1.840518 (Platt-Trudgian Lemma 6), Klyve Thm 5.7 (Selberg form), Klyve's c3 lemma
  (used only by U', not by the headline U''). These are cited KNOWN inputs.
- Minor inherited nit (Dunn Thm 2.1): pi_2(x) <= S(A,P,z) ignores twin pairs with p+2 <= z, which the sieve removes; the correct
  bound is S + pi_2(z). The extra contribution is <= 2 sum z_i/m_i < 1e-15, far below the 6.4e-8 margin. Not blocking.

## Verdict
Every claimed number (R, U', U'') reproduced bit-for-bit from a from-scratch rebuild at both stated precisions; tables, M counts, the
S(0.44)/A(1e10) bound and the full Theorem-3.1 sum were recomputed independently and agree (independent U'' <= 2.1569642936 < 2.156967);
the three new proof steps re-derive correctly. No mismatch, missing object or non-determinism at the stated precisions.
pass: true
