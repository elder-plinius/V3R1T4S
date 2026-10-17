# Criterion skeptic report: E. coli/Shigella genotype-to-phenotype F1, ampicillin only

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
confirmed_scope: Recomputed from the saved per-isolate file, on the hash-selected 20 percent test partition of NCBI Pathogen Detection export PDG000000004.6366 (1715 ampicillin R/S rows, one per isolate, in 1257 groups made of 365 whole PDS SNP clusters holding 823 rows plus 892 isolates with no PDS accession each kept as its own group), the saved LightGBM predictor scores F1 98.80% and accuracy 98.78% (TP 867, FP 8, TN 827, FN 13) against 94.40% F1 and 94.52% accuracy (TP 792, FP 6, TN 829, FN 88) for the reimplemented published genotype rule on the same rows and the 93.9% F1 and 94.5% accuracy in Table 3 of the saved status-source copy, with a paired 95% cluster-bootstrap interval of 3.06 to 5.88 F1 points for model minus rule, as a database-concordance result for ampicillin only (no other antibiotic, no other export, no clinical or treatment meaning).

## What I fetched or ran

I made no web request (the task forbids it), so I have no HTTP status of my own. The HTTP 200 statuses in CLAIM.md are the claimant's. Everything below ran on files inside claim/; scratch scripts are in work/.

- 2026-10-17T01:25:14Z: listed claim/ (CLAIM.md, REPRODUCE.md, four files in code/, four files in result/, one file in status_source/).
- 2026-10-17T01:27:16Z: sha256sum of the package files:
  - status_source/PMC13513162_fullTextXML.xml e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685 (equals the hash in CLAIM.md)
  - result/split.csv 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca (equals the hash in CLAIM.md)
  - result/scores_ampicillin.json dc7690bd86e5e9acc46485803168b5ff227717c4f94d5c63255c3abce0377546
  - result/test_predictions_ampicillin.csv 86336fdf54be424be5bf2de469e1d3453f64547a10b1f7b98e678a52b46e3379
  - result/model_ampicillin.txt b81e5c99f78edb65e283eb2100fb2aaaeb0c40cdcbc4fa9721ec632619363e02
  - code/ecoli_model.py dec8853545a7c6cbc3949f765d1b7ed644e599a39c92c4feecdc6b9b9fa4096e
  - code/ecoli_prep.py 04edd89fc224f2316896d83556fcabd43312c3173aec29a0c0a7b1c34a388e4b
  - code/ecoli_rules.py bda6261870da679c445eb236a0bf13bf4dffd6d54c3ce44285d74f915585cc3c
  - code/ecoli_rule_check.py 96b08c65b3a9a4e394c81f0b9a5a7f0e4a7fde1e87747eaa5620595ddd2206ac
- 2026-10-17T01:30:10Z: work/verify1.py (metrics and split integrity from result/test_predictions_ampicillin.csv, result/split.csv, result/scores_ampicillin.json).
- 2026-10-17T01:30:50Z: work/verify2.py (cluster bootstrap with seed 20261016, other seeds, 100,000 resamples, McNemar counts, leave-one-cluster-out, strata).
- 2026-10-17T01:32:13Z: work/verify3.py (exact McNemar p, trivial baselines, split-gain shares from the LightGBM text file, export date and AMRFinderPlus checks in the saved XML).
- 2026-10-17T01:34:27Z: parsed the four code files (all parse). The lightgbm library is not installed on this PC, so I read result/model_ampicillin.txt as text instead of loading it.
- 2026-10-17T01:34:48Z: work/verify4.py (bootstrap by stratum).
- 2026-10-17T01:35:58Z: work/verify5.py (lower bounds at stricter confidence levels).
- 2026-10-17T01:36:24Z: re-hashed the saved XML (same e0d80a91... value) and re-printed Table 3.

## Values found

Status source (saved copy): Table 3, Ampicillin row: n 7592, sensitivity 89.4%, specificity 99.0%, accuracy 94.5% (94.0 to 95.0), PPV 98.7%, F1-Score 93.9% (93.3 to 94.4). The same table shows 44.5% F1 for amoxicillin-clavulanic acid, the figure the criterion quotes as read 2026-10-15, so the saved copy matches that earlier read. R is the positive class (rounded sensitivity 89.4 and PPV 98.7 give F1 93.82). The paper text gives the NCBI export date as 11 June 2026, AMRFinderPlus 4.2.7 for all 10,201 eligible records, 495,239 E. coli/Shigella records and 56,141 comparisons, all as CLAIM.md says.

