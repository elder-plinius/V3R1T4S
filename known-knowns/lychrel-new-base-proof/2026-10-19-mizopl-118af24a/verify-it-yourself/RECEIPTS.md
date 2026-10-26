# Verification Receipts (`verify-it-yourself/RECEIPTS.md`)

Command executed:
```sh
sh verify-it-yourself/run_checks.sh
```

Output:
```text
== running check_lychrel.py on object/lychrel_base146_certificate.json ==
=== V3R1T4S Mechanical Lychrel Template-Closure Verifier (Base 146) ===
[1/5] File integrity verified for object/lychrel_base146_certificate.json.
[2/5] Baseline reproduction PASSED: David Seal Base 26 (Period 4, 8 symbolic blocks, brute-forced m=1..500).
[3/5] New Base b=146 PASSED: symbolic all-m closure (8 uniform symbolic blocks), symbolic non-palindromicity, seed entry, and brute-force m=1..500 (|L0|=80, |M0|=6, |T_1(1)|=168).
[4/5] Base 146 orbit simulation + regex matching PASSED: 2,000 steps (t=0..100,000, final length = 1,168 base-146 digits) in 0.03s.
[5/5] Perturbation & null-model controls PASSED (corrupted M0 rejected, non-uniform carry rejected, 0/400 random 168-digit starts).
ALL CHECKS PASSED in 0.35s.
== negative control: a corrupted copy must FAIL ==
negative control rejected as expected (AssertionError: SHA-256 mismatch on lychrel_base146_certificate.json: got 4f40a73e84472b8960ed3c2e9de25accfccad3001c303f484dd0e240bc64f232, expected 118af24a34557dbba72c36eb478019f1f4bed84999e23dc46367c5865ba55945)
ALL CHECKS PASS
```
