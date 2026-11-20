# CRITERION verdict: brouwer-qary-unrestricted-a3-a4-a5, cell A4(12,7)

context: fresh reviewer (new context started for the CRITERION role only; saw only CLAIM.md, RECORD.md, object/ and public pages; no access to the search code or the claimant's checker)

verdict_utc: 2026-11-20T14:06:27Z

## Bank entry (fetched once)

- URL: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json
- fetched (UTC): 2026-11-20T14:05:54Z, HTTP 200, 6427050 bytes, sha256 7c3942f228807b3bd1eae1b636f557aca64344161137e8bda5566081a6b846a2
- Exactly one entry with id `brouwer-qary-unrestricted-a3-a4-a5`.
- The `success_criterion` string in the bank and the quote in CLAIM.md are identical (Python string equality: True).
- The `verification_method` string in the bank and the quote in CLAIM.md are identical (True).
- The entry lists two partial wins (p1: ternary n = 17 or 18; p2: LP upper-bound certificate). Neither applies; the claim is made under the full criterion.

## Object (own all-pairs check, stdlib Python)

- File `object/A4-12-7-320words.txt`, sha256 7a882f805e40e7ef6a9565684cc1c36d616b91f2d3081be69aef2d00dfe69d82 (matches CLAIM.md), 4364 bytes.
- 1 header line starting with `#`, 320 body lines, one trailing newline; 0 malformed lines (every body line is exactly 12 characters from 0123).
- M = 320, distinct = 320, length n = 12, alphabet {0,1,2,3}, so q = 4.
- All 51040 pairs computed (no sampling). Minimum Hamming distance 7.
- Distance distribution: {7: 10176, 8: 6816, 9: 17536, 10: 5376, 11: 10176, 12: 960}.
- Construction check (not required by the criterion, done as a consistency check): the two generators as described in CLAIM.md generate a group of order 48 (computed as a permutation group on the 48 position-symbol pairs); the orbits of the 11 listed representatives have sizes [24, 48, 24, 48, 48, 16, 24, 48, 12, 16, 12], their union has 320 words, and it equals the set of words in the file. The description in CLAIM.md therefore matches the file exactly.

## Table cell (from RECORD.md; page not fetched by this reviewer)

- RECORD.md quotes the n = 12 `ub` and `lb` rows: after the row label there is one empty cell, then the values. Reading the first value as d = 3 gives lb row 262144, 65536, 8192, 4096, 256, 128, =, =, = for d = 3..11 and ub row 419430, 109226, 20852, 5864, 1167, 240, 48, 9, 4.
- This column mapping is the right one: lb(d=3) = 262144 = 4^9 is the shortened quaternary Hamming code [12,9,3]; ub(d=11) = 4 is within the Plotkin bound (floor(11/(11 - 9)) = 5); and the note quoted in RECORD.md, `A4(12,7) ≤ 1167.`, matches the ub value in the d = 7 column. Shifting the mapping one column either way would put 1167 under d = 6 or d = 8 and contradict that note.
- Cell A4(12,7): lb 256 (a number, not `=`, so the cell is open), ub 1167. 256 = 4^4 fits the attributed linear [12,4,7] code over GF(4).
- RECORD.md metadata is self-consistent (Content-Length 5747 equals the ETag's hex length 0x1673). Whether the quoted rows and notes are what the page actually serves, and the fetch time 2026-11-20T14:01:15Z, belong to the reviewer who fetches the table; this verdict takes them from RECORD.md.

## Clause by clause

1. "an explicit list of M distinct words over {0..q-1}^n (q in {3,4,5})": met. 320 distinct explicit words in {0..3}^12, q = 4.
2. "an independent script confirms all pairwise Hamming distances >= d": met for d = 7 by this reviewer's own script over all 51040 pairs.
3. "M is STRICTLY GREATER ... than the lower bound for A_q(n,d) in the corresponding live table (quaternary-1.html)": 320 > 256, met against the cell as extracted in RECORD.md. 320 also does not exceed the ub 1167, so there is no contradiction with the table's upper bound (a null check: a claim above the ub would indicate an error).
4. "re-fetched live immediately before claiming": RECORD.md records a fetch at 2026-11-20T14:01:15Z, the same day as the claim. Not independently verified here; left to the table reviewer.
5. "'=' entries are exact and cannot be beaten": the cell's lb is 256, not `=`. Met (on RECORD.md's extraction).
6. "must not appear in the notes under the table": RECORD.md lists one note naming A4(12,7), an upper bound (≤ 1167); none gives a lower bound above 256. Met on RECORD.md's extraction; the bank pitfall "compare against the max of grid and notes" gives the same comparison value 256.
7. "or in an arXiv/journal search done on the day": not checked by this reviewer. It belongs to the novelty reviewer.

Hidden-quantifier and stretched-definition hunt: "all pairwise" was checked over all pairs, not sampled; "distinct" holds; the comparison is with the unrestricted (nonlinear) lower bound, as the table is of unrestricted codes; M = 320 is not a power of 4, so the object is not a GF(4)-linear code that the bank's last pitfall warns may already be in the table; the cell is in the quaternary table's range (n up to 12). No partial-win label is being stretched into a full win.

## Problems found

None in the clauses this role checks. Clauses 4 (live fetch fidelity) and 7 (literature search on the day) rest on other reviewers.

confirmed_scope: `object/A4-12-7-320words.txt` (sha256 7a882f80...) lists 320 distinct words of length n = 12 over q = 4 symbols with minimum Hamming distance 7 over all pairs, which is strictly above the lower bound 256 (ub 1167, not `=`) for A4(12,7) as extracted in RECORD.md from the quaternary table fetched 2026-11-20T14:01:15Z; page fidelity and the literature search are left to the other reviewers.

pass: true
