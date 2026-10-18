# How We Found It: Sign-Pure Sub-Block Conjugation on Composite Tensor `14x15x15`

*(contributor text, unverified)*

## 1. The Seam Obstacle in Serendipitous Tensor Products

In Perminov's `SerendipitousProductBuilder` (arXiv:2603.18699), the composite format `14x15x15` factors as the Kronecker product of $s_1 = (7, 5, 5)$ (`5x5x7_m127_ZT.json`, rank $127$ in `ZT`) and $s_2 = (2, 3, 3)$ (`2x3x3_tensor.mpl`, rank $15$ in `ZT`), giving base rank $127 \times 15 = 1,905$. Whenever $s_1$ contains a disjoint pair of rank-1 terms $(f_0, f_1)$ with $V^{(1)}_{f_0} = \pm V^{(1)}_{f_1}$ (a "$v$-bud"), the direct sum of two copies of $s_2$ ($2 \times 15 = 30$ multiplications) can be replaced by a single copy of $s_3 = (4, 3, 3)$ (`3x3x4_tensor.mpl`, rank $29$ in `ZT`), saving $1$ multiplication per bud pair.

In the standard row/column ordering $(0, 1, 2, 3)$ of `3x3x4_tensor.mpl`, overlapping non-zeros between sub-block $\{0, 1\}$ and sub-block $\{2, 3\}$ have mixed relative signs, so `10` of the `11` disjoint $v$-buds produce entries in $\{\pm 2\}$ (`Z` rank `1,895`, `ZT` rank `1,905`).

## 2. Sign-Pure Sub-Block Conjugation

Applying the sub-block transposition $\pi = (0, 1, 3, 2) \in S_4$ simultaneously to the 4 rows of $U^{(3)}$ and the 4 columns of $W^{(3)}$ preserves the Kronecker delta $\delta_{\pi(r), \pi(r')} = \delta_{r, r'}$ identically while transforming the inter-block overlap sign counts of `3x3x4_tensor.mpl` from mixed signs `(up=5, um=4, wp=2, wm=5)` to **100% sign-pure** `(up=0, um=11, wp=9, wm=0)`.

Consequently, all $11$ disjoint $v$-buds of `5x5x7_m127_ZT.json` (`perm=3` to `7x5x5`) reduce cleanly inside `ZT = {-1, 0, 1}`, lowering the rank from `1,905` to $1,905 - 11 = 1,894$ (`object/14x15x15_m1894_ZT.json`) and beating both the live `ZT` record (`1,905`, `-11`) and the live `Z` record (`1,895`, `-1`).
