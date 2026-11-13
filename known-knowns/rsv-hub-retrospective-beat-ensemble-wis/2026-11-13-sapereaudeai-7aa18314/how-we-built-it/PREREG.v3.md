# PREREG.v3 (crash fix under escape hatch E3, written 2026-11-13T01:50:48Z, date -u)

The frozen pipeline (METHOD_FREEZE.md, 2026-11-13T01:49:32Z) crashed on the first 2024-25 origin (2024-10-13) before
writing any file: the 2024-10-11 vintage carries 65-130 rows that stop in 2016 for 8 locations, and a series whose last
week is years old asks the analog step for a 400-week-ahead outcome (no training rows; numpy vstack error;
attempts/forecaster/out/run_season_2024-25.log). No 2024-25 output existed and nothing had been scored.

Fix (one line in code/model_rsv.py): a series whose last observed week is more than 8 weeks before the vintage's last
week is treated as absent, so the frozen missing-group fallback covers it. For every vintage where no series is stale
(all 2023-24 dev vintages: the dev run had no crash and the same code path) outputs are unchanged, so the dev
selection stands. New sha256 of code/model_rsv.py is recorded in attempts/forecaster/freeze_hashes_v3.txt; all other
frozen files and parameters are unchanged. Nothing else changes.
