# REPRODUCE report: E. coli/Shigella ampicillin genotype-to-phenotype claim (PDG000000004.6366)

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)

## What I ran (UTC times from date -u, 2026-10-17)
1. sha256sum (11:48:59Z) of data/PDG000000004.6366.metadata.tsv = 7eb4639d4aa7c621927d0a55e6d185801f4af77401c270f7ad14f3c9ce6d101b and data/PDG000000004.6366.reference_target.cluster_list.tsv = 58c22fd5c39d083dae3963d332c5ec25ac22c39a4f42675b37e1bb7ca954a7c8: both match CLAIM.md. result/split.csv = 68a7e358...0577dca (match); status_source XML = e0d80a91...5685 (match).
2. Own checker written before reading code/ (from the CLAIM.md definition: "assembly, AMR genotypes and AST phenotypes all present; R/S only"; split "TEST iff int(sha256('V3R1T4S-ecoli-2026-10-16|' + cluster), 16) % 100 < 20"; isolates without a PDS are singletons). It parses the metadata and cluster list directly. Findings:
   - my first pass treated asm_acc "NULL" as present and got 8214 ampicillin R/S rows; after treating NULL as missing I get 8012 distinct isolates with ampicillin R or S, 1715 of them in TEST, and the TEST isolate set is identical to result/test_predictions_ampicillin.csv (symmetric difference 0).
   - the claim's 8013 (6298 train + 1715 test) = my 8012 + one isolate (PDT000077415.3) whose AST field holds both ampicillin=R and ampicillin=S; the author's code keeps both rows (documented as "non-identical duplicates retained"). That row is in train, so the test set is unaffected.
   - labels (AST_call) and clusters in the prediction file: 0 mismatches against my parse of the export. 1257 distinct test clusters (claim: 1257). split.csv: 10836 rows, 0 mismatches against my own hash rule, 0 clusters spanning train and test.
   - recomputed from the prediction file: model TP 867 FP 8 TN 827 FN 13, F1 0.98803 (98.80%), accuracy 0.98776 (98.78%); rule TP 792 FP 6 TN 829 FN 88, F1 0.94398 (94.40%), accuracy 0.94519 (94.52%). Matches CLAIM.md.
   - my own reimplementation of the rule (any acquired bla gene, intrinsic blaEC/blaHER excluded, status COMPLETE/POINT only) reproduces rule_pred for all 1715 test rows (0 mismatches).
3. Pipeline rerun from a scratch copy (venv_shared, Python 3.12.13, pandas 3.0.6, numpy 2.5.4, scikit-learn 1.9.1, lightgbm 4.7.0 = pinned). ecoli_prep.py: 589253 rows, 10836 eligible (matches claim), split.csv differs from result/split.csv only by CRLF line endings written on Windows; after stripping CR the sha256 is 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca (identical). ecoli_model.py was run for ampicillin only (loop restricted in the scratch copy; other seven antibiotics not rerun, not part of this claim).
   - rerun results.json["ampicillin"] equals result/scores_ampicillin.json exactly (Python dict equality: True, including CIs 98.25-99.28, diff CI 3.06-5.88, 236 trees, threshold 0.5601).
   - rerun test_predictions.csv vs result/test_predictions_ampicillin.csv: 1715 rows each, same isolates, 0 rows differing in AST_call, rule_pred, model_prob, model_pred or cluster. Saved model text identical modulo CRLF. Deterministic.
4. Live status source: curl https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML at 11:51:48Z, HTTP 200, sha256 e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685 (identical to the saved copy). Table 3 ampicillin: N 7592, accuracy 94.5%, F1 93.9%.

## Reasoning on the criterion
- Predictor, per-isolate prediction file, hash-pinned export, split file with sha256, cluster-held-out partition: all present and verified.
- F1 98.80% vs published 93.9% (+4.9 points) and vs recomputed rule 94.40% (+4.40 points); required margin is 3 points. The paired cluster-bootstrap difference CI lower bound is 3.06%, just above 3 but above. The model CI (98.25-99.28) lies fully above the rule CI (92.78-95.87).
- Accuracy 98.78% >= published 94.5%. Full confusion matrix reported and recomputed by me.
- Model features: genotype tokens and collection metadata only; AST_phenotypes is not a feature (read in ecoli_model.py after my own checks). Threshold chosen on out-of-fold train predictions; the claim discloses repeated reads of test rows for other analyses with no change to the model.
- Not independently verified: the rule's equality with the paper's Supplementary Table S3/S9 (those files were not in the claim package and I did not download them); I only confirmed that the rule is a simple, sensible bla-gene rule whose recompute on this export (94.4%) is close to the paper's 93.9%. The 3.06-point lower bound is a thin margin over the 3-point requirement.

pass: true
