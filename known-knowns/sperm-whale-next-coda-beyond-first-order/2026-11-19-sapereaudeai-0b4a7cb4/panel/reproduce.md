# REPRODUCE skeptic verdict: sperm-whale-next-coda-beyond-first-order (FULL criterion)

context: subagent (Claude Code Agent tool, reproduce type)

Claim checked (CLAIM.md): pooled held-out cross-entropy of the frozen `full` model 2.1238 bits/coda over 3,418 scored
codas; R1 2.7802 (gain 0.6563); single-previous-coda twin 2.6549 (gain 0.5311); 95% paired REC bootstrap for the twin
gain [0.4571, 0.6325].

All numbers below were copied from command output; scripts and outputs are in ../panel_work/reproduce/ (scripts/ and
out/; the fetched CSV is in its own directory fetched/; the author's code was run from a hash-identical copy in
authorrun/code/ so nothing was written into the claim folder). Interpreter: Python 3.11.15, numpy 2.4.6, scipy 1.17.1,
pandas 3.1.0, every job run with `-I`, single-threaded, one at a time.

## My independent checker (written from the definition before reading the author's code)

Definition used (bank, verbatim): "Streams: codas grouped by REC, ordered by TsTo, with ties (7 in the file) kept in
file order. Token of a coda: (min(nClicks, 10), duration bin), with 5 equal-frequency Duration bins cut on the
training folds only. Folds: sort the distinct REC strings and put the i-th in fold i mod 5; each fold is held out
once. Scored: every coda with at least 2 earlier codas in its stream. Reference R1: a bigram over tokens with additive
smoothing chosen from 0.01, 0.03, 0.1, 0.3 and 1 by inner cross-validation on the training folds."

- scripts/check1.py: csv-module parsing (no pandas); streams = REC groups sorted by (TsTo, file row); folds by sorted
  REC strings; scored = positions >= 2; bin edges = hand-written linear-interpolation quantiles (0.2/0.4/0.6/0.8) of
  every training-fold Duration; bin = number of edges <= d; token (c-1)*5+b; R1 = bigram counts over all consecutive
  training pairs, P = (n(a,b)+alpha)/(n(a)+50 alpha), alpha by leave-one-training-fold-out inner CV (total held-out
  log-loss on scored positions, ties to the first grid value), evaluated under two readings of the inner-CV binning.
  Then it loads every saved probs_*.csv, checks keys/fold/y_token against my scored set, checks every vector (sum, zeros,
  finiteness), and recomputes all cross-entropies and gains.
- scripts/check2.py: my own paired REC bootstrap (10,000 resamples, fresh seed 5150731; statistic = sum of gains /
  number of positions in the resample; percentile interval).
- scripts/indep_model.py (written after reading seqlib.py for the feature definitions, but entirely my own code):
  own streams/bins/tokens/count tables, own 19 features (normal cdf via math.erfc), own exact-Hessian Newton optimiser
  for the strictly convex L2-penalised objective, own inner-CV lambda search; fits `twin`, `full`, and a
  literal-truncation twin `trunc` (the full feature map computed on a history cut to coda t-1 only).
- scripts/feature_check.py: my features vs the author's seqlib.feats at every row; optimiser gap.
- scripts/leak_mine.py: my own leakage test against the author's fitted model (perturbs the predicted coda only).

## Checks

