# Baseline record (kit/RUN.md step 3c): the published evaluation reproduced

Source of the expected values: github.com/dwolffram/hospitalization-nowcast-hub-evaluation (main; repo pushed
2023-10-26T06:32:14Z), `data/scores/wis_national.csv` (sha256 78aeb28a...7c37), `wis_states.csv` (2cde62e4...4563),
`wis_age.csv` (88936f4c...e022): 31 cells of mean WIS (Wolffram et al. 2023, PLoS Comput Biol 19:e1011394, Fig 7).
Data: hub nowcast files for forecast dates 2021-11-22..2022-04-29 via the evaluation's released assembly
`data/submissions.csv.gz` (sha256 04608675de78ac9ff6f0dc731f6491819d31c372ee928647399988c0e571f8e1), verified
against the hub's own files (attempts/p3-reproduce/out/p3_provenance*.txt); truth = hub
`COVID-19_hospitalizations_preprocessed.csv` at commit 11c745322c055cfbd4f0c8f72241642a50aea399 (sha256
bdd34ddb31149d12d4276b02e12c9ac9df5ecc9c92911748516d16d61608d380). Metric: mean over quantile rows of
2 (1{y<q} - tau)(q - y), per model and level (national = DE 00+; states = 16 states 00+, ILM excluded; age = DE six
age groups, RKI excluded). Tolerance: 1% relative per cell (the criterion's own).

Command (from the run folder):

    python -I attempts/p3-reproduce/code/p3_reproduce.py . attempts/p3-reproduce/out

Captured output: attempts/p3-reproduce/out/p3_log.txt; table attempts/p3-reproduce/out/p3_ladder.csv; the S2 rows
are copied to baseline/p3_S2_vs_published.csv.

Result (copied from the output): S2 (published exclusion + repair rules) reproduces 31 of 31 cells within 1%;
28 cells agree to |relative difference| < 1e-9 (largest 2.2e-16); the 3 Epiforecasts cells differ by +1.03e-4
(national), +1.28e-5 (states), +6.7e-7 (age). Expected vs reproduced for the comparator the criterion names:
MeanEnsemble national 259.594450 vs 259.594450; states 22.186471 vs 22.186471; age 41.484004 vs 41.484004.
Without the rules: S0 25/31 within 1% (0 exact), S1 25/31 within 1% (23 exact).

Baseline status: reproduced (not unresolved).
