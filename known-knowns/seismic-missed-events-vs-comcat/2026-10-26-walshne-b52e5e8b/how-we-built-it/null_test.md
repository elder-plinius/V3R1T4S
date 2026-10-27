# null_test (run 2026-10-26-1727 PREREG.md L1 with PREREG.v2.md; the bank's circular-shift design, float64 detector)

controls: 600
best_control: 0.6121
real: 0.6705
real_beats_all_controls: yes
command: cd claim && python -I code/null_full.py fetch && python -I code/null_full.py prep && python -I code/null_full.py run 12 && python -I code/null_full.py summary

- **What ran:** the full pipeline (385 templates, 8 stations, 9 x MAD detection, +/-2 s declustering) on 600 whole-day
  controls. Stations 2-8 are circularly shifted by distinct whole minutes in [10, 1430] (>= 10 min apart).
  - 400 controls on 2024-12-10..12: best 0.6121 (13,888 declustered detections).
  - 200 controls on 2024-12-09: best 0.5351 (1,466).
- **Numerics:** float64 FFT numerator and direct per-window norms (PREREG.v2.md). The checker
  (attempts/detector-f64/checker_v2_out.txt) agrees with a direct Pearson computation to 2.5e-12.
- **Raw per-control maxima** (no threshold, no declustering): best 0.6121; none >= 0.6705
  (claim/data/null_per_control_max.csv).
- **Expected false count over the 3.0-day span:** 0 x 3.0 / 600 = 0 (95 % upper bound 0.015); pre-registered rule
  EFC < 0.05: met.
- **Changes from run 2026-10-24-0604:** the 12-09 values move from 0.5609 / 3,926 (float32 artefacts) to 0.5351 / 1,466. The best is
  0.5351 (unrounded 0.535149, 16:56:04.85, mid-day; run 13 REPRODUCE's exact recomputation: 0.5352, a rounding boundary). The 12-10..12 values and the event NCC are unchanged.
- **Early-hours sensitivity (PREREG.md L2, not the criterion's null):** 3,000 sample-shift controls in the first 2 h of
  the span: 1 control >= the event's 0.6706 (best 0.6887); EFC_early 0.012 < 0.05.
  attempts/early-null/result/early_summary.txt.
- **Output:** attempts/detector-f64/summary_out.txt and claim/data/null_summary.txt.
