# PREREG.v2 (amendment before any score; written 2026-11-13T02:43:30Z by date -u)

Nothing has been scored (no dev score, no 2025-26 forecast). While smoke-testing one DEV forecast (R = 2025-01-11,
output looked at, not scored) the US NHSN series in the 2025-01-08 vintage showed that RSV admission reporting before
the CMS reporting requirement of 2024-11-01 is not comparable: US weekly counts were 0-315 through 2023-24 and
2024-10-05 (6), then 156, 296, 480, 970 (week ending 2024-11-02), 2571 (2024-11-09), 3396, ... 15173 (2025-01-04).
The Oct-Nov 2024 rise is a reporting ramp, not epidemic growth, and would enter the analog library as fake growth.

Change (mechanical adaptation of route (a)'s own history-exclusion parameters `excl` (COVID period) and `min_hist`
(first usable week), which route (a) froze for its data): for route (b) min_hist = 2024-11-09 (the first full epiweek
after the 2024-11-01 requirement) and excl = none; analog anchor and outcome weeks before min_hist are never used,
exactly as route (a)'s code treats weeks before its min_hist. Everything else in PREREG.md stands.
Dev configuration D7 is redefined (it was "t0 = 26", which is now void because min_hist binds): D7 = D0 with
min_hist = 2023-10-07 (no regime exclusion, the literal copy), to show the effect on dev. The freeze rule is unchanged
(D0 unless another configuration is >= 3% better on dev mean WIS).
