# Table record

Note added 2026-11-08: this is the 2026-11-07 17:40 run's record, kept as written. Its van der Meer et al. 2026
lines (the last two items) are superseded by `the-record-we-beat/record.md` and `panel/novelty.md`: the full text was
read on 2026-11-07 and is a Swiss Alps study with no Norway experiment. Its "1979-2019" should read 1980-2019
(Sjursen et al. 2025, Table E1).

- Status source: https://github.com/khsjursen/ML_MB_Norway, fetched again 2026-11-07T17:42:57Z, HTTP 200, saved as
  table/status_ML_MB_Norway.html, sha256 30dafd86b1ce916f9dc4ce4fd687a6a0940e00a86936bc8cf2877e0f4545c8c4
  (commitCount 403, unchanged). First fetch 2026-11-07T14:35:04Z, HTTP 200, sha256
  4e06c3be7a6a45e0445bc9550a0235573fc3a4b796ffd93a727d3d458b2f2cc9 (commitCount 403). No newer result posted than the
  paper; README points to ODINN-SciML/MassBalanceMachine as the successor.
- Published MBM test RMSEs (bank entry; notebook src/3.1.1_ML_model_performance_test.ipynb, sha256
  b6226ca7ba52e5c42d3aad2d6bde514bce62c56c545c5f833b2d54d2010599ad, cell 36 output, verbatim):
  "Mass Balance Machine - Ba: RMSE=1.00, MSE=0.99, MAE=0.77, Bias=-0.01, R²=0.64, Count=1065"
  "Mass Balance Machine - Bw: RMSE=0.59, MSE=0.35, MAE=0.46, Bias=-0.01, R²=0.66, Count=999"
  "Mass Balance Machine - Bs: RMSE=0.70, MSE=0.49, MAE=0.54, Bias=0.04, R²=0.72, Count=1028"
- Reproduced here from MBM's shipped model: Ba 0.9962, Bw 0.5881, Bs 0.7001 (baseline/output.txt).
- Temperature-index models in the same paper (notebook src/3.3_model_comparison_point.ipynb, sha256
  8d4ffd4fbebc1e4cac2d1b41a92c81ea23a81b793978d4d2541438dd147b91ec, fetched 2026-11-07T14:47:09Z, HTTP 200), test
  glaciers, sub-period 1979-2019 only (n=517 winter), calibrated with geodetic data that include the test glaciers:
  "OGGM - Bw: RMSE=0.82", "GloGEM - Bw: RMSE=0.65", "PyGEM - Bw: RMSE=0.87"; MBM on the same subset "Bw: RMSE=0.55".
- Last-24-month literature search (2026-11-07): no lower RMSE on these full test sets by a model without test-glacier
  observations was found. Opened: tc.copernicus.org/articles/19/5801/2025/ (and its discussion and relations pages),
  github.com/ODINN-SciML/MassBalanceMachine, EGU26-11039 and EGU26-20051 abstracts, tc.copernicus.org/articles/20/6045/2026/
  (GlaUnTI, a different 13-glacier test set). One source unread: the ESSOAr PDF of an LSTM-MBM preprint (HTTP 403; Swiss
  Alps per its search snippet).
- Also unread (HTTP 403 on its Wiley page, 2026-11-07 about 15:05Z, not retried and not fetched again):
  van der Meer et al. 2026, "Glacier mass balance modeling using a Long Short-Term Memory network", JGR Machine Learning
  and Computation, doi 10.1029/2026JH001250. Search snippets suggest it uses the same Norway data; whether it reports a
  full 14-test-glacier RMSE, or a small-model winter RMSE, is unknown here.
