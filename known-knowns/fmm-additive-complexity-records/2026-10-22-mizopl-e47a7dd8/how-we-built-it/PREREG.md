# Pre-Registration — Run `2026-10-22-0110` (`fmm-additive-complexity-records`)

- **Target ID**: `fmm-additive-complexity-records` (`category: algorithms`, `disclosure: open`)
- **Pre-Registered UTC**: `2026-10-22T01:10:00Z`
- null_test: required
- **Primary Status Sources**:
  - `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` (`343,774` bytes, `sha256: 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae`)
  - `https://github.com/dronperminov/FastMatrixMultiplication/tree/master/schemes/results/addition_reduced_ZT` (commit `048b64987b`, `data/reduced_known.json` `sha256: ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d`)
  - `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` (`94,842` bytes, `sha256: c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`)

## Pre-Registered Hypotheses & Multi-Tier Attack Plan (`CONFIRMED_SOLUTION` + `p3`)

1. **Lens 1 (`lens1_cl1_tellegen_reducer` — Matroid-Optimal Distance-1 Target Closure $\text{Cl}_1$ + Tellegen Transposition on $W^T$ + Exact Residual-Reduction Lookahead):**
   - Build a C++17 straight-line program synthesizer (`claim/clss_cl1_tellegen_reducer.cpp`) that pre-loads all distinct target vectors into the dictionary, cascades Distance-1 target closures ($t_p = \pm t_q \pm e_j$ and $t_p = \pm d_a \pm d_b$), scores candidate stepping-stone intermediates by exact residual $L_1$ reduction $\sum_t (\|r(t)\|_1 - \|r'(t)\|_1)$, and applies Tellegen's transposition theorem ($\text{cr}(W^T) = \text{cr}(W) + \text{nz\_rows}(W) - \text{nz\_cols}(W)$) on the $m \times (n_1 n_3)$ transpose $W$.
2. **Lens 2 (`lens2_cross_pool_tensor_mining` — Cross-Pool Tensor Mining across `naive_addition_reduced_ZT`, `ZT`, and `serendipitous_base` + Symbolic Verification over $\mathbb{Z}$):**
   - Apply our $\text{Cl}_1$ + Tellegen reducer across all rank-equal ternary tensors in Perminov's `addition_reduced_ZT`, `naive_addition_reduced_ZT`, `ZT`, and `serendipitous_base` directories for $\max(n, m, p) \le 8$, export valid ternary SLP `.json` files with strictly unit coefficients in $\{-1, +1\}$, and verify exact symbolic polynomial equality $C = A \cdot B$ over $\mathbb{Z}[A, B]$ to beat the live minimum `cr` on at least 3 distinct exact-SOTA formats (`CONFIRMED_SOLUTION` + `p3`).

## Null Control Protocol
- Evaluate **400 deterministic random-order disjoint-pair greedy CSE controls** (`seed = 20261022`) on the `2x4x7` ($m = 45, \text{cn} = 345$) tensor in `claim/verify.py`, recording `real` (`cr = 157`), `best_control` (`262`), `median` (`281.0`), and `IQR` (`9.0`), plus corrupted-gate negative control rejection over $\mathbb{Z}[A, B]$.
