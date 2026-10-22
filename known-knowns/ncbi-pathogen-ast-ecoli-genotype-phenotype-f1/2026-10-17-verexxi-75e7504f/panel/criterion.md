# Criterion review: E. coli gentamicin LightGBM vs the published genotype-field rule (target ncbi-pathogen-ast-ecoli-genotype-phenotype-f1)

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)

confirmed_scope: On the single pre-fixed hash split of NCBI export PDG000000004.6366 (1623 gentamicin R/S comparisons in 1192 groups, of which 357 are PDS SNP clusters and 835 are isolates with no PDS accession treated as singletons), the saved LightGBM gentamicin predictor scores F1 96.28% and accuracy 98.64% (TP 285, FP 9, TN 1316, FN 13) against 92.41% and 97.17% (TP 280, FP 28, TN 1297, FN 18) for the reimplemented published genotype rule on the identical rows, which is 3.88 F1 points above the published 92.4% and 3.87 above the recomputed rule, with the model F1 above the rule's 95% percentile cluster-bootstrap interval (88.09% to 95.31%) and accuracy above the published 97.6%; this is a database-concordance result for gentamicin on that one partition only, carries no clinical interpretation, and rests on a published-figure re-read and NCBI file hashes that this review could not re-check.

## What I fetched or ran

- Network: none. I was told not to use the web, so no URL was fetched and there is no HTTP status to report. I did not re-read the Europe PMC source and did not download the NCBI metadata or cluster list.
- Clock (date -u): first reading 2026-10-17T01:25:12Z, last reading 2026-10-17T01:33:40Z.
- Judged only the claim package. sha256sum of the files as I found them:
  - CLAIM.md eb34ac40dd462cb6f4892a3b857864347f3e10f31499f6d256681efa87e5722e
  - REPRODUCE.md 5883e6e45a0c345c10cd6529e9e063a424d7489b0d5a6cf6d90ab5849d5f2e3a
  - status_source/PMC13513162_fullTextXML.xml e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685 (equals the hash recorded in CLAIM.md)
  - result/split.csv 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca (equals the hash recorded in CLAIM.md)
  - result/test_predictions_gentamicin.csv 75e7504f005731e2bf48b7bf8484b44a98afecd30fa4c58fbe7041eb9fb48d28
  - result/scores_gentamicin.json adad9247862e9ed2830751b154395c3f9e84b77d73d97818829c65c7bf734ebd
  - result/model_gentamicin.txt 75f88e78b536702a64817e5a0de4073944373d99d685ef28880f13693e3e0715
  - code/ecoli_prep.py 04edd89fc224f2316896d83556fcabd43312c3173aec29a0c0a7b1c34a388e4b
  - code/ecoli_rules.py bda6261870da679c445eb236a0bf13bf4dffd6d54c3ce44285d74f915585cc3c
  - code/ecoli_model.py dec8853545a7c6cbc3949f765d1b7ed644e599a39c92c4feecdc6b9b9fa4096e
  - code/ecoli_rule_check.py 96b08c65b3a9a4e394c81f0b9a5a7f0e4a7fde1e87747eaa5620595ddd2206ac
- Python (3.14, pandas, numpy) scratch scripts in the sibling work folder, run on the saved files only: XML table and paragraph scans, split and prediction integrity checks, an exact re-run of the claim's cluster bootstrap, subset and discordance checks, a model-file parse, and threshold and leave-one-cluster-out sensitivity.
- Not in the package, so not checked: the NCBI metadata TSV and cluster list (so ecoli_prep.py and ecoli_model.py could not be re-run), the paper's supplementary tables NCBI_S8 and NCBI_S9 (so the claimed zero-mismatch rule check could not be re-run), PREREG.md (cited in CLAIM.md as frozen before fitting), and results for the other seven antibiotics.

## Clause by clause against the success criterion

1. Published baseline (status_source). Parsed with ElementTree. Article ids: pmcid PMC13513162, doi 10.3390/ijms27167157. Table 3 gentamicin row: 7344 R/S comparisons, sensitivity 93.6%, specificity 98.3%, accuracy 97.6% (97.2 to 97.9), PPV 91.1%, NPV 98.8%, balanced accuracy 96.0%, F1 92.4% (91.2 to 93.5). The same table gives amoxicillin-clavulanic acid F1 44.5%, matching the example quoted in the criterion. Methods text defines F1 as 2TP over (2TP + FP + FN) with resistant as the positive class, uses percentile bootstrap intervals, and states the export date 11 June 2026 and AMRFinderPlus 4.2.7. The paper gives no other gentamicin figure and no alternative gentamicin rule (its only alternative-rule analysis is blaTEM-1 for amoxicillin-clavulanic acid). So the bar is F1 92.4% and accuracy 97.6%. The live re-read itself I could not repeat (see item 11).

