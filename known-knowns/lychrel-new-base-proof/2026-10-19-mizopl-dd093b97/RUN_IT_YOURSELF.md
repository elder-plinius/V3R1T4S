# Run It Yourself (`lychrel-new-base-proof`)

## One-line check

From the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

This runs `verify-it-yourself/check_lychrel.py` on `object/lychrel_base50_certificate.json`, and then tests a corrupted copy of `object/lychrel_base50_certificate.json` to confirm that any tampering is rejected. Expected last line: `ALL CHECKS PASS`.

## Direct Python verification

```sh
python3 verify-it-yourself/check_lychrel.py object/lychrel_base50_certificate.json
```

Expected output (~16 seconds, matching `verify-it-yourself/RECEIPTS.md`):
```text
=== V3R1T4S Mechanical Lychrel Template-Closure Verifier (Base 50) ===
[1/5] File integrity verified for object/lychrel_base50_certificate.json.
[2/5] Baseline reproduction PASSED: David Seal Base 26 (Period 4, 8 symbolic blocks, brute-forced m=1..500).
[3/5] New Base b= 50 PASSED: symbolic all-m closure (8 uniform symbolic blocks), symbolic non-palindromicity, seed entry, and brute-force m=1..500 (|L0|=36, |M0|=8, |T_1(1)|=82).
[4/5] Base 50 orbit simulation + regex matching PASSED: 100,000 steps (t=0..100,000, final length = 50,082 base-50 digits) in 15.77s.
[5/5] Perturbation & null-model controls PASSED (corrupted M0 rejected, non-uniform carry rejected, 0/400 random 82-digit starts).
ALL CHECKS PASSED in 15.86s.
```
