# Pre-Registration: Statistical Mechanics Entropy Targets

- `null_test: not needed because exact algebraic / transfer-matrix and Collatz-Wielandt certificate computations`

## Target 1: `kings-hard-core-entropy-a247413-digits` (Tractability 3.5, `physics`)

### 1.1 Goal & Success Criteria
- **Full Win**: Compute the King's graph hard-core entropy constant $\Lambda = e^\kappa = \lim_{m,n\to\infty} Z_{m,n}^{1/(mn)} = 1.34264395112460129\dots$ (OEIS `A247413`, currently 18 digits `1,3,4,2,6,4,3,9,5,1,1,2,4,6,0,1,2,9` from snapshot `data/A247413.json`, SHA-256 `12c0e72579f0e422ddf1a43bfb25eda74756be01107b7bfcee3d8af08da40ef8`) to **$D \ge 26$ decimal digits** (exceeding the $18 + 4 = 22$ digit requirement), such that:
  1. **Method A (Nishino–Okunishi / Baxter Symmetric Corner Transfer Matrix Renormalization Group — CTMRG)** in 80-digit `mpmath` arithmetic on the symmetric $2$-state Interaction-Round-a-Face (IRF) weight tensor $W(a,b,c,d)$ of the King's graph across increasing bond dimensions $\chi \in \{10, 14, 18, 22, 26, 30\}$ and
  2. **Method B (Exact Strip Transfer Matrices $\lambda_1(T_m)$ + Exponential/Prony/Levin/Wynn Extrapolation)** in 80-digit arithmetic across widths $m = 1 \dots 20$ (with dihedral reflection symmetry compression and exact $A063443(n)$ verification for $n \le 12$)
  agree on all $D \ge 26$ decimal digits and reproduce all 18 published OEIS digits.
- **Partial Win `p1` (Rigorous Two-Sided Bounds Certifying $\ge 12$ Decimals)**:
  - Using Calkin–Wilf / Friedland–Peled / Lundow–Markström reflection-positivity inequalities on strip and cylinder transfer matrices together with explicit positive integer Collatz–Wielandt certificate vectors ($\min_i (Tv)_i/v_i \le \lambda_1(T) \le \max_i (Tv)_i/v_i$) evaluated in exact arbitrary-precision integer arithmetic, certify a rigorous two-sided interval $[\Lambda_{\text{lower}}, \Lambda_{\text{upper}}]$ agreeing to $\ge 13$ decimals.
- **Partial Win `p2` (Boundary / Surface Free-Energy Constant)**:
  - Compute the free-boundary surface growth factor $\Lambda_s = \lim_{m\to\infty} \frac{\lambda_1(T_m)}{\Lambda^m}$ (and $f_s = \ln \Lambda_s$) to $\ge 20$ decimals via both strip transfer-matrix ratios $\lambda_1(T_m)/\Lambda^m$ and fixed-boundary CTMRG.

---

## Target 2: `potts-antiferromagnet-colouring-entropy-bounds` (Tractability 3.0, `physics`)

### 2.1 Goal & Success Criteria
- **Partial Win `p2`**: Independently reproduce Lundow & Markström's (2008) eigenvalue table for proper $q=4$-colorings of the square grid across open ($P_m$) and cylindrical ($C_m$) strips using full $S_q \times D_m$ color-and-reflection orbit compression, releasing exact/multiprecision dominant eigenvalues.
- **Partial Win `p1`**: Compute $W_{\text{sq}}(4)$ and $W_{\text{sq}}(5)$ to $\ge 18$ decimals by two independent non-rigorous methods (CTMRG on the $q$-state Potts antiferromagnet IRF/vertex tensor in `mpmath`, and strip transfer-matrix sequence extrapolation), confirming that both lie strictly inside the Lundow–Markström rigorous brackets and agree with $W_{\text{sq}}(4) \approx 2.336056641$ within $10^{-9}$.
- **Full Win**: Strictly improve at least one of the published rigorous bounds of Lundow & Markström (2008) by the required margin ($\ge 10^{-9}$ for $W_{\text{sq}}(4)$ or $W_{\text{sq}}(5)$, or $\ge 10^{-6}$ for $W_c(3)$ or $W_c(4)$) using $S_q \times D_m$ symmetry-compressed transfer matrices and explicit Collatz–Wielandt certificate vectors verified in exact integer / outward-rounded interval arithmetic.
