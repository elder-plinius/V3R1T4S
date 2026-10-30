# Verification Receipts (`ccd-dzugutov-zetterling-polytetrahedral-clusters`)

## 1. Command & Exact Output (`sh verify-it-yourself/run_checks.sh`)

```text
$ sh verify-it-yourself/run_checks.sh
  [Calib] Dzugutov  : 12/12 point files verified via live URLs & SHA-256 (max |dE| = 4.587e-07 < 1e-6)
  [Calib] mDzugutov : 12/12 point files verified via live URLs & SHA-256 (max |dE| = 4.797e-07 < 1e-6)
  [Calib] Z1        : 12/12 point files verified via live URLs & SHA-256 (max |dE| = 4.761e-07 < 1e-6)
  [Calib] Z2        : 12/12 point files verified via live URLs & SHA-256 (max |dE| = 4.669e-07 < 1e-6)
[1/3] 48 calibration point files and 502-Cluster CCD Audit verified: 502/502 reproduced within < 1e-6 (max |dE| = 9.953e-7); 5 corrupted Z1/Z2 origin files verified.
  [01/20] mDzugutov_74  | E_new = -180.9875532166 | E_CCD =  -180.982763 | dE =  -0.004790 | ||g||_f64 = 1.09e-13 | ||g||_55d = 5.43e-34 | Hessian: PASS
  [02/20] mDzugutov_134 | E_new = -343.3900404390 | E_CCD =  -343.386067 | dE =  -0.003973 | ||g||_f64 = 1.84e-13 | ||g||_55d = 7.74e-34 | Hessian: PASS
  [03/20] mDzugutov_177 | E_new = -462.5826604786 | E_CCD =  -462.579581 | dE =  -0.003079 | ||g||_f64 = 2.57e-13 | ||g||_55d = 9.14e-34 | Hessian: PASS
  [04/20] mDzugutov_241 | E_new = -641.7941625208 | E_CCD =  -641.793084 | dE =  -0.001079 | ||g||_f64 = 3.25e-13 | ||g||_55d = 1.04e-33 | Hessian: PASS
  [05/20] Z1_38         | E_new = -100.1301837463 | E_CCD =   -99.874893 | dE =  -0.255291 | ||g||_f64 = 1.72e-13 | ||g||_55d = 9.24e-34 | Hessian: PASS
  [06/20] Z1_42         | E_new = -111.1739767527 | E_CCD =  -111.113917 | dE =  -0.060060 | ||g||_f64 = 2.19e-13 | ||g||_55d = 8.63e-34 | Hessian: PASS
  [07/20] Z1_44         | E_new = -116.8727164354 | E_CCD =  -116.579062 | dE =  -0.293654 | ||g||_f64 = 2.61e-13 | ||g||_55d = 9.31e-34 | Hessian: PASS
  [08/20] Z1_54         | E_new = -146.3500928888 | E_CCD =  -146.333923 | dE =  -0.016170 | ||g||_f64 = 2.49e-13 | ||g||_55d = 1.13e-33 | Hessian: PASS
  [09/20] Z1_65         | E_new = -176.4054458998 | E_CCD =  -176.220446 | dE =  -0.185000 | ||g||_f64 = 3.44e-13 | ||g||_55d = 1.21e-33 | Hessian: PASS
  [10/20] Z1_67         | E_new = -182.6367678185 | E_CCD =  -182.418355 | dE =  -0.218413 | ||g||_f64 = 3.48e-13 | ||g||_55d = 1.45e-33 | Hessian: PASS
  [11/20] Z1_68         | E_new = -185.3634223842 | E_CCD =  -185.275450 | dE =  -0.087972 | ||g||_f64 = 3.56e-13 | ||g||_55d = 1.44e-33 | Hessian: PASS
  [12/20] Z1_74         | E_new = -202.8773603525 | E_CCD =  -202.558045 | dE =  -0.319315 | ||g||_f64 = 3.66e-13 | ||g||_55d = 1.29e-33 | Hessian: PASS
  [13/20] Z1_75         | E_new = -205.8062213765 | E_CCD =  -205.448065 | dE =  -0.358156 | ||g||_f64 = 3.71e-13 | ||g||_55d = 1.43e-33 | Hessian: PASS
  [14/20] Z1_76         | E_new = -208.6187854827 | E_CCD =  -208.375341 | dE =  -0.243444 | ||g||_f64 = 3.81e-13 | ||g||_55d = 1.30e-33 | Hessian: PASS
  [15/20] Z2_35         | E_new =  -92.2845205483 | E_CCD =   -92.270480 | dE =  -0.014041 | ||g||_f64 = 3.10e-13 | ||g||_55d = 9.46e-34 | Hessian: PASS
  [16/20] Z2_43         | E_new = -113.9462385534 | E_CCD =  -113.534760 | dE =  -0.411479 | ||g||_f64 = 3.47e-13 | ||g||_55d = 1.08e-33 | Hessian: PASS
  [17/20] Z2_56         | E_new = -149.2304029120 | E_CCD =  -148.936593 | dE =  -0.293810 | ||g||_f64 = 4.41e-13 | ||g||_55d = 1.41e-33 | Hessian: PASS
  [18/20] Z2_59         | E_new = -157.2398070630 | E_CCD =  -157.230650 | dE =  -0.009157 | ||g||_f64 = 4.15e-13 | ||g||_55d = 1.42e-33 | Hessian: PASS
  [19/20] Z2_69         | E_new = -184.6267084482 | E_CCD =  -184.286813 | dE =  -0.339895 | ||g||_f64 = 4.85e-13 | ||g||_55d = 1.24e-33 | Hessian: PASS
  [20/20] Z2_80         | E_new = -214.1928466438 | E_CCD =  -213.815040 | dE =  -0.377807 | ||g||_f64 = 6.76e-13 | ||g||_55d = 1.31e-33 | Hessian: PASS
[2/3] All 20 new putative global minima verified in float64 and 55-digit Decimal (including 3 mDzugutov records in N=101..250 satisfying p1).
[3/3] All 20 analytical 3N x 3N Hessians certified: 6 zero modes (< 1e-6) and 0 negative modes (Cholesky SPD on 3N-6 vibrational subspace with lambda_7 > 0.20).
PASS: ccd-dzugutov-zetterling-polytetrahedral-clusters verification complete.
```

## 2. Artifact Checksum

- `object/dzugutov_zetterling_20_records_and_502_audit.json`:
  - Size: `977,760` bytes
  - SHA-256: `3797a33831b0b1ff9bfd5e14964e32ec0ce2d2b39b5f5f42d7909f59a5900b96`
