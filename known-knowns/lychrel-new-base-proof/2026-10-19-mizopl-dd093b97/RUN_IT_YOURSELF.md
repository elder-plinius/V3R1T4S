# Run It Yourself (`lychrel-new-base-proof`)

## One-line check

From the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

This runs `verify-it-yourself/check_lychrel.py` on `object/` and `the-record-we-beat/`, and then tests a corrupted copy of `object/lychrel_base50_certificate.json` to confirm that any tampering is rejected. Expected last line: `ALL CHECKS PASS`.

## Direct Python verification

```sh
python3 verify-it-yourself/check_lychrel.py object the-record-we-beat
```

Expected output (~16 seconds):
```text
[1/6] Baseline reproduction PASSED: David Seal Base 26 (Period 4, 8 symbolic blocks, brute-forced m=1..500).
[2/6] New Base b= 50 PASSED: symbolic all-m closure (8 uniform symbolic blocks), symbolic non-palindromicity, seed entry, and brute-force m=1..500 (|L0|=36, |M0|=8, |T_1(1)|=82).
[2/6] New Base b= 98 PASSED: symbolic all-m closure (8 uniform symbolic blocks), symbolic non-palindromicity, seed entry, and brute-force m=1..500 (|L0|=37, |M0|=16, |T_1(1)|=92).
[2/6] New Base b=146 PASSED: symbolic all-m closure (8 uniform symbolic blocks), symbolic non-palindromicity, seed entry, and brute-force m=1..500 (|L0|=80, |M0|=6, |T_1(1)|=168).
[3/6] Base 50 orbit simulation + regex matching PASSED: 100,000 steps (t=0..100,000, final length = 50,082 base-50 digits) in 15.77s.
[4/6] Kuitche (2023) mechanical audit PASSED across all bases b=3..10.
[5/6] File integrity and Wikipedia status snapshot verified.
[6/6] Perturbation & null-model controls PASSED (0/400 random 82-digit starts).
ALL CHECKS PASSED in 16.33s.
```
