# REPRODUCE panel report: A054961 a(16) >= 102 (claim/A054961_n16_m102.txt)
context: independent fresh-context REPRODUCE panelist (a knowledgeWork subagent with no prior conversation), working only from the claim folder
reviewed: Thu Oct 22 19:30:23 UTC 2026
verdict: SURVIVES

## Definition (quoted, OEIS A054961 title)
> "Maximal number of binary vectors of length n such that the unions (or bitwise ORs) of any 2 distinct vectors are all distinct."

So a family of m distinct length-n 0/1 vectors witnesses a(n) >= m iff the C(m,2) ORs v_i|v_j (i<j) are pairwise distinct.

## Step 1: own checker, written before opening any .py/.c in the claim folder (scratch directory, mycheck.py)
```python
#!/usr/bin/env python3
# Independent checker for OEIS A054961: "Maximal number of binary vectors of length n
# such that the unions (or bitwise ORs) of any 2 distinct vectors are all distinct."
import sys, hashlib, itertools
def check(path, n):
    raw = open(path, 'rb').read()
    print("sha256", hashlib.sha256(raw).hexdigest())
    lines = raw.decode('ascii').split('\n')
    if lines and lines[-1] == '': lines = lines[:-1]
    for i, s in enumerate(lines):
        if len(s) != n or any(c not in '01' for c in s):
            print("BAD LINE", i+1, repr(s)); return False
    vecs = [int(s, 2) for s in lines]
    m = len(vecs)
    print("lines", m)
    if len(set(vecs)) != m:
        print("DUPLICATE VECTORS"); return False
    seen = {}
    pairs = 0
    for i, j in itertools.combinations(range(m), 2):
        o = vecs[i] | vecs[j]; pairs += 1
        if o in seen:
            print("COLLISION", seen[o], (i+1, j+1), format(o, '0%db' % n)); return False
        seen[o] = (i+1, j+1)
    print("pairs", pairs, "distinct ORs", len(seen), "expected", m*(m-1)//2)
    return len(seen) == m*(m-1)//2
if __name__ == '__main__':
    ok = check(sys.argv[1], int(sys.argv[2]))
    print("RESULT", "VALID" if ok else "INVALID"); sys.exit(0 if ok else 1)
```

Calibration (n=4): pos = {1000,0100,0010,0001} (ORs are the 6 distinct weight-2 vectors); neg = {1100,0011,1110,0001} (1100|0011 = 1111 = 0011|1110); dup = {1000,1000,0100}.
```
$ python3 mycheck.py pos.txt 4   -> lines 4 / pairs 6 distinct ORs 6 expected 6 / RESULT VALID (exit 0)
$ python3 mycheck.py neg.txt 4   -> COLLISION (1, 2) (2, 3) 1111 / RESULT INVALID (exit 1)
$ python3 mycheck.py dup.txt 4   -> DUPLICATE VECTORS / RESULT INVALID (exit 1)
$ python3 mycheck.py claim/A054961_n16_m102.txt 16
sha256 de9e6522f190dbddc1bf2db69e8e1dcf9cb8995e8adc7f5b9a61093b95ffe381
lines 102
pairs 5151 distinct ORs 5151 expected 5151
RESULT VALID
$ sha256sum claim/A054961_n16_m102.txt
de9e6522f190dbddc1bf2db69e8e1dcf9cb8995e8adc7f5b9a61093b95ffe381
$ wc -l claim/A054961_n16_m102.txt   -> 102 (file ends with a single newline; every line exactly 16 chars of 0/1, checked in mycheck.py)
```
Result: sha256 matches the claim; 102 lines, all length-16 0/1; 102 distinct vectors; all 5151 pairwise ORs distinct. The check is exhaustive over all pairs (no sampling). Weight distribution I computed independently: {4: 101, 1: 1}, matching CLAIM.md.

Also with my checker: claim/provenance/parent_W16_n16_m101_s360013.txt -> 101 lines, 5050/5050 distinct ORs, VALID; the regenerated 102-family (regen102) -> 5151/5151, VALID.

