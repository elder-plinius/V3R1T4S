# Panel skeptic REPRODUCE: p3 confound audit, T2D in the MetAML benchmark (run 2026-11-12-1824)

context: subagent (Claude Code Agent tool, subagent_type reproduce, fresh context)

Inputs read: claim/ only (CLAIM.md, REPRODUCE.md, prereg/, folds/, inputs/, results/, code/, audit_results.csv,
bank_entry.json). Nothing else in the run folder was read. All work was done on a copy of claim/ in a separate scratch
folder. Machine limits were respected (2 threads, under 300 MB per process; one exception, which I killed, is noted
under "Problems found").

Kit instruction followed: before reading the author's code I wrote my own checker from the PREREG.md definitions:
loaders, cohort and fold checks, covariate-only LR, species RF, pair decomposition, null N1, and a within-study
permutation with my own RNG. Definitions quoted in my checker:

- "Species features: rows whose name contains "|s__" and not "|t__" (MetaPhlAn2 species level), values as given."
- "W1 = dataset_name in {t2dmeta_long, t2dmeta_short} with disease in {t2d, n}; W2 = dataset WT2D with disease in
  {t2d, n} ...; external healthy controls for P2 = disease "n" and bodysite "stool" from Quin_gut_liver_cirrhosis,
  Zeller_fecal_colorectal_cancer, hmp, hmpii, metahit. Label 1 = t2d." "Study = pubmedid".
- "sequencing depth = log10(number_reads) from curatedMetagenomicData sampleMetadata.rda ..., matched by sample id"
- "Folds: StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=r), r = 0..19, stratified on the label,
  grouped by subjectID"
- "Species model M_sp ...: RandomForestClassifier(n_estimators=500, max_features="sqrt", criterion="gini",
  random_state=1000*r+k), fitted on the training folds only."
- "Covariate model M_cov (primary): numeric covariates -> median imputation with missing-indicator -> standardise;
  categorical (country, study) -> one-hot (unknown ignored); LogisticRegression(C=1.0, max_iter=5000)."
- "AUC statistic: mean of the 200 per-fold test AUCs (10 folds x 20 repeats). Interval (primary): MetAML-style margin
  t(0.975, df=9) x mean over repeats of the per-repeat fold standard error". "Fractions R4 carry the AUC interval
  through the same formula", with "f = (AUC_x - 0.5) / (AUC_published - 0.5)".
- "Within-study permutation (R3): reduced species pipeline (RF n_estimators=100, otherwise as M_sp) on the repeat-0
  folds, mean fold AUC; 400 permutations (seeds 0..399) per setting, labels shuffled within study".
- null_test.md: "study-of-origin-only logistic regression, mean per-fold AUC on the repeat-0 grouped folds ...
  Controls: the identical pipeline with the study column permuted across samples (numpy default_rng seeds 0..399)."

## Verdict

Every number in the claim object (claim/audit_results.csv, 70 rows) that I recomputed agrees exactly with the saved
outputs. Every headline number in the claim sentence was rerun in full and matches. Most of those reruns used my own
independent code; the P2 permutation set was rerun in full with the author's script (all 401 rows identical) and
checked independently with my own RNG. The four species-RF baselines reproduce bit for bit from my own code: all
200 per-fold AUCs and every out-of-fold score. I found no leakage: the corrupted-test-fold test passes. The null
test N1 reproduces exactly. I found no mismatch, no missing object and no non-determinism. Thread count does not
change the results: my 2-thread reruns equal the author's runs bit for bit, and the author's default is 4 threads.

## What was rerun in full (independent code unless stated)

