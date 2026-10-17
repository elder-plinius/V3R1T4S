Criterion skeptic report: E. coli ciprofloxacin cluster-held-out F1 claim (target ncbi-pathogen-ast-ecoli-genotype-phenotype-f1)
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
confirmed_scope: On the 10,836 eligible isolates of NCBI Pathogen Detection export PDG000000004.6366 (hash-pinned in CLAIM.md) with the whole-PDS-cluster split in result/split.csv (sha256 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca), a LightGBM predictor over exported AMR-genotype tokens plus collection year, species label and epi_type scores ciprofloxacin resistant-class F1 96.13% (95% cluster-bootstrap interval 93.65% to 97.84%) and accuracy 98.35% (TP 348, FP 12, TN 1317, FN 16) on 1693 isolate comparisons in 1246 held-out clusters, against 80.36% F1 and 89.72% accuracy (TP 356, FP 166, TN 1163, FN 8) for the reimplemented published genotype-field rule on the same rows (paired F1 difference 95% interval 11.09 to 21.88 points) and 77.2% F1 and 89.9% accuracy published in Table 3 of PMC13513162, as a single-split database-concordance result for ciprofloxacin only with no clinical or treatment meaning.

## What I fetched or ran

No web access was used (the task forbids it), so I made no HTTP requests and have no HTTP status of my own to report. The statuses and fetch times quoted from CLAIM.md below are the claim's own record and were not re-observed by me. Everything else is from commands run in Git Bash with Python on the saved files; scratch scripts are in work/ (xml_tables.py, xml_text.py, xml_text2.py, xml_text3.py, check1.py to check5.py).

Shell clock (date -u): 2026-10-17T01:25:11Z at start, 2026-10-17T01:27:13Z at the hashing step, 2026-10-17T01:32:42Z and 2026-10-17T01:33:21Z at the last two analysis steps.

1. Package contents (ls): CLAIM.md, REPRODUCE.md, code/ (ecoli_model.py, ecoli_prep.py, ecoli_rules.py, ecoli_rule_check.py), result/ (model_ciprofloxacin.txt, scores_ciprofloxacin.json, split.csv, test_predictions_ciprofloxacin.csv), status_source/PMC13513162_fullTextXML.xml. There is no PREREG.md inside claim/ although CLAIM.md cites one.

2. sha256sum at 2026-10-17T01:27:13Z:
   - status_source/PMC13513162_fullTextXML.xml e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685 (identical to CLAIM.md)
   - result/split.csv 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca (identical to CLAIM.md)
   - result/test_predictions_ciprofloxacin.csv 66e32eea192baad34c9e892bc9fc82eb32a87668791890db310c345b5961052f
   - result/model_ciprofloxacin.txt c34685133ecb4692265e356b30973952eb0905b10a60c7d697e41e53758f97d5
   - result/scores_ciprofloxacin.json 9d226565b2067fb76e147e2bc0842427604dea8f6da02cd38e2e57a2631052a1
   - code/ecoli_model.py dec8853545a7c6cbc3949f765d1b7ed644e599a39c92c4feecdc6b9b9fa4096e; code/ecoli_prep.py 04edd89fc224f2316896d83556fcabd43312c3173aec29a0c0a7b1c34a388e4b; code/ecoli_rules.py bda6261870da679c445eb236a0bf13bf4dffd6d54c3ce44285d74f915585cc3c; code/ecoli_rule_check.py 96b08c65b3a9a4e394c81f0b9a5a7f0e4a7fde1e87747eaa5620595ddd2206ac

3. Published baseline, parsed from the saved XML (Table 3, "prespecified primary analysis"): ciprofloxacin N R/S AST 7615, sensitivity 97.3%, specificity 88.4%, accuracy 89.9% (89.3 to 90.6), PPV 63.9%, NPV 99.4%, balanced accuracy 92.8%, F1 77.2% (75.5 to 78.7). Amoxicillin-clavulanic acid F1 in the same table is 44.5%, which equals the example the criterion itself quotes as read 2026-10-15, so the saved table is the table the criterion points to. The paper defines F1 as 2 x TP / (2 x TP + FP + FN), the harmonic mean of PPV and sensitivity (resistant class positive); sensitivity 97.3 and PPV 63.9 give 0.7714, consistent with the printed 77.2. The claim uses the same definition. The paper's only alternative rule (post hoc) is for amoxicillin-clavulanic acid; no other published ciprofloxacin F1 appears in the saved text.
   CLAIM.md records the status source fetched 2026-10-16T17:08:10Z (HTTP 200) and again 2026-10-16T19:28:36Z (HTTP 200) with identical sha256; I confirmed only the hash of the saved copy.

