# RSV forecast hub (HopkinsIDD archive, 2024-25): an as-of forecaster below the hub-ensemble's season-average WIS

## What
On route (a), 2024-25 season of HopkinsIDD/rsv-forecast-hub at commit 6bf251ac (unchanged live at 2026-11-13T02:13Z), the frozen as-of forecasts of V3R1T4S-asofKA (hub-format copies in attempts/forecaster/result/submission/) have season-average WIS 72.24 against the hub-ensemble's own files' 99.70 on the 3,065 hub-ensemble tasks that have truth in target-data/2026-06-05_rsvnet_hospitalization.csv (0-0.99, 1-4 and 5-64 as exact sums of its finer groups; the 695 65-130 tasks have no truth there and are unscored for both, our forecasts for 370 of them being all-zero placeholders), a relative difference of -27.6% with paired stationary-bootstrap 90% interval about [-36%, -20%] over the 14 reference dates, the whole gain coming from the 265 national (US) tasks while our state-level forecasts score worse than the ensemble's.

Bank target `rsv-hub-retrospective-beat-ensemble-wis`, route (a). The object is the set of 31 frozen quantile forecast
files in `object/forecasts/` (hub submission format, model id V3R1T4S-asofKA, origin dates 2024-10-13 .. 2025-05-11),
listed with their sha256 in `object/forecasts_sha256.txt`; in the run folder these are
attempts/forecaster/result/submission/, the scored files minus horizon -1 rows. This is a forecasting-method benchmark result, not
public-health guidance.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (Python 3 with pyarrow; fetches the 14 hub-ensemble files of 2024-25 plus the
empty 2024-12-01 file and the target-data file from the pinned hub commit, checks their sha256, recomputes both
season-average WIS and a stationary bootstrap). Expected last line: `PASS`. About 10-30 seconds on a laptop.
Rebuilding the forecasts from the hub's archive vintages (about 560 MB of public CSV) is in RUN_IT_YOURSELF.md.

## Compared to
| comparator | season-average WIS | scored tasks | source |
|---|---|---|---|
| hub-ensemble (HopkinsIDD/rsv-forecast-hub, model-output/hub-ensemble, 2024-25 files) | 99.7021 (recomputed; the hub publishes no scores) | 3,065 over 14 reference dates | https://github.com/HopkinsIDD/rsv-forecast-hub/tree/6bf251ac3fc798e55ed95d0b7269f5f5781c0207/model-output/hub-ensemble |
| this object, same tasks | 72.2386 | 3,065 | object/forecasts/ |
Relative difference -27.55%, stationary bootstrap (mean block 3 over reference dates) 90% interval [-35.78%, -19.84%].
Truth: target-data/2026-06-05_rsvnet_hospitalization.csv at the same commit, "inc hosp"; the submission groups 0-0.99,
1-4 and 5-64 are sums of the file's finer groups; 65-130 has no truth for 2024-25 and is unscored for both.
Snapshot details (fetch times, HTTP status, sha256): the-record-we-beat/RECORD.md.

## Not claimed
- Not a forecast of the 65-130 group: the hub's target file has no 65-130 truth for 2024-25, so those 695 ensemble tasks
  are unscored for both, and 370 of our 695 forecasts there are all-zero placeholders (six peak origins, 2024-12-08 ..
  2025-01-26; a fallback whose share came out zero). If 65-130 were scored with 65+ values from the hub's archive
  vintages, or with 0-130 minus the other groups from the final file, the margin disappears (rel about -1%, 90%
  interval about [-25%, +16%]). See DISCLOSURES.md items 9-11.
- Not better on state-level forecasts: on state tasks ours is worse than the ensemble (+18%; state 0-130 +9%, state
  pediatric +35%); the whole gain comes from the 265 national (US) tasks.
- Not public-health guidance; a retrospective benchmark on one completed season.
- Partial win p1 is NOT met: CEPH-Rtrend_rsv is slightly better than this object on its own tasks (106.09 vs 108.10).
- The result rests on scoring against the hub's current (revised) target data. Against the first-reported value of each
  week the order reverses (ours +26% worse); against the view four weeks later or at season end ours is 25-26% better.
- The gain comes from a backfill nowcast and the national series: US tasks -45%, state tasks +18% (ours worse).
- The same frozen pipeline does not beat the 2023-24 hub-ensemble when run as-of on 2023-24 (+18.6%): with no archive
  vintages before 2023-10-16 its revision correction has nothing to learn from.
- The WIS is a Python implementation of the scoringutils/hubverse formula (weigh = TRUE, median once), not the R
  package itself.
- Not a claim about the CDCgov hub (route b) or about any other season.

## Credits
- US RSV Forecast Hub, Johns Hopkins University Infectious Disease Dynamics Group: https://github.com/HopkinsIDD/rsv-forecast-hub
  (target data, archive vintages, hub-ensemble and every team's model-output); now continued by CDC's CFA at
  https://github.com/CDCgov/rsv-forecast-hub .
- Teams whose forecasts form the ensemble and the p1 comparison: CU-RSV_SVIRS (Columbia University), CEPH-Rtrend_rsv,
  JHU_CSSE-RSV, Metaculus-cp, UGA_flucast-INFLAenza (University of Georgia), UM-DeepOutbreak, PSI-PROF, hub-baseline
  (model-metadata/ in the hub).
- RSV-NET, CDC: https://data.cdc.gov/Public-Health-Surveillance/Weekly-Rates-of-Laboratory-Confirmed-RSV-Hospitali/29hc-w46k
- hubverse (hubEnsembles, hubEvals) https://hubverse.io and scoringutils (Bosse et al.) https://epiforecasts.io/scoringutils/ ;
  WIS: Bracher et al. 2021, PLoS Comput Biol 17:e1008618, https://doi.org/10.1371/journal.pcbi.1008618 .
- Stationary bootstrap: Politis and Romano 1994, JASA 89:1303-1313, https://doi.org/10.1080/01621459.1994.10476870 .
