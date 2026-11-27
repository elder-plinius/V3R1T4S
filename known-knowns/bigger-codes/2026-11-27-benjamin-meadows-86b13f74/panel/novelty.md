# NOVELTY verdict: constant-weight-codes, cell A(25,10,12)
context: fresh reviewer (new subagent context started for the NOVELTY role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:56:49Z

## Claim under review

A(25,10,12) >= 142, object file object/A-25-10-12-142words.txt. The size is new only if 142 is strictly greater than the live Brouwer table lower bound for the cell (and its mirror A(25,10,13)), than any value in arXiv:2608.13906 (Echols), arXiv:2607.19550 (Lysenstoen) or any newer arXiv paper, and not above the upper bound.

## 1. Live Brouwer table

One plain curl request to https://aeb.win.tue.nl/codes/Andw.html; headers and body are in my scratch folder.

| item | value (from command output) |
|---|---|
| HTTP status | 200 |
| Date | Fri, 27 Nov 2026 18:53:42 GMT |
| Last-Modified | Fri, 27 Nov 2026 00:32:42 GMT |
| ETag | "1fe1b-6613732bff19f" |
| Content-Length | 130587 (body on disk: 130587 bytes) |
| sha256 of body | ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad |
| local time of fetch (date -u) | 2026-11-27T18:53:43Z |

The page is byte-identical (same sha256, ETag and Last-Modified) to the copy recorded in the-record-we-beat/RECORD.md.

Cell: section "Bounds on A(n,10,w)" (header columns w = 6..16), row `<th>25</th>`, seventh data cell (w = 12), line 2238 of the page source:

```
<td><a href="cwc/d10/a25.10.12.141H">141</a><sup>E</sup>-433<sup>KT</sup></td>
```

Lower bound 141 (label E), upper bound 433 (label KT). The table prints only w <= n/2, so the mirror cell A(25,10,13) has no separate entry; it is the same cell by complement.

Label E on the page: "William Echols, arXiv:2608.13906 (with 126 new codes) and email 2026-08-08 (with 6 new codes, removing five items from the list of lost codes)." Label KT: Hyun Kwang Kim and Phan Thanh Toan.

Other notes naming this cell: one only, in the note for label Nu (Nurmela, Kaikkonen and Östergård, 1997): "A(25,10,12) >= 132". That is an older, smaller value. No entry for this cell in the lost-codes text (searched the page for `25,10,12`, `25,10,13`, `a25.10.12`, `a25.10.13`).

## 2. arXiv papers

- arXiv:2608.13906 (Echols, v1 14 Aug 2026, only version): Table 1 row `| 25 | 10 | 12 | 137 | 141 | +4 |`, i.e. 141. The paper points to the repository williamechols/cwc-seeded-tabu-search; its file tree (GitHub API, HTTP 200, 140 paths, not truncated) holds `codes/25_10_12_141.txt` and no larger file for this cell.
- arXiv:2607.19550 (Lysenstoen, v1 21 Jul 2026, only version): the paper is about d = 6 cells (A(23,6,10), A(24,6,10), A(23,6,11), A(24,6,8)); no value for A(25,10,12) or A(25,10,13) in the abstract or HTML text.
- Newer papers: arXiv full-text searches for "constant weight codes" and "constant-weight code", sorted newest first, returned the same 2026 list. Relevant newer lower-bound papers checked:
  - arXiv:2611.24958 (Iskandar, 10 Nov 2026): 13 cells, all d = 4 or d = 6; none is this cell.
  - arXiv:2610.24025 (16 Oct 2026): A(n,6,w) cells only.
  - arXiv:2611.03682 (22 Oct 2026): kissing numbers via A(n,8,8) codes; not this cell.
  - arXiv:2611.00173: an upper bound for A(19,6,8); not this cell.
- Papers citing Echols (Semantic Scholar citations API, HTTP 200): 2611.24958, 2611.03682, 2610.24025, 2609.35051 (kissing numbers, abstract names no A(25,10,12) value). None lists a value for this cell.

## 3. V3R1T4S repository (main branch and pull requests)

- TROPHY_CASE.md (raw.githubusercontent.com, HTTP 200, 100 lines) and known-knowns/bigger-codes/INDEX.csv (HTTP 200, 30 data rows): no entry for A(25,10,12) or A(25,10,13); the constant-weight cells listed are all d = 6 or d = 8.
- Pull requests: GitHub API `pulls?state=all&per_page=100`, pages 1 to 13, all HTTP 200, 1203 pull requests in total (numbers 1 to 1258). A regex over titles and bodies for 25,10,12 / 25,10,13 in any separator found none. The only constant-weight pull requests with d = 10 in the title are 348 to 351 (Delsarte LP upper bounds for A(31,10,7), A(32,10,7), A(33,10,7), A(34,10,8)). The API rate limit for my address reached 0 on page 13, the last page (3 items), so the listing is complete.

## 4. Neighbouring hosted codes (optional check)

Downloaded once each: cwc/d10/a26.10.13.234H and cwc/d10/a26.10.12.213H (both HTTP 200). My script checked both (sizes 234 and 213, weights, distinctness, minimum distance >= 10) and took, for every coordinate, the shortened length-25 subcode:

```
dl/a26.10.13.234H size 234 valid; best shortened length-25 subcodes by weight: {12: 118, 13: 118}
dl/a26.10.12.213H size 213 valid; best shortened length-25 subcodes by weight: {11: 100, 12: 117}
```

The largest value these imply for A(25,10,12) = A(25,10,13) is 118, below 141.

## Object size

I wrote my own check from the definition before opening anything in verify-it-yourself/ (I did not open that folder at all). Output:

```
86b13f74de60c58c60f8255a4ced73ad9a126038dc79c543021b55b5159bc658  object/A-25-10-12-142words.txt
M 142 distinct 142 min distance 10 pairs 10011
```

All 142 words have length 25 and weight 12. The sha256 matches the claim.

## Problems found

None. The README says the table credits Echols with "126 new codes" while the Echols abstract says 124; the table's own note reads "with 126 new codes", so the package quotes the table correctly. This does not affect novelty.

## Reasoning

The largest published value I found for A(25,10,12) / A(25,10,13) is 141: the live table (fetched 2026-11-27, Last-Modified the same day), Echols' paper and his code repository. Lysenstoen gives no value for the cell; no newer arXiv paper or paper citing Echols lists one; the V3R1T4S repository has no merged entry or pull request for it; neighbouring hosted codes imply at most 118. 142 is strictly greater than 141 and does not exceed the upper bound 433.

pass: true
