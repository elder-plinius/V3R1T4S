context: subagent (fresh context, knowledgeWork)
role: REPRODUCE

Scope: claim/ only (CRITERION.txt, CLAIM.md, REPRODUCE.md, 1507.06183.pdf, certs/). I wrote my own checker, solver and errata scripts from the paper before opening claim/code/. When I did open claim/code/check_cert.py, its model matched mine. No injection_suspected: grep found no steering text in the code or docs.

Definitions used (quoted from 1507.06183): Table 1, gamma=0. adopt: "(1,0,irrelevant) α / (0,1,irrelevant) 1−α, reward (0,h)". override, feasible "only when a > h": "(a−h,0,irrelevant) α / (a−h−1,1,relevant) 1−α, reward (h+1,0)". wait and match as in Table 1. w_ρ(x,y) = (1−ρ)x − ρy. Sec 4.2: the truncating states max{a,h}=T allow adopt only. Compensation: eq (7) when T=a≥h; the next display / eq (28) when T=h>a. The dual check is r + ΣP·h − h(s) ≤ g for every (state, action) pair.

Errata (my own exact series, Monte Carlo and proof, alpha=.45):
- E1 (Lemma 13 / eq 22 → eq 7) is REAL. From the origin the walk returns with probability α + (1−α)q = 2α, not α/(1−α). The series gives E[last] = 49.500000 at (0,0), 55.000000 at (1,0) and 77.000000 at (5,0). The corrected 2K+... formula gives the same values. The printed values are 24.75, 30.25 and 52.25. alpha=.3 agrees too: series 2.625 vs printed 1.3125.
- E2 (eq 28) is REAL. The series gives P(ret) = q^d exactly, and E[U|ret] = 4.5, 9.0, 31.5 for d = 1, 2, 7, which equals αd/(1−2α). So E[a0|ret] = h + αd/(1−2α). The printed value d/(1−2α) = 10, 20, 70 is the duration, not a0. The recursion for G(d) holds exactly in Fractions for d ≤ 60. Monte Carlo at (249,250) gives E[a0|ret] = 254.47 (corrected 254.5, printed 10).

Exact certificate checks (my code, Fractions/integers, both compensation variants built separately from the formulas):
- Headline: certs/upper_a45_T2000_rho67005787.txt.gz, rho = 67005787/10^8, T = 2000.
  - Label-collapsed check over 10003001 pairs: g = -29177/5497558138880 (~ -5.307265e-09) at (1648,1661) wait. Corrected: CERT_OK. Printed: CERT_OK.
  - Full literal labeled enumeration over 32010003 (state, action) pairs: the same g for both variants, CERT_OK.
  - Truncating-state max residual: -6.169611e-09 (corrected) and -6.170049e-09 (printed).
  - This is an exhaustive check, not a sample.
- T=250 cert at rho 0.67078: g = -82708181/21990232555520 (~ -3.761133e-06) over 501253 labeled pairs, OK for both variants.
- T=1000 cert at rho 0.67006: g ~ -1.232017e-06, OK for both variants.
- Lower: certs/lower_a45_T1500_rho67005786, policy checked in under-paying M^1500 over all 2253001 states. Every boundary action is adopt and every override is feasible. g_lo = 837/1374389534720 > 0, so REV(policy) > 0.67005786.
- Negative controls (all behave as required):
  - NEG_dual T2000 rho .67005785: CERT_FAIL, g = +15001/2199023255552 (~ +6.82e-09), both variants.
  - NEG_pol T2000 rho .67005785 (corrected): g_lo = 36019/5497558138880 > 0.
  - NEG_pol T250 rho .67045 (corrected): g_lo ~ +1.931330e-04.
  - NEG_dual T95 rho .66: CERT_FAIL, +1.363664e-02.
  - NEG_tampered T250: CERT_FAIL, +9.728014e-04 at (10,10).
- Determinism: a box reset deleted my working copy partway through. The parent restored claim/ and I rebuilt my scripts. Every exact output on the restored files was identical to my outputs from before the reset. The PDF sha256 matches scout_record.md. I had not hashed the certs before the reset, so the identical exact outputs are my evidence that the restored files are the same.

Calibration (my own float builder: label-collapsed, which is exact at gamma=0; renewal/SSP value iteration):
- Under-paying root at T=95, alpha .425: [0.56808786, 0.56808796]. SSZ: 0.56808.
- Under-paying root at T=95, alpha .45: [0.66891317, 0.66891325]. SSZ: 0.66891.
- Optimal gain of N at alpha .45, T=95, rho .66 (Dinkelbach / policy iteration on the renewal form): corrected +0.0133693, printed +0.0100061. Both positive, as required.

Prop. 3 scrutiny (corrected rewards):
- Part I bounds re-derived. Pathwise, the attacker's accepted blocks within an epoch are at most its cumulative blocks at the last visit of the gap walk to 0. Overrides only happen at gap ≥ 1, and honest rewards are ≤ 0.
- In the h=T>a case, the no-return branch pays ≤ -ρh, and the return branch is bounded by (1-ρ)(2K + E[a0|ret]) by the strong Markov property.
- So corrected (7)/(28) over-pay. The printed N is not shown to over-pay: E1 makes eq (7) too small. Soundness therefore rests on the corrected variant, which passes.
- Part II only needs, for any admissible π with v^π ≥ 0: N-numerator ≥ M-numerator ≥ 0 and a shorter epoch. It does not need an optimal policy to exist.
- So g < 0 implies every REV(π) < rho. Strictness of the sup also follows: the residuals are continuous in rho over finitely many constraints, so the certificate still holds at a slightly smaller rho.
- Relied on but not re-proved: SSZ Lemma 8 (renewal ratio) and the admissibility conditions.

Conclusion: both errata are real. The headline T=2000 certificate holds exactly over every pair for both compensations. The lower certificate and the calibration reproduce, and all negative controls fail as they should. Result: 0.67005786 < max REV < 0.67005787 at alpha=0.45, gamma=0.
pass: true
