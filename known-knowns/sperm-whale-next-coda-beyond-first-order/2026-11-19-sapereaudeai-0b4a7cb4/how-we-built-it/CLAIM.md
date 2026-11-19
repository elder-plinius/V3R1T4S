# Claim

**Claim (one sentence).** On sperm-whale-dialogues.csv, under the bank's exact streams, tokens, folds and scored set,
a frozen log-linear next-coda model that reads only earlier codas of the same REC stream (code/seqlib.py, feature set
`full`) has a pooled held-out cross-entropy of 2.1238 bits per coda over the 3,418 scored codas, 0.6563 bits below
reference R1 (2.7802) and 0.5311 bits below its own single-previous-coda twin (2.6549), and the 95% paired REC
bootstrap interval (10,000 resamples) for the twin gain is [0.4571, 0.6325].

target: sperm-whale-next-coda-beyond-first-order (bank/targets.json of V3R1T4S)
claimed: the full success criterion (conditions (1) and (2)).

## Success criterion (verbatim from the bank)

> Data: sperm-whale-dialogues.csv. Streams: codas grouped by REC, ordered by TsTo, with ties (7 in the file) kept in file order. Token of a coda: (min(nClicks, 10), duration bin), with 5 equal-frequency Duration bins cut on the training folds only. Folds: sort the distinct REC strings and put the i-th in fold i mod 5; each fold is held out once. Scored: every coda with at least 2 earlier codas in its stream. Reference R1: a bigram over tokens with additive smoothing chosen from 0.01, 0.03, 0.1, 0.3 and 1 by inner cross-validation on the training folds. The claim is a frozen model, trained on the training folds only, that outputs a full distribution over tokens at each scored position from earlier codas of the same stream (their intervals, durations, whale labels, time stamps), never from any field of the coda being predicted. Pooled over the 5 folds, both must hold: (1) its cross-entropy is at least 0.10 bits per coda BELOW R1 (direction: min); (2) it is at least 0.05 bits below the same model retrained with its input cut to the single previous coda, and the 95 percent interval of a paired bootstrap over REC groups (10,000 resamples) for this gain excludes 0. Deliverables: code, folds, bin edges, and per-position probabilities for the model, its cut twin and R1.

Bank verification method (verbatim): "The skeptic downloads the two CSV files, records their checksums, regenerates
folds and bin edges with an independent script, fits R1 and the truncated twin themselves, and recomputes all
cross-entropies from the per-position probabilities after checking that each vector sums to 1 with no zero entries.
They rerun the bootstrap with a fresh seed and test for leakage by altering every field of the predicted coda and
confirming that the predictions do not change."

Bank pitfalls (verbatim): "The 3,840 codas (3,418 scored) fall into 5 folds of 483 to 1,387 codas, which is small;
gains of a few hundredths of a bit can come from repeated runs of one token, so a repetition-aware twin is the
honest comparison." "Whale labels in the dialogues file may be per-recording rather than global identities; treat
them as speaker turns within a recording."

## Numbers (from result/content_summary.json; bits per coda; gain = reference minus model)

| held-out fold | n | R1 | twin | rep (diag) | local (diag) | full (model) |
|---|---|---|---|---|---|---|
| 0 | 514 | 2.8708 | 2.8026 | 2.7158 | 2.3067 | 2.0762 |
| 1 | 1305 | 3.0440 | 2.8269 | 2.7454 | 2.5893 | 2.3752 |
| 2 | 508 | 2.9201 | 2.8370 | 2.7508 | 2.3837 | 2.1533 |
| 3 | 692 | 2.3700 | 2.3144 | 2.1914 | 2.0010 | 1.8144 |
| 4 | 399 | 2.3335 | 2.2610 | 2.1949 | 2.0576 | 1.8625 |
| pooled | 3418 | 2.7802 | 2.6549 | 2.5653 | 2.3351 | 2.1238 |

(Generated from result/content_summary.json by script.)

