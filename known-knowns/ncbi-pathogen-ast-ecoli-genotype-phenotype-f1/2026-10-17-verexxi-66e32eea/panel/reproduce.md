# REPRODUCE skeptic report: ciprofloxacin F1 claim on NCBI Pathogen Detection export PDG000000004.6366

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)

Summary: for ciprofloxacin, every number in CLAIM.md reproduced exactly, both from my own independent checker and from three runs of the unchanged pipeline. I found no mismatch, no missing object and no non-determinism in the claimed result. The only difference I saw is a Windows line-ending artifact (CRLF) that does not touch content; I removed it to get byte-exact matches (section 6, item 1).

All times are UTC from `date -u` on this PC, 2026-10-17. Python is the shared venv (3.12.13; pandas 3.0.6, numpy 2.5.4, scikit-learn 1.9.1, lightgbm 4.7.0, versions printed by importlib.metadata). My scratch scripts and logs are in work/ (my_step1 to my_step11). Files below are named relative to claim/.

## 1. The definition I checked against (quoted from CLAIM.md)

Success criterion, verbatim:

```
Success means, for at least one of the eight antibiotics, a released predictor plus a saved per-isolate prediction file on a frozen, hash-pinned export of the NCBI Pathogen Detection E. coli/Shigella metadata (export date and sha256 published), with the paper's eligibility and phenotype-mapping rules reimplemented and published as code and applied identically to both predictors, evaluated on a held-out partition split by SNP cluster (PDS accession; no cluster spans train and test, split file committed with sha256), whose F1 for that antibiotic is STRICTLY GREATER (direction: max) than the published genotype-field-inference F1 for that antibiotic, re-read live from https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML immediately before claiming (e.g. 44.5% for amoxicillin-clavulanic acid as read 2026-10-15), by at least 3 points absolute AND outside a 95% bootstrap interval over clusters, with accuracy no lower than the published accuracy for that antibiotic and the full confusion matrix reported. Because the published numbers come from a 2026-06-11 export, a claim on a newer export must also recompute the published rule on the same new export and beat that recomputation. No clinical or treatment interpretation may be attached.
```

Rules CLAIM.md states for the pipeline (also used as my definition):
- eligibility and phenotype mapping: "assembly, AMR genotypes and AST phenotypes all present; R/S only; the eight antibiotics; exact duplicate rows collapsed".
- split: "whole SNP clusters (PDS_acc from cluster_list.tsv; isolates without a PDS are singletons)"; an isolate is TEST when the integer value of the SHA-256 hex digest of the salt string 'V3R1T4S-ecoli-2026-10-16|' followed by the cluster name, taken modulo 100, is below 20.

Instruction from the kit: "Before reading the author's code, write your own checker from the definition (quote it). Verify every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism."

## 2. Order of work

I read CLAIM.md, REPRODUCE.md, the saved result files and the paper XML (Table 3 and the Methods text), then wrote and ran my own checker (steps 1 to 5 below) before opening any file in code/. Only then did I read the four short scripts in code/ and run them, from a scratch copy whose four files have the same sha256 as claim/code, with PYTHONDONTWRITEBYTECODE set, so claim/ stayed untouched. Everything I verified was checked on all rows (all 589,253 metadata rows, all 10,836 split rows, all 1,693 predictions, all 495,239 paper records, all 7,615 published ciprofloxacin predictions), never a sample. The claim has no exhaustive-search component.

## 3. Log

1. 06:03:29Z to 06:03:31Z, sha256sum of the pinned files. All match CLAIM.md:
   - data/PDG000000004.6366.metadata.tsv 7eb4639d4aa7c621927d0a55e6d185801f4af77401c270f7ad14f3c9ce6d101b (551123573 bytes)
   - data/PDG000000004.6366.reference_target.cluster_list.tsv 58c22fd5c39d083dae3963d332c5ec25ac22c39a4f42675b37e1bb7ca954a7c8 (22021637 bytes)
   - status_source/PMC13513162_fullTextXML.xml e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685
   - result/split.csv 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca
   - also recorded: result/test_predictions_ciprofloxacin.csv 66e32eea192baad34c9e892bc9fc82eb32a87668791890db310c345b5961052f, result/model_ciprofloxacin.txt c34685133ecb4692265e356b30973952eb0905b10a60c7d697e41e53758f97d5, result/scores_ciprofloxacin.json 9d226565b2067fb76e147e2bc0842427604dea8f6da02cd38e2e57a2631052a1.

