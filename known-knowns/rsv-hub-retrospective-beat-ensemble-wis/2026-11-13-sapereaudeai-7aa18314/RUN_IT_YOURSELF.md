# Run it yourself (from this folder, fresh shell)

1. Check the claim (network, about 30 s): `sh verify-it-yourself/run_checks.sh`
   Expected output ends with:
   `season-average WIS ours 72.2386 hub-ensemble 99.7021 relative -0.2755`
   `stationary bootstrap (mean block 3, 4000 resamples) 90% interval [-0.3609, -0.2001]` (seeded; the run's own numpy
   bootstrap with 10,000 resamples gave [-0.3578, -0.1984])
   `PASS`
   Offline: `HUB=/path/to/a/checkout/of/rsv-forecast-hub/at/6bf251ac sh verify-it-yourself/run_checks.sh`.
2. Rebuild the object (Python 3.11, numpy 2.4.6, pandas 3.1.0, pyarrow 26.0.1; about 3 minutes, about 300 MB RAM):
   - lay the hub out as `data/hopkins/hub/` next to a folder `attempts/` with `attempts/forecaster/code/` =
     how-we-built-it/forecaster/*.py and `attempts/evaluator/code/` = how-we-built-it/evaluator/*.py (the scripts locate
     their inputs relative to that layout); copy how-we-built-it/forecaster/FROZEN_PARAMS.json to attempts/forecaster/;
   - fetch the inputs listed in how-we-built-it/inputs_vintages_pinned.tsv and inputs_modeloutput_pinned.tsv (path,
     size, git blob SHA) from https://raw.githubusercontent.com/HopkinsIDD/rsv-forecast-hub/6bf251ac3fc798e55ed95d0b7269f5f5781c0207/ followed by the listed path
     (how-we-built-it/evaluator/fetch_list.sh does it politely), plus hub-config/tasks.json saved as
     data/hopkins/hub-config_tasks.json;
   - `python attempts/forecaster/code/run_season.py attempts/forecaster/FROZEN_PARAMS.json out/fc 2024-25`
   - `python attempts/forecaster/code/make_submission.py out/fc out/submission` and compare sha256 with
     object/forecasts_sha256.txt (31 identical files).
3. Look-ahead audit: how-we-built-it/contrarian/lookahead_audit.py ORIGIN (an ISO date) reruns one origin against an archive cut to
   vintages dated on or before it (rows after origin - 8 days removed) and compares bytes (17/17 identical in the run).
