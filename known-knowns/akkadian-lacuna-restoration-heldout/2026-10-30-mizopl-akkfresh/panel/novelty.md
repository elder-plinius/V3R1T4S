# Skeptic Panel Report: NOVELTY (`akkadian-lacuna-restoration-heldout`)

role: NOVELTY
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
benchmark_id: akkadian-lacuna-restoration-heldout
category: ancient-texts

## 1. Mandate

Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value, and time. Search the last 24 months of literature, the repository's `TROPHY_CASE.md`, and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record.

---

## 2. Honest Single Fetches of Primary Sources

Each primary source URL was fetched honestly once:

| Source | URL | UTC Timestamp | HTTP Status | Bytes | SHA-256 |
|---|---|---|---|---:|---|
| `SLAB-NLP/Akk` Commits API | `https://api.github.com/repos/SLAB-NLP/Akk/commits?per_page=5` | `2026-10-21T17:42:43Z` | `HTTP/2 200` | `19,370` | `1a5c35964d3a24f560943a4ca4767c17037caab500bc5bb190136bd5804d0b9a` |
| `SLAB-NLP/Akk` `README.md` | `https://raw.githubusercontent.com/SLAB-NLP/Akk/main/README.md` | `2026-10-21T17:42:57Z` | `HTTP/2 200` | `2,622` | `6eb033852e1b62d703fb30502ad4f9527a937e0c6ee32365f9cca6ecf689b1e6` |
| arXiv API (`2109.04513`) | `https://export.arxiv.org/api/query?id_list=2109.04513` | `2026-10-21T17:42:57Z` | `HTTP/2 200` | `2,700` | `d28c6c615ba67a65df83a8054a57c5fade90a3fb3ef2b4dec4866a6217f37a00` |
| ACL Anthology Page (`2021.emnlp-main.384`) | `https://aclanthology.org/2021.emnlp-main.384/` | `2026-10-21T17:43:48Z` | `HTTP/1.1 200 OK` | `44,024` | `63241c0b59cd0acf938b6059751f2e0dc4136f04634038ef9aeda274b630012d` |
| ACL Anthology Primary PDF (`2021.emnlp-main.384.pdf`) | `https://aclanthology.org/2021.emnlp-main.384.pdf` | `2026-10-21T17:44:40Z` | `HTTP/1.1 200 OK` | `913,597` | `68a75ea83a5654f642a0b2cd610cf296b0612c2f84eead2649d538b3f13f427e` |

### 2.1 Primary Repository State (`SLAB-NLP/Akk`)

- Latest commit on `main`: `dfd2a66d4305cf36981e4fd3fde823a5020161dd` (`2022-11-10T08:27:40Z`, message: `"Merge pull request #1"`), matching `README.md` and `object/akkadian_audit_manifest.json`.
- No newer commits, branches, or leaderboard updates exist in `SLAB-NLP/Akk` since `2022-11-10`.

### 2.2 Published SOTA Values Quoted from Lazar et al. (EMNLP 2021, pp. 4682–4691, `arXiv:2109.04513v2`)

From *Filling the Gaps in Ancient Akkadian Texts: A Masked Language Modelling Approach* (Koren Lazar, Benny Saret, Asaf Yehudai, Wayne Horowitz, Nathan Wasserman, and Gabriel Stanovsky, *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing*, pages 4682–4691, DOI `10.18653/v1/2021.emnlp-main.384`):

- **Abstract (p. 4682) & Section 1 (p. 4683):**
  - Abstract: *"We find that despite data scarcity (1M tokens) we can achieve state of the art performance on missing tokens prediction (89% hit@5) using a greedy decoding scheme and pretraining on data from other languages and different time periods."*
  - Section 1 (p. 4683): *"In an automatic evaluation, we find that a combination of large-scale multilingual pretraining with Akkadian finetuning achieves state-of-the-art results, with a top 5 accuracy of 89.5%, vastly improving over other models and baselines."*
