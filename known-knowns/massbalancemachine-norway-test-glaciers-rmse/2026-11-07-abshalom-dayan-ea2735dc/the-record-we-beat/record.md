# The record we beat

- Status source: https://github.com/khsjursen/ML_MB_Norway
  - fetched 2026-11-08T15:13:39Z, HTTP 200, 218563 bytes, page sha256
    54afc81db061fa4907f816f530cfb01e1efc7df4c912dca0e5c1167cebdf7319 (403 commits; visible text identical to the
    2026-11-08T12:13:09Z reading). No newer result is posted.
  - earlier: fetched 2026-11-07T20:48:55Z, HTTP 200, page sha256 d647ec10a617be22dabdcd485cc03d4dddec40496cd88fd8dbe8c2066e8c0321
    (commitCount 403); fetched 2026-11-07T17:42:57Z, HTTP 200, page sha256 30dafd86b1ce916f9dc4ce4fd687a6a0940e00a86936bc8cf2877e0f4545c8c4
    (commitCount 403); fetched 2026-11-07T14:35:04Z, HTTP 200, sha256
    4e06c3be7a6a45e0445bc9550a0235573fc3a4b796ffd93a727d3d458b2f2cc9 (commitCount 403).
- Cell compared against: notebook src/3.1.1_ML_model_performance_test.ipynb, cell 36 output, verbatim:
  - "Mass Balance Machine - Ba: RMSE=1.00, MSE=0.99, MAE=0.77, Bias=-0.01, R²=0.64, Count=1065"
  - "Mass Balance Machine - Bw: RMSE=0.59, MSE=0.35, MAE=0.46, Bias=-0.01, R²=0.66, Count=999"
  - "Mass Balance Machine - Bs: RMSE=0.70, MSE=0.49, MAE=0.54, Bias=0.04, R²=0.72, Count=1028"
  - fetched https://raw.githubusercontent.com/khsjursen/ML_MB_Norway/main/src/3.1.1_ML_model_performance_test.ipynb
    at 2026-11-08T16:46:59Z, HTTP 200, 1888299 bytes, sha256
    b6226ca7ba52e5c42d3aad2d6bde514bce62c56c545c5f833b2d54d2010599ad (the same sha256 as the copy read on 2026-11-07).
- 1980-2019 subset, n=517; sub-period values do not set the bar (target card). Notebook
  src/3.3_model_comparison_point.ipynb, fetched raw from
  https://raw.githubusercontent.com/khsjursen/ML_MB_Norway/main/src/3.3_model_comparison_point.ipynb at
  2026-11-07T21:04:20Z, HTTP 200, sha256 8d4ffd4fbebc1e4cac2d1b41a92c81ea23a81b793978d4d2541438dd147b91ec, cell 51
  output, verbatim:
  - "Mass Balance Machine - Bw: RMSE=0.55, MSE=0.30, MAE=0.43, Bias=-0.05, R²=0.68, Count=517"
  - "GloGEM - Bw: RMSE=0.65, MSE=0.42, MAE=0.51, Bias=-0.35, R²=0.55, Count=517"
  - "OGGM - Bw: RMSE=0.82, MSE=0.68, MAE=0.63, Bias=0.26, R²=0.26, Count=517"
  - "PyGEM - Bw: RMSE=0.87, MSE=0.76, MAE=0.69, Bias=0.59, R²=0.17, Count=517"
  GloGEM, OGGM and PyGEM are calibrated on geodetic balances that include the test glaciers.
- Paper: https://tc.copernicus.org/articles/19/5801/2025/ (annual 1.00 and winter 0.59 m w.e. in its text).
