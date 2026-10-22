# Reproduce report: A(25,6,11) >= 8720

context: Claude Code subagent, fresh context

Role: reproduce skeptic. Scope: only this cell. Currency of the table value and novelty are not judged here.

## Folder integrity
The package folder was checked with shasum -a 256 -c against the contributor's hash list from inside the package folder: every listed file reported OK (0 failures). The folder was then copied to a private workspace and all work was done there.

## Definition (quoted from the bank statement and the target's success criterion)
"A(n,d,w) is the maximum number of binary words of length n and weight w with pairwise Hamming distance >= d."
"Success means an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER (direction: max) than the lower bound shown at verification time in the (n,d,w) cell ... M must not exceed the tabulated upper bound; exceeding it means a bug."
Verification method (quoted): "assert popcount == w for each, all distinct, and popcount(x ^ y) >= d for all pairs".

Cell claimed: n=25, d=6, w=11, M=8720.

## Properties checked from the shipped files (own checker, written before looking at verify-it-yourself/)
1. Format: every line of object/A25_6_11_8720.txt is a 0/1 string of exactly 25 characters; line count equals 8720.
2. Distinctness: all 8720 words are pairwise different as integers.
3. Weight: every word has exactly 11 ones (checked by bit counting on the integer value).
4. Distance: all 38014840 unordered pairs were computed (XOR then byte-table popcount, numpy, blocks of 512 words); the minimum distance must be at least 6 and the violation count must be zero.
5. Object identity: sha256 of the object file is 46ae5613f60a668ea22c94f602bee8c8aa8332011fe4b2016500f8d6e93214c3; INDEX.csv lists 46ae5613f60a668ea22c94f602bee8c8aa8332011fe4b2016500f8d6e93214c3; equal.
6. Table comparison from the recorded excerpt only (no network): excerpt cell reads "8718^Pl^-24630 | ncols 9 11" (superscripts between carets; lower bound first, then the printed upper bound 24630). INDEX.csv table_value is 8718. 8720 > 8718: True. 8720 <= upper bound 24630: True.

## Command and real output (own checker, run before the author's script)
Command: (own checker, not shipped in this package; run on object/A25_6_11_8720.txt with parameters 25 6 11 8720)
Full output:
```
lines: 8720 expected M: 8720
malformed lines (wrong length or non-01 chars): 0
distinct words: 8720
weights: min 11 max 11
pairs checked: 38014840 expected: 38014840
min pairwise distance: 6 violations (<6): 0
RESULT: PASS
```

## Author's run_checks.sh (run only after my own checker)
Command: sh verify-it-yourself/run_checks.sh (from a private copy of the package). Output:
```
sha256 matches INDEX.csv (46ae5613f60a668ea22c94f602bee8c8aa8332011fe4b2016500f8d6e93214c3)
== check_cw.py on object/A25_6_11_8720.txt (count, distinct, weight, all pairwise distances)
A25_6_11_8720.txt: M=8720 n=25 w=11 min distance 6 >= 6 PASS
checker verdict: PASS
== negative control 1: a copy whose last word is replaced by a copy of the first word must FAIL
negative control 1 rejected as expected
== negative control 2: the same object checked against a claim of one more word must FAIL
negative control 2 rejected as expected
ALL CHECKS PASS
```
Comparison: my checker and the author's agree (PASS on count, distinctness, weight, all pairs, sha256, both negative controls rejected). No mismatch, no missing object, no non-determinism seen (the check is exhaustive over all pairs, not a sample).

## Doubts
None about the object. Whether 8720 still beats the live table, and whether arXiv papers hold a better value, is for the novelty skeptic.

reproduce: the code of 8720 words meets length 25, weight 11, distance >= 6 exactly, exhaustively verified.
pass: true
