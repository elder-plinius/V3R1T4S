# Run it yourself

From this package folder in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

What it does:

1. Creates a throwaway Python venv in a temporary directory (nothing is written into this package).
2. Installs `numpy==2.5.4`, `sympy==1.14.0`, `scikit-learn==1.9.1` (see `verify-it-yourself/requirements.txt`).
3. Runs `verify-it-yourself/check.py`, which:
   - downloads PMLB dataset 522_pm10 (12 KB) and verifies its sha256;
   - downloads the live results-table pointer and verifies its sha256 against the value recorded at claim time (proving the table is unchanged);
   - verifies `object/expressions.json` against its sha256 in `INDEX.csv`;
   - re-scores all 30 expressions on their splits (sklearn `train_test_split`, train_size 0.75, random_state = each listed seed), computing test R^2 and SRBench complexity for each;
   - checks the medians against the claimed values and the bar.

Expected output (last lines):

```
dataset OK: 500 rows, 7 features, sha256 matches
live table OK: LFS pointer oid matches the recorded table sha256
object integrity OK: expressions.json sha256 matches INDEX.csv
re-scored 30/30 splits: median R2 = 0.3313, median complexity = 145.5
bar check OK: median R2 0.3313 > 0.3009 and median complexity 145.5 <= 4996.5
PASS
```

Exit code 0 on PASS, 1 on FAIL. Rough time: 2 to 4 minutes on a laptop, mostly the one-time installs. The full real output of a run is saved in `verify-it-yourself/RECEIPTS.md`.

## How to rebuild the object

The object was produced by the code in `how-we-built-it/`:

1. Get the dataset: download `https://github.com/EpistasisLab/pmlb/raw/master/datasets/522_pm10/522_pm10.tsv.gz` (sha256 `ecbabaa5a989a8c11f5a57e874c135f386da5379d6689ae6d5d4264a652fa5e0`) and the SRBench table `results.feather` from the `srbench_2025` branch (sha256 `5b428264a346f6bbbeabded219f87454b9206afa70c19c012075c672533f342e`). You also need SRBench's `symbolic_utils.py` and `read_file.py` from the same branch (the checker imports them for the complexity count).
2. Lay the files out as the original run did: the checker as `code/check_srbench.py`, the lens code as `attempts/smuggler/code/gam_sr.py`, the dataset and table under `runs/data/`, and the frozen rule as `PREREG.md`. See `how-we-built-it/COMMANDS.md` for the exact commands.
3. Run the smuggler lens over the 30 listed seeds; it writes the 30 expressions and their scores. Re-scoring the saved expressions with the verifier above reproduces median R^2 0.3313 and median complexity 145.5.
