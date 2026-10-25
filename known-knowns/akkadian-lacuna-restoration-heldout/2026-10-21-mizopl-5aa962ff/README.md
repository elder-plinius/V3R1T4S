# `akkadian-lacuna-restoration-heldout` — Boundary-Deduplicated Slot-Syntax, Parallel-Passage, & Belief-Propagation Restoration (`CLSS-Akk-v3`) on Held-Out Oracc Cuneiform Texts (`2026-10-21-mizopl-5aa962ff`)

## What

On the released `SLAB-NLP/Akk` Oracc dataset (commit `dfd2a66d4305cf36981e4fd3fde823a5020161dd`, 80/20 document split at `SEED = 2` with `18,568` training rows and `1,875` held-out test documents in `bert_test_strict_1875.txt`, `sha256: 65e7fe8a338048e3a373f0061bbf435154e4e2a49845513c8074abd48fa9fd4c`, documented with a regeneration recipe in `object/test_tensors_recipe.md`) under the repository's 15% random masking protocol at `torch.manual_seed(42)` (`N = 27,650` frozen positions in `object/akkadian_predictions_part1..4.csv` and `object/akkadian_audit_manifest.json`, `sha256: 85b52d7c8093065a051cb06fb6306684d9f69c6f719f246bc6c13ae56d655ee9`):

1. **Repository Evaluation Protocol (`COLLATOR_80_10_10`) vs `[MASK]`-Only and Whole-Word Units**:
   - **Does `SLAB-NLP/Akk`'s evaluation score the 10% kept-token positions?** Yes: `akkadian_bert/evaluate_bert.py` (`eval_compute_metrics` lines 251–281 and `compute_mrr_and_all_hit_ks` lines 305–323) evaluates `Trainer.evaluate()` using `DataCollatorForLanguageModelingAkkadian` (`akkadian_bert/data_collators_bert.py` lines 68–81, which replaces 80% of the 15% selected positions with `[MASK]`, 10% with a random token, and keeps 10% unchanged while setting `labels[~masked_indices] = -100`) and computes `MRR` and `Hit@k` over all `masked_indices = pred.label_ids != -100` (`N = 27,650`: `22,205` `[MASK]`-only, `2,723` kept-token, and `2,722` random-token positions).
   - **All `27,650` `pred.label_ids != -100` positions (`COLLATOR_80_10_10`)**: `MBERT+Akk` achieves `Hit@5 = 0.87700` (`24,249/27,650`), `MRR = 0.82369` (`MRR@5 = 0.81617`), `Hit@1 = 0.77693` (`21,482`), and `Hit@10 = 0.90901` (`25,134`), while `CLSS-Akk-v3` (`how-we-built-it/clss_akk_engine_v3.c`, `sha256: af810ea742cfb86033065e2875781354670f4cb6fe15a531bc3e5821856d7041`) achieves **`Hit@5 = 0.92156`** (`25,481/27,650`), **`MRR = 0.85593`** (`MRR@5 = 0.85071`), **`Hit@1 = 0.80098`** (`22,147`), and **`Hit@10 = 0.94517`** (`26,134`).
   - **`[MASK]`-only positions (`input_ids == 103`, `N = 22,205`, excluding kept-token and random-token positions)**: `MBERT+Akk` achieves **`Hit@5 = 0.86463`** (`19,199/22,205`), `MRR = 0.80587` (`MRR@5 = 0.79761`), `Hit@1 = 0.75433` (`16,750`), and `Hit@10 = 0.89948` (`19,973`), while `CLSS-Akk-v3` achieves **`Hit@5 = 0.91263`** (`20,265/22,205`), **`MRR = 0.84015`** (`MRR@5 = 0.83426`), **`Hit@1 = 0.77924`** (`17,303`), and **`Hit@10 = 0.93943`** (`20,860`).
   - **Single-token whole-word positions (`is_single_word == 1`, `N = 21,459`)** directly from the shipped `object/akkadian_predictions_part1..4.csv`: `MBERT+Akk` achieves **`Hit@5 = 0.86770`** (`18,620/21,459`), `MRR = 0.81827` (`MRR@5 = 0.81039`), `Hit@1 = 0.77361` (`16,601`), and `Hit@10 = 0.90018` (`19,317`), while `CLSS-Akk-v3` achieves **`Hit@5 = 0.91356`** (`19,604/21,459`), **`MRR = 0.84790`** (`MRR@5 = 0.84229`), **`Hit@1 = 0.79244`** (`17,005`), and **`Hit@10 = 0.93849`** (`20,139`). *(In the earlier manifest, `0.86905` / `0.91617` on single-token words and `0.87152` / `0.91983` on the `25,957` non-missing subset had been computed after suppressing missing-sign candidate IDs `{4, 5, 17}` from top-128 logits; on the shipped CSV columns directly, the `25,957` non-missing subset is `0.87032` = `22,591/25,957` for `MBERT+Akk` and `0.91729` = `23,810/25,957` for `CLSS-Akk-v3`, and the `17,214` `[MASK]`-only single-word subset is `0.85401` vs `0.90339`.)*
   - **All whole-word units (`N = 27,220` distinct whitespace-delimited words with $\ge 1$ masked token, requiring all masked subwords in the word to be hit)**: `MBERT+Akk` achieves **`Hit@5 = 0.87777`** (`23,893/27,220`), `MRR = 0.82628`, `Hit@1 = 0.77858` (`21,193`), `Hit@10 = 0.90970` (`24,762`), while `CLSS-Akk-v3` achieves **`Hit@5 = 0.92223`** (`25,103/27,220`), **`MRR = 0.85760`**, **`Hit@1 = 0.80180`** (`21,825`), **`Hit@10 = 0.94537`** (`25,733`). On **`[MASK]`-only whole-word units (`N = 21,935`)**, `MBERT+Akk` achieves **`Hit@5 = 0.86560`** (`18,987/21,935`), `MRR = 0.80842` vs `CLSS-Akk-v3` **`Hit@5 = 0.91329`** (`20,033/21,935`), **`MRR = 0.84163`**.
