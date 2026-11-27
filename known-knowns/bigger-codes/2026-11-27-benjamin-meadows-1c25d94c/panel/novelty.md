# NOVELTY verdict: constant-weight-codes, cell A(29,6,6)
context: fresh reviewer (new subagent context started for the NOVELTY role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:57:37Z

## Claim under review

A(29,6,6) >= 1207, object file object/A-29-6-6-1207words.txt. Its sha256 in my run: `1c25d94ca5861e9762b92ce4dc28d493bf2c2d5827466cb73cdf949c73079642` (matches the package). I wrote my own check script (my scratch folder, nov.py) from the definition. I did not open verify-it-yourself/ at any point. The script reported `object size 1207 mind 6`: every word has length 29 and weight 6, all words are distinct, and the minimum pairwise distance is 6.

## 1. Brouwer's table (live fetch)

One plain curl request to https://aeb.win.tue.nl/codes/Andw.html, made at 2026-11-27T18:53:44Z:

- HTTP status: 200
- Date: Fri, 27 Nov 2026 18:53:44 GMT
- Last-Modified: Fri, 27 Nov 2026 00:32:42 GMT
- ETag: "1fe1b-6613732bff19f"
- Content-Length: 130587 (130587 bytes received)
- sha256 of body: `ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad`

These are the same Last-Modified, ETag, length and sha256 as in the-record-we-beat/RECORD.md, so the page has not changed since the claimant's fetch.

Cell, under section "Bounds on A(n,6,w)", row n = 29, in the third column (the column headers read w = 4, 5, 6, ...):

```
<td><a href="cwc/d6/a29.6.6.1205H">1205</a><sup>Pil</sup>-1459</td>
```

The sub-table "Values of A(n,6,6)" prints the same value: `<td>1205<sup>Pil</sup>-1459</td>`. The lower bound is 1205 and the upper bound is 1459. The label legend reads: "Pil: research group Pilcraft, email 2026-11-21, with 3 new codes." The table prints only w <= 14, so the mirror cell A(29,6,23) does not appear on its own; by complement it equals this cell. I found no other note on the page that names this cell.

Result: 1205 < 1207 <= 1459.

## 2. arXiv

- arXiv:2608.13906 (Echols). I parsed every table row of the HTML version and found 124 (n,d,w) entries, which matches the paper's "124 improved cells". The d = 6 entries are (21,6,5), (43,6,5), (44,6,5), (54,6,5), (55,6,5), (56,6,5), (58,6,5), (59,6,5), (30,6,6), (34,6,6), (35,6,6), (20,6,8) and (22,6,8). Neither (29,6,6) nor (29,6,23) is among them. The paper's code repository (GitHub tree API, one request, HTTP 200) lists 140 paths. The w = 6, d = 6 files are only 30_6_6_1316, 34_6_6_2017 and 35_6_6_2204. No file exists for (29,6,6).
- arXiv:2607.19550 (Lysenstoen). This paper covers A(23,6,10) and A(24,6,10). Neither its text nor its tables mention (29,6,6) or (29,6,23).
- Newer papers. I ran two arXiv API searches over https, sorted by submission date: "constant weight codes" and "constant-weight code" (both HTTP 200). I also listed the papers that cite Echols through the Semantic Scholar API (HTTP 200, 4 citing papers). Among 2026 papers I checked these in HTML: 2611.24958 (Thirteen improved CW codes), 2610.24025 (prescribed-automorphism search, d = 6 and 27 <= n <= 29), 2610.10973 (G-invariant Erdős–Hanani), 2609.35051 and 2611.03682 (the kissing-number papers that cite Echols). I searched their text for the pattern A(29,6,6) and A(29,6,23), and their tables for n,d,w = 29,6,6 or 29,6,23. Every one returned 0 hits. 2610.24025 lists n = 29 values only for w = 9, 10 and 11. 2611.24958 lists (29,6,5) >= 333, which Brouwer's table has since raised to 336.

## 3. V3R1T4S repository

- TROPHY_CASE.md on main (raw, HTTP 200, sha256 `83af764f…6113`): it has no entry for A(29,6,6) or A(29,6,23). Its n = 29 entries are A(29,6,10), A(29,6,11) and A(29,6,12).
- known-knowns/bigger-codes/INDEX.csv on main (raw, HTTP 200, sha256 `e7ed745e…2ff7`): it has no row for (29,6,6) or (29,6,23).
- Pull requests. Page 1 of the pulls API (state=all, 100 per page, HTTP 200) covers PRs 1152 to 1258, and no title on it names the cell. The Link header gives 13 pages. My requests for pages 2 to 8 each returned HTTP 403, with the message "API rate limit exceeded". The unauthenticated limit had already been used up on this network. As the rules require, I stopped there and did not retry or switch routes. As a substitute I used the GitHub issue-search API, which has a separate limit and searches both titles and bodies. A query for the exact title form `"A(30,12,9)"` returned the known PR 1254, which shows that the search finds titles written in this format. The queries `"A(29,6,6)"`, `"A(29, 6, 6)"`, `"A(29,6,23)"`, `"29,6,6"` and `in:title "(29,6,6)"` returned no PR for this cell. The only matches were fuzzy hits on other cells: A(35,6,6) in PRs 59 and 507, and A(29,6,11) to A(29,6,14) upper-bound claims in PRs 449 to 452.

## 4. Neighbouring cells (optional)

I downloaded the hosted code https://aeb.win.tue.nl/codes/cwc/d6/a30.6.6.1316H once (HTTP 200, Last-Modified Sun, 02 Aug 2026 11:05:45 GMT, sha256 `544c3295…a487`). It has 1316 words and minimum distance 6. Shortening it to length 29 (keeping the words that have a 0 in one coordinate) gives at most 1156 words over the 30 coordinates. Appending a zero to the A(28,6,6) code gives 1174. The table does not list A(30,6,7). The largest value I found from neighbouring cells is 1174. The largest value I found from any source is 1205, the table's own entry.

## Problems found

The pull-request title listing is incomplete: I read page 1 of 13 directly, and pages 2 to 8 returned HTTP 403 because the rate limit was exhausted. The calibrated search over titles and bodies covers the gap, so I consider this check passed. A complete listing of all titles was not possible in this run. Nothing else.

## Reasoning

The live table's lower bound for A(29,6,6) is 1205, credited to Pilcraft (2026-11-21), and the upper bound is 1459. The size 1207 is strictly greater than 1205 and below 1459. None of the arXiv papers I checked lists a value for this cell or its complement: Echols, Lysenstoen, the three newer constant-weight papers, or the papers that cite Echols. The V3R1T4S repository has no existing claim on the cell on its main branch, and searches found no claim in its PRs. Shortening the neighbouring hosted code gives far less than 1205. On everything I could check, M = 1207 is new.

pass: true
