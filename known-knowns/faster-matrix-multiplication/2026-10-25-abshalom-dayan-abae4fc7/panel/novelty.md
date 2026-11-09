context: subagent (Claude Opus 5.5, fresh context, given only a copy of claim/)

# Novelty check: <14,14,15> rank 1709 over Q (target fmm-catalogue-small-format-rank, main criterion)

Each URL below was fetched once with one plain GET (curl, User-Agent "V3R1T4S-research-agent (honest single GET)",
no cookies, no retries). Times are UTC from `date -u`. The sha256 is of the saved body. Raw bodies and the log
are in fetch/ (fetch/fetch_log.txt) next to this file. No fetch was blocked.

## The four criterion sources plus matmulcatalog (sorted format (14,14,15), every orientation)

| fetched (UTC) | HTTP | URL | sha256 | value read |
|---|---|---|---|---|
| 2026-10-25T10:09:20Z | 200 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | `{'format': [14, 14, 15], 'rank': 1789}`; this is the only entry whose sorted format is (14,14,15) |
| 2026-10-25T10:09:20Z | 200 | https://fmm.univ-lille.fr/14x14x15.html | 63ce18bf1085d0f315839876c397d7ff9bfe725fa5fd998883f382a14e6b907a | "<14x14x15:1798>", taken from Perminov, FastMatrixMultiplication, GitHub, February 2026 |
| 2026-10-25T10:09:20Z | 200 | https://fmm.univ-lille.fr/ (index, the bank's status_source) | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | row "<14x14x15:1789>", construction column "<14x14x1:196> + <14x14x14:1593>" (a plain composition) |
| 2026-10-25T10:09:21Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 77203a718e82fec693578d193c9ccbb2332edcf41f086088a8405cd403666c5a | "`14x14x15` / 1798 (?) / 1798 (1813) / 1790 (1813)": ZT 1798, Z 1798, Q 1790; minimum 1790 |
| 2026-10-25T10:09:21Z | 200 | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | e6866337cf18c6f4bb9d2b950240341d901260e28b560a301853202c03b1a5fc | no path for 14x14x15, 14x15x14 or 15x14x14 |
| 2026-10-25T10:09:22Z | 200 | https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/README.md | 6ef17ff86e9a74b710e4e6173f67187b735ecdef760d2634a16d33bdf73b904b | no 14x14x15 row (nearest rows are 13x13x15 and 11x14x14) |
| 2026-10-25T10:09:22Z | 200 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json | 5c600b98b4bb8f9feed5b4d9ffabf11af34b98f49bf43ae250b81e71f43e000b | 8 entries for sorted (14,14,15): 1789 (derived, "naive-14x14x1 +p 14x14x14"), 1790 (Perminov 2023, Q), 1798, 1798, 1799, 1799, 1812, 1813; lowest 1789 |

The minimum over the four criterion sources is **1789** (fmm_sota.json and the Lille index). The per-format Lille page
says 1798. The bodies of fmm_sota.json, the Lille per-format page, the Lille index, ranks.md and the MerlijnW70 tree
match the author's hashes in claim/TABLE_RECORD.md exactly, so these sources have not changed since the claim.

## This repository (elder-plinius/V3R1T4S, read-only API GETs; main is at 1ebdef41c30414cd2a036b00f5e81d0fc4c1dc25, 2026-10-24T16:13:09Z)

