# Skeptic Panel Report — Role: NOVELTY (`fmm-ternary-integer-ring-upgrade`, `14x15x15`, `ZT` rank `1894`)

role: NOVELTY
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target: fmm-ternary-integer-ring-upgrade
format: 14x15x15
ring: ZT
claimed_rank: 1894
object_file: object/14x15x15_m1894_ZT.json
object_sha256: bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb
object_bytes: 944884

## 1. Primary Status Table Fetches as of Filing (`2026-10-18`, Single Honest GETs, No Retries)

### 1.1 `dronperminov/FastMatrixMultiplication` — `README.md` / `docs/ranks.md`
- **URL (at filing):** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md` (table moved upstream to `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md`)
- **Fetched UTC:** `2026-10-18T17:19:53Z`
- **HTTP Status:** `200`
- **SHA-256:** `0dc78efcb144382ef7b703d37563722f5d328b83a42eddc17c0018e9bd628ca8`
- **Exact `14x15x15` row as of filing (`2026-10-18: ZT 1,905, Z 1,895`):**
  `| 14x15x15 |  1905 (32)  |  1895 (33)   |  1848 (99)   | **2.811404586** |`
- **Table values for `14x15x15` as of filing (`2026-10-18`):**
  - `ZT rank = 1,905`
  - `Z rank = 1,895`
  - `Q rank = 1,848` (note: `1,848` is not the overall best because a rational rank-`1,842` scheme is already merged here in `V3R1T4S` `TROPHY_CASE.md`).
  - Also published upstream by the contributor (`@mizopl`) on 2026-10-19 (`schemes/known/mizopl/14x15x15_m1894_ZT.json`); `docs/ranks.md` now lists `ZT 1,894 / Z 1,894`.
- **Comparison with claim:** The claimed ternary (`ZT`) rank `r = 1894` improves on the table as of filing (`2026-10-18: ZT 1,905, Z 1,895`) by `-11` multiplications in `ZT` (`1894 < 1905`) and `-1` multiplication in `Z` (`1894 < 1895`), while remaining above the rational `Q` ranks (`1894 >= 1848 > 1842`).

### 1.2 `dronperminov/FastMatrixMultiplication` — `schemes/status.json` & Repository Tree as of Filing (`2026-10-18`)
- **URL (`status.json`):** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/status.json`
- **Fetched UTC:** `2026-10-18T17:19:54Z`
- **HTTP Status:** `200`
- **SHA-256:** `809a1e34183516c33c84cccd6484b49ca5682a43b5e36bd9739c2b6eb4ebaf31`
- **Exact `14x15x15` entry in `status.json` as of filing (`2026-10-18`):**
  - `"ranks": {"Z": 1895, "Q": 1848, "ZT": 1905}`
  - `schemes.ZT`: single entry `schemes/results/ZT/14x15x15_m1905_ZT.json` (`rank: 1905`, `values: [-1, 0, 1]`, `complexity: 55464`)
  - `schemes.Z`: `schemes/results/Z/14x15x15_m1895_Z.json` (`rank: 1895`, `values: [-2, -1, 0, 1, 2]`, `complexity: 55893`) and `schemes/known/tensor/14x15x15_tensor.mpl` (`rank: 1905`)
  - `schemes.Q`: `schemes/results/Q/14x15x15_m1848_Q.json` (`rank: 1848`) and `schemes/results/Q/14x15x15_m1890_Q.json` (`rank: 1890`)
- **URL (repository recursive git tree):** `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1`
- **Fetched UTC:** `2026-10-18T17:21:13Z`
- **HTTP Status:** `200` (`1,818,813` bytes, `sha256: 0cb3669d76a7e34604a34d2a204c0bf4e27525ba5348675bea6605d7e7032fab`)
- **Result:** As of filing (`2026-10-18`), no scheme of rank at most `1894` in `ZT` (or `Z`) existed in `dronperminov/FastMatrixMultiplication`.

### 1.3 `sedoglavic/fmm_digest` — `fmm_sota.json`
- **URL:** `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`
- **Fetched UTC:** `2026-10-18T17:19:55Z`
- **HTTP Status:** `200` (`343,798` bytes, `sha256: 256d5753d1ff2640c11b3b1e5a1faaf21dc22c98055e1429a319f89e4e2a3c24`)
- **Exact `[14, 15, 15]` entry:**
  `{ "format": [14,15,15], "rank": 1848, "exponent": 2.811405 }`
- **Result:** Claimed rank `r = 1894` is at least `1848` (and above the rational rank-`1,842` scheme already merged in `V3R1T4S`), satisfying Criterion Clause (2).

### 1.4 `MerlijnW70/fmm-schemes` — Repository Tree
- **URL:** `https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1`
- **Fetched UTC:** `2026-10-18T17:20:57Z` (`HTTP 200`, `9,577` bytes, `sha256: e6866337cf18c6f4bb9d2b950240341d901260e28b560a301853202c03b1a5fc`)
- **Findings:** There is no `14x15x15` scheme of any rank in `MerlijnW70/fmm-schemes`.

## 2. Literature & Repository Search (Last 24 Months)

- **OpenAlex Literature Search (covering arXiv, Zenodo, and DOI-indexed publications through 2026):**
  - **Query 1 URL:** `https://api.openalex.org/works?search=%2214x15x15%22&per-page=25` (`2026-10-18T17:22:16Z`, HTTP `200`, `sha256: 56f89f1b93041781131234663535129269409335c5c021161075190892607117` — 0 matrix multiplication papers).
  - **Query 2 URL:** `https://api.openalex.org/works?search=%22ternary%22+%22flip+graph%22+%22matrix+multiplication%22&per-page=25` (`2026-10-18T17:22:17Z`, HTTP `200`, `sha256: 8211270804870039997423961992522411351748801071574099640153161877` — all ternary/integer schemes from those papers for formats up to `(16, 16, 16)` were integrated into `dronperminov/FastMatrixMultiplication`, which listed `ZT = 1905` and `Z = 1895` as of filing on `2026-10-18`).

## 3. `TROPHY_CASE.md` and Open Pull Requests

### 3.1 `elder-plinius/V3R1T4S` — `TROPHY_CASE.md`
- **URL:** `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md` (`2026-10-18T17:21:47Z`, HTTP `200`, `31,235` bytes, `sha256: b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`)
- **Findings:** Row 44 records a rational (`Q`-only) scheme for `(14, 15, 15)` of rank `1,842` over `Q` (under `fmm-catalogue-small-format-rank`, showing that `1,848` is not the overall best over `Q`). There is no `ZT` or `Z` scheme for `14x15x15` in `TROPHY_CASE.md`.

### 3.2 `elder-plinius/V3R1T4S` — Open Pull Requests
- **URL:** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` (`2026-10-18T17:21:47Z`, HTTP `200`, `sha256: dddcd21e1f0d20d39662e71e8c8f4ba01af722697b9d95ffc75a9c67abb7d543`)
- **Findings:** None of the other open PRs claims format `14x15x15`.

## 4. Verdict

The claimed rank-1894 ternary (`ZT = {-1, 0, 1}`) bilinear scheme `object/14x15x15_m1894_ZT.json` improves on the table as of filing (`2026-10-18: ZT 1,905, Z 1,895`) by `-11` in `ZT` and `-1` in `Z`, remains above the rational `Q` ranks (`1,848` in Perminov / `fmm_sota.json` and `1,842` merged in `V3R1T4S`), and had no prior occurrence in `ZT` or `Z` as of filing (`2026-10-18`).

pass: true
