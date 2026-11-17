# How we found it (contributor text, unverified)

The bank's p3 asks for a confound audit of one disease in the MetAML benchmark. Before any model was fitted, the
disease was fixed by a rule (the MetAML non-cancer disease with the most source studies: type 2 diabetes, the only one
with two), and the readings, data, folds, models, baselines and null were frozen in how-we-built-it/PREREG.md.

We reimplemented the paper's random forest on species abundance in scikit-learn and reproduced its four published T2D
AUCs on committed, subject-grouped 10-fold x 20 folds. Then, on the same folds, we fitted logistic models that see
only covariates (per-sample sequencing depth from curatedMetagenomicData, age, BMI, country, study of origin), alone
and together, and reran the paper's pipeline (100 trees, one fold repeat) on 400 label permutations within study.

What we saw: inside the Qin 2012 cohort the controls are about 12 years younger than the cases, so age alone matches
the published microbiome AUC; inside WT2D, BMI and sequencing depth carry most of it; and in the paper's pooled set
with healthy controls from four other studies, knowing only which study a sample came from already gives the
published 0.837, while the random forest trained on within-study-permuted labels still reaches 0.760. The species
signal itself is not just age: on age-matched Qin 2012 pairs the species score keeps AUC 0.711.

What failed or was dropped: a first run of the pooled settings crashed at the last (pair-decomposition) step on a
pandas string type and was rerun with identical numbers; a linear learner shows a smaller cohort-structure share
under permutation (0.52 instead of 0.77), which is reported as a sensitivity result. Three sensitivity analyses were
added in later timestamped PREREG files before their results existed.
