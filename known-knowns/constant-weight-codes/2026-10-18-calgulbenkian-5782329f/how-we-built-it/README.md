# How this object was built

Source: the contributor's snapshot of its working folder `cwc` (taken 2026-10-18T17:35:35Z), copied here as `PREREG.md` (the pre-registration, frozen before the run) and `RESULTS.md` (the run's results table covering all of its constant-weight-code goals; the row for this claim is "Family A2", cell A(35,14,14), certified value 837). Local absolute paths in these two files were replaced by `{WORKDIR}`.

## What the snapshot does and does not contain

- It documents the method: Family A2 of the pre-registration, a pure Delsarte linear program of the Johnson scheme (constraints D1 to Dw only, no table inputs), solved in exact rational arithmetic with Python `fractions.Fraction`, for cells with n above 28 whose upper bound the live table does not print.
- The LP-building and solving source code is NOT in the snapshot. The snapshot holds only the code-search program (`cwc_search.c`, for lower-bound codes, which this claim does not use) and the contributor's own verifier (not copied here). The exact commands that built this certificate are therefore not recorded.
- What is recorded is the certificate itself: `object/` holds the LP optimum, the active constraints with their coefficients, and the dual values, so anyone can re-derive the same linear program from the definition and compare.
- Not copied, on purpose: the contributor's verifier script, binaries, the saved copy of the third-party table page (`data/`) and the reference folder (`ref/`).
