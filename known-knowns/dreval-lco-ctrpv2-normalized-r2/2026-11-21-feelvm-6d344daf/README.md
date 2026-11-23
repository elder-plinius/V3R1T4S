# dreval-lco-ctrpv2-normalized-r2 — partial win p2 (CONFIRMED_PARTIAL)

## What

The bank criterion's enumerated partial win p2 is met by the single drevalpy run att_v1ens_v2 (EnsembleResidualOmics, drevalpy 1.6.0 pipeline, CTRPv2 / LN_IC50_curvecurator, test_mode=LCO, the package's own 10 CV splits, hyperparameters selected only on the package's validation partitions with tuning metric "Pearson" disclosed and frozen in PREREG.v5 before the scored run): scored under the report-era drevalpy v1.3.1 normalization — the ruler under which the same-splits RandomForest re-run reproduces the published best to 0.0005 and under which alone the published comparators are defined — its mean normalized Pearson 0.459961 and Spearman 0.443224 strictly beat the live-table best (RandomForest 0.434693/0.428291, max over all 15 models in the claimtime heatmap, unchanged from the bank's 2026-10-13 values) by +0.0253 and +0.0149 (both >= 0.01) and its mean normalized R^2 0.208691 clears the 0.175180 not-lose floor (+0.0235); nothing beyond this is confirmed — the headline R^2 win is not met (+0.0230 < 2xSE 0.0276) and no superiority under the pinned v1.6.0 ruler is claimed (0.3652 < 0.376 EnsembleMF on the live leaderboard, disclosed).

## Check it yourself

One command from this folder (python3 with nothing beyond the standard library; gzip/csv/hashlib):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Laptop time: ~1 minute.

The checker verifies object integrity (embedded sha256 manifest), recomputes all three
normalized metrics from the packaged per-split predictions plus the packaged v1.3.1-ruler
naive predictions (replicating the package's own replicate-merge semantics), and checks the
p2 margins and the honest near-miss on the headline R^2 win. Regenerating the CV splits from
the pinned data (byte-identical check against `object/SPLITS_MANIFEST.csv`) is optional and
described in RUN_IT_YOURSELF.md (needs `pip install drevalpy==1.6.0` and the dataset,
~30 min).

## Compared to

| metric (CTRPv2 LCO, report-era ruler, mean over 10 splits) | this claim | published best (live) | holder | margin |
|---|---|---|---|---|
| normalized Pearson | **0.459961** | 0.434693 | RandomForest | +0.0253 (>= 0.01) |
| normalized Spearman | **0.443224** | 0.428291 | RandomForest | +0.0149 (>= 0.01) |
| normalized R^2 | **0.208691** | 0.185180 | RandomForest | +0.0235 (floor: live best - 0.01) |

Table: https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LCO_normalized.html
(fetched 2026-11-21T10:56Z, HTTP 200, sha256 31a313febc02831bc4930304b76263ec66b28297619768382d9d9badf600ed68;
per-split source: Zenodo record 17343165, all_results.zip -> all_results/evaluation_results.csv).
Leaderboard constraint: https://raw.githubusercontent.com/daisybio/drevalpy/main/docs/_static/img/leaderboard_light.png
(fetched 2026-11-21T10:56Z, sha256 1b2313ee5de8e1fffb7e34ff0bc4724f49fca66c97c9b0cb71bb383c1684d563):
best normalized Pearson EnsembleMF 0.376 — 0.459961 >= 0.376.

## Not claimed

- The headline R^2 win (live max + 0.02 AND >= 2x across-split SE): the margin is +0.0230
  (>= 0.02 absolute) but 2xSE = 0.0276 (SE 0.0138 over 10 splits) — honestly not claimed.
- Any superiority under the pinned drevalpy 1.6.0's own (v1.6.0) ruler: the claim run scores
  normalized Pearson 0.365247 under it (below EnsembleMF's leaderboard 0.376) — the package's
  metric changed after the report (naive-predictor tissue fallback + split RNG), which is a
  documented reproducibility finding, not part of this claim.
- p1 (LTO) and p3 (reproducibility audit) are separate, unclaimed results.

## Credits

- drevalpy benchmark, pipeline, models and data: Bernett et al., Nature Communications 2026
  (https://github.com/daisybio/drevalpy, v1.6.0 pinned; data: Zenodo record 23159774;
  report: https://dilis-lab.github.io/drevalpy-report/).
- Published comparators: the report's own per-split table (Zenodo record 17343165,
  all_results/evaluation_results.csv) and the maintained DrEval Challenge Leaderboard.
- scikit-learn (RandomForest, Ridge, StandardScaler, PCA), numpy, pandas, scipy.
- The V3R1T4S bank entry dreval-lco-ctrpv2-normalized-r2 (elder-plinius/V3R1T4S) defined the
  success criterion quoted above.
