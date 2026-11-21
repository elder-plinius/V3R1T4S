# The record we beat

## Table 1: DrEval report heatmap (CTRPv2 LCO normalized R^2 / Pearson / Spearman)

- URL: https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LCO_normalized.html
- UTC fetch time: 2026-11-21T10:56:00Z (and an identical earlier fetch at 2026-11-21T01:44:00Z, same sha256)
- HTTP status: 200
- sha256: 31a313febc02831bc4930304b76263ec66b28297619768382d9d9badf600ed68
- Extracted cells (Plotly bdata float64 decode, 15 models): max normalized R^2 = RandomForest
  0.185180; max normalized Pearson = RandomForest 0.434693; max normalized Spearman =
  RandomForest 0.428291. Corroborated by the report's own per-split table (Zenodo record
  17343165, all_results.zip -> all_results/evaluation_results.csv): RandomForest mean over
  CV_split 0..9 = 0.185180 / 0.434693 / 0.428291.

## Table 2: maintained DrEval Challenge Leaderboard

- URL: https://raw.githubusercontent.com/daisybio/drevalpy/main/docs/_static/img/leaderboard_light.png
- UTC fetch time: 2026-11-21T10:56:00Z
- HTTP status: 200
- sha256: 1b2313ee5de8e1fffb7e34ff0bc4724f49fca66c97c9b0cb71bb383c1684d563
- Extracted cell: best normalized Pearson = EnsembleMF 0.376 (34 models).
