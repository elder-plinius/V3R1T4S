# European COVID-19 Forecast Hub archive: scores.csv reproduced (p3)

Target: `covid19-hub-europe-archive-beat-eurocovidhub-ensemble`, partial win p3. This is a scoring reproduction on
an archived forecasting benchmark: a methods result, not public-health guidance.

## What

An independent Python recomputation (no R, no scoringutils) of the wis, sharpness, underprediction and overprediction values of all 31,256 rows (15 models, forecast dates 2023-10-30 to 2024-09-16) of the European COVID-19 Forecast Hub archive's evaluation/scores.csv (sha256 c59afa8e3c9530e71d1c4c5445794bf6600b9ae3aaecec89db7e34def4aeb54c) from the archive's data-processed files and truth data shows that, with the pre-registered ECDC truth for all three targets, exactly 7 models (EuroCOVIDhub-baseline, EuroCOVIDhub-ensemble, Lydia-SARIMA, Lydia-simpleARIMA, epiforecasts-tsensemble, epiforecasts-weeklygrowth, fjordhest-ensemble) have a per-model mean component more than 1% from the published mean (largest 2.14%, Lydia-simpleARIMA underprediction), and that all of this excess comes from the 531 Czech inc hosp rows, which match exactly when scored against the archive's OWID hospitalisation file, under which all 15 models agree within 1% on all four components (max 3.2e-6) and the only 3 non-matching rows are exact half-integer values that half-to-even rounding sends to the published integers.

Rules needed to reconcile (each shown by output in how-we-built-it/outputs/): hospitalisation truth from the archive's
data-truth/OWID/truth_OWID-Incident Hospitalizations.csv, which covers Czechia only, so hospitalisations are scored
for Czechia only (with the ECDC hospitalisation file, 1,642 extra hospitalisation rows would be kept: 1,608 in 11
other countries and 34 Czech weeks with an ECDC value but no OWID value); case and death truth from
data-truth/ECDC/truth_ECDC-Incident {Cases, Deaths}.csv (identical to the final 2024-09-27 vintage on every published
key); horizons 1-4 only; status "final" only (222 rows dropped, status read as EuroForecastHub::add_status does);
the anomalies list removes nothing in this period; 8 epiforecasts-tsensemble files are dated the Sunday before the
forecast Monday. Re-derived, these rules keep exactly the 31,256 published rows of the 357 fetched files.

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (standard library only, a few seconds on a laptop). The full recomputation from the
public inputs (about 80 MB, numpy and pandas, a few minutes) is in RUN_IT_YOURSELF.md.

## Compared to

| table | cell | published | recomputed | fetched |
|---|---|---|---|---|
| [evaluation/scores.csv](https://raw.githubusercontent.com/european-modelling-hubs/covid19-forecast-hub-europe_archive/main/evaluation/scores.csv) (sha256 c59afa8e3c9530e71d1c4c5445794bf6600b9ae3aaecec89db7e34def4aeb54c) | per-model means of wis, sharpness, underprediction, overprediction, 15 models | e.g. EuroCOVIDhub-ensemble mean WIS 350.3998 (3,379 rows) | 350.3998 (OWID hospitalisation truth) | 2026-11-13T05:39:54Z, HTTP 200 |

All 15 models x 4 components x 2 truth modes are in object/p3_reproduction_table.csv; the published values are in
the-record-we-beat/record.md.

## Not claimed

- The bias column was not recomputed.
- Nothing about rows or files outside the 357 fetched files (one per published model and forecast date), or about
  any other version of scores.csv.
- The OWID hospitalisation file was not the pre-registered primary truth; it is the explanation of the >1%
  differences under the primary truth (how-we-built-it/PREREG.md).
- No claim that no one else has recomputed these scores; the panel's search found no earlier public one.
- Not public-health guidance; no statement about any epidemic.

## Credits

- The European COVID-19 Forecast Hub (ECDC-funded; Katharine Sherratt, Sebastian Funk, Nikos Bosse and colleagues):
  the archive, its truth data and scores.csv, https://github.com/european-modelling-hubs/covid19-forecast-hub-europe_archive
  ; the hub's evaluation paper, https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10238088/fullTextXML
- The forecasting teams whose submissions are in data-processed: ECDC (norrsken, soca_simplex), EuroCOVIDhub
  (ensemble, baseline), ICM, ISI, Lydia, PL_GRedlarski, epiforecasts, fjordhest.
- scoringutils (epiforecasts), https://github.com/epiforecasts/scoringutils, and EuroForecastHub,
  https://github.com/european-modelling-hubs/EuroForecastHub (read as text, not run).
- Bracher, Ray, Gneiting and Reich (2021), "Evaluating epidemic forecasts in an interval format", PLoS Comput Biol
  17:e1008618, for the WIS definition.
- ECDC and Our World in Data for the truth data.
