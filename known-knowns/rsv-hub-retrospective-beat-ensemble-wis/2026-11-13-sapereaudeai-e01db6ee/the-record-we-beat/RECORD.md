# The record (snapshot record; pages are not copied)

There is no record value to beat for p3: it asks for an independent recomputation and for the discrepancies with the
hub's own published scores, and the hub's repository has no score file. This file records the status source, the
pinned inputs and the third-party scores the object was reconciled with or that were read.

Bank status source: https://github.com/CDCgov/rsv-forecast-hub/tree/main/model-output/RSVHub-ensemble
- fetched 2026-11-13T05:24:10Z (run 2026-11-13-0523), HTTP 200, 266809 bytes, page sha256
  c6b703d616958268f2a722f8076877d8f5e48d20e2e9c03db8584113112fe205: main currentOid
  1985aee45bca6b655e22b8bc2096b515bd6327f2, 36 RSVHub-ensemble files, no scores file.
- fetched 2026-11-13T03:51:34Z (run 2026-11-13-0349), HTTP 200, one curl with a V3R1T4S User-Agent, 266808 bytes, page
  sha256 99950339e0c1344012f5f880cc17cfce4bd1b300a593af5c250b1c4c721552e9: main currentOid
  1985aee45bca6b655e22b8bc2096b515bd6327f2, 36 RSVHub-ensemble files (29 for 2025-26), no scores file.
- earlier fetch (run 2026-11-13-0233): 2026-11-13T02:34:25Z, HTTP 200, sha256
  8413d6a2a4859761e8110ede51c58ae25dd1e149542efa036dfbfba308ecf699 (main was e947ca8 then).
Hub pinned: e947ca8fe8d50a581a181e6aefacfe922ba95af5 (git ls-remote 2026-11-13T02:34:34Z). Live head at
2026-11-13T03:51:58Z: 1985aee45bca6b655e22b8bc2096b515bd6327f2, whose only change against e947ca8 is one added 2026-27
file (model-output/UM-DeepOutbreak/2026-11-14-UM-DeepOutbreak.csv); every input of the object is unchanged at the live
head, and no score/evaluation path exists in either tree.
Inputs: verify-it-yourself/pinned_inputs.txt (sha256 of the 247 model-output files, oracle-output.parquet,
time-series.parquet, tasks.json), fetched from raw.githubusercontent.com at the pinned commit, HTTP 200 each.

Third-party scores this work reconciled or read (not a complete list; details: published_scores_found.md):
- arXiv 2605.16238 v2 (abs page re-fetched 2026-11-13T03:51:40Z, HTTP 200, sha256
  ecb6dccab0300a7313fe7c3cae702314b5a2a57284a2e3b7cbbabe4b15e990e6; versions v1, v2), Supplementary Table 6: mean WIS
  Google_SAI-RSVEns 14.7, RSVHub-ensemble 16.4, CEPH-Rtrend_rsv 19.8, RSVHub-baseline 18.3 (hosp; 52 jurisdictions
  without US; horizons 0-3; 2026-01-03..2026-05-30; 4,576 tasks each).
- github.com/sarahmart/epi-hub-analysis at 2294a6331e6317059b49b20da893a86b2f0751dd (main, re-checked 03:52:23Z):
  data/processed/rsv/scores.parquet (26,248 hosp rows, sha256 5ae0994bd13633dfd3e5b4043ff6ede340316580423be0a34492fc3ba6be43bb)
  and data/season_summaries/rsv_summary.csv (sha256 119341ae044de382a97302e0313722d4fefecd06573cd40e6ca50f352abd1798).
- github.com/ACCIDDA/EpiBenchmark (main ddcc507e53027dbac5520396e5a9d9e7097cf355), file
  src/epibench/challenges-library/epb_rsv_inchosp_2025-2026_dev/rsv25-26_complete-model-scores.parquet (added in
  1eacf63, 2026-09-24), fetched 2026-11-13T03:52:53Z, HTTP 200, sha256
  0b444178c715db9c2bdb35e0433a1fb79a208aff5838e0fbf0ea4c8c1f01a610: RSVHub-ensemble and RSVHub-baseline, hosp,
  5-level WIS, means 26.688404 and 32.291779 over 5,824 rows each.
- github.com/ACCIDDA/tapestry, branch restructure/unified-model at 6546e066ab6b5aec52fa2e1445c6d1623d054827, file
  docs/legacy-v0/results/B2-screen/benchmark/leaderboard.csv, fetched 2026-11-13T03:59:54Z, HTTP 200, sha256
  22e4699bef320ab09a0e420ae907e75e8ece7221df1a120912019492c81e9c88: 20 RSVHub-ensemble 2025-2026 rows (e.g. hosp
  states_dc all: n 5916, wis 16.01423091; ED states_dc all: n 5475, wis 0.000818615898); on the same commit,
  docs/legacy-v0/workflows/hub-evaluation.md (sha256 17fa1c626531f14f5130bae7f1d68ab1e6d594ba89387424dc52e363d6886d3a)
  and docs/legacy-v0/results/B2-screen/benchmark/manifest.json (sha256
  d854dcf97ae2b353b5edad5da9485ccea268412ca956394b000a079570a9bc8b), read from a shallow git fetch at
  2026-11-13T04:37:04Z: RSVHub-ensemble and UGA_flucast-INFLAenza on their common units, hosp 29.00743753 / 40.80432946
  (5,824 units), ED 0.00082381104 / 0.0009037065455 (5,350 units).
- tapestry docs/experiments/google-comparison-20261005/ at 06508218 (per-seed.csv sha256
  eb8cc88ee108ecebf48958fb06fc8709619c4280bb4f6c7ab2e3558244a31de9, native-location-scores.csv sha256
  63d2e29ac64d9b192752c4bdc94497346c377c4f85bd7e6c40ed23f8c99a1a89, fetched 2026-11-13T05:24:28Z..05:24:33Z, HTTP 200):
  Google_SAI-RSVEns pooled WIS 15.39366298787946 on 4,692 hosp tasks and per-location WIS of Google_SAI-RSVEns and
  RSVHub-ensemble (reconciled); results.md (location-relative ratio 0.967110).
- Not reconciled (relative or log-scale quantities): arXiv 2605.16238 v2 Supplementary Table 7 (mean log WIS by
  horizon, 6 hub directories);
  Zenodo 10.5281/zenodo.22988800 (timidity_zenodo_deposit_v7.zip fetched 2026-11-13T04:44:38Z, HTTP 200, sha256
  4dc26f49fa4c1daf1e956c90603f5a5193dd4f31f33753a814a47c466f58f344; RSVHub-ensemble WIS relative to RSVHub-baseline).
Reconciliation results: object/p3_reconcile_epi_hub_analysis.txt and how-we-built-it/records/reconcile_*.txt
(how-we-built-it/records/: epibenchmark, tapestry, tapestry_ed_rule, tapestry_hubeval, tapestry_google).
