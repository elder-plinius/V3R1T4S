# Baseline record (kit/RUN.md step 3c)

No published score exists for either RSV hub (scout.md: no scores file in HopkinsIDD/rsv-forecast-hub or
CDCgov/rsv-forecast-hub; the HopkinsIDD dashboard's Evaluation tab is commented out). So there is no published value to
reproduce; PREREG.md says so. What this folder records instead:

1. Dev season 2023-24, every model and the hub-ensemble recomputed by our scorer (before any forecast of ours existed):
   command (from the run folder): python attempts/evaluator/code/baseline_dev.py 2023-24
   output: baseline_dev_2023-24.txt (pinball and interval WIS forms agree to 1.8e-12; RETRO hub-ensemble files equal
   the exact mean of the RETRO members' quantiles on all 7,800 tasks, max abs diff 0).
2. Test season 2024-25, every model and the hub-ensemble (computed after METHOD_FREEZE.md):
   command: python attempts/evaluator/code/baseline_dev.py 2024-25 ; output: hub_season_wis_2024-25.txt
   hub-ensemble season-average WIS 99.702 on 3,065 scored tasks (14 reference dates) - the comparator of the claim.
Metric as the hub/bank define it: scoringutils/hubverse quantile WIS (weigh = TRUE, median once), 23 levels,
season average = mean over scored tasks. Data: hub commit 6bf251ac3fc798e55ed95d0b7269f5f5781c0207, truth
target-data/2026-06-05_rsvnet_hospitalization.csv (0-0.99, 1-4, 5-64 as sums of its finer groups; 65-130 has no truth).
Expected score: none published. Tolerance: the two WIS forms within 1e-9 (met). The same wis.py reproduced the FluSight
hub's published scoringutils table for 58 models to two decimals in an earlier V3R1T4S run (dossier
flusight-retrospective-beat-ensemble-wis, run 2026-11-12-1832), which is our evidence that it equals the hubverse WIS.
