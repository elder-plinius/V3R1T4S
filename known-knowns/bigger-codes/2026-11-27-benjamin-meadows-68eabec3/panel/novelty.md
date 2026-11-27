# NOVELTY verdict: constant-weight-codes, cell A(27,8,8)
context: fresh reviewer (new subagent context started for the NOVELTY role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:57:27Z

## Scope

I was asked whether M = 778 is strictly greater than every published value for A(27,8,8), which is the same cell as A(27,8,19). I did not read or run the claimant's checker (verify-it-yourself/). Validity of the code belongs to the other reviewers. The only thing I checked on the object was that object/A-27-8-8-778words.txt has sha256 68eabec3d2808175e4f0f8db629c0b6137d8ab94b19e8e24e23186b03f6bc26f and holds 778 distinct non-comment lines (778 after `sort -u`).

## 1. Brouwer's table (live fetch)

I made one plain curl request to https://aeb.win.tue.nl/codes/Andw.html at 2026-11-27T18:53:48Z, saving headers and body in my scratch folder.

- HTTP status: 200
- Date: Fri, 27 Nov 2026 18:53:49 GMT
- Last-Modified: Fri, 27 Nov 2026 00:32:42 GMT
- ETag: "1fe1b-6613732bff19f"
- Content-Length: 130587 (body file is 130587 bytes)
- sha256 of the body: ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad. This is the same as the page snapshot in the-record-we-beat/RECORD.md, so the page has not changed since the claimant's fetch.

The cell is in section "Bounds on A(n,8,w)" (columns w = 5..14), row `<th>27</th>`, fourth data column (w = 8), at page line 1561:

```
<td><a href="cwc/d8/a27.8.8.777H">777</a><sup>Di</sup>-1252</td>
```

That gives lower bound 777 and upper bound 1252. The label Di resolves on page line 280 to "Di: Kerem Dilker, email 2026-11-26 with 31 new bounds." The table only prints w up to n/2, so the mirror cell A(27,8,19) does not appear separately. Searching for `27,8,8`, `27,8,19` and `a27.8.19` found no note on the page that names this cell. The notes in the d=8 Comments section cover other cells (A(27,8,5), A(27,8,9), A(27,8,10), A(27,8,13), A(27,8,14) and others), but not A(27,8,8).

778 > 777 and 778 <= 1252.

## 2. arXiv papers

- Echols, arXiv:2608.13906 (only version v1, 14 Aug 2026). In Table 1 of the HTML version, the row `| 27 | 8 | 8 | 769 | 775 | +6 |` lists 775. The code repository the paper names (github.com/williamechols/cwc-seeded-tabu-search, one API tree request, HTTP 200) contains `codes/27_8_8_775.txt` for this cell. Largest value: 775.
- Lysenstoen, arXiv:2607.19550 (only version v1, 21 Jul 2026). The abstract gives only d = 6 cells: A(23,6,10), A(24,6,10), A(23,6,11), A(24,6,8). No value for this cell.
- Newer papers. I searched arXiv for "constant weight codes" and "constant-weight code" (sorted newest first, 50 per page), plus "Brouwer table constant weight" and "tabu search codes". These 2026 hits list explicit lower bounds:
  - Iskandar, arXiv:2611.24958: 13 cells, all with d = 4 or 6. A(27,8,8) is not among them.
  - Dzoba, arXiv:2610.24025: d = 6 cells only.
  - Lin, arXiv:2611.03682: weight-8, distance-8 codes for kissing configurations in dimensions 32 to 39, so lengths 32 to 39 and not length 27.
  - Rosin, arXiv:2603.00174: the Table 1 rows near this cell include A(27,8,10) but not A(27,8,8).

  The other hits are about upper bounds or are off topic.
- Papers citing Echols. My one request to the Semantic Scholar citations API returned HTTP 429. Per the rules I did not retry. The arXiv searches above are the substitute coverage.

No paper I found gives a value above 775 for this cell.

## 3. V3R1T4S repository

- TROPHY_CASE.md on main (raw.githubusercontent.com, HTTP 200) and known-knowns/bigger-codes/INDEX.csv on main (HTTP 200) do not mention A(27,8,8) or A(27,8,19). The only d=8, n=27 entries are A(27,8,10) and A(27,8,11).
- Pull requests, from the GitHub API with state=all, 100 per page, one request per page:
  - Pages 1 to 10 returned HTTP 200. They hold 1000 pull requests, #206 to #1258, created 2026-10-16T02:58:23Z to 2026-11-27T18:05:15Z. A regular expression for "27,8,8", "27,8,19", "27-8-8" and the like matched no title and no body.
  - Pages 11 to 13 returned HTTP 403 (unauthenticated API rate limit). Per the rules I did not retry and did not switch to another route. The pull requests older than 2026-10-16 (numbers below 206) are therefore unchecked.
  - A plain request to the github.com pulls search page returned 200, but the results load client-side, so the page showed nothing usable.

## 4. Neighbouring cells (optional)

I downloaded each hosted code once and wrote my own parser and checker (shorten.py in my scratch folder, standard library, run with -I):

| code | sha256 | result |
|---|---|---|
| cwc/d8/a28.8.8.1057H | c1d8cc162ff1c5c0bd8ea0596b95100171fa733ca13e7e3e6b5fae17eb32faa0 | 1057 words, weight 8, minimum distance 8 confirmed. Shortening (keep the words with 0 in one coordinate, best coordinate) gives A(27,8,8) >= 760. |
| cwc/d8/a28.8.9.1419H | 68f5c2d82ca9cc38356185ee83cab56540472efcf7b126fb7d5614da88bbc17f | 1419 words, weight 9, minimum distance 8. Shortening (keep the words with 1 in one coordinate) gives A(27,8,8) >= 466. |

The largest value these neighbours imply is 760, below 777.

## Problems found

- Two parts of the search could not be completed. The Semantic Scholar citation lookup returned 429, and the V3R1T4S pull requests older than 2026-10-16 (API pages 11 to 13) returned 403.
- I do not count either gap against novelty, for two reasons:
  - The repository's success criterion covers only Brouwer's table and arXiv papers. Both were checked in full.
  - On 2026-10-16 the table's value for this cell was 769 or lower (Echols lists 769 as the prior table value). A pull request from before that date claiming 778 or more would have beaten the table by at least 9. No such claim appears on main in TROPHY_CASE.md or INDEX.csv, and none appears in any of the 1000 pull requests since.
- The gaps are recorded here so the pull-request history can be re-checked once the rate limit resets.

## Reasoning

| source | largest value for A(27,8,8) |
|---|---|
| live table (unchanged since the claimant's snapshot) | 777 (upper bound 1252) |
| Echols (paper and repository) | 775 |
| Lysenstoen | none |
| 2026 arXiv papers found | none |
| V3R1T4S (main and checked pull requests) | none |
| shortening of hosted neighbouring codes | 760 |

M = 778 is strictly greater than all of these and does not exceed the upper bound 1252. The size is new for this cell.

pass: true
