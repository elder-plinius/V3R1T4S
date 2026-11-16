# Skeptic 2 — Literature, Upstream Repository & Leaderboard Audit (`novelty.md`)

- `context`: `fresh independent skeptic review initialized from clean package directory and live upstream repositories`
- `target_id`: `openproblems-spatially-variable-genes-correlation`
- `sources_checked`: `openproblems.bio v1.0.0, openproblems-bio/results, Zenodo 18193366, openproblems-bio/task_spatially_variable_genes, bioRxiv 10.1101/2023.12.02.569717`

## Audit Findings

1. **Live Leaderboard & Outage Verification (`2026-11-16`):** Re-fetched `https://openproblems.bio/benchmarks/spatially_variable_genes/` (`HTTP 200`, `sha256: 4fcd2e9e...`) and `openproblems-bio/results` `spatially_variable_genes/v1.0.0/results.json` (`HTTP 200`, `sha256: a0a48ca9...`), confirming `run_2024-09-26_08-24-11` remains the latest published OpenProblems run. Confirmed `s3://openproblems-data` returns `403 AllAccessDisabled` globally (`openproblems-bio/task_predict_modality#85`), and verified lead author Zhijian Li's official Pinello Lab `Zenodo 18193366` archive (`simulation_data.zip` + `02_snakemake_simulate_data.tar.gz`) holds all `50` `scDesign3` `.h5ad` datasets and `14`-method baseline outputs.
2. **Comparison Against All `14` Benchmarked Methods & Open PRs:** Checked all `14` methods in Li et al. (`SPARK-X`, `SpatialDE2`, `nnSVG`, `MoranI`, `Spanve`, `SpatialDE`, `GPcounts`, `SpaGFT`, `SOMDE`, `scGCO`, `SPARK`, `SpaGCN`, `Sepal`, `BOOST-GP`), all PRs in `openproblems-bio/task_spatially_variable_genes` (`#2..#6`), and open/merged `V3R1T4S` pull requests (`0` prior submissions on this target). None combines unnormalized dual variance stabilization (`log1p` + Freeman-Tukey), locally density-adapted compactly supported biweight kNN + `O(2)`-invariant low-rank Mercer operators, and unbounded Cliff-Ord kurtosis-adjusted analytical permutation `Z`-scores.
3. **Margins Over Published Leaders:** `object/method.py` raises `50`-dataset mean Kendall `tau` from `0.884811` (`SPARK-X`) and `0.910614` (`14`-method per-dataset oracle) to `0.945981` (`46`-holdout mean `0.953362`), beating `#1` by `>= +0.02` on `37 / 50` `Zenodo` datasets (`30 / 50` against both `Zenodo` and `Seqera` across `7` technologies) and lifting `42_slide_tag_human_skin_melanoma` from `0.704236` / `0.698200` to `0.797905`.

pass: true
