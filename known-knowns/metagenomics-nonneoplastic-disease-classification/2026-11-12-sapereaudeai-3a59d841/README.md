# How much of the MetAML type 2 diabetes AUCs is cohort structure and host covariates: a confound audit (bank target metagenomics-nonneoplastic-disease-classification, partial win p3)

## What
For type 2 diabetes in the MetAML benchmark (Pasolli et al. 2016), on committed subject-grouped 10-fold x 20-repeat folds on which a scikit-learn reimplementation of the paper's random forest on species abundance reproduces the four published AUCs within the pre-registered tolerances (0.744, 0.768, 0.743 and 0.856 against 0.744, 0.762, 0.743 and 0.837), the pre-registered covariate-only logistic models reach AUC 0.735 from age alone within Qin 2012 (96% of the published above-chance signal), 0.683 from depth, age, BMI and country together within WT2D (70%), 0.711 from study, depth, age, BMI and country together in the merged T2D+WT2D set (87%) and 0.840 from study of origin alone in that set pooled with the healthy stool controls of four other studies (101% of the published 0.837), while in the pooled set a 100-tree version of the paper's random forest on one fold repeat averages 0.760 (77%) over 400 within-study label permutations and its real-label AUC exceeds all 400 within-study permutations in each of the four settings.

These are retrospective classification statistics on published research cohorts. They are not clinical advice, and
they say nothing about diagnosing diabetes in any person.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: `PASS`. Laptop time: under a second, Python 3 standard library only (set PYTHON if python3 is not
on PATH). It recomputes the single-covariate AUCs exactly from the shipped covariate table and committed folds, the
pooled study-only AUC, the permutation summaries, the null and the headline fractions. To rebuild every number from
the public data (about 1.5 CPU-hours), see RUN_IT_YOURSELF.md.

## Compared to
| what | value | source | fetched (UTC) |
|---|---|---|---|
| published RF-on-species AUCs audited (status source) | T2D 0.744, WT2D 0.762, T2D+WT2D 0.743, T2D+WT2D plus healthy controls of four other datasets 0.837 | Pasolli et al. 2016, PLoS Comput Biol 12(7): e1004977, https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4939962/fullTextXML | 2026-11-12T18:27:02Z |
| our reimplementation on the committed folds (baseline) | 0.744, 0.768, 0.743, 0.856 | how-we-built-it/baseline/README.md | - |
| nearest published work (as read by the NOVELTY skeptic, panel/novelty.md) | the same mechanism on another cohort (MetaHIT IBD, Danish vs Spanish controls) and metformin confounding in SIAMCAT (Wirbel et al. 2021, Genome Biol); an age/sex/BMI leave-one-dataset-out baseline across ten T2D cohorts (the 8,117-metagenome cross-cohort T2D study, Nat Med 2024, PMC11620793); the Qin 2012 age imbalance in age-group counts (Ghosh et al. 2020, eLife) | panel/novelty.md | 2026-11-12 |

## Not claimed
- Not that the gut microbiome carries no T2D signal: the paper's random forest with real labels beats all 400
  within-study permutations in every setting, and on age-matched Qin 2012 pairs the species score keeps AUC 0.711
  (how-we-built-it/results/sensitivity/s7_matched_pairs.json).
- A covariate's fraction says how much of the published AUC a model that sees only that covariate can reach, not how
  much of the species model's AUC the covariate causes. The 96% for age within Qin 2012 is an age imbalance between
  cases and controls inside one study, not cohort structure.
- The 0.760 permutation value comes from a reduced version of the paper's pipeline (100 trees, one fold repeat; its
  real-label AUC is 0.843 against 0.856 for the full pipeline). With a linear learner the same permutation gives 0.674
  (52% of the published signal): the cohort-structure share depends on the learner (results/sensitivity/s3_summary.txt).
- The pooled study-only AUC follows arithmetically from the published sample counts (scoring each sample by its
  study's case fraction gives about 0.842); it is new as an explicit statement on this benchmark, not as an empirical
  surprise. The Qin 2012 age imbalance was visible in Ghosh et al. 2020's age-group counts (about 0.70 implied); 0.735
  refines it with continuous age.
- In the pooled set (P2), the age-, BMI- and depth-alone rows of object/audit_summary.md include a missingness flag
  that marks HMP membership; complete-case values are lower (age 0.681, BMI 0.570, depth 0.625; results/sensitivity
  s4 and s6). The headline sentence does not use those rows. The fraction of the permutation mean against our
  reproduced P2 AUC (0.856) is 0.729.
- Our pooled set has 882 samples (223 T2D, 659 controls, with "healthy" read as disease label n, stool); MetAML's
  Methods mention 908 samples for its pooled analysis, so the external-control set may differ slightly; the published
  0.837 is reproduced at 0.856, inside the pre-registered +/- 0.03.
- Freeze times are written inside the PREREG files; file times in a copied package cannot prove the order.
- Nothing about the main success criterion, p1 or p2 (other attempts of the same run are listed in
  how-we-built-it/other_prereg_files_of_this_run/ and the run report).

## Credits
- MetAML and its data: Pasolli E, Truong DT, Malik F, Waldron L, Segata N (2016), PLoS Comput Biol 12(7): e1004977;
  https://github.com/SegataLab/metaml
- The cohorts, as cited by MetAML: Qin et al. 2012 (T2D), Karlsson et al. 2013 (WT2D), Qin et al. 2014 (cirrhosis),
  Zeller et al. 2014 (colorectal), the Human Microbiome Project (HMP), and the MetaHIT study used as MetAML's IBD set.
- Per-sample read counts: curatedMetagenomicData (Waldron lab and contributors),
  https://github.com/waldronlab/curatedMetagenomicData
- Related analyses found and read by the NOVELTY skeptic (panel/novelty.md): SIAMCAT (Wirbel et al. 2021), the
  8,117-metagenome cross-cohort T2D study (Nat Med 2024, https://pmc.ncbi.nlm.nih.gov/articles/PMC11620793/), Ghosh et
  al. 2020 (eLife), Forslund et al. 2015 (Nature, metformin), Vujkovic-Cvijin et al. 2020 (Nature, host variables).
- Software: scikit-learn, numpy, scipy, pandas; rdata (pure-Python .rda reader).
