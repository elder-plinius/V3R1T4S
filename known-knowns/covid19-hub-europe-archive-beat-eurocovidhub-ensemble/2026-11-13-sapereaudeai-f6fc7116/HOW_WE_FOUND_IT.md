# How we found it

contributor text, unverified

The bank target asks, as partial win p3, for an independent recomputation of the European COVID-19 Forecast Hub
archive's published scores.csv. The run had about 85 minutes, so it did p3 only.

1. Read the hub's evaluation code (code/evaluation/load_and_score_models.r) and EuroForecastHub's score_forecasts
   and add_status as text: scoringutils 1.x interval score with the dispersion / underprediction / overprediction
   split, 23 quantiles, point forecasts used as the median where the median is missing, status "final" only,
   anomalies removed, values rounded to integers.
2. Froze the readings in PREREG.md (per-model means of the four columns; the bank's 1% threshold; primary truth = the
   archive's ECDC truth files) before scoring anything.
3. Wrote the WIS in Python and checked it against an independent pinball form, a known positive and a known negative.
4. Fetched the 357 forecast files behind the published rows (one per model and forecast date; 8 had Sunday file
   dates, which the hub maps to the following Monday) and the truth files, from raw.githubusercontent.com.
5. A first pass on partial data matched almost every row; sharpness (which does not depend on truth) matched exactly
   for every model. The non-matching rows were nearly all Czech hospitalisations. The hub's data-truth README says
   hospitalisations are evaluated against OWID data; the archive's OWID file covers Czechia only, and scores.csv has
   hospitalisation rows for Czechia only. With that file every Czech hospitalisation row matched.
6. On the full data: 31,253 of 31,256 rows exact on all four rounded components, 3 half-integer rounding ties; under
   the pre-registered ECDC hospitalisation file, 7 models differ by more than 1% in under- or overprediction, all
   from the 531 Czech hospitalisation rows. The hub's row-selection rules, re-derived, keep exactly the published
   rows of the fetched files.

What did not explain anything: the truth vintage for cases and deaths (the final 2024-09-27 vintage is identical on
every published key) and the anomalies list (it removes nothing in this period). The 1/(K+1) WIS normalisation does
not reproduce the published values (its rounded wis equals the published wis on 13,252 of 31,256 rows), so the
match pins down the convention. Rows with negative horizons in the files (2,374 keys: -1, -2, -3 wk ahead) are not
hub targets and are not parsed.

This is a methods result on an archived benchmark. It is not public-health guidance.
