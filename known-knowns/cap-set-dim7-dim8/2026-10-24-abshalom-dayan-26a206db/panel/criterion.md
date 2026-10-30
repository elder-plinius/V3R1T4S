# CRITERION skeptic verdict: claim on partial win p1 (target cap-set-dim7-dim8)

context: subagent (Agent tool, fresh context, claude-opus-5-5)

## Bottom line

Partial win p1 is met, read literally, for F_3^9. The file `cap_1104_n9.txt` is a cap of 1104 distinct vectors in
F_3^9. I checked that exhaustively with my own code, by two routes that share nothing with the package's checker.
1104 is strictly larger than 1082, the largest F_3^9 cap stated in the sources p1 names. It is also larger than the
unrefereed 1084 posted on GitHub on 2026-10-23. It is not a tie, the bar is not the wrong one, and no definition is
stretched. The main success criterion (n = 7 or 8) is not met, and the claim does not say it is.

## Clause-by-clause judgement of p1

p1 (verbatim): "A cap in F_3^9 or F_3^10, verified exhaustively, strictly larger than the best published cap for that
dimension at verification time (Edel's tables, FunSearch, X-evolve, OEIS, fresh arXiv search)."

| Clause | Judgement | Evidence (all paths relative to the claim folder) |
|---|---|---|
| Object type: "a cap" | Met | The object is a set of points. The condition tested is the affine one: no three distinct points x, y, z with x + y + z = 0 mod 3. In F_3, three distinct points are collinear exactly when x + y + z = 0, so this is the standard cap-set definition in F_3^9 = AG(9,3) (affine 9-space over the three-element field). For distinct x and y, the third point -(x+y) always differs from both (since -(x+y) = x forces y = x), so the bank's pair test leaves no loophole. |
| Space: "F_3^9" | Met | Strict parse: 1104 lines, each exactly 9 characters from {0,1,2}, LF line endings, no blank lines, comments or CR characters. The affine rank of the set is 9 (it does not sit in a lower-dimensional flat). |
| Distinct vectors | Met | 1104 distinct, 0 duplicates (my strict parse and both package routes). |
| "verified exhaustively" | Met | All 608,856 unordered pairs checked, so no pair's third point lies in S (my route 2, plus the package's checkers A and B). Independent exact route 3: an exact count of all solutions of x + y + z = 0 in S^3, done with an integer Fourier transform over F_3^9, finds 1104 solutions, which equals \|S\|, so there are 0 lines. Null models confirm the counter does detect lines: S plus one point gives 168 lines, and a random 1104-subset gives 11,435 lines. |
| "strictly larger" | Met | 1104 > 1082 by 22, and 1104 > 1084 by 20. Not a tie. |
| "best published cap for that dimension": Edel's tables | Met: bar 1082 | Edel's table is projective. I fetched it myself; the sha256 is identical to the package record. Row k = 8, q = 3 gives 541, and the page lists "A 541 Cap in PG(8,3)". The package records Theorem 1 of the 2012 Bierbrauer–Edel survey: an n-cap in PG(d,q) gives a 2n-cap in AG(d+1,q). So 2 x 541 = 1082 in AG(9,3). This compares like with like, affine against affine. **Null model:** Edel's 1216-cap in PG(9,3) could in principle give a larger AG(9,3) cap by deleting a hyperplane. Its published dual weight distribution (it sums to 3^10 = 59049) has maximum weight 1068, so its largest affine part is 1068 < 1082. |
| FunSearch | Met: bar 1082 | Read in `sources/funsearch-cap_set.ipynb` (sha256 matches the package): "recall that largest known cap set for `n = 9` has size `1082`" and "Discovered function that builds a $1082$-cap in $n = 9$ dimensions ... This matches the previously known best construction". |
| X-evolve | No n = 9 value | From the package record (Table 2 covers n = 3..8 only). I did not re-fetch the HTML. My arXiv listing of its abstract (2508.07932) claims only the asymptotic constant C >= 2.2203. |
| OEIS | No n = 9 value | From the package record (A090245 gives exact maxima only through n = 6). Not re-fetched. The Wikipedia source I fetched cites A090245 as "1, 2, 4, 9, 20, 45, 112, ...". |
| Fresh arXiv search at verification time | Met: nothing at or above 1104 found | Three arXiv API queries, 2026-10-24 20:24–20:28Z (details below). No title or abstract states any cap size in F_3^9 / AG(9,3). The newest construction paper, 2601.16917 (Jan 2026, AG(15,3), 124928 points), lists the known values as c_{7,3} >= 236, c_{8,3} >= 512 and c_{9,3} <= 2070, with **no** lower bound for c_{9,3}. |
| "at verification time" (staleness) | Met | Edel's table was last changed 2010-04-28, but FunSearch (2023) reaffirms 1082 for n = 9. Nothing newer was found on arXiv, Wikipedia or the Noirsys README (which gives "prior 1082"). The bar is not stale in the claim's favour. |
| Unrefereed public claims (not in p1's list) | 1104 still larger | Noirsys/capset README, fetched by me: "\| $c(9,3)$ \| **1084** \| 1082 \| two independent checkers \|". Its own caveat: "The $n=9$ clearance is **absence of evidence**". |
| "genuine, non-subsumed win" | Met | (a) The main criterion is not met, so p1 is not subsumed by a main win. (b) No trivial derivation from published pieces reaches 1104. Products of the best caps in dimensions adding to 9 give at most 2·512 = 1024, 4·236 = 944, 9·112 = 1008 and 20·45 = 900. Doubling gives 1082, and the affine section of the 1216-cap gives 1068. (c) S is not closed under negation (\|S ∩ -S\| = 336), so it is not simply the doubling of a 552-cap in PG(8,3) relabelled. (d) S is complete: 0 points of F_3^9 can be added. (e) It lies within known upper bounds: c_{9,3} <= 2070 (from 2601.16917), and each 8-dimensional slice (80/512/512) is within c_{8,3} <= 771. |

**Main success criterion (n = 7 or 8):** not met, and not claimed. The object lives in F_3^9. Its two 512-point slices
are the FunSearch 512-cap of F_3^8 and a linear image of it, so for n = 8 they only tie the record, which is not a win.

**Wording nit (not a stretch of the result):** CLAIM.md calls 1082 "the largest published cap in F_3^9 (Edel's
tables ...)". Edel's tables list projective caps, and 1082 follows from them only through the doubling theorem. The
derivation is standard and recorded in the package, and FunSearch states 1082 for n = 9 directly. The bar is right.

