# Run It Yourself

From this package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Running verification for gsp-pure-nash-poa-conjecture...
Calibration 1 (2-slot): ratio = 5/4 (5/4) -> PASS
Calibration 2 (3-slot): ratio = 1.259133 >= 1.259133 -> PASS
Partial Win p2 (n=4): All 24 rankings certified <= 1.259134 (worst case = 1.259133) -> PASS
SUCCESS: ALL CHECKS PASSED
PASS
```

To re-run the full 24-ranking optimization search:
```sh
python3 how-we-built-it/certify_n4_all_24_rankings.py
```
