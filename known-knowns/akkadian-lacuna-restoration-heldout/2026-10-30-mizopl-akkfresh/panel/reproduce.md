# Skeptic Panel Report: REPRODUCE (`akkadian-lacuna-restoration-heldout`)

role: REPRODUCE
context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
mandate: "Before reading the author's code, write your own checker from the definition (quote it). Verify every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism."

---

## 1. Quoted Definitions and Evaluation Equations

Before reading `how-we-built-it/stage3_run_clss_and_export.py`, `how-we-built-it/clss_akk_engine_v3.c`, or `how-we-built-it/train_mbert_akk_baseline.py`, we inspected `README.md`, `RUN_IT_YOURSELF.md`, and `object/akkadian_audit_manifest.json` and wrote an independent standalone checker (`verify-it-yourself/check_akkadian_package.py`) directly from the benchmark definitions:

1. **Evaluation Corpus, Pre-Registration, and Composition-Disjoint Protocol (quoted from `README.md`):**
   - Upstream Oracc Akkadian corpus: `data/akk_from_jsons.jsonl` (`21,156,545` bytes, `sha256: b970895b8be1ff6dfe8b569110b311d9d6f3b213e60d1a61e6b963da783623a3`) from `https://github.com/SLAB-NLP/Akk` at commit `dfd2a66d4305cf36981e4fd3fde823a5020161dd`.
   - Split & composition deduplication (`SEED = 20261031`): `23,211` raw records deduplicated by `id_text` to `14,430` unique texts, split 80/20 (`11,544` initial train, `2,886` held-out test), and filtered by removing `2,323` training documents that shared empty/exact `bert_input` (`23`), $\ge 20\%$ of distinct word 8-grams in either direction (`1,704`), or any contiguous $\ge 15$-word block (`596`) with any test document, yielding **`9,221` clean composition-disjoint training documents** (`bert_train_clean.txt`, `sha256: 4905a304a059533aa39e2204cef1bc0c16ba77e4dc9a701d312db09a80cf4f91`) and **`2,886` held-out test documents** (`bert_test_heldout.txt`, `sha256: 2813b573c52285d0ed636b41b6e725df66feeb424966653ebcd862e5f69eef14`).
   - Pre-registered masked positions (`torch.manual_seed(20261031)`): $N = 38,151$ word-piece positions (`30,545` `[MASK]`, `3,833` unchanged, `3,773` random; `frozen_masked_positions.csv` `sha256: 5af36f37415efc204cde20cf4be2259abc9abaea88dc31be9b37b0ba72ca325f`, committed to GitHub in `e26fa2cb33964bfe549770d311120ba1f804d81f` at `2026-10-30T08:24:24Z` before model training).

2. **Ranking Metrics (`Hit@k`, `MRR`, and `MRR@5`):**
   For each masked position $i \in \{1, \dots, N\}$ ($N = 38,151$) with ground-truth target token $y_i$ and strict 1-based rank $r_i$ assigned by the model:
   $$\text{Hit@}k = \frac{1}{N} \sum_{i=1}^{N} \mathbf{1}[r_i \le k], \quad k \in \{1, 5, 10\}$$
   $$\text{MRR} = \frac{1}{N} \sum_{i=1}^{N} \frac{1}{r_i} \mathbf{1}[1 \le r_i \le 100], \qquad \text{MRR@5} = \frac{1}{N} \sum_{i=1}^{N} \frac{1}{r_i} \mathbf{1}[1 \le r_i \le 5]$$

3. **Two-Part Comparability & Superiority Clauses:**
   - **Clause (1):** Reproduced `MBERT+Akk` baseline (`object/akkadian_predictions_part1..6.csv`, frozen in commit `00db937`) must achieve $\text{Hit@5} \in [0.87000, 0.91000]$ ($0.89 \pm 0.02$).
   - **Clause (2):** New system `CLSS-Akk-v3` (`object/akkadian_predictions_part1..6.csv`) must strictly beat both the published paper numbers ($\text{MRR} = 0.83$, $\text{Hit@5} = 0.89 / 0.895$) and the reproduced `MBERT+Akk` baseline on the identical $N = 38,151$ frozen masked positions.

