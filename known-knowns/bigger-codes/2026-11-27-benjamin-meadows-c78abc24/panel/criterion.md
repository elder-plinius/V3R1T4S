# CRITERION verdict: constant-weight-codes, cell A(26,10,12)
context: fresh reviewer (new subagent context started for the CRITERION role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:55:59Z

## 1. Bank entry

- Fetched https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json once at 2026-11-27T18:53:42Z, HTTP 200, sha256 7c3942f228807b3bd1eae1b636f557aca64344161137e8bda5566081a6b846a2.
- A script in my scratch folder walked the JSON, found exactly 1 object with id constant-weight-codes, and compared its fields with the text quoted in the brief using Python string equality:
  - `success_criterion equal: True`
  - `verification_method equal: True`

## 2. Independent all-pairs check

I wrote this check from the bank's verification method before opening verify-it-yourself/. It stores each word as a Python int, asserts popcount == 12 for every word, asserts all words are distinct, and computes popcount(x ^ y) for every pair. Output on object/A-26-10-12-214words.txt:

```
sha256 c78abc24b831d29945e88f58953941927761132fa60f8a2cd2696a5dcec81715
header lines 1 body lines 214
M 214 pairs 22791 min distance 10 pairs below d 0
all weights 12 distinct True PASS
```

Distance distribution, from my own count: [(10, 5210), (12, 8756), (14, 2712), (16, 4676), (18, 1425), (20, 12)]. This matches the distribution in RUN_IT_YOURSELF.md exactly. Only after this did I read verify-it-yourself/check_cw.py. It checks the same properties (length, alphabet, weight, distinctness, all pairs, d even, lb < M <= ub).

## 3. Table cell, live

- Fetched https://aeb.win.tue.nl/codes/Andw.html once with curl at 2026-11-27T18:53:44Z, HTTP 200, sha256 ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad. That is the same sha256 RECORD.md gives for the claimant's fetch, so the page has not changed since then.
- In section "Bounds on A(n,10,w)" the header columns are w = 6..16. Row 26 holds 8 cells (w = 6..13): 13, 30-36, 68, 91-213, 130-397, 168-565, **213-691**, 234-754. The w = 12 cell in the page source is `<td><a href="cwc/d10/a26.10.12.213H">213</a><sup>Bol</sup>-691<sup>KT</sup>`. Its link names a26.10.12, and the neighbouring cells link i26.11 and a26.10.13, which confirms the column.
- Lower bound 213 (Bol: "Ignacio Bolívar, email 2026-11-09 with A(26,10,12) ≥ 213, ..."), upper bound 691 (KT: Kim & Toan, arXiv:1212.3467).
- Mirror cell A(26,10,14): row 26 stops at w = 13 = n/2, so the table prints no separate w = 14 cell, and complement symmetry makes it the same cell. I considered the mirror, and it gives no larger value.
- 214 > 213 holds strictly, 214 <= 691, and d = 10 is even.

## 3b. arXiv papers named in the criterion, and newer ones

- arXiv:2608.13906 (Echols, v1, 2026-08-14): HTTP 200 on abs and html. I parsed Table 1 into 124 rows. Its d = 10 rows near n = 26 are (26,10,8), (27,10,8), (25,10,12), (26,10,13) and (27,10,13). It has no (26,10,12) or (26,10,14) row.
- arXiv:2607.19550 (Lysenstoeen, v1, 2026-07-21): HTTP 200. Every A(n,d,w) it mentions has d = 6. It has no value for this cell.
- Newer papers: one arXiv API query for "constant weight codes", sorted by date (https, HTTP 200), returned two relevant papers after August. arXiv:2610.24025 mentions only d = 6 and d = 8 cells. arXiv:2611.24958 lists 13 cells, all with d = 4 or 6. Neither has a value for A(26,10,12) or A(26,10,14).

The strict improvement therefore holds against the table, against both named papers, and against the newer arXiv papers I found.

## 4. Package text

- Scope sentence (README "## What", first paragraph): 214 distinct words, length 26, weight 12, minimum distance 10, the complement cell, lower bound 213 and upper bound 691 at the 18:39:11Z fetch. My checks confirm every part of it, and it claims nothing beyond the object and the cell. "22791 pairs" is correct. "88 CPU seconds" is 87.8 rounded, as in how-we-built-it/COMMANDS.md.
- RECORD.md: the cell source, the labels Bol and KT, the seed URL and the seed sha256 all match my fetches. I fetched the seed at 2026-11-27T18:55:30Z: HTTP 200, sha256 662ef208b5b79c7dd842e717caf9fa298cb1f217b9bdcbad433a0cfc363199d4, Last-Modified Mon, 09 Nov 2026 17:25:20 GMT, 213 distinct weight-12 words.
- Credits: the seed's author (Ignacio Bolívar, as credited in the table), Brouwer's table, Rosin (the bit-swap tabu method, arXiv:2603.00174, whose title and author I confirmed on its abs page, plus the CWBC repo, whose MIT notice ships as how-we-built-it/LICENSE-CWBC), Echols (the seeded variant), Lysenstøen, and the contributor. The seed author and the method authors are all credited.
- A grep for solved, first ever, breakthrough, world record, unprecedented and novel found none of these words in README.md, HOW_WE_FOUND_IT.md, RUN_IT_YOURSELF.md or RECORD.md. "## Not claimed" correctly disclaims optimality, maximality, a new method and a symmetry group.

## Problems found

None material to the criterion. Two small imprecisions:

1. The README says "The program keeps the 213 seed words, adds one word ... and then repeatedly moves one 1 to a 0 position". My comparison of the object with the hosted seed (bit order most-significant first) shows the final code contains 178 of the 213 seed words: 36 words in the object are not in the seed, and 35 seed words are missing from it. Read in order, the sentence describes the starting state, and later moves do change seed words, but a reader could take "keeps" to mean that all 213 survive. Wording like "starts from the 213 seed words ... the final code shares 178 of them" would be exact. This does not change the claimed result.
2. HOW_WE_FOUND_IT.md (labelled "contributor text, unverified") says the first pass ran seeds 1001 to 1020 and that "the other 8 runs at 214 words" failed. That totals 9 runs, not 20. Also, how-we-built-it/logs/original-runs.tsv lists only the one successful run, although COMMANDS.md says it "lists them". The text is labelled unverified, and the claim does not depend on it.

## Reasoning

The object is an explicit list of 214 distinct length-26 weight-12 binary vectors with all pairwise distances >= 10, where d = 10 is even. My own check confirms this. 214 is strictly greater than the lower bound 213 shown today in the (26,10,12) cell of Andw.html, and that page is byte-identical to the claimant's fetch. The mirror cell is the same cell under the table's w <= n/2 convention. 214 does not exceed the upper bound 691. Neither Echols, Lysenstoen nor the newer arXiv papers I found give a value for this cell. The bank text matches the brief exactly. The scope sentence claims no more than the checks establish, credits are complete, and none of the barred words appear. Both imprecisions are in method narrative, not in the claim.

pass: true
