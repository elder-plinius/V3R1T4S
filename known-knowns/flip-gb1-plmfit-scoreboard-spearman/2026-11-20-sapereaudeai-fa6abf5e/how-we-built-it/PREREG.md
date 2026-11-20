# PREREG - run 2026-11-20-0535

frozen: 2026-11-20T05:36:42Z (from `date -u`, printed in `out/start_time.txt` and the shell transcript)

null_test: not needed because this run computes no search and makes no "beats chance" claim: it scores two
fully-specified, previously recorded model configurations with a deterministic checker against a table value
(`scipy.stats.spearmanr` against the released file's own `score` column, compared with the PLMFit scoreboard's
0.8791). There is no key, period, language or structure detection anywhere in it.

## 1. What this run is

This run is a **test of a selection criterion, not a search.** It fits exactly two configurations, both recorded
before this run began, and scores them once. No grid is searched, no model family is extended, no hyperparameter
is tuned, no fourth-order block is added, and nothing is selected using any number produced this run.

## 2. The two configurations, verbatim from the sealed file

Copied from `data/UNSCORED-PREDICTION-as-sealed.md` (sha256
`e1adf72c2eaed4e7008b06846bd29ab10172694103cbff1195ac969d1f431da5`), a verbatim copy of
`runs/2026-11-20-0215/claim/UNSCORED-PREDICTION.md`, whose table reads:

| fit set | extrapolation fold | the criterion's pick | extrapolation rho |
|---|---|---|---|
| all (2,990 rows) | 424 -> 2,566 | `s2=0.5 s3=0.25 alpha=0.03`, squared error on `log(y+0.001)` | 0.797099 |
| trainonly (2,691 rows) | 384 -> 2,307 | `s2=1 s3=1 alpha=0.001`, squared error on `log(y+0.01)` | 0.777742 |

In the code's own notation, and cross-checked against
`runs/2026-11-20-0215/claim/extrap_select.out`'s two `WOULD SELECT:` lines:

- **A (fit set `all`)**: `s2=0.5, s3=0.25, alpha=0.03, objective=ls, transform=log0.001`, fitted on the 2,990
  rows whose `three_vs_rest` value is `train` or `validation`.
- **B (fit set `trainonly`)**: `s2=1, s3=1, alpha=0.001, objective=ls, transform=log0.01`, fitted on the 2,691
  rows whose `three_vs_rest` value is `train`.

Nothing else about either model may change: the kernel is
`K(i,j) = m + s2^2*C(m,2) + s3^2*C(m,3)` with `m` the number of the four sites at which two sequences agree, the
solver is the centred dual ridge of `code/gb1k.py` (`ridge_dual`), and the prediction is
`mean(transform(y_fit)) + k_te @ ridge_dual(...)`, exactly as `refit_predict` in run 2026-11-20-0215's `attack.py`
computes it for an `ls` configuration.

## 3. Honouring the sealed file's own caveat

The sealed file states that row A is only **nearly** sealed: its author knew the kernel shape `(0.5, 0.25)` was
the earlier run's winner and had scored 0.900143 / 0.901307, and A is the same shape and penalty with a different
target-transform offset. Row B is the genuinely clean out-of-sample test. This run reports both and **rests every
conclusion on B**. Row A is never described as sealed.

## 4. Seeds, and the determinism statement made in advance

Seeds **1, 2, 3** for each configuration, passed on the command line, giving six prediction files. The seed is
used to initialise `numpy.random.default_rng(seed)` and `sklearn KFold(shuffle=True, random_state=seed)` inside
the program, exactly as before.

**Prediction, registered now:** because the configuration is given rather than selected, nothing in the fit is
random, so the three seeds will produce **identical** predictions and the seed-to-seed standard deviation will be
exactly 0. That is declared here so it cannot later be dressed up as a finding, and no seed-to-seed variation will
be manufactured to fill the bank's "at least three seeds" wording. The program prints the sha256 of each
prediction file so the identity is checkable; if the sha256s were to differ, that would be a bug and would be
reported as one.

## 5. The statistic, and the thresholds

- Spearman: `scipy.stats.spearmanr(y_test, prediction).statistic`, with `y_test` the released file's own `score`
  column for the 5,743 rows whose `three_vs_rest` value is `test`, in the file's own row order.
- Coverage gate: a prediction file must cover each of those 5,743 sequences exactly once, with no duplicates and
  no extras, or it is not scored.
