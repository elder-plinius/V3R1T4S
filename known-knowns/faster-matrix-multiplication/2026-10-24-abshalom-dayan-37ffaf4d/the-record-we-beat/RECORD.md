# The record we compare against: <18,18,19> and its permutations

Rank does not change when the format is permuted, so every source was searched for 18x18x19, 18x19x18 and 19x18x18.
Every fetch was one plain GET (curl with the User-Agent "V3R1T4S-research-agent (honest single GET)", no cookies, no
retries; GitHub API reads were plain GET requests to api.github.com). Times are UTC from `date -u`; sha256 is of the saved body. The
complete log of every request is FETCH_LOG.txt next to this file. Pages are not copied here.

## The bank's p1 sources (fmm_sota.json and the Lille catalogue)

| fetched (UTC) | HTTP | URL | sha256 of body | selected headers | value for the cell |
|---|---|---|---|---|---|
| 2026-10-24T19:05:59Z | 200 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | content-length 343774 | `{"format": [18, 18, 19], "rank": 3355, "exponent": 2.791302}`; createdAt 2026-10-19T20:46:33; 5456 entries; no entry for 18x19x18 or 19x18x18 (the digest lists sorted formats) |
| 2026-10-24T19:05:59Z | 200 | https://fmm.univ-lille.fr/ (catalogue index; the bank's status_source) | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | Last-Modified Tue, 20 Oct 2026 08:14:45 GMT | row 18x18x19: ⟨18×18×19:3355⟩, construction (description column) ⟨18×18×1:324⟩ + ⟨18×18×18:3031⟩ (a block sum; 3031 is LITA's 18x18x18 scheme). No row for 18x19x18 or 19x18x18 |
| 2026-10-24T19:05:59Z | 200 | https://fmm.univ-lille.fr/18x18x19.html (per-format page) | 0bae85379d91e8a22a54e37fc984a936bc6885947f00ccd481ee5e97e42beab3 | Last-Modified Fri, 19 Jun 2026 19:35:35 GMT | "Description of fast matrix multiplication algorithm: ⟨18×18×19:3524⟩", "the (Kronecker) tensor product of ⟨18×9×19:1762⟩ with ⟨1×2×1:2⟩" |
| 2026-10-24T19:06:00Z | 404 | https://fmm.univ-lille.fr/18x19x18.html | 9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e | - | Not Found (the catalogue has pages for sorted formats only) |
| 2026-10-24T19:06:00Z | 404 | https://fmm.univ-lille.fr/19x18x18.html | 9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e | - | Not Found |

fmm_digest repository head when checked: commit 42d2933cf0, 2026-10-20T08:11:11Z ("add Witteveen's new results").

The per-format page (3524, June) is older than the index and the digest (3355, October); the catalogue front page
says its underlying data are being reconstructed. The bar from these sources is 3355.

Re-fetched once more at 2026-10-24T19:24:24Z (fmm_sota.json) and 19:24:25Z (index, 18x18x19.html): HTTP 200,
sha256 unchanged (2a653515..., 57e936b6..., 0bae8537...). Newest pull request at 19:24:25Z: #708; none newer.

## Other comparators (kit/POLICY.md, FMM section, and the bank's other sources)

