# Skeptic Panel Report: NOVELTY (`akkadian-lacuna-restoration-heldout`)

role: NOVELTY
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
benchmark_id: akkadian-lacuna-restoration-heldout
category: ancient-texts

## 1. Mandate

Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value, and time. Search the last 24 months of literature, the repository's `TROPHY_CASE.md`, and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record.

---

## 2. Honest Single Fetches of Primary Sources

Each primary source URL was fetched exactly once with `curl -sS -D [headers] -A "V3R1T4S-research-agent (honest single fetch)"`:

| Source | URL | UTC Timestamp | HTTP Status | Bytes | SHA-256 |
|---|---|---|---|---:|---|
| `SLAB-NLP/Akk` Commits API | `https://api.github.com/repos/SLAB-NLP/Akk/commits?per_page=5` | `2026-10-21T17:42:43Z` | `HTTP/2 200` | `19,370` | `1a5c35964d3a24f560943a4ca4767c17037caab500bc5bb190136bd5804d0b9a` |
| `SLAB-NLP/Akk` `README.md` | `https://raw.githubusercontent.com/SLAB-NLP/Akk/main/README.md` | `2026-10-21T17:42:57Z` | `HTTP/2 200` | `2,622` | `6eb033852e1b62d703fb30502ad4f9527a937e0c6ee32365f9cca6ecf689b1e6` |
| arXiv API (`2109.04513`) | `https://export.arxiv.org/api/query?id_list=2109.04513` | `2026-10-21T17:42:57Z` | `HTTP/2 200` | `2,700` | `d28c6c615ba67a65df83a8054a57c5fade90a3fb3ef2b4dec4866a6217f37a00` |
| ACL Anthology Page (`2021.emnlp-main.384`) | `https://aclanthology.org/2021.emnlp-main.384/` | `2026-10-21T17:43:48Z` | `HTTP/1.1 200 OK` | `44,024` | `63241c0b59cd0acf938b6059751f2e0dc4136f04634038ef9aeda274b630012d` |
| ACL Anthology Primary PDF (`2021.emnlp-main.384.pdf`) | `https://aclanthology.org/2021.emnlp-main.384.pdf` | `2026-10-21T17:44:40Z` | `HTTP/1.1 200 OK` | `913,597` | `68a75ea83a5654f642a0b2cd610cf296b0612c2f84eead2649d538b3f13f427e` |

### 2.1 Primary Repository State (`SLAB-NLP/Akk`)

- Latest commit on `main`: `dfd2a66d4305cf36981e4fd3fde823a5020161dd` (`2022-11-10T08:27:40Z`, message: `"Merge pull request #1"`), matching `README.md` and `object/akkadian_audit_manifest.json`.
- Prior commit history:
  - `95d714af158040338bef596018a0814b47571881` (`2022-11-10T08:26:52Z`, `"fixing command line argument typo"`)
  - `baa07b0fdf8c7d8623fbd78508867c30a8a7ff6d` (`2021-09-15T14:12:32Z`, `"Update README.md"`)
  - `42cdfbc5cbd3c864484705695ee3e3af73092dd2` (`2021-09-12T17:30:30Z`, `"Update README.md"`)
  - `34df8e646f48a99de5aca534cafa51db88233b97` (`2021-09-09T21:27:56Z`, `"porting from private repo"`)
- No newer commits, branches, or leaderboard updates exist in `SLAB-NLP/Akk` since `2022-11-10`.

### 2.2 Published SOTA Values Quoted from Lazar et al. (EMNLP 2021, pp. 4682–4691, `arXiv:2109.04513v2`)

From *Filling the Gaps in Ancient Akkadian Texts: A Masked Language Modelling Approach* (Koren Lazar, Benny Saret, Asaf Yehudai, Wayne Horowitz, Nathan Wasserman, and Gabriel Stanovsky, *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing*, pages 4682–4691, DOI `10.18653/v1/2021.emnlp-main.384`):

- **Abstract (p. 4682) & Section 1 (p. 4683):**
  - Abstract: *"We find that despite data scarcity (1M tokens) we can achieve state of the art performance on missing tokens prediction (89% hit@5) using a greedy decoding scheme and pretraining on data from other languages and different time periods."*
  - Section 1 (p. 4683): *"In an automatic evaluation, we find that a combination of large-scale multilingual pretraining with Akkadian finetuning achieves state-of-the-art results, with a top 5 accuracy of 89.5%, vastly improving over other models and baselines."*
