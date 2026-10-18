# Skeptic Panel Report — Role: NOVELTY

role: NOVELTY
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target: fmm-ternary-integer-ring-upgrade
format: 9x12x14
claimed_ring: ZT
claimed_rank: 954
object_file: claim/9x12x14_m954_ZT.json
object_sha256: a873a293abc4e1b7c659250591e544062ad26ca556af28f29b25e63998355b02

## Mandate

Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value and time. Search the last 24 months of literature, the repository's `TROPHY_CASE.md` and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record.

## 1. Primary Tables & Live Repository Status (Single Honest Fetch per URL)

Each primary URL was fetched exactly once with `curl -sS -A "V3R1T4S-research-agent (honest single fetch)"` and zero retries:

1. **Perminov Master `README.md`**
   - **URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md`
   - **Fetched UTC:** `2026-10-18T12:35:49Z`
   - **HTTP Status:** `200` (`112,671` bytes)
   - **SHA-256:** `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341` (matches `claim/perminov_README.md` byte-for-byte)
   - **Exact Quoted Rows for `9x12x14`:**
     - Line 229 (summary table):
       `| 9x12x14  |   945 (Q)   |     [940](schemes/results/Q/9x12x14_m940_Q.json) (Q)     | **2.805232985** |`
     - Line 1350 (ring-comparison table with columns `Format | ZT rank | Z rank | Q rank | omega`):
       `| 9x12x14  |   960 (?)   |   960 (?)    |  940 (945)   | **2.805232985** |`
   - **Live Values:** `ZT rank = 960`, `Z rank = 960`, `Q rank = 940`.
   - **Comparison:** The claimed `ZT` scheme in `claim/9x12x14_m954_ZT.json` has rank `954`, which is strictly less than the live `ZT rank = 960` (and also strictly less than the live `Z rank = 960`) by `6` multiplications (`954 - 960 = -6`), while satisfying `954 >= 940 = min(960, 960, 940)` (Clause 1 and Clause 2).

2. **Perminov `schemes/status.json`**
   - **URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/status.json`
   - **Fetched UTC:** `2026-10-18T12:35:49Z`
   - **HTTP Status:** `200` (`2,165,677` bytes)
   - **SHA-256:** `b9b86c506ef4826220e5479569c6a84eaa720b703f73b705c043a3c90b463311`
   - **Exact Quoted Entry for `"9x12x14"`:**
     - `"ranks": {"Q": 940, "ZT": 960, "Z": 960}`
     - `"omegas": {"Q": 2.805232984593238, "ZT": 2.8138600302025685, "Z": 2.8138600302025685}`
     - `"schemes"."ZT"`: single entry with `"rank": 960`, `"complexity": 16610`, `"values": [-1, 0, 1]`, `"source": "schemes/results/ZT/9x12x14_m960_ZT.json"`
     - `"schemes"."Z"`: absent (no pure-integer scheme strictly below `ZT` rank `960`)
     - `"schemes"."Q"`: ranks `940`, `942`, `944`, `945` (all requiring fractional denominators `1/2`, `1/4`, or `1/8`).

3. **Perminov Full Git Tree (`dronperminov/FastMatrixMultiplication`)**
   - **URL:** `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1`
   - **Fetched UTC:** `2026-10-18T12:36:31Z`
   - **HTTP Status:** `200` (`1,818,813` bytes, `truncated: false`, `6,637` tree entries)
   - **SHA-256:** `0cb3669d76a7e34604a34d2a204c0bf4e27525ba5348675bea6605d7e7032fab`
   - **All files matching `9x12x14` (or any permutation of `(9, 12, 14)`):**
     - `schemes/known/tensor/9x12x14_tensor.mpl` (rank `945` in `Q`)
     - `schemes/results/Q/9x12x14_m940_Q.json` and `.m`
     - `schemes/results/Q/9x12x14_m942_Q.json` and `.m`
     - `schemes/results/Q/9x12x14_m944_Q.json` and `.m`
     - `schemes/results/ZT/9x12x14_m960_ZT.json` and `.m`
   - **Verification of Clause (3a):** No scheme of rank `<= 954` in `ZT` or `Z` exists in `schemes/results/ZT`, `schemes/results/Z`, or anywhere else in `dronperminov/FastMatrixMultiplication`.