## Step 2: CLAIM.md / REPRODUCE.md commands
Run in a fresh copy of the claim folder in a scratch directory, with ../data/ populated from the run's data/ copies (own_n16_m92.txt sha256 43125990...a7f7 matches runs/2026-10-19-1345/claim_a054961_16_92/A054961_n16_m92.txt). Every command in REPRODUCE.md run in order (bash -v); the only change was wrapping each mc2w call as `timeout 1200 env MC2W=4 ./mc2w ...` to cap it. Real output:
```
sha256sum A054961_n16_m102.txt
de9e6522f190dbddc1bf2db69e8e1dcf9cb8995e8adc7f5b9a61093b95ffe381  A054961_n16_m102.txt
python3 check_union.py A054961_n16_m102.txt 16 2
n=16 k=2 m=102 stray_chars=[] lengths_ok=True distinct=True clash=None
VALID
python3 check_indep_stdlib.py A054961_n16_m102.txt 16
n=16 m=102 pairs=5151 distinct_unions=5151
PASS
python3 check_def_both_readings.py A054961_n16_m102.txt 16
file=A054961_n16_m102.txt sha256=de9e6522f190dbddc1bf2db69e8e1dcf9cb8995e8adc7f5b9a61093b95ffe381 n=16 m=102 distinct=True
readingA_exactly2: pairs=5151 distinct_unions=5151 dup=0 -> PASS
readingB_atmost2: objects=5253 distinct=5227 dup=26 -> FAIL
weights={1: 1, 4: 101} fixed_weight=False
column_weights=[27, 25, 21, 24, 24, 27, 26, 25, 25, 23, 26, 26, 25, 28, 28, 25] min=21
strict_containments=26
RESULT PASS
python3 structure_check.py A054961_n16_m102.txt
m=102 n=16
weights: [(1, 1), (4, 101)]
column sums: [27, 25, 21, 24, 24, 27, 26, 25, 25, 23, 26, 26, 25, 28, 28, 25]
max vectors vanishing on 1 coordinate: 81
for t in pos_n8 neg_n8 stray_n8 space_n8; do echo "$t: $(python3 check_union.py selftest_inputs/$t.lines 8 2 | tail -1) | $(python3 check_indep_stdlib.py selftest_inputs/$t.lines 8 | tail -1) | $(python3 check_def_both_readings.py selftest_inputs/$t.lines 8 2>&1 | tail -1)"; done
pos_n8: VALID | PASS | RESULT PASS
neg_n8: INVALID | FAIL | RESULT FAIL
stray_n8: INVALID | FAIL | AssertionError: malformed row
space_n8: INVALID | FAIL | AssertionError: malformed row
echo "oeis_n12_46: $(python3 check_union.py selftest_inputs/oeis_n12_46.lines 12 2 | tail -1) | $(python3 check_indep_stdlib.py selftest_inputs/oeis_n12_46.lines 12 | tail -1) | $(python3 check_def_both_readings.py selftest_inputs/oeis_n12_46.lines 12 | tail -1)"
oeis_n12_46: VALID | PASS | RESULT PASS
python3 extract_selftests.py ../data/emath_poisonall.txt ../data/ws_wolfy-out.txt selftest_inputs
../data/emath_poisonall.txt 6160a150cd0a3e794149f3dd30367280b0abc8bd20ac17a257aed13a4f58d97b OK
../data/ws_wolfy-out.txt f445d27a7c366cc683b26434112bc1ced76f09695623b2c1f8ea8681f9b0e508 OK
wrote 3 files to selftest_inputs
for f in pos_emath_n16_m91 pos_wolfy_n16_m91 neg_emath_n16_m91_dup; do echo "$f: $(python3 check_union.py selftest_inputs/$f.txt 16 2 | tail -1) | $(python3 check_indep_stdlib.py selftest_inputs/$f.txt 16 | tail -1) | $(python3 check_def_both_readings.py selftest_inputs/$f.txt 16 | tail -1)"; done
pos_emath_n16_m91: VALID | PASS | RESULT PASS
pos_wolfy_n16_m91: VALID | PASS | RESULT PASS
neg_emath_n16_m91_dup: INVALID | FAIL | RESULT FAIL
python3 compare_published.py A054961_n16_m102.txt selftest_inputs/pos_emath_n16_m91.txt selftest_inputs/pos_wolfy_n16_m91.txt ../data/own_n16_m92.txt
family A054961_n16_m102.txt m=102 weights=[(1, 1), (4, 101)]
ref selftest_inputs/pos_emath_n16_m91.txt m=91 weights=[(0, 1), (4, 7), (5, 49), (6, 34)] shared_vectors=0
  weight classes where ref has more vectors than family: [(0, 1), (5, 49), (6, 34)] -> family cannot contain any coordinate-permuted copy of ref
ref selftest_inputs/pos_wolfy_n16_m91.txt m=91 weights=[(0, 1), (4, 7), (5, 49), (6, 34)] shared_vectors=0
  weight classes where ref has more vectors than family: [(0, 1), (5, 49), (6, 34)] -> family cannot contain any coordinate-permuted copy of ref
ref ../data/own_n16_m92.txt m=92 weights=[(0, 1), (4, 89), (5, 2)] shared_vectors=6
  weight classes where ref has more vectors than family: [(0, 1), (5, 2)] -> family cannot contain any coordinate-permuted copy of ref
gcc -O2 -o mc2w provenance/mc2w.c -lm
timeout 1200 env MC2W=4 ./mc2w 16 101 900 360013 regen101 | tail -1
FOUND
cmp regen101 provenance/parent_W16_n16_m101_s360013.txt && echo "cmp101: identical"
cmp101: identical
timeout 1200 env MC2W=4 ./mc2w 16 102 120 360014 regen102 regen101 | tail -1
FOUND
cmp regen102 A054961_n16_m102.txt && echo "cmp102: identical"
cmp102: identical

real	1m52.610s
user	1m52.256s
sys	0m0.324s
```
Every line matches the 'Real output' block in REPRODUCE.md (sha256, VALID, PASS, reading A PASS / reading B FAIL as documented, self-tests VALID|PASS|PASS then INVALID|FAIL|FAIL with AssertionError on malformed rows, oeis_n12_46 VALID|PASS|PASS, source sha256 OK, both published 91-families VALID|PASS|PASS, duplicate negative INVALID|FAIL|FAIL, compare_published output identical, both FOUND, cmp101 identical, cmp102 identical).

