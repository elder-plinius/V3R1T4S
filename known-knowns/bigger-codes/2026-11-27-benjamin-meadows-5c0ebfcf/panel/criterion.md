# CRITERION verdict: constant-weight-codes, cell A(29,10,8)
context: fresh reviewer (new subagent context started for the CRITERION role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:56:19Z

## 1. Bank entry

- Fetched https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json once with plain curl at 2026-11-27T18:53:42Z: HTTP 200, sha256 7c3942f228807b3bd1eae1b636f557aca64344161137e8bda5566081a6b846a2.
- Exactly one entry with id `constant-weight-codes` (`found 1`). A Python script in my scratch folder compared its `success_criterion` and `verification_method` strings with the text quoted in my brief, by exact string equality:
  - `success_criterion equal 582 582`
  - `verification_method equal 413 413`
- So the criterion I judge against is the live bank text, character for character.

## 2. My own all-pairs check (written from the verification method before I read verify-it-yourself/)

- Object: object/A-29-10-8-98words.txt, sha256 `5c0ebfcf58bd20ac9e89c62b10560e485e9a416bf027df1dd4c680feaf3354ee` (shasum -a 256). This matches the README, INDEX.csv and the brief.
- The script skips the one `#` header line, checks that every other line is 29 characters of 0/1, turns each word into a Python int, and checks popcount == 8 for each word, that all words are distinct, and popcount(x ^ y) over all pairs.
- Output: `M 98 min_dist 10 pairs 4753 pass True`.
- Distance distribution: 10:2327, 12:1315, 14:714, 16:397. This matches the distribution printed in RUN_IT_YOURSELF.md.
- Complement check: all 98 complemented words have weight 21 and minimum distance 10, so A(29,10,21) >= 98 also holds.
- After my own checks I ran the claimant's verify-it-yourself/check_cw.py read-only. It printed the same sha256, 4753 pairs, the same distribution, minimum distance 10, and `PASS` (exit 0). I did not run planted_bugs.py or run_checks.sh, because they may write files into the package.

## 3. Brouwer table cell

- Fetched https://aeb.win.tue.nl/codes/Andw.html once with plain curl at 2026-11-27T18:53:44Z: HTTP 200, 130587 bytes, sha256 `ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad`. This is byte-identical to the page recorded in the-record-we-beat/RECORD.md, which has the same sha256 and Content-Length.
- In the section "Bounds on A(n,10,w)" the columns are w = 6..16. Row n = 29 reads `20`, `42-66`, then for w = 8: `<td><a href="cwc/d10/a29.10.8.96">96</a><sup>E</sup>-203</td>`. The lower bound is 96 and the upper bound is 203. The separate "Values of A(n,10,8)" table also lists `96-203` for n = 29.
- Mirror cell: the table only lists w <= 16, and 21 > n/2. Under complement symmetry A(29,10,21) = A(29,10,8), so the mirror is this same cell and has no separate, larger entry. The package considers this explicitly in README and RECORD.md.
- d = 10 is even. 96 < 98 <= 203, so M is strictly greater than the lower bound and does not exceed the upper bound.
- Seed code https://aeb.win.tue.nl/codes/cwc/d10/a29.10.8.96, fetched once at 2026-11-27T18:55:16Z: HTTP 200, Content-Length 2880, Last-Modified Sun, 02 Aug 2026 11:05:44 GMT, sha256 `71b98dcc2ed90dabffe98c800d42162e852cc0babe8511ae3b60897a16f7e26b`. All of these match RECORD.md and RUN_IT_YOURSELF.md. The seed is a valid code: 96 distinct weight-8 words, minimum distance 10.

## 4. arXiv papers named in the criterion, and newer ones

- arXiv:2608.13906 (Echols), abstract page and HTML v1, read with `seek read` at 18:54:24Z and 18:54:31Z. It has one version only (v1, 14 Aug 2026), and the abstract says 124 new constructions. Its table row reads `| 29 | 10 | 8 | 91 | 96 | +5 |`, so Echols gives 96 for this cell. There is no w = 21 row. 98 > 96.
- arXiv:2607.19550 (Lysenstøen), abstract read at 18:54:38Z. It covers A(23,6,10), A(24,6,10), A(23,6,11) and A(24,6,8), all with d = 6. It gives no value for A(29,10,8).
- Newer papers: I sent one query to the arXiv API (https, HTTP 200 at 18:54:51Z; an earlier http request answered 301 and returned nothing). The query was "constant weight codes" OR "constant-weight codes", sorted by submission date. Results newer than 2608.13906 that improve constant-weight lower bounds:
  - 2610.24025 (abstract): d = 6 cells only.
  - 2611.03682 (abstract): codes of weight 8 and distance 8.
  - 2611.24958 (HTML v1): 13 cells, all with d = 4 or d = 6.
  - None of these lists A(29,10,8). The other recent results (2611.00173 is an upper bound for A(19,6,8), 2609.23869 is nonbinary, the others are designs and theory) do not touch this cell.
- Limit: this is a keyword search of arXiv. A paper that never uses either phrase would not be found. Within that limit, no arXiv value for the cell is 98 or more.

## 5. Package statements

- Scope sentence (first paragraph under "## What"): 98 distinct words, length 29, weight 8, minimum distance 10, A(29,10,21) >= 98 by complement, more than lower bound 96, not more than upper bound 203, table fetched at 2026-11-27T18:39:11Z. I verified every element of this sentence, and it claims nothing beyond them.
- "## Compared to":
  - Last-Modified and the bounds are consistent with my fetch, which has the same sha256.
  - "The table credits the lower bound 96 to William Echols, arXiv:2608.13906 (with 126 new codes)" quotes the table's source entry E word for word. The abstract's own count is 124, which is the count the bank text uses. The README attributes the 126 to the table, so this is accurate.
  - "Echols lists 96 for this cell" is true. "Lysenstoen lists no value for it" is true.
- "## Not claimed": it disclaims optimality, maximality, a new method and a symmetry group, and it says the code is not yet in the table. All of these are consistent with what I observed. The live cell still shows 96.
- "## Credits":
  - Brouwer is credited for the table and the hosted seed.
  - Echols is credited for the 96-word seed code and the seeded variant.
  - Rosin is credited for the bit-swap tabu search (arXiv:2603.00174, CWBC repository, MIT licence; how-we-built-it/LICENSE-CWBC carries the MIT notice "Copyright (c) 2026 Christopher Rosin").
  - Lysenstøen is credited as compared against.
  - So the seed code's author and the method's authors are all credited.
- Run figures: COMMANDS.md and logs/original-runs.tsv record 64.8 + 84.8 = 149.6 CPU s for seeds 1011 and 1001. The README's "150 CPU seconds" is a rounding of this.
- Wording check: a grep of the package's .md, .txt, .csv, .py and .sh files for solved / first ever / breakthrough / world record / new record / unprecedented / record-breaking finds none. The only hits for "optimal" are in "Not optimal" disclaimers. The folder name "the-record-we-beat" is a title for the table snapshot, not a "world record" claim.

## Problems found

None material. Two minor wording points that do not affect the criterion:
- README says each run "keeps the words of the previous code, adds one word ... and then repeatedly moves one 1 to a 0 position inside a word". Only 54 of the 96 seed words appear unchanged in the final object; the other 42 were changed by the search. The same sentence goes on to describe moves inside words, and "Not claimed" calls the code a local-search improvement of the seed, so nothing is overstated. "Starts from the words" would be more exact than "keeps".
- HOW_WE_FOUND_IT.md refers to "the novelty review in panel/", but there is no panel/ folder in the package as I received it. This is a forward reference, not a claim about the object.

## Reasoning

Every clause of the bank criterion holds for this object and cell:
- It is an explicit list of 98 distinct length-29 weight-8 vectors.
- All 4753 pairwise distances are >= 10, and d is even.
- 98 is strictly greater than the lower bound of 96 shown in the live table at check time; the page is byte-identical to the claimant's snapshot.
- The mirror cell under complement is the same cell.
- 98 is strictly greater than Echols's 96. Lysenstøen and the newer arXiv papers I found give no value for the cell.
- 98 does not exceed the upper bound of 203.

The package's scope sentence and its other checkable statements are true. Credits are complete, and no banned superlatives are used.

pass: true
