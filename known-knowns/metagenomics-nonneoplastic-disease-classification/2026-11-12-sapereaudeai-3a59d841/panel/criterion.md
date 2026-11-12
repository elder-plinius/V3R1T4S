# CRITERION skeptic: run 2026-11-12-1824, target metagenomics-nonneoplastic-disease-classification, partial win p3

context: subagent (Claude Code Agent tool, subagent_type criterion, fresh context)
date: 2026-11-12T20:02Z
inputs read: claim/ only (CLAIM.md, bank_entry.json, prereg/, baseline/, audit_results.csv, audit_summary.md,
results/, code/, folds/, inputs/, REPRODUCE.md, status_record.md). One plain fetch of the status source
(Europe PMC PMC4939962 fullTextXML, HTTP 200, 181821 bytes, sha256 1edb0d04...661c, the same hash as
claim/status_record.md). Small independent checks used panel scratch scripts (not shipped). I used the venv Python
(`-I`, 2 threads).

## The criterion, read literally

p3: "A reproducible confound audit for one disease: quantify how much of the published AUC is recoverable from
sequencing-depth, study-of-origin, age/BMI/country covariates alone (and from label permutation within study), with
code and numbers, documenting the fraction of apparent signal that is cohort structure."

| element named in p3 | covered? | where (relative to claim/) |
|---|---|---|
| one disease | yes: T2D, picked by a rule written before any results (the only MetAML non-cancer disease with two source studies) | prereg/PREREG.md |
| "the published AUC" | yes: four published RF species-abundance AUCs (0.744, 0.762, 0.743, 0.837). I re-read them in the live source: the quotes and the species/marker order are correct | CLAIM.md, baseline/README.md |
| sequencing depth alone | yes, in all four settings (cMD number_reads matched by sample id; complete in W1, W2 and P1; 818/882 in P2, with a complete-case S4) | results/*/W1..P2_audit.json, results/sensitivity/s4_* |
| study of origin alone | yes, in the two multi-study settings: P1 0.5175, P2 0.8404. In W1 and W2 the value is 0.5 by construction (one study each) | same |
| age / BMI / country alone | yes, each one alone, age+BMI, and all named covariates together (LR primary, RF secondary) | same |
| label permutation within study | yes: 400 seeds per setting, labels shuffled within pubmedid, with a reduced species RF (100 trees, repeat-0 folds), as pre-registered | results/*/perm_*.tsv |
| code and numbers | yes: code/, audit_results.csv (70 rows), raw JSON/TSV/OOF files, REPRODUCE.md | |
| fraction of apparent signal that is cohort structure | yes: R4, f = (AUC_x - 0.5)/(AUC_published - 0.5), with intervals carried through | audit_results.csv |
| reproducible | yes: committed folds regenerate exactly; my re-runs match (below) | folds/, my checks |

No element is missing. "Covariates alone" is covered under both readings: each covariate on its own, and all the
named covariates together without the microbiome.

## Readings: frozen before results, and followed

- prereg/PREREG.md (frozen_utc 18:34:42Z) fixes R1-R5, the disease rule, the folds, the models, the baseline
  tolerances and the null. The code does what it says: StratifiedGroupKFold(10, shuffle, rs=r) grouped by
  dataset:subject (HMP and HMPII merged); RF500 with sqrt and gini, seed 1000r+k; LR C=1 with median imputation plus
  a missingness indicator, standardisation and one-hot encoding, all inside a fold-fitted Pipeline; RF100 permutations
  on the repeat-0 folds; N1 permutes the study column.
- The sensitivity analyses in v2, v4 and v5 are labelled as such and replace no primary number. v4 (S6) says openly
  that it was written after the P2 covariate numbers had been seen.
- The freeze times are self-attested. File times in the package are copy times (19:53Z), so the package itself
  cannot prove the order. Its content is consistent with the order it claims.
