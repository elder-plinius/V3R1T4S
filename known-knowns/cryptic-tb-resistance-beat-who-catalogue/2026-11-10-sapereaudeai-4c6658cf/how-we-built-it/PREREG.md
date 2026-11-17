# PREREG: cryptic-tb-resistance-beat-who-catalogue, run 2026-11-10-1136 (second run)

frozen_at: Tue Nov 10 11:44:57 UTC 2026 (date -u). Written before any baseline, engine-check or model score of this
run exists. No model has been trained on split v2 and no phenotype has been read by any code of this run. The split
below was generated at 11:41:29-11:41:37Z from SNP distances only, and audited at 11:41:59Z from distances and
lineage labels only.

null_test: required

## Criterion (verbatim from repo/bank/targets.json)

Success means, for at least one drug, a released model plus a saved per-isolate prediction file on a held-out test split of the CRyPTIC reuse table (split defined BEFORE training by a published rule that is lineage/phylogeny-aware - isolates grouped by genomic cluster so no cluster spans train and test - and fixed by a committed split file with sha256), using only the public VCFs/variant calls and the pinned reuse table CRyPTIC_reuse_table_20240917.csv (sha256 logged; the reuse/ directory holds five dated tables with real content changes between them, and DLM_PHENOTYPE_QUALITY exists only from the 20231208 table onward), such that on that held-out split the model's sensitivity is STRICTLY GREATER (direction: max) than the WHO catalogue's sensitivity computed on the SAME isolates and the same phenotype column, at specificity no lower than the WHO catalogue's on those isolates, with both differences outside a 95% bootstrap interval over isolates (and over clusters). Phenotype quality filtering must follow the compendium's documented rule, be stated in advance and applied identically to both predictors. The claim must be stated per drug, must report the exact catalogue version and the ECOFF used, and must present the full confusion matrices. No clinical or treatment interpretation may be attached; MIC/phenotype prediction only.

Partial wins p1, p2, p3: verbatim in target.md.

## What has been seen before this file (disclosed)

Run 2026-11-10-0944 trained and scored models on its own Mykrobe-label split (run-1 TEST, 3,705 isolates) and has
reported those results (REPORT.md of that run). Of the 3,073 TEST isolates of split v2 below, 918 were in run-1 TEST
(seen) and 2,155 were in run-1 TRAIN (never scored as held-out). Every rule in this file is either run 1's frozen
protocol unchanged or a change forced by the new input table; none is tuned on run-1 TEST results. Results are also
reported on the 2,155-isolate never-held-out subset (see "Statistic").

## Data (pinned)

- Reuse table: data/CRyPTIC_reuse_table_20240917.csv (copied from run 2026-11-10-0944, which fetched it at
  2026-11-10T09:45:20Z, HTTP 200), sha256 f785ae87f2bfb7f39f08d2ca2618a1925a290c39bfdfd5a535995b1827541c1b, 12,287 rows.
