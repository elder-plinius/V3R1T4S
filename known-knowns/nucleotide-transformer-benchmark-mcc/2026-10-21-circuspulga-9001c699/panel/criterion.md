# CRITERION skeptic — nucleotide-transformer-benchmark-mcc, partial win p3
context: subagent (fresh knowledgeWork subagent; saw only claim/ and the bank text for this target in bank/targets.json and known-unknowns/biology/nucleotide-transformer-benchmark-mcc.md)

## Target of judgment
Full success criterion: NOT claimed (no new model beats any task's best mean MCC by >= 0.02). Not judged further.
Named partial win, verbatim from the bank:
> p3: A reproducible audit of fold-to-fold variance on the histone tasks, showing which published ranking differences are inside the noise, with the per-fold numbers from benchmark.csv.

## Independent check (own checker, written from the definition, before relying on the author's code)
- claim/data/benchmark.csv: sha256 a93c1e722f6b15312818903dc048207845598925889f415caaf61e3af7d60ca6 (matches claim/CLAIM.md), 273 data rows, 18 tasks; the 10 histone tasks are H2AFZ, H3K27ac, H3K27me3, H3K36me3, H3K4me1, H3K4me2, H3K4me3, H3K9ac, H3K9me3, H4K20me1.
- Exact two-sided paired sign-flip test over the 10 per-fold MCC values (all 1024 sign patterns, statistic |mean difference|), per model pair, per histone task.
- All 1009 histone pairs in claim/objects/FOLD_AUDIT.json reproduced: 0 mismatches in p or mean difference (tolerance 1e-9).
- Best vs second (my recomputation): H2AFZ p=0.281, H3K36me3 p=0.315, H3K4me1 p=0.615, H3K4me3 p=0.494, H3K9me3 p=0.451, H4K20me1 p=0.996 (p >= 0.05, 6 tasks, exactly the 6 named in the claim); H3K27ac p=0.0078, H3K27me3 p=0.029, H3K4me2 p=0.0020, H3K9ac p=0.016 (p < 0.05).
- Rows without exactly 10 folds (HyenaDNA-32KB on H3K9me3 and H4K20me1, HyenaDNA-1KB on H3K9me3; plus enhancers, non-histone) are excluded and listed in claim/objects/FOLD_AUDIT.json; my checker finds the same exclusions.
- Table access audit: no User-Agent, cookie, retry or request code found in claim/code/.

## Clause by clause (literal)
1. "reproducible": MET for the fold-variance part. claim/code/fold_audit_v2.py + claim/data/benchmark.csv rerun deterministically; I reproduced every pair. NOT MET from claim/ for the SE_test / threshold part: it needs the Hugging Face test labels (claim/data has only their sha256 in nt_sha256.txt, not the parquet files) and REPRODUCE.md admits exact values depend on a shared-RNG call order in code/nt.py. score_test.npy lengths match n_test (checked H2AFZ 3000, H3K4me3 776) but MCC/bootstrap SE could not be recomputed here.
2. "audit of fold-to-fold variance on the histone tasks": MET. All 10 histone tasks, every pair of 10-fold entries (105/105/.../78/91 pairs), paired over folds, with per-task fold SD of the best entry.
3. "showing which published ranking differences are inside the noise": MET for fold-to-fold noise (each pair labelled with its exact p; FOLD_AUDIT lists models not significantly below the best). Hidden quantifier: it covers only entries with exactly 10 folds (3 histone rows excluded, disclosed). No multiplicity correction across 105 pairs per task, so pairs labelled "outside the noise" at p < 0.05 are per-comparison, not family-wise; the "inside the noise" (p >= 0.05) statements are not inflated by this.
4. "with the per-fold numbers from benchmark.csv": MET. The audit uses the per-fold MCC arrays of the live-fetched file, copied in claim/data/benchmark.csv.

## Stretches flagged
- The claim's second half (SE_test 0.015-0.033, threshold 0.030-0.066, "meaningful only on H3K4me2", "0.02 margin below the threshold on every histone task") is test-sampling noise estimated from the author's own small CNN, not fold-to-fold variance of the published entries; it is not required by p3, and it is not verifiable from claim/. Excluded from confirmed_scope. (Arithmetically consistent: given THRESHOLD.json, only H3K4me2's best-vs-second gap 0.0482 exceeds its threshold 0.0358 with p < 0.05.)
- The sign-flip test treats the 10 fold values as exchangeable paired samples on one shared test set; it measures training/fold variability only, which is what p3 names ("fold-to-fold variance").
- Null model: the exact sign-flip distribution is the null; p-values reproduced exactly. The CNN label-permutation null (NULLS.json) concerns the excluded part.
- Not subsumed: p3 is a separate enumerated partial win, not a weaker restatement of p1/p2 or the full criterion. Novelty (whether such an audit is already published) is NOVELTY's question, not judged here.

confirmed_scope: On the 10 histone tasks of benchmark.csv (sha256 a93c1e72...), an exact paired sign-flip test over the 10 per-fold MCC values of every pair of entries with exactly 10 folds (3 HyenaDNA rows excluded) reproduces claim/objects/FOLD_AUDIT.json exactly and shows the best entry is not significantly above the second (p >= 0.05) on H2AFZ, H3K36me3, H3K4me1, H3K4me3, H3K9me3 and H4K20me1; the SE_test-based threshold is not confirmed.

pass: true
