# Baseline record (kit/RUN.md step 3c)

The bank's own gate for this target is the published scoreboard value, so that gate is this step
(`kit/RUN.md`: "Where the success criterion already sets a baseline gate, that gate is this step").

- **The gate**: PLMFit scoreboard, GB1 three-vs-rest = **0.8791** (ProGen2-medium, 764M parameters, adapters, 50%
  of layers, CLS pooling, linear head). Read live by this run at 2026-11-20T05:42:28Z, HTTP 200, page sha256
  `51b672d563c778ae40a435cad51424a5b8e0f82294211642d2bfff4983792f0b`, saved as
  `../data/status/plmfit_README_2026-11-20-0535_preclaim.md`, command output `../out/fetch1.txt`.
- **No baseline model was re-run by this run.** None of the published numbers for this split has released
  predictions that could be re-scored, and re-running a 764M-parameter language model is outside this run's scope
  and its machine budget. So, as `kit/RUN.md` step 3c requires to be said plainly: **no baseline was reproduced**,
  and the comparison rests on the released file's own `score` column scored with
  `scipy.stats.spearmanr` by `../code/boot_mean.py`, whose known-positive and known-negative test is in
  `../attempts/sealed-scoring/score_selftest.out`.
- **Same data, split and metric.** Both the bar and this run's numbers are Spearman on the 5,743 rows whose
  `three_vs_rest` value is `test` in `gb1_data_full.csv` (sha256 `93588112...a529de`). The counts were recounted
  by this run's own program: 2,691 `train` / 299 `validation` / 5,743 `test`. The scoring unit is the test row and
  the aggregation is a single Spearman over all test rows, which is how the scoreboard reports it.
- **Published comparison values** with their URLs: `related_work-carried.md`, carried unchanged from run
  2026-11-20-0215's own literature record. The highest for this split is 0.8995 +- 0.0058 (ProtEGNN(t6)). This
  run performed no literature search of its own; the NOVELTY panel skeptic does that.
