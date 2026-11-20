# CRITERION verdict: brouwer-qary-unrestricted-a3-a4-a5, cell A3(15,10)
context: fresh reviewer (new context started for the CRITERION role only; saw only CLAIM.md, RECORD.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-20T14:06:30Z

## What I fetched

- Bank file: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json, one curl request, HTTP 200, fetched 2026-11-20T14:05:57Z, sha256 7c3942f228807b3bd1eae1b636f557aca64344161137e8bda5566081a6b846a2. Exactly one entry has id `brouwer-qary-unrestricted-a3-a4-a5`.
- I did not fetch the table page (that belongs to another reviewer, per the brief).

## Criterion text comparison

- `success_criterion` in the bank entry vs the quote in CLAIM.md: identical, character for character (Python string equality True, both 604 characters).
- `verification_method` vs the second quote in CLAIM.md: identical (True, both 164 characters).
- The bank entry's own `statement` (status checked 2026-10-28) independently lists "A3(15,10) 27-39", matching RECORD.md's extraction.

## My own computation (stdlib Python, all pairs)

On `object/A3-15-10-31words.txt` (sha256 86da3f818e06cbe15a35aabf63c8849ee96e1ccf3dd36c9964113732876d9555, matches CLAIM.md):

- 1 header line starting with `#`, 31 word lines; every word has length 15 over {0,1,2}.
- M = 31, distinct = 31.
- All 465 pairs checked: minimum Hamming distance 10; distance distribution {10: 360, 11: 75, 12: 30}.
- Rebuilding the code from the words-only description (orbits of `000000000000000` and `001111201221012` under the 15 cyclic shifts and the global 1<->2 exchange) gives 31 words, equal as a set to the file. The construction text matches the object.

## RECORD.md extraction of the cell

RECORD.md quotes the n = 15 `ub` and `lb` rows: after the label cell and one empty cell, 12 values. Reading the first value as d = 3 puts ub 39 / lb 27 at d = 10, and `=` at d = 11..14. I checked that this column assignment is forced, not assumed:

- Shifting one column right would put ub 10 at d = 12 and ub 39 at d = 11; the Plotkin bound for q = 3, n = 15 gives A3(15,11) <= 11 and A3(15,12) <= 6, so that reading is impossible.
- Shifting one column left would make d = 10 an exact `=` cell with value 10, contradicted by the 31-word code above.
- The quoted note line `A3(15,10) ≤ 39` and the bank statement's "27-39" agree with the d = 10 reading.

The lb entry is the number 27, not `=`, so under the stated convention the cell is open. Whether those rows really appear in the live page as quoted, the page hash and the fetch time are for the table reviewer; I took them from RECORD.md (fetched 2026-11-20T14:01:14Z).

## Clause by clause

1. "explicit list of M distinct words over {0..q-1}^n (q in {3,4,5})": met (31 distinct words, q = 3, n = 15).
2. "an independent script confirms all pairwise Hamming distances >= d": met for d = 10 by my own all-pairs script (no sampling, written without seeing the claimant's checker).
3. "M is STRICTLY GREATER ... than the lower bound for A_q(n,d) in the corresponding live table": 31 > 27, with 31 <= ub 39, so no conflict with the upper bound. Met, given RECORD.md's cell value; the live value itself is the table reviewer's check.
4. "re-fetched live immediately before claiming": RECORD.md states a fetch at 2026-11-20T14:01:14Z, the same day as the claim. I cannot verify the fetch itself; left to the table reviewer.
5. "'=' entries are exact and cannot be beaten": the cell is lb 27, not `=`. Met.
6. "must not appear in the notes under the table": RECORD.md says the only note naming A3(15,10) is the upper bound 39. Not verified by me (no page fetch); left to the table reviewer.
7. "or in an arXiv/journal search done on the day": not checked by me; belongs to the novelty reviewer.

Hidden quantifiers and definitions: "distinct" checked; "all pairwise" checked over all 465 pairs; "lower bound" read as the lb row, not the ub row; the bank pitfall "compare against the max of grid and notes" is covered only through RECORD.md's note extraction. The claim is the full success criterion, not a partial win (p1 concerns n = 17 or 18, p2 upper bounds), and it is not subsumed by anything I can see: the claimed value exceeds the listed lb by 4 and stays below the ub.

Null-model check: a code meeting the stated bounds trivially (the 27-word record or anything from the table) would not pass; 31 words at distance 10 cannot be obtained from the cells I can see. Monotonicity relations with neighbouring cells (for example A3(15,10) >= A3(16,11) or >= A3(14,10)) could only show the table's 27 was already stale; those rows are not in RECORD.md, so that is left to the table reviewer.

## Problems found

None in the object or the criterion quote. Open items outside this role: the live table cell, the notes and the fetch time (table reviewer), and the literature search (novelty reviewer).

confirmed_scope: `object/A3-15-10-31words.txt` (sha256 86da3f81...) is a set of 31 distinct words of length n = 15 over q = 3 symbols with minimum Hamming distance 10 (all 465 pairs checked), so A3(15,10) >= 31, which exceeds the lower bound 27 (upper bound 39) that RECORD.md extracts from the ternary table fetched 2026-11-20T14:01:14Z; the live-table and literature clauses rest on the other reviewers.

pass: true
