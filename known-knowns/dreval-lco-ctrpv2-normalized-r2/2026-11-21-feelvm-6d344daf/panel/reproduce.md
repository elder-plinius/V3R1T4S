# REPRODUCE skeptic verdict — dreval-lco-ctrpv2-normalized-r2 (partial win p2)

context: subagent (fresh session). Scope: only `claim/` was read; all work done in
`panel_work_reproduce/`; nothing in `claim/` was modified.

## Definition (quoted, and implemented from scratch BEFORE reading claim/code/recompute_normalized.py)

> "loads each split's prediction CSV (EnsembleResidualOmics), merges the v1.3.1-ruler naive
> predictions (naive_v131/predictions_split_i.csv, column naive_pred) on (cell_line_name,
> pubchem_id), subtracts the naive prediction from both true and predicted responses, and
> computes per-split R^2, Pearson, Spearman; then the mean and SE over the 10 splits. Handle
> duplicate (cell_line_name, pubchem_id) replicate keys the way pandas' left-merge from the
> model rows does (the package's own semantics)."

> Naive ruler: "overall_mean + cell_line_effect + drug_effect fitted on that split's
> train+validation rows ONLY ... with unseen test cell lines contributing zero cell-line
> effect."

My checker implements exactly this: pandas `how="left"` merge of the naive rows onto the
model rows on (cell_line_name, pubchem_id) (replicate keys multiply per pandas join
semantics), y_true_norm = response - naive_pred, y_pred_norm = predictions - naive_pred,
sklearn `r2_score`, scipy `pearsonr`, scipy `spearmanr` per split; mean and SE
(std ddof=1 / sqrt(10)) over the 10 splits. Metrics chosen independently of the author's
code (author used manual corrcoef/SSE formulas — values agree to float noise).

## What I ran (exact commands)

```
mkdir -p runs/2026-11-21-0140/panel_work_reproduce runs/2026-11-21-0140/panel
<venv>/python.exe -I panel_work_reproduce/my_checker.py run1.json
<venv>/python.exe -I panel_work_reproduce/my_checker.py run2.json
diff run1.json run2.json                                  # byte-identical
# plus exploration scripts (explore.py, explore2.py, decode_heatmap4.py) and inline python -I heredocs
```

Checker source: `panel_work_reproduce/my_checker.py` (own implementation, definition quoted
in its docstring). Outputs: `panel_work_reproduce/run1.json`, `run2.json`.

## What I found (numbers)

### 1. Claimed means and per-split values (v1.3.1 ruler) — CONFIRMED

- mean normalized R^2 = 0.208691 (claim 0.2087, diff 9e-6); SE = 0.013799 (claim 0.0138,
  diff 1.2e-6; ddof=1/sqrt(10)).
- mean normalized Pearson = 0.459961 (claim 0.4600, diff 3.9e-5).
- mean normalized Spearman = 0.443224 (claim 0.4432, diff 2.4e-5).
- All 30 per-split values in CLAIM.md reproduced; max abs diff 5.0e-5 (i.e. exact to the
  quoted 4 decimals). Example: split 0 R2 0.271933 / Pearson 0.527627 / Spearman 0.499934.

### 2. Naive ruler definition — CONFIRMED exactly

- Recomputed naive = overall_mean(train+val) + (cl_mean - overall if cl in fit else 0) +
  (drug_mean - overall if drug in fit else 0) from `splits/cv_split_i_train.csv` +
  `cv_split_i_validation.csv` matches the saved `naive_v131/predictions_split_i.csv`
  column naive_pred to max abs diff 8.9e-16 (float epsilon) on ALL 10 splits.
- Test cell lines never appear in train or validation of the same split (0 common cell
  lines, all 10 splits; 88-89 test cell lines per split, all unseen -> zero cell-line
  effect, as the definition says). 0 unseen test drugs (545 fit drugs).
- naive_v131 keys == test keys exactly; response columns identical (diff 0).

### 3. Merge semantics is genuinely the package's own — CONFIRMED

The pandas left-merge multiplies replicate keys (test sets contain 258 duplicate
(cell_line, drug) keys with identical response/prediction/naive values; 6 test cell lines
per split lack omics and are absent from the model files). My merge-based recomputation of
the v1.6.0-ruler normalized columns (subtracting the pipeline's own
`NaiveMeanEffectsPredictor/predictions/` predictions) reproduces drevalpy's own
`evaluation_results.csv` "R^2: normalized"/"Pearson: normalized"/"Spearman: normalized"
to <= 6e-17 on ALL 10 splits (requirement was >= 3); a no-multiplication dedup variant
diverges by up to 1.2e-2, proving the merge weighting is what the package uses. Raw
(unnormalized) R^2/Pearson/Spearman recomputed on the model files' own rows also match
`evaluation_results.csv` exactly. CLAIM.md's "splits 7/8/9 normR2 0.123118/0.151534/0.153417
identical in both" verified verbatim.

### 4. Margins — CONFIRMED

- Pearson: 0.459961 - 0.434693 (decoded from saved live heatmap, RandomForest) = +0.025268
  >= 0.01 (claim +0.0253 vs 0.4347). PASS.
- Spearman: 0.443224 - 0.428291 = +0.014933 >= 0.01 (claim +0.0149). PASS.
- R^2 floor: 0.208691 >= 0.1752 (= 0.1852 - 0.01). PASS.
- Near-miss honest: R^2 margin vs RF re-run 0.1857 = +0.022991 >= 0.02, but 2xSE = 0.027598
  > 0.022991 -> headline R^2 win correctly NOT claimed (claim: 0.0230 vs 0.0276). Verified.

### 5. Determinism — CONFIRMED

- My checker run twice: `run1.json` and `run2.json` byte-identical (diff empty).
- Pipeline's own evaluation reproduced independently at float-epsilon (above).

### 6. Live-table artifacts saved in claim/ — CONFIRMED (with one caveat)

- sha256(heatmap_algorithms_LCO_normalized.claimtime.html) =
  31a313febc02831bc4930304b76263ec66b28297619768382d9d9badf600ed68 (matches CLAIM.md prefix).
  Decoded Plotly bdata (float64): RandomForest normalized R^2 = 0.185180 = max of 15 models;
  RandomForest Pearson 0.434693, Spearman 0.428291 — exactly the published bar CLAIM.md uses.
- sha256(leaderboard_light.claimtime.png) = 1b2313ee5de8e1fffb7e34ff0bc4724f49fca66c97c9b0cb71bb383c1684d563
  (matches CLAIM.md prefix). PNG shows best normalized Pearson EnsembleMF 0.376, 34 models;
  0.4600 >= 0.376 leaderboard constraint satisfied. (CLAIM.md says 34 models — matches the
  PNG; claim/REPRODUCE.md step 7 says "33 models", a trivial typo in REPRODUCE.md, not in
  the claim numbers.)
- Caveat: "byte-identical to the 01:44Z fetch" is not verifiable from claim/ alone (only the
  claimtime copies are saved).

### 7. BASELINE.md RF row — internally consistent; NOT verifiable from claim alone

- RF artifacts (`results/rf_lco_baseline/...`, `results/rf_v131repro/...` under `../dreval_run/`)
  are NOT inside claim/; also `report_evaluation_results.csv`, which BASELINE.md says was
  "copied here", is absent from claim/. Per instruction this is marked "not verifiable from
  claim alone" rather than failed.
- Internal consistency verified: CLAIM.md RF row (0.1857 / 0.4329 / 0.4276, SE 0.0122)
  equals BASELINE.md Track A v1.3.1-ruler numbers; deltas vs published 0.1852/0.4347/0.4283
  = 0.0005/0.0018/0.0007 (arithmetic correct; gate 0.0005 << 0.02 correct). The published
  per-split list in BASELINE.md averages to 0.185180 with std 0.048029 (as stated), and the
  published-bar values themselves are independently confirmed from the saved heatmap bdata.

### Missing/absent objects (noted, none break verification)

- `report_evaluation_results.csv` described in BASELINE.md as "copied here" is not in claim/.
  The values it would substantiate (published 0.185180/0.434693/0.428291) are independently
  confirmed from the saved heatmap HTML.
- RF prediction/baseline run outputs are outside claim/ (explicitly anticipated by the
  panel instruction for item 6).
- All objects required for items 1-5 (10 prediction CSVs, 10 naive_v131 CSVs, 10 pipeline
  naive CSVs, all split CSVs, evaluation_results.csv) are present and complete.

## Conclusion

Every property checked — claimed means, all 30 per-split values, the naive-ruler definition
recomputed from raw splits, disjointness of test cell lines, the merge/duplicate semantics
(proven to be the package's own via exact reproduction of drevalpy's evaluation on all 10
splits), the margins, the honest near-miss, determinism, and the saved live-table artifacts —
reproduces exactly. The only unverifiable-from-claim items (RF re-run artifacts, the 01:44Z
fetch identity) are anticipated by the panel instruction and marked as such, and the claim's
RF row is internally consistent.

pass: true
