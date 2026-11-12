# PREREG.v7: partial win p1 attempt (cross-cohort T2D, held-out cohort fixed here)

frozen_utc: 2026-11-12T19:56:59Z

Written before any abundance table of the held-out cohort has been parsed and before any model of this attempt is
fitted. Seen so far for the held-out cohort: label counts only (attempts/p1-cross-cohort/out/meta_counts.txt).
Nothing in earlier PREREG files changes.

null_test: required (unchanged for the run; for p1 see N-p1 below)

## Criterion (verbatim, bank partial win p1)

"A strictly leak-free cross-cohort result for one disease (train on cohorts A..., test on an untouched cohort B of the
same disease) with AUC >= 0.70 and a documented pre-registration of the held-out cohort, together with the within-cohort
number for context."

## Pre-registered held-out cohort B

curatedMetagenomicData MetaCardis_2020_a (relative abundance 2022-10-19, sha256 e26ebf50...32ee; Fromentin/
Forslund MetaCardis, France/Germany/Denmark). Positives: study_condition "T2D" (550). Negatives (primary reading,
the analogue of the non-diabetic/NGT controls of the training cohorts): disease "healthy" (234). Secondary (reported,
not the pass reading): all study_condition "control" (642, which includes metabolic syndrome and IGT). No model,
feature choice or threshold is developed on B; B is scored once with the frozen model.

## Training cohorts A

curatedMetagenomicData QinJ_2012 (T2D 170 vs control 174) and KarlssonFH_2013 (T2D 53 vs control 43; IGT excluded),
relative abundance 2021-10-14 (sha256 95cf4ea5...87a and d7641026...1fd). Features: MetaPhlAn3 species present in the
union of the two training cohorts (species names; B's columns are aligned to them, missing species = 0); B-only
species are dropped. Per-sample transforms only (no use of B's feature distribution).

## Development on A only, then freeze

Dev metric: mean of the two cross-study AUCs (train Qin -> test Karlsson; train Karlsson -> test Qin). Candidates
(fixed list): (a) RF500 sqrt on relative abundance (MetAML's model); (b) RF500 on presence/absence (> 0);
(c) L2 logistic on training-standardised log10(abundance/100 + 1e-5), species with prevalence >= 10% in training,
C in {0.01, 0.1, 1} (three candidates). The candidate with the best dev metric (ties: earlier in the list) is
frozen, refitted on Qin + Karlsson together (random_state 0), and applied once to B.

## Pass and reporting

Pass: AUC on B (primary negatives) >= 0.70 (single held-out evaluation, the bank's number; a 95% interval from 2,000
stratified bootstrap resamples of B is reported, not a gate). Reported next to it: the secondary-negatives AUC, the
AUC within each country of B, and, for context, B's within-cohort AUC by 10-fold CV x 5 of the same frozen model
type (computed after the held-out score is written).

## Null N-p1

400 controls: the frozen model applied to B with B's labels permuted (seeds 0..399); the real AUC must beat all.
(This is a sanity null; the bank's bar is the 0.70.)

## Escape hatches

If species alignment leaves fewer than 50% of the frozen model's features present in B, report it and still score.
No second p1 attempt on B in this run.
