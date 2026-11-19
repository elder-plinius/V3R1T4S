# Run It Yourself (`ghz-nonlocality-robustness-below-049143`)

## 1. Run the Dual-Enumerator + 55-Digit Interval Verifier

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Calibration checks (mpmath.iv, 55 dps + C++ brute-force vs orbit):
  Mermin 2x2x2 v*       = 0.5
  Impl A & B small-grid = PASS (2x2x2, 6x8x24, 8x12x24, 9x6x18)
Independent exact symmetry-reduced orbit enumerations (18 x 24 x 72):
  Alice C_36 / D_36     = 7286 / 3771 orbits
  Bob C_48              = 349536 orbits
  Orbit pairs checked   = 1318100256 (covering 2^42 = 4,398,046,511,104 strategies)
  Exact L (Impl A, min) = 130692616
  Exact L (Impl B, max) = 130692616
Quantum expectations & critical visibility (mpmath.iv, 55 dps):
  Q_noise               = 0 (exact)
  Q_GHZ                 = [265961302.907030467068957871517, 265961302.907030467068957871517]
  Certified v* interval = [0.4913971114274656713239021, 0.4913971114274656713239021]
  Record beaten         = 0.49143 (arXiv:2310.20677v3 Table III; target <= 0.49142)
PASS
```