| fetched (UTC) | HTTP | source | sha256 | finding for <18,18,19> (any order) |
|---|---|---|---|---|
| 2026-10-24T19:06:00Z | 200 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json (Chatain Lacelle, arXiv 2606.13408) | 5c600b98b4bb8f9feed5b4d9ffabf11af34b98f49bf43ae250b81e71f43e000b | three schemes: rank 3355 (Q,R,C; lineage "naive-18x18x1 +p 18x18x18"), 3356 (same lineage), 3524 (F3,Q,R,C; Kronecker lineage); external_best_rank 3355 (fmm-lille). Repository head de26810759, 2026-10-21T04:14:18Z |
| 2026-10-24T19:06:00Z | 200 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | no row (sections stop at max dimension 16) |
| 2026-10-24T19:06:01Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 77203a718e82fec693578d193c9ccbb2332edcf41f086088a8405cd403666c5a | no row; largest dimension in any format name: 16 |
| 2026-10-24T19:06:01Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/additions.md | 258cfa9846615ac5e75f665969b2aad3ca496a11fcb9d9561e368474a309ca88 | no row; largest dimension in any format name: 8 |
| 2026-10-24T19:06:01Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 52db72a9cd408815d98ebcd851d55fb13b8d84eaa70b7ebd7c4de67cc29b9e61 | scope up to 16x16x16; no row |
| 2026-10-24T19:06:02Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | e451692724898898bbc051649324b015be4d7842d403f9c54909f4513f32d489 | no mention |
| 2026-10-24T19:06:02Z | 200 | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 (whole repository, including schemes/results/ and schemes/known/) | 408ac494c266f4a35503469729a264ff85643d988e1ef543701410622407a3f7 | 6863 paths, not truncated; largest dimension in any path 16; no file for the cell |
| 2026-10-24T19:06:04Z | 200 | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/HEAD?recursive=1 | e6866337cf18c6f4bb9d2b950240341d901260e28b560a301853202c03b1a5fc | 39 paths, not truncated; largest dimension 16; no file for the cell |
| 2026-10-24T19:14:08Z | 200 | https://api.github.com/repos/jakobmoosbauer/flips/git/trees/HEAD?recursive=1 | c776d2055bd45a7033f70e6c79f4959a51cf375a86e800a70b2fc32506385155 | small formats only (largest named format 666); nothing for the cell |
| 2026-10-24T19:03:59Z | 200 | https://api.github.com/repos/khoruzhii/lita/contents/schemes | 8d289a9bcacbc9f7bfb4c824b2647bdedb8e1eedb1200bb7a22bf7594e4e6cd9 | 20 square schemes 13x13x13 ... 32x32x32 (18x18x18 r3031, 19x19x19 r3633); no rectangular scheme |

Formats that contain <18,18,19> componentwise (restricting them gives the cell at the same or lower rank): the lowest
in fmm_sota.json are (18,18,19) 3355, (18,18,20) 3526, (18,19,19) 3633, (19,19,19) 3633; in matmulcatalog (18,18,19)
3355, 3356, 3524, then (18,18,20) 3526, (18,19,19) 3595. None is at or below 3225.

## This repository (elder-plinius/V3R1T4S)

