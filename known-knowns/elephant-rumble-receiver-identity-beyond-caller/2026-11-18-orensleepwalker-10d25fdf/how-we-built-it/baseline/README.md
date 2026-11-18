# Baseline record (kit step 3c)

Published baseline: Pardo et al. 2024 (Nature Ecology and Evolution 8:1353-1364), random forest predicting the receiver from the spectral features, 7-fold CV stratified by caller and receiver: 27.5% (bank statement; the paper's main result). Code source: Zenodo 10576772, file data/20240104_vocal_labeling_code_for_upload_revision1.R, section 10, MODEL 1 (ranger, 500 trees, mtry 6, min.node.size 1, replace FALSE, sample.fraction 0.6). Data: Dryad version 16, the n469 spectral file (sha256 in data/SHA256SUMS), 437 calls with Cert_ID_Bin == 1. Split: caller x receiver stratified 7 folds, 100 fresh draws (PREREG.md). Metric: share of calls whose predicted receiver equals Elicitor1_ID, averaged over draws.

Expected 0.275, tolerance 0.02 (partial win p3; set in PREREG.md before running).
Command: `WORKERS=4 python3 code/run_real.py` then `python3 code/summarize.py` (run folder; Python environment with numpy, pandas, scikit-learn).
Reproduced: mean 0.26954233409610984 over 100 draws (sd 0.00794), from output/summary.json, key mean.rf. Difference from 0.275: -0.0055, inside the tolerance.
The criterion's own baseline gate, the caller-habit rule, is computed on the same draws: 0.49224256292906177 (key mean.habit).
