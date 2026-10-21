# PREREG v5: focused stage on A(26,6,9), batch 4 (PREREG.md, v2, v3, v4 unchanged)

frozen_utc: 2026-10-17T00:01:26Z
(frozen before batch 4 is launched; batch 3 ended 2026-10-17T00:00:14Z, all 11 jobs rc=0)

## Batch 3 result (measured, from attempts/plateau-walk/output/b3_*.log and *_best.json)
11 plateau walks x 2 threads (22 threads), seeds 301-311, 3600 s each.
| start | seeds | bests |
|---|---|---|
| 5995 s202 | 301-304 | 5995, 5995, 5995, 5995 |
| 5995 s209 | 305-308 | 5995, 5996 (s306, 1489 s), 5996 (s307, 1800 s), 5996 (s308, 3506 s) |
| 5995 s207 | 309-311 | 5995, 5995, 5995 |
Gain in batch 3: +1 (5995 -> 5996), all from the s209 start. Three DISTINCT 5996 codes (pairwise common words
5782-5802), frozen and valid under both checkers (23:25:52Z, 23:43:37Z, 00:00:45Z; logs/freeze/b3_*_5996.json).
8 of 11 walks gained nothing. Rounds per walk 2413-2470. Gains per batch so far: +2, +2, +1.

## Batch 4 (60 min) decision, by the PREREG.md rule (a batch with gain continues)
- Lens: plateau-walk only (unchanged engine and neighbourhood).
- 11 jobs x 2 numba threads = 22 threads. Starts: the three 5996 codes (s306: 4 walks, s307: 4, s308: 3), seeds 401-411.
- Freezing, panel cadence and stop rule unchanged. Last confirmed value for the jump rule: 5995 (the 5996 panel runs
  during this batch).
