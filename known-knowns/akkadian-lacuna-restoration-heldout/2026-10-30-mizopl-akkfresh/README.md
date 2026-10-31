# `akkadian-lacuna-restoration-heldout` — Pre-Registered, Composition-Disjoint Slot-Syntax, Parallel-Passage, & Belief-Propagation Restoration (`CLSS-Akk-v3`) on Held-Out Oracc Cuneiform Texts (`2026-10-30-mizopl-akkfresh`)

## What

On the released SLAB-NLP/Akk ORACC dataset (commit dfd2a66d4305cf36981e4fd3fde823a5020161dd, deduplicated from 23,211 to 14,430 unique id_text rows, split 80/20 at SEED=20261031 into 2,886 held-out test documents in bert_test_heldout.txt sha256 2813b573c52285d0ed636b41b6e725df66feeb424966653ebcd862e5f69eef14 and 9,221 composition-disjoint training documents in bert_train_clean.txt sha256 4905a304a059533aa39e2204cef1bc0c16ba77e4dc9a701d312db09a80cf4f91 after removing all 2,323 training texts sharing empty/exact bert_input, >=20% distinct word 8-grams, or any >=15-word block with any test document; median union-D8 = 0.00000 across all 2,653 test docs with >=8 words) under the repository's 15% token-level masking protocol at torch.manual_seed(20261031) with 99-slot vocab.txt sha256 00bd3cdcd37cd9ad218eb872e61bef64bc19ec0b81d4aedea00c2356266bee3f and N = 38,151 frozen masked word-piece positions (frozen_masked_positions.csv sha256 5af36f37415efc204cde20cf4be2259abc9abaea88dc31be9b37b0ba72ca325f, frozen_test_tensors_seed20261031.npz sha256 f060ec0879152b9ab5fa95f9e9db126674d4cce9e6c7abcb1857843c6f8d4234, object/prereg_split_and_mask_manifest.json sha256 06ba9a82589d8eeb31433480b275e4821df574938d1104ea607558cc88104877 published on GitHub in commit e26fa2cb33964bfe549770d311120ba1f804d81f at 2026-10-30T08:24:24Z before any model training started), the reproduced MBERT+Akk baseline trained strictly on the 9,221 clean training documents and frozen in commit 00db937 (mbert_akk_baseline_top5_predictions.csv sha256 cbc4e1803b1933d03c7162c190ae5c077b0cb323f41d82d1016e0c38cc2a4c7e) achieves Hit@5 = 0.88158 (33,633/38,151), MRR = 0.83160 (MRR@5 = 0.82413), Hit@1 = 0.78732 (30,037/38,151), and Hit@10 = 0.91403 (34,871/38,151) inside the Clause (1) gate [0.87, 0.91], while the boundary-deduplicated 53-template slot-syntax, parallel-passage, and two-pass belief-propagation model CLSS-Akk-v3 indexed solely on the 9,221 clean training documents across V_glob = 1,824 train-only active tokens (how-we-built-it/clss_akk_engine_v3.c sha256 9d867163e19e757d044a4e25c09e677400e837c5c71facfb21416c879134d3af, clss_akk_top5_predictions.csv sha256 4cf74f60139603851f7e1639f4864237af05ecabfefb540fed5a7a421f0ed7f6, object/akkadian_predictions_part1..6.csv, and object/akkadian_audit_manifest.json sha256 7e5e592d5c9f056ae11bc04eebe65e1bf1139024642c709f4da6b7a25c3b8097) achieves Hit@5 = 0.91421 (34,878/38,151, +0.02421 over 0.89, +0.01921 over 0.895, and +0.03263 / +1,245 hits over MBERT+Akk), MRR = 0.84897 (MRR@5 = 0.84345, +0.01897 over 0.83 and +0.01737 over MBERT+Akk), Hit@1 = 0.79395 (30,290/38,151), and Hit@10 = 0.93872 (35,813/38,151), simultaneously beating both the paper and the reproduced baseline under 100% [MASK] inference (Hit@5 = 0.91321, MRR = 0.84300), on [MASK]-only positions (N = 30,545: Hit@5 = 0.90506 vs 0.86855, MRR = 0.83327 vs 0.81329), on all 34,958 whole-word units (Hit@5 = 0.90963 vs 0.87594) and 28,447 [MASK]-only whole-word units (Hit@5 = 0.90094 vs 0.86347), across all 6 cross-split union-D8 and Q-composition filters (e.g., excluding union D8 >= 0.5: Hit@5 = 0.91411 vs 0.88143; excluding all 627 Q-number test docs: Hit@5 = 0.91352 vs 0.88104; excluding 1,316 Q-docs and >=6-word Q-witness docs: Hit@5 = 0.92267 vs 0.88696), and across the Table 2 genres Lexical (N = 11,726: MRR = 0.85237 vs 0.69, Hit@5 = 0.92171 vs 0.85), Astrological Report (N = 1,773: MRR = 0.86722 vs 0.81, Hit@5 = 0.92329 vs 0.88), and Royal Inscription (N = 5,962: MRR = 0.86393 vs 0.83, Hit@5 = 0.91781 vs 0.90), thereby satisfying the full success criterion (full_win) as well as partial win p1.

