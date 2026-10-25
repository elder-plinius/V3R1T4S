# Null Model & Negative Control Audit — `akkadian-lacuna-restoration-heldout`

controls: 400
best_control: 0.25378
real: 0.92156
median: 0.24846
iqr: 0.00260
command: sh verify-it-yourself/run_checks.sh
real_beats_all_controls: yes

## 1. 400 Empirical Label-Permutation Null Controls (`N = 27,650` Masked Positions, `seed = 0`)

To verify that our evaluation pipeline and scoring code have zero label leakage or tautological scoring artifacts, `verify-it-yourself/check_akkadian_package.py` (`np.random.default_rng(0)`) evaluates `400` independent random permutations of the `N = 27,650` ground-truth target labels (`label_id`) against the shipped `CLSS-Akk-v3` top-5 predictions (`object/akkadian_predictions_part1..4.csv`):

| Metric | `CLSS-Akk-v3` (Real) | `MBERT+Akk` Baseline (Real) | 400-Permutation Null Mean ± SD | 400-Permutation Null Median (IQR) | 400-Permutation Null Max (`best_control`) | Z-Score vs Null |
|---|---:|---:|---:|---:|---:|---:|
| **`Hit@5`** | **`0.92156`** | `0.87700` | `0.24852 ± 0.00178` | `0.24846` (`0.00260`) | **`0.25378`** | **`+378.1 sigma`** (`0 / 400` pass) |
| **`MRR` / `MRR@5`** | **`0.85593` (`0.85071`)** | `0.82369` (`0.81617`) | `0.14616 ± 0.00130` | `0.14617` (`0.00169`) | **`0.15072`** | **`+541.9 sigma`** (`0 / 400` pass) |
| **`Hit@1`** | **`0.80098`** | `0.77693` | `0.08205 ± 0.00141` | `0.08206` (`0.00181`) | **`0.08651`** | **`+509.9 sigma`** (`0 / 400` pass) |

*(Reconciliation note on earlier null-control figures: an earlier draft of `null_test.md` reported `best_control = 0.06043` for `Hit@5` and `0.03892` for `MRR` from uniform random sampling over the `1,875`-sign vocabulary rather than permuting the empirical `label_id` vector, while `RECEIPTS.md` reported `0.25606` from `author_checker_akkadian.py` where `1,000` bootstrap draws preceded the `400` permutations on the same `default_rng(0)` stream. Using a dedicated `np.random.default_rng(0)` directly on the shipped `object/akkadian_predictions_part1..4.csv` gives `best_control = 0.25378` for `Hit@5` and `0.15072` for `MRR@5` across all files.)*

## 2. Unigram Frequency & Shuffled-Context Negative Controls

1. **Global Unigram Frequency Baseline (Trained on `18,568` Training Docs):**
   - Always predicting the top-5 most frequent tokens in the training split (`['-', '.', '\U0001F607', 'a', 'u']`) achieves `Hit@1 = 0.20644`, `Hit@5 = 0.44658`, `MRR = 0.32166` (`MRR@5 = 0.30707`), and excluding punctuation/missing-sign tokens (`a`, `u`, `i`, `na`, `ša`) achieves `Hit@1 = 0.06412`, `Hit@5 = 0.14839`, `MRR = 0.08826`.
2. **Context-Scrambled C Engine Control:**
   - Cyclic-shifting test context positions by `+7` tokens before querying `CLSS-C-v3` collapses `Hit@5` from `0.89638` to `0.15114` and `MRR` from `0.82480` to `0.09104`.
