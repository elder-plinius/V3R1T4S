# PREREG v4: focused stage on A(26,6,9), batch 3 (PREREG.md, v2, v3 unchanged)

frozen_utc: 2026-10-16T22:59:55Z
(frozen before batch 3 is launched; batch 2 ended 2026-10-16T22:59:27Z, all 12 jobs rc=0)

## Batch 2 result (measured, from attempts/plateau-walk/output/b2_*.log and *_best.json)
12 plateau walks x 2 threads, 4 from each 5993 code (s101, s102, s104), seeds 201-212, 3600 s each.
| start | seeds | bests |
|---|---|---|
| 5993 s101 | 201-204 | 5993, 5995 (s202, at 2006 s), 5994 (s203), 5993 |
| 5993 s102 | 205-208 | 5993, 5993, 5995 (s207, at 3448 s), 5993 |
| 5993 s104 | 209-212 | 5995 (s209, at 2375 s), 5994 (s210), 5993, 5994 (s212, at 171 s) |
Gain in batch 2: +2 (5993 -> 5995). Three DISTINCT 5995 codes (pairwise common words 5688-5827), frozen and valid
under both checkers (22:33:24Z, 22:43:34Z, 22:58:32Z; logs/freeze/b2_*_5995.json). 6 of 12 walks gained nothing.
Rounds per walk in 3600 s: 2332-2407 (batch 1, 8 concurrent jobs: about 2620 for 2-thread walks), so 12 concurrent
jobs cost about 10 % rounds per walk; total rounds per batch still rose (about 28,300 vs about 13,000 for the plateau lens).

## Batch 3 (60 min) decision, by the PREREG.md rule (a batch with gain continues)
- Lens: plateau-walk only (unchanged engine and neighbourhood).
- 11 jobs x 2 numba threads = 22 threads, so that freezes, checks and the 5995 panel fit under the 24-thread cap
  (deviation of batch 2 recorded). Starts: the three 5995 codes (s202: 4 walks, s209: 4, s207: 3), seeds 301-311.
- Freezing, panel cadence and stop rule unchanged (PREREG.md, v2). Last confirmed value for the jump rule: 5993.

Correction appended 2026-10-16T23:00:07Z, before batch 3 is launched (measurement arithmetic only, no decision changed): total plateau-lens rounds were 28,261 in batch 2 (sum of 12 logs) and 14,839 in batch 1 (sum of 5 logs), not 'about 13,000'.
