# Run It Yourself

## Requirements

- Python 3.8+ (standard library only for the standalone package verifier).
- Runtime: < 2 seconds on a single CPU core; < 25 MB RAM.

## Verification Command

```bash
sh verify-it-yourself/run_checks.sh
```

Expected terminal line: `PASS` (exit code 0). Modifying any digit in `object/moabb_ssvep_within_session_cells.csv` causes `sh verify-it-yourself/run_checks.sh` to print `FAIL` and exit with status 1.

## How to Rebuild the Object from Scratch

To re-run MOABB's `WithinSessionEvaluation` and rebuild `object/moabb_ssvep_within_session_cells.csv` and `verify-it-yourself/data/moabb_ssvep_fold_witness.json.gz` from the public EEG datasets:

```bash
pip install -r how-we-built-it/requirements.txt
PYTHONPATH=how-we-built-it python3 how-we-built-it/export_moabb_witness.py
sh verify-it-yourself/run_checks.sh
```
