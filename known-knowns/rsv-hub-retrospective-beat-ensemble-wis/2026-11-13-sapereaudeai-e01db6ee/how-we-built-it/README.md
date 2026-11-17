# How we built it (code and records)

- code/p3_recompute.py + code/wis.py: the recomputation (python -I code/p3_recompute.py <hub dir> <out dir>), where
  <hub dir> holds the files in inputs_pinned.tsv (CDCgov/rsv-forecast-hub at e947ca8fe8d50a581a181e6aefacfe922ba95af5).
  Output: p3_table.csv, p3_exclusions.txt, p3_era_subset.txt (object/). Text outputs are written with LF.
- code/p3_reconcile_k2.py: the reconciliation with the row-level scores of the arXiv 2605.16238 analysis repository.
- code_reconcile/: hubload.py (loader), epibench_reconcile.py, tapestry_reconcile.py, tapestry_ed_variants.py,
  tapestry_hubeval_reconcile.py, tapestry_google_reconcile.py, truth_revisions.py, count_uga_shared.py. Outputs in
  records/ (with arxiv_supp_table7.txt and zenodo_22988800_scan.txt, read from the arXiv HTML and the Zenodo zip).
- PREREG.md, PREREG.v2.md, PREREG.v3.md (the p3 object, frozen before the table was computed), PREREG.v4.md: run
  2026-11-13-0233. prereg_later_runs/: the readings and checks of runs 2026-11-13-0349 and 2026-11-13-0523.
- baseline/: kit step 3c, the reproduction of Supplementary Table 6 (reproduce_era_table.py with score_cdc.py and
  wis.py; outputs era_reproduction.txt and era_reproduction_rerun.txt). Its loader and aggregation are written
  separately, but its wis.py is byte-identical to code/wis.py.
- null test: every PREREG says "null_test: not needed because ..." (a recomputation, no search or chance claim).