- Three-seed mean and standard deviation (both `ddof=0` and `ddof=1` are printed).
- **Bootstrap interval of the mean**, 10,000 resamples, `numpy.random.default_rng(0)`: each resample draws 5,743
  test-row indices with replacement, computes the Spearman of each of the three seeds' predictions on that same
  resample, averages the three, and the interval is the 2.5th and 97.5th percentiles of those 10,000 means. This
  is the interval p2 asks for ("a bootstrap 95% interval" on a result reported as a three-seed mean). A per-seed
  interval is also printed for information, but **no per-seed gate is imposed**: run 2026-11-20-0215's CRITERION
  skeptic ruled that reading to be self-invented strictness, and the bank's text is read here in its most
  favourable fair sense.
- Thresholds, fixed now:
  - **p2**: three-seed mean > 0.8791 **and** the mean's bootstrap 95% interval entirely above 0.8791.
  - **full win**: three-seed mean >= 0.8791 + 0.02 = **0.8991**, the mean's bootstrap interval excluding 0.8791,
    **and** strictly above every published value for this split, the highest known being **0.8995 +- 0.0058**
    (ProtEGNN(t6)). A number between 0.8991 and 0.8995 does **not** meet the full criterion.
  - The previous run's noise-floor estimate of a defensible beat, **about 0.906**, is reported alongside as
    context. It is not a gate the bank states and is not treated as one.
- 0.8791 is a **carried-over** bar (`scout.md`): no status page was fetched this run, so every comparison is
  marked `PENDING STATUS CHECK`. If and only if a number met a threshold would the status page be re-fetched once,
  honestly, before any claim.

## 6. The selection-criterion comparison, specified before the scores exist

Run 2026-11-20-0215 measured, over the six models its cross-validation criterion selected, a rank agreement with
the test column of **+0.3143** for that cross-validation criterion and **+1.0000** for the withheld
extrapolation-matched criterion (`criterion_vs_test.out`). This run adds the two models the withheld criterion
would itself have selected. The comparison to be reported, fixed now:

1. Does A beat the three `all` cross-validation picks (0.895591, 0.887735, 0.893644; mean 0.892323) on test?
2. Does B beat the three `trainonly` cross-validation picks (0.886541, 0.890334, 0.882926; mean 0.886601)?
3. The eight-point rank agreement (six old models plus A and B) between each criterion's score and the test score.
   For A and B the cross-validation number is **not available** without re-running the grid, which is out of
   scope, so the eight-point version is reported only where both columns exist, and the honest statement is the
   six-point one plus the two new out-of-sample points.
4. An explicit statement of how weak this evidence is. Registered in advance: with six to eight points, a rank
   agreement of +1.0000 has a one-sided permutation probability of `1/720` at six points and `1/40320` at eight
   if the ranks were exchangeable, but the six points were **not** independently chosen (they are the
   cross-validation criterion's own winners, and the withheld criterion was examined after the test scores
   existed), so the correct reading is **suggestive, not established**. No claim of any kind will be made about
   the criterion comparison: it is a methodological observation for the next run, not a bank win.

## 7. Leakage

Features are built only from the 20-letter amino-acid alphabet `ACDEFGHIKLMNPQRSTVWY` and the four known varying
sites (0-indexed 38, 39, 40, 53; 1-indexed 39, 40, 41, 54 of the 265-residue 5LDE chain A construct). No
statistic computed over test rows enters any feature, target transform, penalty or decision. Target transforms are
computed from fitting rows only. The released sequences are used unchanged: never trimmed, padded or re-derived.

Two audits, both to be saved:

- **Line-by-line audit** of the fitting program, recorded in `attempts/sealed-scoring/report.md`, naming every
  place the `score` column is read and showing that each is restricted to fitting rows.
- **Empirical audit**: a copy of the released file in which the `score` of every `three_vs_rest == test` row is
  replaced by the literal `nan`, all other bytes unchanged. The fitting program is run on that copy and its six
  prediction files must be **byte-identical** to the real ones (compared by sha256 and by `cmp`). Pass criterion:
  all six identical.

## 8. Stopping rule

Six prediction files, one scoring pass, stop. If neither number meets a threshold in section 5, the run reports a
measured negative, makes **no claim**, and runs **no skeptic panel** - that is a complete and correct outcome. The
three-skeptic panel (`reproduce`, `novelty`, `criterion`) is run only if a number actually meets a threshold, and
then the skeptics are launched one or two at a time. No outward action of any kind, in any case; `outbox/` is not
touched.

## 9. Fair, not strictest

No gate appears in this file that the bank does not state, with the single exception of the explicitly-labelled
context number 0.906, which is reported and not enforced. Declared escape hatch: if the program's own
determinism check (section 4) fails, or the coverage gate fails, the run reports that as a bug and makes no claim.