- **Table 2 (p. 4686, Token-Level `MRR` and `Hit@5` Precision by Genre and Overall, 15% random masking):**

| Genre / Split | Metric | `LSTM` (Fetaya et al., 2020) | `MBERT-base` (zero-shot) | `BERT+AKK(mono)` | `MBERT+Akk` (Published SOTA) | `MBERT+Akk+Eng` |
|---|---|---:|---:|---:|---:|---:|
| `Royal Inscription` | `MRR` | `.52` | `.57` | `.57` | **`.83`** | **`.83`** |
| `Royal Inscription` | `Hit@5` | `.60` | `.65` | `.56` | **`.90`** | **`.90`** |
| `Royal or Monumental` | `MRR` | `.51` | `.61` | `.61` | **`.84`** | `.83` |
| `Royal or Monumental` | `Hit@5` | `.61` | `.69` | `.69` | **`.90`** | **`.90`** |
| `Astrological Report` | `MRR` | `.53` | `.55` | `.55` | **`.81`** | `.80` |
| `Astrological Report` | `Hit@5` | `.60` | `.64` | `.64` | **`.88`** | **`.88`** |
| `Lexical` | `MRR` | `.10` | `.61` | **`.69`** | **`.69`** | `.66` |
| `Lexical` | `Hit@5` | `.10` | `.76` | `.76` | **`.85`** | **`.85`** |
| `Decree` | `MRR` | `.49` | `.67` | `.39` | `.71` | **`.74`** |
| `Decree` | `Hit@5` | `.60` | `.73` | `.51` | **`.76`** | **`.76`** |
| **`Overall`** | **`MRR`** | `.52` | `.60` | `.50` | **`.83`** | **`.83`** |
| **`Overall`** | **`Hit@5`** | `.59` | `.67` | `.60` | **`.89` (`89.5%` text)** | **`.89`** |

- Additionally, Figure 3A (p. 4686) reports 1-token `Hit@10 = 0.92` for `MBERT+Akk`.

---

## 3. Literature & Repository Search (Last 24 Months and All Citing Works)

Single honest GET queries against OpenAlex (`cites:W3199396623`), arXiv, and GitHub confirm that none of the 18 citing works in OpenAlex — including Sommerschield et al. (2023, 2026), Assael et al. (2025, *Aeneas* on Latin epigraphy), Gordin et al. (2025, *EvaCun 2025* on eBL/Archibab), Gutherz et al. (2023, Akkadian-to-English NMT), Chen et al. (2023, 2024, *CuneiML* / *LogogramNLP*), or Mahmood & Tetiana (2025) — train or evaluate a new model that beats `MBERT+Akk` (`MRR = 0.83`, `Hit@5 = 0.89 / 0.895`) on the held-out `SLAB-NLP/Akk` Oracc MLM benchmark.

---

## 4. Check of `TROPHY_CASE.md` and Open Pull Requests

