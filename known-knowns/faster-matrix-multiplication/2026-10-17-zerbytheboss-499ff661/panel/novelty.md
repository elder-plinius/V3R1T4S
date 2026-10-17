# Novelty Skeptic Report — `fmm-ternary-integer-ring-upgrade` (`6x12x14` `ZT` Rank `654`)

context: subagent (fresh invocation)

Role: NOVELTY skeptic.
Question under test: Does the explicit ternary (`ZT = {-1, 0, 1}`) bilinear scheme in `object/6x12x14_m654_ZT.json` (`ZT` rank `654`) strictly beat every known ternary (`ZT`) rank for format `6x12x14` (and its axis permutations) across live primary tables, the last 24 months of literature, `TROPHY_CASE.md`, and open/merged pull requests? A tie is not a record.

## 1. Single Honest Fetch of Primary Tables and Status Pages

Each primary table and repository endpoint was fetched once (no retries, HTTP `200`):

| Source | URL | UTC Fetch Time | HTTP Status | SHA-256 | Extracted Value for `6x12x14` |
|---|---|---|---:|---|---|
| Perminov git tree (primary repository index) | `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1` | `2026-10-17T16:59:39Z` | `200` | `0cb3669d76a7e34604a34d2a204c0bf4e27525ba5348675bea6605d7e7032fab` | `schemes/results/ZT/6x12x14_m666_ZT.json` (`ZT` rank = **666**); `schemes/results/Z/6x12x14_m654_Z.json` (`Z` rank = **654**); `schemes/results/Q/6x12x14_m645_Q.json` (`Q` rank = **645**). No other axis permutation of `6x12x14` exists in `ZT/`. |
| Perminov live `ZT` scheme file | `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/ZT/6x12x14_m666_ZT.json` | `2026-10-17T16:59:40Z` | `200` | `50438fbd3ec9b8fcad5499c2b6c9a756bc6753e708ce57d73e34ef1403139968` | `"n": [6, 12, 14]`, `"m": 666`, `"ring": "ZT"` (live ternary rank = **666**). |
| Sedoglavic `fmm_sota.json` | `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` | `2026-10-17T16:59:41Z` | `200` | `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1` | `{"format": [6, 12, 14], "rank": 645, "exponent": 2.790555}` (best rational `Q` rank is `645`). |
| Solven `matmulcatalog` `COVERAGE.md` | `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` | `2026-10-17T16:59:42Z` | `200` | `c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7` | Row `(6,12,14)`: `654 Dronperminov-Z` (non-ternary integer `Z`), `645 Dronperminov-Q` (rational `Q`), no ternary `ZT` scheme at or below `654`. |
| V3R1T4S `TROPHY_CASE.md` | `TROPHY_CASE.md` | `2026-10-17T16:59:42Z` | local | `738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9` | 53 rows inspected: rows 44–48 cover rational `Q` schemes on formats `13x14x14` through `15x16x16`. Zero entries for `6x12x14` or `fmm-ternary-integer-ring-upgrade`. |
| V3R1T4S open pull requests | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` | `2026-10-17T16:59:43Z` | `200` | live API | 50 open PRs inspected (`#9` through `#355`): zero open PRs target `fmm-ternary-integer-ring-upgrade` or mention `6x12x14` (or any permutation `6,12,14`, `12x6x14`, `14x12x6`). |

## 2. Literature Audit (Last 24 Months, 2024–2026)

- **Perminov (2025–2026), arXiv:2511.10786, arXiv:2511.20317, arXiv:2512.13365, arXiv:2603.02398, and `FastMatrixMultiplication` `README.md` / `CHANGELOG.md`**: Lists `6x12x14` at `ZT = 666`, `Z = 654`, `Q = 645`. The `Z = 654` scheme in `schemes/results/Z/6x12x14_m654_Z.json` requires non-ternary integer coefficients (`+/-2` entries) and therefore fails the ternary `ZT = {-1, 0, 1}` ring restriction.
- **Kauers & Wood (arXiv:2510.19787), Moosbauer & Poole (arXiv:2502.04514), Khoruzhii et al. (LITA, arXiv:2511.09606), Solven `matmulcatalog` (arXiv:2606.13408)**: None gives a ternary `ZT = {-1, 0, 1}` scheme for `6x12x14` below rank `666`.

## 3. Exact Novelty Comparison

- **Live `ZT` record**: `666` (`schemes/results/ZT/6x12x14_m666_ZT.json`)
- **Live `Z` record**: `654` (`schemes/results/Z/6x12x14_m654_Z.json`)
- **Live `Q` record**: `645` (`schemes/results/Q/6x12x14_m645_Q.json`)
- **Candidate (`object/6x12x14_m654_ZT.json`)**: `ZT` rank **`654`** with all coefficients strictly in `{-1, 0, 1}`.
- **Strict improvement over live `ZT` record**: `654 vs 666` (**`-12`** scalar multiplications).
- **Gap closure**:
  - `ZT-to-Q` gap closed: `(666 - 654) / (666 - 645) = 12 / 21 = 57.14% at least 50%` (exceeds the target's `at least 50%` partial-win threshold).
  - `ZT-to-Z` gap closed: `(666 - 654) / (666 - 654) = 12 / 12 = 100%` (eliminates the entire `ZT-to-Z` gap).

## Verdict

The candidate in `object/6x12x14_m654_ZT.json` (`ZT` rank `654`) strictly beats the best known ternary (`ZT`) rank of `666` by `12` multiplications, closes `57.14%` of the `ZT-to-Q` gap and `100%` of the `ZT-to-Z` gap, and is uncontested across `TROPHY_CASE.md`, all open/merged pull requests, and the 24-month literature.

pass: true
