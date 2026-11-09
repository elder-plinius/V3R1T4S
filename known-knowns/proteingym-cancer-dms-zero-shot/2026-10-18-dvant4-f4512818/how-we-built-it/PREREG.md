# PREREG: proteingym-cancer-dms-zero-shot

frozen_at: 2026-10-18T19:11:52Z (from date -u). No cancer-target assay label has been read by any method code before this time. The
convention check computed the published single-model columns' Spearman, which reproduces the public CSV and chooses nothing.

## Criterion (verbatim)
Success means a saved score file assigning one real-valued fitness prediction to every mutant in the ProteinGym reference CSV for a chosen cancer-gene DMS assay (the assay's own reference file as distributed by ProteinGym, sha256 logged), produced by a method that is ZERO-SHOT with respect to that assay - it may use sequence, structure, MSAs, and other models' published score files, but no measurement from ANY ProteinGym DMS assay of the same UniProt protein may enter the method, and no hyperparameter, weight, threshold, model-selection decision or combination weight may be chosen using the target assay's labels - such that the Spearman correlation, recomputed by the skeptic with the official ProteinGym scoring convention (same mutant set, same direction convention, same NaN handling), is STRICTLY HIGHER (direction: max) than the maximum over all model columns for that assay in the live DMS-level Spearman CSV (re-fetched immediately before claiming) by at least 0.015 absolute. Any hyperparameter or combination weight must be fitted on a declared set of NON-cancer-gene assays, or on no data at all, and the fitting set must be logged with a sha256-stamped pre-registration file written before the target assay is scored. Deliverables: the score file, the pre-registration file, the method code, the list of external score files used with their provenance, and the skeptic-recomputable Spearman.

## Cancer-gene assays scored (frozen; attempts/optimizer/split.json, sha256 bf163ae630a11ccf759b27ee72cce9f617c8b48c262c891d5298541a9a5a3163)
The 13 assays of the 8 proteins the bank names (BRCA1, BRCA2, PTEN, MSH2, P53, RASK, RASH, ERBB2). Each one is scored. All
13 are reported, wins and losses alike.

## Fitting set (frozen)
187 assays: every ProteinGym substitution assay except the 13 targets and 17 assays of 16 further oncology-related proteins
(MET, SRC, RAF1, MK01, PPM1D, SHOC2, YAP1, TPOR, PPARG, CAR11, PRKN, GRB2, CASP3, CASP7; MLH1 and VHL are listed but have
no assay). The exclusion is by UniProt id. No fitting assay shares a UniProt id with a target.

## Method M1 (the only method that can carry a claim)
1. For each of the 95 model columns in the v1.3 merged score files (zero_shot_substitutions_scores.zip, sha256
   3fd7cdb5e78f1d43cabfabfeb6578c252b63af23ba2ab44db0094dc3a42de36d), compute Spearman with DMS_score on each fitting assay.
   Take the protein-balanced mean (each assay weighted 1/number of fitting assays of its protein).
2. Select the 12 models with the highest protein-balanced mean.
3. On the target assay, z-score each selected model's raw scores over that assay's mutants (mean 0, sd 1; no labels).
   The prediction is the unweighted mean of the 12 z-scores.
Chosen from leave-protein-out exploration on the fitting set only (attempts/optimizer/explore_fit*_output.txt). Over 187
held-out fitting assays, z/K=12/equal beat the live per-assay max by >= 0.015 on 30/187 (16%).

## Statistic and thresholds
- Statistic: Spearman(DMS_score, prediction) on the official reference file (same mutants), computed by
  attempts/checker/code/pg_checker.py. Bar: live per-assay max over all model columns of the live DMS-level CSV.
- Main win: margin >= 0.015 on at least one target assay. Because 13 assays are tried, the report gives the count over all 13,
  together with the leave-protein-out base rate (16%), so that a single win is read in context.
- p1: margin >= 0.015 on >= 3 target assays with M1.
- p2: margin >= 0.02 on MSH2_HUMAN_Jia_2020 with M1.
- p3 (audit, reported for all 13): reachable fraction = (rho_M1 - best_single_live) / (rho_oracle - best_single_live).
  Here rho_oracle is the best equal-weight z-score ensemble that greedy forward selection finds using the target's own
  labels (up to 12 models from the 95). It is a ceiling, not a method.
- Information only: 1,000 mutant-bootstrap resamples of (rho_M1 - rho_bestcolumn) for each assay, using the best column
  present in the zip.

null_test: not needed because the claim is a frozen prediction file scored by a deterministic checker against a live table value; there is no search over target labels (the leave-protein-out base rate and the oracle ceiling are reported for context)

Any change after scoring goes in a new timestamped PREREG.v2.md.
