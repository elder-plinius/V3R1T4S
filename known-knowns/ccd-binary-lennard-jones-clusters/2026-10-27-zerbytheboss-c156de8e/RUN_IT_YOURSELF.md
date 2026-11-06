# Run It Yourself

## 1. Verify object/blj_600_cell_audit.csv in < 0.5 Seconds
From this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
This runs `verify-it-yourself/check_blj_audit.py`, validating the entire 600-cell audit table, checking the dimer analytical controls (E = -1.0 at r=2^(1/6)), verifying that all 576 posted files reproduce their posted energies to within 1e-5, and confirming that the 101 updated minima cells are cataloged correctly.

## 2. Inspect the Lens 1 Audit Engine
The recomputation script that parsed the Cambridge Cluster Database archive is located in:
`how-we-built-it/run_lens1.py`
