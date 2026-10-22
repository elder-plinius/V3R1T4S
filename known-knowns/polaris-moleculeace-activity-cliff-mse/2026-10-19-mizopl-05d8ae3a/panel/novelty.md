# Panelist Report: NOVELTY (`polaris-moleculeace-activity-cliff-mse`)

context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)

## 1. Mandate & Scope

Per the V3R1T4S novelty mandate:
> *"Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value and time. Search the last 24 months of literature, this repo's TROPHY_CASE.md and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record."*

This audit was executed in a fresh subagent context reading strictly from `claim/CLAIM.md`, `claim/REPRODUCE.md`, `claim/CHEMBL287_Ki_manifest.json`, `claim/moleculeace_30_sweep_manifest.json`, and `claim/MoleculeACE_results.csv`, paired with single honest HTTP `GET` fetches (`curl -sS -D ... -A "V3R1T4S-research-agent (honest single fetch)"`) of the live Polaris API, live Polaris benchmark leaderboard pages, arXiv API and HTML papers, OpenAlex API, GitHub repository search APIs, and the live V3R1T4S `TROPHY_CASE.md` and open pull requests endpoints.

---

## 2. Honest Single Fetches of Live Polaris API & Leaderboard Pages

Each live Polaris endpoint was fetched exactly once with zero retries. Below are the exact URLs, UTC timestamps (`date -u`), HTTP status codes, byte lengths, `sha256` digests, and extracted leaderboard records:

| Endpoint Type | URL | UTC Fetch Time | HTTP Status | Bytes | SHA-256 Digest | Extracted Live Data / Leaderboard Entries |
|---|---|---|---|---:|---|---|
| Primary Polaris Benchmark API | `https://polarishub.io/api/v1/benchmark/molecularml/moleculeace-chembl287-ki` | `2026-10-19T15:07:25Z` | `HTTP/2 200` | `8,023` | `444c87a326f4a92621fd7fad88704f11c6a8a64e8e747a1f263e899390054593` | `name = "moleculeace-CHEMBL287-Ki"`, `nTrainDatapoints = 1061`, `nTestDatapoints = {"test": 267}`, `targetCols = ["y"]`, `mainMetric = "mean_squared_error"`, exact 1,061 train and 267 test indices matching `claim/CHEMBL287_Ki_manifest.json` |
| Primary Headline Leaderboard Page (`CHEMBL287_Ki`) | `https://polarishub.io/benchmarks/molecularml/moleculeace-chembl287-ki` | `2026-10-19T15:07:54Z` | `HTTP/2 200` | `156,554` | `af074d1acad331e811eef5f662e90d07109146dbe676ed9996e47c502b25b55f` | 1 listed entry: `autosota-moleculeace-chembl287-ki` with `mean_squared_error = 0.5031813063290076` (`RMSE = 0.70935274`) |
| Multi-Entry Leaderboard Page (`CHEMBL234_Ki`) | `https://polarishub.io/benchmarks/molecularml/moleculeace-chembl234-ki` | `2026-10-19T15:07:55Z` | `HTTP/2 200` | `164,720` | `cb50c81480230367bdb0febeac7fd88670ce9949a2b6eff4279085ec5d84f51e` | 3 listed entries: (1) `autosota-moleculeace-chembl234-ki` (`mean_squared_error = 0.37022063353143536`), (2) `aether-pharmaos-chembl234-ki-ensemble` (`mean_squared_error = 0.40363769296273044`), (3) `MolEncoder` (`mean_squared_error = 0.49614280994488874`) |
| Multi-Entry Leaderboard Page (`CHEMBL236_Ki`) | `https://polarishub.io/benchmarks/molecularml/moleculeace-chembl236-ki` | `2026-10-19T15:07:56Z` | `HTTP/2 200` | `164,711` | `880f969504c2acaa867d7b5adb36cfde9e29641fc96ba2ec945c586855b3fb3b` | 3 listed entries: (1) `autosota-moleculeace-chembl236-ki` (`mean_squared_error = 0.4496849288681984`), (2) `aether-pharmaos-chembl236-ki-ensemble` (`mean_squared_error = 0.4703740102898284`), (3) `MolEncoder` (`mean_squared_error = 0.7274940482755294`) |
| Cliff Benchmark Leaderboard Page (`CHEMBL219_Ki`) | `https://polarishub.io/benchmarks/molecularml/moleculeace-chembl219-ki` | `2026-10-19T15:07:57Z` | `HTTP/2 200` | `156,552` | `85cb6a6e8b842fb9dfbbb3d8028c2f9feda74cc6017f12d031ad5b7a2dc0bcbc` | 1 listed entry: `autosota-moleculeace-chembl219-ki` with `mean_squared_error = 0.4687070545630029` |
| Cliff Benchmark Leaderboard Page (`CHEMBL204_Ki`) | `https://polarishub.io/benchmarks/molecularml/moleculeace-chembl204-ki` | `2026-10-19T15:07:57Z` | `HTTP/2 200` | `156,589` | `3217311b5f51ce8e249dc052dc0b74544cba4e33e64af8189796ccacd61207bf` | 1 listed entry: `autosota-moleculeace-chembl204-ki` with `mean_squared_error = 0.48515433936939145` |
| Cliff Benchmark Leaderboard Page (`CHEMBL244_Ki`) | `https://polarishub.io/benchmarks/molecularml/moleculeace-chembl244-ki` | `2026-10-19T15:07:58Z` | `HTTP/2 200` | `156,588` | `1542ec784af609aeb5b65381a1163bc6a02463e6685577df2aba994e1b30436b` | 1 listed entry: `autosota-moleculeace-chembl244-ki` with `mean_squared_error = 0.4749981512616306` |

