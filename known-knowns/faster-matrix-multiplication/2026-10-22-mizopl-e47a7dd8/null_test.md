# Null Model & Negative Control Audit — `fmm-additive-complexity-records`

controls: 400
best_control: 304
real: 167
median: 336
iqr: 13
command: sh verify-it-yourself/run_checks.sh
real_beats_all_controls: yes

## 1. 400 Random-Order Disjoint-Pair Greedy CSE Null Controls on `3x3x7` ($m = 49, \text{cn} = 404$)

To verify that the reduced addition counts achieved by `how-we-built-it/clss_cl1_tellegen_reducer.cpp` on the 4 submitted programs (`3x3x7` $m=49$ `cr=167`, `3x5x6` $m=68$ `cr=245`, `3x5x7` $m=79$ `cr=294`, `5x6x6` $m=130$ `cr=492`) come from genuine multi-row target closure ($\text{Cl}_1$) and Tellegen transposition duality on $W^T$ rather than random column ordering, `verify-it-yourself/verify.py` evaluates `400` independent random-order disjoint-pair greedy CSE reductions (`seed = 20261022`) on the exact same `3x3x7` ($m = 49, \text{cn} = 404$) matrices $(U, V, W^T)$ expanded from our submitted file `object/schemes/3x3x7_m49_cr167_cn404_ZT_reduced.json`:

| Method | Reduced Additions `cr` on `3x3x7` ($m = 49$) | Delta vs Null `best_control` (`304`) | Status |
| :--- | :---: | :---: | :---: |
| **400 Random Greedy CSE Controls (`seed = 20261022`)** | `median = 336`, `IQR = 13`, `best_control = 304` | `0` | `0 / 400` reach `167` |
| **Our Ternary SLP (`object/schemes/3x3x7_m49_cr167_cn404_ZT_reduced.json`)** | **`167`** (`33, 53, 81`) | **`-137`** | **PASS** |

## 2. Corrupted-Gate & Tellegen-Ablation Negative Controls

1. **Corrupted-Gate Symbolic Rejection Control:**
   - Flipping a single sign (`u_fresh[0][0]["value"] *= -1`) in `object/schemes/3x3x7_m49_cr167_cn404_ZT_reduced.json` causes `verify_symbolic_product_over_Z` in `verify-it-yourself/verify.py` to immediately reject the scheme (`AssertionError`).
2. **Tellegen Transposition Ablation Control on $W^T$:**
   - Ablating Tellegen transposition on $W^T$ on `5x6x6` ($m = 130$, synthesized from `schemes/results/naive_addition_reduced_ZT/5x6x6_m130_c1697_ZT.json`) strictly degrades $c_w$ compared to synthesizing the $130 \times 30$ matrix $W$ and transposing via $\text{cr}(W^T) = \text{cr}(W) + \text{nz\_rows}(W) - \text{nz\_cols}(W)$ (`cw = 225`, `cr = 492`).
