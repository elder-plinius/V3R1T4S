# PREREG v3: focused stage on A(26,6,9), batch 2 (PREREG.md and PREREG.v2.md unchanged)

frozen_utc: 2026-10-16T21:59:04Z
(frozen before batch 2 is launched; batch 1 ended 2026-10-16T21:54:37Z, all 8 jobs rc=0)

## Batch 1 result (measured, from attempts/*/output/b1_*.log and *_best.json)
| job | lens | threads | start | best | time to best (s) | rounds in 3600 s |
|---|---|---|---|---|---|---|
| b1_scale_t2_s101 | plateau | 2 | 5991 s21 | 5993 | 2218 | 2624 |
| b1_scale_t4_s102 | plateau | 4 | 5991 s21 | 5993 | 837 | 3245 |
| b1_scale_t8_s103 | plateau | 8 | 5991 s21 | 5992 | 2896 | 3734 |
| b1_plateau_s22_s104 | plateau | 2 | 5991 s22 | 5993 | 1152 | 2606 |
| b1_plateau_s22_s107 | plateau | 2 | 5991 s22 | 5992 | 576 | 2630 |
| b1_deep_s21_s105 | deep | 2 | 5991 s21 | 5991 | - | 462 |
| b1_deep_s22_s106 | deep | 2 | 5991 s22 | 5991 | - | 462 |
| b1_deep_s21_s108 | deep | 2 | 5991 s21 | 5991 | - | 465 |
Gain in batch 1: +2 (5991 -> 5993), plateau lens only. Three DISTINCT 5993 codes (pairwise common words 5732-5797),
frozen and valid under both checkers at 21:58Z (logs/freeze/b1_*.json; sha256 2205ae3a..., 1656e108..., a583fe37...).
Deep lens: 0 improving moves in about 460 rounds per job (each round about 8 s versus about 1.4 s for plateau).
Thread scaling: 8 threads gave 1.42x the rounds of 2 threads (3734 vs 2624); per thread, 2-thread jobs are about 2.8x
more efficient. No sign that more threads per walk reach a better value.

## Batch 2 (60 min) decision, by the PREREG.md rule (a batch with gain continues)
- Lens: plateau-walk only (lb_lns_gen.py, unchanged, default neighbourhood). The deep lens is stopped for this cell:
  its batch-1 result (no gain from either start, at equal threads and time) is reported as a negative measurement.
- 12 jobs x 2 numba threads = 24 threads (cap). Starts: the three distinct 5993 codes, 4 jobs each, seeds 201-212.
- Statistic and freezing as in PREREG.md / v2: each gain frozen and two-checker validated at once; panel, gate and
  package on the best code at batch end (immediately on a jump of >= 5 over 5993).
- Stop rule unchanged: stop or change method after two consecutive batches with no gain.