## Commands run and outputs (from inside the claim folder)

1. Hashes:
```
$ shasum -a 256 cap_1104_n9.txt checker/capcheck.py inputs/record_512_n8.txt inputs/verify_structure.py sources/funsearch-cap_set.ipynb
26a206db2dafae4a7f2c6f7478738acf5550af13998da2d4d0dff610ba83f82e  cap_1104_n9.txt
0d162d448d862f6ae35910ae000bb7a2f49e2564207a065b7d61fb8586e0f2dd  checker/capcheck.py
15f918afc3f5fc39bb300447e18929f980e51feea47f5113c3238ef80ad24860  inputs/record_512_n8.txt
485eabb0a199f4020d77974d899f2ff0c5a9156d899541721b2d1cebced926fa  inputs/verify_structure.py
f97f6f6ec331e5809ca4d40205224d2c5c613687d4f65316ecc2dd04a1724203  sources/funsearch-cap_set.ipynb
```
(The first three and the notebook match CLAIM.md. CLAIM.md gives no hash for `verify_structure.py`.)

2. Package checker:
```
$ python3 -I checker/capcheck.py cap_1104_n9.txt 9; echo "exit $?"
checker A: CAP - cap of size 1104 (pairs checked: 608856)
checker B: CAP - 0 lines inside S (lines meeting S twice or more: 608856)
VERDICT: CAP size 1104 n 9
exit 0
```

3. My own independent check (`criterion_check.py`, output saved in `criterion_check_output.txt`, Python 3.14.7):
```
$ python3 -I criterion_check.py cap_1104_n9.txt
route1 strict parse: lines=1104 problems=none
route1 distinct vectors: 1104 (duplicates: 0)
route2 pairs checked: 608856, pairs whose third point is in S: 0
route3 ordered solutions of x+y+z=0 in S^3: 1104 (|S| = 1104; cap iff equal)
route3 nontrivial unordered 3-term lines inside S: 0
route4 null A (S plus point code 0): solutions 2113, lines 168
route4 null B (random 1104-subset, seed 20261024): lines 11435
all-zero vector in S: False
first-digit slice sizes: {0: 80, 1: 512, 2: 512}
affine rank of S in F_3^9: 9
```
Route 3 uses exact arithmetic in Z[w], where w is a cube root of unity, so there is no floating point. The identity
used is sum over xi of fhat(xi)^3 = 3^9 · #{(x,y,z) in S^3 : x+y+z = 0}.

4. Structure and the 512 input:
```
$ python3 -I inputs/verify_structure.py
slice sizes {'0': 80, '1': 512, '2': 512}
slice1 == C: True  slice2 == D C: True
|K| = 92  slice0 subset of K: True
slice0 is a cap: True
$ python3 -I checker/capcheck.py inputs/record_512_n8.txt 8
checker A: CAP - cap of size 512 (pairs checked: 130816)
checker B: CAP - 0 lines inside S (lines meeting S twice or more: 130816)
VERDICT: CAP size 512 n 8
```
This is consistent with a valid three-slice construction. Every line of F_3^9 either lies inside one first-coordinate
slice or meets each slice once. So S is a cap exactly when each slice is a cap and slice 0 avoids -(C + D C). The
exhaustive checks above do not rely on this argument.

5. Extra facts (`criterion_extra.py`, output saved in `criterion_extra_output.txt`):
```
$ python3 -I criterion_extra.py
S == -S: False  |S & -S| = 336
points of F_3^9 outside S that could be added without creating a line: 0
```

6. Network: one GET per page, no retries, nothing bypassed. Saved under `criterion_fetch/`. Times are UTC, taken just
before each request.

