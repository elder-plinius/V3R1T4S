# Reproduce report: A(55,8,7) >= 4432

context: Claude Code subagent, fresh context

Role: reproduce skeptic. Scope: only this cell. Currency of the table value and novelty are not judged here.

## Folder integrity
The package folder was checked with shasum -a 256 -c against the contributor's hash list from inside the package folder: every listed file reported OK (0 failures). The folder was then copied to a private workspace and all work was done there.

## Definition (quoted from the bank statement and the target's success criterion)
"A(n,d,w) is the maximum number of binary words of length n and weight w with pairwise Hamming distance >= d."
"Success means an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER (direction: max) than the lower bound shown at verification time in the (n,d,w) cell ... M must not exceed the tabulated upper bound; exceeding it means a bug."
Verification method (quoted): "assert popcount == w for each, all distinct, and popcount(x ^ y) >= d for all pairs".

Cell claimed: n=55, d=8, w=7, M=4432.

## Properties checked from the shipped files (own checker, written before looking at verify-it-yourself/)
1. Format: every line of object/A55_8_7_4432.txt is a 0/1 string of exactly 55 characters; line count equals 4432.
2. Distinctness: all 4432 words are pairwise different as integers.
3. Weight: every word has exactly 7 ones (checked by bit counting on the integer value).
4. Distance: all 9819096 unordered pairs were computed (XOR then byte-table popcount, numpy, blocks of 512 words); the minimum distance must be at least 8 and the violation count must be zero.
5. Object identity: sha256 of the object file is 50a6e273e744067f04a66224a610b1af8d524d8fc1ba932e4039bf94ae43fb2b; INDEX.csv lists 50a6e273e744067f04a66224a610b1af8d524d8fc1ba932e4039bf94ae43fb2b; equal.
6. Table comparison from the recorded excerpt only (no network): excerpt cell reads "4426^Pl^-9617" (superscripts between carets; lower bound first, then the printed upper bound 9617). INDEX.csv table_value is 4426. 4432 > 4426: True. 4432 <= upper bound 9617: True.

## Command and real output (own checker, run before the author's script)
Command: (own checker, not shipped in this package; run on object/A55_8_7_4432.txt with parameters 55 8 7 4432)
Full output:
```
lines: 4432 expected M: 4432
malformed lines (wrong length or non-01 chars): 0
distinct words: 4432
weights: min 7 max 7
pairs checked: 9819096 expected: 9819096
min pairwise distance: 8 violations (<8): 0
RESULT: PASS
```

## Author's run_checks.sh (run only after my own checker)
Command: sh verify-it-yourself/run_checks.sh (from a private copy of the package). Output:
```
sha256 matches INDEX.csv (50a6e273e744067f04a66224a610b1af8d524d8fc1ba932e4039bf94ae43fb2b)
== check_cw.py on object/A55_8_7_4432.txt (count, distinct, weight, all pairwise distances)
A55_8_7_4432.txt: M=4432 n=55 w=7 min distance 8 >= 8 PASS
checker verdict: PASS
== negative control 1: a copy whose last word is replaced by a copy of the first word must FAIL
negative control 1 rejected as expected
== negative control 2: the same object checked against a claim of one more word must FAIL
negative control 2 rejected as expected
ALL CHECKS PASS
```
Comparison: my checker and the author's agree (PASS on count, distinctness, weight, all pairs, sha256, both negative controls rejected). No mismatch, no missing object, no non-determinism seen (the check is exhaustive over all pairs, not a sample).

## Doubts
None about the object. Whether 4432 still beats the live table, and whether arXiv papers hold a better value, is for the novelty skeptic.

reproduce: the code of 4432 words meets length 55, weight 7, distance >= 8 exactly, exhaustively verified.
pass: true