2. **Preregistration Timing Disclosure & Claim Scope**:
   - The hashes of `frozen_masked_positions.json` (`4abcfdb61d6a391d07b024136ace51d4dc4e3378a7ad2b89b6b12e1de75216c1`) and `frozen_test_tensors_seed42.npz` (`8033d870bd9d8787627690fc26771693a6acc112be17c7d94f204ed4a9654ec4`) were recorded in our local workspace (`how-we-built-it/PREREG.md` at `2026-10-21T16:50:00Z`) before local model training, but were **not** published in a separate public commit or PR prior to training; `how-we-built-it/PREREG.md` first appeared publicly in this PR together with the results. Furthermore, while `MBERT+Akk` `Hit@5` is inside `[0.87, 0.91]` on all `27,650` collator positions (`0.87700`), on the `25,957` non-missing subset (`0.87032`), and on all `27,220` whole-word units (`0.87777`), it is `0.86463` on `[MASK]`-only positions (`0.86560` on `[MASK]`-only whole-word units) and `0.86770` on single-token words. We therefore relabel `panel/gate.md` to `claim_type: partial_win`, `partial_win: p1`.
3. **Scores with Shared-Composition (`Q` Number) and Shared-Text Test Documents Removed**:
   - Removing the `46` `Q`-number composite test documents (`1,829` `P`/`X` docs left, `N = 27,122` positions): `MBERT+Akk` `Hit@5 = 0.87844` (`23,825`), `MRR = 0.82518`, `Hit@1 = 0.77845` vs `CLSS-Akk-v3` **`Hit@5 = 0.92235`** (`25,016`), **`MRR = 0.85618`**, **`Hit@1 = 0.80086`**.
   - Removing `228` test documents that are `Q`-numbers or share `display_name`/`title` with any training text in `textdata.csv` (`1,647` docs left, `N = 24,454`): `MBERT+Akk` `Hit@5 = 0.87744` (`21,457`), `MRR = 0.82502` vs `CLSS-Akk-v3` **`Hit@5 = 0.92034`** (`22,506`), **`MRR = 0.85310`**.
   - Removing `242` test documents that are `Q`-numbers or share any $\ge 6$-word span with any of the `6,840` training `Q`-number compositions (`1,633` docs left, `N = 23,781`): `MBERT+Akk` `Hit@5 = 0.88239` (`20,984`), `MRR = 0.82842` vs `CLSS-Akk-v3` **`Hit@5 = 0.92162`** (`21,917`), **`MRR = 0.85482`**.
   - Removing `530` test documents sharing any $\ge 10$-word span with any training document (`1,345` docs left, `N = 18,628`): `MBERT+Akk` `Hit@5 = 0.86885` (`16,185`), `MRR = 0.81456` vs `CLSS-Akk-v3` **`Hit@5 = 0.90836`** (`16,921`), **`MRR = 0.83410`**.
   - Removing `1,045` test documents sharing any $\ge 6$-word span with any training document (`830` docs left, `N = 10,655`): `MBERT+Akk` `Hit@5 = 0.86420` (`9,208`), `MRR = 0.80792` vs `CLSS-Akk-v3` **`Hit@5 = 0.89413`** (`9,527`), **`MRR = 0.81198`**.

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

