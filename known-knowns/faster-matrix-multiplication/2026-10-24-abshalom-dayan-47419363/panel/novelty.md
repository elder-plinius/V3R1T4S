# Novelty skeptic: <18,19,19> rank 3424 over Q (target fmm-catalogue-small-format-rank, partial win p1)

context: subagent (fresh context, Agent tool, model claude-opus-5-5; saw claim/ and its own fetches)

## Bottom line

Every source I could reach lists <18,19,19> (sorted, any axis order) at 3595 or higher. The best value is 3633 in the
Lille index and fmm_sota.json, 3816 on the Lille per-format page and 3595 in matmulcatalog. No format containing
<18,19,19> is listed at 3424 or lower in any of the three tables. No pull request in this repository (open or
closed), no file in the pinned repo copy and no paper or repository I found in the last 24 months gives a rank of
3424 or lower. The claimed 3424 is strictly below every known value: 209 below the bank's two p1 sources (3633) and
171 below the lowest public value (matmulcatalog 3595). It is not a value the Lille 'construction' column produces:
that column lists Proj([[19, 0], [0]], <19x19x19:3633>), which is rank 3633. I did not check whether the scheme is
correct; another skeptic does that, and novelty depends on it.

## How I fetched

Each URL got one plain GET with curl, User-Agent "V3R1T4S-research-agent (honest single GET)", no cookies, no
proxy (`--noproxy '*'`) and no retries. The helper script is panel_work/novelty2/scripts/fetch1.sh. The log is
panel_work/novelty2/data/fetch_log.tsv: UTC time from `date -u`, HTTP status, URL, saved file, sha256 of the body
and size. Bodies and response headers are saved next to it in panel_work/novelty2/data/. Every request returned
HTTP 200. There were no blocks, challenge pages or 401/403/429/503 responses. One note on the MerlijnW70 tree URL:
my first command never sent a request, because zsh stopped on the unquoted `?` ("no matches found") before curl
ran. The single logged GET at 18:08:17Z is the only request made to that URL.

I scanned every fetched page for text addressed to reviewers. None was found.

## Primary tables (status sources), fetched 2026-10-24

| UTC time | HTTP | URL | sha256 of body | value for sorted <18,19,19> |
|---|---|---|---|---|
| 2026-10-24T18:05:46Z | 200 | https://fmm.univ-lille.fr/ (Last-Modified: Tue, 20 Oct 2026 08:14:45 GMT) | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | row `18x19x19`: name ⟨18×19×19:3633⟩, fast_tensor_rank 3633, classical 6498, construction (description column) `Proj([[19, 0], [0]],⟨19×19×19:3633⟩)` |
| 2026-10-24T18:05:47Z | 200 | https://fmm.univ-lille.fr/18x19x19.html (Last-Modified: Fri, 19 Jun 2026 21:23:26 GMT) | 7de98cb2a073dcfaa8ee3a879caaa3f6c02c1d1ab9828b9da1cf016828161490 | "Description of fast matrix multiplication algorithm: ⟨18×19×19:3816⟩", a block decomposition ⟨9×10×10:597⟩ + ⟨9×10×9:534⟩ + ⟨9×9×10:534⟩ + ... |
| 2026-10-24T18:05:47Z | 200 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | `{'format': [18, 19, 19], 'rank': 3633, 'exponent': 2.801315}`; createdAt 2026-10-19T20:46:33; 5456 entries |

The sha256 values of all three bodies match the scout's and claim-time fetches recorded in claim/TABLE_RECORD.md,
so the tables have not changed since then. The Lille index front page says "Front page is up-to-date, underlying
data are currently reconstructed". That explains why the per-format page (3816, last modified in June) is older than
the index (3633).

## Formats that contain <18,19,19> (restriction check)

Restricting a scheme for a larger format gives a scheme for <18,19,19> of at most the same rank. I parsed all 5222
rows of the Lille index, all 5456 entries of fmm_sota.json and all 11136 schemes of matmulcatalog. For each I kept
every format whose sorted dimensions are at least (18,19,19) component by component.

