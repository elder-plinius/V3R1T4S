# Null test — PREREG.md section 6, made concrete in PREREG.v4 section 4

controls: 400
best_control: -0.005470
real: 0.224287
real_beats_all_controls: yes
command: $ENV/bin/python -I attempts/null-test/code/null_test.py 400 16

## What each control is

The frozen PotencyTransfer model, refitted on the official seed-42 LDO splits as saved by the drevalpy 1.3.5
pipeline, training on train+validation as the pipeline does for its final model, scored by normalized R^2
against the NaiveMeanEffectsPredictor trained on the same data. In each control the 545-drug universe is
randomly permuted (seed 1,000,000 + k), so every drug's Morgan fingerprint, target-pathway set and NCI-60
teacher value are those of a different drug, consistently in training and test. Responses, splits,
cell-line effects and all tuning are untouched; only the link between a drug and its own chemistry is broken.

## Result (from `attempts/null-test/output/null_summary.json`)

| | mean normalized R^2 over 10 splits |
|---|---:|
| real (unpermuted) | **+0.2243** |
| controls: mean / SD | -0.0266 / 0.0047 |
| controls: 5th / 50th / 95th percentile | -0.0339 / -0.0265 / -0.0194 |
| controls: best of 400 | -0.0055 |

The real value exceeds the best control by +0.2298, about 53 control standard deviations above the control
mean. The controls sit at the level of the mean-effects baseline, as they should if a drug's structure
carries no information once it is attached to the wrong drug.

## Disclosures

1. Controls were run with `attempts/potency-transfer/code/potency_core_fast.py`, verified equivalent to the
   frozen reference implementation: identical hyperparameter choices and predictions within 2e-7
   (`attempts/potency-transfer/output/fast_equivalence.txt`, `smoke_test_class.txt`). Running the full CLI
   400 times was not feasible; the unpermuted value from this harness (0.2243) is the cross-check.
2. This harness aligns predictions to the baseline row by row. drevalpy's own evaluation left-merges on
   (drug, cell line, split) and so double-counts CTRPv2's 4,118 duplicated pairs, giving 0.2249 for the same
   predictions. Real and controls here share one metric, so the comparison is internally consistent
   (`attempts/null-test/output/metric-note.txt`).
