# The record compared against (snapshot, not the pages)

All fetches by the run and by the three skeptics: one plain GET each, User-Agent naming V3R1T4S (the run:
"V3R1T4S-research-agent (honest single GET)"), no cookies, no retries, no blocked request. Times are UTC from `date -u`.
No page body is copied here. Next to this file: `TABLE_RECORD.md` (the run's own table record, unchanged except that a run id was removed),
`fetch_log.txt` (the run's fetch log: time, HTTP status, URL, saved name, sha256, size) and `headers/` (the response
headers of the run's fetches, one file per URL). Lines for Authorization, X-OAuth-*, tokens and rate limits were
removed from them. The strict-transport-security line of the four github.com API responses was removed too, because
one of its directive names contains a letter sequence that the kit's never-publish scan flags by accident (a false
positive). The run's requests were unauthenticated plain GETs and carried no such header. Two kinds of fetch time are
given for each source: the claim-time fetch by the run (2026-10-25T07:03Z to 07:05Z) and the panel's live re-fetches
(2026-10-25T10:09Z to 10:14Z, from `panel/novelty.md` and `panel/criterion.md`); the sha256 of each body is the same
in both, except for the dynamic github.com repository page named below.

## The four sources the criterion names

### fmm_sota.json (Sedoglavic's digest of the Lille catalogue)
- URL: https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json
- fetched (UTC): 2026-10-25T07:05:01Z by the run; 2026-10-25T10:09:20Z by the NOVELTY skeptic (same sha256)
- HTTP status: 200; selected headers (run's fetch): date: Sun, 25 Oct 2026 07:05:01 GMT; content-type: text/plain; charset=utf-8
- sha256 of the body: 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae
- extracted cell: {"format": [14, 14, 15], "rank": 1789, "exponent": 2.813395}; file createdAt 2026-10-19T20:46:33;
  the only entry whose sorted format is (14,14,15)

### Lille per-format page
- URL: https://fmm.univ-lille.fr/14x14x15.html
- fetched (UTC): 2026-10-25T07:03:39Z by the run; 2026-10-25T10:09:20Z by the NOVELTY skeptic and 10:13:20Z by the
  CRITERION skeptic (same sha256)
- HTTP status: 200; selected headers (run's fetch): Server: Apache; Content-Type: text/html; Last-Modified: Wed, 10 Jun 2026 10:22:10 GMT
- sha256 of the body: 63ce18bf1085d0f315839876c397d7ff9bfe725fa5fd998883f382a14e6b907a
- extracted cell: "Description of fast matrix multiplication algorithm: <14x14x15:1798>" (the algorithm is taken from
  Perminov's repository, February 2026, per the page)

### Perminov docs/ranks.md (the table that replaced the README table on 2026-10-23)
- URL: https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md
- fetched (UTC): 2026-10-25T07:05:02Z by the run; 2026-10-25T10:09:21Z by the NOVELTY skeptic and 10:13:20Z by the
  CRITERION skeptic (same sha256)
- HTTP status: 200; selected headers (run's fetch): date: Sun, 25 Oct 2026 07:05:02 GMT; content-type: text/plain; charset=utf-8
- sha256 of the body: 77203a718e82fec693578d193c9ccbb2332edcf41f086088a8405cd403666c5a
- extracted cell: row `14x14x15` under the header Format / ZT rank / Z rank / Q rank: ZT 1798, Z 1798, Q 1790
  (the bracketed 1813 values are earlier ranks); minimum 1790

### MerlijnW70/fmm-schemes
- URLs: https://github.com/MerlijnW70/fmm-schemes (repository page),
  https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 (full tree, not truncated),
  https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/SHA256SUMS
- fetched (UTC): tree 2026-10-25T07:03:41Z and SHA256SUMS 2026-10-25T07:05:03Z by the run; tree 2026-10-25T10:09:21Z
  (NOVELTY) and 10:13:50Z (CRITERION), repository page 10:13:20Z (CRITERION), README (raw) 10:09:22Z (NOVELTY)
- HTTP status: 200 for all
- sha256 of the bodies: tree e6866337cf18c6f4bb9d2b950240341d901260e28b560a301853202c03b1a5fc (same in all three
  fetches); SHA256SUMS de848328881cf69cbe2a8d8309e04d94826cf1431b5b39e81db63f95af58a3fd; README
  6ef17ff86e9a74b710e4e6173f67187b735ecdef760d2634a16d33bdf73b904b; repository page (dynamic HTML, bytes differ per
  fetch) 703ab8974c6d8b4b5e505df8bbb489c4a865bb025871da26f18a49818c281af8
- extracted cell: none. 39 tree paths (31 scheme files) and 32 SHA256SUMS lines; no file for 14x14x15, 14x15x14 or
  15x14x14. The criterion clause has nothing to beat for this source, so the bar is the minimum over the three
  sources that list the format: 1789.

The minimum over the four sources is 1789 (fmm_sota.json); the claimed rank 1709 is 80 below it.

### Re-fetch immediately before filing (criterion text)
- fmm_sota.json: 2026-10-25T11:18:27Z, HTTP 200, sha256 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae (unchanged): 1789
- https://fmm.univ-lille.fr/14x14x15.html: 2026-10-25T11:18:27Z, HTTP 200, sha256 63ce18bf1085d0f315839876c397d7ff9bfe725fa5fd998883f382a14e6b907a (unchanged): 1798
- Perminov docs/ranks.md: 2026-10-25T11:18:27Z, HTTP 200, sha256 77203a718e82fec693578d193c9ccbb2332edcf41f086088a8405cd403666c5a (unchanged): minimum 1790
- MerlijnW70/fmm-schemes tree: 2026-10-25T11:18:37Z, HTTP 200: 39 paths, none for 14x14x15 in any orientation
- Pull requests of this repository up to #751: none names this format.

## Other sources checked for the same cell
- Lille catalogue index (the bank's status_source): https://fmm.univ-lille.fr/ , fetched 2026-10-25T03:46:47Z,
  05:57:36Z (both by the run) and 10:09:20Z (NOVELTY), HTTP 200, sha256
  57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 (unchanged); Last-Modified: Tue, 20 Oct 2026
  08:14:45 GMT. Row <14x14x15:1789>, construction column "<14x14x1:196> + <14x14x14:1593>" (a plain composition).
- matmulcatalog docs/catalog.json, https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json ,
  fetched 2026-10-25T05:57:36Z (run) and 10:09:22Z (NOVELTY), HTTP 200, sha256
  5c600b98b4bb8f9feed5b4d9ffabf11af34b98f49bf43ae250b81e71f43e000b: eight <14,14,15> entries, ranks 1789 (derived,
  "naive-14x14x1 +p 14x14x14"), 1790 (Perminov 2023, Q), 1798, 1798, 1799, 1799, 1812, 1813; lowest 1789.
- LITA repository tree, https://api.github.com/repos/khoruzhii/lita/git/trees/HEAD?recursive=1 , fetched
  2026-10-25T05:58:12Z (run) and 10:10:54Z (NOVELTY), HTTP 200, sha256
  75d497884cdff3414cc1b996c21083229d2984437f308186a686048ba4f7ee57 (same in both fetches):
  schemes/ holds only cubes N x N x N for N = 13..32; no <14,14,15>.

## Values already public in the V3R1T4S repository (the claim is below both)
- Merged: known-knowns/faster-matrix-multiplication, <14,14,15> rank **1716** over Q (scheme file
  schemes/14x14x15_r1716_Q.json), TROPHY_CASE.md entry 47:
  https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md , fetched 2026-10-25T05:57:36Z (run),
  10:09:23Z (NOVELTY) and 10:14:17Z (CRITERION), HTTP 200, sha256
  b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 (same in all three). 1709 is 7 below it.
- Closed, not merged: pull request #6, https://github.com/elder-plinius/V3R1T4S/pull/6 , "[claim]
  fmm-catalogue-small-format-rank: format (14, 14, 15) rank 1715 over Q (beats 1789 bar)", opened 2026-10-14T02:53:11Z
  by calgulbenkian, closed 2026-10-14T12:52:42Z. Found by the search
  https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+is:pr+14x14x15&per_page=100, fetched 2026-10-25T07:03:42Z
  (run), 10:10:55Z (NOVELTY) and 10:13:51Z (CRITERION), HTTP 200, sha256
  0d5a7f526bf81fb4c38836f7f630c5a39785d3dffc17896b5c22ae6046cf5520 (same in all three): one result, #6. 1709 is 6 below it.
- All 710 to 711 pull requests (state=all, 8 pages) were scanned by both NOVELTY (10:10:17Z to 10:10:24Z) and CRITERION
  (10:13:50Z to 10:14:08Z) for every spelling and orientation of the format: only #6 (1715) and #399 (a bank refresh
  that quotes the catalogue change 1790 -> 1789 and holds no scheme). Nothing at or below 1709.