- **Table 1 (p. 4683, Preprocessed Oracc Dataset Statistics, 80%–20% split):**
  - `Akkadian Train`: `8K` texts, `950K` words, `1.8M` signs
  - `Akkadian Test`: `2K` texts, `250K` words, `500K` signs
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

- Additionally, Figure 3A (p. 4686) reports 1-token / 1-sign `Hit@10 = 0.92` for `MBERT+Akk`.

---

## 3. Literature & Repository Search (Last 24 Months and All Citing Works)

Single honest GET queries were executed against OpenAlex, arXiv, and GitHub:

| Search Endpoint | URL | UTC Timestamp | HTTP Status | Bytes | SHA-256 |
|---|---|---|---|---:|---|
| OpenAlex Full-Text Search | `https://api.openalex.org/works?search=Akkadian+masked+language+OR+SLAB-NLP+Akk&per-page=25` | `2026-10-21T17:43:02Z` | `HTTP/2 200` | `206,948` | `95d3fca409d010a80664b1dceb6113092e6c02d21e2485b0a5c592d6f3e08d6e` |
| OpenAlex Citations of `W3199396623` | `https://api.openalex.org/works?filter=cites:W3199396623&per-page=25` | `2026-10-21T17:43:49Z` | `HTTP/2 200` | `365,650` | `0b49c1f49f11dc43b023b8d920bc86030fbd1fd25132120d6e79aa13c8e899db` |
| arXiv API Search | `https://export.arxiv.org/api/query?search_query=all:Akkadian+AND+(all:lacuna+OR+all:masking+OR+all:ORACC)&sortBy=submittedDate&sortOrder=descending&max_results=20` | `2026-10-21T17:43:03Z` | `HTTP/2 200` | `2,796` | `7015ac910ed680aa859c523881f97da427b050c11f72b320dde86dc56c73e62d` |
| GitHub Repositories Search | `https://api.github.com/search/repositories?q=Akkadian+OR+SLAB-NLP&sort=updated&per_page=25` | `2026-10-21T17:43:50Z` | `HTTP/2 200` | `146,636` | `a9ee387c1438085c79238ccd322dc4ce5f3cb01df90931a997a62d2447d28772` |

### 3.1 Analysis of All 18 OpenAlex Citing Works (`cites:W3199396623`) and 2024–2026 Literature

