# The published values this reproduction is compared with

p3 has no record table: the bar is the tolerance 0.01 m w.e. around MBM's own published test RMSEs.

- Source: https://github.com/khsjursen/ML_MB_Norway (status page), fetched 2026-11-08T17:30:39Z, HTTP 200,
  218592 bytes, page sha256 a5ba5d954cf4ad155294eeed1d09819ec168826ccbd519fd9367e2ded9c6b299 (the page itself is
  not shipped). Head commit on the page and in the GitHub API (fetched the same minute, HTTP 200):
  32d8175adab27963c6ca2766f2420f24cdb72a6b, 2025-10-08T14:15:56Z.
- Extracted values: src/3.1.1_ML_model_performance_test.ipynb at that commit (sha256
  b6226ca7ba52e5c42d3aad2d6bde514bce62c56c545c5f833b2d54d2010599ad), cell 36 output:
  - "Mass Balance Machine - Ba: RMSE=1.00, MSE=0.99, MAE=0.77, Bias=-0.01, R²=0.64, Count=1065"
  - "Mass Balance Machine - Bw: RMSE=0.59, MSE=0.35, MAE=0.46, Bias=-0.01, R²=0.66, Count=999"
  - "Mass Balance Machine - Bs: RMSE=0.70, MSE=0.49, MAE=0.54, Bias=0.04, R²=0.72, Count=1028"
- This package: 0.9962 / 0.5881 / 0.7001 (n 1065 / 999 / 1028), |diff| 0.0038 / 0.0019 / 0.0001.
