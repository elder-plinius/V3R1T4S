# How We Found It: Sign-Pure Sub-Block Conjugation on Composite FMM Tensors

*(contributor text, unverified)*

## 1. Upstream Ingredient Schemes (`dronperminov/FastMatrixMultiplication`)

The construction uses three public ingredient schemes from A. Perminov's `FastMatrixMultiplication` repository (referenced by upstream URL and SHA-256 rather than vendored in the package):

1. **`3x4x7_m64_ZT.json`** (rank `64` in `ZT`, permuted to `7x3x4`):
   - **URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/ZT/3x4x7_m64_ZT.json`
   - **Bytes / SHA-256:** `19,411` bytes, `sha256: 229e7c5b145c27fe62565912cf68b28036a39a8f969868560344b16df696bacd`
2. **`2x3x3_tensor.mpl`** (`2x3x3`, rank `15` in `ZT`):
   - **URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/known/tensor/2x3x3_tensor.mpl`
   - **Bytes / SHA-256:** `2,235` bytes, `sha256: c98747b97b6a386978770e627bc3e0482dc8cabea9cad47f5963ca40f7330d5d`
3. **`3x3x4_tensor.mpl`** (`3x3x4`, rank `29` in `ZT`, permuted to `4x3x3`):
   - **URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/known/tensor/3x3x4_tensor.mpl`
   - **Bytes / SHA-256:** `4,806` bytes, `sha256: 597a7fafb994ee15ea3472ab9c03b5823c34767f5bc376ab738965229684eabb`

## 2. The Seam Obstacle in Serendipitous Tensor Products

In Perminov's `SerendipitousProductBuilder` (arXiv:2603.18699), a composite format such as `14 x 9 x 12` (`9x12x14`) can be factored as the Kronecker product of $s_1 = (7, 3, 4)$ (`3x4x7_m64_ZT.json`, rank $64$ in `ZT`) and $s_2 = (2, 3, 3)$ (`2x3x3_tensor.mpl`, rank $15$ in `ZT`), giving base rank $64 \times 15 = 960$. Whenever $s_1$ contains a disjoint pair of rank-1 terms $(f_0, f_1)$ with $V^{(1)}_{f_0} = \pm V^{(1)}_{f_1}$ (a "$v$-bud"), the direct sum of two copies of $s_2$ ($2 \times 15 = 30$ multiplications) can be replaced by a single copy of $s_3 = (4, 3, 3)$ (`3x3x4_tensor.mpl`, rank $29$ in `ZT`), saving $1$ multiplication per bud pair.

However, whenever $U^{(1)}_{f_0}$ and $U^{(1)}_{f_1}$ (or $W^{(1)}_{f_0}$ and $W^{(1)}_{f_1}$) have overlapping non-zero positions, combining them with $s_3$ sums row $r_2 \in \{0, 1\}$ and row $r_2 + 2 \in \{2, 3\}$ of $U^{(3)}$ (and columns $c_2, c_2 + 2$ of $W^{(3)}$). In the standard row/column ordering $(0, 1, 2, 3)$ of `3x3x4_tensor.mpl`, the overlapping non-zeros between sub-block $\{0, 1\}$ and sub-block $\{2, 3\}$ have mixed relative signs (`5` positive and `4` negative in $U^{(3)}$; `2` positive and `5` negative in $W^{(3)}$), so every choice of relative sign produces entries in $\{\pm 2\}$ (`Z` instead of `ZT`).

## 3. Sign-Pure Sub-Block Conjugation

Because the matrix multiplication tensor $T_{(4, 3, 3)}$ has the Kronecker delta $\delta_{r, r'}$ across $r, r' \in \{0, 1, 2, 3\}$, applying any permutation $\pi \in S_4$ simultaneously to the 4 rows of $U^{(3)}$ and the 4 columns of $W^{(3)}$ preserves $\delta_{\pi(r), \pi(r')} = \delta_{r, r'}$ identically without altering $V^{(3)}$. In particular, conjugating the second `<2, 3, 3>` sub-block $\{2, 3\}$ by the transposition $\pi = (0, 1, 3, 2)$ leaves the target tensor 100% invariant while transforming the inter-block overlap sign counts of `3x3x4_tensor.mpl` from `(up=5, um=4, wp=2, wm=5)` to `(up=0, um=11, wp=9, wm=0)` — i.e., **100% sign-pure** in both $U^{(3)}$ and $W^{(3)}$.

Consequently, every single-overlap $v$-bud in $s_1 = (7, 3, 4)$ cancels all potential $\pm 2$ entries by a uniform sign choice `scales = [1, +-1]`, allowing all $6$ disjoint $v$-buds of `3x4x7_m64_ZT.json` (`perm=3`) to be reduced inside `ZT = {-1, 0, 1}` and yielding `object/9x12x14_m954_ZT.json` of rank $960 - 6 = 954$.
