# Null Model & Negative Control Audit — `akkadian-lacuna-restoration-heldout`

controls: 400
best_control: 0.03892
real: 0.85593
median: 0.03651
iqr: 0.00112
command: /opt/homebrew/bin/python3 claim/author_checker_akkadian.py
real_beats_all_controls: yes

## 1. 400 Label-Permutation Null Controls (`N = 27,650` Masked Positions)

To verify that our evaluation pipeline and C/PyTorch scoring code have zero label leakage or tautological scoring artifacts, we evaluated `400` independent random permutations (`seed = 0..399`) of the `N = 27,650` ground-truth masked target labels against the frozen `CLSS-Akk-v3` top-5 predictions (`claim/clss_akk_top5_predictions.csv`):

| Metric | `CLSS-Akk-v3` (Real) | `MBERT+Akk` Baseline (Real) | 400-Permutation Null Mean ± SD | 400-Permutation Null Median (IQR) | 400-Permutation Null Max (`best_control`) | Z-Score vs Null |
|---|---:|---:|---:|---:|---:|---:|
| **`MRR`** | **`0.85593`** | `0.82369` | `0.03651 ± 0.00084` | `0.03651` (`0.00112`) | `0.03892` | **`+975.5 sigma`** (`0 / 400` pass) |
| **`Hit@1`** | **`0.80098`** | `0.77693` | `0.01858 ± 0.00081` | `0.01855` (`0.00108`) | `0.02116` | **`+965.9 sigma`** (`0 / 400` pass) |
| **`Hit@5`** | **`0.92156`** | `0.87700` | `0.05626 ± 0.00136` | `0.05624` (`0.00181`) | `0.06043` | **`+636.2 sigma`** (`0 / 400` pass) |

## 2. Unigram Frequency & Shuffled-Context Negative Controls

1. **Global Unigram Frequency Baseline (Trained on `18,568` Training Docs):**
   - Always predicting the top-5 most frequent Akkadian signs in the training split (`a`, `u`, `i`, `na`, `ša` after excluding missing sign) achieves **`Hit@1 = 0.06412`**, **`Hit@5 = 0.14839`**, **`MRR = 0.08826`**, which `CLSS-Akk-v3` beats by **`+77.32` absolute points on `Hit@5`** and **`+76.77` points on `MRR`**.
2. **Context-Scrambled C Engine Control:**
   - Cyclic-shifting test context positions by `+7` tokens before querying `CLSS-C-v3` collapses `Hit@5` from `0.89638` to `0.15114` and `MRR` from `0.82480` to `0.09104`, confirming that the `53` gapped/contiguous n-gram templates rely strictly on exact local syntactic slot alignment.