4. Recomputed from result/test_predictions_ciprofloxacin.csv: 1693 rows, 1693 unique isolates (no duplicated or conflicting R/S rows), 1246 unique clusters, test R count 364 (prevalence 21.5%).
   - Model: TP 348, FP 12, TN 1317, FN 16; F1 0.96133 (96.13%), accuracy 0.98346 (98.35%).
   - Rule (rule_pred column, same rows): TP 356, FP 166, TN 1163, FN 8; F1 0.80361 (80.36%), accuracy 0.89722 (89.72%).
   - Both match result/scores_ciprofloxacin.json and CLAIM.md exactly. model_pred equals (model_prob at or above the stored threshold 0.3437) on all 1693 rows; no probability lies within 0.0005 of the threshold.

5. Split integrity (result/split.csv, 10,836 isolates, 8,737 clusters): clusters spanning train and test 0; PDS root accessions spanning train and test 0 (2,121 PDS clusters, 4,220 isolates; 6,616 isolates with no PDS are their own cluster); 0 rows disagree with the stated rule (test iff int(sha256 of 'V3R1T4S-ecoli-2026-10-16|' + cluster, base 16) mod 100 is below 20); every prediction isolate is a test row in split.csv with the same cluster; no test cluster appears in train. Test share is 2,297 of 10,836 isolates (21.2%).

6. Bootstrap replicated with the same algorithm and seed (numpy default_rng 20261016, 10,000 resamples of the 1246 clusters, all rows of a cluster kept together): model F1 interval 0.936507 to 0.978449, rule F1 interval 0.733724 to 0.857656, paired difference interval 0.110918 to 0.218781. These equal the stored values in result/scores_ciprofloxacin.json to 1e-9. Other seeds (1, 2, 3; 4,000 resamples): paired difference lower bounds 10.90 to 10.99 points, upper bounds 21.75 to 21.84 points. Across the 10,000 replicates the smallest paired difference is 7.15 points and the share below 3 points is 0.0. Accuracy difference interval (model minus rule) 6.58 to 11.01 points. Interval widened to 99.375% (Bonferroni over the eight antibiotics): 9.52 to 24.67 points.

7. Robustness and null checks on the saved predictions:
   - Dropping the largest 1, 3, 10 test clusters: model F1 0.9627, 0.9539, 0.9488 versus rule 0.8050, 0.7635, 0.7643.
   - The 881 comparisons (52.0%) from isolates with no PDS accession: model F1 0.9360, accuracy 0.9818; rule F1 0.7219, accuracy 0.8933. The 812 comparisons from 365 real PDS clusters: model F1 0.9747, accuracy 0.9852; rule F1 0.8540, accuracy 0.9015.
   - Per-cluster paired comparison: model more correct in 117 clusters, rule more correct in 6, tied in 1123; exact one-sided sign test p about 4.2e-28.
   - Trivial predictors: always-resistant F1 0.3539. The model's resistant calls (360) are a strict subset of the rule's (522): zero rows where the model says R and the rule says S; the model removed 162 rule R calls, 154 correctly (rule false positives) and 8 wrongly (true positives lost). So the 8 extra misses come from filtering, and the whole gain is false-positive removal.
   - Training-side sanity: out-of-fold (5-fold group by cluster) train F1 is 0.9570 against 0.9613 on test, so there is no sign of test-specific tuning or leakage.

8. Released model file (result/model_ciprofloxacin.txt): 213 trees, max_feature_idx 226 (227 columns = 213 vocabulary tokens + 14 engineered columns), matching n_trees 213 and vocab 213 in the scores file. Gain share by column: top vocabulary token 33.24%, the rule's own ciprofloxacin call 31.91%, collection year 7.25%, count of gyrA/parC/parE POINT annotations 6.87%, epi_type 1.87%, species label 0.96%. The three non-genotype metadata columns together carry 10.08% of gain; genotype-derived columns carry 89.92%. The model uses AMR_genotypes tokens, rule outputs, collection year, scientific_name and epi_type only; AST_phenotypes is read for labels and is not a feature (code/ecoli_model.py featurize).

9. Wording scan (grep for clinical, treatment, patient, therapy, dose, prescribe): the only hits are the criterion text and the sentence in CLAIM.md that says no clinical or treatment interpretation is attached.

## Criterion, element by element

