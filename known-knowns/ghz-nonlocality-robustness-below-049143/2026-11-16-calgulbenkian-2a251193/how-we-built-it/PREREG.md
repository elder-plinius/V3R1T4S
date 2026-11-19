# Pre-Registration: ghz-nonlocality-robustness-below-049143

frozen_utc: 2026-11-15T15:13:48Z
target_id: ghz-nonlocality-robustness-below-049143
null_test: not needed because exact mathematical certificate (finite rational Bell functional with exact exhaustive deterministic local bound L and 40-digit outward-rounded interval evaluation of Q_GHZ, Q_noise, and v*)

## Frozen Success Rules and Thresholds

- **Full win (`solution_claim`)**: An explicit tripartite ($N = 3$) binary-outcome Bell functional with exact integer/rational coefficients (`m_A, m_B, m_C` settings), exact projective measurement directions on $S^2$, exact white-noise expectation $Q_{\text{noise}}$ on $I/8$, 40-digit `mpmath.iv` outward-rounded GHZ expectation $Q_{\text{GHZ}}$ on $|\mathrm{GHZ}_3\rangle = (|000\rangle + |111\rangle)/\sqrt{2}$, and **exact** deterministic local maximum $L$ over $\{\pm 1\}^{m_A} \times \{\pm 1\}^{m_B} \times \{\pm 1\}^{m_C}$ certified as required by `verification_method`, such that the upper endpoint of the outward-rounded interval for $v^* = (L - Q_{\text{noise}}) / (Q_{\text{GHZ}} - Q_{\text{noise}})$ satisfies
  $$v^* \le 0.49142000 = 0.49143 - 10^{-5}.$$
- **Partial win `p2` (`partial_win_claim`)**: Exact local-bound certification of an uncertified `arXiv:2310.20677` planar instance (e.g. $N = 3, m \ge 32$) giving $v^* \le 0.49142$ (which simultaneously satisfies the full $N = 3$ win criterion).
- **Partial win `p1` (`partial_win_claim`)**: Certified improvement by at least $10^{-5}$ for some $N \in \{4, \dots, 10\}$ over `arXiv:2310.20677` Table 3 (`0.32493, 0.20872, 0.13422, 0.08569, 0.05544, 0.03521, 0.02301`).

## Calibration Checks (Frozen Before Execution)

1. Reproduce Mermin's $2 \times 2 \times 2$ inequality on $|\mathrm{GHZ}_3\rangle$: $L = 2, Q_{\text{GHZ}} = 4, Q_{\text{noise}} = 0 \implies v^* = 0.5$.
2. Reproduce a published planar value from `arXiv:2310.20677` Table 6 (e.g. $N = 3, m = 6 \implies v^* = 50/101 = 0.4950495\ldots$, $m = 8 \implies 0.49317$, $m = 10 \implies 0.49206$) to verify exact agreement of state conventions, noise model $v |\mathrm{GHZ}_3\rangle\langle\mathrm{GHZ}_3| + (1-v) I/8$, and local bound computation.
3. Verify that every candidate single-qubit observable $O = n_x X + n_y Y + n_z Z$ satisfies $\|n\|_2 = 1$ exactly (or via exact rational Weierstrass parameterization $n(a,b) = \left(\frac{2a}{1+a^2+b^2}, \frac{2b}{1+a^2+b^2}, \frac{1-a^2-b^2}{1+a^2+b^2}\right)$ so $\|n\|_2 = 1$ holds identically over $\mathbb{Q}$ with zero normalization rounding!).
