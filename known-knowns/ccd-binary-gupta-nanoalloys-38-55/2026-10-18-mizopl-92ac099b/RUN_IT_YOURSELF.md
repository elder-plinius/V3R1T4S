# Run it yourself

## 1. Check the shipped objects

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`. To run the checker alone:

```sh
python3 verify-it-yourself/check_bingupta.py
```

It extracts `object/CuAg_55.rar` via `bsdtar`, verifies that the exact Nunez & Johnston (2010) Gupta parameters reproduce all 56 header energies within `4.890e-09 eV` (`<= 1e-6 eV`), evaluates `object/Cu39Ag16_improved.txt` and all 7 companion improved structures in both `float64` and 30-digit `mpmath` (`mp.dps = 30`), checks that every 30-digit gradient norm is `< 1e-10` (`2.17e-28` on `Cu39Ag16`), computes the exact `165x165` analytical Hessian in `float64` to confirm `6` near-zero modes (`|lambda| < 1e-6`) and `0` negative eigenvalues, and polishes the archive structures in 30-digit `mpmath` to confirm distinct basins (`dE = -1.18984440 eV` on `Cu39Ag16`). The run script also verifies that a corrupted copy of `object/Cu39Ag16_improved.txt` is rejected.

## 2. How the objects were built

`how-we-built-it/` holds the C++ cross-composition template + homotop ILS optimizer (`deep_cuag55.cpp`), the 30-digit `mpmath` polisher and analytical Hessian verifier (`verify_cuag55.py`), and `PREREG.md`.
