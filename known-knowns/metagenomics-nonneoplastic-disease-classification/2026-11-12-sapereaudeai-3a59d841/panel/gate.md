# Honesty gate (kit RUN.md step 7), run 2026-11-12-1824 (p3 confound audit)

Read by the run's main session at 2026-11-12T21:03Z (date -u): panel/reproduce.md, panel/novelty.md, panel/criterion.md.
- REPRODUCE (subagent, fresh context): pass: true. Independent covariate LR/RF, species RF, null N1, permutation
  reruns (all 400 P2 seeds and samples of the others) and a leakage test match the claim exactly. Documentation
  findings, none blocking: read_rda.py needs about 1.1 GB with rdata; FOLDS sha256 files have CRLF endings; the fold
  grouping key is dataset:subject (hmp and hmpii pooled); 16 W2 permutations scored 9 folds; P2 missingness channel.
- NOVELTY (subagent, fresh context): pass: true. Status source re-fetched 19:54:36Z (identical). No published or filed
  work contains this quantification of the MetAML T2D AUCs; caveats: the pooled study-only AUC follows arithmetically
  from the published sample counts (new as an explicit statement), and the Qin 2012 age imbalance was visible in
  Ghosh et al. 2020 age-group counts (about 0.70 implied).
- CRITERION (subagent, fresh context): pass: true; every element of p3 covered for T2D; baselines within their
  pre-registered tolerances on the same data, folds and metric; wording notes carried into the package README.
No downgrade reason applies: no hedged verdict, no reproduction mismatch, baselines resolved, the status-source
fetch is under 6 hours old (19:54:36Z), and the scope is the CRITERION sentence, which names the reduced permutation
pipeline exactly.

status: CONFIRMED_PARTIAL
confirmed_scope: For type 2 diabetes in the MetAML benchmark (Pasolli et al. 2016), on committed subject-grouped 10-fold x 20-repeat folds on which a scikit-learn reimplementation of the paper's random forest on species abundance reproduces the four published AUCs within the pre-registered tolerances (0.744, 0.768, 0.743 and 0.856 against 0.744, 0.762, 0.743 and 0.837), the pre-registered covariate-only logistic models reach AUC 0.735 from age alone within Qin 2012 (96% of the published above-chance signal), 0.683 from depth, age, BMI and country together within WT2D (70%), 0.711 from study, depth, age, BMI and country together in the merged T2D+WT2D set (87%) and 0.840 from study of origin alone in that set pooled with the healthy stool controls of four other studies (101% of the published 0.837), while in the pooled set a 100-tree version of the paper's random forest on one fold repeat averages 0.760 (77%) over 400 within-study label permutations and its real-label AUC exceeds all 400 within-study permutations in each of the four settings.
