# CRITERION verdict: constant-weight-codes, cell A(29,6,6)
context: fresh reviewer (new subagent context started for the CRITERION role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:55:53Z

## 1. Bank entry

- Fetched https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json once with curl at 2026-11-27T18:53:50Z: HTTP 200, sha256 7c3942f228807b3bd1eae1b636f557aca64344161137e8bda5566081a6b846a2.
- Exactly one entry has id `constant-weight-codes`. A program compared its fields with the text quoted in the brief:
  - success_criterion equal: True (582 characters both)
  - verification_method equal: True (413 characters both)

## 2. Own all-pairs check (written before reading verify-it-yourself/)

My scratch-folder script `mycheck.py` (standard library only, run with `-I`) reads every non-`#` line of object/A-29-6-6-1207words.txt, requires length 29 and alphabet {0,1}, stores each word as a Python int, asserts `bit_count() == 6` for each, asserts all distinct, and takes the minimum of `(x ^ y).bit_count()` over every pair. Output:

```
sha256 1c25d94ca5861e9762b92ce4dc28d493bf2c2d5827466cb73cdf949c73079642
M 1207
pairs 727821
min_distance 6
weights_ok True distinct True
PASS
```

`shasum -a 256` gives the same hash, matching the brief and INDEX.csv. Distance distribution from a second run of my own code: 6:74765, 8:189907, 10:316695, 12:146454. This matches the distribution printed in RUN_IT_YOURSELF.md. After that I read verify-it-yourself/check_cw.py. It checks the same properties (all pairs, no sampling, d even, lb < M <= ub) and I found no defect in it.

## 3. Brouwer table cell and mirror

- Fetched https://aeb.win.tue.nl/codes/Andw.html once with curl at 2026-11-27T18:53:52Z: HTTP 200, sha256 ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad. This is identical to the sha256 recorded in the-record-we-beat/RECORD.md (fetch 18:39:11Z), so I read the same page content that the claimant read.
- Section "Bounds on A(n,6,w)" has columns w = 4..14. Row n = 29, column w = 6:
  `<td><a href="cwc/d6/a29.6.6.1205H">1205</a><sup>Pil</sup>-1459</td>`
  The separate "Values of A(n,6,6)" table shows the same value for n = 29: `1205<sup>Pil</sup>-1459`.
- Lower bound 1205, upper bound 1459. M = 1207 > 1205 (strict, margin 2) and 1207 <= 1459. d = 6 is even.
- Mirror: A(29,6,23) = A(29,6,6) by complement. The table has no column w = 23 (its columns stop at w = 14 for n = 29, i.e. w <= n/2), so the w = 6 entry is the only entry for that cell. README states the complement cell explicitly and RECORD.md notes that it is not listed separately. The mirror was considered.
- Label Pil: "research group Pilcraft, email 2026-11-21, with 3 new codes" (page line), as the package says.

## 4. arXiv values for the cell

All fetched once each with curl, all HTTP 200:
- arXiv:2608.13906 (Echols, "New lower bounds for constant-weight codes via seeded bit-swap tabu search", v1 14 Aug 2026). I parsed the HTML full text for rows `n d w old new +gain` whose gain equals new - old and found exactly 124 such rows, which matches "124 improved cells". There is no row for (29,6,6) or (29,6,23). Its d = 6 rows with w = 6 are n = 30, 34, 35 only.
- arXiv:2607.19550 (Lysenstoen, v1 21 Jul 2026). The full text names A(18,6,*), A(23..28,6,*) cells only. It has no n = 29 mention at all.
- Newer papers: an arXiv API query (constant-weight / constant weight code(s) in the abstract, newest first, 40 results, fetched 2026-11-27T18:55:16Z) turned up five later papers that could bear on the cell: 2611.24958, 2610.24025, 2611.03682, 2611.26226 and 2611.00173. I searched each one's HTML full text. None gives a value for A(29,6,6) or A(29,6,23). 2611.24958 mentions only A(29,6,5) for n = 29, d = 6. 2610.24025 mentions only A(29,6,9..11).
- So M = 1207 is strictly greater than every value found for this cell in the named and newer arXiv papers (none found). Limit: the search covered arXiv abstracts matching those phrases; it does not prove that no paper anywhere contains the cell.

## 5. Package text

- README "## What", first paragraph (scope sentence): 1207 distinct words, length 29, weight 6, minimum distance 6, the complement cell, more than the lower bound 1205 and not above the upper bound 1459, at the 18:39:11Z fetch. I verified every one of these facts above. The paragraph claims nothing more.
- Other checkable facts I verified: the 727821 pair count, the distance distribution, the sha256 values of the object and the page, the cell text, the Pilcraft label text, and that Echols and Lysenstoen give no value for the cell. I did not fetch the seed code a29.6.6.1205H and did not run rebuild.sh. Those belong to other roles, and the criterion does not need them.
- Credits: the seed code's authors (research group Pilcraft, as credited in the table) are credited. The method authors are credited: Rosin (arXiv:2603.00174 and the CWBC repository, MIT, with how-we-built-it/LICENSE-CWBC included) and Echols for the seeded variant. Brouwer's table is credited.
- Banned words: a grep of all .md and .csv files for solved, first ever, breakthrough, world record, new record, best known, novel and state of the art found none. "optimal" appears only in "Not optimal" disclaimers. "## Not claimed" disclaims optimality, a new method, maximality and a symmetry group, and says the code is not yet in the table.

## Problems found

Neither of these touches the claim or the criterion:
- HOW_WE_FOUND_IT.md (headed "contributor text, unverified") says "2 run(s) of the first pass reached 1207 words". The logs show a chain: one run reached 1206 (seed 1001) and one run reached 1207 (seed 1011). README and COMMANDS.md describe this correctly. The same file's counts of failed runs ("the other 13 runs at 1207 words", the 1208 attempts) cannot be checked from how-we-built-it/logs/original-runs.tsv, which lists only the two successful runs. The wording is loose. It does not overstate the result.
- HOW_WE_FOUND_IT.md refers to "the novelty review in panel/". No panel/ folder is in the package as reviewed. The reference is presumably to reviews still to be added.

## Reasoning

The bank entry's text matches the brief character for character. The object holds 1207 distinct weight-6 words of length 29 with minimum distance 6, checked over all pairs with my own code. The live table cell (the same page bytes the claimant recorded) shows lower bound 1205 and upper bound 1459, so the improvement is strict and within the upper bound. d is even. The mirror cell has no separate entry and was considered. The named arXiv papers and the newer ones found give no value for the cell. The scope sentence states only what was verified, the credits are complete, and no overstated wording is used. Both problems above are in the contributor's search narrative, not the claim.

pass: true
