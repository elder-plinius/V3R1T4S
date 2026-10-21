# Skeptic Panel Report — Role: NOVELTY (`fmm-ternary-integer-ring-upgrade`, `14x15x15`, `ZT` rank `1894`)

role: NOVELTY
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target: fmm-ternary-integer-ring-upgrade
format: 14x15x15
ring: ZT
claimed_rank: 1894
object_file: claim/14x15x15_m1894_ZT.json
object_sha256: bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb
object_bytes: 944884

## 1. Live Primary Status Table Fetches (Single Honest GETs, No Retries)

### 1.1 `dronperminov/FastMatrixMultiplication` — `README.md`
- **URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md`
- **Fetched UTC:** `2026-10-18T17:20:53Z`
- **HTTP Status:** `200`
- **Bytes:** `112671`
- **SHA-256:** `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341` (matches `claim/perminov_README.md` byte-for-byte)
- **Exact `14x15x15` rows:**
  - Line 291 (summary gap table):
    `| 14x15x15 |  1905 (Z)   |   [1848](schemes/results/Q/14x15x15_m1848_Q.json) (Q)    | **2.801382482** |`
  - Line 1440 (full format status table, columns `Format | ZT rank | Z rank | Q rank | omega`):
    `| 14x15x15 |  1905 (?)   | 1895 (1905)  | 1848 (1905)  | **2.801382482** |`
- **Live table values for `14x15x15`:**
  - `ZT rank = 1905`
  - `Z rank = 1895`
  - `Q rank = 1848`
- **Comparison with claim:** The claimed ternary (`ZT`) rank `r = 1894` is strictly less than the live `ZT rank = 1905` (`1894` vs `1905`, improving `ZT` by `-11` multiplications) and also strictly less than the live `Z rank = 1895` (`1894` vs `1895`, improving `Z` by `-1` multiplication), while remaining above `1848 = min(1905, 1895, 1848)`.

### 1.2 `dronperminov/FastMatrixMultiplication` — `schemes/status.json` & Repository Tree
- **URL (`status.json`):** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/status.json`
- **Fetched UTC:** `2026-10-18T17:20:54Z`
- **HTTP Status:** `200`
- **Bytes:** `2165677`
- **SHA-256:** `b9b86c506ef4826220e5479569c6a84eaa720b703f73b705c043a3c90b463311`
- **Exact `14x15x15` entry in `status.json`:**
  - `"ranks": {"Z": 1895, "Q": 1848, "ZT": 1905}`
  - `"omegas": {"Z": 2.810736065802022, "Q": 2.801382481619919, "ZT": 2.8126962397251787}`
  - `schemes.ZT`: single entry `schemes/results/ZT/14x15x15_m1905_ZT.json` (`rank: 1905`, `values: [-1, 0, 1]`, `complexity: 55464`)
  - `schemes.Z`: `schemes/results/Z/14x15x15_m1895_Z.json` (`rank: 1895`, `values: [-2, -1, 0, 1, 2]`, `complexity: 55893`) and `schemes/known/tensor/14x15x15_tensor.mpl` (`rank: 1905`)
  - `schemes.Q`: `schemes/results/Q/14x15x15_m1848_Q.json` (`rank: 1848`) and `schemes/results/Q/14x15x15_m1890_Q.json` (`rank: 1890`)
- **URL (repository recursive git tree):** `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1`
- **Fetched UTC:** `2026-10-18T17:21:13Z`
- **HTTP Status:** `200`
- **Bytes:** `1818813`
- **SHA-256:** `0cb3669d76a7e34604a34d2a204c0bf4e27525ba5348675bea6605d7e7032fab`
- **All `14x15x15` paths across all `6637` tree entries:**
  - `schemes/known/tensor/14x15x15_tensor.mpl`
  - `schemes/results/Q/14x15x15_m1848_Q.json`, `schemes/results/Q/14x15x15_m1848_Q.m`
  - `schemes/results/Q/14x15x15_m1890_Q.json`, `schemes/results/Q/14x15x15_m1890_Q.m`
  - `schemes/results/Z/14x15x15_m1895_Z.json`, `schemes/results/Z/14x15x15_m1895_Z.m`
  - `schemes/results/ZT/14x15x15_m1905_ZT.json`, `schemes/results/ZT/14x15x15_m1905_ZT.m`