### Comparison Against Live Polaris Leaderboard Entries & Official MoleculeACE Paper (`claim/MoleculeACE_results.csv`)

We verified `claim/MoleculeACE_results.csv` (`36,991` bytes, `sha256: 6aa88c897f16bbb328793a2917289e3972b3fc8b50cc56be840f6714ea9baae5`, van Tilborg et al., *Journal of Chemical Information and Modeling* 2022, 720 rows = 30 targets $\times$ 24 model-descriptor combinations):

| Target (`slug`) | Live Polaris Best MSE | MoleculeACE Paper Best Overall MSE (Method) | Claimed CLSS Overall MSE (`rel_impr` vs Polaris / vs Paper) | MoleculeACE Paper Best Cliff MSE (Method) | Claimed CLSS Cliff MSE (`rel_impr` vs Paper Cliff Best) | Strictly Beats All Listed Entries? |
|---|---:|---:|---:|---:|---:|---|
| **`CHEMBL287_Ki`** (`moleculeace-chembl287-ki`) | **`0.50318131`** (1 entry) | **`0.51009699`** (`SVM+ECFP`, `RMSE = 0.714211`) | **`0.40802135`** (**`-18.9117%`** / **`-20.0110%`**) | **`0.61875106`** (`RF+PHYSCHEM` / `MLP+ECFP`, `RMSE = 0.786607`) | **`0.50213600`** (**`-18.8468%`**) | **YES (strict record)** |
| **`CHEMBL234_Ki`** (`moleculeace-chembl234-ki`) | **`0.37022063`** (3 entries) | **`0.38646355`** (`SVM+ECFP`, `RMSE = 0.621662`) | **`0.36037801`** (**`-2.6586%`** / **`-6.7498%`**) | **`0.39920182`** (`SVM+ECFP`, `RMSE = 0.631824`) | **`0.37651009`** (**`-5.6843%`**) | **YES (beats all 3 entries)** |
| **`CHEMBL236_Ki`** (`moleculeace-chembl236-ki`) | **`0.44968493`** (3 entries) | **`0.48471536`** (`GBM+ECFP`, `RMSE = 0.696215`) | **`0.44350711`** (**`-1.3738%`** / **`-8.5015%`**) | **`0.62749623`** (`RF+ECFP`, `RMSE = 0.792147`) | **`0.57538859`** (**`-8.3041%`**) | **YES (beats all 3 entries)** |
| **`CHEMBL219_Ki`** (`moleculeace-chembl219-ki`) | **`0.46870705`** (1 entry) | **`0.50354978`** (`SVM+ECFP`, `RMSE = 0.709612`) | **`0.41121465`** (**`-12.2662%`** / **`-18.3368%`**) | **`0.58465090`** (`GBM+ECFP`, `RMSE = 0.764625`) | **`0.46940348`** (**`-19.7122%`**) | **YES (strict record)** |
| **`CHEMBL204_Ki`** (`moleculeace-chembl204-ki`) | **`0.48515434`** (1 entry) | **`0.52291827`** (`SVM+ECFP`, `RMSE = 0.723131`) | **`0.42704071`** (**`-11.9784%`** / **`-18.3351%`**) | **`0.73755916`** (`SVM+ECFP`, `RMSE = 0.858813`) | **`0.65130003`** (**`-11.6952%`**) | **YES (strict record)** |
| **`CHEMBL244_Ki`** (`moleculeace-chembl244-ki`) | **`0.47499815`** (1 entry) | **`0.51144897`** (`SVM+ECFP`, `RMSE = 0.715157`) | **`0.43389566`** (**`-8.6532%`** / **`-15.1634%`**) | **`0.63457383`** (`SVM+ECFP`, `RMSE = 0.796601`) | **`0.55421912`** (**`-12.6628%`**) | **YES (strict record)** |

