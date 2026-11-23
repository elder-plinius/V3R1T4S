Sat Nov 21 07:06:46 UTC 2026

# PREREG v4 — dreval-lco-ctrpv2-normalized-r2

Timestamp: 2026-11-21T07:07Z (see date line above), BEFORE any Track A attacker split beyond 3
was scored. Thresholds unchanged from PREREG.md/.v2/.v3.

## Protocol FINALIZATION (supersedes PREREG.v3's Track B-primary decision)

RF reproduction evidence (all from command output, 10 Track A RF splits complete):
- Track A = drevalpy v1.6.0's OWN split generation (default_rng(42), the pinned package's own
  protocol; splits verified sha256-identical across run dirs).
- Track A RF evaluated under the v1.3.1 ruler: mean normR2 0.1857 (SE 0.0122) vs published
  0.1852 (delta 0.0005); Pearson 0.4329 vs 0.4347; Spearman 0.4276 vs 0.4283.
- The published baseline REPRODUCES on the pinned package's own splits once the report's
  (v1.3.1) ruler is applied. No split reconstruction is needed.

FROZEN PRIMARY PROTOCOL:
- Splits: drevalpy v1.6.0's own LCO generation (Track A result dirs).
- Ruler: v1.3.1 NaiveMeanEffectsPredictor semantics (code/compute_naive_preds_v131.py),
  applied to both baseline and attacker; the v1.6.0-ruler values are co-reported.
- Baseline gate: PASSED (0.1857 vs 0.1852, within +-0.02) -- recorded, not retuned.
- Win evaluation: attacker mean normR2 (v1.3.1 ruler, 10 splits) >= max(0.1852 published, our
  RF 0.1857) + 0.02 AND >= 2x SE(10); Pearson >= 0.4247 AND >= live leaderboard max;
  p2 = Pearson >= 0.4447 AND Spearman >= 0.4383 AND normR2 >= 0.175180.
- Track B (v1.3.1-semantics reconstructed splits) continues as a second-partition robustness
  track; Track B RF gate unchanged (its 10-split mean vs 0.1852).

null_test: not needed because (unchanged) explicit benchmark score vs live table value.