2. 06:05:15Z to 06:05:25Z, my_step1_parse.py (csv module, tab delimiter). 589,253 data rows, 67 columns, no row with a wrong width, target_acc unique. By organism name 587,717 records are E. coli or Shigella and 1,536 are other Escherichia (albertii, fergusonii, and so on). AST_phenotypes items: S 103047, ND 36828, R 28772, I 2486, DD 54, NS 21. amrfinder_version is 4.2.7 for all 11,052 records that have an AST field.

3. 06:05:44Z to 06:05:48Z, my_step2_eligible.py, my own eligibility and mapping from the definition. Records with assembly accession, AMR genotypes and AST phenotypes all non-NULL: 10,836. That set equals the isolate set of result/split.csv exactly (0 only in mine, 0 only in the split file). Long R/S table for the eight antibiotics: 58,347 rows before and after collapsing exact duplicates (nothing to collapse); 2 isolate-antibiotic keys carry both R and S, none of them for ciprofloxacin. Ciprofloxacin: 7,923 comparisons (R 1,526, S 6,397).

4. 06:06:02Z to 06:06:04Z, my_step3_split.py. Cluster list: 380,990 rows, 59,507 distinct PDS, no isolate under more than one PDS. I recomputed cluster and train/test for all 10,836 isolates from the hash rule and compared with result/split.csv: 0 cluster-name mismatches, 0 train/test mismatches (train 8,539 isolates, test 2,297, 8,737 clusters, 0 clusters on both sides). Ciprofloxacin: 6,230 train, 1,693 test, 1,246 test clusters, test R 364, test S 1,329. These equal n_train, n_test, n_test_clusters and test_R in result/scores_ciprofloxacin.json.

5. 06:06:34Z to 06:06:35Z, my_step4_metrics.py. result/test_predictions_ciprofloxacin.csv: 1,693 rows, no duplicate isolate, no blank cell, isolate set equal to my derived ciprofloxacin TEST set, 0 AST_call mismatches against my labels, 0 cluster mismatches. My own confusion matrices and metrics from the file:
   - model: TP 348, FP 12, TN 1317, FN 16, F1 0.961326, accuracy 0.983461
   - published rule recomputed on the same rows: TP 356, FP 166, TN 1163, FN 8, F1 0.803612, accuracy 0.897224
   - both equal result/scores_ciprofloxacin.json (F1, accuracy and counts, to the last digit).
   - model_pred equals "probability at or above 0.3437" on every row (lowest probability predicted R 0.346059, highest predicted S 0.335916).

6. 06:07:09Z to 06:07:12Z, my_step5_boot.py, my own cluster bootstrap (10,000 resamples of the 1,246 clusters, numpy default_rng(20261016), percentile 2.5 and 97.5):
   - model F1 interval 0.9365 to 0.9784 (claimed 93.65% to 97.84%)
   - rule F1 interval 0.7337 to 0.8577 (claimed 73.37% to 85.77%)
   - paired difference interval 0.1109 to 0.2188 (claimed 11.09% to 21.88%)
   - model F1 exceeded rule F1 in all 10,000 resamples, and by at least 0.03 in all 10,000.
   - seeds 1, 2, 3 give paired intervals 0.1097 to 0.2184, 0.1104 to 0.2176, 0.1101 to 0.2176.
   - point differences: model minus recomputed rule 0.1577; model minus published 0.772 is 0.1893.

7. 06:07:21Z to 06:07:22Z, live re-read of the status source with curl: HTTP 200, 218472 bytes, sha256 e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685, byte-identical (cmp) to status_source/PMC13513162_fullTextXML.xml. Table 3, ciprofloxacin row, read from the XML: N R/S AST 7615, accuracy 89.9% (89.3 to 90.6), F1-score 77.2% (75.5 to 78.7).

8. 06:08:29Z, HEAD requests only (no download) to the two NCBI URLs. Both HTTP/1.1 200 OK. Metadata: Last-Modified Fri, 16 Oct 2026 03:34:08 GMT, Content-Length 551123573 (the export date CLAIM.md states). Cluster list: Last-Modified Fri, 16 Oct 2026 09:31:48 GMT, Content-Length 22021637.