Across the complete 30-benchmark suite (`claim/moleculeace_30_sweep_manifest.json`, `sha256: 42c12361b8406c2530934bbed45a1acf701e4e03b50514a44f1dd056c17405e8`), the single fixed CPU recipe strictly beats the live Polaris leaderboard best MSE on **29 of 30** benchmarks (including both multi-entry leaderboards `moleculeace-chembl234-ki` and `moleculeace-chembl236-ki`), achieves $\ge 5.0\%$ relative MSE improvement and $\ge 95.0\%$ paired bootstrap win rate simultaneously on **21 of 30** benchmarks, strictly beats the MoleculeACE paper best overall MSE across all 24 methods on **28 of 30** benchmarks, and strictly beats the MoleculeACE paper best cliff MSE on **21 of 30** benchmarks.

---

## 3. Literature & Repository Audit (Last 24 Months: 2024–2026)

Every search endpoint below was queried with a single honest HTTP `GET` request:

| Source | Query URL | UTC Fetch Time | HTTP Status | Bytes | SHA-256 Digest | Summary of Findings |
|---|---|---|---|---:|---|---|
| arXiv API (Search) | `https://export.arxiv.org/api/query?search_query=all:MoleculeACE&sortBy=submittedDate&sortOrder=descending&max_results=25` | `2026-10-19T15:09:53Z` | `HTTP/2 200` | `12,874` | `f4a37020b925597bb67a0ce06c6d80a759662230b8c34843ab8fd8e9cecb2430` | 5 matching preprints (`2609.38744v1`, `2604.16123v2`, `2601.02530v3`, `2506.15792v2`, `2402.13779v1`) |
| arXiv API (IDs) | `https://export.arxiv.org/api/query?id_list=2608.18982,2502.11572,2609.38744,2604.16123,2506.15792` | `2026-10-19T15:11:10Z` | `HTTP/2 200` | `12,141` | `2e6b93a0cbdb94db4336e9ed5d7d4307161151dad21809d829358f078fc12fc5` | Metadata and abstracts for `arXiv:2608.18982v1` (Monroe, Aug 2026) and recent TFM/MFM preprints |
| arXiv HTML (`2608.18982v1`) | `https://arxiv.org/html/2608.18982v1` | `2026-10-19T15:11:55Z` | `HTTP/2 200` | `560,274` | `05432a908d2c3073b17f4321e89b9242a10fec73b23ce6c4d27a850822555cbf` | Full text & Table 1 of *Monroe: A Molecular Foundation Model for In-Context Probabilistic Inference* (Aug 19, 2026) |
| arXiv HTML (`2609.38744v1`) | `https://arxiv.org/html/2609.38744v1` | `2026-10-19T15:11:56Z` | `HTTP/2 200` | `673,957` | `81c05fcacf6055cd4fe0adf7ccfeb96fa99a01603dbe1f8da1a70b1ba44411eb` | Full text of *MolPAIR* (Sep 30, 2026; structural-shift re-splits, mean RMSE `0.8749`–`0.8850`, mean cliff RMSE `0.9565`) |
| arXiv HTML (`2604.16123v2`) | `https://arxiv.org/html/2604.16123v2` | `2026-10-19T15:11:57Z` | `HTTP/2 200` | `548,837` | `4f97a0cba788a85a0d1f2c3313fa9899f5361cdb45849cd1d7f8ccd626fa42bf` | Full text of *Tabular foundation models for in-context prediction of molecular properties* (Apr 17, 2026; 5-repeat random 80/20 splits) |
| arXiv HTML (`2506.15792v2`) | `https://arxiv.org/html/2506.15792v2` | `2026-10-19T15:11:58Z` | `HTTP/2 200` | `182,541` | `43b57fccd815439d98eb5cc5b7be1f25ff068e78927fa0e4b41fd00579442b56` | Full text of *CheMeleon: Deep Learning Foundation Models from Classical Molecular Descriptors* (Jun 18, 2025) |
| OpenAlex Works Search | `https://api.openalex.org/works?search=MoleculeACE&per-page=25` | `2026-10-19T15:09:54Z` | `HTTP/2 200` | `482,979` | `9d10cf19b38cb54d23552cf00e345478dfc3e98f310ff4e094c4ef3518bf398b` | 63 total works indexed; top 25 inspected including `GraphCliff` (`2026-08-07`, `https://doi.org/10.1145/3770855.3818898`), `Monroe` (`2026-08-19`), `MolPAIR` (`2026-09-30`), `MaskMol` (`2024-09-02`), and `SQRL` (`2025-01-15`) |
| GitHub Repo Search (`MoleculeACE`) | `https://api.github.com/search/repositories?q=MoleculeACE` | `2026-10-19T15:09:56Z` | `HTTP/2 200` | `45,154` | `4f16fed836cb7d3e7c1d7a3a0e856cdcf5a4d7b407a9faaa69bbc7397e5d4b07` | `total_count = 8` repositories (`MoleculeACE`, `moleculeace-feedstock`, `benchmark_gp`, `moleculeace-serialization-audit`, `MoleculeACE_Re`, `MoleculeACE_GCN_Implementation`, `GraphCliff-XACs`, `litmus`); none beat our `CHEMBL287_Ki` or 30-target MSE |
| GitHub Repo Search (`moleculeace-chembl287-ki`) | `https://api.github.com/search/repositories?q=moleculeace-chembl287-ki` | `2026-10-19T15:10:25Z` | `HTTP/2 200` | `55` | `4af480b8ee5b87b369a76c49bd22c9a783908272ebffbe97898f8ab0f0772a5f` | `total_count = 0` repositories |