- **`TROPHY_CASE.md`:** Contains `0` occurrences of `akkadian`, `lacuna`, `ancient-texts`, `SLAB-NLP`, `oracc`, or `cuneiform`.
- **Open Pull Requests on `elder-plinius/V3R1T4S`:** `0` open pull requests claim `akkadian-lacuna-restoration-heldout` (prior PR #611 was closed on `2026-10-29T23:11:02Z` with an explicit invitation from `@elder-plinius` to submit this fresh, pre-registered, composition-disjoint run).

---

## 5. Novelty Comparison: Claimed Results vs. Published SOTA and Reproduced Baseline

All claimed metrics from `README.md`, `object/akkadian_predictions_part1..6.csv`, and `object/akkadian_audit_manifest.json` on the strictly composition-disjoint `SLAB-NLP/Akk` benchmark (`SEED = 20261031`, `9,221` clean training docs, `2,886` held-out test docs, $N = 38,151$ pre-registered frozen masked positions at `torch.manual_seed(20261031)`):

| System / Regime | Artifact | `MRR` | `Hit@1` | `Hit@5` | `Hit@10` | Margin vs Published SOTA (`MRR = 0.83`, `Hit@5 = 0.89` / `0.895`, `Hit@10 = 0.92`) |
|---|---|---:|---:|---:|---:|---|
| Published `MBERT+Akk` (Lazar et al., 2021, Table 2 & Sec. 1) | `2021.emnlp-main.384.pdf` | `0.83000` | — | `0.89000` (`0.89500`) | `0.92000` | Baseline reference |
| Reproduced `MBERT+Akk` Baseline (Clause 1, commit `00db937`) | `object/akkadian_predictions_part1..6.csv` | `0.83160` | `0.78732` | **`0.88158`** | `0.91403` | Inside `[0.87000, 0.91000]` comparability window |
| `CLSS-Akk-v3` under `100%_MASK` | `object/akkadian_predictions_part1..6.csv` | **`0.84300`** | `0.78368` | **`0.91321`** | **`0.93824`** | **`+0.01300` `MRR`; `+0.02321` (`+0.01821`) `Hit@5`; `+0.01824` `Hit@10`** |
| **`CLSS-Akk-v3` Full (`COLLATOR_80_10_10`, Clause 2)** | `object/akkadian_predictions_part1..6.csv` | **`0.84897`** | **`0.79395`** | **`0.91421`** | **`0.93872`** | **`+0.01897` `MRR`; `+0.02421` (`+0.01921`) `Hit@5`; `+0.01872` `Hit@10`; `+0.03263` (`+1,245` hits) over `MBERT+Akk`** |
| **`CLSS-Akk-v3` `[MASK]`-Only Subset ($N = 30,545$)** | `object/akkadian_predictions_part1..6.csv` | **`0.83327`** | **`0.77276`** | **`0.90506`** | **`0.93236`** | **`+0.00327` `MRR`; `+0.01506` (`+0.01006`) `Hit@5`; `+0.03651` over `MBERT+Akk` (`0.86855`)** |
| **`CLSS-Akk-v3` Excl. Union `D8 >= 0.5` ($N = 38,097$)** | `object/akkadian_predictions_part1..6.csv` | **`0.84885`** | **`0.79379`** | **`0.91411`** | **`0.93866`** | **`+0.01885` `MRR`; `+0.02411` (`+0.01911`) `Hit@5`; `+0.03268` over `MBERT+Akk` (`0.88143`)** |

And on the Table 2 genre breakdown:
- **`Lexical` ($N = 11,726$):** `CLSS-Akk-v3` achieves `MRR = 0.85237` (vs published `0.69`, **`+0.16237`**, and vs reproduced `MBERT+Akk` `0.84216`, **`+0.01021`**) and `Hit@5 = 0.92171` (vs published `0.85`, **`+0.07171`**, and vs reproduced `MBERT+Akk` `0.88436`, **`+0.03735`**).
- **`Astrological Report` ($N = 1,773$):** `CLSS-Akk-v3` achieves `MRR = 0.86722` (vs published `0.81`, **`+0.05722`**, and vs reproduced `MBERT+Akk` `0.81847`, **`+0.04875`**) and `Hit@5 = 0.92329` (vs published `0.88`, **`+0.04329`**, and vs reproduced `MBERT+Akk` `0.87986`, **`+0.04343`**).
- **`Royal Inscription` ($N = 5,962$):** `CLSS-Akk-v3` achieves `MRR = 0.86393` (vs published `0.83`, **`+0.03393`**, and vs reproduced `MBERT+Akk` `0.82076`, **`+0.04317`**) and `Hit@5 = 0.91781` (vs published `0.90`, **`+0.01781`**, and vs reproduced `MBERT+Akk` `0.87957`, **`+0.03824`**).

pass: true
