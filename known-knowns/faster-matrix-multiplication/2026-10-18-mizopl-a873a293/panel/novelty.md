# Skeptic Panel Report — Role: NOVELTY

role: NOVELTY
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target: fmm-ternary-integer-ring-upgrade
format: 9x12x14
claimed_ring: ZT
claimed_rank: 954
object_file: object/9x12x14_m954_ZT.json
object_sha256: a873a293abc4e1b7c659250591e544062ad26ca556af28f29b25e63998355b02

## Mandate

Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value and time. Search the last 24 months of literature, the repository's `TROPHY_CASE.md` and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record.

## 1. Primary Tables & Repository Status as of Filing (2026-10-18, Single Honest Fetch per URL)

Each primary URL was fetched exactly once with `curl -sS -A "V3R1T4S-research-agent (honest single fetch)"` and zero retries:

1. **Perminov Master `README.md` (table now at `docs/ranks.md`)**
   - **URL (at filing):** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md` (table moved upstream to `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md`)
   - **Fetched UTC:** `2026-10-18T12:35:49Z`
   - **HTTP Status:** `200` (`112,671` bytes)
   - **SHA-256:** `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341`
   - **Exact Quoted Rows for `9x12x14` as listed on 2026-10-18 (`ZT 960, Z 960`):**
     - Line 229 (summary table):
       `| 9x12x14  |   945 (Q)   |     [940](schemes/results/Q/9x12x14_m940_Q.json) (Q)     | **2.805232985** |`
     - Line 1350 (ring-comparison table with columns `Format | ZT rank | Z rank | Q rank | omega`):
       `| 9x12x14  |   960 (?)   |   960 (?)    |  940 (945)   | **2.805232985** |`
   - **Values Listed on 2026-10-18:** `ZT 960, Z 960`, `Q rank = 940` (also published upstream by the contributor on 2026-10-19 as `schemes/known/mizopl/9x12x14_m954_ZT.json`; `docs/ranks.md` now lists `ZT 954 / Z 954`).
   - **Comparison:** The claimed `ZT` scheme in `object/9x12x14_m954_ZT.json` has rank `954`, which is strictly less than the rank listed on 2026-10-18 (`ZT 960, Z 960`) by `6` multiplications (`954 - 960 = -6`), while satisfying `954 >= 940 = min(960, 960, 940)` (Clause 1 and Clause 2).

2. **Perminov `schemes/status.json`**
   - **URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/status.json`
   - **Fetched UTC:** `2026-10-18T12:35:49Z`
   - **HTTP Status:** `200` (`2,165,677` bytes)
   - **SHA-256:** `b9b86c506ef4826220e5479569c6a84eaa720b703f73b705c043a3c90b463311`
   - **Exact Quoted Entry for `"9x12x14"` as listed on 2026-10-18 (`ZT 960, Z 960`):**
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
   - **All files matching `9x12x14` (or any permutation of `(9, 12, 14)`) on 2026-10-18:**
     - `schemes/known/tensor/9x12x14_tensor.mpl` (rank `945` in `Q`)
     - `schemes/results/Q/9x12x14_m940_Q.json` and `.m`
     - `schemes/results/Q/9x12x14_m942_Q.json` and `.m`
     - `schemes/results/Q/9x12x14_m944_Q.json` and `.m`
     - `schemes/results/ZT/9x12x14_m960_ZT.json` and `.m`
   - **Verification of Clause (3a):** As of filing on 2026-10-18, no scheme of rank `<= 954` in `ZT` or `Z` existed in `schemes/results/ZT`, `schemes/results/Z`, or anywhere else in `dronperminov/FastMatrixMultiplication`.

4. **MerlijnW70 Full Git Tree (`MerlijnW70/fmm-schemes`)**
   - **URL:** `https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1`
   - **Fetched UTC:** `2026-10-18T12:35:51Z`
   - **HTTP Status:** `200` (`9,577` bytes, `truncated: false`, `39` tree entries)
   - **SHA-256:** `e6866337cf18c6f4bb9d2b950240341d901260e28b560a301853202c03b1a5fc`
   - **Result:** The repository contains 31 scheme files under `schemes/`, and zero files for format `9x12x14`.
   - **Verification of Clause (3b):** No scheme for `9x12x14` exists in `MerlijnW70/fmm-schemes`.

5. **Sedoglavic `fmm_sota.json` & FMM-Lille `9x12x14.html` & Solven `matmulcatalog`**
   - **`fmm_sota.json` URL:** `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`
     - **Fetched UTC:** `2026-10-18T12:35:50Z` | **HTTP Status:** `200` (`343,798` bytes)
     - **SHA-256:** `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1`
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
   - **Result:** `totalResults: 5` preprints (`2609.17533v1`, `2606.13408v3`, `2606.02480v2`, `2603.02398v1`, `2511.20317v2`). None of these papers reports a `ZT` or `Z` rank below `960` for `(9, 12, 14)`.

## 3. V3R1T4S `TROPHY_CASE.md` and Pull Requests

1. **`TROPHY_CASE.md`**
   - **URL:** `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`
   - **Fetched UTC:** `2026-10-18T12:36:13Z` | **HTTP Status:** `200` (`31,235` bytes)
   - **SHA-256:** `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`
   - **Result:** `TROPHY_CASE.md` has no existing entry for `fmm-ternary-integer-ring-upgrade` or for format `9x12x14`.

2. **Open & Closed Pull Requests (`elder-plinius/V3R1T4S`)**
   - **Open PRs URL:** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` (`2026-10-18T12:36:13Z`, HTTP `200`, `sha256: e184e332e31e2ad6a06335b024e6c495c1b5cca95aed40efa3a20425f1b16afa`) — zero prior PRs mention `9x12x14`.
   - **Closed PRs URL:** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=closed&per_page=100` (`2026-10-18T12:40:05Z`, HTTP `200`, `sha256: 53a2d774a19fc14e7362e05755b32d3c35400bfe694cf2e379a358848cc9addc`) — zero closed/merged PRs mention `9x12x14`.

## Verdict

The claimed rank-954 ternary (`ZT = {-1, 0, 1}`) bilinear scheme `object/9x12x14_m954_ZT.json` strictly improves upon the rank listed on 2026-10-18 (`ZT 960, Z 960`) in `README.md` / `docs/ranks.md` for format `9x12x14` by 6 multiplications (`954 < 960`), remains above the overall best `Q` rank (`940 <= 954`), and had no prior occurrence in any repository, paper, trophy case, or pull request at filing.

pass: true