---

## 2. Independent Artifact Integrity & Checksum Verification

Our independent checker verified the exact byte count and SHA-256 digest of every saved artifact in the package (`0.48s` total runtime):

| Artifact Path | Verified Bytes | Verified SHA-256 Digest | Status |
|---|---:|---|---|
| `object/akkadian_audit_manifest.json` | `326,637` | `7e5e592d5c9f056ae11bc04eebe65e1bf1139024642c709f4da6b7a25c3b8097` | Exact Match |
| `object/prereg_split_and_mask_manifest.json` | `190,476` | `06ba9a82589d8eeb31433480b275e4821df574938d1104ea607558cc88104877` | Exact Match |
| `object/baseline_frozen_manifest.json` | `979` | `b30998900a380114736b025b5e1fc333754af49e59eafae456c8cddb358d82c4` | Exact Match |
| `object/test_tensors_recipe.md` | `3,498` | `10e76d818b299317b99422d379cd443ff1825dbdf44d0878485bac07fb82f3bc` | Exact Match |
| `object/akkadian_predictions_part1.csv` | `831,159` | `f6669e1dbd8e383baab4e29bea5b62c8d16b25eee602f0119a76e389858cc905` | Exact Match |
| `object/akkadian_predictions_part2.csv` | `837,389` | `7a4a4d9b62615aa995d283f97bff252eaa997a157c1931f4d36cea3146396cce` | Exact Match |
| `object/akkadian_predictions_part3.csv` | `846,352` | `01fee33f699f9a77efd270f60f361a2b17066cf8e1ad5681bfe958083090999f` | Exact Match |
| `object/akkadian_predictions_part4.csv` | `845,892` | `a9279330136ae3c0243cfa948656098e47ec4b02cee9ccea7c632125b6fa851e` | Exact Match |
| `object/akkadian_predictions_part5.csv` | `848,306` | `397f971cc5135e59e138897de5841ea9cd474f64c0cb670dcbf1c7cac7aef3bf` | Exact Match |
| `object/akkadian_predictions_part6.csv` | `846,334` | `0ae0fe2878b2c10ddd6d8a137164668ae672ba74cb6bfc69edaf633214a44c92` | Exact Match |
| `how-we-built-it/clss_akk_engine_v3.c` | `36,050` | `9d867163e19e757d044a4e25c09e677400e837c5c71facfb21416c879134d3af` | Exact Match |
| `how-we-built-it/build_corpus_bin.py` | `4,420` | `d6da9205c4ffeeb76ee36c9922f9f19390fda5061ae3dcef46ab8924981b17f6` | Exact Match |
| `how-we-built-it/stage1_freeze_split_and_masks.py` | `15,510` | `b72ceeeb4df6cb49e82e94c0160e7751a43b4cb8a4617efd8219485e430001b0` | Exact Match |
| `how-we-built-it/train_mbert_akk_baseline.py` | `7,406` | `ab41d64c456b58d3331cad4ab22ac39d3f2e2aad4354e658c6f17387c94efcb4` | Exact Match |
| `how-we-built-it/continue_mbert_akk_baseline.py` | `7,344` | `3b284fe50a523004b579d7c0a9e20d341a05144025db5d4281beba1ee4d7957c` | Exact Match |
| `how-we-built-it/eval_mbert_baseline_frozen.py` | `8,047` | `c3efa6073f4728fc136f83d5ae9168b15c598a24f3772c9cdb06918c31a789d8` | Exact Match |
| `how-we-built-it/stage3_run_clss_and_export.py` | `33,371` | `23563da416521a34d7e14bbab6220e072eeee17ee081fecf7e06f1a927568d1d` | Exact Match |
| `verify-it-yourself/check_akkadian_package.py` | `11,882` | `0aa6c966138ae7827f23d206b007eea4a504193ae6168fcdefed4a9496c222fe` | Exact Match |

---

## 3. Position Alignment & Partition Verification