4. **MerlijnW70 Full Git Tree (`MerlijnW70/fmm-schemes`)**
   - **URL:** `https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1`
   - **Fetched UTC:** `2026-10-18T12:35:51Z`
   - **HTTP Status:** `200` (`9,577` bytes, `truncated: false`, `39` tree entries)
   - **SHA-256:** `e6866337cf18c6f4bb9d2b950240341d901260e28b560a301853202c03b1a5fc`
   - **Result:** The repository contains 31 scheme files under `schemes/`, and zero files for format `9x12x14` (the only formats with dimension 14 are `6x11x14_m617_ZT.json`, `7x9x14_m598_ZT.json`, `8x10x14_m724_ZT.json`, `9x14x16_m1260_ZT.json`, `10x13x14_m1150_ZT.json`, `10x14x16_m1416_ZT.json`, `11x14x14_m1367_ZT.json`, `13x14x16_m1805_ZT.json`).
   - **Verification of Clause (3b):** No scheme for `9x12x14` exists in `MerlijnW70/fmm-schemes`.

5. **Sedoglavic `fmm_sota.json` & FMM-Lille `9x12x14.html` & Solven `matmulcatalog`**
   - **`fmm_sota.json` URL:** `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`
     - **Fetched UTC:** `2026-10-18T12:35:50Z` | **HTTP Status:** `200` (`343,798` bytes)
     - **SHA-256:** `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1` (matches `claim/fmm_sota.json` byte-for-byte)
     - **Exact Quoted Entry:** `{"format": [9, 12, 14], "rank": 940, "exponent": 2.805233}`
   - **FMM-Lille Page URL:** `https://fmm.univ-lille.fr/9x12x14.html`
     - **Fetched UTC:** `2026-10-18T12:35:50Z` | **HTTP Status:** `200` (`21,817` bytes)
     - **SHA-256:** `323f57258b783077a2d21b2eb6d085420074372dab97d6bfbabc65b6b7888bb9`
     - **Quoted Value:** `Description of fast matrix multiplication algorithm: (9x12x14:940)` (rational `Q` scheme of rank `940`).
   - **Solven `matmulcatalog` `COVERAGE.md` URL:** `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md`
     - **Fetched UTC:** `2026-10-18T12:35:51Z` | **HTTP Status:** `200` (`94,842` bytes)
     - **SHA-256:** `c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`
     - **Exact Quoted Row (Line 500):**
       `| ⟨9,12,14⟩ | **✓ 960** Dronperminov-ZT [Z→F₂] | **✓ 940** Dronperminov-Q | — | — | **940** in R/Q/Z | +16610 | — |`
     - Confirms that across `solven-eu/matmulcatalog` as well, the best known `ZT` / `Z` scheme for `(9, 12, 14)` is Perminov's rank-`960` `ZT` scheme, whereas rank `940` is over `Q`.

## 2. Literature & Repository Search (Last 24 Months)

1. **arXiv API — Exact Format & Ternary Flip Graph Query**
   - **URL:** `https://export.arxiv.org/api/query?search_query=all:%229x12x14%22+OR+all:%22ternary+flip+graph%22&sortBy=submittedDate&sortOrder=descending&max_results=25`
   - **Fetched UTC:** `2026-10-18T12:36:11Z` | **HTTP Status:** `200` (`764` bytes)
   - **SHA-256:** `75aa591abd13f1c5c32d3fb86de49ceeed8274e981be994cc8a5cef451c82f48`
   - **Result:** `totalResults: 0`.

2. **arXiv API — Fast Matrix Multiplication & Flip Graph (2024–2026)**
   - **URL:** `https://export.arxiv.org/api/query?search_query=all:%22fast+matrix+multiplication%22+AND+all:%22flip+graph%22&sortBy=submittedDate&sortOrder=descending&max_results=25`
   - **Fetched UTC:** `2026-10-18T12:36:30Z` | **HTTP Status:** `200` (`10,265` bytes)
   - **SHA-256:** `a3308d0c1c3e544864e98a111192e31eb726696f9cf10fc664c731d57f3a05fd`
   - **Result:** `totalResults: 5` preprints:
     - `2609.17533v1` (2026-06-22): *GPU-Accelerated Search for Fast Matrix Multiplication over F_2* (`(7,7,7)` over `F_2` at rank 245).
     - `2606.13408v3` (2026-06-11): *A catalog of fast matrix multiplication algorithms with exhaustive derivations* (corresponds to `solven-eu/matmulcatalog` checked above, which lists `960` for `(9,12,14)` in `ZT`).
     - `2606.02480v2` (2026-06-01): *Meta Flip Graph meets Serendipitous Product: new Fast Matrix Multiplication results* (corresponds to `dronperminov/FastMatrixMultiplication`, which lists `960` for `9x12x14` in `ZT` and `Z`).
     - `2603.02398v1` (2026-03-02): *Fast Matrix Multiplication in Small Formats: Discovering New Schemes with an Open-Source Flip Graph Framework* (earlier release of `dronperminov/FastMatrixMultiplication`).
     - `2511.20317v2` (2025-11-25): *Fast Matrix Multiplication via Ternary Meta Flip Graphs* (earlier release of `dronperminov/FastMatrixMultiplication`).
   - None of these papers reports a `ZT` or `Z` rank below `960` for `(9, 12, 14)`.

