# PREREG (frozen 2026-10-16T17:48:10Z, before any model is fitted or scored)

criterion: verbatim in target.md. One antibiotic per claim. Antibiotics attempted (all eight): ciprofloxacin, ampicillin,
gentamicin, tetracycline, trimethoprim-sulfamethoxazole, ceftriaxone, amoxicillin-clavulanic acid, meropenem.

data: NCBI Pathogen Detection PDG000000004.6366.metadata.tsv (sha256 7eb4639d4aa7c621927d0a55e6d185801f4af77401c270f7ad14f3c9ce6d101b,
Last-Modified 2026-10-16 03:34:08 GMT) + PDG000000004.6366.reference_target.cluster_list.tsv
(sha256 58c22fd5c39d083dae3963d332c5ec25ac22c39a4f42675b37e1bb7ca954a7c8).
eligibility and phenotype mapping: code/ecoli_prep.py (reproduces the paper's S1 eligibility flags and its S9 comparison table exactly on the paper's own records).
published rule: code/ecoli_rules.py (reproduces all 56,141 S9 predictions and the eight S10 confusion matrices exactly); recomputed on the new export.
split: whole SNP clusters (PDS_acc; isolates without a PDS are singletons); TEST iff int(sha256('V3R1T4S-ecoli-2026-10-16|'+cluster),16) % 100 < 20.
split.csv sha256 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca (computed before any model was fitted).

model (one family, fixed now): per antibiotic, LightGBM binary classifier; features built with vocabularies from TRAIN isolates only:
indicators for AMR genotype tokens (COMPLETE/POINT hits and other-status hits separately; tokens in >= 10 train isolates),
counts (all tokens, acquired bla, QRDR point mutations gyrA/parC/parE), the eight published-rule outputs, collection year,
scientific_name, epi_type. Hyperparameters: learning_rate 0.03, num_leaves 15, min_child_samples 20, feature_fraction 0.8,
bagging 0.8, L2 1.0. Number of trees = mean early-stopping iteration (logloss, patience 100) over a 5-fold GroupKFold by
cluster inside TRAIN; decision threshold = the value maximising F1 on those out-of-fold TRAIN predictions. Test labels are
used only for the final scoring.

statistic: on the TEST partition, F1 and accuracy of the model and of the published rule recomputed on the same rows, full
confusion matrices, and 10,000 bootstrap replicates resampling TEST clusters with replacement (numpy default_rng(20261016)):
95% percentile intervals for model F1, rule F1 and the paired difference (model - rule).

thresholds for a claim on antibiotic a (all required):
- F1_model >= F1_published(a) + 0.03, F1_published re-read live from the status source right before claiming;
- F1_model >= F1_rule_recomputed_on_test(a) + 0.03;
- the 2.5th percentile of the model's cluster-bootstrap F1 > max(F1_published(a), F1_rule_recomputed_on_test(a))
  ("outside a 95% bootstrap interval over clusters"), and the paired-difference interval lies entirely above 0;
- accuracy_model >= accuracy_published(a) (Table 3).
secondary (reported, not claimable): the same pipeline on the paper's own records (NCBI_S2, 2026-06-11 snapshot) and a
random isolate-level split (bank partial win p3, leakage demonstration).
null_test: not needed because the comparator is a fixed deterministic rule recomputed on the identical test rows and the uncertainty is handled by the prespecified paired cluster bootstrap; no search or "beats chance" claim is made.
