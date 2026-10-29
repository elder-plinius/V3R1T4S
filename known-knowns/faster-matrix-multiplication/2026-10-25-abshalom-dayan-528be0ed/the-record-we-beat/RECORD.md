# The record we compare against: <30,30,31> and its permutations

Rank does not change when the format is permuted, so every source was searched for all axis orders (30x30x31, 30x31x30, 31x30x30). Every fetch was one plain GET (curl with the User-Agent "V3R1T4S-research-agent (honest single GET)", no cookies, no retries; GitHub API reads were plain GET requests to api.github.com). Times are UTC from `date -u`; sha256 is of the saved body. The complete log of every request (shared by the four cells of this batch; rows dated 2026-10-24 are carried over unchanged from the earlier 8-cell batch (the files in data/ are those very files) and rows dated 2026-10-25 are new GETs of this batch; the 2026-10-24 pull-request list and main-branch rows were superseded by the 2026-10-25 re-read) is FETCH_LOG.txt next to this file. Pages are not copied here. Looking the format up in the saved pages is code/table_lookup.py (output: table_lookup.txt); the pull-request and arXiv scans are code/novelty_scan.py (output: novelty_scan.txt).

## The bank's p1 sources (fmm_sota.json and the Lille catalogue)

| fetched (UTC) | HTTP | URL | sha256 of body | value for the cell |
|---|---|---|---|---|
| 2026-10-24T22:35:43Z | 200 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (fmm_sota.json) | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | `{"format": [30, 30, 31], "rank": 12789}`; createdAt 2026-10-19T20:46:33; 5456 entries; no entry for the other axis orders (the digest lists sorted formats) |
| 2026-10-24T22:35:44Z | 200 | https://fmm.univ-lille.fr/ (Lille catalogue index, the bank's status_source) | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | row 30x30x31: 12789, construction column: ⟨30×30×1:900⟩ + ⟨30×30×30:11889⟩; Last-Modified Tue, 20 Oct 2026 08:14:45 GMT. No row for the other axis orders |
| 2026-10-25T07:25:19Z | 200 | https://fmm.univ-lille.fr/30x30x31.html (Lille per-format page) | a3cf5c52c4a678248f250acbd25747e5b8fef066476f119e45ae7aef345931c3 | The algorithm ⟨30×30×31:13610⟩ could be constructed using the following decomposition: ⟨30×30×31:13610⟩ = ⟨30×30×1:900⟩ + ⟨30×30×30:12710⟩ .; Last-Modified Mon, 21 Nov 2022 11:35:27 GMT |
| - | - | https://fmm.univ-lille.fr/<other axis orders>.html | - | not fetched in this batch (the catalogue has pages for sorted formats only; all 16 non-sorted pages fetched for the earlier 8-cell batch were Not Found, HTTP 404) |

fmm_digest repository head when checked: commit 42d2933cf0, 2026-10-20T08:11:11Z. The fmm_sota.json and the Lille index fetched here are byte-identical (same sha256) to the copies fetched at 2026-10-24T19:05:59Z for the sibling <18,18,19> claim (2a653515..., 57e936b6...), so these two tables did not change between the two fetches.

The per-format page (13610) is older than the index and the digest (12789); the catalogue front page says its underlying data are being reconstructed. The bar from the bank's two p1 sources is 12789 (the lower of the digest and the index values, both 12789).

## Other comparators (kit/POLICY.md, FMM section, and the bank's other sources)

