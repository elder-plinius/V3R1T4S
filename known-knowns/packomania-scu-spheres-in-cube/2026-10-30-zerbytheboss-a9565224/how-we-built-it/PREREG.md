# PREREG: packomania-scu-spheres-in-cube

Date: 2026-10-30T10:35:00Z

## Hypotheses
1. H1 (Data Integrity Audit): The 50-digit mpmath feasible radius calculation $r^* = \min(\min_{i<j} \|c_i - c_j\|/2, 1/2 - \max_i \max(|x_i|, |y_i|, |z_i|))$ across all $N \le 1000$ coordinate files reproduces the live `radius.txt` table within numerical formatting precision (typically $\le 1.5 \times 10^{-12}$ for complete $N$-center files), identifying any truncated files or rounding discrepancies (`p3`).
2. H2 (Pre-2000 Hand Construction Optimization): Hand-placed configurations by Dave Boll ($N \in \{16, 19, 20, 24, 25, 29, 30, 31, 39, 48\}$) and Hugo Pfoertner ($N \in \{28, 35, 37, 38, 40, 44, 45, 50, 52, 53, 60, 61, 62, 67\}$) possess sub-optimal contact graphs with vacant free volume. Riemannian L-BFGS and Active-Set SQP optimization will contract loose rattlers, expand the contact manifold, and strictly beat the live table radius by $r^* - r_{\text{table}} \ge 10^{-11}$ (`p1` / `CONFIRMED_SOLUTION`).
3. H3 (Sibling SSP Packing Optimization): Sibling sphere-in-sphere configurations with unoptimized author rows can be relaxed to exceed live `ssp` table radii by $r^* - r_{\text{table}} \ge 10^{-10}$ (`p2`).

## Verification Methodology
- Verification Engine: Exact 50-digit arithmetic using Python `mpmath` (`mp.dps = 50`).
- Strict Margin: $\Delta r = r^* - r_{\text{table}} \ge 10^{-11}$ for `scu`, $\ge 10^{-10}$ for `ssp`.
- Container Centering: $[-1/2, 1/2]^3$ for cube; $\|c_i\|_2 + r^* \le 1$ for unit sphere.
- Structural Divergence: Non-isometry certified via sorted $\binom{N}{2}$ squared pairwise distance multisets.

null_test: not needed because sphere packing feasibility and radius optimality are verified by exact 50-digit mpmath continuous geometry without statistical sampling.
