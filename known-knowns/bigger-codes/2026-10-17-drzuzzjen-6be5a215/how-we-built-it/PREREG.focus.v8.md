# PREREG v8: method 3 (kick-regrow), batch 7 = calibration of larger kicks (PREREG.md, v2-v7 unchanged)

frozen_utc: 2026-10-17T03:05:52Z
(frozen before any batch-7 kick or job; batch 6 ended 2026-10-17T03:04:27Z, all 11 jobs rc=0)

## Batch 6 result (measured; table in attempts/kick-regrow/calibration_b6.txt)
- Gate of v7: every R in {25, 50, 100, 200} is CALIBRATED (each walk regrew to 5996). This only enables those R; a
  recovery is not a finding. No walk exceeded 5996 (improvement: none).
- Basin: every walk regained 5996 within 24-26 s, and that first 5996 code shares 5986-5996 of its 5996 words with
  its source state; 190-200 of the R removed words (95-100 %) came back. Two walks (R=25 seed 601, R=50 seed 604)
  returned to EXACTLY their source state (same sha256 as logs/cur_check_b5). The rest of each hour was ordinary
  plateau drift (final states share 5791-5834 words with the source, as in the plateau-walk lens). All 11 final and
  11 best states are valid under both checkers (03:05:00Z-03:05:32Z, logs/check_b6/).
- Reading: kicks of up to 200 random words do not leave the 5996 basin; with these R, method 3 is a plateau walk.

## Batch 7 (60 min) design: calibration of larger kicks, same gate
- Starts: the 11 batch-6 final states (valid, distinct 5996 codes), one kick each (tools/kick.py, kick seed = walk seed):
  R = 500 for starts 1-4 (seeds 701-704), R = 1000 for starts 5-8 (705-708), R = 2000 for starts 9-11 (709-711).
- Engine, threads, time unchanged (lb_lns_gen.py default neighbourhood, 2 threads, 3600 s): 22 threads.
- Gate (decided now): an R is calibrated if at least one of its walks regrows to >= 5996 within 60 min. Informative
  measure reported for every walk: common words of its first 5996 (if any) and of its final state with its source,
  and the number of removed words back. Improvement (> 5996) is reported separately and frozen/paneled as before.
- Decision rule: if no R in {500, 1000, 2000} regrows to 5996, method 3 is dead (small kicks stay in the basin, large
  kicks lose too much) and the focused stage on A(26,6,9) closes with the negative result. If some R regrows to 5996
  in a DIFFERENT basin (first 5996 sharing < 5900 words with the source), one further 60-min batch with those R is
  allowed (v9). If it regrows only into the same basin, method 3 is closed as well.

Correction appended 2026-10-17T03:06:11Z, before any batch-7 job is run (wording only, no decision changed): '190-200 of the R removed words' should read: of the R removed words, 95-100 % came back (24-25 of 25, 48-50 of 50, 95-97 of 100, 190-195 of 200).
