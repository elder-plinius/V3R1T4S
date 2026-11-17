# PREREG.v6: the kit-format null test for p2 (frozen 2026-11-12T19:28:36Z)

Written while the frozen 1971 scan was 32 of 365 days in; the only 1971 number seen so far was a code test of
score_p2.py on those first 30 days (5 of 5 scanned events recovered, reversed-data rate 1.02/day). No threshold,
reading or design is changed by this file; it adds a null test in the kit's format (>= 400 controls).

- Statistic: R2-primary recall at the frozen theta (onset within +/- 300 s of a time, among times whose window was
  scanned), exactly as score_p2.py computes it for the catalogued 1971 A1 times.
- Controls: 400 shifted catalogues. Control k (k = 1..400) moves every catalogued 1971 A1 time by its own offset
  drawn uniformly from 1 to 10 days with a random sign (numpy default_rng seed 20261113 + k), then applies the same
  recall computation to the forward detections of the frozen scan. This measures how often the detector "recovers"
  a time that holds no catalogued A1 event (chance coincidence with false alarms and with other events).
- null_test.md: controls 400, best_control = the highest control recall, real = the 1971 recall,
  real_beats_all_controls = yes only if real > best_control. Command: attempts/evaluator-first/code/p2_null.py.
- The 200-draw chance recovery of PREREG.v2 / score_p2.py is still reported as pre-registered.
