# How We Found It: Higher-Order $S_{b \cdot g}$ Sub-Block Conjugation on Serendipitous Tensor Products

*(contributor text, unverified)*

## 1. Diagnosing Why `ZT > Z` Gaps Persisted in Serendipitous Tensor Products

Following the upstream merge of our first four ternary schemes (`9x12x14:954`, `10x15x15:1389`, `12x15x15:1640`, `14x15x15:1894`) into `dronperminov/FastMatrixMultiplication` (commit `b4f756b`, `schemes/known/mizopl/`), we audited the remaining formats in `dronperminov/FastMatrixMultiplication/master/README.md` where the ternary (`ZT`) rank exceeded the integer (`Z`) rank (`ZT > Z`):
- `6x12x14`: `ZT = 666`, `Z = 654` (gap `12`)
- `9x10x13`: `ZT = 771`, `Z = 763` (gap `8`)
- `9x10x16`: `ZT = 924`, `Z = 920` (gap `4`)
- `10x15x16`: `ZT = 1,488`, `Z = 1,484` (gap `4`)
- `11x15x16`: `ZT = 1,641` (`1,632` in `status.json`), `Z = 1,629` (gap `12` / `3`)
- `12x13x16`: `ZT = 1,548`, `Z = 1,544` (gap `4`)

In our earlier PRs (#402 and #432), we had discovered that for $g=2$ bud pairs where the multiplier scheme $s_2$ had dimension $b=2$ along the bud axis (`s3` of dimension $b \cdot g = 4$), permuting the $4$ sub-block coordinates of $s_3$ by $\pi = (0, 1, 3, 2) \in S_4$ aligned the zero structure of $s_3$ with the bud vectors of $s_1 \otimes s_2$.

However, when we tested simple $S_g$ group-order permutations on `6x12x14`, `9x10x13`, `9x10x16`, `11x15x16`, and `12x13x16`, two deeper structural barriers emerged:
1. **The Hidden Serendipitous Base Directory (`schemes/results/serendipitous_base/`):** Standard `schemes/results/ZT/` files for small formats optimize rank or additive complexity rather than bud count. Perminov's repository stores specialized high-bud base schemes in `schemes/results/serendipitous_base/` (`2x3x7_m35_07bf0c95_ZT.json`, `2x3x13_m65_0c34eb32_ZT.json`, `2x3x8_m40_0040c82e_ZT.json`, `2x3x11_m55_014e74df_ZT.json`, and `2x4x13_m84_0037b2c7_ZT.json`).
2. **Higher-Order Clique Sizes ($g \in \{2, 3, 4, 5\}$) and Multiplier Dimensions ($b \in \{1, 2, 3\}$):** In `6x12x14`, `9x10x13`, and `9x10x16`, the multiplier scheme $s_2$ has dimension $b = 3$ along the $u$-bud axis, so a clique of $g \in \{2, 3, 4, 5\}$ buds invokes an auxiliary scheme $s_3$ of dimension $b \cdot g \in \{6, 9, 12, 15\}$ (`6x4x2`, `9x4x2`, `12x5x1`, `15x5x1`, `6x5x2`, `9x5x2`). Merely permuting the $g$ outer blocks in $S_g$ or permuting the $b=3$ inner coordinates uniformly across all $g$ blocks leaves $\pm 2$ collisions in `6x12x14`, `9x10x13`, and `9x10x16` (`L-FTIR-002` initial test).

## 2. The Full $S_{b \cdot g}$ Sub-Block Conjugation Law (`L-FTIR-002` & `L-FTIR-003`)

We realized that the tensor contraction across a bud clique of size $g$ with multiplier dimension $b$ is invariant under the **entire symmetric group $S_{b \cdot g}$** acting simultaneously on the two incident matrix slices of $s_3$ along its axis of length $b \cdot g$, because
$$\sum_{\ell=0}^{b g - 1} \delta_{i, \pi(\ell)}\,\delta_{\pi(\ell), j} = \delta_{i, j} \quad \forall \pi \in S_{b \cdot g}.$$
Moreover, when the two non-bud axes of $s_3$ have equal dimensions (such as `4x3x4` in `10x15x16`, where $n_1 = n_3 = 4$), transposing $s_3$ across its equal dimensions provides an additional involution that changes which factor carries the dense combinations.

Implementing a fast simulated-annealing / exact permutation search over $\pi \in S_{b \cdot g}$ (plus equal-dimension axis swaps of $s_3$) in `how-we-built-it/build_all_7_schemes.py` immediately resolved every single format:
- **`10x15x16` (`L-FTIR-001` $\to 1$):** Using `s1 = (5, 5, 4)` ($m=76$) $\times$ `s2 = (2, 3, 4)` ($m=20$), transposing `s3 = (4, 3, 4)` ($m=38$) across its equal axes and applying $\pi \in S_4$ converted all `18/18` $v$-bud pairs to `ZT`, lowering `ZT` rank from `1,488` to **`1,484`** (`-4`).
- **`6x12x14`, `9x10x13`, `9x10x16`, and `11x15x16` (`L-FTIR-002` $\to 1$):** Full $S_{b \cdot g}$ conjugation (`S_6`, `S_9`, `S_{12}`, `S_{15}` for `b=3` and `S_3`, `S_5` for `b=1`) eliminated **100% of $\pm 2$ collisions** across all bud cliques (`15/15` in `6x12x14`, `16/16` in `9x10x13`, `16/16` in `9x10x16`, `16/16` in `11x15x16`), closing all four `ZT > Z` gaps to `0` (`666 -> 654`, `771 -> 763`, `924 -> 920`, `1,641 -> 1,629`).
- **`12x13x16` in `Z` (`1,544 -> 1,541`, `-3`) and `ZT` (`1,548 -> 1,546`, `-2`, `L-FTIR-003` $\to 1$):** Scanning all 11 serendipitous base schemes for `2x4x13` revealed that `2x4x13_m84_0037b2c7_ZT.json` (transposed to $(2, 13, 4)$, $m=84$) $\times$ `(6, 1, 4)` ($m=24$) has $w$-bud profile $3 \times 1 + 2 \times 2 + 19 \times 3 + 5 \times 4 = 84$, giving an exact integer (`Z`) scheme of rank $3(24) + 2(39) + 19(54) + 5(73) = 1,541$, beating the live `Z = 1,544` record by `3` multiplications! Under $S_3$ and $S_4$ conjugation, `25/26` bud groups become strictly ternary (`ZT`); splitting the single obstructed 4-tuple `Group 24 = [38, 57, 63, 64]` into two disjoint pairs `[38, 63]` and `[57, 64]` separates the mixed-sign pair `(63, 64)` at cost $2 \times 39 - 73 = +5$, producing `12x13x16_m1546_ZT.json` (`ZT: 1,548 -> 1,546`, `-2`).
