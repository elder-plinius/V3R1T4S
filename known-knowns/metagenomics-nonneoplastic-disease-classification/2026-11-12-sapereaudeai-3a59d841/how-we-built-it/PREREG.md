# PREREG: run 2026-11-12-1824, target metagenomics-nonneoplastic-disease-classification

frozen_utc: 2026-11-12T18:34:42Z (written before any model is fitted and before any covariate-only, permutation or
species-model result exists; only metadata counts per dataset have been looked at)

## Criterion (verbatim from repo/bank/targets.json, partial win p3)

"A reproducible confound audit for one disease: quantify how much of the published AUC is recoverable from
sequencing-depth, study-of-origin, age/BMI/country covariates alone (and from label permutation within study), with
code and numbers, documenting the fraction of apparent signal that is cohort structure."

p1 and p2 are not attempted as claims in this run (p1: the only second T2D cohort, WT2D, is used in this audit and so
cannot be "untouched"; p2: no time budget). The main success criterion is not attempted.

## Readings chosen before any result (most favourable FAIR reading, per the human's standing rule)

R1. "the published AUC": the published cross-validated MetAML AUCs (Pasolli et al. 2016, PLoS Comput Biol,
    PMC4939962, read from the status source fetched 2026-11-12T18:27:02Z) for the chosen disease with the paper's own
    baseline learner (random forest on MetaPhlAn2 species abundance). For T2D these are, quoted from the text:
    W1 T2D (Qin 2012) within-cohort 0.744 (95% CI 0.688-0.800); W2 WT2D (Karlsson 2013) within-cohort 0.762
    (0.651-0.873); P1 T2D+WT2D merged, cross-validated 0.743; P2 T2D+WT2D plus the healthy controls of the
    cirrhosis, colorectal, HMP and IBD datasets, cross-validated 0.837. All four are audited.
R2. "recoverable from ... covariates alone": the cross-validated AUC of a model that sees only the covariate(s),
    under the same folds as the species model. Reported for each covariate alone and for all named covariates
    together. The bank sets no minimum effect size; none is invented here.
R3. "label permutation within study": disease labels shuffled within each study (study = source publication,
    pubmedid), then the identical species pipeline is run; the resulting AUC is what cohort structure plus chance can
    give. Within a single-study setting (W1, W2) this is an ordinary label permutation.
R4. "fraction of apparent signal that is cohort structure": f = (AUC_x - 0.5) / (AUC_published - 0.5), reported for
    x = study-of-origin-only, all-covariates, and the mean within-study-permutation AUC; also reported against our
    reproduced AUC. Values may fall outside [0, 1]; they are reported as computed, never clipped.
R5. The p3 pass condition is the quantification itself: code, numbers and intervals for every item of R1-R4 for one
    disease. No threshold on the size of the confound.

## Disease choice rule (fixed before any covariate-only result)

The non-cancer disease with the most distinct source studies (pubmedid) among the MetAML benchmark's disease
datasets; ties broken by metadata completeness. From the paper and the metadata counts: T2D is the only disease
with two studies (Qin et al. 2012, pubmed 23023125; Karlsson et al. 2013, pubmed 23719380). Chosen: **T2D**.

## Data (hashes recorded in scout.md)

- MetAML data/abundance.txt.bz2, sha256 64b505c9...dcc16 (SegataLab/metaml master, head commit 52fbd54a).
- Species features: rows whose name contains "|s__" and not "|t__" (MetaPhlAn2 species level), values as given.
- Cohorts: W1 = dataset_name in {t2dmeta_long, t2dmeta_short} with disease in {t2d, n}; W2 = dataset WT2D with
  disease in {t2d, n} (IGT excluded, as in MetAML); external healthy controls for P2 = disease "n" and bodysite
  "stool" from Quin_gut_liver_cirrhosis, Zeller_fecal_colorectal_cancer, hmp, hmpii, metahit. Label 1 = t2d.
- Covariates: age, BMI, country, gender from the MetAML table; sequencing depth = log10(number_reads) from
  curatedMetagenomicData sampleMetadata.rda (devel, sha256 168c8650...3444), matched by sample id (MetAML sampleID
  == cMD sample_id). Depth is the per-sample read count of the same sequencing run as reprocessed by cMD.
