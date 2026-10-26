# Reproduce report: A(35,6,6) >= 2218

context: Claude Code subagent, fresh context

Role: reproduce skeptic. Scope: only this cell. Currency of the table value and novelty are not judged here.

## Folder integrity
The package folder was checked with shasum -a 256 -c against the contributor's hash list from inside the package folder: every listed file reported OK (0 failures). The folder was then copied to a private workspace and all work was done there.

## Definition (quoted from the bank statement and the target's success criterion)
"A(n,d,w) is the maximum number of binary words of length n and weight w with pairwise Hamming distance >= d."
"Success means an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER (direction: max) than the lower bound shown at verification time in the (n,d,w) cell ... M must not exceed the tabulated upper bound; exceeding it means a bug."
Verification method (quoted): "assert popcount == w for each, all distinct, and popcount(x ^ y) >= d for all pairs".

Cell claimed: n=35, d=6, w=6, M=2218.

## Properties checked from the shipped files (own checker, written before looking at verify-it-yourself/)
1. Format: every line of object/A35_6_6_2218.txt is a 0/1 string of exactly 35 characters; line count equals 2218.
2. Distinctness: all 2218 words are pairwise different as integers.
3. Weight: every word has exactly 6 ones (checked by bit counting on the integer value).
4. Distance: all 2458653 unordered pairs were computed (XOR then byte-table popcount, numpy, blocks of 512 words); the minimum distance must be at least 6 and the violation count must be zero.
5. Object identity: sha256 of the object file is dd2eb057e40bc19bbd7f6a2838681200d6d55b4018e9b01a62082c35822e413e; INDEX.csv lists dd2eb057e40bc19bbd7f6a2838681200d6d55b4018e9b01a62082c35822e413e; equal.
6. Table comparison from the recorded excerpt only (no network): excerpt cell reads "2217^Pl^-3249" (superscripts between carets; lower bound first, then the printed upper bound 3249). INDEX.csv table_value is 2217. 2218 > 2217: True. 2218 <= upper bound 3249: True.

## Command and real output (own checker, run before the author's script)
Command: (own checker, not shipped in this package; run on object/A35_6_6_2218.txt with parameters 35 6 6 2218)
Full output:
```
lines: 2218 expected M: 2218
malformed lines (wrong length or non-01 chars): 0
distinct words: 2218
weights: min 6 max 6
pairs checked: 2458653 expected: 2458653
min pairwise distance: 6 violations (<6): 0
RESULT: PASS
```

## Author's run_checks.sh (run only after my own checker)
Command: sh verify-it-yourself/run_checks.sh (from a private copy of the package). Output:
```
sha256 matches INDEX.csv (dd2eb057e40bc19bbd7f6a2838681200d6d55b4018e9b01a62082c35822e413e)
== check_cw.py on object/A35_6_6_2218.txt (count, distinct, weight, all pairwise distances)
A35_6_6_2218.txt: M=2218 n=35 w=6 min distance 6 >= 6 PASS
checker verdict: PASS
== negative control 1: a copy whose last word is replaced by a copy of the first word must FAIL
negative control 1 rejected as expected
== negative control 2: the same object checked against a claim of one more word must FAIL
negative control 2 rejected as expected
ALL CHECKS PASS
```
Comparison: my checker and the author's agree (PASS on count, distinctness, weight, all pairs, sha256, both negative controls rejected). No mismatch, no missing object, no non-determinism seen (the check is exhaustive over all pairs, not a sample).

## Doubts
None about the object. Whether 2218 still beats the live table, and whether arXiv papers hold a better value, is for the novelty skeptic.

reproduce: the code of 2218 words meets length 35, weight 6, distance >= 6 exactly, exhaustively verified.
pass: true
