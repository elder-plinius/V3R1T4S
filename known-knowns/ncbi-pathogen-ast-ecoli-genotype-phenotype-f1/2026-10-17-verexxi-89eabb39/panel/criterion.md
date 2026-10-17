# Criterion skeptic report: ceftriaxone claim, target ncbi-pathogen-ast-ecoli-genotype-phenotype-f1

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)

confirmed_scope: On the hash-defined test partition of NCBI Pathogen Detection export PDG000000004.6366 (1531 ceftriaxone comparisons in 1114 groups, of which 337 are PDS SNP clusters holding 754 rows and 777 are unclustered isolates treated as one-isolate groups), the LightGBM predictions saved in result/test_predictions_ceftriaxone.csv score F1 97.66% (95% cluster-bootstrap CI 96.32% to 98.69%) and accuracy 98.76% with TP 396, FP 10, TN 1116, FN 9, which is 3.06 points above the published 94.6% F1 (published accuracy 97.9%) and 3.15 points above the published genotype rule recomputed on the same rows (F1 94.51%, accuracy 97.19%, paired-difference CI 1.21 to 5.44 points), for ceftriaxone only, as a database-concordance result with no clinical interpretation, and with the margin over the 3-point bar only 0.06 points (one more test error would put it below the bar).

## Short verdict

The result meets the full success criterion as it is literally written, for ceftriaxone, by a very thin margin. Every numeric clause I could test from the saved files holds. Two scope facts must travel with the claim: half of the test rows are not in any NCBI SNP cluster, and the 3-point bar is cleared by 0.06 points. Items that need data or the web are listed at the end as not tested by me.

## What I fetched or ran

All file names are relative to claim/ (commands were run from the folder that contains claim/). I made no network requests, because web use is not permitted in this role. I therefore have no HTTP status of my own to report. The two fetch times and HTTP 200 statements for the paper in CLAIM.md (2026-10-16T17:08:10Z and 2026-10-16T19:28:36Z) are the claimant's statements and were not re-checked by me.

Timestamps from `date -u` during the session: 2026-10-17T01:25:13Z (start), 2026-10-17T01:27:33Z (after hashing), 2026-10-17T01:32:27Z (after the paper identity check), 2026-10-17T01:34:45Z (after the singleton check), 2026-10-17T01:36:17Z (last check). All analysis below ran inside that window.

1. `ls` and `find` on claim/: CLAIM.md, REPRODUCE.md, code/ (ecoli_model.py, ecoli_prep.py, ecoli_rules.py, ecoli_rule_check.py), result/ (model_ceftriaxone.txt, scores_ceftriaxone.json, split.csv, test_predictions_ceftriaxone.csv), status_source/PMC13513162_fullTextXML.xml. Not in claim/: PREREG.md (CLAIM.md says it was frozen before any model was fitted), the input data, and the scores for the other seven antibiotics.
2. `sha256sum` of every file (2026-10-17T01:27:33Z):
   - status_source/PMC13513162_fullTextXML.xml e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685 (equals the hash in CLAIM.md)
   - result/split.csv 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca (equals the hash in CLAIM.md)
   - result/test_predictions_ceftriaxone.csv 89eabb391ad14ed90c3a4092923eb720d3cc7a870aed165011fe24aa9a193bc3
   - result/scores_ceftriaxone.json b48f8a55010b4dacdf6f6cfb7d940791a2233a7c0a6ad9e8f3a385f123ce36a8
   - result/model_ceftriaxone.txt 36b252abf1c9dbef0e76dd22741f90a7cf0fd6677b67603598cb232422c39223
   - code/ecoli_model.py dec88535..., code/ecoli_prep.py 04edd89f..., code/ecoli_rules.py bda62618..., code/ecoli_rule_check.py 96b08c65...
   - Python 3.14.4, numpy 2.4.0, pandas 2.3.3. lightgbm and scikit-learn are not installed and I did not install them (that needs the web), so I could not re-score the model file.
