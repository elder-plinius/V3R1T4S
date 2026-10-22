# Reproduce report: A(51,6,6) >= 11187

context: Claude Code subagent, fresh context

Role: reproduce skeptic. Scope: only this cell. Currency of the table value and novelty are not judged here.

## Folder integrity
The package folder was checked with shasum -a 256 -c against the contributor's hash list from inside the package folder: every listed file reported OK (0 failures). The folder was then copied to a private workspace and all work was done there.

## Definition (quoted from the bank statement and the target's success criterion)
"A(n,d,w) is the maximum number of binary words of length n and weight w with pairwise Hamming distance >= d."
"Success means an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER (direction: max) than the lower bound shown at verification time in the (n,d,w) cell ... M must not exceed the tabulated upper bound; exceeding it means a bug."
Verification method (quoted): "assert popcount == w for each, all distinct, and popcount(x ^ y) >= d for all pairs".

Cell claimed: n=51, d=6, w=6, M=11187.

## Properties checked from the shipped files (own checker, written before looking at verify-it-yourself/)
1. Format: every line of object/A51_6_6_11187.txt is a 0/1 string of exactly 51 characters; line count equals 11187.
2. Distinctness: all 11187 words are pairwise different as integers.
3. Weight: every word has exactly 6 ones (checked by bit counting on the integer value).
4. Distance: all 62568891 unordered pairs were computed (XOR then byte-table popcount, numpy, blocks of 512 words); the minimum distance must be at least 6 and the violation count must be zero.
5. Object identity: sha256 of the object file is 3684474037a4c99801649121c6515c307e50684c4652135eaba3767b5a1c1df5; INDEX.csv lists 3684474037a4c99801649121c6515c307e50684c4652135eaba3767b5a1c1df5; equal.
6. Table comparison from the recorded excerpt only (no network): excerpt cell reads "11184^Pl^-16660" (superscripts between carets; lower bound first, then the printed upper bound 16660). INDEX.csv table_value is 11184. 11187 > 11184: True. 11187 <= upper bound 16660: True.

## Command and real output (own checker, run before the author's script)
Command: (own checker, not shipped in this package; run on object/A51_6_6_11187.txt with parameters 51 6 6 11187)
Full output:
```
lines: 11187 expected M: 11187
malformed lines (wrong length or non-01 chars): 0
distinct words: 11187
weights: min 6 max 6
pairs checked: 62568891 expected: 62568891
min pairwise distance: 6 violations (<6): 0
RESULT: PASS
```

## Author's run_checks.sh (run only after my own checker)
Command: sh verify-it-yourself/run_checks.sh (from a private copy of the package). Output:
```
sha256 matches INDEX.csv (3684474037a4c99801649121c6515c307e50684c4652135eaba3767b5a1c1df5)
== check_cw.py on object/A51_6_6_11187.txt (count, distinct, weight, all pairwise distances)
A51_6_6_11187.txt: M=11187 n=51 w=6 min distance 6 >= 6 PASS
checker verdict: PASS
== negative control 1: a copy whose last word is replaced by a copy of the first word must FAIL
negative control 1 rejected as expected
== negative control 2: the same object checked against a claim of one more word must FAIL
negative control 2 rejected as expected
ALL CHECKS PASS
```
Comparison: my checker and the author's agree (PASS on count, distinctness, weight, all pairs, sha256, both negative controls rejected). No mismatch, no missing object, no non-determinism seen (the check is exhaustive over all pairs, not a sample).

## Doubts
None about the object. Whether 11187 still beats the live table, and whether arXiv papers hold a better value, is for the novelty skeptic.

reproduce: the code of 11187 words meets length 51, weight 6, distance >= 6 exactly, exhaustively verified.
pass: true
