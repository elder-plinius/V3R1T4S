# Prospective Pre-Registration & Zero-Shot Holdout Protocol (`PREREG.md`)

- `target_id`: `openproblems-spatially-variable-genes-correlation`
- `dev_datasets_count`: `4`
- `blind_holdout_datasets_count`: `46`
- `wave1_method_frozen_utc`: `2026-11-16T19:15:00Z`
- `wave1_method_sha256`: `4503ac7a6e97aa6816353b486e8c87f7b64f5caeba32c6ae3f486eb6f44a7336`
- `wave1_zeroshot_evaluated_utc`: `2026-11-16T19:26:35Z`
- `wave2_eb_method_frozen_utc`: `2026-11-16T21:10:00Z`
- `wave2_eb_method_sha256`: `4c27e2538339e69f18061879d5418afd2a1ea1de14355b649860ae5cd097b05f`
- `wave2_zeroshot_evaluated_utc`: `2026-11-16T21:11:56Z`

## 1. Strict `4`-Dev / `46`-Holdout Split

Before touching the `46` holdout datasets, development and parameter selection were restricted exclusively to `4` datasets (`42_slide_tag_human_skin_melanoma`, `44_stereo_seq_Drosophila_embryo_E7`, `34_MERFISH_Human_cortex`, `01_10x_Visium_mouse_brain`). Neither `.var`, `.uns`, `.obs`, `.X` (`normalized`), gene names, nor column indices are ever read by `object/method.py` or `object/ams_svg_eb_v2.py` (enforced via AST check in `verify-it-yourself/verify.py`).

## 2. Single Zero-Shot Holdout Pass & Non-Regression Promotion Rule

1. **Wave 1 (`object/method.py`, `sha256: 4503ac7a6e97aa6816353b486e8c87f7b64f5caeba32c6ae3f486eb6f44a7336`):** Evaluated once across all `46` blind holdout datasets (`object/benchmark_50_datasets.json`), achieving `50 / 50` strict wins on matched `Zenodo 18193366` `.h5ad` inputs (`50`-dataset mean `0.945981`, `46`-holdout mean `0.953362`) and `50 / 50` datasets within `0.02` of `#1` across both `Zenodo 18193366` and `Seqera v1.0.0`.
2. **Wave 2 (`object/ams_svg_eb_v2.py`, `sha256: 4c27e2538339e69f18061879d5418afd2a1ea1de14355b649860ae5cd097b05f`):** Pre-registered promotion rule required matching `50 / 50` strict `Zenodo` wins with zero dataset regressions below `0.02` of `#1` while dominating all `5` capture-dropout stress regimes (`object/depth_paradox_benchmark.json`). In its single zero-shot `50`-dataset pass (`object/wave2_eb_v2_benchmark_50.json`), `ams_svg_eb_v2` won all `5` Depth-Paradox regimes and lifted `4 / 4` Dev datasets (`0.861095 -> 0.863571`), while scoring `49 / 50` strict `Zenodo` wins (`-0.019809` on `11_10x_Visium_Human_Cerebellum`, `1`-spot Purkinje/granular layer collinearity). Under the pre-holdout rule, `object/method.py` remains the default without post-holdout retuning, and `object/ams_svg_eb_v2.py` is archived alongside it.
