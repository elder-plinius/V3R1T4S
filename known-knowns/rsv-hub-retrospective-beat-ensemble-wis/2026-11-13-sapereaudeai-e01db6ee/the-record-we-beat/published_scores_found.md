# Third-party scores for the CDCgov RSV hub's 2025-26 season that this claim was reconciled with or read

This file names the third-party score sets the work read, says what was read in each, and says which values were
reconciled with the object's code and data. It does not claim to be a complete list. Other sources may publish values
that overlap the object's cells, and the sources below may hold more than is described here.

The hub's own tree (e947ca8 and the live head 1985aee) has no score or evaluation file, and the hubverse hub list
(https://hubverse.io/community/hubs.html, fetched 2026-11-13T04:02:18Z, HTTP 200) shows no evaluation link for the RSV
Forecast Hub. Hub issues #294 and #515 and pull request #295 describe scoring for an internal CDC page.

## Reconciled (the object's code and hub files reproduce these published values)

1. arXiv 2605.16238 v2 (2026-10-14; https://arxiv.org/abs/2605.16238; abs page 2026-11-13T03:51:40Z HTTP 200, versions
   v1 and v2) and its analysis repository github.com/sarahmart/epi-hub-analysis at
   2294a6331e6317059b49b20da893a86b2f0751dd: data/processed/rsv/scores.parquet (26,248 row-level hosp WIS values, 7 hub
   directories, 22 reference dates 2026-01-03..2026-05-30, horizons -1..3, with truth_value) and
   data/season_summaries/rsv_summary.csv (the four Supplementary Table 6 hub rows at full precision; Table 6 prints
   Google_SAI-RSVEns 14.7, RSVHub-ensemble 16.4, CEPH-Rtrend_rsv 19.8, RSVHub-baseline 18.3 on 52 jurisdictions without US,
   horizons 0-3, 4,576 tasks each). Record: object/p3_reconcile_epi_hub_analysis.txt (their truth values; summary task
   set = 52 jurisdictions without US, horizons 0-3).
2. github.com/ACCIDDA/EpiBenchmark (main ddcc507e53027dbac5520396e5a9d9e7097cf355):
   src/epibench/challenges-library/epb_rsv_inchosp_2025-2026_dev/rsv25-26_complete-model-scores.parquet (git blob
   4300c200079d180548264b918c97572966508543, added in 1eacf63 on 2026-09-24): 11,648 row-level hosp scores of
   RSVHub-ensemble and RSVHub-baseline (28 reference dates 2025-11-22..2026-05-30, 52 locations, horizons 0-3, WIS on
   the 5 levels 0.025, 0.25, 0.5, 0.75, 0.975). Record: record/reconcile_epibenchmark.txt (truth = the hub's
   time-series.parquet as_of 2026-09-16).
3. github.com/ACCIDDA/tapestry (also served as github.com/ACCIDDA/chromantis), three files sets:
   a. branch restructure/unified-model, commit 6546e066ab6b5aec52fa2e1445c6d1623d054827,
      docs/legacy-v0/results/B2-screen/benchmark/leaderboard.csv: 20 RSVHub-ensemble aggregate rows for 2025-2026
      (hosp and ED x states+DC / US x horizon all/0/1/2/3). Records: record/reconcile_tapestry.txt and
      record/reconcile_tapestry_ed_rule.txt (truth as_of 2026-09-02; for ED, rows whose target_end_date is not
      reference_date + 7 x horizon left out; states+DC excludes US and Puerto Rico).
   b. same commit, docs/legacy-v0/workflows/hub-evaluation.md and docs/legacy-v0/results/B2-screen/benchmark/manifest.json:
      season WIS of RSVHub-ensemble and UGA_flucast-INFLAenza on their common ensemble-defined units, both targets:
      hosp 29.00743753 / 40.80432946 on 5,824 units, ED 0.00082381104 / 0.0009037065455 on 5,350 units. Record:
      record/reconcile_tapestry_hubeval.txt. The values reproduce with truth as_of 2026-09-02, horizons 0-3, rows whose
      target_end_date is not reference_date + 7 x horizon left out, and Puerto Rico (location 72) left out, as in
      tapestry's units. UGA_flucast-INFLAenza and RSVHub-ensemble share 5,936 hosp units at horizons 0-3, of which 112
      are in Puerto Rico; 5,824 is the count without them.
   c. main, commit 06508218a000e33d428d9180e25d9786767c1618, folder docs/experiments/google-comparison-20261005/ (all of
      its files: comparison.png, covid_covid_hosp_2025-2026-google-matched.parquet,
      flusight_flu_hosp_2025-2026-google-matched.parquet, native-location-scores.csv, per-seed.csv, provenance.json,
      results.md, rsv_rsv_hosp_2025-2026-google-matched.parquet, summary.csv, support.csv). For RSV it holds:
      Google_SAI-RSVEns's natural-scale pooled mean WIS 15.39366298787946 on 4,692 hosp tasks (51 states+DC, horizons
      0-3, 23 reference dates 2025-12-27..2026-05-30; per-seed.csv, together with log1p and log(x+0.5) pooled WIS and
      the group's own model's scores); per-location summed WIS of Google_SAI-RSVEns and RSVHub-ensemble on those tasks
      (native-location-scores.csv); the location-relative ratio 0.967110 against RSVHub-ensemble (results.md,
      summary.csv); the task support (support.csv); the truth vintage 2026-09-02 and the hub commit 53baf7db
      (provenance.json); and the matched row-level Google_SAI-RSVEns quantiles with the truth used (the RSV parquet).
      Record: record/reconcile_tapestry_google.txt (the pooled value and all 51 per-location sums for both models
      reproduce with truth as_of 2026-09-02 on the tasks both models have).
   d. tapestry also publishes RSVHub-ensemble 2025-26 scores as plots, read but not reconciled: commit 6546e066 (and
      pull/1 head cf1091e8), docs/legacy-v0/results/B2-screen/benchmark/plots/rsv_rsv_hosp_2025-2026/ and
      .../rsv_rsv_prop_ed_visits_2025-2026/, each with components-US.svg, components-states_dc.svg, fans-37.svg,
      fans-US.svg, relative-wis-US.svg, relative-wis-states_dc.svg, timeseries-US.svg and timeseries-states_dc.svg
      (by the titles in their SVG text: "Total WIS Components by Model", "Mean Relative WIS by Model and Horizon",
      "Mean WIS by Reference Date", with RSVHub-ensemble next to the group's variants; the fans plots show forecast
      fans); and docs/experiments/archive/Forward-2025/matched-hub-scores.csv on main (summed ensemble WIS next to one
      own model, on the same task sets as 3a).

