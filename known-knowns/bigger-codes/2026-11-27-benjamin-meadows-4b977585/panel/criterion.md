# CRITERION verdict: constant-weight-codes, cell A(27,8,12)
context: fresh reviewer (new subagent context started for the CRITERION role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:56:31Z

## 1. Bank entry

- Fetched https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json once at 2026-11-27T18:53:58Z: HTTP 200, sha256 7c3942f228807b3bd1eae1b636f557aca64344161137e8bda5566081a6b846a2.
- Found exactly 1 entry with id `constant-weight-codes`. A script compared its `success_criterion` and `verification_method` with the text quoted in my brief, character by character:
  - `success_criterion identical: True len 582 582`
  - `verification_method identical: True len 413 413`

## 2. Own all-pairs check (written before reading verify-it-yourself/)

I wrote my checker in my scratch folder from the verification method, before opening verify-it-yourself/. It parses each 27-character 0/1 line as a Python int and skips the `#` header line. It asserts that every word has popcount 12 and that all words are distinct, then computes popcount(x ^ y) for all 5734191 pairs (3387·3386/2) and takes the minimum.

- `shasum -a 256 object/A-27-8-12-3387words.txt` gives 4b977585972408991e43784ce2f81591c529d9f3a9d770ee9fc4262eb056e3ba, which matches the brief and INDEX.csv.
- Output: `M 3387 min_distance 8 all_weight 12 distinct True pass True`

## 3. Table cell, live

- Fetched https://aeb.win.tue.nl/codes/Andw.html once with curl at 2026-11-27T18:54:00Z: HTTP 200, 130587 bytes, sha256 ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad. This is the same page hash that the-record-we-beat/RECORD.md gives for the claimant's fetch.
- Section "Bounds on A(n,8,w)", columns w = 5..14, row 27, column w = 12:
  `<td><a href="cwc/d8/a27.8.12.3374H">3374</a><sup>Di</sup>-10460<sup>KT</sup></td>`
- Lower bound 3374 (label Di = "Kerem Dilker, email 2026-11-26 with 31 new bounds."), upper bound 10460 (label KT = Kim & Toan, arXiv:1212.3467).
- 3387 > 3374 (strict, margin 13). 3387 <= 10460. d = 8 is even.
- Mirror cell A(27,8,15): the table lists only w <= 13 for n = 27 (w <= n/2), so A(27,8,15) is this same cell. The mirror is covered.

## 4. arXiv comparison (part of the criterion)

- arXiv:2608.13906 (Echols; HTML fetched at 2026-11-27T18:54:53Z, HTTP 200): its table row reads `27 8 12 3335 3337 +2`, so this paper gives 3337 for the cell. 3387 > 3337. This matches the README's "Echols lists 3337".
- arXiv:2607.19550 (Lysenstoen; abstract and HTML fetched, HTTP 200): every cell it names has d = 6 (A(18,6,*), A(23..28,6,*)). It has no value for A(27,8,12), which matches the README.
- Newer papers: one arXiv API query (title/abstract "constant weight"/"constant-weight", newest first, HTTP 200, entries through 2026-11-23) turned up four relevant papers. I fetched each HTML version (HTTP 200) and searched it for the cell:
  - 2611.24958 (Iskandar, thirteen cyclic codes): 13 cells, none with n = 27, d = 8.
  - 2610.24025 (prescribed-automorphism search): its n = 27 cells are all d = 6.
  - 2611.03682 (kissing numbers): w = d = 8 only.
  - 2608.20287 (Honeycomb framework): no A(27,8,12) value.
- No paper found gives a value of 3387 or more for this cell. Limit of this check: papers posted in the last few days may not be indexed by the API yet.

## 5. Package statements

I checked these against the object or live pages, and each is true:

- 3387 distinct words, length 27, weight 12, minimum distance 8. The complement statement for A(27,8,15) is correct.
- Bounds 3374 and 10460, and the table's Last-Modified date and page sha256, as recorded in RECORD.md (my page hash is identical).
- The seed URL serves 3374 weight-12 words (fetched at 2026-11-27T18:56:00Z, HTTP 200). Its sha256 is 91aff7ff2e09ed7449bd464412f5ceba1e37e02d5d2f08fc46ee89d835baf7a6, its Content-Length is 27001 and its Last-Modified is Thu, 26 Nov 2026 20:15:24 GMT, all matching RECORD.md. 2699 of the object's words occur in the seed, which fits the README's description: the search keeps the previous words and then moves bits inside words.
- Credit to Dilker matches the Di label. The pair count 5734191 is correct.
- Credits: the seed code's author (Kerem Dilker, as the table credits him) and the table (A. E. Brouwer) are credited. The method's authors are credited: Christopher D. Rosin, arXiv:2603.00174, whose abs page confirms the title "Automated Discovery of Improved Constant Weight Binary Codes" and Rosin as author; how-we-built-it/LICENSE-CWBC is the MIT notice for Rosin's code. William Echols is credited for the seeded variant.
- Scope sentence (first paragraph under "## What"): it claims only a 3387-word code for this cell (and its complement), compared with the table at a stated fetch time. That is exactly what I established.
- "## Not claimed" disclaims optimality, a new method, maximality and other cells.
- None of "solved", "first ever", "breakthrough" or "world record" appears in README.md, HOW_WE_FOUND_IT.md or RUN_IT_YOURSELF.md. "record" appears only in "as recorded in RECORD.md" and the folder name the-record-we-beat.

## Problems found

None that are material. Minor points that do not change the verdict:
- HOW_WE_FOUND_IT.md refers to "the novelty review in panel/", but the package has no panel/ folder at review time. This points to panel output still to come.
- HOW_WE_FOUND_IT.md says "13 run(s) of the first pass reached 3387 words". This could be misread as 13 independent runs each reaching 3387. The README makes it clear these are 13 chained runs adding one word each.
- verify-it-yourself/run_checks.sh compares against hard-coded bounds (3374, 10460) rather than re-fetching the table. The verification method's re-fetch was done in this review (section 3).

## Reasoning

Every clause of the bank criterion holds for this object:
- an explicit list of M = 3387 distinct weight-12 length-27 vectors with all pairwise distances >= 8, d even;
- M strictly greater than the live table's lower bound 3374, with the mirror cell considered;
- M strictly greater than the Echols value 3337 and greater than any value in Lysenstoen (none) or the newer arXiv papers found (none for this cell);
- M not above the upper bound 10460.

The verification was done by an independent script with Python ints and popcount, plus a fresh fetch of the table. The package's claims match what was established and overstate nothing material.

pass: true
