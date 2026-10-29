# The record we compare against: <26,27,27> and its permutations

Rank does not change when the format is permuted, so every source was searched for all axis orders (26x27x27, 27x26x27, 27x27x26). Every fetch was one plain GET (curl with the User-Agent "V3R1T4S-research-agent (honest single GET)", no cookies, no retries; GitHub API reads were plain GET requests to api.github.com). Times are UTC from `date -u`; sha256 is of the saved body. The complete log of every request (shared by the eight cells of this batch) is FETCH_LOG.txt next to this file. Pages are not copied here. Looking the format up in the saved pages is code/table_lookup.py (output: table_lookup.txt); the pull-request and arXiv scans are code/novelty_scan.py (output: novelty_scan.txt).

## The bank's p1 sources (fmm_sota.json and the Lille catalogue)

| fetched (UTC) | HTTP | URL | sha256 of body | value for the cell |
|---|---|---|---|---|
| 2026-10-24T22:35:43Z | 200 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (fmm_sota.json) | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | `{"format": [26, 27, 27], "rank": 9233}`; createdAt 2026-10-19T20:46:33; 5456 entries; no entry for the other axis orders (the digest lists sorted formats) |
| 2026-10-24T22:35:44Z | 200 | https://fmm.univ-lille.fr/ (Lille catalogue index, the bank's status_source) | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | row 26x27x27: 9233, construction column: Proj([[27, 0], [0]], ⟨27×27×27:9233⟩ ); Last-Modified Tue, 20 Oct 2026 08:14:45 GMT. No row for the other axis orders |
| 2026-10-24T22:35:57Z | 200 | https://fmm.univ-lille.fr/26x27x27.html (Lille per-format page) | 5ff38edffc609c8688ec9819d333974749d0e2030d8803eeac7d9a8c1564cb06 | The algorithm ⟨26×27×27:10036⟩ is the projection [[1, 0], [0]] of ⟨27×27×27:10234⟩ .; Last-Modified Mon, 02 Jan 2023 12:02:11 GMT |
| 2026-10-24T22:35:59Z | 404 | https://fmm.univ-lille.fr/27x26x27.html | 9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e | Not Found (the catalogue has pages for sorted formats only) |
| 2026-10-24T22:35:59Z | 404 | https://fmm.univ-lille.fr/27x27x26.html | 9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e | Not Found (the catalogue has pages for sorted formats only) |

fmm_digest repository head when checked: commit 42d2933cf0, 2026-10-20T08:11:11Z. The fmm_sota.json and the Lille index fetched here are byte-identical (same sha256) to the copies fetched at 2026-10-24T19:05:59Z for the sibling <18,18,19> claim (2a653515..., 57e936b6...), so these two tables did not change between the two fetches.

The per-format page (10036) is older than the index and the digest (9233); the catalogue front page says its underlying data are being reconstructed. The bar from the bank's two p1 sources is 9233 (the lower of the digest and the index values, both 9233).

## Other comparators (kit/POLICY.md, FMM section, and the bank's other sources)