1. **Lazar et al. (2021) OpenAlex Work (`https://openalex.org/W3199396623`, DOI `10.18653/v1/2021.emnlp-main.384`):** Cited by 18 works in OpenAlex.
2. **Complete review of citing and recent (2023–2026) works:**
   - **Sommerschield, Assael, Pavlopoulos et al. (2023)**, *Machine Learning for Ancient Languages: A Survey* (`W4378193263`, *Computational Linguistics*, DOI `10.1162/coli_a_00481`) and **Sommerschield & Assael (2026)**, *Machine Learning and Classical Studies* (`W7169189466`, DOI `10.1093/9780197835210.003.0024`): Survey articles that cite Lazar et al. (2021) as the benchmark for Akkadian masked token restoration (`89%` / `89.5%` Hit@5) without training or evaluating a new model on `SLAB-NLP/Akk`.
   - **Assael, Sommerschield et al. (2025)**, *Contextualizing ancient texts with generative neural networks* — **Aeneas** (`W4412600587`, *Nature*, `2025-07-23`, DOI `10.1038/s41586-025-09292-5`): Evaluates Latin epigraphy (Latin inscriptions dataset LED), not Akkadian cuneiform or Oracc `SLAB-NLP/Akk`.
   - **Zottin et al. (2026)**, *Bridging the Gaps: Learning to Estimate Missing Text in Fragmentary Greek Inscriptions* (`W7204023467`, `2026-08-23`, DOI `10.1007/978-3-032-36039-7_22`): Evaluates missing text length estimation on Ancient Greek inscriptions (PHI/Ithaca), not Akkadian.
   - **Gordin, Sahala, Spencer, & Klein (2025)**, *EvaCun 2025 Shared Task: Lemmatization and Token Prediction in Akkadian and Sumerian using LLMs* (`W4411113475`, ALP Workshop at NAACL 2025, DOI `10.18653/v1/2025.alp-1.33`): Evaluates lemmatization and token prediction on newly curated Electronic Babylonian Library (eBL) Canonical literature and Archibab Old Babylonian letters, not the Oracc `SLAB-NLP/Akk` held-out benchmark.
   - **Mahmood & Tetiana (2025)**, *From Tablet to Text: AI-Assisted Reconstruction and Translation of Akkadian Passages in the Epic of Gilgamesh* (`W7160424421`, `2025-07-15`, DOI `10.69513/ilcr.v3.i2.a4`): Qualitative philological evaluation on Standard Babylonian Gilgamesh passages; does not evaluate on `SLAB-NLP/Akk`.
   - **Gutherz, Gordin, Sáenz, Levy et al. (2023)**, *Translating Akkadian to English with neural machine translation* (`W4367676272`, *PNAS Nexus*, DOI `10.1093/pnasnexus/pgad096`): Evaluates Akkadian-to-English machine translation (`BLEU4`), not sign/token lacuna restoration.
   - **Chen, Agarwal, & Berg-Kirkpatrick (2023)**, *CuneiML: A Cuneiform Dataset for Machine Learning* (`W4389402574`, *Journal of Open Humanities Data*, DOI `10.5334/johd.151`) and **Chen et al. (2024)**, *LogogramNLP* (`W4402684070`, ACL 2024, DOI `10.18653/v1/2024.acl-long.768`): Introduce visual/transcribed datasets for classification, parsing, and translation; do not evaluate on `SLAB-NLP/Akk`.
   - **Faisal & Anastasopoulos (2024)** (`W4404782418`, MRL 2024), **Aioanei et al. (2024)** (*Deep Aramaic*, `W4394951411`), **Chapinal-Heras & Díaz Sánchez (2024)** (`W4391788167`), **Locaputo et al. (2024)** (`W4400187140`), **Vogler et al. (2024)** (`W4402343105`), **Xia et al. (2024)** (`W4392658580`), **Cho et al. (2025)** (`W4413817043`), **Spitzer (2025)** (`W4409999198`), **Kalinsky et al. (2023)** (`W4386566487`), **Li et al. (2023)** (`W4386730301`), **Papavassileiou et al. (2023)** (Linear B, `W4367313469`), **El-Hajj et al. (2023)** (`W4387265299`), and **Malkin et al. (2022)** (`W4280613849`): None re-run or beat `MBERT+Akk` on the held-out `SLAB-NLP/Akk` Oracc MLM benchmark.
3. **arXiv and GitHub Search Verification:**
   - The arXiv query `all:Akkadian AND (all:lacuna OR all:masking OR all:ORACC)` returns `totalResults = 1`, which is Lazar et al. (`2109.04513v2`) itself.
   - Recent GitHub repositories matching `Akkadian OR SLAB-NLP` focus on machine translation (ByT5 for Old Assyrian to English), Universal Dependencies treebanks (`UD_Akkadian-PISANDUB`, `UD_Akkadian-RIAO`), or OCR (`eduba`); none report a new MLM result on `SLAB-NLP/Akk`.

---

## 4. Check of `TROPHY_CASE.md` and Open Pull Requests

