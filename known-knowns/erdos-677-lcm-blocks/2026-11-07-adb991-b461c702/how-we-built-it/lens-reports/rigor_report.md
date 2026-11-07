# report — rigor lens, run 2026-11-06-0918

claim level: progress

## Result
Judge steps 2 and 3 of the PREREG hold for k = 26..28. They were recomputed tonight after the PREREG, with code copied
unchanged from run 2026-10-29-0821.
- **Ratio set** (code/taskA_ratio_audit_k.py 400 26 28; out/taskA_ratio_audit_k26-28.txt): admissible_r(k) equals
  the Lemma-A set, |admissible_r| = 21262, 16402, 21262, "TOTAL missing over k=26..28: 0". All 290 equal-lcm pairs
  with n < m ≤ 400 have their ratio in the set.
- **Margin, interval arithmetic** (code/rig_margin.py 26 28 1000000 1 1000; out/rig_margin_k26-28.txt): "TOTAL
  pairs=58926 failures=0 undecided=0".
- **Margin, exact rational intervals** (code/rig_margin_exact.py, run per k; out/rig_margin_exact_k26.txt, _k27,
  _k28): "TOTAL pairs=21262 / 16402 / 21262 failures=0 undecided=0".

dead lines:
- **Running the exact margin as one process for 26..28:** about 1.5 h on one core. Split per k (about 30 min each),
  with identical arithmetic per ratio. The single-process form is superseded.
- **η smaller than 10^-3 for k ≥ 29:** not attempted. The ratio counts (114817 at k = 29, 30) make k ≥ 29 impractical
  for the enumeration anyway.
- **Kernel-checking the margin:** out of scope tonight. The checks are exact-rational programs, not Lean.
