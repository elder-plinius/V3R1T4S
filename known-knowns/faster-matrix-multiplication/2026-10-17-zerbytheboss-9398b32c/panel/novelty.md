# Novelty Skeptic Report — `fmm-additive-complexity-records` (`4x5x5` Rank `76` in `280` Reduced Additions)

context: subagent (fresh invocation)

Role: NOVELTY skeptic.
Question under test: Does the straight-line program in `object/4x5x5_m76_cr280_ZT_reduced.json` (`280` reduced additions at rank `76` for `4x5x5`) strictly beat every known reduced addition count for `4x5x5` at rank `76` across live primary tables, the last 24 months of literature, `TROPHY_CASE.md`, and open/merged pull requests (including merged PR `#222` at `281`)? A tie is not a record.

## 1. Single Honest Fetch of Primary Tables and Status Pages

Each primary table and repository endpoint was fetched once (no retries, HTTP `200`):

| Source | URL | UTC Fetch Time | HTTP Status | SHA-256 | Extracted Value for `4x5x5` (Rank `76`) |
|---|---|---|---:|---|---|
| Perminov git tree (primary repository index) | `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1` | `2026-10-17T16:59:39Z` | `200` | `0cb3669d76a7e34604a34d2a204c0bf4e27525ba5348675bea6605d7e7032fab` | Single `addition_reduced_ZT` file for `4x5x5` (and its permutations): `schemes/results/addition_reduced_ZT/4x5x5_m76_cr299_fv112_cn530_ZT_reduced.json` (`cr = 299`). |
| Perminov live `addition_reduced_ZT` scheme | `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/4x5x5_m76_cr299_fv112_cn530_ZT_reduced.json` | `2026-10-17T16:59:40Z` | `200` | `b0093dd8e7611da102507b2428b242ecd6a8e6e7152fb1258ea4b7750bf9d0b5` | `"m": 76`, `"cr": 299` (`U = 75`, `V = 95`, `W = 129`, total `299`), `"fv": 112`, `"cn": 530`. |
| Sedoglavic `fmm_sota.json` | `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` | `2026-10-17T16:59:41Z` | `200` | `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1` | `{"format": [4, 5, 5], "rank": 76, "exponent": 2.82122}` (confirms rank `76` is the best known rank for `4x5x5`). |
| Solven `matmulcatalog` `COVERAGE.md` | `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` | `2026-10-17T16:59:42Z` | `200` | `c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7` | Row `(4,5,5)`: `76 Alphatensor-F2`, `76 Alphatensor-Z`, naive addition count `+549` (unreduced). |
| V3R1T4S `TROPHY_CASE.md` | `TROPHY_CASE.md` | `2026-10-17T16:59:42Z` | local | `738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9` | 53 rows inspected: zero entries in `TROPHY_CASE.md` for `4x5x5`. |
| V3R1T4S merged package (PR `#222`) | `known-knowns/faster-matrix-multiplication/` (merged PR `#222`) | `2026-10-17T16:59:42Z` | local | `08d7b199e9ecc9f7254dc46c23ecf2128e83444277b19eac6bbcb678a107f819` | Merged PR `#222` establishes **`281`** reduced additions (`U = 75`, `V = 84`, `W = 122`) for `4x5x5` at rank `76`. |
| V3R1T4S open pull requests | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` | `2026-10-17T16:59:43Z` | `200` | live API | 50 open PRs inspected (`#9` through `#355`): open `fmm-additive-complexity-records` PRs are `#330` (`2x5x6`), `#313` (`2x4x7`), `#229` (`2x4x7`), `#218` (`4x5x6`), and `#205` (`5x5x5`). Zero open PRs cover `4x5x5` (or `5x4x5`, `5x5x4`). |

## 2. Literature Audit (Last 24 Months, 2024–2026)

- **Perminov (2025), arXiv:2512.13365** (*"Parallel Heuristic Exploration for Additive Complexity Reduction in Fast Matrix Multiplication"*): Table 3 reports `4x5x5` at rank `76` with naive `530`, prior literature `451`, GV `315`, GP-5 `300`, GP-40 `299`, and Perminov's proposed method `299` (matching the live `cr299` file).
- **Mårtensson and Stankovski Wagner (2025–2026), IACR ePrint 2024/2063 (ACDA 2025) & IACR ePrint 2026/849**: Table 3.3 (ternary AlphaTensor `455-76` without basis change) gives `310` additions (and `437` with basis change); Table 3.4 (over `Z`) gives `451` additions (matching `reduced_known.json` `"4x5x5-76": {"Z": 451, "Z2": 372}`).
- **Hells et al. (2026), IACR ePrint 2026/1688 & `werekorren/fmm_add_reduction`**: Public `hells_bells` scheme folders stop at `532` and include no `4x5x5` scheme.
- **Lille FMM Catalogue (`https://fmm.univ-lille.fr/4x5x5.html`)**: Lists rank `76` (citing Fawzi et al. 2022) with no reduced addition count.

## 3. Exact Novelty Comparison

- **Perminov live repository (`addition_reduced_ZT`)**: `299` (`U = 75 + V = 95 + W = 129`)
- **Perminov arXiv:2512.13365 & GP-40**: `299`
- **Mårtensson & Stankovski Wagner (ePrint 2026/849 Table 3.3)**: `310`
- **Perminov `reduced_known.json` (`Z`) / ACDA 2025**: `451`
- **Merged V3R1T4S PR `#222`**: `281` (`U = 75 + V = 84 + W = 122`)
- **Candidate (`object/4x5x5_m76_cr280_ZT_reduced.json`)**: **`280`** (`U = 75 + V = 84 + W = 121`)
- **Strict improvement**:
  - Beats Perminov's live `299` by **`-19`** additions (`280 vs 299`).
  - Beats merged V3R1T4S PR `#222` (`281`) by **`-1`** addition (`280 vs 281`).

## Verdict

The candidate straight-line program in `object/4x5x5_m76_cr280_ZT_reduced.json` (`280` reduced additions at best-known rank `76` for `4x5x5`) strictly beats Perminov's live record (`299`), all published 2024–2026 literature (`299`, `310`, `451`), and merged V3R1T4S PR `#222` (`281`), with no competing open pull requests.

pass: true