- Lille index, lowest such formats: (18,19,19) 3633; (19,19,19) 3633 (Khoruzhii, Gelß and Pokutta 2026); (18,19,20)
  3878; (18,20,20) 3994; (19,19,20) 3994; (19,20,20) 3994; (20,20,20) 3994. Formats at 3424 or below: none.
- fmm_sota.json, lowest such formats: [18,19,19] 3633; [19,19,19] 3633; [18,19,20] 3878; [18,20,20] 3994; [19,19,20]
  3994. Formats at 3424 or below: none.
- matmulcatalog: 1597 such schemes, the lowest being [18,19,19] 3595, [19,19,19] 3633 and [18,19,19] 3798. Schemes at
  3424 or below: none.

Splitting along one axis and summing two listed schemes does not reach 3424 either. With fmm_sota.json ranks, and
counting <1,m,p> or <n,1,p> as m·p or n·p, the best split is 3697 = <18,18,19> 3355 + <18,1,19> 342. The
matmulcatalog Q/Z/R ranks give the same best split, 3697.

## Other catalogues and repositories

| UTC time | HTTP | URL | sha256 | finding |
|---|---|---|---|---|
| 2026-10-24T18:06:50Z | 200 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json (Chatain Lacelle, arXiv 2606.13408) | 5c600b98b4bb8f9feed5b4d9ffabf11af34b98f49bf43ae250b81e71f43e000b | 11136 schemes, max_dim up to 32. Two entries for [18,19,19]: rank 3595 (fields Q,R,C; lineage_compact `19x19x19 ∖[9||]`; file derived/section19/18x19x19-r3595-derived-b13fd17.json; external_best_rank 3633, fmm-lille) and rank 3798 (lineage `R[2x2x2; 9,9 \| 9,10 \| 7,12]`). Nothing at or below 3424. |
| 2026-10-24T18:12:18Z | 200 | https://api.github.com/repos/solven-eu/matmulcatalog/commits?per_page=5 | 175bd77d308a284d74b66af5854a9f55a8219a53b6e0b2bee1c66003cc7cf44a | latest commit de26810759, 2026-10-21T04:14:18Z, "Regenerate docs/*.json + upstream comparison reports", so the catalog.json above is three days old |
| 2026-10-24T18:08:11Z | 200 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | sections run only to "Section 16 — max-dimension = 16"; no <18,19,19> row |
| 2026-10-24T18:08:11Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 52db72a9cd408815d98ebcd851d55fb13b8d84eaa70b7ebd7c4de67cc29b9e61 | scope stated as "from `2x2x2` to `16x16x16`" and "max(n₁, n₂, n₃) ≤ 16"; no <18,19,19> |
| 2026-10-24T18:08:17Z | 200 | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/HEAD?recursive=1 | e6866337cf18c6f4bb9d2b950240341d901260e28b560a301853202c03b1a5fc | 39 tree entries (truncated: False); largest dimension in any file name is 16; no <18,19,19> |
| 2026-10-24T18:06:51Z | 200 | https://raw.githubusercontent.com/khoruzhii/lita/master/README.md | 97df246f15643a7396307765d23432d03bcb5af97a9f8bf92cae85cb428d5b3f | square schemes only: even N table (18: 3031, 20: 3994, ...) and odd table (17: 2723, 19: 3633, 21: 4723, ...); no rectangular schemes |
| 2026-10-24T18:06:52Z | 200 | https://api.github.com/repos/khoruzhii/lita/contents/schemes | 8d289a9bcacbc9f7bfb4c824b2647bdedb8e1eedb1200bb7a22bf7594e4e6cd9 | 20 files, all square, 13x13x13_r1379.npz through 32x32x32_r14196.npz (including 18x18x18_r3031.npz, 19x19x19_r3633.npz, 20x20x20_r3994.npz); no 18x19x19 file |

## This repository (pull requests and the pinned copy)

