context: subagent (Claude Code Agent tool, fresh context)

# REPRODUCE skeptic: covid19-hub-europe-archive-beat-eurocovidhub-ensemble, partial win p3

Claim under test (claim/CLAIM.md): an independent Python recomputation of all 31,256 rows of the archive's
evaluation/scores.csv from data-processed and the truth files reproduces the published rounded wis, sharpness,
underprediction and overprediction (31,253 rows exact, 3 rounding ties) with OWID hospitalisation truth, so all 15
per-model means are within 1%; with the ECDC hospitalisation file 7 models differ by more than 1%, all from 531 Czech
hospitalisation rows.

## Definition I implemented (written before reading the author's code)

Bracher, Ray, Gneiting and Reich (2021), weighted interval score for a forecast F with median m and K central
prediction intervals [l_k, u_k] at levels 1 - alpha_k:

    WIS(F, y) = 1/(K + 1/2) * ( w_0 * |y - m| + sum_{k=1..K} w_k * IS_{alpha_k}(F, y) ),  w_0 = 1/2, w_k = alpha_k / 2
    IS_alpha(F, y) = (u - l) + (2/alpha) * (l - y) * 1(y < l) + (2/alpha) * (y - u) * 1(y > u)

so w_k * IS_k = alpha_k/2 * (u_k - l_k) [dispersion, "sharpness"] + (l_k - y)+ [overprediction] + (y - u_k)+
[underprediction], and the median term 1/2|y - m| splits into 1/2 (m - y)+ [overprediction] and 1/2 (y - m)+
[underprediction]; each component is divided by K + 1/2. With the hub's 23 quantiles, K = 11 intervals
(0.01/0.99, 0.025/0.975, 0.05/0.95, 0.1/0.9, ..., 0.45/0.55; alpha_k = 2 * lower quantile). I wrote it as a weighted
mean over the components present (median weight 1/2, interval weight 1), so a median-only forecast scores |y - m|.
Row handling taken from the hub's own R code in claim/data/docs/ (read as text): forecast_date = ceiling_date(file date,
"week", week_start = 2) - 1; point forecasts become the 0.5 quantile when no 0.5 quantile is given; quantiles
filtered to the 23 hub levels; rows without truth dropped; status from EuroForecastHub::add_status (OWID file for
hosp, cases file for both cases and deaths, missing = final) must be "final"; anomaly anti-join and post-anomaly
filter; wis/sharpness/underprediction/overprediction rounded with R's round(), i.e. IEC 60559 half to even. For
near-ties (|fractional part - 0.5| < 1e-6) I recomputed exactly in rational arithmetic from the decimal strings in the
files. Code: panel/work_reproduce/my_wis_check.py (sha256 742ce7a2...) and panel/work_reproduce/extra_checks.py;
output panel/work_reproduce/my_check_log.txt. No R, no scoringutils, no code from claim/code/ used.

## What I verified with my own checker (numbers from my output)

OWID hospitalisation truth (claim's reconciling rule):
- published rows 31,256; rows with no forecast file 0; duplicate quantile entries 0; n_quantiles equal on 31,256.
- float64 + half-even rounding: 31,253 rows equal on all four rounded components; the 3 others are exactly the rows
  the claim names: EuroCOVIDhub-ensemble BG 2024-02-19 h2 sharpness (float 35.49999999999999, exact 71/2),
  epiforecasts-EpiNow2 LU 2024-05-20 h2 sharpness (float 2.5000000000000004, exact 5/2), EuroCOVIDhub-baseline NL
  2023-12-11 h4 wis (float 4504.500000000001, exact 9009/2). In exact arithmetic all three are exact half-integers and
  R's half-to-even rounding gives the published 36, 2 and 4504, so with exact arithmetic 31,256 of 31,256 rows match
  on all four components (stronger than claimed).
- ae_median equal on 31,256 rows; cov_95 and cov_50 equal on 31,255 rows, the remaining row being the point-only
  forecast where the published value is NA (no intervals).
- per-model means (15 models): 0 models over 1%; max |relative difference| of rounded recomputed means 0 with exact
  ties; with float rounding the one-unit tie shifts give 3.20e-6 (EpiNow2 sharpness), 1.88e-6, 3.55e-7, matching the
  claimed 3.2e-6.
- the point-only row (EuroCOVIDhub-ensemble, inc case, BG, 2023-12-18, h1) scores |y - m| = 13 = published.

ECDC hospitalisation truth (prereg primary):
- float rounding: 30,722 rows exact on all four (claim: 30,722); 531 non-matching rows beyond the 3 ties, all
  inc hosp CZ (claim: 531 of 534).
- 7 models over 1%, same models and values as claimed: EuroCOVIDhub-baseline under -1.511%; EuroCOVIDhub-ensemble
  under -1.120%, over +1.075%; Lydia-SARIMA under -1.909%; Lydia-simpleARIMA under -2.136%, over +1.129%;
  epiforecasts-tsensemble over +1.153%; epiforecasts-weeklygrowth over +1.922%; fjordhest-ensemble under -1.724%.
  Max 2.14%. Max mean-WIS shift 0.492% (fjordhest-ensemble), consistent with "no model's mean WIS moves by more than
  0.5%".

Why (truth vintages, published keys): 1,862 distinct truth keys (1,049 case, 776 death, 37 hosp, all hosp keys CZ);
ECDC vs final 2024-09-27 vintage: cases 1,049 compared 0 differ, deaths 776 compared 0 differ; ECDC vs OWID hosp: 37
compared, 36 differ. Confirmed.

Row selection, re-derived from every row of the 357 fetched files: 357 files, one per published (model,
forecast_date); 8 epiforecasts-tsensemble files are Sunday-dated, mapped by the hub's ceiling_date rule (my mapping,
not data/file_map.tsv). OWID mode: kept 31,256 = published (0 kept-not-published, 0 published-not-kept); drops:
horizon 0 keys 5,382, no truth 9,284, status not final 222, anomaly 0, after anomaly 0. ECDC-hosp mode: kept 32,898,
1,642 extra, all inc hosp. Confirmed.

