# Receipts: real output of verify-it-yourself/run_checks.sh

Machine: Linux, 8-core shared machine (heavily loaded at the time, load average about 36-55), Python 3.13.5. Each run
was started from a copy of this package folder with `sh verify-it-yourself/run_checks.sh` (under `nice -n 19`).
The first line of each block is the UTC start time; the last lines are the exit code and the wall time, added by the
wrapper that ran the script.

## Clean copy (expected last line PASS)

```
2026-11-03T20:53:56Z
== 1. sha256 of object/code_n9_d3_k1042.txt
got  b51b30e3082648bc6cb0511bd156b71ae51c967f7281a83010d2c0e844e4a93a
want b51b30e3082648bc6cb0511bd156b71ae51c967f7281a83010d2c0e844e4a93a
sha256: match
== 2. 1042 words, n=9, d=3, GC=4, edit distance and reverse-complement constraint (exhaustive, two methods)
file: object/code_n9_d3_k1042.txt  n=9 d=3 w=floor(n/2)=4  words=1042
format: all 1042 words are length 9 over ACGT
GC weight: every word has exactly 4 letters from {G,C}
distinct: yes
size: 1042 (expected 1042) ok
self-test: bit-parallel Levenshtein vs plain DP on 20000 random string pairs (lengths 0-11): 0 mismatches
method A (bit-parallel DP Levenshtein): 542361 distinct pairs, min d(x,y) = 3; 1085764 ordered pairs incl. x=y, min d(x,rc(y)) = 3
method B (edit balls of radii 1 and 1, hash index, meet in the middle): 0 violations; method A: 0 violations
methods A and B agree
VALID: 1042 words, a (9,3,4)_4 DNA code with edit distance, fixed GC weight and reverse-complement constraint
PASS
== 3. control: the same object read with d=4 must FAIL (minimum distance is exactly 3; method A only, to keep it fast)
method A (bit-parallel DP Levenshtein): 542361 distinct pairs, min d(x,y) = 3; 1085764 ordered pairs incl. x=y, min d(x,rc(y)) = 3
first violation: pair, lines 1 and 31 (CGTGTCTTA, CGCAGTTTA): d(x,y)=3 d(x,rc y)=8
NOT a valid (9,4,4)_4 RC+GC edit-metric DNA code
FAIL
control: FAIL at d=4 as expected
== 4. control: last word replaced by the first word with one A<->T substitution must FAIL
GC weight: every word has exactly 4 letters from {G,C}
distinct: yes
first violation: pair, lines 1 and 1042 (CGTGTCTTA, CGAGTCTTA): d(x,y)=1 d(x,rc y)=6
NOT a valid (9,3,4)_4 RC+GC edit-metric DNA code
FAIL
near control: FAIL as expected
== 5. control: last word replaced by a copy of the first word must FAIL
GC weight: every word has exactly 4 letters from {G,C}
distinct: 1 duplicate lines
FAIL
dup control: FAIL as expected
== 6. control: last word replaced by the reverse complement of the first word (tests the RC constraint) must FAIL
GC weight: every word has exactly 4 letters from {G,C}
distinct: yes
first violation: rc, lines 1 and 1042 (CGTGTCTTA, TAAGACACG): d(x,y)=7 d(x,rc y)=0
NOT a valid (9,3,4)_4 RC+GC edit-metric DNA code
FAIL
rc control: FAIL as expected
== 7. control: one letter of the last word changed so its GC weight is 5 must FAIL
GC weight: 1 words do not have exactly 4 letters from {G,C}, e.g. CGGGTAGTA
distinct: yes
first violation: pair, lines 223 and 1042 (CCTGTAGTA, CGGGTAGTA): d(x,y)=2 d(x,rc y)=8
NOT a valid (9,3,4)_4 RC+GC edit-metric DNA code
FAIL
gc control: FAIL as expected
== 8. control: the one-word code ACGTACGTA (d(x, rc(x)) = 2 < 3; the RC rule includes x = y) must FAIL
GC weight: every word has exactly 4 letters from {G,C}
distinct: yes
first violation: rc, lines 1 and 1 (ACGTACGTA, ACGTACGTA): d(x,y)=0 d(x,rc y)=2
NOT a valid (9,3,4)_4 RC+GC edit-metric DNA code
FAIL
self control: FAIL as expected
PASS
exit 0
wall 212 s
```

## Corrupted copy (expected last line FAIL)

One letter of the object changed: line 521 `TCGGATGAA` -> `ACGGATGAA` (an A<->T substitution, so the GC weight stays 4).
The object has no digits, so the kit's own corrupted-copy test (which changes one digit) cannot apply to it; this
letter corruption is the equivalent test.

