# CRITERION verdict: constant-weight-codes, cell A(30,12,9)

context: fresh reviewer (new subagent context started for the CRITERION role only; saw only CLAIM.md, RECORD.md, object/, search/ and public pages; no access to the claimant's checker)

verdict_utc: 2026-11-26T20:26:17Z

## Bank entry (fetched once)

- URL: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json
- fetched 2026-11-26T20:25:49Z, HTTP 200, sha256 of the file 7c3942f228807b3bd1eae1b636f557aca64344161137e8bda5566081a6b846a2
- entry id constant-weight-codes found; its success_criterion and verification_method were compared by program with the quoted lines in CLAIM.md (text after the leading quote marker).
- success_criterion: identical, 582 characters each.
- verification_method: identical, 413 characters each.
- The entry has two enumerated partial wins (p1 explicit certificate at the tabulated size, p2 improved upper bound); neither is claimed, and the claim is judged against the full criterion.

## Own all-pairs check of the object

Script written from scratch (Python standard library, words as Python ints, popcount of XOR over all pairs). Output, copied from the program:

- object/A-30-12-9-45words.txt sha256 806649f74bcb4ec5746f248ef5f087f88d56120661f95e0d7a464d9965f9060d (matches CLAIM.md)
- 47 split lines: 1 header line starting with a hash sign, 45 code lines, 1 empty trailing line; no other lines, no CR characters
- every code line has length 30 and uses only the characters 0 and 1
- weights: all 9
- distinct words: 45
- pairs: 990; minimum distance 12; distance histogram 12: 756, 14: 141, 16: 36, 18: 57 (matches the intersection counts 3, 2, 1, 0 stated in CLAIM.md)
- complements: all weight 21, minimum distance 12, so the same object gives A(30,12,21) at least 45
- coordinate degrees: 3 coordinates in 8 words, 3 in 13, 18 in 14, 6 in 15 (matches CLAIM.md)

## Clause by clause

1. "explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w": met, M = 45, n = 30, w = 9, all distinct (own computation).
2. "all pairwise distances >= d (d even)": met, minimum distance 12, d = 12 is even, so no odd-d reduction applies.
3. "STRICTLY GREATER than the lower bound shown at verification time in the (n,d,w) cell": per RECORD.md the cell reads 44-74 at 2026-11-26T20:13:38Z (page sha256 7429c8d2567123d043a5881bf67a3f1344b268b94a63af794eceefde2c165604); 45 > 44. I did not fetch the table (another reviewer does). The RECORD.md extraction reads correctly: the quoted n = 30 row in the "Bounds on A(n,12,w)" section has cells 9, 30, 44-74, 101-159; the third cell is w = 9 under the stated column start w = 7, and its link target, the file a30.12.9.44 under cwc/d12, independently encodes n = 30, d = 12, w = 9 and size 44. In the lb-ub convention, 44 is the lower bound and 74 the upper bound (superscript Po). Whether that cell still reads 44 at verification time is left to the live-table reviewer.
4. "also checking the mirror cell A(n,d,n-w)": the mirror is A(30,12,21). RECORD.md says the table lists only w at most n/2, so the mirror has no separate entry and shares the value 44-74; this is consistent with the table convention and with the complement map I computed (the complement of the object is a valid 45-word A(30,12,21) code). Confirming on the live page that no separate or larger mirror value exists is left to the live-table reviewer.
5. "strictly greater than any value for that cell in arXiv:2608.13906, arXiv:2607.19550 or any newer arXiv paper": not checked here. RECORD.md quotes a table note crediting 44 to polishing Rosin's 43 (arXiv:2603.00174), which suggests the table already reflects the literature it cites, but the papers' own tables and any newer arXiv paper belong to the novelty reviewer.
6. "M must not exceed the tabulated upper bound": 45 does not exceed 74 (from RECORD.md). An own Johnson-type chain (A(n,12,6) = floor(n/6), then A(n,d,w) at most floor(n/w times A(n-1,d,w-1))) gives at most 193, so 45 is not ruled out by a trivial bound either.
7. Verification method: an independent script with Python ints and all pairwise popcounts was used (stdlib, not numpy; the method lists numpy or bitset blocks as means, the substance, every one of the 990 pairs, is met). The re-fetch of the table at check time is the live-table reviewer's step.

## Null model and subsumption

- 45 is one above the tabulated 44, so the claim depends only on the object being valid and the cell still reading 44; the validity part is fully confirmed above.
- RECORD.md's table of bounds implied by neighbouring hosted codes (best 42, from A(29,12,9) at least 42 with a zero coordinate appended) shows no trivial derivation of 45; I did not recompute it (it needs the hosted files). Trivial constructions I can rule out without data: shortening or puncturing cannot raise a cell above its neighbours' implications, and the d = 14 cell value 10 cited there is far below 45.
- No stretched definition found: the object is a plain constant-weight code at exactly the claimed n, d, w, not a different cell, a non-binary code, or a weight-relaxed code.

## Problems found

- None in the object or in the quotes.
- Minor: the bank's verification method names numpy; this check used plain Python ints, which computes the same popcounts exactly.

## Reasoning

Every clause I can decide from the object and the bank text is met literally. The two remaining clauses (the live cell at verification time including the mirror, and the arXiv literature including newer papers) are factual checks outside this role, and RECORD.md's extraction of the cell from the quoted page rows is correct as read. On that basis the claim meets the full success criterion, not a partial win, subject to the live-table and novelty reviewers confirming the cell still reads 44-74 and no paper lists 45 or more.

confirmed_scope: The file object/A-30-12-9-45words.txt (sha256 806649f7...) is a list of 45 distinct binary words of length 30, each of weight 9, with minimum Hamming distance 12 (so also A(30,12,21) at least 45 by complement), which exceeds the lower bound 44 and does not exceed the upper bound 74 of the A(30,12,9) cell as recorded in RECORD.md from the table fetched at 2026-11-26T20:13:38Z.

pass: true