## Read but not reconciled (relative or log-scale quantities)

4. arXiv 2605.16238 v2 Supplementary Table 7 (record/arxiv_supp_table7.txt): mean log WIS by horizon for 6 hub
   directories on the Table 6 task set; it is a summary of the row-level file in item 1.
5. Zenodo 10.5281/zenodo.22988800 (2026-09-27; timidity_zenodo_deposit_v7.zip, md5 f20da82557e7f38f9860df985d88ec1f;
   record/zenodo_22988800_scan.txt): RSVHub-ensemble WIS relative to RSVHub-baseline (natural and log scale) for RSV
   2025-26 hosp by horizon and phase; log-scale RMSE and Mincer-Zarnowitz slopes for six component directories.

## Other places looked at (2026-11-13), where no 2025-26 RSV hub score table was seen
github.com/CDCgov/cfa-forecast-hub-reports (weekly summaries), github.com/ACCIDDA/RespiLens (game scoring of single
scenarios), EpiBenchmark's docs site and its Zenodo record 21413793 (challenge data), arXiv 2608.05883 (COVID 2024/25),
medRxiv 2026.10.09.26364706 (Japanese influenza), several GitHub repositories found by search. The CDC RSV page
(https://www.cdc.gov/cfa-modeling-and-forecasting/rsv-data-vis/index.html) returned HTTP 403 and was not read.
