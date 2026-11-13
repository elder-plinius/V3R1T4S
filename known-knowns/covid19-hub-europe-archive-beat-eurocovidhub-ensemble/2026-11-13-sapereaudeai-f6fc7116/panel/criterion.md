context: subagent (Claude Code Agent tool, fresh context)

# CRITERION skeptic: covid19-hub-europe-archive-beat-eurocovidhub-ensemble, partial win p3

Written 2026-11-13 about 06:10 UTC. Paths are relative to claim/ unless they start with `../panel/`.

## What was checked

- Bank text: the p3 statement and the main criterion copied in CLAIM.md match bank/targets.json word for word.
- I ran the claim's own code (REPRODUCE.md steps 1 to 5) into my work folder. The self-test passed. `p3_reproduce.py`
  in modes owidhosp and primary gives logs and per-model CSVs byte-identical to reference_outputs/. `rederive_exclusions.py`
  (both modes) and `vintage_diff.py` also give outputs byte-identical to reference_outputs/.
- I wrote my own check (`../panel/work_criterion/indep_check.py`, log `../panel/work_criterion/indep_log.txt`). It does its
  own parsing of the 357 raw forecast files and the truth files, its own WIS decomposition with an assertion against the
  pinball form, and exact rational arithmetic for the tie rows. It does not use claim/code. Results:
  primary 30,722 of 31,256 rows exact on all 4 rounded components; owidhosp 31,253 exact. In both modes the same
  per-model relative differences as the claim to 5 significant figures. Under primary the same 7 models are over 1%.
  Under owidhosp none is.
- Data provenance: all 367 fetch-log entries for archive files have matching sha256 on disk, including all 357
  data-processed files, the truth files and scores.csv (c59afa8e...). I made one honest request (User-Agent naming
  V3R1T4S) for data-truth/OWID/truth_OWID-Incident Hospitalizations.csv at the pinned commit ef5eef84. It returned
  HTTP 200 and 11,177 bytes, with sha256 6e225033... identical to the claim's copy. This is the file the "why" rests on.
- Circularity: no published value enters the recomputation. scores.csv supplies only the row keys and the
  (model, forecast_date) file list (pre-registered reading 5). `rederive_exclusions.py` decides "kept" without the
  published set. Negative controls show the comparison can fail:
  - the 1/(K+1) form matches only 13,252 rows;
  - the ECDC hospitalisation truth leaves 534 rows non-exact.

## p3 word by word

- **"independent"**: yes. It is a separate Python implementation with no R and no scoringutils. The hub's R code was
  read only as text, for conventions: point-as-median, permitted quantiles, rounding, and the Monday file-date map. My
  second independent implementation agrees.
- **"scoring reproduction / recompute"**: yes. The four components were recomputed for every published row (31,256 of
  31,256 covered, 0 missing files) and then averaged per model. This is not a lookup.
- **"the published per-model WIS decomposition in scores.csv"**: met. The pre-registered reading is the per-model mean
  of wis, sharpness, underprediction and overprediction over each model's published rows. That is the natural reading,
  and the row-level match goes beyond it. The bias column is not part of the decomposition. It was not recomputed, and
  the claim says so.
- **"from data-processed and the truth data"**: yes. Every input is an archive file from data-processed/ or data-truth/
  (ECDC and OWID), sha-verified. The bank's "the truth data" does not name a provider, so the archive's OWID
  hospitalisation file is literally inside "the truth data".
- **"documenting every model whose recomputed value differs by more than 1%"**: met under the frozen primary reading
  (ECDC truth for all three targets). All 7 over-1% models are named with the component and size:
  - EuroCOVIDhub-baseline underprediction -1.51%;
  - EuroCOVIDhub-ensemble underprediction -1.12% and overprediction +1.07%;
  - Lydia-SARIMA underprediction -1.91%;
  - Lydia-simpleARIMA underprediction -2.14% and overprediction +1.13%;
  - epiforecasts-tsensemble overprediction +1.15%;
  - epiforecasts-weeklygrowth overprediction +1.92%;
  - fjordhest-ensemble underprediction -1.72%.

  The 8 others are within 1%. Under the OWID rule, no model is over 1%.
- **"and why"**: shown by output for each of the 7, not just asserted.
  - mismatch_diagnosis.txt: 531 of the 534 non-exact rows are inc hosp CZ.
  - vintage_diff.txt: ECDC and OWID differ on 36 of the 37 published Czech weeks.
  - per_model_owidhosp.csv: with only the Czech hospitalisation truth swapped to the archive's OWID file, each of the 7
    falls to at most 3.2e-6, and all 531 rows match exactly.
  - rederive_*.txt: with OWID the hub's re-derived rules give exactly the published row set. With the ECDC file they
    would add 1,642 non-Czech hospitalisation rows that scores.csv does not contain. This is consistent with the hub's
    data-truth README, which names OWID-collated data (Czechia) for hospitalisations.
  - My own check adds a per-model attribution. Dropping the inc hosp CZ rows from both sides brings every model to
    |rel diff| <= 3.3e-6 under the primary truth, so the >1% part comes entirely from those rows.
  - The 3 remaining non-exact rows are exact half-integers in rational arithmetic (71/2, 5/2, 9009/2). R's
    half-to-even rounding of those exact values gives the published 36, 2 and 4504. The mismatch is float error on the
    recompute side, so "exact half-integer rounding tie" is accurate.

