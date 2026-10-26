# PREREG.v2: vnncomp-2026-unsolved-instance-counterexample (run 2026-10-25-1500)

Written at 2026-10-25T15:34:52Z (date -u), before any attack output exists on the rows it adds. Everything in PREREG.md stays in force
(criterion, judge items 1-6, thresholds, null-test line, stop rules, clock); this file changes only the pool.

## Change

The 6 traffic_signs_recognition_2023 (2.0) eps-1 rows on 3_48_48 and 3_64_64 (properties model_48_idx_{1703,6371,178}
and model_64_idx_{1703,6371,178}, eps 1.00000) join tonight's pool, attacked by lens search-engineer with GPU searches
only. PREREG.md excluded them because the known method (CP-SAT) is CPU-bound and the CPU is hot; a GPU discrete search
does not need the CPU. Reason for the change: the live results table shows alpha-beta-CROWN falsifying five of the six
matching eps-3 rows in 3-6 s, so these nets are fragile one level up and the eps-1 rows have a real chance of being
satisfiable. Budget: at most 600 s of GPU per job, rows attacked until 2026-10-25T20:00Z. A candidate is judged by
PREREG.md's judge, unchanged.
