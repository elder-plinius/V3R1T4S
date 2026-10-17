# REPRODUCE report: ecoli-cro-reproduce (ceftriaxone, ncbi-pathogen-ast-ecoli-genotype-phenotype-f1)
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)

## Inputs (no download; pinned files already in claim/data/)
- sha256sum (run 2026-10-17 11:48Z): data/PDG000000004.6366.metadata.tsv = 7eb4639d4aa7c621927d0a55e6d185801f4af77401c270f7ad14f3c9ce6d101b (matches CLAIM.md); data/PDG000000004.6366.reference_target.cluster_list.tsv = 58c22fd5c39d083dae3963d332c5ec25ac22c39a4f42675b37e1bb7ca954a7c8 (matches); status_source/PMC13513162_fullTextXML.xml = e0d80a91... (matches); result/split.csv = 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca (matches).
- Saved paper XML, Table 3 text read: ceftriaxone accuracy 97.9%, F1 94.6% (abstract also says so). I did not re-fetch the live URL (rules said no downloads), so the "re-read live" step is not independently re-done by me; I rely on the saved copy hash.

## Step 1: own checker, written before running the author's pipeline (work/mycheck.py)
Definition used (quoted from CLAIM.md/prep docstring): eligible = assembly, AMR genotypes and AST phenotypes all non-empty/non-NULL; R/S only; TEST iff int(sha256('V3R1T4S-ecoli-2026-10-16|'+cluster),16)%100<20, cluster = PDS_acc from cluster_list, else singleton. I parsed the 551 MB export myself with csv (not the author's code) and found:
- 589,253 rows, 10,836 eligible, 7,098 ceftriaxone R/S isolates, 0 conflicting calls.
- result/split.csv: 10,836 rows, 0 mismatches against my cluster and test/train assignment.
- test set: 1,531 expected test ceftriaxone isolates = 1,531 prediction rows, 0 missing, 0 extra, 0 label mismatches against the metadata, 0 cluster mismatches, 1,114 clusters.
- From the saved predictions and my parsed labels: model TP 396 FP 10 TN 1116 FN 9, F1 97.657%, accuracy 98.759%; rule TP 370 FP 8 TN 1118 FN 35, F1 94.508%, accuracy 97.191%. All match CLAIM.md.
- model_pred equals (model_prob >= 0.3253) on all rows (0 mismatches). rule_pred matches a regex application to the genotype field (note: I reused the author's ESC pattern, so this only checks application, not that the rule equals the paper's; the paper-table check in ecoli_rule_check.py needs the supplementary zip, which I did not download).

## Step 2: full rerun from a scratch copy (work/scratch; claim/ untouched)
Python 3.12 venv_shared; pandas 3.0.6, numpy 2.5.4, scikit-learn 1.9.1, lightgbm 4.7.0 per REPRODUCE.md (version line printed by the venv).
- ecoli_prep.py: same counts (589253 rows, 10836 eligible, 8737 clusters, AMRFinderPlus 4.2.7 for all). prep/split.csv differs from result/split.csv by bytes only because of Windows CRLF line endings; after removing CR it is byte-identical (sha256 68a7e358...).
- ecoli_model.py (all eight antibiotics, finished 12:00Z): ceftriaxone results.json entry is exactly equal to result/scores_ceftriaxone.json (F1 0.9765721331689272, acc 0.9875898105813194, CIs, diff_CI 1.21% to 5.44%, threshold 0.3253, 211 trees); rerun test_predictions rows for ceftriaxone are identical to result/test_predictions_ceftriaxone.csv (1531 rows, list equality True); saved model file identical modulo CR. Deterministic.

## Reasoning on the criterion
- F1 97.66 vs recomputed rule 94.51: +3.15 points, vs published 94.6: +3.06; both at least 3. Paired cluster-bootstrap diff CI 1.21% to 5.44% excludes 0; model F1 exceeds the rule's own upper CI limit 96.58%. Accuracy 98.76% >= published 97.9%. Full confusion matrix reported. Recomputed on the same new export, as required. Split by whole PDS clusters, verified no cluster crosses (split derived per cluster).
- Margin is thin (3.15 vs 3.0 threshold), and the lower diff-CI bound is 1.21, but the criterion is on point F1 plus outside the interval, which holds. Threshold selected on train OOF only; label history disclosed in CLAIM.md. The side checks (other antibiotics: tetracycline and TMP-SMX show no gain) are not part of this claim.
- No mismatch, missing object or non-determinism found.

pass: true
