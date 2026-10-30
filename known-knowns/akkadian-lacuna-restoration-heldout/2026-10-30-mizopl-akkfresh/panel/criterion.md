# Panel Report — CRITERION (`akkadian-lacuna-restoration-heldout`)

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
claim_type: full_win
confirmed_scope: On the released SLAB-NLP/Akk ORACC dataset (commit dfd2a66d4305cf36981e4fd3fde823a5020161dd, deduplicated from 23,211 to 14,430 unique id_text rows, split 80/20 at SEED=20261031 into 2,886 held-out test documents in bert_test_heldout.txt sha256 2813b573c52285d0ed636b41b6e725df66feeb424966653ebcd862e5f69eef14 and 9,221 composition-disjoint training documents in bert_train_clean.txt sha256 4905a304a059533aa39e2204cef1bc0c16ba77e4dc9a701d312db09a80cf4f91 after removing all 2,323 training texts sharing empty/exact bert_input, >=20% distinct word 8-grams, or any >=15-word block with any test document; median union-D8 = 0.00000 across all 2,653 test docs with >=8 words) under the repository's 15% token-level masking protocol at torch.manual_seed(20261031) with 99-slot vocab.txt sha256 00bd3cdcd37cd9ad218eb872e61bef64bc19ec0b81d4aedea00c2356266bee3f and N = 38,151 frozen masked word-piece positions (frozen_masked_positions.csv sha256 5af36f37415efc204cde20cf4be2259abc9abaea88dc31be9b37b0ba72ca325f, frozen_test_tensors_seed20261031.npz sha256 f060ec0879152b9ab5fa95f9e9db126674d4cce9e6c7abcb1857843c6f8d4234, object/prereg_split_and_mask_manifest.json sha256 06ba9a82589d8eeb31433480b275e4821df574938d1104ea607558cc88104877 published on GitHub in commit e26fa2cb33964bfe549770d311120ba1f804d81f at 2026-10-30T08:24:24Z before any model training started), the reproduced MBERT+Akk baseline trained strictly on the 9,221 clean training documents and frozen in commit 00db937 (mbert_akk_baseline_top5_predictions.csv sha256 cbc4e1803b1933d03c7162c190ae5c077b0cb323f41d82d1016e0c38cc2a4c7e) achieves Hit@5 = 0.88158 (33,633/38,151), MRR = 0.83160 (MRR@5 = 0.82413), Hit@1 = 0.78732 (30,037/38,151), and Hit@10 = 0.91403 (34,871/38,151) inside the Clause (1) gate [0.87, 0.91], while the boundary-deduplicated 53-template slot-syntax, parallel-passage, and two-pass belief-propagation model CLSS-Akk-v3 indexed solely on the 9,221 clean training documents across V_glob = 1,824 train-only active tokens (how-we-built-it/clss_akk_engine_v3.c sha256 9d867163e19e757d044a4e25c09e677400e837c5c71facfb21416c879134d3af, clss_akk_top5_predictions.csv sha256 4cf74f60139603851f7e1639f4864237af05ecabfefb540fed5a7a421f0ed7f6, object/akkadian_predictions_part1..6.csv, and object/akkadian_audit_manifest.json sha256 7e5e592d5c9f056ae11bc04eebe65e1bf1139024642c709f4da6b7a25c3b8097) achieves Hit@5 = 0.91421 (34,878/38,151, +0.02421 over 0.89, +0.01921 over 0.895, and +0.03263 / +1,245 hits over MBERT+Akk), MRR = 0.84897 (MRR@5 = 0.84345, +0.01897 over 0.83 and +0.01737 over MBERT+Akk), Hit@1 = 0.79395 (30,290/38,151), and Hit@10 = 0.93872 (35,813/38,151), simultaneously beating both the paper and the reproduced baseline under 100% [MASK] inference (Hit@5 = 0.91321, MRR = 0.84300), on [MASK]-only positions (N = 30,545: Hit@5 = 0.90506 vs 0.86855, MRR = 0.83327 vs 0.81329), on all 34,958 whole-word units (Hit@5 = 0.90963 vs 0.87594) and 28,447 [MASK]-only whole-word units (Hit@5 = 0.90094 vs 0.86347), across all 6 cross-split union-D8 and Q-composition filters (e.g., excluding union D8 >= 0.5: Hit@5 = 0.91411 vs 0.88143; excluding all 627 Q-number test docs: Hit@5 = 0.91352 vs 0.88104; excluding 1,316 Q-docs and >=6-word Q-witness docs: Hit@5 = 0.92267 vs 0.88696), and across the Table 2 genres Lexical (N = 11,726: MRR = 0.85237 vs 0.69, Hit@5 = 0.92171 vs 0.85), Astrological Report (N = 1,773: MRR = 0.86722 vs 0.81, Hit@5 = 0.92329 vs 0.88), and Royal Inscription (N = 5,962: MRR = 0.86393 vs 0.83, Hit@5 = 0.91781 vs 0.90), thereby satisfying the full success criterion (full_win) as well as partial win p1.

