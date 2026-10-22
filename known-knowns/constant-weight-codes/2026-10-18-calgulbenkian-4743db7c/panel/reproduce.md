# Reproduce report: A(52,8,7) >= 3802

context: Claude Code subagent, fresh context

Role: reproduce skeptic. Scope: only this cell. Currency of the table value and novelty are not judged here.

## Folder integrity
The package folder was checked with shasum -a 256 -c against the contributor's hash list from inside the package folder: every listed file reported OK (0 failures). The folder was then copied to a private workspace and all work was done there.

## Definition (quoted from the bank statement and the target's success criterion)
"A(n,d,w) is the maximum number of binary words of length n and weight w with pairwise Hamming distance >= d."
"Success means an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER (direction: max) than the lower bound shown at verification time in the (n,d,w) cell ... M must not exceed the tabulated upper bound; exceeding it means a bug."
Verification method (quoted): "assert popcount == w for each, all distinct, and popcount(x ^ y) >= d for all pairs".

Cell claimed: n=52, d=8, w=7, M=3802.

## Properties checked from the shipped files (own checker, written before looking at verify-it-yourself/)
1. Format: every line of object/A52_8_7_3802.txt is a 0/1 string of exactly 52 characters; line count equals 3802.
2. Distinctness: all 3802 words are pairwise different as integers.
3. Weight: every word has exactly 7 ones (checked by bit counting on the integer value).
4. Distance: all 7225701 unordered pairs were computed (XOR then byte-table popcount, numpy, blocks of 512 words); the minimum distance must be at least 8 and the violation count must be zero.
5. Object identity: sha256 of the object file is 4743db7cec4929d05cba257484e8cce16c1f304d94efdb0b82d6870f191e473c; INDEX.csv lists 4743db7cec4929d05cba257484e8cce16c1f304d94efdb0b82d6870f191e473c; equal.
6. Table comparison from the recorded excerpt only (no network): excerpt cell reads "3799^Pl^-7577" (superscripts between carets; lower bound first, then the printed upper bound 7577). INDEX.csv table_value is 3799. 3802 > 3799: True. 3802 <= upper bound 7577: True.

## Command and real output (own checker, run before the author's script)
Command: (own checker, not shipped in this package; run on object/A52_8_7_3802.txt with parameters 52 8 7 3802)
Full output:
```
lines: 3802 expected M: 3802
malformed lines (wrong length or non-01 chars): 0
distinct words: 3802
weights: min 7 max 7
pairs checked: 7225701 expected: 7225701
min pairwise distance: 8 violations (<8): 0
RESULT: PASS
```

## Author's run_checks.sh (run only after my own checker)
Command: sh verify-it-yourself/run_checks.sh (from a private copy of the package). Output:
```
sha256 matches INDEX.csv (4743db7cec4929d05cba257484e8cce16c1f304d94efdb0b82d6870f191e473c)
== check_cw.py on object/A52_8_7_3802.txt (count, distinct, weight, all pairwise distances)
A52_8_7_3802.txt: M=3802 n=52 w=7 min distance 8 >= 8 PASS
checker verdict: PASS
== negative control 1: a copy whose last word is replaced by a copy of the first word must FAIL
negative control 1 rejected as expected
== negative control 2: the same object checked against a claim of one more word must FAIL
negative control 2 rejected as expected
ALL CHECKS PASS
```
Comparison: my checker and the author's agree (PASS on count, distinctness, weight, all pairs, sha256, both negative controls rejected). No mismatch, no missing object, no non-determinism seen (the check is exhaustive over all pairs, not a sample).

## Doubts
None about the object. Whether 3802 still beats the live table, and whether arXiv papers hold a better value, is for the novelty skeptic.

reproduce: the code of 3802 words meets length 52, weight 7, distance >= 8 exactly, exhaustively verified.
pass: true
