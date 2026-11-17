# report — rigor lens, run 2026-11-09-0917

claim level: progress

## Result
PREREG steps 1-3 hold for k = 29, recomputed after the PREREG with the 2026-11-06 claim's code (bytes unchanged)
plus one new wrapper.
- **Small X** (code/search677b.c, seed 20261109; out/search_N1.1e6.txt, out/verify_N1.1e6.txt): COMPLETE, K = 147,
  the k = 29 line has cand = 0; 2 candidates in all, 0 exact-equal.
- **Ratio set** (code/taskA_ratio_audit_k.py 400 29 29; out/taskA_ratio_audit_k29.txt): |admissible_r(29)| =
  114817 = the Lemma-A set, missing 0, extra 0; all 110 equal-lcm pairs with n < m <= 400 have their ratio in it.
- **Margin, interval arithmetic** (code/rig_margin.py; out/rig_margin_k29.txt): TOTAL pairs=114817 failures=0
  undecided=0, worst relative margin lower bound 0.99999994 (451 s).
- **Margin, exact rational intervals** (code/rig_margin_exact.py through the new code/shard_margin.py on 4 shards;
  out/rig_margin_exact_k29_shard0..3.txt): 28705 + 28704 + 28704 + 28704 = 114817 pairs, 0 failures, 0 undecided
  in every shard (3218-3230 s each).
- **The wrapper** (out/wrap_test_*): on k = 5..12, SHARD=0/1 reproduces the unsharded output exactly (times
  stripped) and three shards add up to the unsharded counts.

dead lines:
- **Running the exact margin as one process for k = 29:** about 3.6 h on one core at tonight's rate. Superseded by
  the 4-way split.
- **η below 10^-3 for k = 29:** not needed; the worst relative margin (0.99999994) leaves the same headroom as k <= 28.
- **Kernel-checking the margin:** out of scope; the checks are exact-rational programs, not Lean.