| item | result |
|---|---|
| Input hashes | abundance.txt.bz2 64b505c9...dcc16 and sampleMetadata.rda 168c8650...3444 both match REPRODUCE.md |
| Cohorts | My own parser gives 3610 samples and 1291 species. Counts: W1 344 (170/174), W2 96 (53/43), P1 440 (223/217), P2 882 (223/659). Depth: my own streaming .rda reader matched 818 samples (hmp 146/152, hmpii 0/44, metahit 71/85, all others complete). The 177 duplicate cMD rows carry identical read counts. All of this equals the JSON n_nonmissing counts. |
| Fold files (all 5, all 20 repeats) | sha256 values match folds/FOLDS.sha256 and FOLDS_v2.sha256. Each repeat is a partition into 10 folds. Cases per fold: W1 17, W2 5-6, P1/P2 22-23. No raw subjectID straddles folds in any grouped file (P2 has 801 subjects for 882 samples). Regeneration: W2 and P2_ungrouped regenerate exactly from the PREREG definition; the author's code/prep.py regenerates all four grouped files byte-identical. |
| Covariate-only LR: all 32 rows (8 sets x 4 settings, 200 folds each) | Each row matches the JSON per-fold AUCs, mean and margin exactly, and every CSV row matches exactly (AUC, interval, fraction, fraction interval). Headlines: W1 age 0.7345 (0.961), W1 ALL 0.7301 (0.943), W2 BMI 0.6724 (0.658), W2 depth 0.6606 (0.613), W2 ALL 0.6828 (0.698), P1 ALL 0.7112 (0.869), P2 study 0.8404 (1.010). |
| Species RF500 baselines, W1/W2/P1/P2, 20 x 10 each (800 fits) | Bit-identical to the saved per-fold AUCs and to every saved OOF score (max abs diff 0). W1 0.744237 [0.6862, 0.8023], W2 0.768404 [0.6449, 0.8919], P1 0.742586 [0.6906, 0.7945], P2 0.855991 [0.8251, 0.8868]. |
| Pair decomposition, all 12 rows | From my own OOF scores. Species RF: P1 same-study 0.7420 / different-study 0.7326 (31859/16532 pairs); P2 0.7351 / 0.8882 (31859/115098 pairs). Covariate LR study and ALL, P1 and P2: all 8 rows match, including the 2.5-97.5 ranges. |
| Null N1 (400 controls) | My code gives real 0.8305438467987875 and best control 0.5751598302882888; all 400 controls equal results/pooled/null_n1_controls.txt (to its 6 decimals). Real beats every control; 0 controls reach it. This equals prereg/null_test.md. |
| P2 within-study permutation, all 401 rows (author's code/audit_perm.py) | All rows string-identical to results/pooled/perm_P2.tsv. Mean 0.7595 (fraction 0.770), 2.5-97.5 range 0.7342-0.7847, max 0.7970, real 0.8434 beats all. |
| Every row of audit_results.csv recomputed from saved raw outputs | 70 rows, 0 mismatches. This includes all fractions and fraction intervals, and the permutation mean, percentiles, max and real value from each TSV. The author's summarize_audit.py regenerates audit_results.csv byte-identical. |
| Leakage (bank verification method) | I called the author's own closures in code/audit_lib.py on W2 and P2, all 10 folds of repeat 0, for RF500 species and covariate LR (ALL+sex). The test-fold features and covariates were replaced by noise or absurd values and the test labels were flipped. Predictions on the training rows were bit-identical, and so were test predictions when only the test labels were corrupted. A control check confirmed that the corruption does change test-side predictions. Result: 100/100 checks passed. No cross-sample fitting happens outside the folds; prep.py applies only per-sample transforms. |
| S7 matched pairs (cited under "Not claimed") | My code gives W1 species score over 3572 age-matched pairs 0.7110 (0.6869-0.7220) and W2 over 273 BMI-matched pairs 0.7696, both equal to results/sensitivity/s7_matched_pairs.json. |
| check_auc.py | Its internal tests pass; repeat-0 P2 fold AUCs agree with the saved values within 5e-7, which is the JSON rounding. |

## Spot checks (sample, not full)

- Within-study permutations W1, W2 and P1, rerun with the author's script for a sample of seeds. W1: -1, 0-5 and
  200-205. W2: -1, 0-11 and 108-111, which includes seeds 9 and 110, two of the 16 seeds with a single-class test
  fold. P1: -1, 0-5 and 394-399. All 43 sampled rows are identical to the shipped TSVs. The summary statistics for
  all 400 rows per setting were recomputed from the TSVs. In every setting the real value beats every control (0
  controls >= real).
- An independent shuffle with my own RNG, not the author's seeds. P2: 40 permutations, mean 0.7604 +/- 0.0020 (SE),
  against the claimed 0.7595. W2: 39 scored permutations, mean 0.5052 +/- 0.0158, against the claimed 0.5024. Real
  labels beat all of mine. The real-label RF100 values reproduce exactly (P2 0.843379, W2 0.775917).
- Covariate RF (secondary rows): W2 study, W2 ALL and P2 study (0.841958) were rerun and match exactly. The other 5
  covariate-RF rows were only checked against their JSON, not rerun.
- Sensitivity analyses S1-S6 were not rerun. They are not part of the claim object.
- The published values (0.744, 0.762, 0.743, 0.837) were taken from the quotes in CLAIM.md. I did not re-fetch the
  paper; that check belongs to the other panel skeptics.

## Problems found (none blocks reproduction)

1. REPRODUCE.md step 1 (code/read_rda.py) does a full rdata conversion of sampleMetadata.rda. When I ran that
   approach it exceeded 1.1 GB of memory, so I killed it; it cannot run under a 300 MB limit. I replaced it with my
   own streaming reader of the same .rda (hash verified), filtered to the same six cMD studies read_rda.py keeps.
   With that table, prep.py reproduced the folds byte-identical and every downstream number exactly. The memory
   requirement should be stated in REPRODUCE.md. Also, prep.py's depth matcher relies on that six-study filter: a
   sample id with two (study, reads) entries becomes missing. Fed the full cMD table, prep.py would lose the 71
   metahit depths.
2. folds/FOLDS.sha256, folds/FOLDS_v2.sha256 and baseline/FOLDS.sha256 ship with CRLF line endings, so the
   documented `sha256sum` comparison with `-c` fails on a plain shell until the CRs are stripped. The hashes
   themselves are correct.
3. Fold grouping key. PREREG says "grouped by subjectID". prep.py groups by lowercased dataset_name:subjectID and
   pools hmp and hmpii under one key. A naive regeneration with the raw subjectID gives different, equally valid
   folds for W1, P1 and P2, so a verifier needs prep.py to regenerate the shipped files. The grouping property holds
   for the shipped files: no subject straddles folds.
4. W2 permutation: 16 of the 400 controls are averaged over 9 folds, because one test fold had a single class after
   shuffling. This is disclosed in results/within-cohort/perm_summary.txt but not in audit_results.csv. It does not
   change the conclusion: real 0.7759 vs max control 0.7372.
5. Interpretation, for the criterion panel; these are not reproduction failures.
   - In P2 the depth-, age- and BMI-alone LR rows include a missing-indicator channel that marks HMP/hmpii
     membership. PREREG.v4 and the author's S4/S6 complete-case runs (not rerun by me) give lower values: depth
     0.625, age 0.681. The sentence's W1, W2 and P1 covariate numbers and P2 study-only have no missing inputs.
   - The 77% within-study-permutation fraction compares the reduced pipeline (RF100, repeat-0 folds) with the
     published 0.837. Against the same reduced pipeline's real-label value (0.8434) it would be 0.756.

## Scratch reproduction (not part of the claim)

My scripts and outputs are in the run's panel-reproduce scratch folder: loaders, fold checks, covariate LR/RF,
species RF, null N1, permutation, leakage test and the comparison scripts.

pass: true