## Step 3: deterministic regeneration from claim/provenance/mc2w.c
Compiled with gcc -O2 in the fresh copy (above). The 101 rebuild (seed 360013, random start, 900 s wall cap) took about 112 s of CPU here and is byte-identical to claim/provenance/parent_W16_n16_m101_s360013.txt; the 102 rebuild (seed 360014, warm start from regen101) takes about 0.2 s and is byte-identical to claim/A054961_n16_m102.txt. A second independent 102 run also gave a byte-identical file (cmp102 (second run): identical).

## Anything odd
- mc2w.c reads time(0) only as a wall-clock budget cutoff and for log lines (lines 34, 36, 45, 47); the search itself is seeded. So the trajectory is deterministic, but on a much slower machine the 101 run (about 112 s here vs a 900 s cap) could hit the cap and fail to regenerate. Not a correctness issue: the claim rests on the saved file, which I verified directly.
- Reading B (stricter 'at most 2' / singletons too) fails, as CLAIM.md openly says; the OEIS title is reading A (unions of 2 distinct vectors), which my checker implements, and the OEIS n=4 example includes 0000, consistent with reading A.
- CLAIM.md's 91 -> 102 margin (+11) is large; I did not re-check literature or the published record (outside REPRODUCE scope). Upper bound sanity: C(102,2)=5151 <= 2^16, no contradiction.
- The claim folder sits under run directory 2026-10-19-1746 though files are dated 2026-10-22 (close-out date per CLAIM.md); harmless.
- I wrote nothing in the claim folder; its sha256 for A054961_n16_m102.txt was unchanged after the runs.

pass: true
