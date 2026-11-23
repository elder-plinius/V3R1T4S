# Claim (partial win p4)

**Claim (one sentence).** On the bank's dialogues folds (sperm-whale-dialogues.csv, 3,418 scored codas), a frozen
logistic-regression model that reads only earlier codas of the same REC stream predicts whether the next coda carries
the same whale label as the previous one with pooled held-out log-loss 0.7631 bits per coda, 0.0872 bits below a
smoothed first-order model of the same-or-switch sequence (0.8503), with a 95% REC bootstrap interval of
[0.0649, 0.1166] (10,000 resamples).

target: sperm-whale-next-coda-beyond-first-order (bank/targets.json of V3R1T4S)
claimed: partial win p4 only.

## Partial win p4 (verbatim from the bank)

> Turn-taking: on the dialogues folds, predict whether the next coda carries the same whale label as the previous one with held-out log-loss at least 0.05 bits below a smoothed first-order model of that same-or-switch sequence, with a bootstrap interval over REC groups excluding 0.

The bank's success criterion, whose streams, folds and scored set "the dialogues folds" refers to (verbatim):

> Data: sperm-whale-dialogues.csv. Streams: codas grouped by REC, ordered by TsTo, with ties (7 in the file) kept in file order. Token of a coda: (min(nClicks, 10), duration bin), with 5 equal-frequency Duration bins cut on the training folds only. Folds: sort the distinct REC strings and put the i-th in fold i mod 5; each fold is held out once. Scored: every coda with at least 2 earlier codas in its stream. Reference R1: a bigram over tokens with additive smoothing chosen from 0.01, 0.03, 0.1, 0.3 and 1 by inner cross-validation on the training folds. The claim is a frozen model, trained on the training folds only, that outputs a full distribution over tokens at each scored position from earlier codas of the same stream (their intervals, durations, whale labels, time stamps), never from any field of the coda being predicted. Pooled over the 5 folds, both must hold: (1) its cross-entropy is at least 0.10 bits per coda BELOW R1 (direction: min); (2) it is at least 0.05 bits below the same model retrained with its input cut to the single previous coda, and the 95 percent interval of a paired bootstrap over REC groups (10,000 resamples) for this gain excludes 0. Deliverables: code, folds, bin edges, and per-position probabilities for the model, its cut twin and R1.

Bank pitfall (verbatim): "Whale labels in the dialogues file may be per-recording rather than global identities;
treat them as speaker turns within a recording."

## Readings fixed before scoring (PREREG.md, frozen 2026-11-19T09:55:11Z)

- Target y_t = 1 if Whale_t equals Whale_{t-1}, at the criterion's 3,418 scored positions (each has y_{t-1}).
- "Smoothed first-order model of that same-or-switch sequence": P(y_t | y_{t-1}) from training-fold counts with
  additive smoothing alpha chosen from the R1 grid {0.01, 0.03, 0.1, 0.3, 1} by inner leave-one-training-fold-out CV.
- The model obeys the criterion's input rule: only earlier codas of the same stream; the predicted coda's label,
  time stamp, gap and all other fields are never read.
- Model: StandardScaler + LogisticRegression (L2, lbfgs) on 21 history features (p4lib.FEATURE_SETS['full']),
  C from {0.01, 0.1, 1, 10} by inner leave-one-training-fold-out CV. Bootstrap: REC groups owning a scored
  position, with replacement, statistic = pooled per-coda gain, seed 20261119, percentile 95% interval.

## Numbers (generated from result/p4_summary.json)

| held-out fold | n | ref alpha | C | reference | model | pattern (diag) | gain |
|---|---|---|---|---|---|---|---|
| 0 | 514 | 1.0 | 0.1 | 0.8664 | 0.7937 | 0.8102 | +0.0727 |
| 1 | 1305 | 0.01 | 0.1 | 0.8494 | 0.7801 | 0.8015 | +0.0693 |
| 2 | 508 | 1.0 | 0.1 | 0.8835 | 0.7325 | 0.7796 | +0.1511 |
| 3 | 692 | 0.01 | 0.1 | 0.7903 | 0.7168 | 0.7470 | +0.0735 |
| 4 | 399 | 1.0 | 0.1 | 0.8945 | 0.7875 | 0.8215 | +0.1070 |
| pooled | 3418 | | | 0.8503 | 0.7631 | 0.7909 | +0.0872 |

Same-label rate at scored positions 0.364. Reference P(same | previous transition switch / same) per fold about
0.23 / 0.60.

- Gain model vs reference: +0.0872, 95% REC bootstrap [0.0649, 0.1166].
- Pre-declared diagnostics, never gates: the same LR on switch-pattern features only (last two same/switch states and
  an A-B-A indicator): +0.0595 [0.0437, 0.0793]; RECs with at least 2 whale labels only (3,181 positions): +0.0590
  [0.0347, 0.0809]; RECs with a single label (237 positions) average +0.4664; folds not used in development (0, 1, 3;
  2,511 positions): +0.0711 [0.0441, 0.1036]. Development used folds 2 and 4 only.

## Leakage self-test (built into code/score_p4.py)

For every one of the 3,418 held-out scored positions, a copy of the stream had every field (nClicks, Duration,
ICI1-ICI28, Whale, TsTo) of the predicted coda and of all later codas replaced by random values; the model and
reference predictions at that position were recomputed: 0 of 3,418 changed (bit-identical). A deliberately leaky
predictor reading the predicted coda's nClicks was flagged at 3,418 of 3,418. Single-position recomputation equals
the batch prediction within 3.4e-16.

## Null controls (null/; PREREG.md design N4)

400 controls, each the full frozen pipeline (5 folds, all inner CV) on data whose whale labels were resimulated
per REC from the pooled first-order same/switch chain (other fields real; seed 1000 + control). Pooled gain over
the reference: best control +0.00095 bits, mean -0.0059; real +0.0872 beats all 400 (null/N4_controls.csv).

## Files

data/sperm-whale-dialogues.csv (sha256 1856c8bf915cc5ae6f928aaa2036cbbc6ad8840bb6e4f6a96aaeb96953215da2, fetched
2026-11-19T09:39:08Z, HTTP 200, from
https://raw.githubusercontent.com/pratyushasharma/sw-combinatoriality/7228c8eed2cc27ddd23b74c51aeccec9d762389e/data/sperm-whale-dialogues.csv);
code/ (frozen, sha256 as listed in PREREG.md); result/p4_per_position.csv (REC, pos, fold, y_same, p_same_ref,
p_same_model, p_same_pattern), result/p4_summary.json, result/run_output.txt, result/folds.csv; null/; PREREG.md,
PREREG.v2.md (the v2 note concerns p3 only); baseline/README.md.

## Status source (scout record)

https://export.arxiv.org/api/query?search_query=abs:%22sperm%20whale%22&sortBy=submittedDate&sortOrder=descending&max_results=25
fetched 2026-11-19T09:37:53Z, HTTP 200, sha256 1d1a18b7520dbb62d3416d2e8a45e0c0d01378ed080bc6d5929f0fc849c4e94f;
no returned abstract reports a same-or-switch prediction result.

## Credit

Data: Sharma, Gero, Payne, Gruber, Rus, Torralba and Andreas, Nature Communications 15:3617 (2024),
https://github.com/pratyushasharma/sw-combinatoriality (Dominica Sperm Whale Project DTag recordings).