- Minor deviations:
  - R4 says fractions are "also reported against our reproduced AUC". This is done for the covariate rows (JSON
    `frac_vs_reproduced`) but not for the permutation mean. Computed from the shipped numbers, P2 gives
    (0.7595-0.5)/(0.8560-0.5) = 0.729.
  - prereg/PREREG.v3.md is cited by v4 but is not in the package. By v4's description it concerns p2. The p3 code
    follows PREREG.md as written, so the gap does not touch p3.

## Baseline record (same data, split and metric as the claim)

Same data (the 1,291 species rows of inputs/abundance.txt.bz2, sha256 64b505c9...dcc16, which I re-hashed). Same
committed folds as every covariate and permutation number. Same metric: mean per-fold AUC over 10 x 20. Tolerances
against the pre-registered ones:

| setting | published | tolerance | reproduced (my recomputation from saved OOF) | verdict |
|---|---|---|---|---|
| W1 | 0.744 | inside 0.688-0.800 | 0.7442 | met |
| W2 | 0.762 | inside 0.651-0.873 | 0.7684 | met |
| P1 | 0.743 | +/- 0.03 | 0.7426 | met |
| P2 | 0.837 | +/- 0.03 | 0.8560 (+0.019) | met |

The W1 and W2 tolerances (the published 95% CIs) are wide, but they were fixed in advance, and the actual misses are
at most 0.007. Per-fold AUCs recomputed from the saved OOF scores match the JSON to within 5e-7. Margins and CIs
recompute exactly.

## Independent checks I ran (all match the shipped numbers)

- Folds: all 20 repeats of W1, W2, P1, P2 and P2_ungrouped regenerate identically from the pre-registered rule.
  No subject straddles folds in the grouped files. The only multi-sample subjects are 58 HMP/HMPII subjects. The
  Qin 2012 stages share no subject or sample.
- Cohort counts: W1 170/174, W2 53/43 (IGT excluded), P1 223/217, P2 223/659 (stool-only "n" from the cirrhosis,
  colorectal, HMP+HMPII and MetaHIT datasets). These are four external studies by pubmedid.
- Covariate-only LR written independently: W1 age 0.7345, W2 BMI 0.6724, P1 study 0.5175, P2 study 0.8404. Depth
  from inputs/sampleMetadata.rda: W1 0.5910, W2 0.6606, P1 0.5940, all with complete matching.
- Reduced species RF, repeat-0 folds: real labels W1 0.738197 and P2 0.843379; within-study permutation seeds 0 and
  1 (W1 0.527217, 0.506307; P2 0.744230, 0.744313). All identical to the shipped TSV rows.
- Permutation files: 400 unique seeds per setting. Real label above every control in all four settings (W1 0.738 vs
  max 0.613; W2 0.776 vs 0.737; P1 0.743 vs 0.596; P2 0.843 vs 0.797). The S3 linear check agrees (P2 0.788 vs
  0.750; W1 0.699 vs 0.607). In W2, 16 of the 400 permutations were scored on 9 folds because one test fold had a
  single class. This is immaterial.
- Every number in the CLAIM sentence matches audit_results.csv at the stated rounding (W1 age 0.734516 -> 0.735).

## Null models

- N1 (claim/prereg/null_test.md): the P2 study-only LR scores 0.8305 on the repeat-0 folds, against at most 0.5752
  over 400 study-column permutations (mean 0.4994). It passes as pre-registered and matches
  results/pooled/null_n1.json. It is a low bar: it only shows that the study-only number is a real association
  rather than an artefact of encoding or CV, which is expected since every external control is label 0.
- N2, the within-study permutation, is the informative null. In P2 it shows that 77% of the published above-chance
  signal (0.760 mean) is available to the species RF from cohort structure alone. In every setting it shows that real
  labels carry signal beyond that structure.

## Bank pitfalls, applied to the audit itself

- Fitting inside folds: yes. The imputation, scaling and one-hot encoding of the covariate models sit in a Pipeline
  fitted on training rows. The RF has no normalisation, feature selection or tuning. S3 standardises inside the
  training fold.
