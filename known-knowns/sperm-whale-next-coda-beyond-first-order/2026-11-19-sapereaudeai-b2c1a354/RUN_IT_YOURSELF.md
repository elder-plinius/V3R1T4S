# Run it yourself

Three levels, cheapest first. Level 1 needs nothing but Python 3. Levels 2 and 3 need the source data, numpy and
scipy.

## 1. Check the shipped object (a few seconds, standard library only)

```sh
sh verify-it-yourself/run_checks.sh
```

This is the check described in `README.md`. It hashes `object/`, rebuilds the scored set, recomputes every pooled
number from the shipped per-position probabilities, checks p4's 0.05-bit threshold, runs its own 10,000-resample
paired REC bootstrap under seed `20261119`, checks the disclosed switch-pattern diagnostic and reads the null
test. Last line `PASS` or `FAIL`. `verify-it-yourself/RECEIPTS.md` lists every check and the expected output.

## 2. Refit the model from the source data (about 40 seconds, needs numpy and scipy)

Fetch the pinned CSV into a `data/csv/` folder beside this one:

```sh
mkdir -p data/csv
curl -L -o data/csv/sperm-whale-dialogues.csv \
  https://raw.githubusercontent.com/pratyushasharma/sw-combinatoriality/7228c8ee/data/csv/sperm-whale-dialogues.csv
```

Expected sha256 `1856c8bf...5da2`, 500,380 bytes, which is the size the bank records. **Do not load the
repository's `.p` files**: unpickling runs code, and the bank says so. The two CSVs hold everything needed.

Then:

```sh
python3 -I how-we-built-it/code/score_p4.py data/csv/sperm-whale-dialogues.csv out
```

The first argument is the CSV, the second an output directory. It prints one line per fold and then the pooled
summary as JSON.

### What the refit should reproduce

| fold | n | reference | model | pattern | C | alpha |
|---|---|---|---|---|---|---|
| 0 | 514 | 0.8664 | 0.7937 | 0.8102 | 0.1 | 1.0 |
| 1 | 1305 | 0.8494 | 0.7801 | 0.8015 | 0.1 | 0.01 |
| 2 | 508 | 0.8835 | 0.7325 | 0.7796 | 0.1 | 1.0 |
| 3 | 692 | 0.7903 | 0.7168 | 0.7470 | 0.1 | 0.01 |
| 4 | 399 | 0.8945 | 0.7875 | 0.8215 | 0.1 | 1.0 |

Pooled: reference 0.8503173539892255, model 0.7631118132162007, pattern 0.7908640718479825, gain
0.08720554077302466 with interval [0.0648638786136118, 0.11662173812015673]. `out/p4_summary.json` should match
`object/p4_summary.json` and `out/p4_per_position.csv` should match `object/p4_per_position.csv` byte for byte.
`object/run_output.txt` is the frozen run's own console output, including the per-fold leakage results.

The leakage self-test runs as part of scoring. On each fold it rewrites every field of the predicted coda and of
every coda after it, re-scores, and reports how many predictions moved: the expected answer is 0 of that fold's
positions - 0 of 3,418 pooled - with a deliberately leaky control feature moving every one of them. Both figures
are the `leak=` field of each line in `object/run_output.txt`.

## 3. Rebuild the null test (about 80 minutes on one core)

```sh
python3 -I how-we-built-it/null/nulls.py N4 data/csv/sperm-whale-dialogues.csv 0 400 nulls/N4_a.csv
```

Design N4 resimulates every stream's whale labels from the pooled first-order same-or-switch chain fitted on the
training folds, then reruns the whole frozen pipeline, all five folds and all inner cross-validation. All 400
control gains as this run computed them are in `how-we-built-it/null/N4_controls.csv`; the design, the command and
what the control does and does not rule out are in `how-we-built-it/null_test.md`. The runner checkpoints each
control and skips indices already present, so the job can be stopped and restarted, and split across workers by
giving each a different index range. The 80-minute figure is derived, not measured: one control is a full
five-fold refit, and the frozen run's own five folds took 12 seconds end to end (`object/run_output.txt`), so 400
controls is about 80 minutes on one core. This run computed them across several workers and did not time a single
worker over the whole range.

## Reading the claim itself

`how-we-built-it/CLAIM.md` is the claim as written during the run, `how-we-built-it/PREREG.md` the
pre-registration frozen at 2026-11-19T09:55:11Z before any held-out score existed, `how-we-built-it/PREREG.v2.md`
the one escape-hatch record (a harness fix on a different lens), `how-we-built-it/REPRODUCE.md` the author's own
reproduction notes and `how-we-built-it/baseline/README.md` the baseline and prior-work survey. `panel/` holds the
three independent skeptic verdicts, the honesty gate and the freeze audit. `prompt/` holds the run prompt and
charter, with the workspace path replaced by a placeholder.