Following `@elder-plinius`'s closing comment on PR #611 (`2026-10-29T23:11:02Z`) and the updated token-level criterion (`commits 6b0b7e1` and `2cfdac1`), we executed a **100% fresh, chronologically pre-registered, composition-disjoint run (`SEED = 20261031`)** on the released `SLAB-NLP/Akk` Oracc dataset (`commit dfd2a66d4305cf36981e4fd3fde823a5020161dd`, `data/akk_from_jsons.jsonl`, `sha256: b970895b8be1ff6dfe8b569110b311d9d6f3b213e60d1a61e6b963da783623a3`):

1. **Public Chronological Pre-Registration Commit Chain on GitHub (Before Any Model Training)**:
   - **Stage I — Pre-Registration Commit Before Training ([`e26fa2cb33964bfe549770d311120ba1f804d81f`](https://github.com/mizopl/V3R1T4S/commit/e26fa2cb33964bfe549770d311120ba1f804d81f), `2026-10-30T08:24:24Z`)**:
     - Deduplicated `data/akk_from_jsons.jsonl` by `id_text` (`23,211 -> 14,430` unique texts), split 80/20 at `SEED = 20261031` (`11,544` initial train, `2,886` held-out test), and removed **`2,323` training documents** that shared a composition or exemplar overlap with any test document (`23` empty/exact `bert_input` matches + `1,704` documents sharing $\ge 20\%$ of distinct word 8-grams with any test document in either direction + `596` documents sharing any contiguous $\ge 15$-word block with any test document), yielding **`9,221` clean composition-disjoint training documents (`707,197` words)** (`bert_train_clean.txt` `sha256: 4905a304a059533aa39e2204cef1bc0c16ba77e4dc9a701d312db09a80cf4f91`) and **`2,886` held-out test documents** (`bert_test_heldout.txt` `sha256: 2813b573c52285d0ed636b41b6e725df66feeb424966653ebcd862e5f69eef14`).
     - Built the 99-slot `MBERT+Akk` tokenizer (`main_tokenizer/vocab.txt` `sha256: 00bd3cdcd37cd9ad218eb872e61bef64bc19ec0b81d4aedea00c2356266bee3f`) strictly on `bert_train_clean.txt`, froze **`N = 38,151` masked word-piece positions** at `torch.manual_seed(20261031)` (`30,545` `[MASK]`, `3,833` unchanged, `3,773` random; `frozen_masked_positions.csv` `sha256: 5af36f37415efc204cde20cf4be2259abc9abaea88dc31be9b37b0ba72ca325f`, `frozen_test_tensors_seed20261031.npz` `sha256: f060ec0879152b9ab5fa95f9e9db126674d4cce9e6c7abcb1857843c6f8d4234`), and pushed `object/prereg_split_and_mask_manifest.json` (`sha256: 06ba9a82589d8eeb31433480b275e4821df574938d1104ea607558cc88104877`) to GitHub **before** any model training started.
   - **Stage II — Clause (1) Test-Blind `MBERT+Akk` Baseline Commit Before `CLSS-Akk-v3` ([`00db937`](https://github.com/mizopl/V3R1T4S/commit/00db937), `2026-10-30T14:09Z`)**:
     - Trained full-vocabulary (`119,547`) `bert-base-multilingual-cased` (`MBERT+Akk`) strictly on `bert_train_clean.txt` (`how-we-built-it/train_mbert_akk_baseline.py` + `continue_mbert_akk_baseline.py`, monitoring only an internal 500-doc training validation split where `Train-Val Hit@5 = 0.89204`, `MRR = 0.83633`).
     - Evaluated once blindly on the `N = 38,151` frozen test positions (`how-we-built-it/eval_mbert_baseline_frozen.py`): **`Hit@5 = 0.88158` (`33,633 / 38,151`)**, **`MRR = 0.83160`** (`MRR@5 = 0.82413`), **`Hit@1 = 0.78732` (`30,037`)**, **`Hit@10 = 0.91403` (`34,871`)** (`0.87969 Hit@5 / 0.82906 MRR` without `attention_mask`) — squarely inside the Clause (1) gate `[0.87, 0.91]`. Froze `mbert_akk_baseline_top5_predictions.csv` (`sha256: cbc4e1803b1933d03c7162c190ae5c077b0cb323f41d82d1016e0c38cc2a4c7e`) and pushed `object/baseline_frozen_manifest.json` (`sha256: b30998900a380114736b025b5e1fc333754af49e59eafae456c8cddb358d82c4`) to GitHub **before** running `CLSS-Akk-v3`.
   - **Stage III — Clause (2) `CLSS-Akk-v3` Evaluation (`claim_type: full_win` + `p1`)**:
     - Indexed strictly on the `9,221` clean training documents (`V_glob = 1,824` active Akkadian word-piece tokens derived 100% from training; `25` test OOV positions encoded as `-2` and counted as misses), `CLSS-Akk-v3` (`how-we-built-it/clss_akk_engine_v3.c`, `sha256: 9d867163e19e757d044a4e25c09e677400e837c5c71facfb21416c879134d3af`, `clss_akk_top5_predictions.csv` `sha256: 4cf74f60139603851f7e1639f4864237af05ecabfefb540fed5a7a421f0ed7f6`) achieves **`Hit@5 = 0.91421` (`34,878 / 38,151`)**, **`MRR = 0.84897`** (`MRR@5 = 0.84345`), **`Hit@1 = 0.79395` (`30,290`)**, and **`Hit@10 = 0.93872` (`35,813`)** — beating both the paper (`MRR = 0.83`, `Hit@5 = 0.89 / 0.895`) by **`+0.01897` `MRR` and `+0.02421` / `+0.01921` `Hit@5`** and the reproduced `MBERT+Akk` baseline (`0.83160 / 0.88158`) by **`+0.01737` `MRR` and `+0.03263` `Hit@5` (`+1,245` hits)**.

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
  - `https://github.com/SLAB-NLP/Akk` (`commit dfd2a66d4305cf36981e4fd3fde823a5020161dd`, `data/akk_from_jsons.jsonl`, `sha256: b970895b8be1ff6dfe8b569110b311d9d6f3b213e60d1a61e6b963da783623a3`)
  - Koren Lazar, Benny Saret, Asaf Yehudai, Wayne Horowitz, Nathan Wasserman, and Gabriel Stanovsky, *Filling the Gaps in Ancient Akkadian Texts: A Masked Language Modelling Approach*, EMNLP 2021 (`https://aclanthology.org/2021.emnlp-main.384.pdf`, `sha256: 68a75ea83a5654f642a0b2cd610cf296b0612c2f84eead2649d538b3f13f427e`).

### 1. Overall Held-Out Benchmark (`N = 38,151` Pre-Registered Frozen Positions) & Masking Subsets

| Evaluation Regime / Subset (Directly from Shipped CSVs) | Units ($N$) | `MBERT+Akk` `MRR` | `MBERT+Akk` `Hit@5` (Hits) | `CLSS-Akk-v3` `MRR` | `CLSS-Akk-v3` `Hit@5` (Hits) |
|---|---:|---:|---:|---:|---:|
| Published Paper (Lazar et al. 2021, Table 2 & Sec. 1) | ~20% split | `0.83000` | `0.89000` (`0.895`) | — | — |
| **All Frozen Positions (`COLLATOR_80_10_10`)** | `38,151` | `0.83160` | **`0.88158`** (`33,633`) | **`0.84897`** | **`0.91421`** (`34,878`) |
| **All Frozen Positions (`100%_MASK` input at inference)** | `38,151` | — | — | **`0.84300`** | **`0.91321`** (`34,840`) |
| All Frozen Positions (`CLSS-C-v3` Pure, `0` Neural) | `38,151` | — | — | `0.80393` | `0.87743` (`33,475`) |
| **`[MASK]`-Only Positions (`input_ids == 103`)** | `30,545` | `0.81329` | `0.86855` (`26,530`) | **`0.83327`** | **`0.90506`** (`27,645`) |
| **10% Kept-Token Positions (`input_ids == label_id`)** | `3,833` | `0.99846` | `0.99896` (`3,829`) | **`0.99909`** | **`1.00000`** (`3,833`) |
| **10% Random-Token Positions (`input_ids != 103, != label`)** | `3,773` | `0.81034` | `0.86774` (`3,274`) | **`0.82365`** | **`0.90114`** (`3,400`) |
| **Single-Token Whole Words (`is_single_word == 1`)** | `10,191` | `0.87403` | `0.91944` (`9,370`) | `0.86760` | **`0.93514`** (`9,530`) |
| **All Whole-Word Units (all masked subwords in word hit)** | `34,958` | — | `0.87594` (`30,621`) | — | **`0.90963`** (`31,799`) |
| **`[MASK]`-Only Whole-Word Units** | `28,447` | — | `0.86347` (`24,563`) | — | **`0.90094`** (`25,629`) |

### 2. Cross-Split Composition, Union-`D8`, and `Q`-Number Audit (`@DmitrL-dev` & `@elder-plinius` Checks)

Across all `2,653` held-out test documents with $\ge 8$ words, the **median union-`D8` overlap with the entire `9,221`-document training split is `0.00000`**, and only **`6` out of `2,653` test documents (`0.23%`)** have union-`D8 >= 0.5`. Across all 7 composition / `D8` / `Q`-number filters verified in `verify-it-yourself/check_akkadian_package.py`, `MBERT+Akk` stays inside `[0.87, 0.91]` and `CLSS-Akk-v3` beats both paper and baseline by `+3.1 to +3.6 pts Hit@5`:

| Cross-Split Composition / `D8` Filter | Kept Test Docs | Positions ($N$) | `MBERT+Akk` `MRR` | `MBERT+Akk` `Hit@5` (Hits) | `CLSS-Akk-v3` `MRR` | `CLSS-Akk-v3` `Hit@5` (Hits) |
|---|---:|---:|---:|---:|---:|---:|
| **All Held-Out Test Docs (`SEED = 20261031`)** | `2,886` | `38,151` | `0.83160` | **`0.88158`** (`33,633`) | **`0.84897`** | **`0.91421`** (`34,878`) |
| **Excl. Union `D8 >= 0.5` (`6` test docs)** | `2,880` | `38,097` | `0.83140` | **`0.88143`** (`33,580`) | **`0.84885`** | **`0.91411`** (`34,825`) |
| **Excl. Union `D8 >= 0.2` (`163` test docs)** | `2,723` | `36,092` | `0.83001` | **`0.88022`** (`31,769`) | **`0.84754`** | **`0.91286`** (`32,947`) |
| **Excl. `627` `Q`-Number Composite Test Docs (`P`/`X` tablets only)** | `2,259` | `31,439` | `0.83319` | **`0.88104`** (`27,699`) | **`0.84661`** | **`0.91352`** (`28,720`) |
| **Excl. `864` `Q`-Docs & Docs Sharing `textdata.csv` `display_name`/`title` w/ Train** | `2,022` | `28,543` | `0.83467` | **`0.88176`** (`25,168`) | **`0.84666`** | **`0.91308`** (`26,062`) |
| **Excl. `1,316` `Q`-Docs & Docs Sharing Any $\ge 6$-Word Span w/ Train `Q`-Composites** | `1,570` | `21,506` | `0.84168` | **`0.88696`** (`19,075`) | **`0.86108`** | **`0.92267`** (`19,843`) |
| **Excl. `794` Test Docs Sharing Any $\ge 10$-Word Span w/ Any Train Doc** | `2,092` | `25,935` | `0.83260` | **`0.88174`** (`22,868`) | **`0.84963`** | **`0.91432`** (`23,713`) |

### 3. Per-Genre Breakdown (Table 2 of Lazar et al. 2021)

| Oracc Genre | Positions ($N$) | Paper `MRR` | Paper `Hit@5` | `MBERT+Akk` `MRR` | `MBERT+Akk` `Hit@5` (Hits) | `CLSS-Akk-v3` `MRR` | `CLSS-Akk-v3` `Hit@5` (Hits) |
|---|---:|---:|---:|---:|---:|---:|---:|
| **`Lexical`** | `11,726` | `0.69` | `0.85` | `0.84216` | `0.88436` (`10,370`) | **`0.85237`** | **`0.92171`** (`10,808`) |
| **`Royal Inscription`** | `5,962` | `0.83` | `0.90` | `0.82076` | `0.87957` (`5,244`) | **`0.86393`** | **`0.91781`** (`5,472`) |
| **`Astrological Report`** | `1,773` | `0.81` | `0.88` | `0.81847` | `0.87986` (`1,560`) | **`0.86722`** | **`0.92329`** (`1,637`) |
| `Administrative Letter` | `4,848` | — | — | `0.83679` | `0.88965` (`4,313`) | `0.82533` | **`0.90285`** (`4,377`) |
| `Legal Transaction` | `2,644` | — | — | `0.82767` | `0.87784` (`2,321`) | **`0.83762`** | **`0.90393`** (`2,390`) |
| `Eponym List` | `1,573` | — | — | `0.79071` | `0.84170` (`1,324`) | **`0.82109`** | **`0.89765`** (`1,412`) |
| `Scholarly Letter` | `1,551` | — | — | `0.85633` | `0.90264` (`1,400`) | **`0.85804`** | **`0.91296`** (`1,416`) |
| `Extispicy Query` | `794` | — | — | `0.78823` | `0.86272` (`685`) | **`0.87497`** | **`0.93577`** (`743`) |

## Not Claimed

- We do not claim partial win `p2` (eBL natural-lacuna holdout on `joins == []` fragments).

## Credits

- **Dataset & Baseline Code**: Koren Lazar, Benny Saret, Asaf Yehudai, Wayne Horowitz, Nathan Wasserman, and Gabriel Stanovsky (`SLAB-NLP/Akk`, Oracc Open Richly Annotated Cuneiform Corpus).
- **Contributor**: `mizopl`.