Contrast 13,252: with the 1/(K+1) form (median at full weight) the rounded WIS equals the published wis on 13,252 of
31,256 rows (OWID truth), confirmed; on all four components it matches only 9,005 rows. The half-weight form matching
31,256 and the 1/(K+1) form not matching is strong evidence the definition is the one the hub used.

## Author's REPRODUCE.md steps (outputs written only under panel/work_reproduce/check_out/)

1. code/wis_selftest.py: last line `SELFTEST PASS`; output identical to reference_outputs/wis_selftest.txt.
2. code/p3_reproduce.py owidhosp: first line `truth: owidhosp | published rows: 31256 | covered: 31256 | rows exact on
   all 4 (rounded): 31253 | missing files: 0`, last line `models over 1% (or <95% rows covered): []`; log identical
   to reference_outputs/p3_log_owidhosp.txt; per_model_owidhosp.csv and per_model_target_owidhosp.csv byte-identical.
3. primary: `rows exact on all 4 (rounded): 30722`, 7 models; log identical to reference_outputs/p3_log_primary.txt;
   per_model_primary.csv and per_model_target_primary.csv byte-identical.
4. code/rederive_exclusions.py: `kept AND published: 31256`, `kept but NOT published: 0`, `published but NOT kept: 0`;
   byte-identical to reference_outputs/rederive_owidhosp.txt.
5. code/vintage_diff.py: byte-identical to reference_outputs/vintage_diff.txt.
Determinism: the author's outputs from my fresh run are byte-identical to the saved references; my own checker gave
identical summary numbers on four runs.

## Provenance spot check (5 files, one plain request each, 5 s apart, User-Agent V3R1T4S-panel-reproduce, all HTTP 200)

- evaluation/scores.csv: c59afa8e...54c = data/scores.csv = the sha256 stated in REPRODUCE.md (note: scores.csv has
  no row in reference_outputs/fetch_log_all.tsv).
- data-truth/OWID/truth_OWID-Incident Hospitalizations.csv: 6e225033...fcca = fetch log = local file.
- data-truth/ECDC/truth_ECDC-Incident Hospitalizations.csv: bbdcc1f7...88b = fetch log = local file.
- data-truth/ECDC/truth_ECDC-Incident Cases.csv: 762d81fa...be7 = fetch log = local file.
- data-processed/EuroCOVIDhub-ensemble/2024-02-19-EuroCOVIDhub-ensemble.csv: 6462185e...bc = fetch log = local file.

## Not verified / issues found (none changes a claimed number)

- Hub's actual scoringutils version and R floating-point path not checked (no R allowed); equivalence shown only
  empirically (31,256 of 31,256 rows).
- Wording, CLAIM.md rule 1: "1,642 extra hospitalisation rows (other countries)" is not exact: 34 of the 1,642 are
  CZ (CZ weeks with ECDC hosp truth but no OWID truth); 1,608 are other countries (12 locations in all). Should be
  corrected before filing.
- Wording, CLAIM.md rule 4: besides the 5,382 horizon-0 keys, the fetched files have 2,374 negative-horizon keys
  (-1: 1,383, -2: 754, -3: 237) that code/p3_reproduce.py drops silently (regex `^(\d+) wk ahead`); they are not
  hub targets and do not change the kept set, but the claim should mention them.
- Wording, CLAIM.md rule 5: "matches only 13,252 of 31,256 rounded rows" is a wis-only count (the log says so); on
  all four components it is 9,005.
- scores.csv is missing from reference_outputs/fetch_log_all.tsv (its hash is only in REPRODUCE.md); re-fetch matched.
- Whether using the non-preregistered OWID truth to explain the >1% differences satisfies p3 is for the criterion
  skeptic; the numbers under both truth choices reproduce.

pass: true
