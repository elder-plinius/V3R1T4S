# NOVELTY verdict: constant-weight-codes, cell A(29,10,8)
context: fresh reviewer (new subagent context started for the NOVELTY role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:57:04Z

## Claim under review

A(29,10,8) >= 98, object object/A-29-10-8-98words.txt. The package's comparison point is the table lower bound 96 (upper bound 203).

Object sanity check (my own script, written from the definition before reading verify-it-yourself/; I did not open verify-it-yourself/ at any point):

```
sha256 5c0ebfcf58bd20ac9e89c62b10560e485e9a416bf027df1dd4c680feaf3354ee
M 98 min distance 10
```

The script also asserted that every word has length 29, uses only 0/1, has weight 8, and that all words are distinct. So M = 98.

## 1. Brouwer's table (live)

One plain curl request, started at 2026-11-27T18:53:44Z:

```
HTTP status 200
Date: Fri, 27 Nov 2026 18:53:45 GMT
Last-Modified: Fri, 27 Nov 2026 00:32:42 GMT
Content-Length: 130587
ETag: "1fe1b-6613732bff19f"
sha256 ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad
```

These match the package's RECORD.md (same Last-Modified, ETag, length and sha256), so the table has not changed since the claimant fetched it.

Cell, section "Bounds on A(n,10,w)", row n = 29, column w = 8 (page line 2278):

```
<td><a href="cwc/d10/a29.10.8.96">96</a><sup>E</sup>-203</td>
```

So the lower bound is 96 (label E) and the upper bound is 203. The table prints only w <= n/2, so the mirror cell A(29,10,21) is not shown separately; by complementation it is the same cell. Label E on the page reads: "William Echols, arXiv:2608.13906 (with 126 new codes) and email 2026-08-08 (with 6 new codes, removing five items from the list of lost codes)." A search of the page for "29,10,8" and "29,10,21" returned nothing. The notes after the d=10 table (polished group codes, A(21,10,8), A(25,10,8)) do not mention this cell.

98 > 96 and 98 <= 203.

## 2. arXiv papers

- arXiv:2608.13906 (Echols), HTML v1, Table 1 has the row `29 | 10 | 8 | 91 | 96 | +5` (prior 91, new 96). Table 2 lists only (32,8,2)-derived cells. The largest value Echols gives for this cell is 96.
- arXiv:2607.19550 (Lysenstoen), abstract and HTML: the only cells are A(23,6,10), A(24,6,10), A(23,6,11), A(24,6,8) (all d = 6), plus their polished values. No value for A(29,10,8).
- arXiv search for "constant weight codes" and for "constant-weight code", sorted newest first (both returned 92 results). I checked the 2026 entries that report constant-weight lower bounds:
  - 2611.24958 (Iskandar, thirteen improved codes): its table covers only d = 4 and d = 6 cells (including A(29,6,5) >= 333). Nothing at d = 10.
  - 2610.24025 (Dzoba): A(n,6,w) cells only.
  - 2611.03682 (Lin, kissing numbers): new weight-8, distance-8 codes. Nothing at d = 10.
  - 2610.10973 (Chee): asymptotic G-invariant packing theorem, no table values for this cell.
  - 2611.00173 (Chang): an upper bound for A(19,6,8).
- arXiv search for "Brouwer's table" (3 results; 2610.24025 and 2611.00173 are the 2026 ones) and for "tabu constant weight" (2 results; 2603.00174, Rosin) found nothing newer that touches this cell.
- Papers citing Echols: the Semantic Scholar citations API answered HTTP 429. I stopped for that URL as the rules require. The arXiv searches above are the substitute for this check.

## 3. V3R1T4S repository (main branch and pull requests)

- raw TROPHY_CASE.md: HTTP 200, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113. It has no row for A(29,10,8) or A(29,10,21), and its constant-weight rows are all d = 6 or d = 8.
- raw known-knowns/bigger-codes/INDEX.csv: HTTP 200, sha256 e7ed745ea3299877231732acb040b97d5e7953c04ef7a76f228856d3b92e2ff7, 31 lines. It has no row for this cell and no d = 10 row at all.
- Pull requests via the GitHub API (state=all, per_page=100): 13 pages, each fetched once, all HTTP 200, 1203 pull requests in total (numbers 1 to 1258). I searched the titles and bodies of all of them for 29,10,8 / 29,10,21 / 29-10-8 / A29_10_8 and found no match. The only titles naming a d = 10 cell are #348 to #351: Delsarte LP upper bounds for A(32,10,7), A(33,10,7), A(34,10,8) and A(31,10,7), none of which is this cell.

## 4. Neighbouring cells (optional check)

I downloaded two hosted codes, once each, and checked them with my own script:
- cwc/d10/i30.8 (A(30,10,8) >= 108, label c): 4 base words under a 27-cycle on coordinates 4 to 30. That expands to 108 words of weight 8 with minimum distance 10. Shortening on a coordinate where the words have a 0 gives at most 81 words for (29,10,8).
- cwc/d10/a30.10.9.203H (A(30,10,9) >= 203): 203 words of weight 9 with minimum distance 10. Keeping the words with a 1 in one coordinate and deleting that coordinate gives at most 63 words for (29,10,8).
- From the table itself, appending a zero coordinate to A(28,10,8) >= 85 gives 85.

The largest value these simple derivations give is 85, below 96.

## Problems found

None that affect novelty. Two lookups were refused and I did not retry either: the Semantic Scholar citations API (HTTP 429) and the GitHub tree listing of Echols' code repository (HTTP 403, API rate limit). The criterion does not need the repository listing, because Echols' paper itself gives 96 for this cell and Brouwer credits the same 96 to Echols.

## Reasoning

M = 98 is strictly greater than the live table's lower bound of 96. The table was re-fetched in this review and is identical to the claimant's fetch. 98 is also greater than every other value I found: Echols 96; Lysenstoen none; newer 2026 arXiv papers none; V3R1T4S main branch and all 1203 pull requests none; neighbour-code derivations at most 85. It is not above the upper bound of 203.

pass: true