| # | Check | Result |
|---|---|---|
| a | Fetched sperm-whale-dialogues.csv myself (one request, HTTP 200, 500,380 bytes, 2026-11-19T10:22:05Z); sha256 1856c8bf915cc5ae6f928aaa2036cbbc6ad8840bb6e4f6a96aaeb96953215da2 = claim's value and = data/sperm-whale-dialogues.csv | PASS |
| b1 | 3,840 codas, 33 columns, 219 RECs; 7 TsTo ties within RECs (bank says 7) | PASS |
| b2 | Folds: my REC->fold map equals result/folds.csv for all 219 RECs; codas per fold 598/1387/593/779/483, scored 514/1305/508/692/399, total scored 3,418 | PASS |
| b3 | Bin edges: my hand-written quantiles equal result/bin_edges.csv exactly (max diff 0.000e+00) in all 5 folds; training-bin occupancy e.g. fold 0 [649, 648, 648, 648, 649] | PASS |
| b4 | Scored set: the (REC, pos) keys, fold and y_token of all five probs_*.csv equal mine at all 3,418 positions | PASS |
| c | R1: my inner CV picks alpha 0.3 in every fold (author: 0.3); my R1 vectors equal probs_R1.csv exactly (max abs diff 0.000e+00); my R1 pooled 2.780154 | PASS |
| d1 | Twin, independent implementation: lambda equals the author's in all 5 folds (1e-4, 1e-2, 1e-3, 1e-3, 1e-3); pooled 2.654906 vs saved 2.654909 (diff -3.19e-06); max per-position prob diff 5.971e-05 | PASS |
| d2 | Full, independent implementation: lambda equals the author's in all 5 folds (1e-3, 1e-3, 1e-3, 1e-2, 1e-3); pooled 2.123844 vs saved 2.123847 (diff -3.65e-06); max prob diff 6.249e-04 | PASS |
| d3 | Why the small differences: my features equal the author's exactly for 15 of 19 features (diff 0 or 1.78e-15); the 4 lognormal-bin features differ by at most 2.21e-04, from erfc-vs-scipy rounding of normal tail probabilities near the 1e-12 floor. My features x the author's saved theta reproduce the saved full/twin vectors to 3.818e-07/2.591e-07. The author's L-BFGS-B objective is at most 7.43e-08 nats above my Newton optimum. So the differences are optimiser tolerance plus floating-point rounding, not a definitional mismatch | PASS |
| e1 | Every vector in probs_R1/twin/full/rep_diagnostic/local_diagnostic.csv: 0 zero entries, 0 non-finite, max abs(sum-1) 2.220e-16 / 6.661e-16 / 6.661e-16 / 6.661e-16 / 6.661e-16; min entry 5.455e-04 / 1.240e-05 / 5.264e-06 / 2.073e-06 / 1.947e-06 | PASS |
| e2 | Cross-entropies recomputed from the saved vectors: R1 2.780154 (folds 2.8708, 3.044, 2.9201, 2.37, 2.3335); twin 2.654909 (2.8026, 2.8269, 2.837, 2.3144, 2.261); full 2.123847 (2.0762, 2.3752, 2.1533, 1.8144, 1.8625); rep 2.565329; local 2.335085, all equal to CLAIM.md's table | PASS |
| e3 | Gains: full vs R1 0.6563064778564618 (>= 0.10); full vs twin 0.5310621359536838 (>= 0.05); full vs rep 0.441481564826697; full vs local 0.21123767905720925, all equal to the claim | PASS |
| f | REC bootstrap, fresh seed 5150731, 10,000 resamples over 188 REC groups: full vs twin [0.4572, 0.6327] (lower bound > 0; 0 of 10,000 resamples <= 0; min resample 0.4134); full vs R1 [0.5879, 0.7461]. At the author's seed 20261119 my own bootstrap code gives exactly [0.4571, 0.6325] and [0.5883, 0.7465] | PASS |
| g | Frozen pipeline rerun (score_content.py, hash-identical copy, my fetched data), 10:24:38Z to 10:36:18Z, exit 0. sha256 identical to the saved files: folds.csv 675bd6cb..., probs_R1.csv 7dbfd5df..., probs_twin.csv d708d63a..., probs_full.csv d456be16..., content_summary.json 9d2c0aec...; probs_rep_diagnostic.csv and probs_local_diagnostic.csv bit-identical to the rerun's arrays; printed output (56 lines) identical apart from elapsed seconds; GATES all True. Deterministic | PASS |
| g2 | Code hashes: all 5 files in code/ match PREREG.md's freeze list (swlib 1cac1753..., leak 1f04fcb8..., seqlib 8570c8ce..., seqpipe 135b45ee..., score_content cde79a2e...) | PASS |
| h1 | My leakage test against the author's fitted model (author code + saved theta; this reconstruction reproduces all saved R1/twin/full vectors with max abs diff 0.000e+00). At each of the 3,418 positions the predicted coda alone was altered in 4 patterns ("shift" and "extreme" change every field, nClicks, Duration, ICI1-28, Whale and TsTo, at 3,418 of 3,418 positions; also "copy previous coda" and "random"), plus the stream cut at t and at t+1: 20,508 recomputed vectors each for R1, twin and full, 0 changed (max abs diff 0.000e+00) | PASS |
| h2 | Positive controls of my test: a predictor reading nClicks[t] was flagged 3,418/3,418; the author's full model fed a history that includes coda t was flagged 3,418/3,418 | PASS |
| h3 | Code reading: seqlib.feats reads only the History view (arrays sliced [:t] in swlib.History, tokens recomputed from those rows), indices t-1, t-2 and earlier rows only, plus training-fold tables; seqpipe uses tok[t] only as the label; R1 reads tok[t-1]. No feature reads any field of coda t; TsTo and ICIs are never used as features. Held-out rows use tables, bin edges and theta from the 4 training folds only. The TWIN features depend only on coda t-1 (confirmed: identical when my code computes them from a one-coda history) | PASS |
| s1 | Sensitivity, twin read literally as "the full model with input cut to the single previous coda" (my `trunc`): pooled 2.646417; full vs trunc 0.522573 [0.4454, 0.6276] (seed 5150731); condition (2) still holds. trunc vs author twin 0.008489 [-0.0078, 0.0223] | PASS |
| s2 | Sensitivity, inner-CV bins re-cut on the 3 inner-training folds: alpha becomes 0.1 in folds 1 and 2; R1 pooled 2.7947805529794203; gain 0.6709333787575393; condition (1) still holds | PASS |
| s3 | Pristine-fold diagnostic (folds 0, 1, 3; 2,511 codas, 111 RECs), fresh seed: full vs twin 0.5212 [0.4408, 0.6529]; full vs R1 0.6634 [0.5881, 0.7802], matching the claimed 0.5212 and 0.6634 | PASS |

