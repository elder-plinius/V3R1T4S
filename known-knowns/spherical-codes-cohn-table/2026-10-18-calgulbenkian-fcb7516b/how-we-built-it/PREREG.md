# Preregistration: Cohn's Table of Spherical Codes (`spherical-codes-cohn-table`)

## Target & Success Criterion
- **Target ID**: `spherical-codes-cohn-table`
- **Status Sources**:
  - `data/index.html` (`https://spherical-codes.org/`, SHA-256 `8ba8f44d9fd752ab9f70fa954c9455e4ea08398c5e47a9664feea876b3037004`)
  - `data/plain.txt` (`https://spherical-codes.org/plain`, SHA-256 `b87dcc6df39fb05f8d969ab5a12864e9e8bee6299ab60b4ca3844b57433e971d`)
- **Objective**: For a row $(d, N)$ present in `plain.txt`, find $N$ vectors $x_1, \dots, x_N \in \mathbb{R}^d$ given to $\ge 25$ significant digits such that after normalizing each vector to unit length in `mpmath` at 50 decimal digits (`mp.dps = 50`), the maximum pairwise inner product (cosine of the minimal angle)
  $$c^* = \max_{1 \le j < k \le N} \langle x_j, x_k \rangle$$
  satisfies:
  1. **Goal A (Full Win)**: On an unstarred row (`&ast;` absent in `index.html`) that does **not** contain `"needs more optimization"` in `index.html`, is not `(6, 526)`, and is not in the kissing-number regime (`9 <= d <= 23` and $c^* \le 0.5$), $c_{\text{table}} - c^* \ge 10^{-10}$.
  2. **Goal B (Partial Win `p2`)**: A batch of $\ge 20$ certified improvements ($c_{\text{table}} - c^* \ge 10^{-10}$ each) to rows labeled `"needs more optimization"` in a single dimension $d \in 4..32$.
  3. **Goal C (Partial Win `p3`)**: An exact algebraic minimal polynomial certificate for an unstarred, unlabeled row $(d, N)$ that currently has no minimal polynomial listed in `plain.txt`, where $c^*$ is polished to 100-digit precision via Newton-Raphson on the rigid active contact graph, shown via `mpmath.findpoly` at 60 digits (confirmed at 100 digits) to be an exact algebraic root matching $c_{\text{table}}$ to $10^{-12}$, with contact Jacobian rigidity verified.

## Null Test
- `null_test`: not needed because explicit spherical code coordinates and algebraic minimal polynomials are verified deterministically in 50-to-100-digit `mpmath` arithmetic against the published table values.

## Methodology
1. **Riemannian L-BFGS + Basin-Hopping Optimizer (`sc_opt.c`)**:
   - Minimizes the smooth log-sum-exp objective $L_\beta(X) = \frac{1}{\beta} \log \sum_{j < k} \exp(\beta \langle x_j, x_k \rangle)$ on $(S^{d-1})^N$ with $\beta$ continuation from $10^2$ to $10^{11}$ and tangential basin-hopping kicks.
2. **Arbitrary-Precision Active-Set Minimax & Newton-Raphson Polisher (`verify_sc.py`)**:
   - Uses iterative linearized minimax / Gauss-Newton projection on the active contact graph in `mpmath` (50 to 110 digits) to polish configurations to $\ge 30$–$100$ digits, verify Jacobian rigidity ($\operatorname{rank}(J) = dN - \binom{d}{2} - 1$), and extract exact integer minimal polynomials via `mpmath.findpoly`.
