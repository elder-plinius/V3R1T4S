# CRITERION verdict: constant-weight-codes, cell A(25,10,12)
context: fresh reviewer (new subagent context started for the CRITERION role only; saw only the claim package and public pages; no access to other reviewers' files)
verdict_utc: 2026-11-27T18:56:13Z

## 1. Bank entry

- Fetched https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json once at 2026-11-27T18:53:43Z, HTTP 200, sha256 7c3942f228807b3bd1eae1b636f557aca64344161137e8bda5566081a6b846a2.
- Exactly one entry with id `constant-weight-codes`. A script in my scratch folder compared its `success_criterion` and `verification_method` fields with the text quoted in the review brief: `success_criterion exact_equal= True len 582 582`, `verification_method exact_equal= True len 413 413`. The brief quotes the live bank text exactly.

## 2. My own all-pairs check

I wrote this check from the verification method before I opened the claimant's checker in verify-it-yourself/. It is a standard-library script that reads each non-comment line as a Python int, asserts length 25 and the 0/1 alphabet, asserts popcount == 12 for every word, asserts all words are distinct, and computes popcount(x ^ y) for all pairs.

```
sha256 86b13f74de60c58c60f8255a4ced73ad9a126038dc79c543021b55b5159bc658
M 142 min_distance 10 pairs 10011 ok True
```

- The sha256 matches the brief and INDEX.csv.
- Distance distribution: [(10, 3930), (12, 1972), (14, 2596), (16, 1119), (18, 367), (20, 26), (22, 1)]. This matches the expected output in RUN_IT_YOURSELF.md.
- Mutation check: I made a copy with one word replaced by a duplicate of another, and my script rejected it (`AssertionError: dup`, exit 1).
- After my own check, I ran the claimant's verify-it-yourself/check_cw.py. It also ended `PASS` with minimum distance 10.

## 3. Brouwer table, cell and mirror

- Fetched https://aeb.win.tue.nl/codes/Andw.html once with curl at 2026-11-27T18:54:06Z: HTTP 200, 130587 bytes, sha256 ad1196547427dbaa0ee7eb1970c445d4d7f4890c39860ebd8433bc9df6ceefad. That is the same sha256 RECORD.md gives for the claimant's 18:39:11Z fetch, so the page has not changed since then.
- Section "Bounds on A(n,10,w)": the column headers are 6 to 16. My parser read row n=25 as w=6:10, w=7:28-32, w=8:51-75, w=9:75-157, w=10:100-262, w=11:125-379, w=12:141-433. The raw cell is `<td><a href="cwc/d10/a25.10.12.141H">141</a><sup>E</sup>-433<sup>KT</sup></td>`. The file link name a25.10.12 confirms the column alignment.
- Lower bound 141. 142 > 141, which holds strictly. Upper bound 433. 142 <= 433, so the upper bound is not exceeded. d = 10 is even.
- Mirror cell: the n=25 row stops at w=12 = floor(25/2), so A(25,10,13) has no cell of its own and is the same cell by complement symmetry. The package states this in both README.md and RECORD.md.
- Label E on the page reads "William Echols, arXiv:2608.13906 (with 126 new codes) and email 2026-08-08 (with 6 new codes ...)". Label KT reads "Hyun Kwang Kim & Phan Thanh Toan, arXiv:1212.3467v1". Both match RECORD.md.
- I fetched the hosted seed https://aeb.win.tue.nl/codes/cwc/d10/a25.10.12.141H once (HTTP 200). Its sha256 is 71f7603eac9ee759f07696eb2741dcb9b159503eee639f13a28bfd66493a4a97, the same as in RECORD.md. It holds 141 words, all of weight 12.

## 3b. arXiv papers named in the criterion, and newer ones

- arXiv:2608.13906 (William Echols, submitted 14 Aug 2026, v1; abs and HTML both HTTP 200). Its Table 1 row for this cell reads `25 10 12 137 141 +4`, so the paper's value is 141 and 142 beats it. The paper's own count is "124 new constructions". The README's "126 new codes" is a quotation of the table's label E, so it is accurate as a quote.
- arXiv:2607.19550 (Christian Lysenstoeen, 21 Jul 2026; HTTP 200). Neither the text nor the tables contain any A(25,...) value with d=10. The README's statement that it "lists no value for it" is true.
- Newer arXiv papers: I ran one arXiv API query (all:"constant weight codes", newest first; HTTP 200 after one 301 redirect to https). Two newer papers give lower bounds:
  - arXiv:2610.24025 (prescribed-automorphism search). All its cells are d=6 or d=8.
  - arXiv:2611.24958 (thirteen improved codes, cyclic orbit certificates). All its rows are d=4 or d=6.
  - Neither paper has a d=10 cell. No arXiv value found exceeds 141 for this cell.
- arXiv:2603.00174 (Christopher D. Rosin, "Automated Discovery of Improved Constant Weight Binary Codes", HTTP 200) exists as credited.

## 4. Package statements

- Scope sentence (first paragraph under "## What"). Each part is true against the object and the live page: 142 distinct words, length 25, weight 12, minimum distance 10, the complement cell, lower bound 141, upper bound 433, and the fetch time. It claims nothing beyond the strict improvement in this one cell.
- "## Not claimed" disclaims optimality, other cells, a new method, maximality and table inclusion. All of these disclaimers are appropriate.
- Credits:
  - Brouwer (the table and the hosted seed).
  - William Echols, as author of the seed code and of the seeded variant of the method. The table's label E confirms that the seed is his.
  - Christopher D. Rosin (arXiv:2603.00174, and the CWBC repository with its MIT licence; the licence text is included as how-we-built-it/LICENSE-CWBC with the Rosin copyright line).
  - Lysenstøen.
  - The seed code's author and the method's authors are all credited.
- Forbidden words: a grep of the package's .md, .txt, .csv, .sh and .py files for solved, first ever, breakthrough, world record, unprecedented and optimal found only the two "Not optimal" disclaimers.
- HOW_WE_FOUND_IT.md is labelled as unverified contributor text and makes no claim beyond the scope sentence.
- One minor wording point, not material to the criterion. README.md says the program "keeps the 141 seed words, adds one word ..., and then repeatedly moves one 1 to a 0 position inside a word". My comparison against the hosted seed shows that the final object contains 117 of the 141 seed words unchanged; 25 words differ from every seed word. The sentence describes the starting state, and the following clause says words are then modified, so it is not false. A reader could still take "keeps" to mean the final code is the seed plus one word. how-we-built-it/COMMANDS.md ("reads the start file's words, adds the missing word(s)") is clearer.

## Problems found

None material. The only issue is the "keeps the 141 seed words" wording above, which is imprecise but not false and does not affect the claim.

## Reasoning

The object is an explicit list of 142 distinct length-25, weight-12 binary words with all pairwise distances >= 10, and d is even. 142 is strictly greater than the lower bound 141 shown in the live (25,10,12) cell. The mirror cell is the same cell under complement symmetry. 142 does not exceed the upper bound 433. Neither of the two named arXiv papers, nor either newer arXiv paper on these codes that I found, gives a value of 142 or more for this cell. The bank criterion holds word by word, and the package's scope sentence and fact statements check out against the object and the live pages.

pass: true