### Detailed Comparison Against 2024–2026 Literature Benchmarks

1. **Comparison on `CHEMBL287_Ki` (`moleculeace-chembl287-ki`):**
   - No paper or repository in the 2024–2026 literature reports a test-set MSE on the official `CHEMBL287_Ki` split lower than the live Polaris leaderboard best (`0.50318131`, `RMSE = 0.709353`) or the MoleculeACE paper best (`SVM+ECFP` `MSE = 0.51009699`, `RMSE = 0.714211`; cliff best `MSE = 0.61875106`, `RMSE = 0.786607`).
   - Our single fixed CPU recipe (`claim/CHEMBL287_Ki_test_predictions.csv`, `sha256: 05d8ae3a3797f666ed320364280c2ba0c099417174d42a0a4736f0366726623c`) achieves overall `MSE = 0.40802135` (`RMSE = 0.638765`, **`-18.9117%`** below Polaris best and **`-20.0110%`** below MoleculeACE paper best) and cliff `MSE = 0.50213600` (`RMSE = 0.708616`, **`-18.8468%`** below MoleculeACE paper cliff best).
   - Notably, Table 9 of `arXiv:2608.18982v1` (*Monroe*, Aug 2026) specifically documents why standard achiral fingerprints fail on `CHEMBL287_Ki` (`SOR`, Sigma opioid/intracellular receptor, `103` cliff molecules, `164` non-cliff molecules): **`40.4%` of molecules contain `R/S` tetrahedral stereocenters and `1.5%` contain `E/Z` stereobonds**, which standard achiral `ECFP` collapses completely.