9. Code read after step 8 (code/ecoli_prep.py, ecoli_rules.py, ecoli_model.py, ecoli_rule_check.py). Findings are in section 5.

10. 06:08:46Z to 06:08:54Z, `python -P -s code/ecoli_prep.py data/PDG000000004.6366.metadata.tsv data/PDG000000004.6366.reference_target.cluster_list.tsv prep`. Output: 589253 rows in export, 10836 eligible, 4220 with a PDS, 8737 clusters, amrfinder 4.2.7 for all 10836, 58347 long R/S rows, 2 conflicting keys, ciprofloxacin n 7923 R 1526, test n 1693 R 364. These agree with my steps 3 and 4.

11. 06:09:56Z to 06:11:15Z, `python -P -s code/ecoli_model.py prep rerun cluster` (all eight antibiotics, exit 0, "JOB DONE"). The REPRODUCE.md estimate of 3 to 5 minutes per antibiotic was far too high here; the whole run took 79 seconds.

12. 06:11:32Z, my_step6_compare.py, rerun versus claim for ciprofloxacin:
    - rerun results.json entry for ciprofloxacin equals result/scores_ciprofloxacin.json for every key and value (Python equality, including all float digits, threshold 0.3437, 213 trees, oof_train_f1, CIs).
    - the 1,693 rerun prediction rows equal result/test_predictions_ciprofloxacin.csv in every cell (including model_prob to 6 decimals, order and columns).
    - model file: 213 trees in both; identical bytes except CR characters (see section 6, item 1).

13. 06:11:53Z to 06:12:08Z, downloaded the paper's supplementary package from EuropePMC supplementaryFiles: HTTP 200, 32354723 bytes, sha256 20c239859ba85c3666fe646f0bcefa834b660eca0b538518cbb2cf0e7eebcdc7. It holds the nested NCBI package (S1, S7, S8, S9, S10).

