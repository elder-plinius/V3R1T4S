# Run It Yourself — ecc-inversion-addition-chains

Exact reproduction commands from this folder in a fresh shell.

## 1. Fast Standalone Verification (< 1 second)
Run the pure Python verifier from this package folder:
```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```
VERIFICATION COMPLETE: 20/20 chains algebraically certified.
Secondary curve wins (p1): 2 (M-383: 395 < 396; M-511: 524 < 525)
Main curve improvements:    2 (Curve25519 Field: 265 < 266; NIST P-384 Field: 396 < 397)
ALL CHECKS PASSED.
PASS
```

## 2. Rebuilding the Chains from Scratch
To run the addition chain generator in Python:
```sh
cd how-we-built-it
python3 generate_chains.py
```
Execution time: ~2 seconds.
Generates all 20 addition chains and verifies Fermat tests across all curves.
