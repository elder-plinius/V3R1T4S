# PREREG - sperm-whale-next-coda-beyond-first-order

frozen: 2026-11-19T09:55:11Z (date -u), before any held-out score on bank folds 0, 1 or 3 of the dialogues file or
on Dominica folds 1, 2 or 4. Development so far touched only the dev folds (below); its outputs are in
attempts/*/dev_output_*.txt and attempts/evaluator/smoke_dev_output.txt.

null_test: required

## Criterion (verbatim, from target.md)

Main: "Pooled over the 5 folds, both must hold: (1) its cross-entropy is at least 0.10 bits per coda BELOW R1
(direction: min); (2) it is at least 0.05 bits below the same model retrained with its input cut to the single
previous coda, and the 95 percent interval of a paired bootstrap over REC groups (10,000 resamples) for this gain
excludes 0." Partial wins p1, p2, p3, p4 as quoted verbatim in target.md.

## Data

data/csv/sperm-whale-dialogues.csv sha256 1856c8bf915cc5ae6f928aaa2036cbbc6ad8840bb6e4f6a96aaeb96953215da2 (500,380 B)
data/csv/DominicaCodas.csv sha256 53dd44fbfb0040da93656aa44883954f3abe18dd6539e90c625af86a96db6b45 (747,518 B)
both from sw-combinatoriality commit 7228c8eed2cc27ddd23b74c51aeccec9d762389e. No .p file is fetched or loaded.

## Development split (declared, already used)

- Dialogues: dev = bank folds 2 and 4 (the two smallest by coda count, 593 and 483; chosen by size before any
  predictive statistic), 87 REC, 907 scored, with 4 REC sub-folds (dev RECs sorted, j-th in sub-fold j mod 4).
  Pristine folds: 0, 1, 3 (2,511 scored codas).
- Dominica: dev = date folds 0 and 3 (the two smallest by row count, 1,367 and 1,612), 4 date sub-folds.
  Pristine folds: 1, 2, 4.
- The gates below are on the bank's pooled 5-fold numbers (the bank's own definition). The pristine-fold numbers
  are reported as a disclosed diagnostic, never as a gate.

## Common protocol (bank, literal; implemented in attempts/evaluator/code/swlib.py)

- Streams: rows grouped by REC, stable sort by TsTo with ties in file order (mergesort on REC, TsTo, file row).
- Folds: distinct REC strings sorted as text (Python sorted), i-th REC in fold i mod 5; each fold held out once.
- Scored: every coda with >= 2 earlier codas in its stream (3,418).
- Token: (min(nClicks,10), duration bin); vocabulary = all 50 pairs (click class 1-10 x bin 0-4), token id
  (c-1)*5+b. Bin edges = numpy.quantile(Duration of every coda in the 4 training folds, [0.2,0.4,0.6,0.8]) with
  numpy's default linear interpolation; bin = searchsorted(edges, Duration, side='right') (edges[b-1] <= d < edges[b]).
- Inner CV ("inner cross-validation on the training folds"): leave one of the 4 training folds out in turn
  (using the bank's own fold labels), total held-out log-loss on that fold's scored positions; the grid value with
  the lowest total wins, ties to the first grid value.
- R1: bigram counts over all consecutive pairs inside training streams; P = (n(a,b)+alpha)/(n(a)+50 alpha), alpha
  from {0.01, 0.03, 0.1, 0.3, 1} by inner CV; refit on all 4 training folds.
- Cross-entropy: mean of -log2 p(true token) over scored positions; pooled = over all 3,418 positions of the 5
  held-out folds.
- Paired bootstrap: 10,000 resamples, numpy default_rng seed 20261119, over the REC groups that own >= 1 scored
  position (resampled with replacement, same count); statistic = sum of per-position gains / number of positions in
  the resample (the pooled per-coda gain); 95% percentile interval [2.5%, 97.5%]. "Excludes 0" = lower bound > 0.
  Gain = reference bits minus model bits (positive = model better).

## Model for the main criterion, p1 and p2 (attempts/sequence-model/code/seqlib.py, seqpipe.py)

Log-linear tilt over the 50 tokens, P(x|h) = softmax_x(theta . F(x,h)), L2-penalised maximum likelihood
(L-BFGS-B), lambda from {1e-4, 1e-3, 1e-2, 1e-1} by inner CV, refit on all training rows. Training rows =
positions >= 2 of training-fold streams. Count-table features (unigram add-0.5, bigram and skip-bigram add-0.3)
are cross-fitted for training rows (tables from the other 3 training folds) and use all 4 training folds for
held-out rows. Feature sets, exactly as in seqlib.py:
- `full` (THE FROZEN MODEL): TWIN + REP + HIGH, 19 features.
- `twin` (THE CUT TWIN of condition (2) and p2): TWIN = bigram on the previous token, unigram, same click class /
  same bin / |bin difference| to coda t-1, and two tempo features from coda t-1's exact duration and click count.
  Same rows, same lambda search; its input is the single previous coda.
- diagnostics, pre-declared, never gates: `rep` = TWIN + REP (run length of the previous token, stream-local
  repeat rate): the repetition-aware comparison the bank's pitfall names; `local` = TWIN + REP + order-free bag of
  the stream's earlier codas (token cache and click-class cache): a stream-local first-order reference in the sense
  of Sinha and Chavan's stream-local control.
- The model reads only earlier codas of the same stream (History slices rows [:t]) plus training-fold tables.

Gates (bank thresholds only):
- main criterion: pooled gain(full vs R1) >= 0.10 AND pooled gain(full vs twin) >= 0.05 with its REC-bootstrap
  lower bound > 0.
- p1: gain(full vs R1) >= 0.05 and its lower bound > 0.
- p2: gain(full vs twin) >= 0.03 and its lower bound > 0.
Any claim text must also report gain(full vs rep) and gain(full vs local) with their intervals, and say plainly
what part of the gain is stream-level context rather than coda order.

## p4 model (attempts/turn-taking/code/p4lib.py)

- Target y_t = 1 if Whale_t == Whale_{t-1}, at the 3,418 scored positions (so y_{t-1} is defined).
- Reference ("a smoothed first-order model of that same-or-switch sequence"): P(y_t | y_{t-1}) from counts over
  positions >= 2 of training streams, additive alpha from {0.01, 0.03, 0.1, 0.3, 1} by inner CV (the R1 grid and
  rule; the most natural fair reading).
- Frozen model: StandardScaler + LogisticRegression (lbfgs, L2) on the 21 `full` features of p4lib.FEATURE_SETS
  (switch states of the last two transitions, A-B-A indicator, stream-local same rate, counts of transitions and
  labels so far, run length, speaker share, gaps and overlaps between the last three earlier codas, time since
  another whale, previous click count and duration), C from {0.01, 0.1, 1, 10} by inner CV. All features come from
  rows [:t]; the predicted coda's time stamp, gap and label are never read.
- Diagnostic, never a gate: the same LR on `pattern` (s1, s2, missing flag, A-B-A only); gains on single-label vs
  multi-label RECs.
- Gate p4: pooled gain(model vs reference) >= 0.05 bits with REC-bootstrap lower bound > 0.

## p3 model (attempts/dominica/code/dompipe.py)

- Exactly the bank's p3: tokens = CodaType (vocabulary = the 35 CodaType strings of the file), Date rewritten '-'
  -> '/', streams = rewritten Date + Unit ordered by codaNUM2018 (stable), folds = distinct rewritten Date strings
  sorted as text, i-th in fold i mod 5, scored = >= 2 earlier codas in the stream (8,501).
- Reference: smoothed bigram over CodaType, additive alpha from the R1 grid by inner CV on the training folds.
- Frozen model `full`: log-linear tilt with bigram, unigram, same-as-previous, run length, repeat rate, stream
  cache, skip-bigram, same-as-t-2, same-whale-last-token (IDN of earlier codas), echo-after-switch; lambda grid and
  inner CV as above. It uses two or more previous codas. Diagnostics: `one`, `rep`, `local`.
- Bootstrap over rewritten-Date groups, 10,000 resamples, seed 20261119.
- Gate p3: pooled gain(full vs bigram) >= 0.05 with Date-bootstrap lower bound > 0.

## Leakage self-test (bank verification method; built into every scoring script)

For every held-out scored position of every fold: copy the stream, alter every field (nClicks, Duration,
ICI1-ICI28, Whale, TsTo; for Dominica CodaType, IDN, nClicks, Duration) of the predicted coda AND of all later codas,
keep the stream order, recompute each prediction (model, twin, diagnostics, references) through the normal
single-position code path, and require bit-identical vectors. A deliberately leaky predictor that reads the
predicted coda must be flagged (positive control). Any change on a real predictor = no claim.

## Null design (kit rule; 400 controls each, the same frozen pipeline end to end, all 5 folds, all inner CV)

- N4 (p4): per REC keep Whale_0 and Whale_1; for t >= 2 draw y_t from the pooled first-order same/switch chain
  (maximum likelihood from all real scored transitions); on a switch draw a new label uniformly from
  {1..max(K,2)} minus the current one (K = number of distinct real labels of that REC). Other fields real.
  Statistic: pooled gain(model vs reference). Under this null the first-order reference is the true model.
- N2 (condition (2) and p2): per REC keep coda 0; for t >= 1 pick uniformly a real within-stream transition u -> v
  of the whole file whose source u has the current coda's global token (click class and Duration quintile cut on
  the whole file; used only to build controls), and copy v's nClicks, Duration and ICIs (a uniformly random coda if
  no transition exists). Whale and TsTo real. Statistic: pooled gain(full vs twin). The gain(full vs R1) under N2 is
  recorded as context for condition (1)/p1 only, NOT a gate: p1 and condition (1) are comparisons with the bank's
  fixed reference R1 and their bank test is the REC bootstrap.
- N3 (p3): per stream keep the first coda; for t >= 1 draw the next CodaType from the pooled first-order empirical
  transition distribution of the whole file (unigram if a type has no outgoing transition). Other fields real.
  Statistic: pooled gain(full vs bigram).
- Control i uses seed 1000 + i. A structural claim (p4, condition (2)/p2, p3) needs its real gain above every one
  of its 400 controls. Results in null_test.md.

## Escape hatches (declared now)

- A crash or a non-modelling bug in the frozen run (an exception, an indexing error, a leakage-test failure
  traced to the harness, not the model) may be fixed once; the fix and the rerun are recorded in PREREG.v2.md with
  the time. Model families, features, grids, folds, seeds and gates never change.
- If the leakage self-test flags a real predictor, that model's claim is void (no repair in this run).
- If a null run cannot finish 400 controls within the budget, the claim stays PROMISING at most.

## Code at freeze (sha256)

1cac175385a23e1154d4d51a3ffedc73072e457e5d0de25697694d87f79d79de attempts/evaluator/code/swlib.py
1f04fcb87a473be805e4902e718d572db157cc9dd329875fafcf7d9be67bcbf7 attempts/evaluator/code/leak.py
7a8c385dd8ad1e1b8cfc38980a07d47a5e82e28e0c51c65716fc8680edc7c360 attempts/turn-taking/code/p4lib.py
784d8d2bc6098ab37e75b0907bf5b9eb9fbb514e5bf815db28939fcd08f98bcd attempts/turn-taking/code/score_p4.py
8570c8cef9c690ce2896bf4f4bf68feb3df5de24c16c98e85a59137bf30bbf58 attempts/sequence-model/code/seqlib.py
135b45eeba7cfcea6a615be7cc3e2ef7dd5d702d2616dd9b257317a39020fd47 attempts/sequence-model/code/seqpipe.py
cde79a2e6c44f42033747f3e33f0fe61abf0a223927c5df6c62bf63eecd31305 attempts/sequence-model/code/score_content.py
63f94f42fd5e470b9bd11521944d43cd5ad96932314348c81a51860df9d70c53 attempts/dominica/code/dompipe.py
303337acdfb9a66149e886825081805b5af34feae7ae13ca40b4c14f49d95e4d attempts/dominica/code/score_p3.py

## Baseline (kit step 3c)

No published baseline exists for this exact setup: WhaleLM released no code or absolute values, and Sinha and Chavan
use other corpora and tokens (the bank says their numbers are context, not baselines). The criterion's own reference
R1 (and the p4 and p3 references) are the baselines; they are computed here from the definition and recomputed
independently by any skeptic. Recorded in baseline/.
