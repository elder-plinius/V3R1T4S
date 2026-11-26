# Pre-Registration (`magic-state-distillation-fewest-qubits`)

- `target_id`: `magic-state-distillation-fewest-qubits`
- `frozen_utc`: `2026-11-10T09:50:00Z`
- `null_test`: `not needed because magic-state-distillation-fewest-qubits is an exact algebraic and combinatorial existence/non-existence problem over F_2 verified by deterministic exact linear algebra and group-orbit enumeration`
- `primary_criterion`: Exact $\mathbb{F}_2$ polynomial-algebra triorthogonality conditions Eqs. (18a)–(18d) and distance condition Eq. (19) (for $T$-to-$T$) and Eqs. (40a)–(40d) and distance condition Eq. (42) (for $T$-to-$\text{CCZ}$) of Jacinto et al. (`arXiv:2606.07734v2`), combined with exhaustive $\mathrm{AGL}(r, 2)$-orbit enumeration of Reed–Muller dual supports $\mathbf{1}_Y \in \mathrm{RM}(r-4, r)$ for `p1` ($N_{\text{CCZ}}(4) = 10$) and `p2` ($N_T(4) \ge 9$).
- `planned_lenses`:
  1. `Lens 1 (Exact F_2-Linear Fredholm Alternative & Quotient Reduction on Reed-Muller Supports)`: Projecting triorthogonal check columns $X \subseteq \mathbb{F}_2^r \setminus \{0\}$ onto their even completion $Y \in \mathrm{RM}(r-4, r)$ and testing existence of a distance-$4$ logical row $u \in V_4(X)$ via the exact $\mathbb{F}_2$-linear Fredholm Alternative ($\mathbf{1}_X \notin \mathrm{Span}\{x_a|_X, (x_a x_b)|_X, e_a \oplus e_b \oplus e_{a \oplus b}\}$).
  2. `Lens 2 (Three-Handle Self-Contained AGL(7, 2) Orbit Exhaustion & Hyperplane Parity Split)`: Certifying pairwise orbit disjointness, 8-level Schreier–Sims stabilizer orders, and exact $2^{64}$ orbit mass across all `3,486` $\mathrm{AGL}(7, 2)$-orbits of $\mathrm{RM}(3, 7)$, plus testing hyperplane parity splits (`Master Theorem 3a/3b`) and parity-extension lifts (`Master Theorem 4`).
