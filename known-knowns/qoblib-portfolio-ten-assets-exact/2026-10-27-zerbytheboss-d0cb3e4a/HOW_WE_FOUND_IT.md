# How We Found It — `qoblib-portfolio-ten-assets-exact`

Contributor text, unverified.

## Brief & Observation
The multi-period Markowitz portfolio optimization problem on QOBLIB (instance `po_a010_t10_orig_b004_l1e-03`) has a published incumbent objective of `-8397` from Maximilian Schicker (`2025-08-19`, `06-portfolio/solutions/po_a010_t10_orig/po_a010_t10_orig_b004_l1e-3.bst.sol`). However, the reported bound in that submission was Gurobi's numerical MIP bound of `-15342.65126758` after `3600.03 s`, leaving open whether a better integer schedule exists or whether `-8397` is globally optimal.

Analyzing the problem structure shows that each period requires choosing positions across 10 assets (long and short) with integer unit counts $u \in \{0, 1, 2, 3\}$ and total portfolio units $\sum_g u_g \le 4$. This yields:
$$\sum_{k=0}^4 \binom{20 + k - 1}{k} = 1 + 20 + 210 + 1540 + 8835 = 10,606 \text{ states per period.}$$

## What Failed
Direct all-pairs dynamic programming over 10 periods requires evaluating $8 \times 10,606^2 \approx 900 \times 10^6$ state transitions. While feasible in compiled Rust (taking ~6 seconds), verifying an all-pairs certificate in a standalone Python script would require quadratic transition loops across all 8 interior transitions.

## What Worked
We solved and certified global optimality through three steps:

1. **Step 1 (Compiled Rust DP)**:
   We built an exact-integer Bellman solver in Rust exploring all 10,606 count states and 899,897,888 transitions in exact arithmetic. This confirmed that no schedule $\le -8398$ exists and that $\min_{s \in S} V_9(s) = -8397$.

2. **Step 2 (Polytope & Slack Audit)**:
   We checked that cash slack is contained in $[6, 14] \subset [0, 15]$ and budget slack in $[0, 4] \subset [0, 127]$ for every state in $S$, so the binary slack registers never restrict the discrete count state space $S$.

3. **Step 3 (Hasse-Diagram Distance Transform Certificate)**:
   Because the state space $S$ is a lower semilattice under componentwise ordering $\le$, the weighted-$L_1$ transition cost between any two states factors through their meet $m = p \wedge s$. We formulated a two-pass distance transform on the Hasse diagram of $S$ (35,400 cover relations):
   - Downward-meet pass: $D_t(u) = \min_{p \ge u} (V_{t-1}(p) + \text{dist}(p, u))$
   - Upward-join pass: $U_t(u) = \min_{m \le u} (D_t(m) + \text{dist}(u, m))$
   Furthermore, because `bqp_u3_c10.zpl` sums inter-period transaction costs only over `t in TX \ { t_beg, t_end } = {1, ..., 8}` and has no transaction-cost term between periods 8 and 9, period 9 decouples as $V_9(s) = \text{stage}_9(s) + \min_{p \in S} V_8(p)$. This reduces verification from $\sim 900 \times 10^6$ transition checks to $8 \times 35,400 = 283,200$ local cover checks, allowing `verify-it-yourself/check_portfolio_opt.py` to verify all stage costs and Bellman inequalities in under 0.6 seconds.
