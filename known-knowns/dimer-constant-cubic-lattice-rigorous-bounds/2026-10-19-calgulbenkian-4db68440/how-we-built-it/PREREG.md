# Pre-Registration: `dimer-constant-cubic-lattice-rigorous-bounds`

- **Problem ID**: `dimer-constant-cubic-lattice-rigorous-bounds`
- **Category**: `physics` (Statistical Mechanics / Lattice Combinatorics)
- **Tractability**: `3.0`
- **Target Constants**:
  1. **3D Cubic Lattice Dimer Entropy Constant ($\ell_3$)**:
     $$\ell_3 = \lim_{n \to \infty} \frac{\log M(Q_n)}{|V(Q_n)|}$$
     Best published rigorous bounds:
     $$0.440075 \le \ell_3 \le 0.452130$$
     - Lower bound `0.440075`: Ciucu (1998) / Schrijver (1998).
     - Upper bound `0.452130`: Qidong He, *"Improved Upper Bounds on the Cubic Lattice Dimer Constant via Diagonal Layers"*, `arXiv:2607.28810v2` (August 11, 2026), Theorem 1.1 & Table 2 (`(m, n) = (5, 5)` at Collatz–Wielandt iteration $p = 2$).
  2. **3D Cubic Lattice Monomer-Dimer Entropy ($h_3$)**:
     Best published rigorous bounds (Friedland & Peled `arXiv:math/0402009`; Friedland, Krop, Lundow, Markström `arXiv:math/0603001`):
     $$0.7849602275 \le h_3 \le 0.7862023450$$
  3. **4D Hypercubic Lattice ($\mathbb{Z}^4$) Dimer Entropy Constant ($\ell_4$)**:
     Best published rigorous bounds (Schrijver 1998; Butera, Federbush, Pernici, *Phys. Rev. E* **88**, 032113 (2013), `arXiv:1305.7028`, Table III, p. 5):
     $$0.55808612 \le \ell_4 \le \frac{\ln(8!)}{16} = 0.66278769\dots$$

## Success Criteria & Win Paths

1. **Full Win ($\ell_3$ Upper Bound Improvement)**:
   - Certify a rigorous upper bound on $\ell_3$ strictly below Qidong He's `0.452130` (`arXiv:2607.28810`) by at least $10^{-6}$, accompanied by an explicit positive integer test vector and exact integer arithmetic Collatz–Wielandt verification.
2. **Partial Win `p1` (Independent Reproduction of He's Table 2)**:
   - Independently reproduce He's `0.452130` at $(m, n) = (5, 5)$ ($p = 2$) and all 11 smaller entries of Table 2 (`(2,2), (3,2), (3,3), (4,2), (4,3), (4,4), (5,2), (5,3), (5,4), (6,2), (6,3)`) to all 6 decimal places using exact integer arithmetic.
3. **Partial Win `p2` (3D Monomer-Dimer Entropy $h_3$ Bound Improvement)**:
   - Certify a rigorous improvement on the published bounds $0.7849602275 \le h_3 \le 0.7862023450$ by extending Csikvári's 2-lift matching-generating-function inequality (He's Theorem 2.4 at unit monomer/dimer activity $t = 1$) to diagonal transfer layers $\mathbb{T}_{m,n,l}$.
4. **Partial Win `p3` (4D Hypercubic Dimer Constant $\ell_4$ Upper Bound Improvement)**:
   - Generalize the diagonal layer transfer matrix and $S_4 \ltimes (\mathbb{Z}_{m_1} \times \mathbb{Z}_{m_2} \times \mathbb{Z}_{m_3})$ symmetry reduction to $\mathbb{Z}^4$ and certify a rigorous upper bound on $\ell_4$ strictly below `0.66278769`.

## Methodology & Verification Protocol

1. **Exact 256-Bit Integer Arithmetic**: All matrix-vector multiplications $\vec{y} = X_{m,n}^{(i)} Y_{m,n}^{(i)} \vec{x}$ are performed in exact 256-bit unsigned integer arithmetic (`u256`), and all Collatz–Wielandt ratio comparisons $\frac{y_u}{x_u} \gtrless \frac{y_v}{x_v}$ are performed via exact 512-bit cross-multiplication $y_u x_v \gtrless y_v x_u$.
2. **Algorithmic Speedups Over He's Baseline**:
   - **Greedy Neighbor-Overlap Vertex Ordering**: Ordering vertices of $U$ to maximize shared neighbors with already-placed vertices collapses the permanent DFS branching tree by 10x–30x.
   - **Future-Reachability Bitmask Pruning**: Precomputing `future_reach[pos]` and pruning branches whenever `__builtin_popcount(used | future_reach[pos + 1]) < k` eliminates Hall-infeasible subtrees early.
   - **Register-Only Leaf Counting at $p = 0$**: Unrolling the final 2 levels of the DFS into bitwise popcounts avoids memory lookups on the initial all-ones vector pass.
   - **Monotone Sector Early Stopping (Proposition 3.3)**: Evaluating the middle sector $i = \lfloor mn/2 \rfloor$ first and stopping smaller sectors $i < \lfloor mn/2 \rfloor$ as soon as $C_{m,n; p}^{(i)} \le C_{m,n; p_{\max}}^{(\lfloor mn/2 \rfloor)}$.
3. **Standalone Verification**: `verify_cubic_dimer.py` independently verifies all certificates and Table 2 reproductions.
