Path note (added 2026-10-20 at the maintainer's request): this file quotes the claim-folder paths the panel reviewed. In this package, CLAIM.md is README.md together with verify-it-yourself/expected.json; REPRODUCE.md is RUN_IT_YOURSELF.md; the result/ files are in how-we-built-it/ (split.csv, the model and the scores json) and object/ (the per-isolate predictions); status_source/ is the-record-we-beat/; target.md is not shipped. The work*/ folders named in this file are the working tree of the run and are not shipped either.

# PANEL criterion skeptic: amoxicillin-clavulanic acid

context: subagent (same VM)
Read only inside this folder. Recompute script: work_criterion/recompute.py (no downloads).

| Clause | Evidence | Verdict |
|---|---|---|
| Released predictor + per-isolate prediction file | result/model_amoxicillin-clavulanic_acid.txt, result/test_predictions_amoxicillin-clavulanic_acid.csv (1422 rows, 1421 isolates, 1045 clusters) | met |
| Frozen hash-pinned export, date + sha256 | CLAIM.md: PDG000000004.6366 metadata and cluster list, Last-Modified 2026-10-16, sha256 given. Raw TSVs are not in the folder, so the sha256 and the 10,836 eligible count could not be checked here | stated, not independently verifiable |
| Eligibility/mapping rules as code, applied identically to both | code/ecoli_prep.py, code/ecoli_rules.py; model_pred and rule_pred are in the same file on the same rows. Claimed paper-table reproduction (56,141 rows, 0 mismatches) rests on supplementary files that are not in the folder | met on the code; reproduction of the paper's own numbers unverified |
| Cluster-held-out split, committed split file + sha256 | result/split.csv sha256 recomputed = 68a7e358...577dca (matches). No test cluster appears among train clusters. All test isolates have split=test. Rule re-derived from the sha256-mod-100 rule: 0 violations | met |
| F1 strictly greater than published, margin at least 3 points | Recomputed model F1 91.971% vs published 44.5% (Table 3 in status_source; sha256 of saved copy matches). Margin 47.5 points | met |
| Outside a 95% bootstrap interval over clusters | Model CI 86.9-95.4 (my 2000-resample check 87.0-95.4); published 44.5 and recomputed-rule upper bound 53.2 are both outside it. Paired difference CI 39.8-54.4, excludes 0 | met |
| Accuracy no lower than published | 97.68% recomputed vs 73.6% | met |
| Full confusion matrix | Recomputed TP 189 FP 7 TN 1200 FN 26 (model); 176/395/812/39 (rule); both match the claim | met |
| Newer export: also beat the rule recomputed on the same export | Rule on the same 1422 rows: F1 44.78%, acc 69.48% (recomputed from the csv). Model beats it by 47.2 points | met |
| No clinical interpretation | CLAIM.md says "database-concordance benchmark for surveillance. No clinical or treatment interpretation" | met |

## Null models and stretch hunting
- Recomputed published rule is the null: F1 44.78%, accuracy 69.48%. All-S gets accuracy 84.9% and all-R gets F1 26.3%, so the accuracy clause would be a weak bar alone. The F1 clause is the binding one and is passed by a wide margin.
- Duplicate or conflicting rows: 1 isolate has both R and S labels (2 rows). Dropping it leaves model F1 92.2% and rule F1 44.7%. No effect.
- The paper also publishes a post hoc alternative rule (TEM-1-only not sufficient; Section 2.4, Supp. Table S5) that raises F1. Its F1 is not in the saved XML text and was not compared. The criterion names the Table 3 value (44.5%), so this is not a failure, but it is a stronger published null left untested.
- Amoxicillin-clavulanic acid has the lowest published F1 of the eight, so it is the easiest baseline. The criterion says "at least one" antibiotic, so this is permitted. It is a selection among eight, and no multiplicity correction applies.
- Test labels were read again after the primary scoring (contrarian checks). The claim says no model, feature or threshold change followed. PREREG.md is cited but is not in the folder, so the pre-registration cannot be checked here.
- "Re-read live immediately before claiming": the status source was saved at 17:08Z and re-read at 19:28Z with an identical sha256. This is the claimant's statement, and only the saved copy is available.
- Not independently reproduced: training the model, the export hash, and the rule check against the paper's tables.

confirmed_scope: On the cluster-held-out TEST partition in result/split.csv (sha256 68a7e358...577dca) of NCBI export PDG000000004.6366 as the claimant describes it, the LightGBM model's predictions in result/test_predictions_amoxicillin-clavulanic_acid.csv score F1 91.97% and accuracy 97.68% (TP 189, FP 7, TN 1200, FN 26), against 44.78% and 69.48% for the code-reimplemented Table 3 genotype rule on the same 1422 rows and 44.5% and 73.6% published, with the model's cluster-bootstrap F1 interval lying above both baselines, for amoxicillin-clavulanic acid only and for database concordance only.

pass: true
