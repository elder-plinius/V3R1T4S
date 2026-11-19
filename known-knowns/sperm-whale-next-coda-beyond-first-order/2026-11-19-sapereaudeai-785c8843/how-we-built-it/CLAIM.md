# Claim (partial win p3)

**Claim (one sentence).** On DominicaCodas.csv (all 8,719 rows, both clans), under the bank's p3 definition of
tokens, streams, date folds and scored set (8,501 codas with at least 2 earlier codas in their stream), a frozen
log-linear model that uses two or more previous codas of the same stream has pooled held-out cross-entropy 1.5895
bits per coda, 0.1284 bits below a smoothed bigram over CodaType (1.7179), with a 95% bootstrap interval over
rewritten-Date groups of [0.0879, 0.1630] (10,000 resamples).

target: sperm-whale-next-coda-beyond-first-order (bank/targets.json of V3R1T4S)
claimed: partial win p3 only.

## Partial win p3 (verbatim from the bank)

> The same test on DominicaCodas.csv, all 8,719 rows of both clans: tokens are CodaType; each Date is first rewritten with every hyphen replaced by a slash (the file writes four days both ways, for example 02-03-2015 and 02/03/2015); streams are rows sharing that rewritten Date and Unit, ordered by codaNUM2018; folds are the distinct rewritten Date strings sorted as text, with the i-th in fold i mod 5; a model using two or more previous codas beats a smoothed bigram over the same tokens by at least 0.05 bits per coda, with a bootstrap interval over Date groups excluding 0.

"The same test" refers to the bank's main criterion for the dialogues file (verbatim): "Scored: every coda with at
least 2 earlier codas in its stream. Reference R1: a bigram over tokens with additive smoothing chosen from 0.01,
0.03, 0.1, 0.3 and 1 by inner cross-validation on the training folds. The claim is a frozen model, trained on the
training folds only, that outputs a full distribution over tokens at each scored position from earlier codas of the
same stream ..., never from any field of the coda being predicted."

## Readings fixed before scoring (PREREG.md, frozen 2026-11-19T09:55:11Z)

- Vocabulary = the 35 CodaType strings of the file (result/p3_vocab.csv). Streams sorted stably by codaNUM2018.
  97 rewritten Date strings, folds of 20/20/19/19/19 dates (result/p3_folds.csv). 109 streams, 8,501 scored.
- Smoothed bigram: additive alpha from {0.01, 0.03, 0.1, 0.3, 1} by inner leave-one-training-fold-out CV (alpha 0.3
  chosen in every fold).
- Model `full` (code/dompipe.py): softmax tilt with features bigram, unigram, same-as-previous, run length, stream
  repeat rate, stream cache, skip-bigram (coda t-2), same-as-t-2, last CodaType of the identified whale (IDN) of coda
  t-1, echo of coda t-2 after an IDN change; lambda from {1e-4, 1e-3, 1e-2, 1e-1} by inner CV.
- Disclosed in PREREG.v2.md (written before any p3 score was seen): the IDN column holds strings, and the frozen
  IDN features compare with the integer 0, so the label '0' (5,705 unidentified rows) acts as one more whale label.
  The model was not changed. Also recorded there: the first scoring attempt crashed in the leakage harness before
  any score was produced; only the harness was fixed (code/dompipe.py sha256 unchanged).

## Numbers (generated from result/p3_summary.json; bits per coda)

| held-out fold | n | bigram alpha | bigram | one (diag) | rep (diag) | local (diag) | full (model) |
|---|---|---|---|---|---|---|---|
| 0 | 1327 | 0.3 | 1.5077 | 1.4951 | 1.4759 | 1.3831 | 1.3644 |
| 1 | 1914 | 0.3 | 1.7059 | 1.6874 | 1.6860 | 1.6142 | 1.5932 |
| 2 | 2003 | 0.3 | 1.8709 | 1.8726 | 1.8646 | 1.7538 | 1.7213 |
| 3 | 1568 | 0.3 | 1.8484 | 1.8489 | 1.8290 | 1.7379 | 1.6978 |
| 4 | 1689 | 0.3 | 1.5941 | 1.5930 | 1.5792 | 1.5192 | 1.5052 |
| pooled | 8501 | | 1.7179 | 1.7121 | 1.7005 | 1.6150 | 1.5895 |

