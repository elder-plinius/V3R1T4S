# Reproduce report: A(27,8,10) >= 1740

context: Claude Code subagent, fresh context

Role: reproduce skeptic. Scope: only this cell. Currency of the table value and novelty are not judged here.

## Folder integrity
The package folder was checked with shasum -a 256 -c against the contributor's hash list from inside the package folder: every listed file reported OK (0 failures). The folder was then copied to a private workspace and all work was done there.

## Definition (quoted from the bank statement and the target's success criterion)
"A(n,d,w) is the maximum number of binary words of length n and weight w with pairwise Hamming distance >= d."
"Success means an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER (direction: max) than the lower bound shown at verification time in the (n,d,w) cell ... M must not exceed the tabulated upper bound; exceeding it means a bug."
Verification method (quoted): "assert popcount == w for each, all distinct, and popcount(x ^ y) >= d for all pairs".

Cell claimed: n=27, d=8, w=10, M=1740.

## Properties checked from the shipped files (own checker, written before looking at verify-it-yourself/)
1. Format: every line of object/A27_8_10_1740.txt is a 0/1 string of exactly 27 characters; line count equals 1740.
2. Distinctness: all 1740 words are pairwise different as integers.
3. Weight: every word has exactly 10 ones (checked by bit counting on the integer value).
4. Distance: all 1512930 unordered pairs were computed (XOR then byte-table popcount, numpy, blocks of 512 words); the minimum distance must be at least 8 and the violation count must be zero.
5. Object identity: sha256 of the object file is bdbf1cf2b34d5a2771172cea5d11fe6abcff25a0de03cc60808796fbe6e0acbe; INDEX.csv lists bdbf1cf2b34d5a2771172cea5d11fe6abcff25a0de03cc60808796fbe6e0acbe; equal.
6. Table comparison from the recorded excerpt only (no network): excerpt cell reads "1737^Pl^-4986 | ncols 9 10" (superscripts between carets; lower bound first, then the printed upper bound 4986). INDEX.csv table_value is 1737. 1740 > 1737: True. 1740 <= upper bound 4986: True.

## Command and real output (own checker, run before the author's script)
Command: (own checker, not shipped in this package; run on object/A27_8_10_1740.txt with parameters 27 8 10 1740)
Full output:
```
lines: 1740 expected M: 1740
malformed lines (wrong length or non-01 chars): 0
distinct words: 1740
weights: min 10 max 10
pairs checked: 1512930 expected: 1512930
min pairwise distance: 8 violations (<8): 0
RESULT: PASS
```

## Author's run_checks.sh (run only after my own checker)
Command: sh verify-it-yourself/run_checks.sh (from a private copy of the package). Output:
```
sha256 matches INDEX.csv (bdbf1cf2b34d5a2771172cea5d11fe6abcff25a0de03cc60808796fbe6e0acbe)
== check_cw.py on object/A27_8_10_1740.txt (count, distinct, weight, all pairwise distances)
A27_8_10_1740.txt: M=1740 n=27 w=10 min distance 8 >= 8 PASS
checker verdict: PASS
== negative control 1: a copy whose last word is replaced by a copy of the first word must FAIL
negative control 1 rejected as expected
== negative control 2: the same object checked against a claim of one more word must FAIL
negative control 2 rejected as expected
ALL CHECKS PASS
```
Comparison: my checker and the author's agree (PASS on count, distinctness, weight, all pairs, sha256, both negative controls rejected). No mismatch, no missing object, no non-determinism seen (the check is exhaustive over all pairs, not a sample).

## Doubts
None about the object. Whether 1740 still beats the live table, and whether arXiv papers hold a better value, is for the novelty skeptic.

reproduce: the code of 1740 words meets length 27, weight 10, distance >= 8 exactly, exhaustively verified.
pass: true
