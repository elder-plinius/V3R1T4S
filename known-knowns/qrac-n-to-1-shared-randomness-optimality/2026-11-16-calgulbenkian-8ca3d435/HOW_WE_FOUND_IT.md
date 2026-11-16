# How We Found It

_Note: contributor text, unverified._

1. **Gram / Walsh-moment relaxations (`formalist`)**: Exact rational moment relaxations over $(S^2)^4$ proved $p(4) \le 0.7428655 < 0.745$ (`p1`), showing why Cauchy-Schwarz (`0.75`) is loose, while exposing two obstacles for naive spherical-angle branch-and-bound: polar coordinate singularities at $v_k = \pm v_1$ and non-differentiability of $\|\sum_i x_i v_i\|_2$ on the regular-tetrahedron locus $w_s = 0$.
2. **Rational Weierstrass symmetry reduction + AM-GM / $LDL^T$ hybrid (`search_engineer`)**: Ordering pairwise inner products so $|v_i \cdot v_j| \le v_1 \cdot v_2$ and flipping signs so $v_1 \cdot v_k \ge 0$ placed all four axes in the closed upper hemisphere $S^2_+$, bijected rationally onto $a^2 + b^2 \le 1$ by the Weierstrass map (collapsing Ambainis's maximizer to the isolated point $z^* = (0,0,1,0,1)$). Majorizing $\sqrt{q_s} \le \frac{\rho_s}{2} + \frac{q_s}{2\rho_s}$ eliminated the $w_s = 0$ singularity on `32,152` `'A'` leaves, while outward-rounded interval $LDL^T$ certified strict concavity $-H_{\text{mid}} \succ 0$ on `410` `'Q'` leaves near $z^*$, shrinking the tree `17.4x` to `43,476` leaves (`98 KB`).