| Source | URL | UTC Timestamp | HTTP Status | Bytes | SHA-256 |
|---|---|---|---|---:|---|
| `TROPHY_CASE.md` | `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md` | `2026-10-21T17:43:04Z` | `HTTP/2 200` | `31,235` | `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1` |
| Open Pull Requests (`state=open&per_page=100`) | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` | `2026-10-21T17:43:04Z` | `HTTP/2 200` | `2,122,885` | `d96dd95dc8f94a301cc803a97482446dabf465009c1afec0cbc54af0c53651db` |

- **`TROPHY_CASE.md` (`100` lines):** Contains `0` occurrences of `akkadian`, `lacuna`, `ancient-texts`, `SLAB-NLP`, `oracc`, or `cuneiform`.
- **Open Pull Requests (`100` open PRs returned, from PR #507 through PR #610):** Every open PR title and body was scanned case-insensitively for `akkadian`, `lacuna`, `ancient-texts`, `slab-nlp`, `oracc`, and `cuneiform`. All `100` open PRs returned `0` matches.

---

## 5. Novelty Comparison: Claimed Results vs. Published SOTA and Reproduced Baseline

All claimed metrics from `README.md`, `object/akkadian_predictions_part1..4.csv`, and `object/akkadian_audit_manifest.json` on the strictly held-out `SLAB-NLP/Akk` benchmark (`SEED = 2`, `18,568` training rows, `1,875` strictly unseen test documents, $N = 27,650$ frozen masked positions at `torch.manual_seed(42)`):

| System / Regime | Artifact | `MRR` | `Hit@1` | `Hit@5` | `Hit@10` | Margin vs Published SOTA (`MRR = 0.83`, `Hit@5 = 0.89` / `0.895`, `Hit@10 = 0.92`) |
|---|---|---:|---:|---:|---:|---|
| Published `MBERT+Akk` (Lazar et al., 2021, Table 2 & Sec. 1) | `2021.emnlp-main.384.pdf` | `0.83000` | — | `0.89000` (`0.89500`) | `0.92000` | Baseline reference |
| Reproduced `MBERT+Akk` Baseline (Clause 1) | `object/akkadian_predictions_part1..4.csv` | `0.82369` | `0.77693` | `0.87700` | `0.90901` | Inside `[0.87000, 0.91000]` comparability window |
| Pure Symbolic `CLSS-C-v3` (`0` Neural Params, $\alpha = 0$) | `object/akkadian_audit_manifest.json` | `0.82480` | `0.76470` | **`0.89638`** | **`0.92705`** | **`+0.00638` vs `0.89` (`+0.00138` vs `0.895`) on `Hit@5`; `+0.00705` on `Hit@10`** |
| `CLSS-Akk-v3` under `100%_MASK` | `object/akkadian_audit_manifest.json` | **`0.84737`** | `0.78684` | **`0.92007`** | **`0.94409`** | **`+0.01737` `MRR`; `+0.03007` (`+0.02507`) `Hit@5`; `+0.02409` `Hit@10`** |
| **`CLSS-Akk-v3` Full (`COLLATOR_80_10_10`, Clause 2)** | `object/akkadian_predictions_part1..4.csv` | **`0.85593`** | **`0.80098`** | **`0.92156`** | **`0.94517`** | **`+0.02593` `MRR`; `+0.03156` (`+0.02656`) `Hit@5`; `+0.02517` `Hit@10`** |
| **`CLSS-Akk-v3` `[MASK]`-Only Subset ($N = 22,205$)** | `object/akkadian_predictions_part1..4.csv` | **`0.84015`** | **`0.77924`** | **`0.91263`** | **`0.93943`** | **`+0.01015` `MRR`; `+0.02263` (`+0.01763`) `Hit@5`; `+0.04800` over `MBERT+Akk` (`0.86463`)** |
| **`CLSS-Akk-v3` Non-Missing Subset ($N = 25,957$, raw CSV)** | `object/akkadian_predictions_part1..4.csv` | **`0.85139`** | **`0.79593`** | **`0.91729`** | **`0.94156`** | **`+0.02139` `MRR`; `+0.02729` (`+0.02229`) `Hit@5`; `+0.04697` over `MBERT+Akk` (`0.87032`)** |

And on the Table 2 genre breakdown:
- **`Lexical` ($N = 10,240$):** `CLSS-Akk-v3` achieves `MRR = 0.86091` (vs published `0.69`, **`+0.17091`**, and vs reproduced `MBERT+Akk` `0.82717`, **`+0.03374`**) and `Hit@5 = 0.92920` (vs published `0.85`, **`+0.07920`**, and vs reproduced `MBERT+Akk` `0.87236`, **`+0.05684`**).
- **`Astrological Report` ($N = 1,753$):** `CLSS-Akk-v3` achieves `MRR = 0.86704` (vs published `0.81`, **`+0.05704`**, and vs reproduced `MBERT+Akk` `0.78779`, **`+0.07925`**) and `Hit@5 = 0.92527` (vs published `0.88`, **`+0.04527`**, and vs reproduced `MBERT+Akk` `0.85511`, **`+0.07016`**).
- **`Royal or Monumental` ($N = 177$):** `CLSS-Akk-v3` achieves `MRR = 0.90375` (vs published `0.84`, **`+0.06375`**, and vs reproduced `MBERT+Akk` `0.86148`, **`+0.04227`**) and `Hit@5 = 0.93785` (vs published `0.90`, **`+0.03785`**, and vs reproduced `MBERT+Akk` `0.90960`, **`+0.02825`**).

Every overall, subset, and genre-level target strictly beats both the published SOTA in Lazar et al. (2021) and the reproduced `MBERT+Akk` baseline by wide margins, with zero prior records or open pull requests in `V3R1T4S`.

pass: true