## Notes (not failures of the claimed values)

1. CLAIM.md's file list names `null_test.md` (the null controls for condition (2)), but that file is absent from the
   claim package. I did not verify the null test; it is not in the bank's deliverables or in this skeptic's scope.
   It should be added to the package, or the reference removed, before filing.
2. score_content.py and seqlib.py add `code/../../evaluator/code` to sys.path, a path outside the claim folder.
   That path does not exist now, so it is harmless, but the package should be self-contained. REPRODUCE.md step 2 also
   writes rerun/ inside the claim folder; I ran a hash-identical copy in my work folder instead.
3. In fold 3's training set, 4 durations fall exactly on an edge (the quantile index is an integer). The convention
   edges[b-1] <= d < edges[b] (PREREG) is used consistently, and my checker matches it at all 3,418 scored tokens.
4. Inside lambda selection, training rows' cross-fitted tables include the inner-held-out fold. This affects only
   hyperparameter choice within the training folds. The outer held-out fold never enters a table, bin edge or fit.

Conclusion: every claimed value (2.1238, 2.7802, 2.6549, +0.6563, +0.5311, [0.4571, 0.6325]) and every claimed
property (folds, bin edges, scored set, vectors sum to 1 with no zero, no leakage, determinism) reproduces.
Independent implementations of R1, the twin and the full model agree. Fresh-seed bootstrap and the literal-truncation
twin both keep both conditions met.

pass: true
