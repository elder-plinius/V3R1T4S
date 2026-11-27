# Receipts

Command (from the package folder): `sh verify-it-yourself/run_checks.sh`
Run: 2026-11-21T20:01:12Z, Python 3.13.18

```
degree 36, 37 coefficients, all +-1
Graeffe iterations m = 18; certified lower bound on M(f) about 5.866336 (display only, rounded down by up to a factor 2^(1/2^m))
table value + 1e-9 = 5.823385552581
PASS
```

## Corrupted-copy test (by hand)
kit/check_run.py flips digits and our object has none, so the middle coefficient was flipped instead and the same checker was run on that copy against table value 5.823385551581: last line `FAIL`.
