# Run it yourself

From this package folder in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

What it does:

1. Creates a throwaway Python venv in a temporary directory (nothing is
   written into this package).
2. Installs `numpy==2.5.4`, `sympy==1.14.0`, `scikit-learn==1.9.1`
   (see `verify-it-yourself/requirements.txt`).
3. Runs `verify-it-yourself/check.py`, which:
   - downloads PMLB dataset 1028_SWD (3 KB) and verifies its sha256;
   - downloads the live results-table pointer and verifies its sha256
     against the value recorded at claim time (proving the table is unchanged);
   - verifies `object/expressions.json` against its sha256 in `INDEX.csv`;
   - re-scores all 30 expressions on their splits (sklearn
     `train_test_split`, train_size 0.75, random_state = each listed seed),
     computing test R^2 and SRBench complexity for each;
   - checks the medians against the claimed values and the bar.

Expected output (last lines):

```
dataset OK: 1000 rows, 10 features, sha256 matches
live table OK: LFS pointer oid matches the recorded table sha256
object integrity OK: expressions.json sha256 matches INDEX.csv
re-scored 30/30 splits: median R2 = 0.3911, median complexity = 75.5
bar check OK: median R2 0.3911 > 0.3800 and median complexity 75.5 <= 3270
PASS
```

Exit code 0 on PASS, 1 on FAIL. Rough time: 2 to 4 minutes on a laptop,
mostly the one-time installs. The full real output of a run is saved in
`verify-it-yourself/RECEIPTS.md`.

## How to rebuild the object

The object was produced by the code in `how-we-built-it/`:

1. Get the dataset: download
   `https://github.com/EpistasisLab/pmlb/raw/master/datasets/1028_SWD/1028_SWD.tsv.gz`
   (sha256 `b0526495039ad62169c52a9cf34a957f16b1d02cab995746d3098bbdbfa951cc`)
   and the SRBench table `results.feather` from the `srbench_2025` branch.
2. Lay the files out as the original run did: the checker as `code/check_srbench.py`,
   the lens code as `attempts/smuggler/code/distill_sr.py` (which imports the
   dictionary code from `attempts/constructor/code/dict_sr.py`), the dataset
   and table under `runs/data/`, and the frozen rule as `PREREG.v2.md`.
   See `how-we-built-it/COMMANDS.md` for the exact commands.
3. Run the smuggler lens over the 30 listed seeds; it writes the 30
   expressions and their scores. Re-scoring the saved expressions with the
   verifier above reproduces median R^2 0.3911 and median complexity 75.5.
