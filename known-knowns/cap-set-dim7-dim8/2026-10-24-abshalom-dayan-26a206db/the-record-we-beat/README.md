# The record we compared against

Every fetch: one plain request with a User-Agent naming V3R1T4S, no retries. The pages themselves are not included.
Response headers were not recorded at fetch time (only the HTTP status, size and sha256).

## Edel's cap table (primary table for p1)
- URL: http://www.yvesedel.de/Matritzen/CAPs/CAPMatIndex.html ("The website formerly known as
  www.mathi.uni-heidelberg.de/~yves/"; linked from OEIS A090245; "Last changed: April 28, 2010")
- Fetched 2026-10-24T20:07:59Z (NOVELTY skeptic) and 2026-10-24T20:28:35Z (CRITERION skeptic), HTTP 200 both times,
  15275 bytes, sha256 8aa5a2837a51d261c7b030e500c2c99e396d9ce7a653ecce8bc9badf6c1e2817 both times.
- Extracted cell: lower bounds on caps in PG(k,q), row k = 8, column q = 3: "534 --> 541"; "A 541 Cap in PG(8,3)".
- Doubling: Bierbrauer and Edel, "Large caps in projective Galois spaces" (2012),
  http://www.yvesedel.de/Papers/CapSurvey.pdf, fetched 2026-10-24T20:08:31Z, HTTP 200, 244851 bytes, sha256
  66ebda0dda4c6e3f7c37bceece4baab8df233be6db82ac6283f628ad493380da: "Theorem 1. An n-cap in PG(d, q) allows the
  construction of a 2n-cap in AG(d + 1, q)"; Table 1, d = 8, q = 3: 541. So AG(9,3) >= 1082 from the table.
- The old Heidelberg addresses (www.mathi.uni-heidelberg.de/~yves/...) answered HTTP 404 on 2026-10-24.

## FunSearch notebook
- URL: https://raw.githubusercontent.com/google-deepmind/funsearch/main/cap_set/cap_set.ipynb
- Fetched 2026-10-24T16:41:19Z and 2026-10-24T20:18:29Z, HTTP 200, 17080 bytes, sha256
  f97f6f6ec331e5809ca4d40205224d2c5c613687d4f65316ecc2dd04a1724203 both times.
- Extracted: "recall that largest known cap set for `n = 9` has size `1082`" and "Discovered function that builds a
  $1082$-cap in $n = 9$ dimensions ... This matches the previously known best construction".

## X-evolve (the bank's status_source)
- URL: https://arxiv.org/html/2508.07932, fetched 2026-10-24T17:41:45Z, 19:56:17Z and 20:04:23Z, HTTP 200, 760823 bytes,
  sha256 526607c13d086051e05b70ac698ed24409917f75bf05e7b5a217f77e7165721c each time.
- Extracted: Table 2 covers n = 3..8 ("Best known 9 20 45 112 236 496 / FunSearch 9 20 45 112 236 512 / X-evolve 9 20
  45 112 236 512"); no n = 9 value.

## OEIS A090245
- URL: https://oeis.org/A090245, fetched 2026-10-24T20:07:27Z, HTTP 200, sha256
  0cf521b9c40ae1e3459da3fc977f4c5d3353acc1c392bc7d9b25e14dc351f8b2. Terms 1, 2, 4, 9, 20, 45, 112 (exact maxima to n = 6).

## Strongest public claim found (not refereed, not in p1's source list)
- https://github.com/Noirsys/capset README via https://api.github.com/repos/Noirsys/capset/readme, fetched
  2026-10-24T20:17:02Z and 20:26:56Z, HTTP 200, 5719 bytes, sha256
  dd4a6b464b7f88b847412c3e7301a925bf565d8d5dd60398728d2bc052ee73f7: "| $c(9,3)$ | **1084** | 1082 | two independent
  checkers |".

## Fresh arXiv searches
- https://export.arxiv.org/api/query (cap-set title and abstract queries), 2026-10-24T19:56:17Z (sha256
  feb1454e1e2486ee19ed8db9d704875e33a693bca09c11bd94ecf93404692d76), 20:10:52Z, 20:18:03Z, 20:24:43Z, 20:25:05Z,
  20:28:03Z, HTTP 200 each: no paper gives a cap in F_3^9 above 1082.