3. Parsed the saved paper XML with Python. Identity: article title "Antibiotic-Specific Genotype-Phenotype Concordance and Cross-Database Interoperability in Public Escherichia coli/Shigella WGS-AMR Metadata", PMC13513162, DOI 10.3390/ijms27167157, International Journal of Molecular Sciences volume 27. Table 3 ceftriaxone row: N 6841, sensitivity 92.1%, specificity 99.3%, accuracy 97.9% (97.5-98.2), PPV 97.3%, NPV 98.0%, balanced accuracy 95.7%, F1 94.6% (93.7-95.4). The abstract repeats "ceftriaxone (accuracy, 97.9%; F1-score, 94.6%)". The same table gives amoxicillin-clavulanic acid F1 44.5%, which equals the example the criterion quotes as read 2026-10-15, so the saved copy is consistent with the live document of that date. Methods: F1 is 2 x TP / (2 x TP + FP + FN) with R as the positive class; NCBI export dated 11 June 2026; paper bootstrap is isolate-level. Counts 495,239, 10,201 and 56,141 appear in the paper.
4. Split checks on result/split.csv: 10836 rows, 10836 distinct isolates, 8737 distinct clusters. Recomputing int(sha256("V3R1T4S-ecoli-2026-10-16|" + cluster), 16) % 100 below 20 as the test rule reproduces the split column on all 10836 rows (0 mismatches). Clusters spanning train and test: 0. Isolates: train 8539, test 2297 (clusters: train 6998, test 1739). Isolates with no PDS accession: 6616, each its own group named NOPDS_ followed by its own accession (naming verified); isolates with a PDS accession: 4220 in 2121 PDS clusters.
5. Per-isolate file checks (result/test_predictions_ceftriaxone.csv): 1531 rows, 1531 distinct isolates, 1114 clusters, only ceftriaxone, no duplicate isolates; every isolate is present in split.csv, marked test, and carries the same cluster label. model_pred equals (model_prob at or above the 0.3253 threshold in scores_ceftriaxone.json) on all rows (0 mismatches).
6. Recomputed metrics from that file: model F1 0.976572, accuracy 0.987590, TP 396, FP 10, TN 1116, FN 9; rule F1 0.945083, accuracy 0.971914, TP 370, FP 8, TN 1118, FN 35. These equal result/scores_ceftriaxone.json and CLAIM.md. Test rows: 405 R and 1126 S.
7. Re-ran the claim's own cluster bootstrap (10,000 resamples, numpy default_rng seed 20261016, same code as code/ecoli_model.py) on the saved predictions. Model F1 CI 96.323 to 98.692, rule F1 CI 92.231 to 96.577, paired difference CI 1.211 to 5.437 (percent). All three equal scores_ceftriaxone.json to three decimals. Share of resamples with paired difference of at least 3 points: 0.5198; with model F1 minus 94.6 of at least 3 points: 0.5504; with paired difference of zero or less: 0.0.
8. Strata, leave-one-cluster-out and error budget on the same file (details below).
9. Read result/model_ceftriaxone.txt: 211 trees; parameters learning_rate 0.03, num_leaves 15, min_data_in_leaf 20, bagging_fraction 0.8, feature_fraction 0.8, lambda_l2 1, seed 20261016 (match the P dictionary in code/ecoli_model.py). Feature split counts (saved importance type is split count): 90 features used in 2699 splits; collection year 432, number of genotype tokens 384, the ceftriaxone rule flag 145, count of gyrA/parC/parE point mutations 114.

## Clause by clause against the success criterion