- Subject/replicate leakage: grouped by subject, verified (0 straddles). Only S1 is deliberately ungrouped (the
  paper's literal scheme) and is reported as a sensitivity: 0.858 vs 0.856.
- Protocol mismatch: same cohort, same feature table and feature type, same 10 x 20 CV as the published values.
- Sample size: intervals and per-fold AUCs are given everywhere. W2 (n=96) has wide intervals. For example, the
  BMI fraction is 0.66 with interval 0.15-1.16, so the W2 fractions are imprecise.
- Study-of-origin confounding is the object of the audit itself.

## Stretched wording (not blocking; fix before filing)

1. CLAIM.md says "the paper's species pipeline trained on labels permuted within study gives 0.760". The pipeline
   that produced 0.760 is a reduced one: 100 trees, the repeat-0 folds only, mean fold AUC. Its real-label value is
   0.843, against 0.856 for the full pipeline. It should be called "a 100-tree version of the paper's random forest
   on one fold repeat". The same qualifier belongs on "real labels beating all 400 within-study permutations".
2. audit_summary.md labels the P2 rows "covariates only: age / bmi / depth" (0.776 / 0.699 / 0.661). These models also
   see a missingness indicator that marks HMP/HMPII membership. The complete-case values are age 0.681, BMI 0.570 and
   depth 0.625 (results/sensitivity/s6_*, s4_*). The CLAIM sentence does not use the P2 single-covariate rows, so
   nothing claimed is inflated, but the table should carry a footnote.
3. A covariate fraction is the share of the published above-chance AUC that a covariate can recover. It is not the
   share of the species model's AUC caused by that covariate: species scores keep 0.711 on age-matched Qin 2012
   pairs (S7). The W1 age figure (96%) reflects a case-control age imbalance inside one study, not between-cohort
   structure. The CLAIM sentence words this correctly ("recoverable without disease signal from the microbiome").
   The scope below keeps to "recover".
4. The RF covariate model gives higher W1 numbers than the primary LR (ALL 0.768, 110%). The claim reports the
   pre-registered primary LR, which is correct. Nothing should be phrased as "at most".

Not required by p3 and not held against the claim: medication (metformin), a known T2D microbiome confounder in
these same cohorts, is not among the bank's named covariates.

## Verdict

The claim meets p3 as written. For one disease (T2D) it gives code, committed folds and numbers with intervals for
the AUC recoverable from sequencing depth, study of origin, age, BMI and country alone, and from within-study label
permutation, as fractions of the published AUCs. The baselines reproduce within their pre-registered tolerances on
the same data, folds and metric. The audit avoids the bank's leakage and grouping pitfalls. This is a quantification
win of the kind p3 describes, not a restatement of the paper. The paper's own shuffled-label control is an ordinary
label permutation, with no within-study permutation and no covariate-only models. Prior publication elsewhere is the
NOVELTY skeptic's question, not this panel seat's.

confirmed_scope: For type 2 diabetes in the MetAML benchmark (Pasolli et al. 2016), on committed subject-grouped 10-fold x 20-repeat folds on which a scikit-learn reimplementation of the paper's random forest on species abundance reproduces the four published AUCs within the pre-registered tolerances (0.744, 0.768, 0.743 and 0.856 against 0.744, 0.762, 0.743 and 0.837), the pre-registered covariate-only logistic models reach AUC 0.735 from age alone within Qin 2012 (96% of the published above-chance signal), 0.683 from depth, age, BMI and country together within WT2D (70%), 0.711 from study, depth, age, BMI and country together in the merged T2D+WT2D set (87%) and 0.840 from study of origin alone in that set pooled with the healthy stool controls of four other studies (101% of the published 0.837), while in the pooled set a 100-tree version of the paper's random forest on one fold repeat averages 0.760 (77%) over 400 within-study label permutations and its real-label AUC exceeds all 400 within-study permutations in each of the four settings.

pass: true
