# Reproduce report: e757-n21

context: Claude Code subagent, fresh context
role: reproduce

Step 1: shasum -a 256 -c on the contributor's hash list run inside the package folder: every listed file reported OK (0 failures). All work was then done on a private copy of the package folder; no network was used.

## Definition (quoted from the target's success criterion and the claim record, which is not shipped)
"(4,5)-set A of reals (every 4-element subset determines at least five distinct values among its six pairwise absolute differences)". Success criterion items checked here: "(1) Every 4-subset has at least 5 distinct absolute differences, checked exhaustively. (2) The exact maximum Sidon subset size s(A) is certified by two independent exact methods (bitmask branch-and-bound and an ILP that forbids every a+b=c+d, including a=b, i.e. 3-APs) ... (4) s/|A| >= 9/17 ... (6) The checker reproduces s=8 on the Ma-Tang 14-set as a calibration test." Sidon set as used: all sums a+b (a <= b, a=b allowed) pairwise distinct, i.e. no a+b=c+d with {a,b} different from {c,d}, 3-APs included. The claim is the partial win p1: n=21 (not a multiple of 14), s=12, ratio 4/7 equal to (not below) the listed 4/7.

## My checker (written before reading verify-it-yourself/ code; only the calibration JSON was read as input)
My own checker (not shipped in this package): (a) all C(n,4) 4-subsets, count of distinct absolute differences, must be >= 5; (b) the minimal conflict sets (index sets of size 3 or 4 realising a+b=c+d) are derived from all pair sums, and then three exact methods give s(A): (i) exhaustive over all 2^n subsets by superset-closure of the conflict sets in numpy with a popcount maximum; (ii) my own depth-first branch-and-bound with incremental sum sets; (iii) my own ILP (pulp/CBC, one constraint per minimal conflict set, formulated by me). Each returned witness subset is re-checked Sidon by direct pair sums. (c) The ratio is a fractions.Fraction compared with 4/7 and 9/17. (d) Calibration on the Ma-Tang 14-set. (e) A control (the progression 0..4) that must be rejected as (4,5).

## Command and real output
Own checker, run on object/witness_n21_s12.json and verify-it-yourself/calibration_ma_tang.json (its output is shown below):

```
calibration set [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
== Ma-Tang calibration (expect s=8) n 14 distinct True
 4-subsets checked 1001 with <5 distinct differences 0
 exhaustive over all 2^14 subsets: s = 8 ; minimal conflict sets 12 ; #optimal subsets 143 ; witness Sidon: True
 own branch-and-bound: s = 8 witness Sidon: True
 own ILP (CBC): Optimal s = 8 witness Sidon: True
 ratio 4/7 ; <4/7: False ; ==4/7: True ; >=9/17: True ; n%14: 0
object sha256 6478bc3cabcce580910f07fd9e3fee3a15d5b398ba12c9f9f557cfa7af7f2539
== object A n 21 distinct True
 4-subsets checked 5985 with <5 distinct differences 0
 exhaustive over all 2^21 subsets: s = 12 ; minimal conflict sets 19 ; #optimal subsets 1325 ; witness Sidon: True
 own branch-and-bound: s = 12 witness Sidon: True
 own ILP (CBC): Optimal s = 12 witness Sidon: True
 ratio 4/7 ; <4/7: False ; ==4/7: True ; >=9/17: True ; n%14: 7
methods agree: calib True object True
control AP 0..4 (4,5) check: (5, 5)
```

The control line shows (cnt, bad) = (5, 5): all five 4-subsets of the progression fail, so the check does reject non-(4,5) sets.

## Clause-by-clause
- (1) (4,5): all 5985 4-subsets of the 21 distinct integers have >= 5 distinct differences (0 bad): met.
- (2) Exact s(A) = 12 by three independent methods (exhaustive 2^21, branch-and-bound, ILP with status Optimal): met. 1325 distinct subsets of size 12 are Sidon, none of size 13.
- (3) Ratio 12/21 = 4/7 exactly (Fraction): equal to, not below, 4/7. The claim is only the tie/partial win p1, which asks for equality with n not a multiple of 14 (21 mod 14 = 7): reproduced as stated. This role does not judge the live table.
- (4) 4/7 >= 9/17: yes.
- (6) Calibration: the Ma-Tang 14-set is (4,5) and has s = 8 by all three methods (ratio 4/7).
- Item (5) (the blow-up lemma in arXiv:2602.23282) needs the paper and cannot be decided from the saved files; it is not a reproduction clause.
- The object's own reported fields (num_3aps = 19, s = 12, ratio 4/7) agree with my 19 minimal conflict sets (all 3-APs) and s = 12.

## Author's own run (after my checker; PY with pulp as instructed)
```
sha256 matches INDEX.csv (6478bc3cabcce580910f07fd9e3fee3a15d5b398ba12c9f9f557cfa7af7f2539)
== calibration: the Ma-Tang 14-set must give s = 8 (and be a (4,5)-set)
n=14 bad_4_subsets=0 relations=12 s_branch_and_bound=8 s_exhaustive_2^n=8 ratio=4/7 n_multiple_of_14=True ratio<4/7=False ratio==4/7=True ratio>=9/17=True
PASS
== object: n = 21, s = 12 by branch-and-bound and by exhaustive enumeration of all 2^21 subsets
n=21 bad_4_subsets=0 relations=19 s_branch_and_bound=12 s_exhaustive_2^n=12 ratio=4/7 n_multiple_of_14=False ratio<4/7=False ratio==4/7=True ratio>=9/17=True
PASS
== second exact method: ILP (pulp + CBC; needs PY with pulp installed)
ILP: n=14 relations=12 status=Optimal s(A)=8 returned_subset_is_sidon=True PASS
ILP: n=21 relations=19 status=Optimal s(A)=12 returned_subset_is_sidon=True PASS
== negative control: a copy with one element moved to break the (4,5)-property must FAIL
negative control rejected as expected: n=21 bad_4_subsets=1 relations=16 s_branch_and_bound=14 s_exhaustive_2^n=14 ratio=2/3 n_multiple_of_14=False r
ALL CHECKS PASS
```

## Result
No mismatch. Author and skeptic agree on every number.

pass: true
