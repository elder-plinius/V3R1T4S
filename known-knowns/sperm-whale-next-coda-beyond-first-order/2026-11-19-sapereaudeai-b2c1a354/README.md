# Sperm whale turn-taking: partial win p4

Target `sperm-whale-next-coda-beyond-first-order`, partial win **p4**. Run `2026-11-19-0936`.

## What

The claim, exactly as this run's CRITERION panellist worded it and its honesty gate records it in
`panel/gate.md`:

> On the bank's five REC folds of sperm-whale-dialogues.csv (3,418 scored codas), the frozen logistic-regression model, trained on the training folds only and reading only earlier codas of the same REC stream, predicts whether each scored coda carries the same whale label as the previous coda with pooled held-out log-loss 0.7631 bits per coda, 0.0872 bits below a smoothed first-order same-or-switch chain fitted on the pooled training-fold streams (0.8503 bits; additive alpha chosen by inner CV from the R1 grid), with a 95% paired REC-group bootstrap interval of [0.065, 0.117] (10,000 resamples) excluding 0.

To six decimals: model 0.763112 bits per position, reference 0.850317, gain **0.087206**, paired REC bootstrap
[0.064864, 0.116622], and the gain is positive in all five folds. The threshold is 0.05 bits with an interval
excluding zero. All 400 null controls fall below the real gain, the best of them at 0.000947 - a margin of 92.1
times.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Python 3 standard library only, a few seconds, no network. It hashes every file in `object/`, then starts from the
shipped per-position **probabilities** rather than from losses, so it also checks the step from probability to
log-loss. It reconstructs the scored set, recomputes all three pooled cross-entropies, checks p4's threshold, runs
its own 10,000-resample paired REC bootstrap under its own seed (`20261119`, not the claim's), checks the
disclosed switch-pattern diagnostic and reads the null test. Last line is `PASS` or `FAIL`.

`RUN_IT_YOURSELF.md` refits the model from the source data, which needs numpy and scipy and downloads the pinned
CSV from the authors' repository.

## Compared to

| quantity | V3R1T4S draft PR #1175 | this claim |
|---|---|---|
| model, pooled bits per position | 0.780268 | **0.763112** |
| reference, pooled bits per position | 0.850317 | 0.850317 |
| gain | 0.070050 | **0.087206** |
| scored positions | 3,418 | 3,418 |
| filed | 2026-11-19T09:59:53Z | not filed when this package was built |

**#1175 cleared partial win p4 publicly first**, and it did so 4 minutes 42 seconds after this run's
pre-registration freeze at 2026-11-19T09:55:11Z. This claim does not derive from it: the model, the features and
the freeze all predate it, and the run's NOVELTY panellist found it afterwards. On identical positions against an
identical reference this claim is better by 0.017156 bits, with a paired REC bootstrap of the difference of
[0.0034, 0.0334]. **Maintainers can credit this cell only once**, and the first public clearance was #1175's.

The reference is the bank's own comparator for p4: a smoothed first-order same-or-switch chain fitted on the
pooled training-fold streams, its additive alpha chosen by inner cross-validation from the same grid the bank
specifies for R1. Both sides of the comparison are scored on exactly the same 3,418 positions.
`the-record-we-beat/record.md` records the status source with its fetch time, HTTP status and sha256.

## Not claimed

- **Not that turn-taking in sperm whales is a new finding.** WhaleLM already describes whale exchanges as
  predictable, qualitatively; that credit stands and is repeated in `Credits`. What is new here is a number on
  this benchmark's exact binary task, better than the only other public number on it.
- **No composition-preserving control was run for p4.** This run ran one for the content model and for the
  Dominica file - 800 controls, in the full criterion's package - and both passed, but **not for p4**. The p4 null
  (design N4) resimulates labels from pooled first-order transitions, which destroys differences between
  recordings along with the higher-order structure, so "the gain is not explainable by each recording's own switch
  habits" is **not** established here. See `how-we-built-it/null_test.md`.
- **About two thirds of the margin is reachable from the switch pattern alone.** A model seeing only the stream's
  earlier same-or-switch values gains 0.059453 of the 0.087206; the rest comes from the timing, overlap and
  speaker-share features. That diagnostic is below #1175's gain of 0.070050, so #1175's result is not reducible to
  the switch pattern either. The verifier checks this number.
- **Recordings with a single whale label are easy and they are in the pooled figure.** 237 of the 3,418 positions
  sit in recordings where only one whale is labelled, and there the answer is always "same". On the 3,181
  positions in recordings with two or more labels the gain is 0.058957, interval [0.034716, 0.080932] - still
  clearing the threshold, but a third smaller. Both numbers are in `object/p4_summary.json`.
- **Not a refit by this checker.** `verify-it-yourself/` checks the claim's arithmetic and runs its own bootstrap;
  it does not refit. `RUN_IT_YOURSELF.md` does that.
- **Development used folds 2 and 4 only.** On the three folds never touched in development the gain is 0.071140,
  interval [0.044058, 0.103554]. Lower than the pooled figure and still above the threshold.
- **The freeze cannot be proved from inside this package.** `panel/freeze_audit.md` is this run's audit of the
  freeze and states its own limit: file timestamps show what exists, not what was deleted. Note that the per-fold
  gains are uneven - 0.0727, 0.0693, 0.1511, 0.0735, 0.1070 - and the largest is on fold 2, one of the two
  development folds. That is why the three-fold figure above is given.

## Credits

Data and dialogue annotations: Sharma, Gero, Payne, Gruber, Rus, Torralba and Andreas, *Nature Communications*
15:3617 (2024), https://doi.org/10.1038/s41467-024-47221-8, and the authors' repository
https://github.com/pratyushasharma/sw-combinatoriality at pinned commit 7228c8ee.

Prior work on predictable sperm whale turn-taking: WhaleLM, https://doi.org/10.1101/2024.10.31.621071.

Prior public clearance of this exact cell: V3R1T4S draft PR #1175, by another contributor, 2026-11-19.

Built with the V3R1T4S kit at commit 5d2d31e76fe1f4d7eb4b75c7646d06425c10640c. Submitted as SapereAudeAI.
