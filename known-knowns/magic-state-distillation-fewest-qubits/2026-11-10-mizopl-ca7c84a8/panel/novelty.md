# Skeptic 2 — Novelty & Literature Audit (`novelty.md`)

- `context`: `fresh independent skeptic review comparing package against arXiv:2606.07734, arXiv:2609.30860, and arXiv:2610.06535`
- `target_id`: `magic-state-distillation-fewest-qubits`

## Audit Findings

1. **Comparison with Jacinto et al. (`arXiv:2606.07734v2`), Wills et al. (`arXiv:2609.30860`), and Jain (`arXiv:2610.06535v1`)**:
   - In `arXiv:2606.07734v2` (Table I & Section V), the minimum qubit counts for distance-$4$ distillation were bounded only by $8 \le N_T(4) \le 10$ (with $N=8, d=4$ timing out after 2 months of SAT solving across $55 \le n \le 127$) and $9 \le N_{\text{CCZ}}(4) \le 10$ (open on $N=9$ for $55 \le n \le 63$).
   - Neither `arXiv:2609.30860` (exhaustive up to $n \le 54$) nor `arXiv:2610.06535v1` (exhaustive up to $r \le 7$ only for $k \ge 3$) resolved $k=1$ ($T$-to-$T$) at $N=8, r=7$ across $55 \le n \le 127$ or $k=3$ ($T$-to-$\text{CCZ}$) at $N=9, r=6$ across $55 \le n \le 63$.
2. **Five New Structural Theorems & Complete Resolution of `p1` and `p2`**:
   - **Master Theorem 1 (`F_2-Linear Fredholm Alternative Reduction`)** eliminates all nonlinear constraints on Fixed Reed–Muller Check Supports $X \subseteq \mathbb{F}_2^r \setminus \{0\}$ for $T$-to-$T$ ($d=4, 5$) and reduces $T$-to-$\text{CCZ}$ ($d=4$) to the small quotient $V_4(X)/L_X$.
   - **Master Theorem 2 (`Analytic + Exhaustive Proof of p1: N_CCZ(4) = 10`)** proves via the exact weight gap of $\mathrm{RM}(2, 6)$ (zero codewords in $[49, 63]$) and the collinear-triple rank `57/63` on $\mathbb{F}_2^6 \setminus \{0\}$ (`dim(V_4/L_X) = 0`) that no $N \le 9, d \ge 4$ $T$-to-$\text{CCZ}$ protocol exists for any $1 \le n \le 63$.
   - **Master Theorem 5 (`Three-Handle Self-Contained RM(3, 7) Orbit Exhaustion`)** proves `p2` ($N_T(4) \ge 9$) across all `3,486` $\mathrm{AGL}(7, 2)$-orbits (`446,208` shifted supports) in `~11s`.
   - **Master Theorems 3 & 4 (`Hyperplane Parity Split, Collinearity Locking & Parity-Extension Lifting`)** explain the skewed hyperplane geometry of all $d=4$ factories and the canonical $(N, n, 4) \to (N+1, n+1, 5)$ lifting law.

pass: true