Prediction file, recomputed by me: 1715 rows, 1715 distinct isolates, no repeated isolate-antibiotic key, 880 R and 835 S. Model: TP 867, FP 8, TN 827, FN 13, F1 0.988034, accuracy 0.987755. Rule: TP 792, FP 6, TN 829, FN 88, F1 0.943981, accuracy 0.945190. These equal result/scores_ampicillin.json and CLAIM.md. model_pred equals (model_prob at least 0.5601) on all 1715 rows. The model file has 236 trees and max_feature_idx 226 (227 columns = 213 vocabulary tokens + 14 engineered), matching n_trees 236 and vocab 213 in the JSON.

Bootstrap: re-running the code's procedure (10,000 resamples of the 1257 groups, numpy default_rng seed 20261016) on the saved predictions reproduces all three published intervals exactly (maximum absolute difference 0.0): model F1 98.25 to 99.28, rule F1 92.78 to 95.87, model minus rule 3.06 to 5.88 points. Unrounded: model minus 93.9 = +4.903 points; model minus recomputed rule = +4.405 points.

Split: result/split.csv has 10,836 isolates (8,539 train, 2,297 test) in 8,737 groups. Recomputing int(sha256('V3R1T4S-ecoli-2026-10-16|' + cluster), 16) % 100 below 20 for every group gives 0 mismatches with the recorded split. 0 groups appear in both partitions. All 1715 prediction rows are isolates marked test in split.csv with matching group ids.

## Criterion, clause by clause