- At least one of the eight antibiotics: ceftriaxone is one of the eight (Table 2 lists 6841 comparisons in the paper; ANTIBIOTICS list in code/ecoli_rules.py). Confirmed.
- Released predictor plus saved per-isolate prediction file: result/model_ceftriaxone.txt plus code, and result/test_predictions_ceftriaxone.csv. Confirmed present. Caveat: the 213-token feature vocabulary is not stored with the model; code/ecoli_model.py rebuilds it from the training split.
- Frozen, hash-pinned export with export date and sha256 published: CLAIM.md gives the URLs, Last-Modified 2026-10-16 03:34:08 GMT, 551123573 bytes and sha256 7eb4639d... (metadata), and sha256 58c22fd5... (cluster list). Published: yes. Checked against the data: no (data is not in claim/).
- Paper's eligibility and phenotype-mapping rules reimplemented as code and applied identically to both predictors: code/ecoli_prep.py and code/ecoli_rules.py exist; both predictors are scored on the same 1531 rows in one file. Confirmed for the identical-rows part. That the code reproduces the paper's 10,201 records and 56,141 comparisons exactly is claimed but needs the paper's supplement: not tested.
- Held-out partition split by SNP cluster, no cluster spans train and test, split file with sha256: confirmed by items 2 and 4 (hash matches, rule reproduces every label, 0 spanning clusters). See caveat on unclustered isolates below.
- F1 strictly greater than the published genotype-field-inference F1: 97.6572 against 94.6 (Table 3 and abstract). Confirmed.
- By at least 3 points absolute: 3.0572 points. If the published 94.6 is rounded and the true value were as high as 94.65, the margin is still 3.0072. Confirmed.
- Outside a 95% bootstrap interval over clusters: the criterion does not say which interval. Under each natural reading it holds: published 94.6 lies below the model CI lower bound 96.323; the model F1 97.657 lies above the upper bound of the recomputed rule CI (96.577) and above the paper's own CI upper bound (95.4); the paired difference CI 1.211 to 5.437 excludes zero. Confirmed under these readings; see the strict reading below.
- Accuracy no lower than published: 98.7590 against 97.9. Confirmed (also above the recomputed rule's 97.1914).
- Full confusion matrix reported: yes for both predictors (CLAIM.md and result/scores_ceftriaxone.json), and I recomputed it. Confirmed.
- Newer export, so recompute the rule on the same new export and beat it: rule F1 94.5083 on the same rows against model 97.6572 (plus 3.1489 points, accuracy 98.7590 against 97.1914). Confirmed, and it would also meet a stricter "at least 3 points" reading of "beat".
- No clinical or treatment interpretation: CLAIM.md states a database-concordance benchmark with no clinical interpretation; I found none. Confirmed.
- Status source re-read live immediately before claiming: not repeated by me. The saved copy hashes to the value the claimant recorded and shows 94.6% and 97.9%. The claimant records re-reads at 2026-10-16T17:08:10Z and 2026-10-16T19:28:36Z.
- No partial win is used: CLAIM.md says the random-split and June-record secondaries are not used for this claim.

## Hidden quantifiers and stretched definitions

1. "Whole SNP clusters ... 1114 clusters" overstates cluster protection. Of the 1114 test groups, 337 are PDS clusters (754 rows) and 777 are one-isolate pseudo-clusters for isolates with no PDS accession (777 rows, 50.8% of test rows; 69.7% of test groups). In the eligible set 6616 of 10836 isolates (61%) have no PDS accession. CLAIM.md does disclose "isolates without a PDS are singletons", so this is disclosure, not concealment, and "no cluster spans train and test" is literally true. But the leakage protection of an SNP-cluster split applies to only half the test rows. Strata (my computation from the saved file):
   - PDS rows only (754 rows): model F1 98.84, accuracy 99.20; rule F1 96.22, accuracy 97.48.
   - Unclustered rows only (777 rows): model F1 95.59, accuracy 98.33; rule F1 91.43, accuracy 96.91.
   - Neither stratum alone is 3 points above both comparators (PDS rows: plus 4.24 over 94.6 but plus 2.62 over the recomputed rule; unclustered rows: plus 0.99 over 94.6 but plus 4.16 over the recomputed rule). The pooled partition clears both (3.06 and 3.15). The criterion is written for the whole held-out partition, so I judge the pooled numbers, and I name the composition in the scope.
2. Strict reading of "outside a 95% bootstrap interval". If it meant that the 3-point margin itself must hold at the interval edge (paired difference lower bound of at least 3 points, or model CI lower bound of at least 97.6), the claim would fail (1.211 and 96.323). The text does not say that. It says "by at least 3 points absolute AND outside a 95% bootstrap interval", which I read as a point margin of at least 3 plus statistical separation from the baseline; both hold. I flag this as the one interpretive risk.
3. The 3-point bar is cleared by 0.06 points and is fragile.
   - With TP 396, 19 errors give F1 97.657 (margin 3.057) and 20 errors give 97.537 (margin 2.937). The claim has exactly 19 errors (10 FP plus 9 FN).
   - Leave-one-cluster-out: removing any one of 3 of the 1114 clusters (PDS000202052.3 with 61 rows, PDS000117091.440 with 31 rows, PDS000076588.1 with 12 rows) drops the margin over 94.6 below 3 (2.822, 2.863, 2.986). Removing PDS000202052.3 alone gives model 97.422 and rule 95.265, margins 2.822 over 94.6 and 2.157 over the recomputed rule. That cluster has 37 R and 24 S rows; the rule is wrong on 9 and the model on 0, so it supplies 9 of the 24 net errors the model removes (rule 43 errors, model 19).
   - Only about half of cluster resamples keep the paired difference at 3 points or more (0.5198). The bar is met on the pre-fixed partition; it is not met robustly. This is not a literal failure, but the claim must not be worded as a robust 3-point win.
4. Selection among eight antibiotics: the primary job scored all eight and the claim is ceftriaxone only. The criterion allows "at least one of the eight", so this is permitted, but no multiplicity adjustment applies to the CI and the other seven results are not in claim/.

## Null models and baseline checks

- Trivial nulls on the test rows: always-S accuracy 73.55% with R-class F1 0; always-R accuracy 26.45% with R-class F1 41.84%. Neither is near the bar.
- Baseline fidelity (the main null-model risk, a weakened baseline): the recomputed rule on the test rows has sensitivity 91.36% and specificity 99.29%, against the paper's 92.1% and 99.3%, and F1 94.51% against 94.6%. The baseline is not weakened.
- Model versus rule structure: the model never turns a rule-positive into a negative (0 of 378 rule-positive rows). It adds 28 positives beyond the rule: 26 are true R and 2 are true S. So the whole gain is recovery of 26 of the rule's 35 false negatives at the cost of 2 extra false positives. The error table is: rule right and model right 1486; rule wrong and model right 26; rule right and model wrong 2; both wrong 17.
- The model leans heavily on collection year, genotype-token count and a gyrA/parC/parE point-mutation count (item 9) as well as the rule flag. That is allowed (CLAIM.md says inputs are the genotype annotations and collection metadata), but the gain is not demonstrably from gene identity alone. No results of simple alternative rules (the claimant's "contrarian checks") or a metadata-only model are in claim/, so I cannot say whether a one-line patch to the paper's rule would match the model. The criterion does not require beating such a rule.
- Training-side leakage in code: the vocabulary, categories and early-stopping folds use training isolates only, the threshold 0.3253 is chosen on out-of-fold training predictions (5-fold GroupKFold by cluster), AST_phenotypes is never used as a feature, and the out-of-fold training F1 is 0.9706 against test 0.9766 (no sign of test-driven tuning). This is from reading code/ecoli_model.py and scores_ceftriaxone.json.

## Not tested by me (accepted only on the claimant's record, or left open)

- The metadata and cluster-list sha256 values and the export date: the data is not in claim/.
- That result/test_predictions_ceftriaxone.csv really comes from result/model_ceftriaxone.txt and that the rule predictions are the rule applied to the genotype field: no features or genotype data, no LightGBM installed.
- That the rule reproduces the paper's 56,141 predictions and eight confusion matrices with 0 mismatches: needs the paper's supplementary tables.
- PREREG.md and the statement that the model, features, threshold and split were frozen before test labels were read; the contrarian checks on the same test rows (about 18:40Z) are described but not shown.
- The live re-read of the status source: web use was not allowed for me.
- Whether any other published result already exceeds 94.6% F1 for ceftriaxone on this kind of data: I only had the bank's comparator (Table 3 of the paper).

## Reasoning

The success criterion is a list of mechanical clauses, and every clause that can be tested from the claim package holds on the saved per-isolate file: F1 97.66% against 94.6% published (plus 3.06 points) and against 94.51% recomputed on identical rows (plus 3.15 points), accuracy 98.76% against 97.9%, published value outside the model's cluster-bootstrap interval, paired difference interval above zero, full confusion matrices, a split file whose hash matches and whose labels follow the stated hash rule with no spanning cluster, and no clinical interpretation. The baseline is faithful, the bootstrap reproduces exactly, and I found no feature that uses the phenotype. The weak points are about margin and scope, not about a failed clause: a 0.06-point margin that three clusters can flip, a test set that is half unclustered isolates, and an undefined "outside the interval" that fails only under a stricter reading than the text supports. I therefore confirm a narrow win and write the scope to carry those facts. Items I could not test without the data or the web are listed above and belong to the reproduction and provenance checks, not to this criterion check.

pass: true
