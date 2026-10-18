# Run It Yourself: Verify and Rebuild `object/sol_m28.json`

## 1. Quick Verification (< 0.1 seconds)

From the root of this package directory:

```bash
sh verify-it-yourself/run_checks.sh
```

Expected final line: `PASS` (`Total violations = 0`, `Total cost = 45873`).

## 2. Rebuild `object/sol_m28.json` from `the-record-we-beat/published_sol_m28.json`

Compile `how-we-built-it/seam_surgery_ihtp.cc` and run with `how-we-built-it/subset_nra_milp.py`:

```bash
clang++ -O3 -std=c++17 how-we-built-it/seam_surgery_ihtp.cc -o seam_surgery_ihtp
./seam_surgery_ihtp verify-it-yourself/m28.json the-record-we-beat/published_sol_m28.json rebuilt_m28.json 8.0 5.0 42
python3 how-we-built-it/subset_nra_milp.py verify-it-yourself/m28.json rebuilt_m28.json rebuilt_m28.json 12 6 42
python3 how-we-built-it/subset_nra_milp.py verify-it-yourself/m28.json rebuilt_m28.json rebuilt_m28.json 40 7 101
python3 how-we-built-it/subset_nra_milp.py verify-it-yourself/m28.json rebuilt_m28.json rebuilt_m28.json 50 8 202
rm -f seam_surgery_ihtp
```