- Released predictor and saved per-isolate prediction file: present (result/model_ampicillin.txt, result/test_predictions_ampicillin.csv, one row per test isolate holding the truth, rule_pred, model_prob and model_pred). Met.
- Frozen, hash-pinned export with date and sha256: stated in CLAIM.md (metadata 7eb4639d..., cluster list 58c22fd5..., Last-Modified 2026-10-16 03:34:08 GMT). Stated; not re-hashed by me.
- Paper's eligibility and phenotype mapping as code, applied identically to both predictors: code/ecoli_prep.py builds one R/S table; code/ecoli_model.py scores both predictors on the same test frame, and the prediction file carries both columns for the same 1715 rows. Met.
- Split by SNP cluster (PDS), no cluster spans train and test, split file sha256 committed: verified above. Met, with the composition note below.
- F1 strictly greater than the published F1 by at least 3 points: 98.803 vs 93.9 = +4.90. Also +4.41 over the rule recomputed on the new export (needed because the export is newer than the paper's 11 June 2026 one). Met.
- Outside a 95% bootstrap interval over clusters: 93.9 and 94.40 both lie below the model interval (98.25 to 99.28); 98.80 lies above the rule interval (92.78 to 95.87) and above the paper's own published interval (93.3 to 94.4); the paired interval 3.06 to 5.88 excludes 0 and sits above 3.0. In the bootstrap, 98.05 percent of resamples show a difference of at least 3.0 points. Across 20 other seeds the paired lower bound ranged 3.056 to 3.119 and with 100,000 resamples it was 3.08. Met under every reading I tried.
- Accuracy no lower than published: 98.78 vs 94.5 published (and 94.52 recomputed). Met.
- Full confusion matrix: given for both predictors. Met.
- No clinical or treatment interpretation: CLAIM.md states none is attached and I found none. Met.
- Published number re-read live immediately before claiming: CLAIM.md records fetches at 2026-10-16T17:08:10Z and 2026-10-16T19:28:36Z (HTTP 200, identical hash). I cannot repeat it (no web). The saved copy hashes to the stated value and its Table 3 gives the figures used.

## Hidden quantifiers, stretched definitions, null models

1. Group count. CLAIM.md says "whole SNP clusters (... 1257 clusters)". Only 4,220 of the 10,836 eligible isolates have a PDS accession; 6,616 do not. In the ampicillin test file 365 groups are real PDS clusters (823 rows; largest 61 rows; 171 with more than one row) and 892 groups are single isolates with no PDS. The singleton rule is disclosed in CLAIM.md and the criterion's test (no cluster spans train and test) holds, but 892 of 1715 test rows are effectively isolate-level hold-outs. By stratum (work/verify4.py, same seed, 10,000 resamples): PDS rows model 99.04 (98.34 to 99.59) vs rule 94.99 (92.42 to 97.20), difference 4.05 (2.02 to 6.48); no-PDS rows model 98.53 (97.61 to 99.29) vs rule 93.71 (91.92 to 95.40), difference 4.82 (3.29 to 6.46). The gain appears in both strata, but on PDS rows alone the paired lower bound (2.02) is below 3. The criterion does not restrict to PDS rows, so this is a scope note and I wrote the scope sentence to state the composition.
2. Best of eight. The criterion allows "at least one of the eight antibiotics", so choosing ampicillin after all eight were scored (CLAIM.md history item 1) is permitted. The paired 95% lower bound is only 0.056 above 3.0 (3.056); a 99.375 percent interval (Bonferroni over eight) has lower bound 2.607. The criterion asks for a 3-point margin plus a 95% interval and no multiplicity correction, and the point margins are +4.90 and +4.41, so I treat this as a note, not a failure.
3. Null models. Always-R scores F1 67.82% and accuracy 51.31%; always-S scores F1 0. The recomputed rule (94.40%) is the meaningful null. Model right and rule wrong on 75 rows; rule right and model wrong on 2 rows (exact McNemar two-sided p 3.98e-20). Dropping the single most influential group leaves the difference at 4.03 points (the largest cluster, 61 rows); dropping the three most influential leaves 3.67. The rule's 88 false negatives sit in 71 groups (largest 9). The model's 13 false negatives and 8 false positives sit in 13 and 8 different groups.
4. Not a metadata shortcut. From split gain in the saved LightGBM text file (column roles read from the featurize order in code/ecoli_model.py, since the file has anonymous column names): 70.2% on the count of acquired bla tokens, 10.3% on the eight rule outputs (6.9% on the ampicillin rule), 17.3% on vocabulary tokens, 1.2% on collection year, scientific name and epi type combined. So the model is mostly the rule's own signal plus genotype evidence the published rule discards. Whether a one-line hand patch of the rule would match it cannot be judged here: the contrarian-check outputs named in CLAIM.md history item 2 are not in the package. The criterion compares against the published rule, not a patched one.
5. Leakage paths in code/ecoli_model.py: the threshold comes from out-of-fold train predictions (5-fold GroupKFold by cluster); test labels appear only in the final scoring block (lines 60 to 75); the token vocabulary and category maps are built from train isolates only; the train rows and test rows come from the split column. CLAIM.md discloses later reads of the test rows (history items 2 and 3) with no change to the claimed model.
6. Rule reimplementation. code/ecoli_rules.py is described as calibrated to reproduce the paper's per-comparison predictions; the paper's supplementary tables are not in the package, so the claimed 0 mismatches could not be re-run. The recomputed rule F1 of 94.40 sits at the upper edge of the paper's published interval for 93.9 (93.3 to 94.4), consistent with a faithful copy. The margin over the published figure (+4.90) does not depend on the reimplementation. For the margin over the true rule to drop under 3 points, the true rule would have to score above 95.80 on these rows, 1.4 points above the reimplementation.
7. Released predictor. The model file uses anonymous columns and the token vocabulary is not saved; it is regenerated deterministically by code/ecoli_prep.py and code/ecoli_model.py from the pinned export (REPRODUCE.md). That satisfies "released predictor" but the package alone cannot score a new isolate.
8. Timing. The last recorded live re-read of the status source (2026-10-16T19:28:36Z) is about six hours older than this review. The criterion wants the re-read immediately before claiming, so repeat it at the moment of posting.

## Not verified by me

- sha256 and contents of the two NCBI files (not in the package; no web use allowed).
- The live status source (no web use allowed); only the saved copy was checked.
- The rule's exact replication of the paper's supplementary predictions and eligibility flags (the supplementary zip is not in the package).
- A full re-run of code/ecoli_prep.py and code/ecoli_model.py (needs the 551 MB export).
- PREREG.md, which CLAIM.md cites but which is not in the package. The criterion does not require pre-registration, so I judged the quoted thresholds directly.

## Decision

Read literally, the ampicillin claim meets the full success criterion on the evidence in the package: strictly higher F1 than the published 93.9% (+4.90) and than the rule recomputed on the same new export (+4.41), each by more than 3 points, outside the 95% cluster-bootstrap intervals, accuracy above the published 94.5%, full confusion matrices for both predictors, same rows for both, a clean whole-group split with its hash, a released model and per-isolate prediction file, and no clinical claim. The notes above (singleton groups, best-of-eight, thin paired lower bound, unverified raw-data hashes and rule replication, stale status re-read) narrow the scope sentence but do not break any quoted clause.

pass: true
