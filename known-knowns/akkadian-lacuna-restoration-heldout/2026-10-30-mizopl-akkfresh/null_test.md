# Null Model & Negative Control Audit — `akkadian-lacuna-restoration-heldout`

controls: 400
best_control: 0.21918
real: 0.91421
median: 0.21496
iqr: 0.00189
command: sh verify-it-yourself/run_checks.sh
real_beats_all_controls: yes

## 1. 400 Empirical Label-Permutation Null Controls (`N = 38,151` Masked Positions, `seed = 0`)

To verify that our evaluation pipeline and scoring code have zero label leakage or tautological scoring artifacts, `verify-it-yourself/check_akkadian_package.py` (`np.random.default_rng(0)`) evaluates `400` independent random permutations of the `N = 38,151` ground-truth target labels (`label_id`) against the shipped `CLSS-Akk-v3` top-5 predictions (`object/akkadian_predictions_part1..6.csv`):

| Metric | `CLSS-Akk-v3` (Real) | `MBERT+Akk` Baseline (Real) | 400-Permutation Null Mean ± SD | 400-Permutation Null Median (IQR) | 400-Permutation Null Max (`best_control`) | Z-Score vs Null |
|---|---:|---:|---:|---:|---:|---:|
| **`Hit@5`** | **`0.91421`** (`34,878`) | `0.88158` (`33,633`) | `0.21494 ± 0.00155` | `0.21496` (`0.00189`) | **`0.21918`** | **`+450.6 sigma`** (`0 / 400` pass) |
| **`MRR` / `MRR@5`** | **`0.84897` (`0.84345`)** | `0.83160` (`0.82413`) | `0.13531 ± 0.00110` | `0.13533` (`0.00142`) | **`0.13845`** | **`+641.4 sigma`** (`0 / 400` pass) |
| **`Hit@1`** | **`0.79395`** (`30,290`) | `0.78732` (`30,037`) | `0.08375 ± 0.00114` | `0.08388` (`0.00160`) | **`0.08655`** | **`+625.7 sigma`** (`0 / 400` pass) |

## 2. Unigram Frequency Baseline Control (`9,221` Composition-Disjoint Training Docs)

Always predicting the 5 most frequent word-piece tokens in the `9,221`-document clean training split (`['-', 'a', 'u', 'i', 'ša']`) achieves `Hit@1 = 0.21184`, `Hit@5 = 0.35103`, and `MRR@5 = 0.26419`, failing the claim criteria by more than `56` percentage points.
