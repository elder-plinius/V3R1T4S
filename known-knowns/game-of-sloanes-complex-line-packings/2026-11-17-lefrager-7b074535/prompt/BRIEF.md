# Attack Brief — `game-of-sloanes-complex-line-packings`

## Mathematical Framing

Given `(d, n)` with `3 <= d <= 7`, we seek `n` unit vectors `Phi = [phi_0, ..., phi_{n-1}] in C^{d x n}`, `||phi_j||_2 = 1`, minimizing the worst-case Grassmannian coherence:
`mu(Phi) = max_{0 <= j < k < n} |<phi_j, phi_k>|` (equivalently minimizing `t = mu^2 = max_{j<k} |<phi_j, phi_k>|^2`).

Why existing records (`hlc`, `jrr`, `JJ`, `dgm`) get stuck:
1. Smooth surrogates (`sum_{j<k} |<phi_j, phi_k>|^{2p}` or `LogSumExp(beta * |g_{jk}|^2)`) suffer from extreme conditioning (`beta > 1e4` becomes stiff) or stop strictly above the nonsmooth Clarke-stationary minimax kink where ~`O(n)` active pairs tie at `|g_{jk}|^2 = t`.
2. Standard gradient optimizers get trapped in rigid high-coherence basins from generic random initializations, whereas deleting vectors, injecting algebraic/group-orbit structure, or running alternating minimax active-set steps jumps between basins.

## Diverse Attack Angles (>= 5 Distinct Methods)

1. **Smooth Manifold Annealing + Exact Active-Set Minimax SQP (`physics-geometry` / C++17 OpenMP):**
   - Stage A: Riemannian L-BFGS / BB-gradient on `(S^{2d-1})^n` minimizing `LogSumExp(beta * |<phi_j, phi_k>|^2)` as `beta` schedules from `10 -> 2000`.
   - Stage B: **Exact Minimax Active-Set Polishing** via projected linearized SQP / minimax dual simplex: identify active + near-active pairs `E = {(j,k) : |g_{jk}|^2 >= t_max - eps}`, compute the minimum-norm convex hull direction of their Riemannian gradients (Wolfe / Frank-Wolfe / quadratic dual solver on the probability simplex over active pairs), and Armijo line-search directly on the true `max_{j<k} |g_{jk}|^2` objective! This directly solves nonsmooth minimax kinks to `1e-13` precision.
2. **Basin-Hopping & Repulsion/Insertion Surgeries (`physics-geometry` / C++17 OpenMP):**
   - Warm-started from `baseline/*.txt` AND cold-started: identify the worst-coupled vector(s) participating in maximum-coherence pairs, delete 1–3 vectors or kick them across `CP^{d-1}`, re-insert via greedy worst-pair minimax + alternating repulsion/projection, then polish with Stage A + Stage B.
   - Vector-deletion transfer (`(d, n+k) -> (d, n)` and greedy add `(d, n-1) -> (d, n)`).
3. **Alternating Frame / Block-Coordinate Minimax & Second-Order Gauss-Newton (`solver-reduction`):**
   - Optimize one vector `phi_i` at a time against fixed `{phi_j}_{j != i}` using exact sequential minimax / ellipsoid / trust-region step on `S^{2d-1}`, which has only `2d - 1` real degrees of freedom per block (`5` variables in `C^3`!).
4. **Algebraic & Group-Orbit Parameterizations (`circuit-minimalism`):**
   - Search over finite-group / cyclic-difference-set / Weyl-Heisenberg / Vandermonde / symmetric seed families in `C^3, C^4` as low-dimensional structural starts, then break symmetry slightly and polish with active-set minimax SQP.
5. **Dual Colab Verification & Parallel Search (`colab-gpu-solver`):**
   - Re-verify any local improvement in Colab with `mpmath` (40+ digits) and live `README.md` + open PR check; optionally run batched PyTorch/NumPy multi-start optimization for higher `(d, n)` rows on Colab.

## Kill Criteria
- Drop any candidate optimization target row cleanly if multi-lens effort confirms the baseline already sits in a deep isolated minimax basin with zero improvement (`< 1e-10`) and pivot cleanly among the 104 unclaimed open `(d, n)` rows (e.g., `(3,19)`, `(3,20)`, `(3,21)`, `(3,23)`, `(3,37)`, `(3,39)`, `(3,13)`, `(3,15)`, `(3,28)`, `(3,31)`, `(3,33)`, `(4,21)`, `(4,24)`, `(4,27)`, `(5,31)`).