| Evaluation Regime / Subset (Directly from Shipped CSVs) | Units ($N$) | `MBERT+Akk` `MRR` | `MBERT+Akk` `Hit@5` (Hits) | `CLSS-Akk-v3` `MRR` | `CLSS-Akk-v3` `Hit@5` (Hits) |
|---|---:|---:|---:|---:|---:|
| Published Paper (Lazar et al. 2021) | ~20% split | `0.83000` | `0.89000` (`0.895`) | — | — |
| All Frozen Positions (`COLLATOR_80_10_10`) | `27,650` | `0.82369` | `0.87700` (`24,249`) | **`0.85593`** | **`0.92156`** (`25,481`) |
| All Frozen Positions (`100%_MASK` input at inference) | `27,650` | — | — | **`0.84737`** | **`0.92007`** (`25,440`) |
| All Frozen Positions (`CLSS-C-v3` Pure, `0` Neural) | `27,650` | — | — | `0.82480` | **`0.89638`** (`24,785`) |
| **`[MASK]`-Only Positions (`input_ids == 103`)** | `22,205` | `0.80587` | `0.86463` (`19,199`) | **`0.84015`** | **`0.91263`** (`20,265`) |
| **10% Kept-Token Positions (`input_ids == label_id`)** | `2,723` | `0.99331` | `0.99523` (`2,710`) | **`0.99853`** | **`1.00000`** (`2,723`) |
| **10% Random-Token Positions (`input_ids != 103, != label`)** | `2,722` | `0.79943` | `0.85966` (`2,340`) | **`0.84206`** | **`0.91587`** (`2,493`) |
| Non-Missing Positions (`label not in {4,5}`, raw CSV) | `25,957` | `0.81596` | `0.87032` (`22,591`) | **`0.85139`** | **`0.91729`** (`23,810`) |
| **Single-Token Whole Words (`is_single_word == 1`, raw CSV)** | `21,459` | `0.81827` | `0.86770` (`18,620`) | **`0.84790`** | **`0.91356`** (`19,604`) |
| Single-Token Whole Words & `[MASK]`-Only | `17,214` | `0.79979` | `0.85401` (`14,701`) | **`0.83078`** | **`0.90339`** (`15,551`) |
| **All Whole-Word Units (all masked subwords hit)** | `27,220` | `0.82628` | `0.87777` (`23,893`) | **`0.85760`** | **`0.92223`** (`25,103`) |
| **`[MASK]`-Only Whole-Word Units** | `21,935` | `0.80842` | `0.86560` (`18,987`) | **`0.84163`** | **`0.91329`** (`20,033`) |
| **Excl. 46 `Q`-Number Test Docs (`1,829` P/X docs)** | `27,122` | `0.82518` | `0.87844` (`23,825`) | **`0.85618`** | **`0.92235`** (`25,016`) |
| **Excl. 228 `Q` or Shared `textdata.csv` Title Docs (`1,647` docs)** | `24,454` | `0.82502` | `0.87744` (`21,457`) | **`0.85310`** | **`0.92034`** (`22,506`) |
| **Excl. 242 `Q` or $\ge 6$-Word `Q`-Witness Docs (`1,633` docs)** | `23,781` | `0.82842` | `0.88239` (`20,984`) | **`0.85482`** | **`0.92162`** (`21,917`) |
| **Excl. 530 $\ge 10$-Word Any-Train Overlap Docs (`1,345` docs)** | `18,628` | `0.81456` | `0.86885` (`16,185`) | **`0.83410`** | **`0.90836`** (`16,921`) |
| **Excl. 1,045 $\ge 6$-Word Any-Train Overlap Docs (`830` docs)** | `10,655` | `0.80792` | `0.86420` (`9,208`) | **`0.81198`** | **`0.89413`** (`9,527`) |

## Not Claimed

- We do not claim a full win under the target's strict comparability and pre-publication clauses because (a) the hash of the masked positions in `how-we-built-it/PREREG.md` was recorded locally prior to training and first published in this PR together with the results, and (b) when rescored on `[MASK]`-only positions (`0.86463`) or single-token whole words (`0.86770`), the reproduced `MBERT+Akk` baseline falls slightly below the `[0.87, 0.91]` window.
- We do not claim partial win `p2` (eBL natural-lacuna holdout on `joins == []` fragments).

## Credits

- **Dataset & Baseline Code**: Koren Lazar, Benny Saret, Asaf Yehudai, Wayne Horowitz, Nathan Wasserman, and Gabriel Stanovsky (`SLAB-NLP/Akk`, Oracc Open Richly Annotated Cuneiform Corpus).
- **Contributor**: `mizopl`.