| fetched (UTC) | HTTP | source | sha256 | finding for <26,27,27> (any order) |
|---|---|---|---|---|
| 2026-10-24T22:35:44Z | 200 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json | 5c600b98b4bb8f9feed5b4d9ffabf11af34b98f49bf43ae250b81e71f43e000b | schemes listed for the format in any order (rank; lineage; fields): 9179 (27x27x27 ∖[13||]; Q,R,C); 9787 (27x27x28^ABC->BCA ∖[13|27|]; Q,R,C); 9913 (27x27x27 ↓[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25|0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26|0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]; Q,R,C); 10036 (naive-26x27x1 +p naive-26x1x26 +m DIS09Lemma4(n=26); Q,R,C); 10107 (2x27x27-r1107-hk71-20b900f +n 2x3x3 ⊗ 2x3x3 ⊗ 3x3x7→⟨7,3,3⟩ ↓[1,2,3,4,5,6|0,1,2|0,1,2]; F3,Q,R,C). external_best_rank 9233 (fmm-lille). The 9179 entry is the plain coordinate projection 27x27x27 ∖[13||] of LITA's 27^3 scheme, the same value as the best plain projection computed in how-we-built-it/slice_accounting_output.txt |
| 2026-10-24T22:35:45Z | 200 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | no row (sections stop at max dimension 16) |
| 2026-10-24T22:35:45Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 77203a718e82fec693578d193c9ccbb2332edcf41f086088a8405cd403666c5a | no row; largest dimension in any format name 16 |
| 2026-10-24T22:35:45Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/additions.md | 408d8f898e841dca75606d5c18937ec036d8a8b86ac1be11310b11d76da4a1f0 | no row; largest dimension in any format name 16 (the file differs from the sibling run's 19:06Z copy: Perminov pushed a commit at 2026-10-24T21:35:33Z) |
| 2026-10-24T22:35:46Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 52db72a9cd408815d98ebcd851d55fb13b8d84eaa70b7ebd7c4de67cc29b9e61 | scope up to 16x16x16; no row |
| 2026-10-24T22:36:00Z | 200 | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 | 8ef0a8a125664f6ddf3f849fbadf5842f27648ad45fcf42d31c3efe2c48f9996 | 6865 paths, not truncated; largest dimension in any path 16; no path for the format; repository head 17c09f4d0f, 2026-10-24T21:35:33Z |
| 2026-10-24T22:36:01Z | 200 | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/HEAD?recursive=1 | e8beb36f9a59f2d400c6a8503273017983ecd8971e27af1ab40788db3279a22b | 39 paths, not truncated; largest dimension 16; no path for the format |
| 2026-10-24T22:36:02Z | 200 | https://api.github.com/repos/khoruzhii/lita/contents/schemes | 5ae1ba358b3bcde175717b3509bbfb2d51a7859f334b30e5a92a3a129338b185 | 20 square schemes 13x13x13 ... 32x32x32 (27x27x27 r9233 is the one this scheme is cut from); no rectangular scheme |
| 2026-10-24T22:36:02Z | 200 | https://api.github.com/repos/khoruzhii/lita/commits?per_page=3 | 0cda42a19c59bdb6d003d15635c6da40c2084484ab0012b1d197dac165817779 | head 472a79fbc8, 2026-10-07T19:22:13Z |
| 2026-10-24T22:35:46Z | 200 | https://raw.githubusercontent.com/khoruzhii/lita/472a79fbc8248423a97bebb3aacbc89e769b9b3e/README.md | 97df246f15643a7396307765d23432d03bcb5af97a9f8bf92cae85cb428d5b3f | README at the pinned commit; states the manuscript is in preparation (read for credit only) |
| 2026-10-24T22:36:03Z | 200 | https://api.github.com/repos/sedoglavic/fmm_digest/commits?per_page=3 | 90efc74092e30c3e76e738bc34902e14feec6f511f77fb26b3ad71f9df394be9 | head 42d2933cf0, 2026-10-20T08:11:11Z |
| 2026-10-24T22:36:03Z | 200 | https://api.github.com/repos/solven-eu/matmulcatalog/commits?per_page=3 | 9b18c46469f4110e4e11f6c17772d1816ae2f50cd3eb4dc51e0a119298ef676b | head de26810759, 2026-10-21T04:14:18Z |

Formats that contain <26,27,27> componentwise (restricting them gives the cell at the same or a lower rank): the lowest in fmm_sota.json are 27x27x27 9233, 26x27x28 9794, 26x28x28 9846, 27x27x28 9846. None is at or below 8828.

## This repository (elder-plinius/V3R1T4S)

| fetched (UTC) | HTTP | query | sha256 | finding |
|---|---|---|---|---|
| 2026-10-24T22:36:11Z to 2026-10-24T22:36:17Z | 200 (7 pages) | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1..7 | see FETCH_LOG.txt | 691 pull requests (#1 to #714; 343 open, 198 closed, 150 merged). Titles and bodies scanned for the format in any axis order and notation and for the numbers 8828, 9179, 9233, 9787, 9913, 10036, 10107: 0 pull requests name the format (any axis order or notation); 1 pull request (#208, a covering-design claim) contains one of these numbers by coincidence and is not about this format (novelty_scan.txt lists it) |
| 2026-10-24T22:36:43Z to 2026-10-24T22:38:05Z | 200 (121 requests) | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/N/files?per_page=100 for the 121 FMM-related pull requests | see FETCH_LOG.txt | 2969 file names (first 100 files of each; PRs #465 and #616 have 100 or more): none names the format or contains these numbers; the largest NxMxP in an FMM PR file name is 19 (#708 and #714) |
| 2026-10-24T22:36:05Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | b1f7db3b79a823a824cd42da5e80f5c671ae03ca303e056686fb78a411fd9a0b | 5439 paths, not truncated; largest dimension in any FMM path 16; nothing for the format |
| 2026-10-24T22:36:06Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | no row for the format |
| 2026-10-24T22:36:06Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 | no row for the format |
| 2026-10-24T22:36:04Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/commits?per_page=3 | a2fca2872220514df41bec5e1bd6af794dae6192d2983dbbefeabc44ecb0e18a | main head 1ebdef41c304 at the time of this fetch; newest pull request #714 |

Sibling cells: PR #708 (<18,19,19> 3424) and PR #714 (<18,18,19> 3225) are the sibling cells of the 19-family, built by the same two slices from LITA's 19x19x19 scheme. Neither names this format.

## Literature

- arXiv API, author search "Khoruzhii" (fetched 2026-10-24T22:41:54Z, HTTP 200, sha256 ec7db8baadf6ba5046351808f2244f324e954d16674421d1b665d9e0aa14d928): 13 entries (2000 to 2026-07-02); none gives a rank for <26,27,27>, none is the LITA manuscript (its README says the manuscript is in preparation).
- arXiv API, the 100 most recent papers with "matrix multiplication" and "rank" in the abstract (fetched 2026-10-24T22:41:54Z, HTTP 200, sha256 86c2ae9936afe014c35cb3c1067210e0ca4f5fe92307cb730fcd420122eb37ef; 2025-03-07 to 2026-10-19): no abstract names the format in any order or one of the ranks above.
- No further literature search (web search, full texts) was run for this cell; a rank for this format in a paper not found by these two queries cannot be excluded.

## Lowest public value for <26,27,27> in any axis order

**9179**: matmulcatalog docs/catalog.json (27x27x27 ∖[13||]). fmm_sota.json and the Lille index list **9233** (construction: Proj([[27, 0], [0]], ⟨27×27×27:9233⟩ )); the Lille per-format page shows 10036. The claimed 8828 is 351 below 9179 and 405 below the table value 9233.
