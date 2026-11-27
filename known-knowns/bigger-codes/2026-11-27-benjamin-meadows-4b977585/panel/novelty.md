# NOVELTY verdict: constant-weight-codes, cell A(27,8,12)
context: fresh reviewer (new subagent context started for the NOVELTY role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:57:23Z

## What I checked

1. The live Brouwer table (one curl request), the cell A(27,8,12), its labels and the comments on the page.
2. arXiv:2608.13906 (Echols) and arXiv:2607.19550 (Lysenstoen).
3. Newer arXiv papers: the arXiv search for "constant weight codes" and for "constant-weight code", sorted newest first (both returned the same 18 papers from 2026), the search for "Brouwer's table", and the papers citing Echols (Semantic Scholar citations API).
4. The V3R1T4S repository: TROPHY_CASE.md and known-knowns/bigger-codes/INDEX.csv on main, and its pull requests.
5. Optional: the shortening bounds that two hosted neighbouring codes give for this cell.

Before using any table value I counted and checked the object with my own script, written from the definition, in my scratch folder. I did not read verify-it-yourself/ at any point. Result: object/A-27-8-12-3387words.txt, sha256 4b977585972408991e43784ce2f81591c529d9f3a9d770ee9fc4262eb056e3ba (matches the claim), `M 3387 n 27 w 12 min distance 8`.

## 1. Live table

- `curl` of https://aeb.win.tue.nl/codes/Andw.html at 2026-11-27 18:53:43 UTC (output of `date -u`): HTTP 200, Date `Fri, 27 Nov 2026 18:53:42 GMT`, Last-Modified `Fri, 27 Nov 2026 00:32:42 GMT`, Content-Length 130587, ETag `"1fe1b-6613732bff19f"`, body sha256 `ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad`. This is byte-identical to the page in the-record-we-beat/RECORD.md, so the table has not changed since the claimant's fetch.
- Cell (section "Bounds on A(n,8,w)", row 27, column w = 12):
  `<td><a href="cwc/d8/a27.8.12.3374H">3374</a><sup>Di</sup>-10460<sup>KT</sup></td>`
  Lower bound 3374, upper bound 10460.
- Lower-bound label: `Di: Kerem Dilker, email 2026-11-26 with 31 new bounds.` Upper-bound label: `KT: Hyun Kwang Kim & Phan Thanh Toan, Improved Semidefinite Programming Bound on Sizes of Codes, arXiv:1212.3467v1, Dec 2012.`
- Mirror cell A(27,8,15): the d = 8 table has columns w = 5..14 only (w up to n/2), so the mirror is this same cell.
- Notes: none of the page's notes names A(27,8,12). The d = 8 comments mention A(27,8,5), A(27,8,9), A(27,8,10), A(27,8,13) and A(27,8,14), and BSSS values for other cells, but nothing for (27,8,12).

## 2. Echols and Lysenstoen

- Echols, arXiv:2608.13906v1, Table 1 row: `| 27 | 8 | 12 | 3335 | 3337 | +2 |`. That is 3337, below 3387.
- Lysenstoen, arXiv:2607.19550: the abstract and full HTML cover A(23,6,10), A(24,6,10), A(23,6,11) and A(24,6,8) only. A grep of the HTML for `A(27`, `(27,8`, `,8,` and `d = 8` returned nothing, so the paper has no value for this cell.

## 3. Newer arXiv papers

The search hits that report binary constant-weight lower bounds, together with the papers citing Echols (4 citations: 2611.24958, 2611.03682, 2610.24025, 2609.35051):
- 2611.24958 (Iskandar, thirteen improved codes): its table covers (16,4,7), (20,4,5), (25,4,6), (29,4,5), (29,6,5) and seven (n,4,5) cells. Not this cell.
- 2610.24025 (Dzoba): A(n,6,w) cells only.
- 2611.03682 (Lin, kissing numbers): weight-8, distance-8 codes only.
- 2609.35051 (kissing-number constructions): its HTML has no match for `A(27`, `(27, 8`, `27,8,12` or weight 12.
- None of the other search hits (upper bounds, q-ary and nonbinary codes, designs, Steiner systems) lists a lower bound for A(27,8,12).

No arXiv value larger than 3374 turned up for this cell. The largest arXiv value I found is Echols' 3337.

## 4. V3R1T4S repository

- raw main TROPHY_CASE.md: HTTP 200, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113. known-knowns/bigger-codes/INDEX.csv: HTTP 200, sha256 e7ed745ea3299877231732acb040b97d5e7953c04ef7a76f228856d3b92e2ff7 (fetched 18:56:02 UTC). Grepping both for `27,8,12` and `27,8,15` gives no match. Their nearest cells are A(27,8,10) ≥ 1737 and A(27,8,11) ≥ 2421.
- Pull requests:
  - Page 1 of the unauthenticated REST API list of open PRs: HTTP 200, 100 PRs, none with a title naming (27,8,12).
  - Page 2 of the open list, and page 1 of the closed list: HTTP 403, body `API rate limit exceeded`. I stopped for those URLs and did not retry them.
  - The HTML pulls page with a search query: HTTP 200, but it loads its results client-side, so the static HTML has no results to read.
  - I then ran read-only searches through the authenticated GitHub search API (no writes):
    - `constant-weight in:title`: 37 PRs (open and closed), listed in full. None names A(27,8,12) or A(27,8,15). The A(27,8,…) titles are for w = 10 and 11 only (#438, #439, #57).
    - `27 8 12 in:title,body`: 60 hits. The only constant-weight hit is #57, which is about A(27,8,10).
  - No existing or pending claim on this cell turned up.

## 5. Neighbouring cells (optional)

- The hosted a28.8.12.4962H code checks out with my own script: 4962 distinct words, min distance 8. Taking the words with a 0 in the best coordinate gives A(27,8,12) ≥ 2847.
- Hosted i28.13 (A(28,8,13) ≥ 6848, group code): my reading of its orbit format expanded to 11640 words with min distance 2, so I misread the format. That number is not used. The table value 6848 alone guarantees only ceil(6848·13/28) = 3180 by averaging.
- Neither neighbour reaches 3374.

## Problems found

None that affect novelty. One procedural note: the unauthenticated GitHub REST API rate-limited (HTTP 403) the second open-PR page and the closed-PR page. I covered the PR check with authenticated read-only search queries instead of retrying those URLs.

## Reasoning

M = 3387 is strictly greater than:
- the live table's lower bound, 3374 (Di), on a page unchanged since the claimant's fetch;
- Echols' 3337;
- every other value I found (none in Lysenstoen or the newer arXiv papers, 2847 from shortening a neighbour);
- every claim in the V3R1T4S repository (none for this cell).

It does not exceed the upper bound 10460 (KT). The mirror cell is the same cell. The size is new.

pass: true
