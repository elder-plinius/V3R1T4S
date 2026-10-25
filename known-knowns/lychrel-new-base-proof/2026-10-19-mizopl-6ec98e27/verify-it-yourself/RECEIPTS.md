# Verification Receipts (`verify-it-yourself/RECEIPTS.md`)

Command executed:
```sh
sh verify-it-yourself/run_checks.sh
```

Output:
```text
== running check_lychrel.py on object/lychrel_base98_certificate.json ==
=== V3R1T4S Mechanical Lychrel Template-Closure Verifier (Base 98) ===
[1/5] File integrity verified for object/lychrel_base98_certificate.json.
[2/5] Baseline reproduction PASSED: David Seal Base 26 (Period 4, 8 symbolic blocks, brute-forced m=1..500).
[3/5] New Base b= 98 PASSED: symbolic all-m closure (8 uniform symbolic blocks), symbolic non-palindromicity, seed entry, and brute-force m=1..500 (|L0|=37, |M0|=16, |T_1(1)|=92).
[4/5] Base 98 orbit simulation + regex matching PASSED: 2,000 steps (t=0..100,000, final length = 1,092 base-98 digits) in 0.02s.
[5/5] Perturbation & null-model controls PASSED (corrupted M0 rejected, non-uniform carry rejected, 0/400 random 92-digit starts).
ALL CHECKS PASSED in 0.28s.
== negative control: a corrupted copy must FAIL ==
negative control rejected as expected (AssertionError: SHA-256 mismatch on lychrel_base98_certificate.json: got 69f06b7b66167089967e37216c15a4c74c41d26b98a0c92e5d6f9b96606972f9, expected 6ec98e276bfb691187e5ebdb4c8ccf0c149f2754e201e362c15a4a681dbb5256)
ALL CHECKS PASS
```
