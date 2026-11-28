# PREREG — bitcoin-selfish-mining-revenue-bounds (run 2026-11-26-1939)
frozen (UTC): 2026-11-26 19:42:51 UTC
command that produced the time: date -u

## Criterion (verbatim from bank/targets.json)
A machine-checkable certificate that max over all policies of REV in the untruncated SSZ model (definitions as in arXiv 1507.06183, Sections 2-4, with gamma = 0) is at most U, where U <= 0.70099 at alpha = 0.45 or U <= 0.90466 at alpha = 0.475. Each bar is 1e-4 below the published SSZ Table 2 upper bound (0.70109, 0.90476); lower is better. The certificate has three parts. (i) A rational rho = U and a truncation T. (ii) The finite over-paying MDP N_rho^T built exactly as SSZ Section 4.2 defines it (same states, actions and transition probabilities; compensation rewards from eq. (7) and the following display). (iii) A rational or outward-rounded interval average-reward dual certificate: a gain g < 0 and a bias vector h over all states of N_rho^T such that, for every state s and every action a allowed in s, r_rho(s,a) + sum_{s'} P(s'|s,a) h(s') - h(s) <= g. Here r_rho(s,a) is the expected one-step reward, the transition-probability-weighted w_rho(R_t, honest blocks accepted), including SSZ's truncation compensation. An independent checker rebuilds N_rho^T from the paper's formulas (not from the claimant's files), verifies every inequality, and concludes via SSZ Proposition 3 that max REV < rho. The checker must first reproduce SSZ Table 2's epsilon-OPT values 0.56808 (alpha = 0.425) and 0.66891 (alpha = 0.45) within one unit of their last printed digit with its own model builder. As a sanity test that the over-paying MDP is not mis-built, its own policy-iteration solve of N_rho^T at alpha = 0.45, rho = 0.66 must return a positive optimal gain. These safety margins compare against numerical published bars. If an incumbent is available as an exact certificate, any exactly certified strict improvement over it counts.

Partial wins remain as in target.md (p1, p2, p3). Corollary 14 of the same paper (REV <= rho + 2 u when the under-paying value at that rho is nonnegative) is an additional published certificate form and will be tried if u stays positive.

## Statistic / checker
- Official truncation: only adopt is legal when max(a,h)=T.
- Under-paying adopt reward: w = -rho * h (ordinary adopt).
- Over-paying adopt reward: eq. (7) / (28) as transcribed in BRIEF.md from the fetched PDF (sha256 0cc1fdc04eb5c925e294eff74dc5388f2921b6cd8164985b29dae4cf34da2b34).
- Calibration: under-paying PI at T=95 reproduces 0.56808 (alpha=0.425) and 0.66891 (alpha=0.45) within one unit of the last printed digit, or is reported honestly if it instead matches the tighter PTO digits as in the previous run.
- Sanity: over-paying gain at alpha=0.45, rho=0.66 is positive.
- Bank-format win: dual with g<0 at some rho<=0.70099 (alpha=0.45) or 0.90466 (0.475), inequalities checked with fractions or outward rounding.
- Corollary-14 win: under-paying value >= 0 at rho', over-paying u certified, U = rho' + 2*u <= the bar (lower better).

## Thresholds
Unchanged from the bank (full win and p1-p3).

## Null design
null_test: not needed because a claim is an explicit certificate or an explicit policy checked by a deterministic builder against the bank's inequalities and published table digits, not a search or "beats chance" statistic.

## Baseline
not applicable (deterministic object versus a table value / inequality).

## Out of scope
Live mining, pools, SHA-256d nonce search, attacks on third-party systems. Charter remains unpublished.
