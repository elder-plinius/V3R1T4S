# Exact Commands Executed

```bash
# 1. Run self-contained zero-leakage physical pipeline across all 293 two-band light curves
#    (automatically compiles how-we-built-it/binary_lens_kernel.c on first import)
python3 how-we-built-it/solve_roman_dc18.py \
  --lc-dir data/roman_dc18/lc/lc \
  --out-tsv object/roman_dc18_predictions.tsv \
  --workers 8

# 2. Run standalone verifier
sh verify-it-yourself/run_checks.sh
```