2. Same rows for model and rule. result/test_predictions_gentamicin.csv has 1623 rows, 1623 distinct isolates, antibiotic gentamicin only, columns isolate, antibiotic, cluster, AST_call, rule_pred, model_prob, model_pred. Both confusion matrices sum to 1623 with 298 R and 1325 S, so they are scored on identical rows. No isolate has more than one gentamicin row, so no conflicting R and S duplicates. In code/ecoli_model.py both predictors are applied to the same test table: the model on features of those isolates, the rule through ecoli_rules.predict on the same AMR_genotypes field. The eligibility and R/S mapping (code/ecoli_prep.py) is built once and shared.

3. Metrics recomputed from the saved predictions. Model: TP 285, FP 9, TN 1316, FN 13, F1 0.9628378, accuracy 0.9864449. Rule: TP 280, FP 28, TN 1297, FN 18, F1 0.9240924, accuracy 0.9716574. These equal result/scores_gentamicin.json and CLAIM.md. model_pred equals (model_prob at least 0.4751) on all 1623 rows (0 mismatches).

4. Strictly greater, by at least 3 points. Model F1 96.2838% minus published 92.4% is 3.8838 points; minus the recomputed rule 92.4092% is 3.8745 points. Both are at least 3 and strictly positive. Accuracy 98.64% is not below the published 97.6% (and not below the recomputed rule's 97.17%).

5. Outside a 95% bootstrap interval over clusters. I re-ran the claim's bootstrap (10,000 resamples of test clusters, numpy default_rng seed 20261016, percentile 2.5 and 97.5, same pairing of model and rule). It reproduced scores_gentamicin.json exactly: model F1 interval 93.682 to 98.0, rule F1 interval 88.09 to 95.307, paired difference interval 1.805 to 6.954. The text does not say whose interval, so I checked the natural readings: (a) model F1 96.28 is above the upper end 95.31 of the rule's cluster-bootstrap interval, and only 0.3% of rule resamples reach it; (b) the published 92.4 is below the lower end 93.68 of the model's interval (0.2% of model resamples are at or below 92.4); (c) the paired difference excludes zero in 100% of resamples. All pass. A much stricter reading (lower end of the paired interval at least 3 points) would fail, since that end is 1.81; the criterion text does not say that, it separates "at least 3 points" from "outside a 95% bootstrap interval".

6. Held-out split by SNP cluster, split file hash. result/split.csv has 10836 rows, 10836 distinct target_acc (matches the 10,836 eligible isolates in CLAIM.md), 8737 distinct cluster labels, and 8539 train rows and 2297 test rows. No cluster label carries more than one split value (0 clusters). I recomputed the stated rule, test if int(sha256 of the salt string plus cluster, 16) mod 100 is below 20, for every row: 0 mismatches. All 1623 prediction rows are test isolates in split.csv with the same cluster label. File hash matches CLAIM.md.

7. No test-label use in fitting. Reading code/ecoli_model.py: the genotype vocabulary (tokens seen in at least 10 train isolates) and the species and epi_type codes come from train isolates only; the number of trees (mean best iteration over 5 GroupKFold-by-cluster folds) and the decision threshold 0.4751 come from out-of-fold train predictions; test labels are first used in the final scoring block. The released model file agrees with the code and with scores_gentamicin.json: 243 trees, learning rate 0.03, 15 leaves, bagging 0.8, L2 1, seed 20261016, 227 features (213 vocabulary tokens plus 14 engineered). Features are AMR genotype tokens, token counts, the published rule's output for each of the eight antibiotics, collection year, scientific_name and epi_type; no AST phenotype of any antibiotic is a feature. Gain share in the model file: the rule's own gentamicin output (column 218) 69.2%, collection year 2.0%, token count 3.0%.

8. Released predictor and per-isolate predictions. result/model_gentamicin.txt (LightGBM text model) plus the code, and result/test_predictions_gentamicin.csv with one row per test isolate. The vocabulary needed to apply the model is not saved separately; it is regenerated deterministically from the pinned export and split by the code (documented in REPRODUCE.md). Acceptable for the clause, but the model file alone is not a standalone predictor.

9. Newer export, rule recomputed and beaten. The export is dated 2026-10-16 (CLAIM.md), the published numbers come from 2026-06-11. The rule was recomputed on the same new rows (F1 92.41%) and the model beats it by 3.87 points, with the interval checks in item 5 also taken against that recomputation.

10. Confusion matrix and no clinical interpretation. Full TP, FP, TN, FN reported for both predictors in CLAIM.md and the json. A grep for clinical, treatment, patient, therapy and diagnosis in CLAIM.md, REPRODUCE.md and the code finds only the criterion's own sentence and the claim's disclaimer ("database-concordance benchmark for surveillance. No clinical or treatment interpretation is attached").

11. Live re-read "immediately before claiming". CLAIM.md records fetches of the status source at 2026-10-16T17:08:10Z and 2026-10-16T19:28:36Z (HTTP 200, same sha256, Table 3 unchanged). I can confirm only that the saved copy has that hash and shows gentamicin F1 92.4% and accuracy 97.6%. My first clock reading is 2026-10-17T01:25:12Z, about six hours after the last recorded re-read, so the filer must re-read Table 3 again at the moment of filing. Likewise the export hashes (metadata 7eb4639d..., cluster list 58c22fd5...) are as stated in CLAIM.md and were not re-checked by me.

## Null-model and robustness checks on the saved predictions

- Paired discordance: rule wrong and model right 27 rows; rule right and model wrong 3; both wrong 19; both right 1574. Exact McNemar p about 8.4e-06 (row level, ignores clustering). Cluster-level sign-flip test on net corrected rows (observed net gain 24, 20,000 flips, seed 1): p about 0.0003. The 30 disagreements fall in 23 clusters, at most 4 in any cluster. So the gain is spread over many clusters, not one outbreak.
- Where the gain comes from: rule false positives fall from 28 to 9 (22 removed, 3 added), false negatives from 18 to 13.
- Subsets: isolates with no PDS accession (835 rows, 115 R): model F1 94.22 vs rule 91.23. Rows in real PDS clusters (788 rows, 357 clusters, 183 R): 97.55 vs 93.12. Clusters with more than one gentamicin row (162 clusters, 593 rows): 97.96 vs 94.04. The advantage appears in each subset.
- Leave-one-cluster-out: smallest paired margin 3.261 (dropping cluster PDS000225708.42), largest 4.597; no single cluster removal takes it below 3.0. Dropping the 8 clusters with 10 or more rows (187 rows) gives model 95.00 vs rule 90.51, margin 4.49.
- Threshold sensitivity on test (threshold was fixed from train out-of-fold): thresholds 0.30 to 0.80 give F1 95.71 to 96.61, margins 3.30 to 4.20; at 0.20 it drops to 93.44 (margin 1.03). Only 6 rows have probability between 0.35 and 0.60. The result is not a knife-edge on the threshold.
- Interval-method sensitivity: percentile is what the paper and the code use. A basic (reverse percentile) interval for the rule would be 89.51 to 96.73, which would contain the model's 96.28; the basic interval for the paired difference is 0.80 to 5.94, still excluding zero.
- Seed sensitivity (8 other seeds, 4000 resamples): the rule's upper bound stays 95.21 to 95.37; the paired lower bound 1.77 to 1.88.
- Multiplicity (best of eight antibiotics): the criterion allows "at least one of the eight", so this is not a violation. As a stress check, the 99.375% paired interval is 1.18 to 8.32, still excluding zero.

## Hidden quantifiers and stretched definitions found

- "1192 clusters" and "whole SNP clusters": 835 of the 1192 groups are isolates with no PDS accession, each treated as its own singleton; only 357 are real PDS clusters (788 rows). This is a reasonable operational reading of "split by PDS accession" and is stated in the code, but the count overstates how many SNP clusters were held out. The scope sentence says so.
- "LightGBM predictor over genotype annotations and metadata": the published rule's output is itself a feature (69.2% of gain), so the model is the published rule plus a learned correction. Not prohibited; the rule is a function of the same genotype field.
- "Published rule recomputed": it is the claimant's regex reimplementation, described in the code as calibrated to reproduce the paper's per-comparison predictions. The claimed zero-mismatch check against 56,141 published predictions cannot be re-run from the package. The gentamicin regex (aac(3), aac(6')-Ib, IIc, Il, ant(2''), armA, rmt, npmA; COMPLETE or POINT status) is consistent with the paper's text for aminoglycosides.
- The 3-point margin is thin relative to noise. The point margin is 3.88 against a bar of 3 (0.88 spare); 77.6% of cluster resamples give a paired margin of at least 3, and 75.5% of model resamples exceed 95.4 (published plus 3). The model's out-of-fold train F1 is 94.73% against 96.28% on test, so the test draw is somewhat favorable. The criterion is a point-estimate gate on the frozen partition, so this does not fail it, but it is not evidence that the true effect is 3 points or more.
- PREREG.md and the test-label history (an exploratory read of the same test rows after the primary scoring, with no model change) are asserted in CLAIM.md; I could not check the timeline.

## Decision

Every clause of the success criterion that can be tested from the package holds for gentamicin on the frozen partition: same 1623 rows for both predictors, F1 96.28% vs published 92.4% and recomputed 92.41% (margins 3.88 and 3.87), model above the rule's 95% cluster-bootstrap interval, accuracy 98.64% vs 97.6%, split verified with no cluster spanning train and test and the recorded hash, no test-label use in fitting or threshold choice, full confusion matrices, no clinical claim. The win is not driven by one cluster, one subset or the threshold. Open items for the filer, none of which changes the numbers above: re-read Table 3 at filing time, confirm the NCBI file hashes, and keep the scope as narrow as the sentence above.

pass: true