- Study = pubmedid (hmp and hmpii share one study, HMP 2012).

## Protocol

- Folds: StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=r), r = 0..19, stratified on the label,
  grouped by subjectID (so repeated samples of one person never straddle folds). Fold files are written and hashed
  (folds/*.csv, sha256 in folds/FOLDS.sha256) before any model is fitted.
- Species model M_sp (the paper's baseline): RandomForestClassifier(n_estimators=500, max_features="sqrt",
  criterion="gini", random_state=1000*r+k), fitted on the training folds only.
- Covariate model M_cov (primary): numeric covariates -> median imputation with missing-indicator -> standardise;
  categorical (country, study) -> one-hot (unknown ignored); LogisticRegression(C=1.0, max_iter=5000). All fitting
  inside training folds. Secondary: the same encoded matrix into the RF of M_sp.
- Covariate sets: depth; age; BMI; age+BMI; country; study (P1, P2 only); ALL = depth+age+BMI+country(+study in
  P1/P2). Extra (secondary, not a named covariate): ALL+sex.
- AUC statistic: mean of the 200 per-fold test AUCs (10 folds x 20 repeats). Interval (primary): MetAML-style margin
  t(0.975, df=9) x mean over repeats of the per-repeat fold standard error; also the 2.5-97.5 percentile range of the
  20 repeat means. Fractions R4 carry the AUC interval through the same formula.
- Within-study permutation (R3): reduced species pipeline (RF n_estimators=100, otherwise as M_sp) on the repeat-0
  folds, mean fold AUC; 400 permutations (seeds 0..399) per setting, labels shuffled within study; the real-label
  reduced-pipeline AUC is computed the same way. Reported: mean, 2.5-97.5 percentile range, max.
- P2 pair decomposition: from the M_sp out-of-fold scores of each repeat, the AUC over (case, control) pairs from the
  same study versus pairs with an external-study control; mean over repeats.

## Baseline (kit/RUN.md step 3c)

- Baseline: MetAML RF on species abundance, settings W1, W2, P1, P2 (paper text values above; paper Figs 2, 6, 7).
- Code revision: MetAML's own code is not run (Python 2-era scripts); the RF is reimplemented in scikit-learn
  (installed version recorded in output) with the paper's stated settings. Data: abundance.txt.bz2 above. Split:
  the committed folds above. Metric: per-fold AUC averaged over 10 folds x 20 repeats.
- Expected scores and tolerance: W1 0.744 (tolerance: inside the published 95% CI 0.688-0.800); W2 0.762 (inside
  0.651-0.873); P1 0.743 and P2 0.837 (no CI in the text; tolerance +/- 0.03). A miss makes that setting's
  comparison "unresolved" (reported, never retuned); fractions are then reported against both numbers.

## Null design

null_test: required

N1 (primary, written to null_test.md): setting P2, statistic = study-of-origin-only M_cov AUC (mean fold AUC on the
repeat-0 folds). Controls: 400 runs of the identical pipeline with the study column randomly permuted across
samples (seeds 0..399), which removes any study-label association. Real must beat every control.
N2 (reported in the audit, not a gate): real-label reduced species AUC versus the 400 within-study permutations, per
setting; says whether microbiome signal remains beyond cohort structure.

## Escape hatches (declared now)

E1. Depth: models run on the samples with a matched read count; n is reported. If a cohort has no match at all, its
    depth is reported as unavailable (MetAML Table 1 gives only per-dataset means, which equal a study indicator).
E2. Baseline miss: see above; the audit still reports fractions against both the published and reproduced AUC.
E3. Time: if fewer than 400 within-study permutations finish for a setting, the number completed is reported (N2 is
    not a gate). N1 must have 400.
E4. Sample counts: if our cohort definitions do not give the paper's counts, ours are used and both are reported.
E5. If the panel or time fails, the status is PROMISING at most.

## What would change nothing

No reading above is changed after results. Any change goes into a new, timestamped PREREG.v2.md, said in the report.
