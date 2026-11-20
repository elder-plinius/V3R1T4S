# Receipts: what `run_checks.sh` checks, and what it cannot

`sh verify-it-yourself/run_checks.sh` runs `check_p4.py`, Python 3 standard library only, no network, a few
seconds. Its last line is `PASS` or `FAIL` and nothing follows it.

## The eight check groups

| # | what it establishes |
|---|---|
| 1 | every file in `object/` matches the sha256 embedded in `check_p4.py`, so a single changed byte fails and the checker stops before quoting any number |
| 2 | the scored set is the bank's: 3,418 positions, each with at least 2 earlier codas in its REC stream, 5 folds each held out once, every position scored in the fold its REC belongs to, per-fold counts equal to `p4_summary.json` |
| 3 | every shipped probability lies strictly inside (0, 1), every label is 0 or 1, and the same-label rate matches the summary |
| 4 | the pooled cross-entropies recomputed from those probabilities equal `p4_summary.json` for the reference, the model and the switch-pattern diagnostic, to within 1e-9 |
| 5 | p4's threshold: reference minus model is at least 0.05 bits |
| 6 | p4's interval condition: a 10,000-resample paired bootstrap over the 188 REC groups, under this checker's own seed `20261119`, gives a 95% interval for the gain that excludes 0 |
| 7 | the switch-pattern-only diagnostic equals the value `README.md` discloses, and the full model beats it |
| 8 | `how-we-built-it/null_test.md` reports at least 400 controls, says the real gain beat all of them, states a real gain equal to the gain recomputed here, and a best control below it |

## Expected output

The three summary lines before `PASS`:

```
  model         0.763112 bits per position over 3418 scored positions
  reference     0.850317   gain 0.087206  (threshold 0.05, own-seed 95% [lo, hi])
  pattern only  0.790864   gain 0.059453  (diagnostic, disclosed, not the claim)
```

The bootstrap interval is computed under the checker's own seed, so it will not be identical to the claim's
[0.064864, 0.116622]; it should be close to it and its lower end must be above 0. That is the point of using a
different seed: the interval is re-derived, not copied.

## What it deliberately does not do

- **It does not refit the model.** Refitting needs the source data, numpy and scipy. `RUN_IT_YOURSELF.md` section
  2 does it in about 40 seconds and should reproduce `object/` byte for byte; this run's REPRODUCE panellist
  refit everything independently and that verdict is in `panel/reproduce.md`.
- **It does not re-run the null controls.** It reads the recorded result. All 400 control gains are shipped in
  `how-we-built-it/null/N4_controls.csv` and `RUN_IT_YOURSELF.md` section 3 recomputes them.
- **It cannot check the freeze.** Nothing inside a package can. `panel/freeze_audit.md` is this run's own audit
  and states its limit: timestamps show what exists, not what was deleted.
- **It cannot check novelty.** `the-record-we-beat/record.md` records the status source and the one competing
  public value with fetch times; whether a better number has appeared since is not knowable from here.

## The corrupted-copy test

The repository's own `check_run.py --package` copies this package, flips one digit in the first text file of
`object/`, and requires `run_checks.sh` to exit non-zero with a last line of exactly `FAIL`. Check group 1 is what
makes that happen: the sha256 of the changed file no longer matches, the checker prints its failures and ends with
`FAIL` and nothing after it.
