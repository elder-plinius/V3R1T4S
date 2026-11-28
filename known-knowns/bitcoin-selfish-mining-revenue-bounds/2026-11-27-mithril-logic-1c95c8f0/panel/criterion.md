context: subagent (fresh context, knowledgeWork)
role: CRITERION

## What I checked (every number below is from my own command output)
- I read CRITERION.txt, CLAIM.md, REPRODUCE.md, run_checks.sh, scout_record.md, code/check_cert.py, code/check_policy.py, and code/build/ssp.py. I checked them against 1507.06183.pdf (Table 1, Sec. 4.2 eq. (7) and the display after it, Lemma 13 eqs. (22)-(26), and the Prop. 3 proof eqs. (27)-(28)).
- The claimant's checker matches Table 1 at gamma = 0. Adopt gives (0,h). Override is allowed only when a > h and gives (h+1,0). Wait/match follow the table, and the gamma branch has probability 0. Truncating states max(a,h)=T allow adopt only, with the compensation reward.
- **Independent checker.** I wrote my own exact checker, claim/_crit/mychk.py. It rebuilds N_rho^T from the paper with the full 3-label state space, explicit per-action transition lists, and Fractions. It takes only the H integers from certs/. It has three compensation variants:
  - printed7: (T,T) uses eq. (7);
  - printed28: (T,T) uses the display after (7), which settles the a = h = T ambiguity in the printed text;
  - corrected: E1 and E2 fixed.
- **Main certificate, certs/upper_a45_T2000_rho67005787.txt.gz** (alpha 9/20, rho 67005787/10^8, T 2000). In my checker, all three variants give 32010003 pairs and max residual g = -29177/5497558138880 (about -5.3073e-9) at (1648,1661,0,wait): OK. The claimant's check_cert.py gives the same g, CERT_OK, for both printed and corrected.
- **T=250 certificate, certs/upper_a45_T250_rho67078.txt.gz.** My checker (all three variants) and check_cert.py both give g = -82708181/21990232555520 (about -3.761e-6), 501253 pairs: OK.
- The T=1000 certificate gives g about -1.232e-6, CERT_OK (check_cert.py).
- **Negative controls (all behave as required):**
  - NEG_dual T2000 at rho 0.67005785: CERT_FAIL, +6.82e-9.
  - NEG_pol T2000 (corrected): g_lo about +6.55e-9, POLICY_GAIN_POSITIVE.
  - NEG_pol T250 at rho 0.67045: +1.931e-4, POLICY_GAIN_POSITIVE.
  - NEG_dual T95 at rho 0.66: CERT_FAIL, +1.364e-2.
  - NEG_tampered T250: CERT_FAIL at (10,10). My checker also fails it, +9.728e-4.
  - Null model: the honest policy at rho 0.66 has gain -0.21 (= alpha - rho) in my solver, as expected.
