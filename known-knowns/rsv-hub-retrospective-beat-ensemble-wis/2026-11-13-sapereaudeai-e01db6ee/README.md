# RSV forecast hub (CDCgov, 2025-26): an independent per-model season-WIS recomputation, reconciled with third-party scores

## What
code/p3_recompute.py deterministically and byte-reproducibly (object/p3_table.csv sha256 e01db6ee9d55baf24c06fa801c2fdfee27d9c1f70d1d513b9e98b75bd6d2f804) recomputes, from the 247 in-season model-output files of github.com/CDCgov/rsv-forecast-hub at commit e947ca8fe8d50a581a181e6aefacfe922ba95af5 (reference dates 2025-09-20..2026-05-30, all unchanged at head 1985aee45bca6b655e22b8bc2096b515bd6327f2) and that commit's target-data/oracle-output.parquet, the per-model mean 23-level quantile WIS, MAE, 50%/95% coverage, shared-task comparisons with RSVHub-ensemble and pairwise relative WIS scaled to RSVHub-baseline of every model directory with 2025-26 quantile forecasts (8 for wk inc rsv hosp, 5 for wk inc rsv prop ed visits), with its data rules in object/p3_exclusions.txt and no hub score file to compare against, while the separate scripts code/p3_reconcile_k2.py and code_reconcile/ reproduce the named arXiv 2605.16238 v2 repository, EpiBenchmark and tapestry score sets to within 2e-12 absolute under the truth vintages and task rules the claim states, for the pinned oracle only and with p3's "released" clause met only once this package is published.

Bank target `rsv-hub-retrospective-beat-ensemble-wis`, partial win p3. The object is `object/p3_table.csv` (13 rows: 8
model directories for wk inc rsv hosp, 5 for wk inc rsv prop ed visits), with its data rules (`object/p3_exclusions.txt`)
and the Table 6 subset (`object/p3_era_subset.txt`). This is a scoring and reconciliation result for forecasting-methods
research, not public-health guidance and not a forecasting result.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (Python 3 with pandas and pyarrow). It fetches the 250 pinned hub files and the
third-party score files one GET at a time (or uses local copies via HUB, EXT, EXT2; see RUN_IT_YOURSELF.md), checks
every sha256, recomputes every row's season-average WIS and MAE from the definition and rescores the third-party values
listed below. Expected last line: `PASS`. The downloads are about 128 MB; from local copies the check took about 70 s
on the contributor's laptop (2026-11-13).

## Compared to
The hub's repository has no score file (status source https://github.com/CDCgov/rsv-forecast-hub/tree/main/model-output/RSVHub-ensemble,
fetched 2026-11-13T05:24:10Z, HTTP 200; the-record-we-beat/RECORD.md). The third-party score sets below were
reconciled; the list is not complete, and other sources may publish values that overlap the table.

| third-party scores | what was reconciled | rule and truth |
|---|---|---|
| arXiv 2605.16238 v2 analysis repository (github.com/sarahmart/epi-hub-analysis at 2294a63) | 26,248 row-level hosp WIS values, 7 directories | their truth values; within 1e-12 absolute |
| arXiv 2605.16238 v2 Supp. Table 6 (https://arxiv.org/abs/2605.16238) | 4 hub rows | pinned oracle: 14.635 / 16.422 / 19.804 / 18.306 vs 14.7 / 16.4 / 19.8 / 18.3 |
| github.com/ACCIDDA/EpiBenchmark rsv25-26_complete-model-scores.parquet (blob 4300c200) | 11,648 row-level hosp scores, RSVHub-ensemble and RSVHub-baseline, 5 levels | time-series as_of 2026-09-16; within 1e-12 |
| github.com/ACCIDDA/tapestry B2-screen leaderboard.csv (6546e06) | 20 RSVHub-ensemble aggregates, both targets | as_of 2026-09-02; ED date-consistent rows; states+DC without Puerto Rico; within 1e-12 relative |
| github.com/ACCIDDA/tapestry hub-evaluation.md / manifest.json (6546e06) | RSVHub-ensemble and UGA_flucast-INFLAenza on common units, both targets (4 values) | as_of 2026-09-02; horizons 0-3; date-consistent rows; Puerto Rico out; within 1e-12 relative |
| github.com/ACCIDDA/tapestry google-comparison per-seed.csv, native-location-scores.csv (06508218) | Google_SAI-RSVEns pooled WIS; per-location WIS of Google_SAI-RSVEns and RSVHub-ensemble | as_of 2026-09-02; states+DC; horizons 0-3; common tasks; within 2e-12 absolute (largest 1.82e-12 on a sum of about 9,077) |
Read but not reconciled: arXiv Supp. Table 7 (log WIS), tapestry's B2-screen RSV plots and the google-comparison
location-relative ratio, Zenodo 10.5281/zenodo.22988800 (ensemble relative to baseline). Details:
the-record-we-beat/published_scores_found.md.

## Not claimed
- Not a claim that these values are unpublished elsewhere, and not a complete list of published scores for the
  season; other sources (including those named) publish values that overlap the table (DISCLOSURES.md item 2).
- Not a forecasting result and not public-health guidance; no model ranking claim, no significance test.
- Not final truth: the table holds for the oracle-output at e947ca8 (= the 2026-11-12 vintage); 50 of 4,305 in-season
  truth rows changed between the 2026-11-04 and 2026-11-12 vintages (DISCLOSURES.md item 3).
- Not the hub's own scorer: a Python re-implementation of the scoringutils/hubverse WIS; R hubEvals was not run.
- Not a judgement on the two mis-dated 2025-09-27 ED files beyond documenting them and their effect (DISCLOSURES.md
  item 6).

## Credits
- RSV Forecast Hub, US CDC Center for Forecasting and Outbreak Analytics: https://github.com/CDCgov/rsv-forecast-hub
  (model-output, target data, RSVHub-ensemble, RSVHub-baseline); continues the US RSV Forecast Hub of the Johns Hopkins
  IDD group (https://github.com/HopkinsIDD/rsv-forecast-hub).
- The teams whose 2025-26 forecasts are scored: CEPH-Rtrend_rsv, CFA_Pyrenew (E, H, HE), Google_SAI-RSVEns,
  UGA_flucast-INFLAenza, UM-DeepOutbreak (model-metadata/ in the hub).
- NHSN hospital admissions and NSSP ED-visit data (CDC), as served in the hub's target-data.
- Martinson, Brenner, Plomecka, Williams, Reich, Shamsi, arXiv 2605.16238 (https://arxiv.org/abs/2605.16238) and its
  analysis repository https://github.com/sarahmart/epi-hub-analysis .
- ACCIDDA (Atlantic Coast Center for Infectious Disease Dynamics and Analytics): EpiBenchmark
  (https://github.com/ACCIDDA/EpiBenchmark) and tapestry (https://github.com/ACCIDDA/tapestry).
- Zenodo 10.5281/zenodo.22988800 (deposit "Code, derived tables and frozen rescaling factors for 'The CDC influenza
  forecast ensemble predicts changes that are too small'").
- hubverse (https://hubverse.io) and scoringutils (Bosse et al., https://epiforecasts.io/scoringutils/); WIS: Bracher
  et al. 2021, PLoS Comput Biol 17:e1008618, https://doi.org/10.1371/journal.pcbi.1008618 .
