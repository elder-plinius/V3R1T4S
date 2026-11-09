# Notes: Lens 3 — Certified Hasse-Diagram Bellman Distance Transform & Optimality Export

## Theoretical Foundations
1. **Poset Metric Property**:
   The feasible state space $S = \{u \in \{0,1,2,3\}^{20} : \sum_{g=0}^{19} u_g \le 4\}$ is a downward-closed order ideal (lower semilattice) of $\mathbb{Z}_{\ge 0}^{20}$. For any two states $p, s \in S$, their meet $m = p \wedge s$ (defined componentwise by $m_g = \min(p_g, s_g)$) strictly satisfies $m \in S$.

2. **Weighted-$L_1$ Geodesic Path Decomposition**:
   Under weighted-$L_1$ transition cost $d_w(p, s) = \sum_{g=0}^{19} w_{t,g} |p_g - s_g|$, the metric decomposes into:
   $$d_w(p, s) = d_w(p, p \wedge s) + d_w(p \wedge s, s) = \sum_{g=0}^{19} w_{t,g}(p_g - m_g) + \sum_{g=0}^{19} w_{t,g}(s_g - m_g).$$
   Both paths $p \to m$ and $m \to s$ consist solely of unit coordinate decrements/increments through states with total count $\le \max(\|p\|_1, \|s\|_1) \le 4$, remaining strictly inside $S$.

3. **Two-Pass Hasse Dynamic Programming**:
   - Downward-meet table:
     $$D_t(u) = \min_{p \ge u, p \in S} \left( V_{t-1}(p) + \sum_{g=0}^{19} w_{t,g}(p_g - u_g) \right).$$
     Computed in decreasing order of $\|u\|_1$ (from 4 down to 0) via local cover relations:
     $$D_t(u) = \min\left( V_{t-1}(u), \min_{g: u+e_g \in S} (D_t(u + e_g) + w_{t,g}) \right).$$
   - Upward-join table:
     $$U_t(u) = \min_{m \le u, m \in S} \left( D_t(m) + \sum_{g=0}^{19} w_{t,g}(u_g - m_g) \right).$$
     Computed in increasing order of $\|u\|_1$ (from 0 up to 4) via local cover relations:
     $$U_t(u) = \min\left( D_t(u), \min_{g: u_g > 0} (U_t(u - e_g) + w_{t,g}) \right).$$
   - Stage value update:
     $$V_t(s) = \text{stage}_t(s) + U_t(s).$$

4. **Complexity Reduction**:
   Evaluating all $8 \times 10,606^2 = 899,897,888$ state transitions directly took 6.25s in optimized Rust. The Hasse distance transform executes over $8 \times 35,400 = 283,200$ cover relations in only **138ms** (a 45x speedup), while producing bit-identical Bellman value tables and an independently checkable 5-inequality certificate.