2. **30-Target Macro-Average Comparison Against Recent Papers (`Monroe`, `CheMeleon_PFN`, `MiniMol_PFN`, `CheMeleon`, `GraphCliff`, `SVM+ECFP`):**
   - Under the bank's `success_criterion` clause (d), *"The model must be fit on the official train split only; multi-target transfer is allowed only from OTHER MoleculeACE targets' train splits."* External pre-training on millions of molecules outside MoleculeACE (such as `Monroe`'s 81M-molecule PM6 + PCBA pre-training or `CheMeleon`'s 1M-molecule pre-training) is disallowed by the bank rule.
   - Even when compared directly against all methods reported in Table 1 of `arXiv:2608.18982v1` (`https://arxiv.org/html/2608.18982v1`, Aug 19, 2026) and `GraphCliff` (Aug 2026) on the 30 MoleculeACE benchmarks, our single fixed CPU-only CLSS recipe trained strictly on each target's own official `split == 'train'` (`zero` external pre-training) achieves the **lowest 30-target mean Activity-Cliff RMSE (`0.7211`) of any known method**:

| Method | External Pre-Training Data | Allowed by Bank Rule (d)? | 30-Target Mean Overall RMSE | 30-Target Mean Activity-Cliff RMSE |
|---|---|---|---:|---:|
| **`CLSS` (Ours, `claim/run_clss_moleculeace.py`)** | **None (`0` external molecules; official `split == 'train'` only)** | **YES** | **`0.6303`** (`MSE = 0.4020`) | **`0.7211`** (`MSE = 0.5298`) |
| `SVM+ECFP` (van Tilborg et al., *JCIM* 2022 best overall baseline) | None (`0` external molecules) | YES | `0.6712` | `0.7511` |
| `GBM+ECFP` (van Tilborg et al., *JCIM* 2022) | None (`0` external molecules) | YES | `0.6948` | `0.7835` |
| `RF+ECFP` (van Tilborg et al., *JCIM* 2022) | None (`0` external molecules) | YES | `0.7000` | `0.7857` |
| `GraphCliff` (2026, short-long range gating GNN) | None (`0` external molecules) | YES | `0.665` | `0.757` |
| `Monroe` (`arXiv:2608.18982v1` Table 1, Aug 2026, MFM + TabPFN) | 81,000,000 PM6 molecules + PCBA | NO (external pre-training) | `0.629 ± 0.004` | `0.737 ± 0.006` |
| `CheMeleon_PFN` (`arXiv:2608.18982v1` Table 1, Aug 2026) | 1,000,000 PubChem molecules | NO (external pre-training) | `0.641 ± 0.013` | `0.741 ± 0.020` |
| `MiniMol_PFN` (`arXiv:2608.18982v1` Table 1, Aug 2026) | 6,000,000 ChEMBL/PubChem molecules | NO (external pre-training) | `0.642 ± 0.004` | `0.760 ± 0.008` |
| `CheMeleon` (`arXiv:2506.15792v2` / `2608.18982v1` Table 1) | 1,000,000 PubChem molecules | NO (external pre-training) | `0.662 ± 0.016` | `0.760 ± 0.026` |
| `MiniMol` (`arXiv:2608.18982v1` Table 1) | 6,000,000 ChEMBL/PubChem molecules | NO (external pre-training) | `0.703 ± 0.018` | `0.794 ± 0.031` |
| `MolFormer` (`arXiv:2608.18982v1` Table 1) | 100,000,000 ZINC/PubChem molecules | NO (external pre-training) | `0.748 ± 0.018` | `0.854 ± 0.027` |

---

## 4. V3R1T4S `TROPHY_CASE.md` & Open Pull Requests Audit

