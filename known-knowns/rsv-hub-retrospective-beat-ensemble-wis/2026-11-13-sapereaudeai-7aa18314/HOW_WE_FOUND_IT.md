# How we found it (contributor text, unverified)

Target: bank `rsv-hub-retrospective-beat-ensemble-wis`, route (a): the HopkinsIDD US RSV Forecast Hub archive, which
scores RSV-NET-derived weekly hospitalisation counts by state and age group. Neither hub publishes scores, so the
comparator is the hub-ensemble's own model-output, re-scored.

1. Evaluator first. A Python WIS (the scoringutils formula) was re-validated on this hub's 23 levels. The hub's current
   target file turned out to lack the submission age groups 0-0.99, 1-4 and 5-64 (they are exact sums of its finer
   groups) and to have no 65-130 rows for 2023-24 or 2024-25 (unscorable). The archive of dated target-data vintages has
   traps: a vintage labelled 2023-12-08 holds data to 2023-12-30, one labelled 2024-11-22 lacks North Carolina and is
   seven weeks stale for twelve states. The as-of rule (vintage dated on or before the origin, data ending at least
   8 days before it, latest data per location) was written down before any forecast was scored.
2. The lever. RSV-NET first reports are about 60% below the final values at lag 0 and still 10-20% low several weeks
   later; the hub asked teams to project the raw data. Our pipeline estimates lag-specific revision factors from the
   previous season's vintages (as seen in the current vintage) and corrects the latest weeks before forecasting.
3. The forecaster: kernel analogs on log rates per 100,000 (last three weekly changes, level against the 52-week maximum,
   week of year), pooled over series with analogs from other locations down-weighted, quantiles from the weighted analog
   outcomes, spread multiplier 0.75.
4. Development on 2023-24 only: 40 configurations, chosen by a statistic fixed in advance; frozen with hashes before any
   2024-25 forecast was scored; two availability fixes (a crash on stale 2016 rows, the defective 2024-11-22 vintage)
   were recorded as amendments before scoring. Scored once on 2024-25.
5. What failed: no revision correction (dev ratio 1.25 against the ensemble), a short-gap correction (1.16), a damped
   trend on top of the analogs (explodes on sparse series), longer shape windows and same-age weighting (no gain).
6. Caveats we found ourselves: the gain comes from the backfill nowcast and the national series (US tasks -45%, states
   +18%), and against first-reported values (rather than the hub's current target data) the result reverses (+26%).
   Partial win p1 is not met: CEPH-Rtrend_rsv is slightly better than us on its own tasks.
