# PREREG (written 2026-11-13T04:32:59Z, before any score of ours or any recomputed published score exists)

target: german-hospitalization-nowcast-hub-beat-ensemble-wis

## Criterion and partial wins (verbatim, bank/targets.json)

Success means saved quantile nowcasts, in the hub's submission format, for every (forecast_date, location, age_group, delay horizon) row for which the hub ensemble has a nowcast over one declared continuous evaluation period of at least eight weeks within the hub's operating window, produced by a deterministic pipeline that at each date reads ONLY the reporting triangle as it stood on that date (the hub's dated truth files), whose mean weighted interval score against the hub's final truth, recomputed by the skeptic with public scoring code on exactly those rows, is STRICTLY LOWER (direction: min) than the ensemble's by at least 5% relative, with a stationary bootstrap over dates at 90% excluding zero. The scorer must first reproduce the ensemble's published scores from https://github.com/KITmetricslab/hospitalization-nowcast-hub and the evaluation of https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10446237/fullTextXML (re-read live immediately before claiming) to within 1%. Submitted nowcasts of other teams may not be consumed.

- p1: Beat the ensemble by >= 5% relative WIS restricted to the youngest and oldest age strata, where delays are longest and the submitted pool thinnest, over the declared period.
- p2: Beat every individual submitted model (not necessarily the ensemble) over the declared period under the as-of discipline, with the bootstrap interval excluding zero.
- p3: A reproduction of the hub's published evaluation: recompute per-model WIS for the published period from data-processed and the truth data with a released script, documenting every discrepancy and the exclusion rules needed to reconcile it.

null_test: not needed because p3 is a deterministic recomputation of published table values by a deterministic scorer, and p1 compares one frozen nowcaster with one named comparator (the hub MeanEnsemble) on a pre-declared period using a stationary-bootstrap interval over dates (no search over models, periods, strata or targets on the scored period).

## Readings fixed now (most favourable FAIR reading, chosen before any result)

- **Hub ensemble** = `NowcastHub-MeanEnsemble` (the paper's pre-specified primary ensemble, section 2.4). The
  MedianEnsemble is reported descriptively only.
- **Declared period** = forecast dates 2021-11-22 .. 2022-04-29 inclusive (159 daily dates, the paper's study period;
  continuous, more than 8 weeks, inside the hub's operating window).
- **Horizons** = the hub's targets "0 day ahead inc hosp" .. "-28 day ahead inc hosp" (7-day sums ending on
  forecast_date + h, count scale, not per 100k), quantile levels 0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975.
- **WIS** = mean over the 7 quantile levels of 2 x pinball loss = the paper's equation (2) with alpha = 0.5, 0.2, 0.05
  (identical to the evaluation repository's `qs()` averaged over quantile rows).
- **Final truth** = the data version of 2022-08-08 (the paper's protocol "final state", the truth the published
  ensemble scores used): rowSums of all value columns of the hub's `COVID-19_hospitalizations_preprocessed.csv` at
  commit 11c745322c055cfbd4f0c8f72241642a50aea399 (2022-08-08T05:10:27Z), 7-day rolling sum per stratum. Descriptive
  only: the 40-day truth of the paper's sensitivity analysis (`truth_40d.csv.gz`).
- **"Submitted models"** (for any p2 statement) = the 8 individual teams' models scored in the paper (Epiforecasts,
  ILM, KIT, LMU, RIVM, RKI, SU, SZ) as stored in data-processed / data-processed_retrospective for the period.
- **Age strata for p1**: location DE, age groups `00-04` (youngest) and `80+` (oldest); the hub has no age-by-state
  strata. p1 statistic = mean WIS POOLED over all scored rows of the two strata (the literal "restricted to the
  youngest and oldest age strata"); per-stratum values are reported descriptively.

## p3 (reproduce the published evaluation); this is also step 3c's baseline record

- **Published values (expected)**: `data/scores/wis_national.csv`, `wis_states.csv`, `wis_age.csv` from
  https://github.com/dwolffram/hospitalization-nowcast-hub-evaluation (main; repo pushed 2023-10-26): 31 cells of
  mean WIS (11 models national, 10 states, 10 age) plus their spread / over / under components. These are the
  numbers behind the paper's Fig 7.
- **Inputs**: the hub's data-processed (+ data-processed_retrospective, which replaces a prospective file of the same
  model and date, as the paper's released loader does) for 2021-11-22..2022-04-29, read through the evaluation
  repository's released assembly `data/submissions.csv.gz` (sha256 recorded in baseline/); its identity with the
  hub's own files is checked on every hub file we fetched (all 159 MeanEnsemble files, plus a provenance sample on
  2021-11-22, 2022-01-15 and 2022-03-31 for every model; dates chosen before any comparison). If the other models'
  full hub files arrive within the budget, the assembly is checked against all of them too.
  KIT-frozen_baseline is not in the hub; its file comes from the evaluation repository. ILM/LMU fill rows come from
  the hub's data-processed_updated_models, as the paper's `fix_ILM` / `fix_LMU` rules state.
- **Truth**: recomputed from the hub truth at commit 11c74532 (above) and compared cell by cell with the evaluation
  repository's `truth_2022-08-08.csv`.
- **Scorer**: our own Python (numpy/pandas) script, written from the paper's definition; the evaluation's R code is
  read as documentation only, never run (no R here).
- **Ladder (declared)**: S0 = every quantile row in the assembly, no fixes, no exclusions; S1 = S0 + the paper's
  exclusion rule (targets listed as missing for Epiforecasts, MeanEnsemble, MedianEnsemble, SZ are removed for ALL
  models); S2 = S1 + the paper's fixes (RKI implausible >1e6 or NA values replaced by the -1/0 day values;
  Epiforecasts missing 0.1 quantile interpolated from a normal fitted to the 0.025 and 0.25 quantiles; ILM and LMU
  missing rows filled from data-processed_updated_models). Each step's per-cell differences are reported.
- **Tolerance**: within 1% relative per cell (the criterion's own tolerance for the scorer gate). p3 is reproduced
  when all 31 cells are within 1% with every rule documented; any cell outside 1% is a documented discrepancy with
  its cause, or unresolved.
- **Escape hatch**: if the assembly and the hub's files disagree anywhere in the checked set, p3 is reported as a
  reproduction of the authors' assembly only, the disagreement is listed, and no p3 claim is made from it.

## p1 (one frozen nowcaster vs the MeanEnsemble on DE 00-04 and 80+)

- **As-of discipline**: at forecast date t the model reads only triangle cells value_kd (k = 0..80) of reference
  date d with d + k <= t, from the hub's raw `COVID-19_hospitalizations.csv` at commit 11c74532. Audit done before
  this prereg (data only): truncating that file reproduces the hub's dated vintages of 2021-12-15, 2022-01-15 and
  2022-03-15 exactly (0 mismatching cells out of 2,062,746 / 2,361,555 / 2,930,256 known cells). The `value_>80d`
  column cannot be truncated exactly and is NOT read. No case counts, no other team's nowcasts, no truth after t.
- **Development**: model choices are made ONLY on forecast dates 2021-07-01..2021-10-10, scored against the triangle
  as it stood on 2021-11-21 (everything known before the declared period starts); at most 6 pre-listed
  configurations. The chosen configuration, its code and its sha256 are frozen in attempts/p1-nowcast/FROZEN.md
  before the first forecast of the declared period is made; the declared period is then run once and scored once.
- **Rows**: every (forecast_date, DE, age_group in {00-04, 80+}, horizon 0..-28) row for which the hub's
  data-processed MeanEnsemble file (as fetched) has all 7 quantiles; both predictors scored on exactly those rows.
- **Statistic**: pooled mean WIS ratio r = mean WIS(ours) / mean WIS(MeanEnsemble); relative difference r - 1.
- **Interval**: stationary bootstrap over forecast dates (Politis-Romano, mean block length 7 days, B = 10000,
  seed 20261113), 90% percentile interval of r - 1, resampling per-date pooled WIS sums of both predictors jointly.
- **p1 pass**: r - 1 <= -0.05 AND the 90% interval of r - 1 lies entirely below 0. Otherwise p1 is not met.
- **Fallback**: if the model cannot produce a quantile set for a row (for example too few complete reference
  dates), it emits the pre-declared fallback (all 7 quantiles = the as-of observed 7-day sum times the as-of point
  completion factor; if that is undefined, the as-of observed sum) and the report states how often it was used.
- **Descriptive only** (never used to decide): per-stratum values, the MedianEnsemble and the individual models on
  the same rows, scores against the 40-day truth, and the published-evaluation row subset.
- **Escape hatches**: (a) if the hub MeanEnsemble files differ from the assembly on any 00-04/80+ row, the hub file
  (data-processed) is the comparator; (b) if the model cannot be frozen before 05:55 UTC, p1 is not attempted on the
  declared period and the run reports the development results only.