- Gain full vs smoothed bigram: +0.1284, 95% Date bootstrap [0.0879, 0.1630].
- Pre-declared diagnostics, never gates: `one` (previous-coda tilt) vs bigram +0.0059 [0.0001, 0.0122]; full vs `rep`
  (previous coda + run length + repeat rate) +0.1110 [0.0738, 0.1430]; full vs `local` (rep + order-free stream cache)
  +0.0255 [0.0147, 0.0356]. From the pooled table: bigram minus local = 0.1029 of the 0.1284 bits, of which the order-free
  stream cache alone (rep minus local) is 0.0855 bits, i.e. stream-level context (which coda types a unit uses that
  day); 0.0255 bits remains for ordered features. Folds not used in development (1, 2, 4; 5,606
  positions): +0.1187 [0.0700, 0.1564]. Development used folds 0 and 3 only.

## Leakage self-test (built into code/score_p3.py)

For every one of the 8,501 held-out scored positions, a copy of its stream had every field the model can read
(CodaType token, IDN, nClicks, Duration) of the predicted coda and of all later codas altered, and all five
predictors (bigram, one, rep, local, full) were recomputed at that position: 0 of 42,505 vectors changed
(bit-identical); the positive control (a reader of the predicted coda's token) changed at 8,501 of 8,501.
Single-position recomputation equals the batch predictions exactly. All vectors strictly positive (min 3.9e-05),
sums within 1.2e-15 of 1.

## Null controls (null/; PREREG.md design N3)

COMPLETE. This section read PENDING while the package was assembled and while the panel read it; the controls
have since finished. Design N3: each stream's CodaType sequence is resimulated from the pooled first-order
transitions, then the whole frozen pipeline is rerun end to end, all 5 folds and all inner CV.

- controls: 400 of 400, no missing index, no duplicate
- best control: +0.0011542479820425993
- real gain: +0.1284227460626554
- real beats all controls: yes (111.3x the best control; zero controls at or above the real gain)
- control distribution: mean -0.00469, sd 0.00208, min -0.01019, max +0.00115

The aggregated file covering all three null designs of this run is the main claim's null/null_test.md, section
"p3 claim: design N3".

**What this null does and does not establish.** N3 destroys between-stream heterogeneity as well as order, so
beating it rules out a single pooled homogeneous first-order process and nothing narrower. It does **not**
preserve each stream's composition. By the pre-declared decomposition only +0.0255 of the +0.1284 bits is
ordered structure beyond a stream-local reference, and a composition-preserving control (within-stream CodaType
swaps) is untested here. It is the control that a same-cell attempt, V3R1T4S draft PR #1159, reported failing.
See this attempt's panel/gate.md for the full caveat.

## Files

data/DominicaCodas.csv (sha256 53dd44fbfb0040da93656aa44883954f3abe18dd6539e90c625af86a96db6b45, 747,518 bytes,
fetched 2026-11-19T09:39:11Z, HTTP 200, from
https://raw.githubusercontent.com/pratyushasharma/sw-combinatoriality/7228c8eed2cc27ddd23b74c51aeccec9d762389e/data/DominicaCodas.csv);
code/dompipe.py (frozen model), code/score_p3.py (scoring and leakage harness); result/p3_probs_bigram.csv and
result/p3_probs_full.csv (stream = "rewritten Date|Unit", pos, fold, y_token, p0..p34 over result/p3_vocab.csv),
result/p3_summary.json, result/p3_folds.csv, result/run_output.txt; PREREG.md, PREREG.v2.md; baseline/README.md.

## Status source (scout record)

https://export.arxiv.org/api/query?search_query=abs:%22sperm%20whale%22&sortBy=submittedDate&sortOrder=descending&max_results=25
fetched 2026-11-19T09:37:53Z, HTTP 200, sha256 1d1a18b7520dbb62d3416d2e8a45e0c0d01378ed080bc6d5929f0fc849c4e94f.

## Credit

Data: Sharma, Gero, Payne, Gruber, Rus, Torralba and Andreas, Nature Communications 15:3617 (2024),
https://github.com/pratyushasharma/sw-combinatoriality (Dominica Sperm Whale Project). Context: Sinha and Chavan,
arXiv 2606.16084 (+0.2076 bits over a pooled first-order model, -0.0285 against a stream-local reference, on a
different public Dominica coda set).
