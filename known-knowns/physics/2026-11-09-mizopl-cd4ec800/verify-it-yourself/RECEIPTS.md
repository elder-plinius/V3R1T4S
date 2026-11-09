# Verification Receipts (`magic-state-stabilizer-rank-exponents`)

## 1. Object & Verifier Hashes

- `object/constructive_witnesses.json` sha256: `cd4ec800e62d15f39a5d2a85d70f0340762a299467bb472c8c6ae70b381bbf24` (`171363` bytes)
- `object/p2_p3_lower_bound_certificates.json` sha256: `f47a7e4538882abaaf86e5d7ddaae8666c862d7952a4c2be6fb19262555a5ed1` (`67031` bytes)
- `verify-it-yourself/verify.py` sha256: `3acbd0e74464bed8cb059b8fdbcbf5178142cfc3ea43cc2178a4fe00efbf856e` (`48564` bytes)

## 2. Clean Verification Run (`sh verify-it-yourself/run_checks.sh`)

```text
$ sh verify-it-yourself/run_checks.sh
[OK] Verified all 10 constructive witnesses (60 QlAb stabilizer terms, 0 integer residual)
[OK] Verified all 4 lower-bound & obstruction certificates from first principles
PASS
```

## 3. Adversarial Corruption Check (`python3 verify-it-yourself/verify.py --corrupt`)

```text
$ python3 verify-it-yourself/verify.py --corrupt
VERIFICATION ERROR: W03_fcat6_s3x3: exact Z[i] decomposition failed on Galois component A
FAIL
(exit code: 1)
```
