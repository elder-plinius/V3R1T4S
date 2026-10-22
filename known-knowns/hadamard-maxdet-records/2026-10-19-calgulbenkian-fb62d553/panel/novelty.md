context: Claude Code subagent, fresh context [Sonnet 5.5]

# novelty report: maxdet-117

Claim: a 117 x 117 matrix with entries +1 or -1 and normalised determinant |det| / 2^116 = 325 x 29^57 = 73887205478246242985652874268409752933911041846892660492861670872395821475850942725425. Target hadamard-maxdet-records, full success criterion (strictly greater than the archived MaxDet value, the Caltech/arXiv value, EinsteinArena and any newer value).

Read from the package folder: the claim record (not shipped), INDEX.csv, the-record-we-beat/README.md.

## Common sources (fetched once; the raw files and the full fetch log are not shipped in this package)

- Fetch method: plain curl with the honest client string, one request per URL, no retries. Times are UTC. Where a fetch needed a deviation it is stated under unresolved.
- TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, 2026-10-19T05:27:03Z, HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1. It lists six result families (degree-diameter graphs, constant-weight codes, matrix multiplication, the Lehmer bound, VNN-COMP counterexamples, a RobustBench attack) plus two cipher commitments. No row for maximal determinants.
- known-knowns listing: https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns, 2026-10-19T05:27:03Z, HTTP 200, sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011. Twenty directories. The only one on this target is hadamard-maxdet-records.
- Pull requests: I used a snapshot of all V3R1T4S pull requests (titles and bodies, 473 entries, fetch time 2026-10-19T04:30:31Z) instead of the api.github.com pulls pages, and did not fetch the API pulls pages. I read every title and searched every body for the target ids and keywords (hadamard-maxdet).
- The contributor's review ruling R1: closed pull requests from the 2026-10-14 bulk close by the same contributor (#65-#120) are the author's own earlier filings, not competing values. They are reported, not counted against a cell.

## Primary sources (maximal determinants)