3. **GitHub Repositories & Upstream Pull Requests**
   - **GitHub Repository Search URL:** `https://api.github.com/search/repositories?q=FastMatrixMultiplication+OR+fmm-schemes+OR+matmulcatalog`
     - **Fetched UTC:** `2026-10-18T12:36:12Z` | **HTTP Status:** `200` (`74,326` bytes) | **SHA-256:** `06b911ba5d1a0a091dc74656770da80015fe713a1d649a56a73a62c4ffa213fc`
     - Returns `13` repositories; the only active small-format scheme catalogues are `dronperminov/FastMatrixMultiplication`, `MerlijnW70/fmm-schemes`, and `solven-eu/matmulcatalog`, all checked above.
   - **Upstream PRs on `dronperminov/FastMatrixMultiplication`:**
     - **URL:** `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/pulls?state=all&per_page=100`
     - **Fetched UTC:** `2026-10-18T12:40:25Z` | **HTTP Status:** `200` (`231,560` bytes) | **SHA-256:** `05773197d68a86850461dc8dccad504031dc2e42427dfb799b1687a325acad71`
     - Returns `12` pull requests total (`#1` through `#14`). None mentions `9x12x14` (PR `#14` is for `6x12x14` `ZT` rank `654` and `4x5x5` reduced additions; PRs `#6`–`#13` are straight-line addition reductions).
   - **Upstream PRs on `MerlijnW70/fmm-schemes`:**
     - **URL:** `https://api.github.com/repos/MerlijnW70/fmm-schemes/pulls?state=all&per_page=100`
     - **Fetched UTC:** `2026-10-18T12:40:26Z` | **HTTP Status:** `200` (`2` bytes, `[]`) | **SHA-256:** `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
     - Zero pull requests.

## 3. V3R1T4S `TROPHY_CASE.md` and Pull Requests

1. **`TROPHY_CASE.md`**
   - **URL:** `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`
   - **Fetched UTC:** `2026-10-18T12:36:13Z` | **HTTP Status:** `200` (`31,235` bytes)
   - **SHA-256:** `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`
   - **Result:** The matrix multiplication entries in `TROPHY_CASE.md` (rows 44–48) are 5 rational (`Q`) schemes for formats `(14,15,15)`, `(13,14,14)`, `(15,16,16)`, `(14,14,15)`, and `(13,14,15)`. There are zero entries for `fmm-ternary-integer-ring-upgrade` or for format `9x12x14`.

2. **Open Pull Requests (`elder-plinius/V3R1T4S`)**
   - **URL:** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100`
   - **Fetched UTC:** `2026-10-18T12:36:13Z` | **HTTP Status:** `200` (`1,955,678` bytes)
   - **SHA-256:** `e184e332e31e2ad6a06335b024e6c495c1b5cca95aed40efa3a20425f1b16afa`
   - **Result:** `92` open pull requests total. Only one open PR targets `fmm-ternary-integer-ring-upgrade` (PR `#356`, which claims format `6x12x14` `ZT` rank `654`). Zero open PRs mention `9x12x14`.

3. **Closed / Merged Pull Requests (`elder-plinius/V3R1T4S`)**
   - **URL:** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=closed&per_page=100`
   - **Fetched UTC:** `2026-10-18T12:40:05Z` | **HTTP Status:** `200` (`1,747,563` bytes)
   - **SHA-256:** `53a2d774a19fc14e7362e05755b32d3c35400bfe694cf2e379a358848cc9addc`
   - **Result:** `100` most recent closed/merged pull requests checked. Zero closed or merged PRs target `fmm-ternary-integer-ring-upgrade` or mention `9x12x14`.

## Verdict

The claimed rank-954 ternary (`ZT = {-1, 0, 1}`) bilinear scheme `claim/9x12x14_m954_ZT.json` strictly improves upon the best known `ZT` rank (`960`) and `Z` rank (`960`) for format `9x12x14` by 6 multiplications (`954 < 960`), remains above the overall best `Q` rank (`940 <= 954`), and does not appear in any existing repository, paper, trophy case, or open/closed pull request.

pass: true
