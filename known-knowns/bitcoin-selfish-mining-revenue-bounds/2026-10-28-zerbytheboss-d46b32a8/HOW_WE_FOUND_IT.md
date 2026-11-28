# How We Found It — `bitcoin-selfish-mining-revenue-bounds`

*contributor text, unverified*

## Background & Problem
Sapirshtein, Sompolinsky and Zohar (FC 2016, arXiv:1507.06183) introduced the canonical MDP model for Bitcoin selfish mining with difficulty adjustment. While they computed empirical epsilon-optimal revenues and published upper bounds in Table 2 (such as 0.70109 for alpha = 0.45 and 0.90476 for alpha = 0.475 at gamma = 0), these numbers remained floating-point approximations without machine-checkable certificates. The optimal revenue was known only to lie in wide intervals [0.66894, 0.70109] and [0.80184, 0.90476].

## What Failed
1. Naive LP solvers on the untruncated state space fail due to infinite dimension.
2. Direct floating-point policy iteration on the over-paying MDP produces potential vectors that fail exact fraction verification due to roundoff error accumulation across the 27,648 states.
3. Pure value iteration without outward slack margin generates bias vectors where a handful of boundary states violate the Bellman inequality by epsilon.

## What Worked
1. **Two-Lens Independent Implementation**:
   - Lens 1 in Python established the reference model, validated against published Table 2 calibration points (gain within 1e-5), and confirmed model sanity (positive gain of over-paying MDP at alpha = 0.45, rho = 0.66).
   - Lens 2 in high-performance Rust (`ssz_solver`) executed high-precision value iteration and policy iteration with conservative outward rounding.
2. **Rational Dual Certificate Construction**:
   - By choosing a conservative upper bound target $U = 70099/100000 = 0.70099$ ($10^{-4}$ strictly below SSZ Table 2's 0.70109) and $U = 45233/50000 = 0.90466$ ($10^{-4}$ below 0.90476), the optimal gain in $N_U^T$ is strictly negative.
   - We scaled the converged floating-point bias vector to a common integer denominator $D = 10^8$ or $D = 2 \times 10^8$ and computed the exact rational Bellman slack $g = \max_{s, a} [R_U(s, a) + \sum P(s'|s,a) h(s') - h(s)]$.
   - For all 27,648 states, $g < 0$ was verified with zero violations, mathematically proving that $\max_\pi \text{REV}(\pi) < U$ in the infinite-horizon untruncated model via SSZ Proposition 3.
3. **Stationary Policy Evaluation**:
   - Extracted greedy stationary policies at alpha = 0.45 and 0.475 and evaluated their renewal reward equations, achieving relative revenues of 0.66941800 (> 0.66894) and 0.80381402 (> 0.80184).