- Orrick MaxDet archive, order tables. The archive-it URL named in the triage record (https://wayback.archive-it.org/219/20190316001107/http://www.indiana.edu/~maxdet/page3.shtml) answered HTTP 302 with an empty body at 2026-10-19T05:26:59Z, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty). I did not retry that URL. I then made one request to the equivalent web.archive.org address of the same capture and followed its single redirect: page3 at 2026-10-19T05:27:20Z, HTTP 200 (final URL https://web.archive.org/web/20190315055615/http://www.indiana.edu/~maxdet/page3.shtml), sha256 2d3a908284c4f3b483e84fca7fa0b6bca28f9e47e90a0f18411ad11d05bde76d; page2 at 2026-10-19T05:36:45Z, HTTP 200 (final URL https://web.archive.org/web/20190316151116/http://www.indiana.edu/~maxdet/page2.shtml), sha256 339f6269ef4225b4f7980ba970bab5d2dedcb0e8a56c8af8b40ba3ba6d2bc9ae. The archived page is dated March 2019. Row read: Order 117: 7.231499425E85 ??, .72.
- Rokicki's newrec page: the archive-it address (https://wayback.archive-it.org/219/20190315055615/http://tomas.rokicki.com/newrec.html, 2026-10-19T05:27:01Z) returned HTTP 404 (sha256 765bec8caffbacb0eae95ec76a0c4c19ad702f842253a827f47772ad7a928097). One request to the web.archive.org copy (2026-10-19T05:27:21Z, redirected once to the capture of 2021-01-26, https://web.archive.org/web/20210126204345/https://tomas.rokicki.com/newrec.html) returned HTTP 200, sha256 10cc7afb6221b9ad7f93d5e075f5d403606ee947aad0917acd04cf7d766f0877. The page says "N is for the size of a 0/1 matrix", so N = order minus 1, and its third column is the 0/1 determinant, which equals the normalised determinant of the +-1 matrix of order N+1. It lists N=116 (order 117) 7.2315e85; this equals the Orrick archive value (to the digits shown); Rokicki's table is the origin of the Orrick entry for this order.
- Math-AI-Caltech hadamard-maxdet: README https://raw.githubusercontent.com/Math-AI-Caltech/hadamard-maxdet/main/README.md, 2026-10-19T05:26:58Z, HTTP 200, sha256 a445d9670ccb33c604865f9e19d5dc4b1487fee1c616e5ab6223a5feaaea4abd: title "Record Maximal-Determinant +-1 Matrices (dimensions 51, 103, 107, 111, 115, 119)"; "Each row describes a matrix of order n = 3 mod 4". Order 117 is 1 mod 4, so it cannot be in that file. Its pulls page (https://github.com/Math-AI-Caltech/hadamard-maxdet/pulls, 2026-10-19T05:26:58Z, HTTP 200, sha256 faffb4bd868874a17ad835d7cf0840016d4b6c0cccf0f33d2aae6c1911454577) shows openCount 0 and closedCount 0 in the page data, so there are no pending submissions there.
- arXiv:2608.22518 v3 "New Records for the Hadamard Maximal Determinant Problem" (https://arxiv.org/html/2608.22518, 2026-10-19T05:32:55Z, HTTP 200, sha256 ed31ecc98caead7d86d22447a70f8219e9c99048569ca1cc07c935ad4fee0bb6): the text does not contain the order 117 (searched as a whole number); its new records are order 51 and orders 103 to 119 congruent to 3 mod 4. arXiv API query 3 of 4 (maximal determinant, newest first, 2026-10-19T05:32:38Z, HTTP 200, sha256 f4ab225c450b018b72440833240b65c58ef478f0d4a2735c38224ee14938dd35): the only 2026 determinant paper is 2608.22518; the others are older surveys and unrelated papers. EinsteinArena home page (2026-10-19T05:40:57Z, sha256 f5c8fff10812b9c529aec39e0f9922c564c7bb3a1cbfb872ec5ef72a87258094): only "Hadamard Maximal Determinant (order 51)".
- Merged work: known-knowns/hadamard-maxdet-records holds one package, 2026-10-15-anonymous-c6d1e0ab-0108345c (directory listing fetched 2026-10-19T05:27:58Z, HTTP 200, sha256 67fe98eab3bbc112148d6b9d9cf3283e2072f2f2d65be83e689a795f6c589c8b), which is merged pull request #155 (for a different order; the contributor's own, merged 2026-10-15). Closed pull request by the same contributor (R1, not competing): #67 (order 117, 324 x 29^57). No other contributor has a pull request on this target.

## This cell

Value compared: 325 x 29^57 = 73887205478246242985652874268409752933911041846892660492861670872395821475850942725425.
Record values found: Orrick archive 7.231499425E85; Rokicki N=116 entry 7.2315e85 (same).
Ratio: 1.0217 times the Orrick/Rokicki value. The contributor's closed #67 filed 324 x 29^57; this value is larger by a factor 1.00309 (R1: own earlier filing).
Merged work: no merged package for order 117.

Propagation test (PR #350 rule). The standard rule I tested is bordering a Hadamard matrix of order n-1 (order 116 here, normalised determinant 58 x 29^57). Bordering gives at most (D116 / 2)(1 + sqrt(116)) = about 341.3 x 29^57, and the claimed value 325 x 29^57 is below that ceiling, so I tested whether the object actually is a bordered Hadamard matrix. It is not. For a Hadamard core of order 116 the 116 core rows would have pairwise inner products +-1 in the full matrix, i.e. one row whose deletion leaves no pair with another inner product; in the object 252 row pairs have another inner product and no single row covers them all, so there is no Hadamard core of order 116 and the object is not a single-row bordered Hadamard matrix. The value is a search result.


## Open questions for the panel, as far as they concern novelty

1. Does Rokicki's newrec page or any newer source list a larger determinant for order 117? Rokicki's page (capture 2021-01-26) lists the same value as Orrick for this order (see above) and nothing larger; the Caltech repository and the 2026 paper have no row for it; no newer arXiv value was found (queries above).
2. Is there any newer record for order 117 than the 2019 Orrick copy? None found in the Caltech repository (n = 3 mod 4 only), arXiv:2608.22518, EinsteinArena (order 51 only), the repository pull requests (none open) or my arXiv query. The Orrick page marks the order as not proved (??), ratio below the Barba bound. 

unresolved: the live Orrick site no longer exists; the archive copy is dated March 2019, so values published after 2019 outside the Caltech repository, arXiv and this repository could not be seen (Google Scholar not searched). The archive-it addresses did not serve (302 empty, 404); I used web.archive.org captures of the same pages, following one redirect each, which is a small deviation from one plain request per URL. EinsteinArena detail pages were not fetched beyond its home page. Whether the matrix is valid and its determinant exact is for the reproduce role (I only used the matrix for the bordered-Hadamard test).

novelty verdict: the determinant strictly exceeds every value I could find (Orrick, Rokicki, Caltech, arXiv, the repository's merged package and open or closed pull requests) and is not a bordered Hadamard matrix.

pass: true
