# NOVELTY verdict: constant-weight-codes, cell A(26,10,12)
context: fresh reviewer (new subagent context started for the NOVELTY role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:57:22Z

## Claim under review

A(26,10,12) >= 214 from object/A-26-10-12-214words.txt (sha256 c78abc24b831d29945e88f58953941927761132fa60f8a2cd2696a5dcec81715). My role is only whether 214 is strictly greater than every published value for this cell (and its mirror A(26,10,14)), and not above the upper bound.

## 1. Brouwer's table, live fetch

One plain curl request, started at 2026-11-27T18:53:44Z (from `date -u`).

| item | value |
|---|---|
| URL | https://aeb.win.tue.nl/codes/Andw.html |
| HTTP status | 200 |
| Date | Fri, 27 Nov 2026 18:53:44 GMT |
| Last-Modified | Fri, 27 Nov 2026 00:32:42 GMT |
| ETag | "1fe1b-6613732bff19f" |
| Content-Length | 130587 (body 130587 bytes) |
| sha256 of body | ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad |

This is byte-identical to the page recorded in the-record-we-beat/RECORD.md (same sha256, Last-Modified and ETag); the table has not changed since the claimant's fetch.

Section "Bounds on A(n,10,w)" (header n\w, columns 6 to 16). Row 26 reads, in page order: 13 (w=6), 30-36, 68-104, 91-213, 130-397, 168-565, then the w=12 cell (page line 2248):

```
<td><a href="cwc/d10/a26.10.12.213H">213</a><sup>Bol</sup>-691<sup>KT</sup></td>
```

Lower bound 213, label Bol; upper bound 691, label KT. The table lists w <= n/2 only, so the mirror A(26,10,14) has no separate cell; it equals this one.

Notes naming the cell or its labels:
- Bol: "Ignacio Bolívar, email 2026-11-09 with A(26,10,12) ≥ 213, A(54,6,5) ≥ 2210."
- KT: "Hyun Kwang Kim & Phan Thanh Toan, Improved Semidefinite Programming Bound on Sizes of Codes, arXiv:1212.3467v1, Dec 2012."
- No other note on the page contains "A(26,10,12)" or "A(26,10,14)" (grep).

214 > 213 and 214 <= 691.

## 2. arXiv papers

- arXiv:2608.13906 (Echols, "New lower bounds for constant-weight codes via seeded bit-swap tabu search", v1 only, submitted 14 Aug 2026): fetched abs (200) and HTML v1 (200). I parsed Table 1 into 124 (n,d,w,prior,new,gain) rows, matching the abstract's "124 new constructions". No row for (26,10,12) or (26,10,14). Nearby rows: (26,10,8) 55->68, (25,10,12) 137->141, (26,10,13) 225->234, (28,10,14) 812->814.
- arXiv:2607.19550 (Lysenstoen, v1 only): abs (200) and HTML v1 (200). Every A(n,d,w) mentioned has d = 6 (cells with n 18 to 28). No d = 10 cell.
- Newer papers: arXiv search, sorted newest first, for "constant weight codes" (200), "constant-weight code" (200) and "Brouwer's table" (200). Lower-bound papers newer than Echols found and checked:
  - arXiv:2611.24958 (thirteen cyclic-orbit codes): Table rows are d = 4 and d = 6 only. No (26,10,12).
  - arXiv:2610.24025 (prescribed-automorphism search): abstract lists only A(n,6,w) cells.
  - arXiv:2611.03682 (kissing numbers): uses weight-8, distance-8 codes only.
  - Also checked the earlier arXiv:2603.00174 (Rosin): its 24-row table has d = 10 rows (22,10,8), (25,10,8), (28,10,7) only.
  - The other results of the searches are upper-bound, nonbinary or unrelated papers (for example arXiv:2611.00173, an upper bound for A(19,6,8)).
- Papers citing Echols: the Semantic Scholar citations API answered HTTP 429; I stopped for that URL as the rules require. The date-sorted arXiv searches above are my coverage of newer papers.
- Echols's code repository (github.com/williamechols/cwc-seeded-tabu-search): the GitHub API tree request answered HTTP 403 (rate limit); stopped for that URL. The paper's Table 1 is in the paper itself and does not point to the repository for its values, so this is not needed for the criterion.

## 3. V3R1T4S repository (main branch and pull requests)

- TROPHY_CASE.md (raw, 200, 31306 bytes, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113): no occurrence of A(26,10,12), A(26,10,14) or A26_10_.
- known-knowns/bigger-codes/INDEX.csv (raw, 200, 7579 bytes, sha256 e7ed745ea3299877231732acb040b97d5e7953c04ef7a76f228856d3b92e2ff7): the n = 26 rows are A(26,6,8), A(26,6,9), A(26,6,11), A(26,6,13). No d = 10 cell for n = 26.
- Pull requests, state=all, through the GitHub API at 100 per page, pages 1 to 13 (each 200; 1203 PRs). Searched titles and bodies for A(26,10,12), A(26,10,14), (26,10,12), A26_10_12, a26.10.12 and A-26-10-12: 0 hits. Of 37 titles containing "constant-weight", the d = 10 ones are four closed Delsarte LP upper-bound claims (A(31,10,7), A(34,10,8), A(33,10,7), A(32,10,7)); none for this cell.

## 4. Neighbouring hosted codes (optional)

Downloaded once each from the table's d10 folder (both 200): a27.10.13.425H (sha256 a610fa4eb8bc262213a46eeeb4226e61d8a3c75d2083c3ae41f2b280ec441170) and a28.10.14.817H (sha256 7d6670ee15184f18d8374e7d11c7fc92c0bc000c0501e0d259368f01f8e51db7). My script verified both (425 and 817 distinct words, correct weight, minimum distance 10) and shortened them:

```
A(27,10,13) shortened on a 1-coordinate -> A(26,10,12) >= 208 (coord 12 )
A(28,10,14) shortened on two 1-coordinates -> A(26,10,12) >= 202
A(28,10,14) shortened on two 0-coordinates -> A(26,10,14)=A(26,10,12) >= 201
```

Other neighbours by table value only: appending a coordinate to A(25,10,12) >= 141 or A(25,10,11) >= 125 gives at most 141; averaging over the unhosted A(27,10,12) >= 351 gives 351*15/27 = 195. Largest value found this way: 208, below 214.

## Size of the object (sanity check for the comparison)

Written from the definition before and without reading verify-it-yourself/ (I did not open the claimant's checker at all). My script on object/A-26-10-12-214words.txt:

```
c78abc24b831d29945e88f58953941927761132fa60f8a2cd2696a5dcec81715  (shasum -a 256)
M 214 distinct 214 weights [12]
min distance 10
pairs 22791
M>213 True M<=691 True
```

## Problems found

None for novelty. Two lookups could not be completed (Semantic Scholar citations 429; GitHub API tree of Echols's repository 403 rate limit). Neither is needed by the criterion: the criterion names Brouwer's table, the two arXiv papers and newer arXiv papers, and the newer arXiv papers were covered by date-sorted arXiv searches.

## Reasoning

The live table (unchanged since the claimant's fetch) gives 213-691 for A(26,10,12), credited to a 2026-11-09 email. Neither named arXiv paper nor any newer arXiv lower-bound paper I found lists this cell, the V3R1T4S repository has no existing or pending claim on it, and shortening the neighbouring hosted codes gives at most 208. 214 is strictly greater than every published value I found and does not exceed the upper bound 691.

pass: true
