# CRyPTIC TB resistance (partial win p2): random splits inflate a genome-wide model's held-out sensitivity

## What

On the pinned 12,287-row CRyPTIC reuse table, for ethionamide (HIGH-quality R/S phenotypes) and one fixed genome-wide 10-nearest-neighbour model on the released CRyPTIC SNP distances, sensitivity at >= 95% specificity is 0.3496 on the frozen 12-SNP single-linkage cluster-aware split v2 versus 0.5135-0.6678 (mean 0.6003) on all 400 pre-registered random isolate-level splits of the same TEST size, a random-split inflation of 0.2507 on average (at least 0.1639), of which 0.15 to 0.21 remains in the panel's post hoc composition controls; this is shown for this distance-based model and this drug only.

Released here: the cluster-aware split (object/split_v2.csv.gz; uncompressed sha256
3b4ed12292c1804bdd5e226c72e233eacf1be780f8432656e292e1d225640a56), the 400 random control splits
(object/random_control_splits_membership.bin: one 1,536-byte little-endian bit row per seed 1..400, bit i = row i of
the split file is in TEST), the per-split metrics (object/p2_knn_ETH_metrics.csv, also 100 alternative cluster-aware
splits made by the same rule with other salts: 0.1799 to 0.4662) and the per-isolate split-v2 TEST scores
(object/predictions_ETH_knn10_split_v2_test.csv). Code: how-we-built-it/code/.

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Python 3 standard library only (set PYTHON to choose an interpreter). Expected last line `PASS`, a few seconds. It
checks the object hashes, that no cluster spans TRAIN and TEST, recomputes the split-v2 value from the per-isolate
scores with the stated threshold rule, and checks the 400 control values and split sizes. With numpy and the public
distance matrix (RUN_IT_YOURSELF.md) it also recomputes the 10-NN on split v2 and three random splits.

## Compared to

| comparison | value | source |
|---|---|---|
| same model, same drug, 400 random isolate-level splits (the trap) | 0.5135 to 0.6678, mean 0.6003 | this package, object/p2_knn_ETH_metrics.csv |
| same model, same drug, cluster-aware split v2 | 0.3496 | this package |
| status source (no newer reuse table; pinned table still newest) | CRyPTIC_reuse_table_20240917.csv | https://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/reuse/ fetched 2026-11-10T11:38:39Z (the-record-we-beat/) |
| closest prior found by the NOVELTY skeptic: a public repository on the same pinned table, one random vs one k-means-cluster-disjoint split per drug, AUROC only, figure only (no split files, no per-split metrics, no null) | ETH AUROC 0.94 random vs 0.91 cluster-disjoint | https://github.com/waqastakkar/tgp-Trustworthy_Genotype-to-Phenotype_AMR_Predictio (reports/figures/ood_gap.svg; read through the GitHub API on 2026-11-10, panel/novelty.md) |

Precedents on other data (neighbouring cells, named by the NOVELTY skeptic): Hu et al. 2024, Brief Bioinform 25:bbae206
(random vs other fold designs on PATRIC M. tuberculosis data); "Biased sampling confounds machine learning prediction of
antimicrobial resistance", PLOS Biol 23(12):e3003539, 2025 (five other species). This package is a reproducible
methodology demonstration on the CRyPTIC table, not a discovery that population-structure leakage exists.

## Not claimed

- Not the bank's main success criterion (beating the WHO catalogue): no model here beats WHO-UCN-TB-2023.5 on the
  run's frozen rule without depending on how filter-fail calls are read.
- Not other models or drugs: the inflation is shown for this 10-NN model and ethionamide only (secondary drugs with
  fewer controls are in how-we-built-it/logs/p2_secondary_summary.txt and are not claimed).
- Not predictive value: this model is a weak predictor (on the same TEST isolates the WHO catalogue's sensitivity is
  0.797); nothing here is clinical advice or a per-patient interpretation.
- Clusters come from CRyPTIC's released distance matrix, not recomputed from the VCFs.

## Credits

- The CRyPTIC Consortium: the reuse table, the GPI SNP-distance matrix and labels, the Mykrobe lineage table
  (https://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/).
- Walker TM et al. 2013, Lancet Infect Dis 13(2):137-146 (https://pubmed.ncbi.nlm.nih.gov/23158499/): the 12-SNP
  transmission threshold used for the clusters.
- WHO catalogue WHO-UCN-TB-2023.5 in the GARC1 translation of https://github.com/oxfordmmm/tuberculosis_amr_catalogues
  (used only in the run's baseline record, how-we-built-it/baseline/).
- The authors of https://github.com/waqastakkar/tgp-Trustworthy_Genotype-to-Phenotype_AMR_Predictio (closest prior:
  random vs cluster-disjoint splits on the same table), Hu et al. 2024 (Brief Bioinform 25:bbae206,
  https://www.biorxiv.org/content/10.1101/2024.01.31.578169v2.full) and the PLOS Biol 2025 study
  (https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3003539), as read by the NOVELTY skeptic.
- numpy, pandas, scikit-learn.