| fetched (UTC) | HTTP | query | sha256 | finding |
|---|---|---|---|---|
| 2026-10-24T19:07:17Z to 19:07:36Z | 200 (7 pages) | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1..7 | see FETCH_LOG.txt | 685 pull requests (#1 to #708; 337 open, 348 closed, 150 merged). Titles and bodies scanned for 18x18x19 / 18x19x18 / 19x18x18 in x, ×, comma, space and bracket notations, and for the number 3225: one hit, #708 (open, created 2026-10-24T18:58:23Z, the sibling <18,19,19> 3424 claim by the same contributor), whose "Not claimed" list says "The run also built <18,18,19> at 3225 (fmm_sota.json 3355); it is not part of this package", and its how-we-built-it/ holds the code that rebuilds this scheme (see "Prior publication" below). No pull request contains the <18,18,19> scheme files |
| 2026-10-24T19:10:06Z to 19:12:05Z | 200 (118 requests) | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/{number}/files for each of the 118 FMM-related pull requests | see FETCH_LOG.txt | 3199 file names; none names 18x18x19 in any order or contains 3225; the largest NxMxP in a file name is 18x19x19 (#708) |
| 2026-10-24T19:06:49Z to 19:07:07Z | 200 | GitHub search, `repo:elder-plinius/V3R1T4S is:pr` with 18x18x19, 18x19x18, 19x18x18, 3225, "18,18,19", 18×18×19 | see FETCH_LOG.txt | 0, 0, 0, 1 (#708), 1 (#708) and 50 loose matches for "18×18×19" (GitHub tokenises it into separate numbers; the FMM ones are #45, #46, #50, #51, #399, #615 and #708, and the full-listing scan above shows that only #708 names the cell) |
| 2026-10-24T19:09:54Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/commits?per_page=3 | a2fca2872220514df41bec5e1bd6af794dae6192d2983dbbefeabc44ecb0e18a | main head 1ebdef41c304, 2026-10-24T16:13:09Z |
| 2026-10-24T19:09:55Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | b1f7db3b79a823a824cd42da5e80f5c671ae03ca303e056686fb78a411fd9a0b | 5439 paths, not truncated; largest dimension in any FMM path 16; nothing for the cell |
| 2026-10-24T19:09:55Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/known-knowns/faster-matrix-multiplication/INDEX.csv | 8e5b2a6c3c2b6a18dd3c2489f742b73890b9c81bb9d051f0628bab25101e83b7 | no row for the cell |
| 2026-10-24T19:09:56Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 | no row for the cell |

## Literature

- arXiv API, author search "Khoruzhii" (fetched 2026-10-24T19:13:38Z, HTTP 200, sha256
  00a4daf510e8e4cc5580b8d896d4d5d65d27d404ff59bded64eb8e7507b29fed): 13 entries; none is the LITA manuscript (its
  README says the manuscript is in preparation) and none gives a rank for <18,18,19>.
- arXiv API, the 100 most recent papers with "matrix multiplication" and "rank" in the abstract (fetched
  2026-10-24T19:13:41Z, HTTP 200, sha256 b84312a70075b32f4ede2c530eb7eb955a03f28b3e5ec9e3600477526c88393c; 2025-03 to
  2026-10-19): no abstract names <18,18,19> in any order or 3225. The newest relevant one, arXiv 2610.26563v2
  (tensor contraction aggregation; abs and HTML fetched 2026-10-24T19:13:55Z and 19:13:57Z, HTTP 200), has no
  18/18/19 format, no 3225 and no 3355 in its full text.
- Web searches (run between 19:12:05Z and 19:13:22Z): "18x18x19" matrix multiplication rank; LITA local
  improvements trilinear aggregation Khoruzhii Serafin Gelß Pokutta arXiv rectangular matrix multiplication schemes;
  fast matrix multiplication new rank upper bounds formats up to 32 2026 restriction slice square scheme rectangular
  18 19. No result gives a rank for <18,18,19> in any order.

## Lowest public value for <18,18,19> in any axis order

**3355**: fmm_sota.json (sedoglavic/fmm_digest, regenerated 2026-10-19) and the Lille catalogue index (block sum
⟨18×18×1:324⟩ + ⟨18×18×18:3031⟩), also matmulcatalog docs/catalog.json. The per-format Lille page shows 3524. The
claimed 3225 is 130 below 3355 and 299 below 3524.

## Re-fetched by the panel (unchanged)

| fetched (UTC) | by | URL | HTTP | sha256 of body | value for the cell |
|---|---|---|---|---|---|
| 2026-10-24T19:28:13Z to 19:28:14Z | novelty panelist (panel/novelty.md) | https://fmm.univ-lille.fr/, https://fmm.univ-lille.fr/18x18x19.html, fmm_sota.json | 200 | unchanged (57e936b6..., 0bae8537..., 2a653515...) | 3355 (index and digest), 3524 (per-format page) |
| 2026-10-24T19:34:28Z | criterion panelist (panel/criterion.md) | https://fmm.univ-lille.fr/ | 200 | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 (unchanged) | ⟨18×18×19:3355⟩, construction ⟨18×18×1:324⟩ + ⟨18×18×18:3031⟩ |
| 2026-10-24T19:34:29Z | criterion panelist (panel/criterion.md) | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 200 | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae (unchanged) | [18, 18, 19] -> 3355 |

The novelty panelist also re-read every pull request of this repository (685, #1 to #708) at 19:29:01Z to 19:29:08Z
and PR #708 itself at 19:29:16Z to 19:29:18Z: no other filing names the cell or 3225.

## Prior publication by the same contributor (PR #708)

PR #708 (https://github.com/elder-plinius/V3R1T4S/pull/708, opened 2026-10-24T18:58:23Z by the same contributor for
the sibling cell <18,19,19> rank 3424; one commit e4bb688f43, 2026-10-24T18:31:54Z) already made two things public
for this cell:
- the value 3225 for <18,18,19>, in its "Not claimed" list;
- in its how-we-built-it/, the identical deterministic code (code/rebuild_lita_slices.py, engine.py, convert.py and
  export_txt.py, text-identical to how-we-built-it/code/ here), whose COMMANDS.md states that the second slice gives
  <18,18,19> 3225 from LITA's 19x19x19 scheme. Running it on LITA's public data rebuilds this exact scheme.

#708 does not contain the <18,18,19> scheme files; those are first filed in this package.

Dated note for the record: value and generator first made public by the contributor in #708 on 2026-10-24.