14. 06:12:55Z, my_step7_rule.py, the published rule against the paper's own predictions. S9 has 7,615 ciprofloxacin rows (R 1331, S 6284); recomputed from S9, the published ciprofloxacin confusion is TP 1295, FP 731, TN 5553, FN 36, F1 0.7715, accuracy 0.8993, which reproduces Table 3 (77.2% and 89.9%) and the S10 row. The author's code/ecoli_rules.py predicts all 7,615 ciprofloxacin S9 rows with 0 mismatches, and its matched-marker sets equal the S9 matched_markers column in all 7,615 rows. My own first implementation written only from the S7 sentence (any gyrA, parC, parE, qnr, qepA, oqx or aac(6')-Ib-cr marker) disagreed with S9 in 89 rows (84 when only COMPLETE and POINT tokens count). So the author's narrower parC rule is what the paper's outputs require.

15. 06:13:33Z to 06:13:39Z, my_step8_s1.py on the paper's S1 (495,239 records), my own code. My eligibility (assembly, genotype and AST present) has 0 row-level mismatches against the paper's has_assembly, has_amr_genotypes, has_ast_phenotypes and eligible_genotype_phenotype flags, and gives 10,201 eligible records. My R/S mapping on those records gives 56,141 rows, equal as a multiset of (isolate, antibiotic, call) to S9; ciprofloxacin 7,615 rows (R 1,331, S 6,284).

16. 06:13:48Z to 06:13:50Z, the author's ecoli_rule_check.py unchanged on the NCBI package: "mismatches 0" for all eight antibiotics; ciprofloxacin TP 1295, FP 731, TN 5553, FN 36, F1 0.771522. The eight matrices sum to TP 11752, FP 2524, TN 40942, FN 923, 56141 comparisons, equal to the paper's Table 4.

17. 06:13:57Z to 06:15:21Z, second unchanged run of ecoli_model.py (output folder rerun2). results.json (sha256 3a76c93bfb2cebc65b8f3424c76e23fbfd59978fdf01da21af0bd97342b85c54), test_predictions.csv for all eight antibiotics (sha256 6385ef7a23b8f3d697f2ef2c734493434d2ffbf4236beafe98a8e2c0d5d6938f) and all eight model files are byte-identical between run 1 and run 2.

18. 06:15:51Z to 06:15:57Z, my_step9_simple.py, a plausibility check only: a transparent genotype-only predictor fit on TRAIN labels alone with my own featurization (counts of gyrA 83/87, parC 80/84, other gyrA/parC, parE and plasmid markers). Depth-3 decision tree: TEST F1 0.9143, accuracy 0.9628 (TP 336, FP 35, TN 1294, FN 28); depth 4: F1 0.9193, accuracy 0.9652. My crude any-marker rule reproduces the author's rule baseline confusion exactly (356, 166, 1163, 8).

19. 06:18:31Z to 06:21:07Z, the unchanged prep and model scripts run through a 5-line wrapper that only sets os.linesep to LF (what pandas would write on Linux). REPRODUCE.md's own check, `cmp prep/split.csv result/split.csv`, printed "split identical"; the script's printed split hash is 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca. The ciprofloxacin slice of the rerun predictions is byte-identical to result/test_predictions_ciprofloxacin.csv (sha256 66e32eea192baad34c9e892bc9fc82eb32a87668791890db310c345b5961052f). The scores entry equals result/scores_ciprofloxacin.json.

20. 06:23:34Z, `sha256sum -c` over the 11 hashed files of claim/ against the hashes from step 1: all OK; no file in claim/ modified since I started; 14 files, none added.

## 4. Clause by clause

- Released predictor plus saved per-isolate predictions: result/model_ciprofloxacin.txt (213 trees) and result/test_predictions_ciprofloxacin.csv (1,693 rows) are present and are regenerated bit for bit by the unchanged code. PASS.
- Frozen, hash-pinned export with date and sha256: both sha256 values and sizes match; HEAD shows Last-Modified Fri, 16 Oct 2026 03:34:08 GMT for the metadata file. PASS.
- Eligibility and phenotype mapping as code, applied identically to both predictors: my independent implementation gives the same isolate set (10,836), the same labels and the same cipro counts as code/ecoli_prep.py; on the paper's own S1 and S9 both reproduce the paper's flags and its 56,141-row table. Model and rule are scored on the same 1,693 rows of one file. PASS.
- Split by SNP cluster, no cluster on both sides, split file with sha256: recomputed from the stated hash rule, 0 mismatches against result/split.csv, 0 clusters spanning, sha256 68a7e358... PASS.
- F1 strictly greater than the published F1: 96.13% against 77.2% published (difference 18.93 points). PASS.
- At least 3 points AND outside a 95% bootstrap interval over clusters: 96.13% against the recomputed rule 80.36% is 15.77 points; the paired interval is 11.09% to 21.88% (lower end above 3 points and above 0); the model interval 93.65% to 97.84% lies wholly above the rule interval 73.37% to 85.77%, and 96.13% is outside the rule interval. PASS under every reading of "outside".
- Accuracy no lower than published: 98.35% against 89.9% published (and 89.72% for the recomputed rule). PASS.
- Full confusion matrix reported: model TP 348, FP 12, TN 1317, FN 16; rule TP 356, FP 166, TN 1163, FN 8; both reproduced by me. PASS.
- Newer export: published rule recomputed on the same export and beaten: rule_pred column, F1 80.36%, accuracy 89.72%; baseline fidelity is shown in log items 14 to 16. PASS.
- Published F1 re-read live: done at 06:07:21Z, HTTP 200, file identical to the saved copy. PASS.
- No clinical or treatment interpretation: CLAIM.md says the result is a database-concordance benchmark with no clinical or treatment interpretation, and I found none. PASS.

## 5. Threats I tested

- Label leakage. From code/ecoli_model.py: features are indicators for AMR_genotypes tokens seen at least 10 times among TRAIN isolates (213 of them), plus 14 extras: token count, acquired-bla count, gyrA/parC/parE point-mutation count, the eight genotype-rule indicators, collection year, scientific_name code and epi_type code. That is 227 features, matching max_feature_idx=226 in the saved model file. No AST_phenotypes, number_drugs_* or other phenotype-derived column is read in featurize; vocabulary and category codes come from TRAIN isolates only; the threshold is the F1 maximiser on out-of-fold TRAIN predictions (5-fold GroupKFold by cluster); test labels appear only in the final scoring block, after predictions exist. The out-of-fold TRAIN F1 (0.9570) is close to the TEST F1 (0.9613), which gives no sign of test-specific tuning. My step 9 shows a plain genotype-only tree trained on TRAIN alone already gets TEST F1 0.91 to 0.92, so the gain over the rule (0.80) has a visible genotype mechanism and is not an artifact.
- Baseline fidelity (is the "published rule" a strawman?). The author's rule reproduces all 56,141 published predictions, all eight published confusion matrices and the matched-marker sets (log items 14 to 16). A literal reading of the S7 sentence gives a lower baseline on the TEST rows (F1 0.7876, accuracy 0.8866, 18 rows differ from rule_pred), so the author's baseline is the stronger of the readings. The saved rule_pred column is reproduced on all 1,693 rows by the marker families visible in S9.
- Non-determinism. Three runs on this PC (run 1, run 2, wrapper run) plus the author's saved files from a different machine give identical scores, predictions and model files, apart from CR characters.
- Eligibility without an organism filter. code/ecoli_prep.py does not filter by organism, while my implementation does (E. coli and Shigella names only); both give the same 10,836 isolates, so no E. albertii or E. fergusonii record is eligible and the missing filter has no effect on this export. The line `elig = elig[... | True]` in ecoli_prep.py is a no-op.
- Conflicting duplicates: none for ciprofloxacin, so the "retain non-identical duplicates" rule does not matter here.

## 6. Caveats and what I could not verify

1. Windows line endings. On Windows the unchanged scripts write CRLF. The first rerun's prep/split.csv therefore failed REPRODUCE.md's `cmp` at character 25 of line 1 (CR before LF), raw sha256 9b5ac08e89f7b1e8ed4d07f2d825fa805edf5a4d45b0597369eb5d463e9ce668; with CR removed it is identical to result/split.csv (sha256 68a7e358...). LightGBM also writes CRLF into the model text file (rerun model sha256 5a16f4836510e31a21a34d3b11f670a55569bd92edbcdc745a7f0255224354ed against the claim's c34685133ecb4692265e356b30973952eb0905b10a60c7d697e41e53758f97d5); identical after CR removal, and I could not change LightGBM's writer. Content is identical in every case; REPRODUCE.md's `cmp` lines assume a POSIX shell.
2. CLAIM.md's "Test-label evaluation history" mentions a PREREG.md frozen before any model was fitted and a single scoring of the TEST clusters. PREREG.md is not in the package, and the timeline of past test-label use cannot be verified from files. This is not a clause of the success criterion. What I can say from the code is that no step before final scoring reads test labels, and the pipeline is deterministic, so the saved numbers are what the frozen code produces.
3. 4,220 of the 10,836 eligible isolates have a PDS; the other 6,616 are singleton clusters by the claim's rule. Cluster disjointness is by PDS accession only, so near-identical genomes outside the cluster list could in principle sit on both sides. That is exactly the bank's definition of the split, so it does not breach the criterion, and I did not measure it.
4. The pipeline fits all eight antibiotics and the claim reports ciprofloxacin (the criterion says "at least one"). The gain is not blanket: in the same run tetracycline (paired interval -0.0041 to 0.0022) and trimethoprim-sulfamethoxazole (-0.0084 to 0.0132) show no gain. For ciprofloxacin the margin is far larger than any selection effect among eight.
5. I reran the author's code in the pinned package versions, on a different machine from the author's; I did not re-implement LightGBM or train with other library versions. Novelty against literature beyond the bank's published number is outside a reproduce check.
6. At the end of my work one python job was running on the PC from a sibling panel folder for a different claim, started at 06:21:58Z. It is another agent's job and I did not touch it. All my own background jobs finished with exit code 0 before I wrote this report; none of mine is left running.

## 7. Verdict

Every property of the ciprofloxacin claim that can be checked from the package and the pinned sources checked out: data hashes, live status source, eligibility, labels, cluster split, predictions, F1 and accuracy recomputed from predictions and labels, confusion matrices, cluster-bootstrap intervals, baseline fidelity against the paper's own predictions, and an exact, repeatable rerun of the released pipeline. No mismatch, missing required object or non-determinism was found.

pass: true
