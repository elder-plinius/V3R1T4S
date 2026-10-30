# Run It Yourself

Exact commands from this package folder in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Running verification for unit-demand-lottery-vs-item-pricing-gap...
Calibration (CMS n=64): R = 2.164275, R/D = 1.082138 > 1.073 -> PASS
Partial Win p1 (n=8): Exact primal-dual LP = 15/8 = 15/8 with 0 gap -> PASS
Solution Instance (n=50000, S=4.6): R = 2.278139987, D = 2.0, R/D = 1.139069994 > 1+ln(2)/5 by +0.000441 -> PASS
SUCCESS: ALL CHECKS PASSED
PASS
```

To re-run the discovery and derivation scripts from `how-we-built-it/`:
```sh
python3 how-we-built-it/lens1_cms_and_p1.py
python3 how-we-built-it/lens2_discovery_and_certificate.py
```

Requirements:
- Python 3.8+ with `scipy` and standard library modules (`fractions`, `json`, `math`, `os`, `sys`).
