# Verification receipts

Command run from the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Output:

```text
sha256 matches INDEX.csv (92ac099b6963dcaedd5dbc1000731a5a87c99fc6e208b30475c6850e420a991d)
== check_bingupta.py on object/
[PASS] Step 1 (Archive Calibration): 56/56 files in CuAg_55.rar verified; max |E_eval - E_header| = 4.890e-09 eV (<= 1.0e-06 eV)

Step 2 (30-digit mpmath evaluation, gradient norm, 165x165 analytical Hessian, and distinct-basin polish check):
  [PASS] Cu39Ag16 (Cu=39, Ag=16) | E_arch= -162.61229825 | E_arch_pol= -162.61229825 | E*= -163.80214265 | dE= -1.18984440 eV | |g|_mp30=2.17e-28 | zero_modes=6 (max 2.51e-15) | neg_modes=0 | lambda_7=0.6999
  [PASS] Cu34Ag21 (Cu=34, Ag=21) | E_arch= -160.81218484 | E_arch_pol= -160.81218484 | E*= -161.76692486 | dE= -0.95474003 eV | |g|_mp30=6.34e-23 | zero_modes=6 (max 2.43e-15) | neg_modes=0 | lambda_7=0.7141
  [PASS] Cu33Ag22 (Cu=33, Ag=22) | E_arch= -160.43136967 | E_arch_pol= -160.43136967 | E*= -161.35336662 | dE= -0.92199695 eV | |g|_mp30=4.52e-23 | zero_modes=6 (max 2.34e-15) | neg_modes=0 | lambda_7=0.7338
  [PASS] Cu31Ag24 (Cu=31, Ag=24) | E_arch= -159.69487106 | E_arch_pol= -159.69487106 | E*= -160.49285973 | dE= -0.79798867 eV | |g|_mp30=1.56e-26 | zero_modes=6 (max 2.45e-15) | neg_modes=0 | lambda_7=0.7294
  [PASS] Cu22Ag33 (Cu=22, Ag=33) | E_arch= -156.38507389 | E_arch_pol= -156.38507389 | E*= -156.61674699 | dE= -0.23167311 eV | |g|_mp30=7.04e-26 | zero_modes=6 (max 2.04e-15) | neg_modes=0 | lambda_7=0.7790
  [PASS] Cu20Ag35 (Cu=20, Ag=35) | E_arch= -155.56958143 | E_arch_pol= -155.56958143 | E*= -155.69839654 | dE= -0.12881511 eV | |g|_mp30=4.53e-24 | zero_modes=6 (max 2.17e-15) | neg_modes=0 | lambda_7=0.7775
  [PASS] Cu15Ag40 (Cu=15, Ag=40) | E_arch= -153.49887624 | E_arch_pol= -153.49887624 | E*= -153.62512358 | dE= -0.12624733 eV | |g|_mp30=2.89e-28 | zero_modes=6 (max 2.41e-15) | neg_modes=0 | lambda_7=0.2414
  [PASS] Cu17Ag38 (Cu=17, Ag=38) | E_arch= -154.40077125 | E_arch_pol= -154.40077125 | E*= -154.46534927 | dE= -0.06457801 eV | |g|_mp30=2.57e-28 | zero_modes=6 (max 1.30e-15) | neg_modes=0 | lambda_7=0.2504

ALL CHECKS PASSED (CONFIRMED_SOLUTION on Cu39Ag16 with dE = -1.18984440 eV and 7 additional CuAg55 compositions).
== negative control: a corrupted copy must FAIL
negative control rejected as expected (FAIL: Cu39Ag16 30-digit header energy mismatch vs coordinate evaluation)
ALL CHECKS PASS
```