## Is the OWID file a legitimate "why" or a post-hoc change of reading?

It is legitimate as the "why":
- PREREG.md (frozen 05:44:59Z) fixed ECDC for all three targets as primary.
- Its escape hatch allows a cause to be stated if it is "shown by output (for example ... the row reproduces exactly
  under the declared alternative truth vintage, or under a stated rule)". OWID is a stated rule (CLAIM Rule 1), and
  the row reproduction under it is exact.
- CLAIM.md says plainly that OWID was "NOT declared in advance".
- The p3 verdict does not depend on swapping the reading. Under the frozen primary reading, p3 is already satisfied,
  because p3 asks for documentation of the >1% models and their cause, not for all models within 1%.

What would not be legitimate is presenting "15 of 15 within 1%" as the pre-registered result. The one-sentence claim
leads with the OWID numbers, but it labels them and gives the primary numbers in the same sentence. I treat this as
emphasis, not misstatement. The confirmed scope below is anchored on the primary reading.

## Hidden quantifiers, stretched definitions, null model

- **Granularity**: at model x target_variable level under the primary truth, 10 inc hosp groups exceed 1%. Their
  component differences go up to -100% underprediction and +1134% overprediction (epiforecasts-EpiNow2), and WIS moves
  up to +47%. Three of these groups belong to models whose overall means stay within 1%: ECDC-norrsken_green,
  ECDC-soca_simplex and epiforecasts-EpiNow2.
  - CLAIM.md's text names only the per-model 7. The groups are listed in reference_outputs/per_model_target_primary.csv
    and have the same shown cause. Under OWID, 0 of 37 groups exceed 1% (max 3.3e-6).
  - PREREG fixed per-model means as deciding and per model x target as secondary, before results. This is the fair
    reading of "per-model", so it is not a gap, but a reader should know the hospitalisation slice is far off under
    the primary truth.
- **"every model"**: all 15 models in scores.csv are covered, with 0 missing files and 100% of rows. No model was
  excused.
- **Null model**: the "not needed" reasoning holds. This is a deterministic recomputation against a published table,
  with no search or selection. The negative controls above show the agreement is not automatic.

## baseline/ record

Same data, split and metric as the claim:
- data: the archive files fetched 2026-11-13, sha-verified;
- split: all 31,256 published rows, per model;
- metric: per-row 23-quantile Bracher WIS decomposition, rounded per row, then the per-model mean.

baseline/p3_per_model_vs_published.csv has the stated sha256 (f6fc7116...). Its published and recomputed columns
equal reference_outputs/per_model_{primary,owidhosp}.csv to within 1e-5 for all 15 models in both modes.

## Scope nits (not blocking)

- The one-sentence claim says the script "recomputes every one of the 31,256 rows". It recomputes wis, the 3
  components, ae_median and coverage, but not bias. "What is not claimed" carves bias out.
- The README says the OWID/final files are the ones used for scoring. The claim used OWID/truth_OWID-Incident
  Hospitalizations.csv. The exact match of all 531 rows makes this immaterial. "The source the README names" is true at
  the level of the provider (OWID), not the file.
- The "commit ef5eef84 at fetch time" is inferred from tree pages, while files came from main. My pinned-commit fetch
  of the OWID file matched, which supports it.
- "Non-subsumed": nothing in the package shows a prior claim of this partial win (the scout found no trophy or
  known-knowns entry). Open V3R1T4S PRs were not checked, and a published recomputation is for the NOVELTY skeptic to
  rule out.

## Decision

The result meets the enumerated partial win p3 literally under the readings frozen before any score existed:
- the recomputation is independent and covers every row and every model;
- every model over 1% is named;
- the cause is shown by output for each;
- the scope statements, read with "What is not claimed", are no wider than the evidence.

confirmed_scope: An independent Python recomputation (no R, no scoringutils) of the wis, sharpness, underprediction and overprediction values of all 31,256 rows (15 models, forecast dates 2023-10-30 to 2024-09-16) of the European COVID-19 Forecast Hub archive's evaluation/scores.csv (sha256 c59afa8e3c9530e71d1c4c5445794bf6600b9ae3aaecec89db7e34def4aeb54c) from the archive's data-processed files and truth data shows that, with the pre-registered ECDC truth for all three targets, exactly 7 models (EuroCOVIDhub-baseline, EuroCOVIDhub-ensemble, Lydia-SARIMA, Lydia-simpleARIMA, epiforecasts-tsensemble, epiforecasts-weeklygrowth, fjordhest-ensemble) have a per-model mean component more than 1% from the published mean (largest 2.14%, Lydia-simpleARIMA underprediction), and that all of this excess comes from the 531 Czech inc hosp rows, which match exactly when scored against the archive's OWID hospitalisation file, under which all 15 models agree within 1% on all four components (max 3.2e-6) and the only 3 non-matching rows are exact half-integer values that half-to-even rounding sends to the published integers.

pass: true