- Condition (1): full vs R1 = +0.6563 (REC bootstrap [0.5883, 0.7465]); threshold 0.10.
  - **R1 depends on an inner-CV convention the bank does not pin down**, so both public values for this cell are
    stated here. This claim selects alpha by leave-one-training-fold-out using the outer fold's bin edges and
    summing the loss over scored positions only: R1 = 2.7802. Recutting the bin edges inside the inner CV, or
    scoring all transitions (positions >= 1), selects alphas [0.3, 0.1, 0.1, 0.3, 0.3] and gives R1 = 2.794781,
    which is the value reported by V3R1T4S PR #1159. Averaging per-fold mean losses, or leaving one REC out,
    gives 2.787390. The two numbers are the same quantity under different readings, not a discrepancy. This
    claim uses the *lowest* (strongest, hardest to beat) of them; condition (1) holds under every reading and at
    every fixed alpha on the grid, the margin ranging from +0.6508 (test-set-oracle R1) to +0.6709 (R1 2.7948).
- Condition (2): full vs twin = +0.5311, 95% REC bootstrap [0.4571, 0.6325]; threshold 0.05, interval excludes 0.
- Repetition-aware comparison (bank pitfall): `rep` = twin + run length of the previous token + stream-local repeat
  rate: full vs rep = +0.4415 [0.3716, 0.5370].
- Stream-local comparison: `local` = rep + an order-free bag of the stream's earlier codas (token cache and
  click-class cache): full vs local = +0.2112 [0.1741, 0.2445].
- Decomposition of the 0.5311-bit gain over the twin, into the three nested steps (they sum to 0.5310):
  - +0.0896 (rep vs twin): run length of the previous token and stream-local repeat rate. **These depend on
    order**, so this part is not order-free.
  - +0.2302 (local vs rep): the order-free bag of the stream's earlier codas. This is the part that is matched by
    stream-level context with no order.
  - +0.2112 (full vs local): ordered and recency features (skip-bigram, coda t-2 identity, tempo trend, last
    same-click-class duration, whale-switch echoes).

  An earlier draft of this file said that 0.3198 bits (local vs twin) was "matched by stream-level context with no
  order". That was wrong: 0.0896 of those 0.3198 bits comes from the order-dependent REP features, and only
  0.2302 bits is the order-free bag. Corrected after the CRITERION skeptic flagged it (its item 10). Neither
  condition is affected.
- Pre-declared diagnostic, never a gate: on the folds not used during development (0, 1, 3; 2,511 codas) full vs
  twin = +0.5212 [0.4416, 0.6544] and full vs R1 = +0.6634 [0.5911, 0.7792]. Development used folds 2 and 4 only.

Bootstrap: numpy default_rng seed 20261119, resampling with replacement the 188 REC groups that own a scored
position, statistic = pooled per-coda gain (ratio of sums), percentile interval.

## Leakage self-test (built into code/score_content.py)

For every one of the 3,418 held-out scored positions, a copy of its stream had every field (nClicks, Duration,
ICI1-ICI28, Whale, TsTo) of the predicted coda and of every later coda replaced by random values, and the
prediction at that position was recomputed through the normal code path: 0 of 3,418 vectors changed for each of
R1, twin, rep, local and full (bit-identical); a deliberately leaky predictor that reads the predicted coda's
nClicks was flagged at 3,418 of 3,418. Single-position recomputation equals the batch predictions exactly
(max abs difference 0.0). All vectors are strictly positive (min 5.3e-06) and sum to 1 within 6.7e-16.

## Files

- data/sperm-whale-dialogues.csv: sha256 1856c8bf915cc5ae6f928aaa2036cbbc6ad8840bb6e4f6a96aaeb96953215da2, 500,380
  bytes, fetched 2026-11-19T09:39:08Z (HTTP 200) from
  https://raw.githubusercontent.com/pratyushasharma/sw-combinatoriality/7228c8eed2cc27ddd23b74c51aeccec9d762389e/data/sperm-whale-dialogues.csv
