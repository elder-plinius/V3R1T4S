# Table record (the scout's record and the claim-time re-fetch)

Every fetch was one plain GET with the User-Agent "V3R1T4S-research-agent (honest single GET)", no cookies, no
retries. Times are UTC from `date -u`; sha256 of the saved body. (fetch_log.txt also has three rows with HTTP 000
at 07:03:29Z-07:03:31Z: a shell quoting slip joined URL and file name into one argument, curl rejected it locally
before connecting, and no request was sent; each URL was then sent once, correctly, at 07:03:39Z-07:03:42Z.)

| fetched (UTC) | HTTP | URL | sha256 of body | value for sorted <14,14,15> |
|---|---|---|---|---|
| 2026-10-25T03:46:47Z | 200 | https://fmm.univ-lille.fr/ (catalogue index; the bank's status_source) | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | row "<14x14x15:1789>" |
| 2026-10-25T05:57:36Z | 200 | https://fmm.univ-lille.fr/ (re-fetch; Last-Modified: Tue, 20 Oct 2026 08:14:45 GMT) | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 (unchanged) | row "<14x14x15:1789>" |
| 2026-10-25T07:03:39Z | 200 | https://fmm.univ-lille.fr/14x14x15.html (per-format page, fetched immediately before claiming; Last-Modified: Wed, 10 Jun 2026 10:22:10 GMT) | 63ce18bf1085d0f315839876c397d7ff9bfe725fa5fd998883f382a14e6b907a | "Description of fast matrix multiplication algorithm: <14x14x15:1798>" |
| 2026-10-25T07:05:01Z | 200 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (fetched immediately before claiming) | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae (same as 03:46:45Z and 05:57:34Z) | {"format": [14, 14, 15], "rank": 1789, "exponent": 2.813395}; createdAt 2026-10-19T20:46:33 |
| 2026-10-25T07:05:02Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md (fetched immediately before claiming) | 77203a718e82fec693578d193c9ccbb2332edcf41f086088a8405cd403666c5a (same as 03:46:45Z and 05:57:34Z) | row "`14x14x15` | 1798 (?) | 1798 (1813) | 1790 (1813) | 2.813604914" under the header "Format / `ZT` rank / `Z` rank / `Q` rank": ZT 1798, Z 1798, Q 1790; minimum 1790 |
| 2026-10-25T07:05:03Z | 200 | https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/SHA256SUMS (fetched immediately before claiming) | de848328881cf69cbe2a8d8309e04d94826cf1431b5b39e81db63f95af58a3fd (same as 03:46:46Z and 05:57:35Z) | 32 lines; no 14x14x15 (or 14x15x14, 15x14x14) file |
| 2026-10-25T07:03:41Z | 200 | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 (full repository tree, not truncated) | e6866337cf18c6f4bb9d2b950240341d901260e28b560a301853202c03b1a5fc | 39 paths; none for 14x14x15 or a permutation of it |

The minimum over the four sources the criterion names is 1789 (fmm_sota.json); the claimed rank 1709 is 80 below it.

Values already public in this repository (the claim is below every one):
- known-knowns/faster-matrix-multiplication (merged; README and INDEX.csv in the pinned repository copy, commit
  1ebdef41c30414cd2a036b00f5e81d0fc4c1dc25): <14,14,15> rank **1716** over Q, scheme `schemes/14x14x15_r1716_Q.json`.
  TROPHY_CASE.md (https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, fetched
  2026-10-25T05:57:36Z, HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1), entry
  47: "<14,14,15> rank 1716 over Q". 1709 is 7 below it.
- Pull requests. GitHub search over all pull requests for this target, open and closed
  (https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+is:pr+fmm-catalogue-small-format-rank&per_page=100,
  fetched 2026-10-25T05:57:35Z, HTTP 200, sha256 61185fc16ae90961d7ff86074bf85ac30e9d9f0b0041a5bea83d1524d10e0ca7,
  34 pull requests): one for this cell, #6 "[claim] fmm-catalogue-small-format-rank: format (14, 14, 15) rank 1715
  over Q (beats 1789 bar)", closed 2026-10-14T12:52:42Z, not merged. A second search for the format string in any
  pull request (https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+is:pr+14x14x15&per_page=100,
  fetched 2026-10-25T07:03:42Z, HTTP 200, sha256
  0d5a7f526bf81fb4c38836f7f630c5a39785d3dffc17896b5c22ae6046cf5520, 1 result) finds the same #6 only. 1709 is 6 below
  1715.

Other sources checked for the same cell:
- matmulcatalog docs/catalog.json (https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json,
  fetched 2026-10-25T05:57:36Z, HTTP 200, sha256
  5c600b98b4bb8f9feed5b4d9ffabf11af34b98f49bf43ae250b81e71f43e000b): eight <14,14,15> entries, ranks 1789 (derived,
  "naive-14x14x1 +p 14x14x14"), 1790 (Perminov 2023, Q), 1798, 1798, 1799, 1799, 1812 and 1813; every entry gives
  external_best_rank 1789 from fmm-lille. Lowest 1789.
- LITA repository tree (https://api.github.com/repos/khoruzhii/lita/git/trees/HEAD?recursive=1, fetched
  2026-10-25T05:58:12Z, HTTP 200, sha256 75d497884cdff3414cc1b996c21083229d2984437f308186a686048ba4f7ee57): schemes/
  holds only cubes N x N x N for N = 13..32 (including schemes/15x15x15_r1977.npz, git blob sha1
  65821484d954b4aade06cbda624932ba2a481f7b, the parent used here); no <14,14,15> scheme.
- The LITA parent file itself: https://raw.githubusercontent.com/khoruzhii/lita/HEAD/schemes/15x15x15_r1977.npz,
  fetched 2026-10-24T16:05:03Z (HTTP 200) by an earlier run of the same contributor, sha256
  94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33; its git blob sha1 matches the tree listing above.