---

## 1. Artifact Integrity and Chronological Pre-Registration Chain

All shipped package artifacts were independently hashed and checked against `SHA256SUMS` and `object/akkadian_audit_manifest.json` (`326,637` bytes, `sha256: 7e5e592d5c9f056ae11bc04eebe65e1bf1139024642c709f4da6b7a25c3b8097`), and the chronological commit chain on `mizopl/V3R1T4S` branch `submission/2026-10-30-mizopl-akkfresh` was verified:

1. **Stage I Pre-Registration Commit Before Any Model Training ([`e26fa2cb33964bfe549770d311120ba1f804d81f`](https://github.com/mizopl/V3R1T4S/commit/e26fa2cb33964bfe549770d311120ba1f804d81f), `2026-10-30T08:24:24Z`)**:
   - Published `how-we-built-it/PREREG.md`, `how-we-built-it/stage1_freeze_split_and_masks.py`, and `object/prereg_split_and_mask_manifest.json` (`sha256: 06ba9a82589d8eeb31433480b275e4821df574938d1104ea607558cc88104877`), locking the SHA-256 digests of `bert_train_clean.txt` (`4905a304...`), `bert_test_heldout.txt` (`2813b573...`), `main_tokenizer/vocab.txt` (`00bd3cdc...`), `frozen_masked_positions.csv` (`5af36f37...`), and `frozen_test_tensors_seed20261031.npz` (`f060ec08...`) on GitHub **before** training `MBERT+Akk` or `CLSS-Akk-v3`.
2. **Stage II Frozen `MBERT+Akk` Baseline Commit Before `CLSS-Akk-v3` ([`00db937`](https://github.com/mizopl/V3R1T4S/commit/00db937), `2026-10-30T14:09Z`)**:
   - Published `object/baseline_frozen_manifest.json` (`sha256: b30998900a380114736b025b5e1fc333754af49e59eafae456c8cddb358d82c4`), locking the SHA-256 digest of `mbert_akk_baseline_top5_predictions.csv` (`cbc4e1803b1933d03c7162c190ae5c077b0cb323f41d82d1016e0c38cc2a4c7e`, `Hit@5 = 0.88158`, `MRR = 0.83160`) on GitHub **before** Stage III `CLSS-Akk-v3` ran.

---

## 2. Clause-by-Clause Audit of the Updated Success Criterion (`commits 6b0b7e1` & `2cfdac1`)

### 2.1 Corpus Deduplication, Composition Disjointness, and Token-Level Protocol
- **Deduplication & Composition Filtering (`SEED = 20261031`):** `SLAB-NLP/Akk/data/akk_from_jsons.jsonl` (`23,211` rows) was deduplicated by `id_text` to `14,430` unique texts, split 80/20 (`11,544` initial train, `2,886` test), and cleaned by removing `2,323` training texts (`23` empty/exact `bert_input` matches + `1,704` documents sharing $\ge 20\%$ of distinct word 8-grams with any test document in either direction + `596` documents sharing any contiguous $\ge 15$-word span with any test document), leaving **`9,221` composition-disjoint training documents (`707,197` words)**.
- **Cross-Split Union-`D8` & `Q`-Number Audit:** Across all `2,653` held-out test documents with $\ge 8$ words, the **median union-`D8` is `0.00000`**, and only `6` test documents (`0.23%`) have union-`D8 >= 0.5`. Removing those `6` documents (`N = 38,097`), removing all `163` documents with union-`D8 >= 0.2` (`N = 36,092`), removing all `627` `Q`-number composite test documents (`N = 31,439`), removing `864` `Q` or shared-`textdata.csv`-title documents (`N = 28,543`), removing `1,316` `Q` or $\ge 6$-word `Q`-witness documents (`N = 21,506`), or removing `794` documents sharing any $\ge 10$-word span with training (`N = 25,935`), `MBERT+Akk` remains inside `[0.87, 0.91]` (`0.88022–0.88696`) and `CLSS-Akk-v3` achieves `Hit@5 = 0.91286–0.92267` and `MRR = 0.84661–0.86108`.
- **Tokenization & Masking (`torch.manual_seed(20261031)`):** Uses `SLAB-NLP/Akk`'s exact preprocessing flags (`--remove_subscripts --remove_superscripts`, keeping `-` and `...`, mapping `'x' -> U+1F607` which is never masked), 99-slot `MBERT+Akk` `vocab.txt` built strictly from `bert_train_clean.txt`, 128-token truncation (`ORACCDataset`), and 15% 80/10/10 masking (`DataCollatorForLanguageModelingAkkadian`, `N = 38,151` positions: `30,545` `[MASK]`, `3,833` unchanged, `3,773` random).

### 2.2 Clause (1): Reproduced `MBERT+Akk` Baseline Inside `[0.87, 0.91]`
- Trained strictly on `bert_train_clean.txt` (`9,221` clean docs) with `SLAB-NLP/Akk`'s full-vocabulary (`119,547`) `bert-base-multilingual-cased` setup and evaluated once blindly on the `N = 38,151` frozen test positions:
  - **With `attention_mask` (shipped CSVs):** **`Hit@5 = 0.88158` (`33,633 / 38,151`)**, **`MRR = 0.83160`** (`MRR@5 = 0.82413`), **`Hit@1 = 0.78732` (`30,037`)**, **`Hit@10 = 0.91403` (`34,871`)**.
  - **Without `attention_mask`:** `Hit@5 = 0.87969` (`33,561 / 38,151`), `MRR = 0.82906`.
  - Both land squarely inside the Clause (1) gate `[0.87, 0.91]` (`0.89 +/- 0.02`).

### 2.3 Clause (2) & Partial Win `p1`: `CLSS-Akk-v3` Beats Both Paper and Reproduced Baseline Across All Subsets and Genres

| Evaluation Regime / Subset | Positions ($N$) | `MBERT+Akk` `MRR` | `MBERT+Akk` `Hit@5` (Hits) | `CLSS-Akk-v3` `MRR` | `CLSS-Akk-v3` `Hit@5` (Hits) |
|---|---:|---:|---:|---:|---:|
| Published Paper (Lazar et al. 2021) | ~20% split | `0.83000` | `0.89000` (`0.895`) | — | — |
| **All Frozen Positions (`COLLATOR_80_10_10`)** | `38,151` | `0.83160` | `0.88158` (`33,633`) | **`0.84897`** | **`0.91421` (`34,878`)** |
| **All Frozen Positions (`100%_MASK`)** | `38,151` | — | — | **`0.84300`** | **`0.91321` (`34,840`)** |
| **`[MASK]`-Only Positions (`input_id == 103`)** | `30,545` | `0.81329` | `0.86855` (`26,530`) | **`0.83327`** | **`0.90506` (`27,645`)** |
| **All Whole-Word Units** | `34,958` | — | `0.87594` (`30,621`) | — | **`0.90963` (`31,799`)** |
| **`[MASK]`-Only Whole-Word Units** | `28,447` | — | `0.86347` (`24,563`) | — | **`0.90094` (`25,629`)** |
| **Excl. Union `D8 >= 0.5` (`6` docs)** | `38,097` | `0.83140` | `0.88143` (`33,580`) | **`0.84885`** | **`0.91411` (`34,825`)** |
| **Excl. Union `D8 >= 0.2` (`163` docs)** | `36,092` | `0.83001` | `0.88022` (`31,769`) | **`0.84754`** | **`0.91286` (`32,947`)** |
| **Excl. `627` `Q`-Composite Test Docs** | `31,439` | `0.83319` | `0.88104` (`27,699`) | **`0.84661`** | **`0.91352` (`28,720`)** |
| **Excl. `1,316` `Q` & $\ge 6$-Word `Q`-Witness Docs** | `21,506` | `0.84168` | `0.88696` (`19,075`) | **`0.86108`** | **`0.92267` (`19,843`)** |
| **Genre: `Lexical` (Paper `0.69 / 0.85`)** | `11,726` | `0.84216` | `0.88436` (`10,370`) | **`0.85237`** | **`0.92171` (`10,808`)** |
| **Genre: `Royal Inscription` (Paper `0.83 / 0.90`)** | `5,962` | `0.82076` | `0.87957` (`5,244`) | **`0.86393`** | **`0.91781` (`5,472`)** |
| **Genre: `Astrological Report` (Paper `0.81 / 0.88`)** | `1,773` | `0.81847` | `0.87986` (`1,560`) | **`0.86722`** | **`0.92329` (`1,637`)** |

---

## 3. Verdict

Every clause of the updated `akkadian-lacuna-restoration-heldout` full success criterion (`claim_type: full_win`) and partial win `p1` is satisfied and independently verified from the shipped prediction CSVs and audit manifest.

pass: true