| fetched (UTC) | HTTP | source | sha256 | finding for <30,30,31> (any order) |
|---|---|---|---|---|
| 2026-10-24T22:35:44Z | 200 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json | 5c600b98b4bb8f9feed5b4d9ffabf11af34b98f49bf43ae250b81e71f43e000b | schemes listed for the format in any order (rank; lineage; fields): 12789 (naive-30x30x1 +p 30x30x30; Q,R,C); 12790 (naive-30x30x1 +p 30x30x30; Q,R,C); 13309 (31x31x31 ∖[15|15|]; Q,R,C); 13572 (naive-30x30x1 +p 30x30x30; Q,R,C). external_best_rank 12789 (fmm-lille); nothing below the table value |
| 2026-10-24T22:35:45Z | 200 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | no row (sections stop at max dimension 16) |
| 2026-10-24T22:35:45Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 77203a718e82fec693578d193c9ccbb2332edcf41f086088a8405cd403666c5a | no row; largest dimension in any format name 16 |
| 2026-10-24T22:35:45Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/additions.md | 408d8f898e841dca75606d5c18937ec036d8a8b86ac1be11310b11d76da4a1f0 | no row; largest dimension in any format name 16 (the file differs from the sibling run's 19:06Z copy: Perminov pushed a commit at 2026-10-24T21:35:33Z) |
| 2026-10-24T22:35:46Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 52db72a9cd408815d98ebcd851d55fb13b8d84eaa70b7ebd7c4de67cc29b9e61 | scope up to 16x16x16; no row |
| 2026-10-24T22:36:00Z | 200 | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 8ef0a8a125664f6ddf3f849fbadf5842f27648ad45fcf42d31c3efe2c48f9996 | 6865 paths, not truncated; largest dimension in any path 16; no path for the format; repository head 17c09f4d0f, 2026-10-24T21:35:33Z |
| 2026-10-24T22:36:01Z | 200 | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/HEAD?recursive=1 | e8beb36f9a59f2d400c6a8503273017983ecd8971e27af1ab40788db3279a22b | 39 paths, not truncated; largest dimension 16; no path for the format |
| 2026-10-24T22:36:02Z | 200 | https://api.github.com/repos/khoruzhii/lita/contents/schemes | 5ae1ba358b3bcde175717b3509bbfb2d51a7859f334b30e5a92a3a129338b185 | 20 square schemes 13x13x13 ... 32x32x32 (31x31x31 r13433 is the one this scheme is cut from); no rectangular scheme |
| 2026-10-24T22:36:02Z | 200 | https://api.github.com/repos/khoruzhii/lita/commits?per_page=3 | 0cda42a19c59bdb6d003d15635c6da40c2084484ab0012b1d197dac165817779 | head 472a79fbc8, 2026-10-07T19:22:13Z |
| 2026-10-24T22:35:46Z | 200 | https://raw.githubusercontent.com/khoruzhii/lita/472a79fbc8248423a97bebb3aacbc89e769b9b3e/README.md | 97df246f15643a7396307765d23432d03bcb5af97a9f8bf92cae85cb428d5b3f | README at the pinned commit; states the manuscript is in preparation (read for credit only) |
| 2026-10-24T22:36:03Z | 200 | https://api.github.com/repos/sedoglavic/fmm_digest/commits?per_page=3 | 90efc74092e30c3e76e738bc34902e14feec6f511f77fb26b3ad71f9df394be9 | head 42d2933cf0, 2026-10-20T08:11:11Z |
| 2026-10-24T22:36:03Z | 200 | https://api.github.com/repos/solven-eu/matmulcatalog/commits?per_page=3 | 9b18c46469f4110e4e11f6c17772d1816ae2f50cd3eb4dc51e0a119298ef676b | head de26810759, 2026-10-21T04:14:18Z |

Formats that contain <30,30,31> componentwise (restricting them gives the cell at the same or a lower rank): the lowest in fmm_sota.json are 30x30x32 13254, 30x31x31 13433, 31x31x31 13433, 30x31x32 14196. None is at or below 12395.

## This repository (elder-plinius/V3R1T4S)

| fetched (UTC) | HTTP | query | sha256 | finding |
|---|---|---|---|---|
| 2026-10-25T07:25:23Z to 2026-10-25T07:25:29Z | 200 (7 pages) | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1..7 | see FETCH_LOG.txt | 698 pull requests (#1 to #722; 350 open, 198 closed, 150 merged). Titles and bodies scanned for the format in any axis order and notation and for the numbers 12395, 12789, 12790, 13309, 13572, 13610: 0 pull requests name the format (any axis order or notation) and 0 contain one of these numbers (novelty_scan.txt) |
| 2026-10-24T22:36:43Z to 2026-10-24T22:38:05Z | 200 (121 requests) | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/N/files?per_page=100 for the 121 FMM-related pull requests | see FETCH_LOG.txt | 2969 file names (first 100 files of each; PRs #465 and #616 have 100 or more): none names the format or contains these numbers; the largest NxMxP in an FMM PR file name is 19 (#708 and #714); the file lists are carried over from 2026-10-24 (those PRs did not change); the 7 pull requests created since (#716 to #722) are not FMM-related by title or branch, so their file lists were not fetched, but their titles and bodies are in the scan |
| 2026-10-25T07:25:51Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | b1f7db3b79a823a824cd42da5e80f5c671ae03ca303e056686fb78a411fd9a0b | 5439 paths, not truncated; largest dimension in any FMM path 16; nothing for the format |
| 2026-10-25T07:25:51Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | no row for the format |
| 2026-10-25T07:25:52Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 | no row for the format |
| 2026-10-25T07:25:52Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/commits?per_page=3 | a2fca2872220514df41bec5e1bd6af794dae6192d2983dbbefeabc44ecb0e18a | main head 1ebdef41c304 at the time of this fetch; newest pull request #722 |

Sibling cells: PR #708 (<18,19,19> 3424) and PR #714 (<18,18,19> 3225) are the sibling cells of the 19-family, built by the same two slices from LITA's 19x19x19 scheme. Neither names this format.

## Literature

- arXiv API, author search "Khoruzhii" (fetched 2026-10-24T22:41:54Z, HTTP 200, sha256 ec7db8baadf6ba5046351808f2244f324e954d16674421d1b665d9e0aa14d928): 13 entries (2000 to 2026-07-02); none gives a rank for <30,30,31>, none is the LITA manuscript (its README says the manuscript is in preparation).
- arXiv API, the 100 most recent papers with "matrix multiplication" and "rank" in the abstract (fetched 2026-10-24T22:41:54Z, HTTP 200, sha256 86c2ae9936afe014c35cb3c1067210e0ca4f5fe92307cb730fcd420122eb37ef; 2025-03-07 to 2026-10-19): no abstract names the format in any order or one of the ranks above.
- No further literature search (web search, full texts) was run for this cell; a rank for this format in a paper not found by these two queries cannot be excluded.

## Lowest public value for <30,30,31> in any axis order

**12789**: fmm_sota.json and the Lille index (also matmulcatalog). fmm_sota.json and the Lille index list **12789** (construction: ⟨30×30×1:900⟩ + ⟨30×30×30:11889⟩); the Lille per-format page shows 13610. The claimed 12395 is 394 below 12789 and 394 below the table value 12789.