| Time (UTC) | Page | Result | sha256 of saved body |
|---|---|---|---|
| 20:24:37 | arXiv API query 1 over http | 301 redirect to https, 0 bytes; I then made one request to the https URL | (empty) |
| 20:24:43 | arXiv API query 1 over https: `abs:"cap set" OR abs:"cap sets" OR ti:"cap set" OR abs:"large caps" OR ti:"caps"`, newest 100 | 200, 217907 bytes (911 hits; window back to 2026-03-29, noisy) | 53679597e75bd8ef84dcbdddd888e9d2622203cd3c0f20e558c82c71b97f2641 |
| 20:25:05 | arXiv API query 2: `abs:"cap set" OR abs:"cap sets" OR ti:"cap set" OR ti:"cap sets" OR abs:"large caps" OR abs:"affine caps"`, newest 200 | 200, 188673 bytes (95 hits, all returned, 2008-11-19 to 2026-10-20; list in `criterion_fetch/arxiv_search2_titles.txt`) | a4e4c045ef427005574c183a46de3b5233d0f078f2a135fa82c8b60126fc76fd |
| 20:25:43 | arxiv.org/html/2601.16917v1 | 404 (no HTML version); not retried, file deleted | n/a |
| 20:25:53 | arxiv.org/pdf/2601.16917v1 | 200, 1590771 bytes. I kept only the text extract `criterion_fetch/arxiv_2601.16917v1.txt` (pdftotext) and deleted the PDF to save space | 48ab07c9bde0aaaf54d0e5297d6a47dc4d00e3f6cf3de98f21d1df10c48e1d46 (PDF) |
| 20:26:28 | en.wikipedia.org Cap_set, raw wikitext | 200, 18886 bytes; gives no n = 7, 8 or 9 value | ff1dc3809e1f0263e57f8080a550d0b108f15e23eefdcbd85c5fa93578018627 |
| 20:26:56 | api.github.com repos/Noirsys/capset/readme | 200, 5719 bytes; 1084 for c(9,3), prior 1082 | dd4a6b464b7f88b847412c3e7301a925bf565d8d5dd60398728d2bc052ee73f7 |
| 20:28:03 | arXiv API query 3: `abs:FunSearch OR abs:AlphaEvolve OR abs:"cap set problem"`, newest 200 | 200, 281184 bytes (114 hits, all returned; 26 mention FunSearch and 72 AlphaEvolve; the only LLM-search abstract that mentions caps is X-evolve, which is asymptotic only) | d71245268321a3c6dfc44d99ec25c92b9adf31a882405419e670e6fc63672088 |
| 20:28:35 | yvesedel.de/Matritzen/CAPs/CAPMatIndex.html | 200, 15275 bytes; identical hash to the package record; row 8, q = 3: 541; "Last changed: April 28, 2010" | 8aa5a2837a51d261c7b030e500c2c99e396d9ce7a653ecce8bc9badf6c1e2817 |
| 20:29:18 | yvesedel.de/Matritzen/CAPs/Matrizen/(1216,9,3).html | 200, 14184 bytes; dual weight distribution sums to 59049; maximum weight 1068 (`criterion_fetch/edel_1216_weight_check.txt`) | 19f371e22736f9a9e0f6504db6707553337d9003056af4ba1e0f5bda6638fd69 |

## What I did not verify, and the remaining risk

- X-evolve Table 2 and OEIS A090245: I relied on the package's table record and did not re-read them. Neither is
  recorded as giving an n = 9 value, so neither could raise the bar unless the record is wrong.
- The Bierbrauer–Edel survey's Theorem 1 (doubling): taken from the package record. It is a standard result and is
  consistent with FunSearch's 1082.
- "Published" is checked against p1's named sources plus arXiv titles and abstracts. The full texts of arXiv papers,
  journals outside arXiv (for example the Karapetyan group's venues) and MinT, which timed out for the panel, were not
  searched exhaustively. The newest paper from that group (2601.16917) gives no c_{9,3} lower bound in its own survey
  of known values, and the Noirsys README of 2026-10-23 states "prior 1082". So a published cap of 1104 or more in
  F_3^9 is unlikely but cannot be fully excluded.
- Novelty, priority and acceptance by the bank's maintainers are outside this criterion check.

confirmed_scope: The file cap_1104_n9.txt (sha256 26a206db2dafae4a7f2c6f7478738acf5550af13998da2d4d0dff610ba83f82e) is an affine cap of 1104 distinct points in F_3^9, with no three distinct points summing to 0 mod 3, verified exhaustively over all 608,856 pairs and by an exact Fourier count; 1104 is strictly larger than every F_3^9 cap size found on 2026-10-24 in the sources p1 names as the panel read them (1082 from the FunSearch notebook and from doubling Edel's 541-cap in PG(8,3), no n = 9 value in X-evolve Table 2 or OEIS A090245, none in arXiv titles and abstracts) and than the unrefereed 1084 of Noirsys/capset, so it meets partial win p1 for dimension 9 and does not meet the main n = 7 or 8 criterion.

pass: true