- Across `object/akkadian_predictions_part1..6.csv`, all `38,151` rows (`mask_idx = 0..38,150`) have strictly increasing indices and 5 distinct candidate IDs per row across all 4 models (`mb`, `cl`, `m1`, `pc`).
- Using `index_partition_metadata` in `object/akkadian_audit_manifest.json`, our checker verified:
  - `30,545` `[MASK]`-only positions (`shown_input_id == 103`), `3,833` kept-token positions (`shown_input_id == label_id`), and `3,773` random-token replacement positions (`30,545 + 3,833 + 3,773 = 38,151`).
  - `10,191` single-token whole-word positions (`is_single_word == 1`), `34,958` distinct whole-word units (`38,151 - 3,193` multi-token word continuations), and `28,447` `[MASK]`-only whole-word units.
  - All 6 cross-split composition / union-`D8` / `Q`-number document filters (`38,097` positions excluding union `D8 >= 0.5`; `36,092` excluding union `D8 >= 0.2`; `31,439` excluding `627` `Q`-number test docs; `28,543` excluding `864` `Q` or shared-`textdata.csv`-title docs; `21,506` excluding `1,316` `Q` or $\ge 6$-word `Q`-witness docs; `25,935` excluding `794` $\ge 10$-word train-overlap docs).

---

## 4. Independent Metric Re-Derivation Across All Regimes, Subsets, and Genres

### 4.1 Overall Held-Out Benchmark ($N = 38,151$ Frozen Positions) and Core Subsets

| Regime / Subset | $N$ | `MBERT+Akk` `MRR` | `MBERT+Akk` `Hit@5` (Hits) | `CLSS-Akk-v3` `MRR` | `CLSS-Akk-v3` `Hit@5` (Hits) |
|---|---:|---:|---:|---:|---:|
| **All Frozen Positions (`COLLATOR_80_10_10`)** | `38,151` | `0.83160` | **`0.88158` (`33,633`)** | **`0.84897`** | **`0.91421` (`34,878`)** |
| **All Frozen Positions (`100%_MASK`)** | `38,151` | — | — | **`0.84300`** | **`0.91321` (`34,840`)** |
| **All Frozen Positions (`CLSS-C-v3` Pure, `0` Neural)** | `38,151` | — | — | `0.80393` | `0.87743` (`33,475`) |
| **`[MASK]`-Only Positions (`input_id == 103`)** | `30,545` | `0.81329` | `0.86855` (`26,530`) | **`0.83327`** | **`0.90506` (`27,645`)** |
| **Single-Token Whole Words (`is_single_word == 1`)** | `10,191` | `0.87403` | `0.91944` (`9,370`) | `0.86760` | **`0.93514` (`9,530`)** |
| **All Whole-Word Units (all masked subwords hit)** | `34,958` | — | `0.87594` (`30,621`) | — | **`0.90963` (`31,799`)** |
| **`[MASK]`-Only Whole-Word Units** | `28,447` | — | `0.86347` (`24,563`) | — | **`0.90094` (`25,629`)** |
| **Excl. Union `D8 >= 0.5` (`6` test docs)** | `38,097` | `0.83140` | **`0.88143` (`33,580`)** | **`0.84885`** | **`0.91411` (`34,825`)** |
| **Excl. Union `D8 >= 0.2` (`163` test docs)** | `36,092` | `0.83001` | **`0.88022` (`31,769`)** | **`0.84754`** | **`0.91286` (`32,947`)** |
| **Excl. `627` `Q`-Composite Test Docs (`2,259` P/X docs)** | `31,439` | `0.83319` | **`0.88104` (`27,699`)** | **`0.84661`** | **`0.91352` (`28,720`)** |
| **Excl. `864` `Q`-Docs & Shared `display_name`/`title` Docs** | `28,543` | `0.83467` | **`0.88176` (`25,168`)** | **`0.84666`** | **`0.91308` (`26,062`)** |
| **Excl. `1,316` `Q`-Docs & $\ge 6$-Word `Q`-Witness Docs** | `21,506` | `0.84168` | **`0.88696` (`19,075`)** | **`0.86108`** | **`0.92267` (`19,843`)** |
| **Excl. `794` Docs w/ Any $\ge 10$-Word Train Overlap** | `25,935` | `0.83260` | **`0.88174` (`22,868`)** | **`0.84963`** | **`0.91432` (`23,713`)** |