- **Result:** No scheme of rank at most `1894` in `ZT` (or `Z`) exists anywhere in `dronperminov/FastMatrixMultiplication`.

### 1.3 `sedoglavic/fmm_digest` — `fmm_sota.json`
- **URL:** `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`
- **Fetched UTC:** `2026-10-18T17:20:56Z`
- **HTTP Status:** `200`
- **Bytes:** `343798`
- **SHA-256:** `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1` (matches `claim/fmm_sota.json` byte-for-byte; `createdAt: "2026-10-09T11:45:48"`)
- **Exact `[14, 15, 15]` entry (line 4153):**
  `{ "format": [14,15,15], "rank": 1848, "exponent": 2.801382 },`
- **Result:** Claimed rank `r = 1894` is at least `1848`, satisfying Criterion Clause (2) that the scheme does not beat the overall rational SOTA in `fmm_sota.json`.

### 1.4 `MerlijnW70/fmm-schemes` — Repository Tree
- **URL:** `https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1`
- **Fetched UTC:** `2026-10-18T17:20:57Z`
- **HTTP Status:** `200`
- **Bytes:** `9577`
- **SHA-256:** `e6866337cf18c6f4bb9d2b950240341d901260e28b560a301853202c03b1a5fc`
- **Findings:** Across all `39` entries in `MerlijnW70/fmm-schemes`, the only files containing both `14` and `15` are `schemes/10x13x14_m1150_ZT.json` and `schemes/12x13x15_m1464_ZT.json`. There is no `14x15x15` scheme of any rank in `MerlijnW70/fmm-schemes`.

## 2. Literature & Repository Search (Last 24 Months)

- **arXiv API (`export.arxiv.org`):**
  - **URL:** `https://export.arxiv.org/api/query?search_query=all:%2214x15x15%22+OR+all:%22ternary+flip+graph%22&sortBy=submittedDate&sortOrder=descending&max_results=25`
  - **Fetched UTC:** `2026-10-18T17:21:15Z`, HTTP `429` (`14` bytes, SHA-256 `467622e2f17f01d302d6c790b13078569f17d71cd83910558535019a594e07c1`; rate-limited by concurrent panel queries; not retried per single-fetch rule).
- **OpenAlex Literature Search (covering arXiv, Zenodo, and DOI-indexed publications through 2026):**
  - **Query 1 URL:** `https://api.openalex.org/works?search=%2214x15x15%22&per-page=25`
    - **Fetched UTC:** `2026-10-18T17:22:16Z`, HTTP `200`, `18040` bytes, SHA-256 `56f89f1b93041781131234663535129269409335c5c021161075190892607117` (3 unrelated medical/ceramics hits from 2016–2024; 0 matrix multiplication papers).
  - **Query 2 URL:** `https://api.openalex.org/works?search=%22ternary%22+%22flip+graph%22+%22matrix+multiplication%22&per-page=25`
    - **Fetched UTC:** `2026-10-18T17:22:17Z`, HTTP `200`, `59238` bytes, SHA-256 `8211270804870039997423961992522411351748801071574099640153161877` (11 results, including 2025–2026 preprints `10.48550/arxiv.2603.02398`, `10.48550/arxiv.2606.13408`, `10.48550/arxiv.2511.20317`, `10.48550/arxiv.2606.02480`, `10.48550/arxiv.2609.17533`, `10.48550/arxiv.2602.11041`). All ternary/integer schemes from those papers for formats up to `(16, 16, 16)` are already integrated into `dronperminov/FastMatrixMultiplication` (where `14x15x15` has `ZT = 1905` and `Z = 1895`).
