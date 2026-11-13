# Baseline record (kit/RUN.md step 3c)

The published baseline is the hub's own evaluation/scores.csv (sha256
c59afa8e3c9530e71d1c4c5445794bf6600b9ae3aaecec89db7e34def4aeb54c, fetched 2026-11-13T05:39:54Z, HTTP 200),
written by code/evaluation/score_models.r with scoringutils via EuroForecastHub::score_forecasts.
Expected: the published per-model means of wis, sharpness, underprediction, overprediction; tolerance 1% (bank).
Command: python -I -B code/p3_reproduce.py data check_out owidhosp (and ... primary).
Data: archive main branch raw files as fetched 2026-11-13 (sha256 in reference_outputs/fetch_log_all.tsv).
Metric: per-row WIS with 23 quantiles (Bracher, median at half weight), rounded to integers per row, then the mean
over each model's published rows.

Result (p3_per_model_vs_published.csv, sha256 f6fc71163c4247914cb1f832649ed956887aabef08de4bc353e1904e2662f8e0):
- truth_mode owidhosp: 15/15 models within 1% on all four components, max |relative difference| 3.199e-06;
  31,253 of 31,256 rows exact on all four rounded components (3 half-integer rounding ties).
- truth_mode primary (ECDC hospitalisation file): 7/15 models over 1% (max 0.02136, Lydia-simpleARIMA
  underprediction), all from 531 inc hosp CZ rows; 30,722 rows exact.
The EuroCOVIDhub-ensemble's published mean WIS 350.4 is reproduced as 350.4 (owidhosp; 3379 rows).
