Path note (added 2026-10-20 at the maintainer's request): this file quotes the claim-folder paths the panel reviewed. In this package, CLAIM.md is README.md together with verify-it-yourself/expected.json; REPRODUCE.md is RUN_IT_YOURSELF.md; the result/ files are in how-we-built-it/ (split.csv, the model and the scores json) and object/ (the per-isolate predictions); status_source/ is the-record-we-beat/; target.md is not shipped. The work*/ folders named in this file are the working tree of the run and are not shipped either.

# PANEL reproduce skeptic: amoxicillin-clavulanic acid
context: subagent (same VM)

Criterion quoted from CLAIM.md: "held-out partition split by SNP cluster (PDS accession; no cluster spans train and test, split file committed with sha256), whose F1 ... is STRICTLY GREATER ... than the published genotype-field-inference F1 ... by at least 3 points absolute AND outside a 95% bootstrap interval over clusters, with accuracy no lower than the published accuracy ... and the full confusion matrix reported ... a claim on a newer export must also recompute the published rule on the same new export and beat that recomputation."

## Inputs
- work_reproduce/data/PDG000000004.6366.metadata.tsv sha256 7eb4639d4aa7c621927d0a55e6d185801f4af77401c270f7ad14f3c9ce6d101b (match)
- work_reproduce/data/PDG000000004.6366.reference_target.cluster_list.tsv sha256 58c22fd5c39d083dae3963d332c5ec25ac22c39a4f42675b37e1bb7ca954a7c8 (match)
- NOTE: the REPRODUCE.md latest_snps/ URLs now return 404 (NCBI replaced them with PDG000000004.6367, as CLAIM.md warned).
  I fetched the same two files from the NCBI versioned archive path .../Escherichia_coli_Shigella/PDG000000004.6366/{Metadata,Clusters}/; sha256 identical to the pinned values.
  The export is therefore not retrievable from the URL printed in REPRODUCE.md (reproducibility caveat, not a mismatch).

## Independent checker (written from the definition before reading code; work_reproduce/mine/check1.py, check2.py)
- 589253 metadata rows; eligible (asm_acc, AMR_genotypes, AST_phenotypes non-empty/non-NULL) = 10836 (claim: 10,836)
- amox R/S comparisons (isolate,call deduped) = 6620; TEST (sha256 rule, cluster = PDS or singleton) 1422 rows / 1045 clusters; TRAIN 5198 (claim 1422/1045/5198)
- split.csv: 10836 rows, 0 mismatches vs my cluster/split assignment, 0 extra
- result/test_predictions_amoxicillin-clavulanic_acid.csv: 1422 rows, 1422 unique, set equal to my TEST comparisons: True; cluster column correct: True
- published rule (R iff any acquired bla token, status COMPLETE/POINT, excluding blaEC/blaEC-/blaHER; per ecoli_rules.py text) recomputed from raw export genotypes equals the file rule_pred column for all rows: True
- MY model  {'F1': 0.9197080291970803, 'accuracy': 0.9767932489451476, 'TP': 189, 'FP': 7, 'TN': 1200, 'FN': 26}
- MY rule   {'F1': 0.44783715012722647, 'accuracy': 0.6947960618846695, 'TP': 176, 'FP': 395, 'TN': 812, 'FN': 39}
- scores_amoxicillin-clavulanic_acid.json F1/accuracy/TP/FP/TN/FN match mine exactly (to 1e-12) for model and rule; test_R 215 = 215
- my paired cluster-bootstrap (10000, default_rng(20261016)) diff CI [0.39721809 0.54603194] equals claimed diff_CI; model-minus-rule point diff 0.4719 (>= 3 points, outside CI which excludes 0); model accuracy 0.9768 >= published 0.736
- note: 1 test isolate carries both R and S for amox (non-identical duplicate retained by the paper rule; 2 such keys overall), an irreducible error for both predictors, applied identically.

## Rerun of author pipeline
- ecoli_prep.py: prints eligible 10836, split isolates train 8539 / test 2297; `cmp prep/split.csv result/split.csv` identical; split.csv sha256 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca (matches claim)
- ecoli_model.py: the full 8-antibiotic run took ~19 min per antibiotic here (4 cores, bootstrap dominates), over the 25 min budget; I stopped it by exact PID after ciprofloxacin (its F1 0.9613 matches nothing I was asked to check). I then ran an unmodified copy whose only change is the loop line `for ab in ["amoxicillin-clavulanic acid"]:` (work_reproduce/amoxcode/, diff shown 1 line). Per-antibiotic state is independent (rng and models are created inside the loop), so this is equivalent for this antibiotic.
- rerun_amox/results.json["amoxicillin-clavulanic acid"] == result/scores_amoxicillin-clavulanic_acid.json: identical (incl. CIs, threshold 0.602, 274 trees)
- rerun_amox/test_predictions.csv == result/test_predictions_amoxicillin-clavulanic_acid.csv: identical (same sha256 8061f657...)
- rerun model file == result/model_amoxicillin-clavulanic_acid.txt: byte-identical (deterministic)

## Leakage read of code/ecoli_model.py
Test labels (te.AST_call -> yte) are first touched at line 60 under "final scoring"; training labels ytr, OOF threshold (GroupKFold by cluster on TRAIN only), early stopping valid sets and vocabulary (min count 10 over train isolates, no labels) never use TEST labels. featurize(te.isolate) uses genotype/metadata only. No leak found.

## Not checked
Live re-read of the EuropePMC status source (outside my allowed network); the other 7 antibiotics; the paper-supplementary rule check (ecoli_rule_check.py).

pass: true
