# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this folder on 2026-10-18T07:38:46Z (UTC) (Windows, Git Bash, Python 3).

```
== 1 integrity
ok    sha256 of 1082 data files listed in the object (0 mismatches)
== 2 lattice
lattice SSST: vertex configurations ['3^3.4^2', '4^4', '4^4', '3^3.4^2'], fractions {'3^3.4^2': '1/2', '4^4': '1/2'}, zbar 9/2
ok    every vertex is surrounded by unit triangles and squares filling 360 degrees
ok    lattice is (1/2)(3^3,4^2) + (1/2)(4^4), z = 5, 4, zbar = 9/2 (Wikipedia row 23)
ok    stated zbar 4.5
== 3 transfer matrix (frozen extrapolation rule, exact rational arithmetic)
  #23 site: n_max 16, local exponent 4.079, 24 estimates: p_TM 0.57176453954634 sigma_TM 1.042e-07
ok    #23 site TM recomputed equals the stated 0.57176453954634 +- 1.04e-07 (n_max 16)
  #23 bond: n_max 13, local exponent 3.611, 24 estimates: p_TM 0.45844602208062 sigma_TM 3.748e-08
ok    #23 bond TM recomputed equals the stated 0.45844602208062 +- 3.75e-08 (n_max 13)
== 4 Monte Carlo (crossing of the wrapping probabilities, jackknife, L2^-4 fit over L2 >= 16)
  r23_site L64x16 blocks 60  p_L 0.571766140 +- 1.74e-06
  r23_site L96x24 blocks 60  p_L 0.571763300 +- 2.53e-06
  r23_site L128x32 blocks 60  p_L 0.571769000 +- 2.50e-06
  r23_site L192x48 blocks 60  p_L 0.571769524 +- 3.31e-06
  r23_site L256x64 blocks 60  p_L 0.571765487 +- 2.90e-06
  r23_site L512x128 blocks 60  p_L 0.571765755 +- 3.74e-06
  fit L2 >= 16: p_MC 0.571766679 +- 1.39e-06  chi2/dof 3.52/4
ok    site MC recomputed equals the stated 0.571766679 +- 1.393e-06 (sizes [16, 24, 32, 48, 64, 128], blocks [60, 60, 60, 60, 60, 60])
  r23_bond L64x16 blocks 60  p_L 0.458444342 +- 2.19e-06
  r23_bond L96x24 blocks 60  p_L 0.458445911 +- 2.67e-06
  r23_bond L128x32 blocks 60  p_L 0.458443925 +- 2.67e-06
  r23_bond L192x48 blocks 60  p_L 0.458442330 +- 3.28e-06
  r23_bond L256x64 blocks 60  p_L 0.458449176 +- 3.75e-06
  r23_bond L512x128 blocks 60  p_L 0.458446321 +- 4.73e-06
  fit L2 >= 16: p_MC 0.458445217 +- 1.55e-06  chi2/dof 2.26/4
ok    bond MC recomputed equals the stated 0.458445217 +- 1.553e-06 (sizes [16, 24, 32, 48, 64, 128], blocks [60, 60, 60, 60, 60, 60])
  kagome_site L16x16 blocks 60  p_L 0.652701600 +- 1.28e-06
  kagome_site L24x24 blocks 60  p_L 0.652705120 +- 1.76e-06
  kagome_site L32x32 blocks 60  p_L 0.652705118 +- 1.76e-06
  kagome_site L48x48 blocks 60  p_L 0.652702723 +- 2.27e-06
  kagome_site L64x64 blocks 60  p_L 0.652702271 +- 2.22e-06
  kagome_site L128x128 blocks 60  p_L 0.652704116 +- 2.60e-06
  fit L2 >= 16: p_MC 0.652704208 +- 9.89e-07  chi2/dof 2.18/4
ok    kagome MC recomputed equals the stated 0.652704208 +- 9.89e-07 (sizes [16, 24, 32, 48, 64, 128], blocks [60, 60, 60, 60, 60, 60])
== 5 criterion (numeric parts)
ok    stated one-sigma uncertainty 1.04e-07 <= 2e-6
ok    (a) |TM - MC| = 2.140e-06 <= 3 combined sigma 4.190e-06 (1.53 sigma)
ok    (b) |TM - table 0.5720| = 2.355e-04 <= 3 combined sigma
ok    (c) TM bond 0.4584460221 within 1e-6 of the table 0.45844622 (sigma 3.7e-08 <= 1e-7)
ok    (c) MC bond 0.458445217 within 3 sigma of the table (sigma 1.55e-06 <= 2e-6)
ok    (c) MC kagome site 0.652704208 within 3 sigma of 1 - 2 sin(pi/18) = 0.652703645 (0.57 sigma)
== 6 claimed value
ok    claimed 0.57176454 +- 0.00000010 equals the TM value rounded
PASS
```

Wall clock: 0m30.524s.