- Released predictor plus saved per-isolate prediction file: met (result/model_ciprofloxacin.txt with code/ecoli_model.py; result/test_predictions_ciprofloxacin.csv carries isolate, cluster, AST_call, rule_pred, model_prob, model_pred).
- Frozen hash-pinned export with date and sha256 published: published in CLAIM.md (Last-Modified 2026-10-16 03:34:08 GMT, metadata sha256 7eb4639d4aa7c621927d0a55e6d185801f4af77401c270f7ad14f3c9ce6d101b, cluster list sha256 58c22fd5c39d083dae3963d332c5ec25ac22c39a4f42675b37e1bb7ca954a7c8). Met as stated; bytes not re-downloaded by me.
- Eligibility and phenotype mapping reimplemented as code and applied identically to both predictors: code/ecoli_prep.py builds one eligible table and one long R/S table; the model and the rule are scored on the identical 1693 rows. Met.
- Held-out partition split by SNP cluster, no cluster spans train and test, split file with sha256: met (items 5 and the matching hash).
- F1 strictly greater than the published F1: 96.13% against 77.2% published, a margin of 18.93 points. Met.
- At least 3 points AND outside a 95% bootstrap interval over clusters: against published 77.2%, the model's interval lower bound 93.65% is 16.45 points above; against the recomputed rule, margin 15.77 points and paired interval 11.09 to 21.88 points, which excludes both 0 and 3; the model's F1 is also above the rule's own interval (up to 85.77%). Every reading of "outside the interval" is satisfied. Met.
- Accuracy no lower than published: 98.35% against 89.9% published (and against 89.72% recomputed). Met.
- Full confusion matrix reported: both matrices in CLAIM.md and result/scores_ciprofloxacin.json, and I recomputed them. Met.
- Newer export: published rule recomputed on the same new rows and beaten (80.36% against 96.13%). Met.
- No clinical or treatment interpretation: met (item 9).
- Same comparison rows for model and rule: yes, row for row (item 4).

## Hidden quantifiers and stretched definitions

- F1 definition: same as the paper (resistant class, 2TP over 2TP plus FP plus FN). No macro or weighted substitution.
- "SNP cluster": real PDS accessions where NCBI assigns one; 52.0% of test comparisons are isolates with no PDS accession, each treated as its own cluster. That is the only possible treatment of isolates NCBI did not cluster, it is stated in CLAIM.md and the code, and the model wins in both the singleton and the PDS-cluster subsets. I cannot check from the package whether two target records of one BioSample could fall on opposite sides of the split as separate singletons; the criterion defines the partition by PDS accession, so this is a caveat and not a criterion failure.
- Multiple antibiotics: all eight were scored once and ciprofloxacin is reported. The criterion says "for at least one of the eight", and the 99.375% interval (9.52 to 24.67 points) still excludes 3 points, so the selection does not change the result.
- Baseline strength: the published rule counts any gyrA point annotation as resistant, which is why its precision is low; the claim does not hide this, it recomputes the rule on the same rows. The recomputed rule behaves like the published one (sensitivity 97.8% against 97.3%, specificity 87.5% against 88.4%, PPV 68.2% against 63.9%, accuracy 89.72% against 89.9%). For a faithful-reimplementation error to erase the margin, the true rule would need F1 of at least 93.13% on these rows, against 77.2% published, which is not plausible.
- Metadata features: collection year, species label and epi_type are used (10.08% of gain) and the claim says so openly ("exported AMR genotype annotations and collection metadata"). The criterion does not restrict features, so this is allowed; the confirmed_scope names them rather than calling the predictor genotype-only.
- Test-label history: CLAIM.md discloses three uses of the test rows and states that none changed features, hyperparameters, threshold or split. I cannot read PREREG.md (not in claim/), so any pre-registered threshold beyond the criterion's own (3 points, cluster-bootstrap interval, accuracy no lower, newer-export recomputation) is unchecked; I applied the criterion's thresholds from its verbatim text.
- Non-subsumed: the only published result on this benchmark is Table 3 of PMC13513162 (77.2% F1 for ciprofloxacin); nothing in the saved paper offers a higher ciprofloxacin figure, and this is the full cluster-split criterion, not a weaker partial win (the claim keeps the random-split variant out of this claim).

## Not verified by me, and conditions on the pass

1. Live re-read of the paper immediately before claiming: not done (no web allowed). The saved copy matches the hash CLAIM.md records and contains the 44.5% example value. The poster must repeat the live re-read at posting time and re-judge if ciprofloxacin F1 77.2% or accuracy 89.9% has changed.
2. The metadata TSV and cluster list were not re-downloaded or re-hashed, the model was not retrained, and the reimplemented rule was not re-run against the paper's supplementary tables (the claim reports 0 mismatches over 56,141 predictions; that needs a download). My checks cover the saved predictions, split, scores, model file and baseline table, and they agree with each other and with CLAIM.md.
3. Minor release weakness: the column-to-token vocabulary is not saved as its own file; it is rebuilt by code/ecoli_model.py from the pinned export and split.csv, so the model file alone is not a standalone predictor. This does not breach the criterion, which asks for a released predictor plus prediction file.
4. If NCBI removes the PDG000000004.6366 directory, third parties would hold only the hashes; the criterion asks for date and hash, which are published.

## Verdict

On the evidence in claim/, the result meets the full success criterion for ciprofloxacin literally: same rows for model and rule, cluster-disjoint split with committed hash, margin of 15.77 points over the recomputed rule and 18.93 over the published 77.2%, paired cluster-bootstrap interval 11.09 to 21.88 points, accuracy and full confusion matrices reported, no clinical wording. No hidden quantifier or stretched definition changes that. The conditions above are process items for the poster (final live re-read) or checks outside my sandbox, not defects in the evidence I could read.
pass: true
