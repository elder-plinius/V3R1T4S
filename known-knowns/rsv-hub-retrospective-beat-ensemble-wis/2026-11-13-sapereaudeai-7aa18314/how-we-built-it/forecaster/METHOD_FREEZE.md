# METHOD_FREEZE (frozen 2026-11-13T01:49:32Z, from date -u), before any 2024-25 forecast is scored

Model id: V3R1T4S-asofKA (as-of kernel analogs with a backfill nowcast), route (a), HopkinsIDD RSV hub.

Pipeline: code/model_rsv.py + code/asof_rsv.py, parameters FROZEN_PARAMS.json, run by code/run_season.py for every
Sunday origin date of the 2024-25 round in hub-config/tasks.json (2024-10-13 .. 2025-05-11), horizons -1..5, all
locations in the as-of vintage x {0-130, 0-0.99, 1-4, 5-64, 65-130}, 23 quantiles.
- as-of rule: PREREG.v2 (vintage D <= O and its last week <= O - 8 days; latest data week wins).
- backfill nowcast: revision factors by age group and lag 0..10 = log(sum over locations and earlier vintages U of the
  data vintage's value / U's value) over usable vintages U whose last week is at least 26 weeks before the data
  vintage's last week and falls in October..April (season pulls). At the first test origin these are the 2023-24
  season vintages viewed from the 2024-10-25 vintage.
- kernel analogs: features d1..d3 and level-vs-52-week-max of log(rate per 100k + 0.1), bandwidth 0.5 (standardised),
  week-of-year kernel sd 3 weeks, analogs from other locations weighted 0.03, all age groups pooled (weight 1), history
  from 2016-08 on except 2020-06..2021-08, outcome weeks within the last 4 weeks never used, spread multiplier 0.75,
  nowcast spread multiplier 0.5, min ESS 30 (else equal weights).
- fallbacks (frozen): series with any history are forecast (short series such as NC get analogs from other
  locations); a group absent from the vintage gets the location's 0-130 quantiles x the US share of that group over
  the last 52 weeks (only 65-130 in some locations, which has no truth and is unscored).

Selection (PREREG development protocol): 40 configurations (work/dev/dev_results.jsonl; out/batch1-5.tsv, plus c01),
chosen by the pre-declared statistic (ratio of our mean WIS to the hub-ensemble's on the 2023-24 ensemble tasks,
horizons 0..4, real-time file where both exist). Chosen: h02_bw05m075w3, dev ratio 0.7951 (pediatric 0.795, 0-130
0.816, US 0-130 0.705, states 1.056; vs CU-RSV_SVIRS 0.695, CEPH-Rtrend_rsv 0.732, PSI-PROF 0.971,
UGA_flucast-INFLAenza 0.951). Re-run with the final code (fallbacks added) gives the same 0.7951 (h02_recheck_samecfg).

Disclosure (honest list of what this session saw before freezing):
- The dev statistic used a DEVELOPMENT-ONLY revision reference (the 2024-10-25 vintage as "near final" for the 2023-24
  season vintages), because no vintage before 2023-10-16 exists to estimate revisions as-of inside 2023-24. The frozen
  pipeline replaces it by the as-of rule above; at the first test origin its factors match the preview within 0.035 in
  log (printed table in the run log of this session; e.g. 0-130 lag 0: 0.430 preview vs 0.451 frozen rule).
- 2024-25 facts seen: task sets of every 2024-25 hub file (attempts/evaluator/task_sets.txt; no values), row counts
  of one frozen-config forecast for origin 2024-10-27 (no values), series history lengths in the 2024-10-25 vintage,
  and, while comparing the two archive file families, a few as-of input values of 2025-02-07/08 vintages (US weekly
  counts for 2025-01-11..01-25 as first reported). No 2024-25 truth from the final target file and no WIS of any
  2024-25 forecast (ours or the hub's) has been computed or looked at.
- Not used for selection: a check of long-term revisions (season totals of 2022-23 and 2023-24 across vintages and the
  final file), which showed the final file is 3-10% above the late-2024 view for 2023-24 totals; nothing was changed
  because of it.

Files frozen (sha256, also in freeze_hashes.txt):
f08ef86554749fdc88338dc989cbcd84f8f369d7efdf28c30f369d38978926b5 *code/model_rsv.py
fd12a197fdfc6877b2739b7414eb633733a4288e89f9d1488eb57a792e1698ff *code/asof_rsv.py
cf3c065782c256c9a483413f7bac3ff3b56895dedbf2bba5c166903731825465 *code/run_season.py
bf138af5c405544a0f37516dfeaeab6104d1c41ad52882d461a6e8328898dcf8 *FROZEN_PARAMS.json
6f4d7597135ff5f4744087a9c7d0e8ff8516a24ec94ecc52b396881440cf8c4d *../evaluator/code/score.py
c00fa4596e19c6ee041bc55fb6e8f9e86b0f426de385c91b0951befdb79c0306 *../evaluator/code/score_test.py
ffb8f12a518378c065853e841ae4cfd0c9d55b98c69c3a6d93af542360bc6f22 *../evaluator/code/wis.py
1502251a29dbb923d54334d66b544e23a2022ce2a1609d8dcd94c3c1eeca57e2 *../evaluator/code/parse_mo.py

Next (after this file exists): run code/run_season.py FROZEN_PARAMS.json result/forecasts 2024-25 once, then
../evaluator/code/score_test.py result/forecasts 2024-25 ../evaluator/test/2024-25 once.