| UTC time | HTTP | URL | sha256 | finding |
|---|---|---|---|---|
| 2026-10-24T18:06:49Z | 200 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+is:pr+fmm-catalogue-small-format-rank&per_page=100 | af891869319f6a948b03c2c358feb6074d90371d74d2a9b7807354cfb7fba078 | total_count 32, incomplete_results False, 32 items, open and closed |
| 2026-10-24T18:06:50Z | 200 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+is:pr+18x19x19&per_page=100 | c9938edecb99d754b2d039ac9eec320a94c769b6a6417921e2dcbef9e2fe01a0 | total_count 0 |

What the 32 pull requests hold:
- Two open claims for fmm-ternary-integer-ring-upgrade: #402 (9x12x14) and #432 (14x15x15).
- 29 claims for this target, merged or closed, every one for a format with max dimension 18 or less. The largest are
  #46 (17,18,18) rank 2968, #45 (17,17,18) rank 2916 and #51 (16,18,18) rank 2900. All of these closed claims count
  as prior public work. None is for a format that contains <18,19,19>. A <17,18,18> or <18,18,18> scheme can only
  feed <18,19,19> by adding blocks, and the best such split from listed values is 3697, as shown above.
- One closed bank update, #399.

I also scanned the titles and bodies of all 32 for any three-number format with a 19 in it, and for the string
"3424". The only matches were false positives, such as comma-grouped large numbers in #399, #402 and #432. The
search API body has the same sha256 as the scout's fetch at 2026-10-24T17:40:57Z.

Pinned repo copy (read only):
- TROPHY_CASE.md (100 lines) has five matrix multiplication rows: <15,16,16> 2180, <14,15,15> 1842, <13,14,14> 1558,
  <14,14,15> 1716 and <13,14,15> 1677, the last three superseded by later contributed schemes. Nothing has a
  dimension above 16.
- known-knowns/faster-matrix-multiplication/INDEX.csv and the INDEX.csv files of its 39 dated contribution folders
  cover formats up to 15x16x16 only.
- A grep of the whole copy (excluding .git) for 18x19x19, 19x18x19, 19x19x18, "18, 19, 19", 18×19×19, <18,19,19>,
  ⟨18,19,19⟩ and 19x19x19 found nothing. The only hits for "3424" were numbers inside graph edge lists and model
  files, unrelated to matrix multiplication.

## Literature, last 24 months (2024-10 to 2026-10)

These were web searches, plus one curl GET per paper page I opened. The opened pages were scanned for any
18/19/19 format and for "3424":

| source | what it covers | <18,19,19> at or below 3424? |
|---|---|---|
| Chatain Lacelle, "A catalog of fast matrix multiplication algorithms with exhaustive derivations", arXiv 2606.13408 (v1 2026-06-11, v3 2026-08-14). Abs page fetched 2026-10-24T18:10:31Z, sha256 9a31847c…; HTML v1 fetched 2026-10-24T18:10:31Z, sha256 83611dc9… | catalog to <32,32,32>; claims 908 wins in the 17..32 band (2026-07-12 snapshot) | no; its data (catalog.json above) gives 3595 |
| Khoruzhii, Serafin, Gelß, Pokutta, LITA (GitHub; manuscript "in preparation", no arXiv listing found) | square N×N×N only | no; 19x19x19 is 3633, and restricting it naively gives 3633 (Lille) or 3595 (matmulcatalog) |
| Kauers and Wood, "Consequences of the Moosbauer-Poole Algorithms", arXiv 2505.05896 (HTML v1 fetched 2026-10-24T18:10:31Z, sha256 c4b7567b…) | flip-graph improvements for small rectangular formats seeded by 5x5x5:93 and 6x6x6:153 | no hit for 18/19/19 or 3424 |
| Kauers and Wood, "Exploring the Meta Flip Graph for Matrix Multiplication", arXiv 2510.19787 (abs fetched 2026-10-24T18:13:04Z, sha256 2c4dc52e…; HTML v1 fetched 2026-10-24T18:13:13Z, sha256 40cd9142…) | "improved rank bounds for about thirty matrix formats" | no hit for 18/19/19 or 3424 |
| Perminov, arXiv 2606.02480 (abs fetched 2026-10-24T18:13:04Z, sha256 176c25e2…), plus 2603.02398 and 2511.20317 (seen in search results only) | "all 680 rectangular formats with dimensions up to 16 × 16 × 16" | out of scope (max dimension 16) |
| Novikov et al., "AlphaEvolve", arXiv 2506.13131 (abs fetched 2026-10-24T18:13:05Z, sha256 7a0d9acc…) | small formats (4x4x4 rank 48 over C, 14 settings per secondary sources) | out of scope |
| Uznański, "Rectangular matrix multiplication from polynomial products", arXiv 2610.10494 (v2 2026-10-11; abs and HTML fetched 2026-10-24T18:12:02Z, sha256 b516332d… and c8047057…) | asymptotic exponents ω(1,k,1), no finite-format ranks | no hit for 18/19/19 or 3424 |
| arXiv 2512.21980 (abs fetched 2026-10-24T18:10:31Z, sha256 bea1a3ee…), "A 58-Addition, Rank-23 Scheme for General 3x3" | 3x3x3 additions | out of scope |
| Schwartz and Zwecher, arXiv 2508.01748 (search result only) | trilinear aggregation exponent at N=44 | out of scope (square, asymptotic) |