- Variant calls: CRyPTIC data table MUTATIONS_GPI.csv.gz (release_june2022/reproducibility/data_tables/cryptic-analysis-group/,
  downloaded by the human), 273,330,616 bytes, sha256 736c809f70d945a75c72cff9d703139f8ac4f11e7aba76e1f48b4be32d30b178:
  15,977,221 rows, genome-wide genes, codon REF/ALT, INDEL_LENGTH, IS_NULL / IS_FILTER_PASS flags. Null calls (alt X/x)
  are dropped; filter-fail calls (alt O/o, the "O" calls) are kept (run 1: keeping them makes the engine reproduce
  piezo's released calls). No het calls occur in the rows of the catalogue genes (attempts/evaluator-first/build_gpi_output.txt).
- Distances: GPI_SNP_DISTANCES_VALUES.npy (463,784,096 bytes, sha256 02d7cd4602a0bc900448f0fb290cf958a3b2c834f0bd878ca880af91eedef5dd,
  int16 15,228 x 15,228) with data/tables/GPI_SNP_DISTANCES_LABELS.npy (sha256 611512d71d066bb71ff1dd289950b63abf5538af94654884d9c8b8c0dce25e61).
- Lineage labels: data/tables/MYKROBE_LINEAGE.csv.gz (sha256 02a9e0fa90b6a1b1356d65ee1bd5f4ba752fd7a950646b3a2363e28bbbf9d64a).

## Split v2 (frozen)

- Code: attempts/split-v2/code/make_split_v2.py (sha256 64907253c1b07fee3b6e160c5c9922c2f91135eebfc9a81bd0126c80ad10b0b4).
- Rule: link two reuse isolates when their released SNP distance is <= 12 (the 12-SNP threshold of Walker et al. 2013,
  Lancet Infect Dis 13:137-146); clusters are the connected components (single linkage) with no hub removal, so no
  TRAIN isolate is within 12 SNPs of any TEST isolate. Components larger than 614 isolates (5%) go to TRAIN whole
  (one: 2,539 isolates, the hub-chained lineage 2/4 component found by run 1). The other components are ordered by
  sha256('V3R1T4S-cryptic-split-v2|' + smallest UNIQUEID in the component) and go whole to TEST until TEST first holds
  >= 3,072 isolates (25%). One salt, never re-rolled.
- split/split.csv sha256 3b4ed12292c1804bdd5e226c72e233eacf1be780f8432656e292e1d225640a56: 7,420 clusters (6,399
  singletons); TEST 3,073 isolates in 2,282 clusters, TRAIN 9,214 isolates in 5,138 clusters.
- Audit (attempts/split-v2/audit_split_v2_output.txt): 0 negative entries; minimum TRAIN-TEST distance 13 SNPs in
  both directions; 0 clusters span TRAIN and TEST; 0 of run 1's hub-removed 12-SNP clusters span it; 671 TEST
  isolates have a TRAIN isolate within 20 SNPs, 1,530 within 50.

## Phenotype filter (identical for both predictors; unchanged from run 1)

- Column <DRUG>_BINARY_PHENOTYPE of the pinned table; ECOFFs as in the reuse README table (BDQ 0.25, CFZ 0.25,
  DLM 0.12, LZD 1, ETH 4, EMB 4, INH 0.1, RIF 0.5 mg/L, and the README values for the other drugs).
- Primary: <DRUG>_PHENOTYPE_QUALITY == HIGH and phenotype in {R, S} ('I' excluded). Secondary (reported, never used to
  pick a winner): HIGH or MEDIUM.

## Comparator and engine check (step 3c)

- Primary comparator: WHO catalogue 2nd edition WHO-UCN-TB-2023.5, GARC1 v2.1 (oxfordmmm/tuberculosis_amr_catalogues,
  sha256 1f756526c44ca233bbf982d9e81521d6eb3509c9aa0efe1b43da1d2c21d6d440). The 3rd edition (30 Oct 2026) has no
  machine-readable translation in that repository at 11:39:07Z (data/fetch_log.txt). Secondary: WHO-UCN-GTB-PCI-2021.7.
- Look-up: attempts/evaluator-first/code/who_lookup2.py (sha256 34c2435e504372e0bb1e064a87d7090ea1336c301cc90b36ba7fc374416c93ed),
  self-test 13/13 PASS (who_lookup2_selftest.txt) before any scoring. One indel reading only: '*_fs' matches coding
  indels whose INDEL_LENGTH is not a multiple of 3; rules with explicit indel bases are matched on position and length;
  '&' rules see codon-implied nucleotide changes (fabG1@L203L&fabG1@g609a). Isolate call R if any winning rule is R.
  Circularity stated: both WHO editions were derived partly from CRyPTIC isolates.
- Engine check: the same engine run with NC_000962.3_CRyPTIC_v1.2_GARC1_RUS.csv (sha256 c91c2d42...f7aa) against the
  released CRyPTIC PREDICTIONS table (sha256 de940f0f296ec7669157f4adbfc4645b5f138c123c3861c4a551e4c4defa9425),
  catalogue v1.2. Expected: isolate-level agreement of the R / not-R call. Tolerance: >= 99.0% for every drug both
  cover (run 1's tolerance). A drug below tolerance makes its WHO comparison unresolved; nothing is retuned.

## Statistic and thresholds (main criterion and p1; unchanged from run 1 except the cluster unit)

- Per drug, on TEST isolates passing the filter: sensitivity, specificity, full 2x2 tables for model and catalogue.
- Paired bootstrap of (model - catalogue), 1,000 resamples over isolates and 1,000 over TEST clusters (split v2
  clusters), numpy seed 20261110, 2.5% and 97.5% percentiles.
- Main criterion met for drug D only if sens_model > sens_cat, spec_model >= spec_cat, 2.5% bound of the sensitivity
  difference > 0 and 2.5% bound of the specificity difference >= 0, in BOTH bootstraps, AND the point estimates
  satisfy sens_model > sens_cat and spec_model >= spec_cat on the 2,155-isolate never-held-out subset. All 13 drugs
  evaluated and reported; Bonferroni note (13 drugs). The stricter reading (specificity difference's 2.5% bound > 0)
  is also reported.
- p1 for D in {BDQ, DLM, CFZ, LZD, ETH}: sens_model - sens_cat >= 0.10 and spec_model >= spec_cat on TEST, with both
  bootstraps and confusion matrices reported.

## Model (catalogue-plus-residual; run 1's frozen protocol, inputs from MUTATIONS_GPI)

- Features per drug D: indicators of every GENE@MUTATION (indels as 'N_indel' plus 'N_ins_L'/'N_del_L') with >= 3
  carriers among all TRAIN isolates, in the genes of any WHO 2023.5 or 2021.7 row for D; per-gene aggregates (any
  coding non-synonymous, any stop/frameshift/indel, any promoter change); WHO-2023.5 R-call and U-hit indicators.
- L1 logistic regression (liblinear, class_weight balanced). C from {0.03, 0.1, 0.3, 1.0} by 5-fold GroupKFold over
  TRAIN split-v2 clusters (max mean out-of-fold average precision). Threshold: the largest score threshold whose pooled
  out-of-fold TRAIN specificity is >= the WHO-2023.5 TRAIN specificity, with maximal OOF sensitivity under that
  constraint ('call nothing R' always allowed). Refit on all TRAIN; TEST touched once.

## p2 (leakage) and the null_test.md record

- Model (fixed, no tuning): genome-wide k-nearest-neighbour on the released SNP distances. For a test isolate, take
  the k = 10 nearest training isolates among those with a HIGH-filter R/S phenotype for the drug (stable sort by
  distance, ties by matrix index); score = sum(w_j * R_j) / sum(w_j), w_j = 1 / (1 + d_j).
- Metric: sensitivity at >= 95% specificity on the test part: threshold t = the smallest score value such that the
  fraction of test negatives with score >= t is <= 0.05; sensitivity = fraction of test positives with score >= t.
  Average precision reported alongside.
- Drug: ETH (fixed now; run 1's p2 drug). Real: split v2. Controls: 400 random isolate-level splits with the same
  TEST size (3,073 of 12,287), numpy seeds 1..400. Leakage is demonstrated only if every one of the 400 random-split
  metrics is strictly greater than the split-v2 metric (null_test.md: real_beats_all_controls = yes means the
  cluster-aware value is below all 400 controls); margin = mean(controls) - real, with min and max.
- Secondary (reported, never used to pick a drug): the same for the other 12 drugs; 100 alternative cluster-aware
  splits by the same rule with salts 'V3R1T4S-cryptic-split-v2-alt-1'..'-100', to show the gap is not one grouping.

## p3 (candidate variants; run 1's PREREG.v4 design on split v2)

- Catalogue WHO-UCN-TB-2023.5 (GARC1 v2.1). 'Absent' = no exact row for that drug (any grade, indel bases normalised
  to length) and never the R-causing mutation of a WHO-2023.5 call in this run's look-up.
- Candidates: per drug, non-synonymous variants (incl. promoter, rRNA, indels) in the genes of any WHO row for the drug,
  >= 5 carriers among HIGH-filter R/S TRAIN isolates. Background: HIGH-filter R/S isolates with no WHO-2023.5 R call.
- TRAIN: one-sided Fisher exact p < 0.05 / (number of candidates over all 13 drugs).
- TEST: R-carrier count against 4,000 phenotype permutations within TEST Mykrobe lineage labels
  (MYKROBE_LINEAGE_NAME_2); one-sided p = (1 + exceedances) / 4001 < 0.05 / (number passing TRAIN), >= 1 R carrier,
  odds ratio > 1. p3 met only if >= 10 variants replicate. Association on public isolates only.