- **Lower certificate (check_policy.py, under, T1500, rho 0.67005786):** g_lo = 837/1374389534720 > 0, POLICY_GAIN_POSITIVE. This is supporting evidence only; I checked it with the claimant's code, not with an independent checker.
- **Calibration with my own builder** (claim/_crit/mypi.py: label-collapsed policy iteration with renewal-form evaluation, T=95):
  - Under-paying root at alpha .425 is in [0.56808786, 0.56808796]; SSZ gives 0.56808, so the gap is 7.9e-6, under 1e-5. OK.
  - Under-paying root at alpha .45 is in [0.66891317, 0.66891325]; SSZ gives 0.66891, so the gap is 3.2e-6. OK.
  - The optimal gain of N at alpha .45, rho .66 is +1.000611546e-02 (printed) and +1.336925514e-02 (corrected). Both are positive. OK.
  - Extra: the printed-N root at T=95 is in [0.67576632, 0.67576640]. This fits SSZ's 0.70109 being the loose rho'+2(u+eps') output of Algorithm 1, not the N root.
- **Bar:** U = 0.67005787 <= 0.70099, about 0.0309 below the bar.

## Ruling on the key tension (errata vs. "exactly as printed")
- **Literal reading.** The criterion asks for N_rho^T built "exactly as SSZ Section 4.2 defines it". The main certificate is valid for N exactly as printed, under both readings of the (T,T) state. So the format requirement is met literally.
- **Errata are real.**
  - E1: from the origin, the walk returns with probability alpha (step to +1, then a.s. return) plus (1-alpha)q = alpha, so 2*alpha in total. E[#returns] is therefore 2alpha/(1-2alpha), not alpha/(1-2alpha). The exact series gives E[psi(0,0)] = 99 at alpha .45, so E[last] = 49.5 against the printed 24.75; Monte Carlo gives 49.352.
  - E2: a0 >= h because h cannot decrease before adopt. The printed E[a0|return] = (h-a)/(1-2alpha) is the expected excursion duration. I re-derived the Doob-transform value h + alpha*d/(1-2alpha). Monte Carlo at (249,250) gives 254.553 against the corrected 254.500 and the printed 10. The exact recursion identity also holds for d <= 60.
  - So SSZ's proof of Prop. 3 does not establish that the printed N over-pays. Concluding "via SSZ Prop. 3 as printed" would be formally compliant but rests on a flawed proof.
- **Substance needs the corrected Prop. 3, and I re-checked it.** I re-derived Part I as a pathwise bound:
  - D' (cumulative attacker minus honest blocks from the fork) follows the free walk.
  - The state's gap is D' minus the number of overrides, so an override needs D' >= 1. Every override therefore happens at or before psi.
  - Credited attacker blocks are thus at most the attacker blocks mined by psi, which is last(a,h). Honest penalties are <= 0.
  - With h=T > a, no credit is possible before the return to the diagonal. With no return, the reward is <= -rho*h.
  - Taking expectations (strong Markov at the return) gives exactly the corrected (7) and (28).
  - Part II (the ratio argument) does not depend on the compensation formula and is inherited unchanged from SSZ.
- The certificate passes for the corrected N, so the contrapositive gives:
  - u'^T <= g < 0, hence v*_rho < 0, hence REV < rho for every admissible policy.
  - This holds up to SSZ's own framework (the class A, optimal-policy existence in Part II, and Prop. 2 / Appendix C); no new gap is introduced.
- **Conclusion:** the full criterion is met literally (printed N) and in substance (corrected N, which also over-pays the printed N pointwise). The corrected Prop. 3 did need re-proving. I did that for Part I as above, and Part II carries over verbatim.

## Partial wins
- The full criterion is met at alpha = 0.45, so p2 is not needed.
- p1 is not literally established: there is an exact inequality certificate REV(pi) > 0.67005786, not an exact rational REV value from the Markov chain, and the claim says so.
- p3 is not addressed.
- alpha = 0.475 is not claimed.

## Caveats
- **Novelty is not my role.** Novelty of the errata, and the overlap with PR #814 and arXiv 2607.24415, are for NOVELTY. The criterion's incumbent clause is satisfied anyway, since 0.67005787 is far below about 0.70099.
- **Injection: none suspected.** I read CLAIM.md, REPRODUCE.md, scout_record.md, run_checks.sh and the code in full and found no steering text.
- **Process notes.**
  - Before I started using claim/_crit/, a PDF text dump and a run_checks log were briefly written to the parent of claim/; I moved the PDF dump into claim/_crit/.
  - My private copy, including claim/_crit/, was removed from the machine before I finished, after all the runs above had completed. My scripts and logs no longer exist on disk; the numbers above are from their output in my session.

confirmed_scope: For SSZ's gamma = 0 model at alpha = 9/20, the rational certificate certs/upper_a45_T2000_rho67005787.txt.gz is an exactly verified average-reward dual certificate with gain -29177/5497558138880 < 0 for N_rho^T at T = 2000, rho = 67005787/10^8, both as printed (eq. (7) and the following display) and with the corrected Lemma 13 / eq. (28) compensation, which by the corrected Prop. 3 argument gives max REV < 0.67005787 <= 0.70099 within SSZ's policy class.
pass: true
