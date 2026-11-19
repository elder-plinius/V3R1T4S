# Receipts: what `run_checks.sh` checks, and what it cannot

`sh verify-it-yourself/run_checks.sh` runs `check_p3.py`, Python 3 standard library only, no network, a few
seconds. Its last line is `PASS` or `FAIL` and nothing follows it.

## The eight check groups

| # | what it establishes |
|---|---|
| 1 | every file in `object/` matches the sha256 embedded in `check_p3.py`, so a single changed byte fails and the checker stops before quoting any number |
| 2 | the scored set is the bank's: 8,501 positions, each with at least 1 earlier coda in its stream, 5 folds each held out once, every position scored in the fold its rewritten Date belongs to, 96 rewritten-Date groups, 35 CodaType symbols, every scored token inside the vocabulary |
| 3 | every per-position loss is finite and strictly positive |
| 4 | the pooled cross-entropies recomputed from those losses equal `p3_summary.json` for the bigram and the full model, to within 1e-9 |
| 5 | p3's threshold: bigram minus full is at least 0.05 bits, and the gain equals the one the summary records |
| 6 | p3's interval condition: a 10,000-resample paired bootstrap over the 96 rewritten-Date groups, under this checker's own seed `31415926`, gives a 95% interval that excludes 0 |
| 7 | the N3 null reports at least 400 controls with the real gain above all of them, its stated real gain equals the gain recomputed here, and all 400 shipped N3 control gains are below it |
| 8 | the composition-preserving control ships 400 gains and all of them are below the order-only gain the summary records, and that order-only gain is a minority of the claimed gain |

## Expected output

The three summary lines before `PASS`:

```
  full          1.589491 bits per coda over 8501 scored codas
  bigram        1.717914   gain 0.128423  (threshold 0.05, own-seed 95% [lo, hi])
  of that gain, 0.025465 is ordered structure; the rest is order-free stream context
```

The bootstrap interval is computed under the checker's own seed, so it will not be identical to the claim's
[0.087931, 0.162994]; it should be close to it and its lower end must be above 0. That is the point of using a
different seed: the interval is re-derived, not copied.

## What it deliberately does not do

- **It does not refit the model.** Refitting needs the source data, numpy and scipy. `RUN_IT_YOURSELF.md` section
  2 does it in about 2 minutes; this run's REPRODUCE panellist refit everything independently, including a
  separately written smoothed bigram that came out bit-identical to the shipped one, and that verdict is in
  `panel/reproduce.md`.
- **It cannot re-derive the ordered component.** The 0.025465 figure is `full - local`, and the stream-local
  reference's per-position probabilities are not shipped - the probability files are 6.5 MB each, over this
  repository's 1 MB per-file cap. Check group 8 therefore tests that figure against the summary and against all
  400 composition-preserving controls, but takes the figure itself on trust. Section 3 of `RUN_IT_YOURSELF.md`
  regenerates it from the source data. This is the one number in `README.md` that the shipped object cannot
  confirm, and it is the number the "Not claimed" section leans on, so it is called out here rather than buried.
- **It does not re-run any control.** It reads the recorded results and the 800 shipped control gains. Sections 4
  and 5 of `RUN_IT_YOURSELF.md` recompute them.
- **It cannot check the freeze.** Nothing inside a package can. `panel/freeze_audit.md` is this run's own audit
  and states its limit: timestamps show what exists, not what was deleted.
- **It cannot check novelty.** `the-record-we-beat/record.md` records the status source and the one withheld
  competing figure with fetch times; whether anything has appeared since is not knowable from here.

## The corrupted-copy test

The repository's own `check_run.py --package` copies this package, flips one digit in the first text file of
`object/`, and requires `run_checks.sh` to exit non-zero with a last line of exactly `FAIL`. Check group 1 is what
makes that happen: the sha256 of the changed file no longer matches, the checker prints its failures and ends with
`FAIL` and nothing after it.
