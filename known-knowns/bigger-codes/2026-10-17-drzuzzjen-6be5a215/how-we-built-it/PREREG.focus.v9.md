# PREREG v9: method 3 (kick-regrow), batch 8 = the one further batch allowed by v8 (PREREG.md, v2-v8 unchanged)

frozen_utc: 2026-10-17T04:08:11Z
(frozen before any batch-8 kick or job; batch 7 ended 2026-10-17T04:06:21Z, all 11 jobs rc=0)

## Batch 7 result (measured; per-walk table in attempts/kick-regrow/calibration_b7.txt)
- RECOVERY (gate of v8): R=500 4/4 walks regrew to 5996 (5 s); R=1000 4/4 (15-19 s); R=2000 2/3 (252 s and 286 s;
  the third ended at 5995). All three R are calibrated; a recovery is not a finding.
- BASIN (first 5996 versus its source state): R=500 5977-5986 common words, R=1000 5954-5965 (both >= 5900: same
  basin by the v8 definition); R=2000: seed 711's first 5996 shares 5823 words with its source (< 5900: a different
  basin), seed 709's first 5996 was overwritten by its later 5997 (not measurable from the saved files).
- IMPROVEMENT: one walk, R=2000 seed 709: 5997 at 1146 s (frozen 03:25:33Z, both checkers valid, sha256
  6be5a215...ff524de8; shares 5789 words with its source and at most 5812 with any earlier 5996 start or final).
  Its three-skeptic panel started at batch end (claims/A26_6_9_5997).
- All 11 final and 11 best states valid under both checkers (04:07:19Z-04:07:51Z, logs/check_b7/).

## Batch 8 (60 min), by the v8 decision rule (some R regrew to 5996 in a different basin: R=2000 only)
- R = 2000 only (R=500 and R=1000 regrow into the same basin and are not continued).
- Starts: the 5997 code (6 kicks, seeds 801-806) and the 5 batch-7 final states of the R=1000 and R=2000 walks other
  than the 5997 walk (seeds 807-811: b7_kick_r1000_s705..s708 and b7_kick_r2000_s711 finals). Kick seed = walk seed.
- Engine, threads, time unchanged (2 threads, 3600 s, 11 jobs = 22 threads; the panel's single-thread checks fit
  under the cap).
- Statistic: per walk, recovery to the start size, best size, basin overlap with the source; improvement (> 5997) is
  frozen at once and paneled at batch end (immediately if >= 6001, i.e. +5 over the last confirmed 5996).
- After batch 8 the method stops unless batch 8 improves on 5997 (then one further batch, v10); this caps method 3
  at 3-4 batches inside the focused-stage cap (2026-10-18T08:54:30Z).