| fetched (UTC) | HTTP | URL | sha256 | value read |
|---|---|---|---|---|
| 2026-10-25T10:09:23Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 | entry 47: "<14,14,15> rank 1716 over Q"; no lower <14,14,15> entry and no superseding note for it (the notes cover 2180, 1558, 1677 only) |
| 2026-10-25T10:09:23Z | 404 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/INDEX.csv | (404 body) | no top-level INDEX.csv; the family file below is the right one |
| 2026-10-25T10:09:48Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | e49a030f07630ba8def4ae850727750719a3401efe6da1940ad03fc80ee8874c | 5439 paths, not truncated. The only 14x14x15 file is known-knowns/faster-matrix-multiplication/schemes/14x14x15_r1716_Q.json. None of the 39 contributed folders under faster-matrix-multiplication/ holds a 14x14x15 (or permuted) object |
| 2026-10-25T10:10:17Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | row 14x14x15 rank 1716 ("peel of our 14x15x15 rank 1843") |
| 2026-10-25T10:10:17Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-unknowns/algorithms/fmm-catalogue-small-format-rank.md | bd5a841310037fba869e8c1120f26287111c403e21914e8c68d78dd78c27072f | target file (read for context only) |
| 2026-10-25T10:10:17Z to 10:10:24Z | 200 x 8 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1..8 | p1 167bb277…, p2 3169b48e…, p3 05fd81ff…, p4 ad589e9f…, p5 d27d4c26…, p6 f801d074…, p7 2adbdd5e…, p8 734ac8b8… (full hashes in fetch/fetch_log.txt) | 710 PRs (#1 to #735), open, closed and merged |
| 2026-10-25T10:10:55Z | 200 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+14x14x15&per_page=100 | 0d5a7f526bf81fb4c38836f7f630c5a39785d3dffc17896b5c22ae6046cf5520 | total_count 1: PR #6 |

I searched the titles and bodies of all 710 PRs for "14x14x15", "14x15x14", "15x14x14", "<14,14,15>", "<14,15,14>",
"<15,14,14>", "(14, 14, 15)", "(14, 15, 14)", "(15, 14, 14)", "14,14,15", "14×14×15", "⟨14,14,15⟩" and
"14 x 14 x 15", with and without spaces. Two PRs match:
- #6 (closed 2026-10-14T12:52:42Z, not merged, by calgulbenkian): "format (14, 14, 15) rank 1715 over Q (beats 1789 bar)",
  object 14x14x15_r1715_Q.json. This confirms the author's 1715.
- #399 (closed, not merged): a bank refresh that only quotes the catalogue change <14,14,15> 1790 -> 1789. It contains no scheme.
None of the open fmm PRs (#708, #714 are <18,...> p1 claims; the rest are ternary or additive) touches this format.
The author's facts check out: 1716 merged (TROPHY_CASE #47) and 1715 in closed PR #6. Nothing in the repository or its PRs is at or below 1709.

## Parent and literature (last 24 months)

| fetched (UTC) | HTTP | URL | sha256 | value read |
|---|---|---|---|---|
| 2026-10-25T10:10:54Z | 200 | https://api.github.com/repos/khoruzhii/lita/git/trees/HEAD?recursive=1 | 75d497884cdff3414cc1b996c21083229d2984437f308186a686048ba4f7ee57 | schemes/ holds only cubes NxNxN, N = 13..32 (14x14x14_r1593, 15x15x15_r1977, ...); no rectangular scheme |
| 2026-10-25T10:10:54Z | 200 | https://raw.githubusercontent.com/khoruzhii/lita/HEAD/README.md | 97df246f15643a7396307765d23432d03bcb5af97a9f8bf92cae85cb428d5b3f | square ranks only (N=15: 1977 from R_odd formula; N=14: 1593); mentions 2-reduction tools; no rectangular formats and no slice-cutting to <14,14,15> |
| 2026-10-25T10:10:54Z | 200 | https://api.github.com/repos/khoruzhii/lita/commits?per_page=20 | cf34a56c78a4ff03e87c58e8a4eae6c3b0602bf84ed38574c3f057e1a23350f4 | latest commit 2026-10-07 ("Improve even LITA construction"); nothing about rectangular schemes |

Web searches (WebSearch, 2026-10-25, around 10:11Z):
- LITA (Khoruzhii, Serafin, Gelß, Pokutta): I found no arXiv preprint for LITA itself, only the repository and a LinkedIn
  post about exponents at N=42. The related arXiv 2511.10786 (Khoruzhii, Gelß, Pokutta, flip-graph search for
  structured matrix multiplication) covers small structured formats and does not include <14,14,15>.
- Perminov, arXiv 2603.02398 (March 2026, "Fast Matrix Multiplication in Small Formats"): its 680-format table up to
  16x16x16 is the same source as docs/ranks.md (Q 1790 for 14x14x15). Perminov, arXiv 2511.20317 (ternary meta flip
  graphs): small formats only.
- Kauers and Wood, arXiv 2505.05896 and 2510.19787 (meta flip graph; Arai et al.'s "plus" transitions): about thirty
  improved formats, all far smaller than <14,14,15>.
- Schwartz and Zwecher, arXiv 2508.01748 (trilinear aggregation, ISSAC 2026): asymptotic exponent and large square
  base cases; no <14,14,15> rank.
- AlphaEvolve/AlphaTensor follow-ups and SAT/Heule-style work concern formats up to about 6, so they do not apply here.
- Searches for "14x14x15", "⟨14,14,15⟩" or "14×14×15" with rank, matrix multiplication or upper bound found only Lille
  pages of neighbouring formats and lower-bound papers. No published <14,14,15> scheme below 1789 turned up outside this repository.

## Composition clause

The only construction listed for this cell is the Lille/matmulcatalog composition <14,14,1>+<14,14,14> = 196+1593 = 1789.
The claim's construction (claim/CLAIM.md, claim/rebuild/) restricts LITA's 15x15x15 r1977 by two exact slices and then
applies exact 2-reductions. 1709 does not equal any listed composed value. Simple compositions from the public parts
(for example 1593+196, or 13x14x15 1645 + <1,14,15> 210 = 1855) all come out above 1789.

## Verdict

Best known value for <14,14,15> (any orientation):
- Public catalogues named by the criterion: **1789** (fmm_sota.json; Lille index, composition). The Lille per-format page says 1798 and Perminov's minimum is Q 1790. MerlijnW70 has nothing for this format.
- Anywhere public, including this repository: **1715** (closed PR #6, calgulbenkian, 2026-10-14; it was not merged but is public), then 1716 (merged, TROPHY_CASE #47).

The claimed rank 1709 is strictly below all of them: 80 below the criterion minimum 1789, 6 below 1715 and 7 below 1716.
It is not a tie and not a listed composition. I found no source at or below 1709. Exactness and correctness of the
scheme are for the other skeptics; this file judges novelty only.

pass: true