We performed single honest `GET` requests for `TROPHY_CASE.md` and all three pages of open pull requests on `elder-plinius/V3R1T4S` (covering all `259` open pull requests from `#9` through `#567`):

| Resource | URL | UTC Fetch Time | HTTP Status | Bytes | SHA-256 Digest | Result |
|---|---|---|---|---:|---|---|
| `TROPHY_CASE.md` | `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md` | `2026-10-19T15:09:57Z` | `HTTP/2 200` | `31,235` | `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1` | `0` occurrences of `polaris-moleculeace-activity-cliff-mse`, `moleculeace`, `chembl287`, or `polaris` |
| Open PRs (Page 1: `#467`–`#567`, 100 PRs) | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` | `2026-10-19T15:09:58Z` | `HTTP/2 200` | `2,137,846` | `a38b658a7f3354f4a23c479350ed0c441f3aa026186e07b2a8d06949188a75e7` | `0 / 100` open PRs reference `polaris-moleculeace-activity-cliff-mse`, `moleculeace`, `chembl287`, or `activity-cliff` |
| Open PRs (Page 2: `#365`–`#466`, 100 PRs) | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=2` | `2026-10-19T15:11:11Z` | `HTTP/2 200` | `2,211,468` | `e9d985af4675b0569ca85bb693135b0a12523ce0c55e043311d3a17ceee4d620` | `0 / 100` open PRs reference `polaris-moleculeace-activity-cliff-mse`, `moleculeace`, `chembl287`, or `activity-cliff` |
| Open PRs (Page 3: `#9`–`#364`, 59 PRs) | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=3` | `2026-10-19T15:11:13Z` | `HTTP/2 200` | `1,139,793` | `fbc901780ac66c27c3d8fb50667bd37d7ff82ff24ad963656bd0ddf6996a878d` | `0 / 59` open PRs reference `polaris-moleculeace-activity-cliff-mse`, `moleculeace`, `chembl287`, or `activity-cliff` |

---

## 5. Novelty Verdict

1. **Live Polaris Leaderboard Strictly Beaten:** On the primary headline benchmark `moleculeace-chembl287-ki` (`CHEMBL287_Ki`), our test-set `mean_squared_error = 0.40802135` strictly beats the live Polaris leaderboard best (`0.50318131`, `-18.9117%` relative MSE reduction) and the MoleculeACE paper best (`0.51009699`, `-20.0110%` relative MSE reduction). Across all 30 MoleculeACE benchmarks, the single fixed recipe beats the live Polaris leaderboard best on **29 of 30** benchmarks (including both 3-entry leaderboards `moleculeace-chembl234-ki` at `0.36037801 < 0.37022063` and `moleculeace-chembl236-ki` at `0.44350711 < 0.44968493`) and achieves $\ge 5.0\%$ relative MSE margin + $\ge 95.0\%$ paired bootstrap win rate simultaneously on **21 of 30** benchmarks.
2. **Activity-Cliff Subset & 2024–2026 Literature Strictly Beaten:** On `CHEMBL287_Ki` activity-cliff molecules (`cliff_mol == 1`, $n = 103$), our cliff `MSE = 0.50213600` (`RMSE = 0.708616`) strictly beats the MoleculeACE paper best cliff MSE (`0.61875106`, `-18.8468%`) and reproduced `SVM+ECFP` (`0.65858689`, `-23.7555%`). Across all 30 targets, our 30-target mean Activity-Cliff RMSE of **`0.7211`** (with zero external pre-training) strictly beats `SVM+ECFP` (`0.7511`), `GraphCliff` (`0.757`, Aug 2026), `CheMeleon` (`0.760`, Jun 2025), `MiniMol_PFN` (`0.760`, Aug 2026), `CheMeleon_PFN` (`0.741`, Aug 2026), and even the 81M-molecule pre-trained foundation model `Monroe` (`0.737`, Aug 2026).
3. **Unclaimed in V3R1T4S:** Neither `TROPHY_CASE.md` nor any of the `259` open pull requests (`#9`–`#567`) touches `polaris-moleculeace-activity-cliff-mse`.

pass: true
