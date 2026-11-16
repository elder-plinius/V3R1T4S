# Skeptic 3 — Target Criterion, Pitfall & Digit-Parity Audit (`criterion.md`)

- `context`: `fresh independent skeptic review initialized from clean package directory and target specification`
- `target_id`: `openproblems-spatially-variable-genes-correlation`
- `target_spec_checked`: `known-unknowns/biology/openproblems-spatially-variable-genes-correlation.md`

## Audit Findings

1. **Zero Label Peeking & Feature-Order Immunity:** Static AST inspection in `verify-it-yourself/verify.py` verifies neither `object/method.py` nor `object/ams_svg_eb_v2.py` accesses `.var`, `.uns`, `.obs`, `.X`, `.layers`, or dataset-name literals (`feature_id` suffixes `_0.5` and 21-block feature ordering are never seen). On scrambled copies, `row_positions` scores near `0` (`|tau| < 0.12`), `true_ranking` scores `1.000000`, and `score_svg` reproduces unpermuted scores within `< 1e-12`.
2. **Exact Official Metric & NaN Pitfall Guards:** `eval_kendall` enforces one finite float64 score per input feature (`len == n_vars`) and raises an error if any reference gene's 21-level Kendall `tau-b` is `NaN` or undefined (preventing partial-output or constant-tie inflation). Missing method entries (`BOOST-GP`, `SpaGCN`, `SOMDE`, `Sepal`, `GPcounts`, `nnSVG`) are excluded rather than treated as `0` when computing per-dataset `#1` baselines, and `true_ranking` is excluded as a positive control.
3. **Cross-RNG Honesty & Programmatic Digit Parity:** Every table cell, runtime bound (`mean = 2.0778s`, `max = 7.9113s`; `< 5.0s` `max(10,000, N)`-normalized rate on `48 / 50` datasets and `12 / 12` panel datasets), CrossRef DOI, and SHA-256 digest in `README.md` and `INDEX.csv` was audited programmatically against `object/*.json`, including explicit disclosure of the single cross-RNG negative delta (`01_10x_Visium_mouse_brain`: `-0.007976` vs `Seqera` `nnsvg`) and `scDesign3` simulation scope.

pass: true
