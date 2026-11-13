# PREREG.v4 (as-of availability fix, written 2026-11-13T01:53:47Z, date -u; nothing of 2024-25 has been scored)

Found while checking coverage of the frozen 2024-25 run (files kept unscored in
attempts/forecaster/result/forecasts_v3_unscored/): the 2024-11-22 vintage, the PREREG.v2 data vintage for origin
2024-11-24, lacks North Carolina (37) entirely and stops at 2024-09-28 for all 12 other states (only US is current to
2024-11-16). With it our 2024-11-24 file has no NC rows, so it would not cover every task of the hub-ensemble's
2024-11-24 file (R6), and the states would be forecast from 7-week-old data.

Amended as-of rule (adds to PREREG.v2; the usability test is unchanged): the data vintage is chosen as in PREREG.v2,
but a location that is absent from it, or whose own last week there is earlier than in another usable vintage, is taken
from the usable vintage where that location's own last week is latest (ties: the later vintage in the PREREG.v2 order).
Every value read still comes from a vintage dated on or before the origin and ending at least 8 days before it.

Effect, checked before scoring: in 2024-25 only origin 2024-11-24 changes (12 states and NC from the 2024-11-15 vintage,
data to 2024-11-09; US from 2024-11-22). Every other 2024-25 file must stay byte-identical (checked after the rerun).
In the dev season only origin 2023-10-29 changes (one location from 2023-10-20); the selected configuration's dev
statistic is recomputed and reported (the runner-up is 0.0094 behind; if the change exceeds that, this is reported).
Code: attempts/forecaster/code/asof_rsv.py (sha256 in attempts/forecaster/freeze_hashes_v4.txt). Nothing else changes.
