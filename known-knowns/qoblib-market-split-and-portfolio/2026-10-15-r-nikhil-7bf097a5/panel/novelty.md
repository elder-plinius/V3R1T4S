# NOVELTY verdict
context: codex exec (fresh context via codex-fresh)

The selected result passes the novelty comparison: **−1,696,664 < −1,090,282**, a strict improvement of **606,382** objective units over the strongest comparable public result found. This is for **QOBLIB class 06, `po_a400_t10_s00`, B=100, lambda=0.01**, with the other reference-model parameters fixed as in `CLAIM.md`. Lower is better. This is an objective-value record for that cell, not a claim of optimality or a new optimization method.

## Mandatory primary fetch

- **URL:** https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/README.md
- **Value:** **no published entry for `a400_t10_s00_b100_l1e-02`**. The response has 129 instance rows and no a400 row. Absence is not a numerical incumbent.
- **Time:** **2026-10-15 17:22:09.206925 UTC**, response completed; request began at 17:22:08.523155 UTC.
- **Receipt:** HTTP **200**, exactly **one HTTP request**, no redirect or retry; 10,450 bytes; SHA256 `05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a`.
- Saved response: `novelty/primary.body`; complete receipt: `novelty/primary.meta.json`; request code: `novelty/fetch_once.py`.

## Public incumbents, trophy case, and open PRs

I reused the successful current snapshots identified in `comparison/CURRENT_SOURCES.md`, verified all 18 response hashes against their metadata, and searched the complete supplied open-PR lists: **25 QOBLIB PRs** and **62 V3R1T4S PRs**. Neither list has a next-page link.

| Source | Comparable value or finding | Source receipt time, UTC |
|---|---|---|
| https://github.com/ZIB-AOPT/QOBLIB/pull/87 | **−1,090,282**, selected cell, RestrictedChainDP | Current PR list: 2026-10-15 17:20:19; solution fetched 13:20:15 |
| https://github.com/ZIB-AOPT/QOBLIB/pull/64 | **−459,673**, selected cell, 4colors-Optimizer | Current PR list: 2026-10-15 17:20:19; solution fetched 13:21:49 |
| https://github.com/ZIB-AOPT/QOBLIB/pull/44 | a003–a010 instances; no selected-cell result | 2026-10-15 17:20:19 |
| https://github.com/ZIB-AOPT/QOBLIB/pull/92 | a200 orig and s00, B=50; different cells | 2026-10-15 17:20:19 |
| https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | No QOBLIB/portfolio entry | 2026-10-15 17:20:50 |
| https://github.com/elder-plinius/V3R1T4S/pulls | Relevant PRs #170 and #176 concern the two a200 cells; no selected-cell duplicate | 2026-10-15 17:20:21 |

The current PR #87 and #64 heads remain `1772e1d7f5341b1b87f7e66029cf143b075ca259` and `e2fefab5060ea7f65fd906048d8dcb98b02643ed`, respectively, matching the pinned solution URLs in `comparison/SOURCES.md`. The saved files are `comparison/pr87-a400.sol` and `comparison/pr64-a400.sol`.

I separately inspected **issue comments, inline review comments, and review-summary bodies**. Counts in that order are #44: **14/0/0**; #64: **3/0/0**; #87: **3/0/0**; #92: **0/0/0**. No comment introduces a stronger selected-cell value. The four `/pulls/{number}/reviews` responses really are supplied, separately fetched HTTP-200 empty arrays, at 17:20:10–17:20:13 UTC. The historical missing-review note in `data/supplemental/coverage.json` therefore does not describe current coverage. Historical dates were retained.

Running the supplied rational checker sequentially reproduced feasibility and objectives **−1,696,664**, **−1,090,282**, and **−459,673** for the candidate and both incumbents. Output is in `novelty/checks.txt`. This is a rerun of the supplied checker, not a newly written independent correctness proof.

## Literature: 2024-10-15 through 2026-10-15

I searched arXiv for QOBLIB, QUBOLib, and quantum portfolio benchmarks, then broadened to `portfolio AND (benchmark OR QOBLIB)` without requiring quantum terminology. The responses contain **32** and **430** records, **434 distinct records** together, with no omitted pagination. I screened their metadata and abstracts for comparable instance/model results. I also searched Crossref within the same date window, examining its first 100 relevance-ranked results, and used the supplied 30-result framework search. Exact query URLs, times, and raw responses are in `novelty/arxiv-search.meta.json`, `novelty/arxiv-broad.meta.json`, and `novelty/crossref-search.meta.json`; parsed records are in `novelty/literature-search.json` and `novelty/literature-broad.json`.

The closest full texts checked were:

| Literature | Finding relevant to this cell |
|---|---|
| QOBLIB, https://arxiv.org/html/2504.03832v1 and https://arxiv.org/html/2504.03832v2 | v1 Table 6 is a200/B=50; v2 Table 6 is a050/B=20. Neither reports an exact selected-cell incumbent. |
| https://arxiv.org/html/2502.05226v1 | Dynamic-portfolio experiments use n200/T10 and n499/T15, B=60; different cells/data. |
| https://arxiv.org/html/2603.23200v1 | Block-coordinate CIM experiments use six assets and 22 trading intervals. |
| https://arxiv.org/html/2607.03218v1 | Different asset-weight, class-exposure and turnover-constrained model; no selected-cell result. |
| https://arxiv.org/html/2509.17876v3 | A variance-minimizing benchmark of 270 instances; different formulation/data. |
| https://arxiv.org/html/2604.22625v1 | FlashFolio solves convex portfolio programs; no selected QOBLIB integer-cell result. |

Full responses and extracted text are saved under `novelty/`. The supplied framework landing page is metadata, not full-text evidence of a competing record. The historical QUBOLib index from https://zenodo.org/records/23027944/files/qubolib.tar.gz (receipt **2026-10-15 14:35:53 UTC**) contains 128 portfolio instances: 64 a010 and 64 a050, **no selected a400 cell**. I verified the supplied index hash and queried it read-only.

## Independent public repositories

I checked the supplied untruncated KenWuqianghao and mnn31 trees, fetched their README/result summaries, and followed additional public repositories named in the historical source ledger. KenWuqianghao's 27-value table has other a400 cells and lambdas, but no selected-cell result; mnn31's independent result documentation covers the small exact-DP instances, with its large selected-cell submission already counted as PR #87.

Additional checked sources were MaldoAlberto/negsearch's portfolio table and instance definitions (a003–a010, altered parameters); daviondk/qubo-gnn's comparison/results tables (OR-Library port1–port5); iconbaypark2900/quantum-hybrid-portfolio's QOBLIB runtime documentation (adapter capped at 15 assets); MysticCodingCat/CUDA-Native-HUBO (cubic portfolio objective); YaroslavPelekhov/Quantum (QOBLIB MIS); and r-nikhil/INVENTA (the two a200 results). None supplies a tie or improvement for the selected cell. Their exact raw URLs, acquisition times and response hashes accompany the saved `novelty/*.body` files in matching `.meta.json` receipts.

All **22 new public requests returned HTTP 200**, with one attempt per URL. Previously blocked providers in the historical ledger were not retried. Computation used sequential standard-library Python with numerical thread settings at one, bounded response reads and streaming covariance checks; no installs or authentication. The resource-limit setup failed before any primary HTTP request, and the optional timing wrapper could not query a macOS clock statistic after all three checker runs passed; these details are retained in `novelty/summary.json`.

The record comparison is strictly favorable against all comparable published values found in this search. No tie was accepted.

pass: true
