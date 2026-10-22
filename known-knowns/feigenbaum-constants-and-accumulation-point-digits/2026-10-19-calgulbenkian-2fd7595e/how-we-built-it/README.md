# How we built it (quartic Feigenbaum constants)

Code (copied from the contributor's snapshot, nothing changed except that no absolute paths occur):

- `feig_c.c`: a C library (built as a shared library `libfeig_c`) that evaluates the collocation system for the renormalization fixed point in MPFR arithmetic. `test_mpfr.c` is a small link test.
- `solve_feigenbaum.py`: solves the Chebyshev collocation equations for the quartic (z = 4) fixed point and its eigenfunction at N1 = 1070 and N2 = 1100 coefficients with a mixed-precision Newton iteration (double-precision LU in the loop, MPFR residuals), then writes `results/feigenbaum_z4_certificates.json`. The same script also solves the separate logistic and Myrberg accumulation-point problem (the p1 cell of the target); that part is not claimed in this package.
- `polish_feigenbaum.py`: refines the saved z = 4 certificates with further mixed-precision LU steps; its docstring says it raised the agreement from 936 to at least 1070 decimals after the first solve. It overwrites the same JSON file. This JSON file is the object of this package (`object/`, split into six parts of at most 900000 bytes).

Requirements: Python 3 with numpy, scipy and gmpy2 (which needs the GNU MPFR and GMP libraries), and a C compiler. The shared library file `libfeig_c.dylib` is a compiled binary and is not shipped; `solve_feigenbaum.py` expects it next to the script (`LIB_PATH`). The compile command is not recorded in the snapshot.

Commands (inferred from the code, not from a command log): `python3 solve_feigenbaum.py` and then `python3 polish_feigenbaum.py`, both run from a folder that has a `results/` subfolder. Wall time per the script's own comment: a few seconds for the first solve.

No PREREG.md was recorded for this cell: the snapshot of the contributor's workspace holds no pre-registration for it, so none is shipped. The exact command lines of the runs are not recorded either, except where stated below.
