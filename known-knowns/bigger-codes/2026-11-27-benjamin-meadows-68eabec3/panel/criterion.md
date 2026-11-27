# CRITERION verdict: constant-weight-codes, cell A(27,8,8)
context: fresh reviewer (new subagent context started for the CRITERION role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:56:07Z

## 1. Bank entry versus the quoted criterion

- Fetched https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json once at 2026-11-27T18:53:45Z: HTTP 200, sha256 7c3942f228807b3bd1eae1b636f557aca64344161137e8bda5566081a6b846a2.
- Exactly one entry with id constant-weight-codes. I extracted the two quoted paragraphs from the review brief by program (the lines starting with `> `) and compared them with the entry's fields as strings:
  - success_criterion equal: True (582 characters each)
  - verification_method equal: True (413 characters each)

## 2. Own all-pairs check of the object

Written from the verification method before I opened verify-it-yourself/ (script in my scratch folder: words parsed as Python ints from the 0/1 rows, popcount via bin().count, every pair i<j checked).

```
sha256 68eabec3d2808175e4f0f8db629c0b6137d8ab94b19e8e24e23186b03f6bc26f
header lines 1 data lines 778
M 778 pairs 302253 min distance 8 dist {8: 90546, 10: 19328, 12: 161656, 14: 18110, 16: 12613}
ALL OK
```

Every row has length 27 and alphabet {0,1}; every word has weight 8; all 778 words are distinct; the minimum distance is 8 (d = 8 is even). The sha256 matches the claim and INDEX.csv. Afterwards I ran the claimant's verify-it-yourself/check_cw.py: its output (pairs, distance distribution, minimum 8, PASS) matches mine. That checker takes the table bounds as arguments and does not re-fetch the table; the re-fetch the method requires was done by me (section 3).

## 3. The table cell and its mirror

Fetched https://aeb.win.tue.nl/codes/Andw.html once with curl at 2026-11-27T18:53:47Z: HTTP 200, sha256 ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad, Last-Modified Fri, 27 Nov 2026 00:32:42 GMT, ETag "1fe1b-6613732bff19f", Content-Length 130587. The sha256 is identical to the one recorded in the-record-we-beat/RECORD.md, so the page has not changed since the claimant's fetch.

In section "Bounds on A(n,8,w)" (header columns n\w 5 6 7 8 9 10 11 12 13 14), row n = 27, column w = 8:

```
<a href="cwc/d8/a27.8.8.777H">777</a><sup>Di</sup>-1252
```

Lower bound 777 (label Di = "Kerem Dilker, email 2026-11-26 with 31 new bounds"), upper bound 1252. 778 > 777 (strict, margin 1) and 778 <= 1252. Mirror cell: A(27,8,19); the table's rows for n = 27 only run to w = 14, so w = 19 is not listed and is represented by the same w = 8 cell under complement. Mirror considered: yes, no separate higher value exists on the page.

## 4. arXiv papers named in the criterion, and newer ones

- arXiv:2608.13906 (Echols, "New lower bounds for constant-weight codes via seeded bit-swap tabu search", HTTP 200 abstract and HTML): Table 1 row `27 8 8 769 775 +6`, so the paper's value is 775 < 778. No row for (27,8,19).
- arXiv:2607.19550 (Lysenstøen, HTTP 200 abstract and HTML): abstract gives A(23,6,10), A(24,6,10), A(23,6,11), A(24,6,8) only; the HTML body contains no (27,8,8) or (27,8,19) cell.
- Newer papers: two arXiv API queries (HTTP 200 each), sorted by submission date: "constant weight codes" / "constant-weight codes", and abstracts containing "Brouwer" and "weight". Relevant newer binary constant-weight papers found: 2610.24025 (d = 6 cells only), 2611.00173 (upper bound for A(19,6,8) only), 2611.24958 (thirteen cells; its Table 1 lists d = 4 and d = 6 cells only, none with n = 27, d = 8). 2611.26226 is about q >= 3. None gives a value for A(27,8,8) or A(27,8,19).

So 778 is strictly greater than every value found for this cell.

## 5. Package text against what is established

- Scope sentence (first paragraph under "## What"): 778 distinct words, length 27, weight 8, minimum distance 8, A(27,8,19) by complement, exceeds lower bound 777, not above upper bound 1252, table fetched 2026-11-27T18:39:11Z. Every part is confirmed by sections 2 and 3. It claims nothing beyond that.
- Other checkable facts: 302253 pairs (= 778*777/2) and the distance distribution in RUN_IT_YOURSELF.md match my output. Echols's 775 and "Lysenstoen lists no value" are true (section 4). The Last-Modified header, ETag, Content-Length and page sha256 in RECORD.md match my fetch. The seed URL https://aeb.win.tue.nl/codes/cwc/d8/a27.8.8.777H is the link in the cell; my one fetch of it (HTTP 200) gave sha256 b342cddfbbf96828dff9f5763b2d63138af014c7d0f94e8a41197dd88cd01868 and Last-Modified Thu, 26 Nov 2026 20:15:24 GMT, as RECORD.md states; it holds 777 weight-8 words, 651 of which appear unchanged in the object, which fits the described local search (start from the seed, then move bits).
- Credits: Brouwer (table and hosted seed), Kerem Dilker (seed code author, as the table credits it), Christopher D. Rosin (arXiv:2603.00174, abstract HTTP 200, author "Rosin, Christopher D."; CWBC repository page HTTP 200, shows MIT License), William Echols (arXiv author "Echols, William") for the seeded variant, Christian Lysenstøen (arXiv author "Lysenstoeen, Christian"). Seed author and method authors are credited.
- "## Not claimed" correctly disclaims optimality, maximality, symmetry, a new method, and table inclusion.
- A word scan of README.md, RUN_IT_YOURSELF.md, HOW_WE_FOUND_IT.md, the-record-we-beat/RECORD.md and the object's header for solved, first ever, breakthrough, world record, new record, unprecedented returned no matches.

## Problems found

None material. Two minor notes, neither affecting the claim:
- HOW_WE_FOUND_IT.md (marked "contributor text, unverified") mentions six other runs at 778 and twenty at 779, but how-we-built-it/logs/original-runs.tsv records only the one successful run (seed 1005, 55.1 CPU s, 7029649 steps), so those counts can't be checked from the package. They are not part of the scope sentence.
- README's construction paragraph says the program "keeps the 777 seed words" and then moves bits; the final object keeps 651 of them. Read as a description of the starting state, this is accurate.

## Reasoning

The bank text matches the brief exactly. The object meets every clause of the success criterion: an explicit list of M = 778 distinct weight-8 vectors of length 27, all 302253 pairwise distances >= 8 with d even. M is strictly greater than the lower bound 777 that the live table showed when I checked, and not above the upper bound 1252. The mirror cell was considered. M is also strictly greater than Echols's 775, and neither Lysenstøen nor any newer arXiv paper I found gives a value for this cell. The package's scope sentence and stated facts are true, credits are complete, and none of the banned words appear.

pass: true
