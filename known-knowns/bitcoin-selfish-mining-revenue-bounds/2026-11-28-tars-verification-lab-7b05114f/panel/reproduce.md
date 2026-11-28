# REPRODUCE review: max REV < 169/250 at alpha=9/20, gamma=0 (N_{169/250}^{95} exact dual)

context: fresh knowledgeWork subagent, no prior context

Reviewer role: REPRODUCE (independent, skeptical). Inputs read: only claim/ (CLAIM.md, FORMULA.md, REPRODUCE.md, scout.md, data/, object/, code/). I wrote my own builder and checker in reproduce_work/ next to this file (relative to claim/: ../panel/reproduce_work/) (model.py, exact_check.py, solve.py; logs exact_check.log, solve.log) from the paper BEFORE I opened or ran claim/code/. I ran the author's code afterwards on a scratch copy outside the run folder, so claim/ was not modified (all claim/ mtimes predate this review).

## Definition I checked against (quoted from data/arxiv-1507.06183.pdf; sha256 0cc1fdc0...2b34 matches CLAIM.md)
- Table 1 (p.8, data/ssz-page-08-table1.png): adopt -> (1,0,irr) w.p. alpha / (0,1,irr) w.p. 1-alpha, reward (0,h); override (a>h) -> (a-h,0,irr) alpha / (a-h-1,1,rel) 1-alpha, reward (h+1,0); wait in irr/rel -> (a+1,h,irr) alpha / (a,h+1,rel) 1-alpha; wait in active and match in relevant (a>=h) -> (a+1,h,active) alpha / (a-h,1,rel) gamma(1-alpha) reward (h,0) / (a,h+1,rel) (1-gamma)(1-alpha).
- Section 4.2 (p.10-11): in states with max{a,h}=T only adopt; N_rho^T pays at T=a>=h "(1-rho)·α(1-α)/(1-2α)^2 + 1/2·((a-h)/(1-2α)+a+h)" (7), and at T=h>=a "(1-(α/(1-α))^(h-a))·(-ρh) + (α/(1-α))^(h-a)·(1-ρ)·(α(1-α)/(1-2α)^2 + (h-a)/(1-2α))".
- Appendix, proof of Prop. 3, eq. (27): "(1-ρ)·E[last(a,h)] = (1-ρ)·( α(1-α)/(1-2α)^2 + 1/2·(a-h)/(1-2α) + a + h )... This is precisely the reward given in state (a,h) in Low-Triangle with a=T, in the over-paying MDP N_ρ^T." Lemma 13 eqs (22)-(26) give E[last].
- w_rho = r_att - rho(r_att + r_hon).

## Independent results (my checker, exact Fractions; bias floats converted with as_integer_ratio)
- Bias object/over_bias.npy sha256 a07a5dbb...3ea1 matches CLAIM.md; 27648 = 96·96·3 entries, all finite. Index convention s=(a·96+h)·3+fork. The bias is identical across the three fork values for every (a,h), so the certificate does not depend on the fork ordering: all 6 orderings give the same g_bar.
- Every state and every action Table 1 allows: 72678 inequalities. I also included match at (a,0,relevant), which the author's checker leaves out (72583); those states are unreachable. 0 off-board successors (the builder asserts this); every row's probabilities sum to exactly 1.
- max residual g_bar = -51696398727/351843720888320 ≈ -1.4693000e-4 < 0, at (a=26,h=0,irr), wait. This is identical to the claimed value. With the author's match rule h>=1 I also get 72583 inequalities and the same g_bar. At (T,T) I tried both cap formulas: g_bar is unchanged.
- My own float policy iteration on N_{0.676}^{95} gives optimal gain -1.46930e-4, so the dual is essentially tight and consistent.
- Proof chain I re-derived: (i) the dual inequality with bounded h telescopes, so every policy's average reward in N is <= g_bar < 0, so u_rho^{T*} < 0. (ii) Prop. 3 (if v_rho* >= 0 then u >= v_rho*) in contrapositive form: u < 0 implies v_rho* < 0. (iii) Lemma 8 ratio form: v_rho^pi = ((1-rho)E R1 - rho E R2)/E tau, so any policy with REV(pi) >= rho would have v_rho^pi >= 0. Therefore every policy has REV < rho = 0.676 <= 0.70099 (bank bar). Step (ii) relies on SSZ's published Prop. 3. I did not re-prove it, but the criterion permits relying on it.

## Table 2 calibration and sanity (my own builder and solver, T=95, under-paying M_rho^T, Dinkelbach + policy iteration)
- alpha=0.425: REV = 0.56808788 vs published 0.56808, |diff| 7.9e-6 <= 1e-5: OK
- alpha=0.45: REV = 0.66891320 vs published 0.66891, |diff| 3.2e-6: OK
- Over-paying N_{0.66}^{95}, alpha=0.45: optimal gain +1.0006e-2 > 0 (the stationary-distribution gain agrees): OK

## Author's code (run after my checker, on a copy)
- code/exact_table1_dual.py with the REPRODUCE.md arguments: n=72583, offboard 0, identity_eq7_eq24 true, g_bar = -51696398727/351843720888320, all flags true. This matches object/exact_dual_rho169_250.json (sha256 8d09a679...066d matches CLAIM.md).
- code/calibrate_and_sanity.py (~4.5 min): 0.5680878768 and 0.6689132045 (both within one unit), sanity gain 0.0100061 > 0. CALIBRATION: PASS, SANITY: PASS. These match my independent numbers to about 1e-10. The runs are deterministic.

## Caveat the panel must weigh (a disclosure issue, not a numeric one)
Printed eq. (7) on p.11 has NO outer parenthesis after (1-rho). I checked at 300 dpi: the 1/2·(...) term is not multiplied by (1-rho). FORMULA.md calls its transcription "Printed equation (7)", but it silently inserts "(1-rho) * ( ... )" around the whole bracket and only comments on the 1/2 grouping. If I apply the printed (7) literally, the same bias FAILS: g_bar ≈ +353.2, at a cap adopt with a=95.

I still accept the (1-rho)·(whole bracket) reading, for three reasons:
- The paper's own appendix eq. (27) states that (1-rho)·E[last] with the full bracket "is precisely the reward given" in N_rho^T.
- Lemma 13 / (24)-(26) give exactly that bracket as E[last].
- The literal reading is dimensionally inconsistent with w_rho: the attacker-block term is unscaled by (1-rho).

So the literal print is a typesetting typo, and the claim's N is the one that SSZ's Prop. 3 proof actually covers. CLAIM.md's wording "printed equation (7)" should be amended to "eq. (7) as given by appendix eq. (27)", with the missing parentheses disclosed. If the panel insists on the literal print, the verdict flips to fail.

## Verdict
Every saved object, the claimed exact g_bar, the inequality count (up to the unreachable-state match convention, which passes either way), the Table 2 calibration and the rho=0.66 sanity test all reproduce independently and deterministically. The definition matches Table 1, Section 4.2 and appendix (27). The only mismatch is the undisclosed parenthesization relative to the literal print of (7), documented above.

pass: true
