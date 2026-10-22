# Null Model & Negative Control Audit — `fmm-additive-complexity-records`

controls: 400
best_control: 262
real: 157
median: 281.0
iqr: 9.0
command: /opt/homebrew/bin/python3 -B claim/verify.py
real_beats_all_controls: yes

## 1. 400 Random-Order Disjoint-Pair Greedy CSE Null Controls on `2x4x7` ($m = 45, \text{cn} = 345$)

To verify that the reduced addition counts achieved by `claim/clss_cl1_tellegen_reducer.cpp` come from genuine multi-row target closure ($\text{Cl}_1$) and Tellegen transposition duality on $W^T$ rather than random column ordering, `claim/verify.py` evaluates `400` independent random-order disjoint-pair greedy CSE reductions (`seed = 20261022`) on the exact same `2x4x7` ($m = 45, \text{cn} = 345$) matrices $(U, V, W^T)$:

| Method | Reduced Additions `cr` on `2x4x7` ($m = 45$) | Delta vs Live Champion (`168`) | Delta vs Null `best_control` (`262`) | Status |
| :--- | :---: | :---: | :---: | :---: |
| **400 Random Greedy CSE Controls (`seed = 20261022`)** | `median = 281.0`, `IQR = 9.0`, `best_control = 262` | `+94` | `0` | `0 / 400` beat live `168` or our `157` |
| **Live `addition_reduced_ZT` Champion (`2x4x7_m45_cr168_cn308`)** | `168` (`32, 65, 71`) | `0` | `-94` | Baseline |
| **Our Secondary Tensor (`2x4x7_m45_cr164_cn285`)** | **`164`** (`27, 64, 73`) | **`-4`** | **`-98`** | **PASS** |
| **Our Primary Tensor (`2x4x7_m45_cr157_cn345`)** | **`157`** (`26, 58, 73`) | **`-11`** (`-6.55%`) | **`-105`** | **PASS** |

## 2. Corrupted-Gate & Tellegen-Ablation Negative Controls

1. **Corrupted-Gate Symbolic Rejection Control:**
   - Flipping a single sign (`u_fresh[0][0]["value"] *= -1`) in `claim/schemes/2x4x7_m45_cr157_cn345_ZT_reduced.json` causes `verify_symbolic_product_over_Z` in `claim/verify.py` to immediately reject the scheme (`AssertionError`).
2. **Tellegen Transposition Ablation Control on $W^T$:**
   - Ablating Tellegen transposition on $W^T$ (forcing direct synthesis on $W^T$ instead of synthesizing $W$ and transposing via $\text{cr}(W^T) = \text{cr}(W) + \text{nz\_rows}(W) - \text{nz\_cols}(W)$) strictly degrades $c_w$ across `7 / 9` exact-SOTA winning formats (e.g. `2x4x7` $c_w$ degrades from `73` to `82`, `2x5x5` from `59` to `66`, `5x6x7` from `265` to `286`, and `5x7x7` from `313` to `338`).
