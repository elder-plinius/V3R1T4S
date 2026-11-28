# PREREG — bitcoin-selfish-mining-revenue-bounds

Date: 2026-10-28T22:14:15Z

## Verbatim Success Criterion
A machine-checkable certificate that max over all policies of REV in the untruncated SSZ model (definitions as in arXiv 1507.06183, Sections 2-4, with gamma = 0) is at most U, where U <= 0.70099 at alpha = 0.45 or U <= 0.90466 at alpha = 0.475. Each bar is 1e-4 below the published SSZ Table 2 upper bound (0.70109, 0.90476); lower is better. The certificate has three parts. (i) A rational rho = U and a truncation T. (ii) The finite over-paying MDP N_rho^T built exactly as SSZ Section 4.2 defines it (same states, actions and transition probabilities; compensation rewards from eq. (7) and the following display). (iii) A rational or outward-rounded interval average-reward dual certificate: a gain g < 0 and a bias vector h over all states of N_rho^T such that, for every state s and every action a allowed in s, r_rho(s,a) + sum_{s'} P(s'|s,a) h(s') - h(s) <= g. Here r_rho(s,a) is the expected one-step reward, the transition-probability-weighted w_rho(R_t, honest blocks accepted), including SSZ's truncation compensation. An independent checker rebuilds N_rho^T from the paper's formulas (not from the claimant's files), verifies every inequality, and concludes via SSZ Proposition 3 that max REV < rho. The checker must first reproduce SSZ Table 2's epsilon-OPT values 0.56808 (alpha = 0.425) and 0.66891 (alpha = 0.45) within one unit of their last printed digit with its own model builder. As a sanity test that the over-paying MDP is not mis-built, its own policy-iteration solve of N_rho^T at alpha = 0.45, rho = 0.66 must return a positive optimal gain. These safety margins compare against numerical published bars. If an incumbent is available as an exact certificate, any exactly certified strict improvement over it counts.

## Checker and Judgment Protocol
The independent checker:
1. Reconstructs $N_\rho^T$ independently from the formulas in arXiv:1507.06183 Sections 2-4.
2. Checks that the claimed gain $g$ is strictly negative ($g < 0$).
3. Evaluates $r_\rho(s, a) + \sum_{s'} P(s'|s, a) h(s') - h(s) \le g$ for EVERY state $s \in S$ and EVERY valid action $a \in A(s)$, using exact rational or outward-rounded interval arithmetic.
4. Reproduces the calibration facts:
   - Under-paying MDP $M_\rho^T$ policy iteration yields SSZ Table 2 $\epsilon$-OPT values:
     - $\alpha = 0.425 \implies 0.56808 \pm 10^{-5}$
     - $\alpha = 0.45 \implies 0.66891 \pm 10^{-5}$
   - Sanity check: Policy iteration on $N_\rho^T$ at $\alpha = 0.45, \rho = 0.66$ yields positive optimal gain $> 0$.
5. Confirms $U \le 0.70099$ for $\alpha = 0.45$ and $U \le 0.90466$ for $\alpha = 0.475$ (CONFIRMED_SOLUTION).
6. Checks partial wins:
   - p1: Exact rational evaluation of stationary policy exceeding $0.66894 + 10^{-6}$ at $\alpha = 0.45$ or $0.80184 + 10^{-6}$ at $\alpha = 0.475$.
   - p2: Certified upper bounds for $\alpha = 0.40$ ($U < 0.48904$) and $\alpha = 0.425$ ($U < 0.57226$).

null_test: not needed because the claim consists of explicit machine-checkable exact/interval mathematical certificates verified deterministically by an independent checker verifying all state-action Bellman inequalities.