The web search queries were:
- "matrix multiplication 18x19x19 rank scheme"
- "Local Improvements to Trilinear Aggregation" Khoruzhii Pokutta
- matmulcatalog Chatain Lacelle arXiv 2606.13408
- fast matrix multiplication new ranks rectangular formats up to 32 2026 arXiv flip graph
- "19x19x19" OR "18x19x19" matrix multiplication rank 3633
- LITA trilinear aggregation rectangular matrix multiplication schemes derived restriction 2026 new ranks 17 to 32
- AlphaEvolve matrix multiplication tensor decomposition ranks formats 2025

None of them turned up a rank for <18,19,19> in any axis order (18x19x19, 19x18x19, 19x19x18) at or below 3424. The
lowest published value I found anywhere is 3595 (matmulcatalog). Web search coverage is never complete: a result
posted in the last few days and not yet indexed would be missed. Every catalogue named in the bank entry was read
live today.

## Check against the p1 wording

- Strictly below the live fmm_sota.json entry: 3424 < 3633. Yes.
- Strictly below the live Lille per-format page: 3424 < 3816. Yes. It is also below the live Lille index row, 3633.
- Not a plain composition already listed in the Lille construction column: the listed construction
  Proj([[19, 0], [0]], ⟨19×19×19:3633⟩) gives 3633, not 3424. The claim's general one-slice restriction (208 terms
  vanish, 3425 remain) followed by a 2-reduction (3424) gives a value no catalogue lists.
- Strictly below everything else known: matmulcatalog 3595. Perminov, MerlijnW70 and matmulcatalog COVERAGE.md do
  not cover max dimension 19. No pull request and no repo file lists this format. This is not a tie.
- Level: p1 only, since max(18,19,19) = 19 lies in 17..32. The main criterion needs max <= 16.

## Files

- claim/CLAIM.md and claim/TABLE_RECORD.md: read
- panel_work/novelty2/scripts/fetch1.sh: single-GET helper
- panel_work/novelty2/scripts/grepfmt.py: page scanner for 18/19/19 and "3424"
- panel_work/novelty2/data/fetch_log.tsv: one line per GET
- panel_work/novelty2/data/lille_index.html, lille_18x19x19.html, fmm_sota.json: the status sources
- panel_work/novelty2/data/matmulcatalog_catalog.json, matmulcatalog_COVERAGE.md, matmulcatalog_commits.json,
  perminov_README.md, merlijnw70_tree.json, lita_README.md, lita_schemes_listing.json: other catalogues
- panel_work/novelty2/data/gh_search_pr_target.json, gh_search_pr_18x19x19.json: pull request searches
- panel_work/novelty2/data/arxiv_*.html: literature pages
- each fetched body has a `.headers` file with the response headers

pass: true
