# REPRODUCE skeptic report

Panel member: REPRODUCE. I wrote my own checker from the criterion and PREREG text before reading `code/m1.py`.

## Definition quoted (success criterion, verbatim from CLAIM.md)

> Success means a saved score file assigning one real-valued fitness prediction to every mutant in the ProteinGym reference CSV for a chosen cancer-gene DMS assay (the assay's own reference file as distributed by ProteinGym, sha256 logged), produced by a method that is ZERO-SHOT with respect to that assay - it may use sequence, structure, MSAs, and other models' published score files, but no measurement from ANY ProteinGym DMS assay of the same UniProt protein may enter the method, and no hyperparameter, weight, threshold, model-selection decision or combination weight may be chosen using the target assay's labels - such that the Spearman correlation, recomputed by the skeptic with the official ProteinGym scoring convention (same mutant set, same direction convention, same NaN handling), is STRICTLY HIGHER (direction: max) than the maximum over all model columns for that assay in the live DMS-level Spearman CSV (re-fetched immediately before claiming) by at least 0.015 absolute. Any hyperparameter or combination weight must be fitted on a declared set of NON-cancer-gene assays, or on no data at all, and the fitting set must be logged with a sha256-stamped pre-registration file written before the target assay is scored. Deliverables: the score file, the pre-registration file, the method code, the list of external score files used with their provenance, and the skeptic-recomputable Spearman.

Method text re-implemented (PREREG.md, Method M1), paraphrased for reference: (1) for each of the 95 model columns compute Spearman with `DMS_score` on each fitting assay and take the protein-balanced mean (each assay weighted 1/number of fitting assays of its protein); (2) select the 12 models with the highest protein-balanced mean; (3) on the target assay z-score each selected model's raw scores over that assay's mutants and predict the unweighted mean of the 12 z-scores.

## What I checked

1. Mutant set of `result/PTEN_HUMAN_Matreyek_2021.M1.csv` vs `inputs/reference/PTEN_HUMAN_Matreyek_2021.csv`; duplicates; finiteness; all stated sha256 values (result, PREREG, split.json, reference file, live table copy).
2. Spearman(`DMS_score`, `prediction`) with scipy on the inner join by `mutant` (no NaNs present, so NaN handling is moot; no sign flip applied — direct correlation, as ProteinGym does).
3. Per-assay maximum over model columns of `inputs/DMS_substitutions_Spearman_DMS_level.csv`, excluding the five metadata columns, and the margin.
4. My own from-text re-implementation of M1 over all 187 fitting assays x 95 model columns (exhaustive, not a sample), compared against the saved result file; only afterwards read `code/m1.py`.
5. Label independence: replaced the target's `DMS_score` with random normals and recomputed; checked that no fitting assay shares a UniProt ID with PTEN_HUMAN and that the fitting list is exactly the complement of the frozen target + extra-excluded assays.
6. Determinism: my implementation re-run from a fresh read; the author's script run twice from relocated paths.

## Output of my own code (pasted)

```
result_cols: ['mutant', 'prediction']
n_result: 5083
n_ref: 5083
set_equal: True
order_equal: True
result_dupes: 0
pred_all_finite: True
pred_numeric: float64
sha_result: 1aecf9c14a0746b6b434b38acebfdfe8ddeefec98bedb322d6ea53b1ee7760db
sha_result_claimed: 1aecf9c14a0746b6b434b38acebfdfe8ddeefec98bedb322d6ea53b1ee7760db
sha_result_ok: True
sha_prereg: 365981fd71fee2d6d4e236fbdfaa476f05b76d8129de5f0e0722581a061420ad
sha_prereg_claimed: 365981fd71fee2d6d4e236fbdfaa476f05b76d8129de5f0e0722581a061420ad
sha_prereg_ok: True
sha_split: bf163ae630a11ccf759b27ee72cce9f617c8b48c262c891d5298541a9a5a3163
sha_split_claimed: bf163ae630a11ccf759b27ee72cce9f617c8b48c262c891d5298541a9a5a3163
sha_split_ok: True
n_merged: 5083
nan_DMS: 0
rho_claimfile: 0.5657628915591417
rho_pval: 0.0
n_model_cols: 97
n_model_cols_nonnan: 97
live_max: 0.516
live_argmax: VenusREM
margin: 0.04976289155914171
margin_ok: True
strictly_higher: True
n_models_in_scores: 95
n_fitting: 187
missing_fitting_files: []
pbm_top15: [('VenusREM', 0.541973), ('ProSST-2048', 0.530464), ('ProSST-4096', 0.524451), ('S3F_MSA', 0.517234), ('ProSST-1024', 0.513004), ('S2F_MSA', 0.508143), ('ESCOTT', 0.502578), ('ESM3', 0.499359), ('ProSST-512', 0.498999), ('ProSST-128', 0.496375), ('RSALOR', 0.491337), ('S3F', 0.489568), ('PoET', 0.489304), ('GEMME', 0.478644), ('VespaG', 0.47816)]
selected_12: ['VenusREM', 'ProSST-2048', 'ProSST-4096', 'S3F_MSA', 'ProSST-1024', 'S2F_MSA', 'ESCOTT', 'ESM3', 'ProSST-512', 'ProSST-128', 'RSALOR', 'S3F']
pbm_gap_12_13: 0.00026469693404379546
n_compare: 5083
max_abs_diff: 3.922779878706706e-10
allclose_1e-12: False
rho_mine: 0.5657628915591417
max_abs_diff_ddof1: 0.0002987135987524425
label_scramble_max_diff: 0.0
target_uniprot: PTEN_HUMAN
fitting_assays_sharing_uniprot: []
fitting_overlap_with_target_assays: []
fitting_overlap_with_extra_excluded: []
fitting_set_matches_complement: True
target_protein_in_target_proteins: True
fitting_with_PTEN_prefix: []
rerun_identical: True
```

Numerical probe (three independent arithmetic routes for step 3, including an extended-precision `longdouble` route, plus selection robustness):

```
maxdiff A vs file : 3.922779878706706e-10     (2-D array route)
maxdiff B vs file : 3.922779878706706e-10     (per-column 1-D route)
maxdiff C vs file : 3.922779878706706e-10     (longdouble route)
maxdiff A vs B    : 0.0
rho[file] = 0.5657628915591417
rho[A]    = 0.5657628915591417
rho[B]    = 0.5657628915591417
rho[C]    = 0.5657628915591417
rank order identical A/B/file: True True
uniprot maps agree on fitting assays: True
live top12 == True | 12th,13th: ('S3F', 0.48956849407036207) ('PoET', 0.4893037971363183)
meta top12 == True | 12th,13th: ('S3F', 0.48956849407036207) ('PoET', 0.4893037971363183)
live unweighted-mean top12 == False      (protein balancing is load-bearing, as pre-registered)
any NaN in fitting rho matrix: 0
model col count: 95
```

sha256 of the other stated objects, and the zip-vs-reference label cross-check:

```
ref file sha  : 1c52aba95950c6d3b1ac8320df4cb99a79ae97353bd43e24c87ef78dbb02e636   (matches REPRODUCE.md)
live csv sha  : f432423b87f79ac9778dfac86e3d95be041d246bc618dc0a406b35b0b7466437   (matches SCOUT_RECORD.md)
live csv bytes: 141235                                                            (matches SCOUT_RECORD.md)
scores vs reference: rows 5083/5083, mutant sets equal: True, order equal: True
max |DMS_score zip - DMS_score reference|: 4.996199010065538e-10
ties in DMS_score: 81   ties in prediction: 0
```

Determinism, author code (`code/m1.py` with input paths relocated, output written outside claim/, run twice):

```
selected: ['VenusREM', 'ProSST-2048', 'ProSST-4096', 'S3F_MSA', 'ProSST-1024', 'S2F_MSA', 'ESCOTT', 'ESM3', 'ProSST-512', 'ProSST-128', 'RSALOR', 'S3F']
selected: ['VenusREM', 'ProSST-2048', 'ProSST-4096', 'S3F_MSA', 'ProSST-1024', 'S2F_MSA', 'ESCOTT', 'ESM3', 'ProSST-512', 'ProSST-128', 'RSALOR', 'S3F']
author run1 sha: 9feace6e36d2687cf1d0672d18815084c86261f666234ecf802f3ca3b0637e24
author run2 sha: 9feace6e36d2687cf1d0672d18815084c86261f666234ecf802f3ca3b0637e24
identical runs: True
claim sha      : 1aecf9c14a0746b6b434b38acebfdfe8ddeefec98bedb322d6ea53b1ee7760db
authorcode vs claimfile maxdiff: 3.922779878706706e-10
rho author-code rerun: 0.5657628915591417
```

After reading `code/m1.py`: it implements exactly the three PREREG steps, uses `UniProt ID` from the live table for the protein weights (I used `UniProt_ID` from `inputs/DMS_substitutions.csv`; the two maps agree on all 187 fitting assays), z-scores with population sd (ddof=0, matching my implementation — ddof=1 would differ by 3e-4), and never opens the reference file or the target's `DMS_score`.

## Mismatches and caveats

- One real mismatch, understood and quantified: the saved `result/...M1.csv` is not bitwise reproducible from `inputs/scores/`. Every route I tried (my from-text implementation, the author's own code re-run, and an extended-precision recomputation) lands 3.9228e-10 away from the saved file, identically. The cause is that the packaged score CSVs are rounded to ~10 significant digits: the same rounding shows up independently as a 5.0e-10 difference between the target's `DMS_score` in `inputs/scores/` and in the reference file, which `code/m1.py` never reads. So the saved file was produced from full-precision ProteinGym scores and the packaged inputs are a rounded copy. The effect is well below any decision threshold: predicted ranks are identical, and Spearman agrees to all 16 printed digits (0.5657628915591417). I record this as agreement "to float precision of the supplied inputs", not as a bitwise reproduction, and I note that the full-precision zip itself is not in the package, so the last 1e-10 of the saved object is not independently checkable from claim/ alone.
- The model-selection step is tight: the 12th selected model (S3F, 0.4895685) beats the 13th (PoET, 0.4893038) by only 2.6e-4 protein-balanced Spearman. That is ~6 orders of magnitude above the input-rounding noise, so the frozen selection is stable here, but it is a thin margin in the method's design.
- Out of scope for me, flagged for the convention/leakage members: I verified the live-table copy's sha256 and byte count against SCOUT_RECORD.md, but I cannot verify from saved files alone that this copy equals what the live URL served at claim time, nor that the 95-column scores are the unmodified v1.3 zip (the zip sha256 is stated, the zip is not shipped).
- Everything else checked clean: 5083/5083 mutants, same set and same order, no duplicates, all predictions finite real numbers, no NaNs anywhere in the join or in the 187x95 fitting correlation matrix, margin 0.0498 >= 0.015 and strictly higher than the live max (0.516, VenusREM), target labels provably unused (randomizing them changes nothing, max diff 0.0), no fitting assay sharing UniProt PTEN_HUMAN (and none even name-prefixed PTEN), fitting set exactly the 187-assay complement of the 13 frozen targets plus 17 extra exclusions, PREREG and split sha256 as stated, PREREG frozen 19:11:52Z before the prediction file at 19:13:23Z, and both my implementation and the author's reproduce identically on re-run.

context: subagent (Claude Code Agent, fresh context)
pass: true