```
2026-11-03T21:01:37Z
== 1. sha256 of object/code_n9_d3_k1042.txt
got  43de1c4c12a3cdbe68e5588b670e805cad2eb8fab2785add2ede3a84086fb35f
want b51b30e3082648bc6cb0511bd156b71ae51c967f7281a83010d2c0e844e4a93a
sha256: MISMATCH
== 2. 1042 words, n=9, d=3, GC=4, edit distance and reverse-complement constraint (exhaustive, two methods)
file: object/code_n9_d3_k1042.txt  n=9 d=3 w=floor(n/2)=4  words=1042
format: all 1042 words are length 9 over ACGT
GC weight: every word has exactly 4 letters from {G,C}
distinct: yes
size: 1042 (expected 1042) ok
self-test: bit-parallel Levenshtein vs plain DP on 20000 random string pairs (lengths 0-11): 0 mismatches
method A (bit-parallel DP Levenshtein): 542361 distinct pairs, min d(x,y) = 2; 1085764 ordered pairs incl. x=y, min d(x,rc(y)) = 3
method B (edit balls of radii 1 and 1, hash index, meet in the middle): 5 violations; method A: 5 violations
methods A and B agree
first violation: pair, lines 173 and 521 (ACAGGTGAA, ACGGATGAA): d(x,y)=2 d(x,rc y)=7
NOT a valid (9,3,4)_4 RC+GC edit-metric DNA code
FAIL
== 3. control: the same object read with d=4 must FAIL (minimum distance is exactly 3; method A only, to keep it fast)
method A (bit-parallel DP Levenshtein): 542361 distinct pairs, min d(x,y) = 2; 1085764 ordered pairs incl. x=y, min d(x,rc(y)) = 3
first violation: pair, lines 1 and 31 (CGTGTCTTA, CGCAGTTTA): d(x,y)=3 d(x,rc y)=8
NOT a valid (9,4,4)_4 RC+GC edit-metric DNA code
FAIL
control: FAIL at d=4 as expected
== 4. control: last word replaced by the first word with one A<->T substitution must FAIL
GC weight: every word has exactly 4 letters from {G,C}
distinct: yes
first violation: pair, lines 1 and 1042 (CGTGTCTTA, CGAGTCTTA): d(x,y)=1 d(x,rc y)=6
NOT a valid (9,3,4)_4 RC+GC edit-metric DNA code
FAIL
near control: FAIL as expected
== 5. control: last word replaced by a copy of the first word must FAIL
GC weight: every word has exactly 4 letters from {G,C}
distinct: 1 duplicate lines
FAIL
dup control: FAIL as expected
== 6. control: last word replaced by the reverse complement of the first word (tests the RC constraint) must FAIL
GC weight: every word has exactly 4 letters from {G,C}
distinct: yes
first violation: pair, lines 173 and 521 (ACAGGTGAA, ACGGATGAA): d(x,y)=2 d(x,rc y)=7
NOT a valid (9,3,4)_4 RC+GC edit-metric DNA code
FAIL
rc control: FAIL as expected
== 7. control: one letter of the last word changed so its GC weight is 5 must FAIL
GC weight: 1 words do not have exactly 4 letters from {G,C}, e.g. CGGGTAGTA
distinct: yes
first violation: pair, lines 173 and 521 (ACAGGTGAA, ACGGATGAA): d(x,y)=2 d(x,rc y)=7
NOT a valid (9,3,4)_4 RC+GC edit-metric DNA code
FAIL
gc control: FAIL as expected
== 8. control: the one-word code ACGTACGTA (d(x, rc(x)) = 2 < 3; the RC rule includes x = y) must FAIL
GC weight: every word has exactly 4 letters from {G,C}
distinct: yes
first violation: rc, lines 1 and 1 (ACGTACGTA, ACGTACGTA): d(x,y)=0 d(x,rc y)=2
NOT a valid (9,3,4)_4 RC+GC edit-metric DNA code
FAIL
self control: FAIL as expected
FAIL
exit 1
wall 171 s
```

The corrupted word is within edit distance 2 of another codeword (5 violations found by both methods), so the sha256
check and both exhaustive methods reject it independently, and the controls still fail as they should.

## Cross-check with the family's plain-DP checker (by hand, not part of run_checks.sh)

`nice -n 19 python3 verify-it-yourself/verify_dna_edit_code.py code_n9_d3_k1042.txt 9 3 --expect-size 1042` on a byte
copy of object/code_n9_d3_k1042.txt (same sha256), started 2026-11-03 about 20:51Z on the same machine (load average
about 51); the last line is the exit code and wall time added by the wrapper:

```
file: code_n9_d3_k1042.txt  n=9 d=3 w=floor(n/2)=4  words=1042
format: all 1042 words are length 9 over ACGT
GC weight: every word has exactly 4 letters from {G,C}
distinct: yes
size: 1042 (expected 1042) ok
method A (DP Levenshtein): 542361 distinct pairs, min d(x,y) = 3; 1085764 ordered pairs incl. x=y, min d(x,rc(y)) = 3
method B (edit balls of radii 1 and 1, meet in the middle): 0 violations; method A: 0 violations
methods A and B agree
VALID: 1042 words, a (9,3,4)_4 DNA code with edit distance, fixed GC weight and reverse-complement constraint
PASS
exit 0 wall 169
```

Both checkers agree: 0 violations by all four method runs, min d(x,y) = 3 and min d(x,rc(y)) = 3.
