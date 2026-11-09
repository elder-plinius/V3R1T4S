# REPRODUCE skeptic report

context: subagent (fresh context; inputs limited to claim/, no NOTES, attempt reports or REPORT read)

## Definition checked (quoted from claim/claim.md, success criterion (1))
"for every composition (d_1..d_s) of m-t into s non-negative parts the first d_i rows of the C_i together have rank m-t over F_b, checked exhaustively"
Here b=2, m=24, s=17, t=11, so k=m-t=13. The expected number of compositions is C(13+16,16)=67863915.

## What I did
1. I wrote my own F_2 checker in C before reading anything in checkers/. It lives in a scratch dir outside claim/. It parses net_F2_t11_m24_s17.txt (skips '#' lines, splits blocks on blank lines, accepts only 0/1, checks the row length) and enumerates every composition of k into s parts by plain recursion. For each composition it stacks the first d_i rows of every C_i and runs a fresh Gaussian elimination over F_2, with no incremental shortcuts. It counts the compositions and the rank failures.
2. I ran it on net_F2_t11_m24_s17.txt and on net_F2_t11_m24_s17_first13rows.txt with t=11.
3. Controls:
   - Negative control: t=10 (k=14) on the same file.
   - Mutation control: a copy with row 1 of C_2 overwritten by row 1 of C_1, run at t=11.
   - Independent Python re-check of one reported t=10 failing composition.
   - Python check that the first13rows file equals rows 1..13 of each block of the full file.
   - Python rank of each full 24x24 C_i.
4. Only after that did I compute the sha256s and run the author's checkers per REPRODUCE.md. I ran them on a scratch copy of claim/, so claim/ was not modified.

## Hashes
- net_F2_t11_m24_s17.txt c3c441c507605e64d545fb6c6ab57863c7306e8b29dc88bafca22577dfd54618 (matches REPRODUCE.md)
- net_F2_t11_m24_s17_first13rows.txt a4b7187724050c0d657597b5d1b399fd78bd4b8bcb250143f2e9834bc646dbe6 (matches REPRODUCE.md)

## Results: my checker
- net_F2_t11_m24_s17.txt: 17 blocks of 24x24 parsed. t=11, k=13: 67863915 compositions checked, 0 failures, PASS. Count equals C(29,16).
- net_F2_t11_m24_s17_first13rows.txt: 17 blocks of 13 rows parsed. 67863915 checked, 0 failures, PASS. Result is identical.
- first13rows equals the first 13 rows of each C_i in the full file: true.
- Each full C_i has rank 24 over F_2 (nonsingular). This is not needed by the definition and is reported for information only.
- Negative control t=10 (k=14): 145422675 = C(30,16) compositions checked, 1136 failures, FAIL as required. Example failing composition: (0,0,0,0,0,0,0,0,0,0,2,1,1,7,0,3,0). Python independently gives rank 13 < 14 for it.
- Mutation control (corrupted copy, t=11): 13037914 failures, FAIL. The checker detects defects.
- Determinism: the full-file and first13rows runs gave identical counts and verdicts.

## Results: author's checkers (cross-check)
- checkers/netcheck_b.c, args `2 24 17 11`: PASS, compositions_reached=67863915.
- checkers/netcheck_f2.py, args `24 17 11`: PASS, compositions_certified=67863915 expected=67863915.
- checkers/netcheck_b.c, args `2 24 17 10`: FAIL (control, as expected).
- checkers/netcheck_b.c on the mutated copy: FAIL.

## Mismatches
None. My checker and both author checkers agree on PASS at t=11 and FAIL at t=10, and the hashes match.

## Scope
This report covers only criterion (1): the exhaustive rank property and the claimed value t=11 for the saved object. It does not assess criteria (2) to (4): the comparison against the live MinT page and novelty in the literature.

pass: true