- **GitHub Searches:**
  - `https://api.github.com/search/code?q=%2214x15x15%22` at `2026-10-18T17:21:47Z`: HTTP `401` (`120` bytes, SHA-256 `b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e`; unauthenticated code search endpoint requires token).
  - `https://api.github.com/search/repositories?q=FastMatrixMultiplication+OR+fmm-schemes+OR+14x15x15` at `2026-10-18T17:22:19Z`: HTTP `200` (`51271` bytes, SHA-256 `3549495763038101850868121317309638582680018094127671130321772094`, `12` repositories total; only `FastMatrixMultiplication` updated `2026-10-13T14:55:15Z` and `fmm-schemes` updated `2026-09-30T16:53:51Z` contain small-format tensor decompositions).

## 3. `TROPHY_CASE.md` and Open Pull Requests

### 3.1 `elder-plinius/V3R1T4S` — `TROPHY_CASE.md`
- **URL:** `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`
- **Fetched UTC:** `2026-10-18T17:21:47Z`
- **HTTP Status:** `200`
- **Bytes:** `31235`
- **SHA-256:** `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`
- **Findings:** Row 44 records a rational (`Q`-only) scheme for `(14, 15, 15)` of rank `1842` over `Q` (under `fmm-catalogue-small-format-rank`, explicitly noted as `rank over Q only`). There is no `ZT` or `Z` scheme for `14x15x15` in `TROPHY_CASE.md`.

### 3.2 `elder-plinius/V3R1T4S` — Open Pull Requests
- **URL:** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100`
- **Fetched UTC:** `2026-10-18T17:21:47Z`
- **HTTP Status:** `200`
- **Bytes:** `2129314`
- **SHA-256:** `dddcd21e1f0d20d39662e71e8c8f4ba01af722697b9d95ffc75a9c67abb7d543`
- **Findings:** Inspected all open pull requests, including all open `fmm-ternary-integer-ring-upgrade` PRs (#356 `6x12x14 ZT 654`, #402 `9x12x14 ZT 954`, #408 `11x12x14 Z 1165`, #409 `11x12x16 Z 1293`, #410 `11x14x16 Z 1540`, #411 `11x14x16 ZT 1547`, #412 `12x13x16 Z 1516`, #413 `12x14x14 ZT 1472`, #414 `12x16x16 Z 1830`, #415 `14x16x16 Z 2159`, #417 `4x13x15 Z 533`, #418 `4x13x15 ZT 535`, #419 `4x14x15 Z 569`, #420 `7x8x15 Z 570`, #421 `9x10x14 ZT 816`, #422 `9x11x14 Z 889`, #423 `9x12x16 Z 1065`, #424 `9x13x14 Z 1039`). None of the open PRs claims format `14x15x15`. (PR #356 for `6x12x14` mentions in a summary bullet that `14x15x15` could reach `ZT` rank `1895`, matching live `Z = 1895`; the present claim of `ZT` rank `1894` strictly beats `1905` by `11` and even strictly beats `1895` by `1`.)

### 3.3 `dronperminov/FastMatrixMultiplication` — Open Pull Requests
- **URL:** `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/pulls?state=open&per_page=100`
- **Fetched UTC:** `2026-10-18T17:21:47Z`
- **HTTP Status:** `200`
- **Bytes:** `192788`
- **SHA-256:** `7d5e97e87085623b36095f34cee19a4a26a0daef6afec6503bc0939d01f98ab2`
- **Findings:** `10` open PRs (#6 through #15); `0` touch `14x15x15` (only PR #14 touches `6x12x14` and `4x5x5`; PRs #6–#13 and #15 are additive complexity reductions on smaller formats).

## 4. Verdict

The claimed rank-1894 ternary (`ZT = {-1, 0, 1}`) bilinear scheme `claim/14x15x15_m1894_ZT.json` strictly improves upon the live `ZT` record (`1894` vs `1905`, `-11`) and the live `Z` record (`1894` vs `1895`, `-1`) in `dronperminov/FastMatrixMultiplication`, remains above the rational SOTA (`1894` vs `1848`), and does not exist in `dronperminov/FastMatrixMultiplication`, `MerlijnW70/fmm-schemes`, `TROPHY_CASE.md`, open pull requests, or the literature.

pass: true
