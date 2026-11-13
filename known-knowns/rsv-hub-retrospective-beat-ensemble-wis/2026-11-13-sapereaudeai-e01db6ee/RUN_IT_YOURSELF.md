# Run it yourself

From this folder, in a fresh shell, with Python 3 and pandas + pyarrow:

    sh verify-it-yourself/run_checks.sh

It downloads the 250 pinned hub files (about 128 MB) from
https://raw.githubusercontent.com/CDCgov/rsv-forecast-hub/e947ca8fe8d50a581a181e6aefacfe922ba95af5/ , the two
epi-hub-analysis score files from https://raw.githubusercontent.com/sarahmart/epi-hub-analysis/2294a6331e6317059b49b20da893a86b2f0751dd/
and the EpiBenchmark and tapestry files (URLs in verify-it-yourself/pinned_published2.txt), one GET at a time, into
.hub_cache/, .ext_cache/ and .ext2_cache/ (or set HUB=/path/to/the/hub/at/that/commit, EXT=/path/to/a/folder holding
scores.parquet and rsv_summary.csv, EXT2=/path/to/a/folder holding rsv25-26_complete-model-scores.parquet,
b2screen_leaderboard.csv, manifest.json, per-seed.csv and native-location-scores.csv). It checks every sha256,
recomputes every row's season-average WIS and MAE from the definition and compares them with object/p3_table.csv,
checks the four Supplementary Table 6 rows, rescores all 26,248 epi-hub-analysis rows with their truth values, all
11,648 EpiBenchmark rows (5 levels, truth = time-series as_of 2026-09-16), the 20 tapestry RSVHub-ensemble cells, the 4
tapestry hub-evaluation values and the tapestry google-comparison values (23 levels, truth = as_of 2026-09-02, with the
task rules stated in the-record-we-beat/published_scores_found.md). Expected last line: PASS. Time: mostly the
downloads; from local copies it took about 45-70 s on the contributor's laptop (2026-11-13).

To rebuild the object and its rule files (LF line endings on every platform):

    python -I how-we-built-it/code/p3_recompute.py <hub dir> out
    python -I how-we-built-it/code/p3_reconcile_k2.py <hub dir> <scores.parquet> <rsv_summary.csv> out/p3_reconcile_epi_hub_analysis.txt
    sha256sum out/* object/*

The reconciliation records in how-we-built-it/records/ are rebuilt by the scripts in how-we-built-it/code_reconcile/
(each takes the hub folder, the third-party file and an output path; see each script's usage line).
