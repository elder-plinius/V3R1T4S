# `akkadian-lacuna-restoration-heldout` — Boundary-Deduplicated Slot-Syntax, Parallel-Passage, & Belief-Propagation Restoration (`CLSS-Akk-v3`) on Held-Out Oracc Cuneiform Texts (`2026-10-21-mizopl-5aa962ff`)

## What

On the released SLAB-NLP/Akk ORACC dataset (commit dfd2a66d4305cf36981e4fd3fde823a5020161dd, 80/20 document split at SEED=2 with 18,568 training rows and 1,875 strictly zero-overlap held-out test documents in claim/bert_test_strict_1875.txt, sha256 65e7fe8a338048e3a373f0061bbf435154e4e2a49845513c8074abd48fa9fd4c) under the repository's 15% random masking protocol at torch.manual_seed(42) (N = 27,650 frozen masked positions in claim/frozen_masked_positions.json, sha256 4abcfdb61d6a391d07b024136ace51d4dc4e3378a7ad2b89b6b12e1de75216c1, and claim/frozen_test_tensors_seed42.npz, sha256 8033d870bd9d8787627690fc26771693a6acc112be17c7d94f204ed4a9654ec4), the reproduced MBERT+Akk baseline trained strictly on the training split (claim/mbert_akk_baseline_top5_predictions.csv, sha256 e0dbc99d781c410800484a693143fe1bfc027631e4714cf498d59845bfcb9e48) achieves Hit@5 = 0.87700 (24,249/27,650) on all positions and Hit@5 = 0.87152 (22,622/25,957) on the non-missing sign subset (both inside the required [0.87, 0.91] calibration window) with MRR = 0.82369 (MRR@5 = 0.81617) and Hit@1 = 0.77693, while the hybrid slot-syntax, parallel-passage, and two-pass belief-propagation model CLSS-Akk-v3 indexed solely on the training split (claim/clss_akk_engine_v3.c, sha256 af810ea742cfb86033065e2875781354670f4cb6fe15a531bc3e5821856d7041; claim/clss_akk_top5_predictions.csv, sha256 4d974bb65acd8993a726065a4626cee8d96f0ea1bd01539e49c3dac1dac7ad9d) achieves Hit@5 = 0.92156 (25,481/27,650, +0.03156 over the paper's 0.89, +0.02656 over 0.895, and +0.04456 over MBERT+Akk), MRR = 0.85593 (MRR@5 = 0.85071, +0.02593 over the paper's 0.83 and +0.03224 over MBERT+Akk), Hit@1 = 0.80098 (22,147/27,650), and Hit@10 = 0.94517 (26,134/27,650) with a 10,000/10,000 (100.00%, p = 0.0001) paired bootstrap win rate, simultaneously beating both the paper and the reproduced baseline on the 25,957 non-missing subset (Hit@5 = 0.91983, MRR = 0.85981), on the 21,459 single-token whole-word subset (Hit@5 = 0.91617, MRR = 0.85708), under 100% [MASK] replacement (claim/clss_akk_100mask_top5_predictions.csv, Hit@5 = 0.92007, MRR = 0.84737), with the zero-neural-parameter symbolic engine CLSS-C-v3 on Hit@5 (claim/clss_c_v3_pure_top5_predictions.csv, Hit@5 = 0.89638, MRR = 0.82480), and across the Table 2 genre subsets Lexical (MRR = 0.86091 vs 0.69, Hit@5 = 0.92920 vs 0.85), Astrological Report (MRR = 0.86704 vs 0.81, Hit@5 = 0.92527 vs 0.88), and Royal or Monumental (MRR = 0.90375 vs 0.84, Hit@5 = 0.93785 vs 0.90), thereby satisfying the full success criterion and subsuming partial win p1.

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `< 1` second on CPU (`python3` + `numpy`).

## Compared To

- **Target ID**: `akkadian-lacuna-restoration-heldout` (`category: ancient-texts`)
- **Primary Benchmark Sources**:
  - `https://github.com/SLAB-NLP/Akk` (commit `dfd2a66d4305cf36981e4fd3fde823a5020161dd`, `data/akk_from_jsons.jsonl`, `sha256: b970895b8be1ff6dfe8b569110b311d9d6f3b213e60d1a61e6b963da783623a3`)
  - Koren Lazar, Benny Saret, Asaf Yehudai, Wayne Horowitz, Nathan Wasserman, and Gabriel Stanovsky, *Filling the Gaps in Ancient Akkadian Texts: A Masked Language Modelling Approach*, EMNLP 2021 (`https://aclanthology.org/2021.emnlp-main.384.pdf`, `sha256: 68a75ea83a5654f642a0b2cd610cf296b0612c2f84eead2649d538b3f13f427e`).

| Evaluation Regime / Subset | Positions ($N$) | Model | `MRR` | `MRR@5` | `Hit@1` | `Hit@5` | `Hit@10` |
|---|---:|---|---:|---:|---:|---:|---:|
| Published Paper (Lazar et al. 2021) | ~20% split | `MBERT+Akk` (Paper) | `0.83000` | — | — | `0.89000` (`0.895`) | `0.92000` |
| All Frozen Positions (`COLLATOR_80_10_10`) | `27,650` | `MBERT+Akk` Baseline | `0.82369` | `0.81617` | `0.77693` (`21,482`) | `0.87700` (`24,249`) | `0.90901` (`25,134`) |
| All Frozen Positions (`COLLATOR_80_10_10`) | `27,650` | `CLSS-C-v3` Pure (`0` Neural) | `0.82480` | `0.81807` | `0.76470` (`21,144`) | **`0.89638`** (`24,785`) | **`0.92705`** (`25,633`) |
| All Frozen Positions (`100%_MASK`) | `27,650` | `CLSS-Akk-v3` (`100%_MASK`) | **`0.84737`** | **`0.84205`** | `0.78684` (`21,756`) | **`0.92007`** (`25,440`) | **`0.94409`** (`26,104`) |
| All Frozen Positions (`COLLATOR_80_10_10`) | `27,650` | **`CLSS-Akk-v3` Full** | **`0.85593`** | **`0.85071`** | **`0.80098`** (`22,147`) | **`0.92156`** (`25,481`) | **`0.94517`** (`26,134`) |
| Non-Missing Subset (`label not in {4,5}`) | `25,957` | `MBERT+Akk` Baseline | `0.82008` | `0.81221` | `0.77451` (`20,104`) | `0.87152` (`22,622`) | `0.90488` (`23,488`) |
| Non-Missing Subset (`label not in {4,5}`) | `25,957` | **`CLSS-Akk-v3` Full** | **`0.85981`** | **`0.85453`** | **`0.80899`** (`20,999`) | **`0.91983`** (`23,876`) | **`0.94387`** (`24,500`) |
| Single-Token Whole Words (non-missing) | `21,459` | **`CLSS-Akk-v3` Full** | **`0.85708`** | **`0.85165`** | **`0.80670`** (`17,311`) | **`0.91617`** (`19,660`) | **`0.94058`** (`20,184`) |

## Not Claimed

- We do not claim partial win `p2` (eBL natural-lacuna holdout on `joins == []` fragments).

## Credits

- **Dataset & Baseline Code**: Koren Lazar, Benny Saret, Asaf Yehudai, Wayne Horowitz, Nathan Wasserman, and Gabriel Stanovsky (`SLAB-NLP/Akk`, Oracc Open Richly Annotated Cuneiform Corpus).
- **Contributor**: `mizopl`.