### 4.2 Per-Genre Table 2 Breakdown

| Oracc Genre | $N$ | Paper `MRR` | Paper `Hit@5` | Baseline `MRR` | Baseline `Hit@5` (Hits) | `CLSS-Akk-v3` `MRR` | `CLSS-Akk-v3` `Hit@5` (Hits) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `Lexical` | `11,726` | `0.69` | `0.85` | `0.84216` | `0.88436` (`10,370`) | **`0.85237`** | **`0.92171` (`10,808`)** |
| `Royal Inscription` | `5,962` | `0.83` | `0.90` | `0.82076` | `0.87957` (`5,244`) | **`0.86393`** | **`0.91781` (`5,472`)** |
| `Astrological Report` | `1,773` | `0.81` | `0.88` | `0.81847` | `0.87986` (`1,560`) | **`0.86722`** | **`0.92329` (`1,637`)** |
| `Administrative Letter` | `4,848` | — | — | `0.83679` | `0.88965` (`4,313`) | `0.82533` | **`0.90285` (`4,377`)** |
| `Legal Transaction` | `2,644` | — | — | `0.82767` | `0.87784` (`2,321`) | **`0.83762`** | **`0.90393` (`2,390`)** |
| `Eponym List` | `1,573` | — | — | `0.79071` | `0.84170` (`1,324`) | **`0.82109`** | **`0.89765` (`1,412`)** |
| `Scholarly Letter` | `1,551` | — | — | `0.85633` | `0.90264` (`1,400`) | **`0.85804`** | **`0.91296` (`1,416`)** |
| `Extispicy Query` | `794` | — | — | `0.78823` | `0.86272` (`685`) | **`0.87497`** | **`0.93577` (`743`)** |

### 4.3 Negative Controls

- **Negative Control 1 (400 Label Permutations, `np.random.default_rng(0)`):** Permuting the `38,151` ground-truth `label_id` values directly from `object/akkadian_predictions_part1..6.csv` with `np.random.default_rng(0)` collapses `CLSS-Akk-v3` to `Hit@5 = 0.21494 +/- 0.00155` (`median = 0.21496`, `IQR = 0.00189`, `best_control = 0.21918`, $z = +450.6\text{ SD}$) and `MRR@5 = 0.13531 +/- 0.00110` (`median = 0.13533`, `IQR = 0.00142`, `best_control = 0.13845`, $z = +641.4\text{ SD}$).
- **Negative Control 2 (Training Unigram Top-5 Predictor):** Always predicting the 5 most frequent training tokens (`['-', 'a', 'u', 'i', 'ša']`) yields `MRR@5 = 0.26419`, `Hit@1 = 0.21184`, and `Hit@5 = 0.35103`.

---

## 5. Static Audit of `how-we-built-it/build_corpus_bin.py` and `how-we-built-it/clss_akk_engine_v3.c`

We audited `how-we-built-it/build_corpus_bin.py` and all `856` lines of `how-we-built-it/clss_akk_engine_v3.c`:
1. **100% Train-Derived Active Vocabulary (`build_corpus_bin.py`):** Iterates strictly over `train_docs` (`9,221` clean training documents) to populate `active_ids` (`V_glob = 1,824`); `test_lbl` is never scanned when constructing the candidate vocabulary (`25` test OOV positions are encoded as `-2` and scored as misses).
2. **Template Hash Tables, 3-Gram Passage Anchor Index, and Unigram Priors (`clss_akk_engine_v3.c`):** Built strictly over `d = 0..N_train-1` (`train_seqs`, `9,221` training documents). `test_seqs` is never indexed.
3. **Two-Pass Inference (`eval_worker`, lines 351–664):** Constructs `seq[i]` strictly from `in_toks[i]` (or `MASK_C` at masked indices when `mode_100 == 1`, and maps `UNK_C` to `MASK_C`). Throughout Pass 1 and Pass 2 (lines 386–623), `lbl_toks[i]` is never read as a token value.

Every check in `sh verify-it-yourself/run_checks.sh` passed with zero discrepancies.

pass: true
