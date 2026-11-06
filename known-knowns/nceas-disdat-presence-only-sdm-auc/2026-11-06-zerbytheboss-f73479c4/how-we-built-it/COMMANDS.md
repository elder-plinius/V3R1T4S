# Exact Commands Executed

```bash
# 1. Fit presence-only SDM models across all 6 disdat regions and export predictions + species AUCs
python3 how-we-built-it/solve_disdat_sdm.py

# 2. Run the standalone pure-stdlib package verifier
sh verify-it-yourself/run_checks.sh
```
