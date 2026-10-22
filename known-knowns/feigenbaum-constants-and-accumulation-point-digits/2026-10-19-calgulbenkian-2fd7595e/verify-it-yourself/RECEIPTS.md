# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from the package folder by the packager on 2026-10-19 (python3 3.9.6, Darwin). Wall time about 70 seconds. Exit status 0.

```
== reassemble the object from its 6 numbered parts and check sha256 (whole file first)
whole file sha256 2fd7595e5467256b137eb202bfcfe1ddbae3bc843bb6df1a8b601ea40ecd1ca6 ; PARTS.sha256 says 2fd7595e5467256b137eb202bfcfe1ddbae3bc843bb6df1a8b601ea40ecd1ca6 ; INDEX.csv says 2fd7595e5467256b137eb202bfcfe1ddbae3bc843bb6df1a8b601ea40ecd1ca6 ; parts checked: 6, bad: 0
== z4_check.py: fixed-point and eigenfunction residuals at 1300 digits, two resolutions (about 30 s)
== resolution N1: 1070 Chebyshev coefficients for phi, 1070 for psi
alpha = 1/phi(1) = -1.6903029714052448533437801503241613482282780597095619666824232634497392
fixed-point residuals phi(u)*phi(1) - phi(v) at 31 points: largest in absolute value 1.309e-1092
delta from the eigen-equation at u = 10/31: 7.284686217073343364308930567995553069478046619799790659072121
eigen-equation residuals (L psi)(u) - delta psi(u) at the same 31 points: largest in absolute value -7.682e-1088
  psi(0) = 1.00000000000000000000 ; largest |psi(u)| at the test points 1.000
== resolution N2: 1100 Chebyshev coefficients for phi, 1100 for psi
alpha = 1/phi(1) = -1.6903029714052448533437801503241613482282780597095619666824232634497392
fixed-point residuals phi(u)*phi(1) - phi(v) at 31 points: largest in absolute value -1.264e-1100
delta from the eigen-equation at u = 10/31: 7.284686217073343364308930567995553069478046619799790659072121
eigen-equation residuals (L psi)(u) - delta psi(u) at the same 31 points: largest in absolute value -8.762e-1100
  psi(0) = 1.00000000000000000000 ; largest |psi(u)| at the test points 1.000
== the two resolutions (1070 and 1100 coefficients; the larger is 2.80 % bigger)
|alpha_N1 - alpha_N2| ~ 1e-1086   decimals agreeing: 1085
|delta_N1 - delta_N2| ~ 1e-1085   decimals agreeing: 1084
printed alpha_4_N1 (1100 decimals) vs computed |alpha|: agree to 1e-1100; printed delta_4_N1 vs computed delta: agree to 1e-1088
printed alpha_4_N2 (1100 decimals) vs computed |alpha|: agree to 1e-1101; printed delta_4_N2 vs computed delta: agree to 1e-1100
worst fixed-point residual over both resolutions ~ 1e-1092; worst eigen-equation residual ~ 1e-1088
claimed agreeing decimals: alpha 1085, delta 1082; measured: alpha 1085, delta 1084
Thurlby thesis table 4.6, alpha_4: 330 decimals transcribed; leading characters equal to this computation: 332 of 332
Thurlby thesis table 4.6, delta_4: 324 decimals transcribed; leading characters equal to this computation: 326 of 326
OEIS A195102 data: 49 digits, leading digits equal to |alpha_4| of this computation: 49
alpha_4 = -1.690302971405244853343780150324161348228278059709561966682423...
delta_4 = +7.284686217073343364308930567995553069478046619799790659072121...
elapsed 34.2 s
RESULT PASS
== negative control: one Chebyshev coefficient of the first resolution changed by 1e-900; the check must FAIL
negative control rejected as expected: worst fixed-point residual over both resolutions ~ 1e-900; worst eigen-equation residual ~ 1e-898
ALL CHECKS PASS
```