- result/folds.csv (REC -> fold), result/bin_edges.csv (4 edges per held-out fold),
  result/probs_R1.csv, result/probs_twin.csv, result/probs_full.csv (per-position 50-vectors; token id
  (c-1)*5+b), result/probs_rep_diagnostic.csv, result/probs_local_diagnostic.csv, result/content_summary.json,
  result/run_output.txt (the frozen run's printed output).
- code/: the frozen code (sha256 equal to PREREG.md's list).
- PREREG.md (frozen 2026-11-19T09:55:11Z, before any held-out score) and PREREG.v2.md (a harness fix on a
  different partial win, p3; nothing in this claim changed).
- baseline/README.md: the baseline record.
- null/null_test.md: the null controls for condition (2) (400 N2 controls). The superseded partial file
  null/null_test_PROVISIONAL.md is kept alongside it for the record.

## Status source (scout record)

https://export.arxiv.org/api/query?search_query=abs:%22sperm%20whale%22&sortBy=submittedDate&sortOrder=descending&max_results=25
fetched 2026-11-19T09:37:53Z, HTTP 200, 40,549 bytes, sha256
1d1a18b7520dbb62d3416d2e8a45e0c0d01378ed080bc6d5929f0fc849c4e94f. Entries newer than the bank's 2026-11-13 check:
2606.16084v5, 2609.16612v3 and 2610.33974v2 (all dated 2026-11-17, Sinha and Chavan) and 2610.29101v1.

## Credit

Data: Sharma, Gero, Payne, Gruber, Rus, Torralba and Andreas, Nature Communications 15:3617 (2024),
https://github.com/pratyushasharma/sw-combinatoriality (DTag recordings of the Dominica Sperm Whale Project).
Prior sequence work this builds on and compares with: WhaleLM (Sharma, Gero, Rus, Torralba, Andreas; bioRxiv
2024.10.31.621071); Sinha and Chavan, arXiv 2606.16084, 2609.16612, 2610.33974.

## Prior public claims in this cell (disclosure; this claim is a record improvement, not first evidence)

This claim was developed independently and is not derived from either PR below. Both were found by the NOVELTY
skeptic after this run's freeze (2026-11-19T09:55:11Z).

- **V3R1T4S draft PR #1159** (another contributor, filed 2026-11-18) is the **first public clearance of the full
  criterion** for this cell: an order-3 n-gram at 2.564371 bits, with R1 2.794781 and twin 2.850952. This claim's
  novelty is therefore the strictly lower cross-entropy (2.1238, a 0.4406-bit improvement) and the larger twin
  gain, not the existence of the effect.
- **V3R1T4S draft PR #1175** (same contributor, created 2026-11-19T09:59:53Z, 4 min 42 s after this run's freeze)
  is the **first public clearance of p4** at 0.780268 bits against the same 0.850317 reference. This claim's p4
  result (0.7631118) beats it on identical positions with an identical reference, on every fold, with a paired
  REC bootstrap of the difference of [0.0034, 0.0334]. Maintainers may wish to credit the p4 cell only once.
- #1159 reported a Dominica p3 figure of +0.097416 and **declined to claim it**, because it failed that PR's
  payload-shuffle control (within-stream CodaType swaps, which preserve each stream's composition). See the p3
  caveat in the run report: the N3 null used here does not preserve stream composition, and by this claim's own
  decomposition only +0.0255 of the +0.1284 p3 gain comes from order beyond a stream-local reference.

## Post-hoc checks (computed after the freeze; disclosed as post hoc; they can only narrow the claim)

- Literal twin reading (posthoc/posthoc_truncated_twin.py, output posthoc/truncated_twin_summary.json): the frozen
  `full` feature map applied to a history truncated to coda t-1 alone, retrained with the same lambda search on the
  same rows, scores 2.6464 bits per coda pooled (pre-registered twin 2.6549); full vs this twin = +0.5226, 95% REC
  bootstrap [0.4463, 0.6273].
- Deployment-level bootstrap (posthoc/contrarian.py; REC strings share 46 tag-deployment prefixes): full vs twin
  [0.4479, 0.6350], full vs R1 [0.5697, 0.7506]; every fold's gain is positive; without the largest REC (729
  positions) full vs twin = +0.5753 (posthoc/contrarian_content_output.txt).
