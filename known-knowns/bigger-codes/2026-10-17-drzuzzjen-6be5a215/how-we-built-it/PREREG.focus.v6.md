# PREREG v6: focused stage on A(26,6,9), batch 5 (PREREG.md and v2-v5 unchanged)

frozen_utc: 2026-10-17T01:02:26Z
(frozen before batch 5 is launched; batch 4 ended 2026-10-17T01:01:31Z, all 11 jobs rc=0)

## Batch 4 result (measured)
11 plateau walks x 2 threads from the three 5996 codes (s306 x4, s307 x4, s308 x3), seeds 401-411, 3600 s each:
every walk ended at 5996 (no *_best.json written; logs "done best=5996"), 2451-2480 rounds each.
Gain in batch 4: 0. This is the FIRST batch without gain; by the PREREG.md rule the stage continues, and two
consecutive batches without gain stop or change the method.
Final states (*_cur.npy): all 11 are valid 5996 codes under both workspace checkers (01:01:52Z-01:02:07Z,
logs/cur_check_b4/), pairwise distinct, each 161-213 words away from its start (5783-5835 common words).

## Batch 5 (60 min) decision
- Lens and engine unchanged (plateau-walk, lb_lns_gen.py, default neighbourhood, 2 threads, 3600 s).
- Starts: the 11 batch-4 final states (seeds/cur_b4/*.npy), one walk each, new seeds 501-511. Reason (from measured
  data, not a new method): in batch 3 one gain came at 3506 s of 3600 s, and the batch-4 walks ended on plateaus far
  from their starts; continuing them tests whether 60-min walks are simply too short (an effective 120-min walk).
- 11 jobs x 2 threads = 22 threads. Freezing and panel cadence unchanged; last confirmed value 5996 (reproduced by the
  Mac 2026-10-17T00:28:21Z).
- Stop rule: if batch 5 also gives no gain, this cell's plateau-walk search stops (two consecutive batches without
  gain); the plateau (sizes, rounds, neighbourhood) is then reported as the negative result, and any further method
  for this cell needs its own preregistration.
