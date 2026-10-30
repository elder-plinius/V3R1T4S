# Reproduction Guide: Partial Win (p2)

This reproduction dual-verifies all four certificates in $< 10$ seconds.

## Quick Dual Verification
Run the unified verification script from the run directory:
```bash
python3 claim/verify.py
```

Expected output:
```
======================================================================
MINIMUM COMPARISON SELECTION (n=18): DUAL CHECKER VERIFICATION
======================================================================
[PASS] (18, 9) 34 cmp: Cremer checker ACCEPT, Pathcheck exact_worst=34
       Beats GKP Table 3 (37) by 3 cmp; beats Hadian-Sobel (41) by 7 cmp
[PASS] (18, 8) 35 cmp: Cremer checker ACCEPT, Pathcheck exact_worst=35
       Beats GKP Table 3 (37) by 2 cmp; beats Hadian-Sobel (38) by 3 cmp
[PASS] (18, 7) 34 cmp: Cremer checker ACCEPT, Pathcheck exact_worst=34
       Beats GKP Table 3 (35) by 1 cmp; beats Hadian-Sobel (35) by 1 cmp
[PASS] (18, 6) 31 cmp: Cremer checker ACCEPT, Pathcheck exact_worst=31
       Beats GKP Table 3 (32) by 1 cmp; beats Hadian-Sobel (32) by 1 cmp
======================================================================
VERIFICATION RESULT: ALL CHECKS PASSED (CLAIM p2 CONFIRMED)
======================================================================
```

## Step-by-Step Manual Verification

### 1. Verify (18, 9) Certificate (worst=34 comparisons)
```bash
python3 -I code/verifier/verify_rs_algorithm.py \
  certificates/select_9th_of_18_34cmp.rs \
  --expect-n 18 --expect-i 9 --expect-worst 34

python3 -I code/independent_checks/checker/pathcheck.py \
  certificates/select_9th_of_18_34cmp.rs
```

### 2. Verify (18, 8) Certificate (worst=35 comparisons)
```bash
python3 -I code/verifier/verify_rs_algorithm.py \
  certificates/select_8th_of_18_35cmp.rs \
  --expect-n 18 --expect-i 8 --expect-worst 35

python3 -I code/independent_checks/checker/pathcheck.py \
  certificates/select_8th_of_18_35cmp.rs
```

### 3. Verify (18, 7) Certificate (worst=34 comparisons)
```bash
python3 -I code/verifier/verify_rs_algorithm.py \
  certificates/select_7th_of_18_34cmp.rs \
  --expect-n 18 --expect-i 7 --expect-worst 34

python3 -I code/independent_checks/checker/pathcheck.py \
  certificates/select_7th_of_18_34cmp.rs
```

### 4. Verify (18, 6) Certificate (worst=31 comparisons)
```bash
python3 -I code/verifier/verify_rs_algorithm.py \
  certificates/select_6th_of_18_31cmp.rs \
  --expect-n 18 --expect-i 6 --expect-worst 31

python3 -I code/independent_checks/checker/pathcheck.py \
  certificates/select_6th_of_18_31cmp.rs
```
