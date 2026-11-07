# Run It Yourself

## 1. Verify the 600-Cell & 666-File Coordinate Audit in `< 1` Second
From this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
This runs `verify-it-yourself/check_blj_audit.py` using only the Python standard library, recomputing the pairwise binary Lennard-Jones energy from raw 3D coordinates for all 666 coordinate point files stored in `verify-it-yourself/data/blj_all_666_point_files.json.gz`, checking the analytical dimer controls (`E = -1.0` at `r = 2^(1/6)`), verifying the analytical `3N x 3N` Hessian zero-mode threshold (`|lambda| < 1e-6`), and validating every row of `object/blj_600_cell_audit.csv` and `object/blj_all_666_files_reproduction_audit.csv`.

## 2. Inspect the Audit Builder
The script that parses `table.html`, `all.tar`, the 27 live `new` server files, and the 4 hosted improvement archives is located at:
`how-we-built-it/run_lens1.py`
